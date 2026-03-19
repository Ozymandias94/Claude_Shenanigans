"""Horoscope API router."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, HTTPException

from app import cache
from app.ai import generator
from app.models.schemas import HoroscopeRequest, HoroscopeResponse, SystemInfo, SystemReading
from app.systems import chinese, egyptian, vedic, western

router = APIRouter(prefix="/horoscope", tags=["horoscope"])

SYSTEM_INFO = [
    SystemInfo(
        id="western",
        name="Western Astrology",
        description="Tropical zodiac natal chart using Swiss Ephemeris. Includes Sun, Moon, Ascendant, and seven classical + three modern planets.",
        requires_time=True,
        requires_location=True,
    ),
    SystemInfo(
        id="vedic",
        name="Vedic Astrology (Jyotish)",
        description="Sidereal zodiac with Lahiri ayanamsha and Whole Sign houses. Includes Nakshatra placement of the Moon.",
        requires_time=True,
        requires_location=True,
    ),
    SystemInfo(
        id="chinese",
        name="Chinese BaZi",
        description="Four Pillars of Destiny using the 60-Jiazi sexagenary cycle of Heavenly Stems and Earthly Branches.",
        requires_time=True,
        requires_location=False,
    ),
    SystemInfo(
        id="egyptian",
        name="Egyptian Astrology",
        description="Ancient Egyptian zodiac based on birth date correspondence to deities, derived from Dendera temple sources and surviving literature.",
        requires_time=False,
        requires_location=False,
    ),
]


@router.get("/systems", response_model=list[SystemInfo])
def list_systems():
    return SYSTEM_INFO


@router.post("/daily", response_model=HoroscopeResponse)
def daily_horoscope(req: HoroscopeRequest):
    try:
        birth = date.fromisoformat(req.birth_date)
    except ValueError:
        raise HTTPException(status_code=422, detail="birth_date must be YYYY-MM-DD")

    try:
        t_parts = req.birth_time.split(":")
        birth_hour, birth_minute = int(t_parts[0]), int(t_parts[1])
    except (ValueError, IndexError):
        raise HTTPException(status_code=422, detail="birth_time must be HH:MM")

    today = date.today()
    readings: dict[str, SystemReading] = {}

    for system in req.systems:
        cache_key = cache.make_key(system, req.name, req.birth_date, req.birth_time)
        cached = cache.get(cache_key)
        if cached:
            # We still need chart_data for the response — recompute (cheap)
            chart_data = _compute_chart(
                system, req, birth, birth_hour, birth_minute
            )
            readings[system] = SystemReading(chart_data=chart_data, daily_reading=cached)
            continue

        chart_data = _compute_chart(system, req, birth, birth_hour, birth_minute)
        reading_text = generator.generate_daily_reading(system, chart_data, req.name, today)
        cache.set(cache_key, reading_text)
        readings[system] = SystemReading(chart_data=chart_data, daily_reading=reading_text)

    return HoroscopeResponse(
        date=today.isoformat(),
        name=req.name,
        readings=readings,
    )


def _compute_chart(system: str, req: HoroscopeRequest, birth: date, hour: int, minute: int) -> dict:
    if system == "western":
        return western.get_western_chart(
            name=req.name,
            year=birth.year, month=birth.month, day=birth.day,
            hour=hour, minute=minute,
            lat=req.birth_lat, lng=req.birth_lng,
            tz_str=req.birth_tz,
        )
    elif system == "vedic":
        return vedic.get_vedic_chart(
            name=req.name,
            year=birth.year, month=birth.month, day=birth.day,
            hour=hour, minute=minute,
            lat=req.birth_lat, lng=req.birth_lng,
            tz_str=req.birth_tz,
        )
    elif system == "chinese":
        return chinese.get_bazi_chart(
            year=birth.year, month=birth.month, day=birth.day, hour=hour
        )
    elif system == "egyptian":
        return egyptian.get_egyptian_sign(month=birth.month, day=birth.day)
    else:
        raise HTTPException(status_code=422, detail=f"Unknown system: {system}")
