#!/usr/bin/env python3
"""Guarded Git synchronization of curated Hakushin research knowledge only.
Commands: audit, status, start TASK, checkpoint TASK, publish.
Never uses reset, rebase, stash, amend, force, or writes to original game files.
"""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

KB = Path(__file__).resolve().parent.parent
REPO = "ButaMonky/Hakushin067-Research-Knowledge"
MAIN = "develop"
MANIFEST = "SOURCE_MANIFEST.tsv"
FILES = (
    ".gitignore", ".gitattributes", "README.md", "kb.py",
    "symbols.tsv", "structs.tsv", "REF_DAT_BEHAVIOR.md", "REF_UI_SYSTEM.md",
    "SYNC_PROTOCOL.md", "SYNC_STATUS.md", "KB_SYNC_BLOCKED_20261029.md",
    "KNOWLEDGE_CURATION_PROTOCOL.md", "RESEARCH_INTAKE_PROTOCOL_20261101.md", "REF_UNIT_EXP_SUMMON.md", "REF_BATTLE_AI_MORALE.md", "REF_AUDIO_VORBIS.md", "REF_BATTLE_TAKEOVER.md",
    "REF_SAVE_PERSISTENCE.md", "REF_SAVE_FORMAT.md", "REF_RANDOM_EVENTS.md", "REF_RTS_SCENARIO.md",
    "REF_SCRIPT_VM_CONTEXT.md", "REF_SCENARIO_COMPAT.md", "REF_STRATEGY_ECONOMY.md",
    "RESEARCH_SOURCE_CATALOG.tsv", "RESEARCH_DUPLICATE_CANDIDATES.tsv", "RESEARCH_DUPLICATE_TRIAGE.md",
    "RESEARCH_INTEGRATION_SNAPSHOT.md",
    "GHIDRA_V9_COVERAGE_REPORT.md", "GHIDRA_V9_AUDIT_RUN_20261031.md",
    "GHIDRA_V9_GAPS_TOP500.tsv",
    "GHIDRA_V9_UNSTUDIED_CALLED_TOP200.tsv", "GHIDRA_V9_B_REVIEW_TOP150.tsv",
    "CANDIDATE_RANKING_20261030.md", "DB_OPTIMIZATION_REPORT_20261030.md",
    "GHIDRA_X32DBG_VERIFICATION_20261030.md",
    "KB_WORKFLOW_125_REPORT_20261029.md", "SYMBOLS_EXPANSION_REPORT_20261029.md",
    "tools/ApplyKnowledge.java", "tools/VerifyKnowledge.java", "tools/build_catalog.bat",
    "tools/build_catalog.py", "tools/build_kb.py", "tools/audit_research.py", "tools/test_research_inventory.py",
    "tools/v9_coverage.py", "tools/test_v9_coverage.py", "tools/check_symbols.py",
    "tools/research_index.py", "tools/optimize_research_db.py",
    "tools/rank_candidates.py", "tools/test_rank_candidates.py",
    "tools/verify_debugger_exports.py", "tools/test_debugger_exports.py",
    "tools/export_x32dbg_database.py", "tools/test_x32dbg_database.py",
    "tools/test_kb_workflow.py",
    "tools/sync_knowledge.py", "tools/test_sync_knowledge.py",
    "research/DAT_UI_V4_RESEARCH_20261101.md",
    "research/rea/INDEX.md",
    "research/rea/REA_20261101_17H_P0_FTELL_FRAME_STATIC.md",
    "research/rea/REA_20261101_19H_P0_FTELL_SEH4_SCOPE_STATIC.md",
    "research/rea/REA_20261101_20H_P0_EH4_DISPATCH_PHASE_STATIC.md",
    "research/intake/README.md",
    "research/intake/B/B-20261101-17H-T024-52AD00-MERGE-TIE-LOCAL-STABILITY-01.md",
    "research/intake/B/B-20261101-18H-T024-DUAL-REFERENCE-COORD-AND-PC-RESTORE-01.md",
    "research/intake/B/B-20261102-00H-T024-542280-NATIVE-ATAN2-SENTINEL-ERRATUM-01.md",
    "research/intake/B/B-20261102-01H-T024-5421D0-8DIST-SENTINEL-WRITER-01.md",
    "research/intake/B/B-OFFLINE-20261101-08H-T011-T013-GROUP1E-CALLSITES-AL-POSTCALL-01.md",
    "research/intake/B/B-OFFLINE-20261101-09H-T011-T013-GROUP34-WEIGHTED-SQRT-01.md",
    "research/intake/B/B-OFFLINE-20261101-16H-T011-T024-MIDPOINT-SAR-ROUNDING-OVERFLOW-01.md",
    "research/intake/REA/INDEX.md",
    "research/intake/REA/REA_20261031_22H_23H_20261101_00H_GROW_CALLBACKS.md",
    "research/intake/REA/REA_20261101_01H_02H_RESIDUE_TYPE2_AND_DIVISORS_STATIC.md",
    "research/intake/REA/REA_20261101_03H_05H_OFFLINE_RESIDUE_CORRECTED_STATIC.md",
    "research/intake/REA/REA_20261101_06H_08H_MODE_CACHE_RECOVERY_STATIC.md",
    "research/intake/REA/REA_20261101_21H_22H_FSOPEN_UNWIND_STATIC.md",
    "research/intake/REA/REA_20261101_23H_GETSTREAM_LOCK_OWNERSHIP_STATIC.md",
    "research/intake/REA/REA_20261102_00H_CRT_FILE2_LOCK_INDEX_POINTER_STATIC.md",
    "research/intake/REA/REA_20261102_01H_DUAL_ENTRY_ESI_ABI_STATIC.md",
    "research/intake/E/E-PC-20261101-GOLDEN-G012-AND-KB-BACKLOG.md",
    "research/intake/B/B-20261101-23H-T024-542280-OPTIONAL-DOUBLE-FALLBACK-01.md",
    "research/intake/B/B-OFFLINE-20261028-21H-T028-WANDER-MERCENARY-DUAL-RESULT-SINK-01.md",
    "research/intake/B/B-OFFLINE-20261028-22H-T028-ALTERNATE-RESULT-VECTOR-PAIR-01.md",
    "research/intake/B/B-OFFLINE-20261101-13H-T011-T024-DISTANCE-SORT-MODE-GATE-01.md",
    "research/intake/B/B-OFFLINE-20261101-14H-T011-T024-DISTANCE-COMPARE-BOUNDARY-01.md",
    "research/intake/B/B-OFFLINE-20261101-15H-T011-T024-NAN-COMPARATOR-TRANSITIVITY-01.md",
    "research/intake/B/B_T028_20261028_21H22H_BACKFILL_MANIFEST.tsv",
    "research/intake/B/T011_T024_DUAL_LIST_MODE3_VECTOR_NATIVE_20261101_12H.md",
    "research/intake/B/T011_T024_GROUP34_DUAL_BUCKET_ELIGIBILITY_NATIVE_20261101_11H.md",
    "research/intake/B/T011_T024_GROUP34_PROXIMITY_RATIO_100TICK_NATIVE_20261101_10H.md",
    "research/intake/B/T013_T024_528E86_GROUP1C_GATE_DISPATCH_NATIVE_20261101_20H.md",
    "research/intake/B/T013_T024_KB_CANDIDATE_528E86_GATE_20261101_20H.tsv",
    "research/intake/B/T013_T024_KB_CANDIDATE_MODE0_DISPATCH_GATES_20261101_21H.tsv",
    "research/intake/B/T013_T024_MODE0_DISPATCH_UPSTREAM_GATES_NATIVE_20261101_21H.md",
    "research/intake/B/T024_DUAL_CALLER_FACTOR_PROVENANCE_STATIC_20261101_22H.md",
    "research/intake/B/T024_GROUP_REF_FTOL_YFLIP_NATIVE_20261101_19H.md",
    "research/intake/B/T024_KB_CANDIDATE_REF_FTOL_YFLIP_20261101_19H.tsv",
    "research/intake/B/T024_KB_CURATION_SOURCE_MAP_20261101_19H.tsv",
    "research/intake/E/E-20261031-06H-TRAINING-COUNT-CROSSWALK.md",
    "research/intake/E/E-20261031-07H-LEADER-CACHE-CORRECTION.md",
    "research/intake/E/E-20261031-08H-CACHE-DUPLICATE-CLEANUP.md",
    "research/intake/E/E-20261101-00H-COORD-RECT-RAW-ONLY.md",
    "research/intake/E/E-20261101-01H-VIEWFLAG-WRITER-CONSUMER.md",
    "research/intake/E/E-20261101-02H-OFF-EXACT-VSLOT-NEGATIVES.md",
    "research/intake/E/E-20261101-2249-T020-INTAKE-MANIFEST.md",
    "research/intake/E/E-AUDIT-20261031-09H-T020-T011-BULK-ERASE-BOUNDARY-01.md",
    "research/intake/E/E-AUDIT-20261031-10H-T020-T011-PARTIAL-ERASE-GUARD-01.md",
    "research/intake/E/E-AUDIT-20261031-11H-T020-T011-SUCCESSOR-BEFORE-ERASE-01.md",
    "research/intake/E/E-AUDIT-20261031-12H-T020-T013-SIGNED-DUAL-FIELD-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-13H-T020-T013-FIXED-ANCHOR-CORRECTION-01.md",
    "research/intake/E/E-AUDIT-20261031-14H-T020-T013-POSTRANK-UNIT8-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-15H-T020-T013-KIND8-PREQUEUE-RNG-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-16H-T020-T013-BUCKET-MERGE-SIGNED-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-17H-T020-T013-DRAIN-RESTORE-CAP-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-18H-T020-T013-RNG-CONTEXT-NEGATIVE-INFERENCE-01.md",
    "research/intake/E/E-AUDIT-20261031-19H-T020-T013-A14-DRAW-BOUNDARY-01.md",
    "research/intake/E/E-AUDIT-20261031-20H-T020-T013-SCRIPT-LIST-COUNTER-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-21H-T020-T013-HEAD-SENTINEL-COORD-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-22H-T020-T013-ALT-LIST-RESET-ORDER-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-23H-T020-T013-RECT-INSET-WINAPI-01.md",
    "research/intake/E/E-INTAKE-MANIFEST-20261101-2352-T020-09H16H.md",
    "research/intake/E/E-INTAKE-MANIFEST-20261102-0049-T020-17H23H.md",
    "research/intake/E/E-LEGACY-20261028-29-SOURCE-CROSSWALK-PART1-20261102.md",
    "research/intake/E/E-OFFLINE-20261101-0351-T020-T013-SCAN-RECT-VCALL-GATE-01.md",
    "research/intake/E/E-OFFLINE-20261101-0453-T020-T013-THREE-CALLER-RETURN-USE-01.md",
    "research/intake/E/E-OFFLINE-20261101-0549-T020-DUAL-CALLER-LATCH.md",
    "research/intake/E/E-OFFLINE-20261101-0644-T020-T013-CROSS-SCOPE-INTEGRITY-01.md",
    "research/intake/E/E-OFFLINE-20261101-0745-T018-T020-POINTER-IDENTITY-NORMALIZATION-01.md",
    "research/intake/E/E-OFFLINE-20261101-08H-T018-T020-CALLER-TEMPORAL-IDENTITY-01.md",
    "research/intake/E/E-OFFLINE-20261101-09H-T018-T020-G2-BIJECTION-ORDER-01.md",
    "research/intake/E/E-OFFLINE-20261101-10H-G2-DEFINITION-RUNTIME.md",
    "research/intake/E/E-OFFLINE-20261101-11H-T018-T020-G012-ARTIFACT-ATOM-01.md",
    "research/intake/E/E-OFFLINE-20261101-12H-T018-T020-CROSS-RUN-ALIAS-ADMISSION-01.md",
    "research/intake/E/E-OFFLINE-20261101-13H-PARENT-SYMLINK-GATE.md",
    "research/intake/E/E-OFFLINE-20261101-14H-PINNED-HANDLE-PROVENANCE.md",
    "research/intake/E/E-OFFLINE-20261101-15H-SIX-GATE-COVERAGE.md",
    "research/intake/E/E-OFFLINE-20261101-16H-CNB02-SOURCE-ADMISSION.md",
    "research/intake/E/E-OFFLINE-20261101-INTAKE-BATCH-MANIFEST.md",
    "research/intake/REA/REA_20261101_09H_11H_CACHE_SEEK_RECOVERY_STATIC.md",
    "research/save_analysis_20261101/pkg/hakushin_compat/__init__.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/diplomacy_native_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/legacy_rng.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/native_stream_strings.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/normal_save_body_and_tail.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/normal_save_complete_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/power_native_full_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/power_runtime_writer_tail.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/real_save_frontmatter.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/save_envelope.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/spot_native_full_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/spot_runtime_writer_fragment.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/unit_native_full_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/unit_native_wire_prefix.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/unit_runtime_prefix.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/world_graph_native_wire.py",
    "research/save_analysis_20261101/tools/run_body_tail.py",
    "research/save_analysis_20261101/tools/tail_segments.py",
    "research/save_analysis_20261101/tools/tail_generations.py",
    "research/save_analysis_20261101/tools/tail_late_generations.py",
    "research/save_analysis_20261101/tools/field_stats.py",
    "research/save_analysis_20261101/tools/relation_checks.py",
    "research/save_analysis_20261101/tools/findings_vs_save.py",
    "research/save_analysis_20261101/tools/verify_ref.py",
    "research/save_analysis_20261101/tools/asmgrep.py",
    "research/save_analysis_20261101/tools/pseudo_grep.py",
    "research/save_analysis_20261101/tools/findings_offsets.py",
    "research/save_analysis_20261101/tools/kb_lookup.py",
    "research/save_analysis_20261101/tools/list_deps.py",
    "research/save_analysis_20261101/README.md",
    "sources/legacy_comments_20261011.tsv",
    "sources/legacy_symbols_20261011.tsv",
)
ALLOWED = set(FILES) | {MANIFEST}
RESTRICTED = (
    re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[A-Za-z0-9._-]+"),
    re.compile(r"(?i)\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"(?i)\b(?:github_pat_|gh[pousr]_)[A-Za-z0-9_-]{18,}\b"),
    re.compile(r"(?i)\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"-----BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY-----"),
)
TASK = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{2,48}\Z")

class Blocked(Exception):
    pass

def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def digest(data):
    return hashlib.sha256(data).hexdigest().upper()

def command(parts, check=True):
    try:
        p = subprocess.run(parts, cwd=KB, capture_output=True,
                           timeout=60, text=True, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Blocked(f"外部コマンド失敗: {parts[0]} / {type(e).__name__}")
    if p.returncode and check:
        # Don't echo raw process output; it can contain private credentials.
        raise Blocked(f"外部コマンド拒否: {parts[0]} {parts[1]} (exit={p.returncode})")
    return p.stdout.strip(), p.returncode

def git(*args, check=True):
    return command(("git", "-C", str(KB), *args), check=check)

def ensure_root():
    top, rc = git("rev-parse", "--show-toplevel", check=False)
    if rc or Path(top).resolve() != KB.resolve():
        raise Blocked("knowledge の独立Gitリポジトリでない")
    return True

def safe_files(root=KB, enforce_git=False):
    problems, hashes = [], {}
    ignore = root / ".gitignore"
    if not ignore.is_file():
        problems.append(".gitignore がない")
    else:
        content = ignore.read_text(encoding="utf-8")
        for mandatory in ("/*", "/tools/*", "/sources/*",
                          "/generated/", "!/symbols.tsv", "!/structs.tsv"):
            if mandatory not in content.splitlines():
                problems.append(".gitignore 必須規則欠落: "+mandatory)
    for relative in FILES:
        f = root / relative
        if not f.is_file() or f.is_symlink():
            problems.append("不足・リンク: "+relative)
            continue
        raw = f.read_bytes()
        hashes[relative] = (digest(raw), len(raw))
        if len(raw) > 2_000_000 or b"\x00" in raw:
            problems.append("サイズまたはバイナリ不適切: "+relative)
            continue
        try:
            s = raw.decode("utf-8-sig")
        except UnicodeError:
            if relative.endswith(".bat"):
                try:
                    s = raw.decode("cp932")
                except UnicodeError:
                    problems.append("解読不能: "+relative)
                    continue
            else:
                problems.append("UTF-8以外の原稿: "+relative)
                continue
        # The standard Git SSH transport identity is not a private email.
        sanitized = s.replace("git@github.com:", "git-ssh-remote:")
        if any(p.search(sanitized) for p in RESTRICTED):
            problems.append("機密の可能性あり（出典を確認）: "+relative)
    if enforce_git:
        ensure_root()
        tracked, _ = git("ls-files", "-z")
        for relative in tracked.split("\x00"):
            if relative and relative not in ALLOWED:
                problems.append("許可外のGit追跡対象: "+relative)
        staged, _ = git("diff", "--cached", "--name-only")
        for relative in staged.splitlines():
            if relative and relative not in ALLOWED:
                problems.append("許可外のステージ済みファイル: "+relative)
    return problems, hashes

def manifest(hashes):
    return ("# Generated locally by sync_knowledge.py\n"
            "path\tsha256\tbytes\n" +
            "".join(f"{k}\t{h}\t{size}\n"
                    for k,(h,size) in sorted(hashes.items())))

def write_manifest(hashes):
    path = KB / MANIFEST
    tmp = KB / (MANIFEST + ".tmp")
    if tmp.exists():
        raise Blocked("manifestの前回の一時ファイルがある")
    tmp.write_text(manifest(hashes), encoding="utf-8", newline="\n")
    os.replace(tmp, path)

def verify_staged_bytes(names):
    """Index objects must contain exactly the bytes recorded in the manifest."""
    for name in names:
        actual = git("hash-object", "--no-filters", "--", name)[0]
        indexed = git("rev-parse", ":" + name)[0]
        if actual != indexed:
            raise Blocked("Git indexと原本のバイトが一致しない: " + name)

def verify_manifest(hashes):
    f = KB / MANIFEST
    if not f.is_file():
        return False
    return f.read_text(encoding="utf-8") == manifest(hashes)

def branch():
    return git("branch", "--show-current")[0]

def clean():
    return not git("status", "--porcelain", "--untracked-files=all")[0]

def private_repo():
    ensure_root()
    url, _ = git("remote", "get-url", "origin")
    accepted = (f"https://github.com/{REPO}", f"https://github.com/{REPO}.git",
                f"git@github.com:{REPO}", f"git@github.com:{REPO}.git")
    if url not in accepted:
        raise Blocked("origin URLが指定の非公開研究リポジトリと一致しない")
    vis, _ = command(("gh","repo","view",REPO,"--json","visibility","--jq",".visibility"))
    if vis.upper() != "PRIVATE":
        raise Blocked("GitHub private 設定を確認できない")

def journal(action, status, task="", message=""):
    folder = KB / ".git"
    if not folder.is_dir():
        return
    item = dict(timestamp=stamp(), action=action, status=status,
                task=task, detail=message[:240])
    with open(folder / "kb-sync-journal.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False)+"\n")

@contextlib.contextmanager
def lock(action):
    path = KB / ".git/kb-sync.lock"
    if not path.parent.is_dir():
        raise Blocked("Git未初期化")
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    except FileExistsError:
        raise Blocked("他の操作がロック保持中。勝手に解除しない")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dict(action=action,time=stamp(),pid=os.getpid()), f)
        yield
    finally:
        path.unlink(missing_ok=True)

def audit_or_block(require_git=False):
    issues, hashes = safe_files(enforce_git=require_git)
    if issues:
        raise Blocked("; ".join(issues[:8]))
    return hashes

def start(task):
    audit_or_block(True)
    with lock("start"):
        if branch() != MAIN or not clean():
            raise Blocked("developがクリーンでない、または別ブランチ")
        private_repo()
        git("fetch", "origin", MAIN)
        if git("rev-parse","HEAD")[0] != git("rev-parse","origin/"+MAIN)[0]:
            raise Blocked("GitHubのdevelopが先行または分岐。ff-onlyの確認が必要")
        new = "work/kb-"+task
        git("switch","-c",new)
        base = dict(branch=new, base=git("rev-parse","HEAD")[0], created=stamp())
        (KB/".git/kb-sync-base.json").write_text(
            json.dumps(base,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        journal("start","LOCAL_ONLY",task,new)
        print("STARTED",new)

def checkpoint(task):
    before = audit_or_block(True)
    with lock("checkpoint"):
        b = branch()
        if b != "work/kb-"+task:
            raise Blocked("作業IDと作業ブランチが一致しない")
        basefile = KB/".git/kb-sync-base.json"
        if not basefile.is_file():
            raise Blocked("作業開始のベースSHA記録がない")
        base = json.loads(basefile.read_text(encoding="utf-8-sig"))
        if base.get("branch") != b:
            raise Blocked("開始時のブランチ情報不一致")
        if git("diff","--cached","--name-only")[0]:
            raise Blocked("他のステージ変更があるため中止")
        write_manifest(before)
        git("add","--",*FILES,MANIFEST)
        after = audit_or_block(True)
        verify_staged_bytes((*FILES, MANIFEST))
        if after != before or not verify_manifest(after):
            raise Blocked("競合: 書込み中に内容/SHAが変化。indexを確認するまで中断")
        staged = git("diff","--cached","--name-only")[0].splitlines()
        if not staged:
            print("NO_CHANGE")
            return
        git("commit","-m","knowledge checkpoint: "+task)
        sha=git("rev-parse","HEAD")[0]
        journal("checkpoint","LOCAL_ONLY",task,sha)
        print("LOCAL_CHECKPOINT",sha)

def publish():
    hashes=audit_or_block(True)
    with lock("publish"):
        b=branch()
        if not b.startswith("work/kb-") or not clean() or not verify_manifest(hashes):
            raise Blocked("作業ブランチではない/dirty/manifestが不一致")
        private_repo()
        basefile=KB/".git/kb-sync-base.json"
        if not basefile.is_file():
            raise Blocked("作業開始SHAがない")
        base=json.loads(basefile.read_text(encoding="utf-8-sig"))
        if base.get("branch")!=b:
            raise Blocked("作業ブランチと基準SHAが異なる")
        git("fetch","origin",MAIN)
        if git("rev-parse","origin/"+MAIN)[0]!=base.get("base"):
            raise Blocked("リモートdevelopが進んでいる。競合確認が必要")
        sha=git("rev-parse","HEAD")[0]
        git("push","origin","HEAD:refs/heads/"+b)
        remote=git("ls-remote","--heads","origin","refs/heads/"+b)[0]
        if not remote.startswith(sha+"\t"):
            raise Blocked("push後のリモートSHAが一致しない")
        journal("publish","SYNCED",b,sha)
        print("SYNCED",b,sha)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("action",choices=("audit","status","manifest","start","checkpoint","publish"))
    ap.add_argument("task",nargs="?")
    args=ap.parse_args()
    try:
        if args.action=="audit":
            audit_or_block((KB/".git").exists())
            print("AUDIT_PASS",len(FILES))
        elif args.action=="manifest":
            before=audit_or_block((KB/".git").exists())
            if (KB/".git").exists() and branch() != MAIN and not branch().startswith("work/kb-"):
                raise Blocked("manifest生成は許可されたGitブランチでのみ可能")
            write_manifest(before)
            after=audit_or_block((KB/".git").exists())
            if before != after or not verify_manifest(after):
                raise Blocked("manifest保存中に原本が変化")
            print("MANIFEST_WRITTEN",len(after))
        elif args.action=="status":
            problems,fs=safe_files(enforce_git=(KB/".git").exists())
            print("SOURCE_COUNT",len(fs),"ISSUES",len(problems))
            for problem in problems: print("ISSUE",problem)
            if (KB/".git").exists():
                print("BRANCH",branch(),"CLEAN",clean())
                print("MANIFEST_OK",verify_manifest(fs))
        else:
            if args.action in ("start","checkpoint"):
                if not args.task or not TASK.fullmatch(args.task):
                    raise Blocked("作業IDを英数字・ハイフンで指定")
                (start if args.action=="start" else checkpoint)(args.task)
            else:
                publish()
        return 0
    except Blocked as err:
        print("BLOCKED",str(err))
        journal(args.action,"BLOCKED",args.task or "",str(err))
        return 2

if __name__=="__main__":
    sys.exit(main())

