"""E/T020 synthesized receipt-to-G2 overlay erratum, existing ID only.

Research: E-AUDIT-20261021-2345-CNB02-RECEIPT-PROVENANCE-GATE-01.
This is historical synthetic validation, NOT native Golden, MATCH or READY.
Legacy source and original PC reports stay unchanged.
"""
import copy
import unittest
import t020_cnb02_receipt_provenance_gate_20261021_2345 as legacy
import t020_cnb02_g2_roster_role_coverage_overlay_20261026_09H as roles
import t020_cnb02_g2_placeholder_identity_review_20261026_13H as identity

# Preserve explicit legacy rejection/not-run/comparison-lacking states; no overlay may erase them.
HARD_STATES = frozenset({
    "INELIGIBLE", "DESIGNED_NOT_RUN", "REJECT_SOURCE", "REJECT_EVIDENCE",
    "VERIFY", "REJECT_DOUBLE_COMMIT", "NO_STRICT_COMPARISON",
})


def review_receipt(receipt):
    """Apply post-2026-10-21 G2 diagnostics; never promote a legacy schema gate."""
    old = legacy.gate(receipt)
    g2 = receipt.get("stages", {}).get("g2")
    g2 = g2 if isinstance(g2, dict) else {}
    issues = sorted(set(roles.review(g2)["issues"]) |
                    set(identity.review(g2)["issues"]))
    status = (old if old in HARD_STATES else
              "G2_REVIEW_REQUIRED" if issues else "SCHEMA_ONLY_NOT_GOLDEN")
    return {"legacy_verdict": old, "g2_issues": issues, "status": status,
            "actual_golden_pass": False, "strict_match": False,
            "new_formal_ready": False}


class ReceiptG2ErratumTests(unittest.TestCase):
    def base(self):
        return legacy.ReceiptProvenanceTests().base()

    def test_legacy_false_eligible_defense_missing(self):
        r = self.base()
        r["synthetic"] = False
        self.assertEqual(legacy.gate(r), "ELIGIBLE_FOR_REVIEW_NOT_MATCH")
        o = review_receipt(r)
        self.assertIn("NO_DEFENSE_ROSTER_RECEIPT", o["g2_issues"])
        self.assertEqual(o["status"], "G2_REVIEW_REQUIRED")

    def test_missing_attack_receipt(self):
        r = self.base()
        r["stages"]["g2"]["roster"][0]["side"] = "defense"
        self.assertIn("NO_ATTACK_ROSTER_RECEIPT", review_receipt(r)["g2_issues"])

    def test_placeholder_visible_identity(self):
        r = self.base()
        r["stages"]["g2"]["roster"][0]["unit_visible"] = "unknown"
        self.assertIn("G2_UNIT_ID_PLACEHOLDER_REVIEW", review_receipt(r)["g2_issues"])

    def test_cross_role_alias_review(self):
        r = self.base()
        r["stages"]["g2"]["roster"].append(
            {"side": "defense", "unit_visible": "u1", "troop_visible": "t1"})
        self.assertIn("CROSS_ROLE_VISIBLE_PAIR_ALIAS_REVIEW",
                      review_receipt(r)["g2_issues"])

    def test_static_map_label_unqualified(self):
        self.assertIn("MAP_ID_UNVERIFIED", review_receipt(self.base())["g2_issues"])

    def test_two_combat_rows_still_not_golden(self):
        r = self.base()
        r["stages"]["g2"]["map_id"] = "s16-unverified-label"
        r["stages"]["g2"]["roster"].append(
            {"side": "defense", "unit_visible": "ud", "troop_visible": "td"})
        out = review_receipt(r)
        self.assertEqual(out["g2_issues"], [])
        self.assertEqual(out["status"], "SCHEMA_ONLY_NOT_GOLDEN")
        self.assertFalse(out["actual_golden_pass"])
        self.assertFalse(out["strict_match"])
        self.assertFalse(out["new_formal_ready"])

    def test_double_commit_not_promoted(self):
        r = self.base()
        r["commit_paths"] = ["native", "new_api"]
        out = review_receipt(r)
        self.assertEqual(out["legacy_verdict"], "REJECT_DOUBLE_COMMIT")
        self.assertEqual(out["status"], "REJECT_DOUBLE_COMMIT")
        self.assertFalse(out["new_formal_ready"])

    def test_not_observed_not_promoted(self):
        r = self.base()
        r["old_observed"] = False
        out = review_receipt(r)
        self.assertEqual(out["legacy_verdict"], "DESIGNED_NOT_RUN")
        self.assertEqual(out["status"], "DESIGNED_NOT_RUN")
        self.assertFalse(out["actual_golden_pass"])

    def test_missing_new_capture_retains_comparison_block(self):
        r = self.base()
        r["new_capture_sha"] = None
        out = review_receipt(r)
        self.assertEqual(out["legacy_verdict"], "NO_STRICT_COMPARISON")
        self.assertEqual(out["status"], "NO_STRICT_COMPARISON")
        self.assertFalse(out["strict_match"])

    def test_does_not_mutate_receipt(self):
        r = self.base()
        original = copy.deepcopy(r)
        review_receipt(r)
        self.assertEqual(r, original)


if __name__ == "__main__":
    unittest.main()
