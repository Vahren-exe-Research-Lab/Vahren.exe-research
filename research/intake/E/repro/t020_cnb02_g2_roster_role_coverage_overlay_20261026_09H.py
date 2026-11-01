"""E-only G2 role-presence overlay. Synthetic diagnostics; NEVER a native Golden gate."""
import copy
import unittest
import t020_cnb02_g2_roster_shape_diagnostic_20261026_08H as shape08
import t020_cnb02_g2_semantic_review_20261025_11H as semantic11

COMBAT = ("attack", "defense")

def review(g2):
    base = shape08.review(g2)
    issues = set(base["issues"])
    represented = set()
    if isinstance(g2, dict) and isinstance(g2.get("roster"), list):
        for row in g2["roster"]:
            if not isinstance(row, dict):
                continue
            role = row.get("side")
            if (role in COMBAT and isinstance(role, str)
                    and shape08.ident(row.get("unit_visible"))
                    and shape08.ident(row.get("troop_visible"))):
                represented.add(role)
    for role in COMBAT:
        if role not in represented:
            issues.add("NO_" + role.upper() + "_ROSTER_RECEIPT")
    return {"verdict": "VERIFY_NOT_GOLDEN", "issues": sorted(issues),
            "coverage": "ROLE_PRESENCE_ONLY_NOT_NATIVE_MEMBERSHIP",
            "actual_golden_pass": False, "strict_match": False}

class RoleCoverageTests(unittest.TestCase):
    def base(self):
        return {"map_id": "s16",
                "sides": {"attack": ["po2"], "defense": ["target"], "support": []},
                "roster": [
                    {"side": "attack", "unit_visible": "ua", "troop_visible": "ta"},
                    {"side": "defense", "unit_visible": "ud", "troop_visible": "td"}]}
    def check(self, g2, flag):
        out = review(g2)
        self.assertIn(flag, out["issues"])
        self.assertFalse(out["actual_golden_pass"])
        self.assertFalse(out["strict_match"])
    def test_earlier_11h_detected_missing_defense(self):
        receipt = semantic11.synthetic_candidate()
        receipt["stages"]["g2"]["roster"] = receipt["stages"]["g2"]["roster"][:1]
        self.assertIn("NO_DEFENSE_ROSTER_RECEIPT",
                      semantic11.review_g2(receipt)["flags"])
    def test_08h_attack_only_shape_is_still_non_golden(self):
        g2 = self.base()
        g2["roster"] = g2["roster"][:1]
        self.assertEqual(shape08.review(g2)["verdict"], "VERIFY_NOT_GOLDEN")
        self.check(g2, "NO_DEFENSE_ROSTER_RECEIPT")
    def test_missing_attack_receipt(self):
        g2 = self.base()
        g2["roster"] = g2["roster"][1:]
        self.check(g2, "NO_ATTACK_ROSTER_RECEIPT")
    def test_both_roles_present(self):
        out = review(self.base())
        self.assertFalse(any(x.startswith("NO_") for x in out["issues"]))
        self.assertEqual(out["verdict"], "VERIFY_NOT_GOLDEN")
    def test_numeric_defense_unit_cannot_satisfy_role(self):
        g2 = self.base()
        g2["roster"][1]["unit_visible"] = 4
        self.check(g2, "NO_DEFENSE_ROSTER_RECEIPT")
        self.check(g2, "ROSTER_IDS_NOT_TEXT")
    def test_nonexistent_role_cannot_satisfy_defense(self):
        g2 = self.base()
        g2["roster"][1]["side"] = "neutral"
        self.check(g2, "NO_DEFENSE_ROSTER_RECEIPT")
    def test_support_empty_allowed_when_combat_roles_present(self):
        out = review(self.base())
        self.assertNotIn("SIDE_SCHEMA", out["issues"])
        self.assertNotIn("NO_SUPPORT_ROSTER_RECEIPT", out["issues"])
    def test_no_roster_flags_both_unproven(self):
        g2 = self.base()
        g2["roster"] = []
        self.check(g2, "NO_ATTACK_ROSTER_RECEIPT")
        self.check(g2, "NO_DEFENSE_ROSTER_RECEIPT")
    def test_fake_hashes_never_promote(self):
        g2 = self.base()
        g2.update(map_sha="a"*64, capture_sha="b"*64, old_observed=True)
        self.assertEqual(review(g2)["verdict"], "VERIFY_NOT_GOLDEN")
    def test_ids_are_not_assumed_equal_to_power_labels(self):
        g2 = self.base()
        out = review(g2)
        self.assertEqual(out["coverage"], "ROLE_PRESENCE_ONLY_NOT_NATIVE_MEMBERSHIP")
        self.assertFalse(out["actual_golden_pass"])
    def test_duplicate_pair_still_requires_review(self):
        g2 = self.base()
        g2["roster"].append(copy.deepcopy(g2["roster"][0]))
        self.check(g2, "DUPLICATE_ROSTER_REFERENCE_VERIFY")
    def test_malformed_input_is_not_golden(self):
        self.check(None, "NO_ATTACK_ROSTER_RECEIPT")

if __name__ == "__main__":
    unittest.main()
