# FinTech Monitor

The narrative layer: thesis-driven weekly briefs written in NotebookLM against one corpus
(the weekly deal log, the Tape summary, the Thesis Ledger, prior issues, and a voice
reference). Nine runs per week: 8 subsector briefs + 1 cross-sector synthesis.

- `design/` — the product plan (why this exists, the Tape/Narrative/Board layers) and the
  starter kit (the concrete Excel → NotebookLM → agent build).
- `prompts/` — everything needed to run a week: the full run guide, the house rules
  (method, not data — governs voice, dollar conventions, ledger discipline), the standing
  prompts (`Prompts_v2` full-length, `Prompts_SHORT` compressed equivalent), and the voice
  reference benchmark (style only, never data).
- `sources/` — the grounding documents uploaded to the notebook: weekly deal logs and the
  master Thesis Ledger (the living state that carries week to week).
- `issues/` — finished output: published Monitor issues and the InsurTech pilot dry run
  that validated the voice.
