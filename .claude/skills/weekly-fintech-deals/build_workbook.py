#!/usr/bin/env python3
"""
build_workbook.py — Weekly FinTech deals workbook, matched to the finalized-DB schema
AND its exact visual styling (so a weekly tab drops straight into the master DB).

Two tabs, exact names and column order:
  "All M&A (PE & Strategic)":
     x | Week | Sector | Target Country | Deal Type | Date | Target | Acquirer | EV ($M) |
     EV / Revenue | EV / EBITDA | Target Description | Link / Press Release |
     Mults Source | Mults Basis | Public Deal | HL Deal | Seller
  "Growth Capital Raises":
     x | Week | Sector | Target Country | Date | Target | Lead Investor(s) | Amount ($M) |
     Valuation ($M) | EV / Revenue | EV / EBITDA | Target Description | Link / Press Release

Styling (reverse-engineered from Finalized_Deals_History.xlsx — keep in lockstep):
  - Header on ROW 3 (rows 1-2 left blank); freeze panes A4; gridlines OFF.
  - Header: Segoe UI 8pt bold white on solid fill 0069A3 (M&A) / 0067A5 (Raises),
    centered + wrapped, 45pt tall, thin top border.
  - Body: Segoe UI 8pt; thin bottom border per row (no vertical rules); Description and
    Mults Source left-aligned, everything else centered + wrapped.
  - Number formats: money "$"#,##0 (EV/Amount/Valuation), 0.0x (multiples),
    d-mmm-yy (Week/Date). Undisclosed = "-" (displays as-is under every format).
  - Autofilter from the header row (M&A B3:.., Raises A3:..).

Conventions (locked):
  - Deal Type is STRICTLY "Strategic M&A" or "PE Buyout" (validated; build fails otherwise).
  - Undisclosed / not-applicable = "-" (never blank) in EV/Amount/Valuation/multiples and
    the M&A meta columns.
  - All money in USD $M (convert at announcement-date FX BEFORE building).
  - Week = the deal's Saturday-Friday week, labeled by ending Friday (DD-Mmm-YY), derived
    from Date automatically.
  - Link column renders the word "Link" hyperlinked to the source.

Usage: python3 build_workbook.py deals.json "Weekly_Fintech_Deals_<endingFriday>.xlsx"
"""
import json, sys, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ALLOWED_DEAL_TYPES = {"Strategic M&A", "PE Buyout"}

MA_HEADERS = ["x","Week","Sector","Target Country","Deal Type","Date","Target","Acquirer",
              "EV ($M)","EV / Revenue","EV / EBITDA","Target Description","Link / Press Release",
              "Mults Source","Mults Basis","Public Deal","HL Deal","Seller"]
MA_KEYS    = ["x","week","sector","country","deal_type","date","target","acquirer",
              "ev","ev_rev","ev_ebitda","description","link",
              "mults_source","mults_basis","public_deal","hl_deal","seller"]

RA_HEADERS = ["x","Week","Sector","Target Country","Date","Target","Lead Investor(s)",
              "Amount ($M)","Valuation ($M)","EV / Revenue","EV / EBITDA",
              "Target Description","Link / Press Release"]
RA_KEYS    = ["x","week","sector","country","date","target","lead",
              "amount","valuation","ev_rev","ev_ebitda","description","link"]

DASH_KEYS = {"ev","ev_rev","ev_ebitda","amount","valuation",
             "mults_source","mults_basis","public_deal","hl_deal","seller"}

# Exact column widths lifted from the finalized DB (A.. per tab).
MA_WIDTHS = {"A":2.73,"B":12.54,"C":14.73,"D":14.73,"E":15.18,"F":11.73,"G":17.73,"H":20.73,
             "I":12.73,"J":13.0,"K":13.0,"L":106.73,"M":12.73,"N":12.73,"O":10.73,"P":15.73,
             "Q":13.0,"R":17.0}
RA_WIDTHS = {"A":2.73,"B":12.54,"C":14.73,"D":15.27,"E":11.73,"F":17.73,"G":26.73,"H":12.73,
             "I":13.0,"J":13.0,"K":13.0,"L":102.73,"M":12.73}

# Number formats (exact strings from the finalized DB).
FMT_DATE  = r'[$-409]d\-mmm\-yy;@'
FMT_MONEY = '"$"#,##0_);\\("$"#,##0\\);"$"\\ \\–?'
FMT_MULT  = r'0.0\x'
DATE_HEADERS  = {"Week", "Date"}
MONEY_HEADERS = {"EV ($M)", "Amount ($M)", "Valuation ($M)"}
MULT_HEADERS  = {"EV / Revenue", "EV / EBITDA"}
LEFT_HEADERS  = {"Target Description", "Mults Source"}

HFONT = Font(name="Segoe UI", size=8, bold=True, color="FFFFFF")
BFONT = Font(name="Segoe UI", size=8)
LFONT = Font(name="Segoe UI", size=8, color="0563C1", underline="single")
HCEN  = Alignment(horizontal="center", vertical="center", wrap_text=True)
BCEN  = Alignment(horizontal="center", vertical="center", wrap_text=True)
BLEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
THIN  = Side(style="thin", color="D9D9D9")
TOPB  = Border(top=THIN)
BOTB  = Border(bottom=THIN)

HDR_ROW = 3  # headers live on row 3; data begins on row 4


def week_ending_friday(date_str):
    """DD-Mmm-YY -> that week's ending Friday as DD-Mmm-YY."""
    try:
        d = datetime.datetime.strptime(str(date_str).strip(), "%d-%b-%y").date()
    except ValueError:
        return "-"
    fri = d + datetime.timedelta(days=(4 - d.weekday()) % 7)
    return fri.strftime("%d-%b-%y")


def norm(row, key):
    v = row.get(key, None)
    if key == "week" and (v in (None, "")):
        return week_ending_friday(row.get("date", ""))
    if key == "x":
        return v if v not in (None, "") else ""
    if v in (None, ""):
        return "-" if key in DASH_KEYS else ""
    return v


def fill_sheet(ws, headers, keys, rows, widths, hexfill, filter_first_col):
    ws.sheet_view.showGridLines = False
    hfill = PatternFill("solid", fgColor=hexfill)
    link_idx = keys.index("link")

    # header on row 3
    for ci, htext in enumerate(headers, 1):
        c = ws.cell(HDR_ROW, ci, htext)
        c.fill = hfill; c.font = HFONT; c.alignment = HCEN; c.border = TOPB
    ws.row_dimensions[HDR_ROW].height = 45

    for ri, row in enumerate(rows, HDR_ROW + 1):
        if "deal_type" in keys:
            dt = row.get("deal_type", "")
            if dt not in ALLOWED_DEAL_TYPES:
                raise ValueError(f"Deal Type must be one of {ALLOWED_DEAL_TYPES}, got: {dt!r} ({row.get('target')})")
        for ci, key in enumerate(keys, 1):
            c = ws.cell(ri, ci)
            header = headers[ci - 1]
            # the leftmost flag column carries no rule/border in the finalized DB
            if ci > 1:
                c.border = BOTB
            if ci - 1 == link_idx:
                url = row.get("link", "")
                c.value = "Link" if url else "-"
                if url:
                    c.hyperlink = url; c.font = LFONT
                else:
                    c.font = BFONT
                c.alignment = BCEN
                continue
            v = norm(row, key)
            c.value = v
            c.font = BFONT
            c.alignment = BLEFT if header in LEFT_HEADERS else BCEN
            # number formats apply to the whole column (a text "-" still renders as "-")
            if header in MONEY_HEADERS:
                c.number_format = FMT_MONEY
            elif header in MULT_HEADERS:
                c.number_format = FMT_MULT
            elif header in DATE_HEADERS:
                c.number_format = FMT_DATE

    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    ws.freeze_panes = f"A{HDR_ROW + 1}"
    last = HDR_ROW + len(rows)
    ws.auto_filter.ref = f"{filter_first_col}{HDR_ROW}:{get_column_letter(len(headers))}{last}"


def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else "deals.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "Weekly_Fintech_Deals.xlsx"
    with open(data_path) as f:
        data = json.load(f)
    ma = sorted(data.get("ma", []), key=lambda r: (r.get("sector",""), r.get("date","")))
    ra = sorted(data.get("raises", []), key=lambda r: (r.get("sector",""), r.get("date","")))
    wb = Workbook()
    ws = wb.active; ws.title = "All M&A (PE & Strategic)"
    fill_sheet(ws, MA_HEADERS, MA_KEYS, ma, MA_WIDTHS, "FF0069A3", "B")
    ws2 = wb.create_sheet("Growth Capital Raises")
    fill_sheet(ws2, RA_HEADERS, RA_KEYS, ra, RA_WIDTHS, "FF0067A5", "A")
    wb.save(out_path)
    print(f"Wrote {out_path}: {len(ma)} M&A + {len(ra)} raises")


if __name__ == "__main__":
    main()
