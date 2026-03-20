"""Egyptian Astrology API router."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, HTTPException

from app import cache
from app.ai import generator
from app.models.schemas import ReadingRequest, ReadingResponse
from app.systems import egyptian_chart, egyptian_transits
from app.systems.egyptian import get_egyptian_sign

router = APIRouter(prefix="", tags=["reading"])


@router.post("/reading", response_model=ReadingResponse)
def get_reading(req: ReadingRequest):
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

    # --- Natal chart (cached per user identity) ---
    natal_key = cache.make_key("natal", req.name, req.birth_date, req.birth_time)
    natal_chart = cache.get(natal_key)
    if natal_chart is None:
        natal_chart = egyptian_chart.calculate_natal_chart(
            birth_date=birth,
            birth_hour=birth_hour,
            birth_minute=birth_minute,
            lat=req.birth_lat,
            lng=req.birth_lng,
            tz_str=req.birth_tz,
        )
        cache.set(natal_key, natal_chart)

    # Sign data (for response summary)
    sign_data = get_egyptian_sign(month=birth.month, day=birth.day)

    # --- Daily transits (cached per date, shared across all users) ---
    transit_key = cache.make_key("transits", today.isoformat())
    transits = cache.get(transit_key)
    if transits is None:
        transits = egyptian_transits.calculate_daily_transits(
            today=today,
            natal_saturn_deg=natal_chart.get("saturn_degree"),
            natal_jupiter_deg=natal_chart.get("jupiter_degree"),
        )
        cache.set(transit_key, transits)

    # --- PUSH: may be pre-resolved (no Claude call) ---
    if req.reading_type == "push":
        push_text = _resolve_push(transits, transits.get("today_sun_decan", 1))
        if push_text:
            return ReadingResponse(
                reading_type="push",
                text=push_text,
                date=today.isoformat(),
                natal_summary=_natal_summary(sign_data, natal_chart),
            )

    # --- Reading cache (per user + reading_type + date) ---
    reading_key = cache.make_key(req.reading_type, req.name, req.birth_date, today.isoformat())
    cached_text = cache.get(reading_key)
    if cached_text:
        return ReadingResponse(
            reading_type=req.reading_type,
            text=cached_text,
            date=today.isoformat(),
            natal_summary=_natal_summary(sign_data, natal_chart),
        )

    # --- Generate via Claude ---
    text = generator.generate_reading(
        reading_type=req.reading_type,
        natal_chart=natal_chart,
        transits=transits,
        person_name=req.name,
        birth_date=req.birth_date,
        birth_time=req.birth_time,
        birth_location=req.birth_location_name or f"{req.birth_lat},{req.birth_lng}",
        today=today,
    )
    cache.set(reading_key, text)

    return ReadingResponse(
        reading_type=req.reading_type,
        text=text,
        date=today.isoformat(),
        natal_summary=_natal_summary(sign_data, natal_chart),
    )


def _resolve_push(transits: dict, sun_decan: int) -> str | None:
    """Return a pre-written push string if a high-priority event is active.
    Returns None if Claude should generate the push line instead.
    Priority order per engine Section 12.7:
      1. Oct 7 (Death of Osiris) → hemerological push
      2. Jul 20 (Set's Birthday) → hemerological push
      3. Jul 23 (Sothis) → hemerological push
      4. Eclipse → let Claude generate
      5. Exact station → let Claude generate
      6. Hemerological event → hemerological push
      7. Active retrograde → let Claude generate
      8. Default → let Claude generate (daily Sun decan push)
    """
    from app.systems.hemerological_calendar import HEMEROLOGICAL_CALENDAR
    from datetime import date as _date

    today = _date.today()
    hem_entry = HEMEROLOGICAL_CALENDAR.get((today.month, today.day))

    # Rules 1–2: These two override everything
    if (today.month, today.day) in {(10, 7), (7, 20)}:
        if hem_entry and hem_entry.get("push"):
            return hem_entry["push"]

    # Rule 3: Sothis
    if transits.get("sothis_active") and hem_entry and hem_entry.get("push"):
        return hem_entry["push"]

    # Rules 4–5: Eclipse / station → Claude handles
    if transits.get("today_eclipse") != "NONE":
        return None
    if transits.get("today_stations"):
        return None

    # Rule 6: Other hemerological events
    if hem_entry and hem_entry.get("push"):
        return hem_entry["push"]

    # Rules 7–8: Let Claude generate
    return None


def _natal_summary(sign_data: dict, natal_chart: dict):
    from app.models.schemas import NatalSummary
    return NatalSummary(
        sign=sign_data["sign"],
        deity=sign_data["deity"],
        season=natal_chart.get("season", "SHEMU"),
        asc_decan=natal_chart.get("asc_decan"),
        sun_decan=natal_chart.get("sun_decan", 1),
        moon_decan=natal_chart.get("moon_decan", 1),
        lot_fortune_house=natal_chart.get("lot_fortune_house"),
        lot_fortune_decan=natal_chart.get("lot_fortune_decan"),
        lot_daimon_house=natal_chart.get("lot_daimon_house"),
        lot_daimon_decan=natal_chart.get("lot_daimon_decan"),
    )
