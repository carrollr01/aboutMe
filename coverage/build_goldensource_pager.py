"""Build the GoldenSource coverage two-pager on the Houlihan Lokey template.

Usage:  python build_goldensource_pager.py [path/to/HL_template.pptx] [out.pptx]

The HL template is NOT committed to this repo (it carries the firm's
"Strictly Confidential. Not for Distribution." cover). Point the first argument
at a local copy of the HL Refresh 2023 deck; the script inherits its master,
theme, fonts and footer logo, and writes only the two content pages.
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

SRC = sys.argv[1] if len(sys.argv) > 1 else "source.pptx"
OUT = sys.argv[2] if len(sys.argv) > 2 else "GoldenSource_Coverage_Twopager.pptx"

# ---------------------------------------------------------------- HL palette
NAVY = RGBColor(0x00, 0x28, 0x55)   # theme dk2 - primary for main slides
MID = RGBColor(0x50, 0x8B, 0xC9)    # theme accent1
PALE = RGBColor(0x9F, 0xC3, 0xDA)   # theme accent6
GRAY = RGBColor(0x52, 0x57, 0x66)   # theme dk1 - body copy
SLATE = RGBColor(0x7E, 0x85, 0x97)  # theme accent3
LGRAY = RGBColor(0xBC, 0xBF, 0xC6)  # theme accent2 - rules
TEAL = RGBColor(0x24, 0xB1, 0xB1)   # theme accent4 - sparing accent
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TINT = RGBColor(0xF3, 0xF6, 0xFA)   # body fill for content boxes
TINT2 = RGBColor(0xE8, 0xEE, 0xF5)  # alternating row fill

HEAD = "Segoe UI Semibold"
BODY = "Segoe UI"

# ------------------------------------------------------------------- geometry
LX, RX, COL_W = 0.25, 5.20, 4.55
BAND_Y, BAND_H = 0.90, 0.58
TOP = 1.60
BOT = 6.95
HDR_H = 0.30
PAD = 0.11


# --------------------------------------------------------------------- helpers
def delete_all_slides(prs):
    lst = prs.slides._sldIdLst
    for sld in list(lst):
        prs.part.drop_rel(sld.get(qn("r:id")))
        lst.remove(sld)


def no_line(shape):
    shape.line.fill.background()
    shape.shadow.inherit = False


def rect(slide, x, y, w, h, fill=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    no_line(sh)
    return sh


def set_bullet(para, char="▪", color=MID, font="Arial", size_pct=90):
    """Attach a square bullet to a paragraph via pPr (never a literal char in the text)."""
    pPr = para._p.get_or_add_pPr()
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buClr", "a:buFont", "a:buSzPct"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buClr = pPr.makeelement(qn("a:buClr"), {})
    srgb = pPr.makeelement(qn("a:srgbClr"), {"val": str(color)})
    buClr.append(srgb)
    buSz = pPr.makeelement(qn("a:buSzPct"), {"val": str(size_pct * 1000)})
    buFont = pPr.makeelement(qn("a:buFont"), {"typeface": font})
    buChar = pPr.makeelement(qn("a:buChar"), {"char": char})
    for el in (buClr, buSz, buFont, buChar):
        pPr.append(el)


def no_bullet(para):
    pPr = para._p.get_or_add_pPr()
    for tag in ("a:buChar", "a:buAutoNum", "a:buClr", "a:buFont", "a:buSzPct"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    if not pPr.findall(qn("a:buNone")):
        pPr.append(pPr.makeelement(qn("a:buNone"), {}))


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf


def write(tf, paras, size=8.5, color=GRAY, font=BODY, align=PP_ALIGN.LEFT,
          space_after=4, line_spacing=1.02):
    """paras: list of dicts -> {runs:[(text, opts)], bullet:bool, indent:float,
                                space_before:pt, space_after:pt, align:}"""
    for i, spec in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = spec.get("align", align)
        p.line_spacing = spec.get("line_spacing", line_spacing)
        p.space_after = Pt(spec.get("space_after", space_after))
        p.space_before = Pt(spec.get("space_before", 0))
        indent = spec.get("indent", 0.0)
        if spec.get("bullet"):
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(int(Inches(indent + 0.115))))
            pPr.set("indent", str(int(-Inches(0.115))))
            set_bullet(p, color=spec.get("bullet_color", MID))
        else:
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(int(Inches(indent))))
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


def content_box(slide, x, y, w, h, title, body_fill=TINT):
    """Navy header band + tinted body. Returns (bx, by, bw, bh) of the inner body area."""
    rect(slide, x, y, w, HDR_H, NAVY)
    tf = textbox(slide, x + PAD, y, w - 2 * PAD, HDR_H, anchor=MSO_ANCHOR.MIDDLE)
    write(tf, [plain(title, bold=True, size=9, color=WHITE, font=HEAD)],
          align=PP_ALIGN.CENTER, space_after=0)
    rect(slide, x, y + HDR_H, w, h - HDR_H, body_fill)
    return (x + PAD, y + HDR_H + 0.09, w - 2 * PAD, h - HDR_H - 0.18)


def page_frame(prs, layouts, title, eyebrow, takeaway):
    slide = prs.slides.add_slide(layouts["Title Only"])
    t = slide.shapes.title
    t.text_frame.word_wrap = False
    p = t.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = title
    r.font.name = HEAD
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = NAVY

    tf = textbox(slide, 4.60, 0.40, 5.15, 0.30, anchor=MSO_ANCHOR.BOTTOM)
    write(tf, [plain(eyebrow, size=8.5, color=SLATE, italic=True)],
          align=PP_ALIGN.RIGHT, space_after=0)

    rect(slide, LX, BAND_Y, 9.5, BAND_H, NAVY)
    tf = textbox(slide, LX + 0.14, BAND_Y, 9.5 - 0.28, BAND_H, anchor=MSO_ANCHOR.MIDDLE)
    write(tf, [plain(takeaway, size=9.5, color=WHITE, font=HEAD, bold=True)],
          space_after=0, line_spacing=1.06)
    return slide


def footnote(slide, text):
    tf = textbox(slide, 2.05, 7.10, 7.70, 0.38)
    write(tf, [plain(text, size=7, color=SLATE, italic=True)],
          space_after=0, line_spacing=1.0)


def kv_table(slide, x, y, w, rows, label_w=1.02, row_h=0.215, tall_h=0.335, size=7.5):
    """Alternating-fill key/value rows. rows: (label, value, n_lines)."""
    cy = y
    for i, (label, value, nlines) in enumerate(rows):
        h = row_h if nlines == 1 else tall_h
        if i % 2 == 0:
            rect(slide, x - PAD + 0.02, cy, w + 2 * PAD - 0.04, h, TINT2)
        tf = textbox(slide, x, cy, label_w, h, anchor=MSO_ANCHOR.MIDDLE)
        write(tf, [plain(label, size=size, color=NAVY, bold=True, font=HEAD)], space_after=0)
        tf = textbox(slide, x + label_w, cy, w - label_w, h, anchor=MSO_ANCHOR.MIDDLE)
        write(tf, [plain(value, size=size, color=GRAY)], space_after=0, line_spacing=1.0)
        cy += h
    return cy


def stat_tiles(slide, x, y, w, h, tiles, gap=0.12):
    tw = (w - gap * (len(tiles) - 1)) / len(tiles)
    for i, (num, label) in enumerate(tiles):
        tx = x + i * (tw + gap)
        rect(slide, tx, y, tw, h, WHITE)
        tf = textbox(slide, tx + 0.06, y + 0.04, tw - 0.12, 0.24,
                     anchor=MSO_ANCHOR.MIDDLE, wrap=False)
        write(tf, [plain(num, size=11.5, color=NAVY, bold=True, font=HEAD)],
              align=PP_ALIGN.CENTER, space_after=0)
        tf = textbox(slide, tx + 0.06, y + 0.28, tw - 0.12, h - 0.33, anchor=MSO_ANCHOR.TOP)
        write(tf, [plain(label, size=7, color=GRAY)],
              align=PP_ALIGN.CENTER, space_after=0, line_spacing=1.0)


def txn_table(slide, x, y, w, rows, size=7.5, head_h=0.22, row_h=0.30):
    """Precedent-transaction table: Date | Target | Acquirer | Value."""
    cols = [0.48, 1.56, 1.42, 0.87]           # sums to 4.33
    scale = (w - 0.0) / sum(cols)
    cols = [c * scale for c in cols]
    heads = ["Date", "Target", "Acquirer / Sponsor", "Value"]
    cx = x
    for c, htxt in zip(cols, heads):
        tf = textbox(slide, cx, y, c - 0.06, head_h, anchor=MSO_ANCHOR.BOTTOM)
        write(tf, [plain(htxt, size=7.5, color=NAVY, bold=True, font=HEAD)], space_after=0)
        cx += c
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y + head_h + 0.015),
                                Inches(w), Inches(0.011))
    ln.fill.solid()
    ln.fill.fore_color.rgb = NAVY
    no_line(ln)

    cy = y + head_h + 0.06
    for i, row in enumerate(rows):
        if i % 2 == 0:
            rect(slide, x - 0.05, cy, w + 0.10, row_h, TINT2)
        cx = x
        for j, (c, cell) in enumerate(zip(cols, row)):
            bold = (j == 1)
            tf = textbox(slide, cx, cy, c - 0.06, row_h, anchor=MSO_ANCHOR.MIDDLE)
            write(tf, [plain(cell, size=size, color=NAVY if bold else GRAY, bold=bold,
                             font=HEAD if bold else BODY)],
                  space_after=0, line_spacing=1.0)
            cx += c
        cy += row_h
    return cy


# ================================================================ build deck
prs = Presentation(SRC)
delete_all_slides(prs)
layouts = {l.name: l for l in prs.slide_master.slide_layouts}

# ------------------------------------------------------------------- PAGE 1
s1 = page_frame(
    prs, layouts,
    "GoldenSource",
    "Coverage Profile  |  Data & Analytics  |  July 2026",
    "Forty-year enterprise data management franchise for capital markets — sponsor-owned "
    "since 2022, coming off a record 2025, and now repositioning its governed data layer as "
    "the control plane for AI in financial services",
)

# Left: company overview
bx, by, bw, bh = content_box(s1, LX, TOP, COL_W, 2.50, "COMPANY OVERVIEW")
tf = textbox(s1, bx, by, bw, bh)
write(tf, [
    {"bullet": True, "runs": [
        ("Founded in 1984 and headquartered in New York, GoldenSource is one of the original "
         "enterprise data management (EDM) vendors in capital markets and is widely credited "
         "with defining the category.", {})]},
    {"bullet": True, "runs": [
        ("Masters, governs and distributes securities, entity, counterparty, client, pricing, "
         "position, corporate-action and ESG data for banks, asset managers and insurers, with "
         "100+ pre-built vendor feeds.", {})]},
    {"bullet": True, "runs": [
        ("One platform, two go-to-market lenses: the ", {}),
        ("Investment Data Platform", {"bold": True, "color": NAVY, "font": HEAD}),
        (" for the buy side and a ", {}),
        ("Trading, Risk and Regulatory Data Platform", {"bold": True, "color": NAVY, "font": HEAD}),
        (" for the sell side.", {})]},
    {"bullet": True, "runs": [
        ("Recurring subscription licence plus cloud hosting and managed services, SaaS or "
         "on-premise; founding sponsor of the EDM Council.", {})]},
    {"bullet": True, "runs": [
        ("Leadership refreshed under sponsor ownership: James Corrigan became CEO in September "
         "2024, succeeding John Eley after a decade, with a Chief Customer Officer seat created "
         "in 2026.", {})]},
], size=8.0)

# Left: platform
bx, by, bw, bh = content_box(s1, LX, TOP + 2.62, COL_W, BOT - (TOP + 2.62), "PLATFORM AND PRODUCT SUITE")
tf = textbox(s1, bx, by, bw, bh)
write(tf, [
    {"bullet": True, "runs": [
        ("Mastering. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Securities Master across all asset classes and ESG-enabled; Customer and entity "
         "master; Price Master and valuations; corporate actions.", {})]},
    {"bullet": True, "runs": [
        ("Distribution. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Connections and Adaptors for vendor onboarding, the GoldenSource Data Warehouse, and "
         "OMNI — a Snowflake Native App that runs the GoldenSource data model inside a "
         "client’s own Snowflake account.", {})]},
    {"bullet": True, "runs": [
        ("Real time. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("GoldenSource IBOR, a real-time investment book of record launched in 2023.", {})]},
    {"bullet": True, "runs": [
        ("AI. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Scout, launched June 2026 — a “Trusted Contextual Data Layer” with a "
         "chat interface and an MCP-based agent builder, deployed on Amazon Bedrock for "
         "auditability and access control.", {})]},
    {"bullet": True, "runs": [
        ("Platform. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("V10 (October 2024) is cloud-agnostic across AWS, Azure and GCP and is listed in AWS "
         "Marketplace, alongside a maintained on-premise estate.", {})]},
], size=8.0)

# Right: snapshot
bx, by, bw, bh = content_box(s1, RX, TOP, COL_W, 2.50, "COMPANY SNAPSHOT")
kv_table(s1, bx, by - 0.02, bw, [
    ("Founded", "1984  |  Headquartered in New York, NY", 1),
    ("Ownership", "Gemspring Capital (May 2022); previously The Invus Group", 2),
    ("CEO", "James Corrigan (since September 2024)", 1),
    ("Employees", "~620 estimated, versus 380 at the 2022 close", 1),
    ("Revenue", "~$63M estimated (third-party sources; not company-reported)", 2),
    ("Offices", "New York, London, Milan, Mumbai, Melbourne, Hong Kong", 2),
    ("Delivery", "SaaS on AWS, Azure and GCP; AWS Marketplace; on-premise", 2),
])

# Right: milestones
bx, by, bw, bh = content_box(s1, RX, TOP + 2.62, COL_W, 1.72, "SELECTED MILESTONES")
tf = textbox(s1, bx, by, bw, bh)
write(tf, [
    {"runs": [("1984 — ", {"bold": True, "color": NAVY, "font": HEAD}),
              ("Founded in New York; helps establish the EDM category.", {})]},
    {"runs": [("2022 — ", {"bold": True, "color": NAVY, "font": HEAD}),
              ("Gemspring Capital acquires the business from The Invus Group.", {})]},
    {"runs": [("2023–24 — ", {"bold": True, "color": NAVY, "font": HEAD}),
              ("Real-time IBOR launches; OMNI goes live as a Snowflake Native App; V10 ships; "
               "new CEO appointed.", {})]},
    {"runs": [("2025 — ", {"bold": True, "color": NAVY, "font": HEAD}),
              ("Record year, with Q4 wins including a $500B+ global asset manager, a U.S. "
               "super-regional bank and a European multinational bank.", {})]},
    {"runs": [("2026 — ", {"bold": True, "color": NAVY, "font": HEAD}),
              ("Scout AI platform launches on Amazon Bedrock; Chief Customer Officer seat "
               "created.", {})]},
], size=7.5, space_after=3.5)

# Right: momentum tiles
bx, by, bw, bh = content_box(s1, RX, TOP + 4.46, COL_W, BOT - (TOP + 4.46), "MOMENTUM MARKERS")
stat_tiles(s1, bx, by - 0.02, bw, bh - 0.01, [
    ("~620", "Employees, from 380 at the 2022 close"),
    ("3", "Flagship Q4 2025 platform wins"),
    ("4 yrs", "Gemspring hold as of July 2026"),
])

footnote(s1, "Sources: GoldenSource and Gemspring Capital press releases; Businesswire; Finextra; "
             "WatersTechnology; company website. Employee and revenue figures are third-party "
             "estimates and are not company-reported — confirm in diligence.")

# ------------------------------------------------------------------- PAGE 2
s2 = page_frame(
    prs, layouts,
    "GoldenSource",
    "Market Position and Coverage Angle  |  July 2026",
    "The data layer is being re-underwritten for AI — and the category’s scaled "
    "independents have consolidated into strategic and sponsor hands over the last 36 months, "
    "leaving GoldenSource one of the few remaining at scale",
)

# Left: market context
bx, by, bw, bh = content_box(s2, LX, TOP, COL_W, 2.50, "MARKET CONTEXT AND DEMAND DRIVERS")
tf = textbox(s2, bx, by, bw, bh)
write(tf, [
    {"bullet": True, "runs": [
        ("AI moved the buying centre. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("InvestOps 2026 found 98% of firms concerned that poor data yields incorrect AI "
         "insights, and 55% put at least half a basis point of annualised performance at risk. "
         "Data governance is now a board line item, not an operations budget.", {})]},
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
], size=8.0)

# Left: competitive landscape
bx, by, bw, bh = content_box(s2, LX, TOP + 2.62, COL_W, BOT - (TOP + 2.62), "COMPETITIVE LANDSCAPE")
tf = textbox(s2, bx, by, bw, bh)
write(tf, [
    {"runs": [("Scaled strategics and platform owners", {"bold": True, "color": NAVY, "font": HEAD})],
     "space_after": 1.5},
    {"bullet": True, "runs": [
        ("Bloomberg (Data License, PolarLake), FactSet, LSEG, SimCorp under Deutsche Börse, "
         "and Clearwater Analytics following Enfusion.", {})]},
    {"runs": [("Sponsor-backed independents", {"bold": True, "color": NAVY, "font": HEAD})],
     "space_after": 1.5, "space_before": 3},
    {"bullet": True, "runs": [
        ("Gresham under STG — now the sector consolidator, having absorbed Alveo and, in "
         "January 2026, S&P Global’s EDM and thinkFolio businesses; NeoXam under Eurazeo; "
         "plus Rimes, Xceptor, Duco and Solidatus.", {})]},
    {"runs": [("Platform substitution", {"bold": True, "color": NAVY, "font": HEAD})],
     "space_after": 1.5, "space_before": 3},
    {"bullet": True, "runs": [
        ("In-house builds on Snowflake and Databricks lakehouses, often packaged by systems "
         "integrators — the principal budget alternative rather than a like-for-like rival.", {})]},
    {"runs": [("Where GoldenSource sits", {"bold": True, "color": NAVY, "font": HEAD})],
     "space_after": 1.5, "space_before": 3},
    {"bullet": True, "runs": [
        ("One of a shrinking set of independent, cross-asset, multi-vendor masters carrying both "
         "a buy-side and a sell-side installed base — the profile a strategic buys rather "
         "than builds.", {})], "bullet_color": TEAL},
], size=8.0, space_after=3)

# Right: precedent transactions
bx, by, bw, bh = content_box(s2, RX, TOP, COL_W, 2.50, "SELECTED PRECEDENT TRANSACTIONS")
txn_table(s2, bx, by - 0.02, bw, [
    ("Jan-26", "S&P Global EDM / thinkFolio", "STG / Gresham", "n.d."),
    ("Jan-25", "Enfusion", "Clearwater Analytics", "$1.5B"),
    ("Oct-24", "EZOPS", "NeoXam (Eurazeo)", "n.d."),
    ("Jul-24", "Gresham Technologies", "STG (with Alveo)", "£141.9M"),
    ("Apr-23", "SimCorp", "Deutsche Börse", "€3.9B"),
    ("May-22", "GoldenSource", "Gemspring Capital", "n.d."),
])

# Right: coverage angle
bx, by, bw, bh = content_box(s2, RX, TOP + 2.62, COL_W, BOT - (TOP + 2.62), "COVERAGE ANGLE — WHY NOW")
tf = textbox(s2, bx, by, bw, bh)
write(tf, [
    {"bullet": True, "runs": [
        ("Hold period. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Gemspring entered in May 2022. At four-plus years and off a record 2025, GoldenSource "
         "sits squarely in the window for a sponsor-to-sponsor or strategic process.", {})]},
    {"bullet": True, "runs": [
        ("The story is fresh, not stale. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Scout, OMNI, V10 and the IBOR support a credible “modernised under this "
         "sponsor” narrative, with headcount up roughly 60% since close.", {})]},
    {"bullet": True, "runs": [
        ("Scarcity. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("With S&P’s EDM franchise now inside STG/Gresham, the independent field is close "
         "to consolidated — which raises the option value of the assets left.", {})]},
    {"bullet": True, "runs": [
        ("Diligence themes to test. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Licence versus services mix and gross margin; cloud ARR share against on-premise "
         "maintenance; net revenue retention; and how much of Scout is shipped rather than "
         "announced.", {})]},
    {"bullet": True, "runs": [
        ("Houlihan Lokey is already in this market. ", {"bold": True, "color": NAVY, "font": HEAD}),
        ("Sole and Rule 3 adviser to Gresham Technologies on its 2024 take-private by STG, and "
         "co-adviser to STG and Gresham on the 2026 carve-out of S&P Global’s EDM and "
         "thinkFolio businesses.", {})], "bullet_color": TEAL},
], size=8.0)

footnote(s2, "Sources: Houlihan Lokey transaction disclosures; S&P Global, Clearwater Analytics, "
             "Deutsche Börse and STG press releases; Businesswire; Finextra; A-Team Insight; "
             "InvestOps 2026 research cited by GoldenSource. Values as disclosed; n.d. = not "
             "disclosed. Ownership shown where publicly confirmed.")

prs.save(OUT)
print("wrote", OUT)
