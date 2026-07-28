"""Build the GoldenSource coverage two-pager on the Houlihan Lokey template.

Usage:  python build_goldensource_pager.py [path/to/HL_template.pptx] [out.pptx]

The HL template is NOT committed to this repo (it carries the firm's
"Strictly Confidential. Not for Distribution." cover). Point the first argument
at a local copy of the HL Refresh 2023 deck; the script inherits its master,
theme, fonts and footer logo, and writes only the two content pages.

Charts are native PowerPoint charts with embedded Excel workbooks; diagrams are
native shapes. Nothing on either page is a picture.
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_MARK
from pptx.oxml.ns import qn

SRC = sys.argv[1] if len(sys.argv) > 1 else "source.pptx"
OUT = sys.argv[2] if len(sys.argv) > 2 else "GoldenSource_Coverage_Twopager.pptx"

# ---------------------------------------------------------------- HL palette
NAVY = RGBColor(0x00, 0x28, 0x55)   # theme dk2 - primary for main slides
MID = RGBColor(0x50, 0x8B, 0xC9)    # theme accent1
GRAY = RGBColor(0x52, 0x57, 0x66)   # theme dk1 - body copy
SLATE = RGBColor(0x7E, 0x85, 0x97)  # theme accent3
LGRAY = RGBColor(0xBC, 0xBF, 0xC6)  # theme accent2 - rules
TEAL = RGBColor(0x24, 0xB1, 0xB1)   # theme accent4 - reserved for punchlines
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ROW = RGBColor(0xEE, 0xF2, 0xF7)    # table row striping only

# chevron progression, navy -> theme accent1
FLOW = [RGBColor(0x00, 0x28, 0x55), RGBColor(0x1C, 0x44, 0x70),
        RGBColor(0x38, 0x61, 0x8B), RGBColor(0x50, 0x8B, 0xC9)]

HEAD = "Segoe UI Semibold"
BODY = "Segoe UI"

# ------------------------------------------------------------------- geometry
LX = 0.25
FULL_W = 9.50
BAND_Y, BAND_H = 0.90, 0.58
BOT = 6.95
SEC_H = 0.24          # slim section header band
PAD = 0.10


# --------------------------------------------------------------------- helpers
def delete_all_slides(prs):
    lst = prs.slides._sldIdLst
    for sld in list(lst):
        prs.part.drop_rel(sld.get(qn("r:id")))
        lst.remove(sld)


def no_line(shape):
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def rect(slide, x, y, w, h, fill=None, shape=MSO_SHAPE.RECTANGLE):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    return no_line(sh)


def hairline(slide, x, y, w, color=LGRAY, weight=0.008):
    return rect(slide, x, y, w, weight, color)


def vrule(slide, x, y, h, color=LGRAY, weight=0.008):
    return rect(slide, x, y, weight, h, color)


def set_bullet(para, color=MID, char="▪", font="Arial", size_pct=90):
    """Attach a square bullet via pPr - never a literal character in the text."""
    pPr = para._p.get_or_add_pPr()
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buClr", "a:buFont", "a:buSzPct"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buClr = pPr.makeelement(qn("a:buClr"), {})
    buClr.append(pPr.makeelement(qn("a:srgbClr"), {"val": str(color)}))
    for el in (buClr,
               pPr.makeelement(qn("a:buSzPct"), {"val": str(size_pct * 1000)}),
               pPr.makeelement(qn("a:buFont"), {"typeface": font}),
               pPr.makeelement(qn("a:buChar"), {"char": char})):
        pPr.append(el)


def no_bullet(para):
    pPr = para._p.get_or_add_pPr()
    for tag in ("a:buChar", "a:buAutoNum", "a:buClr", "a:buFont", "a:buSzPct"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    if not pPr.findall(qn("a:buNone")):
        pPr.append(pPr.makeelement(qn("a:buNone"), {}))


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf


def write(tf, paras, size=8.0, color=GRAY, font=BODY, align=PP_ALIGN.LEFT,
          space_after=4, line_spacing=1.02):
    for i, spec in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = spec.get("align", align)
        p.line_spacing = spec.get("line_spacing", line_spacing)
        p.space_after = Pt(spec.get("space_after", space_after))
        p.space_before = Pt(spec.get("space_before", 0))
        pPr = p._p.get_or_add_pPr()
        if spec.get("bullet"):
            pPr.set("marL", str(int(Inches(0.115))))
            pPr.set("indent", str(int(-Inches(0.115))))
            set_bullet(p, color=spec.get("bullet_color", MID))
        else:
            pPr.set("marL", "0")
            pPr.set("indent", "0")
            no_bullet(p)
        for text, opts in spec["runs"]:
            r = p.add_run()
            r.text = text
            f = r.font
            f.name = opts.get("font", font)
            f.size = Pt(opts.get("size", size))
            f.bold = opts.get("bold", False)
            f.italic = opts.get("italic", False)
            f.color.rgb = opts.get("color", color)
    return tf


def plain(text, **opts):
    return {"runs": [(text, opts)]}


def lead(label, rest, **opts):
    """A bold navy lead-in followed by body copy, in one paragraph."""
    return {"runs": [(label, {"bold": True, "color": NAVY, "font": HEAD}), (rest, {})], **opts}


def section(slide, x, y, w, label):
    """Slim navy header band. Returns the y at which content should start."""
    rect(slide, x, y, w, SEC_H, NAVY)
    tf = textbox(slide, x + PAD, y, w - 2 * PAD, SEC_H, anchor=MSO_ANCHOR.MIDDLE)
    write(tf, [plain(label, bold=True, size=8.5, color=WHITE, font=HEAD)], space_after=0)
    return y + SEC_H + 0.10


def footnote(slide, text):
    tf = textbox(slide, 2.05, 7.10, 7.70, 0.38)
    write(tf, [plain(text, size=7, color=SLATE, italic=True)],
          space_after=0, line_spacing=1.0)


def page_frame(prs, layouts, title, eyebrow, takeaway):
    slide = prs.slides.add_slide(layouts["Title Only"])
    t = slide.shapes.title
    t.text_frame.word_wrap = False
    r = t.text_frame.paragraphs[0].add_run()
    r.text = title
    r.font.name, r.font.size, r.font.bold = HEAD, Pt(18), True
    r.font.color.rgb = NAVY

    tf = textbox(slide, 4.60, 0.40, 5.15, 0.30, anchor=MSO_ANCHOR.BOTTOM)
    write(tf, [plain(eyebrow, size=8.5, color=SLATE, italic=True)],
          align=PP_ALIGN.RIGHT, space_after=0)

    rect(slide, LX, BAND_Y, FULL_W, BAND_H, NAVY)
    tf = textbox(slide, LX + 0.14, BAND_Y, FULL_W - 0.28, BAND_H, anchor=MSO_ANCHOR.MIDDLE)
    write(tf, [plain(takeaway, size=9.5, color=WHITE, font=HEAD, bold=True)],
          space_after=0, line_spacing=1.06)
    return slide


# ------------------------------------------------------------------- zone art
def kpi_strip(slide, x, y, w, h, items):
    """Open stat row: navy rule on top, hairline dividers, no fills."""
    hairline(slide, x, y, w, NAVY, 0.014)
    cw = w / len(items)
    for i, (num, label) in enumerate(items):
        cx = x + i * cw
        if i:
            vrule(slide, cx, y + 0.08, h - 0.10)
        tf = textbox(slide, cx + 0.14, y + 0.07, cw - 0.28, 0.24, anchor=MSO_ANCHOR.TOP)
        write(tf, [plain(num, size=11.5, color=NAVY, bold=True, font=HEAD)], space_after=0)
        tf = textbox(slide, cx + 0.14, y + 0.31, cw - 0.28, h - 0.33)
        write(tf, [plain(label, size=7.5, color=GRAY)], space_after=0, line_spacing=1.0)


def kv_rows(slide, x, y, w, rows, label_w=0.95, size=7.5):
    """Striped key/value rows. rows: (label, value, n_lines)."""
    cy = y
    for i, (label, value, nlines) in enumerate(rows):
        h = 0.205 if nlines == 1 else 0.32
        if i % 2 == 0:
            rect(slide, x - 0.06, cy, w + 0.12, h, ROW)
        tf = textbox(slide, x, cy, label_w, h, anchor=MSO_ANCHOR.MIDDLE)
        write(tf, [plain(label, size=size, color=NAVY, bold=True, font=HEAD)], space_after=0)
        tf = textbox(slide, x + label_w, cy, w - label_w, h, anchor=MSO_ANCHOR.MIDDLE)
        write(tf, [plain(value, size=size, color=GRAY)], space_after=0, line_spacing=1.0)
        cy += h
    return cy


def flow_diagram(slide, x, y, w, h, stages, chev_h=0.34):
    """Chevron process flow with a module list under each stage."""
    n = len(stages)
    overlap = 0.10
    cw = (w + overlap * (n - 1)) / n
    for i, (title, modules) in enumerate(stages):
        cx = x + i * (cw - overlap)
        ch = rect(slide, cx, y, cw, chev_h, FLOW[i % len(FLOW)], MSO_SHAPE.CHEVRON)
        tf = ch.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.16)
        tf.margin_right = Inches(0.06)
        tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        write(tf, [plain(title, size=7.5, color=WHITE, bold=True, font=HEAD)],
              align=PP_ALIGN.CENTER, space_after=0)
        tf = textbox(slide, cx + 0.18, y + chev_h + 0.07, cw - 0.30, h - chev_h - 0.07)
        write(tf, [{"runs": [(m, {})], "space_after": 1.5, "bullet": True,
                    "bullet_color": FLOW[i % len(FLOW)]} for m in modules],
              size=7, line_spacing=1.0)


def timeline(slide, x, y, w, h, nodes, label_size=7, dot=0.10):
    """Horizontal spine with year nodes; each node captions below the line."""
    n = len(nodes)
    cw = w / n
    axis_y = y + 0.20
    hairline(slide, x + cw * 0.5, axis_y, w - cw, NAVY, 0.011)
    for i, node in enumerate(nodes):
        year, lines, accent = node
        cx = x + i * cw
        mid = cx + cw / 2
        color = TEAL if accent else NAVY
        d = rect(slide, mid - dot / 2, axis_y - dot / 2 + 0.005, dot, dot, color, MSO_SHAPE.OVAL)
        d.line.fill.solid()
        d.line.fill.fore_color.rgb = WHITE
        d.line.width = Pt(1)
        tf = textbox(slide, cx + 0.04, y - 0.02, cw - 0.08, 0.18, anchor=MSO_ANCHOR.BOTTOM)
        write(tf, [plain(year, size=8, color=color, bold=True, font=HEAD)],
              align=PP_ALIGN.CENTER, space_after=0)
        tf = textbox(slide, cx + 0.04, axis_y + 0.13, cw - 0.08, h - (axis_y - y) - 0.13)
        write(tf, [{"runs": [(t, {"bold": b, "color": color if b else GRAY,
                                  "font": HEAD if b else BODY})], "space_after": 0.5}
                   for t, b in lines],
              size=label_size, align=PP_ALIGN.CENTER, line_spacing=1.0)


def lanes(slide, x, y, w, h, rows, chip_w=1.24, gap=0.08):
    """Colour-chipped lanes: a category chip on the left, names on the right."""
    lh = (h - gap * (len(rows) - 1)) / len(rows)
    for i, (label, names) in enumerate(rows):
        ly = y + i * (lh + gap)
        chip = rect(slide, x, ly, chip_w, lh, FLOW[i % len(FLOW)])
        tf = chip.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.05)
        tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        write(tf, [plain(label, size=7, color=WHITE, bold=True, font=HEAD)],
              align=PP_ALIGN.CENTER, space_after=0, line_spacing=1.0)
        tf = textbox(slide, x + chip_w + 0.10, ly, w - chip_w - 0.10, lh,
                     anchor=MSO_ANCHOR.MIDDLE)
        write(tf, [plain(names, size=7.5, color=GRAY)], space_after=0, line_spacing=1.05)


def style_axes(chart, cat_size=7.5):
    chart.has_title = False
    chart.has_legend = False
    va = chart.value_axis
    va.visible = False
    va.has_major_gridlines = False
    ca = chart.category_axis
    ca.has_major_gridlines = False
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.format.line.color.rgb = LGRAY
    ca.tick_labels.font.size = Pt(cat_size)
    ca.tick_labels.font.color.rgb = GRAY
    ca.tick_labels.font.name = BODY


def native_chart(slide, kind, x, y, w, h, categories, values, colors,
                 number_format="General", label_pos=XL_LABEL_POSITION.OUTSIDE_END,
                 gap_width=70, cat_size=7.5):
    cd = CategoryChartData()
    cd.categories = categories
    cd.add_series("Series 1", values)
    gf = slide.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    chart = gf.chart
    style_axes(chart, cat_size)
    plot = chart.plots[0]
    plot.gap_width = gap_width
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.font.size = Pt(8)
    dl.font.bold = True
    dl.font.name = HEAD
    dl.font.color.rgb = NAVY
    dl.number_format = number_format
    dl.number_format_is_linked = False
    dl.position = label_pos
    ser = plot.series[0]
    for i, c in enumerate(colors):
        pt = ser.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = c
    return chart


# ================================================================ build deck
prs = Presentation(SRC)
delete_all_slides(prs)
layouts = {l.name: l for l in prs.slide_master.slide_layouts}

# ==================================================================== PAGE 1
s1 = page_frame(
    prs, layouts,
    "GoldenSource",
    "Coverage Profile  |  Data & Analytics  |  July 2026",
    "Forty-year enterprise data management franchise for capital markets — sponsor-owned "
    "since 2022, coming off a record 2025, and now repositioning its governed data layer as "
    "the control plane for AI in financial services",
)

# --- zone A: open KPI strip, full width
kpi_strip(s1, LX, 1.56, FULL_W, 0.56, [
    ("1984", "Founded — over 40 years in capital markets data"),
    ("100+", "Pre-built vendor data feeds and adaptors"),
    ("6", "Offices across North America, EMEA and APAC"),
    ("4 yrs", "Gemspring Capital hold period to date"),
])

# --- zone B: overview (wide left) + snapshot (narrow right)
cy = section(s1, LX, 2.24, 5.45, "COMPANY OVERVIEW")
tf = textbox(s1, LX + 0.02, cy, 5.41, 4.40 - cy)
write(tf, [
    {"bullet": True, "runs": [
        ("Founded in 1984 and headquartered in New York, GoldenSource is one of the original "
         "enterprise data management (EDM) vendors in capital markets and is widely credited "
         "with defining the category.", {})]},
    {"bullet": True, "runs": [
        ("Masters, governs and distributes securities, entity, counterparty, client, pricing, "
         "position, corporate-action and ESG data for banks, asset managers and insurers.", {})]},
    {"bullet": True, "runs": [
        ("One platform, two go-to-market lenses: the ", {}),
        ("Investment Data Platform", {"bold": True, "color": NAVY, "font": HEAD}),
        (" for the buy side and a ", {}),
        ("Trading, Risk and Regulatory Data Platform", {"bold": True, "color": NAVY, "font": HEAD}),
        (" for the sell side.", {})]},
    {"bullet": True, "runs": [
        ("Recurring subscription licence plus cloud hosting and managed services, deployed SaaS "
         "or on-premise; founding sponsor of the EDM Council.", {})]},
    {"bullet": True, "runs": [
        ("Leadership refreshed under sponsor ownership: James Corrigan became CEO in September "
         "2024, succeeding John Eley after a decade, with a Chief Customer Officer seat created "
         "in 2026.", {})]},
])

cy = section(s1, 5.80, 2.24, 3.95, "COMPANY SNAPSHOT")
kv_rows(s1, 5.86, cy - 0.03, 3.83, [
    ("Founded", "1984  |  New York, NY", 1),
    ("Ownership", "Gemspring Capital (May 2022); previously The Invus Group", 2),
    ("CEO", "James Corrigan (since Sept. 2024)", 1),
    ("Employees", "~620 est., versus 380 at the 2022 close", 1),
    ("Revenue", "~$63M est. (third-party; not company-reported)", 2),
    ("Offices", "New York, London, Milan, Mumbai, Melbourne, Hong Kong", 2),
    ("Delivery", "SaaS on AWS, Azure and GCP; AWS Marketplace; on-premise", 2),
])

# --- zone C: full-width platform flow diagram
cy = section(s1, LX, 4.58, FULL_W, "PLATFORM AND PRODUCT SUITE — HOW THE DATA MOVES")
flow_diagram(s1, LX, cy, FULL_W, 5.76 - cy, [
    ("SOURCE AND CONNECT", ["Connections and Adaptors", "100+ vendor feeds"]),
    ("MASTER AND GOVERN", ["Securities and Entity Master", "Price Master, corporate actions, ESG"]),
    ("DISTRIBUTE", ["Data Warehouse", "OMNI — Snowflake Native App", "Real-time IBOR"]),
    ("CONSUME AND REASON", ["Scout on Amazon Bedrock", "Chat plus MCP agent builder"]),
])

# --- zone D: milestone timeline (wide) + native headcount chart (narrow)
cy = section(s1, LX, 5.86, 6.05, "SELECTED MILESTONES")
timeline(s1, LX, cy, 6.05, BOT - cy, [
    ("1984", [("Founded in", False), ("New York", False)], False),
    ("2022", [("Gemspring buys", False), ("from Invus", False)], True),
    ("2023–24", [("IBOR, OMNI and", False), ("V10; new CEO", False)], False),
    ("2025", [("Record year;", False), ("flagship wins", False)], False),
    ("2026", [("Scout AI", False), ("launches", False)], False),
])

cy = section(s1, 6.55, 5.86, 3.20, "HEADCOUNT UNDER GEMSPRING")
native_chart(s1, XL_CHART_TYPE.COLUMN_CLUSTERED, 6.52, cy - 0.09, 3.26, BOT - cy + 0.05,
             ["2022", "2026E"], (380, 620), [SLATE, NAVY], gap_width=60)

footnote(s1, "Sources: GoldenSource and Gemspring Capital press releases; Businesswire; Finextra; "
             "WatersTechnology; company website. Employee and revenue figures are third-party "
             "estimates and are not company-reported — confirm in diligence.")

# ==================================================================== PAGE 2
s2 = page_frame(
    prs, layouts,
    "GoldenSource",
    "Market Position and Coverage Angle  |  July 2026",
    "The data layer is being re-underwritten for AI — and the category’s scaled "
    "independents have consolidated into strategic and sponsor hands over the last 36 months, "
    "leaving GoldenSource one of the few remaining at scale",
)

# --- zone A: demand drivers (wide) + native survey chart (narrow)
cy = section(s2, LX, 1.56, 5.45, "MARKET CONTEXT AND DEMAND DRIVERS")
tf = textbox(s2, LX + 0.02, cy, 5.41, 3.42 - cy)
write(tf, [
    {"bullet": True, "runs": [
        ("AI moved the buying centre. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Data governance is now a board line item rather than an operations budget: InvestOps "
         "2026 found 98% of firms concerned that poor data drives incorrect AI insights, because "
         "model output is only as defensible as the data underneath it.", {})]},
    {"bullet": True, "runs": [
        ("Regulatory and cost pressure is structural. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Rising vendor data costs, T+1, and widening entity, counterparty and ESG reporting "
         "obligations all reward a single mastered source.", {})]},
    {"bullet": True, "runs": [
        ("Cloud re-platforming reopened a mature category. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Snowflake and Databricks made “where the data lives” a live decision again, "
         "and vendors that ship natively into those environments earn a second look.", {})]},
    {"bullet": True, "runs": [
        ("Vendor consolidation cuts both ways. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Front-to-back platforms squeeze point solutions, but raise the premium on neutral, "
         "multi-vendor mastering that spans them.", {})]},
])

cy = section(s2, 5.80, 1.56, 3.95, "INDICATIVE BUYER UNIVERSE")
lanes(s2, 5.80, cy, 3.95, 3.42 - cy, [
    ("DATA STRATEGICS",
     "S&P Global, LSEG, FactSet, Bloomberg, Deutsche Börse (SimCorp)"),
    ("PLATFORM CONSOLIDATORS",
     "Clearwater Analytics, SS&C, Broadridge, FIS"),
    ("CATEGORY SPONSORS",
     "STG (Alveo, Gresham, S&P EDM), Eurazeo (NeoXam), large-cap software funds"),
])

# --- zone B: full-width consolidation timeline
cy = section(s2, LX, 3.52, FULL_W, "THE INDEPENDENTS HAVE CONSOLIDATED — SELECTED PRECEDENT TRANSACTIONS")
timeline(s2, LX, cy, FULL_W, 4.92 - cy, [
    ("May-22", [("GoldenSource", True), ("Gemspring Capital", False), ("n.d.", False)], True),
    ("Apr-23", [("SimCorp", True), ("Deutsche Börse", False), ("€3.9B", False)], False),
    ("Jul-24", [("Gresham Technologies", True), ("STG, with Alveo", False), ("£141.9M", False)], False),
    ("Oct-24", [("EZOPS", True), ("NeoXam (Eurazeo)", False), ("n.d.", False)], False),
    ("Jan-25", [("Enfusion", True), ("Clearwater Analytics", False), ("$1.5B", False)], False),
    ("Jan-26", [("S&P EDM / thinkFolio", True), ("STG / Gresham", False), ("n.d.", False)], False),
], label_size=7)

# --- zone C: landscape (narrow) + coverage angle (wide)
cy = section(s2, LX, 5.02, 3.95, "COMPETITIVE LANDSCAPE")
tf = textbox(s2, LX + 0.02, cy, 3.91, BOT - cy)
write(tf, [
    lead("Scaled strategics. ",
         "Bloomberg (Data License, PolarLake), FactSet, LSEG, SimCorp under Deutsche Börse, "
         "Clearwater after Enfusion.", bullet=True),
    lead("Sponsor-backed independents. ",
         "Gresham under STG — now the consolidator; NeoXam under Eurazeo; Rimes, Xceptor, "
         "Duco, Solidatus.", bullet=True),
    lead("Platform substitution. ",
         "In-house builds on Snowflake and Databricks lakehouses, packaged by integrators.",
         bullet=True),
    lead("GoldenSource. ",
         "One of the few independent, cross-asset, multi-vendor masters left carrying both a "
         "buy-side and a sell-side installed base.", bullet=True, bullet_color=TEAL),
], size=7.5, space_after=3)

cy = section(s2, 4.55, 5.02, 5.20, "COVERAGE ANGLE — WHY NOW")
tf = textbox(s2, 4.57, cy, 5.16, BOT - cy)
write(tf, [
    lead("Hold period. ",
         "Gemspring entered in May 2022. At four-plus years and off a record 2025, GoldenSource "
         "is squarely in the window for a sponsor-to-sponsor or strategic process.", bullet=True),
    lead("The story is fresh, not stale. ",
         "Scout, OMNI, V10 and the IBOR support a credible “modernised under this sponsor” "
         "narrative, with headcount up roughly 60% since close.", bullet=True),
    lead("Scarcity. ",
         "With S&P’s EDM franchise now inside STG/Gresham, the independent field is close "
         "to consolidated.", bullet=True),
    lead("Test in diligence. ",
         "Licence versus services mix; cloud ARR share against on-premise maintenance; net "
         "revenue retention; and how much of Scout has shipped.", bullet=True),
    lead("Houlihan Lokey is already in this market. ",
         "Rule 3 adviser to Gresham on its 2024 take-private by STG, and co-adviser to "
         "STG/Gresham on the 2026 S&P EDM and thinkFolio carve-out.",
         bullet=True, bullet_color=TEAL),
], size=7.5, space_after=3)

footnote(s2, "Sources: Houlihan Lokey transaction disclosures; S&P Global, Clearwater Analytics, "
             "Deutsche Börse and STG press releases; Businesswire; Finextra; A-Team Insight; "
             "InvestOps 2026. Values as disclosed; n.d. = not disclosed. Buyer universe is HL "
             "analysis, not a disclosed or solicited process.")

prs.save(OUT)
print("wrote", OUT)
