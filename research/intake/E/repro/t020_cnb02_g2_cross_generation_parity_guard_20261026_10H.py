"""E T020: preserve 11H G2 warnings across 08H and 09H synthetic diagnostics."""
import copy
import unittest
import t020_cnb02_g2_semantic_review_20261025_11H as old11
import t020_cnb02_g2_roster_role_coverage_overlay_20261026_09H as role09
import t020_cnb02_g2_roster_shape_diagnostic_20261026_08H as shape08

MAP_PLACEHOLDERS = frozenset({"observed-map", "static_unconfirmed_map",
                               "unknown", "placeholder"})
ROLE_NAMES = ("attack", "defense", "support")

def review(g2):
    previous = role09.review(g2)
    issues = set(previous["issues"])
    if isinstance(g2, dict):
        map_id = g2.get("map_id")
        if isinstance(map_id, str) and map_id.strip().casefold() in MAP_PLACEHOLDERS:
            if "MAP_ID_UNVERIFIED" not in issues:
                issues.add("MAP_PLACEHOLDER_ALIAS_VERIFY")
        sides = g2.get("sides")
        if isinstance(sides, dict):
            for role in ROLE_NAMES:
                members = sides.get(role)
                if isinstance(members, list) and any(not shape08.ident(x) for x in members):
                    issues.add("SIDE_PARTICIPANT_LABEL_UNTYPED")
    return {"verdict": "VERIFY_NOT_GOLDEN", "issues": sorted(issues),
            "coverage": "SYNTHETIC_SHAPE_AND_ROLE_PRESENCE_ONLY",
            "actual_golden_pass": False, "strict_match": False}

class CrossGenerationParityTests(unittest.TestCase):
    def base(self):
        return old11.synthetic_candidate()
    def check(self, receipt, flag):
        outcome = review(receipt["stages"]["g2"])
        self.assertIn(flag, outcome["issues"])
        self.assertEqual(outcome["verdict"], "VERIFY_NOT_GOLDEN")
        self.assertFalse(outcome["actual_golden_pass"])
        self.assertFalse(outcome["strict_match"])
    def test_numeric_side_participant_restores_11h_warning(self):
        receipt = self.base()
        receipt["stages"]["g2"]["sides"]["attack"] = [7]
        self.assertIn("INVALID_SIDE_PARTICIPANT_LABEL", old11.review_g2(receipt)["flags"])
        self.assertEqual(role09.review(receipt["stages"]["g2"])["issues"], [])
        self.check(receipt, "SIDE_PARTICIPANT_LABEL_UNTYPED")
    def test_blank_side_participant(self):
        r = self.base(); r["stages"]["g2"]["sides"]["defense"] = [" "]
        self.check(r, "SIDE_PARTICIPANT_LABEL_UNTYPED")
    def test_none_side_participant(self):
        r = self.base(); r["stages"]["g2"]["sides"]["support"] = [None]
        self.check(r, "SIDE_PARTICIPANT_LABEL_UNTYPED")
    def test_boolean_side_participant(self):
        r = self.base(); r["stages"]["g2"]["sides"]["attack"] = [True]
        self.check(r, "SIDE_PARTICIPANT_LABEL_UNTYPED")
    def test_unknown_map_alias_restores_11h_warning(self):
        r = self.base(); r["stages"]["g2"]["map_id"] = " unknown "
        self.assertIn("MAP_ID_PLACEHOLDER_OR_INVALID", old11.review_g2(r)["flags"])
        self.assertEqual(role09.review(r["stages"]["g2"])["issues"], [])
        self.check(r, "MAP_PLACEHOLDER_ALIAS_VERIFY")
    def test_placeholder_map_alias(self):
        r = self.base(); r["stages"]["g2"]["map_id"] = "PLACEHOLDER"
        self.check(r, "MAP_PLACEHOLDER_ALIAS_VERIFY")
    def test_lowercase_static_map_alias(self):
        r = self.base(); r["stages"]["g2"]["map_id"] = "static_unconfirmed_map"
        self.check(r, "MAP_PLACEHOLDER_ALIAS_VERIFY")
    def test_trimmed_observed_map_alias(self):
        r = self.base(); r["stages"]["g2"]["map_id"] = " Observed-Map "
        self.check(r, "MAP_PLACEHOLDER_ALIAS_VERIFY")
    def test_existing_attack_defense_presence_still_works(self):
        r = self.base(); r["stages"]["g2"]["roster"].pop()
        self.check(r, "NO_DEFENSE_ROSTER_RECEIPT")
    def test_existing_shape_checks_are_preserved(self):
        r = self.base(); r["stages"]["g2"]["roster"][0]["unit_visible"] = 123
        self.check(r, "ROSTER_IDS_NOT_TEXT")
    def test_empty_support_slot_allowed(self):
        r = self.base()
        self.assertNotIn("SIDE_PARTICIPANT_LABEL_UNTYPED", review(r["stages"]["g2"])["issues"])
    def test_normal_shape_never_promotes_golden(self):
        r = self.base(); g = r["stages"]["g2"]
        g.update(map_capture_sha="a"*64, old_observed=True)
        self.assertEqual(review(g)["verdict"], "VERIFY_NOT_GOLDEN")
        self.assertFalse(review(g)["strict_match"])
    def test_malformed_g2_never_promotes(self):
        out = review(None)
        self.assertIn("NO_ATTACK_ROSTER_RECEIPT", out["issues"])
        self.assertFalse(out["actual_golden_pass"])
    def test_reused_visible_pairs_trigger_only_review(self):
        r = self.base(); g = r["stages"]["g2"]
        g["roster"].append(copy.deepcopy(g["roster"][0]))
        self.check(r, "DUPLICATE_ROSTER_REFERENCE_VERIFY")

if __name__ == "__main__":
    unittest.main()
