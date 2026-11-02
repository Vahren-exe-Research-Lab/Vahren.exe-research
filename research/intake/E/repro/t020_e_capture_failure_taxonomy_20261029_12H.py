"""E-owned archival collector failure audit. Read-only; no process or game I/O."""
import hashlib
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "rea_lab" / "headless_analysis" / "search_index"
FIX = HERE / "T020_E_CAPTURE_FAILURE_TAXONOMY_FIXTURE_20261029_12H.json"

def pinned_obj(rec, name_key, hash_key):
    name = rec[name_key]
    if Path(name).name != name:
        raise ValueError("unsafe source filename")
    content = (SOURCE / name).read_bytes()
    if hashlib.sha256(content).hexdigest().upper() != rec[hash_key]:
        raise ValueError("source SHA mismatch: " + name)
    return json.loads(content.decode("utf-8-sig"))

class CollectorFailureAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = json.loads(FIX.read_text(encoding="utf-8-sig"))
        cls.s = {row["summary"]: row for row in cls.f["sessions"]}
        cls.b = {row["summary"]: pinned_obj(row, "summary", "summary_sha256") for row in cls.f["sessions"]}

    def test_summary_source_sha(self):
        self.assertEqual(len(self.s), 3)
        self.assertEqual(len(self.b), 3)

    def test_failure_byte_sha(self):
        for row in self.f["failures"]:
            with self.subTest(row["file"]):
                self.assertIsInstance(pinned_obj(row, "file", "sha256"), dict)

    def test_original_session_class(self):
        for name, meta in self.s.items():
            obj = self.b[name]
            self.assertEqual(obj["origin"], "LIVE_ORIGINAL_READONLY")
            self.assertEqual(obj["status"], "BATTLE_RETURNED")
            self.assertEqual(obj["preflight"]["pid"], meta["pid"])
            self.assertFalse(obj["full_G1_proven"])
            self.assertEqual(obj["structural_captures"], meta["structural_captures"])
            self.assertEqual(obj["capture_failures"], meta["capture_failures"])

    def test_failure_status_is_collector_not_gameplay_bug(self):
        for row in self.f["failures"]:
            data = pinned_obj(row, "file", "sha256")
            self.assertEqual(data["stage"], "native_read")
            self.assertEqual(data["error_type"], "SnapshotError")
            self.assertEqual(data["reason"], row["reason"])
            self.assertIsNone(data["raw_snapshot_file"])
            self.assertFalse(row["is_old_gameplay_bug_proven"])
            self.assertFalse(row["g2_eligible"])

    def test_collector_source_sha_contract(self):
        for version, expected in self.f["collector_sha256"].items():
            path = SOURCE / ("battle_native_detached_capture_" + version + "_20261022.py")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest().upper(), expected)
        for name, meta in self.s.items():
            src = "battle_native_detached_capture_" + meta["collector"] + "_20261022.py"
            self.assertEqual(self.b[name]["code_sha256"][src], self.f["collector_sha256"][meta["collector"]])

    def test_v6_v7_null_slot_and_bound(self):
        v6 = (SOURCE / "battle_native_detached_capture_v6_20261022.py").read_text(encoding="utf-8-sig")
        v7 = (SOURCE / "battle_native_detached_capture_v7_20261022.py").read_text(encoding="utf-8-sig")
        self.assertIn("if not all(values)", v6)
        self.assertIn("if not allow_null and not all(values)", v7)
        self.assertIn("allow_null=True", v7)
        self.assertIn("max_tasks=2048", v7)
        self.assertIn("if count>limit:", v7)

    def test_failure_distribution_and_capture_counts(self):
        from collections import Counter
        freq = Counter(row["classification"] for row in self.f["failures"])
        self.assertEqual(freq, {"COLLECTOR_NULL_SLOT_REJECTION": 3, "COLLECTOR_VECTOR_SLOT_LIMIT": 2})
        self.assertEqual(sum(row["structural_captures"] for row in self.s.values()), 8)
        self.assertEqual(sum(row["capture_failures"] for row in self.s.values()), 5)
        self.assertEqual(len({row["file"] for row in self.f["failures"]}), 5)

    def test_no_golden_or_ready_escalation(self):
        self.assertEqual(set(self.f["golden"].values()), {0})
        self.assertTrue(all(not row["g2_eligible"] for row in self.f["failures"]))
        self.assertIn("NOT_NATIVE", self.f["status"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
