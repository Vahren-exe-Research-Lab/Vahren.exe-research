"""E/T018/T020 G2 synthetic declaration-vs-deployment gap guard.

Follow-on to EXISTING research ID E-OFFLINE-20261101-09H-T018-T020-G2-BIJECTION-ORDER-01.
This is a schema-only policy check of modeled receipts, not any newly recovered
original PC report, native source proof, independent original-game observation,
Golden, MATCH, READY, or a B-owner native finding.

It addresses a narrow gap in previously published E synthetic role-presence
checks: a well-shaped deployed combat row can coexist with an empty declared
attack/defense side list (or vice versa), without producing a relation warning.
Only existence is checked. Matching role labels DO NOT bind Power participants to
runtime Unit/Troop identities; that still needs independently attested same-run
original evidence and cannot be verified by this code.
"""
from __future__ import annotations

import copy
import unittest

ROLES = ("attack", "defense", "support")


def _label(value):
    return type(value) is str and bool(value.strip())


def review(g2):
    """Return conservative presence-mismatch diagnostics; never a native verdict."""
    result = {
        "classification": "SYNTHETIC_ROLE_RELATION_ONLY",
        "issues": [],
        "relation_attested": False,
        "actual_golden_pass": False,
        "strict_match": False,
        "ready": False,
    }
    issues = set()
    if type(g2) is not dict:
        issues.add("G2_NOT_OBJECT")
        result["issues"] = sorted(issues)
        return result
    sides, roster = g2.get("sides"), g2.get("roster")
    if type(sides) is not dict or set(sides) != set(ROLES):
        issues.add("SIDE_SCHEMA")
    if type(roster) is not list:
        issues.add("ROSTER_SCHEMA")
    if "SIDE_SCHEMA" in issues or "ROSTER_SCHEMA" in issues:
        result["issues"] = sorted(issues)
        return result

    declaration = {}
    for role in ROLES:
        participants = sides[role]
        if type(participants) is not list or not all(_label(v) for v in participants):
            issues.add("INVALID_SIDE_DECLARATION_" + role.upper())
            declaration[role] = None
        else:
            declaration[role] = bool(participants)
            if len(set(participants)) != len(participants):
                issues.add("DUPLICATE_SIDE_DECLARATION_" + role.upper())

    deployed = {role: False for role in ROLES}
    for row in roster:
        if type(row) is not dict:
            issues.add("ROSTER_ROW_UNTYPED")
            continue
        side = row.get("side")
        if not _label(side) or side not in ROLES:
            issues.add("ROSTER_SIDE_INVALID")
            continue
        if not _label(row.get("unit_visible")) or not _label(row.get("troop_visible")):
            issues.add("ROSTER_ROW_UNTYPED")
            continue
        deployed[side] = True

    for role in ROLES:
        if declaration[role] is True and not deployed[role]:
            issues.add("DECLARED_WITHOUT_DEPLOYED_" + role.upper())
        elif declaration[role] is False and deployed[role]:
            issues.add("DEPLOYED_WITHOUT_DECLARED_" + role.upper())

    result["issues"] = sorted(issues)
    return result


class DeclaredVsDeployedSyntheticTests(unittest.TestCase):
    @staticmethod
    def baseline():
        return {
            "map_id": "synthetic-map-label",
            "sides": {"attack": ["power-a"], "defense": ["power-d"], "support": []},
            "roster": [
                {"side": "attack", "unit_visible": "unit-a", "troop_visible": "troop-a"},
                {"side": "defense", "unit_visible": "unit-d", "troop_visible": "troop-d"},
            ],
        }

    def check(self, candidate, *flags):
        snapshot = copy.deepcopy(candidate)
        r = review(candidate)
        self.assertEqual(candidate, snapshot)
        self.assertEqual(r["classification"], "SYNTHETIC_ROLE_RELATION_ONLY")
        for key in ("relation_attested", "actual_golden_pass", "strict_match", "ready"):
            self.assertIs(r[key], False)
        for flag in flags:
            self.assertIn(flag, r["issues"])
        return r

    def test_01_baseline_shape_is_not_native_proof(self):
        self.assertEqual(self.check(self.baseline())["issues"], [])

    def test_02_declared_attack_no_deployed_attack(self):
        g = self.baseline(); g["roster"].pop(0)
        self.check(g, "DECLARED_WITHOUT_DEPLOYED_ATTACK")

    def test_03_deployed_attack_no_declaration(self):
        g = self.baseline(); g["sides"]["attack"] = []
        self.check(g, "DEPLOYED_WITHOUT_DECLARED_ATTACK")

    def test_04_declared_defense_no_deployed_defense(self):
        g = self.baseline(); g["roster"].pop(1)
        self.check(g, "DECLARED_WITHOUT_DEPLOYED_DEFENSE")

    def test_05_deployed_defense_no_declaration(self):
        g = self.baseline(); g["sides"]["defense"] = []
        self.check(g, "DEPLOYED_WITHOUT_DECLARED_DEFENSE")

    def test_06_empty_support_optional(self):
        r = self.check(self.baseline())
        self.assertFalse(any("SUPPORT" in issue for issue in r["issues"]))

    def test_07_declared_support_no_deployment(self):
        g = self.baseline(); g["sides"]["support"] = ["support-power"]
        self.check(g, "DECLARED_WITHOUT_DEPLOYED_SUPPORT")

    def test_08_support_deployment_no_declaration(self):
        g = self.baseline()
        g["roster"].append({"side": "support", "unit_visible": "unit-s", "troop_visible": "troop-s"})
        self.check(g, "DEPLOYED_WITHOUT_DECLARED_SUPPORT")

    def test_09_support_both_present_still_unattested(self):
        g = self.baseline(); g["sides"]["support"] = ["support-power"]
        g["roster"].append({"side": "support", "unit_visible": "unit-s", "troop_visible": "troop-s"})
        self.assertEqual(self.check(g)["issues"], [])

    def test_10_attack_row_null_unit_cannot_count_as_deployment(self):
        g = self.baseline(); g["roster"][0]["unit_visible"] = None
        self.check(g, "ROSTER_ROW_UNTYPED", "DECLARED_WITHOUT_DEPLOYED_ATTACK")

    def test_11_defense_row_numeric_troop_does_not_count(self):
        g = self.baseline(); g["roster"][1]["troop_visible"] = 0
        self.check(g, "ROSTER_ROW_UNTYPED", "DECLARED_WITHOUT_DEPLOYED_DEFENSE")

    def test_12_unknown_roster_side_does_not_count(self):
        g = self.baseline(); g["roster"][0]["side"] = "neutral"
        self.check(g, "ROSTER_SIDE_INVALID", "DECLARED_WITHOUT_DEPLOYED_ATTACK")

    def test_13_missing_side_slot_precludes_relation_inference(self):
        g = self.baseline(); g["sides"].pop("support")
        self.check(g, "SIDE_SCHEMA")

    def test_14_nonlist_roster_precludes_relation_inference(self):
        g = self.baseline(); g["roster"] = {}
        self.check(g, "ROSTER_SCHEMA")

    def test_15_nonnative_raw_pointer_is_not_a_label(self):
        g = self.baseline(); g["sides"]["attack"] = [5]
        r = self.check(g, "INVALID_SIDE_DECLARATION_ATTACK")
        self.assertNotIn("DEPLOYED_WITHOUT_DECLARED_ATTACK", r["issues"])

    def test_16_blank_participant_is_not_empty_proof(self):
        g = self.baseline(); g["sides"]["defense"] = [" "]
        r = self.check(g, "INVALID_SIDE_DECLARATION_DEFENSE")
        self.assertNotIn("DEPLOYED_WITHOUT_DECLARED_DEFENSE", r["issues"])

    def test_17_duplicate_side_participant_requires_review(self):
        g = self.baseline(); g["sides"]["attack"] = ["power-a", "power-a"]
        self.check(g, "DUPLICATE_SIDE_DECLARATION_ATTACK")

    def test_18_roster_not_array_of_objects(self):
        g = self.baseline(); g["roster"].append("synthetic")
        self.check(g, "ROSTER_ROW_UNTYPED")

    def test_19_none_not_a_g2_object(self):
        self.check(None, "G2_NOT_OBJECT")

    def test_20_forged_observed_status_does_not_grant_native_proof(self):
        g = self.baseline(); g.update(old_observed=True, native_verified=True,
                                       actual_golden_pass=True, ready=True)
        self.assertEqual(self.check(g)["issues"], [])

    def test_21_empty_all_roles_and_roster_is_shape_only(self):
        g = self.baseline(); g["sides"] = dict.fromkeys(ROLES, [])
        g["roster"] = []
        self.assertEqual(self.check(g)["issues"], [])

    def test_22_declaration_missing_is_not_an_observed_absence(self):
        g = self.baseline(); g["sides"]["attack"] = None
        self.check(g, "INVALID_SIDE_DECLARATION_ATTACK")

    def test_23_two_combat_mismatches_can_coexist(self):
        g = self.baseline(); g["sides"]["attack"] = []; g["roster"].pop(1)
        self.check(g, "DEPLOYED_WITHOUT_DECLARED_ATTACK", "DECLARED_WITHOUT_DEPLOYED_DEFENSE")

    def test_24_no_power_to_unit_identity_mapping_is_claimed(self):
        g = self.baseline()
        g["sides"]["attack"] = ["power-unknown-but-nonempty"]
        self.assertEqual(self.check(g)["issues"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
