"""E/T020 audit: archived 12H golden_eligible is not an original-Golden gate."""
import importlib.util
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE / "t020_t013_backlink_nonunique_gate_20261027_12H.py"
spec = importlib.util.spec_from_file_location("e_b12_helper", OLD)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
SOURCE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
FIELDS = ("runtime_receipt_sha", "g0_ui_sha", "g1_save_sha", "g1_input_sha",
          "g2_map_sha", "g2_three_side_sha", "g2_roster_sha", "new_capture_sha")

def candidate(**overrides):
    x = dict(synthetic=False, source_kind="ORIGINAL_RUNTIME", source_sha=SOURCE,
             g0_battle="r1/b1", g1_battle="r1/b1", g2_battle="r1/b1")
    x.update({k: "present" for k in FIELDS})
    x.update(overrides)
    return x

def strict_review_preflight(x):
    """Only reject invalid claims. Positive outcome NEVER equals Golden PASS."""
    if x.get("synthetic") is not False or x.get("source_kind") != "ORIGINAL_RUNTIME":
        return "NON_NATIVE_CLAIM"
    if x.get("source_sha") != SOURCE:
        return "SOURCE_MISMATCH"
    battle_ids = [x.get(k) for k in ("g0_battle", "g1_battle", "g2_battle")]
    if not all(battle_ids) or len(set(battle_ids)) != 1:
        return "BATTLE_IDENTITY_UNPROVEN"
    if any(not isinstance(x.get(k), str) or
           re.fullmatch(r"[0-9a-fA-F]{64}", x[k]) is None for k in FIELDS):
        return "INVALID_DIGEST_FORMAT"
    return "REVIEW_ONLY_BYTES_AND_LEGALITY_UNATTESTED"

class RegressionAudit(unittest.TestCase):
    def test_prior_accepts_placeholders(self):
        self.assertTrue(prior.golden_eligible(candidate()))
    def test_prior_accepts_cross_battle(self):
        self.assertTrue(prior.golden_eligible(candidate(g2_battle="r2/b9")))
    def test_prior_accepts_foreign_exe(self):
        self.assertTrue(prior.golden_eligible(candidate(source_sha="F" * 64)))
    def test_strict_rejects_placeholders(self):
        self.assertEqual(strict_review_preflight(candidate()), "INVALID_DIGEST_FORMAT")
    def test_strict_rejects_cross_battle(self):
        self.assertEqual(strict_review_preflight(candidate(g2_battle="r2/b9")), "BATTLE_IDENTITY_UNPROVEN")
    def test_strict_rejects_foreign_source(self):
        self.assertEqual(strict_review_preflight(candidate(source_sha="F" * 64)), "SOURCE_MISMATCH")
    def test_strict_rejects_unlabelled_battle(self):
        self.assertEqual(strict_review_preflight(candidate(g1_battle=None)), "BATTLE_IDENTITY_UNPROVEN")
    def test_even_shaped_receipts_cannot_pass_gold(self):
        shaped = candidate(**{k: "A" * 64 for k in FIELDS})
        self.assertEqual(strict_review_preflight(shaped), "REVIEW_ONLY_BYTES_AND_LEGALITY_UNATTESTED")
        self.assertTrue(prior.golden_eligible(shaped))

if __name__ == "__main__":
    unittest.main(verbosity=2)
