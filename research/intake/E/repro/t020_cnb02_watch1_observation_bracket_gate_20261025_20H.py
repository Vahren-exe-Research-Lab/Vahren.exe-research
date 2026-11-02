"""E T020: retrospective observer-bracket classifier (synthetic timestamps only).
Do NOT promote any classification to original Golden or engine event time.
"""
import copy
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

FIXTURE = Path(__file__).with_name("T020_CNB02_WATCH1_SAMPLING_BOUNDS_20261025_19H.json")
EXPECTED_SHA = "9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7"
BRACKET_KINDS = [("mode", 1, 2), ("active", 0, 1),
                 ("active", 1, 0), ("mode", 2, 1)]

def parse_utc(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    t = datetime.fromisoformat(value)
    if t.tzinfo is None:
        raise ValueError("unqualified clock")
    return t.astimezone(timezone.utc)

def classify(fixture, capture_utc, clock="UTC_WALL_OBSERVATION"):
    verdict = {"phase": "VERIFY", "original_gameplay": False,
               "actual_golden_pass": False, "strict_match": False,
               "engine_transition_time_known": False}
    source = fixture.get("source", {})
    if source.get("sha256") != EXPECTED_SHA or source.get("record_count") != 234:
        verdict["phase"] = "SOURCE_PROVENANCE_VERIFY"
        return verdict
    if clock != "UTC_WALL_OBSERVATION":
        verdict["phase"] = "CLOCK_CALIBRATION_VERIFY"
        return verdict
    if capture_utc is None:
        verdict["phase"] = "NO_ACTUAL_G2_CAPTURE"
        return verdict
    try:
        cap = parse_utc(capture_utc)
        brackets = fixture["brackets"]
        assert len(brackets) == 4
        assert [(b["field"], b["old"], b["new"]) for b in brackets] == BRACKET_KINDS
        pairs = [(parse_utc(b["last_old"]), parse_utc(b["first_new"])) for b in brackets]
        assert all(a < b for a, b in pairs)
        assert all(pairs[i][1] <= pairs[i+1][0] for i in range(3))
    except (ValueError, KeyError, TypeError, AssertionError):
        verdict["phase"] = "INVALID_OBSERVATION_BRACKETS"
        return verdict
    m0, m1 = pairs[0]
    a0, a1 = pairs[1]
    z0, z1 = pairs[2]
    r0, r1 = pairs[3]
    if cap <= m0: phase = "BEFORE_MODE2_NOT_G2"
    elif cap < m1: phase = "PHASE_BOUNDARY_VERIFY"
    elif cap <= a0: phase = "PREACTIVE_REVIEW_ONLY"
    elif cap < a1: phase = "PHASE_BOUNDARY_VERIFY"
    elif cap <= z0: phase = "ACTIVE_WINDOW_REVIEW_ONLY"
    elif cap < z1: phase = "PHASE_BOUNDARY_VERIFY"
    elif cap <= r0: phase = "NOT_DEPLOYED_G2"
    elif cap < r1: phase = "NOT_DEPLOYED_G2"
    else: phase = "POSTBATTLE_NOT_G2"
    verdict["phase"] = phase
    verdict["mode_return_uncertain"] = r0 < cap < r1
    return verdict

class ObservationBracketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    def test_prior_b01_to_b05(self):
        for item in self.fixture["regression_fixture_designs"][:5]:
            with self.subTest(id=item["id"]):
                got = classify(self.fixture, item["capture_utc"])
                self.assertEqual(got["phase"], item["expected"])
                self.assertFalse(got["actual_golden_pass"])
                self.assertFalse(got["strict_match"])
    def test_observation_only_b06(self):
        self.assertEqual(classify(self.fixture, None)["phase"], "NO_ACTUAL_G2_CAPTURE")
    def test_confirmed_active_sample_is_review_only(self):
        self.assertEqual(classify(self.fixture, "2026-10-21T14:32:00+00:00")["phase"],
                         "ACTIVE_WINDOW_REVIEW_ONLY")
    def test_mode_exit_uncertainty(self):
        got = classify(self.fixture, "2026-10-21T14:33:35+00:00")
        self.assertEqual(got["phase"], "NOT_DEPLOYED_G2")
        self.assertTrue(got["mode_return_uncertain"])
    def test_invalid_clock_or_naive_time(self):
        self.assertEqual(classify(self.fixture, "2026-10-21T14:32:00+00:00",
                                  "UNSYNCED")["phase"], "CLOCK_CALIBRATION_VERIFY")
        self.assertEqual(classify(self.fixture, "2026-10-21T14:32:00")["phase"],
                         "INVALID_OBSERVATION_BRACKETS")
    def test_provenance_and_bracket_mutation(self):
        altered = copy.deepcopy(self.fixture)
        altered["source"]["sha256"] = "0" * 64
        self.assertEqual(classify(altered, "2026-10-21T14:32:00+00:00")["phase"],
                         "SOURCE_PROVENANCE_VERIFY")
        altered = copy.deepcopy(self.fixture)
        altered["brackets"][1]["last_old"] = "2026-10-21T14:33:40+00:00"
        self.assertEqual(classify(altered, "2026-10-21T14:32:00+00:00")["phase"],
                         "INVALID_OBSERVATION_BRACKETS")

if __name__ == "__main__":
    unittest.main(verbosity=2)