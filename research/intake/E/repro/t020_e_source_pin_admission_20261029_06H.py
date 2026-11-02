"""E/T020 static-only source admission for the 2026-10-29 snapshots.
No native-game invocation; no write to sources; never returns Golden PASS.
"""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / "E_OFFLINE_SYNC_20261029"
PC_MAN = ROOT / "T020_E_PC_20261025_27_BYTE_INVENTORY_20261029_05H.json"
LIB_MAN = STAGE / "T020_E_LIBRARY_SOURCE_MANIFEST_20261029_04H.json"
MANIFEST_PINS = {
    "pc": "29DF7E435A3C63C0A33F7A2F38D83C2EA604E1791F669BAED5A38CF8BDC0DFE1",
    "library": "10AB86C458598FEF0C81AEF2CC7118485950ACC57972D0B5C1B8031E637A37AC",
}
NAME21 = "T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json"
ALIAS21 = NAME21.replace(".json", "_LIBPIN_7D574F25.json")

def digest(raw):
    return hashlib.sha256(raw).hexdigest().upper()

def rows_for(source):
    manifest = PC_MAN if source == "pc" else LIB_MAN
    raw = manifest.read_bytes()
    if digest(raw) != MANIFEST_PINS[source]:
        raise ValueError("MANIFEST_BYTE_MISMATCH")
    doc = json.loads(raw)
    rows = doc["items"]
    expected = 133 if source == "pc" else 23
    if len(rows) != expected:
        raise ValueError("MANIFEST_CARDINALITY")
    return rows

def resolve(source, name):
    """Return verified bytes, never 'native' or 'Golden accepted'."""
    if source not in MANIFEST_PINS or not isinstance(name, str):
        raise ValueError("SOURCE_OR_TYPE_INVALID")
    if not name or name != Path(name).name or "/" in name or "\\" in name:
        raise ValueError("UNTRUSTED_NAME")
    rows = rows_for(source)
    key = "file" if source == "pc" else "name"
    matches = [x for x in rows if x[key] == name]
    if len(matches) != 1:
        raise ValueError("NOT_PINNED_OR_AMBIGUOUS")
    row = matches[0]
    effective_name = ALIAS21 if source == "library" and name == NAME21 else name
    root = ROOT if source == "pc" else STAGE
    full = root / effective_name
    if full.is_symlink() or not full.is_file():
        raise ValueError("MISSING_OR_SYMLINK")
    content = full.read_bytes()
    if len(content) != row["bytes"] or digest(content) != row["sha256"]:
        raise ValueError("SOURCE_BYTE_MISMATCH")
    return {"status": "SOURCE_PINNED_STATIC_ONLY_NOT_NATIVE",
            "path": str(full), "sha256": digest(content),
            "bytes": content}

def reject_unpinned_stale_copy():
    row = next(x for x in rows_for("library") if x["name"] == NAME21)
    stale = STAGE / NAME21
    raw = stale.read_bytes()
    return (len(raw) != row["bytes"] or digest(raw) != row["sha256"])

class SourcePinTests(unittest.TestCase):
    def test_01_snapshot_counts_and_pins(self):
        self.assertEqual(len(rows_for("pc")), 133)
        self.assertEqual(len(rows_for("library")), 23)
    def test_02_pc_report_is_static_pinned(self):
        name = next(x["file"] for x in rows_for("pc") if x["file"].endswith(".md"))
        r = resolve("pc", name)
        self.assertEqual(r["status"], "SOURCE_PINNED_STATIC_ONLY_NOT_NATIVE")
    def test_03_library_21h_pin_and_json(self):
        r = resolve("library", NAME21)
        self.assertIn("LIBPIN_", r["path"])
        data = json.loads(r["bytes"])
        self.assertEqual(len(data["cases"]), 36)
    def test_04_reject_shortened_same_name(self):
        self.assertTrue(reject_unpinned_stale_copy())
    def test_05_reject_unknown(self):
        with self.assertRaisesRegex(ValueError, "NOT_PINNED"):
            resolve("library", "unlisted.json")
    def test_06_reject_traversal(self):
        with self.assertRaisesRegex(ValueError, "UNTRUSTED_NAME"):
            resolve("library", "../T018_GOLDEN_CORPUS.md")
    def test_07_reject_wrong_source(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_OR_TYPE_INVALID"):
            resolve("other", NAME21)
    def test_08_no_native_pass_from_pin(self):
        for origin, name in (("library", NAME21),
                             ("pc", rows_for("pc")[0]["file"])):
            self.assertNotIn("PASS", resolve(origin, name)["status"])
            self.assertNotIn("READY", resolve(origin, name)["status"])

if __name__ == "__main__":
    unittest.main(verbosity=2)