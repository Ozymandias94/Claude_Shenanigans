from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ReadingRequest(BaseModel):
    name: str = Field(..., description="Person's name")
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    birth_time: str = Field("12:00", description="Birth time in HH:MM (24h), defaults to noon")
    birth_lat: float = Field(..., description="Birth latitude in decimal degrees")
    birth_lng: float = Field(..., description="Birth longitude in decimal degrees")
    birth_tz: str = Field(..., description="IANA timezone string, e.g. 'Africa/Cairo'")
    birth_location_name: str | None = Field(None, description="Display name for birth location")
    reading_type: Literal["daily", "natal", "push"] = Field(
        "daily", description="Type of reading to generate"
    )


class NatalSummary(BaseModel):
    sign: str
    deity: str
    season: str  # AKHET | PERET | SHEMU
    asc_decan: int | None  # None if birth time unknown
    sun_decan: int
    moon_decan: int
    lot_fortune_house: int | None
    lot_fortune_decan: int | None
    lot_daimon_house: int | None
    lot_daimon_decan: int | None


class ReadingResponse(BaseModel):
    reading_type: str
    text: str
    date: str
    natal_summary: NatalSummary | None = None
