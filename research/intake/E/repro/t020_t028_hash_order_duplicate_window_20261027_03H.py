"""T020 synthetic CONDITIONAL cache hash/order invariant probe.
B T028 original PE STATIC is not an observed reachable game condition.
The model intentionally assumes 0x4EC4CC order append even if insert flag is 0.
No original file access and no Golden outcome is calculated.
"""
import unittest


def insert(state, key, order_append=True):
    hash_keys, order_keys = state
    unique = key not in hash_keys
    result_hash = hash_keys + ([key] if unique else [])
    result_order = order_keys + ([key] if order_append else [])
    return (result_hash, result_order), unique


def evict_head(state):
    hash_keys, order_keys = state
    if not order_keys:
        return state
    old = order_keys[0]
    return ([k for k in hash_keys if k != old], order_keys[1:])


def diagnose(state):
    hash_keys, order_keys = state
    return {
        "hash_unique": len(hash_keys) == len(set(hash_keys)),
        "count_equal": len(hash_keys) == len(order_keys),
        "orphan_order": [k for k in order_keys if k not in hash_keys],
        "actual_golden_pass": False,
        "strict_match": False,
    }

class ConditionalOnlyTests(unittest.TestCase):
    def test_new_key_balanced(self):
        state, flag = insert(([], []), 7)
        self.assertTrue(flag)
        self.assertTrue(diagnose(state)["count_equal"])

    def test_duplicate_hash_rolled_back_but_order_appended(self):
        state, flag = insert(([7], [7]), 7)
        self.assertFalse(flag)
        self.assertEqual(state, ([7], [7, 7]))
        self.assertFalse(diagnose(state)["count_equal"])

    def test_duplicate_order_suppressed_is_balanced(self):
        state, flag = insert(([7], [7]), 7, order_append=False)
        self.assertFalse(flag)
        self.assertTrue(diagnose(state)["count_equal"])

    def test_head_eviction_can_leave_orphan_in_hypothetical_state(self):
        state, _ = insert(([7], [7]), 7)
        self.assertEqual(evict_head(state), ([], [7]))
        self.assertEqual(diagnose(evict_head(state))["orphan_order"], [7])

    def test_distinct_keys_do_not_create_duplication(self):
        state, flag = insert(([7], [7]), 8)
        self.assertTrue(flag)
        self.assertTrue(diagnose(state)["count_equal"])

    def test_no_native_gameplay_pass_is_reported(self):
        for state in (([], []), ([7], [7]), ([7], [7, 7])):
            self.assertFalse(diagnose(state)["actual_golden_pass"])
            self.assertFalse(diagnose(state)["strict_match"])


if __name__ == "__main__":
    unittest.main()
