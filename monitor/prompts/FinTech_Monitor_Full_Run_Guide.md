# FinTech Monitor — Full Prompt Set & Run Guide
*One notebook. One corpus. Nine lenses → eight subsector narratives + one cross-sector synthesis.*

The InsurTech pilot validated the voice. This is the production design for the whole monitor.

---

## Architecture
- **One NotebookLM notebook: "FinTech Monitor."** Not one per subsector.
- **Sources (one corpus):**
  - the **weekly deal log** — the full workbook, all 8 subsectors (M&A + Raises tabs);
  - the **Tape Summary PDF** (rotation + forward multiples + spread);
  - the **master Thesis Ledger** (one doc, with a `Subsector` column incl. a `Cross-Sector` value);
  - rolling prior weekly reports (continuity) + the benchmark as a "voice reference."
- **Nine runs per week against that one notebook:**
  - **8 subsector prompts** (swap the subsector) → 8 narrative docs + ledger updates for that sector;
  - **1 synthesis prompt** → the flagship cross-sector doc + Cross-Sector ledger updates.
- Because the deal log is **tagged by `Sector`**, each subsector prompt just scopes the lens —
  no separate source files per sector.

---

## Prompt A — Subsector narrative (run 8×, swap `{{SUBSECTOR}}`)
```
You are the senior analyst for our FinTech coverage. Sources: the weekly deal log (all
subsectors), the Tape Summary, and the master Thesis Ledger.

SCOPE: consider ONLY deals tagged Sector = "{{SUBSECTOR}}" this period. Ignore other
subsectors except where a cross-sector tie is unavoidable — then note it in one line.

OUTPUT:
1) THESIS LEDGER UPDATE ({{SUBSECTOR}} rows only): for each open thesis mark CONFIRMS /
   CONTRADICTS / NEUTRAL with the specific deal cited and adjust confidence. Add a NEW thesis
   only with >=2 supporting datapoints; otherwise log a 1-datapoint "watch."
2) NARRATIVE (house voice): lead with this subsector's deal count + $ for the period, then the
   signal — not the press release. Every multiple/volume figure MUST come from the Tape Summary;
   if absent, write "[Tape: __]". Cite a source for every deal claim.
```
Run for each of: Asset & Wealth Tech · Banking & Lending Tech · Capital Markets Tech ·
Corporate Financial Function · Financial Info & Analytics · InsurTech · Payments ·
Real Estate & Mortgage Tech. (Skip a sector cleanly if it had no activity that week.)

## Prompt B — Cross-sector synthesis (run 1×, last)
```
You are the head of FinTech coverage writing the weekly cross-sector synthesis. Sources: the
full weekly deal log (all 8 subsectors), the Tape Summary, the master Thesis Ledger, and this
week's 8 subsector narratives.

OUTPUT:
1) HEADLINE: one line — "[N] deals across [k] subsectors. $[X]. [the one-sentence thesis]."
2) THE READ: the single most important cross-sector story this week.
3) THEMES IN >=2 SUBSECTORS: name each explicitly; list the subsectors + deals; mark
   emerging / building / consensus. Name at least one theme nobody has named yet.
4) CAPITAL ROTATION: where money moved between subsectors vs the trailing trend — cite the
   Tape rotation figures.
5) CROSS-SECTOR LEDGER UPDATE: the rows tagged Subsector = "Cross-Sector."
Anchor every quantitative claim to the Tape Summary; never estimate. Cite sources.
```

---

## Master Thesis Ledger (one doc, all sectors)
| # | Thesis | **Subsector** | Status | Conf. | Evidence For | Against | First seen | Updated | Client implication |
|---|---|---|---|---|---|---|---|---|---|
| … | … | Payments / … / **Cross-Sector** | emerging→consensus | | | | | | |

The `Cross-Sector` rows are the synthesis's domain (e.g., "stablecoin rails are becoming default
payment infrastructure" — shows up in Payments **and** Banking **and** Capital Markets).

---

## Weekly run order (≈30–45 min once warm)
1. **Excel:** finalize the week's deal log + refresh the Tape; export **Tape Summary PDF**.
2. **NotebookLM:** upload this week's deal log + Tape Summary to the FinTech Monitor notebook.
3. **Run Prompt A ×8** (one per subsector) → save 8 narrative docs; update ledger rows.
4. *(Optional, for tighter grounding:)* add the 8 narratives back as sources.
5. **Run Prompt B ×1** → the synthesis flagship; update Cross-Sector ledger rows.
6. Save everything to OneDrive; convert to Word; distribute.

**Outputs each week:** 8 subsector narratives + 1 synthesis + the updated master Thesis Ledger.

---

## Scale path (Agent Builder, later)
Once the manual nine-run loop is proven, an Agent Builder workflow can fan the weekly log out to
the 8 subsector prompts + synthesis automatically and write the drafts back — turning 45 minutes
into a review-and-polish step. Get the prompts right by hand first; automate the rote part second.
