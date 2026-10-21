# Project Context for Agents

## What This Project Is

This is a private wedding-planning workspace for Brittany and Adam. It combines source planning records with the couple's weekend schedule, logistics reviews, personalized HTML itinerary cards, and fantasy-style wedding-party portraits. The planned events are Friday, November 6 and Saturday, November 7, 2026, in the Great Neck / College Point / Flushing, New York area.

## Start Here

- [MASTER_TIMETABLE.md](./MASTER_TIMETABLE.md) is the detailed human-readable weekend plan: schedule, ceremony and entrance orders, transportation, items to bring, catering, vendors, and urgent follow-ups.
- [LOGISTICS_REVIEW.md](./LOGISTICS_REVIEW.md) documents cross-checks, conflicts and pacing risks, and distinguishes confirmed arrangements from suggestions.
- `generate_cards.py` contains the data and templates for the master HTML timetable, the party-member day cards, and the gallery index in `cards/`.

Read the relevant source records before changing names, times, roles, vendor details, guest lists, or contractual arrangements. The Markdown plan, generator data, and generated HTML can drift; do not assume one is automatically derived from another.

## Files and Update Workflow

- `generate_cards.py` writes `cards/master_timetable.html`, `cards/index.html`, and the per-person `*_day1.html` / `*_day2.html` pages. Update its embedded schedule/card data and templates when changing generated content. Update `MASTER_TIMETABLE.md` as well when the change affects the human-readable plan. Regenerate from the project root with `python generate_cards.py`, then inspect the affected output.
- `cards/style.css` and `cards/gallery.css` control the generated pages' styles. The card pages link to portrait files under `dnd_portraits/`.
- `generate_dnd_portraits.py` uses source photos in `wedding_party_pictures/` and `run_comfy_graph.py` to create images in `dnd_portraits/`. Image generation depends on a running/configured ComfyUI service and may use external compute. It skips portraits that already exist. Do not run it unless portrait generation is part of the requested change.
- `run_comfy_graph.py` runs ComfyUI workflows; `workflow_files/` contains workflow inputs. Avoid changing service configuration or workflow files without a specific need.
- Root CSV and PDF files are source records for schedule, venue, hotel, transport, budget, menu, florist, and RSVP details. They are reference material, not disposable build artifacts.

Run generators only when needed: they overwrite generated files. Keep edits to generated HTML in the generator as well, or they will be lost on regeneration.

## Timetable Updates (repeatable process)

When the timetable CSVs change, follow [UPDATE_WORKFLOW.md](./UPDATE_WORKFLOW.md). In short: edit `generate_cards.py` and `MASTER_TIMETABLE.md`, run `./build.sh` (regenerates all cards, then runs `audit_cards.py`, which checks every CSV cell appears on that person's cards), and fix any `GAP`/`UNMAPPED`/`BROKEN` lines until it exits 0. `python3 audit_cards.py --dump <name>` shows one person's full CSV slice.

## Accuracy and Privacy

- Treat contractual/source-record details as stronger evidence than inferred planning suggestions. Preserve labels such as `[Suggested]` and clearly identify assumptions; do not turn a recommendation into a confirmed arrangement.
- Dates, room-block status, payment deadlines, transportation, vendor contacts, headcounts, and other logistics are time-sensitive. Check the current date and the latest source documents before presenting any item as still urgent or confirmed.
- This workspace contains personal information, guest/RSVP data, contact details, contracts, budgets, and identifiable photos. Use only the minimum necessary details in outputs; do not copy sensitive source data into new documentation, publish it, or send it to external services without explicit authorization.
- Preserve the couple's names, role spellings/capitalization, and established schedule wording unless a source or the user confirms a correction. In particular, distinguish similarly named people by their documented role rather than guessing.

## Action and Itinerary Writing

- Itemize actions: one concrete action per bullet, numbered step, or timetable row. Do not combine separate tasks into a vague summary such as “take photos, make the entrance, and share a dance.”
- Put each action in chronological order and include its date/time or a clear relative cue (for example, “after the second course” or “after the previous entrance group”). When the exact minute is not confirmed, use the documented time window or cue rather than inventing a time.
- For every processional or grand-entrance entry, state who walks together and which person/group enters immediately before them. Do not rely on an unordered list of names alone.
- Keep the Markdown plan, generator data, and generated HTML consistent. When editing generated itineraries, update the generator and the human-readable plan, then regenerate and inspect the affected pages.

## Development and Validation

- The project is primarily standalone Python scripts and static HTML/CSS. No test suite or dependency manifest was present when this guidance was written. A local `.venv` exists, but do not assume its packages or external services are available.
- For card/timetable changes, use the smallest relevant validation: run `python generate_cards.py` from the project root if regeneration is intended, then inspect the generated pages and confirm that links and referenced assets exist. Do not invoke the portrait-generation or ComfyUI workflow merely to validate HTML changes.
