#!/usr/bin/env python3
"""Reusable read-only symbols.tsv QA: schema, uniqueness, V9 ownership and provenance.
No game files, dictionary rows or confidence labels are changed.
"""
import argparse
import bisect
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
V9 = KB.parent / "rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite"
KIND = {"func", "code", "global", "object", "string"}
CONF = {"実機確認", "静的確認", "テストのみ", "推定"}
RANK = {"推定": 0, "テストのみ": 1, "静的確認": 2, "実機確認": 3}
NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_:]*\Z")
VA = re.compile(r"0x[0-9a-fA-F]{6}\Z")

def read_rows(path):
    rows, errors = [], []
    for i, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 6:
            errors.append(f"{path.name}:{i}: 6列ではなく{len(fields)}列")
            continue
        rows.append((i, fields))
    return rows, errors

def read_v9(path):
    if path is None or not path.exists():
        return None
    con = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    funs = {int(a, 16) for (a,) in con.execute("SELECT entry_va FROM functions WHERE is_external=0")}
    ranges = sorted((int(a, 16), int(b, 16), int(e, 16)) for a,b,e in
                    con.execute("SELECT start_va,end_va,function_entry_va FROM function_range"))
    con.close()
    return funs, ranges, [a for a,b,e in ranges]

def audit(path, v9_path=V9, compare=None):
    path = Path(path)
    old_rows, old_issues = read_rows(Path(compare)) if compare else ([], [])
    previous = {}
    for n, fields in old_rows:
        if VA.fullmatch(fields[0]):
            previous[int(fields[0],16)] = (n, fields)
    rows, errors = read_rows(path)
    errors.extend(old_issues)
    warnings = []
    seen_va, seen_names = {}, {}
    stats = Counter()
    verified = read_v9(v9_path)
    for n, f in rows:
        addr, kind, name, summary, confidence, source = (s.strip() for s in f)
        stats[kind] += 1
        if not VA.fullmatch(addr):
            errors.append(f"{path.name}:{n}: VAの形式が不正 {addr!r}")
            continue
        a = int(addr, 16)
        if a in seen_va:
            errors.append(f"{path.name}:{n}: VAが重複 {addr}（既存{seen_va[a]}行）")
        seen_va[a] = n
        if not NAME.fullmatch(name):
            errors.append(f"{path.name}:{n}: 名前が不正 {name!r}")
        if name in seen_names:
            errors.append(f"{path.name}:{n}: 名前が重複 {name}（既存{seen_names[name]}行）")
        seen_names[name] = n
        if kind not in KIND:
            errors.append(f"{path.name}:{n}: kind不正 {kind}")
        if confidence not in CONF:
            errors.append(f"{path.name}:{n}: confidence不正 {confidence}")
        if not summary or not source:
            errors.append(f"{path.name}:{n}: summary/sourceが空")
        if any("\n" in x or "\r" in x for x in f):
            errors.append(f"{path.name}:{n}: 改行を含む列")
        if not (0x401000 <= a <= 0xBFFFFF):
            warnings.append(f"{path.name}:{n}: 通常のVA範囲外 {addr}")
        if kind in ("func", "code") and a >= 0x639000:
            warnings.append(f"{path.name}:{n}: コード種別なのにデータ領域 {addr}")
        if 0x5710C0 <= a <= 0x571500:
            warnings.append(f"{path.name}:{n}: 旧安全拒否範囲。既存記述の引用のみ、再解析禁止")
        if verified:
            funcs, ranges, starts = verified
            if kind == "func" and a not in funcs:
                warnings.append(f"{path.name}:{n}: V9関数先頭に無い {addr} {name}")
            if kind == "code":
                i = bisect.bisect_right(starts, a) - 1
                if i < 0 or not (ranges[i][0] <= a <= ranges[i][1]):
                    warnings.append(f"{path.name}:{n}: V9関数範囲に属さないcode {addr}")
        if a in previous:
            old = previous[a][1]
            old_conf, old_source = old[4].strip(), old[5].strip()
            if (confidence in RANK and old_conf in RANK
                    and RANK[confidence] > RANK[old_conf]):
                warnings.append(f"{path.name}:{n}: 確度の引上げは要根拠確認 "
                                f"{addr} {old_conf} -> {confidence}"
                                + ("（source不変）" if source == old_source else ""))
            if old[1] != kind:
                warnings.append(f"{path.name}:{n}: kind変更 {addr} {old[1]} -> {kind}")
    return dict(path=str(path), count=len(rows), by_kind=dict(stats),
                errors=errors, warnings=warnings, changed_from=(
                    str(compare) if compare else None))

def main(argv=None):
    p = argparse.ArgumentParser(description="symbols.tsvを変更せず検証")
    p.add_argument("path", nargs="?", default=str(KB / "symbols.tsv"))
    p.add_argument("--compare", help="以前のTSVとの差分・確度引上げを検出")
    p.add_argument("--v9", default=str(V9))
    p.add_argument("--strict", action="store_true", help="警告も失敗とする")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    result = audit(Path(args.path), Path(args.v9), args.compare)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"辞書品質: {result['count']}件、エラー{len(result['errors'])}、"
              f"警告{len(result['warnings'])}")
        for category in ("errors", "warnings"):
            for item in result[category][:60]:
                print(("ERROR: " if category == "errors" else "WARN: ") + item)
            if len(result[category]) > 60:
                print(f"... 残り{len(result[category])-60}件は --json で確認")
    return 2 if result["errors"] or (args.strict and result["warnings"]) else 0

if __name__ == "__main__":
    raise SystemExit(main())

