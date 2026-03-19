"""Claude-powered daily horoscope reading generator."""

from __future__ import annotations

import os
from datetime import date

import anthropic

from app.systems import western, vedic, chinese, egyptian

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 512

# Universal instructions that apply to every system.
# Edit this to change behavior shared across all four traditions.
BASE_SYSTEM_PROMPT = (
    "You are a masterful astrologer fluent in multiple ancient and modern traditions. "
    "Generate a personalized daily horoscope reading for the user based on their natal "
    "chart data and today's date. The reading must be:\n"
    "- Personalized: reference their specific signs, planets, or pillars\n"
    "- Forward-looking: speak to what today holds for them\n"
    "- Written in second person (you / your)\n"
    "- Thoughtful, poetic, and concrete in its guidance\n"
    "Do not include disclaimers about astrology being for entertainment."
)

# Maps system key → module. Each module exposes SYSTEM_CONFIG and format_for_prompt().
_SYSTEM_MODULES = {
    "western": western,
    "vedic": vedic,
    "chinese": chinese,
    "egyptian": egyptian,
}

_SYSTEM_NAMES = {
    "western": "Western Tropical Astrology",
    "vedic": "Vedic Jyotish Astrology",
    "chinese": "Chinese BaZi (Four Pillars of Destiny)",
    "egyptian": "Ancient Egyptian Astrology",
}


def generate_daily_reading(
    system: str,
    chart_data: dict,
    person_name: str,
    today: date,
) -> str:
    """Call Claude to generate a daily reading for the given system and chart.

    Standard prompt structure (western / vedic / chinese):
      system prompt  = BASE_SYSTEM_PROMPT + module.SYSTEM_CONFIG["system_prompt"]
      user prompt    = date + chart text + SYSTEM_CONFIG["reading_focus"]
                       + SYSTEM_CONFIG["presentation"]

    Full-engine prompt structure (egyptian):
      When SYSTEM_CONFIG contains "full_system_prompt" (a file path), the file
      is loaded and used as the entire system prompt, replacing BASE_SYSTEM_PROMPT
      and the system_prompt/reading_focus/presentation pattern. The user message
      is a structured reading request matching the engine's Section 12.4 format,
      populated from whatever chart data is currently available.

    To tune a system's reading behavior, edit SYSTEM_CONFIG in the relevant
    app/systems/*.py module — no changes needed here.
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    module = _SYSTEM_MODULES[system]
    config = module.SYSTEM_CONFIG
    max_tokens = config.get("max_tokens", MAX_TOKENS)

    engine_path = config.get("full_system_prompt")
    if engine_path:
        with open(engine_path, "r", encoding="utf-8") as fh:
            system_prompt = fh.read()

        chart_text = module.format_for_prompt(chart_data)
        user_prompt = (
            f"READING_TYPE: DAILY\n"
            f"PERSON_NAME: {person_name}\n"
            f"TODAY_DATE: {today.isoformat()}\n\n"
            f"NATAL_CHART_SUMMARY:\n{chart_text}\n\n"
            f"NOTE: Full ephemeris decan calculations are not yet available. "
            f"Generate a DAILY reading using the natal chart summary above. "
            f"Apply the voice and tone rules from Section 2, draw on the deity "
            f"library from Section 3, reference the active season from Section 4, "
            f"and follow the daily reading structure from Section 8.4."
        )
    else:
        system_prompt = BASE_SYSTEM_PROMPT + "\n\n" + config["system_prompt"]
        chart_text = module.format_for_prompt(chart_data)
        system_name = _SYSTEM_NAMES[system]
        user_prompt = (
            f"Today is {today.strftime('%A, %B %d, %Y')}.\n\n"
            f"Generate a {system_name} daily horoscope reading for {person_name}.\n\n"
            f"Their natal chart:\n{chart_text}\n\n"
            f"Reading focus:\n{config['reading_focus']}\n\n"
            f"Presentation:\n{config['presentation']}"
        )

    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text
