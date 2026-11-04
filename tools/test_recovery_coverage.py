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

    def ledger(self, destinations, state="", source_sha=None):
        path = self.root / coverage.LEDGERS[0]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=("source_path", "source_sha256", "destination", "destination_sha256", "review", "coverage_state"), delimiter="\t", lineterminator="\n")
            writer.writeheader()
            for destination, digest in destinations:
                writer.writerow(dict(source_path="local/report.md", source_sha256=source_sha or self.sha, destination=destination, destination_sha256=digest, review="Reviewed text", coverage_state=state))

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

    def test_partial_excerpt_is_not_full_variant(self):
        (self.root / "excerpt.md").write_text("selected finding", encoding="utf-8")
        sha = hashlib.sha256((self.root / "excerpt.md").read_bytes()).hexdigest()
        self.ledger([("excerpt.md", sha)], state="PARTIAL_REDACTED")
        row = coverage.inventory(self.root, ["excerpt.md"])[0]
        self.assertEqual(row["coverage"], "PARTIAL_BODY_AVAILABLE")
        self.assertEqual(row["destinations"], "excerpt.md")

    def test_exact_body_elsewhere_wins_over_partial(self):
        (self.root / "excerpt.md").write_text("selected finding", encoding="utf-8")
        sha = hashlib.sha256((self.root / "excerpt.md").read_bytes()).hexdigest()
        self.ledger([("excerpt.md", sha)], state="PARTIAL_REVIEWED_EXCERPT")
        (self.root / "whole.md").write_bytes(self.body)
        row = coverage.inventory(self.root, ["excerpt.md", "whole.md"])[0]
        self.assertEqual(row["coverage"], "EXACT_BODY_AVAILABLE")
        self.assertEqual(row["destinations"], "whole.md")

    def test_current_receipt_sha_does_not_map_old_catalog(self):
        payload = b"updated original finding"
        (self.root / "current.md").write_bytes(payload)
        current_sha = hashlib.sha256(payload).hexdigest()
        self.ledger([("current.md", current_sha)], source_sha=current_sha)
        row = coverage.inventory(self.root, ["current.md"])[0]
        self.assertEqual(row["coverage"], "SOURCE_REVISION_DIFFERS")
        self.assertEqual(row["sha256"], self.sha)
        self.assertEqual(row["recovered_source_sha256"], current_sha)
        self.assertEqual(row["destinations"], "current.md")

    def test_revision_receipt_does_not_match_basename_only(self):
        payload = b"updated original finding"
        (self.root / "current.md").write_bytes(payload)
        current_sha = hashlib.sha256(payload).hexdigest()
        self.catalog([("another/report.md", self.sha)])
        self.ledger([("current.md", current_sha)], source_sha=current_sha)
        row = coverage.inventory(self.root, ["current.md"])[0]
        self.assertEqual(row["coverage"], "CATALOG_ONLY_UNRESOLVED")
        self.assertEqual(row["recovered_source_sha256"], "")

    def test_exact_snapshot_wins_over_different_revision(self):
        payload = b"selected newer finding"
        (self.root / "current.md").write_bytes(payload)
        current_sha = hashlib.sha256(payload).hexdigest()
        self.ledger([("current.md", current_sha)], source_sha=current_sha, state="PARTIAL_REDACTED")
        (self.root / "snapshot.md").write_bytes(self.body)
        row = coverage.inventory(self.root, ["current.md", "snapshot.md"])[0]
        self.assertEqual(row["coverage"], "EXACT_BODY_AVAILABLE")
        self.assertEqual(row["destinations"], "snapshot.md")

    def test_binary_receipt_cannot_count_as_text(self):
        payload = b"binary\x00payload"
        (self.root / "blob.dat").write_bytes(payload)
        self.ledger([("blob.dat", hashlib.sha256(payload).hexdigest())])
        with self.assertRaisesRegex(ValueError, "not text"):
            coverage.inventory(self.root, [])


if __name__ == "__main__":
    unittest.main()
