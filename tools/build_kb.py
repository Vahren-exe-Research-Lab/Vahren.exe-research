#!/usr/bin/env python3
"""迫真戦記 ver0.67 研究知識ベースの生成（Claude 2026-10-29）

元データ（人が編集するのはこの 2 つだけ）:
  knowledge/symbols.tsv   アドレス事典（関数・位置・グローバル）
  knowledge/structs.tsv   構造体事典（オフセット）

自動で取り込むもの:
  knowledge/sources/legacy_symbols_20261011.tsv  2026-10-11 の名前付き逆コンパイルの関数名 626 件
  knowledge/sources/legacy_comments_20261011.tsv 同・命令名コメント 209 件
  RTTI（dev_lab/docs/PEER_SCRIPT01_RTTI_CLASSES_20261011.md）と原作 EXE から、仮想関数名とグローバルのウィンドウ実体
  研究資料の本文から、各アドレスがどの資料のどの節で話題になっているか（mentions）

生成物（knowledge/generated/ と knowledge/REF_*.md）は、このスクリプトを実行すれば作り直せる。
手で編集しないこと。

使い方（PowerShell）:
  python -B knowledge\\tools\\build_kb.py            # _REDEV_RESEARCH を基準に実行
  python -B knowledge\\tools\\build_kb.py --check    # 生成はせず、入力の検査だけ
"""
import argparse, collections, hashlib, json, os, re, sqlite3, struct, sys, datetime
from pathlib import Path

EXE_SHA = "e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187"
KB = Path(__file__).resolve().parent.parent          # knowledge/
ROOT_DEFAULT = KB.parent                              # _REDEV_RESEARCH/
CONF = ("実機確認", "静的確認", "テストのみ", "推定")
KINDS = ("func", "code", "global", "object", "string")

# mentions を集める資料（存在するものだけ使う）
DOCS = [
    ("FINDINGS", "dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md"),
    ("CODEX_HANDOFF", "dev_lab/docs/CHATGPT_CURRENT_HANDOFF.md"),
    ("WORK_QUEUE", "dev_lab/docs/WORK_REQUEST_QUEUE.md"),
    ("SELECTOR_INDEX", "dev_lab/docs/SELECTOR_LOADER_RESEARCH_INDEX.md"),
    ("DAT_UI_PLAN", "dev_lab/docs/DAT_GENERIC_UI_SPIKE_PLAN_20261026.md"),
    ("MASTER_LEDGER", "MASTER_LEDGER.md"),
    ("LANE_A", "evidence/LANE_A_HANDOFF.md"),
    ("LANE_B", "evidence/LANE_B_HANDOFF.md"),
    ("LANE_C", "evidence/LANE_C_HANDOFF.md"),
    ("LANE_D", "evidence/LANE_D_HANDOFF.md"),
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_tsv(p, ncol):
    rows = []
    for i, line in enumerate(Path(p).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != ncol:
            raise SystemExit(f"{p}:{i}: 列の数が {len(parts)}（{ncol} のはず）: {line[:80]}")
        rows.append((i, [x.strip() for x in parts]))
    return rows


def norm_va(s):
    return int(s, 16)


class PE:
    def __init__(self, path):
        self.d = Path(path).read_bytes()
        pe = struct.unpack_from("<I", self.d, 0x3C)[0]
        nsec = struct.unpack_from("<H", self.d, pe + 6)[0]
        opt = pe + 24
        self.base = struct.unpack_from("<I", self.d, opt + 28)[0]
        so = opt + struct.unpack_from("<H", self.d, pe + 20)[0]
        self.secs = []
        for i in range(nsec):
            o = so + 40 * i
            name = self.d[o:o + 8].rstrip(b"\0").decode("ascii", "replace")
            vsize, va, rsize, raw = struct.unpack_from("<IIII", self.d, o + 8)
            self.secs.append((name, self.base + va, vsize, raw, rsize))

    def sec(self, name):
        return next(s for s in self.secs if s[0] == name)

    def u32(self, va):
        for _, sva, vs, raw, rs in self.secs:
            if sva <= va < sva + min(vs, rs) - 3:
                return struct.unpack_from("<I", self.d, raw + va - sva)[0]
        return None


def load_rtti(root):
    p = root / "dev_lab/docs/PEER_SCRIPT01_RTTI_CLASSES_20261011.md"
    t = p.read_text(encoding="utf-8")
    rows = re.findall(r"^\| `([^`]+)` \| `0x([0-9a-f]+)` \| (\d+) \| (\d+) \| ([^|]+)\|", t, re.M)
    out = []
    for cls, vt, off, n, inh in rows:
        chain = [x.strip() for x in inh.split("→")]
        out.append((cls, int(vt, 16), int(off), int(n), chain))
    return out


def rtti_names(pe, rtti):
    _, tva, tvs, _, _ = pe.sec(".text")
    chains = {}
    for cls, vt, off, n, chain in rtti:
        chains.setdefault(cls, chain)
    slots = collections.defaultdict(list)
    for cls, vt, off, n, chain in rtti:
        for i in range(n):
            f = pe.u32(vt + 4 * i)
            if f is None or not (tva <= f < tva + tvs):
                break
            slots[f].append((cls, off, i))
    names = {}
    for f, lst in slots.items():
        prim = [(c, i) for c, o, i in lst if o == 0] or [(c, i) for c, o, i in lst]
        base = None
        for c, i in prim:
            if all(c in chains.get(c2, [c2]) for c2, _ in prim):
                base = (c, i)
                break
        off = next(o for c, o, i in lst)
        if base:
            c, i = base
            nm = f"{c}::vf{i:02d}" if off == 0 else f"{c}::b{off}_vf{i:02d}"
        else:
            c, i = prim[0]
            nm = f"{c}::vf{i:02d}_shared{len(prim)}"
        names[f] = nm
    return names


def global_instances(pe, rtti):
    _, tva, tvs, raw, rs = pe.sec(".text")
    code = pe.d[raw:raw + min(tvs, rs)]
    vt2 = {}
    chains = {}
    for cls, vt, off, n, chain in rtti:
        vt2[vt] = (cls, off)
        chains.setdefault(cls, chain)
    found = collections.defaultdict(set)
    for m in re.finditer(rb"\xc7\x05(....)(....)", code, re.S):
        g, v = struct.unpack("<II", m.group(1) + m.group(2))
        if v in vt2 and 0x600000 < g < 0xC00000 and vt2[v][1] == 0:
            found[g].add((vt2[v][0], tva + m.start()))
    out = {}
    count = collections.Counter()
    for g in sorted(found):
        classes = sorted({c for c, _ in found[g]})
        # 最も派生したクラス（他のクラスを継承関係に含むもの）を選ぶ
        best = max(classes, key=lambda c: sum(1 for c2 in classes if c2 in chains.get(c, [])))
        count[best] += 1
        nm = "g_" + re.sub(r"[^A-Za-z0-9_]", "_", best) + ("" if count[best] == 1 else f"_{count[best]}")
        site = min(s for c, s in found[g] if c == best)
        out[g] = (nm, best, classes, site)
    return out


def load_ranges(v9):
    if not v9 or not Path(v9).exists():
        return None, {}
    c = sqlite3.connect(Path(v9).resolve().as_uri() + "?mode=ro&immutable=1", uri=True)
    rng = sorted((int(a, 16), int(b, 16), int(e, 16)) for e, a, b in
                 c.execute("SELECT function_entry_va,start_va,end_va FROM function_range"))
    fnames = {int(e, 16): n for e, n in c.execute("SELECT entry_va,name FROM functions WHERE is_external=0")}
    c.close()
    return rng, fnames


def owner_of(rng, starts, va):
    import bisect
    i = bisect.bisect_right(starts, va) - 1
    for j in range(i, max(-1, i - 64), -1):
        a, b, e = rng[j]
        if a <= va <= b:
            return e
    return None


def collect_mentions(root, rng):
    starts = [r[0] for r in rng] if rng else []
    pat = re.compile(r"(?:0x|VA ?)0*([4-9A-Ba-b][0-9A-Fa-f]{5})\b")
    head = re.compile(r"^(#{1,4})\s+(.*)")
    out = []
    used = []
    for short, rel in DOCS:
        p = root / rel
        if not p.exists():
            continue
        used.append((short, rel, sha256(p)))
        heading = "(冒頭)"
        seen = set()
        for ln, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = head.match(line)
            if m:
                heading = m.group(2).strip()[:70]
            for v in pat.findall(line):
                va = int(v, 16)
                if not (0x401000 <= va < 0xC00000):
                    continue
                fn = owner_of(rng, starts, va) if rng else None
                key = (va, short, heading)
                if key in seen:
                    continue
                seen.add(key)
                out.append((va, fn, short, ln, heading))
    return out, used


def esc_md(s):
    return s.replace("|", "\\|")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT_DEFAULT))
    ap.add_argument("--exe", default=None)
    ap.add_argument("--v9", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--accept-confidence-change", action="store_true",
                    help="出典の人手検証後に確度引上げを明示的に受理（通常は拒否）")
    a = ap.parse_args()
    root = Path(a.root)
    exe = Path(a.exe) if a.exe else root / "rea_lab/targets/hakushin067_Vahren.exe"
    v9 = Path(a.v9) if a.v9 else root / "rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite"

    # ---- 入力の検査 ----
    sym = read_tsv(KB / "symbols.tsv", 6)
    sts = read_tsv(KB / "structs.tsv", 7)
    errs = []
    seen = {}
    for ln, (va, kind, name, summ, conf, src) in sym:
        try:
            v = norm_va(va)
        except ValueError:
            errs.append(f"symbols.tsv:{ln}: アドレスが不正 {va}")
            continue
        if kind not in KINDS:
            errs.append(f"symbols.tsv:{ln}: kind が不正 {kind}")
        if conf not in CONF:
            errs.append(f"symbols.tsv:{ln}: 確かさが不正 {conf}")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_:]*", name):
            errs.append(f"symbols.tsv:{ln}: 名前に使えない文字 {name}")
        if v in seen:
            errs.append(f"symbols.tsv:{ln}: アドレス重複（{seen[v]} 行目と）")
        seen[v] = ln
    for ln, (st, off, ty, name, summ, conf, src) in sts:
        if conf not in CONF:
            errs.append(f"structs.tsv:{ln}: 確かさが不正 {conf}")
        try:
            int(off, 16)
        except ValueError:
            errs.append(f"structs.tsv:{ln}: オフセットが不正 {off}")
    if errs:
        print("\n".join(errs))
        return 1
    # All future updates go through the same read-only QA, including --check.
    from check_symbols import audit
    snapshot = KB / "generated/symbols_last_validated.tsv"
    qa = audit(KB / "symbols.tsv", v9, compare=snapshot if snapshot.exists() else None)
    if qa["errors"]:
        print("\n".join("品質エラー: " + s for s in qa["errors"]))
        return 1
    promotions = [s for s in qa["warnings"] if "確度の引上げ" in s]
    if promotions and not a.accept_confidence_change:
        print("辞書の確度引上げを検出しました。出典と実機・静的証拠を人手確認してください。")
        print("\n".join(promotions[:15]))
        print("確認済みの場合だけ --accept-confidence-change を明示指定してください。")
        return 1
    print(f"辞書品質: {qa['count']}件 / エラー0 / 警告{len(qa['warnings'])}件")
    for warning in qa["warnings"][:12]:
        print("品質警告: " + warning)
    symbol_sha_before = sha256(KB / "symbols.tsv")
    if not exe.exists() or sha256(exe) != EXE_SHA:
        print(f"原作 EXE が見つからないか、SHA が違います: {exe}")
        return 1
    print(f"入力 OK: symbols {len(sym)} 行、structs {len(sts)} 行")
    if a.check:
        return 0

    pe = PE(exe)
    rtti = load_rtti(root)
    rnames = rtti_names(pe, rtti)
    ginst = global_instances(pe, rtti)
    rng, v9names = load_ranges(v9)
    legacy = {}
    for line in (KB / "sources/legacy_symbols_20261011.tsv").read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            va, nm = line.split("\t", 1)
            legacy[int(va, 16)] = nm.strip()
    lcomments = []
    for line in (KB / "sources/legacy_comments_20261011.tsv").read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            va, cm = line.split("\t", 1)
            lcomments.append((int(va, 16), cm.strip()))

    # ---- 名前の統合（優先: 手書き > グローバル自動 > 2026-10-11 の名前 > RTTI 自動）----
    allsym = {}
    for ln, (va, kind, name, summ, conf, src) in sym:
        allsym[norm_va(va)] = dict(name=name, kind=kind, origin="curated", conf=conf, summary=summ, source=src)
    for g, (nm, cls, classes, site) in ginst.items():
        if g not in allsym:
            allsym[g] = dict(name=nm, kind="object", origin="auto_global", conf="静的確認",
                             summary=f"{cls} のグローバル実体（{hex(site)} で vtable を設定）", source="自動(RTTI+EXE)")
    for f, nm in legacy.items():
        # 2026-10-11 の「Class::vfNN」は自動の名前で、副 vtable を区別していないので、RTTI の名前を優先する
        if f in rnames and "::vf" in nm:
            continue
        if f not in allsym:
            allsym[f] = dict(name=nm, kind="func", origin="legacy_20261011", conf="静的確認",
                             summary="", source="2026-10-11 名前付き逆コンパイル")
    for f, nm in rnames.items():
        if f not in allsym:
            allsym[f] = dict(name=nm, kind="func", origin="auto_rtti", conf="静的確認",
                             summary="RTTI の仮想関数表から付けた名前", source="自動(RTTI+EXE)")
    # 名前の重複を解消（Ghidra・x32dbg では名前が一意である必要がある）
    byname = collections.defaultdict(list)
    for v, s in allsym.items():
        byname[s["name"]].append(v)
    for nm, vs in byname.items():
        if len(vs) > 1:
            for v in vs:
                if allsym[v]["origin"] != "curated":
                    allsym[v]["name"] = f"{nm}_{v:06X}"

    mentions, used_docs = collect_mentions(root, rng)

    gen = KB / "generated"
    (gen / "ghidra").mkdir(parents=True, exist_ok=True)

    # ---- symbols_all.tsv ----
    with open(gen / "symbols_all.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("# 自動生成（build_kb.py）。手で編集しない。va\tname\tkind\torigin\tconfidence\tsummary\tsource\n")
        for v in sorted(allsym):
            s = allsym[v]
            f.write(f"0x{v:06X}\t{s['name']}\t{s['kind']}\t{s['origin']}\t{s['conf']}\t{s['summary']}\t{s['source']}\n")

    # ---- mentions.tsv ----
    with open(gen / "mentions.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("# 自動生成。va\tfunction\tdoc\tline\theading\n")
        for va, fn, doc, ln, hd in sorted(mentions, key=lambda x: (x[0], x[2], x[3])):
            f.write(f"0x{va:06X}\t{'' if fn is None else f'0x{fn:06X}'}\t{doc}\t{ln}\t{hd}\n")

    # ---- kb.sqlite ----
    dbp = gen / "kb.sqlite"
    if dbp.exists():
        dbp.unlink()
    db = sqlite3.connect(dbp)
    db.executescript("""
      CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
      CREATE TABLE symbols(va INTEGER PRIMARY KEY, name TEXT, kind TEXT, origin TEXT, confidence TEXT, summary TEXT, source TEXT);
      CREATE TABLE structs(struct TEXT, offset INTEGER, type TEXT, name TEXT, summary TEXT, confidence TEXT, source TEXT);
      CREATE TABLE mentions(va INTEGER, function_va INTEGER, doc TEXT, line INTEGER, heading TEXT);
      CREATE TABLE comments(va INTEGER, text TEXT, origin TEXT);
      CREATE INDEX mention_va ON mentions(va); CREATE INDEX mention_fn ON mentions(function_va);
    """)
    db.executemany("INSERT INTO symbols VALUES(?,?,?,?,?,?,?)",
                   [(v, s["name"], s["kind"], s["origin"], s["conf"], s["summary"], s["source"]) for v, s in allsym.items()])
    db.executemany("INSERT INTO structs VALUES(?,?,?,?,?,?,?)",
                   [(st, int(off, 16), ty, nm, sm, cf, sc) for _, (st, off, ty, nm, sm, cf, sc) in sts])
    db.executemany("INSERT INTO mentions VALUES(?,?,?,?,?)", mentions)
    db.executemany("INSERT INTO comments VALUES(?,?,?)", [(v, c, "legacy_20261011") for v, c in lcomments])
    now = datetime.datetime.now().isoformat(timespec="seconds")
    meta = {"built": now, "exe_sha256": EXE_SHA, "v9": (v9.name if rng else "(なし)"),
            "docs": json.dumps(used_docs, ensure_ascii=False)}
    db.executemany("INSERT INTO meta VALUES(?,?)", list(meta.items()))
    db.commit()
    db.close()

    # ---- x32dbg ----
    def rva(v):
        return v - pe.base
    with open(gen / "x32dbg_labels.txt", "w", encoding="ascii", errors="replace", newline="\r\n") as f:
        f.write("// x32dbg labels for Vahren.exe ver0.67 (generated by knowledge/tools/build_kb.py)\n")
        for v in sorted(allsym):
            nm = allsym[v]["name"]
            f.write(f'lbl Vahren.exe+{rva(v):X}, "{nm}"\n')
    with open(gen / "x32dbg_comments.txt", "w", encoding="utf-8", newline="\r\n") as f:
        f.write("// x32dbg 用（UTF-8）。手書きの事典の説明をコメントとして付ける。\n")
        for v in sorted(allsym):
            s = allsym[v]
            if s["origin"] == "curated":
                cm = f"{s['summary']}［{s['conf']}］".replace('"', "'")
                f.write(f'cmt Vahren.exe+{rva(v):X}, "{cm[:250]}"\n')
        for v, c in lcomments:
            c2 = c[:250].replace('"', "'")
            f.write(f'cmt Vahren.exe+{rva(v):X}, "{c2}"\n')

    # ---- Ghidra 用の入力 ----
    ment_by = collections.defaultdict(list)
    for va, fn, doc, ln, hd in mentions:
        k = fn if fn is not None else va
        ment_by[k].append(f"{doc}:{ln} {hd}")
    with open(gen / "ghidra/kb_symbols.tsv", "w", encoding="utf-8", newline="\n") as f:
        for v in sorted(allsym):
            s = allsym[v]
            lines = []
            if s["summary"]:
                lines.append(f"{s['summary']}［{s['conf']}／{s['source']}］")
            refs = ment_by.get(v, [])
            if refs:
                lines.append("資料: " + " ; ".join(sorted(set(refs))[:8]) + (f" ほか {len(set(refs)) - 8} 件" if len(set(refs)) > 8 else ""))
            cm = " // ".join(lines).replace("\t", " ").replace("\n", " ")
            f.write(f"{v:08X}\t{s['kind']}\t{s['name']}\t{cm}\n")
        # 名前のない関数でも、資料で話題になっていればコメントだけ付ける
        for k, refs in sorted(ment_by.items()):
            if k in allsym or k is None:
                continue
            if rng and k in v9names:
                cm = "資料: " + " ; ".join(sorted(set(refs))[:8])
                f.write(f"{k:08X}\tcomment_only\t-\t{cm}\n")
    with open(gen / "ghidra/kb_structs.tsv", "w", encoding="utf-8", newline="\n") as f:
        for _, (st, off, ty, nm, sm, cf, sc) in sts:
            f.write(f"{st}\t{int(off, 16)}\t{ty}\t{nm}\t{sm}［{cf}］\n")
    with open(gen / "ghidra/kb_comments.tsv", "w", encoding="utf-8", newline="\n") as f:
        for v, c in lcomments:
            f.write(f"{v:08X}\t{c}\n")

    # ---- 読みやすい事典 ----
    def mrefs(v, n=4):
        r = sorted(set(ment_by.get(v, [])))
        return "<br>".join(esc_md(x) for x in r[:n]) + (f"<br>ほか {len(r) - n} 件" if len(r) > n else "")
    groups = collections.OrderedDict()
    cur = "その他"
    for line in (KB / "symbols.tsv").read_text(encoding="utf-8").splitlines():
        m = re.match(r"#\s*----\s*(.+?)\s*----", line)
        if m:
            cur = m.group(1)
            continue
        if line.startswith("0x"):
            groups.setdefault(cur, []).append(norm_va(line.split("\t")[0]))
    md = ["# アドレス事典（自動生成。元データは symbols.tsv）", "",
          f"生成: {now}。原作 Vahren.exe ver0.67（SHA {EXE_SHA[:12]}…）の VA（0x400000 基準）。",
          "x32dbg では `Vahren.exe+(VA−0x400000)` で同じ場所を指せる。", "",
          "確かさ: **実機確認**（ゲームで確かめた）／**静的確認**（機械語で確かめた）／**テストのみ**（合成テストだけ）／**推定**。", "",
          f"このほか、自動で名前を付けたもの: グローバルのウィンドウ実体 {sum(1 for s in allsym.values() if s['origin']=='auto_global')} 件、"
          f"2026-10-11 の名前 {sum(1 for s in allsym.values() if s['origin']=='legacy_20261011')} 件、RTTI の仮想関数 {sum(1 for s in allsym.values() if s['origin']=='auto_rtti')} 件。"
          "一覧は generated/symbols_all.tsv。", ""]
    for g, vs in groups.items():
        md += [f"## {g}", "", "| アドレス | 種類 | 名前 | 意味 | 確かさ | 出典 | 資料での言及 |", "|---|---|---|---|---|---|---|"]
        for v in vs:
            s = allsym[v]
            md.append(f"| `0x{v:06X}` | {s['kind']} | `{s['name']}` | {esc_md(s['summary'])} | {s['conf']} | {esc_md(s['source'])} | {mrefs(v)} |")
        md.append("")
    md += ["## グローバルのウィンドウ実体（自動）", "", "| アドレス | 名前 | クラス |", "|---|---|---|"]
    for g, (nm, cls, classes, site) in ginst.items():
        md.append(f"| `0x{g:06X}` | `{allsym[g]['name']}` | {cls} |")
    (KB / "REF_ADDRESSES.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    md = ["# 構造体事典（自動生成。元データは structs.tsv）", "",
          "オフセットは構造体の先頭から。std::string は、文字列の本体（16 バイトの内部バッファまたはポインタ）が書いたオフセットにあり、+0x10 に長さ、+0x14 に容量がある。", ""]
    bys = collections.OrderedDict()
    for _, r in sts:
        bys.setdefault(r[0], []).append(r)
    for st, rows in bys.items():
        md += [f"## {st}", "", "| オフセット | 型 | 名前 | 意味 | 確かさ | 出典 |", "|---|---|---|---|---|---|"]
        for _, off, ty, nm, sm, cf, sc in sorted(rows, key=lambda r: int(r[1], 16)):
            md.append(f"| `+0x{int(off,16):X}` | {ty} | `{nm}` | {esc_md(sm)} | {cf} | {esc_md(sc)} |")
        md.append("")
    (KB / "REF_STRUCTS.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"名前 {len(allsym)} 件（手書き {len(sym)}、グローバル自動 {len(ginst)}、2026-10-11 {len(legacy)}、RTTI {len(rnames)}）")
    print(f"資料での言及 {len(mentions)} 件（{len(used_docs)} 資料）")
    print(f"出力: {gen}")
    # kb.sqlite を作り直したので、目録（files 表と CATALOG.md）も作り直す
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_catalog
    build_catalog.main()
    # Independent incremental DB, not the 10-document legacy mentions table.
    import research_index
    if research_index.main([]) != 0:
        print("研究全文索引の生成に失敗")
        return 1
    # Successful builds establish the next provenance/confidence comparison baseline.
    source = KB / "symbols.tsv"
    if sha256(source) != symbol_sha_before:
        print("symbols.tsv が実行中に変わりました。承認スナップショットは更新しません。")
        return 1
    tmp = snapshot.with_suffix(".tsv.tmp")
    if tmp.exists():
        print("承認スナップショットの一時ファイルが既にあります。競合を確認してください。")
        return 1
    tmp.write_bytes(source.read_bytes())
    os.replace(tmp, snapshot)
    print("辞書の比較基準を保存:", snapshot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
