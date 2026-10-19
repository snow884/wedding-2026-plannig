"""Generates the signature drink images (ComfyUI T2I via run_comfy_graph.py)
and the drink menu HTML at drinks/drink_menu.html."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = "drinks"

DRINKS = [
    {
        "slug": "hypnotic_breeze",
        "key": (255,255,255),
        "tol": 45,
        "for": "The Bride",
        "name": "Hypnotic Breeze",
        "quote": "One sip and I'm under her spell.",
        "ingredients": ["Hpnotiq liqueur", "Vodka", "Pineapple juice"],
        "prompt": (
            "Professional cocktail photography of a Hpnotiq Hypnotic Breeze cocktail, "
            "a glowing turquoise-blue drink in a stemmed glass, a few ice cubes floating on top "
            "and a single pineapple wedge garnish on the rim, nothing else in the glass, "
            "no straw, no stirrer, no cherry, no pink, full glass with a clear stem and round foot, studio product shot, "
            "isolated on a flat pure solid pure white background, floating, no table, no surface, no floor, no shadow, no reflection, background is one uniform flat color edge to edge, even lighting, high detail"
        ),
    },
    {
        "slug": "jack_and_coke",
        "key": (255,0,255),
        "tol": 55,
        "for": "The Groom",
        "name": "Jack &amp; Coke",
        "quote": "Simple, strong, and here to stay, like the groom.",
        "ingredients": ["Jack Daniel's Tennessee Whiskey", "Coca-Cola (or Diet Coke)", "Ice", "Lime wedge"],
        "prompt": (
            "Professional cocktail photography of a Jack and Coke, whiskey and cola in a "
            "tall highball glass with ice cubes and a lime wedge, condensation droplets, "
            "studio product shot, "
            "isolated on a flat pure solid chroma-key magenta (#FF00FF) background, floating, no table, no surface, no floor, no shadow, no reflection, background is one uniform flat color edge to edge, even lighting, high detail"
        ),
    },
    {
        "slug": "moscow_mule",
        "key": (0,0,255),
        "tol": 85,
        "holes": True,
        "for": "Bride &amp; Groom Together",
        "name": "Moscow Mule",
        "quote": "Two kicks of spice, one perfect pair.",
        "ingredients": ["Vodka", "Ginger beer", "Fresh lime juice", "Mint sprig &amp; lime wheel"],
        "prompt": (
            "Professional cocktail photography of a Moscow Mule in a shiny copper mug "
            "with crushed ice, lime wheel and fresh mint sprig garnish, condensation on the "
            "copper, studio product shot, "
            "isolated on a flat pure solid chroma-key blue (#0000FF) background, floating, no table, no surface, no floor, no shadow, no reflection, background is one uniform flat color edge to edge, even lighting, high detail"
        ),
    },
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Cinzel+Decorative:wght@700&family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap');
@page { size: letter; margin: 0.4in; }
body{margin:0;padding:40px 20px;background:#f8f1e4;font-family:'EB Garamond',serif;color:#3b2f2a;text-align:center}
h1{font-family:'Cinzel Decorative',serif;color:#8a6d1d;margin:0 0 4px;font-size:2.4em}
.sub{font-family:'Cinzel',serif;letter-spacing:.2em;color:#8a7a60;margin-bottom:30px}
.menu{max-width:1000px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px}
.drink{background:#fffdf7;border:2px solid #c9a94c;outline:1px solid #c9a94c;outline-offset:-8px;padding:22px;border-radius:4px;break-inside:avoid}
.drink img{width:100%;aspect-ratio:1;object-fit:contain}
.for{font-family:'Cinzel',serif;letter-spacing:.15em;font-size:.85em;color:#8a6d1d;margin-top:14px;text-transform:uppercase}
h2{font-family:'Cinzel',serif;margin:6px 0;font-size:1.6em}
.quote{font-style:italic;color:#6b5a4c;margin:6px 0 12px}
ul{list-style:none;padding:0;margin:0;font-size:1.05em}
li{padding:2px 0}li+li:before{content:'';}
.rule{width:60px;height:2px;background:#c9a94c;margin:10px auto}
"""


def key_out(raw_path, out_path, key=None, tol=85, holes=False):
    """Makes the solid background transparent (edge flood fill + soft edge spill removal)."""
    import numpy as np
    from PIL import Image
    from scipy import ndimage

    img = Image.open(raw_path).convert("RGB")
    a = np.asarray(img).astype(float)
    h, w, _ = a.shape
    # Background colours are sampled from the image border (generated backgrounds are
    # shaded gradients, not a perfectly flat key colour).
    border = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3),
                             a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    from scipy.cluster.vq import kmeans2
    np.random.seed(1)
    centers, _ = kmeans2(border, 6, minit="++")
    dist = np.min(np.linalg.norm(a[:, :, None, :] - centers[None, None], axis=3), axis=2)
    bg = dist < tol
    labels, _ = ndimage.label(bg)
    edge = set(np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))) - {0}
    mask = np.isin(labels, list(edge))
    # Also clear enclosed background pockets (e.g. inside the mug handle), but only large ones.
    tight = dist < 40
    tl, tn = ndimage.label(tight)
    tsizes = ndimage.sum(tight, tl, range(tn + 1))
    if holes:
        mask |= np.isin(tl, [i for i in range(1, tn + 1) if tsizes[i] > 1500])
    fg_labels, n = ndimage.label(~mask)
    fg_sizes = ndimage.sum(~mask, fg_labels, range(n + 1))
    mask |= np.isin(fg_labels, [i for i in range(1, n + 1) if fg_sizes[i] < 3000])
    mask = ndimage.binary_dilation(mask, iterations=1)
    alpha = np.where(mask, 0.0, 255.0)
    alpha = ndimage.gaussian_filter(alpha, 0.8)
    out = np.dstack([a, alpha]).astype("uint8")
    im = Image.fromarray(out, "RGBA")
    im.crop(im.getbbox()).save(out_path)


def build_html():
    cards = []
    for d in DRINKS:
        items = "".join(f"<li>{i}</li>" for i in d["ingredients"])
        cards.append(
            f'<div class="drink"><img src="{d["slug"]}.png" alt="{d["name"]}">'
            f'<div class="for">{d["for"]}</div><h2>{d["name"]}</h2>'
            f'<div class="quote">&ldquo;{d["quote"]}&rdquo;</div><div class="rule"></div>'
            f"<ul>{items}</ul></div>"
        )
    html = (
        f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Signature Drinks — Brittany &amp; Adam</title>'
        f"<style>{CSS}</style></head><body><h1>Signature Drinks</h1>"
        f'<div class="sub">BRITTANY &amp; ADAM &middot; NOVEMBER 7, 2026</div>'
        f'<div class="menu">{"".join(cards)}</div></body></html>'
    )
    with open(os.path.join(OUTPUT_DIR, "drink_menu.html"), "w") as f:
        f.write(html)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if "--html-only" not in sys.argv:
        from run_comfy_graph import generate_image_from_prompt

        for d in DRINKS:
            raw = os.path.join(OUTPUT_DIR, "raw", f"{d['slug']}.png")
            if not os.path.exists(raw):
                os.makedirs(os.path.dirname(raw), exist_ok=True)
                generate_image_from_prompt(d["prompt"], output_file_path=raw)
            key_out(raw, os.path.join(OUTPUT_DIR, f"{d['slug']}.png"), d["key"], d["tol"], d.get("holes", False))
    build_html()


if __name__ == "__main__":
    main()
