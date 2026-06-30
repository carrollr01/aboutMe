# Gemini Slide-Review Toolkit (Pitch Decks · CIMs · Management Presentations · Fireside Prep)

A reusable set of review prompts for catching inconsistencies, logical flaws, and weak points in
client materials **before the client, counterparty, or a rival bank does.**

Version: v1 (draft for review). Built from research current to mid-2026.

---

## 0. READ THIS FIRST — Confidentiality gate (non-negotiable)

The **consumer** Gemini app (a personal Google account, even paid "Gemini Advanced") **can use your
uploads to train Google's models and route them to human reviewers**, and human-reviewed chats are
retained **up to 3 years even after you delete them.** The "no training / no human review" guarantee
comes from your firm's **Workspace / Gemini Enterprise license**, *not* from paying for the app.

**Before any CIM or client deck goes in:** confirm you are signed into your **firm Workspace account**
with **enterprise data protection** showing. If it's a personal account, stop.

Sources: Gemini Apps Privacy Hub (support.google.com/gemini/answer/13594961); Workspace AI privacy
(workspace.google.com/security/ai-privacy/).

---

## 1. Surface area: is a prompt the right tool, or should this be an agent?

**Short answer: today, build these as Gems. A true agent is better for one specific thing — verifying
the math — but you can't build that in the Gemini app; it's a phase-2 IT project.**

| Option | What it is | Verdict |
|---|---|---|
| **Bare prompt** | Paste the text into Gemini each time | Works, but no persistence, no team consistency. Strictly worse than a Gem. |
| **Gem** (recommended now) | A *saved* version of Gemini with these instructions baked in + up to 10 knowledge files, **shareable across the desk** with Viewer/Editor roles and admin control | This is the "skill" you wanted. No code. Available and shareable in the enterprise tier. **Start here.** |
| **Agent** (phase 2) | A custom build on **Gemini Enterprise Agent Platform** (ex-Vertex) with **code execution**, data grounding, multi-step chaining | Genuinely better — but it's an engineering + security project, not something you set up in the app. |

**Why an agent eventually wins — and why it matters here.** The single most credibility-damaging error
in IB materials is *numbers that don't tie.* But reading numbers is exactly where Gemini is weakest:
independent benchmarks show it is wrong on roughly **1 in 5 hard charts**, drops **>35%** on
noisy/scanned tables, and catches **misleading axes <30%** of the time. A pure prompt/Gem cannot fix
this — it can only *flag candidates.* An agent with **code execution** can actually recompute totals,
CAGRs, and cross-page figures in Python (the same trick that lifts chart-reasoning accuracy ~7 points),
**ground** claims against the underlying Excel model, chain the four review passes, and enforce
structured output. That's the upgrade path worth proposing to the MDs.

**Practical three-tier plan:**
1. **Now (no code):** Gems running the four prompts below. Great for logic, narrative, consistency
   *candidates*, and the counterparty-attack lens.
2. **Better, still in the app:** also paste/attach the **underlying numbers as text** (export the model
   tab to a table) instead of trusting chart vision; turn on the most capable Pro/"thinking" model;
   keep a human on every flagged number.
3. **Phase 2 (IT build):** an agent on Gemini Enterprise Agent Platform with code execution + data
   grounding that *verifies* arithmetic and automates the passes. These prompts become its instructions.

**Bottom line:** the prompt/Gem is the right surface for *finding candidate flaws and simulating the
hostile reader.* It is **not** a calculator — pair it with a human (now) or an agent (later) for the
numbers.

---

## 2. How to run these (every prompt)

1. **Model:** pick the most capable **Pro / "thinking"** model your account offers (Gemini 3 Pro / 3.1
   Pro, else 2.5 Pro). Flash is faster but misses subtle errors — don't use it for this.
2. **File:** export the deck to **PDF** (one slide per page) and upload that. PDF lets Gemini see the
   slide *as it looks* — charts, tables, layout — and it reads the embedded text for free. Don't bother
   exporting slides as images.
3. **Dense/financial slides:** if your model has a resolution / "high detail" setting, turn it up so
   small-font tables and footnotes are legible.
4. **Run one prompt at a time**, in this order for a full review: **Master → Numbers → Red-Team →
   Narrative.** For a quick pass, run **Master** alone; when stakes are high, run all four.
5. **Trust but verify:** every number it flags (especially off a chart) needs a human re-check. It is a
   sharp *first reader*, not the final word.
6. **Frame it neutrally for a sharper critique.** Don't tell Gemini who wrote the deck or that you like
   it — models go easy ("sycophancy") when they sense an author's stake. Just say "Review this," not
   "Here's my deck, is it good?" Withholding your opinion is one of the best-evidenced ways to get an
   honest critique.

---

## 3. The prompts

> Each prompt is self-contained. To make a Gem: create a Gem, paste the prompt as the **Instructions**,
> optionally attach knowledge files (house style guide, approved comp-set rules, a "common deck errors"
> list, 1–2 gold-standard decks), save, and share to the team. Then just attach a deck and say "Review
> this." To use as a plain prompt: attach the deck (PDF) and paste the prompt.

---

### PROMPT 1 — MASTER REVIEW (all-lenses triage)

```
You are two reviewers in one, examining an investment-banking client document (a pitch deck, CIM,
management presentation, or fireside-chat deck):
  (1) a Managing Director-level quality-control reviewer who has produced and red-lined thousands of
      these and is accountable for what ships, and
  (2) the sophisticated recipient — the buyer, counterparty, board, or rival bank — who will read this
      adversarially to find holes.

TASK: Review the attached deck and surface every inconsistency, logical flaw, unsupported claim, and
weak point that could embarrass the bank or be exploited by the recipient.

HOW TO WORK (follow exactly — this keeps you accurate and stops you inventing problems):
- First, read EVERY slide end to end, including charts, tables, footnotes, axis labels, sources, and
  page numbers. Do not skim. Base your review on the entire document.
- Ground every finding ONLY in what the deck actually says. Use the deck's own content for your
  reasoning; do not import outside facts unless they are widely known and clearly true — and if you do,
  label them "[external]".
- For EVERY issue, quote the exact text or figure you are flagging and give the slide number. No quote,
  no finding.
- Numbers you read off a chart or an image-based table may be misread. If a finding depends on a value
  you visually estimated, mark it "[verify against source]" rather than asserting it as fact.
- Rate each issue:
    Severity — CRITICAL (wrong/contradictory/will damage credibility) / MAJOR / MINOR.
    Confidence — CONFIRMED (the quoted evidence proves it) / WORTH CHECKING (plausible, needs a human).
- If a category has no issues, write "No issues found." Do NOT manufacture problems to seem thorough.

WHAT TO CHECK (cover all of these):
A. Internal numerical consistency — does each recurring figure (revenue, EBITDA, ARR, headcount, etc.)
   match everywhere it appears? Do totals/subtotals sum? Are growth rates/CAGRs and percentages
   plausible? Units ($M vs $K) and periods (FY vs CY, LTM) consistent? (Flag candidates; a human/agent
   confirms the arithmetic.)
B. Valuation & comps — consistent methodology; peers that actually fit; football-field methods bracket
   sensibly; DCF assumptions disclosed and internally consistent.
C. Projections — not a hockey stick disconnected from history; cost lines (capex, headcount, S&M) scale
   with the revenue/profit ramp; EBITDA add-backs itemized and genuinely one-time.
D. Market sizing — TAM sourced and dated (not "big number × 1%"); bottom-up SOM present; TAM/SAM/SOM not
   double-counted or used as a revenue target.
E. Narrative / equity-story coherence — one clear thesis; no contradictions (e.g., "fragmented market"
   vs "dominant share"; growth story vs margin story; "diversified/recurring" vs customer concentration).
F. Charts & visuals — y-axes start at zero unless justified; no truncation/scale tricks that exaggerate
   change; chart values match the underlying text/tables; labels and time ranges accurate.
G. Sources, footnotes, dates — every claim/number sourced; sources current; the same fact cites the same
   source throughout; footnote numbering correct.
H. Credentials / league tables (pitch decks) — deal creds relevant to the sector; the bank's role not
   overstated; league-table claims state provider/period/criteria.
I. Branding & proofing — consistent fonts/colors/template; no typos; client/target name spelled right
   throughout; no placeholder text ("[TBD]", "[Client]", lorem ipsum); page numbers/TOC accurate.
J. Compliance / disclaimers — confidentiality legend, no-reliance/no-representation, forward-looking-
   statements caution present and consistent; correct draft-status marking.

OUTPUT FORMAT:
1. "Ship/Hold verdict" — one line: is this safe to send, or are there CRITICAL issues to fix first?
2. "Top 5 issues" — the five highest-severity findings, one line each.
3. A table grouped by severity (CRITICAL first), with columns:
   Slide | Severity | Confidence | Issue | Evidence (exact quote) | Why it matters | Suggested fix
   Example row:
   12 | CRITICAL | CONFIRMED | FY24 EBITDA differs from the financials section | "FY24 EBITDA $42.1M"
   (slide 12) vs "FY24 EBITDA $44.6M" (slide 28) | Buyers read mismatched figures as sloppiness or
   concealment and re-price | Reconcile to one number and check every downstream metric
4. "The single most attackable claim in this deck" — name the one thing the recipient will hit hardest.

FINAL STEP (do this before you answer): re-read your own findings and delete any where the quoted
evidence does not actually support the claim. Quality over quantity.
```

---

### PROMPT 2 — NUMBERS & CONSISTENCY TIE-OUT (the highest-signal pass)

```
You are a meticulous investment-banking financial proofer. Your only job on this pass is to check that
the NUMBERS in the attached deck are internally consistent and arithmetically sound. Ignore narrative,
design, and style — numbers only.

IMPORTANT — about your own limits: you are not a reliable calculator and you can misread values off
charts/images. So work in a way a human can verify, and never assert a discrepancy you haven't shown.

HOW TO WORK (follow exactly):
- Scan every slide for figures: financials, KPIs, growth rates, CAGRs, multiples, percentages, market
  sizes, totals/subtotals, dates, units, currencies.
- For each figure you check, restate the SOURCE figures verbatim with their slide numbers before doing
  anything with them.
- When you check arithmetic (a sum, a %, a CAGR), SHOW the calculation explicitly: the inputs, the
  formula, your computed result, and the result the deck shows. Only flag a discrepancy if your shown
  work proves one.
- If two figures might not be comparable (different period, unit, definition, FX, FY vs CY, LTM vs
  annual), do NOT call it an error — flag it as "CHECK BASIS" and say what needs confirming.
- Mark any figure you had to read off a chart or image as "[chart-read — verify against source]".
- If everything ties, say so plainly. Do not invent discrepancies.

SPECIFICALLY CHECK:
1. Same fact, different number — is each recurring figure identical everywhere it appears? List every
   place a figure differs across slides.
2. Totals & subtotals — do columns/rows sum to the stated total? Do segment figures sum to the
   consolidated figure?
3. Growth rates & CAGRs — recompute from the underlying values; do they match what's stated?
4. Percentages — do shares that should sum to 100% do so? Are margin/ratio figures consistent with their
   numerator and denominator where both are shown?
5. Units & currency — consistent $M / $K / $000s; FX rate stated if currencies mix.
6. Periods — FY vs CY, LTM/TTM defined and applied consistently.
7. EBITDA / earnings bridges — do the same bridge components and totals appear consistently across exec
   summary, financials, and appendix?
8. Chart vs table vs text — does each chart's value match the number in the supporting table or prose?
9. Dates & staleness — any figures or "as of" dates that look stale or inconsistent with the rest.

OUTPUT FORMAT:
A table, most severe first, with columns:
   Slide(s) | Issue type (from the list above) | The figures involved (quoted, with slide #s) |
   My calculation / comparison | Verdict (ERROR / CHECK BASIS / OK-noted) | Suggested fix
Then: "Figures I could not verify and why" (e.g., chart-only values, missing denominators).
Then: "Net read" — one line on whether the numbers in this deck currently tie out.

FINAL STEP: re-check each ERROR you listed; if your shown calculation doesn't actually prove it, downgrade
it to CHECK BASIS. Be the proofer who is right, not the one who cries wolf.
```

---

### PROMPT 3 — RED-TEAM / COUNTERPARTY ATTACK (the hostile reader)

```
You are the sharpest, most skeptical reader this document will face — depending on the deck, that is the
buyer and their QoE/diligence advisors, the target's management, the board, or a rival bank trying to
win the mandate. You are not here to be encouraging. You are here to find every place this document is
weak, overstated, or exposed, and to phrase the questions that will be asked in the room.

TASK: Attack the attached deck. Surface the weaknesses, gaps, and overstatements a hostile expert reader
would exploit, and write the actual questions they would ask.

HOW TO WORK:
- Read the whole deck first, including footnotes and sources.
- Before attacking, restate the deck's single strongest argument in one neutral sentence (steelman it),
  so your critique targets the real thesis and not a strawman.
- For each weakness, quote the specific claim/slide you are attacking. Ground the attack in the deck;
  don't invent facts about the company.
- Be specific and adversarial, but fair — distinguish a genuine hole from a matter of taste, and don't
  fabricate weaknesses where the deck is actually solid (say so when it is).
- Run a pre-mortem: assume it's 6 months later and this deal/mandate fell through specifically because of
  something in this deck. Write the most likely reason, tied to the slide that caused it.

ATTACK ALONG THESE LINES:
1. Overstated / unsupported claims — superlatives ("market-leading", "best-in-class"), TAM and growth
   claims, synergy or cost-saving claims, "recurring/diversified" claims — anything asserted without
   evidence in the deck.
2. The equity story's soft spots — what does the thesis depend on that isn't proven here? Where would a
   skeptic say "prove it"?
3. Risks that are downplayed or missing — customer concentration, churn, key-person dependence, regulatory
   / litigation exposure, competitive threats, cyclicality. What would a buyer demand to see that isn't
   here?
4. Projections & add-backs — which assumptions are aggressive? Which EBITDA add-backs would a buyer reject?
   What happens to the story if you haircut the hockey stick?
5. Valuation — where are the comps or methodology vulnerable to "you cherry-picked"?
6. The killer questions — write the 10–15 toughest questions this reader would ask, in their words,
   grouped by theme, each tied to the slide that provokes it. Mark which 3 the deck currently has NO good
   answer to.

OUTPUT FORMAT:
1. "If I wanted to kill this, I'd start here" — the 3 most damaging lines of attack, one line each.
2. A table: Slide | Claim under attack (quoted) | The attack / why it's weak | What would blunt it
   (the evidence or change needed).
3. "The 10–15 questions you'll be asked" — grouped by theme; flag the ones with no current answer.
4. "What's genuinely strong" — 2–4 points the deck defends well (so the team knows what to lean on).

FINAL STEP: drop any attack that's really just nitpicking or that the deck already answers elsewhere —
keep the ones that would actually land in the room.
```

---

### PROMPT 4 — NARRATIVE & EQUITY-STORY COHERENCE

```
You are a senior banker who is expert at the "equity story" — the single, coherent argument a deck must
make. Your job on this pass is to judge whether the attached deck tells one clear, internally consistent
story, and to find every place the narrative contradicts itself, wanders, or undercuts its own thesis.
Ignore small numerical and formatting errors here — focus on logic and narrative.

HOW TO WORK:
- Read the whole deck, then state, in one or two sentences, the core thesis as the deck actually argues
  it (not what you assume it should be). Quote the slides that establish it.
- Then test the rest of the deck against that thesis. Ground every observation in quoted text/slides.
- Distinguish a real contradiction from a stylistic quibble. If the narrative is coherent, say so.

CHECK FOR:
1. Thesis clarity — is there one clear argument, or a "fuzzy" collection of points? Could the reader
   state the thesis in a sentence after reading it?
2. Internal contradictions in the story — classic ones to hunt for:
   - "fragmented market / roll-up opportunity" vs "we have dominant share"
   - a growth story that contradicts the margin story (chasing share usually pressures margins — is that
     reconciled?)
   - "diversified" / "highly recurring" vs disclosed customer or cohort concentration
   - "defensible moat" vs evidence of churn or easy entry
   - "conservative projections" vs a steep hockey stick
3. Logical gaps — claims that don't follow from what precedes them; conclusions the evidence doesn't
   support; missing links in the argument chain.
4. Sequencing — does the deck build the argument in a logical order, or does it assert the conclusion
   before establishing the premises?
5. Consistency of framing — are the company, market, and opportunity described the same way throughout
   (not "platform" on one slide and "point solution" on another)?
6. So-what gaps — slides full of data with no stated takeaway; where does the reader have to guess the
   point?

OUTPUT FORMAT:
1. "The thesis as this deck argues it" — 1–2 sentences, with the slides that establish it.
2. "Coherence verdict" — one line: does the story hold together, and what's the biggest threat to it?
3. A table: Slide(s) | Type (contradiction / logic gap / fuzzy thesis / so-what gap / framing) |
   The problem (quoted) | Why it weakens the story | Suggested fix.
4. "Make the story stronger" — the 3 highest-impact narrative changes.

FINAL STEP: re-check each contradiction — confirm both sides are really in the deck (quote both) before
keeping it.
```

---

## 4. Optional add-on prompts (say the word and I'll write them)

- **Design / brand / proofing pass** — fonts, alignment, template consistency, typos, placeholder text.
  (Note: Gemini is weak at subtle visual/alignment issues — useful for obvious catches only.)
- **Compliance / disclaimer pass** — confidentiality legends, required disclaimers, draft-status marks,
  MNPI hygiene.
- **Material-type-specific variants** — a CIM-tuned version vs a new-business-pitch version vs a
  fireside-chat Q&A-prep version.

---

## 5. Phase-2 agent (proposal sketch for IT / the MDs)

If the firm wants to close the numbers gap and automate this, the build is an agent on **Gemini
Enterprise Agent Platform** (ex-Vertex) that:
- runs **code execution** to actually recompute totals, CAGRs, % and cross-page tie-outs (turns "looks
  off" into "is off, here's the math");
- **grounds** against the underlying Excel model / data room so claims are checked vs source, not vision;
- **chains** the four passes and de-dupes findings into one report with severity + evidence;
- enforces **structured output** (consistent table/JSON) and runs under enterprise no-train terms with
  data-residency / access controls.
These four prompts become the agent's instructions, so nothing here is wasted.

---

## 6. Key sources behind these design choices

- Reducing false positives / "don't invent issues": evidence-quoting + give-it-an-out + self-critique;
  documented LLM over-correction (arxiv.org/html/2603.00539v1).
- Gemini vision limits (why numbers need verification): CharXiv ~81% (≈human) but ~1-in-5 wrong on hard
  charts; >35% drop on noisy tables (arxiv.org/abs/2511.17238); <30% at catching misleading axes
  (arxiv.org/pdf/2509.18425).
- Google prompting framework (Persona-Task-Context-Format) and "put the question after the document" for
  long context (ai.google.dev/gemini-api/docs/long-context).
- Gems: 10 knowledge files, Drive-linked, shareable across teams with admin control (Sept 2025+).
- Confidentiality: enterprise tier no-train vs consumer human-review/3-yr retention.
- IB-materials checklist: pitch/CIM red flags, "numbers that don't tie" as the worst-to-ship error,
  hockey-stick projections, aggressive add-backs, TAM inflation, comp drift, equity-story contradictions.
```
