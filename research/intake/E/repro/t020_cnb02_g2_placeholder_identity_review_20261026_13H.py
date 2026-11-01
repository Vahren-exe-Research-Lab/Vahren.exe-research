"""E/T020 C-NB02: semantic placeholder labels must not count as G2 identity receipts.
Conservative synthetic review; never native Golden or strict MATCH.
"""
import copy
import unittest
import t020_cnb02_g2_support_presence_deployment_review_20261026_1253 as previous

PLACEHOLDERS = frozenset({
    "unknown", "placeholder", "unverified", "tbd", "to_be_confirmed",
    "observed-unit", "observed-troop", "observed-power",
    "synthetic-unit", "synthetic-troop", "synthetic-power", "<missing>",
})
NEW_FLAGS = {
    "unit_visible": "G2_UNIT_ID_PLACEHOLDER_REVIEW",
    "troop_visible": "G2_TROOP_ID_PLACEHOLDER_REVIEW",
}
PARTICIPANT_FLAG = "G2_SIDE_PARTICIPANT_PLACEHOLDER_REVIEW"


def is_placeholder(value):
    return isinstance(value, str) and value.strip().casefold() in PLACEHOLDERS


def review(g2):
    before = previous.review(g2)
    issues = set(before["issues"])
    if isinstance(g2, dict):
        for row in g2.get("roster", []) if isinstance(g2.get("roster"), list) else []:
            if isinstance(row, dict):
                for field, flag in NEW_FLAGS.items():
                    if is_placeholder(row.get(field)):
                        issues.add(flag)
        sides = g2.get("sides")
        if isinstance(sides, dict):
            for members in sides.values():
                if isinstance(members, list) and any(is_placeholder(x) for x in members):
                    issues.add(PARTICIPANT_FLAG)
    return dict(before, issues=sorted(issues), verdict="VERIFY_NOT_GOLDEN",
                actual_golden_pass=False, strict_match=False,
                coverage="VISIBLE_LABELS_ONLY_NOT_NATIVE_IDENTITY")


class PlaceholderReviewTests(unittest.TestCase):
    def base(self):
        return previous.prior.prior11.parity10.old11.synthetic_candidate()["stages"]["g2"]

    def test_baseline_no_placeholders(self):
        self.assertEqual(review(self.base())["issues"], [])

    def check(self, mutate, flag):
        g = self.base()
        mutate(g)
        original = copy.deepcopy(g)
        out = review(g)
        self.assertEqual(g, original)
        self.assertIn(flag, out["issues"])
        self.assertEqual(out["verdict"], "VERIFY_NOT_GOLDEN")
        self.assertFalse(out["actual_golden_pass"])
        self.assertFalse(out["strict_match"])

    def test_attack_unit_unknown(self):
        self.check(lambda g: g["roster"][0].update(unit_visible="unknown"),
                   NEW_FLAGS["unit_visible"])

    def test_prior_did_not_flag_visible_placeholder(self):
        g = self.base()
        g["roster"][0]["unit_visible"] = "unknown"
        self.assertEqual(previous.review(g)["issues"], [])
        self.assertIn(NEW_FLAGS["unit_visible"], review(g)["issues"])

    def test_defense_troop_placeholder(self):
        self.check(lambda g: g["roster"][1].update(troop_visible=" PLACEHOLDER "),
                   NEW_FLAGS["troop_visible"])
    def test_attack_unit_observed_placeholder(self):
        self.check(lambda g: g["roster"][0].update(unit_visible="observed-unit"),
                   NEW_FLAGS["unit_visible"])

    def test_both_aliases_are_reviewed(self):
        g = self.base()
        g["roster"][0].update(unit_visible="TBD", troop_visible="synthetic-troop")
        out = review(g)
        self.assertTrue(set(NEW_FLAGS.values()).issubset(out["issues"]))

    def test_support_power_placeholder_review(self):
        self.check(lambda g: g["sides"]["support"].append("observed-power"),
                   PARTICIPANT_FLAG)

    def test_attack_participant_placeholder_review(self):
        self.check(lambda g: g["sides"]["attack"].append("unknown"),
                   PARTICIPANT_FLAG)

    def test_legitimate_composite_name_not_auto_rejected(self):
        g = self.base()
        g["roster"][0]["unit_visible"] = "Unknown Soldier"
        self.assertEqual(review(g)["issues"], [])

    def test_prior_support_mismatch_still_reported(self):
        self.check(lambda g: g["sides"]["support"].append("po_helper"),
                   "SUPPORT_DECLARED_WITHOUT_DEPLOYED_RECEIPT_REVIEW")

    def test_prior_crossrole_alias_still_reported(self):
        self.check(lambda g: g["roster"].append(dict(g["roster"][0], side="support")),
                   "CROSS_ROLE_VISIBLE_PAIR_ALIAS_REVIEW")

    def test_invalid_type_still_diagnosed(self):
        self.check(lambda g: g["roster"][0].update(unit_visible=7),
                   "ROSTER_IDS_NOT_TEXT")

    def test_no_foreign_sha_can_promote_synthetic(self):
        g = self.base()
        g.update(map_capture_sha="a"*64, old_observed=True)
        self.assertEqual(review(g)["verdict"], "VERIFY_NOT_GOLDEN")


if __name__ == "__main__":
    unittest.main()