"""Offline Ghidra structure export regression tests; no original/native inputs."""
import copy
import tempfile
import unittest
from pathlib import Path

import build_kb


class UnknownWidthExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "ghidra" / "kb_structs.tsv"
        self.path.parent.mkdir()
        self.known = [(2, ["Audio", "0x04", "byte", "flag", "状態", "静的確認", "source"]),
                      (3, ["Audio", "0x20", "ptr", "owner", "owner pointer", "推定", "source"])]
        self.unknown = [(4, ["Audio", "0x21", "unknown", "mode", "width unproven", "静的確認", "source"])]
        self.expected = ("Audio\t4\tbyte\tflag\t状態［静的確認］\n"
                         "Audio\t32\tptr\towner\towner pointer［推定］\n").encode("utf-8")

    def test_mixed_rows_omit_unknown_and_preserve_known_bytes_and_input(self):
        rows = self.known[:1] + self.unknown + self.known[1:]
        original = copy.deepcopy(rows)
        skipped = build_kb.write_ghidra_structs(self.path, rows)
        self.assertEqual(self.path.read_bytes(), self.expected)
        self.assertEqual(skipped, 1)
        self.assertEqual(rows, original)

    def test_all_unknown_produces_no_structural_layout(self):
        original = copy.deepcopy(self.unknown)
        skipped = build_kb.write_ghidra_structs(self.path, self.unknown)
        self.assertEqual(self.path.read_bytes(), b"")
        self.assertEqual(skipped, 1)
        self.assertEqual(self.unknown, original)

    def test_known_rows_keep_previous_output_bytes(self):
        original = copy.deepcopy(self.known)
        build_kb.write_ghidra_structs(self.path, self.known)
        self.assertEqual(self.path.read_bytes(), self.expected)
        self.assertEqual(self.known, original)


if __name__ == "__main__":
    unittest.main()
