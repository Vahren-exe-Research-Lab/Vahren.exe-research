#!/usr/bin/env python3
"""Non-destructive FTS5 migration benchmark: external doc_lines content + no column sizes.
The source DB is read-only. Output path must not exist; deployment is a separate action.
"""
import argparse,hashlib,sqlite3,statistics,time
from pathlib import Path
PROBES=['"経験値"','"0x54E7B0"','"GUI"','"Battle"','"召喚"']
def hash_file(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for block in iter(lambda:f.read(8*1024*1024),b""):h.update(block)
 return h.hexdigest().upper()
def ro(path):
 return sqlite3.connect(path.resolve().as_uri()+"?mode=ro",uri=True,timeout=60)
def counts(c):
 return tuple(c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
              for t in ["docs","doc_lines","mentions"])
def bench(c):
 out={}
 for term in PROBES:
  samples=[];hits=None
  for _ in range(4):
   begin=time.perf_counter()
   hits=c.execute("SELECT COUNT(*) FROM doc_fts WHERE doc_fts MATCH ?",(term,)).fetchone()[0]
   samples.append(time.perf_counter()-begin)
  out[term]=(hits,round(statistics.median(samples)*1000,3))
 return out
def table_signature(c):
 r=c.execute("SELECT sql FROM sqlite_master WHERE name='doc_fts'").fetchone()
 return r[0] if r else None
def build_optimized(source,target):
 if source.resolve()==target.resolve():raise ValueError("Source DB and output path cannot be identical")
 if target.exists():raise FileExistsError(target)
 target.parent.mkdir(parents=True,exist_ok=True)
 first_hash=hash_file(source)
 begin=time.perf_counter()
 src=ro(source)
 base_counts=counts(src)
 base_query=bench(src)
 print("SOURCE_SIZE",source.stat().st_size,"COUNTS",base_counts,"QUERIES",base_query,flush=True)
 dest=sqlite3.connect(target,timeout=90)
 try:
  src.backup(dest,pages=5000,sleep=0.1)
  dest.commit()
  print("COPY_DONE",round(time.perf_counter()-begin,2),"s",flush=True)
  # Rebuild the index only. Existing report lines, document ids and references persist.
  dest.execute("DROP TABLE doc_fts")
  dest.execute("""CREATE VIRTUAL TABLE doc_fts USING fts5(
     text,content='doc_lines',content_rowid='id',tokenize='trigram',columnsize=0)""")
  dest.executescript("""
   CREATE TRIGGER IF NOT EXISTS doc_lines_fts_ai AFTER INSERT ON doc_lines BEGIN
     INSERT INTO doc_fts(rowid,text) VALUES(new.id,new.text);
   END;
   CREATE TRIGGER IF NOT EXISTS doc_lines_fts_ad AFTER DELETE ON doc_lines BEGIN
     INSERT INTO doc_fts(doc_fts,rowid,text) VALUES('delete',old.id,old.text);
   END;
   CREATE TRIGGER IF NOT EXISTS doc_lines_fts_au AFTER UPDATE ON doc_lines BEGIN
     INSERT INTO doc_fts(doc_fts,rowid,text) VALUES('delete',old.id,old.text);
     INSERT INTO doc_fts(rowid,text) VALUES(new.id,new.text);
   END;
  """)
  dest.execute("INSERT INTO doc_fts(doc_fts) VALUES('rebuild')")
  dest.commit()
  print("FTS_REBUILT",round(time.perf_counter()-begin,2),"s",flush=True)
  # Never compact the user's source. VACUUM only the test copy.
  dest.execute("PRAGMA user_version=2")
  dest.execute("VACUUM")
  print("VACUUM_DONE",round(time.perf_counter()-begin,2),"s",flush=True)
  assert counts(dest)==base_counts
  new_query=bench(dest)
  for term in PROBES:
   if base_query[term][0] != new_query[term][0]:
    raise AssertionError(f"FTS result mismatch: {term}: {base_query[term]} {new_query[term]}")
  dest.execute("SAVEPOINT fts_change_qa")
  dest.execute("INSERT INTO doc_lines(path,line_no,heading,text) VALUES(?,?,?,?)",
      ("__QA_TEST_ONLY__",9876543,"test","本検査用 XYZUNIQUE9026"))
  found=dest.execute("SELECT COUNT(*) FROM doc_fts WHERE doc_fts MATCH ?",('"XYZUNIQUE9026"',)).fetchone()[0]
  assert found==1,("insert trigger failed",found)
  dest.execute("DELETE FROM doc_lines WHERE path=?",("__QA_TEST_ONLY__",))
  found=dest.execute("SELECT COUNT(*) FROM doc_fts WHERE doc_fts MATCH ?",('"XYZUNIQUE9026"',)).fetchone()[0]
  assert found==0,("delete trigger failed",found)
  dest.execute("ROLLBACK TO fts_change_qa")
  dest.execute("RELEASE fts_change_qa")
  assert dest.execute("PRAGMA quick_check").fetchone()[0]=="ok"
  dest.commit()
  print("OUTPUT_SIZE",target.stat().st_size,"COUNTS",counts(dest),
        "QUERIES",new_query,flush=True)
  print("FTS_SCHEMA",table_signature(dest),flush=True)
  print("TESTS_PASS","same document/report count, same FTS hits, triggers, quick_check",flush=True)
 finally:
  dest.close();src.close()
 second_hash=hash_file(source)
 if first_hash != second_hash:raise RuntimeError("source was concurrently modified")
 print("INPUT_SHA_UNCHANGED",first_hash,flush=True)
 print("SIZE_REDUCTION_PERCENT",round(100*(1-target.stat().st_size/source.stat().st_size),2),flush=True)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--source",type=Path,required=True)
 p.add_argument("--output",type=Path,required=True)
 a=p.parse_args()
 build_optimized(a.source,a.output)
if __name__=="__main__":main()

