"""Claude-powered Egyptian astrology reading generator.

Phase 2 note: Once app/systems/decan_library.py and app/prompt_builder.py are
in place, _build_user_prompt() will be replaced by prompt_builder functions for
token-optimised decan injection (75-80% token reduction vs. the full engine file).
"""

from __future__ import annotations

import os
from datetime import date

import anthropic

from app.systems.egyptian import SYSTEM_CONFIG

DAILY_MODEL = "claude-sonnet-4-6"
PUSH_MODEL = "claude-haiku-4-5-20251001"

_MAX_TOKENS: dict[str, int] = {"push": 50, "daily": 400, "natal": 900}


def generate_reading(
    reading_type: str,
    natal_chart: dict,
    transits: dict,
    person_name: str,
    birth_date: str,
    birth_time: str,
    birth_location: str,
    today: date,
) -> str:
    """Call Claude to generate an Egyptian astrology reading.

    reading_type must be one of: "daily", "natal", "push"

    The full engine MD is used as the system prompt for now. Phase 2 will
    replace this with app/prompt_builder.py for a slimmed core prompt + dynamic
    decan injection, dropping token usage by ~75-80%.
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    engine_path = SYSTEM_CONFIG["full_system_prompt"]
    with open(engine_path, "r", encoding="utf-8") as fh:
        system_prompt = fh.read()

    model = PUSH_MODEL if reading_type == "push" else DAILY_MODEL
    max_tokens = _MAX_TOKENS.get(reading_type, 400)

    user_prompt = _build_user_prompt(
        reading_type, natal_chart, transits,
        person_name, birth_date, birth_time,
        birth_location, today,
    )

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text


def _build_user_prompt(
    reading_type: str,
    natal_chart: dict,
    transits: dict,
    person_name: str,
    birth_date: str,
    birth_time: str,
    birth_location: str,
    today: date,
) -> str:
    """Assemble a structured reading request per engine Section 12.4."""
    rt = reading_type.upper()

    asc_decan = natal_chart.get("asc_decan", "unknown")
    sun_decan = natal_chart.get("sun_decan", "unknown")
    moon_decan = natal_chart.get("moon_decan", "unknown")
    season = natal_chart.get("season", "unknown")
    lot_f_h = natal_chart.get("lot_fortune_house")
    lot_d_h = natal_chart.get("lot_daimon_house")

    retrogrades = ", ".join(transits.get("active_retrogrades") or []) or "none"
    stations = transits.get("today_stations") or []
    eclipse = transits.get("today_eclipse", "NONE")
    sun_decan_t = transits.get("today_sun_decan", "unknown")
    hem_event = transits.get("hemerological_event")
    khoiak = transits.get("khoiak_active", False)

    lines = [
        f"READING_TYPE: {rt}",
        f"PERSON_NAME: {person_name}",
        f"TODAY_DATE: {today.isoformat()}",
        f"BIRTH_DATE: {birth_date}",
        f"BIRTH_TIME: {birth_time or 'unknown'}",
        f"BIRTH_LOCATION: {birth_location}",
        "",
        "NATAL_CHART_SUMMARY:",
        f"  Egyptian Season: {season}",
        f"  Ascendant Decan: {asc_decan}",
        f"  Sun Decan: {sun_decan}",
        f"  Moon Decan: {moon_decan}",
    ]
    if lot_f_h:
        lines.append(f"  Lot of Fortune: House {lot_f_h}")
    if lot_d_h:
        lines.append(f"  Lot of Daimon: House {lot_d_h}")

    lines += [
        "",
        "TODAY_TRANSIT_CONTEXT:",
        f"  Transiting Sun Decan: {sun_decan_t}",
        f"  Active Retrogrades: {retrogrades}",
        f"  Eclipse Today: {eclipse}",
    ]
    for s in stations:
        lines.append(f"  Station: {s['planet']} {s['type']}")
    if hem_event:
        lines.append(
            f"  Hemerological Event: {hem_event.get('name', '')} "
            f"({hem_event.get('charge', '')})"
        )
    if khoiak:
        lines.append("  Khoiak Mysteries: ACTIVE")

    return "\n".join(lines)
