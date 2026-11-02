"""E/T020 synthetic review guard for B T028 death-count vector lifetime.
No old-game invocation, no runtime-byte capture, no Golden elevation.
"""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DETAIL = ROOT / "data/T028_DEATHCOUNT_RECORD_CLEAR_TRANSITION_NATIVE_20261027_22H.md"
EXPECTED_SHA = "0D93569856C41550EB7F76AE79BD2E5802567AB1E3FBBA45CC9934F0B4D6D8B5"
STRIDE = 0x1C

def vector_gate(begin, end, capacity):
    base = dict(status="VERIFY", candidate_records=None, clear_end=None,
                capacity_released=None, heap_frees_observed=None,
                actual_runtime_clear=None, actual_golden_pass=False,
                strict_match=False, g2_initial_roster=None)
    if any(type(v) is not int for v in (begin, end, capacity)):
        return {**base, "status": "VERIFY_VECTOR_FIELDS"}
    if min(begin, end, capacity) < 0 or not (begin <= end <= capacity):
        return {**base, "status": "VERIFY_VECTOR_BOUNDS"}
    if end != begin and begin == 0:
        return {**base, "status": "VERIFY_NULL_BEGIN"}
    if (end - begin) % STRIDE != 0:
        return {**base, "status": "VERIFY_1C_STRIDE"}
    if begin == end:
        return {**base, "status": "STATIC_EMPTY_SKIP",
                "candidate_records": 0, "clear_end": end}
    return {**base, "status": "STATIC_NONEMPTY_CLEAR_CANDIDATE",
            "candidate_records": (end - begin) // STRIDE,
            "clear_end": begin, "capacity_released": False}

def owner_join(callback, producer_owner, transition_owner, epoch_a, epoch_b):
    if callback != "count":
        return "NO_COUNT_PRODUCER_EVIDENCE"
    if any(v is None for v in (producer_owner, transition_owner, epoch_a, epoch_b)):
        return "VERIFY_MISSING_IDENTITY"
    if epoch_a != epoch_b:
        return "VERIFY_EPOCH_MISMATCH"
    if producer_owner != transition_owner:
        return "VERIFY_OWNER_MISMATCH"
    return "SYNTHETIC_SAME_OWNER_REVIEW_ONLY"

class CountQueueLifetimeGate(unittest.TestCase):
    def test_01_source_pin(self):
        self.assertEqual(hashlib.sha256(DETAIL.read_bytes()).hexdigest().upper(), EXPECTED_SHA)
    def test_02_empty_skip(self):
        self.assertEqual(vector_gate(0x1000, 0x1000, 0x1080)["status"], "STATIC_EMPTY_SKIP")
    def test_03_one_record(self):
        v = vector_gate(0x1000, 0x101C, 0x1100)
        self.assertEqual((v["candidate_records"], v["clear_end"]), (1, 0x1000))
    def test_04_multiple_records(self):
        self.assertEqual(vector_gate(0x2000, 0x2054, 0x20A8)["candidate_records"], 3)
    def test_05_capacity_not_freed(self):
        self.assertIs(vector_gate(0x2000, 0x201C, 0x2054)["capacity_released"], False)
    def test_06_no_heap_free_count(self):
        self.assertIsNone(vector_gate(0x2000, 0x201C, 0x2054)["heap_frees_observed"])
    def test_07_bounds_reject(self):
        for a,b,c in ((30,0,50), (0,56,28), (-1,27,56)):
            self.assertEqual(vector_gate(a,b,c)["status"], "VERIFY_VECTOR_BOUNDS")
    def test_08_missing_or_bool_reject(self):
        for x in (None, True, "4096", 1.0):
            self.assertEqual(vector_gate(x, 4096, 4096)["status"], "VERIFY_VECTOR_FIELDS")
    def test_09_stride_mismatch(self):
        self.assertEqual(vector_gate(0x1000, 0x101D, 0x1100)["status"], "VERIFY_1C_STRIDE")
    def test_10_null_nonempty(self):
        self.assertEqual(vector_gate(0, 28, 56)["status"], "VERIFY_NULL_BEGIN")
    def test_11_count_callback_independent_of_clear(self):
        self.assertEqual(owner_join("dead_event_a", 1, 1, "a", "a"), "NO_COUNT_PRODUCER_EVIDENCE")
    def test_12_missing_owner_is_verify(self):
        self.assertEqual(owner_join("count", None, 7, "a", "a"), "VERIFY_MISSING_IDENTITY")
    def test_13_different_owner_is_verify(self):
        self.assertEqual(owner_join("count", 7, 8, "a", "a"), "VERIFY_OWNER_MISMATCH")
    def test_14_different_epoch_is_verify(self):
        self.assertEqual(owner_join("count", 7, 7, "a", "b"), "VERIFY_EPOCH_MISMATCH")
    def test_15_equal_synthetic_refs_still_review_only(self):
        self.assertEqual(owner_join("count", 7, 7, "a", "a"), "SYNTHETIC_SAME_OWNER_REVIEW_ONLY")
    def test_16_empty_vector_not_an_actual_event_count(self):
        self.assertIsNone(vector_gate(0x1000,0x1000,0x1100)["actual_runtime_clear"])
    def test_17_nonempty_not_golden_pass(self):
        self.assertFalse(vector_gate(0x1000,0x101C,0x1100)["actual_golden_pass"])
    def test_18_nonempty_not_strict_match(self):
        self.assertFalse(vector_gate(0x1000,0x101C,0x1100)["strict_match"])
    def test_19_nonempty_not_g2_roster(self):
        self.assertIsNone(vector_gate(0x1000,0x101C,0x1100)["g2_initial_roster"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
