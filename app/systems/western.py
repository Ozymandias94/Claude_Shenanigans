"""Western tropical natal chart calculations using kerykeion."""

from __future__ import annotations

# Tunable configuration for this system's AI readings.
# Edit these strings to refine how Claude generates Western horoscopes
# without touching any calculation or API logic.
SYSTEM_CONFIG = {
    # Appended to the base system prompt — change Claude's interpretive lens.
    "system_prompt": (
        "You are interpreting a Western tropical natal chart. "
        "Work within the Western astrological tradition: tropical zodiac, Placidus houses, "
        "classical and modern planetary rulerships, and aspect theory. "
        "Ground the reading in the interplay of Sun, Moon, and Ascendant as the core identity "
        "triad, and weave in the personal planets (Mercury, Venus, Mars) as secondary color."
    ),
    # Injected into the user prompt — tells Claude which chart factors to foreground.
    "reading_focus": (
        "Lead with the Sun sign's core drive, then layer in the Moon sign's emotional tone "
        "and the Ascendant's outward style. Reference at least one personal planet placement "
        "(Mercury, Venus, or Mars) that colors today's energy specifically. "
        "Avoid listing every planet — synthesize rather than catalogue."
    ),
    # Tells Claude how to structure and style the output.
    "presentation": (
        "150–200 words. Second person throughout. "
        "Three loose beats: (1) today's overarching tone, "
        "(2) a specific opportunity or challenge to navigate, "
        "(3) a closing reflection or practical suggestion. "
        "Poetic but not flowery — grounded psychological language preferred."
    ),
}


def get_western_chart(
    name: str,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    lat: float,
    lng: float,
    tz_str: str,
) -> dict:
    from kerykeion import AstrologicalSubjectFactory

    subject = AstrologicalSubjectFactory.from_birth_data(
        name=name,
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        lat=lat,
        lng=lng,
        tz_str=tz_str,
        online=False,
    )

    def planet(p) -> dict:
        return {"sign": p.sign, "degree": round(p.abs_pos, 2)}

    return {
        "system": "Western (Tropical)",
        "sun": planet(subject.sun),
        "moon": planet(subject.moon),
        "ascendant": planet(subject.ascendant),
        "mercury": planet(subject.mercury),
        "venus": planet(subject.venus),
        "mars": planet(subject.mars),
        "jupiter": planet(subject.jupiter),
        "saturn": planet(subject.saturn),
        "uranus": planet(subject.uranus),
        "neptune": planet(subject.neptune),
        "pluto": planet(subject.pluto),
    }


def format_for_prompt(chart: dict) -> str:
    lines = [
        f"Sun in {chart['sun']['sign']} ({chart['sun']['degree']}°)",
        f"Moon in {chart['moon']['sign']} ({chart['moon']['degree']}°)",
        f"Ascendant in {chart['ascendant']['sign']}",
        f"Mercury in {chart['mercury']['sign']}",
        f"Venus in {chart['venus']['sign']}",
        f"Mars in {chart['mars']['sign']}",
        f"Jupiter in {chart['jupiter']['sign']}",
        f"Saturn in {chart['saturn']['sign']}",
        f"Uranus in {chart['uranus']['sign']}",
        f"Neptune in {chart['neptune']['sign']}",
        f"Pluto in {chart['pluto']['sign']}",
    ]
    return "\n".join(lines)
