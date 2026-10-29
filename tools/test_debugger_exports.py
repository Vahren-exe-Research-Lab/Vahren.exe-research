#!/usr/bin/env python3
"""Offline x32dbg command generation regressions."""
import tempfile,unittest
from pathlib import Path
import verify_debugger_exports as checker
class DebuggerExportTests(unittest.TestCase):
 def fixture(self,root):
  (root/"generated").mkdir()
  (root/"sources").mkdir()
  (root/"generated/symbols_all.tsv").write_text("0x401010\tFuncLabel\tfunc\n",encoding="utf-8")
  (root/"generated/x32dbg_labels.txt").write_text('lbl Vahren.exe+1010, "FuncLabel"\n',encoding="utf-8")
  (root/"generated/x32dbg_comments.txt").write_text('cmt Vahren.exe+1020, "Instruction comment"\n',encoding="utf-8")
  (root/"sources/legacy_comments_20261011.tsv").write_text("0x401020\tInstruction comment\n",encoding="utf-8")
 def test_legacy_comment_without_symbol(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);self.fixture(root)
   result=checker.validate(root)
   self.assertEqual(result["errors"],[])
   self.assertEqual(result["comments"],1)
 def test_duplicate_comment_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);self.fixture(root)
   p=root/"generated/x32dbg_comments.txt"
   p.write_text('cmt Vahren.exe+1020, "first"\ncmt Vahren.exe+1020, "second"\n',encoding="utf-8")
   result=checker.validate(root)
   self.assertTrue(any("duplicate" in s for s in result["errors"]))
 def test_malformed_command_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);self.fixture(root)
   (root/"generated/x32dbg_labels.txt").write_text('lbl Vahren.exe+1010, "bad\n',encoding="utf-8")
   result=checker.validate(root)
   self.assertTrue(result["errors"])
if __name__=="__main__":unittest.main(verbosity=2)

