# Data source logos

`build_goldensource_pager.py` looks for `<slug>.png` in this directory and drops
it into the matching source slot on the platform panel. If a file is absent the
slot falls back to the vendor name as text, so the build never breaks.

| Slug | Vendor | Domain |
|---|---|---|
| `bloomberg` | Bloomberg | bloomberg.com |
| `lseg` | LSEG | lseg.com |
| `ice` | Intercontinental Exchange | theice.com |
| `spglobal` | S&P Global | spglobal.com |
| `msci` | MSCI | msci.com |
| `moodys` | Moody's | moodys.com |
| `six` | SIX | six-group.com |

Drop in transparent PNGs at 400px+ on the long edge. Height is normalised to
0.15in and width follows the source aspect ratio, so trim whitespace first.

These seven are the vendors GoldenSource names on its own integrations page.
Do not add a vendor to the panel without that kind of citation - a logo on the
page asserts a connector exists.
