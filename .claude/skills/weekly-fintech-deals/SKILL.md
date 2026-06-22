---
name: weekly-fintech-deals
description: Build the weekly FinTech deals workbook. Use when the user asks to compile, research, or format the interesting FinTech M&A and fundraising deals for a given week (e.g. "run the weekly deals for the week ending Friday X", "skillify/redo the deals workbook"). Produces a two-tab Excel (M&A + Growth Capital Raises) with house-style target descriptions and links rendered as "Link".
---

# Weekly FinTech Deals Workbook

Compile the notable FinTech **M&A** and **growth fundraising** deals for a single week
and output a formatted two-tab Excel that matches the user's house style.

## Inputs
- **Target week** — always defined as **Saturday → Friday**, named by its ending Friday
  (e.g. "week ending Friday June 19, 2026" = deals announced 2026-06-13 through 2026-06-19).
- **Optional curated list** — the user may attach an Excel/list of deals they already
  picked (columns like Sector / Type / Link / Target). If provided, **use their list and
  their sector/type classifications as the source of truth** — only research the missing
  fields. If not provided, source the deals yourself (Step 1).

## Selection criteria
Include a deal only if ALL hold:
1. **FinTech.** Sector is one of the taxonomy below.
2. **In-window.** The deal was *announced* within the Sat→Fri window. Verify the date;
   exclude anything announced before or after, even by a day.
3. **Size ≥ $25M.** Equity round size, or M&A enterprise/deal value. If value is
   undisclosed but the deal is clearly notable, include it and leave value blank.
   Note any sub-$25M or borderline calls to the user rather than silently including them.
4. **Type:** M&A = acquisition / take-private / PE control buyout. Raise = equity
   growth/venture round (Seed–Series F, growth equity, strategic minority).

### Sector taxonomy
`Asset & Wealth Tech` · `Banking & Lending Tech` · `Capital Markets Tech` ·
`Corporate Financial Function` (CFO stack: spend, billing, treasury, accounting,
procurement, tax) · `Financial Info & Analytics` · `InsurTech` · `Payments` ·
`Real Estate & Mortgage Tech`. (Crypto/digital-asset infra maps into Capital Markets
Tech, Payments, or Financial Info & Analytics as fits.)

## Process

### 1. Source the deals (skip if user supplied a curated list)
Fan out web research (launch parallel background agents — one for M&A, one for raises).
Search press wires (BusinessWire, PRNewswire), company newsrooms, and fintech outlets
(Fintech Global, PYMNTS, TechCrunch, Axios, FF News, Finextra, Tearsheet). Require a
source URL per deal and verify the announcement date is in-window. Do not fabricate;
drop anything you can't confirm.

### 2. Research each deal's fields
For every deal gather: target (proper legal/brand casing), acquirer **or** lead
investor(s), HQ country, announcement date, EV/deal value (M&A) or amount + valuation
(raise), and a primary source URL. Capture EV/Revenue and EV/EBITDA **only if explicitly
disclosed** — otherwise leave blank (never invent multiples; most private deals don't
disclose them).

### 3. Write the target description
One concise noun-phrase line, matching this house style (see `description-style.md` for
the full example bank):
- Lead with a noun phrase: "Provider of…", "Platform that…", "Developer of…",
  "AI-powered …", "Digital banking provider …", "Agentic risk solution …".
- Specific and concrete (name the product, customer, or mechanism). No trailing period.
- ~15–30 words. Describe what they do, not the deal.

### 4. Build the workbook
Write the deals to a JSON file (schema in `build_workbook.py` header) and run:
```
python3 .claude/skills/weekly-fintech-deals/build_workbook.py deals.json "Weekly_Fintech_Deals_<weekEndingFriday>.xlsx"
```
This produces the two tabs with the exact headers, blue header row, filters, frozen
header, and the **Link column rendered as the word "Link" hyperlinked** to each source.

**Column headers (do not change):**
- M&A: `Sector | Target Country | Deal Type | Date | Target | Acquirer | EV ($M) | EV / Revenue | EV / EBITDA | Target Description | Link / Press Release`
- Raises: `Sector | Target Country | Date | Target | Lead Investor(s) | Amount ($M) | Valuation ($M) | EV / Revenue | EV / EBITDA | Target Description | Link / Press Release`

**Formatting conventions:**
- Date format `DD-Mmm-YY` (e.g. `19-Jun-26`).
- Dollar fields are plain numbers in $M (e.g. `2750`, `29.2`). Blank = undisclosed.
- Use proper company casing (e.g. `additiv`, `m3ter`, `nesto`, `EDGE Markets`).

### 5. Deliver
Send the file with SendUserFile, give a tight summary (counts per tab + headline deals),
and surface any judgment calls (borderline size, sector placement, undisclosed terms).
Then commit and push the workbook + JSON to the working branch.

## Reference
- `build_workbook.py` — the generator (JSON → formatted .xlsx).
- `description-style.md` — bank of approved target-description examples to imitate.
