# Archive — superseded iterations

Early versions of the weekly deals pipeline, kept for history. **Don't build on these.**
The current pipeline is `.claude/skills/weekly-fintech-deals/build_workbook.py` +
`weekly-deals/`.

- `build_xlsx.py`, `build_weekly_formatted.py`, `build_week_jun06_13.py` — one-off builder
  scripts with deal data hardcoded inline (pre-skill era). Their absolute paths still point
  at the old flat repo layout; left untouched intentionally.
- `fintech-acquisitions*.csv`, `fintech-growth-raises*.csv` — CSV exports from those scripts.
- `fintech-deals-*.xlsx`, `fintech-deals-verified.xlsx`, `Weekly_Fintech_Deals_formatted.xlsx`
  — early workbook formats before the schema was locked to the finalized DB.
- `fintech-ma-june-2026.md` — the first manual deal-research writeup (30 May – 7 Jun 2026)
  that seeded the inclusion rules.
