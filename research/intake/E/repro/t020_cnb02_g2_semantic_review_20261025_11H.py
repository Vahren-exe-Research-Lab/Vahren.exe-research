"""E T020: conservative G2 semantic preflight; review only, NEVER Golden PASS."""
from copy import deepcopy
import unittest

import t020_cnb02_receipt_provenance_gate_20261021_2345 as receipts

gate = receipts.gate
sha_ok = receipts.sha_ok

SIDES = ("attack", "defense", "support")
PARENT_REVIEW = {"SYNTHETIC_SCHEMA_ONLY", "ELIGIBLE_FOR_REVIEW_NOT_MATCH"}
PLACEHOLDERS = {"observed-map", "static_unconfirmed_map", "unknown", "placeholder"}


def typed_label(v):
    return isinstance(v, str) and bool(v.strip())


def review_g2(receipt):
    """Report suspicious shapes, not origin, actual deployment, or equivalence."""
    parent = gate(receipt)
    flags = set()
    if parent not in PARENT_REVIEW:
        return dict(parent=parent, flags=["PARENT_NOT_REVIEWABLE"],
                    actual_golden_pass=False, strict_match=False)
    g2 = receipt["stages"]["g2"]
    map_id = g2.get("map_id")
    if not typed_label(map_id) or map_id.strip().lower() in PLACEHOLDERS:
        flags.add("MAP_ID_PLACEHOLDER_OR_INVALID")
    # A hex digest here is not proof of the native loaded map's identity.
    if not sha_ok(g2.get("map_capture_sha")):
        flags.add("NATIVE_MAP_BYTES_UNVERIFIED")
    else:
        flags.add("MAP_HASH_FORMAT_ONLY_NOT_PROOF")
    sides = g2["sides"]
    for side in ("attack", "defense"):
        if not sides[side]:
            flags.add("EMPTY_" + side.upper() + "_SIDE")
    for side in SIDES:
        if any(not typed_label(label) for label in sides[side]):
            flags.add("INVALID_SIDE_PARTICIPANT_LABEL")
    seen = set()
    represented = set()
    for row in g2["roster"]:
        side = row.get("side")
        if not isinstance(side, str) or side not in SIDES:
            flags.add("INVALID_ROSTER_SIDE")
        else:
            represented.add(side)
        if not typed_label(row.get("unit_visible")):
            flags.add("INVALID_UNIT_VISIBLE_ID")
        if not typed_label(row.get("troop_visible")):
            flags.add("INVALID_TROOP_VISIBLE_ID")
        # Duplicate *visible labels* may denote distinct native instances.
        if all(typed_label(row.get(k)) for k in ("unit_visible", "troop_visible")):
            key = (side, row["unit_visible"], row["troop_visible"])
            if key in seen:
                flags.add("DUPLICATE_VISIBLE_PAIR_REVIEW")
            seen.add(key)
    for side in ("attack", "defense"):
        if side not in represented:
            flags.add("NO_" + side.upper() + "_ROSTER_RECEIPT")
    # side lists may represent Powers, not Unit/Troop IDs; do NOT equate them.
    # No native save/recording or deployed roster identity is authenticated here.
    return dict(parent=parent, flags=sorted(flags),
                actual_golden_pass=False, strict_match=False)


def synthetic_candidate():
    r = receipts.ReceiptProvenanceTests().base()
    g2 = r["stages"]["g2"]
    g2["map_id"] = "s16"
    g2["sides"] = {"attack": ["po2"], "defense": ["po_target"], "support": []}
    g2["roster"] = [
        {"side": "attack", "unit_visible": "u_attack", "troop_visible": "t_attack"},
        {"side": "defense", "unit_visible": "u_defend", "troop_visible": "t_defend"},
    ]
    return r


class G2SemanticReviewTests(unittest.TestCase):
    def test_synthetic_baseline_is_not_golden(self):
        result = review_g2(synthetic_candidate())
        self.assertEqual(result["parent"], "SYNTHETIC_SCHEMA_ONLY")
        self.assertEqual(result["flags"], ["NATIVE_MAP_BYTES_UNVERIFIED"])
        self.assertFalse(result["actual_golden_pass"])
        self.assertFalse(result["strict_match"])

    def assert_flag(self, mutator, flag):
        r = synthetic_candidate()
        mutator(r["stages"]["g2"])
        self.assertIn(flag, review_g2(r)["flags"])
    def test_unknown_side(self):
        self.assert_flag(lambda g: g["roster"][0].update(side="neutral"),
                         "INVALID_ROSTER_SIDE")

    def test_numeric_side(self):
        self.assert_flag(lambda g: g["roster"][0].update(side=7),
                         "INVALID_ROSTER_SIDE")

    def test_empty_attack_and_defense(self):
        self.assert_flag(lambda g: g["sides"].update(attack=[], defense=[]),
                         "EMPTY_ATTACK_SIDE")

    def test_duplicate_visible_pair_requires_review_not_rejection(self):
        self.assert_flag(lambda g: g["roster"].append(deepcopy(g["roster"][0])),
                         "DUPLICATE_VISIBLE_PAIR_REVIEW")

    def test_unknown_map(self):
        self.assert_flag(lambda g: g.update(map_id="STATIC_UNCONFIRMED_MAP"),
                         "MAP_ID_PLACEHOLDER_OR_INVALID")

    def test_numeric_unit(self):
        self.assert_flag(lambda g: g["roster"][0].update(unit_visible=17),
                         "INVALID_UNIT_VISIBLE_ID")

    def test_numeric_troop(self):
        self.assert_flag(lambda g: g["roster"][0].update(troop_visible=42),
                         "INVALID_TROOP_VISIBLE_ID")

    def test_untyped_side_participant(self):
        self.assert_flag(lambda g: g["sides"]["attack"].append(7),
                         "INVALID_SIDE_PARTICIPANT_LABEL")
    def test_missing_support_is_parent_verify(self):
        r = synthetic_candidate()
        r["stages"]["g2"]["sides"].pop("support")
        result = review_g2(r)
        self.assertEqual(result["parent"], "VERIFY")
        self.assertEqual(result["flags"], ["PARENT_NOT_REVIEWABLE"])

    def test_support_empty_is_legitimate_shape(self):
        result = review_g2(synthetic_candidate())
        self.assertNotIn("EMPTY_SUPPORT_SIDE", result["flags"])

    def test_missing_defense_roster(self):
        self.assert_flag(lambda g: g["roster"].pop(),
                         "NO_DEFENSE_ROSTER_RECEIPT")

    def test_digest_shape_still_not_native_proof(self):
        self.assert_flag(lambda g: g.update(map_capture_sha="f" * 64),
                         "MAP_HASH_FORMAT_ONLY_NOT_PROOF")

    def test_non_synthetic_claim_never_matches(self):
        r = synthetic_candidate()
        r["synthetic"] = False
        result = review_g2(r)
        self.assertEqual(result["parent"], "ELIGIBLE_FOR_REVIEW_NOT_MATCH")
        self.assertFalse(result["actual_golden_pass"])
        self.assertFalse(result["strict_match"])

    def test_no_original_capture(self):
        r = synthetic_candidate()
        r["old_observed"] = False
        self.assertEqual(review_g2(r)["parent"], "DESIGNED_NOT_RUN")


if __name__ == "__main__":
    unittest.main()
