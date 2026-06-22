#!/usr/bin/env python3
"""
build_workbook.py — Generate the formatted weekly FinTech deals workbook.

Reads a JSON file describing the week's deals and writes a two-tab Excel:
  - "M&A"
  - "Growth Capital Raises"
Links are rendered as the word "Link" hyperlinked to the source URL.

Usage:
    python3 build_workbook.py deals.json "Weekly_Fintech_Deals_<week>.xlsx"

JSON schema:
{
  "ma": [
    {
      "sector": "Payments", "country": "United States",
      "deal_type": "Strategic M&A", "date": "12-Jun-26",
      "target": "Payoneer", "acquirer": "Nuvei",
      "ev": 2750, "ev_rev": "", "ev_ebitda": "",
      "description": "Cross-border payments platform ...",
      "link": "https://..."
    }
  ],
  "raises": [
    {
      "sector": "InsurTech", "country": "United States", "date": "10-Jun-26",
      "target": "Poetic", "lead": "Kleiner Perkins",
      "amount": 50, "valuation": 500, "ev_rev": "", "ev_ebitda": "",
      "description": "Developer of deterministic AI ...",
      "link": "https://..."
    }
  ]
}
Any missing/empty numeric field is rendered as a blank cell.
"""
import json
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

MA_HEADERS = ["Sector", "Target Country", "Deal Type", "Date", "Target", "Acquirer",
              "EV ($M)", "EV / Revenue", "EV / EBITDA", "Target Description", "Link / Press Release"]
RAISE_HEADERS = ["Sector", "Target Country", "Date", "Target", "Lead Investor(s)",
                 "Amount ($M)", "Valuation ($M)", "EV / Revenue", "EV / EBITDA",
                 "Target Description", "Link / Press Release"]

MA_KEYS = ["sector", "country", "deal_type", "date", "target", "acquirer",
           "ev", "ev_rev", "ev_ebitda", "description", "link"]
RAISE_KEYS = ["sector", "country", "date", "target", "lead",
              "amount", "valuation", "ev_rev", "ev_ebitda", "description", "link"]

HEADER_FILL = PatternFill("solid", fgColor="1F6FB2")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)
LINK_FONT = Font(color="0563C1", underline="single", size=11)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT_WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)
LINK_ALIGN = Alignment(horizontal="center", vertical="top")
THIN = Side(style="thin", color="D0D0D0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def fill_sheet(ws, headers, keys, rows, widths):
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill, cell.font, cell.alignment, cell.border = HEADER_FILL, HEADER_FONT, CENTER, BORDER
    link_idx = keys.index("link")
    for ri, row in enumerate(rows, start=2):
        for ci, key in enumerate(keys, start=1):
            val = row.get(key, "")
            if val is None:
                val = ""
            cell = ws.cell(row=ri, column=ci)
            cell.border = BORDER
            if ci - 1 == link_idx:
                cell.value = "Link" if val else ""
                if val:
                    cell.hyperlink = val
                    cell.font = LINK_FONT
                cell.alignment = LINK_ALIGN
            else:
                cell.value = val
                cell.alignment = LEFT_WRAP
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{1 + len(rows)}"
    ws.row_dimensions[1].height = 30


def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else "deals.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "Weekly_Fintech_Deals.xlsx"
    with open(data_path) as f:
        data = json.load(f)
    wb = Workbook()
    ws_ma = wb.active
    ws_ma.title = "M&A"
    fill_sheet(ws_ma, MA_HEADERS, MA_KEYS, data.get("ma", []),
               [24, 15, 15, 11, 16, 18, 9, 11, 11, 62, 10])
    ws_r = wb.create_sheet("Growth Capital Raises")
    fill_sheet(ws_r, RAISE_HEADERS, RAISE_KEYS, data.get("raises", []),
               [24, 15, 11, 16, 26, 11, 13, 11, 11, 62, 10])
    wb.save(out_path)
    print(f"Wrote {out_path}: {len(data.get('ma', []))} M&A + {len(data.get('raises', []))} raises")


if __name__ == "__main__":
    main()
