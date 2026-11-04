"""E/T020 E10->E11->E12 strict synthetic-preflight erratum.

Reuses existing 2026-10-28 10H/11H/12H E study IDs; adds no native evidence.
A True preflight is ELIGIBILITY_ONLY, never original Golden/MATCH/READY.
This script is pure Python: no original EXE/DAT/SAVE/MAP or V9 dependency.
"""
import unittest

FLAGS = ("g0", "g1", "g2", "same_run", "original_dat", "actual_execution")


def strict_eligible(receipts):
    """Reject missing/extra/implicit-truthy flags; does not authenticate any receipt."""
    return (type(receipts) is dict and set(receipts) == set(FLAGS)
            and all(type(receipts[k]) is bool and receipts[k] is True for k in FLAGS))


def strict_verdict(receipts, old_capture=None, new_capture=None):
    """Never produces PASS/READY. Actual source/identity/byte checks are external."""
    if not strict_eligible(receipts):
        return "NOT_ELIGIBLE"
    if old_capture is None:
        return "NO_ACTUAL_GOLDEN"
    if new_capture is None:
        return "NO_STRICT_COMPARISON"
    return "COMPARE_REQUIRED"


class StrictAdmissionErratumTests(unittest.TestCase):
    def valid(self):
        return dict.fromkeys(FLAGS, True)

    def test_literal_true_only_eligible_not_pass(self):
        self.assertTrue(strict_eligible(self.valid()))
        self.assertEqual(strict_verdict(self.valid()), "NO_ACTUAL_GOLDEN")

    def test_each_false_rejected(self):
        for key in FLAGS:
            with self.subTest(key=key):
                x = self.valid(); x[key] = False
                self.assertEqual(strict_verdict(x), "NOT_ELIGIBLE")

    def test_each_truthy_false_string_rejected(self):
        for key in FLAGS:
            with self.subTest(key=key):
                x = self.valid(); x[key] = "false"
                self.assertEqual(strict_verdict(x, {}, {}), "NOT_ELIGIBLE")

    def test_each_integer_one_rejected(self):
        for key in FLAGS:
            with self.subTest(key=key):
                x = self.valid(); x[key] = 1
                self.assertEqual(strict_verdict(x, {}, {}), "NOT_ELIGIBLE")

    def test_other_truthy_placeholders_rejected(self):
        for value in ("0", "true", 2, [], [1], {"proof": True}, None):
            with self.subTest(value=repr(value)):
                x = self.valid(); x["g2"] = value
                self.assertEqual(strict_verdict(x, {}, {}), "NOT_ELIGIBLE")

    def test_partial_and_unknown_keys_rejected(self):
        x = self.valid(); del x["same_run"]
        self.assertFalse(strict_eligible(x))
        x = self.valid(); x["synthetic_fixture_pass"] = True
        self.assertFalse(strict_eligible(x))

    def test_non_dict_rejected(self):
        for x in (None, [], "true", True):
            with self.subTest(value=repr(x)):
                self.assertEqual(strict_verdict(x), "NOT_ELIGIBLE")

    def test_old_capture_alone_not_match(self):
        self.assertEqual(strict_verdict(self.valid(), {"old": 1}), "NO_STRICT_COMPARISON")

    def test_two_captures_only_comparison_required(self):
        self.assertEqual(strict_verdict(self.valid(), {"old": 1}, {"new": 1}),
                         "COMPARE_REQUIRED")

    def test_boolean_flags_do_not_authenticate_real_same_run(self):
        # Caller-provided bools can lie. This is a *synthetic classifier* only.
        x = self.valid()
        self.assertTrue(strict_eligible(x))
        self.assertNotIn(strict_verdict(x, {}, {}), ("PASS", "READY", "STRICT_MATCH"))

    def test_previous_e10_truthiness_bug_reproducer(self):
        # The archived E10 source uses all((g0,g1,g2,same_run,original_dat,actual_execution)).
        x = dict.fromkeys(FLAGS, "false")
        self.assertTrue(all(x[k] for k in FLAGS))
        self.assertFalse(strict_eligible(x))

    def test_invalid_flags_never_compare_even_with_captures(self):
        x = self.valid(); x["actual_execution"] = 1
        self.assertEqual(strict_verdict(x, {"old": 1}, {"new": 1}), "NOT_ELIGIBLE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
