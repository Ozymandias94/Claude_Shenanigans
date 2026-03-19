from __future__ import annotations

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, Field

SystemName = Literal["western", "vedic", "chinese", "egyptian"]


class HoroscopeRequest(BaseModel):
    name: str = Field(..., description="Person's name")
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    birth_time: str = Field("12:00", description="Birth time in HH:MM (24h), defaults to noon")
    birth_lat: float = Field(..., description="Birth latitude in decimal degrees")
    birth_lng: float = Field(..., description="Birth longitude in decimal degrees")
    birth_tz: str = Field(..., description="IANA timezone string, e.g. 'America/New_York'")
    systems: list[SystemName] = Field(
        default=["western", "vedic", "chinese", "egyptian"],
        description="Which astrological systems to include",
    )


class SystemReading(BaseModel):
    chart_data: dict[str, Any]
    daily_reading: str


class HoroscopeResponse(BaseModel):
    date: str
    name: str
    readings: dict[str, SystemReading]


class SystemInfo(BaseModel):
    id: str
    name: str
    description: str
    requires_time: bool
    requires_location: bool
