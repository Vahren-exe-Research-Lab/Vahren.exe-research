#!/usr/bin/env python3
"""Isolated regression tests: no project source files or main databases are changed."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import check_symbols as qa
import research_index as idx

class SymbolQualityTests(unittest.TestCase):
    def test_valid_and_duplicate_va_name(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "symbols.tsv"
            p.write_text(
                "0x550E70\tfunc\tDamage_Core\tダメージ\t静的確認\tT012§3\n"
                "0x57B870\tfunc\tDamage_Core\tAI\t推定\tT013§1\n",
                encoding="utf-8")
            r = qa.audit(p, None)
            self.assertTrue(any("名前が重複" in s for s in r["errors"]))
            p.write_text(
                "0x550E70\tfunc\tDamage_Core\tダメージ\t静的確認\tT012§3\n"
                "0x550E70\tfunc\tDamage_Other\t別名\t推定\tT013§1\n",
                encoding="utf-8")
            r = qa.audit(p, None)
            self.assertTrue(any("VAが重複" in s for s in r["errors"]))

    def test_bad_columns_confidence_and_source(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.tsv"
            p.write_text(
                "0x550E70\tfunc\tBroken\n"
                "0x57B870\tfunc\tAi_Search\t説明\t確定\t\n", encoding="utf-8")
            r = qa.audit(p, None)
            self.assertGreaterEqual(len(r["errors"]), 3)

    def test_confidence_upgrade_requires_human_review(self):
        with tempfile.TemporaryDirectory() as d:
            old, new = (Path(d) / x for x in ("old.tsv","new.tsv"))
            fmt = "0x550E70\tfunc\tDamage_Core\t説明\t{}\tT012§3\n"
            old.write_text(fmt.format("推定"),encoding="utf-8")
            new.write_text(fmt.format("実機確認"),encoding="utf-8")
            r = qa.audit(new, None, old)
            self.assertEqual(r["errors"], [])
            self.assertTrue(any("確度の引上げ" in s for s in r["warnings"]))
            self.assertTrue(any("source不変" in s for s in r["warnings"]))

    def test_protected_and_owner_mapping(self):
        self.assertEqual(idx.normalize_va(0x57AADF,
                         [(0x57AA00,0x57AB00,0x57AA00)],[0x57AA00]),
                         (0x57AA00,0x57AA00,"func"))
        data = "# 検証\nコード0x57AADF、保護0x5710C0、定数0x65BF18"
        lines, refs = idx.extract(data, [], [])
        self.assertEqual(len(lines),2)
        self.assertEqual({r[1] for r in refs},
                         {0x57AADF,0x5710C0,0x65BF18})

class ResearchIndexTests(unittest.TestCase):
    def test_incremental_discovery_and_safe_pending(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            kb = root/"knowledge"
            gen = kb/"generated"
            (root/"data").mkdir()
            gen.mkdir(parents=True)
            src = root/"data/T012_REPORT.md"
            src.write_text(
                "# 戦闘\n0x550E70 damage\n"
                "0x57B870 AI\n"
                "0x5710C0 旧安全拒否\n"
                "経験値という語も記録する。\n",encoding="utf-8")
            manual = kb/"symbols.tsv"
            manual.write_text(
                "0x550E70\tfunc\tDamage_Core\t説明\t静的確認\tT012\n",encoding="utf-8")
            patches = [
                patch.object(idx,"ROOT",root),
                patch.object(idx,"KB",kb),
                patch.object(idx,"DB",gen/"research.sqlite"),
                patch.object(idx,"CANDIDATES",gen/"address_candidates.tsv"),
                patch.object(idx,"RECENT_CANDIDATES",gen/"address_candidates_recent.tsv"),
                patch.object(idx,"SYMBOLS",manual),
                patch.object(idx,"V9",root/"missing-v9.sqlite"),
            ]
            for p in patches: p.start()
            try:
                self.assertEqual(idx.main([]),0)
                self.assertEqual(idx.main(["--check"]),0)
                text = (gen/"address_candidates.tsv").read_text(encoding="utf-8")
                self.assertIn("0x57B870",text)
                self.assertNotIn("0x5710C0",text)
                self.assertNotIn("0x550E70",text)
                recent=(gen/"address_candidates_recent.tsv").read_text(encoding="utf-8")
                self.assertIn("0x57B870",recent)
                self.assertNotIn("0x5710C0",recent)
                c = sqlite3.connect(gen/"research.sqlite")
                self.assertEqual(c.execute("SELECT COUNT(*) FROM docs").fetchone()[0],1)
                self.assertEqual(c.execute("SELECT COUNT(*) FROM mentions").fetchone()[0],3)
                self.assertEqual(c.execute("SELECT COUNT(*) FROM doc_lines").fetchone()[0],5)
                if c.execute("SELECT 1 FROM sqlite_master WHERE name='doc_fts'").fetchone():
                    n=c.execute("SELECT COUNT(*) FROM doc_fts WHERE doc_fts MATCH ?",
                                ('"経験値"',)).fetchone()[0]
                    self.assertEqual(n,1)
                c.close()
                src.write_text("# 戦闘\n0x579940 newer\n",encoding="utf-8")
                self.assertNotIn("0x579940",recent)
                self.assertEqual(idx.main(["--check"]),1)
                self.assertEqual(idx.main([]),0)
                recent=(gen/"address_candidates_recent.tsv").read_text(encoding="utf-8")
                self.assertIn("0x579940",recent)
                self.assertEqual(idx.main(["--check"]),0)
                c = sqlite3.connect(gen/"research.sqlite")
                self.assertEqual(c.execute("SELECT COUNT(*) FROM mentions").fetchone()[0],1)
                c.close()
                src.unlink()
                self.assertEqual(idx.main([]),0)
                c = sqlite3.connect(gen/"research.sqlite")
                self.assertEqual(c.execute("SELECT COUNT(*) FROM docs").fetchone()[0],0)
                c.close()
            finally:
                for p in reversed(patches): p.stop()

if __name__ == "__main__":
    unittest.main(verbosity=2)

