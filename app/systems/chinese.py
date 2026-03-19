"""Chinese BaZi (Four Pillars of Destiny) calculations.

Uses the 60-Jiazi sexagenary cycle of Heavenly Stems and Earthly Branches.
Reference anchor: 1984 = Jiǎzǐ year; 2000-01-01 = Jiǎzǐ day.
"""

from __future__ import annotations

from datetime import date

# Tunable configuration for this system's AI readings.
# Edit these strings to refine how Claude generates BaZi horoscopes
# without touching any calculation or API logic.
SYSTEM_CONFIG = {
    # Appended to the base system prompt — change Claude's interpretive lens.
    "system_prompt": (
        "You are interpreting a BaZi (Four Pillars of Destiny) chart within the Chinese "
        "metaphysical tradition. Work with Five Elements theory (Wuxing): Wood, Fire, Earth, "
        "Metal, Water in their Yang and Yin forms. The Day Master (the person's day stem) is "
        "the self — all other pillars are read in relation to it. "
        "Assess elemental balance: which elements strengthen vs. weaken the Day Master, "
        "and how today's day pillar interacts with the natal chart through combinations, "
        "clashes, harms, or harmonies."
    ),
    # Injected into the user prompt — tells Claude which chart factors to foreground.
    "reading_focus": (
        "Open with the Day Master's element and polarity as the person's core nature. "
        "Identify which natal pillars produce, control, or exhaust the Day Master element. "
        "Then compare today's Day Pillar (stem + branch) against the natal chart: "
        "note any Six Harmonies (combinations), Six Clashes, or Three Harmonies that activate. "
        "Let elemental dynamics — not just symbols — drive the daily narrative."
    ),
    # Tells Claude how to structure and style the output.
    "presentation": (
        "150–200 words. Second person throughout. "
        "Use Chinese metaphysical terms naturally (Day Master, Heavenly Stem, Earthly Branch, "
        "Wuxing, clash, harmony) but anchor each term with immediate meaning. "
        "Three beats: (1) the Day Master's fundamental energy and how today amplifies or "
        "challenges it, (2) a specific elemental dynamic to work with or navigate, "
        "(3) a practical action or mindset aligned with today's qi."
    ),
}

HEAVENLY_STEMS = ["Jiǎ", "Yǐ", "Bǐng", "Dīng", "Wù", "Jǐ", "Gēng", "Xīn", "Rén", "Guǐ"]

STEM_ELEMENTS = [
    "Yang Wood", "Yin Wood", "Yang Fire", "Yin Fire", "Yang Earth",
    "Yin Earth", "Yang Metal", "Yin Metal", "Yang Water", "Yin Water",
]

EARTHLY_BRANCHES = ["Zǐ", "Chǒu", "Yín", "Mǎo", "Chén", "Sì", "Wǔ", "Wèi", "Shēn", "Yǒu", "Xū", "Hài"]

BRANCH_ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
                  "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]

BRANCH_ELEMENTS = [
    "Yang Water", "Yin Earth", "Yang Wood", "Yin Wood", "Yang Earth", "Yin Fire",
    "Yang Fire", "Yin Earth", "Yang Metal", "Yin Metal", "Yang Earth", "Yin Water",
]

# Solar term month boundaries (approximate day of month when each Chinese month begins).
# Month index 0 = Tiger month (Yin, starts ~Feb 4), corresponds to Chinese month 1.
# Each entry is (gregorian_month, approx_day_start).
SOLAR_TERM_STARTS = [
    (2, 4),   # Month 1  – Yin  (Tiger)
    (3, 6),   # Month 2  – Mǎo (Rabbit)
    (4, 5),   # Month 3  – Chén (Dragon)
    (5, 6),   # Month 4  – Sì  (Snake)
    (6, 6),   # Month 5  – Wǔ  (Horse)
    (7, 7),   # Month 6  – Wèi (Goat)
    (8, 7),   # Month 7  – Shēn (Monkey)
    (9, 8),   # Month 8  – Yǒu (Rooster)
    (10, 8),  # Month 9  – Xū  (Dog)
    (11, 7),  # Month 10 – Hài (Pig)
    (12, 7),  # Month 11 – Zǐ  (Rat)
    (1, 6),   # Month 12 – Chǒu (Ox) — previous year's Jan
]

# Earthly branch for each Chinese month (Tiger month = index 2 = Yín)
MONTH_BRANCHES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1]

# Hour branch: each earthly branch covers 2 hours starting at 23:00 for Zǐ
# Hour 23-00 → Zǐ(0), 01-02 → Chǒu(1), ..., 21-22 → Hài(11)
def _hour_branch_index(hour: int) -> int:
    return ((hour + 1) % 24) // 2


def _jiazi(index: int) -> dict:
    stem_idx = index % 10
    branch_idx = index % 12
    return {
        "stem": HEAVENLY_STEMS[stem_idx],
        "stem_element": STEM_ELEMENTS[stem_idx],
        "branch": EARTHLY_BRANCHES[branch_idx],
        "animal": BRANCH_ANIMALS[branch_idx],
        "branch_element": BRANCH_ELEMENTS[branch_idx],
    }


def get_year_pillar(year: int) -> dict:
    index = (year - 4) % 60
    pillar = _jiazi(index)
    return {"pillar": "Year", **pillar, "year": year}


def _chinese_month_index(year: int, month: int, day: int) -> int:
    """Return 0-based Chinese month index (0 = Tiger/Yin month)."""
    for i in range(11, -1, -1):
        gm, gd = SOLAR_TERM_STARTS[i]
        # Month 12 (Chǒu) starts in January of the same year
        check_year = year if i != 11 else year
        if i == 11:
            # Chǒu month starts in January
            if month > 1 or (month == 1 and day >= gd):
                return i
        else:
            if (month > gm) or (month == gm and day >= gd):
                return i
    # Before Jan 6: still in Chǒu of previous year — treat as month index 11
    return 11


def get_month_pillar(year: int, month: int, day: int) -> dict:
    chinese_month_idx = _chinese_month_index(year, month, day)
    branch_idx = MONTH_BRANCHES[chinese_month_idx]
    # Month stem depends on year stem: year_stem_idx % 5 determines month stem base
    year_stem_idx = (year - 4) % 10
    # Month stem base: Tiger month stem = (year_stem_idx % 5) * 2
    month_stem_base = (year_stem_idx % 5) * 2
    stem_idx = (month_stem_base + chinese_month_idx) % 10
    pillar = {
        "stem": HEAVENLY_STEMS[stem_idx],
        "stem_element": STEM_ELEMENTS[stem_idx],
        "branch": EARTHLY_BRANCHES[branch_idx],
        "animal": BRANCH_ANIMALS[branch_idx],
        "branch_element": BRANCH_ELEMENTS[branch_idx],
    }
    return {"pillar": "Month", **pillar}


def get_day_pillar(year: int, month: int, day: int) -> dict:
    ref = date(2000, 1, 1)  # Jiǎzǐ day — index 0
    target = date(year, month, day)
    delta = (target - ref).days
    index = delta % 60
    pillar = _jiazi(index)
    return {"pillar": "Day", **pillar}


def get_hour_pillar(year: int, month: int, day: int, hour: int) -> dict:
    day_pillar = get_day_pillar(year, month, day)
    day_stem_idx = HEAVENLY_STEMS.index(day_pillar["stem"])
    branch_idx = _hour_branch_index(hour)
    # Hour stem: derived from day stem. Even-indexed day stems → base 0, odd → base 5
    hour_stem_base = (day_stem_idx % 5) * 2
    stem_idx = (hour_stem_base + branch_idx) % 10
    pillar = {
        "stem": HEAVENLY_STEMS[stem_idx],
        "stem_element": STEM_ELEMENTS[stem_idx],
        "branch": EARTHLY_BRANCHES[branch_idx],
        "animal": BRANCH_ANIMALS[branch_idx],
        "branch_element": BRANCH_ELEMENTS[branch_idx],
    }
    return {"pillar": "Hour", **pillar}


def get_bazi_chart(year: int, month: int, day: int, hour: int) -> dict:
    year_pillar = get_year_pillar(year)
    month_pillar = get_month_pillar(year, month, day)
    day_pillar = get_day_pillar(year, month, day)
    hour_pillar = get_hour_pillar(year, month, day, hour)

    return {
        "system": "Chinese BaZi (Four Pillars of Destiny)",
        "year_pillar": year_pillar,
        "month_pillar": month_pillar,
        "day_pillar": day_pillar,
        "hour_pillar": hour_pillar,
        "day_master": {
            "stem": day_pillar["stem"],
            "element": day_pillar["stem_element"],
        },
    }


def format_for_prompt(chart: dict) -> str:
    def fmt(p: dict) -> str:
        return (
            f"{p['stem']} ({p['stem_element']}) / {p['branch']} ({p['animal']}, {p['branch_element']})"
        )

    lines = [
        f"Day Master: {chart['day_master']['stem']} — {chart['day_master']['element']}",
        f"Year Pillar:  {fmt(chart['year_pillar'])}",
        f"Month Pillar: {fmt(chart['month_pillar'])}",
        f"Day Pillar:   {fmt(chart['day_pillar'])}",
        f"Hour Pillar:  {fmt(chart['hour_pillar'])}",
    ]
    return "\n".join(lines)
