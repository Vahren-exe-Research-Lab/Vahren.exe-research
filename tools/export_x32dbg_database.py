#!/usr/bin/env python3
"""Export x32dbg labels/comments as a standalone, plain-JSON .dd32 import file.
Never opens the debugger, original executable, or existing user databases.
Requires user to back up existing debugger DB before manual import.
The format is grounded in the x32dbg-generated isolated Notepad smoke database.
"""
import argparse
import json
from pathlib import Path
from verify_debugger_exports import validate,read_script

KB=Path(__file__).resolve().parents[1]
DEFAULT=KB/"generated/x32dbg_knowledge_import.dd32"
MODULE="vahren.exe"

def build_payload(kb=KB):
    result=validate(kb)
    if result["errors"]:
        raise ValueError(f"debugger script validation failed: {result['errors'][:5]}")
    gen=kb/"generated"
    labs,li=read_script(gen/"x32dbg_labels.txt","lbl")
    cmts,ci=read_script(gen/"x32dbg_comments.txt","cmt")
    if li or ci:
        raise ValueError("malformed input command")
    def entry(va,value,comment=False):
        if not (0x400000 < va <= 0xBFFFFF):
            raise ValueError(f"VA out of range: {va}")
        if len(value)>1024 or not value:
            raise ValueError("invalid label/comment")
        # Script escaping is not used by JSON database entries.
        text=value.replace("\\{","{") if comment else value
        return dict(module=MODULE,address=f"0x{va-0x400000:X}",
                    manual=True,text=text)
    return {
      "comments":[entry(va,v,True) for va,v in sorted(cmts.items())],
      "labels":[entry(va,v) for va,v in sorted(labs.items())]
    }

def verify_payload(data, labels_expected=None, comments_expected=None):
    if set(data)!={"comments","labels"}:
        raise ValueError("Only comments and labels are allowed; no debugging state")
    for category in ("comments","labels"):
        addr=set()
        for x in data[category]:
            if set(x)!={"module","address","manual","text"}:
                raise ValueError("Unexpected entry fields")
            if x["module"]!=MODULE or x["manual"] is not True or not x["text"]:
                raise ValueError("Unexpected module/manual/text")
            va=int(x["address"],16)
            if va in addr:raise ValueError("Duplicate RVA")
            addr.add(va)
    if labels_expected is not None and len(data["labels"])!=labels_expected:
        raise ValueError("Label count mismatch")
    if comments_expected is not None and len(data["comments"])!=comments_expected:
        raise ValueError("Comment count mismatch")
    return len(data["labels"]),len(data["comments"])

def export(kb=KB,out=None,check=False):
    out=Path(out) if out else kb/"generated/x32dbg_knowledge_import.dd32"
    data=build_payload(kb)
    num=verify_payload(data)
    if check:
        if not out.is_file():raise FileNotFoundError(out)
        loaded=json.loads(out.read_text(encoding="utf-8"))
        if loaded!=data:raise ValueError("Stale or modified export")
        return num
    out.parent.mkdir(exist_ok=True,parents=True)
    temp=out.with_name(out.name+".tmp")
    if temp.exists():raise FileExistsError(temp)
    temp.write_text(json.dumps(data,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
    if json.loads(temp.read_text(encoding="utf-8"))!=data:
        temp.unlink()
        raise ValueError("Readback mismatch")
    temp.replace(out)
    return num

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--kb",type=Path,default=KB)
    p.add_argument("--output",type=Path)
    p.add_argument("--check",action="store_true")
    a=p.parse_args()
    counts=export(a.kb,a.output,a.check)
    print(("CHECK_PASS" if a.check else "EXPORT_PASS"),
          "labels",counts[0],"comments",counts[1],
          "module",MODULE,"no debugger process accessed")
if __name__=="__main__":main()

