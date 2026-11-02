"""E T020: read-only historical stage8 recorder dependency contract audit.
Never invokes game, process readers, or any other owner module.
"""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "rea_lab" / "headless_analysis" / "search_index"
HASHES = {
    "battle_native_bounded_transition_watch_stage8_20261021.py": "1D4193E82899B9B794766AC0B60AFCF0D0FFD7B16E4ACC711451BD6D0F3031B8",
    "battle_native_bounded_transition_watch_stage8_v2_20261021.py": "B77F4B94EA2817D4957E3029E2B0AD5EBF65233C90BC6B084A33062D38CD5DE8",
    "battle_native_detached_capture_stage7_20261021.py": "C12406B3644B3B80A5423E141592CC4558561C89EC762A3C313DB16937A375B2",
    "battle_native_detached_capture_v5_20261021.py": "BF38D2713DB206B1C5142FE7A958119411A5AAD0405F3EFA9B377C969FD9ED5F",
    "battle_native_detached_capture_v6_20261022.py": "28799AF6FFF5059B2C53A7EB6BD4D0416FAA6084D902623A4C7849060327276F",
    "battle_native_detached_capture_v7_20261022.py": "C8E590CB1ECD69CD18E30164F7DEA74BC6DB29D80C9FCB57991A3F567053126F",
    "battle_native_readonly_live_probe_stage6_20261021.py": "E64634E6B18DCFD06CFE9740F0C80B7AACD8FA8CAD8D686288C6DD02ED32F685",
    "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl": "9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7",
    "BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl": "1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46",
}

def verified(name):
    raw = (ROOT / name).read_bytes()
    assert hashlib.sha256(raw).hexdigest().upper() == HASHES[name], name
    return raw.decode("utf-8")
class HistoricalRecorderContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = {name: verified(name) for name in HASHES}

    def test_01_archive_source_hashes(self):
        self.assertEqual(len(self.src), 9)

    def test_02_original_recorder_backend_routes(self):
        self.assertIn("from battle_native_detached_capture_stage7_20261021 import capture,Reader",
                      self.src["battle_native_bounded_transition_watch_stage8_20261021.py"])
        self.assertIn("from battle_native_detached_capture_v5_20261021 import capture,Reader",
                      self.src["battle_native_bounded_transition_watch_stage8_v2_20261021.py"])

    def test_03_old_peek_rejects_84_byte_side(self):
        helper = self.src["battle_native_readonly_live_probe_stage6_20261021.py"]
        self.assertIn("not 0<size<=64:raise ValueError(\"Unbounded memory request\")", helper)
        for name in ("battle_native_detached_capture_stage7_20261021.py",
                     "battle_native_detached_capture_v5_20261021.py"):
            cap = self.src[name]
            self.assertIn("def read(self,address,n):return peek(self.handle,address,n)", cap)
            self.assertIn("cap.read(side,0x54)", cap)
        self.assertGreater(0x54, 64)

    def test_04_nil_offset_changes_between_versions(self):
        old = self.src["battle_native_detached_capture_stage7_20261021.py"]
        v5 = self.src["battle_native_detached_capture_v5_20261021.py"]
        self.assertIn('capture_tree(cap,E+0x1eed20,0x20', old)
        self.assertIn('capture_tree(cap,E+0x1eed20,0x21', v5)
        self.assertIn('capture_tree(cap,E+0x1eed30,0x18', old)
        self.assertIn('capture_tree(cap,E+0x1eed30,0x19', v5)
    def test_05_v6_v7_have_independent_large_read(self):
        for name in ("battle_native_detached_capture_v6_20261022.py",
                     "battle_native_detached_capture_v7_20261022.py"):
            code = self.src[name]
            self.assertIn("not 1<=n<=65536", code)
            self.assertIn("ReadMemory(self.handle,ctypes.c_void_p(address),out,n", code)
            self.assertIn("cap.read(side,0x54)", code)
            self.assertNotIn("def read(self,address,n):return peek(self.handle,address,n)", code)

    def test_06_saved_errors_are_backend_specific(self):
        a = "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl"
        b = "BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl"
        for name, total, error, reason in (
            (a, 234, "SnapshotError", "unexpected nil tree node"),
            (b, 85, "ValueError", "Unbounded memory request"),
        ):
            rows = [json.loads(x) for x in self.src[name].splitlines()]
            gap = [r for r in rows if r.get("kind") == "CAPTURE_VERIFY_GAP"]
            self.assertEqual(len(rows), total)
            self.assertEqual([x["attempt"] for x in gap], list(range(1,29)))
            self.assertEqual({(x["error_type"],x["reason"]) for x in gap},
                             {(error,reason)})

if __name__ == "__main__":
    unittest.main(verbosity=2)