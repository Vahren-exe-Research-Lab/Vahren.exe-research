#!/usr/bin/env python3
"""Validate x32dbg label/comment scripts without touching a running debugger.
Expected syntax: lbl Vahren.exe+RVA, "name" and cmt Vahren.exe+RVA, "text".
"""
import argparse,csv,json,re
from pathlib import Path
KB=Path(__file__).resolve().parents[1]
RE_COMMAND=re.compile(r'^(lbl|cmt) Vahren\.exe\+([0-9A-Fa-f]+), "((?:[^"\\]|\\.)*)"$')
def read_script(path,expected):
 out={};issues=[]
 for i,line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(),1):
  if not line or line.startswith("//"):continue
  m=RE_COMMAND.fullmatch(line)
  if not m:
   issues.append(f"{path.name}:{i}: syntax invalid")
   continue
  command,offset,value=m.groups()
  if command!=expected:
   issues.append(f"{path.name}:{i}: expected {expected}")
  if not value or '"' in value:
   issues.append(f"{path.name}:{i}: invalid quotation")
  if re.search(r"(?<!\\)\{",value):
   issues.append(f"{path.name}:{i}: unescaped formatting brace")
  if len(value)>1024:
   issues.append(f"{path.name}:{i}: text over 1024 chars")
  va=0x400000+int(offset,16)
  if not 0x401000<=va<=0xBFFFFF:
   issues.append(f"{path.name}:{i}: out-of-range VA")
  if va in out:
   issues.append(f"{path.name}:{i}: duplicate VA")
  out[va]=value
 return out,issues
def validate(kb=KB):
 base=kb/"generated"
 syms={};errors=[]
 p=base/"symbols_all.tsv"
 for i,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
  if line.startswith("#") or not line:continue
  cols=line.split("\t")
  if len(cols)<2:
   errors.append(f"symbols_all.tsv:{i}: expected VA and name");continue
  va=int(cols[0],16)
  syms[va]=cols[1]
 labels,issues=read_script(base/"x32dbg_labels.txt","lbl");errors+=issues
 comments,issues=read_script(base/"x32dbg_comments.txt","cmt");errors+=issues
 for va,name in syms.items():
  if labels.get(va)!=name:
   errors.append(f"label mismatch: 0x{va:06X}")
 for va in labels.keys()-syms.keys():
  errors.append(f"unknown label: 0x{va:06X}")
 # Legacy instruction-site comments legitimately target unnamed addresses.
 legacy=set()
 for line in (kb/"sources/legacy_comments_20261011.tsv").read_text(encoding="utf-8").splitlines():
  if "\t" in line:
   legacy.add(int(line.split("\t",1)[0],16))
 for va in comments:
  if va not in syms and va not in legacy:
   errors.append(f"unknown comment VA: 0x{va:06X}")
 return {"all_symbols":len(syms),"labels":len(labels),"comments":len(comments),
         "errors":errors,"label_examples":[(hex(k),v) for k,v in list(labels.items())[:3]],
         "test_scope":"offline-script-syntax-and-symbol-mapping"}
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--kb",type=Path,default=KB)
 ap.add_argument("--json",action="store_true")
 a=ap.parse_args()
 result=validate(a.kb)
 if a.json:print(json.dumps(result,ensure_ascii=False,indent=2))
 else:
  print("x32dbg scripts",result["labels"],"labels",
        result["comments"],"comments",len(result["errors"]),"errors")
  for e in result["errors"][:20]:print("ERROR",e)
 return 1 if result["errors"] else 0
if __name__=="__main__":
 raise SystemExit(main())

