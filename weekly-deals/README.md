# Weekly deals

The weekly FinTech deal-tracking workstream.

- `Finalized_Deals_History.xlsx` — the canonical precedent DB (650+ curated deals). Source of
  truth for the schema, the inclusion rules, and the description style. New weekly rows get
  finalized into it.
- `inputs/` — `deals_<endingFriday>.json` files fed to the builder. Validated on write by
  the repo's PostToolUse hook, and again by every build.
- `outputs/` — finished `Weekly_Fintech_Deals_<endingFriday>.xlsx` workbooks
  (`_financials` variants carry the multiples-enrichment pass).
- `citations/` — per-week citation manifests auto-written by the builder: one entry per
  deal (source outlet + link) plus the sha256 of the input JSON. Builder-generated only;
  hand edits are blocked by the repo hook.

Rules and builder live in `.claude/skills/weekly-fintech-deals/`; the run is kicked off with
the root `WEEKLY_DEALS_PROMPT.md`. `validate_deals.py` there is the single source of truth
for the locked rules (8 sector labels, one Sat→Fri week, strict deal-type enum, numeric
≥$25M raise floor, required citation links); `.claude/hooks/deals_guard.py` wires it into
every session and locks the enforcement files themselves against in-session edits.

Build command:

```
python3 .claude/skills/weekly-fintech-deals/build_workbook.py \
    weekly-deals/inputs/deals_<endingFriday>.json \
    "weekly-deals/outputs/Weekly_Fintech_Deals_<endingFriday>.xlsx"
```
