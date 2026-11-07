"""Build and search a portable function/memory reference from the checked-in dictionaries.

No game executable, generated database, network or third-party package is required.
Run `python tools/reference.py search 解雇 --json`, `build`, or `check`.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SYMBOL_COLUMNS = ("va", "kind", "name", "summary", "confidence", "source")
FIELD_COLUMNS = ("struct", "offset", "type", "name", "summary", "confidence", "source")


def address(value):
    match = re.fullmatch(r"(?i)Vahren\.exe\+(?:0x)?([0-9a-f]+)", value.strip())
    if match:
        return f"va:0x{0x400000 + int(match[1], 16):08X}"
    if re.fullmatch(r"(?i)(?:0x)?[0-9a-f]{5,8}", value.strip()):
        return f"va:0x{int(value, 16):08X}"
    return value


def table(root, filename, columns):
    rows = []
    with (root / filename).open(encoding="utf-8-sig", newline="") as stream:
        for line, cells in enumerate(csv.reader(stream, delimiter="\t"), 1):
            if not cells or cells[0].startswith("#"):
                continue
            if len(cells) != len(columns):
                raise ValueError(f"{filename}:{line}: expected {len(columns)} columns")
            row = dict(zip(columns, cells))
            row["dictionary_line"] = line
            rows.append(row)
    return rows


def load_mentions(root):
    """Index literal VA occurrences in explicitly recovered, hash-verified reports."""
    ledger = root / "research/recovered/RECOVERY_LEDGER.tsv"
    if not ledger.exists():
        return []
    mentions = []
    seen_sources = set()
    pattern = re.compile(r"0x([0-9a-f]{6,8})(?![0-9a-f])", re.I)
    with ledger.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            relative = Path(row["destination"])
            source = (root / relative).resolve()
            if relative.is_absolute() or not source.is_relative_to(root):
                raise ValueError(f"Source path escapes repository: {row['destination']}")
            if not source.is_file():
                raise ValueError(f"Missing recovered source: {row['destination']}")
            payload = source.read_bytes()
            digest = hashlib.sha256(payload).hexdigest()
            if digest.lower() != row["destination_sha256"].lower():
                raise ValueError(f"Stale recovered source checksum: {row['destination']}")
            if source in seen_sources:
                continue
            seen_sources.add(source)
            path = source.relative_to(root).as_posix()
            for line, content in enumerate(payload.decode("utf-8-sig").splitlines(), 1):
                for va in sorted({int(match[1], 16) for match in pattern.finditer(content)}):
                    mentions.append({
                        "id": f"mention:{path}:{line}:{va:08X}",
                        "kind": "source_mention", "va": f"0x{va:08X}",
                        "subject": f"va:0x{va:08X}", "name": f"{path}:{line}",
                        "summary": content.strip(),
                        "confidence": "文書内の言及（意味・動作の検証なし）",
                        "source": {"path": path, "sha256": digest,
                                   "start_line": line, "end_line": line}})
    return mentions


def load(root):
    root = Path(root).resolve()
    symbols = table(root, "symbols.tsv", SYMBOL_COLUMNS)
    fields = table(root, "structs.tsv", FIELD_COLUMNS)
    for row in symbols:
        row["id"] = address(row["va"])
    for row in fields:
        row["id"] = f"field:{row['struct']}:0x{int(row['offset'], 16):X}"
    ids = set()
    for row in symbols + fields:
        if row["id"] in ids:
            raise ValueError(f"Duplicate dictionary ID: {row['id']}")
        ids.add(row["id"])
    ids.update(f"struct:{row['struct']}" for row in fields)
    relations = []
    relation_ids = set()
    aliases = {}
    structure_names = {row["struct"].casefold() for row in fields}
    path = root / "reference/relations.jsonl"
    for line, text in enumerate(path.read_text(encoding="utf-8-sig").splitlines() if path.exists() else [], 1):
        if not text.strip():
            continue
        item = json.loads(text)
        required = ("id", "subject", "predicate", "object", "summary", "confidence", "source", "target_version")
        if any(not item.get(key) for key in required):
            raise ValueError(f"relations.jsonl:{line}: missing required value")
        if item["id"] in relation_ids:
            raise ValueError(f"Duplicate relation ID: {item['id']}")
        if item["subject"] not in ids or item["object"] not in ids:
            raise ValueError(f"Unknown relation endpoint: {item['id']}")
        source = item["source"]
        relative = Path(source["path"])
        evidence = (root / relative).resolve()
        if relative.is_absolute() or not evidence.is_relative_to(root):
            raise ValueError(f"Source path escapes repository: {item['id']}")
        if not evidence.is_file():
            raise ValueError(f"Missing source: {source['path']}")
        payload = evidence.read_bytes()
        if hashlib.sha256(payload).hexdigest().lower() != source["sha256"].lower():
            raise ValueError(f"Stale source checksum: {source['path']}")
        count = len(payload.decode("utf-8-sig").splitlines())
        if not 1 <= source["start_line"] <= source["end_line"] <= count:
            raise ValueError(f"Invalid source lines: {item['id']}")
        if "aliases" in item:
            names = item["aliases"]
            if item["predicate"] != "uses_layout" or not item["object"].startswith("struct:"):
                raise ValueError(f"Aliases require an explicit uses_layout relation: {item['id']}")
            if not isinstance(names, list) or not names:
                raise ValueError(f"Aliases must be a nonempty list: {item['id']}")
            target = item["object"].removeprefix("struct:")
            for name in names:
                if not isinstance(name, str) or not name.strip() or name != name.strip():
                    raise ValueError(f"Alias must be a nonempty name: {item['id']}")
                key = name.casefold()
                if key in structure_names:
                    raise ValueError(f"Alias collides with a known structure: {name}")
                if key in aliases and aliases[key] != target:
                    raise ValueError(f"Conflicting layout alias: {name}")
                aliases[key] = target
        relations.append(item)
        relation_ids.add(item["id"])
    return {"symbols": symbols, "fields": fields, "relations": relations,
            "mentions": load_mentions(root), "aliases": aliases}


def search(data, query):
    needle = address(query).casefold()
    field = re.fullmatch(r"(.+?)\s*\+\s*(0x[0-9a-f]+)", query, re.I)
    if field:
        name = field[1].strip()
        structure = data["aliases"].get(name.casefold(), name)
        needle = f"field:{structure}:0x{int(field[2], 16):X}".casefold()
    rows = data["symbols"] + data["fields"]
    matched = [row for row in rows if needle in json.dumps(row, ensure_ascii=False).casefold()]
    ids = {row["id"] for row in matched}
    related = [row for row in data["relations"]
               if row["subject"] in ids or row["object"] in ids
               or needle in json.dumps(row, ensure_ascii=False).casefold()]
    mentions = [row for row in data["mentions"]
                if needle in json.dumps(row, ensure_ascii=False).casefold()]
    return matched + related + mentions


def text(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def struct_filename(name):
    return quote(name, safe="") + ".md"


def endpoint_link(identifier, labels):
    parts = identifier.split(":")
    if parts[0] == "va":
        target = f"../symbols/{int(parts[1], 16):08X}.md"
    else:
        target = "../structs/" + quote(struct_filename(parts[1]), safe="")
        if parts[0] == "field":
            target += f"#field-{int(parts[2], 16):x}"
    return f"[{text(labels.get(identifier, identifier))}]({target})"


def relation_lines(relations, identifier, labels):
    lines = []
    for row in relations:
        if identifier not in (row["subject"], row["object"]):
            continue
        source = row["source"]
        link = "../../" + quote(source["path"], safe="/")
        link += f"?plain=1#L{source['start_line']}-L{source['end_line']}"
        lines.append(
            f"- {endpoint_link(row['subject'], labels)} → `{row['predicate']}` → "
            f"{endpoint_link(row['object'], labels)}。{text(row['summary'])} "
            f"（{text(row['confidence'])}、{text(row['target_version'])}）。"
            f"[根拠]({link}) · `{row['id']}`")
    return lines


def render(root, data):
    files = {}
    labels = {row["id"]: row["name"] for row in data["symbols"]}
    labels.update({row["id"]: f"{row['struct']} + {row['offset']} {row['name']}" for row in data["fields"]})
    labels.update({f"struct:{row['struct']}": row["struct"] for row in data["fields"]})
    index = ["# 迫真戦記 ver0.67 関数・メモリ事典", "",
             "<!-- Generated by tools/reference.py. Edit dictionaries and relations, then build. -->", "",
             "辞書の確度・出典を保持しています。関係ごとの確度は各根拠に記載しています。", "",
             "検索は `python tools/reference.py search 解雇`。アドレス、名前、"
             "`StatusWnd+0x1C6` でも検索できます。`--json` で同じ内容を機械可読形式で取得できます。", "",
             "## 関数・アドレス", "", "| VA | 名前 | 種別 | 意味 |", "|---|---|---|---|"]
    for row in sorted(data["symbols"], key=lambda item: int(item["va"], 16)):
        filename = f"{int(row['va'], 16):08X}.md"
        lines = [f"# {row['name']} — {row['va']}", "",
                 "<!-- Generated by tools/reference.py. -->", "",
                 f"{row['summary']}", "", f"- 種別　`{row['kind']}`",
                 "- 対象　迫真戦記 ver0.67", f"- 辞書の確度　{row['confidence']}",
                 f"- 辞書の出典表記　{row['source']}",
                 f"- [元の辞書行](../../symbols.tsv#L{row['dictionary_line']})", "",
                 "## 関数・メモリとの関係", ""]
        lines += relation_lines(data["relations"], row["id"], labels) or ["関係の個別採録は未実施です。"]
        mentions = [item for item in data["mentions"] if item["subject"] == row["id"]]
        if mentions:
            lines += ["", "## 研究文書での言及", "",
                      "以下は文書内の言及（意味・動作の検証なし）です。文書の限界や訂正も併せて確認してください。", ""]
            for mention in mentions:
                source = mention["source"]
                link = "../../" + quote(source["path"], safe="/")
                link += f"?plain=1#L{source['start_line']}-L{source['end_line']}"
                lines.append(f"- [{text(mention['name'])}]({link}) — {text(mention['summary'])}")
        lines += ["", "[事典の入口](../README.md)", ""]
        files["reference/symbols/" + filename] = "\n".join(lines)
        index.append(f"| {row['va']} | [{text(row['name'])}](symbols/{filename}) | {text(row['kind'])} | {text(row['summary'])} |")
    index += ["", "## 構造体・フィールド", ""]
    for name in sorted({row["struct"] for row in data["fields"]}):
        lines = [f"# {name}", "", "<!-- Generated by tools/reference.py. -->", "",
                 "対象は迫真戦記 ver0.67。各フィールドの型・確度・出典は元の辞書から保持しています。", ""]
        lines += relation_lines(data["relations"], f"struct:{name}", labels)
        for row in sorted((item for item in data["fields"] if item["struct"] == name), key=lambda item: int(item["offset"], 16)):
            lines += ["", f"<a id=\"field-{int(row['offset'], 16):x}\"></a>",
                      f"## {row['offset']} {row['name']}", "", row["summary"], "",
                      f"- 型　`{row['type']}`", f"- 辞書の確度　{row['confidence']}",
                      f"- 辞書の出典表記　{row['source']}",
                      f"- [元の辞書行](../../structs.tsv#L{row['dictionary_line']})", ""]
            lines += relation_lines(data["relations"], row["id"], labels) or ["読み手・書き手の個別採録は未実施です。"]
        lines += ["", "[事典の入口](../README.md)", ""]
        filename = struct_filename(name)
        files["reference/structs/" + filename] = "\n".join(lines)
        index.append(f"- [{text(name)}](structs/{quote(filename, safe='')})")
    index += ["", f"辞書項目 {len(data['symbols'])} 件、フィールド {len(data['fields'])} 件、根拠付き関係 {len(data['relations'])} 件。", ""]
    index += [f"回収済み文書のVA言及 {len(data['mentions'])} 件を検索対象に含みます。辞書未登録のVAも検索できます。", ""]
    files["reference/README.md"] = "\n".join(index)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    query = commands.add_parser("search")
    query.add_argument("query")
    query.add_argument("--json", action="store_true")
    commands.add_parser("build")
    commands.add_parser("check")
    args = parser.parse_args()
    try:
        data = load(args.root)
        if args.command == "search":
            matches = search(data, args.query)
            if args.json:
                print(json.dumps(matches, ensure_ascii=False, indent=2))
            else:
                for row in matches:
                    print(f"{row['id']}  {row.get('name', row.get('predicate'))}  {row['summary']}  [{row['confidence']}]")
            return 0
        files = render(args.root, data)
        stale = []
        for directory in ("reference/symbols", "reference/structs"):
            for existing in (args.root / directory).glob("*.md"):
                name = existing.relative_to(args.root).as_posix()
                if name not in files and "<!-- Generated by tools/reference.py." in existing.read_text(encoding="utf-8"):
                    stale.append(name + " (obsolete generated page; review removal)")
        for name, content in files.items():
            output = args.root / name
            if args.command == "build":
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(content, encoding="utf-8", newline="\n")
            elif not output.is_file() or output.read_text(encoding="utf-8") != content:
                stale.append(name)
        if stale:
            print("Rebuild required:\n" + "\n".join(stale), file=sys.stderr)
            return 1
        print(f"{args.command.upper()} PASS ({len(files)} pages)")
        return 0
    except (ValueError, KeyError, OSError) as error:
        print(f"Reference error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
