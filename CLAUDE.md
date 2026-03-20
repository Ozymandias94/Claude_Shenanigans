# CLAUDE.md — Project Context for Claude Code Sessions

> **For every new session:** Read this file first. It tells you exactly where we are, what decisions have been made, and what to do next. Update the "Current Status" and "Next Steps" sections at the end of every session before committing.

---

## Project: Khemet — Egyptian Astrology Mobile App

### What This Is
A mobile app (React Native / Expo) backed by a FastAPI API, delivering personalized astrological readings grounded exclusively in ancient Egyptian cosmology. The reading engine is defined in `app/systems/egyptian_astrology_engine.md` — a complete ~2700-line specification that covers voice rules, the 36 decans, transit events, hemerological calendar, and reading format.

### What This Is NOT
- Not a multi-tradition astrology app. Western, Vedic, and Chinese systems have been removed.
- Not an entertainment gimmick. The readings follow the engine spec strictly (priestly voice, declarative tone, deities as active forces).

---

## Architecture Decisions (Already Made — Don't Revisit)

| Decision | What We Chose | Why |
|---|---|---|
| Mobile framework | React Native (Expo) | Cross-platform, JS ecosystem, OTA updates |
| Backend framework | FastAPI (Python) | Already in place, async-friendly |
| Ephemeris library | pyswisseph | Industry standard, degree-level accuracy |
| Model for PUSH readings | claude-haiku-4-5 | 12-word output, no need for Sonnet |
| Model for DAILY/NATAL | claude-sonnet-4-6 | Best quality for longer readings |
| Token optimization | Decan library as Python dict (NOT sent to Claude) | ~75-80% token reduction vs full engine MD |
| System prompt strategy | Slimmed core prompt (~400 lines) + dynamic decan injection | Only send relevant decans per reading |
| House system | Whole Sign exclusively | Per engine spec |
| Lots | Fortune & Daimon per Section 7 formulas | Day/night birth distinction |

---

## Repository Structure

```
Claude_Shenanigans/
├── CLAUDE.md                          ← You are here
├── main.py                            ← FastAPI app entry point
├── requirements.txt                   ← Python deps (pyswisseph, anthropic, fastapi, etc.)
├── .env.example                       ← Copy to .env, set ANTHROPIC_API_KEY
├── app/
│   ├── ai/
│   │   └── generator.py               ← Claude call logic, reading type routing
│   ├── models/
│   │   └── schemas.py                 ← Pydantic request/response models
│   ├── routers/
│   │   └── horoscope.py               ← FastAPI routes: /reading, /natal, /push
│   ├── systems/
│   │   ├── egyptian.py                ← Sign data + format_reading_request()
│   │   ├── egyptian_astrology_engine.md ← THE SPEC (read-only, do not modify)
│   │   ├── egyptian_chart.py          ← Natal chart calculator (Swiss Ephemeris)
│   │   ├── egyptian_transits.py       ← Daily transit detector
│   │   ├── decan_library.py           ← All 36 decans as Python dict (Section 5)
│   │   └── hemerological_calendar.py  ← Fixed sacred day lookup (Section 11.6.1)
│   ├── prompt_builder.py              ← Assembles slimmed system prompt + user prompt
│   └── cache.py                       ← In-memory daily cache (reuse as-is)
└── mobile/
    ├── app/                           ← Expo Router file-based routing
    │   ├── (tabs)/
    │   │   ├── index.tsx              ← Today's Reading screen
    │   │   ├── natal.tsx              ← Natal Chart screen
    │   │   └── settings.tsx           ← Profile/settings screen
    │   ├── onboarding.tsx             ← First-run birth data entry
    │   └── _layout.tsx                ← Root layout
    ├── components/
    │   ├── ReadingCard.tsx
    │   ├── DecanBadge.tsx
    │   └── SeasonBanner.tsx
    ├── services/
    │   └── api.ts                     ← Backend API client
    ├── store/
    │   └── profile.ts                 ← AsyncStorage birth profile persistence
    └── constants/
        └── theme.ts                   ← Egyptian palette: gold, papyrus, lapis
```

---

## Branch
**Always develop on:** `claude/review-project-status-tL8nV`

Never push to `master` or `main` without explicit permission.

---

## The Engine Spec (Critical Reading)

`app/systems/egyptian_astrology_engine.md` is the source of truth for all reading content. Key sections:

- **Section 2:** Voice & Tone (non-negotiable, priestly, declarative)
- **Section 3:** Planet → Deity mappings
- **Section 4:** Three Seasons (AKHET/PERET/SHEMU from Sun sign)
- **Section 5:** 36 Decans (extracted to `decan_library.py` — not sent raw to Claude)
- **Section 6:** 12 House names (Egyptian names)
- **Section 7:** Lot of Fortune & Daimon formulas
- **Section 8:** Reading structures (NATAL 400-600w, DAILY 180-250w, PUSH 12w max)
- **Section 11:** Transit events (retrogrades, eclipses, stations, hemerological calendar)
- **Section 12:** Implementation notes (for us, not for Claude)

---

## Token Optimization (Implemented)

**What gets sent to Claude per call:**
1. Slimmed system prompt: Sections 1, 2, 3, 4, 8, 10 only (~400 lines instead of 2700)
2. Only the 2–3 relevant decan entries (Asc + Sun + Moon decans, looked up from Python dict)
3. Only active transit context (retrograde block only if retrograde active, etc.)

**What is pre-resolved in Python (no Claude):**
- Hemerological push lines → exact text from `hemerological_calendar.py`
- Khoiak standing layer → fixed string
- Decan lookups → Python dict in `decan_library.py`
- Season detection → pure Python

**Model selection:**
- PUSH → `claude-haiku-4-5-20251001`
- DAILY → `claude-sonnet-4-6`
- NATAL → `claude-sonnet-4-6`

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /health | Health check |
| POST | /reading | Daily reading (default), natal, or push based on `reading_type` |

**Request body (`ReadingRequest`):**
```json
{
  "name": "Nefertari",
  "birth_date": "1990-03-15",
  "birth_time": "14:30",
  "birth_lat": 30.0444,
  "birth_lng": 31.2357,
  "birth_tz": "Africa/Cairo",
  "birth_location_name": "Cairo, Egypt",
  "reading_type": "daily"
}
```

---

## Mobile App

- Framework: Expo (React Native, TypeScript)
- Location: `mobile/` inside this repo
- API base URL: set via `EXPO_PUBLIC_API_URL` env var
- Birth profile stored locally in AsyncStorage
- Geocoding: Nominatim (OpenStreetMap) for city → lat/lng

---

## Current Status

**Session that wrote this file:** Initial setup session
**Phase completed:** Planning
**What's done:**
- [x] Plan finalized and approved
- [x] Existing repo explored
- [ ] Backend cleanup (western/vedic/chinese removed)
- [ ] Egyptian calculation engine completed
- [ ] Mobile app initialized

**Next Steps (pick up here):**
1. Delete `app/systems/western.py`, `vedic.py`, `chinese.py`
2. Update `requirements.txt` (remove kerykeion, simple-ascii-tables)
3. Rewrite `app/models/schemas.py` with new Egyptian-only models
4. Rewrite `app/routers/horoscope.py` with new endpoints
5. Create `app/systems/decan_library.py` (extract from Section 5 of engine MD)
6. Create `app/systems/hemerological_calendar.py` (extract from Section 11.6.1)
7. Create `app/systems/egyptian_chart.py` (Swiss Ephemeris natal calc)
8. Create `app/systems/egyptian_transits.py` (daily transit detection)
9. Create `app/prompt_builder.py` (slimmed prompt assembly)
10. Rewrite `app/ai/generator.py` (reading type routing)
11. Update `app/systems/egyptian.py` (add `format_reading_request()`)
12. Initialize Expo app in `mobile/`
13. Build mobile screens + API client

---

## Known Gotchas

- `pyswisseph` requires the Swiss Ephemeris data files to be present. On first run, `swe.set_ephe_path()` should point to the ephe data directory. The library downloads them automatically if the path is writable.
- Birth time defaults to `"12:00"` if not provided. This disables Ascendant calculation — Sun + Moon decans + Season only in that case (per engine Section 10).
- The hemerological calendar has no leap year correction (per engine Section 12.3 rule 2 — 1-day drift is negligible for consumer app).
- July 20 and Oct 7 are the only two days where hemerological push overrides transit push (highest-charge inauspicious days).
- Khoiak period: Oct 21 fires the opening line. Oct 22–Nov 19 apply the standing layer.
- Whole Sign houses only. Placidus is not used anywhere.
