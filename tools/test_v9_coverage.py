#!/usr/bin/env python3
"""Synthetic tests for Ghidra V9 static graph coverage (no game/real DB writes)."""
import contextlib
import io
from pathlib import Path
import sqlite3
import tempfile
import unittest
import v9_coverage as cv

def fixture(root):
    v9 = root/cv.V9_REL
    v9.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(v9)
    c.execute("CREATE TABLE functions(entry_va TEXT,name TEXT,size_bytes INT,is_external INT,pseudoc TEXT)")
    c.execute("CREATE TABLE function_body(entry_va TEXT)")
    c.execute("CREATE TABLE function_range(start_va TEXT,end_va TEXT,function_entry_va TEXT)")
    c.execute("CREATE TABLE native_callsite(site_va TEXT,target_va TEXT,caller_function_va TEXT,opcode_kind TEXT,independently_verified_target INT,native_opcode_hex TEXT)")
    c.execute("CREATE TABLE ghidra_refs(target_va TEXT,ref_class TEXT)")
    c.execute("CREATE TABLE unresolved_control(owner_va TEXT)")
    functions=[
        ("0x00449500","FUN_00449500",513,0,"pseudoc data "+"x"*60),
        ("0x0046F4C0","FUN_0046f4c0",555,0,"pseudoc data "+"x"*60),
        ("0x005710A0","FUN_005710A0",30,0,"pseudoc data "+"x"*60),
        ("0x00700100","SomeExternal",0,1,"")]
    c.executemany("INSERT INTO functions VALUES (?,?,?,?,?)",functions)
    c.executemany("INSERT INTO function_body VALUES (?)",
                  [(x[0],) for x in functions[:3]])
    c.executemany("INSERT INTO function_range VALUES (?,?,?)", [
        ("0x00449500","0x00449600","0x00449500"),
        ("0x0046F4C0","0x0046F500","0x0046F4C0"),
        ("0x005710A0","0x00571100","0x005710A0")])
    c.executemany("INSERT INTO native_callsite VALUES (?,?,?,?,?,?)", [
        ("0x0046F4C4","0x00449500","0x0046F4C0","E8_DIRECT_CALL",1,"e800000000"),
        ("0x0046F4CE","0x005710A0","0x0046F4C0","E8_DIRECT_CALL",1,"e800000000"),
        ("0x00449564","0x0046F4C0","0x00449500","E9_TAIL_JMP",1,"e900000000")])
    c.executemany("INSERT INTO ghidra_refs VALUES (?,?)", [
        ("Stack[0x4]","DATA"),("0x00449500","CALL")])
    c.execute("INSERT INTO unresolved_control VALUES (?)",("0x00449500",))
    c.commit()
    c.close()
    db=root/cv.RESEARCH_REL
    db.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(db)
    c.execute("CREATE TABLE mentions(normalized_va INT,path TEXT)")
    c.execute("CREATE TABLE docs(path TEXT)")
    c.execute("INSERT INTO mentions VALUES (?,?)",(0x449500,"data/T013_RESEARCH.md"))
    c.execute("INSERT INTO docs VALUES (?)",("data/T013_RESEARCH.md",))
    c.commit()
    c.close()
    (root/"data").mkdir(exist_ok=True)
    (root/"data/T013_RESEARCH.md").write_text("T013 evidence\n",encoding="utf-8")
    (root/"knowledge/symbols.tsv").write_text(
        "0x0046F4C0\tfunc\tConfig_Get\tGetter\t静的確認\tT013\n",encoding="utf-8")

class CoverageTests(unittest.TestCase):
    def test_symbolic_reference_and_protected_range(self):
        self.assertIsNone(cv.number("Stack[0x4]"))
        self.assertIsNone(cv.number("Register"))
        self.assertEqual(cv.number("0x00449500"),0x449500)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            fixture(root)
            data=cv.load(root)
            self.assertIn(0x5710A0,data["denied"])
            self.assertEqual(data["ghidra"][0x449500],1)
            self.assertEqual(data["incoming"][0x449500],1)
            self.assertEqual(data["verified_e8"],1)
            self.assertEqual(data["skipped_native_sites"],1)
            self.assertEqual(data["branches"],1)
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(cv.inspect(data,"0x005710A0"),2)
            self.assertIn("BLOCKED_PROTECTED_RANGE",output.getvalue())
            with contextlib.redirect_stdout(io.StringIO()) as actual:
                self.assertEqual(cv.inspect(data,"0x00449520"),0)
            self.assertIn('"query_va": "0x00449520"',actual.getvalue())
            self.assertIn('"site_va": "0x0046F4C4"',actual.getvalue())

    def test_crosswalk_export_and_no_source_changes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            fixture(root)
            original=(root/"data/T013_RESEARCH.md").read_bytes()
            data=cv.load(root)
            rows,candidates=cv.make_rows(data)
            self.assertEqual(len(rows),2)
            self.assertEqual(len(candidates),1)
            self.assertEqual(candidates[0]["va"],"0x00449500")
            self.assertEqual(candidates[0]["focused_docs"],1)
            out=root/"export"
            with contextlib.redirect_stdout(io.StringIO()):
                cv.emit(root,out,data,rows,candidates)
            self.assertEqual((root/"data/T013_RESEARCH.md").read_bytes(),original)
            self.assertTrue((out/"GHIDRA_V9_COVERAGE_REPORT.md").is_file())
            self.assertTrue((out/"GHIDRA_V9_GAPS_TOP500.tsv").is_file())
            self.assertTrue((root/"knowledge/generated/V9_FUNCTION_CROSSWALK.tsv").is_file())
            report=(out/"GHIDRA_V9_COVERAGE_REPORT.md").read_text(encoding="utf-8")
            self.assertIn("Internal entries without an indexed report",report)
            self.assertIn("Excluded native sites with protected owner/address",report)
            self.assertIn("without an indexed report: **1**",report)
            self.assertNotIn("0x005710A0", (out/"GHIDRA_V9_GAPS_TOP500.tsv").read_text(encoding="utf-8"))

    def test_no_false_semantics_for_symbolic_pointers(self):
        self.assertEqual(cv.clean("line\twith\nspaces"), "line with spaces")
        self.assertIsNone(cv.number("Stack[0x4]"))
        self.assertIsNone(cv.number("undefined8"))
        self.assertEqual(cv.nested_reason(Path("rea_lab/_history_20261029/a.md")),"NESTED_HISTORY_ARCHIVE")
        self.assertEqual(cv.nested_reason(Path("data/recruit_sort_v4/tests/a.json")),"NESTED_PLUGIN_WORKTREE")
        self.assertEqual(cv.nested_reason(Path("rea_lab/P0_TAKEOVER_20261024_01/runtime/a.json")),"NESTED_RUNTIME_LOGS")
        self.assertIsNone(cv.number(""))

if __name__=="__main__":
    unittest.main()
