#!/usr/bin/env python3
"""Offline regression tests for knowledge source audits and Git safety gates."""
import contextlib
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sync_knowledge as sync

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

if __name__=="__main__":
    unittest.main(verbosity=2)

