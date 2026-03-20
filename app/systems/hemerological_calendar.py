"""Egyptian hemerological calendar — fixed sacred day lookup table.

All dates are fixed annual Gregorian dates (no year-to-year recalculation).
Source: Section 11.6.1 of the Egyptian Astrology Engine specification.

Usage:
    from app.systems.hemerological_calendar import get_hemerological_entry, is_khoiak_active

    entry = get_hemerological_entry(month=7, day=23)
    # Returns dict with name, charge, line, push — or None if no entry for that date.
"""

from __future__ import annotations

# ─── Main lookup table ────────────────────────────────────────────────────────
# Keys are (month, day) tuples. Values contain:
#   name     – event name
#   charge   – HIGHLY_AUSPICIOUS | AUSPICIOUS | AUSPICIOUS_CAUTION | INAUSPICIOUS | LIMINAL
#   line     – exact hemerological closing line (added to daily reading)
#   push     – exact push notification copy
HEMEROLOGICAL_CALENDAR: dict[tuple[int, int], dict] = {

    # ── Epagomenal Days (July 18–22) ─────────────────────────────────────────
    (7, 18): {
        "name": "Birth of Osiris",
        "charge": "LIMINAL",
        "line": (
            "Osiris is born today. The lord of the eternal cycle arrives — "
            "what is dying is already in the process of becoming something permanent."
        ),
        "push": "Osiris is born today. What is ending is already regenerating.",
    },
    (7, 19): {
        "name": "Birth of Horus the Elder",
        "charge": "LIMINAL_AUSPICIOUS",
        "line": (
            "Horus the Elder is born today. The sovereign of the whole sky arrives — "
            "what is rightful in your situation asserts itself today without being forced."
        ),
        "push": "Horus the Elder is born. What is rightfully yours announces itself.",
    },
    (7, 20): {
        "name": "Birth of Set",
        "charge": "INAUSPICIOUS",
        "line": (
            "Set is born today, tearing through before his time. "
            "His energy seeks outlets — complete what is in front of you, initiate nothing new."
        ),
        "push": "Set's birthday. His energy seeks outlets. Complete, don't begin.",
    },
    (7, 21): {
        "name": "Birth of Isis",
        "charge": "HIGHLY_AUSPICIOUS",
        "line": (
            "Isis is born today. The Great Weaver arrives — "
            "what has been scattered in your life has a path back to wholeness. She holds the thread."
        ),
        "push": "Isis is born today. The Great Weaver is at her full power.",
    },
    (7, 22): {
        "name": "Birth of Nephthys",
        "charge": "LIMINAL",
        "line": (
            "Nephthys is born today. The goddess of all thresholds stands at every doorway — "
            "something in your life is crossing from one state to another. "
            "Do not rush what is in transit."
        ),
        "push": "Nephthys stands at the threshold today. Let what is crossing, cross.",
    },

    # ── Sothis Rising / New Year (July 23) ───────────────────────────────────
    # Deferred entirely to Sothis Annual Reading (Section 11.3).
    # This entry is included for push copy only; the hemerological line
    # is NOT added to daily readings on this date — the Sothis reading replaces it.
    (7, 23): {
        "name": "Sothis Rising / Egyptian New Year",
        "charge": "MOST_AUSPICIOUS",
        "line": None,  # Sothis Annual Reading replaces daily reading entirely
        "push": "Sopdet rises today. The year opens. What will you plant?",
    },

    # ── August ────────────────────────────────────────────────────────────────
    (8, 9): {
        "name": "Wag Festival (Feast of the Dead)",
        "charge": "AUSPICIOUS_SOLEMN",
        "line": (
            "The Wag Festival. The dead are honored today — "
            "those who came before you stand closer than usual. "
            "What they built is present in what you are building."
        ),
        "push": "The Wag Festival opens. The ancestors are close today.",
    },
    (8, 10): {
        "name": "Festival of Thoth",
        "charge": "HIGHLY_AUSPICIOUS",
        "line": (
            "Thoth's festival. The Divine Scribe opens his records for the new year — "
            "what is written, sent, signed, or learned today carries the force of the god's full attention."
        ),
        "push": "Thoth's festival. What you write today he records personally.",
    },

    # ── September ─────────────────────────────────────────────────────────────
    (9, 5): {
        "name": "Opet Festival Begins",
        "charge": "HIGHLY_AUSPICIOUS",
        "line": (
            "The Opet procession begins. Amun moves through the public world today — "
            "the hidden force behind all things makes itself briefly visible. "
            "What requires the backing of something larger than yourself, invoke it now."
        ),
        "push": "Amun walks in procession today. Invoke what you need his backing on.",
    },

    # ── October ───────────────────────────────────────────────────────────────
    (10, 7): {
        "name": "Death of Osiris (17th of Athyr)",
        "charge": "INAUSPICIOUS",
        "line": (
            "This is the day Osiris was taken. Set's treachery completed itself on this date — "
            "the Duat opens wider today than on ordinary days. "
            "Sacred caution: what can be deferred, defer. What cannot, proceed with full awareness."
        ),
        "push": "The day Osiris fell. Move with care. Complete — do not begin.",
    },
    (10, 21): {
        "name": "Khoiak Mysteries Begin",
        "charge": "LIMINAL",
        "line": (
            "The Khoiak mysteries open today. For the next month the sacred cycle of dissolution "
            "and reassembly is active — what is breaking apart in your life is doing so in the "
            "company of the god who was broken apart and made eternal. This is not random loss."
        ),
        "push": "Khoiak opens. The Osirian mystery is active. What dissolves, transforms.",
    },

    # ── November ──────────────────────────────────────────────────────────────
    (11, 14): {
        "name": "Isis Finds Osiris",
        "charge": "HIGHLY_AUSPICIOUS",
        "line": (
            "Isis finds Osiris today. What was scattered has been gathered. "
            "The reassembly is not yet complete, but the search is over — "
            "the pieces are in her hands. What have you been trying to restore? "
            "It is closer to whole than it appears."
        ),
        "push": "Isis finds what was scattered today. Recovery is closer than it feels.",
    },

    # ── December ──────────────────────────────────────────────────────────────
    (12, 21): {
        "name": "Winter Solstice / Ra Reborn",
        "charge": "AUSPICIOUS",
        "line": (
            "The solstice. Ra reaches his minimum and begins the return — "
            "from this day the light increases. "
            "What you have been carrying through the darkest part of the year, carry a little lighter. "
            "The arc has turned."
        ),
        "push": "The solstice. Ra begins his return. The light increases from today.",
    },

    # ── January ───────────────────────────────────────────────────────────────
    (1, 12): {
        "name": "Triumph of Horus",
        "charge": "HIGHLY_AUSPICIOUS",
        "line": (
            "The tribunal ruled for Horus today. What is rightful in your situation has the divine "
            "record on its side — press your claim. What has been disputed resolves in the direction "
            "of the legitimate."
        ),
        "push": "The tribunal ruled for Horus today. Press the rightful claim.",
    },

    # ── February ──────────────────────────────────────────────────────────────
    (2, 2): {
        "name": "Feast of Hathor's Return",
        "charge": "AUSPICIOUS",
        "line": (
            "Hathor returns from the southern road today. "
            "What went cold in the domain of love and beauty begins to warm — "
            "not all at once, but the direction has changed. She is back at the threshold."
        ),
        "push": "Hathor returns from the south today. What went cold is warming.",
    },

    # ── March ─────────────────────────────────────────────────────────────────
    (3, 4): {
        "name": "Feast of Bastet",
        "charge": "HIGHLY_AUSPICIOUS",
        "line": (
            "Bastet's feast. The goddess of the protected home and the joy of ordinary life "
            "is fully present today — this is a day for the people and pleasures closest to you. "
            "The small warmths are the sacred ones today."
        ),
        "push": "Bastet's feast. The best thing today is close to home.",
    },
    (3, 20): {
        "name": "Spring Equinox / Shemu Opens",
        "charge": "AUSPICIOUS",
        "line": (
            "Shemu opens. The harvest season begins — what was planted in the growing months "
            "is now above the soil and visible. The reaping follows. "
            "What did you plant, and are you ready to receive what grew?"
        ),
        "push": "Shemu opens. The harvest has begun. What did you plant?",
    },

    # ── April ─────────────────────────────────────────────────────────────────
    (4, 28): {
        "name": "Beautiful Feast of the Valley",
        "charge": "AUSPICIOUS",
        "line": (
            "The Beautiful Feast of the Valley. Amun crosses to the West Bank today and the boundary "
            "between the living and the dead becomes transparent. "
            "What those who came before you knew about the problem you are carrying is available today. "
            "The dead are glad to be remembered."
        ),
        "push": "The Feast of the Valley. The ancestors cross over today. Remember them.",
    },

    # ── June ──────────────────────────────────────────────────────────────────
    (6, 8): {
        "name": "Victory of Horus at Edfu",
        "charge": "HIGHLY_AUSPICIOUS",
        "line": (
            "Horus stands over Set at Edfu today. The long contest resolves in the direction "
            "of what is rightful — if you have been engaged in a sustained effort, "
            "a negotiation, a conflict that has dragged, today the field tips. "
            "Press what you have been building toward its conclusion."
        ),
        "push": "Horus defeats Set at Edfu today. The long contest tips your way.",
    },

    # ── Last Days of the Year (July 13–17) ───────────────────────────────────
    (7, 13): {
        "name": "Last Days of the Year",
        "charge": "INAUSPICIOUS",
        "line": (
            "The year runs to its end. The fields are dry, the Nile at its lowest, "
            "Sothis not yet visible. This is the last corridor before the new year opens — "
            "complete what requires completion and release what must be released before Sopdet rises."
        ),
        "push": "The year runs to its end. Complete before Sothis rises.",
    },
    (7, 14): {
        "name": "Last Days of the Year",
        "charge": "INAUSPICIOUS",
        "line": (
            "The year runs to its end. The fields are dry, the Nile at its lowest, "
            "Sothis not yet visible. This is the last corridor before the new year opens — "
            "complete what requires completion and release what must be released before Sopdet rises."
        ),
        "push": "The year runs to its end. Complete before Sothis rises.",
    },
    (7, 15): {
        "name": "Last Days of the Year",
        "charge": "INAUSPICIOUS",
        "line": (
            "The year runs to its end. The fields are dry, the Nile at its lowest, "
            "Sothis not yet visible. This is the last corridor before the new year opens — "
            "complete what requires completion and release what must be released before Sopdet rises."
        ),
        "push": "The year runs to its end. Complete before Sothis rises.",
    },
    (7, 16): {
        "name": "Last Days of the Year",
        "charge": "INAUSPICIOUS",
        "line": (
            "The year runs to its end. The fields are dry, the Nile at its lowest, "
            "Sothis not yet visible. This is the last corridor before the new year opens — "
            "complete what requires completion and release what must be released before Sopdet rises."
        ),
        "push": "The year runs to its end. Complete before Sothis rises.",
    },
    (7, 17): {
        "name": "Last Days of the Year",
        "charge": "INAUSPICIOUS",
        "line": (
            "The year runs to its end. The fields are dry, the Nile at its lowest, "
            "Sothis not yet visible. This is the last corridor before the new year opens — "
            "complete what requires completion and release what must be released before Sopdet rises."
        ),
        "push": "The year runs to its end. Complete before Sothis rises.",
    },
}

# ─── Khoiak period ───────────────────────────────────────────────────────────
# Oct 21 fires the "Khoiak opens" line from the table above.
# Oct 22 – Nov 19: apply this standing layer to every daily reading.
KHOIAK_START = (10, 21)
KHOIAK_END = (11, 19)
KHOIAK_STANDING_LAYER = (
    "The Khoiak mysteries continue. The Osirian dissolution is active. "
    "What is falling apart is in sacred process."
)


# ─── Public API ──────────────────────────────────────────────────────────────

def get_hemerological_entry(month: int, day: int) -> dict | None:
    """Return the calendar entry for this date, or None if not charged."""
    return HEMEROLOGICAL_CALENDAR.get((month, day))


def is_khoiak_active(month: int, day: int) -> bool:
    """True for Oct 22 – Nov 19 (the standing-layer period after opening day)."""
    if month == 10 and day >= 22:
        return True
    if month == 11 and day <= 19:
        return True
    return False


def get_khoiak_standing_layer() -> str:
    return KHOIAK_STANDING_LAYER
