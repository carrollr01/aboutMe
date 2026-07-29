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
- **Margins:** 0.25" outer, content 1.52"–6.95", source note in the master's footer slot
- **Fonts:** Segoe UI Semibold (headers), Segoe UI (body) — the theme's major/minor pair
- **Colour:** navy `002855` (theme `dk2`) as the primary, deliberately *instead of*
  the royal blue `0067A5` the cover layouts use. Body copy `525766`, rules `BCBFC6`,
  slate `7E8597`, mid-blue `508BC9`, teal `24B1B1` reserved for the "punchline" bullets.
  Bodies are white — the only tint is row striping in the snapshot table
- **Type sizes:** everything on the page sits between 7pt and 11.5pt. The only
  exception is the slide title at 18pt, which is the template master's own spec

## Layout

The two pages use deliberately different zone structures so they don't read as
one template applied twice:

| | Page 1 | Page 2 |
|---|---|---|
| Zone A | Open KPI strip, full width | Demand-driver bullets + survey bar chart |
| Zone B | Overview (wide) + snapshot table (narrow) | Full-width consolidation timeline |
| Zone C | Full-width chevron flow diagram | Landscape (narrow) + coverage angle (wide) |
| Zone D | Milestone timeline + headcount column chart | — |

Everything visual is native: the chevron flow and both timelines are PowerPoint
shapes, and the two charts are real PowerPoint charts with embedded Excel
workbooks (`ppt/embeddings/Microsoft_Excel_Sheet*.xlsx`) — double-click to edit
the data in place. No pictures anywhere.

## Sourcing rules

Everything on the pages is public-record and footnoted on the slide. Two things
are explicitly flagged as third-party estimates rather than company figures:
headcount (~620) and revenue (~$63M). Confirm both in diligence before either
number goes in front of a client.

## Changing the icon colour

The five product icons are generated, not hand-drawn. Pass a hex to the
generator and rerun the build:

```bash
cd coverage
node gen_icons.js "#FFFFFF"                       # recolour all five
python build_goldensource_pager.py /path/to/HL_template.pptx
```

HL theme options: `9FC3DA` pale blue (accent6, current) · `508BC9` mid blue
(accent1) · `24B1B1` teal (accent4) · `BCBFC6` light grey (accent2) · `FFFFFF`.

For per-icon colours, edit the `icons` array in `gen_icons.js` — each row is
`[slug, IconComponent, colour]`, so they do not have to match. Icon shapes come
from `react-icons/tb` (Tabler); swap `Tb.TbDatabase` for any other export to
change the glyph.

In PowerPoint without rerunning anything: click an icon, then Graphics Format >
Graphics Fill. The icons are inserted as SVG graphics the same way PowerPoint's
own Insert > Icons does - an `<a:blip>` carrying an `asvg:svgBlip` extension,
with the PNG as the fallback for renderers that do not support SVG. Shapes are
named "Icon <product>" in the selection pane. Right-click > Convert to Shape
turns one into editable freeform paths if you need to recolour part of a glyph.
