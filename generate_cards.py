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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
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
                "Enter alone after Max, Julie, and Dalia, immediately before the flower girls.",
                "When Brittany walks in with Peter, she will hand you her bouquet. "
                "Hold it safely for the entire ceremony.",
                "Exit the church with Brittany, holding her dress.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party (apps + drinks).",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 4 of 8: walk in with Gustavo (Best Man), "
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with the wedding party and immediate family.",
                "Compare speech notes with Marie so your toasts complement each other tomorrow.",
                "Return to the Inn at Great Neck by 8:00 PM with Adam, Brittany, Bara, Meda, Madison, Tomas, and Radka.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, a draft of your Best Man speech, your tux pickup confirmation from Thursday.",
        "duties": [
            ("Morning", ["10:00 AM: Pictures of the groomsmen at the hotel (you, Chris, Erik, Max, and Tomas)."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (first wave, with Chris, Erik, Max, and Tomas) — board by 1:00 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Enter the church together with Adam at the start of the processional; Adam waits at the altar and you sit down.",
                "Suggested: carry the real wedding rings yourself and let Emeric present a decoy "
                "pair on the ring pillow — classic insurance against a toddler losing the rings.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 4 of 8: walk in with Marie (Maid of Honor), "
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with the wedding party and immediate family.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes — save the dancing shoes for tomorrow night.",
        "duties": [
            ("Morning", ["10:00 AM: arrive at the Inn at Great Neck for pre-ceremony pictures with the other bridesmaids.",
                        "12:00 PM: Pictures of the Bridesmaids group at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in with Max and Julie immediately after Erik and Julia.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 7 of 8: walk in with Max and Julie, "
                "immediately after Erik and Julia.",
                "After the parent dances: join open dancing when the MC/DJ opens the floor; follow the MC/DJ's cues around scheduled events through the 12:30 AM reception end.",
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with the wedding party and immediate family.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, Sofia's rehearsal outfit if she's doing her walkthrough.",
        "duties": [
            ("Morning", ["10:00 AM: arrive at the Inn at Great Neck for pre-ceremony pictures with the other bridesmaids.",
                        "12:00 PM: Pictures of the Bridesmaids group at the hotel — Sofia joins this group photo too."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in with Erik immediately after Chris, Autumn, and Bara.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 6 of 8: walk in with Erik, "
                "immediately after Chris, Autumn, and Bara.",
                "After the parent dances: join open dancing when the MC/DJ opens the floor; follow the MC/DJ's cues around scheduled events through the 12:30 AM reception end.",
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with the wedding party and immediate family — sit with your husband Max!",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes — save the dancing shoes for tomorrow night.",
        "duties": [
            ("Morning", ["10:00 AM: arrive at the Inn at Great Neck for pre-ceremony pictures with the other bridesmaids.",
                        "12:00 PM: Pictures of the Bridesmaids group at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in with Max and Dalia immediately after Erik and Julia.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 7 of 8: walk in with Max and Dalia, "
                "immediately after Erik and Julia.",
                "After the parent dances: join open dancing when the MC/DJ opens the floor; follow the MC/DJ's cues around scheduled events through the 12:30 AM reception end.",
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with the wedding party and immediate family; return to the Inn at Great Neck by 8:00 PM with Meda.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, Meda's rehearsal outfit, travel documents/passport copies handy.",
        "duties": [
            ("Morning", ["10:00 AM: arrive at the Inn at Great Neck for pre-ceremony pictures with the other bridesmaids.",
                        "12:00 PM: Pictures of the Bridesmaids group at the hotel — Meda joins this group photo too."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in with Chris and Autumn immediately after Chris escorts Karin.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 5 of 8: walk in with Chris and Autumn, "
                "immediately after Marie and Gustavo.",
                "Before the processional, help Meda get ready for her entry after Marie.",
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with the wedding party and immediate family.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes. Confirm your 7:00 AM pickup with Chris for tomorrow's hair appointment at Christie & Co. in Bayside.",
        "duties": [
            ("Morning — Hair Appointment", [
                "7:00 AM: Chris picks you up at the hotel and drives you to Christie & Co. Luxury Hair Salon & Spa in Bayside.",
                "8:30 AM: hair appointment with Brittany at Christie & Co.; Karin and Omi have a separate appointment at a salon not specified in the timetable.",
            ]),
            ("Late Morning", ["12:00 PM: Pictures of the Bridesmaids group at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (second/main wave, with the rest of the bridal party) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in with Chris and Bara immediately after Chris escorts Karin.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 5 of 8: walk in with Chris and Bara, "
                "immediately after Marie and Gustavo.",
                "After the Grand Entrance &amp; Seating sequence, help Madison stay safe near the dance floor when it is open.",
                "~10:45 PM, during cake cutting: help Madison stay safely with the family.",
            ]),
        ],
        "reminder": "Must bring: comfortable flats for dancing, dress code is any color but white. Chris picks you up at 7:00 AM for the 8:30 AM appointment at Christie & Co. in Bayside.",
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
                "Practice escorting Karin into the church and confirm your later processional transition with the officiant.",
                "Confirm the rest of your processional position with the officiant.",
            ]),
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with the wedding party and immediate family. As Madison's godfather, help keep an eye on her if she's there.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, your tux pickup confirmation from Thursday. Confirm your processional transition with the officiant. Set an early alarm — you're driving Autumn to her 7:00 AM hair appointment pickup.",
        "duties": [
            ("Morning — Drive Autumn to Her Hair Appointment", [
                "7:00 AM: pick up Autumn at the hotel and drive her to Christie & Co. Luxury Hair Salon & Spa in Bayside.",
                "8:30 AM: Brittany and Autumn's appointment at Christie & Co.; Karin and Omi have a separate hair appointment (salon not specified).",
            ]),
            ("Late Morning", ["10:00 AM: Pictures of the groomsmen at the hotel (you, Gustavo, Erik, Max, and Tomas)."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (first wave, with Gustavo, Erik, Max, and Tomas) — board by 1:00 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Escort Karin into the church; this signals the congregation to stand.",
                "Rejoin Autumn and Bara for your trio entry after Karin.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 5 of 8: walk in with Autumn and Bara, "
                "immediately after Marie and Gustavo.",
                "After the Grand Entrance &amp; Seating sequence, help Madison stay safe near the dance floor when it is open.",
                "~10:45 PM, during cake cutting: help Madison stay safely with the family.",
            ]),
        ],
        "reminder": "Must bring: black tux/suit (picked up Thursday), boutonniere. You are personally responsible for "
                    "escorting Karin into the church and then entering with Autumn and Bara. Confirm the transition: the timetable lists you in both processional entries. You're also "
                    "driving Autumn to Christie & Co. in Bayside for the 8:30 AM hair appointment — pickup at 7:00 AM.",
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
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Attend the full processional walkthrough and confirm your position in line with the officiant.",
            ]),
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with the wedding party and immediate family.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes. Remember there's also an 'Eric Demery' at this wedding — don't mix up name cards at dinner! Confirm how you return to your later processional entry after escorting Omi.",
        "duties": [
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck — board by 1:00 PM. "
                          "Note: there is also an 'Eric Demery' at this wedding (Emeric's dad) — "
                          "don't mix up name cards!"]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Escort Omi into the church and help her to her seat.",
                "Afterward, return for your entry with Julia immediately after Chris, Autumn, and Bara; confirm the transition with the officiant because the timetable lists you in both entries.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 6 of 8: walk in with Julia, "
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with the wedding party and immediate family — sit with your wife Julie!",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes, your tux pickup confirmation from Thursday.",
        "duties": [
            ("Morning", ["10:00 AM: Pictures of the groomsmen at the hotel (you, Gustavo, Chris, Erik, and Tomas)."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck (first wave, with Gustavo, Chris, Erik, and Tomas) — board by 1:00 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk with Julie and Dalia immediately after Erik and Julia.",
                "Exit after the main party and form the line outside for the bubble send-off.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "4:30–6:30 PM: private wedding suite with the bridal party.",
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "~7:00 PM: formal portraits.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 7 of 8: walk in with Julie and Dalia, "
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
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "A short, simplified walkthrough of your entrance with Sofia — no need for the full grown-up run-through.",
            ]),
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with your family; return to the Inn at Great Neck by 8:00 PM with Adam, Brittany, Bara, Madison, Tomas, and Radka.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: a comfort item for the long travel day, comfortable shoes for the quick walkthrough.",
        "duties": [
            ("Late Morning", ["12:00 PM: join the Pictures of the Bridesmaids group photo at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck together with your "
                          "mom Bara (second/main wave) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in with Sofia after Marie, immediately before Emeric pulls Madison's wagon.",
                "Scatter flower petals as you walk — the petal basket is included in the OG Floral order.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "6:30 PM: join the bridal party's private suite cocktail hour.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 3 of 8: walk in together with Emeric, Sofia, "
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
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "A short, simplified walkthrough of your entrance with Meda — no need for the full grown-up run-through.",
            ]),
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Optional — an early bedtime is recommended since tomorrow is a big day.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: comfortable shoes for the quick walkthrough.",
        "duties": [
            ("Late Morning", ["12:00 PM: join the Pictures of the Bridesmaids group photo at the hotel."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck together with your "
                          "mom Julia (second/main wave) — board by 1:15 PM."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Walk in with Meda after Marie, immediately before Emeric pulls Madison's wagon.",
                "Scatter flower petals as you walk — the petal basket is included in the OG Floral order.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "6:30 PM: join the bridal party's private suite cocktail hour.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 3 of 8: walk in together with Emeric, Meda, "
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
            ("Ceremony Rehearsal (4:00–5:00 PM, St John's Lutheran Church)", [
                "Optional and brief — at 1 year old, a full rehearsal isn't necessary. A quick look at the wagon route is enough if her nap schedule allows.",
            ]),
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with family; return to the Inn at Great Neck by 8:00 PM.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: snacks, a comfort item/blanket, a diaper bag.",
        "duties": [
            ("Late Morning", ["12:00 PM: join the Pictures of the Bridesmaids group photo at the hotel (your mom Brittany brings the wedding bands and wedding invitation as photo props)."]),
            ("Arrival", ["Ride the Camelot Limo Bus from the Inn at Great Neck together with your "
                          "mom Brittany (second/main wave) — board by 1:15 PM. The wagon travels in the bus's luggage bay."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Ride down the aisle in a decorated wagon, pulled by Emeric, immediately after the flower girls.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "6:30 PM: join the general cocktail hour with the guests.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 3 of 8: enter together with Emeric, Meda, "
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
                "Your parents will be with you during the ceremony.",
            ]),
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", [
                "Attend with your family; the timetable lists your parents taking you to the church the next day.",
            ]),
        ],
        "rehearsal_reminder": "Must bring: the ring pillow (practice run — no need for the real rings tonight), a comfort item.",
        "duties": [
            ("Arrival", ["Travel with your parents, Eric & April Demery, who drive their own car directly to the church; departure time is not specified."]),
            ("Ceremony (2:00 PM, St John's Lutheran Church)", [
                "Pull Madison down the aisle in her wagon, right after the flower girls Meda and Sofia walk in.",
                "Carry the ring pillow forward before the ring exchange. (Suggested: a decoy pair of "
                "rings on your pillow, with Gustavo safely holding the real rings.)",
                "The pastor reads the scripture; everyone kneels for prayer.",
            ]),
            ("Reception (Leonard's Palazzo)", [
                "~5:30 PM: pictures in front of Leonard's Palazzo with the whole group.",
                "6:30 PM: join the general cocktail hour with the guests.",
                "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 3 of 8: enter together with Meda, Sofia, "
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", ["Join the wedding party and immediate family. Return to the Inn at Great Neck by 8:00 PM with Brittany, Gustavo, Bara, Meda, Madison, Tomas, and Radka."]),
        ],
        "rehearsal_reminder": "Bring the ceremony items needed for setup and your comfortable rehearsal shoes.",
        "duties": [
            ("Morning", ["9:30 AM: receive the florist's bouquet delivery at the hotel.",
                         "After the 9:30 AM delivery: route Brittany's bouquet to her room without seeing her.",
                         "10:00 AM: join the groomsmen photos."]),
            ("1:15 PM", ["Ride with Peter in his car directly to St John's Lutheran Church."]),
            ("Ceremony (2:00 PM)", ["Enter with Gustavo at the start of the processional; you wait at the altar while Gustavo sits down.",
                                    "Say your personal vows, then repeat the official religious vows after the pastor.",
                                    "Exchange rings with Brittany and light the unity candle after the family candle-lighting.",
                                    "At the recessional, after everyone else: exit last with Brittany through the bubble line."]),
            ("Reception", ["3:30 PM: take the party bus from the church to Leonard's Palazzo.",
                           "5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "~7:00 PM: join the formal room/portrait shots.",
                           "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 8 of 8: walk in with Brittany after Max, Julie, and Dalia; the wedding party forms an arch.",
                           "After the grand entrance: first dance with Brittany to \"Can't Help Falling in Love\" by Elvis Presley.",
                           "After the first dance, join Radka for the parent dance to \"Zestárli jsme lásko\" by Nohavica."]),
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", ["Join the wedding party and immediate family. Return to the Inn at Great Neck by 8:00 PM with Adam, Gustavo, Bara, Meda, Madison, Tomas, and Radka."]),
        ],
        "rehearsal_reminder": "Bring any ceremony items needed for setup and comfortable rehearsal shoes.",
        "duties": [
            ("Morning", ["Attend the 8:30 AM hair appointment at Christie & Co. Luxury Hair Salon & Spa in Bayside with Autumn.", "Bring the wedding bands and invitation for the 12:00 PM bridesmaids photo."]),
            ("1:15 PM", ["Ride the main-wave limo bus from the Inn at Great Neck to the church."]),
            ("Ceremony (2:00 PM)", ["After the flower girls and Madison's wagon, walk in with Peter.",
                                    "Hand your bouquet to Marie.",
                                    "Say your personal vows, then repeat the official religious vows after the pastor.",
                                    "Exchange rings with Adam and light the unity candle after the family candle-lighting."]),
            ("Reception", ["3:30 PM: take the party bus from the church to Leonard's Palazzo.",
                           "5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "~7:00 PM: join the formal room/portrait shots.",
                           "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 8 of 8: walk in with Adam after Max, Julie, and Dalia; the wedding party forms an arch.",
                           "After the grand entrance: first dance with Adam to \"Can't Help Falling in Love\" by Elvis Presley.",
                           "After the first dance, join Peter for the parent dance to \"Give Me a Way\" by Riley Roth."]),
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", ["Join the wedding party and immediate family."]),
        ],
        "rehearsal_reminder": "Bring the welcome-table and memorial-table crate and wine-box favors to the venue during the week before.",
        "duties": [
            ("Morning", ["8:30 AM: hair appointment with Omi at a separate salon (location not specified in the timetable)."]),
            ("Ceremony (2:00 PM)", ["Chris escorts you into the church; your entrance signals the congregation to stand.",
                                    "Take part in the family candle-lighting.",
                                    "After the ceremony, hand bubbles to everyone outside the church."]),
            ("Reception", ["3:30 PM: take the party bus from the church to Leonard's Palazzo.",
                           "5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 1 of 8: walk in with Peter to \"You Spin Me Round\" by Dead or Alive.",
                           "After the first dance, give the welcome toast with Peter before dinner.",
                           "9:00–10:15 PM Formal Speeches segment, after the second course and before entrées: deliver Brittany's parents' speech with Peter; exact minute is not specified."]),
        ],
        "reminder": "Bring bubbles for the church send-off and confirm the venue crate has everything needed.",
        "flavor": "Brittany's mom — keeping the celebration's many thoughtful details on track.",
    },
    {
        "slug": "peter",
        "name": "Peter",
        "title": "Vowshield Cavalier",
        "role": "Father of the Bride",
        "frame": "white",
        "cost": "Call Time 9:30 AM",
        "rehearsal": [
            ("Ceremony Rehearsal (4:00–5:00 PM)", ["Join the full family walkthrough and practice the candle-lighting ceremony with Karin."]),
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", ["Join the wedding party and immediate family."]),
        ],
        "rehearsal_reminder": "Confirm the car plan for driving Adam to the church on Saturday.",
        "duties": [
            ("Morning", ["Your timetable lists teaching at 9:30 AM and 10:00 AM; the class end time is not specified."]),
            ("1:15 PM", ["1:15 PM: drive Adam directly to St John's Lutheran Church.",
                         "After arrival: leave your car parked at the church."]),
            ("Ceremony (2:00 PM)", ["Escort Brittany down the aisle with her processional group.",
                                    "Take part in the family candle-lighting."]),
            ("Reception", ["3:30 PM: ride the Camelot bus from the church to Leonard's Palazzo.",
                           "5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 1 of 8: walk in with Karin to \"You Spin Me Round\" by Dead or Alive.",
                           "After the first dance, have the parent dance with Brittany to \"Give Me a Way\" by Riley Roth.",
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", ["Join the wedding party and immediate family. Return to the Inn at Great Neck by 8:00 PM with Adam, Brittany, Gustavo, Bara, Meda, Madison, and Radka."]),
        ],
        "rehearsal_reminder": "Bring a memorial-table item in memory of your late brother Dominik.",
        "duties": [
            ("Before the Wedding", ["Bring an item in memory of Dominik for the memorial table."]),
            ("Arrival", ["Ride the main-wave limo bus from the Inn at Great Neck to the church."]),
            ("Ceremony (2:00 PM)", ["Enter together with Tomas as the groom's parents; take part in the family candle-lighting."]),
            ("Reception", ["3:30 PM: take the party bus from the church to Leonard's Palazzo.",
                           "5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 2 of 8: walk in with Tomas immediately after Peter and Karin to \"Hej, Górale\".",
                           "After Brittany and Peter's dance, have the parent dance with Adam to \"Zestárli jsme lásko\" by Nohavica.",
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
            ("Rehearsal Dinner (6:00 PM, Zum Stammtisch)", ["Host the rehearsal dinner with Tomas. Return to the Inn at Great Neck by 8:00 PM with Adam, Brittany, Gustavo, Bara, Meda, and Tomas."]),
        ],
        "rehearsal_reminder": "Confirm the rehearsal dinner plan and keep comfortable shoes handy for the walkthrough.",
        "duties": [
            ("Morning", ["Join the groomsmen photos at the hotel at 10:00 AM."]),
            ("Arrival", ["The timetable lists you on the 1:00 PM first-wave bus and the 1:15 PM main-wave bus; confirm which departure is correct."]),
            ("Ceremony (2:00 PM)", ["Walk into the church with Radka as the groom's parents; take part in the family candle-lighting."]),
            ("Reception", ["3:30 PM: take the party bus from the church to Leonard's Palazzo.",
                           "5:30 PM: join the group photos outside Leonard's Palazzo.",
                           "During the 15–20 minute Grand Entrance &amp; Seating sequence after the 7:30 PM reception start, group 2 of 8: walk in with Radka immediately after Peter and Karin to \"Hej, Górale\".",
                           "After Brittany and Peter's dance, join Radka and Adam for the parent dance to \"Zestárli jsme lásko\" by Nohavica.",
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
     "Full rehearsal-day plan set below; the Oct 18 timetable lists rehearsal dinner at Zum Stammtisch, beginning at 6:00 PM."),
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
    ("4:00–5:00 PM", "Ceremony rehearsal — full walkthrough of the processional order, altar positions, vow cues, ring exchange, candle-lighting, and recessional, led by the officiant.", "Adam, Brittany, full wedding party, both sets of parents, Omi, Eric &amp; April Demery, officiant", "St John's Lutheran Church"),
    ("4:05 PM", "Adam &amp; Brittany step aside to privately practice their vows.", "Adam, Brittany", "St John's Lutheran Church"),
    ("6:00 PM", "Rehearsal dinner begins.", "Wedding party and listed family", "Zum Stammtisch"),
    ("8:00 PM", "Return to the Inn at Great Neck.", "Adam, Brittany, Gustavo, Bara, Meda, Madison, Tomas, Radka", "Zum Stammtisch → Inn at Great Neck"),
]

FRIDAY_NOTES = (
    "<strong>Bring to rehearsal:</strong> comfortable shoes, the officiant's contact info, and the ring pillow "
    "(practice run only)."
)

SATURDAY_ROWS = [
    ("7:00 AM", "Chris drives Autumn from the hotel to Christie & Co. Luxury Hair Salon & Spa.", "Autumn, Chris", "Inn at Great Neck → Bayside"),
    ("8:30 AM", "Hair appointments: Brittany and Autumn at Christie & Co.; Karin and Omi at a separate salon (not specified).", "Brittany, Autumn, Karin, Omi", "Christie & Co. Luxury Hair Salon & Spa, Bayside; second salon TBD"),
    ("9:30 AM", "Adam receives the florist's bouquet delivery at the hotel.", "Adam", "Inn at Great Neck"),
    ("9:30 AM and 10:00 AM", "peter's timetable lists teaching at both times; the class end time is not specified.", "peter", "Off-site"),
    ("After the 9:30 AM delivery", "Adam routes Brittany's bouquet to her room without seeing her, preserving the first-look surprise.", "Adam", "Inn at Great Neck"),
    ("10:00 AM", "Groomsmen take photos at the hotel.", "Adam, Gustavo, Chris, Erik, Max, Tomas", "Inn at Great Neck"),
    ("10:00 AM", "Marie, Dalia, Julia, and Julie arrive at the hotel for pictures.", "Marie, Dalia, Julia, Julie", "Inn at Great Neck"),
    ("12:00 PM", "Pictures of the Bridesmaids group — Brittany brings the wedding bands and wedding invitation as photo props.", "Brittany, Marie, Dalia, Julia, Julie, Bara, Autumn, Meda, Sofia, Madison, Radka, Omi", "Inn at Great Neck"),
    ("1:00 PM", "Camelot Limo Bus departs hotel for the church — first wave (groomsmen + Tomas).", "Gustavo, Chris, Erik, Max, Tomas", "Inn at Great Neck → Church"),
    ("1:15 PM", "Adam and peter depart together by car directly to the church.", "Adam, peter", "Inn at Great Neck → Church"),
    ("1:15 PM", "Camelot Limo Bus departs for the church — second/main wave. Tomas is also listed on the 1:00 PM first wave; confirm his departure.", "Brittany, Marie, Dalia, Julia, Julie, Bara, Autumn, Meda, Sofia, Madison, Karin, Tomas, Radka, Omi", "Inn at Great Neck → Church"),
    ("Departure time not specified", "Emeric, Eric Demery, and April Demery travel by themselves to the church.", "Emeric, Eric Demery, April Demery", "Hotel → Church"),
    ("1:45 PM", "Arrive at church.", "Everyone", "St John's Lutheran Church"),
    ("2:00 PM", "Ceremony begins (ceremony only, no mass).", "Everyone", "St John's Lutheran Church, 2201 123rd St, College Point"),
    ("2:00 PM", "Processional / entrances to altar — see Processional Order.", "See order below", "Church"),
    ("After the processional", "Pastor reads the scripture; everyone kneels for prayer.", "Everyone", "Church"),
    ("During the ceremony", "Adam and Brittany say personal vows, then repeat the official religious vows after the pastor.", "Adam, Brittany", "Church"),
    ("Ring exchange", "Emeric brings the rings to the altar; Adam and Brittany exchange rings.", "Adam, Brittany, Emeric", "Church"),
    ("Candle-lighting", "Peter, Karin, Tomas, and Radka light candles from the Christ candle and hold the couple's hands as they light the unity candle.", "Adam, Brittany, Peter, Karin, Tomas, Radka", "Church"),
    ("After the ceremony", "Karin hands bubbles to everyone; the wedding party forms a line outside for the send-off.", "Karin, wedding party, guests", "Church exterior"),
    ("Recessional", "Everyone exits the church; Adam and Brittany exit last together, with Marie holding Brittany's dress as they exit.", "Everyone; Marie", "Church"),
    ("Church payments and cleanup", "Adam hands the $500 cash donation envelope to the pastor and the $200 envelope to the musician who played the bridal march; Karin uses a broom to clean up the flower petals.", "Adam, Karin", "Church"),
    ("After the rest of the party exits", "Everyone else forms the bubble-send-off line outside.", "Everyone except Adam &amp; Brittany", "Church exterior"),
    ("3:30 PM", "Take the party bus from the church back to Leonard's Palazzo.", "Wedding party and listed family", "St John's Lutheran Church → Leonard's Palazzo"),
    ("Arrival time not specified", "The party bus arrives at Leonard's Palazzo; the timetable gives the 3:30 PM church departure but no arrival time.", "Wedding party and listed family", "Leonard's Palazzo"),
    ("4:30 PM", "Bridal suite becomes available for the wedding party.", "Bridal party", "Leonard's Palazzo"),
    ("4:30–6:30 PM", "Suite Set — appetizers &amp; beverage service.", "Host party", "Private suite, Leonard's Palazzo"),
    ("5:30 PM", "Pictures in front of Leonard's Palazzo.", "Everyone (bridal party, Emeric, both sets of parents, Omi)", "Leonard's Palazzo exterior"),
    ("6:30 PM", "Cocktail hour begins; the wedding party and Meda and Sofia remain in the separate wedding suite.", "Adam, Brittany, Marie, Dalia, Julia, Julie, Bara, Autumn, Gustavo, Chris, Erik, Max, Meda, Sofia", "Private suite, Leonard's Palazzo"),
    ("6:30 PM", "Cocktail hour begins for other guests, including Madison, Emeric, peter, Karin, Tomas, Radka, and Omi.", "Guests", "Leonard's Palazzo"),
    ("7:00 PM", "Formal room/portrait shots.", "Bridal party", "Leonard's Palazzo"),
    ("7:30 PM", "Reception begins.", "Everyone", "Reception room"),
    ("After reception begins (7:30 PM)", "Grand Entrance & Seating, a 15–20 minute sequence — see Grand Entrance Order.", "Everyone", "Reception room"),
    ("After the grand entrance", "Adam and Brittany's first dance to \"Can't Help Falling in Love\" by Elvis Presley (Dancing on Clouds effect).", "Adam, Brittany", "Dance floor"),
    ("After the first dance", "MC/DJ invites other couples to join Adam and Brittany on the dance floor.", "Couples", "Dance floor"),
    ("Parent dances", "Brittany dances with Peter to \"Give Me a Way\" by Riley Roth; Adam dances with Radka to \"Zestárli jsme lásko\" by Nohavica.", "Brittany, Peter, Adam, Radka", "Dance floor"),
    ("After the parent dances", "Open dancing; the requested mix is mostly Pitbull and Bebe Rexha.", "Everyone", "Dance floor"),
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
    "At the 2:00 PM ceremony: Adam and Gustavo enter together; Adam waits at the altar and Gustavo sits down.",
    "Next: Erik escorts Omi (grandmother of the bride) into the church and to her seat.",
    "Next: Tomas and Radka (groom's parents) enter together and are seated.",
    "Next: Chris escorts Karin (bride's mother) into the church; this signals the congregation to stand.",
    "Next: Chris, Autumn, and Bara walk in together.",
    "Next: Erik and Julia walk in together.",
    "Next: Max, Julie, and Dalia walk in together.",
    "Next: Marie (Maid of Honor) enters alone.",
    "Next: Meda and Sofia (flower girls) enter together with their petal baskets.",
    "As they walk: Meda and Sofia scatter petals.",
    "Next: Emeric pulls Madison down the aisle in a wagon; Madison carries a small petal basket.",
    "Next: Brittany walks in with Peter.",
    "At the altar: Brittany hands her bouquet to Marie.",
    "The pastor reads the scripture; everyone kneels for prayer.",
    "Adam and Brittany say their personal vows, then repeat the official religious vows after the pastor.",
    "Emeric brings the rings to the altar.",
    "Next: Adam and Brittany exchange rings.",
    "During the candle-lighting ceremony, Peter, Karin, Tomas, and Radka light candles from the Christ candle; Adam and Brittany light the unity candle with their parents holding their hands.",
    "After the ceremony: Karin hands bubbles to everyone; the wedding party forms a line outside.",
    "At the recessional, everyone exits before Adam and Brittany, who leave last together.",
    "At 3:30 PM: the party bus departs from the church for Leonard's Palazzo.",
]

GRAND_ENTRANCE_ORDER = [
    "The 15–20 minute entrance-and-seating sequence follows cocktail hour. Group 1: Peter and Karin (bride's parents) enter to \"You Spin Me Round\" by Dead or Alive.",
    "Group 2: Tomas and Radka (groom's parents) enter immediately after Peter and Karin to \"Hej, Górale\" (Silesian song).",
    "Group 3: Emeric, Meda, Sofia, and Madison enter together immediately after Tomas and Radka.",
    "Group 4: Marie (Maid of Honor) and Gustavo (Best Man) enter together immediately after Emeric, Meda, Sofia, and Madison.",
    "Group 5: Chris, Autumn, and Bara enter together immediately after Marie and Gustavo.",
    "Group 6: Erik and Julia enter together immediately after Chris, Autumn, and Bara.",
    "Group 7: Max, Julie, and Dalia enter together immediately after Erik and Julia.",
    "Group 8: <strong>Adam and Brittany</strong> enter as the grand finale immediately after Max, Julie, and Dalia, to \"Give Me Everything\" by Pitbull; the wedding party forms an arch.",
]

TRANSPORT_ROWS = [
    ("Morning (pre-bus)", "Chris's personal car", "7:00 AM, Inn at Great Neck", "Christie & Co. Luxury Hair Salon & Spa", "Not listed", "Autumn; Brittany is also listed at the 8:30 AM appointment there"),
    ("Morning (pre-bus)", "Not specified", "Not listed", "Separate hair salon (not named)", "Not listed", "Karin and Omi"),
    ("Day-of (pre-ceremony → reception), first wave", "Camelot Specialty Limo — 26-pax Bus, Bill Townsend (646) 498-4454, Res. #109521", "1:00 PM, Inn at Great Neck", "Church (2:00 PM)", "Church", "Gustavo, Chris, Erik, Max, Tomas (Tomas is also listed in the 1:15 PM wave; confirm)"),
    ("Day-of (pre-ceremony → reception), second wave", "Camelot Specialty Limo — same bus, same reservation", "1:15 PM, Inn at Great Neck", "Church (2:00 PM)", "Leonard's Palazzo", "Brittany, Marie, Dalia, Julia, Julie, Bara, Autumn, Meda, Sofia, Madison, Karin, Tomas, Radka, Omi"),
    ("Day-of (pre-ceremony, separate)", "peter's personal car", "1:15 PM, Hotel", "Church (peter parks the car)", "Church", "Adam + peter"),
    ("Departure time not listed", "Eric &amp; April Demery's personal car", "Hotel", "Church", "Church", "Emeric, Eric Demery, April Demery"),
    ("3:30 PM", "Camelot Specialty Limo — same bus", "St John's Lutheran Church", "Leonard's Palazzo", "Leonard's Palazzo", "Wedding party and listed family; the source lists departure, not an arrival time"),
    ("After the reception", "peter's personal car", "St John's Lutheran Church", "—", "—", "Retrieve the car; responsible person and pickup time to be confirmed"),
    ("Post-reception", "Camelot Limo Bus — extended 12:30 AM return run", "Leonard's Palazzo", "—", "Inn at Great Neck", "Everyone"),
]

TRANSPORT_NOTES = [
    "<strong>1:00 PM:</strong> The first bus wave departs with Gustavo, Chris, Erik, Max, and Tomas.",
    "<strong>1:15 PM:</strong> The main bridal-party bus wave departs the Inn at Great Neck for the church.",
    "The Oct 18 timetable lists Tomas on both bus waves; confirm which departure is correct.",
    "The timetable lists Chris escorting Karin and later entering with Autumn and Bara, and Erik escorting Omi and later entering with Julia. Confirm how each returns to the processional.",
    "Madison rides the Camelot bus with her mom Brittany.",
    "Emeric's wagon travels in the bus's luggage bay.",
]

MUST_BRING_ROWS = [
    ("Adam (Groom)", "Marriage license, vows, wedding band, peter's ride confirmed, tux picked up Thursday", "Needed to legally marry"),
    ("Brittany (Bride)", "Marriage license, vows, bouquet, something old/new/borrowed/blue, wedding bands + wedding invitation (as photo props for the 12:00 PM bridesmaid pictures)", "Bouquet is handed to Marie mid-ceremony"),
    ("Marie (Maid of Honor)", "Tissues/emergency kit, MOH speech notes", "Receives the bouquet, gives a toast later"),
    ("Gustavo (Best Man)", "The real wedding rings (decoy-ring plan), Best Man speech notes, tux picked up Thursday", "Rings must reach the altar"),
    ("Dalia / Julia / Julie / Bara / Autumn (Bridesmaids)", "Dresses/shoes (any color but white), flats for dancing. Autumn: 7:00 AM hotel pickup with Chris; 8:30 AM Christie & Co. appointment with Brittany.", "Comfort for the long day"),
    ("Chris / Erik / Max (Groomsmen)", "Black tux/suit (picked up Thursday), boutonnieres. Chris: 7:00 AM hotel pickup to drive Autumn to Christie & Co. in Bayside.", "Dress code compliance"),
    ("Meda &amp; Sofia (Flower Girls)", "Flower petals/basket", "Provided as part of the OG Floral order"),
    ("Emeric (Ring Bearer)", "Ring pillow (decoy rings recommended), comfort item, the decorated wagon (acquired by Adam the week before)", "Rings are the centerpiece of the ceremony"),
    ("Madison (Flower Girl role)", "Wagon (pulled by Emeric), snacks, comfort item/blanket", "She rides in rather than walks"),
    ("Karin (Mother of the Bride)", "Bubbles for guests, welcome speech notes, the crate of welcome-table/memorial-table items + wine-box favors (dropped off the week before)", "Enters escorted by Chris; hands bubbles to guests after the ceremony"),
    ("peter (Father of the Bride)", "His car (for driving Adam), welcome speech notes", "The timetable lists teaching at 9:30 AM and 10:00 AM; class end time is not specified"),
    ("Tomas &amp; Radka (Groom's Parents)", "Candle-lighting reminder, speech notes. Radka also brings an item in memory of her late brother Dominik for the memorial table.", "Scheduled twice — ceremony + reception"),
    ("Omi (Grandmother of the Bride)", "Comfortable shoes for the aisle escort", "Escorted into the church by Erik; has a separate 8:30 AM hair appointment with Karin (salon not specified)"),
    ("Eric &amp; April Demery (Emeric's parents)", "Both: supervise Emeric", "They drive themselves and Emeric directly to the church; departure time is not specified"),
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


import re

# People whose source-CSV cells say what they do at each shared moment.
SUITE_GROUP = {"adam", "brittany", "gustavo", "chris", "erik", "max", "marie",
               "dalia", "julia", "julie", "bara", "autumn"}
GROOMSMEN = {"adam", "gustavo", "chris", "erik", "max", "tomas"}
ARRIVE_BY_BUS = {"karin", "radka", "gustavo", "chris", "erik", "max", "brittany", "marie",
                 "dalia", "julia", "julie", "bara", "autumn", "meda", "sofia", "madison", "tomas"}
NO_BUBBLES_OR_ARCH = {"adam", "brittany"}

# slug -> list of (day key, section prefix, text, detect regex, anchor regex)
# Added only when the card does not already cover the CSV cell.
PERSON_EXTRAS = {
    "adam": [
        ("rehearsal", "Before the weekend", "Thursday, Nov 5: pick up your tux from Men's Wearhouse.", r"tux", None),
        ("rehearsal", "Before the weekend", "Bring the wagon that Emeric will use to pull Madison down the aisle.", r"wagon", None),
        ("duties", "Ceremony", "While Tomas and Radka light the Adam + Brittany candle from the Christ candle, hold their hands.",
         r"hold.*hands", r"^At the recessional"),
        ("duties", "Ceremony", "Donate the $500 cash envelope to the pastor.", r"\$500", None),
        ("duties", "Ceremony", "Pay the $200 envelope to the musician playing the bridal march.", r"\$200", None),
    ],
    "brittany": [
        ("duties", "Ceremony", "While Karin and Peter light the Adam + Brittany candle from the Christ candle, hold their hands.",
         r"hold.*hands", None),
        ("duties", "Ceremony", "At the recessional, exit the church last with Adam.", r"exit.*last", None),
    ],
    "karin": [
        ("duties", "Arrival", "1:15 PM: take the party bus to the church.", r"1:15", None),
        ("duties", "Ceremony", "After everyone has exited, use a broom to clean up the flower petals.", r"broom", None),
    ],
}


def _minutes(text):
    m = re.match(r"^~?(\d{1,2}):(\d\d)", text)
    if not m:
        return None
    h = int(m.group(1))
    return (h if h == 12 else h + 12) * 60 + int(m.group(2))


def _find_section(duties, prefix):
    for heading, items in duties:
        if heading.startswith(prefix):
            return items
    items = []
    if prefix == "Before the weekend":
        duties.insert(0, (prefix, items))
    elif prefix == "Arrival":
        pos = next((i for i, (h, _) in enumerate(duties) if h.startswith("Ceremony")), len(duties))
        duties.insert(pos, (prefix, items))
    else:
        duties.append((prefix, items))
    return items


def _insert_before(items, text, anchor):
    if anchor:
        for i, existing in enumerate(items):
            if re.search(anchor, existing, re.I):
                items.insert(i, text)
                return
    items.append(text)


def _sort_reception(items):
    keyed, prev = [], 0
    for idx, (text, explicit) in enumerate(items):
        key = explicit
        if key is None:
            key = _minutes(text)
            if key is None and re.search(r"Grand Entrance", text):
                key = 19 * 60 + 30
            elif key is None and re.search(r"^After the (first|parent)", text):
                key = 19 * 60 + 45
            elif key is None:
                key = prev
        prev = key
        keyed.append((key, idx, text))
    return [t for _, _, t in sorted(keyed)]


def fill_source_gaps():
    """Make sure every line of the before / church / reception CSVs is on each card."""
    for person in PEOPLE:
        slug = person["slug"]
        for day, prefix, text, detect, anchor in PERSON_EXTRAS.get(slug, []):
            blob = " ".join(i for _, items in person["rehearsal"] + person["duties"] for i in items)
            if re.search(detect, blob, re.I):
                continue
            _insert_before(_find_section(person[day], prefix), text, anchor)

        duties = person["duties"]
        blob = lambda: " ".join(i for _, items in duties for i in items)
        has = lambda rx: re.search(rx, blob(), re.I)

        morning = _find_section(duties, "Morning")
        if slug in GROOMSMEN and not has(r"groomsm"):
            morning.append("10:00 AM: pictures of the groomsmen at the hotel.")
        if slug == "radka" and not has(r"12:00"):
            morning.append("12:00 PM: pictures of the bridesmaids.")

        ceremony = _find_section(duties, "Ceremony")
        if slug in ARRIVE_BY_BUS:
            if not has(r"1:45"):
                ceremony.insert(0, "1:45 PM: arrive at St John's Lutheran Church on the Camelot Limo Bus.")
        elif slug == "peter" and not has(r"1:45"):
            ceremony.insert(0, "1:45 PM: arrive at St John's Lutheran Church.")
        if not has(r"kneel"):
            _insert_before(ceremony, "Kneel with everyone for the prayer.", r"candle|ring|vows|^exit|exit the church|bubble")
        if slug not in NO_BUBBLES_OR_ARCH and not has(r"hand.*bubbles|bubbles from karin"):
            _insert_before(ceremony, "Karin hands bubbles to everyone — take yours for the send-off.", r"^exit|exit")
        if slug not in NO_BUBBLES_OR_ARCH | {"marie"} and not has(r"line (outside|in front)|form the line"):
            _insert_before(ceremony, "Exit the church and form a line in front of the church.", r"broom")

        reception = _find_section(duties, "Reception")
        new = [(t, None) for t in reception]
        if not has(r"3:30"):
            new.append(("3:30 PM: leave the church on the party bus to Leonard's Palazzo.", 15 * 60 + 30))
        if not has(r"5:30"):
            new.append(("5:30 PM: pictures in front of Leonard's Palazzo.", 17 * 60 + 30))
        if slug in SUITE_GROUP and not has(r"suite"):
            new.append(("4:30 PM: the bridal suite becomes available; set up in the separate wedding suite (appetizers &amp; beverage service).", 16 * 60 + 30))
        if not has(r"cocktail"):
            where = "in the separate wedding suite" if slug in SUITE_GROUP else "with the guests"
            new.append((f"6:30 PM: cocktail hour {where}.", 18 * 60 + 30))
        if slug not in NO_BUBBLES_OR_ARCH and not has(r"arch"):
            new.append(("After the walk-in, everybody forms an arch for the bride and groom.", 19 * 60 + 31))
        if not has(r"dinner"):
            new.append(("Eat dinner.", 20 * 60))
        if slug in NO_BUBBLES_OR_ARCH and not has(r"cake"):
            new.append(("~10:45 PM: cut the cake together.", 22 * 60 + 45))
        if not has(r"open danc"):
            new.append(("Open dancing — mostly Pitbull and Bebe Rexha.", 23 * 60))
        reception[:] = _sort_reception(new)


fill_source_gaps()


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
