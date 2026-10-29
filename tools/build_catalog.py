#!/usr/bin/env python3
"""研究資料フォルダの目録を作る（Claude 2026-10-29）

evidence / wiki / exp_research / exe / tests / data / dev_lab\\docs などの各ファイルについて、
「何のファイルか」（見出し・ID・状態・列名・説明文）を中身から 1 行で取り出し、
作業番号（T005〜T034）ごとにまとめる。

  python -B knowledge\\tools\\build_catalog.py      # 単独で実行（build_kb.py からも呼ばれる）

出力:
  knowledge\\CATALOG.md                 作業番号ごとの目録（報告書は見出しつき、スクリプト等は件数）
  knowledge\\generated\\catalog.tsv      全ファイルの一覧（パス、種類、作業番号、担当、日付、大きさ、1 行説明、対になるファイル）
  knowledge\\generated\\kb.sqlite の files 表（kb.py files で検索）
"""
import collections, datetime, json, re, sqlite3, sys
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
ROOT = KB.parent

# (フォルダ, 説明, 再帰するか)
FOLDERS = [
    ("evidence", "初期（10-06〜10-16）の作業番号ごとの証拠と抽出スクリプト。5 レーンの引継ぎ（LANE_*_HANDOFF.md）もここ", False),
    ("exe", "EXE の静的解析（作業番号ごとのスクリプト .py と、その出力 .txt / .md）", False),
    ("data", "解析結果の報告書（作業番号ごと、B レーンの復旧記録 B_RC_* など）。サブフォルダ normalized（ゲームのテキストを UTF-8 にしたもの）と source_snapshot は目録に含めない", False),
    ("wiki", "Wiki・DAT・ネイティブの照合（2026-10-13、戦闘の技能・移動型・回復など）", False),
    ("exp_research_20261021", "経験値・召喚・移送の調査（2026-10-21〜22）", False),
    ("tests", "E レーンの照合・監査（T018 / T020 の golden、捕捉の検証など。2026-10-20〜）", True),
    ("dev_lab/docs", "作業の記録（引継ぎ、計画、設計、Claude の研究資料）", False),
    ("rea_lab/headless_analysis/search_index", "Ghidra 統合 V9 と戦闘境界の研究（BATTLE_*）", False),
]
TEXT = {"md", "json", "jsonl", "py", "txt", "tsv", "csv", "ps1", "java", "cs", "cmd", "bat", "log"}
MAXREAD = 1_500_000


def task_titles():
    t = {}
    p = ROOT / "MASTER_LEDGER.md"
    if not p.exists():
        return t
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^\|\s*(T0\d\d)\s*\|\s*(P\d)\s*\|\s*([A-Z_]+)\s*\|\s*(.+?)\s*\|\s*$", line)
        if m and m.group(1) not in t:
            text = re.sub(r"[*`]", "", m.group(4))
            short = re.split(r"[。]", text)[0][:70]
            t[m.group(1)] = (short, m.group(3))
    return t


def clean(s, n=110):
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n] + ("…" if len(s) > n else "")


REF_RE = re.compile(r"""["']([^"'\r\n]{1,120}?\.(?:json|jsonl|md|txt|tsv|csv|dat|zip|exe|sqlite))["']""", re.I)


def refs(t):
    """説明文のないスクリプトは、中に出てくるファイル名（読み書きするもの）を並べる"""
    names = []
    for x in REF_RE.findall(t):
        x = re.split(r"[\\/]", x)[-1]
        if x and x not in names and not x.startswith("*"):
            names.append(x)
    return ("（扱うファイル: " + ", ".join(names[:4]) + (" ほか" if len(names) > 4 else "") + "）") if names else ""


def summarize(path, ext, size):
    if ext not in TEXT:
        return {"zip": "ZIP 書庫", "exe": "実行ファイル", "gz": "gzip 圧縮", "sqlite": "SQLite DB", "png": "画像",
                "pdb": "デバッグ情報"}.get(ext, "バイナリ")
    if size > MAXREAD:
        return f"（大きいので中身は読まない、{size // 1_000_000} MB）"
    try:
        raw = path.read_bytes()
    except OSError as e:
        return f"（読めない: {e.__class__.__name__}）"
    encs = ("utf-16",) if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else ("utf-8-sig", "cp932")
    for enc in encs:
        try:
            t = raw.decode(enc)
            break
        except UnicodeDecodeError:
            t = raw.decode("utf-8", "replace")
    lines = [l for l in t.splitlines() if l.strip()]
    if not lines:
        return "（空）"
    if ext == "md":
        head = next((l.lstrip("#").strip() for l in lines if l.startswith("#")), lines[0])
        status = next((l for l in lines[1:8] if re.match(r"^\s*(\[(DATE/)?STATUS\]|Owner|状態|\*\*状態|- 状態|\[ID/OWNER\])", l)), "")
        return clean(head + (" ／ " + status if status else ""), 160)
    if ext == "json":
        try:
            d = json.loads(t)
        except ValueError:
            return "JSON（読めない）"
        if isinstance(d, dict):
            parts = []
            for k in ("title", "research_id", "id", "task_id", "summary", "purpose", "description", "status", "result", "evidence", "source_kind", "conclusion"):
                if k in d and isinstance(d[k], (str, int, float, bool)):
                    parts.append(f"{k}={d[k]}")
                if len(parts) >= 3:
                    break
            if not parts:
                parts.append("キー: " + ", ".join(list(d.keys())[:6]))
            return clean(" ／ ".join(map(str, parts)), 160)
        if isinstance(d, list):
            return f"JSON 配列 {len(d)} 件"
        return "JSON"
    if ext == "jsonl":
        try:
            d = json.loads(lines[0])
            return clean(f"JSONL {len(lines)} 行、キー: " + ", ".join(list(d.keys())[:6]) if isinstance(d, dict) else f"JSONL {len(lines)} 行")
        except ValueError:
            return f"JSONL {len(lines)} 行"
    if ext == "py":
        m = re.search(r'^\s*(?:[rubRUB]{0,2})("""|\'\'\')(.*?)(\1|$)', t, re.S | re.M)
        if m and m.group(2).strip():
            return "スクリプト: " + clean(m.group(2).strip().splitlines()[0])
        c = next((l.strip("# ").strip() for l in lines if l.startswith("#") and not l.startswith("#!") and "coding" not in l), "")
        if c:
            return "スクリプト: " + clean(c)
        return "スクリプト" + refs(t)
    if ext in ("ps1", "java", "cs", "cmd", "bat"):
        c = next((re.sub(r"^(//|#|rem|REM|::)\s*", "", l.strip()) for l in lines if re.match(r"^\s*(//|#|rem |REM |::)", l) and not l.strip().startswith("#!")), "")
        return "スクリプト" + (": " + clean(c) if c else refs(t))
    if ext in ("tsv", "csv"):
        return clean(f"表 {len(lines) - 1} 行、列: " + lines[0].replace("\t", ", "), 160)
    return clean(lines[0], 160)


OWNER_RE = re.compile(r"\b([A-E])-(?:AUDIT|OFFLINE|RC|SYNC|WRQ|\d{8})")


def scan():
    rows = []
    for folder, desc, rec in FOLDERS:
        base = ROOT / folder
        if not base.is_dir():
            continue
        it = base.rglob("*") if rec else base.iterdir()
        for p in it:
            if not p.is_file() or "__pycache__" in p.parts or "_history_" in str(p):
                continue
            rel = p.relative_to(ROOT).as_posix()
            name = p.name
            ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
            st = p.stat()
            tasks = sorted(set(x.upper() for x in re.findall(r"(?i)(?<![A-Z0-9])T0\d\d(?![0-9])", name)))
            dm = re.search(r"(2026)(1\d)(\d\d)", name)
            date = f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}" if dm else datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d")
            summ = summarize(p, ext, st.st_size)
            om = OWNER_RE.search(summ) or OWNER_RE.search(name)
            owner = om.group(1) if om else (name[0] if re.match(r"^[A-E]_", name) else "")
            kind = ("スクリプト" if ext in ("py", "ps1", "java", "cs", "cmd", "bat") else
                    "報告" if ext == "md" else "データ" if ext in ("json", "jsonl", "tsv", "csv", "txt", "log") else "その他")
            rows.append(dict(path=rel, folder=folder, name=name, ext=ext, kind=kind, tasks=",".join(tasks),
                             owner=owner, date=date, size=st.st_size, summary=summ, pair=""))
    # スクリプトと出力の対応（同じ名前の大文字小文字違い）
    stem = collections.defaultdict(list)
    for r in rows:
        stem[(r["folder"], r["name"].rsplit(".", 1)[0].lower())].append(r)
    for k, rs in stem.items():
        if len(rs) > 1:
            for r in rs:
                r["pair"] = ", ".join(x["name"] for x in rs if x is not r)
    return rows


def write(rows, titles):
    gen = KB / "generated"
    gen.mkdir(exist_ok=True)
    cols = ["path", "kind", "tasks", "owner", "date", "size", "summary", "pair"]
    with open(gen / "catalog.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("# 自動生成（build_catalog.py）。" + "\t".join(cols) + "\n")
        for r in sorted(rows, key=lambda r: r["path"]):
            f.write("\t".join(str(r[c]).replace("\t", " ") for c in cols) + "\n")
    db = gen / "kb.sqlite"
    c = sqlite3.connect(db)
    c.execute("DROP TABLE IF EXISTS files")
    c.execute("CREATE TABLE files(path TEXT PRIMARY KEY, folder TEXT, name TEXT, ext TEXT, kind TEXT, tasks TEXT, owner TEXT, date TEXT, size INTEGER, summary TEXT, pair TEXT)")
    c.executemany("INSERT OR REPLACE INTO files VALUES(:path,:folder,:name,:ext,:kind,:tasks,:owner,:date,:size,:summary,:pair)", rows)
    c.commit()
    c.close()

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    md = ["# 研究資料の目録（自動生成。build_catalog.py）", "",
          f"生成: {now}。対象 {len(rows)} ファイル。各ファイルの 1 行説明は、中身の見出し・ID・状態・列名・説明文から自動で取り出したもの。",
          "検索: `python -B knowledge\\kb.py files <語>`（例: `files 教育`、`files --task T026`）。全件は generated\\catalog.tsv。", "",
          "作業番号（T0xx）の題名と状態は MASTER_LEDGER.md の作業表から。担当 A〜E は初期の 5 レーン（ID の先頭の文字から推定）。", "",
          "## フォルダ", "", "| フォルダ | ファイル数 | 期間 | 中身 |", "|---|---:|---|---|"]
    for folder, desc, _ in FOLDERS:
        rs = [r for r in rows if r["folder"] == folder]
        if rs:
            ds = sorted(r["date"] for r in rs)
            md.append(f"| `{folder}` | {len(rs)} | {ds[0]}〜{ds[-1]} | {desc} |")
    md += ["", "## 作業番号ごと", ""]
    by = collections.defaultdict(list)
    for r in rows:
        for t in (r["tasks"].split(",") if r["tasks"] else ["（作業番号なし）"]):
            by[t].append(r)
    for t in sorted(by, key=lambda x: (x.startswith("（"), x)):
        rs = by[t]
        title, status = titles.get(t, ("", ""))
        cnt = collections.Counter(r["kind"] for r in rs)
        folders = collections.Counter(r["folder"] for r in rs)
        md.append(f"### {t}" + (f"　{title}" if title else "") + (f"（{status}）" if status else ""))
        md.append("")
        md.append(f"{len(rs)} ファイル（報告 {cnt['報告']}、データ {cnt['データ']}、スクリプト {cnt['スクリプト']}）。場所: " +
                  "、".join(f"{k} {v}" for k, v in folders.most_common()))
        md.append("")
        reps = sorted([r for r in rs if r["kind"] == "報告"], key=lambda r: r["date"], reverse=True)
        if t.startswith("（"):
            # 作業番号のないものは、フォルダごとに報告を全部並べる
            for folder, _, _ in FOLDERS:
                fr = [r for r in reps if r["folder"] == folder]
                if not fr:
                    continue
                md += [f"#### `{folder}`（報告 {len(fr)} 件）", "", "| 日付 | 報告 | 見出し |", "|---|---|---|"]
                for r in fr:
                    md.append(f"| {r['date']} | `{r['name']}` | {r['summary'].replace('|', '／')} |")
                md.append("")
            md.append(f"データ・スクリプトは `kb.py files --folder <フォルダ>` で。")
            md.append("")
            continue
        if reps:
            md += ["| 日付 | 報告 | 見出し |", "|---|---|---|"]
            for r in reps[:30]:
                md.append(f"| {r['date']} | `{r['path']}` | {r['summary'].replace('|', '／')} |")
            if len(reps) > 30:
                md.append(f"| | ほか {len(reps) - 30} 件 | `kb.py files --task {t} --kind 報告 --limit 500` |")
            md.append("")
    (KB / "CATALOG.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return len(rows)


def main():
    rows = scan()
    n = write(rows, task_titles())
    print(f"目録: {n} ファイル → knowledge\\CATALOG.md、generated\\catalog.tsv、kb.sqlite の files 表")
    return 0


if __name__ == "__main__":
    sys.exit(main())
