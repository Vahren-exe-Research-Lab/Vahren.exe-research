"""E T020 tree/direct flag provenance guard; synthetic only, NOT gameplay."""
import hashlib
import unittest
from pathlib import Path
from t020_t028_triflag_side_mode_provenance_gate_20261028_01H import route

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "b02": ("data/T028_TREE_FLAG_EXACT_MATCH_TO_BATTLE_SIDE_NATIVE_20261028_02H.md",
            "8BB642AB3A4B9180BF06597DE9F48074B2BD809908DB1393FCC1B51BE717050C"),
    "b01": ("data/T028_TRIFLAG_SIDE_MODE_PRODUCER_NATIVE_20261028_01H.md",
            "E2B8A6AC9D364ED314E247885D6B37BA7A1F8DEE22041B577EB1802EE98C5A5A"),
    "b00": ("data/T028_BATTLE_MODE_CONFIG_PRODUCER_NATIVE_20261028_00H.md",
            "D6708901880A1E7C85BE81C542027506546E443EDAF377E5E88577E4BB87AA36"),
}
UNKNOWN = object()

def uint8(v):
    return type(v) is int and 0 <= v <= 255

def candidate(path, *, reached=UNKNOWN, matched=UNKNOWN,
              node_flag=UNKNOWN, direct_gate=UNKNOWN):
    out = {"status": "VERIFY", "path": path, "write_candidate": None,
           "scratch_flag": None, "indexed_key_offset": None,
           "result_flag_offset": None, "owner_identity": None,
           "record_type": None, "native_join_proven": False,
           "gameplay_observed": False, "golden_pass": False,
           "strict_match": False}
    if path == "INDEX":
        out["indexed_key_offset"] = "+0x0C"
        if reached is not True:
            out["status"] = "VERIFY_INDEX_REACHABILITY"
            return out
        if type(matched) is not bool:
            out["status"] = "VERIFY_EXACT_MATCH"
            return out
        if matched:
            if not uint8(node_flag):
                out["status"] = "VERIFY_NODE_BYTE"
                return out
            value = node_flag
            out["result_flag_offset"] = "node+0x14"
        else:
            value = 0
        out["scratch_flag"] = value  # local [ESP+0x74]; not persistent
    elif path == "DIRECT":
        if not uint8(direct_gate):
            out["status"] = "VERIFY_DIRECT_GATE"
            return out
        if direct_gate == 0:
            out["status"] = "VERIFY_OTHER_PATH"
            return out
        if not uint8(node_flag):
            out["status"] = "VERIFY_NODE_BYTE"
            return out
        value = node_flag
        out["result_flag_offset"] = "direct+0x14"
    else:
        out["status"] = "VERIFY_SOURCE_PATH"
        return out
    out["status"] = "STATIC_LOCAL_CANDIDATE"
    out["write_candidate"] = "F54" if value != 0 else "F55"
    return out

def isolated_projection(result, *, all_other_writers_excluded=False,
                        player_raw=UNKNOWN, enemy_raw=UNKNOWN):
    # A local writer is NOT the complete manager state.
    if result["status"] != "STATIC_LOCAL_CANDIDATE":
        return {"status": "VERIFY_LOCAL", "mode": None, "side_slots": None}
    if not all_other_writers_excluded:
        return {"status": "VERIFY_AGGREGATE_WRITERS", "mode": None,
                "side_slots": None}
    from t020_t028_triflag_side_mode_provenance_gate_20261028_01H import ABSENT
    player = ABSENT if player_raw is UNKNOWN else player_raw
    enemy = ABSENT if enemy_raw is UNKNOWN else enemy_raw
    prior = route(1, 0, player_raw=player, enemy_raw=enemy) if (
        result["write_candidate"] == "F54") else route(
            0, 1, player_raw=player, enemy_raw=enemy)
    if prior["status"] != "STATIC_CONDITIONAL_ONLY":
        return {"status": "VERIFY_CONFIG", "mode": None, "side_slots": None}
    return {"status": "SYNTHETIC_PROJECTION_ONLY", "mode": prior["mode"],
            "side_slots": prior["side_slots"], "native_join_proven": False,
            "golden_pass": False, "strict_match": False}

class TreeFlagGate(unittest.TestCase):
    def test_01_b02_pin(self):
        path, sha = SOURCES["b02"]
        self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest().upper(), sha)
    def test_02_b01_pin(self):
        path, sha = SOURCES["b01"]
        self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest().upper(), sha)
    def test_03_b00_pin(self):
        path, sha = SOURCES["b00"]
        self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest().upper(), sha)
    def test_04_index_match_zero(self):
        self.assertEqual(candidate("INDEX", reached=True, matched=True, node_flag=0)["write_candidate"], "F55")
    def test_05_index_match_one(self):
        self.assertEqual(candidate("INDEX", reached=True, matched=True, node_flag=1)["write_candidate"], "F54")
    def test_06_index_match_ff(self):
        self.assertEqual(candidate("INDEX", reached=True, matched=True, node_flag=255)["write_candidate"], "F54")
    def test_07_confirmed_miss_defaults_zero(self):
        r = candidate("INDEX", reached=True, matched=False)
        self.assertEqual((r["write_candidate"], r["scratch_flag"]), ("F55", 0))
        self.assertIsNone(r["result_flag_offset"])
    def test_08_miss_does_not_read_node_flag(self):
        self.assertEqual(candidate("INDEX", reached=True, matched=False, node_flag=None)["write_candidate"], "F55")
    def test_09_unknown_match_refused(self):
        self.assertEqual(candidate("INDEX", reached=True)["status"], "VERIFY_EXACT_MATCH")
    def test_10_unknown_reachability_refused(self):
        self.assertEqual(candidate("INDEX", matched=False)["status"], "VERIFY_INDEX_REACHABILITY")
    def test_11_unvalidated_match_refused(self):
        for v in (0, 1, None, "false"):
            self.assertEqual(candidate("INDEX", reached=True, matched=v)["status"], "VERIFY_EXACT_MATCH")
    def test_12_unknown_node_byte_refused(self):
        self.assertEqual(candidate("INDEX", reached=True, matched=True)["status"], "VERIFY_NODE_BYTE")
    def test_13_invalid_byte_refused(self):
        for v in (None, False, True, -1, 256, "1"):
            self.assertEqual(candidate("INDEX", reached=True, matched=True, node_flag=v)["status"], "VERIFY_NODE_BYTE")
    def test_14_direct_nonzero(self):
        self.assertEqual(candidate("DIRECT", direct_gate=1, node_flag=1)["write_candidate"], "F54")
    def test_15_direct_zero_flag(self):
        self.assertEqual(candidate("DIRECT", direct_gate=1, node_flag=0)["write_candidate"], "F55")
    def test_16_direct_gate_zero_not_same_as_flag_zero(self):
        self.assertEqual(candidate("DIRECT", direct_gate=0, node_flag=1)["status"], "VERIFY_OTHER_PATH")
    def test_17_direct_gate_unknown(self):
        self.assertEqual(candidate("DIRECT", node_flag=1)["status"], "VERIFY_DIRECT_GATE")
    def test_18_direct_invalid(self):
        for v in (None, False, True, -1, 256):
            self.assertEqual(candidate("DIRECT", direct_gate=v, node_flag=1)["status"], "VERIFY_DIRECT_GATE")
    def test_19_direct_node_invalid(self):
        self.assertEqual(candidate("DIRECT", direct_gate=1, node_flag=None)["status"], "VERIFY_NODE_BYTE")
    def test_20_path_provenance_distinct(self):
        a = candidate("INDEX", reached=True, matched=True, node_flag=1)
        b = candidate("DIRECT", direct_gate=1, node_flag=1)
        self.assertNotEqual(a["result_flag_offset"], b["result_flag_offset"])
        self.assertEqual((a["write_candidate"], b["write_candidate"]), ("F54", "F54"))
    def test_21_unknown_source_path(self):
        self.assertEqual(candidate("OTHER", node_flag=1)["status"], "VERIFY_SOURCE_PATH")
    def test_22_no_implicit_global_mode(self):
        r = candidate("INDEX", reached=True, matched=True, node_flag=1)
        self.assertEqual(isolated_projection(r)["status"], "VERIFY_AGGREGATE_WRITERS")
        self.assertIsNone(isolated_projection(r)["mode"])
    def test_23_isolated_projection_still_synthetic(self):
        r = candidate("INDEX", reached=True, matched=True, node_flag=1)
        p = isolated_projection(r, all_other_writers_excluded=True)
        self.assertEqual((p["mode"], p["side_slots"]), (0, ("+0x1E8630", "+0x1E8634")))
        self.assertFalse(p["native_join_proven"] or p["golden_pass"] or p["strict_match"])
    def test_24_missing_index_f55_projection_still_synthetic(self):
        r = candidate("INDEX", reached=True, matched=False)
        p = isolated_projection(r, all_other_writers_excluded=True)
        self.assertEqual((p["status"], p["mode"]), ("SYNTHETIC_PROJECTION_ONLY", 0))
        self.assertEqual(p["side_slots"], ("+0x1E8634", "+0x1E8630"))
    def test_25_invalid_config_not_promoted(self):
        r = candidate("DIRECT", direct_gate=1, node_flag=1)
        self.assertEqual(isolated_projection(r, all_other_writers_excluded=True,
                                             player_raw="on")["status"], "VERIFY_CONFIG")
    def test_26_provenance_and_golden_negative(self):
        r = candidate("INDEX", reached=True, matched=True, node_flag=3)
        self.assertEqual(r["indexed_key_offset"], "+0x0C")
        self.assertEqual(r["result_flag_offset"], "node+0x14")
        self.assertIsNone(r["record_type"])
        self.assertIsNone(r["owner_identity"])
        self.assertFalse(r["native_join_proven"] or r["gameplay_observed"]
                         or r["golden_pass"] or r["strict_match"])

if __name__ == "__main__":
    unittest.main(verbosity=2)

