"""E/T020: cross-role visible Unit/Troop label alias review; synthetic only."""
import copy
import unittest
from collections import defaultdict
import t020_cnb02_g2_unhashable_role_failclosed_20261026_11H as prior11

ROLES = frozenset(("attack", "defense", "support"))
FLAGS = ("CROSS_ROLE_VISIBLE_PAIR_ALIAS_REVIEW",
         "CROSS_ROLE_VISIBLE_UNIT_ALIAS_REVIEW",
         "CROSS_ROLE_VISIBLE_TROOP_ALIAS_REVIEW")

def review(g2):
    upstream = prior11.review(g2)
    issues = set(upstream["issues"])
    pairs, units, troops = defaultdict(set), defaultdict(set), defaultdict(set)
    rows = g2.get("roster") if isinstance(g2, dict) else None
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        role, unit, troop = (row.get(k) for k in ("side", "unit_visible", "troop_visible"))
        if not isinstance(role, str) or role not in ROLES:
            continue
        if not all(isinstance(x, str) and x.strip() for x in (unit, troop)):
            continue
        pairs[(unit, troop)].add(role)
        units[unit].add(role)
        troops[troop].add(role)
    for mapping, flag in zip((pairs, units, troops), FLAGS):
        if any(len(role_set) > 1 for role_set in mapping.values()):
            issues.add(flag)
    return dict(upstream, issues=sorted(issues), verdict="VERIFY_NOT_GOLDEN",
                actual_golden_pass=False, strict_match=False,
                coverage="CROSS_ROLE_VISIBLE_LABEL_AMBIGUITY_ONLY")

class CrossRoleAliasTests(unittest.TestCase):
    def base(self):
        return prior11.parity10.old11.synthetic_candidate()["stages"]["g2"]
    def assert_flag(self, g2, flag):
        before = copy.deepcopy(g2)
        got = review(g2)
        self.assertEqual(g2, before)
        self.assertIn(flag, got["issues"])
        self.assertEqual(got["verdict"], "VERIFY_NOT_GOLDEN")
        self.assertFalse(got["actual_golden_pass"])
        self.assertFalse(got["strict_match"])

    def test_baseline_no_alias(self):
        self.assertFalse(set(review(self.base())["issues"]) & set(FLAGS))
    def test_prior_has_no_cross_role_alias_warning(self):
        g = self.base(); g["roster"][1].update(unit_visible="u_attack", troop_visible="t_attack")
        self.assertEqual(prior11.review(g)["issues"], [])
        self.assertIn(FLAGS[0], review(g)["issues"])
    def test_attack_defense_same_pair(self):
        g = self.base(); g["roster"][1].update(unit_visible="u_attack", troop_visible="t_attack")
        for flag in FLAGS: self.assert_flag(g, flag)
    def test_same_unit_different_troops(self):
        g = self.base(); g["roster"][1]["unit_visible"] = "u_attack"
        out = review(g)["issues"]
        self.assertIn(FLAGS[1], out); self.assertNotIn(FLAGS[0], out)
    def test_same_troop_different_units(self):
        g = self.base(); g["roster"][1]["troop_visible"] = "t_attack"
        out = review(g)["issues"]
        self.assertIn(FLAGS[2], out); self.assertNotIn(FLAGS[0], out)
    def test_attack_support_same_pair_needs_review(self):
        g = self.base(); g["roster"].append(dict(g["roster"][0], side="support"))
        self.assert_flag(g, FLAGS[0])
    def test_same_role_duplicate_still_from_previous(self):
        g = self.base(); g["roster"].append(dict(g["roster"][0]))
        self.assert_flag(g, "DUPLICATE_ROSTER_REFERENCE_VERIFY")
        self.assertFalse(set(review(g)["issues"]) & set(FLAGS))
    def test_nontext_id_fails_previous_and_no_alias(self):
        g = self.base(); g["roster"][1].update(unit_visible=4, troop_visible="t_attack")
        self.assert_flag(g, "ROSTER_IDS_NOT_TEXT")
        self.assertFalse(set(review(g)["issues"]) & set(FLAGS))
    def test_unhashable_role_still_fails_closed(self):
        g = self.base(); g["roster"][0]["side"] = ["attack"]
        self.assert_flag(g, "ROSTER_ROLE_UNHASHABLE_VERIFY")
    def test_non_object_input_fails_closed(self):
        out = review(None)
        self.assertEqual(out["verdict"], "VERIFY_NOT_GOLDEN")
        self.assertFalse(out["actual_golden_pass"])
    def test_distinct_case_is_not_equated_as_native_identity(self):
        g = self.base(); g["roster"][1].update(unit_visible="U_ATTACK", troop_visible="T_ATTACK")
        self.assertFalse(set(review(g)["issues"]) & set(FLAGS))

if __name__ == "__main__":
    unittest.main()
