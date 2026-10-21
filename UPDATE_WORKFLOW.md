# Timetable Update Workflow (cards + master battle plan)

This is the repeatable process for turning a revised timetable into updated
person cards, the master battle plan, and the Markdown plan. Follow it every
time the timetable changes (the Oct 18 update followed exactly these steps).

## 1. What produces what

| Artifact | Produced by | Edited by hand? |
|---|---|---|
| `Wedding 2025 Brittany + Adam - Time table {before,church,reception}.csv` | The couple's spreadsheet export | **Source of truth** — replace the file, never edit it for convenience |
| `generate_cards.py` | — | **Yes.** Single source for all card text, the master battle plan HTML, the index, and the print packet |
| `MASTER_TIMETABLE.md` | — | **Yes.** Human-readable plan; must mirror the generator's shared tables |
| `LOGISTICS_REVIEW.md` | — | **Yes.** Conflicts, risks, confirmed vs. suggested items |
| `cards/*.html` (person `_day1`/`_day2`, `master_timetable`, `index`, `print_all`) | `generate_cards.py` | **Never.** Overwritten on every run |
| `audit_cards.py` | — | Only to add rules (step 6) |
| `build.sh` | — | Rarely |

Nothing is derived automatically from the CSVs: the CSVs are *compared* against
the cards by `audit_cards.py`. Content still has to be written into the
generator and the Markdown plan.

## 2. Prerequisites

- Python 3 (standard library only; no packages needed). `build.sh` uses
  `python3` or `$PYTHON`.
- Run everything from this project directory — the generator writes to the
  relative `cards/` folder and the audit resolves paths from its own location.
- Do **not** run `generate_dnd_portraits.py` / ComfyUI; portraits already exist.

## 3. Step-by-step

1. **Drop in the new CSVs.** Export the three tabs (before, church,
   reception) and overwrite the three files named above. Keep the exact
   filenames.
2. **Diff the change.** See what moved: `git diff` if under git, otherwise keep
   a copy of the old CSVs first (`cp` to a scratch folder) and run
   `diff old.csv new.csv`. List every changed cell per person.
3. **Look at each person's complete CSV slice:**
   `python3 audit_cards.py --dump marie` (or without a name for everyone). Each
   line is `[file|row label] cell text`, so you can read one person's whole day.
4. **Edit `generate_cards.py`** in this order:
   1. Per-person entries in `PEOPLE` (`rehearsal`, `duties`, `rehearsal_reminder`,
      `reminder`, `cost`). `rehearsal` is the Day 1 (Friday) card; `duties` is
      the Day 2 (Saturday) card; each is a list of `(heading, [bullets])`.
   2. Shared tables: `FRIDAY_ROWS`/`FRIDAY_NOTES`, `SATURDAY_ROWS`,
      `PROCESSIONAL_ORDER`, `GRAND_ENTRANCE_ORDER`, `TRANSPORT_ROWS`/`TRANSPORT_NOTES`,
      `MUST_BRING_ROWS`, `URGENT_ITEMS`. These feed the master battle plan.
   3. If a person needs a one-off line the generic rules won't add, put it in
      `PERSON_EXTRAS` (see section 4).
5. **Edit `MASTER_TIMETABLE.md`** so it says the same thing as the shared tables
   (schedule, processional order, entrance order, transport, items to bring).
   Update `LOGISTICS_REVIEW.md` if the change creates, removes, or resolves a
   conflict, timing risk, or transport issue.
6. **Rebuild and audit:** `./build.sh`
   - Regenerates all 43 HTML files and then runs the audit.
   - Exit codes: `0` clean; `1` gaps or broken links; `2` only unmapped cells.
7. **Resolve audit output:**
   - `GAP person [file|row] cell (card lacks /regex/)` — the card is missing that
     CSV cell. Add the action to the generator (step 4) and rebuild.
   - `UNMAPPED ...` — a new kind of cell the audit has no rule for. Decide whether
     the card must show it; if so add it to the card; then add a `(cell regex,
     card regex)` pair to `CELL_RULES` in `audit_cards.py` so future runs check it.
   - `BROKEN file -> ref` — a link or portrait path doesn't resolve; fix the
     generator template or restore the asset.
8. **Inspect the output.** Open `cards/index.html`, `cards/master_timetable.html`
   and a few changed cards (always the people whose cells changed). Skim
   `cards/print_all.html` since that is what gets printed.
9. **Stale-text sweep.** Grep the generator, the two `.md` files, and `cards/`
   for names/times/places that were *removed* in the update (old venue names,
   old times, old pickup locations). The sweep should find none.
10. **Report** what changed, plus any source ambiguities that were *flagged,
    not invented* (see section 6).

## 4. How the generator builds each card

- `PEOPLE` holds the hand-written content. At import time `fill_source_gaps()`
  runs over every person and appends only the *shared* items that person's
  CSV column requires but their entry doesn't already contain (arrival at
  church, kneeling, bubbles, line outside, 3:30 PM bus, 4:30 suite, 5:30
  pictures, 6:30 cocktail hour, arch, dinner, cake, open dancing, groomsmen
  photos). It detects existing coverage by regex, so hand-written lines always win.
- Membership sets at the top of that block (`SUITE_GROUP`, `GROOMSMEN`,
  `ARRIVE_BY_BUS`, `NO_BUBBLES_OR_ARCH`) say who gets which shared item. Edit
  them when the group composition changes (for example a new person in the
  suite).
- `PERSON_EXTRAS` maps a slug to extra lines `(day key, section heading, text,
  detect regex, insert-before regex)`. Use it for person-specific cells (for
  example the pastor envelope, petal broom). The line is skipped when the
  detect regex already matches that person's content.
- Reception bullets are re-sorted by time/cue after gap filling, so appended
  items land in chronological order.
- `write_card`, `write_master_card`, `write_print_packet`, and `main` render
  HTML. Shared styling is in `cards/style.css` and `cards/gallery.css`.

## 5. Writing rules (from `AGENTS.md`)

- One action per bullet, in chronological order.
- Every processional/entrance entry says who walks with whom **and** who is
  immediately before them.
- Don't invent times. Use the documented time window or cue, and mark guesses
  `[Suggested]`.
- Preserve names, role spellings, and `[Suggested]` labels.
- Keep generator, Markdown plan, and generated HTML consistent.
- Don't copy sensitive source data (contacts, budget, RSVP) into documentation.

## 6. Naming and source quirks

- CSV headers differ from card names: Brittney = Brittany, Petr = Peter (slug
  `peter`), Sophia = Sofia. Cells also contain misspellings ("Emerik", "Omni",
  "Cocktain", "rehersal"). The audit's `ALIAS` and rule regexes absorb these.
- Some CSV columns have no card (listed by the audit under "without cards"). Add
  a card via a new `PEOPLE` entry if one is wanted; remove the name from
  `NO_CARD` in `audit_cards.py` at the same time.
- Overlaps that the source itself contains must be **flagged on the plan, not
  silently resolved**: a person listed in two simultaneous entrances, or on two
  bus waves. Raise them in `MASTER_TIMETABLE.md` ("Confirm before the
  rehearsal") and `LOGISTICS_REVIEW.md`.

## 7. Command cheat-sheet

```bash
./build.sh                       # regenerate everything + audit
./build.sh --audit               # audit only
python3 audit_cards.py --dump    # every CSV cell per person
python3 audit_cards.py --dump marie
python3 generate_cards.py        # regenerate only
```

## 8. Troubleshooting

- `FileNotFoundError` / output in the wrong place: you ran from another
  directory. `cd` to this folder (or use `./build.sh`, which does it for you).
- Audit says a card lacks something you wrote: the audit matches by regex —
  use the wording in the card regex or loosen the rule in `CELL_RULES`.
- Edited an HTML file and the change vanished: expected. Make the edit in
  `generate_cards.py`.
- A new person appears in a CSV: add a `PEOPLE` entry (and portrait via the
  portrait workflow only if requested), then rebuild.

## 9. Definition of done

- [ ] CSVs replaced; per-person changes listed
- [ ] `generate_cards.py` and `MASTER_TIMETABLE.md` updated (and `LOGISTICS_REVIEW.md` if relevant)
- [ ] `./build.sh` exits `0` (43 HTML files, no gaps, no unmapped cells, no broken links)
- [ ] Changed cards and the master plan opened and read
- [ ] Stale-text sweep clean
- [ ] Open ambiguities listed to the couple
