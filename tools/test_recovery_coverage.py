"""Check exact source coverage without reading original PC research files."""
import csv
import hashlib
from pathlib import Path
import tempfile
import unittest

import recovery_coverage as coverage


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.body = b"original finding\n"
        self.sha = hashlib.sha256(self.body).hexdigest()
        self.catalog([("local/report.md", self.sha)])

    def catalog(self, entries):
        with (self.root / "RESEARCH_SOURCE_CATALOG.tsv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=coverage.CATALOG_COLUMNS, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            for path, sha in entries:
                writer.writerow(dict(path=path, sha256=sha, bytes="17", lines="1", va_mentions="0", owner="DEV", tasks="T001", domain="UI", research_id="R1"))

    def ledger(self, destinations):
        path = self.root / coverage.LEDGERS[0]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=("source_path", "source_sha256", "destination", "destination_sha256", "review"), delimiter="\t", lineterminator="\n")
            writer.writeheader()
            for destination, digest in destinations:
                writer.writerow(dict(source_path="local/report.md", source_sha256=self.sha, destination=destination, destination_sha256=digest, review="Reviewed text"))

    def test_hash_mention_does_not_count_as_body(self):
        (self.root / "summary.md").write_text("Source SHA: " + self.sha, encoding="utf-8")
        rows = coverage.inventory(self.root, ["summary.md"])
        self.assertEqual(rows[0]["coverage"], "CATALOG_ONLY_UNRESOLVED")

    def test_identical_body_under_other_name_counts(self):
        (self.root / "renamed.md").write_bytes(self.body)
        rows = coverage.inventory(self.root, ["renamed.md"])
        self.assertEqual(rows[0]["coverage"], "EXACT_BODY_AVAILABLE")
        self.assertEqual(rows[0]["destinations"], "renamed.md")

    def test_every_catalog_row_retained(self):
        self.catalog([("local/report.md", self.sha), ("duplicate/report.md", self.sha)])
        rows = coverage.inventory(self.root, [])
        self.assertEqual([row["path"] for row in rows], ["local/report.md", "duplicate/report.md"])
        self.assertEqual(rows[0]["research_id"], "R1")

    def test_reviewed_variant_and_duplicate_receipts(self):
        for name in ("safe.md", "second.md"):
            (self.root / name).write_text("Reviewed redacted version", encoding="utf-8")
        sha = hashlib.sha256((self.root / "safe.md").read_bytes()).hexdigest()
        self.ledger([("safe.md", sha), ("safe.md", sha), ("second.md", sha)])
        rows = coverage.inventory(self.root, [])
        self.assertEqual(rows[0]["coverage"], "RECOVERED_REVIEWED_VARIANT")
        self.assertEqual(rows[0]["destinations"], "safe.md;second.md")

    def test_stale_ledger_and_path_escape_rejected(self):
        (self.root / "safe.md").write_bytes(self.body)
        self.ledger([("safe.md", "0" * 64)])
        with self.assertRaisesRegex(ValueError, "checksum"):
            coverage.inventory(self.root, [])
        self.ledger([("../outside.md", self.sha)])
        with self.assertRaisesRegex(ValueError, "escapes"):
            coverage.inventory(self.root, [])

    def test_binary_receipt_cannot_count_as_text(self):
        payload = b"binary\x00payload"
        (self.root / "blob.dat").write_bytes(payload)
        self.ledger([("blob.dat", hashlib.sha256(payload).hexdigest())])
        with self.assertRaisesRegex(ValueError, "not text"):
            coverage.inventory(self.root, [])


if __name__ == "__main__":
    unittest.main()
