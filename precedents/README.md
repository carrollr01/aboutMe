# Precedents — Deal Valuation Multiples Research

Researches whether a **revenue multiple or EV multiple was published — or can be
calculated from published information** — for a list of FinTech precedent
transactions. Complements the Tape (public comps) with a precedent-transaction
layer.

## What's here

| File | What it is |
|---|---|
| `deals.json` | The deduped deal list: 43 source rows → **35 unique deals** (34 researchable + 1 confidential "Project Lion"). Preserves original spellings in `as_given` and flags suspected typos / swapped parties in `search_hints` (e.g. CloudVerga→CloudVirga, Atlus→Altus, Walker Dunlap→Walker & Dunlop, Technisys/SoFi order swap). |
| `research_multiples.py` | The research script. For each deal it runs one Claude (`claude-opus-4-8`) pass with the server-side web-search tool: verify the parties → look for a published multiple (press release, investor deck, filing, reputable press) → if none, check whether deal value + target revenue/ARR/EBITDA are both public and compute the implied multiple → cite every figure. |
| `outputs/results/*.json` | One structured result per deal (verdict, multiples, calculation, sources, caveats). |
| `outputs/deal_multiples_summary.csv` / `.md` / `.xlsx` | Roll-up across all deals, rebuilt after every run. The `.xlsx` (needs `openpyxl`) has a hyperlinked primary source per deal plus an "All Sources" tab with every citation. |

## Running it

```sh
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...   # or `ant auth login`

python3 research_multiples.py --dry-run          # see the plan (no API calls)
python3 research_multiples.py --deal nasdaq-adenza   # smoke-test one deal
python3 research_multiples.py                    # research everything pending
python3 research_multiples.py --summarize-only   # rebuild the CSV/MD roll-up
```

Runs are **resumable**: each deal's result is saved as soon as it completes,
and already-done deals are skipped on the next run (use `--force` to redo).
A failed deal is reported and simply retried on the next invocation.

## Verdicts

| Verdict | Meaning |
|---|---|
| `published` | An EV or revenue multiple was stated explicitly in a credible source |
| `calculable` | Not published, but deal value and target financials are both public — implied multiple computed and shown |
| `partially_calculable` | One input is soft (unconfirmed press figure, earnout, unclear period) |
| `not_available` | Deal value or target financials are not public |

## Cost & model notes

- Model: `claude-opus-4-8` with adaptive thinking at **medium effort** and the
  `web_search_20260209` server tool, hard-capped at **3 searches per deal**
  (`--max-searches N` to raise it for a stubborn deal).
- The prompt makes the model plan its queries (one to confirm the deal, one for
  the multiple/financials, one held in reserve) instead of browsing, and to
  report unverified gaps in `notes` rather than burning searches or guessing.
- Expect roughly **$0.10–0.30 per deal** (~$4–10 for the full 34), dominated by
  Opus input tokens from search results. Use `--limit` to batch.
- The model is instructed to *verify* the search hints, not assume them — the
  per-deal JSON records how each typo/swap was resolved and its
  `identification_confidence`.
