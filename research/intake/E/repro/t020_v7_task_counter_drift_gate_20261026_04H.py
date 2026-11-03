"""E/T020: V7 snapshot GameTask-counter drift from archived original RAW; no Golden promotion."""
import hashlib
import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "rea_lab" / "headless_analysis" / "search_index"
STAGE12 = BASE / "BATTLE_STAGE12_WAR_SIDE_CROSSWALK_20261022.json"
PIN = "9BC09C7EC861C5E21068ADD274534BD88685BAA1AB1EF780C8B1E3BD4B06EB8E"
EXPECTED = {
    "9cddfc86": [26, 19, 68, 55],
    "b8419f5d": [21, 34, 77, 101],
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def decode_hex_le(value, nbytes):
    binary = bytes.fromhex(value)
    if len(binary) != nbytes:
        raise ValueError("invalid native field width")
    return int.from_bytes(binary, "little")

def guards(raw):
    keys = ("capture_guard_before_task_counter_mode_active_attack",
            "capture_guard_after_task_counter_mode_active_attack")
    result = []
    for key in keys:
        values = raw[key]
        if len(values) != 4:
            raise ValueError("counter/mode/active/attack guard width")
        result.append([decode_hex_le(v, n) for v, n in zip(values, (4, 4, 1, 4))])
    return result

def drift(raw):
    before, after = guards(raw)
    return after[0] - before[0] if after[0] >= before[0] else None

def evidence_gate(raw):
    # Even a stable sampled counter is not a simultaneous atomic state proof.
    if drift(raw) is None:
        return "COUNTER_ORDER_VERIFY"
    if drift(raw) > 0:
        return "COUNTER_DRIFT_NOT_ATOMIC"
    return "STABLE_COUNTER_STILL_VERIFY"

class V7TaskCounterDriftGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(STAGE12.read_text(encoding="utf-8"))
        cls.rows = [(c, json.loads((BASE / c["source"]).read_text(encoding="utf-8")))
                    for c in cls.doc["captures"]]

    def test_eight_source_sha_and_session_separation(self):
        self.assertEqual(digest(STAGE12), PIN)
        self.assertEqual(len(cls_rows := self.rows), 8)
        self.assertEqual(len({c["session"] for c, _ in cls_rows}), 2)
        for c, _ in cls_rows:
            self.assertEqual(digest(BASE / c["source"]), c["source_sha256"])

    def test_little_endian_counter_decode(self):
        c, raw = self.rows[0]
        self.assertEqual(guards(raw)[0], [63, 2, 1, 3])
        self.assertEqual(guards(raw)[1], [89, 2, 1, 3])
        self.assertEqual(drift(raw), 26)

    def test_exact_within_capture_deltas(self):
        groups = {key: [] for key in EXPECTED}
        for c, raw in self.rows:
            tail = c["session"].split("_")[-1]
            groups[tail].append(drift(raw))
        self.assertEqual(groups, EXPECTED)
        self.assertEqual(sum(sum(v) for v in groups.values()), 401)
        self.assertEqual((min(v for g in groups.values() for v in g),
                          max(v for g in groups.values() for v in g)), (19, 101))

    def test_stable_phase_flags_do_not_imply_stable_snapshot(self):
        for c, raw in self.rows:
            before, after = guards(raw)
            self.assertEqual(before[1:], after[1:])
            self.assertEqual(before[1:], [2, 1, 3])
            self.assertEqual(evidence_gate(raw), "COUNTER_DRIFT_NOT_ATOMIC")

    def test_missing_golden_bindings_preserved(self):
        self.assertFalse(self.doc["full_G1_proven"])
        for c, raw in self.rows:
            self.assertFalse(c["atomic"])
            self.assertFalse(raw["recorder_provenance"]["atomic"])
            self.assertFalse(raw["native_task_fully_frozen_proven"])
            self.assertIsNone(raw["capture_context"]["selected_map_sha256"])
            self.assertIsNone(raw["capture_context"]["vm_cursor"])

    def test_synthetic_zero_drift_never_promotes_to_g2(self):
        _, raw = self.rows[0]
        synthetic = dict(raw)
        synthetic["capture_guard_after_task_counter_mode_active_attack"] = list(
            raw["capture_guard_before_task_counter_mode_active_attack"])
        self.assertEqual(drift(synthetic), 0)
        self.assertEqual(evidence_gate(synthetic), "STABLE_COUNTER_STILL_VERIFY")

if __name__ == "__main__":
    unittest.main(verbosity=2)
