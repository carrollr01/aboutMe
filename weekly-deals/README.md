# Weekly deals

The weekly FinTech deal-tracking workstream.

- `Finalized_Deals_History.xlsx` — the canonical precedent DB (650+ curated deals). Source of
  truth for the schema, the inclusion rules, and the description style. New weekly rows get
  finalized into it.
- `inputs/` — `deals_<endingFriday>.json` files fed to the builder.
- `outputs/` — finished `Weekly_Fintech_Deals_<endingFriday>.xlsx` workbooks
  (`_financials` variants carry the multiples-enrichment pass).

Rules and builder live in `.claude/skills/weekly-fintech-deals/`; the run is kicked off with
the root `WEEKLY_DEALS_PROMPT.md`.

Build command:

```
python3 .claude/skills/weekly-fintech-deals/build_workbook.py \
    weekly-deals/inputs/deals_<endingFriday>.json \
    "weekly-deals/outputs/Weekly_Fintech_Deals_<endingFriday>.xlsx"
```
