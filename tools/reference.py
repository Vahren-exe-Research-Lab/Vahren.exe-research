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

import export_static_calls as static_index

ROOT = Path(__file__).resolve().parent.parent
SYMBOL_COLUMNS = ("va", "kind", "name", "summary", "confidence", "source")
FIELD_COLUMNS = ("struct", "offset", "type", "name", "summary", "confidence", "source")


def load_static_calls(root, symbols):
    path = root / "reference/static_calls.tsv"
    meta = root / "reference/static_calls_source.json"
    if not path.exists() and not meta.exists():
        return [], None
    if not path.is_file() or not meta.is_file():
        raise ValueError("Incomplete static call index")
    receipt = json.loads(meta.read_text(encoding="utf-8-sig"))
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest.casefold() != receipt["static_calls_sha256"].casefold():
        raise ValueError("Static call index checksum mismatch")
    if (receipt["format_version"] != 1 or receipt["source_state"] != static_index.SOURCE_STATE
            or receipt["source_pe_sha256"].upper() != static_index.SOURCE_PE_SHA256
            or not re.fullmatch(r"[0-9a-fA-F]{64}", receipt["source_db_sha256"])):
        raise ValueError("Invalid static call source receipt")
    captured = {address(value) for value in receipt["selection"]["eligible_endpoint_vas"]}
    if len(captured) != receipt["counts"]["eligible_endpoints"]:
        raise ValueError("Static call endpoint count mismatch")
    functions = {row["id"]: row for row in symbols if row["kind"] == "func"}
    rows = []
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if tuple(reader.fieldnames or ()) != static_index.COLUMNS:
            raise ValueError("Invalid static call columns")
        for item in reader:
            caller, callee = address(item["caller_va"]), address(item["callee_va"])
            values = [static_index.number(item[key]) for key in ("caller_va", "callee_va", "site_va")]
            if (any(value is None or static_index.in_ranges(value, static_index.EXCLUDED_RANGES) for value in values)
                    or caller not in captured or callee not in captured
                    or caller not in functions or callee not in functions):
                raise ValueError("Unknown or excluded static call endpoint/site")
            if (item["source_state"] != receipt["source_state"]
                    or item["source_db_sha256"].casefold() != receipt["source_db_sha256"].casefold()
                    or values[2] in seen):
                raise ValueError("Inconsistent or duplicate static call site")
            seen.add(values[2])
            site = static_index.va(values[2])
            rows.append({"id": f"static-call:{site}", "kind": "static_callsite",
                         "subject": caller, "object": callee, "predicate": "calls_in_static_index",
                         "site_va": site, "source_record_id": item["source_record_id"],
                         "name": f"{functions[caller]['name']} → {functions[callee]['name']}",
                         "summary": "登録関数間の直接CALL・V9静的索引",
                         "confidence": "静的索引（当時の照合フラグ。今回の独立検証なし）",
                         "source_db_sha256": receipt["source_db_sha256"],
                         "source_pe_sha256": receipt["source_pe_sha256"],
                         "source": {"path": "reference/static_calls.tsv", "sha256": digest,
                                    "start_line": reader.line_num, "end_line": reader.line_num,
                                    "receipt_path": "reference/static_calls_source.json"}})
    if len(rows) != receipt["counts"]["exported_calls"]:
        raise ValueError("Static call row count mismatch")
    return rows, receipt


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


def run_records(content, path, digest, recovery):
    run = json.loads(content)
    if not isinstance(run, dict) or not isinstance(run.get("runId"), str) or not run["runId"]:
        raise ValueError(f"Malformed run record header: {path}")
    if not isinstance(run.get("records"), list):
        raise ValueError(f"Malformed run record list: {path}")
    locations = {}
    for match in re.finditer(r'"address"\s*:\s*("(?:[^"\\]|\\.)*")', content):
        raw = json.loads(match[1])
        locations.setdefault(raw, []).append(content.count("\n", 0, match.start()) + 1)
    rows = []
    seen = set()
    for record in run["records"]:
        required = ("address", "related_task", "title", "status")
        if (not isinstance(record, dict)
                or any(not isinstance(record.get(key), str) or not record[key] for key in required)
                or not isinstance(record.get("methods"), dict)
                or any(not isinstance(value, dict) for value in record["methods"].values())):
            raise ValueError(f"Malformed run record: {path}")
        subject = address(record["address"])
        if not subject.startswith("va:0x") or subject in seen:
            raise ValueError(f"Invalid or duplicate run record address: {path}")
        seen.add(subject)
        if not locations.get(record["address"]):
            raise ValueError(f"Missing literal run record address line: {path}")
        line = locations[record["address"]].pop(0)
        rows.append({
            "id": f"run:{run['runId']}:{subject.removeprefix('va:')}",
            "kind": "research_run_record", "va": subject.removeprefix("va:"),
            "subject": subject, "name": f"{path}:{line}", "summary": record["title"],
            "confidence": "過去の解析取得記録（意味・動作・原作実機の検証なし）",
            "reported_status": record["status"], "run_id": run["runId"],
            "related_task": record["related_task"], "methods": record["methods"],
            "recovery": recovery,
            "source": {"path": path, "sha256": digest, "start_line": line, "end_line": line}})
    return rows


def local_field_mentions(content, path, digest, recovery, line):
    pattern = r"(?<![\w:])([A-Za-z_]\w*(?:::[A-Za-z_]\w*)*)\s*\+\s*(0x[0-9a-f]+)(?![\w])"
    registers = {"eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp", "eip",
                 "rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rsp", "rbp", "rip",
                 "ax", "bx", "cx", "dx", "si", "di", "sp", "bp"}
    rows = []
    seen = set()
    for match in re.finditer(pattern, content, re.I):
        owner = match[1]
        offset = f"0x{int(match[2], 16):X}"
        if owner.casefold() in registers or re.fullmatch(r"r\d+[dwb]?", owner, re.I) or (owner, offset) in seen:
            continue
        seen.add((owner, offset))
        rows.append({
            "id": f"field-mention:{path}:{line}:{owner}:{offset}", "kind": "field_mention",
            "owner_text": owner, "offset": offset, "name": f"{owner} + {offset}",
            "summary": content.strip(), "confidence": "研究文書の局所表記（型・意味・レイアウト未確定）",
            "recovery": recovery,
            "source": {"path": path, "sha256": digest, "start_line": line, "end_line": line}})
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
        reader = csv.DictReader(stream, delimiter="\t")
        previous_line = 1
        for row in reader:
            ledger_start = previous_line + 1
            previous_line = reader.line_num
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
            recovery = {key: row.get(key, "") for key in ("coverage_state", "prior_coverage", "limitations")}
            recovery["ledger"] = {"path": ledger.relative_to(root).as_posix(),
                                  "start_line": ledger_start, "end_line": reader.line_num}
            content = payload.decode("utf-8-sig")
            if source.name == "RUN_RESULT.json":
                mentions.extend(run_records(content, path, digest, recovery))
                continue
            for line, content in enumerate(content.splitlines(), 1):
                if source.suffix.lower() == ".md":
                    mentions.extend(local_field_mentions(content, path, digest, recovery, line))
                for va in sorted({int(match[1], 16) for match in pattern.finditer(content)}):
                    mentions.append({
                        "id": f"mention:{path}:{line}:{va:08X}",
                        "kind": "source_mention", "va": f"0x{va:08X}",
                        "subject": f"va:0x{va:08X}", "name": f"{path}:{line}",
                        "summary": content.strip(),
                        "confidence": "文書内の言及（意味・動作の検証なし）",
                        "recovery": recovery,
                        "source": {"path": path, "sha256": digest,
                                   "start_line": line, "end_line": line}})
    return mentions


def load_citation_registry(root):
    path = root / "reference/sources.json"
    if not path.exists():
        return {}
    registry = json.loads(path.read_text(encoding="utf-8-sig"))
    for name, entry in registry.items():
        relative = Path(entry["path"])
        source = (root / relative).resolve()
        if relative.is_absolute() or not source.is_relative_to(root):
            raise ValueError(f"Citation path escapes repository: {name}")
        if not source.is_file():
            raise ValueError(f"Missing citation source: {name}")
        payload = source.read_bytes()
        if hashlib.sha256(payload).hexdigest().lower() != entry["sha256"].lower():
            raise ValueError(f"Stale citation source checksum: {name}")
        content = payload.decode("utf-8-sig")
        for section, anchor in entry["sections"].items():
            if not isinstance(anchor, str) or not anchor or f'<a id="{anchor}"></a>' not in content:
                raise ValueError(f"Missing citation anchor: {name}§{section}")
    return registry


def recovered_citations(root):
    ledger = root / "research/recovered/RECOVERY_LEDGER.tsv"
    if not ledger.exists():
        return []
    citations = []
    seen = set()
    with ledger.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            label = row.get("source_path", "")
            if not label or (label, row["destination"]) in seen:
                continue
            relative = Path(row["destination"])
            destination = (root / relative).resolve()
            if relative.is_absolute() or not destination.is_relative_to(root):
                raise ValueError(f"Citation path escapes repository: {row['destination']}")
            if not destination.is_file():
                raise ValueError(f"Missing recovered citation source: {row['destination']}")
            if hashlib.sha256(destination.read_bytes()).hexdigest().lower() != row["destination_sha256"].lower():
                raise ValueError(f"Stale recovered citation checksum: {row['destination']}")
            citations.append({"label": label, "path": destination.relative_to(root).as_posix(),
                              "anchor": "", "limitations": row.get("limitations", "")})
            seen.add((label, row["destination"]))
    return citations


def attach_citations(row, registry, recovered=()):
    row["source_links"] = []
    row["unresolved_citations"] = []
    seen = set()
    pattern = r"(?<![\w])([A-Za-z][A-Za-z0-9_]*)(?:§([0-9]+(?:\.[0-9]+)*)|\(§([0-9]+(?:\.[0-9]+)*)\))"
    for match in re.finditer(pattern, row["source"]):
        label = match[0]
        if label in seen:
            continue
        seen.add(label)
        entry = registry.get(match[1], {})
        sections = entry.get("sections", {})
        section = match[2] or match[3]
        anchor = sections.get(section, sections.get(section.split(".")[0]))
        if anchor is None:
            row["unresolved_citations"].append(label)
            continue
        row["source_links"].append({"label": label, "path": entry["path"], "anchor": anchor,
                                    "limitations": entry.get("limitations", "")})
    for citation in recovered:
        pattern = r"(?<![\w./\\-])" + re.escape(citation["label"]) + r"(?![\w./\\-])"
        if re.search(pattern, row["source"]):
            row["source_links"].append(citation)


def validate_source(root, source, identifier):
    if (not isinstance(source, dict)
            or any(not isinstance(source.get(key), str) or not source[key].strip()
                   for key in ("path", "sha256"))
            or not re.fullmatch(r"[0-9a-fA-F]{64}", source["sha256"])):
        raise ValueError(f"Invalid source metadata: {identifier}")
    relative = Path(source["path"])
    evidence = (root / relative).resolve()
    if relative.is_absolute() or not evidence.is_relative_to(root):
        raise ValueError(f"Source path escapes repository: {identifier}")
    if not evidence.is_file():
        raise ValueError(f"Missing source: {source['path']}")
    payload = evidence.read_bytes()
    if hashlib.sha256(payload).hexdigest().lower() != source["sha256"].lower():
        raise ValueError(f"Stale source checksum: {source['path']}")
    count = len(payload.decode("utf-8-sig").splitlines())
    if (any(type(source.get(key)) is not int for key in ("start_line", "end_line"))
            or not 1 <= source["start_line"] <= source["end_line"] <= count):
        raise ValueError(f"Invalid source lines: {identifier}")


def load_corrections(root, endpoints, reserved_ids):
    path = root / "reference/corrections.jsonl"
    corrections = []
    seen = set(reserved_ids)
    required = ("id", "subject", "status", "previous_interpretation", "current_interpretation",
                "summary", "confidence", "target_version")
    for line, content in enumerate(path.read_text(encoding="utf-8-sig").splitlines() if path.exists() else [], 1):
        if not content.strip():
            continue
        item = json.loads(content)
        if (not isinstance(item, dict)
                or any(not isinstance(item.get(key), str) or not item[key].strip() for key in required)):
            raise ValueError(f"corrections.jsonl:{line}: missing required text")
        if item["id"] in seen:
            raise ValueError(f"Duplicate correction ID: {item['id']}")
        if item["subject"] not in endpoints:
            raise ValueError(f"Unknown correction endpoint: {item['id']}")
        if (item["status"] != "corrected" or item["target_version"] not in (
                "ver0.67", "迫真戦記 ver0.67 / Vahren.exe image base 0x400000")):
            raise ValueError(f"Invalid correction status or target version: {item['id']}")
        validate_source(root, item.get("source"), item["id"])
        item["kind"] = "correction"
        corrections.append(item)
        seen.add(item["id"])
    return corrections


def load(root):
    root = Path(root).resolve()
    symbols = table(root, "symbols.tsv", SYMBOL_COLUMNS)
    fields = table(root, "structs.tsv", FIELD_COLUMNS)
    registry = load_citation_registry(root)
    recovered = recovered_citations(root)
    for row in symbols:
        row["id"] = address(row["va"])
    for row in fields:
        row["id"] = f"field:{row['struct']}:0x{int(row['offset'], 16):X}"
    ids = set()
    for row in symbols + fields:
        attach_citations(row, registry, recovered)
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
        validate_source(root, item["source"], item["id"])
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
    source_mentions = load_mentions(root)
    static_calls, static_receipt = load_static_calls(root, symbols)
    corrections = load_corrections(root, {row["id"] for row in symbols + fields}, ids | relation_ids)
    return {"symbols": symbols, "fields": fields, "relations": relations,
            "corrections": corrections,
            "mentions": [row for row in source_mentions if row["kind"] != "field_mention"],
            "field_mentions": [row for row in source_mentions if row["kind"] == "field_mention"],
            "aliases": aliases, "static_calls": static_calls, "static_calls_receipt": static_receipt}


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
    if field:
        field_mentions = [row for row in data["field_mentions"]
                          if row["owner_text"].casefold() == name.casefold()
                          and int(row["offset"], 16) == int(field[2], 16)]
    else:
        field_mentions = [row for row in data["field_mentions"]
                          if needle in json.dumps(row, ensure_ascii=False).casefold()]
    indexed_calls = [row for row in data["static_calls"]
                     if row["subject"] in ids or row["object"] in ids
                     or needle in json.dumps(row, ensure_ascii=False).casefold()]
    corrections = [row for row in data["corrections"]
                   if row["subject"] in ids or needle in json.dumps(row, ensure_ascii=False).casefold()]
    return matched + related + mentions + field_mentions + indexed_calls + corrections


def call_edges(data, query, incoming):
    target = address(query)
    for symbol in data["symbols"]:
        if symbol["name"].casefold() == query.casefold():
            target = symbol["id"]
            break
    endpoint = "object" if incoming else "subject"
    return [row for row in data["static_calls"] if row[endpoint] == target]


def text(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def citation_lines(row):
    lines = []
    for citation in row["source_links"]:
        link = "../../" + quote(citation["path"], safe="/")
        if citation["anchor"]:
            link += "#" + quote(citation["anchor"], safe="")
        lines.append(f"- 出典 [{text(citation['label'])}]({link})。{text(citation['limitations'])}")
    if row["unresolved_citations"]:
        lines.append("- 本文リンク未解決　" + "、".join(row["unresolved_citations"]))
    return lines


def struct_filename(name):
    return quote(name, safe="") + ".md"


def endpoint_link(identifier, labels, prefix="../"):
    parts = identifier.split(":")
    if parts[0] == "va":
        target = f"{prefix}symbols/{int(parts[1], 16):08X}.md"
    else:
        target = prefix + "structs/" + quote(struct_filename(parts[1]), safe="")
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


def correction_lines(corrections, identifier, labels, overview=False):
    rows = [row for row in corrections if identifier is None or row["subject"] == identifier]
    if not rows:
        return []
    lines = ["", "## 訂正履歴", "", "旧解釈は訂正済みの履歴です。現在の意味は辞書と各訂正の確度・対象を確認してください。", ""]
    for row in rows:
        source = row["source"]
        link = ("../" if overview else "../../") + quote(source["path"], safe="/")
        link += f"?plain=1#L{source['start_line']}-L{source['end_line']}"
        endpoint = endpoint_link(row["subject"], labels, prefix="" if overview else "../")
        lines += [f"- {endpoint} · `{text(row['id'])}` · `corrected`。{text(row['summary'])}",
                  f"  - 訂正済みの旧解釈（履歴）　{text(row['previous_interpretation'])}",
                  f"  - → 現在の解釈　{text(row['current_interpretation'])}",
                  f"  - 確度　{text(row['confidence'])}。対象　{text(row['target_version'])}。[訂正の根拠]({link})", ""]
    return lines


def static_call_lines(data, identifier, labels):
    receipt = data["static_calls_receipt"]
    if not receipt or identifier not in {address(value) for value in receipt["selection"]["eligible_endpoint_vas"]}:
        return []
    lines = ["", "## 登録関数間の直接CALL・V9静的索引", "",
             "当時の索引にある採録範囲を表示しています。仮想関数表などの間接呼出しは別の根拠と併せて確認してください。", "",
             "[採録条件・元DB/対象EXEのSHA](../static_calls_source.json)", ""]
    for incoming, title in ((True, "呼び出し元"), (False, "呼び出し先")):
        lines += [f"### {title}", ""]
        grouped = {}
        for row in call_edges(data, identifier, incoming):
            peer = row["subject"] if incoming else row["object"]
            grouped.setdefault(peer, []).append(row)
        if not grouped:
            lines += ["この採録範囲の記録は0件です。", ""]
        for peer, records in sorted(grouped.items()):
            first = min(row["source"]["start_line"] for row in records)
            last = max(row["source"]["end_line"] for row in records)
            proof = f"../static_calls.tsv?plain=1#L{first}-L{last}"
            sites = ", ".join(f"`{row['site_va']}`" for row in records)
            lines += [f"- {endpoint_link(peer, labels)} — {len(records)}箇所。[索引行]({proof})",
                      f"  呼出site　{sites}"]
        lines.append("")
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
                 f"- 辞書の出典表記　{row['source']}"]
        lines += citation_lines(row)
        lines += [f"- [元の辞書行](../../symbols.tsv#L{row['dictionary_line']})", "",
                  "## 関数・メモリとの関係", ""]
        lines += relation_lines(data["relations"], row["id"], labels) or ["関係の個別採録は未実施です。"]
        lines += correction_lines(data["corrections"], row["id"], labels)
        lines += static_call_lines(data, row["id"], labels)
        mentions = [item for item in data["mentions"] if item["subject"] == row["id"]]
        if mentions:
            lines += ["", "## 研究文書での言及", "",
                      "以下は文書内の言及（意味・動作の検証なし）です。文書の限界や訂正も併せて確認してください。", ""]
            context_sources = set()
            for mention in mentions:
                source = mention["source"]
                if source["path"] not in context_sources:
                    recovery = mention["recovery"]
                    ledger = recovery["ledger"]
                    ledger_link = "../../" + quote(ledger["path"], safe="/")
                    ledger_link += f"?plain=1#L{ledger['start_line']}-L{ledger['end_line']}"
                    lines.append(f"- [回収台帳]({ledger_link}) — {text(source['path'])}。"
                                 f"収録状態 {text(recovery['coverage_state'])}。"
                                 f"以前の収録状況 {text(recovery['prior_coverage'])}。"
                                 f"制約・訂正 {text(recovery['limitations'])}")
                    context_sources.add(source["path"])
                link = "../../" + quote(source["path"], safe="/")
                link += f"?plain=1#L{source['start_line']}-L{source['end_line']}"
                lines.append(f"- [{text(mention['name'])}]({link}) — {text(mention['summary'])}")
                if mention["kind"] == "research_run_record":
                    lines.append(f"  取得run `{text(mention['run_id'])}`、Task `{text(mention['related_task'])}`、"
                                 f"記録上の状態 `{text(mention['reported_status'])}`。{text(mention['confidence'])}")
                    for method, metadata in mention["methods"].items():
                        evidence = metadata.get("evidence_id")
                        if evidence:
                            lines.append(f"  - 取得方法 `{text(method)}`、[記録された証拠ID `{text(evidence)}`]({link})")
                    lines += ["", "<details>", "<summary>取得方法の元メタデータ</summary>", "", "```json",
                              json.dumps(mention["methods"], ensure_ascii=False, indent=2), "```", "</details>", ""]
        lines += ["", "[事典の入口](../README.md)", ""]
        files["reference/symbols/" + filename] = "\n".join(lines)
        index.append(f"| {row['va']} | [{text(row['name'])}](symbols/{filename}) | {text(row['kind'])} | {text(row['summary'])} |")
    index += ["", "## 構造体・フィールド", "",
              f"[研究文書の所有者＋オフセット表記](FIELD_MENTIONS.md) — {len(data['field_mentions'])} 件。型や意味の正式登録前の局所表記も検索できます。", ""]
    for name in sorted({row["struct"] for row in data["fields"]}):
        lines = [f"# {name}", "", "<!-- Generated by tools/reference.py. -->", "",
                 "対象は迫真戦記 ver0.67。各フィールドの型・確度・出典は元の辞書から保持しています。", ""]
        lines += relation_lines(data["relations"], f"struct:{name}", labels)
        for row in sorted((item for item in data["fields"] if item["struct"] == name), key=lambda item: int(item["offset"], 16)):
            lines += ["", f"<a id=\"field-{int(row['offset'], 16):x}\"></a>",
                      f"## {row['offset']} {row['name']}", "", row["summary"], "",
                      f"- 型　`{row['type']}`", f"- 辞書の確度　{row['confidence']}",
                      f"- 辞書の出典表記　{row['source']}"]
            lines += citation_lines(row)
            lines += [f"- [元の辞書行](../../structs.tsv#L{row['dictionary_line']})", ""]
            lines += relation_lines(data["relations"], row["id"], labels) or ["読み手・書き手の個別採録は未実施です。"]
            lines += correction_lines(data["corrections"], row["id"], labels)
        lines += ["", "[事典の入口](../README.md)", ""]
        filename = struct_filename(name)
        files["reference/structs/" + filename] = "\n".join(lines)
        index.append(f"- [{text(name)}](structs/{quote(filename, safe='')})")
    index += ["", f"辞書項目 {len(data['symbols'])} 件、フィールド {len(data['fields'])} 件、根拠付き関係 {len(data['relations'])} 件。", ""]
    index += [f"回収済み文書のVA言及・取得記録 {len(data['mentions'])} 件を検索対象に含みます。辞書未登録のVAも検索できます。", ""]
    if data["static_calls_receipt"]:
        index += [f"[登録関数間の直接CALL採録条件](static_calls_source.json) — {len(data['static_calls'])}箇所。"
                  "各関数ページで呼び出し元・先を参照でき、`callers VA --json` / `callees VA --json` でも検索できます。", ""]
    index += [f"[訂正履歴](CORRECTIONS.md) — {len(data['corrections'])} 件。訂正済みの旧解釈と現在の解釈を出典行付きで確認できます。", ""]
    files["reference/README.md"] = "\n".join(index)
    corrections = ["# 訂正履歴", "", "<!-- Generated by tools/reference.py. -->", "",
                   "対象は迫真戦記 ver0.67。旧解釈は歴史的な記録として保持しています。", ""]
    corrections += correction_lines(data["corrections"], None, labels, overview=True) or ["訂正の個別採録は未実施です。", ""]
    corrections += ["[事典の入口](README.md)", ""]
    files["reference/CORRECTIONS.md"] = "\n".join(corrections)
    files.update(render_field_pages(data["field_mentions"]))
    return files



def render_field_pages(mentions):
    files = {}
    index = ["# 研究文書の所有者・オフセット表記", "",
             "<!-- Generated by tools/reference.py. -->", "",
             "所有者名は各報告書内の局所的な表記です。同名でも資料をまたぐ型・意味・レイアウトの同一性は未確定です。", "",
             "所有者とオフセットから詳細ページへ進めます。各ページは最大100表記で、出典行と制約を保持します。", "",
             "| 所有者＋オフセット | 表記数 | 詳細ページ |", "|---|---:|---|"]
    owners = {}
    for mention in mentions:
        owners.setdefault(mention["owner_text"], []).append(mention)
    for owner in sorted(owners, key=lambda value: (value.casefold(), value)):
        rows = sorted(owners[owner], key=lambda row: (int(row["offset"], 16), row["source"]["path"],
                                                    row["source"]["start_line"], row["id"]))
        offsets = {}
        for page_number, position in enumerate(range(0, len(rows), 100), 1):
            chunk = rows[position:position + 100]
            owner_key = hashlib.sha256(owner.encode("utf-8")).hexdigest()[:12]
            filename = f"owner-{quote(owner, safe='')}-{owner_key}-{page_number:03d}.md"
            target = "fields/" + quote(filename, safe="")
            page = [f"# {owner} の局所フィールド表記・{page_number}", "",
                    "<!-- Generated by tools/reference.py. -->", "",
                    "型や意味を確定した構造体辞書とは区別しています。各報告書の文脈と制約を確認してください。", ""]
            last_offset = None
            for mention in chunk:
                offset = mention["offset"]
                if offset != last_offset:
                    page += [f'<a id="field-{int(offset, 16):x}"></a>',
                             f"## {owner} + {offset}", ""]
                    last_offset = offset
                entry = offsets.setdefault(offset, {"count": 0, "pages": []})
                entry["count"] += 1
                link = target + f"#field-{int(offset, 16):x}"
                if link not in entry["pages"]:
                    entry["pages"].append(link)
                source = mention["source"]
                source_link = "../../" + quote(source["path"], safe="/")
                source_link += f"?plain=1#L{source['start_line']}-L{source['end_line']}"
                page += [f"- [{text(source['path'])} 行 {source['start_line']}]({source_link}) — {text(mention['summary'][:160]).rstrip()}",
                         f"  制約・訂正　{text(mention['recovery']['limitations'])}", ""]
            page += ["[所有者＋オフセット索引](../FIELD_MENTIONS.md)", ""]
            files["reference/fields/" + filename] = "\n".join(page)
        for offset, entry in sorted(offsets.items(), key=lambda item: int(item[0], 16)):
            links = " / ".join(f"[{i}]({target})" for i, target in enumerate(entry["pages"], 1))
            index.append(f"| {text(owner)} + {offset} | {entry['count']} | {links} |")
    index += ["", "[事典の入口](README.md)", ""]
    files["reference/FIELD_MENTIONS.md"] = "\n".join(index)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    query = commands.add_parser("search")
    query.add_argument("query")
    query.add_argument("--json", action="store_true")
    for name in ("callers", "callees"):
        query = commands.add_parser(name, help="登録関数間の静的直接CALLを検索")
        query.add_argument("query")
        query.add_argument("--json", action="store_true")
    commands.add_parser("build")
    commands.add_parser("check")
    args = parser.parse_args()
    try:
        data = load(args.root)
        if args.command in ("search", "callers", "callees"):
            matches = (search(data, args.query) if args.command == "search"
                       else call_edges(data, args.query, incoming=args.command == "callers"))
            if args.json:
                print(json.dumps(matches, ensure_ascii=False, indent=2))
            else:
                for row in matches:
                    print(f"{row['id']}  {row.get('name', row.get('predicate', row.get('kind')))}  {row['summary']}  [{row['confidence']}]")
                    if row.get("kind") == "correction":
                        print(f"  訂正済みの旧解釈（履歴） {row['previous_interpretation']}")
                        print(f"  → 現在の解釈 {row['current_interpretation']} / 対象 {row['target_version']}")
                        source = row["source"]
                        print(f"  根拠 {source['path']}:{source['start_line']}-{source['end_line']}")
                    if row.get("kind") == "research_run_record":
                        print(f"  run {row['run_id']} / Task {row['related_task']} / 記録上の状態 {row['reported_status']}")
                        print("  取得方法 " + json.dumps(row["methods"], ensure_ascii=False))
                    if "recovery" in row:
                        recovery = row["recovery"]
                        print(f"  回収状態 {recovery['coverage_state']} / 以前の収録状況 {recovery['prior_coverage']}")
                        print(f"  制約・訂正 {recovery['limitations']}")
            return 0
        files = render(args.root, data)
        stale = []
        for directory in ("reference/symbols", "reference/structs", "reference/fields"):
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
