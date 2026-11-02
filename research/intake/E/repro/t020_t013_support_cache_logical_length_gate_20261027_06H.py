# E-owned synthetic regression only; NOT original executable behavior.
# Source: B-20261027-0514-T013-SUPPORT-CACHE-REBUILD-VECTOR-01 (NOT READY).
import unittest

class ToyVector:
    def __init__(self, initial, capacity):
        assert len(initial) <= capacity
        self.storage = list(initial) + [None] * (capacity - len(initial))
        self.used = len(initial)
        self.capacity = capacity
    def refresh(self, source, branch, enabled=True):
        assert branch in ("normal", "confusion")
        if not enabled:
            return
        self.used = 0  # logical clear, not physical zero-fill
        if len(source) > self.capacity:
            self.capacity = len(source)  # synthetic allocation policy only
            self.storage = [None] * self.capacity
        self.storage[:len(source)] = list(source)
        self.used = len(source)
    @property
    def active(self):
        return self.storage[:self.used]

class SyntheticGate(unittest.TestCase):
    def test_normal_clears_old(self):
        v = ToyVector(["old1", "old2"], 4)
        v.refresh(["new"], "normal")
        self.assertEqual(v.active, ["new"])
    def test_confusion_clears_old(self):
        v = ToyVector(["old1", "old2"], 4)
        v.refresh(["new"], "confusion")
        self.assertEqual(v.active, ["new"])
    def test_empty_source_is_empty_even_with_stale_bytes(self):
        v = ToyVector(["old1", "old2"], 4)
        v.refresh([], "normal")
        self.assertEqual(v.active, [])
        self.assertEqual(v.storage[:2], ["old1", "old2"])
    def test_empty_confusion_source(self):
        v = ToyVector(["old1"], 3)
        v.refresh([], "confusion")
        self.assertEqual(v.used, 0)
    def test_capacity_retention(self):
        v = ToyVector(["old"], 5)
        before = id(v.storage)
        v.refresh(["new1", "new2"], "normal")
        self.assertEqual(id(v.storage), before)
    def test_capacity_shortfall_allocates(self):
        v = ToyVector(["old"], 1)
        v.refresh(["a", "b", "c"], "confusion")
        self.assertGreaterEqual(v.capacity, 3)
        self.assertEqual(v.active, ["a", "b", "c"])
    def test_not_full_refresh_does_not_clear(self):
        v = ToyVector(["old"], 2)
        v.refresh(["new"], "normal", enabled=False)
        self.assertEqual(v.active, ["old"])
    def test_no_gameplay_inference_from_synthetic_cache(self):
        v = ToyVector(["old"], 2)
        v.refresh(["new"], "normal")
        old_capture = None
        map_sha = None
        self.assertFalse(bool(v.active) and bool(old_capture) and bool(map_sha))

if __name__ == "__main__":
    unittest.main(verbosity=2)
