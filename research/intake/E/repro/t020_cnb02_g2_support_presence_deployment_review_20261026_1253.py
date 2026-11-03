"""E/T020 G2 support participation vs deployed-roster conservative review.
Synthetic validation only. No native state, Golden PASS or strict comparison.
"""
import copy
import unittest
import t020_cnb02_g2_cross_role_visible_alias_guard_20261026_1158 as prior

FLAGS = frozenset(("SUPPORT_DECLARED_WITHOUT_DEPLOYED_RECEIPT_REVIEW",
                   "SUPPORT_DEPLOYED_RECEIPT_WITHOUT_DECLARED_PARTICIPANT_REVIEW"))


def valid_label(value):
    return isinstance(value, str) and bool(value.strip())


def review(g2):
    previous = prior.review(g2)
    issues = set(previous["issues"])
    if isinstance(g2, dict):
        sides, roster = g2.get("sides"), g2.get("roster")
        if isinstance(sides, dict) and isinstance(sides.get("support"), list) and isinstance(roster, list):
            participants = sides["support"]
            if all(valid_label(x) for x in participants):
                has_declaration = bool(participants)
                has_deployed_receipt = any(
                    isinstance(row, dict) and row.get("side") == "support"
                    and valid_label(row.get("unit_visible"))
                    and valid_label(row.get("troop_visible")) for row in roster)
                if has_declaration and not has_deployed_receipt:
                    issues.add("SUPPORT_DECLARED_WITHOUT_DEPLOYED_RECEIPT_REVIEW")
                if has_deployed_receipt and not has_declaration:
                    issues.add("SUPPORT_DEPLOYED_RECEIPT_WITHOUT_DECLARED_PARTICIPANT_REVIEW")
    return dict(previous, issues=sorted(issues), verdict="VERIFY_NOT_GOLDEN",
                actual_golden_pass=False, strict_match=False,
                coverage="SUPPORT_PARTICIPATION_DEPLOYMENT_RELATION_IS_NONPROOF")


class SupportRoleReviewTests(unittest.TestCase):
    def base(self):
        return prior.prior11.parity10.old11.synthetic_candidate()["stages"]["g2"]

    def check(self, g2, expected=None):
        original = copy.deepcopy(g2)
        out = review(g2)
        self.assertEqual(g2, original)
        self.assertEqual(out["verdict"], "VERIFY_NOT_GOLDEN")
        self.assertFalse(out["actual_golden_pass"])
        self.assertFalse(out["strict_match"])
        if expected:
            self.assertIn(expected, out["issues"])
        return out

    def test_empty_support_is_permitted_shape(self):
        self.assertFalse(FLAGS.intersection(self.check(self.base())["issues"]))
    def test_nonempty_support_and_matching_roster_still_non_golden(self):
        g = self.base(); g["sides"]["support"] = ["po_helper"]
        g["roster"].append({"side": "support", "unit_visible": "u_helper", "troop_visible": "t_helper"})
        self.assertFalse(FLAGS.intersection(self.check(g)["issues"]))

    def test_declared_support_without_roster_requires_review(self):
        g = self.base(); g["sides"]["support"] = ["po_helper"]
        self.check(g, "SUPPORT_DECLARED_WITHOUT_DEPLOYED_RECEIPT_REVIEW")

    def test_support_roster_without_declared_participant_requires_review(self):
        g = self.base(); g["roster"].append({"side": "support", "unit_visible": "u3", "troop_visible": "t3"})
        self.check(g, "SUPPORT_DEPLOYED_RECEIPT_WITHOUT_DECLARED_PARTICIPANT_REVIEW")

    def test_invalid_support_roster_is_not_evidence_of_deployment(self):
        g = self.base(); g["sides"]["support"] = ["po_helper"]
        g["roster"].append({"side": "support", "unit_visible": None, "troop_visible": "t3"})
        out = self.check(g, "SUPPORT_DECLARED_WITHOUT_DEPLOYED_RECEIPT_REVIEW")
        self.assertIn("ROSTER_IDS_NOT_TEXT", out["issues"])

    def test_invalid_participant_list_does_not_imply_native_absence(self):
        g = self.base(); g["sides"]["support"] = [None]
        out = self.check(g, "SIDE_PARTICIPANT_LABEL_UNTYPED")
        self.assertFalse(FLAGS.intersection(out["issues"]))

    def test_combat_role_missing_retains_prior_guard(self):
        g = self.base(); g["roster"].pop()
        self.check(g, "NO_DEFENSE_ROSTER_RECEIPT")
    def test_cross_role_alias_signal_preserved(self):
        g = self.base(); g["roster"].append(dict(g["roster"][0], side="support"))
        out = self.check(g, "CROSS_ROLE_VISIBLE_PAIR_ALIAS_REVIEW")
        self.assertIn("SUPPORT_DEPLOYED_RECEIPT_WITHOUT_DECLARED_PARTICIPANT_REVIEW", out["issues"])

    def test_nonobject_input_remains_fail_closed(self):
        self.check(None, "G2_NOT_OBJECT")

    def test_missing_support_field_is_schema_review_not_support_absence(self):
        g = self.base(); g["sides"].pop("support")
        out = self.check(g, "SIDE_SCHEMA")
        self.assertFalse(FLAGS.intersection(out["issues"]))

    def test_forged_sha_values_still_do_not_grant_golden(self):
        g = self.base(); g.update(map_capture_sha="a" * 64, old_observed=True)
        self.check(g)

    def test_more_than_one_support_participant_without_roster_is_not_two_missing_troops(self):
        g = self.base(); g["sides"]["support"] = ["po_helper_1", "po_helper_2"]
        out = self.check(g, "SUPPORT_DECLARED_WITHOUT_DEPLOYED_RECEIPT_REVIEW")
        self.assertEqual(sum(flag in out["issues"] for flag in FLAGS), 1)


if __name__ == "__main__":
    unittest.main()
