"""Audits the generated cards against the three timetable CSVs.

For every non-empty cell in the before / church / reception CSVs, the cell is
matched to a rule (CELL_RULES: cell-text regex -> regex that must appear on that
person's day1+day2 cards). A cell with no rule is reported as UNMAPPED so a human
can decide whether the card needs it and, if the cell is new, add a rule.

Usage (from this directory):
    python3 audit_cards.py            # audit; exit 1 on gaps, 2 on unmapped cells
    python3 audit_cards.py --dump     # print every CSV cell per person (no audit)
    python3 audit_cards.py --dump marie
"""
import csv
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(HERE, "cards")
PREFIX = "Wedding 2025 Brittany + Adam - Time table "
CSVS = {"before": PREFIX + "before.csv", "church": PREFIX + "church.csv", "reception": PREFIX + "reception.csv"}

# CSV header first-name (lowercase) -> card slug. People not listed use their own name.
ALIAS = {"brittney": "brittany", "sophia": "sofia", "petr": "peter"}
# CSV columns that intentionally have no card; they are listed in the report.
NO_CARD = {"omi", "eric demery", "april demery"}

# (cell-text regex, regex that must appear on the person's cards)
CELL_RULES = [
    (r"vagon|wagon", r"wagon"),
    (r"get tux", r"tux"),
    (r"decora", r"decorat"),
    (r"church rehersal", r"rehears"),
    (r"practice wows", r"vow"),
    (r"rehersal dinner", r"dinner"),
    (r"return to inn", r"8:00"),
    (r"flower delivery", r"flower|florist"),
    (r"pictures of groomsmen", r"groomsmen"),
    (r"arrive in hotel", r"10:00"),
    (r"pictures of bridesmaids", r"12:00"),
    (r"take party bus to church|adam \+ peter take car", r"1:00|1:15"),
    (r"arrive to church", r"1:45"),
    (r"back to leonards", r"3:30"),
    (r"bridal suite becomes", r"4:30"),
    (r"front of leonards", r"5:30"),
    (r"cocktai", r"cocktail"),
    (r"reception begins", r"7:30"),
    (r"create", r"crate"),
    (r"memory of my brother", r"dominik"),
    (r"hair salon", r"hair"),
    (r"drive autumn", r"drive autumn|autumn"),
    (r"teaching", r"teaching"),
    (r"arrival with camelot", r"camelot"),
    (r"arrive by themselves", r"own car|their own"),
    (r"peters car", r"peter"),
    (r"kneel", r"kneel"),
    (r"personal vows", r"personal vows"),
    (r"official religious", r"religious|vows after"),
    (r"exchange rings", r"ring"),
    (r"brings in rings", r"ring"),
    (r"candle", r"candle"),
    (r"hands? bubbles", r"bubble"),
    (r"form a line", r"line"),
    (r"exit church last", r"last"),
    (r"holding her dress", r"holding (her|brittany's) dress|hold.*dress"),
    (r"leave in the party bus", r"party bus|bus"),
    (r"\$500", r"\$500"),
    (r"\$200", r"\$200"),
    (r"broom", r"broom"),
    (r"separate wedding suite", r"suite"),
    (r"arch", r"arch"),
    (r"eat dinner", r"dinner"),
    (r"open dancing", r"open danc"),
    (r"cut the cake", r"cake"),
    (r"first dance", r"first dance"),
    (r"dance", r"dance"),
    (r"speech|toast", r"speech|toast"),
    (r"bouquet", r"bouquet"),
    (r"walks? in|enter|seated|escort", r"walk|enter|escort|seated"),
]


def load_cells():
    """Returns {person: [(file, row label, text), ...]} from the three CSVs."""
    out = {}
    for key, name in CSVS.items():
        with open(os.path.join(HERE, name), encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        header, label = rows[0], ""
        for row in rows[1:]:
            if len(row) > 1 and row[1].strip():
                label = row[1].strip()
            for i in range(2, len(header)):
                if i < len(row) and row[i].strip():
                    person = header[i].split("(")[0].strip().lower()
                    out.setdefault(person, []).append((key, label, row[i].strip()))
    return out


def card_text(slug):
    parts = []
    for day in ("day1", "day2"):
        path = os.path.join(CARDS, f"{slug}_{day}.html")
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as fh:
            parts.append(html.unescape(re.sub(r"<[^>]+>", " ", fh.read())).lower())
    return re.sub(r"\s+", " ", " ".join(parts))


def dump(only=None):
    for person, cells in load_cells().items():
        if only and ALIAS.get(person, person) != only and person != only:
            continue
        print("==", person)
        for key, label, text in cells:
            print(f"   [{key}|{label}] {text}")


def check_links():
    """Every href/src in the cards must resolve to an existing file."""
    bad = []
    for name in sorted(os.listdir(CARDS)):
        if not name.endswith(".html"):
            continue
        with open(os.path.join(CARDS, name), encoding="utf-8") as fh:
            for ref in re.findall(r'(?:href|src)="([^"#:]+)"', fh.read()):
                if not os.path.exists(os.path.normpath(os.path.join(CARDS, ref))):
                    bad.append((name, ref))
    return bad


def main():
    if "--dump" in sys.argv:
        args = [a for a in sys.argv[2:] if not a.startswith("-")]
        dump(args[0].lower() if args else None)
        return 0

    gaps, unmapped, no_card = [], [], []
    for person, cells in load_cells().items():
        slug = ALIAS.get(person, person)
        if person in NO_CARD:
            no_card.append(person)
            continue
        text = card_text(slug)
        if text is None:
            no_card.append(person)
            continue
        for key, label, cell in cells:
            low = cell.lower()
            rule = next((r for r in CELL_RULES if re.search(r[0], low)), None)
            if rule is None:
                unmapped.append((slug, key, label, cell))
            elif not re.search(rule[1], text):
                gaps.append((slug, key, label, cell, rule[1]))

    broken = check_links()
    print(f"CSV columns without cards (not audited): {', '.join(sorted(set(no_card))) or 'none'}")
    for g in gaps:
        print(f"GAP      {g[0]:9} [{g[1]}|{g[2]}] {g[3][:80]}   (card lacks /{g[4]}/)")
    for u in unmapped:
        print(f"UNMAPPED {u[0]:9} [{u[1]}|{u[2]}] {u[3][:80]}")
    for b in broken:
        print(f"BROKEN   {b[0]} -> {b[1]}")
    print(f"\n{len(gaps)} gap(s), {len(unmapped)} unmapped cell(s), {len(broken)} broken link(s)")
    return 1 if gaps or broken else (2 if unmapped else 0)


if __name__ == "__main__":
    sys.exit(main())
