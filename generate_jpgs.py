#!/usr/bin/env python3
"""Render every card and timetable to A4 JPGs (one JPG per printed page).

Usage: python3 generate_jpgs.py [--dpi 200] [--out jpg_cards]
       python3 generate_jpgs.py --only reception_timetable
Requires: playwright (chromium installed) and PyMuPDF.
"""
import argparse
import io
from pathlib import Path

import fitz
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CARDS = ROOT / "cards"


A4_MM = (210, 297)
RATIO = 297 / 210
FIT_CSS = """
.card{height:auto !important;min-height:0 !important}
.card-inner{flex:1 1 auto !important;min-width:0 !important}
.text-box{flex:1 1 auto !important;overflow:visible !important}
.art-box{flex:none !important;height:90mm !important;width:100% !important}
.art-box img{width:100% !important;height:100% !important}
"""

# Widen the card until its content fits an A4 aspect ratio, then stretch it to exactly A4.
FIT_JS = """
(ratio) => {
  const c = document.querySelector('.card');
  let w = 600;
  for (; w < 3000; w += 10) {
    c.style.setProperty('width', w + 'px', 'important');
    c.style.setProperty('height', 'auto', 'important');
    if (c.getBoundingClientRect().height <= w * ratio) break;
  }
  c.style.setProperty('height', (w * ratio) + 'px', 'important');
  return w;
}
"""


def render_card(page, f, dest, dpi, quality):
    """Print-styled card, sized to exactly A4 proportions so it fills the whole image."""
    page.goto(f.as_uri())
    page.emulate_media(media="print")
    page.add_style_tag(content=FIT_CSS)
    page.wait_for_load_state("networkidle")
    page.evaluate(FIT_JS, RATIO)
    shot = page.locator(".card").screenshot(type="png")
    img = Image.open(io.BytesIO(shot)).convert("RGB")
    size = tuple(round(m / 25.4 * dpi) for m in A4_MM)
    img.resize(size, Image.LANCZOS).save(dest, quality=quality, dpi=(dpi, dpi))
    print(dest.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--out", default="jpg_cards")
    ap.add_argument("--quality", type=int, default=92)
    ap.add_argument(
        "--only",
        choices=("all", "master_timetable", "reception_timetable"),
        default="all",
        help="Render all documents or just one of the timetables",
    )
    args = ap.parse_args()

    out = ROOT / args.out
    out.mkdir(exist_ok=True)
    if args.only == "all":
        files = sorted(CARDS.glob("*_day[12].html")) + [
            CARDS / "master_timetable.html",
            CARDS / "reception_timetable.html",
        ]
    else:
        files = [CARDS / f"{args.only}.html"]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=args.dpi / 96)
        for f in files:
            if f.name not in {"master_timetable.html", "reception_timetable.html"}:
                render_card(page, f, out / f"{f.stem}.jpg", args.dpi, args.quality)
                continue
            page.goto(f.as_uri())
            page.emulate_media(media="print")
            page.wait_for_load_state("networkidle")
            pdf = page.pdf(format="A4", print_background=True, prefer_css_page_size=True)
            doc = fitz.open(stream=pdf, filetype="pdf")
            for i, pg in enumerate(doc, 1):
                suffix = "" if len(doc) == 1 else f"_p{i}"
                dest = out / f"{f.stem}{suffix}.jpg"
                pg.get_pixmap(dpi=args.dpi, alpha=False).save(dest, jpg_quality=args.quality)
                print(dest.name)
            doc.close()
        browser.close()


if __name__ == "__main__":
    main()
