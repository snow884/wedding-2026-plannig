"""Generates Dungeons & Dragons style fantasy portraits for the wedding party
using the ComfyUI image-edit workflow in run_comfy_graph.py.

Each wedding party member's real photo (wedding_party_pictures/) is transformed
into a fantasy RPG character portrait while preserving their likeness. Output
images are written to dnd_portraits/.
"""
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run_comfy_graph import generate_image_from_images_and_prompt

PICTURES_DIR = "wedding_party_pictures"
OUTPUT_DIR = "dnd_portraits"

# Fun D&D class/title + tailored prompt per wedding party member.
# "title" is used later for the MTG-style cards.
PARTY = [
    {
        "file": "marie_maid_of_honor.webp",
        "slug": "marie",
        "role": "Maid of Honor",
        "title": "High Priestess of Devotion",
        "class_desc": (
            "a radiant Cleric High Priestess in flowing white-and-gold ceremonial "
            "robes with a glowing holy symbol pendant, ornate silver circlet, "
            "soft divine light radiating around her hands"
        ),
    },
    {
        "file": "gustavo_best_man.webp",
        "slug": "gustavo",
        "role": "Best Man",
        "title": "Dragon Knight Commander",
        "class_desc": (
            "a noble human Paladin in ornate engraved silver plate armor with a "
            "flowing deep royal-blue cape, holding a radiant longsword, "
            "confident heroic pose"
        ),
    },
    {
        "file": "dalia_bridesmaid.webp",
        "slug": "dalia",
        "role": "Bridesmaid",
        "title": "Shadowblade Ranger",
        "class_desc": (
            "a sharp-eyed Ranger in forest-green leather armor with a hooded "
            "cloak, twin curved daggers at her hips, a short bow across her "
            "back, standing alert in a misty forest"
        ),
    },
    {
        "file": "julia_bridesmaid.webp",
        "slug": "julia",
        "role": "Bridesmaid",
        "title": "Starlight Sorceress",
        "class_desc": (
            "an elegant Sorceress in a flowing midnight-blue gown embroidered "
            "with constellations, swirling arcane starlight energy around her "
            "fingertips, a crystal pendant glowing at her throat"
        ),
    },
    {
        "file": "julie_bridesmaid.webp",
        "slug": "julie",
        "role": "Bridesmaid",
        "title": "Wildheart Druid",
        "class_desc": (
            "a nature-bonded Druid wearing woven leaf-and-vine armor over "
            "earthy robes, a gnarled wooden staff topped with a glowing green "
            "crystal, flowers blooming where she stands"
        ),
    },
    {
        "file": "bara_bridesmaid.webp",
        "slug": "bara",
        "role": "Bridesmaid",
        "title": "Silver-Tongue Bard",
        "class_desc": (
            "a charismatic Bard in a rich burgundy and gold performer's coat, "
            "holding an ornate lute, feathered hat, confident charming smile, "
            "warm stage lighting"
        ),
    },
    {
        "file": "autumn_bridesmaid.webp",
        "slug": "autumn",
        "role": "Bridesmaid",
        "title": "Moonlit Rogue",
        "class_desc": (
            "a cunning Rogue in fitted dark leather armor with subtle silver "
            "filigree, twin daggers sheathed at her belt, a sly confident "
            "smirk, moody moonlit alley backdrop"
        ),
    },
    {
        "file": "chris_groomsman.webp",
        "slug": "chris",
        "role": "Groomsman",
        "title": "Ironclad Fighter",
        "class_desc": (
            "a battle-hardened Fighter in heavy burnished steel plate armor, "
            "a greatsword resting on his shoulder, a determined heroic "
            "stance, epic fantasy battlefield lighting"
        ),
    },
    {
        "file": "Erik_groomsman.webp",
        "slug": "erik",
        "role": "Groomsman",
        "title": "Stormcaller Barbarian",
        "class_desc": (
            "a fierce Barbarian with fur-trimmed leather armor and tribal "
            "tattoos, wielding a massive war axe crackling with storm energy, "
            "wind-swept hair, dramatic lightning sky behind him"
        ),
    },
    {
        "file": "max_groomsman.webp",
        "slug": "max",
        "role": "Groomsman",
        "title": "Iron Fist Monk",
        "class_desc": (
            "a disciplined Monk in simple saffron-and-grey martial robes with "
            "wrapped forearms, calm focused expression, faint glowing chi "
            "energy around his fists, serene temple courtyard backdrop"
        ),
    },
    {
        "file": "meda_flower_girl.webp",
        "slug": "meda",
        "role": "Flower Girl",
        "title": "Petal Pixie",
        "class_desc": (
            "an adorable tiny Pixie sprite with delicate glittering "
            "dragonfly wings, a dress woven from flower petals, scattering "
            "sparkling flower petals, whimsical enchanted garden background, "
            "keep this cheerful and child-appropriate"
        ),
    },
    {
        "file": "sofia_flower_girl.webp",
        "slug": "sofia",
        "role": "Flower Girl",
        "title": "Blossom Sprite",
        "class_desc": (
            "an adorable tiny woodland Sprite with soft glowing butterfly "
            "wings, a flowing dress made of blooming flowers, surrounded by "
            "floating petals, whimsical enchanted garden background, keep "
            "this cheerful and child-appropriate"
        ),
    },
    {
        "file": "madison_dauther_of_adam_and_brittany.webp",
        "slug": "madison",
        "role": "Daughter of the Bride & Groom",
        "title": "Junior Sorceress Princess",
        "class_desc": (
            "a cheerful young Sorceress Princess in a sparkling lavender gown "
            "with a small silver tiara, a tiny glowing wand in hand, "
            "playful sparkle magic around her, whimsical storybook castle "
            "background, keep this cheerful and child-appropriate"
        ),
    },
    {
        "file": "emeric_ring_bearer.webp",
        "slug": "emeric",
        "role": "Ring Bearer",
        "title": "Halfling Ring Courier",
        "class_desc": (
            "a brave little Halfling courier in a tiny embroidered vest and "
            "cloak, proudly carrying an ornate velvet ring box that glows "
            "softly, cheerful determined expression, cozy fantasy village "
            "background, keep this cheerful and child-appropriate"
        ),
    },
    {
        "file": "adam_groom.jpg",
        "slug": "adam",
        "role": "Groom",
        "title": "Oathbound Groom Paladin",
        "class_desc": (
            "a noble human Paladin groom in elegant black-and-gold ceremonial "
            "armor, a deep blue cloak and a subtle wedding boutonniere, holding "
            "a radiant longsword in a confident, warm pose"
        ),
    },
    {
        "file": "brittany_bride.jpg",
        "slug": "brittany",
        "role": "Bride",
        "title": "Dawnlit Bride Sorceress",
        "class_desc": (
            "a radiant human Sorceress bride in an elegant ivory-and-gold "
            "ceremonial gown, delicate floral details and gentle arcane light "
            "glowing around her hands, poised and joyful"
        ),
    },
    {
        "file": "karin_mom_of_bride.jpg",
        "slug": "karin",
        "role": "Mother of the Bride",
        "title": "Keeper of the Hearth",
        "class_desc": (
            "a wise human Cleric matriarch in graceful plum-and-gold robes, "
            "wearing a small radiant pendant and carrying a softly glowing "
            "lantern, composed and warmly welcoming"
        ),
    },
    {
        "file": "Peter_father_of_bride.jpg",
        "slug": "Peter",
        "role": "Father of the Bride",
        "title": "Vowshield Cavalier",
        "class_desc": (
            "a dignified human Cavalier in refined silver-and-navy ceremonial "
            "armor with a blue cloak, carrying a polished shield engraved with "
            "a subtle family crest, noble and reassuring"
        ),
    },
    {
        "file": "radka_mother_of_groom.jpg",
        "slug": "radka",
        "role": "Mother of the Groom",
        "title": "Moonlit Matriarch",
        "class_desc": (
            "a gracious human Druid matriarch in elegant forest-green and "
            "silver robes, surrounded by delicate leaves and a gentle "
            "moonlit glow, serene and welcoming"
        ),
    },
    {
        "file": "tomas_father_of_groom.jpg",
        "slug": "tomas",
        "role": "Father of the Groom",
        "title": "Bannerlord of the Vows",
        "class_desc": (
            "a steadfast human Fighter and family patriarch in tasteful "
            "bronze-and-charcoal ceremonial armor, a warm mantle and a "
            "decorative banner, standing proudly with a calm, kind expression"
        ),
    },
]

PROMPT_TEMPLATE = (
    "Transform the person in the photo into a heroic Dungeons & Dragons fantasy "
    "character portrait: {class_desc}. Dramatic fantasy lighting, epic matte "
    "painting style, highly detailed, sharp focus. Preserve the subject's exact "
    "face, identity, skin tone, hair, and facial features. Fantasy tabletop RPG "
    "character art, trending on artstation."
)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    only = sys.argv[1:] if len(sys.argv) > 1 else None

    failures = []
    for person in PARTY:
        if only and person["slug"] not in only:
            continue

        input_path = os.path.join(PICTURES_DIR, person["file"])
        output_path = os.path.join(OUTPUT_DIR, f"{person['slug']}_dnd.png")

        if os.path.exists(output_path):
            print(f"⏭️  Skipping {person['slug']} (already exists: {output_path})")
            continue

        prompt = PROMPT_TEMPLATE.format(class_desc=person["class_desc"])

        print("\n" + "=" * 70)
        print(f"🎨 Generating portrait for {person['slug']} — {person['title']}")
        print("=" * 70)

        try:
            generate_image_from_images_and_prompt(
                input_image_paths=[input_path],
                prompt=prompt,
                output_file_path=output_path,
            )
            print(f"✅ Done: {output_path}")
        except Exception:
            print(f"❌ Failed generating portrait for {person['slug']}")
            traceback.print_exc()
            failures.append(person["slug"])

    if failures:
        print("\n⚠️ Failed for:", ", ".join(failures))
    else:
        print("\n🎉 All requested portraits generated successfully.")


if __name__ == "__main__":
    main()
