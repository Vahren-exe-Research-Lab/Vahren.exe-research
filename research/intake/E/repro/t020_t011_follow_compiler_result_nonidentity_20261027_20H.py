"""E/T020: fail-closed regression for native follow compiler -> Rush result link.
STATIC / SYNTHETIC ONLY: no original gameplay or Golden acceptance is inferred.
B owner source: B-20261027-2013-T011-T012-FOLLOW-PARSER-RESULT-LINK-01.
"""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/T011_FOLLOW_COMPILER_RUSH_RESULT_LINK_NATIVE_20261027_20H.md"
SOURCE_SHA = "F2B968EF7B5E15583AF0883196EEFC314BACF9C09233DCD61BA98930ABFADCD8"

def compile_follow(raw, synthetic_numeric=None):
    """Only literal raw on has statically known compiled result 1.
    All other raw values take a native getter; without an independently
    supplied *synthetic* result they stay unknown, including raw off/0.
    """
    if not isinstance(raw, str):
        return (None, "UNSUPPORTED_RAW")
    if raw == "on":
        return (1, "STATIC_ON_PATH")
    if type(synthetic_numeric) is int and -(2**31) <= synthetic_numeric < 2**31:
        return (synthetic_numeric, "SYNTHETIC_GETTER_ONLY")
    return (None, "UNKNOWN_NATIVE_NUMERIC_GETTER")

def link_candidate(compiled, result, previous):
    """Represent write candidates, not true object identity or lifetime."""
    empty = {"result_backlink": None, "previous_forward": None,
             "rush_last": None, "parent_id": None, "exp_recipient": None,
             "actual_golden_pass": False, "strict_match": False}
    if type(compiled) is not int:
        return {**empty, "decision": "VERIFY_COMPILED_UNKNOWN"}
    if compiled == 0:
        return {**empty, "decision": "STATIC_BRANCH_SKIP"}
    if result is not None and (type(result) is not int or result <= 0):
        return {**empty, "decision": "VERIFY_INVALID_RESULT"}
    if previous is not None and (type(previous) is not int or previous <= 0):
        return {**empty, "decision": "VERIFY_INVALID_PREVIOUS"}
    if result is None:
        return {**empty, "decision": "SYNTHETIC_RESULT_NULL_CLEAR"}
    if previous is None:
        return {**empty, "decision": "SYNTHETIC_SET_LAST", "rush_last": result}
    return {**empty, "decision": "SYNTHETIC_PAIR_WRITE",
            "rush_last": result, "result_backlink": previous,
            "previous_forward": result}


class FollowCompilerResultGate(unittest.TestCase):
    def test_01_pin_owner_receipt(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper(), SOURCE_SHA)
    def test_02_literal_on_is_one(self):
        self.assertEqual(compile_follow("on"), (1, "STATIC_ON_PATH"))
    def test_03_off_requires_getter(self):
        self.assertEqual(compile_follow("off")[0], None)
    def test_04_zero_raw_not_inferred(self):
        self.assertEqual(compile_follow("0")[0], None)
    def test_05_numeric_raw_not_inferred(self):
        for raw in ("20", "30", "48", "@"):
            self.assertIsNone(compile_follow(raw)[0])
    def test_06_case_untested(self):
        self.assertIsNone(compile_follow("ON")[0])
    def test_07_synthetic_getter_zero(self):
        value, provenance = compile_follow("off", 0)
        self.assertEqual((value, provenance), (0, "SYNTHETIC_GETTER_ONLY"))
        self.assertEqual(link_candidate(value, 0, 123)["decision"], "STATIC_BRANCH_SKIP")
    def test_08_synthetic_getter_nonzero(self):
        self.assertEqual(link_candidate(20, 200, 100)["decision"], "SYNTHETIC_PAIR_WRITE")
    def test_09_on_but_null_result(self):
        self.assertEqual(link_candidate(1, None, 100)["decision"], "SYNTHETIC_RESULT_NULL_CLEAR")
    def test_10_on_first_result(self):
        self.assertEqual(link_candidate(1, 200, None)["rush_last"], 200)
        self.assertIsNone(link_candidate(1, 200, None)["result_backlink"])
    def test_11_previous_result_optional(self):
        r = link_candidate(1, 200, 100)
        self.assertEqual((r["result_backlink"], r["previous_forward"]), (100, 200))
    def test_12_unknown_follow_is_fail_closed(self):
        self.assertEqual(link_candidate(None, 200, 100)["decision"], "VERIFY_COMPILED_UNKNOWN")
    def test_13_boolean_cannot_stand_in_for_compiled_int(self):
        self.assertEqual(link_candidate(True, 200, 100)["decision"], "VERIFY_COMPILED_UNKNOWN")
    def test_14_invalid_pointer_is_review_only(self):
        self.assertEqual(link_candidate(1, -1, 100)["decision"], "VERIFY_INVALID_RESULT")
    def test_15_no_parent_or_exp_from_link(self):
        r = link_candidate(1, 200, 100)
        self.assertIsNone(r["parent_id"])
        self.assertIsNone(r["exp_recipient"])
    def test_16_no_golden_elevation(self):
        r = link_candidate(1, 200, 100)
        self.assertFalse(r["actual_golden_pass"])
        self.assertFalse(r["strict_match"])
    def test_17_raw_bools_invalid(self):
        self.assertEqual(compile_follow(True)[1], "UNSUPPORTED_RAW")
    def test_18_out_of_range_getter_rejected(self):
        self.assertIsNone(compile_follow("48", 2**31)[0])

if __name__ == "__main__":
    unittest.main(verbosity=2)

