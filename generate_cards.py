"""Generates MTG-playing-card-styled HTML instruction cards for every member of
the wedding party, embedding their D&D portrait (dnd_portraits/) and a
personalized itinerary pulled from the master wedding timetable.

Run after generate_dnd_portraits.py has produced the portraits.
"""
import os

OUTPUT_DIR = "cards"
PORTRAIT_DIR_REL = "../dnd_portraits"

# frame: one of white / blue / black / green / red (MTG color identity, reused
# here as a simple visual grouping by wedding role)
PEOPLE = [
    {
        "slug": "marie",
        "name": "Marie Frances Villamor",
        "title": "High Priestess of Devotion",
        "role": "Maid of Honor",
        "frame": "white",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["Check into the Inn at Great Neck (after 3:00 PM)."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Practice the processional, Brittany's bouquet hand-off, and your position beside her at the altar.",
            ]),
            ("4:05 PM", ["Adam &amp; Brittany step aside to privately practice their vows — a quiet moment, give them space."]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family.",
                "Good time to compare notes with Gustavo so your two speeches don't overlap tomorrow.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes (not your wedding heels yet!), a draft of your MOH speech to compare with Gustavo.",
        "duties": [
            ("Morning", ["10:00 AM: arrive at the Inn at Great Neck for pre-ceremony pictures with the other bridesmaids.",
                        "12:00 PM: Pictures of the Bridesmaids group at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — "
                         "board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in alone right after Bara and Autumn process in together, and right before "
                "the flower girls — take your position at the altar just ahead of Brittany's entrance.",
                "When Brittany walks in with Peter, she will hand you her bouquet. "
                "Hold it safely for the entire ceremony.",
                "Exit the church after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party (apps + drinks).",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 4 of 8: walk in with Gustavo (Best Man), "
                "immediately after Emeric, Meda, Sofia, and Madison.",
                "9:00–10:15 PM Formal Speeches segment (after the second course and before entrées): "
                "deliver your Maid of Honor speech after Peter and Karin's parents' speech; exact minute is not specified.",
            ]),
        ],
        "reminder": "Must bring: Brittany's bouquet hand-off reminder, MOH speech notes, "
                    "tissues/emergency kit. Don't let the bouquet get left behind in the limo!",
        "flavor": "“Mama Marie” — Brittany's best friend since high school, always "
                  "prepared for anything.",
    },
    {
        "slug": "gustavo",
        "name": "Gustavo Adolfo Gándara Montaño",
        "title": "Dragon Knight Commander",
        "role": "Best Man",
        "frame": "white",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["Check into the Inn at Great Neck (after 3:00 PM)."]),
            ("Thursday, Nov 5", ["Pick up your tux from Men's Wearhouse."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Practice standing beside Adam at the altar and confirm the ring hand-off choreography with the officiant and Emeric.",
            ]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family.",
                "Compare speech notes with Marie so your toasts complement each other tomorrow.",
                "Return to the hotel by 8:00 PM with Adam, Meda, Tomas, and Radka.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, a draft of your Best Man speech, your tux pickup confirmation from Thursday.",
        "duties": [
            ("Morning", ["10:00 AM: Pictures of the groomsmen at the hotel (you, Chris, Erik, Max, and Tomas)."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (first wave, with Chris, Erik, Max, and Tomas) — board by 1:00 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Enter the church ahead of the family processional and wait at the altar beside Adam.",
                "Suggested: carry the real wedding rings yourself and let Emeric present a decoy "
                "pair on the ring pillow — classic insurance against a toddler losing the rings.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 4 of 8: walk in with Marie (Maid of Honor), "
                "immediately after Emeric, Meda, Sofia, and Madison.",
                "9:00–10:15 PM Formal Speeches segment (after the second course and before entrées): "
                "deliver your Best Man speech after Marie's Maid of Honor speech; exact minute is not specified.",
            ]),
        ],
        "reminder": "Must bring: the real wedding rings (if using the decoy-ring plan), "
                    "Best Man speech notes.",
        "flavor": "A close friend who met Adam at the University of Rochester — "
                  "amazing gentleman, highly intelligent.",
    },
    {
        "slug": "dalia",
        "name": "Dalia Mathew",
        "title": "Shadowblade Ranger",
        "role": "Bridesmaid",
        "frame": "black",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["Check into the Inn at Great Neck (after 3:00 PM)."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Attend the full processional walkthrough and confirm your position in line with the officiant.",
            ]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes — save the dancing shoes for tomorrow night.",
        "duties": [
            ("Morning", ["10:00 AM: arrive at the Inn at Great Neck for pre-ceremony pictures with the other bridesmaids.",
                        "12:00 PM: Pictures of the Bridesmaids group at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in on Max's arm right after Tomas walks in Radka — proceed straight to "
                "your position at the altar.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 7 of 8: walk in with Max and Julie, "
                "immediately after Erik and Julia.",
                "After the 7:45 PM first dance and the parent dances (~7:50 PM): join open dancing when the MC/DJ opens the floor; follow the MC/DJ's cues around scheduled events through the 12:30 AM reception end.",
            ]),
        ],
        "reminder": "Must bring: comfortable flats for dancing, dress code is any color but white.",
        "flavor": "“Daliamma” — Brittany's best friend since middle school; the laughter never stops.",
    },
    {
        "slug": "julia",
        "name": "Julia Dietrich",
        "title": "Starlight Sorceress",
        "role": "Bridesmaid",
        "frame": "black",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["Check into the Inn at Great Neck (after 3:00 PM)."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Attend the full processional walkthrough and confirm your position in line with the officiant.",
                "If your daughter Sofia is doing her flower-girl walkthrough, plan to arrive together.",
            ]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, Sofia's rehearsal outfit if she's doing her walkthrough.",
        "duties": [
            ("Morning", ["10:00 AM: arrive at the Inn at Great Neck for pre-ceremony pictures with the other bridesmaids.",
                        "12:00 PM: Pictures of the Bridesmaids group at the hotel — Sofia joins this group photo too."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in arm-in-arm with Julie right after Dalia and Max process in — proceed "
                "straight to your position at the altar.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 6 of 8: walk in with Erik, "
                "immediately after Chris, Autumn, and Bara.",
                "After the 7:45 PM first dance and the parent dances (~7:50 PM): join open dancing when the MC/DJ opens the floor; follow the MC/DJ's cues around scheduled events through the 12:30 AM reception end.",
            ]),
        ],
        "reminder": "Must bring: comfortable flats for dancing, dress code is any color but white. "
                    "(Note: a different guest named Julia is Sofia's mom — don't mix up your seating card!)",
        "flavor": "Brittany's cousin and childhood partner-in-crime — lemonade stands, sleepovers, "
                  "and late-night dancing until bedtime.",
    },
    {
        "slug": "julie",
        "name": "Julianna “Julie” Anderson",
        "title": "Wildheart Druid",
        "role": "Bridesmaid",
        "frame": "black",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["Check into the Inn at Great Neck (after 3:00 PM)."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Attend the full processional walkthrough and confirm your position in line with the officiant.",
            ]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family — sit with your husband Max!",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes — save the dancing shoes for tomorrow night.",
        "duties": [
            ("Morning", ["10:00 AM: arrive at the Inn at Great Neck for pre-ceremony pictures with the other bridesmaids.",
                        "12:00 PM: Pictures of the Bridesmaids group at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in arm-in-arm with Julia right after Dalia and Max process in — proceed "
                "straight to your position at the altar.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 7 of 8: walk in with Max and Dalia, "
                "immediately after Erik and Julia.",
                "After the 7:45 PM first dance and the parent dances (~7:50 PM): join open dancing when the MC/DJ opens the floor; follow the MC/DJ's cues around scheduled events through the 12:30 AM reception end.",
            ]),
        ],
        "reminder": "Must bring: comfortable flats for dancing, dress code is any color but white.",
        "flavor": "Brittany's best friend since high school Spanish class — always up for an adventure.",
    },
    {
        "slug": "bara",
        "name": "Bara Vystejn Ivanska",
        "title": "Silver-Tongue Bard",
        "role": "Bridesmaid",
        "frame": "black",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["You and Meda are traveling internationally from the Czech Republic — build in buffer time for jet lag before checking into the Inn at Great Neck (after 3:00 PM)."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Attend the full processional walkthrough and confirm your position in line with the officiant.",
                "Help coordinate Meda's short, simplified flower-girl walkthrough with Sofia.",
            ]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family. An early night for Meda is recommended given the travel.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, Meda's rehearsal outfit, travel documents/passport copies handy.",
        "duties": [
            ("Morning", ["10:00 AM: arrive at the Inn at Great Neck for pre-ceremony pictures with the other bridesmaids.",
                        "12:00 PM: Pictures of the Bridesmaids group at the hotel — Meda joins this group photo too."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in arm-in-arm with Autumn right after Julia and Julie process in — proceed "
                "straight to your position at the altar.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 5 of 8: walk in with Chris and Autumn, "
                "immediately after Marie and Gustavo.",
                "During the ceremony processional, help Meda get ready immediately before the flower-girl entry (after Erik and Chris escort Omi).",
            ]),
        ],
        "reminder": "Must bring: comfortable flats for dancing, dress code is any color but white.",
        "flavor": "Adam's younger sister, visiting from the Czech Republic for her first trip "
                  "to the United States — welcoming Brittany into the family since 2023.",
    },
    {
        "slug": "autumn",
        "name": "Autumn Ledbetter",
        "title": "Moonlit Rogue",
        "role": "Bridesmaid",
        "frame": "black",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["Check into the Inn at Great Neck (after 3:00 PM)."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Attend the full processional walkthrough and confirm your position in line with the officiant.",
                "As Madison's godmother, help keep her settled if she joins for a quick look at the space.",
            ]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes. Confirm your 7:00 AM pickup with Chris for tomorrow's hair appointment.",
        "duties": [
            ("Morning — Hair Appointment", [
                "7:00 AM: Chris picks you up at the hotel and drives you to Lush Hair Studio, 185 Northern Blvd, Great Neck.",
                "8:30 AM: your hair salon appointment — you're booked together with Brittany, Karin, and Omi, who travel to the same appointment separately (Karin drives herself, Brittany, and Omi).",
                "~10:30 AM: Chris drives you back to the hotel in time for the 12:00 PM bridesmaid pictures.",
            ]),
            ("Late Morning", ["12:00 PM: Pictures of the Bridesmaids group at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in arm-in-arm with Bara right after Julia and Julie process in — proceed "
                "straight to your position at the altar.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 5 of 8: walk in with Chris and Bara, "
                "immediately after Marie and Gustavo.",
                "After the 7:30–7:45 PM Grand Entrance, help Madison stay safe near the dance floor when it is open.",
                "~10:45 PM, during cake cutting: help Madison stay safely with the family.",
            ]),
        ],
        "reminder": "Must bring: comfortable flats for dancing, dress code is any color but white. Your 8:30 AM "
                    "hair appointment at Lush Hair Studio is confirmed (with Brittany, Karin, and Omi) — Chris is driving you there and back starting at 7:00 AM.",
        "flavor": "Madison's doting godmother — always shows up, always has a good time.",
    },
    {
        "slug": "chris",
        "name": "Christopher Novak",
        "title": "Ironclad Fighter",
        "role": "Groomsman",
        "frame": "blue",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["Check into the Inn at Great Neck (after 3:00 PM)."]),
            ("Thursday, Nov 5", ["Pick up your tux from Men's Wearhouse."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Practice escorting Omi down the aisle together with Erik — walk the exact route at her pace so tomorrow isn't the first time.",
                "Confirm the rest of your processional position with the officiant.",
            ]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family. As Madison's godfather, help keep an eye on her if she's there.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, your tux pickup confirmation from Thursday. You and Erik should sync on Omi's pacing/support needs tonight. Set an early alarm — you're driving Autumn to her 7:00 AM hair appointment pickup.",
        "duties": [
            ("Morning — Drive Autumn to Her Hair Appointment", [
                "7:00 AM: pick up Autumn at the hotel and drive her to Lush Hair Studio, 185 Northern Blvd, Great Neck.",
                "8:30 AM: her hair appointment — she's booked together with Brittany, Karin, and Omi (who travel separately, driven by Karin).",
                "~10:30 AM: drive her back to the hotel in time for the 12:00 PM bridesmaid pictures.",
            ]),
            ("Late Morning", ["10:00 AM: Pictures of the groomsmen at the hotel (you, Gustavo, Erik, Max, and Tomas)."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (first wave, with Gustavo, Erik, Max, and Tomas) — board by 1:00 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk Omi (grandmother of the bride) in together with Erik — offer your arm "
                "and go slow. You walk in right after Marie, just before the flower girls.",
                "Deliver Omi to her front-row seat of honor, then step into your position at the "
                "altar beside the other groomsmen.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 5 of 8: walk in with Autumn and Bara, "
                "immediately after Marie and Gustavo.",
                "After the 7:30–7:45 PM Grand Entrance, help Madison stay safe near the dance floor when it is open.",
                "~10:45 PM, during cake cutting: help Madison stay safely with the family.",
            ]),
        ],
        "reminder": "Must bring: black tux/suit (picked up Thursday), boutonniere. You are personally responsible for "
                    "escorting Omi safely down the aisle — confirm the route with her in advance. You're also "
                    "driving Autumn to and from her 8:30 AM hair appointment at Lush Hair Studio — pickup at 7:00 AM sharp.",
        "flavor": "Brittany's younger (but very protective) brother and Madison's godfather.",
    },
    {
        "slug": "erik",
        "name": "Erik Novak",
        "title": "Stormcaller Barbarian",
        "role": "Groomsman",
        "frame": "blue",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["Check into the Inn at Great Neck (after 3:00 PM)."]),
            ("Ceremony Rehearsal (~5:00–6:00 PM, St John's Lutheran Church)", [
                "Attend the full processional walkthrough and confirm your position in line with the officiant.",
            ]),
            ("Rehearsal Dinner (~6:30–8:30 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes. Remember there's also an 'Eric Demery' at this wedding — don't mix up name cards at dinner! You and Chris should sync on Omi's pacing/support needs tonight.",
        "duties": [
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck — board by 1:00 PM. "
                          "Note: there is also an 'Eric Demery' at this wedding (Emeric's dad) — "
                          "don't mix up name cards!"]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk Omi (grandmother of the bride) in together with Chris — offer your arm and "
                "go slow. You walk in right after Marie, just before the flower girls.",
                "Deliver Omi to her front-row seat of honor, then step into your position at the "
                "altar beside the other groomsmen.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 6 of 8: walk in with Julia, "
                "immediately after Chris, Autumn, and Bara.",
            ]),
        ],
        "reminder": "Must bring: black tux/suit (picked up Thursday), boutonniere.",
        "flavor": "Brittany's second younger brother — successful bodybuilder, great friend, "
                  "soon-to-be brother-in-law.",
    },
    {
        "slug": "max",
        "name": "Maxwell Anderson",
        "title": "Iron Fist Monk",
        "role": "Groomsman",
        "frame": "blue",
        "cost": "Call Time 4:30 PM",
        "rehearsal": [
            ("Arrival", ["Check into the Inn at Great Neck (after 3:00 PM)."]),
            ("Thursday, Nov 5", ["Pick up your tux from Men's Wearhouse."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Attend the full processional walkthrough and confirm your position in line with the officiant.",
            ]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Attend with the wedding party and immediate family — sit with your wife Julie!",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, your tux pickup confirmation from Thursday.",
        "duties": [
            ("Morning", ["10:00 AM: Pictures of the groomsmen at the hotel (you, Gustavo, Chris, Erik, and Tomas)."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (first wave, with Gustavo, Chris, Erik, and Tomas) — board by 1:00 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Escort Dalia down the aisle right after Tomas walks in Radka — proceed straight "
                "to your position at the altar beside the other groomsmen.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "~7:00 PM: formal portraits.",
                "7:30–7:45 PM Grand Entrance, group 7 of 8: walk in with Julie and Dalia, "
                "immediately after Erik and Julia.",
                "You're the hype man — keep the dance floor energy up!",
            ]),
        ],
        "reminder": "Must bring: black tux/suit (picked up Thursday), boutonniere.",
        "flavor": "A great friend of Adam's and Julie's husband — the driving force behind every great party.",
    },
    {
        "slug": "meda",
        "name": "Meda Vystejnova",
        "title": "Petal Pixie",
        "role": "Flower Girl",
        "frame": "green",
        "cost": "Call Time 1:00 PM",
        "rehearsal": [
            ("Arrival", ["Traveling internationally from the Czech Republic with your mom Bara — check into the Inn at Great Neck (after 3:00 PM) and rest up from the trip."]),
            ("Ceremony Rehearsal (~5:00–6:00 PM, St John's Lutheran Church)", [
                "A short, simplified walkthrough of your entrance with Sofia — no need for the full grown-up run-through.",
            ]),
            ("Rehearsal Dinner (~6:30–8:30 PM, Leonard's Palazzo private dining room)", [
                "Optional — an early bedtime is recommended since you're jet-lagged and have a big day tomorrow.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: a comfort item for the long travel day, comfortable shoes for the quick walkthrough.",
        "duties": [
            ("Late Morning", ["12:00 PM: join the Pictures of the Bridesmaids group photo at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck together with your "
                          "mom Bara (second/main wave) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in together with Sofia right after Erik and Chris walk Omi to her seat, and "
                "right before Emeric pulls Madison's wagon down the aisle.",
                "Scatter flower petals as you walk — the petal basket is included in the OG Floral order.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "6:30 PM: you join the bridal party's private suite cocktail hour.",
                "7:30–7:45 PM Grand Entrance, group 3 of 8: walk in together with Emeric, Sofia, "
                "and Madison, immediately after Tomas and Radka.",
                "Before the 10:15 PM entrée service: ask a grown-up to request your kids' meal early.",
            ]),
        ],
        "reminder": "Must bring: a comfy outfit change for late-night dancing is a nice-to-have "
                    "(the flower petals/basket are provided by OG Floral).",
        "flavor": "Adam's niece from the Czech Republic (Bara's daughter) — loves dancing and playing outside.",
    },
    {
        "slug": "sofia",
        "name": "Sofia Lopez",
        "title": "Blossom Sprite",
        "role": "Flower Girl",
        "frame": "green",
        "cost": "Call Time 1:00 PM",
        "rehearsal": [
            ("Arrival", ["Travel to the church with your mom Julia."]),
            ("Ceremony Rehearsal (~5:00–6:00 PM, St John's Lutheran Church)", [
                "A short, simplified walkthrough of your entrance with Meda — no need for the full grown-up run-through.",
            ]),
            ("Rehearsal Dinner (~6:30–8:30 PM, Leonard's Palazzo private dining room)", [
                "Optional — an early bedtime is recommended since tomorrow is a big day.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes for the quick walkthrough.",
        "duties": [
            ("Late Morning", ["12:00 PM: join the Pictures of the Bridesmaids group photo at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck together with your "
                          "mom Julia (second/main wave) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in together with Meda right after Erik and Chris walk Omi to her seat, and "
                "right before Emeric pulls Madison's wagon down the aisle.",
                "Scatter flower petals as you walk — the petal basket is included in the OG Floral order.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "6:30 PM: you join the bridal party's private suite cocktail hour.",
                "7:30–7:45 PM Grand Entrance, group 3 of 8: walk in together with Emeric, Meda, "
                "and Madison, immediately after Tomas and Radka.",
                "Before the 10:15 PM entrée service: ask a grown-up to request your kids' meal early.",
            ]),
        ],
        "reminder": "Must bring: a comfy outfit change for late-night dancing is a nice-to-have "
                    "(the flower petals/basket are provided by OG Floral).",
        "flavor": "Brittany's cousin Julia's daughter — loves playing with friends and family, "
                  "ready to show off her dance moves.",
    },
    {
        "slug": "madison",
        "name": "Madison Ivansky",
        "title": "Junior Sorceress Princess",
        "role": "Daughter of the Bride & Groom",
        "frame": "green",
        "cost": "Call Time 1:00 PM",
        "rehearsal": [
            ("Arrival", ["Travel to the rehearsal with your mom Brittany."]),
            ("Ceremony Rehearsal (~5:00–6:00 PM, St John's Lutheran Church)", [
                "Optional and brief — at 1 year old, a full rehearsal isn't necessary. A quick look at the wagon route is enough if her nap schedule allows.",
            ]),
            ("Rehearsal Dinner (~6:30–8:30 PM, Leonard's Palazzo private dining room)", [
                "Optional — plan around her nap/bedtime schedule rather than the dinner start time.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: snacks, a comfort item/blanket, a diaper bag.",
        "duties": [
            ("Late Morning", ["12:00 PM: join the Pictures of the Bridesmaids group photo at the hotel (your mom Brittany brings the wedding bands and wedding invitation as photo props)."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck together with your "
                          "mom Brittany (second/main wave) — board by 1:15 PM. The wagon travels in the bus's luggage bay."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Ride down the aisle in a decorated wagon, pulled by Emeric, right after the flower "
                "girls Meda and Sofia walk in.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "6:30 PM: you join the general Cocktail Hour with the guests (not the bridal party's private suite).",
                "7:30–7:45 PM Grand Entrance, group 3 of 8: enter together with Emeric, Meda, "
                "and Sofia, immediately after Tomas and Radka.",
                "Before the 10:15 PM entrée service: ask a grown-up to request an earlier kids' meal and snacks for a 1-year-old.",
            ]),
        ],
        "reminder": "Must bring: the wagon, snacks, a comfort item/blanket, a diaper bag — she's "
                    "the youngest member of the wedding party!",
        "flavor": "Mom and Dad's \"little nugget\" — already stealing the show at one year old.",
    },
    {
        "slug": "emeric",
        "name": "Emeric Demery",
        "title": "Halfling Ring Courier",
        "role": "Ring Bearer",
        "frame": "red",
        "cost": "Call Time 1:15 PM",
        "rehearsal": [
            ("Arrival", ["Travel with your parents, Eric & April Demery."]),
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Practice pulling Madison's wagon down the aisle and presenting the ring pillow.",
                "Your dad Eric Demery will be busy rehearsing his reading — your mom April will be your point person tonight.",
            ]),
            ("Rehearsal Dinner (6:00–8:00 PM, Leonard's Palazzo private dining room)", [
                "Optional — an early bedtime is recommended since your dad has a lot to prepare for tomorrow too.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: the ring pillow (practice run — no need for the real rings tonight), a comfort item.",
        "duties": [
            ("Arrival", ["Travel with your parents, Eric & April Demery, who drive their own car "
                          "directly to the church — depart the hotel by 1:15 PM to arrive with time "
                          "to spare before the 2:00 PM ceremony."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Pull Madison down the aisle in her wagon, right after the flower girls Meda and Sofia walk in.",
                "Carry the ring pillow forward before the ring exchange. (Suggested: a decoy pair of "
                "rings on your pillow, with Gustavo safely holding the real rings.)",
                "Your dad Eric Demery delivers the prayer/reading right after Brittany hands her "
                "bouquet to Marie — your mom April will be your point person during that moment.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "6:30 PM: you join the general Cocktail Hour with the guests (not the bridal party's private suite).",
                "7:30–7:45 PM Grand Entrance, group 3 of 8: enter together with Meda, Sofia, "
                "and Madison, immediately after Tomas and Radka.",
                "Before the 10:15 PM entrée service: ask a grown-up to request your kids' meal early.",
            ]),
        ],
        "reminder": "Must bring: the ring pillow (decoy rings recommended), a comfort item for a long day.",
        "flavor": "Our adorable ring bearer, ready to make the big day even more special.",
    },
    {
        "slug": "adam",
        "name": "Adam",
        "title": "Oathbound Groom Paladin",
        "role": "Groom",
        "frame": "blue",
        "cost": "Call Time 9:30 AM",
        "rehearsal": [
            ("2:00 PM", ["Set up decorations at St John's Lutheran Church with Brittany."]),
            ("Ceremony Rehearsal (4:00–5:00 PM)", ["Walk through the processional, vows, ring exchange, unity candle, and recessional."]),
            ("Rehearsal Dinner (6:00–8:00 PM)", ["Join the wedding party and immediate family at Leonard's Palazzo."]),
        ],
        "rehearsal_reminder": "Bring the ceremony items needed for setup and your comfortable rehearsal shoes.",
        "duties": [
            ("Morning", ["9:30 AM: receive the florist's bouquet delivery at the hotel.",
                         "After the 9:30 AM delivery: route Brittany's bouquet to her room without seeing her.",
                         "10:00 AM: join the groomsmen photos."]),
            ("1:15 PM", ["Ride with Peter in his car directly to St John's Lutheran Church."]),
            ("Ceremony (2:00 PM)", ["Before the processional: stand with Gustavo at the altar.",
                                    "2:05 PM: exchange vows with Brittany.",
                                    "2:10 PM: light the unity candle with Brittany.",
                                    "At the recessional, after everyone else: exit last with Brittany through the bubble line."]),
            ("Reception", ["After the ~3:00 PM receiving line and before the 3:30 PM bus: join formal photos at Francis Lewis Park; confirm exact start/end with the photographer.",
                           "~5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "~7:00 PM: join the formal room/portrait shots.",
                           "7:30–7:45 PM Grand Entrance, group 8 of 8: walk in with Brittany after Max, Julie, and Dalia; the wedding party forms an arch.",
                           "7:45 PM: have the first dance with Brittany.",
                           "~7:50 PM, immediately after Brittany and Peter's first parent dance: have the second parent dance with Radka (mother–son dance)."]),
        ],
        "reminder": "Bring your marriage license, vows, and wedding band; confirm Peter's ride and tux pickup.",
        "flavor": "The groom — ready to begin a new adventure with Brittany.",
    },
    {
        "slug": "brittany",
        "name": "Brittany",
        "title": "Dawnlit Bride Sorceress",
        "role": "Bride",
        "frame": "white",
        "cost": "Call Time 8:30 AM",
        "rehearsal": [
            ("2:00 PM", ["Set up decorations at St John's Lutheran Church with Adam."]),
            ("Ceremony Rehearsal (4:00–5:00 PM)", ["Walk through the processional, vows, unity candle, and recessional."]),
            ("Rehearsal Dinner (6:00–8:00 PM)", ["Join the wedding party and immediate family at Leonard's Palazzo."]),
        ],
        "rehearsal_reminder": "Bring any ceremony items needed for setup and comfortable rehearsal shoes.",
        "duties": [
            ("Morning", ["Attend the 8:30 AM hair appointment with Karin and Omi.", "Bring the wedding bands and invitation for the 12:00 PM bridesmaids photo."]),
            ("1:15 PM", ["Ride the main-wave limo bus from the Inn at Great Neck to the church."]),
            ("Ceremony (2:00 PM)", ["During the processional: walk in on Peter's arm.",
                                    "2:05 PM: exchange vows with Adam.",
                                    "2:10 PM: light the unity candle with Adam."]),
            ("Reception", ["After the ~3:00 PM receiving line and before the 3:30 PM bus: join formal photos at Francis Lewis Park; confirm exact start/end with the photographer.",
                           "~5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "~7:00 PM: join the formal room/portrait shots.",
                           "7:30–7:45 PM Grand Entrance, group 8 of 8: walk in with Adam after Max, Julie, and Dalia; the wedding party forms an arch.",
                           "7:45 PM: have the first dance with Adam.",
                           "~7:50 PM: have the first parent dance with Peter (father–daughter dance)."]),
        ],
        "reminder": "Keep the wedding bands and invitation with you for the hotel photos; make sure your bouquet gets to the ceremony.",
        "flavor": "The bride — the day's brightest star and the heart of this celebration.",
    },
    {
        "slug": "karin",
        "name": "Karin",
        "title": "Keeper of the Hearth",
        "role": "Mother of the Bride",
        "frame": "white",
        "cost": "Call Time 8:30 AM",
        "rehearsal": [
            ("Ceremony Rehearsal (4:00–5:00 PM)", ["Join the full family walkthrough and practice the candle-lighting ceremony with Peter."]),
            ("Rehearsal Dinner (6:00–8:00 PM)", ["Join the wedding party and immediate family at Leonard's Palazzo."]),
        ],
        "rehearsal_reminder": "Bring the welcome-table and memorial-table crate and wine-box favors to the venue during the week before.",
        "duties": [
            ("Morning", ["Drive yourself, Brittany, and Omi to the 8:30 AM hair appointment."]),
            ("Ceremony (2:00 PM)", ["~2:05 PM: take part in the candle-lighting with Peter, Tomas, and Radka.",
                                    "~2:10 PM: check the reception arrangements at Leonard's Palazzo.",
                                    "2:50 PM: hand bubbles to guests outside the church."]),
            ("Reception", ["After the ~3:00 PM receiving line and before the 3:30 PM bus: join formal photos at Francis Lewis Park; confirm exact start/end with the photographer.",
                           "~5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "7:30–7:45 PM Grand Entrance, group 1 of 8: walk in with Peter as the first entrance group.",
                           "~7:55 PM: give the brief welcome toast with Peter before the first course.",
                           "9:00–10:15 PM Formal Speeches segment, after the second course and before entrées: deliver Brittany's parents' speech with Peter; exact minute is not specified."]),
        ],
        "reminder": "Bring bubbles for the church send-off and confirm the venue crate has everything needed.",
        "flavor": "Brittany's mom — keeping the celebration's many thoughtful details on track.",
    },
    {
        "slug": "Peter",
        "name": "Peter",
        "title": "Vowshield Cavalier",
        "role": "Father of the Bride",
        "frame": "white",
        "cost": "Call Time 9:30 AM",
        "rehearsal": [
            ("Ceremony Rehearsal (4:00–5:00 PM)", ["Join the full family walkthrough and practice the candle-lighting ceremony with Karin."]),
            ("Rehearsal Dinner (6:00–8:00 PM)", ["Join the wedding party and immediate family at Leonard's Palazzo."]),
        ],
        "rehearsal_reminder": "Confirm the car plan for driving Adam to the church on Saturday.",
        "duties": [
            ("Morning", ["Teach your regular Saturday class from 9:30–10:30 AM."]),
            ("1:15 PM", ["1:15 PM: drive Adam directly to St John's Lutheran Church.",
                         "After arrival: leave your car parked at the church."]),
            ("Ceremony (2:00 PM)", ["During the processional: escort Brittany down the aisle.",
                                    "~2:05 PM: take part in the candle-lighting with Karin, Tomas, and Radka."]),
            ("Reception", ["After the ~3:00 PM receiving line: ride from the church to Francis Lewis Park with the bridal party and immediate family.",
                           "After arriving at the park and before the 3:30 PM bus: join formal photos; confirm exact start/end with the photographer.",
                           "At 3:30 PM: ride the Camelot bus from Francis Lewis Park to Leonard's Palazzo.",
                           "~5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "7:30–7:45 PM Grand Entrance, group 1 of 8: walk in with Karin as the first entrance group.",
                           "~7:50 PM: have the first parent dance with Brittany (father–daughter dance).",
                           "~7:55 PM: give the brief welcome toast with Karin before the first course.",
                           "9:00–10:15 PM Formal Speeches segment, after the second course and before entrées: deliver the first speech in the listed sequence with Karin; exact minute is not specified."]),
        ],
        "reminder": "Bring your car keys and welcome-toast/speech notes; your car stays at the church until after the reception.",
        "flavor": "Brittany's dad — escorting his daughter into her next great chapter.",
    },
    {
        "slug": "radka",
        "name": "Radka",
        "title": "Moonlit Matriarch",
        "role": "Mother of the Groom",
        "frame": "white",
        "cost": "Call Time 1:15 PM",
        "rehearsal": [
            ("Ceremony Rehearsal (4:00–5:00 PM)", ["Join the full family walkthrough and practice the candle-lighting ceremony with Tomas."]),
            ("Rehearsal Dinner (6:00–8:00 PM)", ["Join the wedding party and immediate family at Leonard's Palazzo."]),
        ],
        "rehearsal_reminder": "Bring a memorial-table item in memory of your late brother Dominik.",
        "duties": [
            ("Before the Wedding", ["Bring an item in memory of Dominik for the memorial table."]),
            ("Arrival", ["Ride the main-wave limo bus from the Inn at Great Neck to the church."]),
            ("Ceremony (2:00 PM)", ["~2:05 PM: take part in the candle-lighting with Tomas, Karin, and Peter."]),
            ("Reception", ["After the ~3:00 PM receiving line and before the 3:30 PM bus: join formal photos at Francis Lewis Park; confirm exact start/end with the photographer.",
                           "~5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "7:30–7:45 PM Grand Entrance, group 2 of 8: walk in with Tomas immediately after Peter and Karin.",
                           "~7:50 PM, immediately after the first parent dance (Brittany with Peter): have the second parent dance with Adam (mother–son dance).",
                           "9:00–10:15 PM Formal Speeches segment, after the second course and before entrées: deliver the groom's parents' speech with Tomas, after Gustavo's Best Man speech; exact minute is not specified."]),
        ],
        "reminder": "Bring Dominik's memorial-table item and comfortable shoes for the celebration.",
        "flavor": "Adam's mom — honoring family and welcoming a new daughter.",
    },
    {
        "slug": "tomas",
        "name": "Tomas",
        "title": "Bannerlord of the Vows",
        "role": "Father of the Groom",
        "frame": "white",
        "cost": "Call Time 10:00 AM",
        "rehearsal": [
            ("Ceremony Rehearsal (4:00–5:00 PM)", ["Join the full family walkthrough and practice the candle-lighting ceremony with Radka."]),
            ("Rehearsal Dinner (6:00–8:00 PM)", ["Host the rehearsal dinner with Radka at Leonard's Palazzo."]),
        ],
        "rehearsal_reminder": "Confirm the rehearsal dinner plan and keep comfortable shoes handy for the walkthrough.",
        "duties": [
            ("Morning", ["Join the groomsmen photos at the hotel at 10:00 AM."]),
            ("1:00 PM", ["Ride the first-wave limo bus from the hotel to the church."]),
            ("Ceremony (2:00 PM)", ["During the processional: walk Radka into the church.",
                                    "~2:05 PM: take part in the candle-lighting with Karin and Peter."]),
            ("Reception", ["After the ~3:00 PM receiving line and before the 3:30 PM bus: join formal photos at Francis Lewis Park; confirm exact start/end with the photographer.",
                           "~5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "7:30–7:45 PM Grand Entrance, group 2 of 8: walk in with Radka immediately after Peter and Karin.",
                           "~7:50 PM, immediately after the first parent dance (Brittany with Peter): join Radka for the second parent dance (mother–son dance).",
                           "9:00–10:15 PM Formal Speeches segment, after the second course and before entrées: deliver the groom's parents' speech with Radka, after Gustavo's Best Man speech; exact minute is not specified."]),
        ],
        "reminder": "Be ready for the 10:00 AM photos and board the first-wave bus by 1:00 PM.",
        "flavor": "Adam's dad — leading the way for the groom's family.",
    },
]

CARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{name} — {title} ({day_label})</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="card frame-{frame}">
  <div class="card-inner">
    <div class="day-banner">{day_banner}</div>
    <div class="title-bar">
      <span class="name">{name}</span>
      <span class="cost">{cost}</span>
    </div>
    <div class="art-box">
      <img src="{portrait}" alt="{name} as {title}">
    </div>
    <div class="type-line">
      <span>Legendary Hero — {title}</span>
      <span>{role}</span>
    </div>
    <div class="text-box">
      {duties_html}
      <div class="reminder">⚠️ {reminder}</div>
      <div class="flavor">“{flavor}”</div>
    </div>
    <div class="bottom-row">
      <span class="collector">Brittany &amp; Adam • 11.6–11.7.2026</span>
      <span class="pt-box">{role}<br>{day_label}</span>
    </div>
  </div>
</div>
<div class="back-link">
  <a href="{other_day_file}">{other_day_link_text}</a> &nbsp;•&nbsp;
  <a href="index.html">&larr; Back to the full party</a>
</div>
</body>
</html>
"""


def render_duties(duties):
    parts = []
    for heading, items in duties:
        parts.append(f"<h4>{heading}</h4>")
        parts.append("<ul>")
        for item in items:
            parts.append(f"<li>{item}</li>")
        parts.append("</ul>")
    return "\n      ".join(parts)


def write_card(person, day_number, day_label, day_banner, duties, reminder, cost, other_day_file, other_day_link_text):
    portrait = person.get("portrait", f"{PORTRAIT_DIR_REL}/{person['slug']}_dnd.png")
    html = CARD_TEMPLATE.format(
        name=person["name"],
        title=person["title"],
        cost=cost,
        portrait=portrait,
        role=person["role"],
        duties_html=render_duties(duties),
        reminder=reminder,
        flavor=person["flavor"],
        frame=person["frame"],
        day_label=day_label,
        day_banner=day_banner,
        other_day_file=other_day_file,
        other_day_link_text=other_day_link_text,
    )
    out_path = os.path.join(OUTPUT_DIR, f"{person['slug']}_day{day_number}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Wrote {out_path}")


# ============================================================================
# Master Timetable "Battle Plan" card — one giant scroll with every event,
# every order, every transportation leg, and every must-bring item for the
# whole wedding weekend. Mirrors MASTER_TIMETABLE.md, rendered in the same
# MTG-card visual style as the per-person cards.
# ============================================================================

MASTER_SCROLL_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Master Battle Plan — Brittany &amp; Adam's Wedding Weekend</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="scroll frame-gold">
  <div class="scroll-inner">
    <div class="scroll-title">
      <h1>📜 The Master Battle Plan 📜</h1>
      <div class="sub">Brittany &amp; Adam • Fri, Nov 6 – Sat, Nov 7, 2026 • Great Neck / College Point / Flushing, NY</div>
    </div>
    <div class="scroll-nav">
      <a href="#urgent">⚠️ Urgent</a>
      <a href="#logistics">🏨 Pre-Wedding Logistics</a>
      <a href="#prep">📦 Week-Before &amp; Thursday Prep</a>
      <a href="#friday">🎭 Friday Rehearsal</a>
      <a href="#saturday">📅 Saturday Timeline</a>
      <a href="#processional">⛪ Processional Order</a>
      <a href="#entrance">💃 Grand Entrance Order</a>
      <a href="#transport">🚌 Transportation</a>
      <a href="#items">🎒 Must-Bring Items</a>
      <a href="#catering">🍽️ Catering</a>
      <a href="#vendors">🧾 Vendors</a>
    </div>

    <section id="urgent">
      <h2>⚠️ Urgent / Needs Attention</h2>
      {urgent_table}
    </section>

    <section id="logistics">
      <h2>🏨 Pre-Wedding Logistics</h2>
      {logistics_list}
    </section>

    <section id="prep">
      <h2>📦 Week-Before &amp; Thursday Prep</h2>
      {prep_list}
    </section>

    <section id="friday">
      <h2>🎭 Friday, November 6 — Rehearsal Day</h2>
      {friday_table}
      <div class="callout">{friday_notes}</div>
    </section>

    <section id="saturday">
      <h2>📅 Saturday, November 7 — Full Day Timeline</h2>
      {saturday_table}
      <div class="callout"><strong>Action-item standard:</strong> Each action is shown separately in chronological order with a time or clear sequence cue. Every processional and grand-entrance entry states who walks together and who enters immediately before them. If an exact minute is not confirmed, follow the documented time window or cue rather than assuming a time.</div>
    </section>

    <div class="two-col">
      <section id="processional">
        <h2>⛪ Ceremony Processional Order</h2>
        {processional_list}
      </section>

      <section id="entrance">
        <h2>💃 Grand Entrance Order</h2>
        {entrance_list}
      </section>
    </div>

    <section id="transport">
      <h2>🚌 Transportation Plan</h2>
      {transport_table}
      <div class="callout">{transport_notes}</div>
    </section>

    <section id="items">
      <h2>🎒 What Everyone Must Remember to Bring</h2>
      {items_table}
    </section>

    <section id="catering">
      <h2>🍽️ Catering Snapshot (Leonard's Palazzo — Event #E23526)</h2>
      {catering_list}
    </section>

    <section id="vendors">
      <h2>🧾 Vendor Directory</h2>
      {vendor_grid}
    </section>

    <div class="bottom-row">
      <span class="collector">Brittany &amp; Adam • 11.6–11.7.2026</span>
      <span class="pt-box">Master Battle Plan<br>All Hands on Deck</span>
    </div>
  </div>
</div>
<div class="back-link">
  <a href="index.html">&larr; Back to the full party</a>
</div>
</body>
</html>
"""


def render_table(headers, rows, time_col=0):
    parts = ["<table>", "<tr>"]
    for h in headers:
        parts.append(f"<th>{h}</th>")
    parts.append("</tr>")
    for row in rows:
        parts.append("<tr>")
        for i, cell in enumerate(row):
            cls = ' class="time-col"' if i == time_col else ""
            parts.append(f"<td{cls}>{cell}</td>")
        parts.append("</tr>")
    parts.append("</table>")
    return "\n      ".join(parts)


def render_ordered_list(items):
    parts = ["<ol>"]
    for item in items:
        parts.append(f"<li>{item}</li>")
    parts.append("</ol>")
    return "\n        ".join(parts)


def render_plain_list(items):
    parts = ['<ul class="plain">']
    for item in items:
        parts.append(f"<li>{item}</li>")
    parts.append("</ul>")
    return "\n      ".join(parts)


def render_vendor_grid(vendors):
    parts = ['<div class="vendor-grid">']
    for role, name, contact in vendors:
        parts.append(
            f'<div class="vendor-card"><strong>{role}</strong>{name}<br>{contact}</div>'
        )
    parts.append("</div>")
    return "\n      ".join(parts)


URGENT_ITEMS = [
    ("1", "Hotel room-block cutoff already passed.",
     "The Inn at Great Neck reservation cutoff was 10/7/2026. Call (516) 773-2000 today to confirm the block was extended and lock in the $409/night rate under code Q56RG6D1."),
    ("2", "✅ Resolved — return transportation.",
     "Camelot Limo Bus (Reservation #109521, driver Bill Townsend) extended to run a 12:30 AM return trip, Leonard's Palazzo → Inn at Great Neck."),
    ("3", "✅ Resolved — \"parents' toast\" isn't a duplicate.",
     "The pre-dinner welcome toast is a brief 1–2 minute greeting; the full parents' speech happens later in the formal Speeches segment."),
    ("4", "Kids' meals need to be pre-ordered.",
     "Request kids' meals and an earlier kids' food time from Leonard's Palazzo for Meda, Sofia, Madison, and Emeric — adult entrées aren't served until 10:15 PM."),
    ("5", "Rings are heirlooms carried by the toddler-aged ring bearer.",
     "Use decoy rings on Emeric's pillow; Gustavo (Best Man) privately holds the real rings until the exchange."),
    ("6", "✅ Resolved — rehearsal plan + venue.",
     "Full rehearsal-day plan set below; rehearsal dinner booked in Leonard's Palazzo's private dining room, Friday evening."),
]

LOGISTICS_ITEMS = [
    "<strong>Hotel block:</strong> Inn at Great Neck, 30 Cutter Mill Rd, Great Neck, NY 11021 — (516) 773-2000. Group code <code>Q56RG6D1</code>, rate $409/night (+$25 extra adult/night, +$25 rollaway, cribs free).",
    "<strong>Check-in:</strong> Friday, Nov 6 (after 3:00 PM, photo ID required) · <strong>Check-out:</strong> Sunday, Nov 8 (by 12:00 PM, luggage storage available).",
    "~15 minute walk / ~5 minute drive to Leonard's Palazzo.",
    "<strong>Dress code:</strong> Formal — gentlemen in black tuxedo or suit; ladies in a long or cocktail dress, any color except white.",
]

PREP_ITEMS = [
    "<strong>Week before:</strong> Adam acquires and brings the decorated wagon Emeric will use to pull Madison down the aisle.",
    "<strong>Week before:</strong> Karin packs a crate for Leonard's Palazzo with the welcome-table and memorial-table items, plus the wine-box favors, and drops it off ahead of time.",
    "<strong>Week before:</strong> Radka brings an item in memory of her late brother Dominik for the memorial table.",
    "<strong>Thursday, Nov 5:</strong> Adam, Gustavo, Chris, Erik, and Max all pick up their tuxes from Men's Wearhouse.",
]

FRIDAY_ROWS = [
    ("2:00 PM", "Adam &amp; Brittany set up decorations at the church ahead of the rehearsal.", "Adam, Brittany", "St John's Lutheran Church"),
    ("After 3:00 PM", "Hotel check-in opens (photo ID required). Bara + Meda (traveling from the Czech Republic) should build in buffer time for jet lag.", "Everyone staying at the hotel", "Inn at Great Neck"),
    ("4:00–5:00 PM", "Ceremony rehearsal — full walkthrough of the processional order, altar positions, vow cues, ring exchange, candle-lighting, and recessional, led by the officiant.", "Adam, Brittany, full wedding party, both sets of parents, Omi, Eric &amp; April Demery (practices his reading), officiant", "St John's Lutheran Church"),
    ("4:05 PM", "Adam &amp; Brittany step aside to privately practice their vows.", "Adam, Brittany", "St John's Lutheran Church"),
    ("6:00–6:30 PM", "Travel from church to rehearsal dinner.", "Rehearsal attendees", "Church → Leonard's Palazzo"),
    ("6:00–8:00 PM", "Rehearsal dinner, hosted by the groom's parents (Tomas &amp; Radka).", "Wedding party + immediate family, plus Uncle Danny, Omi, Eric &amp; April Demery", "Leonard's Palazzo — private dining room"),
    ("8:00 PM", "Return to hotel.", "Adam, Brittany, Gustavo, Meda, Tomas, Radka", "Leonard's Palazzo → Inn at Great Neck"),
    ("By 9:30 PM", "Early night for the rest of the kids (Sofia, Madison, Emeric) and jet-lagged travelers; everyone else returns to the hotel at their own pace after dinner winds down.", "Flower girls, ring bearer, international travelers", "Inn at Great Neck"),
]

FRIDAY_NOTES = (
    "<strong>Bring to rehearsal:</strong> comfortable shoes, the officiant's contact info, a printed copy of the "
    "reading for Eric Demery to practice with, and the ring pillow (practice run only)."
)

SATURDAY_ROWS = [
    ("7:00 AM", "Chris picks Autumn up at the hotel and drives her to her hair appointment.", "Autumn, Chris", "Inn at Great Neck → Lush Hair Studio"),
    ("8:30 AM", "Hair salon appointment (Karin drives herself, Brittany, and Omi; Autumn arrives separately with Chris).", "Brittany, Autumn, Karin, Omi", "Lush Hair Studio, 185 Northern Blvd, Great Neck"),
    ("9:30 AM", "Adam receives the florist's bouquet delivery at the hotel.", "Adam", "Inn at Great Neck"),
    ("9:30–10:30 AM", "peter teaches his regular Saturday class (his day job) one last time, finishing in plenty of time before the 1:15 PM ride to the church.", "peter", "Off-site"),
    ("After the 9:30 AM delivery", "Adam routes Brittany's bouquet to her room without seeing her, preserving the first-look surprise.", "Adam", "Inn at Great Neck"),
    ("10:00 AM", "Groomsmen take photos at the hotel.", "Adam, Gustavo, Chris, Erik, Max, Tomas", "Inn at Great Neck"),
    ("10:00 AM", "Marie, Dalia, Julia, and Julie arrive at the hotel for pictures.", "Marie, Dalia, Julia, Julie", "Inn at Great Neck"),
    ("~10:30 AM", "Chris drives Autumn back to the hotel in time for the 12:00 PM bridesmaid pictures.", "Autumn, Chris", "Lush Hair Studio → Inn at Great Neck"),
    ("12:00 PM", "Pictures of the Bridesmaids group — Brittany brings the wedding bands and wedding invitation as photo props.", "Brittany, Marie, Dalia, Julia, Julie, Bara, Autumn, Meda, Sofia, Madison, Radka, Omi", "Inn at Great Neck"),
    ("1:00 PM", "Camelot Limo Bus departs hotel for the church — first wave (groomsmen + Tomas).", "Gustavo, Chris, Erik, Max, Tomas", "Inn at Great Neck → Church"),
    ("1:15 PM", "Eric &amp; April Demery depart by car directly to the church with Emeric.", "Eric Demery, April Demery, Emeric", "Hotel → Church"),
    ("1:15 PM", "Adam + peter depart together in peter's personal car, directly to the church.", "Adam, peter", "Hotel → Church"),
    ("1:15 PM", "Camelot Limo Bus departs hotel for the church — second/main wave (bridal party).", "Brittany, Marie, Dalia, Julia, Julie, Bara, Autumn, Meda, Sofia, Madison, Karin, Radka, Omi", "Inn at Great Neck → Church"),
    ("1:45 PM", "Arrive at church.", "Everyone", "St John's Lutheran Church"),
    ("2:00 PM", "Ceremony begins (ceremony only, no mass).", "Everyone", "St John's Lutheran Church, 2201 123rd St, College Point"),
    ("2:00 PM", "Processional / entrances to altar — see Processional Order.", "See order below", "Church"),
    ("2:05 PM", "Adam &amp; Brittany say their vows.", "Adam, Brittany", "Church"),
    ("2:05 PM", "peter, Karin, Tomas, and Radka begin the candle-lighting ceremony during the vows.", "peter, Karin, Tomas, Radka", "Church"),
    ("2:10 PM", "Adam &amp; Brittany light the unity candle together.", "Adam, Brittany", "Church"),
    ("2:10 PM", "Karin steps out to check the reception arrangements using the crate she dropped off the week before.", "Karin", "Leonard's Palazzo"),
    ("2:50 PM", "Karin hands bubbles to all guests.", "Karin → everyone", "Church exterior"),
    ("2:55 PM", "Recessional: everyone except Adam &amp; Brittany exits the church.", "Everyone except Adam &amp; Brittany", "Church"),
    ("After the rest of the party exits", "Everyone else forms the bubble-send-off line outside.", "Everyone except Adam &amp; Brittany", "Church exterior"),
    ("2:55 PM", "Adam &amp; Brittany exit last through the bubble line.", "Adam, Brittany", "Church exterior"),
    ("~3:00 PM", "Ceremony ends (approximately one-hour runtime per contract).", "—", "Church"),
    ("After ceremony ends (~3:00 PM)", "Receiving line outside the church.", "Everyone", "Church steps"),
    ("After the ~3:00 PM receiving line and before photos", "Bridal party and immediate family travel to Francis Lewis Park.", "Bridal party, immediate family", "Church → Francis Lewis Park"),
    ("After arrival at Francis Lewis Park and before the 3:30 PM bus", "Formal photos; finish in time for the scheduled bus departure. Exact photo start/end to be confirmed with the photographer.", "Bridal party, immediate family", "Francis Lewis Park, Flushing"),
    ("3:30 PM", "Party bus departs for Leonard's Palazzo after the formal photos; confirm the exact pickup point with Camelot.", "Bridal party + both sets of parents + Omi", "Photo location → Leonard's Palazzo"),
    ("4:00 PM", "Limo bus drop-off at the reception venue.", "Bridal party", "Leonard's Palazzo, 555 Northern Blvd"),
    ("4:30 PM", "Bridal suite becomes available for the wedding party.", "Bridal party", "Leonard's Palazzo"),
    ("4:30–6:30 PM", "Suite Set — appetizers &amp; beverage service.", "Host party", "Private suite, Leonard's Palazzo"),
    ("5:30 PM", "Pictures in front of Leonard's Palazzo.", "Everyone (bridal party, Emeric, both sets of parents, Omi)", "Leonard's Palazzo exterior"),
    ("6:30 PM", "Private cocktail hour begins in the bridal suite for the wedding party.", "Bridal party", "Private suite, Leonard's Palazzo"),
    ("6:30 PM", "General Cocktail Hour begins for the guests (invitation time).", "Guests; Madison, Emeric, peter, Karin, Tomas, Radka, Omi", "Leonard's Palazzo"),
    ("7:00 PM", "Formal room/portrait shots.", "Bridal party", "Leonard's Palazzo"),
    ("7:30 PM", "Reception begins.", "Everyone", "Reception room"),
    ("7:30–7:45 PM", "Grand Entrance — see Grand Entrance Order.", "Everyone", "Reception room"),
    ("7:45 PM", "First Dance — Adam + Brittany, \"Dancing on Clouds\" (fog effect).", "Adam, Brittany", "Dance floor"),
    ("7:48 PM", "MC/DJ invites other couples to the floor.", "Everyone", "Dance floor"),
    ("~7:50 PM", "First parent dance: Brittany dances with peter (father–daughter).", "Brittany, peter", "Dance floor"),
    ("Immediately after the first parent dance (~7:50 PM)", "Second parent dance: Adam dances with Radka (mother–son). [Suggested] Run the dances one at a time so each is spotlighted.", "Adam, Radka", "Dance floor"),
    ("After the parent dances (~7:50 PM)", "Open dancing resumes between scheduled reception events; follow the MC/DJ's cues.", "Everyone", "Dance floor"),
    ("~7:55 PM", "Brief welcome toast before the first course.", "peter &amp; Karin", "Reception room"),
    ("~7:55 PM", "Blessing before the first course; exact order relative to the welcome toast is not specified.", "Uncle Danny", "Reception room"),
    ("8:00 PM", "First Course — Penne alla Vodka.", "Everyone, incl. pre-ordered kids' meals", "Reception room"),
    ("8:45–9:00 PM", "Second Course / Salad — Agrigento salad.", "Everyone", "Reception room"),
    ("9:00–10:15 PM, in listed sequence; individual start times unspecified", "Brittany's parents' speech.", "peter &amp; Karin", "Reception room"),
    ("After Brittany's parents' speech within the 9:00–10:15 PM speeches block", "Maid of Honor speech.", "Marie", "Reception room"),
    ("After Marie's speech within the 9:00–10:15 PM speeches block", "Best Man speech.", "Gustavo", "Reception room"),
    ("After Gustavo's speech within the 9:00–10:15 PM speeches block", "Groom's parents' speech.", "Tomas &amp; Radka", "Reception room"),
    ("10:15 PM", "Entrées — Salmon, Filet Mignon, Herb Roasted Chicken, or Melanzana Pomodoro.", "Everyone", "Reception room"),
    ("10:45 PM", "Cake Cutting.", "Adam, Brittany", "Reception room"),
    ("~11:00 PM, after cake cutting", "Bouquet toss.", "Brittany", "Dance floor"),
    ("After bouquet toss, during ~11:00 PM block", "Garter toss.", "Adam", "Dance floor"),
    ("After garter toss, during ~11:00 PM block", "Anniversary dance; DJ calls up couples and eliminates by years married until the longest-married couple remains.", "Couples", "Dance floor"),
    ("After anniversary dance, before 11:30 PM dessert hour", "Last dance.", "Everyone", "Dance floor"),
    ("11:30 PM–12:30 AM", "La Dolce Tavola dessert hour.", "Everyone", "Reception room"),
    ("12:30 AM", "Reception ends — no items may be left at the venue.", "Everyone", "Leonard's Palazzo"),
    ("12:30 AM+", "Return transportation — Camelot Limo Bus extended run.", "Everyone", "Venue → Hotel"),
]

PROCESSIONAL_ORDER = [
    "2:00 PM processional, first: Adam enters alone and takes his position at the altar.",
    "Next: Gustavo (Best Man) enters alone, immediately after Adam, and takes his position beside him.",
    "Next: Tomas walks in with Radka (groom's parents), immediately after Gustavo.",
    "Next: Max escorts Dalia down the aisle, immediately after Tomas and Radka.",
    "Next: Julia and Julie walk in together, arm-in-arm, immediately after Max and Dalia.",
    "Next: Bara and Autumn walk in together, arm-in-arm, immediately after Julia and Julie.",
    "Next: Marie (Maid of Honor) walks in alone, immediately after Bara and Autumn, and takes her position at the altar.",
    "Next: Erik and Chris escort Omi (grandmother of the bride) to her front-row seat, immediately after Marie.",
    "After Omi is seated: Erik and Chris take their positions at the altar.",
    "Next: Meda and Sofia (flower girls) walk in together, immediately after Erik and Chris take their positions.",
    "As they walk: Meda and Sofia scatter petals.",
    "Next: Emeric pulls Madison down the aisle in a decorated wagon, immediately after Meda and Sofia.",
    "Next: Brittany walks in with peter, immediately after Emeric and Madison.",
    "At the altar: Brittany hands her bouquet to Marie.",
    "After the processional: Eric Demery delivers the prayer/reading.",
    "2:05 PM: Adam and Brittany say their vows.",
    "During the vows at 2:05 PM: peter, Karin, Tomas, and Radka begin the candle-lighting ceremony.",
    "After the vows: Emeric brings forward the rings.",
    "Next: Adam and Brittany exchange rings.",
    "2:10 PM: Adam and Brittany light the unity candle together.",
    "At 2:10 PM: Karin steps out to check the reception arrangements at Leonard's Palazzo.",
    "2:50 PM: Karin distributes bubbles to the guests outside the church.",
    "At the ~2:55 PM recessional: everyone except Adam and Brittany exits the church.",
    "After the rest of the party exits: they form the bubble-send-off line outside.",
    "Next: Adam and Brittany exit last through the bubble line.",
    "After the ~3:00 PM receiving line: the bridal party and immediate family travel from the church to Francis Lewis Park.",
    "After arrival at Francis Lewis Park and before the 3:30 PM bus departure: complete formal photos; confirm the exact photo window with Lawrence Photography.",
    "At 3:30 PM: the party bus departs from the pickup point confirmed with Camelot for Leonard's Palazzo.",
]

GRAND_ENTRANCE_ORDER = [
    "7:30–7:45 PM, group 1 of 8: peter walks in with Karin (bride's parents); first entrance group.",
    "7:30–7:45 PM, group 2 of 8: Tomas walks in with Radka (groom's parents), immediately after peter and Karin.",
    "7:30–7:45 PM, group 3 of 8: Emeric, Meda, Sofia, and Madison walk in together, immediately after Tomas and Radka.",
    "7:30–7:45 PM, group 4 of 8: Marie walks in with Gustavo (Maid of Honor and Best Man), immediately after the children.",
    "7:30–7:45 PM, group 5 of 8: Chris, Autumn, and Bara walk in together as a trio, immediately after Marie and Gustavo.",
    "7:30–7:45 PM, group 6 of 8: Erik walks in with Julia, immediately after Chris, Autumn, and Bara.",
    "7:30–7:45 PM, group 7 of 8: Max walks in with Julie and Dalia as a trio, immediately after Erik and Julia.",
    "7:30–7:45 PM, group 8 of 8: <strong>Adam walks in with Brittany</strong> as the grand finale, immediately after Max, Julie, and Dalia; the wedding party forms an arch.",
]

TRANSPORT_ROWS = [
    ("Morning (pre-bus)", "Chris's personal car", "7:00 AM, Inn at Great Neck", "Lush Hair Studio (8:30 AM appt)", "~10:30 AM, Inn at Great Neck", "Autumn + Chris — round trip for Autumn's hair appointment, back in time for the 12:00 PM bridesmaid pictures"),
    ("Morning (pre-bus)", "Karin's personal car", "~8:00 AM, Inn at Great Neck", "Lush Hair Studio (8:30 AM appt)", "~10:30 AM, Inn at Great Neck", "Karin drives herself, Brittany, and Omi to the same hair appointment"),
    ("Day-of (pre-ceremony → reception), first wave", "Camelot Specialty Limo — 26-pax Bus, Bill Townsend (646) 498-4454, Res. #109521", "1:00 PM, Inn at Great Neck", "Church (2:00 PM)", "Church", "Gustavo, Chris, Erik, Max, Tomas"),
    ("Day-of (pre-ceremony → reception), second wave", "Camelot Specialty Limo — same bus, same reservation", "1:15 PM, Inn at Great Neck", "Church (2:00 PM) → Francis Lewis Park", "4:00 PM, Leonard's Palazzo", "Brittany, Marie, Dalia, Julia, Julie, Bara, Autumn, Meda, Sofia, Madison, Karin, Radka, Omi"),
    ("Day-of (pre-ceremony, separate)", "peter's personal car", "1:15 PM, Hotel", "Church (peter parks the car)", "Church", "Adam + peter"),
    ("After the ~3:00 PM receiving line", "Camelot Specialty Limo — same bus", "St John's Lutheran Church", "Francis Lewis Park (formal photos)", "Francis Lewis Park", "peter boards the bus at the church"),
    ("3:30 PM", "Camelot Specialty Limo — same bus", "Francis Lewis Park", "Leonard's Palazzo", "4:00 PM, Leonard's Palazzo", "peter rides with the bridal party, both sets of parents, and Omi"),
    ("After the reception", "peter's personal car", "St John's Lutheran Church", "—", "—", "Retrieve the car; responsible person and pickup time to be confirmed"),
    ("Day-of (direct to church)", "Eric &amp; April Demery's personal car", "Hotel", "—", "Church", "Eric Demery, April Demery, Emeric — depart by 1:15 PM"),
    ("Post-reception", "Camelot Limo Bus — extended 12:30 AM return run", "Leonard's Palazzo", "—", "Inn at Great Neck", "Everyone"),
]

TRANSPORT_NOTES = [
    "<strong>1:00 PM:</strong> The first bus wave departs the Inn at Great Neck with the groomsmen and Tomas.",
    "<strong>1:15 PM:</strong> The main bridal-party bus wave departs the Inn at Great Neck for the church.",
    "Madison rides the Camelot bus with her mom Brittany.",
    "Emeric's wagon travels in the bus's luggage bay.",
]

MUST_BRING_ROWS = [
    ("Adam (Groom)", "Marriage license, vows, wedding band, peter's ride confirmed, tux picked up Thursday", "Needed to legally marry"),
    ("Brittany (Bride)", "Marriage license, vows, bouquet, something old/new/borrowed/blue, wedding bands + wedding invitation (as photo props for the 12:00 PM bridesmaid pictures)", "Bouquet is handed to Marie mid-ceremony"),
    ("Marie (Maid of Honor)", "Tissues/emergency kit, MOH speech notes", "Receives the bouquet, gives a toast later"),
    ("Gustavo (Best Man)", "The real wedding rings (decoy-ring plan), Best Man speech notes, tux picked up Thursday", "Rings must reach the altar"),
    ("Dalia / Julia / Julie / Bara / Autumn (Bridesmaids)", "Dresses/shoes (any color but white), flats for dancing. Autumn: 8:30 AM Lush Hair Studio appointment confirmed (with Brittany, Karin, Omi), back at hotel by ~10:30 AM.", "Comfort for the long day"),
    ("Chris / Erik / Max (Groomsmen)", "Black tux/suit (picked up Thursday), boutonnieres. Chris: drives Autumn to/from her 8:30 AM hair appointment (depart 7:00 AM, back ~10:30 AM).", "Dress code compliance"),
    ("Meda &amp; Sofia (Flower Girls)", "Flower petals/basket", "Provided as part of the OG Floral order"),
    ("Emeric (Ring Bearer)", "Ring pillow (decoy rings recommended), comfort item, the decorated wagon (acquired by Adam the week before)", "Rings are the centerpiece of the ceremony"),
    ("Madison (Flower Girl role)", "Wagon (pulled by Emeric), snacks, comfort item/blanket", "She rides in rather than walks"),
    ("Karin (Mother of the Bride)", "Bubbles for ~100 guests, welcome speech notes, the crate of welcome-table/memorial-table items + wine-box favors (dropped off the week before)", "Distributes bubbles before the recessional; arranges the venue right after the candle ceremony"),
    ("peter (Father of the Bride)", "His car (for driving Adam), welcome speech notes", "Teaches his regular Saturday class 9:30–10:30 AM, then chauffeur + ceremony role + speech"),
    ("Tomas &amp; Radka (Groom's Parents)", "Candle-lighting reminder, speech notes. Radka also brings an item in memory of her late brother Dominik for the memorial table.", "Scheduled twice — ceremony + reception"),
    ("Omi (Grandmother of the Bride)", "Comfortable shoes for the aisle escort", "Walked in by Erik + Chris; also joins the 8:30 AM hair salon trip"),
    ("Eric &amp; April Demery (Emeric's parents)", "Eric: prayer/reading notes; both: supervise Emeric", "Eric reads right after the bouquet hand-off"),
    ("Uncle Danny", "Prayer/blessing notes", "Drives himself directly to Leonard's Palazzo by 6:30 PM"),
    ("Host / Family", "Money box, guest book, welcome banner, signature-drink sign, cake topper, place cards, wine-box favors, memorial table items", "No items may be left at Leonard's Palazzo after 12:30 AM"),
]

CATERING_ITEMS = [
    "<strong>Cocktail Hour (6:30–7:30 PM):</strong> Caprese, grilled vegetables, fruit display, seafood salad, charcuterie, hot displays (shrimp, arancini, calamari), carving station (grilled flank steak), pasta stations.",
    "<strong>First Course (8:00 PM):</strong> Penne alla Vodka.",
    "<strong>Second Course (8:45–9:00 PM):</strong> Agrigento salad.",
    "<strong>Entrées (10:15 PM):</strong> Salmon, Filet Mignon, Herb Roasted Chicken, or Melanzana Pomodoro — kids' meals pre-ordered for Meda, Sofia, Madison, and Emeric.",
    "<strong>Dessert:</strong> 4-tier buttercream wedding cake + La Dolce Tavola dessert hour (11:30 PM–12:30 AM) — pastries, chocolate fountain, cannoli, sundae bar, cheesecake medley, waffles, zeppoles, cordial bar, coffee/tea.",
    "<strong>Bar:</strong> Premium open bar, champagne toast included. Signature drink: <strong>\"Cloud Nine\"</strong> — vodka, elderflower liqueur, and prosecco over a butterfly-pea-flower ice cube that shifts the drink from blue to pink, echoing the \"Dancing on Clouds\" first-dance theme.",
]

VENDORS = [
    ("Venue", "Leonard's Palazzo", "(516) 487-7900"),
    ("Photographer/Video", "Lawrence Photography", "(718) 631-1021"),
    ("Florist/Decorator", "OG Floral (Laurie Cress)", "(718) 746-4846"),
    ("DJ / Photobooth / Cloud Effect", "Epic Entertainment (Gudah)", "—"),
    ("Transportation", "Camelot Specialty Limo", "(516) 731-LIMO"),
    ("Hotel", "Inn at Great Neck", "(516) 773-2000"),
]


def write_master_card():
    urgent_table = render_table(
        ["#", "Issue", "Why it matters"],
        [(n, title, why) for n, title, why in URGENT_ITEMS],
        time_col=None,
    )
    html = MASTER_SCROLL_TEMPLATE.format(
        urgent_table=urgent_table,
        logistics_list=render_plain_list(LOGISTICS_ITEMS),
        prep_list=render_plain_list(PREP_ITEMS),
        friday_table=render_table(["Time", "Event", "Who", "Location"], FRIDAY_ROWS, time_col=0),
        friday_notes=FRIDAY_NOTES,
        saturday_table=render_table(["Time", "Event", "Who", "Location"], SATURDAY_ROWS, time_col=0),
        processional_list=render_ordered_list(PROCESSIONAL_ORDER),
        entrance_list=render_ordered_list(GRAND_ENTRANCE_ORDER),
        transport_table=render_table(
            ["Leg", "Vehicle", "Pick-up", "Stops", "Drop-off", "Who"], TRANSPORT_ROWS, time_col=None
        ),
        transport_notes=render_plain_list(TRANSPORT_NOTES),
        items_table=render_table(["Person / Role", "Must-have item(s)", "Why"], MUST_BRING_ROWS, time_col=None),
        catering_list=render_plain_list(CATERING_ITEMS),
        vendor_grid=render_vendor_grid(VENDORS),
    )
    out_path = os.path.join(OUTPUT_DIR, "master_timetable.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Wrote {out_path}")


def write_print_packet():
    def page_content(filename):
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, encoding="utf-8") as f:
            html = f.read()
        return html.split("<body>", 1)[1].split('<div class="back-link">', 1)[0].strip()

    sections = [page_content("master_timetable.html")]
    for person in PEOPLE:
        for day in (1, 2):
            filename = f"{person['slug']}_day{day}.html"
            sections.append(
                f'<section class="packet-card" aria-label="{person["name"]} — Day {day}">'
                f'{page_content(filename)}</section>'
            )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wedding Print Packet — Brittany &amp; Adam</title>
<link rel="stylesheet" href="style.css">
<style>
body.print-packet {{
  display: block;
  padding: 40px 20px;
}}
.packet-controls {{
  max-width: 1100px;
  margin: 0 auto 24px;
  text-align: center;
  font-family: 'Cinzel', serif;
}}
.packet-controls p {{
  color: #cbbfa0;
}}
.packet-controls button {{
  padding: 10px 20px;
  border: 1px solid #d4af37;
  border-radius: 8px;
  background: #6b4a14;
  color: #fffaf0;
  font: inherit;
  cursor: pointer;
}}
.packet-card {{
  margin: 32px auto;
}}
@media print {{
  body.print-packet {{
    display: block;
    margin: 0;
    padding: 0;
    background: #fff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .packet-controls {{ display: none; }}
  .packet-card {{
    margin: 0;
    break-before: page;
    page-break-before: always;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
}}
</style>
</head>
<body class="print-packet">
<header class="packet-controls">
  <h1>Wedding Print Packet</h1>
  <p>Master Battle Plan followed by every Friday rehearsal and Saturday wedding-day card.</p>
  <button type="button" onclick="window.print()">Print all wedding documents</button>
</header>
{''.join(sections)}
</body>
</html>
"""
    out_path = os.path.join(OUTPUT_DIR, "print_all.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Wrote {out_path}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    write_master_card()

    index_items = []
    for person in PEOPLE:
        # Day 1 — Friday rehearsal card
        write_card(
            person,
            day_number=1,
            day_label="Fri, Nov 6 — Rehearsal",
            day_banner="📜 Day 1 of 2 — Rehearsal",
            duties=person["rehearsal"],
            reminder=person["rehearsal_reminder"],
            cost="Rehearsal Day",
            other_day_file=f"{person['slug']}_day2.html",
            other_day_link_text="Day 2: Wedding Day →",
        )
        # Day 2 — Saturday wedding day card
        write_card(
            person,
            day_number=2,
            day_label="Sat, Nov 7 — Wedding Day",
            day_banner="💍 Day 2 of 2 — Wedding Day",
            duties=person["duties"],
            reminder=person["reminder"],
            cost=person["cost"],
            other_day_file=f"{person['slug']}_day1.html",
            other_day_link_text="← Day 1: Rehearsal",
        )
        index_items.append(person)

    # Build a gallery index.html
    tiles = []
    for person in index_items:
        portrait = person.get("portrait", f"{PORTRAIT_DIR_REL}/{person['slug']}_dnd.png")
        tiles.append(f"""
        <div class="tile">
          <a href="{person['slug']}_day2.html">
            <img src="{portrait}" alt="{person['name']}">
          </a>
          <div class="tile-caption">
            <strong>{person['name']}</strong><br>
            <span>{person['title']}</span>
          </div>
          <div class="tile-links">
            <a href="{person['slug']}_day1.html">Day 1: Rehearsal</a>
            <a href="{person['slug']}_day2.html">Day 2: Wedding Day</a>
          </div>
        </div>""")

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Brittany &amp; Adam's Wedding Party — Hero Roster</title>
<link rel="stylesheet" href="gallery.css">
</head>
<body>
<h1>⚔️ The Wedding Party — Hero Roster ⚔️</h1>
<p class="sub">Each hero has two cards: a Friday rehearsal card and a Saturday wedding-day card. Tap a portrait or a day link below it.</p>
<div class="grid">
  <div class="tile" style="grid-column: 1 / -1;">
    <a href="master_timetable.html">
      <div style="height:120px; display:flex; align-items:center; justify-content:center; background:radial-gradient(circle, #6b4a14, #15110f); font-size:48px;">📜</div>
    </a>
    <div class="tile-caption">
      <strong>The Master Battle Plan</strong><br>
      <span>Every event, every order, every item — the full weekend</span>
    </div>
    <div class="tile-links">
      <a href="master_timetable.html">Open the full timetable →</a>
      <a href="print_all.html">Print all documents →</a>
    </div>
  </div>
  {''.join(tiles)}
</div>
</body>
</html>
"""
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"✅ Wrote {os.path.join(OUTPUT_DIR, 'index.html')}")
    write_print_packet()


if __name__ == "__main__":
    main()
