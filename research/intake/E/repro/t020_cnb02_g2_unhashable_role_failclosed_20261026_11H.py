"""T020/E: fail-closed JSON G2 diagnostics for unhashable roster-side shapes."""
import copy
import unittest
import t020_cnb02_g2_cross_generation_parity_guard_20261026_10H as parity10

def review(g2):
    """Diagnose malformed JSON without mutating input or claiming native proof."""
    safe = g2
    extra = set()
    if isinstance(g2, dict) and isinstance(g2.get("roster"), list):
        rows = list(g2["roster"])
        for i, row in enumerate(rows):
            if isinstance(row, dict):
                role = row.get("side")
                if isinstance(role, (list, dict)):
                    extra.add("ROSTER_ROLE_UNHASHABLE_VERIFY")
                    rows[i] = dict(row, side=None)
        safe = dict(g2, roster=rows)
    result = parity10.review(safe)
    return dict(result, issues=sorted(set(result["issues"]) | extra),
                verdict="VERIFY_NOT_GOLDEN", actual_golden_pass=False,
                strict_match=False, coverage="JSON_SHAPE_ONLY_NOT_NATIVE")

class FailClosedTests(unittest.TestCase):
    def base(self):
        return parity10.old11.synthetic_candidate()["stages"]["g2"]
    def check(self, role, flag):
        g2 = self.base(); g2["roster"][0]["side"] = role
        before = copy.deepcopy(g2); out = review(g2)
        self.assertEqual(g2, before)
        self.assertIn(flag, out["issues"])
        self.assertFalse(out["actual_golden_pass"])
        self.assertFalse(out["strict_match"])
    def test_list_role(self):
        self.check(["attack"], "ROSTER_ROLE_UNHASHABLE_VERIFY")
    def test_object_role(self):
        self.check({"role":"attack"}, "ROSTER_ROLE_UNHASHABLE_VERIFY")
    def test_empty_list_role(self):
        self.check([], "ROSTER_ROLE_UNHASHABLE_VERIFY")
    def test_unknown_string_still_diagnosed(self):
        self.check("neutral", "ROSTER_ROLE_UNRECOGNIZED")
    def test_integer_still_diagnosed(self):
        self.check(7, "ROSTER_ROLE_UNRECOGNIZED")
    def test_missing_defense_preserved(self):
        g2 = self.base(); g2["roster"].pop()
        self.assertIn("NO_DEFENSE_ROSTER_RECEIPT", review(g2)["issues"])
    def test_map_placeholder_preserved(self):
        g2 = self.base(); g2["map_id"] = " UNKNOWN "
        self.assertIn("MAP_PLACEHOLDER_ALIAS_VERIFY", review(g2)["issues"])
    def test_normal_never_promoted(self):
        result = review(self.base())
        self.assertEqual(result["verdict"], "VERIFY_NOT_GOLDEN")
        self.assertEqual(result["issues"], [])
    def test_nonobject_row_still_diagnosed(self):
        g2 = self.base(); g2["roster"].append([])
        self.assertIn("ROSTER_ROW_NOT_OBJECT", review(g2)["issues"])
    def test_10h_list_role_exception_reproduced(self):
        g2 = self.base(); g2["roster"][0]["side"] = ["attack"]
        with self.assertRaises(TypeError):
            parity10.review(g2)
        self.assertIn("ROSTER_ROLE_UNHASHABLE_VERIFY", review(g2)["issues"])
    def test_10h_object_role_exception_reproduced(self):
        g2 = self.base(); g2["roster"][1]["side"] = {"role": "defense"}
        with self.assertRaises(TypeError):
            parity10.review(g2)
        self.assertIn("ROSTER_ROLE_UNHASHABLE_VERIFY", review(g2)["issues"])

if __name__ == "__main__":
    unittest.main()
