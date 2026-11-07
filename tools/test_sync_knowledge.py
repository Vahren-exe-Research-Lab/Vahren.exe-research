#!/usr/bin/env python3
"""Offline regression tests for knowledge source audits and Git safety gates."""
import contextlib
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sync_knowledge as sync
import reference
import recovery_coverage

class KnowledgeSecurityTests(unittest.TestCase):
    def fixture(self, root):
        for name in sync.FILES:
            p=root/name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("reviewed source\n",encoding="utf-8")
        (root/".gitignore").write_text(
            "/*\n/tools/*\n/sources/*\n/generated/\n"
            "!/symbols.tsv\n!/structs.tsv\n",encoding="utf-8")

    def test_curated_domain_guides_are_allowlisted_and_discoverable(self):
        guides = ("REF_SAVE_PERSISTENCE.md", "REF_SAVE_FORMAT.md", "REF_RANDOM_EVENTS.md",
                  "REF_RTS_SCENARIO.md", "REF_SCRIPT_VM_CONTEXT.md",
                  "REF_SCENARIO_COMPAT.md", "REF_STRATEGY_ECONOMY.md",
                  "RESEARCH_DUPLICATE_TRIAGE.md")
        readme = (sync.KB / "README.md").read_text(encoding="utf-8")
        gitignore = (sync.KB / ".gitignore").read_text(encoding="utf-8")
        self.assertEqual(len(set(sync.FILES)), len(sync.FILES))
        for name in guides:
            self.assertIn(name, sync.FILES)
            self.assertIn(name, readme)
            self.assertIn("!/" + name, gitignore.splitlines())
            self.assertTrue((sync.KB / name).is_file())

    def test_basic_audit_and_manifest_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            self.fixture(root)
            issues, fp=sync.safe_files(root)
            self.assertEqual(issues, [])
            self.assertEqual(len(fp), len(sync.FILES))
            with patch.object(sync,"KB",root):
                sync.write_manifest(fp)
                self.assertTrue(sync.verify_manifest(fp))
                (root/"symbols.tsv").write_text("edited\n",encoding="utf-8")
                self.assertFalse(sync.verify_manifest(
                    sync.safe_files(root)[1]))

    def test_block_secret_and_oversized_input(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            self.fixture(root)
            email="private"+chr(64)+"example.invalid"
            (root/"symbols.tsv").write_text(email, encoding="utf-8")
            issues,_=sync.safe_files(root)
            self.assertTrue(any("機密" in s for s in issues))
            (root/"symbols.tsv").write_bytes(b"0"*(2_000_001))
            issues,_=sync.safe_files(root)
            self.assertTrue(any("サイズ" in s for s in issues))

    def test_missing_source_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            self.fixture(root)
            (root/"structs.tsv").unlink()
            issues,_=sync.safe_files(root)
            self.assertTrue(any("不足" in s for s in issues))

    def test_git_remote_identity_and_private_requirement(self):
        with patch.object(sync,"ensure_root",return_value=True), \
             patch.object(sync,"git",return_value=(
                  "https://github.com/"+sync.REPO+".git",0)), \
             patch.object(sync,"command",return_value=("PUBLIC",0)):
            with self.assertRaises(sync.Blocked):
                sync.private_repo()
        with patch.object(sync,"ensure_root",return_value=True), \
             patch.object(sync,"git",return_value=("https://example.invalid/repo.git",0)):
            with self.assertRaises(sync.Blocked):
                sync.private_repo()

    def test_lock_exclusive_and_cleanup(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/".git").mkdir()
            with patch.object(sync,"KB",root):
                with sync.lock("test"):
                    with self.assertRaises(sync.Blocked):
                        with sync.lock("other"):
                            pass
                self.assertFalse((root/".git/kb-sync.lock").exists())

    def test_reject_index_byte_mismatch(self):
        def fake_git(*arguments, **kwargs):
            return ("a", 0) if arguments[0] == "hash-object" else ("b", 0)
        with patch.object(sync,"git",side_effect=fake_git):
            with self.assertRaises(sync.Blocked):
                sync.verify_staged_bytes(("symbols.tsv",))

    def test_no_checkpoint_outside_task_branch(self):
        with patch.object(sync,"audit_or_block",return_value={}), \
             patch.object(sync,"lock",return_value=contextlib.nullcontext()), \
             patch.object(sync,"branch",return_value="develop"):
            with self.assertRaises(sync.Blocked):
                sync.checkpoint("KB-TEST")

    def test_no_branch_start_from_dirty_checkout(self):
        with patch.object(sync,"audit_or_block",return_value={}), \
             patch.object(sync,"lock",return_value=contextlib.nullcontext()), \
             patch.object(sync,"branch",return_value="develop"), \
             patch.object(sync,"clean",return_value=False):
            with self.assertRaises(sync.Blocked):
                sync.start("KB-TEST")

    def test_publish_requires_portable_inputs_in_allowlist_and_git_index(self):
        # Local content/freshness checks accept these files even when Git omits them.
        for kind in ("page", "ledger_source", "citation_source", "relation_source", "registry", "ledger"):
            for missing in ("allowlist", "tracked"):
                with self.subTest(kind=kind, missing=missing), tempfile.TemporaryDirectory() as folder:
                    root = Path(folder)
                    def write(name, content):
                        path = root / name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text(content, encoding="utf-8")
                    write(".gitignore", "/*\n")
                    def sha(name):
                        return hashlib.sha256((root / name).read_bytes()).hexdigest()
                    write("symbols.tsv", "0x55BC60\tfunc\tTest\tSummary\tStatic\tF§1\n")
                    write("structs.tsv", "StatusWnd\t0x1C6\tu8\tflag\tSummary\tStatic\tF§1\n")
                    for name in ("ledger_source.md", "citation_source.md", "relation_source.md"):
                        write(name, "Reviewed text without addresses.\n")
                    ledger = "research/recovered/RECOVERY_LEDGER.tsv"
                    write(ledger, "source_path\tsource_sha256\tdestination\tdestination_sha256\treview\n"
                          + "original/never-open.md\t" + sha("ledger_source.md")
                          + "\tledger_source.md\t" + sha("ledger_source.md") + "\treviewed\n")
                    write("reference/sources.json", json.dumps({"F": {
                        "path": "citation_source.md", "sha256": sha("citation_source.md"),
                        "sections": {}}}))
                    write("reference/relations.jsonl", json.dumps({
                        "id": "test", "subject": "va:0x0055BC60", "predicate": "writes",
                        "object": "field:StatusWnd:0x1C6", "summary": "Summary",
                        "confidence": "Static", "target_version": "0.67",
                        "source": {"path": "relation_source.md", "sha256": sha("relation_source.md"),
                                   "start_line": 1, "end_line": 1}}) + "\n")
                    write("RESEARCH_SOURCE_CATALOG.tsv", "\t".join(recovery_coverage.CATALOG_COLUMNS) + "\n")
                    pages = reference.render(root, reference.load(root))
                    for name, content in pages.items():
                        write(name, content)
                    required = set(pages) | {ledger, "reference/sources.json", "reference/relations.jsonl",
                                             "ledger_source.md", "citation_source.md", "relation_source.md"}
                    # The complete publication set succeeds without admitting unrelated files.
                    with patch.object(sync, "KB", root), \
                         patch.object(sync, "ALLOWED", required), \
                         patch.object(sync, "git", return_value=("\0".join(sorted(required)) + "\0", 0)) as index:
                        sync.verify_portable_publication()
                        index.assert_called_once_with("ls-files", "-z")
                    target = {"page": "reference/symbols/0055BC60.md", "ledger": ledger,
                              "registry": "reference/sources.json"}.get(kind, kind + ".md")
                    allowed = required - ({target} if missing == "allowlist" else set())
                    tracked = required - ({target} if missing == "tracked" else set())
                    # Both existing portable checks' content comparisons still pass.
                    self.assertTrue(all((root / name).read_text(encoding="utf-8") == content
                                        for name, content in reference.render(root, reference.load(root)).items()))
                    coverage = recovery_coverage.render(recovery_coverage.inventory(root, tracked))
                    for name, content in coverage.items():
                        write(name, content)
                    self.assertEqual(coverage, recovery_coverage.render(recovery_coverage.inventory(root, tracked)))
                    branch = "work/kb-PORTABLE-TEST"
                    write(".git/kb-sync-base.json", json.dumps({"branch": branch, "base": "base"}))
                    def fake_git(*arguments, **kwargs):
                        if arguments == ("ls-files", "-z"):
                            return "\0".join(sorted(tracked)) + "\0", 0
                        self.fail("Publication reached remote Git before blocking: " + repr(arguments))
                    with patch.object(sync, "KB", root), \
                         patch.object(sync, "ALLOWED", allowed), \
                         patch.object(sync, "audit_or_block", return_value={}), \
                         patch.object(sync, "lock", return_value=contextlib.nullcontext()), \
                         patch.object(sync, "branch", return_value=branch), \
                         patch.object(sync, "clean", return_value=True), \
                         patch.object(sync, "verify_manifest", return_value=True), \
                         patch.object(sync, "private_repo"), \
                         patch.object(sync, "git", side_effect=fake_git), \
                         patch.object(sync, "command", return_value=("PASS", 0)) as check:
                        with self.assertRaisesRegex(sync.Blocked, target):
                            sync.publish()
                        self.assertEqual([Path(call.args[0][2]).name for call in check.call_args_list],
                                         ["reference.py", "recovery_coverage.py"])

    def test_publish_blocks_stale_reference_before_remote_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / ".git").mkdir()
            branch = "work/kb-PORTABLE-TEST"
            (root / ".git/kb-sync-base.json").write_text(
                json.dumps({"branch": branch, "base": "base"}), encoding="utf-8")
            def fake_git(*arguments, **kwargs):
                if arguments == ("rev-parse", "origin/develop"):
                    return "base", 0
                if arguments == ("rev-parse", "HEAD"):
                    return "head", 0
                if arguments[0] == "ls-remote":
                    return "head\trefs/heads/" + branch, 0
                return "", 0
            with patch.object(sync, "KB", root), \
                 patch.object(sync, "audit_or_block", return_value={}), \
                 patch.object(sync, "lock", return_value=contextlib.nullcontext()), \
                 patch.object(sync, "branch", return_value=branch), \
                 patch.object(sync, "clean", return_value=True), \
                 patch.object(sync, "verify_manifest", return_value=True), \
                 patch.object(sync, "private_repo"), \
                 patch.object(sync, "git", side_effect=fake_git) as git, \
                 patch.object(sync, "command", side_effect=sync.Blocked("stale reference")):
                with self.assertRaisesRegex(sync.Blocked, "stale reference"):
                    sync.publish()
                git.assert_not_called()

if __name__=="__main__":
    unittest.main(verbosity=2)

