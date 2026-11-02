"""T020: byte-bind receipt paths to real files. Never declares gameplay PASS."""
from pathlib import Path
import hashlib
import re
import tempfile
import unittest

EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
ROLES = ("old_exe", "old_save", "old_dat", "old_map", "old_input",
         "g0", "g1", "g2", "g3", "g4", "new_build", "new_capture")
HEX64 = re.compile(r"[0-9a-fA-F]{64}\Z")

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for piece in iter(lambda: f.read(65536), b""):
            h.update(piece)
    return h.hexdigest().upper()

def verify(root, receipt):
    """Independent byte gate, not a claim about who captured any bytes."""
    items = receipt.get("evidence")
    if not isinstance(items, dict) or set(items) != set(ROLES):
        return "REJECT_FIELDS"
    if not all(isinstance(items[role], dict) for role in ROLES):
        return "REJECT_FIELDS"
    synthetic = receipt.get("synthetic") is True
    if not synthetic and items["old_exe"].get("sha256", "").upper() != EXE_SHA:
        return "REJECT_EXE_ID"
    root = Path(root).resolve(strict=True)
    seen = set()
    for role in ROLES:
        item = items[role]
        if not isinstance(item, dict):
            return "REJECT_FIELDS:" + role
        name, expected = item.get("path"), item.get("sha256")
        if not isinstance(name, str) or not name or not isinstance(expected, str):
            return "REJECT_FIELDS:" + role
        if HEX64.fullmatch(expected) is None:
            return "REJECT_HASH_FORMAT:" + role
        rel = Path(name)
        if rel.is_absolute() or ".." in rel.parts or "." == name:
            return "REJECT_PATH:" + role
        key = str(rel).casefold()
        if key in seen:
            return "REJECT_DUPLICATE_PATH:" + role
        seen.add(key)
        p = root / rel
        try:
            if any((root / Path(*rel.parts[:i])).is_symlink()
                   for i in range(1, len(rel.parts) + 1)):
                return "REJECT_SYMLINK:" + role
            resolved = p.resolve(strict=True)
            if not resolved.is_relative_to(root):
                return "REJECT_PATH:" + role
            if not resolved.is_file():
                return "REJECT_NOT_FILE:" + role
            if digest(resolved) != expected.upper():
                return "HASH_MISMATCH:" + role
        except (OSError, ValueError):
            return "MISSING_OR_UNREADABLE:" + role
    return "BYTE_BOUND_SYNTHETIC" if synthetic else "BYTE_BOUND_NOT_GOLDEN"

class ByteBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.items = {}
        for role in ROLES:
            name = "receipts/" + role + ".bin"
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(role.encode("ascii"))
            self.items[role] = {"path": name, "sha256": digest(p)}
        self.receipt = {"synthetic": True, "evidence": self.items}

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, expected):
        self.assertEqual(verify(self.root, self.receipt), expected)

    def test_byte_bound_synthetic_not_golden(self):
        self.check("BYTE_BOUND_SYNTHETIC")

    def test_mutated_save_bytes(self):
        (self.root / self.items["old_save"]["path"]).write_bytes(b"changed")
        self.check("HASH_MISMATCH:old_save")

    def test_placeholder_digest(self):
        self.items["old_input"]["sha256"] = "present"
        self.check("REJECT_HASH_FORMAT:old_input")

    def test_missing_capture(self):
        (self.root / self.items["g4"]["path"]).unlink()
        self.check("MISSING_OR_UNREADABLE:g4")

    def test_cross_role_path_reuse(self):
        self.items["g3"] = dict(self.items["g2"])
        self.check("REJECT_DUPLICATE_PATH:g3")

    def test_escape_above_root(self):
        self.items["old_dat"]["path"] = "../outside.dat"
        self.check("REJECT_PATH:old_dat")

    def test_absolute_path(self):
        self.items["old_map"]["path"] = str((self.root / "outside").resolve())
        self.check("REJECT_PATH:old_map")

    def test_symlink_rejected(self):
        target = self.root / self.items["g0"]["path"]
        link = self.root / "receipts/linked.bin"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("symlink unavailable")
        self.items["g0"]["path"] = "receipts/linked.bin"
        self.check("REJECT_SYMLINK:g0")

    def test_missing_required_role(self):
        self.items.pop("g1")
        self.check("REJECT_FIELDS")

    def test_malformed_exe_receipt(self):
        self.items["old_exe"] = "not a record"
        self.receipt["synthetic"] = False
        self.check("REJECT_FIELDS")

    def test_non_synthetic_wrong_exe_id(self):
        self.receipt["synthetic"] = False
        self.check("REJECT_EXE_ID")

    def test_stage_capture_content_changed(self):
        (self.root / self.items["g2"]["path"]).write_bytes(b"another frame")
        self.check("HASH_MISMATCH:g2")

    def test_directory_not_file(self):
        self.items["new_capture"]["path"] = "receipts"
        self.check("REJECT_NOT_FILE:new_capture")

if __name__ == "__main__":
    unittest.main()