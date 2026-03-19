"""Simple in-memory daily cache for horoscope readings.

Cache keys include today's date, so entries automatically become stale
the next day and are pruned on the next write.
"""

from __future__ import annotations

from datetime import date

_store: dict[tuple, str] = {}


def _today() -> str:
    return date.today().isoformat()


def make_key(system: str, name: str, birth_date: str, birth_time: str) -> tuple:
    return (_today(), system, name, birth_date, birth_time)


def get(key: tuple) -> str | None:
    return _store.get(key)


def set(key: tuple, value: str) -> None:
    today = _today()
    stale = [k for k in _store if k[0] != today]
    for k in stale:
        del _store[k]
    _store[key] = value
