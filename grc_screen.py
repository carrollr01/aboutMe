#!/usr/bin/env python3
"""
GRC screening tool.

Runs over a list of companies and decides, STRICTLY, whether each one fits the
Governance / Risk / Compliance space -- specifically: risk, compliance, AML,
fraud, KYC, regulatory / GRC.

"Strict" means: a company is only a FIT if governance/risk/compliance is its
CORE business -- i.e. it sells risk/compliance/AML/fraud/KYC/regulatory
software or services as the primary product. It is NOT enough that the company
*has* a compliance feature, runs AML/KYC as a back-office step, or produces
regulatory reports as a by-product of some other product (fund admin,
investment accounting, trading tech, CRM, data, planning, etc.). Those are
marked ADJACENT, not FIT.

Usage:
    python3 grc_screen.py                 # console report + CSV
    python3 grc_screen.py --json          # machine-readable JSON to stdout
    python3 grc_screen.py --only-fit      # print only the FIT companies
    python3 grc_screen.py --data x.json   # use an alternate dataset

The dataset (companies.json) holds an honest one-paragraph business
description per company. The verdict is derived from that text -- so to
re-screen new companies you only edit the data, not the logic.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ---------------------------------------------------------------------------
# GRC lexicon -- the categories the user asked about.
# Each category maps to the phrases that count as evidence of that category.
# ---------------------------------------------------------------------------
GRC_CATEGORIES: dict[str, list[str]] = {
    "compliance": [
        "compliance", "regulatory", "regulation", "mar ", "market abuse",
        "market surveillance", "surveillance", "suitability", "disclosure",
        "regulatory reporting", "regtech",
    ],
    "risk": [
        "risk management", "risk monitoring", "enterprise risk", "credit risk",
        "operational risk", "risk analytics", "risk assessment",
    ],
    "aml": [
        "aml", "anti-money laundering", "money laundering", "sanctions",
        "transaction monitoring", "financial crime",
    ],
    "kyc": [
        "kyc", "know your customer", "know-your-customer", "cdd",
        "customer due diligence", "investor due diligence", "onboarding due diligence",
    ],
    "fraud": [
        "fraud", "fraud detection", "fraud prevention",
    ],
    "governance": [
        "governance", "oversight", "director services", "board services",
        "fiduciary", "manco", "aifm", "management company",
    ],
}

# Phrases that signal GRC is the CORE offering (not an incidental feature).
# A FIT requires at least one of these to be present in the description.
CORE_SIGNALS: list[str] = [
    "core business is regulatory compliance",
    "core service offering",
    "governance, risk and compliance is the core",
    "regtech",
    "market surveillance",
    "market abuse",
    "compliance is a named service line",
    "regulatory compliance, risk management, oversight",
]

# Phrases that explicitly demote a match to ADJACENT: they say GRC is present
# but secondary ("part of", "embedded in", "by-product", "back-office step").
DEMOTERS: list[str] = [
    "part of administration",
    "as part of",
    "embedded in",
    "but core is",
    "but it is",
    "not a dedicated",
    "not a compliance",
    "not standalone",
    "by-product",
    "adjacent",
    "incidental",
    "within a trading platform",
    "within a broader",
    "sits within",
]


@dataclass
class Verdict:
    name: str
    aka: str
    primary_domain: str
    verdict: str                     # FIT | ADJACENT | NO
    matched_categories: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    rationale: str = ""


def _find_hits(text: str, phrases: list[str]) -> list[str]:
    hits = []
    low = text.lower()
    for p in phrases:
        # word-ish boundary match so "aml" doesn't fire inside "amalgamate"
        pat = r"(?<![a-z])" + re.escape(p.strip().lower()) + r"(?![a-z])"
        if re.search(pat, low):
            hits.append(p.strip())
    return hits


def screen_company(c: dict) -> Verdict:
    text = f"{c.get('primary_domain','')} {c.get('description','')}"
    low = text.lower()

    matched_categories: list[str] = []
    evidence: list[str] = []
    for cat, phrases in GRC_CATEGORIES.items():
        hits = _find_hits(text, phrases)
        if hits:
            matched_categories.append(cat)
            evidence.extend(f"{cat}: {h}" for h in hits)

    has_core_signal = any(s in low for s in CORE_SIGNALS)
    has_demoter = any(d in low for d in DEMOTERS)

    # --- strict decision logic -------------------------------------------
    if not matched_categories:
        verdict = "NO"
        rationale = "No risk/compliance/AML/KYC/fraud/governance terms in core business."
    elif has_core_signal and not has_demoter:
        verdict = "FIT"
        rationale = "GRC is the core offering (core/RegTech/surveillance/governance signal present, no demotion)."
    elif has_core_signal and has_demoter:
        # Core signal exists but text also says it's secondary -> judge which wins.
        # Treat market-surveillance / dedicated RegTech as a genuine (partial) line.
        if any(s in low for s in ("market surveillance", "market abuse", "regtech")):
            verdict = "FIT"
            rationale = "Has a genuine dedicated RegTech / surveillance product line (partial-core), even if a larger non-GRC business exists."
        else:
            verdict = "ADJACENT"
            rationale = "GRC present but described as secondary to a non-GRC core business."
    else:
        verdict = "ADJACENT"
        rationale = "GRC terms appear only as a feature/back-office step, not the core business -- excluded under strict screening."

    return Verdict(
        name=c.get("name", ""),
        aka=c.get("aka", ""),
        primary_domain=c.get("primary_domain", ""),
        verdict=verdict,
        matched_categories=matched_categories,
        evidence=evidence,
        rationale=rationale,
    )


def load_companies(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_csv(verdicts: list[Verdict], out: Path) -> None:
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["company", "aka", "primary_domain", "verdict",
                    "matched_categories", "evidence", "rationale"])
        for v in verdicts:
            w.writerow([
                v.name, v.aka, v.primary_domain, v.verdict,
                "; ".join(v.matched_categories),
                "; ".join(v.evidence),
                v.rationale,
            ])


VERDICT_ORDER = {"FIT": 0, "ADJACENT": 1, "NO": 2}
BADGE = {"FIT": "[FIT]     ", "ADJACENT": "[ADJACENT]", "NO": "[NO]      "}


def print_report(verdicts: list[Verdict], only_fit: bool = False) -> None:
    ordered = sorted(verdicts, key=lambda v: (VERDICT_ORDER[v.verdict], v.name.lower()))
    counts = {"FIT": 0, "ADJACENT": 0, "NO": 0}
    for v in verdicts:
        counts[v.verdict] += 1

    print("=" * 78)
    print("GRC SCREENING  (strict)  -- risk / compliance / AML / fraud / KYC / governance")
    print("=" * 78)
    for v in ordered:
        if only_fit and v.verdict != "FIT":
            continue
        cats = ", ".join(v.matched_categories) if v.matched_categories else "-"
        print(f"{BADGE[v.verdict]}  {v.name}")
        print(f"             domain : {v.primary_domain}")
        print(f"             matched: {cats}")
        print(f"             why    : {v.rationale}")
        print("-" * 78)

    print(f"SUMMARY:  FIT={counts['FIT']}   ADJACENT={counts['ADJACENT']}   NO={counts['NO']}"
          f"   (total {len(verdicts)})")
    fits = [v.name for v in ordered if v.verdict == "FIT"]
    adj = [v.name for v in ordered if v.verdict == "ADJACENT"]
    print(f"STRICT FIT     : {', '.join(fits) if fits else '(none)'}")
    print(f"ADJACENT (near): {', '.join(adj) if adj else '(none)'}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Strict GRC company screener.")
    ap.add_argument("--data", default="companies.json", help="path to companies JSON")
    ap.add_argument("--csv", default="grc_screening_results.csv", help="CSV output path")
    ap.add_argument("--json", action="store_true", help="emit JSON to stdout instead of a report")
    ap.add_argument("--only-fit", action="store_true", help="report only strict FIT companies")
    ap.add_argument("--no-csv", action="store_true", help="do not write the CSV file")
    args = ap.parse_args(argv)

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"error: dataset not found: {data_path}", file=sys.stderr)
        return 2

    companies = load_companies(data_path)
    verdicts = [screen_company(c) for c in companies]

    if args.json:
        print(json.dumps([asdict(v) for v in verdicts], indent=2))
        return 0

    print_report(verdicts, only_fit=args.only_fit)

    if not args.no_csv:
        out = Path(args.csv)
        write_csv(verdicts, out)
        print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
