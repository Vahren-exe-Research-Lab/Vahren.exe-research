"""E-owned T020: archived G0 Watch vs Stage13 snapshot provenance gate.
STATIC archival analysis only; no original game, hook, or repo mutation.
"""
import copy
import hashlib
import json
from pathlib import Path
import unittest

IDX = Path(__file__).resolve().parents[1] / "rea_lab" / "headless_analysis" / "search_index"
G0 = "BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json"
W1 = "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl"
W1_READY = "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z_READY.json"
W2 = "BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl"
W2_READY = "BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z_READY.json"
ST13 = "BATTLE_STAGE13_INPUT_COVERAGE_20261022.json"
REQ13 = "BATTLE_STAGE13_PACKET_REQUIREMENTS_20261022.json"
SOURCE_PINS = {
    G0: "87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C",
    ST13: "17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB",
    REQ13: "42BE6B86723AA4CD66CF3D59DE93066820F6D3D5EF58F01E548D8685681A57D5",
}

def load(name):
    return json.loads((IDX / name).read_text(encoding="utf-8"))

def digest(name):
    return hashlib.sha256((IDX / name).read_bytes()).hexdigest().upper()

def gate(snapshot, g0):
    if snapshot["pid"] != g0["native_process_pid"]:
        return "DIFFERENT_NATIVE_PROCESS"
    if snapshot.get("g0_watch_sha") != g0["evidence_sha256"]:
        return "NO_SAME_BATTLE_RECEIPT"
    required = ("prebattle_save_sha", "runtime_map_receipt",
                "three_side_roster_receipt", "ordered_unit_troop_receipt")
    if not all(snapshot.get(k) for k in required):
        return "INCOMPLETE_G1_G2"
    return "REVIEW_NOT_AUTOMATIC_GOLDEN"

class Stage13CrossrunEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g0, cls.st13, cls.req = load(G0), load(ST13), load(REQ13)

    def test_input_document_byte_pins(self):
        for name, expected in SOURCE_PINS.items():
            self.assertEqual(digest(name), expected, name)

    def test_real_g0_watch1_binding(self):
        self.assertEqual(digest(W1), self.g0["evidence_sha256"])
        self.assertEqual(digest(W1_READY), self.g0["evidence_ready_sha256"])
        self.assertEqual(self.g0["native_process_pid"], 23272)
        self.assertFalse(self.g0["battle_packet_complete"])

    def test_watch2_not_aliased_by_same_pid_and_ready_id(self):
        r1, r2 = load(W1_READY), load(W2_READY)
        self.assertEqual(r1["pid"], r2["pid"])
        self.assertEqual(r1["id"], r2["id"])
        self.assertNotEqual(digest(W1), digest(W2))
        self.assertNotEqual(digest(W1_READY), digest(W2_READY))
        self.assertNotEqual(digest(W2), self.g0["evidence_sha256"])

    def test_stage13_samples_are_two_other_processes(self):
        rows = self.st13["capture_reports"]
        self.assertEqual(len(rows), 8)
        self.assertEqual({r["pid"] for r in rows}, {28432, 32468})
        self.assertEqual(len({r["session"] for r in rows}), 2)
        self.assertNotIn(self.g0["native_process_pid"], {r["pid"] for r in rows})
        self.assertEqual(sum(r["unit_coverage"]["record_reference"]["unit_observations"]
                             for r in rows), 4190)
        self.assertEqual(self.st13["total_unit_observations"], 4190)

    def test_third_side_does_not_prove_deployed_support(self):
        for r in self.st13["capture_reports"]:
            roles = {x["power_role"]: x for x in r["role_bindings"]}
            self.assertEqual(roles["other_or_empty"]["power_ptr"], "0x0")
            self.assertNotIn("support", roles)
        self.assertFalse(self.st13["full_G1_proven"])

    def test_actual_map_and_prebattle_packet_not_captured(self):
        groups = {x["name"]: x for x in self.req["minimum_groups"]}
        self.assertIn("NO captured", groups["runtime_map"]["current"])
        self.assertFalse(self.req["full_G1_proven"])
        self.assertFalse(self.req["external_roundtrip_proven"])

    def test_synthetic_pid_collision_does_not_promote_golden(self):
        for r in self.st13["capture_reports"]:
            self.assertEqual(gate(r, self.g0), "DIFFERENT_NATIVE_PROCESS")
        forged = copy.deepcopy(self.st13["capture_reports"][0])
        forged["pid"] = self.g0["native_process_pid"]
        self.assertEqual(gate(forged, self.g0), "NO_SAME_BATTLE_RECEIPT")
        forged["g0_watch_sha"] = self.g0["evidence_sha256"]
        self.assertEqual(gate(forged, self.g0), "INCOMPLETE_G1_G2")

if __name__ == "__main__":
    unittest.main(verbosity=2)