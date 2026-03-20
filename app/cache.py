"""Simple in-memory daily cache for horoscope readings.

Cache keys include today's date, so entries automatically become stale
the next day and are pruned on the next write.
"""

from __future__ import annotations

from datetime import date

_store: dict[tuple, object] = {}


def _today() -> str:
    return date.today().isoformat()


def make_key(*args) -> tuple:
    """Build a cache key from any number of string components plus today's date."""
    return (_today(), *args)


def get(key: tuple) -> object | None:
    return _store.get(key)


def set(key: tuple, value: object) -> None:
    today = _today()
    stale = [k for k in _store if k[0] != today]
    for k in stale:
        del _store[k]
    _store[key] = value
