"""E-only T018/T020 regression: audit synthetic Golden G0/G1/G2 provenance.

Usage: python t020_golden_lineage_content_bound_gate_20261028_2045.py
       --db /absolute/path/search.sqlite

Only checks synthetic fixtures + previous code gate. NO native game run; NEVER marks
native Golden PASS or strict MATCH. The static SQLite is read-only/immutable.
"""
import argparse
import base64
import copy
import hashlib
import json
import re
import runpy
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# The previous gate can be a sibling of this directory (conversation artifacts),
# or in the same flat Library export folder. Do not modify the previous files.
PREVIOUS = next((d for d in (ROOT.parent / "E_20261028_1949", ROOT)
                 if (d / "t020_dialog_wrapper_fingerprint_golden_lineage_gate_20261028_1949.py").is_file()),
                ROOT.parent / "E_20261028_1949")
EXPECTED_DB = "0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF"
F = json.loads((ROOT / "T020_GOLDEN_LINEAGE_CONTENT_BOUND_CASES_20261028_2045.json").read_text("utf-8"))
A = argparse.ArgumentParser()
A.add_argument("--db", required=True)
args = A.parse_args()
DB = Path(args.db).resolve()
if not DB.is_file():
    raise FileNotFoundError(DB)

# Import old gate without executing its unittest __main__, retaining old parser contract.
_original_argv = sys.argv
try:
    sys.argv = [str(PREVIOUS / "t020_dialog_wrapper_fingerprint_golden_lineage_gate_20261028_1949.py"),
                "--db", str(DB)]
    OLD = runpy.run_path(sys.argv[0], run_name="golden_schema_audit_import")
finally:
    sys.argv = _original_argv
old_schema_ready = OLD["schema_ready"]

HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")

def unpack(x):
    if not isinstance(x, str):
        raise ValueError("base64 must be string")
    raw = base64.b64decode(x, validate=True)
    if not raw:
        raise ValueError("empty payload")
    return raw

def hash_bound(record, payload_name, digest_name):
    raw = unpack(record[payload_name])
    digest = record[digest_name]
    return bool(isinstance(digest, str) and HEX64.fullmatch(digest)
                and hashlib.sha256(raw).hexdigest().casefold() == digest.casefold())

def hardened_synthetic_ready(c):
    """Independent *synthetic* schema lint, not native authentication.

    Adds concrete content hashes, explicit event ordering, parent receipt links,
    exact integer coordinate types, and rejects malformed identifiers/timestamps.
    """
    if not old_schema_ready(c) or c.get("capture_source") != "SYNTHETIC":
        return False
    try:
        g0, g1, g2 = (c[k] for k in ("g0", "g1", "g2"))
        for k in ("run_id", "scenario"):
            if not isinstance(g0[k], str) or not g0[k].strip():
                return False
        if any(not isinstance(s["id"], str) or not s["id"].strip() for s in g2["sides"]):
            return False
        if any(not isinstance(row[k], str) or not row[k].strip()
               for row in g2["deployed"] for k in ("troop", "unit")):
            return False
        if any(type(row[k]) is not int for row in g2["deployed"] for k in ("x", "y", "order")):
            return False
        if any(type(g[k]) is not int or g[k] < 0 for g in (g1, g0, g2) for k in ("at", "event_seq")):
            return False
        if not (g1["event_seq"] < g0["event_seq"] < g2["event_seq"]):
            return False
        if not (g1["at"] <= g0["at"] <= g2["at"]):
            return False
        for g in (g0, g1, g2):
            if not hash_bound(g, "capture_b64", "capture_sha"):
                return False
        if not all((hash_bound(g1, "save_b64", "save_sha"),
                    hash_bound(g1, "input_b64", "input_sha"),
                    hash_bound(g2, "map_b64", "map_sha"))):
            return False
        if g0["previous_capture_sha"].casefold() != g1["capture_sha"].casefold():
            return False
        if g2["previous_capture_sha"].casefold() != g0["capture_sha"].casefold():
            return False
        return True
    except (ValueError, KeyError, TypeError, AttributeError):
        return False

def apply_changes(base, changes):
    out = copy.deepcopy(base)
    for p, v in changes:
        obj = out
        for k in p[:-1]:
            obj = obj[k]
        obj[p[-1]] = v
    return out

class EvidenceGates(unittest.TestCase):
    def test_old_source_is_unchanged(self):
        d = hashlib.sha256((PREVIOUS / "t020_dialog_wrapper_fingerprint_golden_lineage_gate_20261028_1949.py").read_bytes()).hexdigest().upper()
        self.assertEqual(d, F["previous_test_sha256"])
    def test_old_fixture_is_unchanged(self):
        d = hashlib.sha256((PREVIOUS / "T020_DIALOG_WRAPPER_FINGERPRINT_GOLDEN_LINEAGE_CASES_20261028_1949.json").read_bytes()).hexdigest().upper()
        self.assertEqual(d, F["previous_fixture_sha256"])
    def test_20261021_db_sha(self):
        self.assertEqual(hashlib.sha256(DB.read_bytes()).hexdigest().upper(), EXPECTED_DB)
    def test_20261021_db_quickcheck(self):
        with sqlite3.connect("file:"+DB.as_posix()+"?mode=ro&immutable=1",uri=True) as con:
            con.execute("PRAGMA query_only=ON")
            self.assertEqual(con.execute("PRAGMA quick_check").fetchone()[0],"ok")
    def test_19h_gate_control(self):
        self.assertTrue(old_schema_ready(F["base"]))
        self.assertTrue(hardened_synthetic_ready(F["base"]))
    def test_native_never_certified(self):
        self.assertFalse(OLD["actual_golden"](F["base"]))
        self.assertEqual(F["native_observed"], 0)
        self.assertEqual(F["actual_golden_pass"], 0)
        self.assertEqual(F["strict_match"], 0)

def make_case_test(i, item):
    def test(self):
        record = apply_changes(F["base"], item["changes"])
        self.assertEqual(old_schema_ready(record),item["old_accept"],item["case"])
        self.assertEqual(hardened_synthetic_ready(record),item["hardened_accept"],item["case"])
        self.assertFalse(OLD["actual_golden"](record),item["case"])
    return test
for i, item in enumerate(F["cases"]):
    setattr(EvidenceGates, f"test_case_{i:02}_{item['case']}", make_case_test(i,item))

if __name__ == "__main__":
    unittest.main(argv=[__file__],verbosity=2)
