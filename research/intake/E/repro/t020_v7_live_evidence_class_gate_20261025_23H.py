"""E/T020: archived original-game V7 evidence vs earlier failed watcher epochs; read-only."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "rea_lab" / "headless_analysis" / "search_index"
EXPECTED_EXE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
EXPECTED_V7 = "C8E590CB1ECD69CD18E30164F7DEA74BC6DB29D80C9FCB57991A3F567053126F"
WATCH = [
    ("BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl", "9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7"),
    ("BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl", "1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46"),
]
def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()
def load(name):
    return json.loads((S / name).read_text(encoding="utf-8"))

class V7EvidenceClassTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = load("BATTLE_STAGE11_CROSSRUN_ANALYSIS_20261022.json")
        cls.r = load("BATTLE_STAGE13_PACKET_REQUIREMENTS_20261022.json")
        cls.v6 = load("BATTLE_NATIVE_V6_WIDE_PREFLIGHT_15664_20261021T152712689663Z.json")
        cls.child = load("BATTLE_READER_V6_CROSSPROCESS_SELFTEST_20261022.json")
    def test_provenance_and_distinct_runs(self):
        self.assertEqual(self.a["original_exe_sha256"], EXPECTED_EXE)
        self.assertEqual(len(self.a["runs"]), 2)
        self.assertEqual({r["pid"] for r in self.a["runs"]}, {28432, 32468})
        self.assertEqual([r["structural_captures"] for r in self.a["runs"]], [4, 4])
        self.assertEqual([r["failure_attempts"] for r in self.a["runs"]], [1, 1])

    def test_v7_source_binds_real_runs(self):
        self.assertEqual(digest(S / "battle_native_detached_capture_v7_20261022.py"), EXPECTED_V7)
        for run in self.a["runs"]:
            self.assertEqual(run["capture_code_sha256"]["battle_native_detached_capture_v7_20261022.py"], EXPECTED_V7)

    def test_eight_raw_bytes_match_receipts(self):
        for run in self.a["runs"]:
            for cap in run["captures"]:
                with self.subTest(run=run["pid"], file=cap["file"]):
                    self.assertEqual(digest(S / cap["file"]), cap["sha256"])

    def test_native_structures_are_real_but_not_atomic(self):
        caps = [c for r in self.a["runs"] for c in r["captures"]]
        self.assertEqual(len(caps), 8)
        self.assertTrue(all(not c["guard_stable"] and c["counter_delta"] > 0 for c in caps))
        self.assertTrue(all(c["troops"] == [24, 24, 0] for c in caps))
        self.assertTrue(all(c["units"][2] == 0 for c in caps))

    def test_watcher_failure_epochs_are_distinct(self):
        for name, sha in WATCH:
            self.assertEqual(digest(S / name), sha)
            lines = (S / name).read_text(encoding="utf-8").splitlines()
            self.assertEqual(sum("CAPTURE_VERIFY_GAP" in line for line in lines), 28)
        self.assertTrue(all(run["pid"] != 23272 for run in self.a["runs"]))
    def test_v6_preflight_not_battle_G2(self):
        self.assertEqual(self.v6["game_event_mode"], 1)
        self.assertEqual(self.v6["battle_active"], 0)
        self.assertFalse(self.v6["actual_battle_start_packet_captured"])
        self.assertTrue(all(s["read_bytes"] == 84 for s in self.v6["checks"]["sides"]))

    def test_v6_child_process_not_original(self):
        self.assertEqual(self.child["reads_passed"], 8)
        self.assertEqual(self.child["reads_total"], 8)
        self.assertFalse(self.child["original_game_process_touched"])
        self.assertFalse(self.child["actual_native_battle_G1_packet"])

    def test_stage13_golden_preconditions_still_unmet(self):
        self.assertEqual(self.r["source_exe_sha256"], EXPECTED_EXE)
        self.assertFalse(self.r["full_G1_proven"])
        self.assertFalse(self.r["external_roundtrip_proven"])
        self.assertEqual(self.r["status"], "DESIGN_AND_RETAINED_BYTE_AUDIT_ONLY_NOT_G1_READY")

if __name__ == "__main__":
    unittest.main(verbosity=2)