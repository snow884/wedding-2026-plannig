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
# CSV columns that intentionally have no card (confirmed by the couple); skipped silently.
NO_CARD = {"omi", "eric demery", "april demery"}

# Per-person overrides where the couple's instruction supersedes a CSV cell:
# (person slug, cell-text regex) -> regex that must appear instead.
CELL_OVERRIDES = {
    ("gustavo", r"arrival with camelot"): r"peter's car",  # Oct 26: Gustavo rides in Peter's car
}

# (cell-text regex, regex that must appear on the person's cards)
CELL_RULES = [
    (r"decorations and vagon", r"decorations and (the )?wagon"),
    (r"bring ring, present", r"(?s)(?=.*bring the ring)(?=.*present for karin)(?=.*blue suit)"),
    (r"pick up omni", r"pick up omi"),
    (r"pick up karins cousin", r"karin's cousin"),
    (r"money box", r"(?s)(?=.*crate)(?=.*money box)"),
    (r"vagon|wagon", r"wagon"),
    (r"get tux", r"tux"),
    (r"decora", r"decorat"),
    (r"church rehersal", r"rehears"),
    (r"practice wows", r"vow"),
    (r"rehersal dinner", r"dinner"),
    (r"return to inn", r"8:00"),
    (r"flower delivery", r"flower|florist"),
    (r"pictures of groomsmen", r"groomsmen"),
    (r"arrive in hotel", r"11:40"),
    (r"pictures of bridesmaids", r"12:00"),
    (r"take party bus to church|take car to church", r"1:00|1:15"),
    (r"drive to zum stammtisch", r"drive to zum stammtisch"),
    (r"(drive|arrive) to inn at great neck and check in", r"8:30 pm: .*(drive|arrive).*inn"),
    (r"drive back home", r"drive back home"),
    (r"get dressed in tux", r"get dressed in your tux"),
    (r"bring wedding dress", r"wedding dress shoes"),
    (r"put wedding dress on", r"put on your wedding dress"),
    (r"help brittany get dres", r"help brittany get dressed"),
    (r"change (dhoes|shoes)|help britt?any change", r"change"),
    (r"pack food and formula", r"formula"),
    (r"get madison dressed", r"madison dressed|dress madison"),
    (r"drive to omis house", r"omi"),
    (r"drive to inn at great neck to pick up adam", r"1:00 pm: drive to the inn.*pick up adam"),
    (r"pick up adam", r"pick up adam"),
    (r"practice walking|practice carrying", r"practice (walking|carrying)"),
    (r"arrive to church", r"1:45"),
    (r"back to leonards", r"3:30"),
    (r"francis lewis", r"francis lewis"),
    (r"rompe rompe", r"rompe rompe"),
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
    (r"cut the (wedding )?cake", r"cake"),
    (r"favou?rs?", r"favou?rs? home"),
    (r"opportunity to give speech", r"opportunity to give a speech"),
    (r"thank you speech", r"thank-you speech"),
    (r"first dance", r"first dance"),
    (r"dance", r"dance"),
    (r"speech|toast", r"speech|toast"),
    (r"bouquet", r"bouquet"),
    (r"kdyby byla morava", r"kdyby byla morava.*0:23"),
    (r"dai dai", r"dai dai.*shakira"),
    (r"i.ve gotta feeling", r"i.ve gotta feeling.*1:29"),
    (r"lets get it started", r"let.?s get it started.*black eyed peas"),
    (r"gasolina", r"gasolina.*daddy yankee"),
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


def check_time_groups():
    """No section (<h4> + <ul>) may hold actions that are 15+ minutes apart."""
    sys.path.insert(0, HERE)
    import generate_cards as gc
    bad = []
    for name in sorted(os.listdir(CARDS)):
        if not re.match(r"[a-z]+_day[12]\.html$", name):
            continue
        with open(os.path.join(CARDS, name), encoding="utf-8") as fh:
            body = fh.read()
        for heading, ul in re.findall(r"<h4>(.*?)</h4>\s*<ul>(.*?)</ul>", body, re.S):
            if heading.startswith(gc.UNTIMED_SECTIONS):
                continue
            times = []
            for li in re.findall(r"<li>(.*?)</li>", ul, re.S):
                minutes = gc.item_minutes(html.unescape(li), None, None)
                if minutes is not None:
                    times.append((minutes, li))
            if times and max(t for t, _ in times) - min(t for t, _ in times) >= gc.MAX_GROUP_MINUTES:
                bad.append((name, html.unescape(heading)))
    return bad


def check_event_hours():
    """Every person card and both master plans must state the venue event hours."""
    required = (r"12:30 AM EST", r"6:30–7:30 PM EST")
    paths = [
        os.path.join(CARDS, name)
        for name in sorted(os.listdir(CARDS))
        if re.fullmatch(r"[a-z]+_day[12]\.html", name)
    ]
    paths += [
        os.path.join(CARDS, "master_timetable.html"),
        os.path.join(HERE, "MASTER_TIMETABLE.md"),
    ]
    missing = []
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            text = html.unescape(re.sub(r"<[^>]+>", " ", fh.read()))
        for pattern in required:
            if not re.search(pattern, text):
                missing.append((os.path.basename(path), pattern))
    return missing


# Master-plan wording differs from card wording, so these rules take precedence over
# CELL_RULES when checking the master plan: (cell-text regex, regex a master row must match).
MASTER_RULES = [
    (r"bring ring, present", r"(?s)adam brings the ring.*present for karin.*blue suit"),
    (r"decorations and vagon", r"karin brings the decorations and the wagon"),
    (r"money box", r"money box"),
    (r"drive to zum stammtisch", r"drives to zum stammtisch"),
    (r"(drive|arrive) to inn at great neck and check in", r"arrive at the inn at great neck and check in"),
    (r"drive back home", r"back home to rockland"),
    (r"drive to inn at great neck to pick up adam", r"peter drives to the inn at great neck to pick up adam"),
    (r"pick up omni", r"peter picks up omi"),
    (r"pick up karins cousin", r"karin's cousin"),
    (r"get dressed in tux", r"adam gets dressed in his tux"),
    (r"put wedding dress on|help brittany get dres", r"puts on her wedding dress"),
    (r"arrival with camelot", r"camelot"),
    (r"arrive by themselves", r"by themselves"),
    (r"opportunity to give speech", r"opportunity to give a speech"),
    (r"kdyby byla morava", r"kdyby byla morava.*0:23"),
    (r"dai dai", r"dai dai.*shakira"),
    (r"i.ve gotta feeling", r"i.ve gotta feeling.*1:29"),
    (r"lets get it started", r"let.?s get it started.*black eyed peas"),
    (r"gasolina", r"gasolina.*daddy yankee"),
]


def master_rows():
    rows = []
    with open(os.path.join(HERE, "MASTER_TIMETABLE.md"), encoding="utf-8") as fh:
        rows += [("md", l.lower()) for l in fh]
    with open(os.path.join(CARDS, "master_timetable.html"), encoding="utf-8") as fh:
        raw = fh.read()
    rows += [("html", re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", r))).lower())
             for r in re.findall(r"<tr.*?</tr>|<li.*?</li>|<p.*?</p>", raw, re.S)]
    return rows


def check_master(rules_for):
    """Every distinct CSV cell must be matched by a row in BOTH MASTER_TIMETABLE.md and the master HTML."""
    rows = master_rows()
    seen, gaps = set(), []
    for person, cells in load_cells().items():
        slug = ALIAS.get(person, person)
        for key, label, cell in cells:
            low = cell.lower()
            if low in seen:
                continue
            seen.add(low)
            rule = next((r[1] for r in MASTER_RULES if re.search(r[0], low)), None) or rules_for(slug, low)
            if rule is None:
                continue
            pat = re.compile(rule)
            for fmt in ("md", "html"):
                if not any(f == fmt and pat.search(t) for f, t in rows):
                    gaps.append((person, key, label, cell, rule, fmt))
    return gaps


# Must-bring table checks: (person-row regex, [regexes that must all appear in that row]) in both master formats.
MUST_BRING_CHECKS = [
    (r"adam \(groom", [r"\$500", r"\$200", r"the ring", r"blue suit", r"presents? for karin"]),
    (r"brittany \(bride", [r"wedding dress shoes", r"purse", r"hair extensions", r"something old|borrowed"]),
    (r"marie", [r"hold brittany's dress"]),
    (r"karin \(mother", [r"crate", r"money box", r"wagon", r"bubbles"]),
    (r"tomas . radka|tomas &amp; radka", [r"food and formula", r"headphones", r"dominik"]),
    (r"madison", [r"formula", r"wagon"]),
    (r"peter \(father", [r"omi", r"cousin", r"car"]),
]


def check_must_bring():
    gaps = []
    rows = master_rows()
    for rowrx, needs in MUST_BRING_CHECKS:
        for fmt in ("md", "html"):
            cands = [t for f, t in rows if f == fmt and re.search(rowrx, t) and (fmt == "html" or t.count("|") > 2)]
            for n in needs:
                if not any(re.search(n, t) for t in cands):
                    gaps.append((rowrx, n, fmt))
    return gaps


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
            for (who, rx), need in CELL_OVERRIDES.items():
                if who == slug and re.search(rx, low):
                    rule = (rx, need)
            if rule is None:
                unmapped.append((slug, key, label, cell))
            elif not re.search(rule[1], text):
                gaps.append((slug, key, label, cell, rule[1]))

    def rules_for(slug, low):
        rule = next((r for r in CELL_RULES if re.search(r[0], low)), None)
        for (who, rx), need in CELL_OVERRIDES.items():
            if who == slug and re.search(rx, low):
                rule = (rx, need)
        return rule[1] if rule else None

    mgaps = check_master(rules_for)
    for m in mgaps:
        print(f"MASTER   {m[0]:9} [{m[1]}|{m[2]}] {m[3][:70]}   ({m[5]} master lacks /{m[4]}/)")
    for rowrx, n, fmt in check_must_bring():
        mgaps.append(("must-bring", fmt, rowrx, n, n, fmt))
        print(f"MUSTBRING {rowrx} lacks /{n}/ in {fmt} master")
    broken = check_links()
    wide = check_time_groups()
    timing_gaps = check_event_hours()
    for w in wide:
        print(f"WIDE     {w[0]} section '{w[1]}' spans 15+ minutes")
    for name, need in timing_gaps:
        print(f"TIME     {name} lacks /{need}/")
    print(f"CSV columns intentionally without cards (not audited): {', '.join(sorted(set(no_card))) or 'none'}")
    for g in gaps:
        print(f"GAP      {g[0]:9} [{g[1]}|{g[2]}] {g[3][:80]}   (card lacks /{g[4]}/)")
    for u in unmapped:
        print(f"UNMAPPED {u[0]:9} [{u[1]}|{u[2]}] {u[3][:80]}")
    for b in broken:
        print(f"BROKEN   {b[0]} -> {b[1]}")
    print(f"\n{len(gaps)} gap(s), {len(unmapped)} unmapped cell(s), {len(broken)} broken link(s), {len(wide)} over-wide section(s), {len(mgaps)} master-plan gap(s), {len(timing_gaps)} event-hours gap(s)")
    return 1 if gaps or broken or wide or mgaps or timing_gaps else (2 if unmapped else 0)


if __name__ == "__main__":
    sys.exit(main())
