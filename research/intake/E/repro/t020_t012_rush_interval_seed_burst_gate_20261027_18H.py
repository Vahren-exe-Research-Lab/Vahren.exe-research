"""E/T020 Rush interval seed and burst: bounded STATIC/SYNTHETIC model only.
Never infer actual spawning, old gameplay PASS, deployed G2 roster, or strict MATCH.
"""
import hashlib
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "data/T012_RUSH_SKILL_INTERVAL_FIRST_TICK_BURST_NATIVE_20261027_18H.md"
SRC_SHA = "931ADC0C142968AD5DBBE70DC5E3851BD47D4C1E1F254E26C820CD61E2562CA6"

def infer_dispatches(interval, limit, allowed):
    """Hypothetical invocations of Rush effect body per permitted manager update.
    Preconditions: immutable Skill, no intermediate early return/exception/overflow.
    Every invocation is a candidate, not a confirmed spawned Unit or successful effect.
    """
    if (type(interval) is not int or type(limit) is not int or
        not (0 <= interval <= 20) or not (1 <= limit <= 20) or
        type(allowed) is not list or len(allowed) > 32 or
        any(type(v) is not bool for v in allowed)):
        return {"verdict": "VERIFY_UNSUPPORTED_INPUT", "candidates": None,
                "complete": False, "actual_golden_pass": False,
                "strict_match": False}
    counter = interval  # original Skill+0x78 seed: not zero.
    emitted = 0
    completed = False
    candidates = []
    for permitted in allowed:
        if not permitted or completed:
            candidates.append(0)
            continue
        counter += 1
        if counter < interval:
            candidates.append(0)
            continue
        counter = 0
        emit_this_update = 1
        emitted += 1
        if interval == 0:
            # One native invocation can loop through successive effect-body entries.
            emit_this_update += max(0, limit - emitted)
            emitted = limit
        completed = emitted >= limit
        candidates.append(emit_this_update)
    return {"verdict": "STATIC_MODEL_ONLY", "candidates": candidates,
            "complete": completed, "actual_golden_pass": False,
            "strict_match": False, "dynamic_observed": False,
            "initial_g2_roster_proven": False}

class RushIntervalTest(unittest.TestCase):
    def test_01_source_sha(self):
        self.assertEqual(hashlib.sha256(SRC.read_bytes()).hexdigest().upper(), SRC_SHA)
    def test_02_zero_interval_one(self):
        self.assertEqual(infer_dispatches(0, 1, [True])["candidates"], [1])
    def test_03_zero_interval_three_burst(self):
        self.assertEqual(infer_dispatches(0, 3, [True])["candidates"], [3])
    def test_04_zero_interval_no_extra_after_finish(self):
        self.assertEqual(infer_dispatches(0, 3, [True, True])["candidates"], [3, 0])
    def test_05_one_interval_each_allowed_tick(self):
        self.assertEqual(infer_dispatches(1, 3, [True]*3)["candidates"], [1,1,1])
    def test_06_three_interval_seed_first_tick(self):
        self.assertEqual(infer_dispatches(3, 3, [True])["candidates"], [1])
    def test_07_three_interval_subsequent_gap(self):
        self.assertEqual(infer_dispatches(3, 3, [True]*7)["candidates"], [1,0,0,1,0,0,1])
    def test_08_manager_blocked_first_update(self):
        self.assertEqual(infer_dispatches(3, 1, [False, True])["candidates"], [0,1])
    def test_09_manager_blocks_do_not_advance_counter(self):
        self.assertEqual(infer_dispatches(2, 2, [True, False, True, False, True, True])["candidates"], [1,0,0,0,1,0])
    def test_10_no_permitted_update(self):
        self.assertEqual(infer_dispatches(0, 3, [False]*3)["candidates"], [0,0,0])
    def test_11_nonpositive_limit_unsupported(self):
        self.assertEqual(infer_dispatches(0, 0, [True])["verdict"], "VERIFY_UNSUPPORTED_INPUT")
    def test_12_negative_interval_unsupported(self):
        self.assertEqual(infer_dispatches(-1, 3, [True])["verdict"], "VERIFY_UNSUPPORTED_INPUT")
    def test_13_boolean_skill_fields_rejected(self):
        self.assertEqual(infer_dispatches(True, 3, [True])["verdict"], "VERIFY_UNSUPPORTED_INPUT")
        self.assertEqual(infer_dispatches(1, False, [True])["verdict"], "VERIFY_UNSUPPORTED_INPUT")
    def test_14_unknown_gate_rejected(self):
        self.assertEqual(infer_dispatches(1, 2, [True, None])["verdict"], "VERIFY_UNSUPPORTED_INPUT")
    def test_15_unfinished_is_not_implicit_success(self):
        r = infer_dispatches(3, 2, [True, True])
        self.assertFalse(r["complete"])
        self.assertEqual(r["candidates"], [1,0])
    def test_16_burst_not_gameplay_or_g2(self):
        r = infer_dispatches(0, 3, [True])
        self.assertEqual(r["candidates"], [3])
        for key in ("actual_golden_pass", "strict_match", "dynamic_observed", "initial_g2_roster_proven"):
            self.assertFalse(r[key])
    def test_17_empty_window(self):
        self.assertEqual(infer_dispatches(2, 2, [])["candidates"], [])

if __name__ == "__main__":
    unittest.main(verbosity=2)
