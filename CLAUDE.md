# CLAUDE.md
## Egyptian Astrology App — Session Orientation

---

## What This Is

A mobile astrology app grounded in ancient Egyptian cosmology. It generates
personalized readings using a decan-based system bridging Egyptian tradition
with Greco-Egyptian interpretive astrology. The reading engine runs on the
Anthropic API (claude-sonnet-4-6). The product differentiator is depth,
mythological accuracy, and a voice that no competitor has.

---

## File Map

Read this file every session. Read the others situationally.

```
CLAUDE.md              — This file. Session orientation. Always read.
CHANGELOG.md           — Session log. Read last 3 entries before writing code.
docs/engine.md         — The reading engine (v1.3). DUAL PURPOSE: project
                         documentation AND the Anthropic API system prompt.
                         Pass its full contents as system_prompt when calling
                         the API. Section 12 contains all implementation
                         instructions including ephemeris setup, calculation
                         requirements, request format, caching, and the full
                         daily reading decision tree as pseudocode.
docs/features.md       — Full feature plan organized by release version
                         (Launch / V1.5 / V2 / V3) with how-to-build notes
                         for each feature and cross-references to engine
                         sections.
docs/design.md         — All visual decisions: color schemes, typography,
                         layout, spacing, animation, the sky map structure,
                         and anti-patterns to avoid.
```

---

## Session Start Protocol

Do these in order before writing any code:

1. Read CHANGELOG.md — last 3 entries minimum. Understand current state.
2. Identify which feature(s) from docs/features.md you are working on.
3. Read the relevant section of docs/engine.md for that feature.
   Cross-references are embedded in each feature entry in docs/features.md.
4. Read the relevant section of docs/design.md before writing any UI code.
5. Check the Locked Rules section below before writing anything.

---

## End of Session Protocol (Required)

Add an entry to CHANGELOG.md before closing the session. If CHANGELOG.md
does not exist, create it. New entries go at the top.

Use this format exactly:

```
## [YYYY-MM-DD] — [Brief description of work done]

### Built or changed
- [Specific item]
- [Specific item]

### Files created or modified
- path/to/file — [what changed]

### Feature plan items advanced
- Feature #[N]: [Name] — [started / in progress / complete]

### Decisions made not covered by the spec
- [Any implementation choice the spec did not anticipate]
- [Any deviation from the spec and the reason]

### Left open for next session
- [Incomplete work or known issues]

### Engine sections referenced
- Section [N] — [why it was needed]
```

A session without a changelog entry is a session that will partially need
to be re-done. The changelog is the only memory between sessions.

---

## Locked Rules

These must never be changed without explicit human instruction. If a human
instructs a change to any of these, update this file before changing the code.

**Reading voice:**
The reading never hedges. Never uses "you may," "you might," or "it's
possible." The priestly voice decrees. See docs/engine.md Section 2.

**Four-register structure:**
Every reading has four registers in sequence: Mythological Decree →
Practical Mirror → Transformative Call → Witnessing Close. The witnessing
close is 2-4 sentences max, never resolves the reading, never names any
wisdom tradition or teacher. See docs/engine.md Section 2.8.

**Deity introduction:**
The reader knows nothing about Egyptian mythology. Every deity must arrive
already carrying their character — the name is a label for something the
reader already felt. Never name a deity and move on. See engine Section 2.9.

**Gold is divine, not decorative:**
Gold text and gold accents mean something carries divine authority — an
active decan name, a deity name in the reading body, a hemerological charge.
Everything else is sand, papyrus, or ochre. If you are unsure whether
something should be gold: it is not gold.

**Black Land scheme:**
The Black Land color scheme (dark red/black) activates ONLY on: July 20
(Birth of Set), October 7 (Death of Osiris), eclipse day readings, and
hemerological inauspicious days. It never appears on ordinary days.
Its power comes entirely from its rarity. See docs/design.md Scheme 3.

**Oracle Chamber:**
The Oracle Chamber returns exactly one response per session. No follow-up.
No conversation loop. The single-response constraint is intentional and
mythologically appropriate. It must not be circumvented.

**Whole Sign houses only:**
The house system is Whole Sign exclusively. The Ascendant sign is the full
1st house. Do not implement Placidus, Koch, or any other house system.

**Swiss Ephemeris:**
All planetary position calculations use the Swiss Ephemeris (swisseph npm
package or pyswisseph). Do not use approximation libraries. The decan system
requires degree-level accuracy — a 5° error puts the user in the wrong decan.

**Connect feature gate:**
Do not build the Connect dating feature (Feature #21) until user density
in target cities is confirmed by a human. An empty dating feature damages
retention. This is a scale requirement, not a technical one.

**No purple:**
Purple is not an Egyptian pigment. It reads as generic spiritual app.
Every competitor uses it. We do not. See docs/design.md anti-patterns.

---

## Anti-Patterns

Stop and reconsider if any screen is moving toward these:

- Purple or dark purple gradients anywhere in the UI
- Gold on every surface (gold means nothing if it is everywhere)
- Starfield / constellation backgrounds behind reading cards
- Pill-shaped buttons filled with gold
- Hieroglyphic borders running around every card
- Turquoise/faience as the primary brand color (it is an accent)
- Typewriter / character-by-character text animation on readings
- Spring animations or bounce easing on any transition
- Bullet points or headers visible to the user in reading output
- The Oracle Chamber accepting a follow-up message

---

## Tech Stack Decisions (Locked)

- Ephemeris: Swiss Ephemeris (swisseph / pyswisseph)
- Reading AI: Anthropic API, model claude-sonnet-4-6
- House system: Whole Sign
- Push: FCM (Android) + APNs (iOS)
- Hemerological calendar: static date lookup table, no ephemeris needed
- Khoiak standing layer (Oct 22–Nov 19): constant string appended to daily
  reading, not individual table entries
- Natal data: cached per user after onboarding, regenerated only on
  birth data correction (see docs/engine.md Section 12.5 for full field list)

---
