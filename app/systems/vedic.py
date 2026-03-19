"""Vedic (sidereal) natal chart calculations using kerykeion with Lahiri ayanamsha."""

from __future__ import annotations

# Tunable configuration for this system's AI readings.
# Edit these strings to refine how Claude generates Vedic horoscopes
# without touching any calculation or API logic.
SYSTEM_CONFIG = {
    # Appended to the base system prompt — change Claude's interpretive lens.
    "system_prompt": (
        "You are interpreting a Vedic (Jyotish) natal chart calculated with the Lahiri ayanamsha "
        "and Whole Sign houses. Work strictly within the Jyotish tradition: sidereal zodiac, "
        "Graha dignities (exaltation, debilitation, own sign), the nine Grahas (Sun through Saturn "
        "plus Rahu and Ketu), and the Nakshatra system of 27 lunar mansions. "
        "Reference Vedic concepts authentically — avoid blending Western astrological ideas."
    ),
    # Injected into the user prompt — tells Claude which chart factors to foreground.
    "reading_focus": (
        "Ground the reading in the Moon's Nakshatra first — its name, lord, and pada carry the "
        "most immediate daily significance. Then bring in the Lagna (Ascendant) as the lens through "
        "which all energy is filtered. Note any retrograde Grahas as areas requiring inward review. "
        "Reference the Moon Nakshatra lord's condition in the chart to add depth."
    ),
    # Tells Claude how to structure and style the output.
    "presentation": (
        "150–200 words. Second person throughout. "
        "Use Sanskrit terms naturally (Graha, Lagna, Nakshatra, Pada) but always make meaning "
        "clear from context — do not write as if the reader is an expert. "
        "Three beats: (1) Nakshatra quality coloring the day, "
        "(2) what the Lagna + key Graha positions invite or caution, "
        "(3) a closing practical suggestion aligned with Dharmic principles."
    ),
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury",
]


def _nakshatra(abs_pos: float) -> dict:
    """Map an absolute sidereal longitude (0–360) to a Nakshatra."""
    index = int(abs_pos / (360 / 27)) % 27
    pada = int((abs_pos % (360 / 27)) / (360 / 27 / 4)) + 1
    return {
        "name": NAKSHATRAS[index],
        "lord": NAKSHATRA_LORDS[index],
        "pada": pada,
    }


def get_vedic_chart(
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
        zodiac_type="Sidereal",
        sidereal_mode="LAHIRI",
        houses_system_identifier="W",  # Whole Sign — traditional Vedic
        online=False,
    )

    def planet(p) -> dict:
        return {
            "sign": p.sign,
            "degree": round(p.abs_pos, 2),
            "retrograde": getattr(p, "retrograde", False),
        }

    moon_nakshatra = _nakshatra(subject.moon.abs_pos)

    return {
        "system": "Vedic (Jyotish / Lahiri Sidereal)",
        "sun": planet(subject.sun),
        "moon": {**planet(subject.moon), "nakshatra": moon_nakshatra},
        "ascendant": planet(subject.ascendant),
        "mercury": planet(subject.mercury),
        "venus": planet(subject.venus),
        "mars": planet(subject.mars),
        "jupiter": planet(subject.jupiter),
        "saturn": planet(subject.saturn),
        "moon_nakshatra": moon_nakshatra,
    }


def format_for_prompt(chart: dict) -> str:
    nk = chart["moon_nakshatra"]
    lines = [
        f"Lagna (Ascendant) in {chart['ascendant']['sign']}",
        f"Sun in {chart['sun']['sign']} ({chart['sun']['degree']}°)",
        f"Moon in {chart['moon']['sign']} ({chart['moon']['degree']}°), Nakshatra: {nk['name']} (lord: {nk['lord']}, pada {nk['pada']})",
        f"Mercury in {chart['mercury']['sign']}" + (" (Retrograde)" if chart['mercury']['retrograde'] else ""),
        f"Venus in {chart['venus']['sign']}" + (" (Retrograde)" if chart['venus']['retrograde'] else ""),
        f"Mars in {chart['mars']['sign']}" + (" (Retrograde)" if chart['mars']['retrograde'] else ""),
        f"Jupiter in {chart['jupiter']['sign']}" + (" (Retrograde)" if chart['jupiter']['retrograde'] else ""),
        f"Saturn in {chart['saturn']['sign']}" + (" (Retrograde)" if chart['saturn']['retrograde'] else ""),
    ]
    return "\n".join(lines)
