#!/usr/bin/env python3
"""Read-only Ghidra V9 coverage / corpus crosswalk; no decompilation or game execution."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sqlite3

V9_REL = "rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite"
RESEARCH_REL = "knowledge/generated/research.sqlite"
PROTECTED = (0x5710C0, 0x571500)
TEXT = {".md", ".txt", ".json", ".jsonl", ".csv", ".tsv", ".py", ".java"}
INDEX_EXT = {".md", ".txt", ".json", ".jsonl", ".csv", ".tsv"}
INDEX_MAX = 3_000_000
FOLDERS = ("data", "exe", "evidence", "exp_research_20261021", "tests", "wiki",
           "rea_lab/headless_analysis/search_index", "dev_lab/docs")
COLUMNS = ("rank", "va", "name", "score", "research_docs", "research_mentions",
           "verified_e8_callers", "verified_e8_callees", "ghidra_xrefs",
           "unresolved_sites", "focused_docs", "pseudoc", "size_bytes", "task_hint",
           "example_path", "evidence_state")

def number(value):
    if isinstance(value, int):
        return value
    text = str(value or "")
    if not re.fullmatch(r"(?i)(?:0x)?[0-9a-f]{6,8}", text):
        return None  # Ghidra refs may use Stack[0x4], register, or symbolic targets.
    return int(text, 16)

def ro(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError("Missing indexed source: " + path.name)
    return sqlite3.connect(path.resolve().as_uri()+"?mode=ro&immutable=1", uri=True)

def known_symbols(path):
    found = set()
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("0x"):
            found.add(int(line.split("\t", 1)[0], 16))
    return found

def clean(value):
    s = str(value or "").replace("\t", " ").replace("\r", " ").replace("\n", " ")
    s = re.sub(r"(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s]+", "[LOCAL]", s)
    return s[:150]

def protected_members(c):
    denied = set()
    for start, end, owner in c.execute(
            "SELECT start_va,end_va,function_entry_va FROM function_range"):
        if number(start) <= PROTECTED[1] and number(end) >= PROTECTED[0]:
            denied.add(number(owner))
    return denied

def load(root, symbols_path=None):
    root = Path(root)
    c = ro(root/V9_REL)
    functions = {}
    for va, name, size, external, pseudoc in c.execute(
            "SELECT entry_va,name,size_bytes,is_external,"
            "CASE WHEN length(pseudoc)>50 THEN 1 ELSE 0 END FROM functions"):
        if not external:
            functions[number(va)] = dict(
                name=clean(name), size=int(size or 0), pseudoc=int(pseudoc))
    denied = protected_members(c)
    inward = Counter()
    outward = Counter()
    ghidra = Counter()
    unresolved = Counter()
    verified_e8 = 0
    indexed_branches = 0
    skipped_sites = 0
    for site, target, caller, kind, verified in c.execute(
            "SELECT site_va,target_va,caller_function_va,opcode_kind,"
            "independently_verified_target FROM native_callsite"):
        if (site and PROTECTED[0] <= (number(site) or 0) <= PROTECTED[1]) or (caller and number(caller) in denied) or (target and number(target) in denied):
            skipped_sites += 1
            continue
        if kind == "E8_DIRECT_CALL" and int(verified or 0) == 1:
            verified_e8 += 1
            if target and number(target) in functions:
                inward[number(target)] += 1
            if caller and number(caller) in functions:
                outward[number(caller)] += 1
        else:
            indexed_branches += 1
    for target, refclass in c.execute("SELECT target_va,ref_class FROM ghidra_refs"):
        if target:
            addr = number(target)
            if addr in functions:
                ghidra[addr] += 1
    for (owner,) in c.execute("SELECT owner_va FROM unresolved_control"):
        if owner and number(owner) in functions:
            unresolved[number(owner)] += 1
    counts = {table: c.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]
              for table in ("functions", "function_body", "native_callsite",
                            "ghidra_refs", "unresolved_control")}
    c.close()
    docinfo = {}
    d = ro(root/RESEARCH_REL)
    for va, n_docs, mentions, focused, sample in d.execute(
            "SELECT normalized_va,COUNT(DISTINCT path),COUNT(*),"
            "COUNT(DISTINCT CASE WHEN path LIKE 'data/%' OR path LIKE 'exe/%' "
            "OR path LIKE 'wiki/%' OR path LIKE 'exp_research_%' "
            "THEN path END),"
            "COALESCE(MIN(CASE WHEN path LIKE 'data/%' THEN path END),"
            "MIN(CASE WHEN path LIKE 'exe/%' THEN path END),"
            "MIN(CASE WHEN path LIKE 'exp_research_%' THEN path END),"
            "MIN(CASE WHEN path LIKE 'wiki/%' THEN path END),MIN(path))"
            " FROM mentions GROUP BY normalized_va"):
        docinfo[number(va)] = (int(n_docs), int(mentions), clean(sample), int(focused))
    indexed_paths = {r[0] for r in d.execute("SELECT path FROM docs")}
    d.close()
    named = known_symbols(Path(symbols_path) if symbols_path else root/"knowledge/symbols.tsv")
    digest = hashlib.sha256()
    with (root/V9_REL).open("rb") as source:
        for block in iter(lambda: source.read(4*1024*1024),b""):
            digest.update(block)
    return dict(root=root, v9_sha256=digest.hexdigest().upper(),
                functions=functions, denied=denied, incoming=inward,
                outgoing=outward, ghidra=ghidra, unresolved=unresolved,
                docinfo=docinfo, indexed_paths=indexed_paths, named=named,
                counts=counts, verified_e8=verified_e8, branches=indexed_branches,
                skipped_native_sites=skipped_sites)

def make_rows(data):
    rows = []
    for va, meta in data["functions"].items():
        if va in data["denied"] or PROTECTED[0] <= va <= PROTECTED[1]:
            continue
        docs, mentions, example, focused = data["docinfo"].get(va, (0, 0, "", 0))
        inbound = data["incoming"][va]
        outbound = data["outgoing"][va]
        xrefs = data["ghidra"][va]
        unknown = data["unresolved"][va]
        registered = va in data["named"]
        hint = ",".join(sorted(set(re.findall(r"T0[0-3][0-9]", example)))) or "UNASSIGNED"
        score = round(7*math.log2(1+inbound) +
                      5*math.log2(1+outbound) +
                      3*math.log2(1+docs) +
                      7*math.log2(1+focused) +
                      2*math.log2(1+xrefs) +
                      3*math.log2(1+unknown) +
                      2*meta["pseudoc"], 2)
        is_runtime = bool(re.match(r"(?i)^(?:_|fid_conflict:|operator|exception$|getdataindirecttype|getzname)",meta["name"]))
        rows.append(dict(va=f"0x{va:08X}", name=meta["name"], score=score,
                         research_docs=docs, research_mentions=mentions,
                         verified_e8_callers=inbound, verified_e8_callees=outbound,
                         ghidra_xrefs=xrefs, unresolved_sites=unknown,
                         focused_docs=focused,
                         pseudoc=meta["pseudoc"], size_bytes=meta["size"],
                         task_hint=hint, example_path=example,
                         evidence_state="V9_STATIC_INDEX",
                         registered=int(registered), runtime_hint=int(is_runtime)))
    rows.sort(key=lambda x: (-x["score"], -x["research_docs"],
                             -x["verified_e8_callers"], x["va"]))
    unregistered = [dict(rank=i, **{key: value for key, value in item.items()
                                    if key not in ("registered", "runtime_hint")})
                    for i, item in enumerate((r for r in rows if not r["registered"]
                                             and not r["runtime_hint"]), 1)]
    return rows, unregistered

def write_tsv(path, fields, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def nested_reason(path):
    parts = path.parts
    if any("_history_" in segment for segment in parts):
        return "NESTED_HISTORY_ARCHIVE"
    if "runtime" in parts or "runs" in parts:
        return "NESTED_RUNTIME_LOGS"
    if "P0_TAKEOVER_20261024_01" in parts:
        return "NESTED_TAKEOVER_RESEARCH"
    if "normalized" in parts or "source_snapshot" in parts:
        return "NESTED_SOURCE_SNAPSHOT"
    if "recruit_sort_v4" in parts:
        return "NESTED_PLUGIN_WORKTREE"
    return "NESTED_MANUAL_REVIEW"

def corpus_inventory(root, indexed):
    groups = []
    reasons = Counter()
    total_files = total_bytes = 0
    text_files = indexed_text = 0
    for rel in FOLDERS:
        start = Path(root)/rel
        n = byte_count = text_count = idx = 0
        for base, dirs, names in os.walk(start, followlinks=False):
            dirs[:] = [d for d in dirs if d not in {".git", ".worktrees", "__pycache__"}]
            for name in names:
                p = Path(base)/name
                if p.is_symlink():
                    continue
                try:
                    size = p.stat().st_size
                except OSError:
                    continue
                n += 1
                byte_count += size
                if p.suffix.lower() in TEXT:
                    text_count += 1
                    relative = p.relative_to(root).as_posix()
                    if relative in indexed:
                        idx += 1
                        reasons["INDEXED"] += 1
                    elif p.suffix.lower() not in INDEX_EXT:
                        reasons["CODE_OR_UNSUPPORTED_EXTENSION"] += 1
                    elif size > INDEX_MAX:
                        reasons["LARGE_FILE_LIMIT"] += 1
                    elif rel != "tests" and p.parent != start:
                        reasons[nested_reason(p)] += 1
                    elif "_history_" in p.parts:
                        reasons["EXCLUDED_HISTORY"] += 1
                    else:
                        reasons["ELIGIBLE_BUT_NOT_INDEXED_REVIEW"] += 1
        groups.append((rel, n, text_count, idx, byte_count))
        total_files += n
        total_bytes += byte_count
        text_files += text_count
        indexed_text += idx
    return groups, total_files, total_bytes, text_files, indexed_text, reasons

def overview(data, rows, candidates):
    f = data["functions"]
    allowed = {int(r["va"], 16) for r in rows}
    studied = sum(bool(data["docinfo"].get(va, (0,))[0]) for va in allowed)
    registered = sum(va in data["named"] for va in allowed)
    unknowns = sum(data["unresolved"][va] > 0 for va in allowed)
    no_report = sum(r["research_docs"] == 0 and
                    r["verified_e8_callers"] > 0 and not r["registered"]
                    for r in rows)
    focused = sum(r["focused_docs"] > 0 for r in rows)
    runtime = sum(r["runtime_hint"] and not r["registered"] for r in rows)
    return dict(functions_all=data["counts"]["functions"],
                function_bodies=data["counts"]["function_body"],
                ghidra_refs=data["counts"]["ghidra_refs"],
                native_edges=data["counts"]["native_callsite"],
                verified_direct_e8_sites=data["verified_e8"],
                excluded_protected_native_sites=data["skipped_native_sites"],
                non_verified_or_branch_sites=data["branches"],
                unresolved_control_sites=data["counts"]["unresolved_control"],
                functions_internal=len(f), excluded_protected=len(f)-len(allowed),
                registered_function_entries=registered,
                functions_mentioned_in_reports=studied,
                functions_in_focused_reports=focused,
                internal_without_report=len(allowed)-studied,
                unregistered_runtime_hints_omitted_from_priority=runtime,
                unresolved_owner_functions=unknowns,
                unregistered_called_functions_without_report=no_report,
                unregistered_priority_candidates=len(candidates))

def emit(root, out, data, rows, candidates):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    summary = overview(data, rows, candidates)
    write_tsv(out/"GHIDRA_V9_GAPS_TOP500.tsv", COLUMNS, candidates[:500])
    unseen = [item for item in candidates if item["research_docs"]==0 and item["verified_e8_callers"]>0]
    targeted = [item for item in candidates if any(t in item["task_hint"].split(",") for t in ("T011","T012","T013","T024","T028"))]
    write_tsv(out/"GHIDRA_V9_UNSTUDIED_CALLED_TOP200.tsv", COLUMNS, unseen[:200])
    write_tsv(out/"GHIDRA_V9_B_REVIEW_TOP150.tsv", COLUMNS, targeted[:150])
    generated = Path(root)/"knowledge/generated/V9_FUNCTION_CROSSWALK.tsv"
    # Full function inventory remains local and ignored by GitHub.
    write_tsv(generated, tuple(COLUMNS[1:])+("registered","runtime_hint"), rows)
    corpus, total, total_size, text_total, indexed, reasons = corpus_inventory(
        root, data["indexed_paths"])
    report = ["# Ghidra V9 / research knowledge coverage",
              "",
              "STATIC INDEX ONLY: no executable was run; no original gameplay Golden test.",
              "Ghidra V9 and report index were opened read-only. Scores prioritize review,",
              "not confidence, verified semantics, safety or accepted READY.",
              "V9 SHA256 (local readback): " + data["v9_sha256"],
              "",
              "## Actual V9 function coverage", ""]
    labels = [
        ("All V9 function entries (including external)", "functions_all"),
        ("V9 function bodies", "function_bodies"),
        ("Ghidra references", "ghidra_refs"),
        ("Native call/JMP indexed sites", "native_edges"),
        ("Independently verified native E8 sites outside protected scope", "verified_direct_e8_sites"),
        ("Excluded native sites with protected owner/address", "excluded_protected_native_sites"),
        ("Other indexed native call/JMP sites", "non_verified_or_branch_sites"),
        ("Unresolved control-flow site records", "unresolved_control_sites"),
        ("V9 internal functions", "functions_internal"),
        ("Internal functions with protected-range overlap, excluded", "excluded_protected"),
        ("Entries with a curated symbols.tsv address", "registered_function_entries"),
        ("Function entries cited in indexed reports", "functions_mentioned_in_reports"),
        ("Function entries linked to focused source reports", "functions_in_focused_reports"),
        ("Internal entries without an indexed report", "internal_without_report"),
        ("Functions owning unresolved control-flow records", "unresolved_owner_functions"),
        ("Unregistered + called + not cited in reports", "unregistered_called_functions_without_report"),
        ("Unregistered runtime-helper hints excluded from priority queue", "unregistered_runtime_hints_omitted_from_priority"),
        ("Unregistered gap priority entries", "unregistered_priority_candidates")]
    report += [f"- {label}: **{summary[key]:,}**" for label,key in labels]
    report += ["", "## Corpus size and search-index gap", "",
               "The following counts are file metadata over selected PC research folders;",
               "the analysis does NOT hash or copy all binary Ghidra outputs.", "",
               "| Folder | Files | Text-like | Indexed text | Stored bytes |",
               "|---|---:|---:|---:|---:|"]
    report += [f"| {name} | {n:,} | {txt:,} | {ix:,} | {size:,} |"
               for name,n,txt,ix,size in corpus]
    report += ["", f"- Listed corpus files: {total:,}; total bytes: {total_size:,}.",
               f"- Text-like files: {text_total:,}; present in research index: {indexed:,}.",
               "- The research index can include additional root/knowledge documents beyond these folders.",
               "- Many Ghidra files are generated data, not individually useful findings.",
               "- Unindexed does not necessarily mean missing: source-code and large-file exclusions are intentional.",
               "- Nested files are classified without copying them; archive, original snapshot, runtime traces, and plugin work require independent review before any full-text inclusion.",
               "", "### Search-index scope audit", "",
               "| Reason | Files |", "|---|---:|"]
    report += [f"| {key} | {count:,} |" for key,count in sorted(reasons.items())]
    report += ["", "## Important unregistered V9 candidates (metadata only)", "",
               "| Function VA | Native verified callers | Native verified outgoing | Reports | Score |",
               "|---|---:|---:|---:|---:|"]
    report += [f"| {r['va']} | {r['verified_e8_callers']} | {r['verified_e8_callees']} | {r['research_docs']} | {r['score']} |"
               for r in candidates[:15]]
    report += ["", "## How to reuse", "",
               "Run on a PC with the original research root available:",
               "",
               "    python -B knowledge/tools/v9_coverage.py --root . --out knowledge --export",
               "    python -B knowledge/tools/v9_coverage.py --root . --inspect 0x00449500",
               "",
               "Use GHIDRA_V9_GAPS_TOP500.tsv for candidates, NOT for automatically",
               "renaming functions or claiming a behavior. The full per-function crosswalk",
               "is generated locally in knowledge/generated/V9_FUNCTION_CROSSWALK.tsv.",
               "Other review queues: GHIDRA_V9_UNSTUDIED_CALLED_TOP200.tsv and",
               "GHIDRA_V9_B_REVIEW_TOP150.tsv; these are investigation candidates, not B READY.",
               "Do not upload V9 source/SQLite, original game files or user local paths.",
               "The protected VA range and every function body overlapping it are excluded",
               "from candidate export; this is not permission to revisit refused actions.",
               "",
               "## Next verification steps", "",
               "- Cross-check the top candidate's exact native E8 sites and V9 pseudoc against owner HANDOFF.",
               "- Confirm that a function is a real, legally observable game path before changing status.",
               "- Resolve duplicate/contradictory reports and link corrected research IDs to the curated symbol.",
               "- Acquire original unmodified gameplay evidence for Golden PASS and strict MATCH; currently 0.",
               ""]
    (out/"GHIDRA_V9_COVERAGE_REPORT.md").write_text(
        "\n".join(report), encoding="utf-8", newline="\n")
    print("V9_COVERAGE_OK", json.dumps(summary, ensure_ascii=False))
    print("CORPUS_SCANNED", total, "INDEXED_TEXT", indexed, "TEXT_FILES", text_total)

def inspect(data, va):
    addr = number(va)
    if addr is None:
        print("INVALID_VA")
        return 1
    if PROTECTED[0] <= addr <= PROTECTED[1] or addr in data["denied"]:
        print("BLOCKED_PROTECTED_RANGE")
        return 2
    requested = addr
    c = ro(data["root"]/V9_REL)
    if addr not in data["functions"]:
        site = f"0x{addr:08X}"
        owned = c.execute("SELECT function_entry_va FROM function_range "
                          "WHERE start_va<=? AND end_va>=? LIMIT 1",(site,site)).fetchone()
        if owned:
            addr = number(owned[0])
    if addr in data["denied"]:
        c.close()
        print("BLOCKED_PROTECTED_RANGE")
        return 2
    f = data["functions"].get(addr)
    if not f:
        c.close()
        print("V9_FUNCTION_NOT_FOUND")
        return 1
    docs, hits, sample, focused = data["docinfo"].get(addr, (0, 0, "", 0))
    canonical = f"0x{addr:08X}"
    direct_callers = []
    for site,caller,opcode in c.execute(
            "SELECT site_va,caller_function_va,native_opcode_hex FROM native_callsite "
            "WHERE target_va=? AND opcode_kind='E8_DIRECT_CALL' "
            "AND independently_verified_target=1 LIMIT 60",(canonical,)):
        v = number(site)
        if v is not None and not PROTECTED[0] <= v <= PROTECTED[1] and number(caller) not in data["denied"]:
            direct_callers.append(dict(site_va=site,caller_function_va=caller,opcode=opcode))
        if len(direct_callers) >= 8: break
    direct_callees = []
    for site,target,opcode in c.execute(
            "SELECT site_va,target_va,native_opcode_hex FROM native_callsite "
            "WHERE caller_function_va=? AND opcode_kind='E8_DIRECT_CALL' "
            "AND independently_verified_target=1 LIMIT 60",(canonical,)):
        v = number(site)
        if v is not None and not PROTECTED[0] <= v <= PROTECTED[1] and number(target) not in data["denied"]:
            direct_callees.append(dict(site_va=site,target_va=target,opcode=opcode))
        if len(direct_callees) >= 8: break
    c.close()
    result = dict(query_va=f"0x{requested:08X}",va=canonical, ghidra_name=f["name"],
                  pseudoc_present=bool(f["pseudoc"]),
                  registered_in_symbols=addr in data["named"],
                  verified_native_e8_callers=data["incoming"][addr],
                  verified_native_e8_outgoing=data["outgoing"][addr],
                  ghidra_refs=data["ghidra"][addr],
                  unresolved_owned_sites=data["unresolved"][addr],
                  research_docs=docs, focused_docs=focused, mentions=hits, example_source=sample,
                  sample_verified_direct_callers=direct_callers,
                  sample_verified_direct_callees=direct_callees,
                  v9_sha256=data["v9_sha256"],
                  status="STATIC_METADATA/VERIFY/NOT_READY")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--root", type=Path, required=True)
    a.add_argument("--out", type=Path)
    a.add_argument("--export", action="store_true")
    a.add_argument("--inspect")
    a.add_argument("--symbols", type=Path, help="isolated KB symbols.tsv (default: research root)")
    args = a.parse_args(argv)
    if args.export == bool(args.inspect):
        a.error("Use exactly one of --export or --inspect")
    root = args.root.resolve()
    data = load(root, args.symbols)
    if args.inspect:
        return inspect(data, args.inspect)
    if not args.out:
        a.error("--export requires --out")
    rows,candidates = make_rows(data)
    emit(root,args.out, data,rows,candidates)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
