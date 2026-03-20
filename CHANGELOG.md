# CHANGELOG.md
## Egyptian Astrology App — Session Log

Newest entries at the top. One entry per session in which code was written
or changed. This file is the only memory between sessions — maintain it
carefully.

---

## [2026-03-19] — Project initialization

### Built or changed
- Created project file structure
- Wrote CLAUDE.md (session orientation and locked rules)
- Wrote docs/engine.md (reading engine v1.3 — dual-purpose: project
  documentation and Anthropic API system prompt)
- Wrote docs/features.md (full feature plan, Launch through V3)
- Wrote docs/design.md (color schemes, typography, layout, motion)

### Files created or modified
- CLAUDE.md — created
- CHANGELOG.md — created
- docs/engine.md — created (engine v1.3, 13 sections)
- docs/features.md — created (22 features across 4 release versions)
- docs/design.md — created (4 color schemes, typography, layout, sky map,
  animation, anti-patterns)

### Feature plan items advanced
- None — this session was project setup only. No application code written.

### Decisions made not covered by the spec
- docs/ directory chosen over flat file structure to keep CLAUDE.md concise
  and allow situational reading of supporting files
- engine.md marked as DUAL PURPOSE at top of file — serves as both project
  documentation and the literal system prompt passed to the Anthropic API
  on every reading generation call. This distinction must be preserved.

### Left open for next session
- No application code exists yet. Start with the calculation layer:
  Swiss Ephemeris integration and the natal chart generation pipeline.
  Feature #3 (Natal Birth Reading) is the correct first build target —
  everything else depends on having natal data.
- Recommended first session scope: ephemeris setup → birth data input →
  position calculation → decan lookup → natal field caching (engine
  Section 12.5). Do not start the AI reading call until the calculation
  layer is verified accurate.

### Engine sections referenced
- Section 12 (Implementation instructions) — reviewed for project setup
- Section 12.2 (Ephemeris and calculation stack) — Swiss Ephemeris confirmed
- Section 12.5 (Natal chart caching) — field list confirmed for first build

---
