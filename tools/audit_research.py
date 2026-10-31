#!/usr/bin/env python3
"""Read-only PC research inventory. Metadata and candidate duplicates are not gameplay proof."""
import argparse
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
import re
import sqlite3

TASK_RE = re.compile(r'(?<![A-Za-z0-9])T(0[0-3][0-9])(?![0-9])', re.I)
ID_RE = re.compile(r'\b(?:[A-E]-|EXP-|REA-|RC-)[A-Z0-9_-]{8,95}\b', re.I)
PRIVATE = re.compile(r'(?i)([A-Z]:[\\/]+Users[\\/]|[\w.+-]+@[\w.-]+\.\w+|github_pat_|gh[pousr]_)')
GROUPS = {
    "A":{"005","006","009","010","014","023","031"},
    "B":{"011","012","013","024","028"},
    "C":{"016","025","026","027","029","032","033","034"},
    "D":{"015","017","030"},
    "E":{"018","019","020"}
}
DOMAINS = {
    "011":"UNIT_SKILL_EXP","012":"BATTLE_DAMAGE","013":"AI_TARGET",
    "024":"AI_TARGET","028":"MORALE_RETREAT","005":"SCRIPT_VM",
    "006":"SCRIPT_VM","009":"SCRIPT_VM","010":"SCRIPT_VM",
    "014":"SAVE","023":"ENGINE","031":"RNG",
    "016":"STRATEGY","025":"STRATEGY","026":"STRATEGY",
    "027":"STRATEGY","029":"STRATEGY","032":"EVENT",
    "033":"EVENT","034":"EVENT","015":"RTS_UI",
    "017":"RTS_UI","030":"RTS_UI","018":"GOLDEN_QA",
    "019":"GOLDEN_QA","020":"GOLDEN_QA"
}

def scrub(x):
    s = str(x).replace("\t"," ").replace("\n"," ").replace("\r"," ").strip()
    return "[REDACTED]" if PRIVATE.search(s) else s

def classify(rel,head):
    name = Path(rel).name
    tasks = sorted(set(TASK_RE.findall(name)))
    if not tasks: tasks = sorted(set(TASK_RE.findall(head[:800])))
    owner = ",".join(sorted(g for g,ts in GROUPS.items() if set(tasks)&ts))
    if name=="MASTER_LEDGER.md":
        return "COORD",[],"COORDINATION"
    if "HANDOFF" in name.upper():
        return owner or "COORD",tasks,"COORDINATION"
    if rel.startswith("rea_lab/"):
        return owner or "REA",tasks,DOMAINS.get(tasks[0],"GHIDRA_INDEX") if tasks else "GHIDRA_INDEX"
    if rel.startswith("exp_research_"):
        return owner or "B",tasks or ["011"],"UNIT_SKILL_EXP"
    if rel.startswith("dev_lab/"):
        return owner or "DEV",tasks,DOMAINS.get(tasks[0],"IMPLEMENTATION") if tasks else "IMPLEMENTATION"
    if tasks: return owner or "REVIEW",tasks,DOMAINS.get(tasks[0],"OTHER_TASK")
    return owner or "REVIEW",tasks,"UNCLASSIFIED"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args = ap.parse_args()
    root = args.root.resolve()
    db = root/"knowledge/generated/research.sqlite"
    conn = sqlite3.connect(db.resolve().as_uri()+"?mode=ro",uri=True)
    docs = conn.execute("SELECT path,sha256,bytes,lines,mentions FROM docs ORDER BY path").fetchall()
    conn.close()
    rows,missing,stale = [],[],[]
    by_sha,by_id = defaultdict(list),defaultdict(list)
    domains = Counter()
    redacted = 0
    for rel,sha,size,lines,mentions in docs:
        source = (root/rel).resolve()
        if not source.is_relative_to(root) or not source.is_file():
            missing.append(rel)
            continue
        raw = source.read_bytes()
        if len(raw)!=size or hashlib.sha256(raw).hexdigest().lower()!=sha.lower():
            stale.append(rel)
            continue
        head=raw[:2048].decode("utf-8-sig",errors="replace")
        owner,tasks,domain=classify(rel,head)
        ids=ID_RE.findall(head[:1000])
        rid=ids[0].strip("-_") if ids else "UNSET"
        vals=[rel,sha,size,lines,mentions,owner,",".join("T"+x for x in tasks),domain,rid]
        safe=list(map(scrub,vals))
        redacted+=int(safe[0]=="[REDACTED]")
        rows.append(safe)
        by_sha[sha].append(rel)
        if rid != "UNSET": by_id[rid].append(rel)
        domains[domain]+=1
    exact={h:paths for h,paths in by_sha.items() if len(paths)>1}
    shared={i:paths for i,paths in by_id.items() if len(paths)>1}
    out=args.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    header="path\tsha256\tbytes\tlines\tva_mentions\towner\ttasks\tdomain\tresearch_id\n"
    (out/"RESEARCH_SOURCE_CATALOG.tsv").write_text(header+"".join("\t".join(map(str,x))+"\n" for x in rows),encoding="utf-8",newline="\n")
    dup_header="type\tkey\tcount\tpaths\n"
    dup_lines=[
        "\t".join((kind,scrub(key),str(len(paths)),
                   scrub(" | ".join(paths[:8]) +
                         (f" | [OMITTED_{len(paths)-8}_PATHS]" if len(paths)>8 else ""))))
        for kind,groups in (("EXACT_SHA256",exact),("SHARED_ID_REVIEW",shared))
        for key,paths in sorted(groups.items())
    ]
    (out/"RESEARCH_DUPLICATE_CANDIDATES.tsv").write_text(dup_header+"\n".join(dup_lines)+"\n",encoding="utf-8",newline="\n")
    lines=[
        "# Research source integration snapshot","",
        "This is a metadata inventory, NOT a validation of all research findings.",
        "GitHub does not contain original game files or the generated search database.","",
        f"- Indexed research documents: {len(docs)}",
        f"- Indexed lines: {sum(int(d[3]) for d in docs):,}",
        f"- Indexed VA mentions: {sum(int(d[4]) for d in docs):,}",
        f"- Catalog source receipts: {len(rows)}; missing: {len(missing)}; stale SHA/size: {len(stale)}; redacted path entries: {redacted}",
        f"- Exact-byte duplicate groups: {len(exact)}, total referenced files: {sum(len(v) for v in exact.values())}",
        f"- Shared-primary-ID candidate groups: {len(shared)} (NOT automatically duplicates)","",
        "## Automatic tentative classification","",
        "| Category | Indexed sources |","|---|---:|"
    ]
    lines += [f"| {key} | {count} |" for key,count in sorted(domains.items(),key=lambda x:(-x[1],x[0]))]
    lines += ["","## Review rules","",
        "1. Cross-check research IDs, original ASM/DAT and prior corrections before extracting conclusions.",
        "2. Duplicate SHA means identical content only; duplicate ID can be an expected detail/HANDOFF mirror.",
        "3. Never upgrade STATIC, INFERRED, VERIFY, DYNAMIC or Golden/READY based on metadata.",
        "4. Do not import blocked/refused source payloads or analyze the prohibited address range.",
        "5. The catalog is intentionally paths/SHA and task suggestions; it cannot replace local source files.",
        "6. The search index excludes binaries and over-limit documents, so this is NOT full project backup.",
        "7. Review domain guesses, especially multi-task files, before publication as verified facts.",
        ""]
    (out/"RESEARCH_INTEGRATION_SNAPSHOT.md").write_text("\n".join(lines),encoding="utf-8",newline="\n")
    print(f"INVENTORY_OK indexed={len(docs)} exported={len(rows)} missing={len(missing)} stale={len(stale)} "
          f"exact_sha_groups={len(exact)} shared_id_groups={len(shared)} redacted={redacted}")
    print("TOP_DOMAINS",domains.most_common(16))
    if missing: print("MISSING",missing[:10])
    if stale: print("STALE_SOURCE",stale[:10])

if __name__=="__main__":
    main()
