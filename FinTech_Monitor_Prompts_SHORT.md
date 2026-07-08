# FinTech Monitor — Prompts (short, locked)
*Compressed standing prompts. Same rules as v2.1, ~1/3 the length.*

## Prompt A — Subsector brief (run per sector, swap {{SUBSECTOR}})
```
Write the weekly brief for Sector = {{SUBSECTOR}} only. Sources: deal log, Tape, Thesis Ledger, voice reference.

Open: "[N] deals. $X primary (equity only) / $Y M&A / $Z debt." Count all real deals incl. Context/Watch; exclude special situations (report as "plus N special situation"). Never blend the numbers.

Narrative (voice-ref style): lead with the non-obvious signal, not the biggest deal; short flowing sentences; no filler closers; end on one dated, falsifiable forecast ("Our bet: by 2029…"). Never invent a statistic.

Ledger: score each open {{SUBSECTOR}} thesis CONFIRMS/CONTRADICTS/NEUTRAL + adjust confidence, citing the deal. New thesis only if directional with >=2 points or a non-obvious 1-point "watch"; never restate one deal as a thesis; else leave unchanged.

Numbers from the Tape or write "[Tape: __]". Cite a source per deal.
```

## Prompt B — Cross-sector synthesis (run once, last)
```
Write the cross-sector synthesis — a take, not a recap. Sources: full deal log, Tape, Thesis Ledger, the 8 subsector briefs.

1. Headline: "[N] deals across [k] sectors. $X primary / $Y M&A. [one-sentence thesis]."
2. The one read (3-4 sentences).
3. The unnamed trend: name one signal crossing >=2 sectors or hiding in a Context/Watch deal; why it matters in 2-3 yrs. This is the point — don't skip.
4. Themes in >=2 sectors (list deals + status).
5. Rotation: from the Tape; if absent, say it can't be computed.
6. Cross-Sector ledger update.

Never invent figures; frame forward bets as forecasts. Cite sources.
```

---
## Even shorter (optional): make it a one-liner
Upload these prompts as a source named **"House Rules — instructions, not data."** Then each
weekly run is just:
- `Write the {{SUBSECTOR}} brief per House Rules.`
- `Write the cross-sector synthesis per House Rules.`
NotebookLM reads the rules from the source, so you never paste them again.
