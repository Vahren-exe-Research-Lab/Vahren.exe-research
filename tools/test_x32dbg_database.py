#!/usr/bin/env python3
"""Standalone x32dbg .dd32 JSON export tests (no GUI/debuggee use)."""
import json,tempfile,unittest
from pathlib import Path
import export_x32dbg_database as exporter

class X32DatabaseTests(unittest.TestCase):
 def setup_kb(self,root):
  generated=root/"generated";generated.mkdir()
  source=root/"sources";source.mkdir()
  (generated/"symbols_all.tsv").write_text(
   "0x401010\tTest_Label\tfunc\n",encoding="utf-8")
  (generated/"x32dbg_labels.txt").write_text(
   '// test\nlbl Vahren.exe+1010, "Test_Label"\n',encoding="utf-8")
  (generated/"x32dbg_comments.txt").write_text(
   'cmt Vahren.exe+1010, "Test_Comment"\n',encoding="utf-8")
  (source/"legacy_comments_20261011.tsv").write_text("",encoding="utf-8")
 def test_no_debugger_or_debuggee_required(self):
  with tempfile.TemporaryDirectory() as folder:
   kb=Path(folder);self.setup_kb(kb)
   out=kb/"generated/sample.dd32"
   self.assertEqual(exporter.export(kb,out),(1,1))
   self.assertEqual(exporter.export(kb,out,True),(1,1))
   data=json.loads(out.read_text(encoding="utf-8"))
   self.assertEqual(set(data),{"comments","labels"})
   self.assertEqual(data["labels"][0],{
    "module":"vahren.exe","address":"0x1010",
    "manual":True,"text":"Test_Label"})
   self.assertEqual(data["comments"][0]["text"],"Test_Comment")
   self.assertNotIn("hash",data)
 def test_stale_output_rejected(self):
  with tempfile.TemporaryDirectory() as folder:
   kb=Path(folder);self.setup_kb(kb);out=kb/"generated/sample.dd32"
   exporter.export(kb,out)
   out.write_text("{}")
   with self.assertRaises(ValueError):exporter.export(kb,out,True)
 def test_duplicate_rva_rejected(self):
  with self.assertRaises(ValueError):
   exporter.verify_payload({"comments":[],"labels":[
     dict(module="vahren.exe",address="0x1010",manual=True,text="A"),
     dict(module="vahren.exe",address="0x1010",manual=True,text="B")]})
if __name__=="__main__":unittest.main(verbosity=2)

