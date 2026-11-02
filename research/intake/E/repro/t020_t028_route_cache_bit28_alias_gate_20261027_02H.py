"""E/T020 synthetic-only review of B T028 route-cache key encoding and guards.
No original gameplay execution, no native ABI inference, no Golden verdict.
"""
import unittest

MASK_FIRST = 0x7FFF
MASK_SECOND = 0xFFFF
ALT_BIT = 0x10000000

def packed_key(first, second):
    return ((first & MASK_FIRST) << 16) | (second & MASK_SECOND)

def alternate_key(key):
    return key | ALT_BIT

def same_lookup_key(first, second):
    key = packed_key(first, second)
    return alternate_key(key) == key

def hit_order_action(count_at_hit_branch, key, list_head_key):
    return "REORDER" if count_at_hit_branch > 8000 and key != list_head_key else "KEEP"

def miss_eviction_action(count_at_post_insert_branch):
    return "EVICTION_BRANCH" if count_at_post_insert_branch >= 8192 else "NO_EVICTION_BRANCH"

class RouteCacheSyntheticGuard(unittest.TestCase):
    def test_bit12_in_first_makes_alt_equal(self):
        for first in (0x1000, 0x1001, 0x3000, 0x7FFF):
            with self.subTest(first=first):
                self.assertTrue(same_lookup_key(first, 0x2345))
    def test_bit12_clear_makes_alt_distinct(self):
        for first in (0, 0x0FFF, 0x2000, 0x6000):
            with self.subTest(first=first):
                self.assertFalse(same_lookup_key(first, 0x2345))

    def test_explicit_packed_example(self):
        self.assertEqual(packed_key(0x1000, 0), 0x10000000)
        self.assertEqual(alternate_key(packed_key(0x1000, 0)), 0x10000000)

    def test_second_value_does_not_control_bit28(self):
        self.assertTrue(same_lookup_key(0x1000, 0xFFFF))
        self.assertFalse(same_lookup_key(0, 0xFFFF))

    def test_first_high_bit_is_masked(self):
        self.assertEqual(packed_key(0, 7), packed_key(0x8000, 7))

    def test_second_upper_bits_are_masked(self):
        self.assertEqual(packed_key(3, 7), packed_key(3, 0x10007))

    def test_hit_order_boundary(self):
        key, head = 0x123, 0x456
        self.assertEqual(hit_order_action(8000, key, head), "KEEP")
        self.assertEqual(hit_order_action(8001, key, head), "REORDER")

    def test_hit_same_head_never_reorders(self):
        for n in (8000, 8001, 8192):
            self.assertEqual(hit_order_action(n, 123, 123), "KEEP")

    def test_miss_post_insert_threshold(self):
        self.assertEqual(miss_eviction_action(8191), "NO_EVICTION_BRANCH")
        self.assertEqual(miss_eviction_action(8192), "EVICTION_BRANCH")

    def test_pure_model_not_gameplay(self):
        self.assertIsInstance(packed_key(0x1000, 0), int)

if __name__ == "__main__":
    unittest.main()
