#!/usr/bin/env python3
"""
GRC fit RANKING / scoring test.

Where grc_screen.py answers a binary "is this GRC, yes/no", this scores each
candidate 0-100 on how strong a GRC fit it is and ranks them, so you can pull
the best N of a batch.

It is a transparent rubric, computed from structured attributes in
grc_candidates.json -- not a black box. The four scored components:

  core   (0-40)  Is governance/risk/compliance the CORE business?
                   pure=40, core_adjacent=26, line=12, none=0
  domains(0-30)  Breadth & weight of GRC domains covered (financial-crime and
                   enterprise-GRC domains weigh more than EHS/quality).
  type   (0-20)  Delivery model: platform > intelligence > service >
                   consultancy > tool.
  fin    (0-10)  Relevance to the financial risk/compliance/AML/fraud/KYC theme:
                   financial-crime focus=10, financial-services focus=6, else 0.

Usage:
  python3 grc_rank.py                # ranked table + CSV
  python3 grc_rank.py --top 18       # mark/keep the best 18
  python3 grc_rank.py --json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

CORE_POINTS = {"pure": 40, "core_adjacent": 26, "line": 12, "none": 0}

TYPE_POINTS = {
    "platform": 20,
    "intelligence": 17,
    "service": 14,
    "consultancy": 11,
    "tool": 5,
}

# Domain weights -- the user's theme is risk / compliance / AML / fraud / KYC,
# so financial-crime and enterprise-GRC domains are weighted above EHS/quality.
DOMAIN_WEIGHTS = {
    "aml": 6, "kyc": 6, "fraud": 6,
    "sanctions": 5, "regulatory": 5, "compliance": 5, "risk": 5,
    "audit": 5, "governance": 5, "third_party_risk": 5,
    "resilience": 4, "supply_chain_risk": 4,
    "policy": 3, "ehs": 3, "quality": 2,
}
DOMAIN_CAP = 30

FIN_POINTS = {"crime": 10, "fs": 6, "none": 0}


@dataclass
class Score:
    name: str
    total: int
    core: int
    domains: int
    type: int
    fin: int
    domain_list: list[str] = field(default_factory=list)
    description: str = ""


def score_company(c: dict) -> Score:
    core = CORE_POINTS.get(c.get("core", "none"), 0)
    dom_raw = sum(DOMAIN_WEIGHTS.get(d, 0) for d in c.get("domains", []))
    domains = min(dom_raw, DOMAIN_CAP)
    typ = TYPE_POINTS.get(c.get("type", "tool"), 0)
    fin = FIN_POINTS.get(c.get("fin_context", "none"), 0)
    total = core + domains + typ + fin
    return Score(
        name=c.get("name", ""),
        total=total, core=core, domains=domains, type=typ, fin=fin,
        domain_list=c.get("domains", []),
        description=c.get("description", ""),
    )


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_csv(scores: list[Score], out: Path, top: int | None) -> None:
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "company", "score", "core", "domains", "type",
                    "fin", "in_top", "domain_list", "description"])
        for i, s in enumerate(scores, 1):
            w.writerow([i, s.name, s.total, s.core, s.domains, s.type, s.fin,
                        "Y" if (top and i <= top) else "",
                        "; ".join(s.domain_list), s.description])


def tier(score: int) -> str:
    if score >= 80:
        return "A  pure-play GRC"
    if score >= 65:
        return "B  strong fit"
    if score >= 50:
        return "C  solid / adjacent"
    if score >= 35:
        return "D  niche / partial"
    return "E  weak / out"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Score & rank companies on GRC fit.")
    ap.add_argument("--data", default="grc_candidates.json")
    ap.add_argument("--csv", default="grc_ranking_results.csv")
    ap.add_argument("--top", type=int, default=18, help="size of the shortlist to mark")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-csv", action="store_true")
    args = ap.parse_args(argv)

    path = Path(args.data)
    if not path.exists():
        print(f"error: dataset not found: {path}", file=sys.stderr)
        return 2

    scores = sorted((score_company(c) for c in load(path)),
                    key=lambda s: (-s.total, s.name.lower()))

    if args.json:
        print(json.dumps([asdict(s) for s in scores], indent=2))
        return 0

    print("=" * 84)
    print("GRC FIT RANKING  (0-100)   core(40) + domains(30) + type(20) + fin-theme(10)")
    print("=" * 84)
    print(f"{'#':>2}  {'score':>5}  {'core':>4} {'dom':>3} {'typ':>3} {'fin':>3}  company")
    print("-" * 84)
    for i, s in enumerate(scores, 1):
        cut = "  <== top %d" % args.top if i == args.top else ""
        star = "*" if i <= args.top else " "
        print(f"{i:>2}{star} {s.total:>5}  {s.core:>4} {s.domains:>3} "
              f"{s.type:>3} {s.fin:>3}  {s.name}{cut}")
    print("-" * 84)
    shortlist = [s.name for s in scores[:args.top]]
    print(f"BEST {args.top}: {', '.join(shortlist)}")
    print(f"BELOW CUT: {', '.join(s.name for s in scores[args.top:]) or '(none)'}")

    if not args.no_csv:
        out = Path(args.csv)
        write_csv(scores, out, args.top)
        print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
