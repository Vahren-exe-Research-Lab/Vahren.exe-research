#!/usr/bin/env python3
"""Incremental, read-only-source research full-text/address index for Hakushin 0.67.
Only knowledge/generated/research.sqlite and candidate exports are modified.
Usage: python -B knowledge/tools/research_index.py [--check|--rebuild]
"""
import argparse
import bisect
import hashlib
import re
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
ROOT = KB.parent
DB = KB / "generated/research.sqlite"
V9 = ROOT / "rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite"
SYMBOLS = KB / "symbols.tsv"
CANDIDATES = KB / "generated/address_candidates.tsv"
RECENT_CANDIDATES = KB / "generated/address_candidates_recent.tsv"
FOLDERS = (
    ("data", False), ("exe", False), ("evidence", False), ("wiki", False),
    ("exp_research_20261021", False), ("dev_lab/docs", False),
    ("rea_lab/headless_analysis/search_index", False), ("tests", True),
)
EXTS = {".md", ".txt", ".json", ".jsonl", ".tsv", ".csv"}
MAX_SIZE = 3_000_000
RE_VA = re.compile(r"(?<![A-Za-z0-9_])0[xX]([0-9A-Fa-f]{6,8})(?![0-9A-Fa-f])")
RE_HEADER = re.compile(r"^\s{0,3}#{1,5}\s+(.+)")
PROTECTED = (0x5710C0, 0x571500)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def paths():
    """Allowlisted existing research reports; never walk game DAT, archives or generated."""
    for directory, recursive in FOLDERS:
        base = ROOT / directory
        if not base.is_dir():
            continue
        it = base.rglob("*") if recursive else base.iterdir()
        for p in it:
            if (p.is_symlink() or not p.is_file() or p.suffix.lower() not in EXTS
                    or "_history_" in p.parts or "__pycache__" in p.parts):
                continue
            if p.stat().st_size <= MAX_SIZE:
                yield p
    for p in [ROOT / "MASTER_LEDGER.md", *KB.glob("*.md")]:
        if p.is_file() and not p.is_symlink() and p.name not in {
            "REF_ADDRESSES.md", "REF_STRUCTS.md", "CATALOG.md",
        } and p.stat().st_size <= MAX_SIZE:
            yield p

def load_ranges(path=V9):
    if not path.exists():
        return [], []
    c = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    rr = sorted((int(a, 16), int(b, 16), int(f, 16)) for a, b, f
                in c.execute("SELECT start_va,end_va,function_entry_va FROM function_range"))
    c.close()
    return rr, [x[0] for x in rr]

def normalize_va(va, ranges, starts):
    if not (0x401000 <= va <= 0x8FFFFF):
        return None
    if va >= 0x639000:
        return (va, None, "data")
    i = bisect.bisect_right(starts, va) - 1
    if i >= 0 and ranges[i][0] <= va <= ranges[i][1]:
        owner = ranges[i][2]
        return (owner, owner, "func")
    return (va, None, "unresolved")

def extract(text, ranges, starts):
    """Keep precise VA and normalized function owner; no native execution/decompilation."""
    heading = "(冒頭)"
    lines, refs = [], []
    for line_no, line in enumerate(text.splitlines(), 1):
        m = RE_HEADER.match(line)
        if m:
            heading = m.group(1).strip()[:120]
        lines.append((line_no, heading, line))
        for va in {int(m.group(1), 16) for m in RE_VA.finditer(line)}:
            result = normalize_va(va, ranges, starts)
            if result:
                normalized, owner, kind = result
                refs.append((line_no, va, normalized, owner, kind))
    return lines, refs

def decode(raw):
    if b"\x00" in raw[:200] and not raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return None
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16")
    for enc in ("utf-8-sig", "cp932"):
        try:
            return raw.decode(enc)
        except UnicodeError:
            pass
    return None

def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB, timeout=30)
    c.execute("PRAGMA busy_timeout=30000")
    c.execute("PRAGMA foreign_keys=ON")
    c.executescript("""
        CREATE TABLE IF NOT EXISTS docs(
            path TEXT PRIMARY KEY, sha256 TEXT NOT NULL,
            bytes INTEGER NOT NULL, mtime_ns INTEGER NOT NULL,
            lines INTEGER NOT NULL, mentions INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS doc_lines(
            id INTEGER PRIMARY KEY, path TEXT NOT NULL,
            line_no INTEGER NOT NULL, heading TEXT, text TEXT NOT NULL,
            UNIQUE(path, line_no));
        CREATE INDEX IF NOT EXISTS idx_doc_lines_path ON doc_lines(path,line_no);
        CREATE TABLE IF NOT EXISTS mentions(
            line_id INTEGER NOT NULL, path TEXT NOT NULL, line_no INTEGER NOT NULL,
            va INTEGER NOT NULL, normalized_va INTEGER NOT NULL,
            owner_va INTEGER, kind TEXT NOT NULL,
            UNIQUE(line_id, va));
        CREATE INDEX IF NOT EXISTS idx_mentions_va ON mentions(va);
        CREATE INDEX IF NOT EXISTS idx_mentions_normalized ON mentions(normalized_va);
        CREATE INDEX IF NOT EXISTS idx_mentions_owner ON mentions(owner_va);
        CREATE INDEX IF NOT EXISTS idx_mentions_path ON mentions(path);
    """)
    try:
        c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS doc_fts USING fts5(text, tokenize='trigram')")
        has_fts = True
    except sqlite3.OperationalError:
        has_fts = False
    return c, has_fts

def forget(c, path, fts):
    if fts:
        c.execute("""DELETE FROM doc_fts WHERE rowid IN
                     (SELECT id FROM doc_lines WHERE path=?)""", (path,))
    c.execute("DELETE FROM mentions WHERE path=?", (path,))
    c.execute("DELETE FROM doc_lines WHERE path=?", (path,))
    c.execute("DELETE FROM docs WHERE path=?", (path,))

def index_file(c, p, raw, ranges, starts, fts):
    rel = p.relative_to(ROOT).as_posix()
    content = decode(raw)
    if content is None:
        return False
    lines, refs = extract(content, ranges, starts)
    forget(c, rel, fts)
    st = p.stat()
    c.execute("INSERT INTO docs VALUES(?,?,?,?,?,?)",
              (rel, digest(raw), len(raw), st.st_mtime_ns, len(lines), len(refs)))
    c.executemany("INSERT INTO doc_lines(path,line_no,heading,text) VALUES(?,?,?,?)",
                  ((rel, n, h, t) for n, h, t in lines))
    ids = dict(c.execute("SELECT line_no,id FROM doc_lines WHERE path=?", (rel,)))
    c.executemany("""INSERT INTO mentions
                     (line_id,path,line_no,va,normalized_va,owner_va,kind)
                     VALUES(?,?,?,?,?,?,?)""",
                  ((ids[n], rel, n, va, norm, owner, kind)
                   for n, va, norm, owner, kind in refs))
    if fts:
        c.executemany("INSERT INTO doc_fts(rowid,text) VALUES(?,?)",
                      ((ids[n], t) for n, h, t in lines))
    return True

def curated():
    result = set()
    for line in SYMBOLS.read_text(encoding="utf-8").splitlines():
        if line.startswith("0x"):
            result.add(int(line.split("\t", 1)[0], 16))
    return result

def make_candidates(c, limit=2500):
    known = curated()
    rows = c.execute("""SELECT normalized_va,kind,COUNT(*) hits,
                         COUNT(DISTINCT path) reports,MAX(d.mtime_ns) recent
                         FROM mentions m JOIN docs d USING(path)
                         GROUP BY normalized_va
                         ORDER BY reports DESC,hits DESC,recent DESC""").fetchall()
    result = []
    for va, kind, hits, reports, recent in rows:
        if va in known or PROTECTED[0] <= va <= PROTECTED[1]:
            continue
        origin = c.execute("""SELECT m.path,m.line_no,m.va,l.heading
                              FROM mentions m JOIN doc_lines l ON l.id=m.line_id
                              WHERE m.normalized_va=?
                              ORDER BY (CASE WHEN m.va=m.normalized_va THEN 0 ELSE 1 END),
                                       m.path,m.line_no LIMIT 1""", (va,)).fetchone()
        if origin is None:
            continue
        path, line_no, original, heading = origin
        result.append((f"0x{va:06X}", kind, hits, reports, path,
                       line_no, f"0x{original:06X}", heading.replace("\t", " ")))
        if len(result) >= limit:
            break
    temp = CANDIDATES.with_suffix(".tsv.tmp")
    with open(temp, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 自動候補・未検証。辞書への自動登録や確度の引上げは禁止。\n")
        f.write("va\tkind_candidate\tmentions\treports\texample_path\tline\tmentioned_va\theading\n")
        for row in result:
            f.write("\t".join(map(str, row)) + "\n")
    temp.replace(CANDIDATES)
    return len(result), len(rows)

def make_recent_candidates(c, changed_paths):
    """All new/edited-report addresses, including rare one-hit discoveries."""
    known = curated()
    output = []
    if changed_paths:
        # A temporary table avoids SQLite IN-variable limits with thousands of changed files.
        c.execute("CREATE TEMP TABLE IF NOT EXISTS changed_sources(path TEXT PRIMARY KEY)")
        c.execute("DELETE FROM changed_sources")
        c.executemany("INSERT INTO changed_sources(path) VALUES(?)",
                      ((p,) for p in sorted(set(changed_paths))))
        for va, kind, hits, docs in c.execute("""
            SELECT m.normalized_va,m.kind,COUNT(*) AS hits,COUNT(DISTINCT m.path) AS docs
            FROM mentions m JOIN changed_sources s ON s.path=m.path
            GROUP BY m.normalized_va ORDER BY docs DESC,hits DESC,m.normalized_va
        """):
            if va in known or PROTECTED[0] <= va <= PROTECTED[1]:
                continue
            sample = c.execute("""
                SELECT m.path,m.line_no,m.va,l.heading
                FROM mentions m JOIN changed_sources s ON s.path=m.path
                JOIN doc_lines l ON l.id=m.line_id
                WHERE m.normalized_va=? ORDER BY m.path,m.line_no LIMIT 1
            """, (va,)).fetchone()
            if sample:
                path, number, original, heading = sample
                output.append((f"0x{va:06X}",kind,hits,docs,path,number,
                               f"0x{original:06X}",heading.replace("\t"," ")))
    tmp = RECENT_CANDIDATES.with_suffix(".tsv.tmp")
    with open(tmp,"w",encoding="utf-8",newline="\n") as f:
        f.write("# 直近の更新・新規資料由来の未検証候補。辞書には自動登録しない。\n")
        f.write("va\tkind_candidate\tmentions\treports\texample_path\tline\tmentioned_va\theading\n")
        for fields in output:
            f.write("\t".join(map(str,fields))+"\n")
    tmp.replace(RECENT_CANDIDATES)
    return len(output)


def main(argv=None):
    a = argparse.ArgumentParser(description="研究全文・アドレス参照の増分索引")
    a.add_argument("--check", action="store_true", help="読取専用の更新予定確認")
    a.add_argument("--rebuild", action="store_true", help="対象文書を全件再索引")
    args = a.parse_args(argv)
    selected = {p.relative_to(ROOT).as_posix(): p for p in paths()}
    if args.check:
        if not DB.exists():
            print("未作成: research.sqlite")
            return 1
        c = sqlite3.connect(DB.resolve().as_uri() + "?mode=ro", uri=True)
        known = dict(c.execute("SELECT path,sha256 FROM docs"))
        pending = sum(digest(p.read_bytes()) != known.get(rel) for rel,p in selected.items())
        missing = len(set(known) - set(selected))
        print(f"索引確認: {len(known)}件、変更待ち {pending}件、削除待ち {missing}件")
        c.close()
        return 0 if pending == 0 and missing == 0 else 1
    ranges, starts = load_ranges(V9)
    c, fts = connect()
    old = dict(c.execute("SELECT path,sha256 FROM docs"))
    changed = removed = skipped = 0
    changed_paths = []
    try:
        c.execute("BEGIN IMMEDIATE")
        for rel in sorted(set(old) - set(selected)):
            forget(c, rel, fts)
            removed += 1
        for rel, p in sorted(selected.items()):
            raw = p.read_bytes()
            if not args.rebuild and digest(raw) == old.get(rel):
                skipped += 1
                continue
            if index_file(c, p, raw, ranges, starts, fts):
                changed += 1
                changed_paths.append(rel)
        c.commit()
    except Exception:
        c.rollback()
        raise
    try:
        counts = c.execute("SELECT COUNT(*),COALESCE(SUM(lines),0),COALESCE(SUM(mentions),0) FROM docs").fetchone()
        n, total = make_candidates(c)
        recent = make_recent_candidates(c, changed_paths) if (changed or removed) else None
    finally:
        c.close()
    print(f"研究索引: {counts[0]}資料、{counts[1]}行、{counts[2]}VA言及 "
          f"（更新{changed}/未変更{skipped}/削除{removed}、FTS5={'有' if fts else '無'}）")
    print(f"追加候補: {n}行出力（未登録正規化VAの総数は{total}以下）、{CANDIDATES}")
    if recent is not None:
        print(f"今回変更された資料由来の候補: {recent}件 → {RECENT_CANDIDATES}")
    elif RECENT_CANDIDATES.exists():
        print("更新資料なし。直近候補一覧は前回の出力を保持")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

