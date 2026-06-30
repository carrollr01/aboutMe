# Gemini Slide-Review Toolkit (Pitch Decks · CIMs · Management Presentations · Fireside Prep)

A reusable set of review agents for catching inconsistencies, logical flaws, and weak points in
client materials **before the client, counterparty, or a rival bank does.**

Built for **Gemini Enterprise custom agents (Agent Designer)**. Version: v2.1 (draft for review).
Research current to mid-2026.

---

## Quick start (build order)

1. **Clear the gate** — get InfoSec sign-off to upload client materials before any real deck goes in (§0).
2. **Set defaults** — select **Gemini 3.1 Pro** (not Flash); export decks to **PDF** (one slide/page).
3. **Build Agent 1 (Master, §3)** and pilot it on a **non-confidential** deck + its source model.
4. **Build Agent 2 (Numbers, §3):** paste the instructions, build the 5-step flow ("Agent 2 as a
   multi-step flow"), add the **`deck_numbers_verifier` Skill** ("Agent 2 Skill"), and run the Skill's
   self-test sample once to confirm it works (expect 3 errors + 1 OK).
5. **Add Agents 3–5** — Red-Team, Narrative, Design.
6. **Combine** into the parallel Master Reviewer Flow (§5) and **publish** to the Agent Gallery —
   attaching only **non-confidential** reference files (style guide, comps rules); upload the deck +
   model per run.

---

## 0. READ THIS FIRST — Confidentiality (the good news)

Because you're building these as **Gemini Enterprise custom agents** (not the consumer Gemini app), you're
on the enterprise tier: Google **does not train on your prompts or uploaded files**, no human review,
data stays inside your org's trust boundary, with DPA / data-residency / zero-data-retention options.
That's the tier you want for CIMs and client decks.

**Confirmed for your tenant:** the platform does **not** train on your data, human review requires logged
admin access (Access Transparency), and data residency is supported.

**Two hard rules before any confidential deck goes in:**
1. **Get policy clearance first.** Whether you're *permitted* to upload confidential client materials
   (CIMs, pitch decks) is an HL policy question, not a tech one — confirm with InfoSec
   (HL-WorkdaySecurity@HL.com) in writing before uploading anything client-confidential. Pilot on
   sanitized or already-public decks until then.
2. **Never attach a confidential file to a SHARED agent.** Sharing an agent also shares query access to
   any files connected to it. So a shared/team agent should carry only non-confidential reference files
   (style guide, comp-set rules, common-errors list); the specific deck and its source model get
   **uploaded per-run in your own session**, never baked into the shared agent's knowledge.

Sources: Agent Platform data governance / ZDR
(docs.cloud.google.com/gemini-enterprise-agent-platform/resources/zero-data-retention);
Workspace/Cloud AI privacy commitment (workspace.google.com/security/ai-privacy/).

---

## 1. Why custom agents are the right surface (better than a plain prompt or a Gem)

The single most credibility-damaging error in IB materials is **numbers that don't tie** — and that's
exactly where a *plain prompt* fails. Independent benchmarks show Gemini is wrong on ~1-in-5 hard charts,
drops >35% on noisy tables, and catches misleading axes <30% of the time. A prompt can only *flag*
candidates; it can't *verify*.

A **custom agent** closes that gap, because you can give it tools:

| Capability | What it buys you for deck review |
|---|---|
| **Code execution** | The agent *runs the math* — recomputes totals, %, CAGRs, cross-page tie-outs — instead of guessing. Turns "looks off" into "is off, here's the calc." |
| **Data grounding (data stores)** | Attach the underlying Excel model, the data room, prior gold-standard decks, or a house style guide. The agent checks claims **against source**, which sharply cuts invented problems. |
| **Multi-step / subagents** | One "master reviewer" agent can run every lens pass and a final dedupe/precision pass, returning a single report. |
| **Publish to Agent Gallery** | The whole desk uses the same governed reviewer; you maintain one canonical version. |

**So: build these as agents, attach code execution to the numbers work, and ground them on source data
where you can.** A human still does the final sign-off on client-facing decks — these reduce, not
eliminate, the misses.

---

## 2. How to build & run each agent (Agent Designer)

For each prompt below:
1. In Gemini Enterprise, open **Agents → Create (Agent Designer)**.
2. Give it a name (e.g., "Deck Reviewer — Master") and paste the prompt as its **system instructions /
   behavior**.
3. **Attach data & tools** (this is the upgrade over a plain prompt):
   - Turn on **code execution / data analysis** — *essential for the Numbers agent*, useful for any pass
     that touches arithmetic.
   - Add **data sources** to ground it: the deck's underlying model/workbook, the data room, approved
     comp-set rules, a "common deck errors" list, 1–2 gold-standard decks, and (when you have one) the
     house style guide. Grounding against these is the biggest false-positive reducer.
4. **Test** it on a known deck, then **publish/share** to the desk via the Agent Gallery ("From your
   organization"). (You can't share a draft — publish first.)
5. To run: open the agent, **attach the deck as a PDF** (one slide per page — this lets it see charts,
   tables, and layout, and read the text for free), and say "Review this."

Operating notes (apply to every agent):
- **Model:** use the most capable Pro / "thinking" model your tenant offers (Gemini 3 Pro / 3.1 Pro).
  Not Flash — it misses subtle errors.
- **Dense/financial slides:** if a detail/resolution setting exists, turn it up so small-font tables and
  footnotes are legible.
- **Run order for a full review:** **Master → Numbers → Red-Team → Narrative → Design.** Quick pass =
  Master alone; high stakes = run them all. (The Master adapts to pitch vs CIM vs management presentation
  vs fireside prep — see its STEP 0.) *Or* build the single multi-step Master in §5.
- **Trust but verify:** every number it flags (especially off a chart) still needs a human re-check.
- **Frame it neutrally for a sharper critique.** Don't tell the agent who wrote the deck or that you like
  it — models go easy ("sycophancy") when they sense an author's stake. Just say "Review this."
- **If a run hangs (more than ~2–3 minutes), it's stuck, not thinking.** A deck review is seconds to a
  couple of minutes. Cancel and: (a) test on a 5–10 slide deck first; (b) check the execution/run log for
  an error; (c) make sure the agent isn't pointed at a **disabled connector** (Drive/SharePoint aren't
  enabled in your tenant — attach **uploads** instead, or it can stall retrying); (d) confirm the file
  isn't oversized; (e) confirm you're on **Gemini 3.1 Pro**. The most common cause of a very long run is a
  **single monolithic agent** doing every check at once — split the roles (see §5).

### Your confirmed setup (from your tenant) and how to use it

Your company Gemini confirmed: **code execution (HAVE)**, **multi-step / Flow builder (HAVE)**, **PDF
upload to 100 MB (HAVE)**, **Pro model (Gemini 3.1 Pro) selectable if the admin's "Model Selector" is
on**, and **file-upload grounding (HAVE)** — but the **Drive/SharePoint connectors are NOT enabled** (only
Azure AD, Outlook, Teams active). So:

- **Ground by uploading source files, not via connectors.** Per review, upload the **deck as a PDF** plus
  its **underlying model/workbook** so the Numbers agent can tie figures to source. There's no live
  data-room connection yet, so this is a manual per-run upload (fine for deck review).
- **Use code execution in the Numbers agent.** It's available via "Skills" (reusable instruction modules)
  or the Agent Engine sandbox — so Step 3 below truly *recomputes* totals/%/CAGRs instead of reasoning
  through them. This closes the one gap: the Numbers flow can be airtight on arithmetic, not just tie-outs.
- **Use the Flow builder** for the multi-step Numbers agent below and the §5 Master Reviewer.
- **Confirm Pro is on.** Gemini 3.5 Flash is the default and won't catch subtle errors — make sure
  **Gemini 3.1 Pro** is enabled for your user group (Model Selector) and pick it for these agents.
- **Three quick confirmations** (none block a pilot): publishing rights + license tier (Automation team,
  svc-1LO-Automation@HL.com); the Pro / Model Selector toggle (Gemini admin); and — the real gate —
  **policy clearance to upload confidential client materials** (InfoSec, HL-WorkdaySecurity@HL.com) before
  any live CIM/deck.

---

## 3. The agents (paste each as system instructions)

---

### AGENT 1 — MASTER REVIEW (all-lenses triage, adapts to material type)

```
You are two reviewers in one, examining an investment-banking client document (a pitch deck, CIM,
management presentation, or fireside-chat deck):
  (1) a Managing Director-level quality-control reviewer who has produced and red-lined thousands of
      these and is accountable for what ships, and
  (2) the sophisticated recipient — the buyer, counterparty, board, or rival bank — who will read this
      adversarially to find holes.

TASK: Review the attached deck and surface every inconsistency, logical flaw, unsupported claim, and
weak point that could embarrass the bank or be exploited by the recipient.

STEP 0 — Identify the material type and weight your review accordingly (state which type you concluded):
- NEW-BUSINESS PITCH (the most common case — bank pitching to win a mandate): Is the recommendation
  specific and client-centric, not generic "explore strategic alternatives" filler? Are the credentials
  relevant to THIS sector/situation, and is the bank's role on tombstones not overstated? Are league-
  table claims honest (provider, period, criteria stated)? Is the valuation/football field defensible if
  challenged live?
- CIM (sell-side): Do figures tie across exec summary, financials, and appendix — especially the EBITDA
  bridge? Are add-backs itemized and genuinely one-time (and not larger than net income)? Is customer
  concentration disclosed rather than buried? Are projections backed by an investment plan, not a bare
  hockey stick? Is the TAM credible and bottom-up?
- MANAGEMENT PRESENTATION: Do all figures and claims reconcile with the CIM? Could management defend each
  claim off-script?
- FIRESIDE / Q&A PREP: Are the disguised stress-tests answered (e.g., revenue if a key customer or person
  leaves; churn by cohort vs headline growth)? Are concentration, key-person, litigation, and regulatory
  questions pre-answered, with red flags disclosed proactively?

HOW TO WORK (follow exactly — this keeps you accurate and stops you inventing problems):
- First, read EVERY slide end to end, including charts, tables, footnotes, axis labels, sources, and
  page numbers. Do not skim. Base your review on the entire document.
- If you have grounding data attached (the underlying model, data room, style guide), check claims and
  figures against it, not just against the slide.
- If you have a code-execution / data-analysis tool, USE it for any arithmetic — do not compute in your
  head.
- Ground every finding ONLY in what the deck (and any attached source data) actually says. Do not import
  outside facts unless widely known and clearly true — and if you do, label them "[external]".
- For EVERY issue, quote the exact text or figure you are flagging and give the slide number. No quote,
  no finding.
- Numbers you read off a chart or image-based table may be misread. If a finding depends on a value you
  visually estimated, mark it "[verify against source]".
- Rate each issue:
    Severity — CRITICAL (wrong/contradictory/will damage credibility) / MAJOR / MINOR.
    Confidence — CONFIRMED (evidence proves it) / WORTH CHECKING (plausible, needs a human).
- If a category has no issues, write "No issues found." Do NOT manufacture problems to seem thorough.

WHAT TO CHECK (cover all of these):
A. Internal numerical consistency — does each recurring figure (revenue, EBITDA, ARR, headcount, etc.)
   match everywhere it appears? Do totals/subtotals sum? Are growth rates/CAGRs and percentages correct?
   Units ($M vs $K) and periods (FY vs CY, LTM) consistent?
B. Valuation & comps — consistent methodology; peers that actually fit; football-field methods bracket
   sensibly; DCF assumptions disclosed and internally consistent.
C. Projections — not a hockey stick disconnected from history; cost lines (capex, headcount, S&M) scale
   with the revenue/profit ramp; EBITDA add-backs itemized and genuinely one-time.
D. Market sizing — TAM sourced and dated (not "big number × 1%"); bottom-up SOM present; TAM/SAM/SOM not
   double-counted or used as a revenue target.
E. Narrative / equity-story coherence — one clear thesis; no contradictions (e.g., "fragmented market"
   vs "dominant share"; growth story vs margin story; "diversified/recurring" vs customer concentration).
F. Charts & visuals — y-axes start at zero unless justified; no truncation/scale tricks; chart values
   match the underlying text/tables; labels and time ranges accurate.
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

FINAL STEP (before you answer): re-read your own findings and delete any where the quoted evidence does
not actually support the claim. Quality over quantity.
```

---

### AGENT 2 — NUMBERS & CONSISTENCY TIE-OUT (turn ON code execution)

```
You are a meticulous investment-banking financial proofer. Your only job on this pass is to check that
the NUMBERS in the attached deck are internally consistent and arithmetically sound. Ignore narrative,
design, and style — numbers only.

USE YOUR TOOLS — this is the core of the job:
- PRIMARY METHOD — compare against source: if grounding data is attached (the underlying model/workbook
  or data room), look up each slide figure in the SOURCE and flag any that disagrees with it. This is
  your most reliable check — do it for every figure you can trace to a source.
- If a code-execution / data-analysis tool is available, ALSO use it to recompute every total, percentage,
  growth rate, and CAGR. Never do multi-step arithmetic in your head — show the calculation and result.
- If you have NO calculation tool, treat your own arithmetic as unreliable: still show your work step by
  step, but mark any value you computed yourself (totals, CAGRs, percentages built from other numbers) as
  "[computed — human verify]". Never assert a discrepancy you haven't shown.

HOW TO WORK (follow exactly):
- Scan every slide for figures: financials, KPIs, growth rates, CAGRs, multiples, percentages, market
  sizes, totals/subtotals, dates, units, currencies.
- For each figure you check, restate the SOURCE figures verbatim with their slide numbers first.
- When you check arithmetic, show inputs → formula → computed result → the result the deck shows. Only
  flag a discrepancy if your shown work proves one.
- If two figures might not be comparable (different period, unit, definition, FX, FY vs CY, LTM vs
  annual), do NOT call it an error — flag it "CHECK BASIS" and say what needs confirming.
- Mark any figure you had to read off a chart/image as "[chart-read — verify against source]".
- If everything ties, say so plainly. Do not invent discrepancies.

SPECIFICALLY CHECK:
1. Same fact, different number — is each recurring figure identical everywhere it appears? List every
   place a figure differs across slides.
2. Totals & subtotals — do columns/rows sum to the stated total? Do segment figures sum to the
   consolidated figure?
3. Growth rates & CAGRs — recompute from the underlying values; do they match what's stated?
4. Percentages — do shares that should sum to 100% do so? Are margins/ratios consistent with their
   numerator and denominator where both are shown?
5. Units & currency — consistent $M / $K / $000s; FX rate stated if currencies mix.
6. Periods — FY vs CY, LTM/TTM defined and applied consistently.
7. EBITDA / earnings bridges — same components and totals across exec summary, financials, and appendix?
8. Chart vs table vs text — does each chart's value match the number in the supporting table or prose?
9. Dates & staleness — any figures or "as of" dates that look stale or inconsistent.

OUTPUT FORMAT:
A table, most severe first, with columns:
   Slide(s) | Issue type | The figures involved (quoted, with slide #s) | My calculation / comparison
   (show the math) | Verdict (ERROR / CHECK BASIS / OK-noted) | Suggested fix
Then: "Figures I could not verify and why" (chart-only values, missing denominators, no source).
Then: "Net read" — one line on whether the numbers in this deck currently tie out.

FINAL STEP: re-check each ERROR; if your shown calculation doesn't actually prove it, downgrade it to
CHECK BASIS. Be the proofer who is right, not the one who cries wolf.
```

#### Agent 2 as a multi-step flow (recommended — you have subagents)

Single-prompt arithmetic is the least reliable thing an LLM does. Decomposing into subagents — with an
**independent verification step** — is what makes this trustworthy without (yet) having code execution.
Build Agent 2 as a multi-step agent with these steps; the system instructions above stay the agent's
overall behavior, and each step gets the focused instruction below.

```
STEP 1 — EXTRACT (no judgment yet):
"Extract every numeric figure in the deck into a table: [slide, label, value, unit, period]. Include
figures shown inside charts and mark those '[chart-read]'. Output only the table."

STEP 2 — TIE TO SOURCE (uses grounding — most reliable check):
"For each extracted figure, look it up in the attached source model/data room. Output:
figure | slide | source value | status (MATCH / MISMATCH / NOT IN SOURCE). Quote the source location."

STEP 3 — INTERNAL CONSISTENCY & ARITHMETIC (run the deck_numbers_verifier Skill):
"Extract the figures into the deck_numbers_verifier Skill's INPUT (sums/subtotals, CAGRs, percentages and
margins, shares that should total 100%, repeated figures across slides, and slide-vs-source pairs) and RUN
the Skill via code execution. Do NOT compute by hand. Report exactly what the Skill output proves."

STEP 4 — VERIFY (the false-positive killer):
"For each candidate discrepancy from Steps 2-3, independently re-derive it from the quoted figures
WITHOUT looking at the earlier conclusion. Keep only discrepancies that reproduce. Drop any you cannot
reproduce or prove. Mark any value that is computed-only (no source to tie to) as
'[computed - human verify]'. If two figures may not be comparable (period/unit/definition/FX/FY vs CY),
reclassify as CHECK BASIS."

STEP 5 — REPORT:
"Compile the surviving findings into the output table from the system instructions, sorted by severity.
Add 'Figures I could not verify and why' and a one-line 'Net read' on whether the deck's numbers tie."
```

#### Agent 2 Skill — `deck_numbers_verifier` (code execution)

Your tenant exposes code execution as **Skills**. Build this one and attach it to Agent 2; the agent's job
is to **extract** figures from the deck (and the uploaded source model) into the Skill's `INPUT`, **run**
the Skill, then report only what the Skill proves. The Python does every calculation deterministically, so
the agent never does arithmetic in its head.

**Skill definition**
- **Name:** `deck_numbers_verifier`
- **Description:** Deterministically verifies a slide deck's numbers — sums/subtotals, CAGRs, percentages
  and margins, shares totalling 100%, the same figure repeated across slides, and slide-vs-source tie-outs.
- **When to use:** Whenever reviewing a deck's figures (Step 3 of the Numbers flow).
- **Inputs:** the `INPUT` object below, populated by the agent from the deck and uploaded source model.
- **Output:** a findings list (ERROR / CHECK BASIS / OK), each with the math shown and slide refs.

**The code** (paste as the Skill's code-execution body; if your Skill framework passes inputs as a JSON
argument instead of an inline literal, map the same fields):

```python
import json, math

# The agent fills INPUT from the deck (and the uploaded source model where available).
INPUT = {
    "tolerance_pct": 0.1,        # relative tolerance for rounding (% of the larger value)
    "absolute_tolerance": 0.05,  # absolute tolerance (covers 1-decimal rounding)
    "figures": [                 # any figure you can tie to the source model
        # {"slide": 12, "label": "FY24 EBITDA", "value": 42.1, "source_value": 44.6, "chart_read": False},
    ],
    "sum_checks": [              # totals/subtotals that should equal the sum of parts
        # {"slide": 15, "label": "Total revenue FY24", "total": 120.0, "parts": [40.0, 50.0, 30.5]},
    ],
    "cagr_checks": [            # stated growth rates to recompute
        # {"slide": 20, "label": "Revenue CAGR FY21-24", "begin": 80.0, "end": 120.0, "years": 3, "stated_cagr_pct": 14.5},
    ],
    "percentage_checks": [     # margins/ratios stated as a %
        # {"slide": 18, "label": "Gross margin FY24", "numerator": 72.0, "denominator": 120.0, "stated_pct": 62.0},
    ],
    "share_sum_checks": [      # breakdowns that should sum to ~100%
        # {"slide": 22, "label": "Revenue by region", "shares_pct": [45.0, 30.0, 20.0]},
    ],
    "consistency_checks": [    # the same fact appearing on multiple slides
        # {"label": "FY24 EBITDA", "occurrences": [{"slide": 12, "value": 42.1}, {"slide": 28, "value": 44.6}]},
    ],
}

REL_TOL = INPUT.get("tolerance_pct", 0.1) / 100.0
ABS_TOL = INPUT.get("absolute_tolerance", 0.05)

def close(a, b):
    if a is None or b is None:
        return None
    return abs(a - b) <= max(ABS_TOL, REL_TOL * max(abs(a), abs(b)))

findings = []
def add(verdict, kind, slide, label, detail):
    findings.append({"verdict": verdict, "check": kind, "slide": slide, "label": label, "detail": detail})

# 1. Sums / subtotals
for c in INPUT.get("sum_checks", []):
    parts = [p for p in c.get("parts", []) if p is not None]
    computed = round(sum(parts), 6)
    stated = c.get("total")
    add("OK" if close(computed, stated) else "ERROR", "sum", c.get("slide"), c.get("label"),
        f"parts {c.get('parts')} sum to {computed}; deck states {stated}")

# 2. CAGRs
for c in INPUT.get("cagr_checks", []):
    begin, end, years, stated = c.get("begin"), c.get("end"), c.get("years"), c.get("stated_cagr_pct")
    if not begin or begin <= 0 or not years or years <= 0 or end is None:
        add("CHECK BASIS", "cagr", c.get("slide"), c.get("label"),
            f"cannot compute from begin={begin}, end={end}, years={years}")
        continue
    computed = ((end / begin) ** (1.0 / years) - 1.0) * 100.0
    add("OK" if close(computed, stated) else "ERROR", "cagr", c.get("slide"), c.get("label"),
        f"({end}/{begin})^(1/{years})-1 = {computed:.2f}%; deck states {stated}%")

# 3. Percentages / margins / ratios
for c in INPUT.get("percentage_checks", []):
    num, den, stated = c.get("numerator"), c.get("denominator"), c.get("stated_pct")
    if den in (None, 0):
        add("CHECK BASIS", "percentage", c.get("slide"), c.get("label"),
            f"denominator missing/zero (num={num}, den={den})")
        continue
    computed = num / den * 100.0
    add("OK" if close(computed, stated) else "ERROR", "percentage", c.get("slide"), c.get("label"),
        f"{num}/{den}*100 = {computed:.2f}%; deck states {stated}%")

# 4. Shares should total ~100%
for c in INPUT.get("share_sum_checks", []):
    shares = [s for s in c.get("shares_pct", []) if s is not None]
    total = round(sum(shares), 6)
    add("OK" if close(total, 100.0) else "ERROR", "share_sum", c.get("slide"), c.get("label"),
        f"shares {c.get('shares_pct')} sum to {total}% (expected ~100%)")

# 5. Same fact, different number across slides
for c in INPUT.get("consistency_checks", []):
    occ = c.get("occurrences", [])
    vals = [o.get("value") for o in occ if o.get("value") is not None]
    ok = all(close(vals[0], v) for v in vals) if vals else True
    locs = "; ".join(f"slide {o.get('slide')}={o.get('value')}" for o in occ)
    add("OK" if ok else "ERROR", "consistency", None, c.get("label"),
        locs + ("" if ok else "   <-- figures differ"))

# 6. Slide vs source model tie-out
for f in INPUT.get("figures", []):
    sv = f.get("source_value")
    if sv is None:
        continue
    tag = " [chart-read]" if f.get("chart_read") else ""
    add("OK" if close(f.get("value"), sv) else "ERROR", "source_tie", f.get("slide"), f.get("label"),
        f"slide={f.get('value')} vs source={sv}{tag}")

# Report
order = {"ERROR": 0, "CHECK BASIS": 1, "OK": 2}
findings.sort(key=lambda x: order.get(x["verdict"], 3))
n_err = sum(1 for f in findings if f["verdict"] == "ERROR")
n_chk = sum(1 for f in findings if f["verdict"] == "CHECK BASIS")
print(f"NUMBERS VERIFICATION - {n_err} error(s), {n_chk} to check, {len(findings)-n_err-n_chk} OK\n")
for f in findings:
    where = f"slide {f['slide']}" if f["slide"] is not None else "multi-slide"
    print(f"[{f['verdict']}] {f['check']} | {where} | {f['label']}\n    {f['detail']}")
print("\nMACHINE-READABLE:\n" + json.dumps(findings, indent=2))
```

**Test it once** with this sample `INPUT` (it should report 3 errors and 1 OK): a margin of 72/120 = 60%
stated as 62% (ERROR), regional shares 45+30+20 = 95% (ERROR), FY24 EBITDA shown 42.1 vs 44.6 across
slides (ERROR), and a revenue CAGR 80->120 over 3 yrs = 14.47% stated 14.5% (OK).

```python
INPUT = {
    "cagr_checks": [{"slide": 20, "label": "Rev CAGR", "begin": 80.0, "end": 120.0, "years": 3, "stated_cagr_pct": 14.5}],
    "percentage_checks": [{"slide": 18, "label": "Gross margin", "numerator": 72.0, "denominator": 120.0, "stated_pct": 62.0}],
    "share_sum_checks": [{"slide": 22, "label": "Revenue by region", "shares_pct": [45.0, 30.0, 20.0]}],
    "consistency_checks": [{"label": "FY24 EBITDA", "occurrences": [{"slide": 12, "value": 42.1}, {"slide": 28, "value": 44.6}]}],
}
```

**Tuning:** `tolerance_pct` (default 0.1%) plus `absolute_tolerance` (0.05) absorb normal rounding while
still catching real errors. Loosen them if a deck legitimately rounds hard (e.g., whole-$M figures);
tighten for precision work. Step 4 then re-confirms each ERROR before it reaches the report.

With this Skill, Step 3 of the Numbers flow is **airtight on arithmetic**, not just on source tie-outs.

---

### AGENT 3 — RED-TEAM / COUNTERPARTY ATTACK (the hostile reader)

```
You are the sharpest, most skeptical reader this document will face — depending on the deck, that is the
buyer and their QoE/diligence advisors, the target's management, the board, or a rival bank trying to
win the mandate. You are not here to be encouraging. You are here to find every place this document is
weak, overstated, or exposed, and to phrase the questions that will be asked in the room.

TASK: Attack the attached deck. Surface the weaknesses, gaps, and overstatements a hostile expert reader
would exploit, and write the actual questions they would ask.

HOW TO WORK:
- Read the whole deck first, including footnotes and sources (and any grounding data attached).
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
   claims, synergy/cost-saving claims, "recurring/diversified" claims — anything asserted without
   evidence in the deck.
2. The equity story's soft spots — what does the thesis depend on that isn't proven here? Where would a
   skeptic say "prove it"?
3. Risks downplayed or missing — customer concentration, churn, key-person dependence, regulatory/
   litigation exposure, competitive threats, cyclicality. What would a buyer demand that isn't here?
4. Projections & add-backs — which assumptions are aggressive? Which EBITDA add-backs would a buyer
   reject? What happens to the story if you haircut the hockey stick?
5. Valuation — where are the comps or methodology vulnerable to "you cherry-picked"?
6. The killer questions — write the 10–15 toughest questions this reader would ask, in their words,
   grouped by theme, each tied to the slide that provokes it. Mark which 3 the deck currently has NO good
   answer to.

OUTPUT FORMAT:
1. "If I wanted to kill this, I'd start here" — the 3 most damaging lines of attack, one line each.
2. A table: Slide | Claim under attack (quoted) | The attack / why it's weak | What would blunt it.
3. "The 10–15 questions you'll be asked" — grouped by theme; flag the ones with no current answer.
4. "What's genuinely strong" — 2–4 points the deck defends well (so the team knows what to lean on).

FINAL STEP: drop any attack that's really just nitpicking or that the deck already answers elsewhere —
keep the ones that would actually land in the room.
```

---

### AGENT 4 — NARRATIVE & EQUITY-STORY COHERENCE

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
4. Sequencing — does the deck build the argument in a logical order, or assert the conclusion before
   establishing the premises?
5. Consistency of framing — company, market, and opportunity described the same way throughout (not
   "platform" on one slide and "point solution" on another)?
6. So-what gaps — slides full of data with no stated takeaway; where does the reader have to guess?

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

### AGENT 5 — DESIGN / BRAND / PROOFING PASS

```
You are a meticulous presentation-production editor ("deck doctor") at an investment bank — the last set
of eyes before a deck goes out. Your job on this pass is to catch design, branding, formatting, and
proofreading defects that make a deck look sloppy. At a bank, polish is read as a proxy for competence:
a typo or an inconsistent font plants subconscious doubt about the analysis itself. Ignore the substance
of the argument and the math on this pass — focus only on how the deck looks and reads.

ABOUT YOUR LIMITS (be honest): you reliably catch typos, placeholder text, inconsistent formatting, and
wording errors. You are NOT reliable at subtle pixel-level alignment or spacing. So flag obvious visual
problems, but for fine alignment/spacing mark the item "[verify visually]" rather than asserting it.

IF A HOUSE STYLE GUIDE IS ATTACHED (as grounding data): check the deck against it — approved fonts,
color values, logo lockup, title casing, disclaimer wording, page-layout rules. If none is attached,
check for INTERNAL consistency instead (everything matches everything else in the deck).

CHECK FOR:
1. Spelling & grammar — typos, grammatical errors, wrong word choices.
2. Name accuracy — the client/target/counterparty name spelled correctly and consistently EVERYWHERE
   (the single most embarrassing miss). Also people's names and titles.
3. Placeholder / leftover text — "[TBD]", "[Client]", "[•]", lorem ipsum, leftover text from a prior
   deck or template, "DRAFT" where it shouldn't be (or missing where it should).
4. Font & type consistency — consistent typeface, sizes, weights, colors for the same element types
   (titles, body, footnotes) across all slides.
5. Number & date formatting — consistent currency symbols, thousands separators, decimal places, units
   ($M vs $mm vs $000s), and date formats throughout.
6. Headings & titles — consistent capitalization style and structure; action titles vs label titles not
   mixed haphazardly.
7. Bullets & lists — consistent bullet style, indentation, punctuation (periods on all or none).
8. Page furniture — page numbers present, sequential, correct; the TOC/agenda matches the actual slides
   and page numbers; headers/footers consistent.
9. Footnotes & sources — consistent footnote style and numbering; source lines formatted the same way.
10. Charts & tables — legends, axis labels, and units present and legible; titles consistent; no cut-off
    or overflowing text.
11. Images & graphics — no stretched/distorted logos or photos; consistent treatment; nothing pixelated.
12. Confidentiality / draft markings — confidentiality legend present where required and consistent; the
    draft-status marking matches the deck's intended stage.

OUTPUT FORMAT:
1. "Global issues" — recurring problems affecting many slides (e.g., "two different title fonts used
   throughout"), listed ONCE with examples, so the report isn't 40 rows of the same thing.
2. A table for slide-specific issues, most severe first:
   Slide | Severity (CRITICAL = wrong name/placeholder shipped; MAJOR; MINOR) | Issue type | What's wrong
   (quoted or located) | Suggested fix
3. "Proofing verdict" — one line: is this clean enough to send, or are there must-fix items?

FINAL STEP: a human should still do a final visual proof — note that explicitly, and list anything you
were unsure about under "[verify visually]".
```

---

## 4. Optional add-on agents (say the word and I'll write them)

- **Compliance / disclaimer pass** — confidentiality legends, required disclaimers (no-reliance,
  forward-looking-statements safe harbor), draft-status marks, MNPI hygiene. (Some overlap with the
  design pass's item 12, but a dedicated legal-language pass goes deeper.)
- **Dedicated Pitch vs CIM variants** — two separate agents instead of the auto-detecting Master, if
  you'd rather. (The Master's STEP 0 already adapts, so this is only if you want them fully separate.)

---

## 5. Make it efficient: split the roles into a parallel "Master Reviewer" Flow

If you built one agent that does everything, it will be slow and hard to debug — that's the "one agent in
the flow" you're seeing, and a 20-minute run is usually a monolithic agent grinding through every check
serially (or stalled on a tool). Splitting the roles fixes all three problems. Build this in the Flow
builder:

**Shape:** Orchestrator → [5 lens subagents run in PARALLEL] → Synthesis/dedupe → one report.

**Run in PARALLEL (independent lenses — fan out):**
- **Numbers** subagent — runs the `deck_numbers_verifier` Skill (its own internal pipeline is sequential).
- **Red-Team** subagent.
- **Narrative** subagent.
- **Design** subagent.
- **Cross-cutting** subagent — contradictions across slides / narrative arc (needs the whole deck).

**Keep SEQUENTIAL only where a step needs the previous one:**
- Inside the Numbers subagent: extract → tie-to-source → run Skill → verify → report (each depends on the
  prior — can't be parallelized).
- The final **Synthesis** step: waits for all lens subagents, then dedupes and merges into one
  severity-sorted report in the Master's output format.

**Why this is better than one big agent:**
1. **Faster** — the lenses run concurrently instead of as one long chain.
2. **Debuggable** — if it hangs, you can see WHICH subagent stalled (you couldn't with a monolith).
3. **Higher quality** — single-responsibility subagents beat a mega-prompt. (The research's "curse of
   instructions": packing N checks into one prompt makes it silently drop some — reliability decays
   roughly as success-rate^N.)

**Build notes / caveats:**
- Attach **code execution** to the Numbers subagent; attach **non-confidential reference files** (style
  guide, comps rules, common-errors list) at the Master level — **never** confidential decks (see §0
  sharing rule). Upload the deck + source model **per run**.
- Pick **Gemini 3.1 Pro** for each subagent (Flash misses subtle errors).
- If your Flow builder turns out to run branches sequentially rather than truly concurrently, you still
  get the quality + debuggability win; as a fallback you can run the lens agents as separate agents in
  parallel browser sessions. (Confirm true parallel-branch support with the Automation team.)
- Publish the finished Master to the Agent Gallery so the desk has one "Review my deck" button.

---

## 6. Key sources behind these design choices

- Custom agents / Agent Designer (no-code, data stores, code execution, multi-step, sharing):
  docs.cloud.google.com/gemini/enterprise/docs/agent-designer; cloud.google.com/products/gemini-enterprise-agent-platform.
- Reducing false positives: evidence-quoting + give-it-an-out + self-critique; documented LLM
  over-correction (arxiv.org/html/2603.00539v1).
- Gemini vision limits (why numbers need verification/code execution): ~1-in-5 wrong on hard charts;
  >35% drop on noisy tables (arxiv.org/abs/2511.17238); <30% at catching misleading axes
  (arxiv.org/pdf/2509.18425).
- Anti-sycophancy: withhold authorship/opinion, neutral/question framing beats "be honest"
  (AISI arxiv.org/abs/2602.23971; Anthropic sycophancy work).
- Arithmetic: offload to code execution (PAL, arxiv.org/abs/2211.10435); grounding reduces hallucination.
- Review architecture: global pass + focused lenses + precision filter, then aggregate
  (prompt-chaining beats one mega-prompt, arxiv.org/abs/2406.00507).
- IB-materials checklist: pitch vs CIM red flags, "numbers that don't tie" as the worst-to-ship error,
  hockey-stick projections, aggressive add-backs, TAM inflation, comp drift, equity-story contradictions.

---

## 7. Appendix — Ask your company Gemini what you already have

Paste this into your internal/company Gemini (the one grounded on your org's IT and policy docs) to
confirm your setup before building. It maps 1:1 to what this toolkit needs.

```
You are my company's internal knowledge assistant, grounded on our IT, security, and policy
documentation. I'm building custom review agents in our Gemini Enterprise and need to confirm what our
organization has enabled. For EACH question, answer HAVE / DON'T HAVE / UNCLEAR, give the specific
detail, cite the internal source, and where you're unsure name the team or person I should ask.

1. EDITION & ACCESS — Which Gemini Enterprise edition/license do we have, and does it include custom
   agent building (Agent Designer)? Can someone in my role create and publish agents, or is that
   restricted to admins/specific groups? What's the approval process?
2. CODE EXECUTION — For a custom agent, can I enable a code-execution / data-analysis (Python) tool? If
   yes, how is it turned on, and are there restrictions?
3. DATA GROUNDING — Can I attach data sources / data stores (Google Drive, uploaded files, SharePoint, a
   data room) to a custom agent so it answers from those sources? Which connectors are enabled for us?
4. MULTI-STEP AGENTS — Are multi-step agents (an agent that orchestrates subagents) available to me?
5. MODELS — Which Gemini model(s) power our agents (e.g., Gemini 3 Pro / 3.1 Pro vs Flash)? Can I select
   the Pro / "thinking" model for an agent?
6. FILE HANDLING — Can an agent accept an uploaded PDF deck for analysis? Any file-size or page limits in
   our configuration?
7. DATA PROTECTION — For our Gemini Enterprise: is our content excluded from Google model training, and is
   there any human review? Do we have zero-data-retention and/or data-residency configured? Under policy,
   am I permitted to upload confidential client materials (e.g., CIMs, pitch decks) into these agents?
8. SHARING — Can I publish an agent to our Agent Gallery and share it with my team/department? Who
   controls that?
9. POLICY — What internal compliance or information-security rules must I follow when building an AI agent
   that processes confidential client documents?

Finish with a summary table: capability | HAVE/DON'T HAVE/UNCLEAR | detail | source | who to confirm with.
```

**Which answers are make-or-break for this toolkit:**
- **Must-have to start:** #3 grounding, #4 multi-step, #5 a Pro model, #6 PDF upload, #7 no-train + policy
  clearance for client docs. (You've already confirmed #3 and #4.)
- **The one upgrade to chase:** #2 code execution — turns the Numbers agent from "flag and verify" into
  "recompute and prove."
- If your company Gemini can't answer the infra items (#2, #5, #7), the **Google Workspace / Gemini
  admin** or your IT security team will have them.
```
