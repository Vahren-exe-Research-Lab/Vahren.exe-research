"""E/T020 synthesized receipt-to-G2 overlay erratum, existing ID only.

Research: E-AUDIT-20261021-2345-CNB02-RECEIPT-PROVENANCE-GATE-01.
This is historical synthetic validation, NOT native Golden, MATCH or READY.
Legacy source and original PC reports stay unchanged.
"""
import copy
import math
import unittest
import t020_cnb02_receipt_provenance_gate_20261021_2345 as legacy
import t020_cnb02_g2_roster_role_coverage_overlay_20261026_09H as roles
import t020_cnb02_g2_placeholder_identity_review_20261026_13H as identity

# Preserve explicit legacy rejection/not-run/comparison-lacking states; no overlay may erase them.
HARD_STATES = frozenset({
    "INELIGIBLE", "DESIGNED_NOT_RUN", "REJECT_SOURCE", "REJECT_EVIDENCE",
    "VERIFY", "REJECT_DOUBLE_COMMIT", "NO_STRICT_COMPARISON",
})


def receipt_clock_issues(receipt):
    """Shape/finite-time diagnostics only: not proof of clock continuity."""
    if not isinstance(receipt, dict):
        return ["RECEIPT_NOT_OBJECT"]
    stages = receipt.get("stages")
    if not isinstance(stages, dict):
        return ["STAGES_NOT_OBJECT"]
    issues = set()
    for key in legacy.STAGES:
        if key not in stages:
            continue  # The historical gate already reports missing stages.
        stage = stages[key]
        if not isinstance(stage, dict):
            issues.add("STAGE_NOT_OBJECT")
        elif isinstance(stage.get("t_ms"), float) and not math.isfinite(stage["t_ms"]):
            issues.add("NONFINITE_STAGE_CLOCK")
    return sorted(issues)


def review_receipt(receipt):
    """Add G2 and clock diagnostics without promoting historic schema receipts."""
    clocks = receipt_clock_issues(receipt)
    try:
        old = legacy.gate(receipt)
    except (AttributeError, KeyError, TypeError):
        # Malformed imported receipts must not crash a later Golden intake.
        old = "REJECT_EVIDENCE"
    stages = receipt.get("stages") if isinstance(receipt, dict) else None
    g2 = stages.get("g2") if isinstance(stages, dict) else {}
    g2 = g2 if isinstance(g2, dict) else {}
    issues = sorted(set(roles.review(g2)["issues"]) |
                    set(identity.review(g2)["issues"]))
    status = (old if old in HARD_STATES else
              "REJECT_EVIDENCE" if clocks else
              "G2_REVIEW_REQUIRED" if issues else "SCHEMA_ONLY_NOT_GOLDEN")
    return {"legacy_verdict": old, "g2_issues": issues,
            "source_issues": clocks, "status": status,
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

    def test_nonfinite_g4_clock_rejected_despite_legacy_pass(self):
        r = self.base()
        r["stages"]["g4"]["t_ms"] = float("inf")
        self.assertEqual(legacy.gate(r), "SYNTHETIC_SCHEMA_ONLY")
        out = review_receipt(r)
        self.assertIn("NONFINITE_STAGE_CLOCK", out["source_issues"])
        self.assertEqual(out["status"], "REJECT_EVIDENCE")
        self.assertFalse(out["actual_golden_pass"])

    def test_nonfinite_g2_clock_not_hidden_by_legacy_rejection(self):
        r = self.base()
        r["stages"]["g2"]["t_ms"] = float("nan")
        out = review_receipt(r)
        self.assertIn("NONFINITE_STAGE_CLOCK", out["source_issues"])
        self.assertEqual(out["status"], "REJECT_EVIDENCE")

    def test_malformed_g4_stage_rejected_not_crash(self):
        r = self.base()
        r["stages"]["g4"] = None
        out = review_receipt(r)
        self.assertEqual(out["legacy_verdict"], "REJECT_EVIDENCE")
        self.assertIn("STAGE_NOT_OBJECT", out["source_issues"])
        self.assertEqual(out["status"], "REJECT_EVIDENCE")

    def test_malformed_stages_rejected_not_crash(self):
        r = self.base()
        r["stages"] = None
        out = review_receipt(r)
        self.assertIn("STAGES_NOT_OBJECT", out["source_issues"])
        self.assertEqual(out["status"], "REJECT_EVIDENCE")

    def test_missing_whole_receipt_rejected_not_crash(self):
        out = review_receipt(None)
        self.assertIn("RECEIPT_NOT_OBJECT", out["source_issues"])
        self.assertEqual(out["status"], "REJECT_EVIDENCE")

    def test_double_commit_keeps_primary_rejection_with_bad_clock(self):
        r = self.base()
        r["stages"]["g4"]["t_ms"] = float("inf")
        r["commit_paths"] = ["native", "new_api"]
        out = review_receipt(r)
        self.assertEqual(out["legacy_verdict"], "REJECT_DOUBLE_COMMIT")
        self.assertEqual(out["status"], "REJECT_DOUBLE_COMMIT")
        self.assertIn("NONFINITE_STAGE_CLOCK", out["source_issues"])

    def test_valid_clock_sequence_unaffected(self):
        r = self.base()
        r["stages"]["g1"]["t_ms"] = 5
        out = review_receipt(r)
        self.assertEqual(out["source_issues"], [])
        self.assertEqual(out["status"], "G2_REVIEW_REQUIRED")

    def test_does_not_mutate_receipt(self):
        r = self.base()
        original = copy.deepcopy(r)
        review_receipt(r)
        self.assertEqual(r, original)


if __name__ == "__main__":
    unittest.main()
