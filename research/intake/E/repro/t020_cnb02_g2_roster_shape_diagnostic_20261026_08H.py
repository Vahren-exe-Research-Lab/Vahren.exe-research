"""E T020: synthetic G2 roster-shape diagnostics only; NOT a native Golden gate."""
import copy
import unittest

ROLES = frozenset({"attack", "defense", "support"})
UNVERIFIED_MAPS = {"STATIC_UNCONFIRMED_MAP", "observed-map", "synthetic-map"}

def ident(v):
    return isinstance(v, str) and bool(v.strip())

def review(g2):
    problems = set()
    if not isinstance(g2, dict):
        return {"verdict": "VERIFY_NOT_GOLDEN", "issues": ["G2_NOT_OBJECT"],
                "limits": ["NO_REAL_MAP_OR_DEPLOYMENT_ATTESTATION"]}
    map_id = g2.get("map_id")
    if not ident(map_id) or map_id in UNVERIFIED_MAPS:
        problems.add("MAP_ID_UNVERIFIED")
    sides = g2.get("sides")
    if not isinstance(sides, dict) or set(sides) != ROLES:
        problems.add("SIDE_SCHEMA")
        sides = {}
    for role in ROLES:
        if not isinstance(sides.get(role), list):
            problems.add("SIDE_SCHEMA")
    if all(isinstance(sides.get(role), list) for role in ("attack", "defense")):
        if not sides["attack"] or not sides["defense"]:
            problems.add("ACTIVE_PARTICIPANTS_UNPROVEN")
    roster = g2.get("roster")
    if not isinstance(roster, list) or not roster:
        problems.add("ROSTER_MISSING")
        roster = []
    seen = set()
    for row in roster:
        if not isinstance(row, dict):
            problems.add("ROSTER_ROW_NOT_OBJECT")
            continue
        role = row.get("side")
        if not isinstance(role, str) or role not in ROLES:
            problems.add("ROSTER_ROLE_UNRECOGNIZED")
        unit, troop = row.get("unit_visible"), row.get("troop_visible")
        if not ident(unit) or not ident(troop):
            problems.add("ROSTER_IDS_NOT_TEXT")
            continue
        if role in ROLES:
            key = (role, unit, troop)
            if key in seen:
                problems.add("DUPLICATE_ROSTER_REFERENCE_VERIFY")
            seen.add(key)
    return {"verdict": "VERIFY_NOT_GOLDEN", "issues": sorted(problems),
            "limits": ["MAP_BYTES_NOT_ATTESTED", "SIDE_ROLE_NOT_NATIVE_ATTESTED",
                       "TROOP_DEPLOYMENT_NOT_ATOMIC", "SAME_BATTLE_G0_G1_MISSING"]}

class G2DiagnosticTests(unittest.TestCase):
    def base(self):
        return {"map_id": "real-map-name-unverified", "sides":
                {"attack": ["red"], "defense": ["blue"], "support": []},
                "roster": [{"side": "attack", "unit_visible": "u1",
                            "troop_visible": "t1"}]}
    def check(self, key, change):
        rec = copy.deepcopy(self.base())
        change(rec)
        self.assertIn(key, review(rec)["issues"])
        self.assertEqual(review(rec)["verdict"], "VERIFY_NOT_GOLDEN")
    def test_baseline_shape_is_never_golden(self):
        r = review(self.base())
        self.assertEqual(r["issues"], [])
        self.assertIn("MAP_BYTES_NOT_ATTESTED", r["limits"])
    def test_s01_unknown_side(self):
        self.check("ROSTER_ROLE_UNRECOGNIZED",
                   lambda r: r["roster"][0].update(side="neutral"))
    def test_s02_numeric_side(self):
        self.check("ROSTER_ROLE_UNRECOGNIZED",
                   lambda r: r["roster"][0].update(side=7))
    def test_s03_empty_combat_sides(self):
        self.check("ACTIVE_PARTICIPANTS_UNPROVEN",
                   lambda r: r.update(sides={"attack": [], "defense": [], "support": []}))
    def test_s04_duplicate_roster(self):
        self.check("DUPLICATE_ROSTER_REFERENCE_VERIFY",
                   lambda r: r["roster"].append(copy.deepcopy(r["roster"][0])))
    def test_s05_unverified_map_placeholder(self):
        self.check("MAP_ID_UNVERIFIED",
                   lambda r: r.update(map_id="STATIC_UNCONFIRMED_MAP"))
    def test_s06_numeric_unit(self):
        self.check("ROSTER_IDS_NOT_TEXT",
                   lambda r: r["roster"][0].update(unit_visible=17))
    def test_s06b_numeric_troop(self):
        self.check("ROSTER_IDS_NOT_TEXT",
                   lambda r: r["roster"][0].update(troop_visible=42))
    def test_s07_missing_support_slot(self):
        self.check("SIDE_SCHEMA", lambda r: r["sides"].pop("support"))
    def test_support_empty_is_permitted_shape(self):
        self.assertNotIn("SIDE_SCHEMA", review(self.base())["issues"])
    def test_boolean_id_is_not_text(self):
        self.check("ROSTER_IDS_NOT_TEXT",
                   lambda r: r["roster"][0].update(unit_visible=True))
    def test_roster_contains_nonobject(self):
        self.check("ROSTER_ROW_NOT_OBJECT", lambda r: r["roster"].append(3))
    def test_no_roster(self):
        self.check("ROSTER_MISSING", lambda r: r.update(roster=[]))
    def test_placeholder_hash_cannot_grant_golden(self):
        r = self.base()
        r.update(map_sha="a"*64, capture_sha="b"*64, old_observed=True)
        self.assertEqual(review(r)["verdict"], "VERIFY_NOT_GOLDEN")

if __name__ == "__main__":
    unittest.main()
