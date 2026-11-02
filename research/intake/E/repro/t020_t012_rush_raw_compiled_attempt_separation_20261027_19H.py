"""E/T020 bounded Rush raw-to-compiled interval and attempted-dispatch regression.
STATIC/SYNTHETIC model only. Never infer live effects, G2, Golden PASS or strict MATCH.
"""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/T012_RUSH_COMPILED_INTERVAL_ATTEMPT_LINK_NATIVE_20261027_19H.md"
SOURCE_SHA = "94B1496217B2336458137A03CA89E15C197E5529219ED0BFAFD9953320861ADF"

def compile_interval(raw):
    if type(raw) is not int or raw < -1 or raw > 20:
        return None
    return 0 if raw == -1 else (5 if raw == 0 else raw)

def model(raw, limit, allowed):
    """Count *attempt candidates* per permitted update, not successful effects.
    Normal return, immutable values, known GameTask gate, no overflow are assumed.
    """
    interval = compile_interval(raw)
    if (interval is None or type(limit) is not int or limit < 0 or limit > 20
            or type(allowed) is not list or len(allowed) > 32
            or any(type(v) is not bool for v in allowed)):
        return {"verdict": "VERIFY_UNSUPPORTED", "attempts": None,
                "actual_golden_pass": False, "strict_match": False}
    count, counter, output = 0, interval, []
    for active in allowed:
        if not active or count >= max(1, limit):
            output.append(0)
            continue
        counter += 1
        if counter < interval:
            output.append(0)
            continue
        counter = 0
        n = max(1, limit) - count if interval == 0 else 1
        count += n
        output.append(n)
    return {"verdict": "STATIC_MODEL_ONLY", "compiled_interval": interval,
            "attempts": output, "total_attempts": count, "successful_effects": None,
            "result_object_type": None, "parent_identity": None,
            "initial_g2_roster_proven": False, "dynamic_observed": False,
            "actual_golden_pass": False, "strict_match": False}

class RushRawCompiledTest(unittest.TestCase):
    def test_01_source_byte_sha(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper(), SOURCE_SHA)
    def test_02_raw_minus_one_compiles_zero(self):
        self.assertEqual(compile_interval(-1), 0)
    def test_03_raw_zero_compiles_five(self):
        self.assertEqual(compile_interval(0), 5)
    def test_04_positive_passthrough(self):
        self.assertEqual([compile_interval(x) for x in (1, 2, 5)], [1, 2, 5])
    def test_05_raw_minus_one_burst_four_attempts(self):
        self.assertEqual(model(-1, 4, [True, True])["attempts"], [4, 0])
    def test_06_raw_zero_does_not_burst(self):
        self.assertEqual(model(0, 4, [True]*6)["attempts"], [1, 0, 0, 0, 0, 1])
    def test_07_raw_two_seed_first_tick(self):
        self.assertEqual(model(2, 3, [True]*5)["attempts"], [1, 0, 1, 0, 1])
    def test_08_zero_limit_still_one_attempt(self):
        self.assertEqual(model(-1, 0, [True, True])["attempts"], [1, 0])
    def test_09_blocked_gate_does_not_advance(self):
        self.assertEqual(model(2, 2, [False, True, False, True, True])["attempts"], [0, 1, 0, 0, 1])
    def test_10_unsupported_below_minus_one(self):
        self.assertEqual(model(-2, 4, [True])["verdict"], "VERIFY_UNSUPPORTED")
    def test_11_bool_not_valid_raw_or_limit(self):
        self.assertEqual(model(True, 4, [True])["verdict"], "VERIFY_UNSUPPORTED")
        self.assertEqual(model(-1, False, [True])["verdict"], "VERIFY_UNSUPPORTED")
    def test_12_unknown_gate_rejected(self):
        self.assertEqual(model(-1, 2, [None])["verdict"], "VERIFY_UNSUPPORTED")
    def test_13_attempts_not_effects(self):
        r = model(-1, 4, [True])
        self.assertEqual(r["total_attempts"], 4)
        self.assertIsNone(r["successful_effects"])
    def test_14_no_parent_from_result_pointer(self):
        r = model(-1, 4, [True])
        self.assertIsNone(r["parent_identity"])
        self.assertIsNone(r["result_object_type"])
    def test_15_no_golden_promotion(self):
        r = model(-1, 4, [True])
        self.assertFalse(r["dynamic_observed"])
        self.assertFalse(r["initial_g2_roster_proven"])
        self.assertFalse(r["actual_golden_pass"])
        self.assertFalse(r["strict_match"])
    def test_16_no_update_no_attempt(self):
        self.assertEqual(model(-1, 4, [False, False])["total_attempts"], 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
