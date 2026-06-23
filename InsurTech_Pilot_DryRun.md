# InsurTech Pilot — NotebookLM Dry Run

**Purpose:** a concrete first run of the narrative engine, scoped to InsurTech, so you can
react to real output before pointing it at the full database. Built from the InsurTech deals
we've already verified this session. *Illustrative:* on the real run, NotebookLM produces this
grounded in your corpus with inline citations, and the theses get richer against hundreds of
precedents. The one thing it must NOT invent — multiples/volumes — is shown as a `[Tape: …]`
slot that you fill from the Excel Tape Summary.

---

## 1. NotebookLM source list (upload for the InsurTech pilot)
- Weekly deal logs covering the period (the workbooks we built: wk-ending-Jun-12, wk-ending-Jun-19).
- The **Tape Summary PDF** (even a stub: InsurTech rotation + forward-multiple line).
- The **Thesis Ledger** doc (starts empty; this run seeds it).
- The benchmark report(s) you pasted — as a *style* source, labeled "voice reference, not data."

## 2. Standing prompt (InsurTech-scoped — paste after uploading)
```
You are the senior analyst for our InsurTech coverage. Sources: the weekly deal logs, the
Tape Summary, the Thesis Ledger, and the voice-reference report.
1. THESIS LEDGER UPDATE: for every open thesis, mark this period's deals CONFIRMS / CONTRADICTS
   / NEUTRAL with the specific deal cited, and adjust confidence. Add a NEW thesis only with ≥2
   supporting datapoints OR flag a 1-datapoint "watch." Output the revised ledger table.
2. NARRATIVE: a thesis-driven brief in the voice-reference style — lead with deal count + $,
   then the signal. Every multiple/volume claim must come from the Tape Summary; if absent,
   write "[Tape: __]". Cite a source for every deal claim.
```

---

## 3. Worked output (what the run returns)

### 3a. Thesis Ledger — after this run
| # | Thesis | Status | Conf. | Evidence For | Against | First seen | Updated | Client implication |
|---|---|---|---|---|---|---|---|---|
| 1 | AI is moving into insurance **operations/back-office**, not just distribution | Building | Med-High | Poetic ($50M, Jun 10); Trussed AI (Nassau, Jun 17); Braven ($4.6M, Jun 16) | — | Jun-12 wk | Jun-19 wk | Source AI-ops & governance targets to carriers/MGAs |
| 2 | **AI-native agencies are rolling up distribution books** with primary capital | Emerging | Med | Connie Health ($40M B + 10th acquisition, Clearlink Medicare, Jun 18) | single name | Jun-19 wk | Jun-19 wk | Pitch roll-up adjacencies; map sub-scale Medicare books |
| 3 | **The funnel entrance is the next underwriting-data advantage** | Watch (new) | Low | PruVen (insurance CVC) in Gradial $65M marketing-AI, Jun 18 | 1 datapoint | Jun-19 wk | Jun-19 wk | Watch carrier/CVC bets on first-party intent & content data |

### 3b. Narrative — InsurTech, Week of June 14–20, 2026
> **Four deals. ~$44M tracked. A health-insurance roll-up went shopping *with* its Series B — and an insurer's marketing-AI bet quietly redrew where underwriting advantage will come from.**
>
> *Tags: Carrier Strategy · AI & Automation · Distribution · Medicare/Health · Venture & Growth*
>
> **Thesis in focus — AI is moving into insurance *operations*, not the quote box.** Two weeks
> ago **Poetic** raised $50M (Kleiner Perkins) to automate complex, multi-step insurance
> back-office work with deterministic AI. This week confirmed it from two sides: **Trussed AI**
> (backed by **Nassau Financial Group**) is building the AI governance/compliance layer carriers
> need to deploy that automation safely, and **Braven** (ex-Sytrex, $4.6M seed) is automating
> delegated-authority ops — binder validation, bordereaux — for MGAs and reinsurers. Capital has
> stopped chasing the front-end and started wiring the back office. *(Thesis #1 → confidence up.)*
>
> **The deal that matters most — Connie Health ($40M Series B, HealthQuest Capital).** Look at
> what it did *with* the round: simultaneously closed its **10th acquisition**, absorbing
> Clearlink's Medicare book. That's the AI-native agency playbook — raise primary capital, then
> roll up distribution faster than incumbents can react. This is becoming a consolidation, not a
> company; watch the next two tuck-ins. *(Seeds Thesis #2.)*
>
> **Carrier-strategy read — IAG into Sonder.** A carrier (via Firemark Ventures) taking a
> minority in a people-risk/wellbeing platform is the quiet move to *own the data that prevents
> the claim*, not just price it.
>
> **The trend nobody's named yet.** The week's most overlooked signal sits *outside* the
> insurtech label: **PruVen Capital** — an insurance-linked CVC — turned up in **Gradial's**
> $65M round, an *enterprise-marketing* AI. Why does insurance money back a marketing tool?
> Because whoever controls the funnel entrance — first-party intent and content data — owns the
> cheapest, freshest underwriting signal in 2029. *(Thesis #3, watch.)*
>
> **[Tape: InsurTech public median fwd EV/Revenue = __x (__ vs prior snapshot); trailing-13-wk
> InsurTech primary capital = $__M across __ deals.]**

---

## 4. How to read it / grading vs. the benchmark
- **It independently reproduces the benchmark's headline insight** — "the companies controlling
  the funnel entrance are building the next underwriting data advantage" (Gradial/PruVen). That's
  the validation: the *system* surfaces the same non-obvious trend a top human analyst did.
- **What's still a stub:** the `[Tape: …]` line. That single number is the only thing sourced
  from Excel — it's what makes the prose defensible instead of vibes.
- **What improves on the full DB:** Thesis #2 (roll-up) gets quantified — how many AI-native
  agency acquisitions across the back-catalog, at what cadence; Thesis #1 gets a multiple trend
  (are AI-ops insurtechs re-rating vs. carriers?). The mechanics don't change — only the depth.

**Next:** run this exact prompt in NotebookLM on the two InsurTech logs, drop in one real Tape
number, and compare to the benchmark. If the voice lands, we replicate the pattern across the
other seven subsectors and add the cross-sector synthesis.
