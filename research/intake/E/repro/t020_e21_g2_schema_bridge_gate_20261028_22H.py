"""E-only cross-schema synthetic G2 reviewer; never qualifies native Golden."""
import copy
import json
import unittest
from pathlib import Path
import t020_cnb02_g2_cross_generation_parity_guard_20261026_10H as old_pc

ROOT = Path(__file__).resolve().parent
F = json.loads((ROOT / "T020_E21_G2_SCHEMA_BRIDGE_CASES_20261028_22H.json").read_text(encoding="utf-8"))
BASE = F["capture"]
ALIASES = {"attack": "attack", "defend": "defense", "support": "support"}

def bridge(c):
    """Translate labels for diagnostic use only; source proof remains UNKNOWN."""
    g = c.get("g2") if isinstance(c, dict) else None
    if not isinstance(g, dict):
        g = {}
    flags = {"SYNTHETIC_NOT_NATIVE", "EXTERNAL_G0G1G2_WITNESS_MISSING",
             "ACTIVE_WINDOW_NOT_ATTESTED", "MAP_ID_NOT_SOURCE_ATTESTED"}
    id_role, role_seen = {}, set()
    sides = {"attack": [], "defense": [], "support": []}
    rows = g.get("sides", [])
    if not isinstance(rows, list):
        rows = []
        flags.add("SOURCE_SIDE_SCHEMA_INVALID")
    for row in rows:
        if not isinstance(row, dict):
            flags.add("SOURCE_SIDE_ROW_INVALID")
            continue
        role, sid = row.get("role"), row.get("id")
        if not isinstance(role, str) or role not in ALIASES:
            flags.add("SOURCE_ROLE_UNMAPPED")
            continue
        if not isinstance(sid, str) or not sid.strip():
            flags.add("SOURCE_SIDE_ID_INVALID")
            continue
        mapped = ALIASES[role]
        if role == "defend":
            flags.add("DEFEND_TO_DEFENSE_ALIAS_VERIFY")
        if mapped in role_seen:
            flags.add("SOURCE_ROLE_DUPLICATE")
        if sid in id_role:
            flags.add("SOURCE_SIDE_ID_DUPLICATE")
        role_seen.add(mapped)
        id_role[sid] = mapped
        sides[mapped].append(sid)
    out = {"map_id": g.get("map_id"), "sides": sides, "roster": []}
    orders = []
    deployed = g.get("deployed", [])
    if not isinstance(deployed, list):
        deployed = []
        flags.add("SOURCE_DEPLOYMENT_NOT_LIST")
    for row in deployed:
        if not isinstance(row, dict):
            flags.add("SOURCE_DEPLOYMENT_ROW_INVALID")
            continue
        order = row.get("order")
        if type(order) is not int or order < 0:
            flags.add("SOURCE_ORDER_INVALID")
        else:
            orders.append(order)
        sid = row.get("side_id")
        role = id_role.get(sid) if isinstance(sid, str) else None
        if role is None:
            flags.add("DEPLOYMENT_SIDE_UNMAPPED")
        out["roster"].append({"side": role, "unit_visible": row.get("unit"),
                              "troop_visible": row.get("troop")})
    if sorted(orders) != list(range(len(deployed))):
        flags.add("SOURCE_ORDER_NONCONTIGUOUS")
    flags.update(old_pc.review(out)["issues"])
    if isinstance(c, dict) and c.get("native_receipt_verified") is True:
        flags.add("SELF_ASSERTED_NATIVE_FLAG_NOT_PROOF")
    return {"status": "VERIFY_NOT_GOLDEN", "issues": sorted(flags),
            "normalized_diagnostic": out,
            "actual_golden_pass": False, "strict_match": False}

class CrossSchemaTests(unittest.TestCase):
    def check(self, c, flag):
        r = bridge(c)
        self.assertIn(flag, r["issues"])
        self.assertFalse(r["actual_golden_pass"])
        self.assertFalse(r["strict_match"])
        self.assertEqual(r["status"], "VERIFY_NOT_GOLDEN")

    def test_01_source_pinned_label_not_pc_rehash(self):
        self.assertEqual(F["source_research_id"],
                         "E-OFFLINE-20261028-2149-T018-T020-SEMANTIC-CAPTURE-BINDING-01")
        self.assertEqual(len(F["source_e21_fixture_sha256"]), 64)
        self.assertEqual(F["source_class"], "SYNTHETIC")

    def test_02_reference_defense_roster_missing(self):
        self.check(BASE, "NO_DEFENSE_ROSTER_RECEIPT")

    def test_03_no_native_map_id(self):
        self.check(BASE, "MAP_ID_UNVERIFIED")

    def test_04_legacy_defend_label_requires_mapping_proof(self):
        self.check(BASE, "DEFEND_TO_DEFENSE_ALIAS_VERIFY")

    def test_05_no_external_receipt(self):
        self.check(BASE, "EXTERNAL_G0G1G2_WITNESS_MISSING")

    def test_06_active_window_not_observed(self):
        self.check(BASE, "ACTIVE_WINDOW_NOT_ATTESTED")

    def test_07_self_asserted_native_flag_is_not_proof(self):
        c = copy.deepcopy(BASE); c["native_receipt_verified"] = True
        self.check(c, "SELF_ASSERTED_NATIVE_FLAG_NOT_PROOF")

    def test_08_unknown_deployment_owner(self):
        c = copy.deepcopy(BASE); c["g2"]["deployed"][0]["side_id"] = "X"
        self.check(c, "DEPLOYMENT_SIDE_UNMAPPED")

    def test_09_invalid_source_role(self):
        c = copy.deepcopy(BASE); c["g2"]["sides"][1]["role"] = "defense"
        self.check(c, "SOURCE_ROLE_UNMAPPED")

    def test_10_duplicate_role(self):
        c = copy.deepcopy(BASE); c["g2"]["sides"][1]["role"] = "attack"
        self.check(c, "SOURCE_ROLE_DUPLICATE")

    def test_11_duplicate_side_id(self):
        c = copy.deepcopy(BASE); c["g2"]["sides"][1]["id"] = "A"
        self.check(c, "SOURCE_SIDE_ID_DUPLICATE")

    def test_12_boolean_deployment_order(self):
        c = copy.deepcopy(BASE); c["g2"]["deployed"][0]["order"] = True
        self.check(c, "SOURCE_ORDER_INVALID")

    def test_13_order_gap(self):
        c = copy.deepcopy(BASE); c["g2"]["deployed"][1]["order"] = 4
        self.check(c, "SOURCE_ORDER_NONCONTIGUOUS")

    def test_14_missing_visible_troop(self):
        c = copy.deepcopy(BASE); c["g2"]["deployed"][1]["troop"] = ""
        self.check(c, "ROSTER_IDS_NOT_TEXT")

    def test_15_duplicate_visible_pair(self):
        c = copy.deepcopy(BASE)
        c["g2"]["deployed"].append(copy.deepcopy(c["g2"]["deployed"][0]))
        c["g2"]["deployed"][-1]["order"] = 2
        self.check(c, "DUPLICATE_ROSTER_REFERENCE_VERIFY")

    def test_16_defender_added_still_not_native(self):
        c = copy.deepcopy(BASE)
        c["g2"]["deployed"].append({"order": 2, "side_id": "D",
                                    "unit": "ud", "troop": "td"})
        self.assertNotIn("NO_DEFENSE_ROSTER_RECEIPT", bridge(c)["issues"])
        self.check(c, "EXTERNAL_G0G1G2_WITNESS_MISSING")

    def test_17_placeholder_map_id(self):
        c = copy.deepcopy(BASE); c["g2"]["map_id"] = " observed-map "
        self.check(c, "MAP_PLACEHOLDER_ALIAS_VERIFY")

    def test_18_injected_map_id_still_unattested(self):
        c = copy.deepcopy(BASE); c["g2"]["map_id"] = "s16"
        self.check(c, "MAP_ID_NOT_SOURCE_ATTESTED")

    def test_19_no_support_roster_is_not_auto_failure(self):
        c = copy.deepcopy(BASE)
        c["g2"]["deployed"][1].update(side_id="D",unit="ud",troop="td")
        issues = bridge(c)["issues"]
        self.assertNotIn("NO_DEFENSE_ROSTER_RECEIPT", issues)
        self.assertNotIn("NO_SUPPORT_ROSTER_RECEIPT", issues)
        self.assertFalse(bridge(c)["actual_golden_pass"])

    def test_20_no_source_type_promotion(self):
        self.assertFalse(bridge(BASE)["strict_match"])
        self.assertFalse(bridge(BASE)["actual_golden_pass"])

    def test_21_unhashable_role_fail_closed(self):
        c = copy.deepcopy(BASE); c["g2"]["sides"][0]["role"] = ["attack"]
        self.check(c, "SOURCE_ROLE_UNMAPPED")

    def test_22_unhashable_deploy_side_fail_closed(self):
        c = copy.deepcopy(BASE); c["g2"]["deployed"][0]["side_id"] = ["A"]
        self.check(c, "DEPLOYMENT_SIDE_UNMAPPED")

    def test_23_invalid_g2_type_fail_closed(self):
        c = copy.deepcopy(BASE); c["g2"] = []
        self.check(c, "NO_DEFENSE_ROSTER_RECEIPT")

    def test_24_nonobject_capture_fail_closed(self):
        self.check(None, "EXTERNAL_G0G1G2_WITNESS_MISSING")

if __name__ == "__main__":
    unittest.main(verbosity=2)

