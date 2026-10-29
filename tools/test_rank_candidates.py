#!/usr/bin/env python3
"""Synthetic isolated coverage for evidence ranking; no protected region decompilation."""
import sqlite3,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import rank_candidates as ranker

class RankingTests(unittest.TestCase):
 def test_rank_evidence_and_rejections(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);kb=root/"knowledge";kb.mkdir()
   (kb/"symbols.tsv").write_text("0x550E70\tfunc\tKnown\tDesc\t静的確認\tSource\n",encoding="utf-8")
   v9=root/"v9.sqlite";c=sqlite3.connect(v9)
   c.executescript("""
    CREATE TABLE functions(entry_va TEXT,size_bytes INTEGER,pseudoc TEXT,is_external INTEGER);
    CREATE TABLE native_callsite(target_va TEXT,opcode_kind TEXT,independently_verified_target INTEGER);
    CREATE TABLE function_range(start_va TEXT,end_va TEXT,function_entry_va TEXT);
   """)
   c.executemany("INSERT INTO functions VALUES(?,?,?,?)",[
    ("0x00500000",120,"native pseudocode data"*8,0),
    ("0x00570FC0",600,"protected overlap",0)])
   c.executemany("INSERT INTO native_callsite VALUES(?,?,?)",[
    ("0x00500000","E8_CALL",1),("0x00500000","E8_CALL",1)])
   c.execute("INSERT INTO function_range VALUES(?,?,?)",
    ("0x00570FC0","0x00571100","0x00570FC0"));c.commit();c.close()
   db=root/"research.sqlite";c=sqlite3.connect(db)
   c.executescript("""
    CREATE TABLE doc_lines(id INTEGER PRIMARY KEY,path TEXT,line_no INTEGER,heading TEXT,text TEXT);
    CREATE TABLE mentions(line_id INTEGER,normalized_va INTEGER,va INTEGER,kind TEXT,path TEXT,line_no INTEGER);
   """)
   samples=[
    (1,"data/T012_MAIN.md",0x500000,0x500000,"func","戦闘"),
    (2,"exe/T012_NATIVE.md",0x500000,0x500000,"func","battle"),
    (3,"data/T012_ONE.md",0x500200,0x500200,"code","戦闘"),
    (4,"data/T012_KNOWN.md",0x550E70,0x550E70,"func","戦闘"),
    (5,"data/T012_PROTECTED.md",0x570FC0,0x5710D0,"func","戦闘")]
   for n,path,va,original,kind,heading in samples:
    c.execute("INSERT INTO doc_lines VALUES(?,?,?,?,?)",(n,path,1,heading,"research text"))
    c.execute("INSERT INTO mentions VALUES(?,?,?,?,?,?)",(n,va,original,kind,path,1))
   c.commit();c.close()
   with patch.object(ranker,"KB",kb):
    rows=ranker.rank(db,v9)
   self.assertEqual([x["va"] for x in rows],["0x500000","0x500200"])
   self.assertEqual(rows[0]["rank"],1)
   self.assertGreater(rows[0]["score"],rows[1]["score"])
   self.assertEqual(rows[0]["verified_native_calls"],2)
   self.assertEqual(rows[0]["source_families"],2)
   self.assertEqual(rows[0]["tier"],"P0")

 def test_output_roundtrip(self):
  with tempfile.TemporaryDirectory() as td:
   out=Path(td)/"candidate_priorities.tsv"
   row={k: "" for k in ranker.COLUMNS};row.update(rank=1,va="0x500000",tier="P0")
   ranker.write_tsv([row],out)
   self.assertIn("0x500000",out.read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main(verbosity=2)

