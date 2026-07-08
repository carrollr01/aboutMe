# Tape Phase 2 — Comps Backfill & Multiples (detailed)

## Setup (one-time)
1. Paste *All M&A* tab -> `M&A` (A:K); *Growth Capital Raises* -> `Raises` (A:K).
2. `Subsector Map` is pre-filled (293 tickers) — nothing to do.

## Comps backfill — per quarter-end snapshot
Start with the last 3-4 quarters to confirm it works, then do the full back-history.
1. CapIQ Comps Detail tab: set date cell **D3** to a quarter-end (start recent, e.g. 31-Mar-2026). Let it recalc.
2. Select the data block: Display Name ... Gross Margin, all company rows (data starts ~row 12).
3. Copy.
4. Tape `Comps` sheet -> first empty cell in **column B** -> **Paste Special > Values** (Ctrl+Alt+V, V, Enter). VALUES ONLY.
5. Column A: type the quarter-end date by the first pasted row, select down the block, Fill Down (Ctrl+D).
6. Columns AY-BC auto-compute: Subsector, FwdRev, Fwd EV/Rev, FwdEBITDA, Fwd EV/EBITDA.
7. Move D3 to the next quarter-end (31-Dec-2025, 30-Sep-2025, ... back to 31-Mar-2022); recalc; paste-values at the next empty row; stamp the date. Repeat.

## Multiples
8. `Multiples` sheet: put snapshot dates in B4, C4, D4, ... as REAL dates matching the As-Of dates in Comps col A.
9. Top grid = median forward EV/Revenue by subsector by snapshot (public). Bottom grid = private (your deals). Difference = spread.

## Verify (after first snapshot)
- Comps col AY shows a sector and BA shows a number -> working.
- Put that date in Multiples!B4 -> column fills.

## Likely snags
- TICKER FORMAT: map uses `NASDAQ:SSNC`. If your Ticker column is plain `SSNC`, AY is blank -> tell me, I'll reformat the map.
- Always Paste Special > Values (CapIQ cells are live formulas).
- Dates must be real dates (col A and Multiples row 4), not text.
- MEDIAN(IF()) is an array formula: Excel 365 handles it; older Excel needs Ctrl+Shift+Enter.
