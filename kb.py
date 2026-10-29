#!/usr/bin/env python3
"""迫真戦記 ver0.67 研究知識ベースの検索（Claude 2026-10-29）

関数の疑似コード（Ghidra 統合 V9）に、研究で分かった名前と説明を重ねて表示する。

  python -B knowledge\\kb.py addr 0x55D8F6        # そのアドレスの名前・所属する関数・資料での言及
  python -B knowledge\\kb.py func StatusWnd_Layout # 疑似コード（名前を置き換えて表示）
  python -B knowledge\\kb.py callers 0x584970      # 呼び出し元（直接 CALL のみ）
  python -B knowledge\\kb.py find 解雇              # 名前・説明・構造体から検索
  python -B knowledge\\kb.py struct UnitDef        # 構造体のオフセット
  python -B knowledge\\kb.py docs 0x583CF0         # 資料での言及をすべて
  python -B knowledge\\kb.py files 教育            # 研究資料ファイルの目録から検索（--task T026、--folder exe）

アドレスは 0x 付きの VA（0x400000 基準）。x32dbg の Vahren.exe+15D8F6 のような形も受け付ける。
"""
import argparse, re, sqlite3, sys
from pathlib import Path

KB = Path(__file__).resolve().parent
ROOT = KB.parent
DB = KB / "generated" / "kb.sqlite"
V9 = ROOT / "rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite"
RESEARCH_DB = KB / "generated/research.sqlite"
PENDING_TSV = KB / "generated/address_candidates.tsv"
PENDING_RECENT = KB / "generated/address_candidates_recent.tsv"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def ro(p):
    if not Path(p).exists():
        sys.exit(f"見つかりません: {p}")
    c = sqlite3.connect(Path(p).resolve().as_uri() + "?mode=ro&immutable=1", uri=True)
    c.row_factory = sqlite3.Row
    return c


kb = ro(DB)
v9 = ro(V9) if V9.exists() else None


def parse_addr(s):
    s = s.strip()
    m = re.fullmatch(r"(?i)vahren\.exe\+(?:0x)?([0-9a-f]+)", s)
    if m:
        return 0x400000 + int(m.group(1), 16)
    m = re.fullmatch(r"(?i)(?:0x)?([0-9a-f]{5,8})", s)
    if m:
        return int(m.group(1), 16)
    r = kb.execute("SELECT va FROM symbols WHERE name=?", (s,)).fetchone()
    if r:
        return r["va"]
    r = kb.execute("SELECT va,name FROM symbols WHERE name LIKE ? ORDER BY length(name) LIMIT 5", (f"%{s}%",)).fetchall()
    if len(r) == 1:
        return r[0]["va"]
    if r:
        sys.exit("候補が複数あります: " + ", ".join(f"{x['name']}(0x{x['va']:06X})" for x in r))
    sys.exit(f"アドレスか名前として解釈できません: {s}")


def sym(va):
    return kb.execute("SELECT * FROM symbols WHERE va=?", (va,)).fetchone()


def owner(va):
    if not v9:
        return None
    r = v9.execute("SELECT function_entry_va FROM function_range WHERE start_va<=? AND end_va>=? LIMIT 1",
                   (f"0x{va:08X}", f"0x{va:08X}")).fetchone()
    return int(r[0], 16) if r else None


def label(va):
    s = sym(va)
    return f"{s['name']}" if s else f"0x{va:06X}"


def show_sym(va, indent=""):
    s = sym(va)
    if not s:
        print(f"{indent}0x{va:06X}: （名前なし）")
        return
    print(f"{indent}0x{va:06X}  {s['name']}  [{s['kind']} / {s['confidence']} / {s['origin']}]")
    if s["summary"]:
        print(f"{indent}  {s['summary']}")
    if s["source"]:
        print(f"{indent}  出典: {s['source']}")


def mentions(va, fn=None, limit=12):
    rows = kb.execute("SELECT doc,line,heading,va FROM mentions WHERE va=? OR (function_va=? AND ?) ORDER BY doc,line",
                      (va, fn if fn is not None else -1, 1 if fn is not None else 0)).fetchall()
    seen = set()
    out = []
    for r in rows:
        k = (r["doc"], r["heading"])
        if k in seen:
            continue
        seen.add(k)
        out.append(f"{r['doc']}:{r['line']}  {r['heading']}" + ("" if r["va"] == va else f"  （0x{r['va']:06X}）"))
    for x in out[:limit]:
        print("    " + x)
    if len(out) > limit:
        print(f"    ほか {len(out) - limit} 件（docs コマンドで全部）")
    if not out:
        print("    （なし）")


def research_conn():
    if not RESEARCH_DB.exists():
        return None
    c = sqlite3.connect(RESEARCH_DB.resolve().as_uri() + "?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    return c


def research_refs(va, limit=12):
    """Independently indexed report lines, with exact path/line and V9 owner."""
    c = research_conn()
    if c is None:
        print("    （研究索引なし: python -B knowledge/tools/research_index.py）")
        return
    fn = owner(va) or va
    rows = c.execute("""
        SELECT m.path,m.line_no,m.va,l.heading,l.text
        FROM mentions m JOIN doc_lines l ON l.id=m.line_id
        JOIN docs d ON d.path=m.path
        WHERE m.va=? OR m.normalized_va=?
        ORDER BY CASE WHEN m.va=? THEN 0 ELSE 1 END,
                 d.mtime_ns DESC, m.path, m.line_no LIMIT ?
    """, (va, fn, va, max(1, limit + 1))).fetchall()
    for r in rows[:limit]:
        snippet = " ".join(r["text"].strip().split())[:165]
        print(f"    {r['path']}:{r['line_no']}  [{r['heading']}]  {snippet}")
    if len(rows) > limit:
        print(f"    ほかにも参照あり。docs コマンドは --limit 指定で拡張可能")
    if not rows:
        print("    （なし）")
    c.close()


def cmd_research(a):
    c = research_conn()
    if c is None:
        sys.exit("全文索引なし: python -B knowledge/tools/research_index.py")
    query = a.text.strip()
    if not query:
        sys.exit("検索語が空です")
    filters, args = [], []
    fts = c.execute("SELECT 1 FROM sqlite_master WHERE name='doc_fts'").fetchone()
    if len(query) >= 3 and fts:
        sql = """SELECT l.path,l.line_no,l.heading,l.text
                 FROM doc_fts JOIN doc_lines l ON l.id=doc_fts.rowid
                 WHERE doc_fts MATCH ?"""
        args.append('"' + query.replace('"', '""') + '"')
    else:
        sql = """SELECT l.path,l.line_no,l.heading,l.text FROM doc_lines l
                 WHERE instr(lower(l.text),lower(?)) > 0"""
        args.append(query)
    if a.folder:
        filters.append("l.path LIKE ?")
        args.append(a.folder.strip("/") + "/%")
    if a.task:
        if not re.fullmatch(r"T0\d\d", a.task.upper()):
            sys.exit("taskは T012 のような形式")
        filters.append("l.path LIKE ?")
        args.append("%" + a.task.upper() + "%")
    if filters:
        sql += " AND " + " AND ".join(filters)
    sql += " ORDER BY l.path,l.line_no LIMIT ?"
    args.append(min(max(a.limit, 1), 500) + 1)
    try:
        rows = c.execute(sql, args).fetchall()
    except sqlite3.OperationalError as e:
        sys.exit(f"全文検索に失敗: {e}")
    for r in rows[:a.limit]:
        print(f"{r['path']}:{r['line_no']}  {r['heading']}")
        print("  " + " ".join(r["text"].strip().split())[:230])
    print(f"（{min(len(rows),a.limit)}件表示" +
          ("、続きあり）" if len(rows)>a.limit else "）"))
    c.close()


def cmd_pending(a):
    file = PENDING_RECENT if a.recent else PENDING_TSV
    if not file.exists():
        sys.exit("候補がありません: python -B knowledge/tools/research_index.py")
    count = 0
    for line in file.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line.startswith("va\t"):
            continue
        cells = line.split("\t")
        if len(cells) != 8 or (a.kind and cells[1] != a.kind):
            continue
        print(f"{cells[0]}  [{cells[1]}]  言及{cells[2]}件/{cells[3]}資料 "
              f"{cells[4]}:{cells[5]}  （原文{cells[6]}）")
        count += 1
        if count >= a.limit:
            break
    print(f"（未検証の登録候補 {count}件を表示。symbols.tsvには自動追加しません）")


def cmd_addr(a):
    va = parse_addr(a.target)
    print(f"x32dbg: Vahren.exe+{va - 0x400000:X}")
    show_sym(va)
    fn = owner(va)
    if fn is not None and fn != va:
        print("所属する関数:")
        show_sym(fn, "  ")
    print("資料での言及:")
    mentions(va, fn if fn == va else None)
    print("研究全文索引の関連箇所:")
    research_refs(va, limit=10)


def cmd_docs(a):
    va = parse_addr(a.target)
    mentions(va, va, limit=min(a.limit, 100))
    print("研究全文索引の関連箇所:")
    research_refs(va, limit=min(a.limit, 200))


def cmd_find(a):
    q = f"%{a.text}%"
    rows = kb.execute("SELECT va,name,kind,confidence,summary FROM symbols WHERE name LIKE ? OR summary LIKE ? ORDER BY origin='curated' DESC, va LIMIT ?",
                      (q, q, a.limit)).fetchall()
    for r in rows:
        print(f"0x{r['va']:06X}  {r['name']}  [{r['kind']} / {r['confidence']}]  {r['summary']}")
    st = kb.execute("SELECT * FROM structs WHERE name LIKE ? OR summary LIKE ? OR struct LIKE ?", (q, q, q)).fetchall()
    for r in st:
        print(f"{r['struct']}+0x{r['offset']:X}  {r['name']} ({r['type']}) [{r['confidence']}]  {r['summary']}")
    if not rows and not st:
        print("（見つかりません）")


def cmd_struct(a):
    if not a.name:
        for r in kb.execute("SELECT struct,count(*) n FROM structs GROUP BY struct"):
            print(f"{r['struct']}  {r['n']} 項目")
        return
    for r in kb.execute("SELECT * FROM structs WHERE struct=? ORDER BY offset", (a.name,)):
        print(f"+0x{r['offset']:X}\t{r['type']}\t{r['name']}\t[{r['confidence']}]\t{r['summary']}")


def cmd_callers(a):
    if not v9:
        sys.exit("V9 が見つかりません")
    va = parse_addr(a.target)
    rows = v9.execute("SELECT site_va,caller_function_va,opcode_kind FROM native_callsite WHERE target_va=? ORDER BY site_va",
                      (f"0x{va:08X}",)).fetchall()
    print(f"{label(va)} の呼び出し元 {len(rows)} 件（E8=CALL、E9/EB=JMP）")
    for r in rows[:a.limit]:
        cf = int(r["caller_function_va"], 16) if r["caller_function_va"] else None
        print(f"  {r['site_va']}  {r['opcode_kind']:<12} {label(cf) if cf else '?'}")


def cmd_func(a):
    if not v9:
        sys.exit("V9 が見つかりません")
    va = parse_addr(a.target)
    fn = owner(va) or va
    r = v9.execute("SELECT name,size_bytes,pseudoc,pseudoc_origin FROM functions WHERE entry_va=?", (f"0x{fn:08X}",)).fetchone()
    if not r:
        sys.exit(f"関数が見つかりません: 0x{fn:06X}")
    show_sym(fn)
    print(f"  V9: {r['name']}  {r['size_bytes']} バイト  ({r['pseudoc_origin']})")
    print("資料での言及:")
    mentions(fn, fn, limit=8)
    code = r["pseudoc"] or ""
    names = {x["va"]: x["name"] for x in kb.execute("SELECT va,name FROM symbols")}

    def rep(m):
        v = int(m.group(2), 16)
        n = names.get(v)
        return n if n else m.group(0)
    code = re.sub(r"\b(FUN|DAT|LAB|PTR_FUN|PTR_DAT)_([0-9a-fA-F]{8})\b", rep, code)
    if a.max_chars and len(code) > a.max_chars:
        code = code[:a.max_chars] + f"\n... （{len(code) - a.max_chars} 文字省略。--max-chars 0 で全部）"
    print(code)


def cmd_files(a):
    if not kb.execute("SELECT 1 FROM sqlite_master WHERE name='files'").fetchone():
        sys.exit("目録がありません。python -B knowledge\\tools\\build_catalog.py を実行してください")
    w, args = [], []
    if a.text:
        w.append("(path LIKE ? OR summary LIKE ?)"); args += [f"%{a.text}%"] * 2
    if a.task:
        w.append("(',' || tasks || ',') LIKE ?"); args.append(f"%,{a.task.upper()},%")
    if a.folder:
        w.append("folder LIKE ?"); args.append(f"%{a.folder}%")
    if a.kind:
        w.append("kind=?"); args.append(a.kind)
    sql = "SELECT * FROM files" + (" WHERE " + " AND ".join(w) if w else "") + " ORDER BY date DESC, path LIMIT ?"
    rows = kb.execute(sql, args + [a.limit]).fetchall()
    for r in rows:
        print(f"{r['date']}  {r['path']}  [{r['kind']}{' ' + r['tasks'] if r['tasks'] else ''}]  {r['summary']}")
        if r["pair"]:
            print(f"            対: {r['pair']}")
    print(f"（{len(rows)} 件{'、上限 ' + str(a.limit) if len(rows) == a.limit else ''}）")


def main():
    ap = argparse.ArgumentParser(description="迫真戦記 研究知識ベースの検索")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("addr"); p.add_argument("target"); p.set_defaults(f=cmd_addr)
    p = sp.add_parser("docs"); p.add_argument("target"); p.add_argument("--limit", type=int, default=50); p.set_defaults(f=cmd_docs)
    p = sp.add_parser("find"); p.add_argument("text"); p.add_argument("--limit", type=int, default=40); p.set_defaults(f=cmd_find)
    p = sp.add_parser("struct"); p.add_argument("name", nargs="?"); p.set_defaults(f=cmd_struct)
    p = sp.add_parser("callers"); p.add_argument("target"); p.add_argument("--limit", type=int, default=60); p.set_defaults(f=cmd_callers)
    p = sp.add_parser("func"); p.add_argument("target"); p.add_argument("--max-chars", type=int, default=6000); p.set_defaults(f=cmd_func)
    p = sp.add_parser("files"); p.add_argument("text", nargs="?"); p.add_argument("--task"); p.add_argument("--folder"); p.add_argument("--kind", help="報告 / データ / スクリプト / その他"); p.add_argument("--limit", type=int, default=50); p.set_defaults(f=cmd_files)
    p = sp.add_parser("research", help="研究報告の全文を行番号つきで検索")
    p.add_argument("text"); p.add_argument("--task"); p.add_argument("--folder")
    p.add_argument("--limit", type=int, default=25); p.set_defaults(f=cmd_research)
    p = sp.add_parser("pending", help="出典付きの未登録VA候補を表示（自動編集しない）")
    p.add_argument("--kind"); p.add_argument("--limit", type=int, default=30)
    p.add_argument("--recent", action="store_true", help="直近に更新された資料だけの候補")
    p.set_defaults(f=cmd_pending)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
