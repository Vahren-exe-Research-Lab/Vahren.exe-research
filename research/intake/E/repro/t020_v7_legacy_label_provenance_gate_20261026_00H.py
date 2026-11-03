"""E/T020 independent read-only provenance warning for a V7 collector with V5 CLI names.
No EXE/process access, no writer mutation, and never emits gameplay Golden PASS.
"""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "rea_lab" / "headless_analysis" / "search_index"
SRC = S / "battle_native_detached_capture_v7_20261022.py"
STAGE11 = S / "BATTLE_STAGE11_CROSSRUN_ANALYSIS_20261022.json"
V7_SHA = "C8E590CB1ECD69CD18E30164F7DEA74BC6DB29D80C9FCB57991A3F567053126F"
ORIGINAL_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def classify_label(filename, verified_collector_sha):
    """Classify filename provenance risk only; source SHA must be independently verified."""
    if verified_collector_sha != V7_SHA:
        return "COLLECTOR_SOURCE_UNVERIFIED"
    name = Path(filename).name.upper()
    if "V5" in name:
        return "V7_SOURCE_PINNED_BUT_V5_LEGACY_LABEL"
    if name.startswith("BATTLE_USER_") and "_RAW_" in name:
        return "V7_SOURCE_PINNED_ARCHIVED_RAW_NAME"
    return "V7_SOURCE_PINNED_OTHER_NAME_REVIEW"

class V7LegacyLabelProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = SRC.read_text(encoding="utf-8")
        cls.report = json.loads(STAGE11.read_text(encoding="utf-8"))

    def test_source_sha_is_actual_v7(self):
        self.assertEqual(sha(SRC), V7_SHA)

    def test_stage11_has_same_v7_source_hash_on_two_real_runs(self):
        self.assertEqual(self.report["original_exe_sha256"], ORIGINAL_SHA)
        self.assertEqual(len(self.report["runs"]), 2)
        for run in self.report["runs"]:
            self.assertEqual(run["capture_code_sha256"][SRC.name], V7_SHA)

    def test_source_self_labels_v7(self):
        self.assertIn('"collector_revision":"v7-task-null-slots"', self.src)

    def test_failure_receipt_uses_legacy_v5_id(self):
        self.assertIn('"BRIDGE-V5-READONLY-CAPTURE-BLOCKED"', self.src)
        self.assertIn('BATTLE_NATIVE_CAPTURE_V5_BLOCKED_', self.src)

    def test_success_receipt_uses_legacy_v5_filename(self):
        self.assertIn('BATTLE_NATIVE_DETACHED_V5_', self.src)

    def test_legacy_v5_name_does_not_override_verified_v7_source(self):
        self.assertEqual(classify_label("BATTLE_NATIVE_DETACHED_V5_123.json", sha(SRC)),
                         "V7_SOURCE_PINNED_BUT_V5_LEGACY_LABEL")

    def test_failure_id_is_not_collector_version_proof(self):
        self.assertEqual(classify_label("BATTLE_NATIVE_CAPTURE_V5_BLOCKED_123.json", V7_SHA),
                         "V7_SOURCE_PINNED_BUT_V5_LEGACY_LABEL")

    def test_unverified_sha_is_not_accepted(self):
        for claimed in (None, "", "0" * 64):
            self.assertEqual(classify_label("BATTLE_NATIVE_DETACHED_V5_123.json", claimed),
                             "COLLECTOR_SOURCE_UNVERIFIED")

    def test_archived_real_raw_uses_different_name_namespace(self):
        all_caps = [c for r in self.report["runs"] for c in r["captures"]]
        self.assertEqual(len(all_caps), 8)
        for cap in all_caps:
            self.assertTrue(cap["file"].startswith("BATTLE_USER_"))
            self.assertEqual(classify_label(cap["file"], V7_SHA),
                             "V7_SOURCE_PINNED_ARCHIVED_RAW_NAME")

    def test_no_golden_upgrade_from_collector_revision(self):
        all_caps = [c for r in self.report["runs"] for c in r["captures"]]
        self.assertTrue(all(not c["guard_stable"] for c in all_caps))
        self.assertTrue(all(c["counter_delta"] > 0 for c in all_caps))
        self.assertNotIn("GOLDEN_PASS", classify_label(all_caps[0]["file"], V7_SHA))

if __name__ == "__main__":
    unittest.main(verbosity=2)
