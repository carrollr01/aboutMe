# Building a FinTech Capital Markets Monitor
### Turning a weekly deal log into a longitudinal market-intelligence product

*Prepared June 2026 · FinTech Coverage*

---

## The problem

We capture excellent point-in-time data — a weekly deal log across eight coverage
subsectors and a biweekly public-comps tracker — but we treat each like a **balance
sheet**: produced, filed, never revisited. The value we leave on the table is the
**income statement**: the capital flows, multiple trends, and sector rotation that only
appear when you read the data *across time*.

We already hold hundreds of precedents and a running comps history in a single taxonomy.
That longitudinal record is a genuine proprietary asset — and the basis for becoming our
clients' source of truth on what fintech assets are worth and who is about to transact.

## The product — a FinTech Capital Markets Monitor (three layers)

- **The Tape** — quantitative trends: capital rotation by subsector, valuation multiples
  over time, and the spread between private marks and public comps (our best
  market-temperature gauge; widening private premiums signal late cycle, public-over-private
  signals coming down-rounds and take-privates).
- **The Narrative** — a stateful weekly report per subsector plus a cross-sector synthesis,
  organized around a living **Thesis Ledger** that tracks each market thesis as it forms,
  builds, becomes consensus, or breaks.
- **The Board** — origination intelligence: active acquirers, consolidation plays (serial
  buyers rolling up a space), and companies statistically "due" to raise or sell.

## Design principle (given our tooling)

> **Deterministic math stays in Excel. Language synthesis happens in NotebookLM/Gemini.
> Raw data never leaves OneDrive.**

LLMs are unreliable computing multiples across hundreds of rows, and our data cannot
natively reach the Google tools. So we compute exact numbers where the data already lives
(Excel/OneDrive) and push only **finished, shareable summaries** into NotebookLM and Agent
Builder for narration and querying. This keeps output defensible *and* keeps proprietary
data in-tenant.

## Toolchain mapping

| Layer | Built in | Notes |
|---|---|---|
| Data + Math (The Tape, The Board) | **Excel on OneDrive** | Where the data already lives; PivotTables are exact, compliant, no migration |
| Narrative + Thesis Ledger | **NotebookLM** | Grounded synthesis with citations over weekly logs + exported Tape summaries |
| Report drafting / persona | **Gemini** | Saved prompt (Gem if available) for a consistent house voice |
| Queryable corpus + automation | **Agent Builder** | Phase 3: a grounded "coverage analyst" agent over exported deal data |

## How it stays "stateful" without a database

Two mechanisms, because none of these tools remembers on its own:
1. **The corpus is the memory.** Each week we add the new deal log + Tape summary as
   NotebookLM sources; history accumulates and is never re-derived.
2. **The Thesis Ledger is one living document** that is both input and output. Each week
   NotebookLM reads the prior ledger, scores new deals against every open thesis
   (*confirm / contradict / new*), and we save the update back. **That ledger is the
   income statement, in prose.**

## Data hygiene — the one prerequisite

- A fixed schema on the deal log: `date · subsector · type · target · acquirer/lead ·
  geography · EV · amount · valuation · EV/Rev · EV/EBITDA · stage · theme_tags · source`.
- A controlled vocabulary for `subsector` (the eight) and `theme_tags`.
- **The comps tracker appended with a date stamp each cycle — never overwritten** — so the
  biweekly snapshots become a time series. *(If we have been overwriting, the trend clock
  starts now and we backfill what we can.)*

## Rollout

- **Phase 0 — Foundation (wk 1):** lock the schema in the Excel master; consolidate the
  historical deals; begin stamping comps snapshots.
- **Phase 1 — The Tape (wk 1–2):** Excel PivotTables for sector rotation, multiples-over-
  time, and the private–public spread. The immediate "we've had this the whole time" moment.
- **Phase 2 — The Narrative (wk 2–3):** stand up the NotebookLM notebook + a standing weekly
  prompt + the Thesis Ledger, and **pilot on InsurTech** (gradeable against the existing
  third-party benchmark). Optional: NotebookLM Audio Overview as a distributable briefing.
- **Phase 3 — The Board + Agent Builder:** origination pivots, then a grounded agent the
  coverage team can query in plain English ("every InsurTech deal above 5x revenue since 2024").

## Honest constraints & mitigations

- **OneDrive ↔ Google has no native connector** → one manual export/upload step per week.
  *Mitigation:* keep raw data and math in Excel; push only finished summaries across, so
  data movement is minimal and low-exposure.
- **Gemini basic has no code interpreter** → all computation in Excel (no loss; Excel is exact).
- **Agent Builder is retrieval, not a calculator** → it grounds aggregate queries best on
  structured data (BigQuery). Treat true "ask-the-numbers" as a Phase-3 stretch; Excel
  covers aggregates until then.

## To start

I need two things to finalize the build: the **deal-log column list** and the **comps-tracker
column list**, plus confirmation of whether comps history has been preserved or overwritten.
From there: the starter kit (schema, Tape pivot recipes, NotebookLM standing prompt, Thesis
Ledger + weekly report templates) and an InsurTech pilot.
