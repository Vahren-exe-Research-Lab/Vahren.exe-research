"""E T020: archived-original postbattle witness is not deployed G2 Golden."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
import unittest

ROOT = Path(__file__).resolve().parents[1]
IDX = ROOT / "rea_lab" / "headless_analysis" / "search_index"
CAP = "BATTLE_ORIGINAL_WAR_TREE_CAPTURE_V5_23272_20261021T144551063564Z.json"
DEC = "BATTLE_ORIGINAL_WAR_TREE_DECODE_V5_23272_20261021T144551063564Z.json"
W1 = "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl"
W2 = "BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"

def load(name):
    return json.loads((IDX / name).read_text(encoding="utf-8"))

def sha(name):
    return hashlib.sha256((IDX / name).read_bytes()).hexdigest().upper()

def watch(name):
    return [json.loads(line) for line in (IDX / name).read_text(encoding="utf-8").splitlines() if line]

def g2_proof_gaps(capture, decoded):
    """Necessary-evidence gaps ONLY; not a native trace or PASS validator."""
    gaps = []
    if capture.get("original_exe_sha256") != decoded.get("source_sha256"):
        gaps.append("SOURCE_EXE_MISMATCH")
    if "POSTBATTLE" in capture.get("capture_kind", "") or "POSTBATTLE" in decoded.get("source_kind", ""):
        gaps.append("POSTBATTLE_WITNESS")
    guard = capture.get("capture_guard_initial", {})
    if guard.get("mode") == 1 and guard.get("active") == 0:
        gaps.append("STRATEGY_GUARD_NOT_DEPLOYMENT")
    if capture.get("non_atomic_capture") or capture.get("capture_guard_stable_not_atomic_proof"):
        gaps.append("NONATOMIC_CAPTURE")
    if decoded.get("native_battle_start_packet_proven") is not True:
        gaps.append("NO_NATIVE_START_PACKET")
    if not capture.get("loaded_map_bytes_sha256"):
        gaps.append("NO_LOADED_MAP_BYTE_RECEIPT")
    if not capture.get("deployed_ordered_unit_troop_receipts"):
        gaps.append("NO_ORDERED_DEPLOYMENT_RECEIPT")
    return sorted(gaps)

def active_samples(rows):
    return [datetime.fromisoformat(e["utc"]) for e in rows
            if isinstance((s := e.get("snapshot") or e.get("state") or e.get("initial")), dict)
            and s.get("mode") == 2 and s.get("active") == 1]

class NativeArchiveBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = load(CAP)
        cls.d = load(DEC)
        cls.w1 = watch(W1)
        cls.w2 = watch(W2)
        cls.gaps = g2_proof_gaps(cls.c, cls.d)

    def test_saved_source_identity_is_consistent(self):
        self.assertEqual(self.c["original_exe_sha256"], EXE_SHA)
        self.assertEqual(self.d["source_sha256"], EXE_SHA)
        self.assertEqual(self.d["pid"], 23272)

    def test_postbattle_class_is_not_g2(self):
        self.assertIn("POSTBATTLE_WITNESS", self.gaps)
        self.assertEqual(self.c["capture_kind"], "ORIGINAL_GAME_POSTBATTLE_READONLY_WAR_TREE")

    def test_mode1_guard_does_not_show_deployed_roster(self):
        self.assertIn("STRATEGY_GUARD_NOT_DEPLOYMENT", self.gaps)
        self.assertEqual(self.c["capture_guard_final"]["active"], 0)

    def test_nonatomic_even_when_guard_stable(self):
        self.assertIn("NONATOMIC_CAPTURE", self.gaps)
        self.assertTrue(self.c["capture_guard_stable_not_atomic_proof"])

    def test_definition_pointers_are_not_native_packet(self):
        self.assertEqual(self.d["total_attack_definition_pointers"], 12)
        self.assertIn("NO_NATIVE_START_PACKET", self.gaps)

    def test_loaded_map_and_deployed_units_missing(self):
        self.assertIn("NO_LOADED_MAP_BYTE_RECEIPT", self.gaps)
        self.assertIn("NO_ORDERED_DEPLOYMENT_RECEIPT", self.gaps)

    def test_two_watchers_saved_no_completed_packets(self):
        self.assertEqual(self.w1[-1]["captures_saved"], 0)
        self.assertEqual(self.w2[-1]["captures_saved"], 0)
        self.assertEqual(self.w1[-1]["attempted_capture"], 28)
        self.assertEqual(self.w2[-1]["attempted_capture"], 28)

    def test_capture_filename_label_in_unobserved_gap(self):
        """Label timestamp is NOT an independently verified capture instant."""
        label = datetime(2026, 10, 21, 14, 45, 51, 63564, tzinfo=timezone.utc)
        a, b = active_samples(self.w1), active_samples(self.w2)
        self.assertTrue(a and b)
        self.assertLess(max(a), label)
        self.assertLess(label, min(b))

    def test_cross_source_mismatch_cannot_be_hidden(self):
        c = dict(self.c, original_exe_sha256="0" * 64)
        self.assertIn("SOURCE_EXE_MISMATCH", g2_proof_gaps(c, self.d))

    def test_no_false_actual_or_strict_status(self):
        self.assertTrue(self.gaps)
        self.assertNotIn("PASS", self.gaps)
        self.assertNotIn("MATCH", self.gaps)

if __name__ == "__main__":
    unittest.main()
