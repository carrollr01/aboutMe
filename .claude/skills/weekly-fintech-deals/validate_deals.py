#!/usr/bin/env python3
"""
validate_deals.py — single source of truth for the locked weekly-deals rules.

Consumed three ways (keep it that way — the machine-checkable rules live ONLY here):
  1. CLI:   python3 validate_deals.py weekly-deals/inputs/deals_<YYYY-MM-DD>.json
  2. build_workbook.py imports it — every build validates before writing anything,
     and the citation manifest is generated from the same parsed data.
  3. .claude/hooks/deals_guard.py (PostToolUse) runs the CLI whenever a deals
     input JSON is written, feeding violations straight back into the session.

Hard rules (CLI exits 1 / build refused on ANY violation):
  R1  Sector must be one of the 8 locked labels (both tabs).
  R2  M&A "deal_type" must be exactly "Strategic M&A" or "PE Buyout".
  R3  Dates parse as DD-Mmm-YY and every deal falls in ONE Sat->Fri week; when
      the filename is deals_YYYY-MM-DD.json that date must itself be a Friday
      and must be the ending Friday of every deal's week (announcement date).
  R4  Raise floor: "amount" must be a JSON NUMBER >= 25 (USD $M). Strings,
      "-", empty, or missing amounts are rejected — a round that cannot be
      confirmed >= $25M cannot be entered at all. Combined simultaneous
      tranches are one round at the combined total; if no credible outlet pegs
      the round total, the round is out (record it as an exclusion instead).
  R5  Citation trace: every deal needs an http(s) "link". Optional "source"
      (outlet name; derived from the link domain when absent) and
      "extra_links" (list of corroborating URLs) feed the citation manifest.
"""
import datetime
import hashlib
import json
import os
import re
import sys
from urllib.parse import urlparse

SECTORS = {
    "Asset & Wealth Tech",
    "Banking & Lending Tech",
    "Capital Markets Tech",
    "Corporate Financial Function",
    "Financial Info & Analytics",
    "InsurTech",
    "Payments",
    "Real Estate & Mortgage Tech",
}
ALLOWED_DEAL_TYPES = {"Strategic M&A", "PE Buyout"}
RAISE_FLOOR_USD_M = 25


def parse_date(s):
    """DD-Mmm-YY -> datetime.date, or None."""
    try:
        return datetime.datetime.strptime(str(s).strip(), "%d-%b-%y").date()
    except (ValueError, TypeError):
        return None


def ending_friday(d):
    return d + datetime.timedelta(days=(4 - d.weekday()) % 7)


def friday_from_filename(json_path):
    """deals_YYYY-MM-DD.json -> (date, error_or_None); (None, None) if unnamed."""
    if not json_path:
        return None, None
    m = re.search(r"deals_(\d{4}-\d{2}-\d{2})\.json$", os.path.basename(json_path))
    if not m:
        return None, None
    try:
        d = datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return None, f"filename week '{m.group(1)}' is not a valid date"
    if d.weekday() != 4:
        return None, f"filename week {d.isoformat()} is a {d.strftime('%A')}, not a Friday — name inputs by the ending Friday"
    return d, None


def _iter_deals(data):
    for tab, key in (("M&A", "ma"), ("Raises", "raises")):
        rows = data.get(key, [])
        if not isinstance(rows, list):
            continue
        for i, row in enumerate(rows, 1):
            yield tab, key, i, row


def validate(data, json_path=None):
    """Return a list of violation strings (empty = passes all locked rules)."""
    errors = []
    if not isinstance(data, dict):
        return ["top level must be a JSON object with 'ma' and 'raises' lists"]
    for key in ("ma", "raises"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"'{key}' must be a list")

    expected_friday, fname_err = friday_from_filename(json_path)
    if fname_err:
        errors.append(fname_err)

    fridays_seen = {}
    for tab, key, i, row in _iter_deals(data):
        if not isinstance(row, dict):
            errors.append(f"{tab} #{i}: entry must be an object")
            continue
        name = row.get("target") or f"#{i}"
        if not row.get("target"):
            errors.append(f"{tab} #{i}: 'target' is required")

        # R1 sector
        sector = row.get("sector")
        if sector not in SECTORS:
            errors.append(f"{tab} {name}: sector {sector!r} is not one of the 8 locked labels")

        # R2 deal type (M&A only)
        if key == "ma":
            dt = row.get("deal_type")
            if dt not in ALLOWED_DEAL_TYPES:
                errors.append(
                    f"M&A {name}: deal_type must be exactly 'Strategic M&A' or 'PE Buyout' "
                    f"(got {dt!r}); snap adjacent structures to the nearest and explain the "
                    f"nuance in the description"
                )

        # R3 date / week window
        d = parse_date(row.get("date"))
        if d is None:
            errors.append(f"{tab} {name}: date {row.get('date')!r} is not DD-Mmm-YY")
        else:
            fri = ending_friday(d)
            fridays_seen.setdefault(fri, []).append(f"{tab} {name}")
            if expected_friday and fri != expected_friday:
                errors.append(
                    f"{tab} {name}: announcement date {row.get('date')} belongs to the week "
                    f"ending {fri.strftime('%d-%b-%y')}, not the file's week "
                    f"({expected_friday.strftime('%d-%b-%y')}) — out-of-window deals are excluded"
                )

        # R4 raise floor (Raises only) — numeric or it does not go in
        if key == "raises":
            amount = row.get("amount")
            if isinstance(amount, bool) or not isinstance(amount, (int, float)):
                errors.append(
                    f"Raises {name}: 'amount' must be a JSON number in USD $M (got {amount!r}). "
                    f"The >=${RAISE_FLOOR_USD_M}M floor is locked: a round whose total cannot be "
                    f"confirmed >= ${RAISE_FLOOR_USD_M}M cannot be entered — list it as an "
                    f"exclusion instead"
                )
            elif amount < RAISE_FLOOR_USD_M:
                errors.append(
                    f"Raises {name}: amount ${amount}M is below the locked ${RAISE_FLOOR_USD_M}M "
                    f"floor and cannot be entered (combined simultaneous tranches count as one "
                    f"round at the combined total)"
                )

        # R5 citation
        link = row.get("link")
        if not (isinstance(link, str) and link.startswith(("http://", "https://"))):
            errors.append(f"{tab} {name}: a credible-source 'link' (http/https URL) is required for the citation trace")
        extra = row.get("extra_links", [])
        if extra and (not isinstance(extra, list) or any(
                not (isinstance(u, str) and u.startswith(("http://", "https://"))) for u in extra)):
            errors.append(f"{tab} {name}: 'extra_links' must be a list of http(s) URLs")

    if not expected_friday and len(fridays_seen) > 1:
        span = ", ".join(f.strftime("%d-%b-%y") for f in sorted(fridays_seen))
        errors.append(f"deals span multiple weeks (ending Fridays: {span}) — one file covers one Sat->Fri week")
    return errors


# ---------------------------------------------------------------- citations

def outlet_for(row):
    src = row.get("source")
    if isinstance(src, str) and src.strip():
        return src.strip()
    try:
        host = urlparse(row.get("link", "")).netloc.lower()
        return host[4:] if host.startswith("www.") else (host or "-")
    except ValueError:
        return "-"


def week_iso(data, json_path):
    d, _ = friday_from_filename(json_path)
    if d:
        return d.isoformat()
    for _, _, _, row in _iter_deals(data):
        pd = parse_date(row.get("date")) if isinstance(row, dict) else None
        if pd:
            return ending_friday(pd).isoformat()
    return "unknown"


def build_citation_manifest(data, json_path, workbook_path):
    """Full audit trail for a build: one entry per deal, plus input hash."""
    citations = []
    for tab, key, _, row in _iter_deals(data):
        if not isinstance(row, dict):
            continue
        entry = {
            "tab": "All M&A (PE & Strategic)" if key == "ma" else "Growth Capital Raises",
            "target": row.get("target", ""),
            "date": row.get("date", ""),
            "source": outlet_for(row),
            "link": row.get("link", ""),
        }
        if row.get("extra_links"):
            entry["extra_links"] = row["extra_links"]
        if key == "ma" and row.get("mults_source") not in (None, "", "-"):
            entry["mults_source"] = row["mults_source"]
        citations.append(entry)
    with open(json_path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    return {
        "week_ending": week_iso(data, json_path),
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "input": os.path.basename(json_path),
        "input_sha256": sha,
        "workbook": os.path.basename(workbook_path),
        "citation_count": len(citations),
        "citations": citations,
    }


def manifest_dir_for(workbook_path):
    """outputs/<wb>.xlsx -> sibling citations/; anywhere else -> <dir>/citations/."""
    out_dir = os.path.dirname(os.path.abspath(workbook_path))
    if os.path.basename(out_dir) == "outputs":
        return os.path.join(os.path.dirname(out_dir), "citations")
    return os.path.join(out_dir, "citations")


def main():
    if len(sys.argv) != 2:
        print("usage: validate_deals.py <deals.json>", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL: cannot read {path}: {e}", file=sys.stderr)
        sys.exit(1)
    errors = validate(data, path)
    if errors:
        print(f"FAIL: {len(errors)} locked-rule violation(s) in {path}:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    n_ma = len(data.get("ma", []))
    n_ra = len(data.get("raises", []))
    print(f"OK: {n_ma} M&A + {n_ra} raises pass all locked rules")


if __name__ == "__main__":
    main()
