# Starter Kit — FinTech Capital Markets Monitor
### Tailored to the actual Precedents + Public Comps schemas · Excel(OneDrive) → NotebookLM → Agent Builder

The golden rule again: **exact math in Excel (where the data already lives); language in
NotebookLM/Gemini; only finished summaries cross into Google.**

---

## PART A — Data layer (Excel on OneDrive)

### A1. Deals master — already done, two small additions
Your `All M&A (PE & Strategic)` and `Growth Capital Raises` tabs are the master deal DB and
already use the right schema. Add a few helper columns (cheap, high-leverage):

| New column | Tab | Purpose |
|---|---|---|
| `Quarter` | both | `=YEAR(Date)&"-Q"&ROUNDUP(MONTH(Date)/3,0)` — the time axis for every trend |
| `Stage` | Raises | Seed/A/B/C… (parse from description) — enables the stage-mix and "aging-raiser" views |
| `Investor/Acquirer (norm)` | both | one clean name per firm — enables the Board leaderboard (e.g., "a16z crypto" = "Andreessen Horowitz") |
| `Theme Tags` | both | controlled vocab (e.g., `stablecoin-rails`, `agentic-AI`, `embedded-insurance`) — enables theme tracking |

Then build **`Deals_All`** with **Power Query** (Data → Get Data → combine the two tabs):
add `DealType` = "M&A" / "Raise" and `Capital` = `EV ($M)` for M&A rows / `Amount ($M)` for
raises. One refreshable union table = the source for The Tape. (Power Query so it re-refreshes
each week with no rework.)

### A2. Comps history — the real build
1. **Consolidate** every historical CapIQ version into one long table **`Comps_History`** —
   one row per company *per snapshot*, with an added **`As-Of Date`** column. (Power Query
   "append/merge folder" can stack them automatically if the files share a layout.)
2. Add a **`Subsector` map tab**: `Ticker → Subsector` (your 8). VLOOKUP it into `Comps_History`.
   *Without this, none of the public-multiple trends are possible.*
3. Pick one **constant-horizon multiple** to trend so snapshots are comparable. Recommend
   **forward (CY+1) EV/Revenue** and **forward EV/EBITDA**: a helper that selects the column
   one year ahead of each snapshot's year, e.g.
   `=IF(YEAR(AsOf)=2025, [EV/Rev CY2026], IF(YEAR(AsOf)=2026, [EV/Rev CY2027], …))`.

### A3. CapIQ backfill protocol (do this once, early)
In the CapIQ plugin, step the as-of date to each **quarter-end from 31-Mar-2022 → present**
(~18 pulls), saving each as a snapshot into `Comps_History` with its `As-Of Date`. Result:
~4 years of subsector multiple history immediately — the spine of the whole product.

---

## PART B — The Tape (Excel recipes)

All of these read `Deals_All` and `Comps_History`. Use **Excel 365 dynamic arrays**
(`FILTER`/`MEDIAN`) so no Power Pivot is required. Define named ranges first.

**B1 · Sector Rotation** (PivotTable on `Deals_All`)
- Rows: `Sector` · Columns: `Quarter` · Values: `Sum of Capital` and `Count of Target`.
- Add a second pivot split by `DealType` to see M&A vs. primary capital separately.
- *Read:* where $ and deal-count are entering/leaving each subsector over time.

**B2 · Private multiples over time** (sparse — disclosed deals only)
```
=IFERROR(MEDIAN(FILTER(MA_EVRev,(MA_Sector=$A2)*(YEAR(MA_Date)=B$1)*(MA_EVRev<>""))),"")
```
Grid: rows = Sector, cols = Year. (EV/Rev is blank on most deals, so treat private points as
an *overlay*, not a dense series.)

**B3 · Public multiples over time** (dense — the star series)
```
=IFERROR(MEDIAN(FILTER(C_EVRevFwd,(C_Subsector=$A2)*(C_AsOf=B$1)*(C_EVRevFwd<>""))),"")
```
Grid: rows = Subsector, cols = `As-Of Date`. Repeat for forward EV/EBITDA, and for the
quartiles using `PERCENTILE(FILTER(...),0.25/0.75)` to plot a band, not just a median.

**B4 · Private–Public Spread** (flagship metric)
For each Sector × period: `private median EV/Rev (B2) − public median EV/Rev (B3)`.
- Positive/widening → private marks running hot (late-cycle; down-round risk ahead).
- Negative → public trades above last private marks (expect take-privates / structured rounds).

**B5 · Quality & sentiment overlays** (from comps KPIs)
- Median **Rule of 40** and **YoY Revenue Growth** by Subsector by As-Of Date (the columns are
  already in the comps tab) → is the re-rating earned by fundamentals or just multiple?
- Decompose value change = *multiple Δ* vs *estimate Δ* across snapshots (the valuation bridge).

**Output:** a one-page **"Tape Summary"** (the B1/B3/B4 tables + 2–3 charts). Export to **PDF
each cycle** — this is the only quantitative artifact that crosses into NotebookLM.

---

## PART C — The Narrative (NotebookLM)

### C1 · Notebook & sources
One **master notebook**. Sources to upload (convert Excel/Word → PDF or Google Doc first):
- every **weekly deal log** (the workbooks we build),
- the latest **Tape Summary PDF**,
- the **Thesis Ledger** doc,
- prior **weekly reports** (so it speaks in continuity).
If a subsector gets noisy, spin a focused child notebook for it.

### C2 · Standing weekly prompt (paste this each week, after adding the week's sources)
```
You are the senior analyst for our FinTech coverage group. Sources: this week's deal log,
the current Tape Summary, the Thesis Ledger, and all prior weekly reports.

1. THESIS LEDGER UPDATE. For every open thesis, classify this week's deals as CONFIRMS /
   CONTRADICTS / NEUTRAL, cite the specific deal(s), and adjust the confidence. Propose any
   NEW thesis only if ≥2 datapoints support it. Output the revised ledger table.
2. SUBSECTOR NARRATIVES. For each subsector with activity, 2–4 sentences: what happened, how
   it fits the trailing trend (cite a Tape number), and the "so what" for clients.
3. SYNTHESIS. One cross-sector read. Explicitly name any theme appearing in ≥2 subsectors
   that has not yet been named. Anchor every quantitative claim to the Tape Summary; never
   estimate a multiple yourself. Cite sources for every claim.
```

### C3 · Thesis Ledger template (one living Google Doc / Word file)
| Thesis | Subsector | Status | Confidence | Evidence For | Evidence Against | First seen | Last updated | Client implication |
|---|---|---|---|---|---|---|---|---|
| e.g. "Stablecoin rails are becoming table-stakes payments infra" | Payments | Building | Med | Trace, Flutterwave/Ripple… | — | Jun-26 | Jun-26 | Pitch infra targets to acquirers |

### C4 · Weekly report template (house voice, modeled on the benchmark)
```
[Subsector] Investment Report — Week of [dates]
[N] deals. $[X] deployed. [One-line hook — the surprising signal / the trend nobody named.]

— Thesis in focus: [named thesis + status change this week]
— The deals: [each deal, one line, with the angle not the press release]
— What it means: [the forward read, anchored to a Tape number]
Tags: [coverage tags]
```

---

## PART D — Gemini report-writer persona (Gem or saved prompt)
```
You write FinTech deal commentary in a terse, thesis-driven, senior-banker voice. Lead with
a number and a provocation. No hype, no adjectives without evidence. Every claim ties to a
deal or a provided figure. You never compute multiples — you are given them. Output matches
the weekly report template exactly.
```
Use Gemini to polish/format the NotebookLM draft and to spin alternate formats (email blast,
MD one-pager). Keep the *grounded* work in NotebookLM.

---

## PART E — Phase 3: Agent Builder (later)
Export `Deals_All` → CSV/JSONL → upload to a Cloud Storage bucket → build a Vertex Agent
Builder **data store** → a grounded "Coverage Analyst" agent the team queries in plain English
("every InsurTech deal above 5x revenue since 2024"). For true aggregate queries, ground on
**BigQuery** instead of files. This is the scale + self-serve layer once the manual loop works.

---

## PART F — Weekly operating cadence
1. **Excel (OneDrive):** add the week's deals to the master tabs; refresh `Deals_All`; refresh the Tape; export **Tape Summary PDF**.
2. **(Biweekly) CapIQ:** pull the new comps snapshot → append to `Comps_History` with `As-Of Date`.
3. **NotebookLM:** upload the week's deal log + Tape Summary; run the standing prompt; save the updated Thesis Ledger and the reports back to OneDrive.
4. **Gemini:** polish/format for distribution.

The only cross-the-wall step is uploading two PDFs to NotebookLM — minimal data movement, no raw rows exposed.

---

## Do-first checklist (this week)
- [ ] Add `Ticker → Subsector` map tab to the comps file.
- [ ] Add `As-Of Date` to historical comps versions; stack into `Comps_History` (Power Query).
- [ ] Run the **CapIQ quarter-end backfill** (2022→present).
- [ ] Add `Quarter` + `Capital` + `DealType`; build `Deals_All` (Power Query).
- [ ] Build B1 + B3 + B4; export the first **Tape Summary**.
- [ ] Stand up the NotebookLM notebook; seed the **InsurTech** pilot against the existing benchmark.
