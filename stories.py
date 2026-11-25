"""News for Tuesday 24 November 2026. Facts only, in reading order."""

STORIES = [
    {
        "rank": 1,
        "tier": "lead",
        "region": "EUROPE · UKRAINE / RUSSIA",
        "headline": "Ukraine war spreads beyond its borders.",
        "deck": (
            "Ukraine is sinking Russian ships, and some NATO allies voice anxiety.\n"
            "Moscow threatens a NATO member with \"open war\" over plans to close a border.\n"
            "Zelensky warns that new Russian strikes are coming. Latvia's president calls Russia's ceasefire talks a \"decoy\".\n"
            "A Russian airstrike damaged an apartment block in Zaporizhzhia."
        ),
        "icon": "black_sea",
    },
    {
        "rank": 2,
        "tier": "second",
        "region": "MIDDLE EAST",
        "headline": "Iran–US standoff over Hormuz.",
        "deck": "No talks until Iran's 7 conditions are met. Israel claims Iran is developing chemical weapons; Tehran denies it.",
        "icon": "hormuz",
    },
    {
        "rank": 3,
        "tier": "second",
        "region": "MIDDLE EAST · GAZA",
        "headline": "Gaza: drone strike kills 3.",
        "deck": "An Israeli drone strike killed three Palestinians in southern Gaza.",
        "icon": "gaza",
    },
    {
        "rank": 4,
        "tier": "brief",
        "region": "AMERICAS",
        "headline": "Colombia",
        "deck": "Car bomb outside government offices injures 23. President vows to pursue \"narco-terrorists\".",
        "icon": "flame",
    },
    {
        "rank": 5,
        "tier": "brief",
        "region": "EUROPE",
        "headline": "Serbia",
        "deck": "School shooting; a 17-year-old is arrested.",
        "icon": "school",
    },
    {
        "rank": 6,
        "tier": "brief",
        "region": "BUSINESS",
        "headline": "Germany",
        "deck": "Thousands of VW workers protest layoffs and a pay freeze.",
        "icon": "factory",
    },
    {
        "rank": 7,
        "tier": "brief",
        "region": "MARKETS",
        "headline": "Markets",
        "deck": "US stocks rally after Nvidia reinstates Jensen Huang as CEO.",
        "icon": "chart",
    },
    {
        "rank": 8,
        "tier": "brief",
        "region": "ASIA",
        "headline": "Bangladesh",
        "deck": "Ousted leader Sheikh Hasina plans to return from exile.",
        "icon": "plane",
    },
    {
        "rank": 9,
        "tier": "brief",
        "region": "RELIGION",
        "headline": "Vatican",
        "deck": "Excerpts of Pope Francis's private diary are published.",
        "icon": "book",
    },
    {
        "rank": 10,
        "tier": "ticker",
        "region": "",
        "headline": "",
        "deck": (
            "Malaysia to send 6,803 people back to Myanmar despite the ICJ's Rohingya genocide ruling"
            " • UN debate grows over a treaty on autonomous weapons and drones"
            " • Beaver supermoon lights up the night sky"
        ),
        "icon": "ticker",
    },
]


def stories_by_tier(tier):
    return [story for story in STORIES if story["tier"] == tier]
