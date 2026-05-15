#!/usr/bin/env python3
"""Build the Relationship Resurrection PDF from chapter markdown files."""

from pathlib import Path
import re
import sys
import markdown
from weasyprint import HTML, CSS

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters"
APPENDICES = ROOT / "appendices"
BUILD = ROOT / "build"
OUT_PDF = ROOT / "Relationship_Resurrection.pdf"
OUT_HTML = BUILD / "manuscript.html"
CSS_PATH = BUILD / "style.css"


def md_to_html_fragment(md_text: str) -> str:
    """Render markdown to an HTML fragment (no <html> wrapper)."""
    return markdown.markdown(
        md_text,
        extensions=["extra", "smarty", "sane_lists"],
        output_format="html5",
    )


def wrap_chapter(html: str) -> str:
    """Wrap a chapter's html so it gets the chapter-opener class on the outer div,
    moves the chapter-number heading to a styled eyebrow, and applies a drop cap to
    the first paragraph after the H2 title."""
    # Extract "# Chapter N" → eyebrow
    m = re.match(
        r"\s*<h1>(Chapter [^<]+|Introduction|Appendix [^<]+)</h1>\s*",
        html,
        flags=re.IGNORECASE,
    )
    eyebrow_html = ""
    rest = html
    if m:
        eyebrow = m.group(1).strip()
        eyebrow_html = f'<p class="chapter-num">{eyebrow}</p>'
        rest = html[m.end():]

    # Inject dropcap into the first paragraph that follows the chapter's H2.
    # Find the first <p>...</p> after the first </h2>.
    def inject_dropcap(match: re.Match) -> str:
        prefix = match.group(1)
        first_char = match.group(2)
        body = match.group(3)
        # Skip leading punctuation/whitespace, but if the first char is a letter, drop-cap it.
        if first_char.isalpha():
            return f'{prefix}<span class="dropcap">{first_char}</span>{body}'
        return match.group(0)

    rest = re.sub(
        r"(</h2>\s*<p[^>]*>)(\S)(.*?</p>)",
        inject_dropcap,
        rest,
        count=1,
        flags=re.DOTALL,
    )

    return f'<section class="chapter-opener">{eyebrow_html}{rest}</section>'


def part_divider(eyebrow: str, title: str, sub: str = "") -> str:
    sub_html = f'<div class="part-sub">{sub}</div>' if sub else ""
    return (
        '<section class="part-divider">'
        f'<div class="part-eyebrow">{eyebrow}</div>'
        f'<div class="part-title">{title}</div>'
        '<div class="part-rule"></div>'
        f"{sub_html}"
        "</section>"
    )


def cover() -> str:
    return (
        '<section class="cover">'
        '<div class="cover-eyebrow">A Manual For Couples</div>'
        '<div class="cover-title">Relationship<br/>Resurrection</div>'
        '<div class="cover-rule"></div>'
        '<div class="cover-subtitle">'
        "How to dig out what you buried, kick the door off its hinges, "
        "and remember what you used to be."
        '</div>'
        '<div class="cover-rule"></div>'
        '<div class="cover-byline">After the work of Day &mdash; rebuilt with receipts</div>'
        "</section>"
    )


def half_title() -> str:
    return (
        '<section class="half-title">'
        '<h1>Relationship Resurrection</h1>'
        "</section>"
    )


def toc(items: list[tuple[str, str]]) -> str:
    rows = []
    for kind, label in items:
        if kind == "part":
            rows.append(f'<li class="toc-part">{label}</li>')
        elif kind == "chapter":
            num, title = label
            rows.append(
                f'<li><span class="toc-chapter-num">{num}</span>{title}</li>'
            )
        elif kind == "section":
            rows.append(f'<li>{label}</li>')
    body = "\n".join(rows)
    return (
        '<section class="toc">'
        "<h1>Contents</h1>"
        f"<ol>{body}</ol>"
        "</section>"
    )


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_html() -> str:
    parts = []
    parts.append(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>Relationship Resurrection</title></head><body>"
    )

    parts.append(cover())
    parts.append(half_title())

    # Table of contents
    toc_items = [
        ("section", "Introduction"),
        ("part", "Part I &mdash; His Resurrection"),
        ("chapter", ("1", "The First 72 Hours")),
        ("chapter", ("2", "Kill the Routine Before It Kills You")),
        ("chapter", ("3", "Become the Man From Month One")),
        ("chapter", ("4", "The Physical Resurrection")),
        ("chapter", ("5", "Make Love Like You Just Met Her")),
        ("chapter", ("5.5", "The Dark Arts")),
        ("part", "Part II &mdash; Her Resurrection"),
        ("chapter", ("6", "Stop Punishing Him For Trying")),
        ("chapter", ("7", "Be the Woman He Comes Home To")),
        ("chapter", ("8", "Cook the Meal. Wear the Dress. Choose Him.")),
        ("chapter", ("9", "Give Him the Silence He's Been Begging For")),
        ("chapter", ("10", "Want Him Again")),
        ("part", "Part III &mdash; Resurrection Together"),
        ("chapter", ("11", "The 30-Day Protocol")),
        ("chapter", ("12", "The Vow")),
        ("part", "Appendices"),
        ("chapter", ("A", "The 15 Things He Stopped Doing")),
        ("chapter", ("B", "The 15 Things She Stopped Doing")),
        ("chapter", ("C", "The Date Night Blueprint")),
        ("chapter", ("D", "The Argument Protocol")),
    ]
    parts.append(toc(toc_items))

    # Introduction
    parts.append(wrap_chapter(md_to_html_fragment(read(CHAPTERS / "00-introduction.md"))))

    # Part I
    parts.append(part_divider(
        "Part I",
        "His Resurrection",
        "Six chapters for the man who used to be dangerous.",
    ))
    for fn in [
        "01-the-first-72-hours.md",
        "02-kill-the-routine.md",
        "03-man-from-month-one.md",
        "04-physical-resurrection.md",
        "05-make-love-like-you-met-her.md",
        "05-5-dark-arts.md",
    ]:
        parts.append(wrap_chapter(md_to_html_fragment(read(CHAPTERS / fn))))

    # Part II
    parts.append(part_divider(
        "Part II",
        "Her Resurrection",
        "Five chapters for the woman who used to tremble.",
    ))
    for fn in [
        "06-stop-punishing-him.md",
        "07-woman-he-comes-home-to.md",
        "08-cook-wear-choose.md",
        "09-give-him-silence.md",
        "10-want-him-again.md",
    ]:
        parts.append(wrap_chapter(md_to_html_fragment(read(CHAPTERS / fn))))

    # Part III
    parts.append(part_divider(
        "Part III",
        "Resurrection Together",
        "The day-by-day. The vow. The way back.",
    ))
    for fn in ["11-30-day-protocol.md", "12-the-vow.md"]:
        parts.append(wrap_chapter(md_to_html_fragment(read(CHAPTERS / fn))))

    # Appendices
    parts.append(part_divider(
        "Appendices",
        "Reference",
        "What he stopped. What she stopped. Where to go. How to fight.",
    ))
    for fn in [
        "A-15-things-he-stopped.md",
        "B-15-things-she-stopped.md",
        "C-date-blueprint.md",
        "D-argument-protocol.md",
    ]:
        parts.append(wrap_chapter(md_to_html_fragment(read(APPENDICES / fn))))

    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    html = build_html()
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({len(html):,} chars)")

    css = CSS(filename=str(CSS_PATH))
    HTML(string=html, base_url=str(ROOT)).write_pdf(
        str(OUT_PDF),
        stylesheets=[css],
        optimize_images=True,
    )
    size = OUT_PDF.stat().st_size
    print(f"Wrote {OUT_PDF} ({size:,} bytes)")


if __name__ == "__main__":
    main()
