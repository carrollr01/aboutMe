---
name: weekly-fintech-deals
description: Build the weekly FinTech deals workbook. Use when the user asks to compile, research, or format the FinTech M&A and fundraising deals for a given week (e.g. "run the weekly deals for the week ending Friday X"). Produces a two-tab Excel matching the firm's finalized-DB schema exactly ("All M&A (PE & Strategic)" + "Growth Capital Raises").
---

# Weekly FinTech Deals Workbook

Compile the week's FinTech **control M&A** and **growth equity raises** into a two-tab Excel
matching the finalized deal database (`weekly-deals/Finalized_Deals_History.xlsx` in the
repo — the canonical precedent for every rule below).

## The week
Saturday→Friday, named by ending Friday. A deal qualifies ONLY if its **announcement date**
(never the close/completion date) falls inside the window. Verify every date against a
primary source; exclude prior-week deals even when this week's roundups carry them.

## Inclusion rules (locked — learned from the finalized DB)
1. **FinTech only.** Must have a genuine tech / digital / money-movement / data core. The bar
   is low but real: exclude traditional FS with no tech angle (traditional MGAs/underwriters/
   carriers, pure RIA/advisory roll-ups, IT-services). Borderline targets (pawn+FX retail,
   HR-payroll, insurance holdco with tech layer): include, but the description must carry both
   the fintech angle AND the traditional business honestly.
2. **Credible source required.** Every deal needs at least one reasonably reputable outlet or
   primary release (wire, company newsroom, major trade press). No single-blog/unverifiable
   deals — drop them (this is why C2FO India was cut).
3. **Raises tab:** equity rounds **≥ $25M** (USD). Simultaneous combined tranches (e.g.
   seed+Series A announced together) count as one round at the combined total. **Minority /
   growth-equity investments belong HERE, not in M&A** (e.g. Carbon Underwriting/FTV).
   The floor is machine-enforced: `amount` must be a JSON **number ≥ 25** — a round whose
   total cannot be confirmed ≥ $25M cannot be entered at all; record it as an exclusion
   with its reason instead.
4. **M&A tab:** control transactions only, **no size floor** (small tuck-ins in).
   `Deal Type` is STRICTLY **"Strategic M&A"** or **"PE Buyout"** — zero temperature, no other
   strings (builder enforces). Adjacent deals (take-private by a strategic, JV-stake-to-100%,
   distressed purchase, carve-out) get snapped to the nearest of the two, with the nuance
   explained in the DESCRIPTION, not the type column.
   EXCLUDE from M&A: minority stakes (→ Raises), team/book/portfolio (asset) acquisitions,
   GP-led continuation vehicles / fund secondaries, and non-binding proposals/rumors.
5. **USD only.** Convert non-USD amounts at the announcement-date FX rate; note original
   currency in the description or Mults Basis if material.

## Sectors (exact labels)
Asset & Wealth Tech · Banking & Lending Tech · Capital Markets Tech · Corporate Financial
Function · Financial Info & Analytics · InsurTech · Payments · Real Estate & Mortgage Tech.
(Crypto/digital-asset infra maps into Capital Markets Tech, Payments, or Financial Info &
Analytics.)

## Financials
- Public targets: pull revenue/EBITDA from filings/press; compute EV/Revenue and EV/EBITDA on
  **true enterprise value** (equity value net of cash/debt). Don't default to "undisclosed."
- Private deals: compute multiples when deal value AND revenue/EBITDA are disclosed; mark
  bounds when revenue is a floor (">$200M").
- **Always record the basis**: `Mults Source` (outlet/filing used) and `Mults Basis` (e.g.
  "LTM FY25 rev, adj. EBITDA; EV net of $99M cash"). Numbers are honest-best-effort; the
  source/basis columns exist precisely so a better source can replace them later.
- Flow metrics (TPV, volume, AUM, GWP, deposits, payroll processed) are NEVER revenue.
- Undisclosed / not-applicable = **"-"** (never blank). Negative EBITDA → "n.m.".

## Output format (exact — builder enforces)
Tab 1 **"All M&A (PE & Strategic)"**:
`x | Week | Sector | Target Country | Deal Type | Date | Target | Acquirer | EV ($M) | EV / Revenue | EV / EBITDA | Target Description | Link / Press Release | Mults Source | Mults Basis | Public Deal | HL Deal | Seller`
Tab 2 **"Growth Capital Raises"**:
`x | Week | Sector | Target Country | Date | Target | Lead Investor(s) | Amount ($M) | Valuation ($M) | EV / Revenue | EV / EBITDA | Target Description | Link / Press Release`
- `Week` auto-derives from Date (ending Friday, DD-Mmm-YY). `x` left empty (user's flag col).
- Meta columns (Mults Source/Basis, Public Deal Y/N, HL Deal, Seller): populate what is
  publicly knowable (Seller from the release, Public Deal = listed target, HL Deal only if
  HL is named); "-" otherwise.
- Dates DD-Mmm-YY. Link cell shows "Link" hyperlinked. Rows ordered sector-alpha, then date.
- Build: `python3 .claude/skills/weekly-fintech-deals/build_workbook.py weekly-deals/inputs/deals_<endingFriday>.json "weekly-deals/outputs/Weekly_Fintech_Deals_<endingFriday>.xlsx"`
  (deals JSON lives in `weekly-deals/inputs/`, finished workbooks in `weekly-deals/outputs/`)
- Every build first runs `validate_deals.py` (locked rules: sectors, week window, deal-type
  enum, numeric ≥$25M raise floor, citation links) and refuses to write on any violation.
  Check a file early with `python3 .claude/skills/weekly-fintech-deals/validate_deals.py <json>`.

## Citation trace
Every deal carries `link` (required, http/https) plus optional `source` (outlet name;
derived from the link domain when absent) and `extra_links` (corroborating URLs). Each
successful build writes `weekly-deals/citations/citations_<YYYY-MM-DD>.json` — one entry
per deal (tab, target, date, source, link, mults source) plus the sha256 of the input
JSON. Commit the manifest with the outputs; it is the audit trail for every number in the
workbook. Manifests are builder-written only — never hand-edit them.

## Enforcement & guardrails (do not bypass)
- `validate_deals.py` is the single source of truth for the machine-checkable rules. It
  runs three ways: standalone CLI, inside every `build_workbook.py` run, and via the
  PostToolUse hook the moment a `weekly-deals/inputs/deals_*.json` is written.
- A PreToolUse hook (`.claude/hooks/deals_guard.py`, wired in `.claude/settings.json`)
  blocks in-session edits to the validator, builder, hooks, settings, and citation
  manifests. If a locked rule genuinely needs to change, the human owner disables the
  guard first (`/hooks`, or edit `.claude/settings.json` outside a session), makes the
  change, and re-enables it.
- Never respond to a validation failure by weakening or working around a check — fix the
  data, or record the deal as an exclusion with its reason in the delivery summary.

## Descriptions
Follow `description-style.md` (rewritten from the user's actual edits). Core: short,
product-first noun phrase; no "partnered with X across Y countries" padding; carry the
traditional angle for borderline names.

## Deliver
Send the file; summarize counts, headliners, computed multiples, borderline calls; ALWAYS
list notable exclusions with reasons (out-of-window / non-fintech / not-control / no credible
source) so the user can sanity-check. Commit and push.
