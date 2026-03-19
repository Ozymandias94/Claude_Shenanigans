"""Egyptian zodiac system.

Based on the ancient Egyptian calendar and surviving astrological literature,
including the Dendera zodiac and decan system. The 12 signs below follow the
widely-cited correspondence of deities to birth date ranges derived from
ancient Egyptian temple sources and scholarly reconstructions.

The full reading engine (voice rules, deity library, decan library, transit
logic, and implementation instructions) lives in egyptian_astrology_engine.md
in this directory. generator.py loads that file as the complete system prompt
when it is present, replacing the BASE_SYSTEM_PROMPT + system_prompt pattern
used by the other three systems.
"""

from __future__ import annotations

import os

# Path to the engine instruction file relative to this module's directory.
_ENGINE_PATH = os.path.join(os.path.dirname(__file__), "egyptian_astrology_engine.md")

# Tunable configuration for this system's AI readings.
# full_system_prompt: path to the engine file — when present, generator.py
# loads it and uses it as the entire system prompt, bypassing BASE_SYSTEM_PROMPT
# and the system_prompt/reading_focus/presentation pattern.
SYSTEM_CONFIG = {
    "full_system_prompt": _ENGINE_PATH,
    # max_tokens override — engine readings are longer than the default 512.
    "max_tokens": 1024,
}

# Each sign has multiple non-contiguous date ranges (month, day).
# Ranges are inclusive: [start, end].
EGYPTIAN_SIGNS = [
    {
        "name": "The Nile",
        "deity": "Hapi",
        "sacred_animal": "Ibis",
        "element": "Water",
        "quality": "Adaptable and life-giving",
        "traits": ["intuitive", "generous", "unpredictable", "deeply connected to nature"],
        "ranges": [((1, 1), (1, 7)), ((6, 19), (6, 28)), ((9, 1), (9, 7)), ((11, 18), (11, 26))],
    },
    {
        "name": "Amon-Ra",
        "deity": "Amon-Ra",
        "sacred_animal": "Ram",
        "element": "Fire",
        "quality": "Sovereign and radiant",
        "traits": ["optimistic", "leadership", "creative", "powerful"],
        "ranges": [((1, 8), (1, 21)), ((2, 1), (2, 11))],
    },
    {
        "name": "Mut",
        "deity": "Mut",
        "sacred_animal": "Vulture",
        "element": "Earth",
        "quality": "Nurturing and protective",
        "traits": ["practical", "devoted", "strong-willed", "maternal"],
        "ranges": [((1, 22), (1, 31)), ((9, 8), (9, 22))],
    },
    {
        "name": "Geb",
        "deity": "Geb",
        "sacred_animal": "Goose",
        "element": "Earth",
        "quality": "Grounded and enduring",
        "traits": ["reliable", "humorous", "connected to ancestry", "sensory"],
        "ranges": [((2, 12), (2, 29)), ((8, 20), (8, 31))],
    },
    {
        "name": "Osiris",
        "deity": "Osiris",
        "sacred_animal": "Bull",
        "element": "Water",
        "quality": "Transformative and just",
        "traits": ["dual-natured", "vulnerable yet strong", "idealistic", "seeking truth"],
        "ranges": [((3, 1), (3, 10)), ((11, 27), (12, 18))],
    },
    {
        "name": "Isis",
        "deity": "Isis",
        "sacred_animal": "Cobra",
        "element": "Water",
        "quality": "Magical and devoted",
        "traits": ["perceptive", "industrious", "protective", "deeply loving"],
        "ranges": [((3, 11), (3, 31)), ((10, 18), (10, 29)), ((12, 19), (12, 31))],
    },
    {
        "name": "Thoth",
        "deity": "Thoth",
        "sacred_animal": "Ibis / Baboon",
        "element": "Air",
        "quality": "Intellectual and cosmic",
        "traits": ["highly intelligent", "innovative", "seeks knowledge", "communicative"],
        "ranges": [((4, 1), (4, 19)), ((11, 8), (11, 17))],
    },
    {
        "name": "Horus",
        "deity": "Horus",
        "sacred_animal": "Falcon",
        "element": "Fire",
        "quality": "Courageous and sky-born",
        "traits": ["courageous", "motivated", "regal", "protective of others"],
        "ranges": [((4, 20), (5, 7)), ((8, 12), (8, 19))],
    },
    {
        "name": "Anubis",
        "deity": "Anubis",
        "sacred_animal": "Jackal",
        "element": "Earth",
        "quality": "Guardian and guide",
        "traits": ["empathetic", "introverted", "highly perceptive", "guardian of transitions"],
        "ranges": [((5, 8), (5, 27)), ((6, 29), (7, 13))],
    },
    {
        "name": "Seth",
        "deity": "Seth",
        "sacred_animal": "Sha (Set animal)",
        "element": "Fire",
        "quality": "Fierce and transformative",
        "traits": ["energetic", "seeks excitement", "perfectionist", "strong-willed"],
        "ranges": [((5, 28), (6, 18)), ((9, 28), (10, 2))],
    },
    {
        "name": "Bastet",
        "deity": "Bastet",
        "sacred_animal": "Cat",
        "element": "Fire",
        "quality": "Joyful and protective",
        "traits": ["charming", "intuitive", "fiercely protective", "independent"],
        "ranges": [((7, 14), (7, 28)), ((9, 23), (9, 27)), ((10, 3), (10, 17))],
    },
    {
        "name": "Sekhmet",
        "deity": "Sekhmet",
        "sacred_animal": "Lioness",
        "element": "Fire",
        "quality": "Powerful and healing",
        "traits": ["authoritative", "honest", "perfectionist", "healing force"],
        "ranges": [((7, 29), (8, 11)), ((10, 30), (11, 7))],
    },
]


def _in_range(month: int, day: int, start: tuple, end: tuple) -> bool:
    sm, sd = start
    em, ed = end
    birth = (month, day)
    return (sm, sd) <= birth <= (em, ed)


def get_egyptian_sign(month: int, day: int) -> dict:
    """Return the Egyptian zodiac sign for a given birth month and day."""
    for sign in EGYPTIAN_SIGNS:
        for start, end in sign["ranges"]:
            if _in_range(month, day, start, end):
                return {
                    "system": "Egyptian Zodiac",
                    "sign": sign["name"],
                    "deity": sign["deity"],
                    "sacred_animal": sign["sacred_animal"],
                    "element": sign["element"],
                    "quality": sign["quality"],
                    "traits": sign["traits"],
                }
    # Fallback: shouldn't happen with complete date coverage
    return {
        "system": "Egyptian Zodiac",
        "sign": "Unknown",
        "deity": "Unknown",
        "sacred_animal": "Unknown",
        "element": "Unknown",
        "quality": "Unknown",
        "traits": [],
    }


def format_for_prompt(chart: dict) -> str:
    traits = ", ".join(chart["traits"])
    return (
        f"Sign: {chart['sign']} (governed by {chart['deity']})\n"
        f"Sacred Animal: {chart['sacred_animal']}\n"
        f"Element: {chart['element']} — {chart['quality']}\n"
        f"Core Traits: {traits}"
    )
