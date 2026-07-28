# Coverage pagers

Two-page company profiles for targets we may want to work with, built in the HL
house style (HL Refresh 2023 master).

| File | What it is |
|---|---|
| `GoldenSource_Coverage_Twopager.pptx` | GoldenSource — company profile (p.1) + market position and coverage angle (p.2) |
| `build_goldensource_pager.py` | Generator for the above |

## Rebuilding

```bash
python coverage/build_goldensource_pager.py /path/to/HL_template.pptx coverage/GoldenSource_Coverage_Twopager.pptx
```

The HL template is **not committed** — it carries the firm's "Strictly
Confidential. Not for Distribution." cover. Point the first argument at a local
copy of any deck on the HL Refresh 2023 master; the script deletes its slides and
inherits the master, theme, fonts and footer logo, so the output picks up HL
branding automatically.

## Style spec

Pulled from the template's own theme rather than approximated:

- **Page:** 10" x 7.5" (letter, 4:3) — HL's native size, not 16:9
- **Grid:** 0.25" outer margins, two 4.55" columns split at 5.20", content 1.60"–6.95"
- **Fonts:** Segoe UI Semibold (headers), Segoe UI (body) — the theme's major/minor pair
- **Colour:** navy `002855` (theme `dk2`) as the primary, deliberately *instead of*
  the royal blue `0067A5` the cover layouts use. Body copy `525766`, rules `BCBFC6`,
  slate `7E8597`, mid-blue `508BC9` for bullets, teal `24B1B1` reserved for the two
  "punchline" bullets
- **Type sizes:** everything on the page sits between 7pt and 11.5pt. The only
  exception is the slide title at 18pt, which is the template master's own spec

## Sourcing rules

Everything on the pages is public-record and footnoted on the slide. Two things
are explicitly flagged as third-party estimates rather than company figures:
headcount (~620) and revenue (~$63M). Confirm both in diligence before either
number goes in front of a client.
