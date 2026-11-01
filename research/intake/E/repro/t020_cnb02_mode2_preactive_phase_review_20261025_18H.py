"""E T020: single-watch phase taxonomy. Synthetic checks; NEVER a Golden gate.
Does not join separate captures/runs or modify the 16H/17H validators.
"""
import math
import unittest
from datetime import datetime

FIELDS = ("mode2_enter", "active_enter", "active_zero", "mode1_return", "g2_capture")
def assess(row):
    if row.get("same_clock") is not True:
        phase = "CLOCK_DOMAIN_VERIFY"
    elif any(type(row.get(k)) not in (float, int) or
             not math.isfinite(row[k]) for k in FIELDS):
        phase = "TIME_EVIDENCE_INVALID"
    else:
        m, a, z, r, c = (row[k] for k in FIELDS)
        if not (m <= a < z <= r):
            phase = "PHASE_ORDER_INVALID"
        elif c < m:
            phase = "BEFORE_MODE2_NOT_G2"
        elif c < a:
            phase = "MODE2_PREACTIVE_VERIFY"
        elif c < z:
            phase = "ACTIVE_WINDOW_REVIEW_ONLY"
        elif c < r:
            phase = "ACTIVE_ZERO_EXIT_TAIL_NOT_G2"
        else:
            phase = "MODE1_POSTBATTLE_NOT_G2"
    return {"phase": phase, "golden_pass": False, "strict_match": False}

def baseline():
    return dict(mode2_enter=10.0, active_enter=13.0,
                active_zero=130.0, mode1_return=132.0,
                g2_capture=15.0, same_clock=True)

CASES = (
    (9.9, "BEFORE_MODE2_NOT_G2"),
    (10.0, "MODE2_PREACTIVE_VERIFY"),
    (12.99, "MODE2_PREACTIVE_VERIFY"),
    (13.0, "ACTIVE_WINDOW_REVIEW_ONLY"),
    (129.99, "ACTIVE_WINDOW_REVIEW_ONLY"),
    (130.0, "ACTIVE_ZERO_EXIT_TAIL_NOT_G2"),
    (131.99, "ACTIVE_ZERO_EXIT_TAIL_NOT_G2"),
    (132.0, "MODE1_POSTBATTLE_NOT_G2"),
)

class PhaseWindowTests(unittest.TestCase):
    def test_synthetic_intervals(self):
        for stamp, expected in CASES:
            with self.subTest(stamp=stamp):
                x = baseline(); x["g2_capture"] = stamp
                got = assess(x)
                self.assertEqual(got["phase"], expected)
                self.assertFalse(got["golden_pass"])
                self.assertFalse(got["strict_match"])

    def test_bad_clock(self):
        x = baseline(); x["same_clock"] = False
        self.assertEqual(assess(x)["phase"], "CLOCK_DOMAIN_VERIFY")

    def test_bad_order(self):
        x = baseline(); x["active_enter"] = 131.0
        self.assertEqual(assess(x)["phase"], "PHASE_ORDER_INVALID")

    def test_nonfinite(self):
        x = baseline(); x["g2_capture"] = float("inf")
        self.assertEqual(assess(x)["phase"], "TIME_EVIDENCE_INVALID")

    def test_bool_not_number(self):
        x = baseline(); x["active_zero"] = True
        self.assertEqual(assess(x)["phase"], "TIME_EVIDENCE_INVALID")

    def test_saved_watch1_phase_gaps_only(self):
        # Times from 2026-10-21 original watch retrospective JSON;
        # no actual G2 capture timestamp is asserted here.
        def utc(stamp):
            return datetime.fromisoformat(stamp)
        m = utc("2026-10-21T14:31:34.951083+00:00")
        a = utc("2026-10-21T14:31:37.765392+00:00")
        z = utc("2026-10-21T14:33:34.325867+00:00")
        r = utc("2026-10-21T14:33:35.933687+00:00")
        self.assertEqual(round((a-m).total_seconds(),6), 2.814309)
        self.assertEqual(round((r-z).total_seconds(),6), 1.607820)

if __name__ == "__main__":
    unittest.main(verbosity=1)