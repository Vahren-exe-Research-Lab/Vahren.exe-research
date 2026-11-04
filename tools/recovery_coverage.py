"""Compare catalog snapshot SHA256 values to reviewed repository text bodies.

Original PC research paths are metadata only and are never opened by this tool.
"""
import argparse
import collections
import csv
import hashlib
import io
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
CATALOG_COLUMNS = ("path", "sha256", "bytes", "lines", "va_mentions", "owner", "tasks", "domain", "research_id")
OUTPUT_COLUMNS = CATALOG_COLUMNS + ("coverage", "destinations")
LEDGERS = (
    "research/recovered/RECOVERY_LEDGER.tsv",
    "research/recovered/exp/EXP_RECOVERY_LEDGER.tsv",
    "research/recovered/dev_evidence/DEV_EVIDENCE_LEDGER.tsv",
)
OUTPUT_TSV = "research/recovered/COVERAGE.tsv"
OUTPUT_MD = "research/recovered/COVERAGE.md"


def repository_file(root, relative):
    path = Path(relative)
    resolved = (root / path).resolve()
    if path.is_absolute() or not resolved.is_relative_to(root):
        raise ValueError(f"Path escapes repository: {relative}")
    if not resolved.is_file() or (root / path).is_symlink():
        raise ValueError(f"Missing or linked repository file: {relative}")
    return resolved


def records(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def inventory(root, tracked_paths):
    root = Path(root).resolve()
    catalog = records(root / "RESEARCH_SOURCE_CATALOG.tsv")
    bodies = collections.defaultdict(set)
    variants = collections.defaultdict(set)
    for relative in sorted(set(tracked_paths) - {OUTPUT_TSV, OUTPUT_MD}):
        path = repository_file(root, relative)
        payload = path.read_bytes()
        if b"\x00" in payload:
            continue
        try:
            payload.decode("utf-8-sig")
        except UnicodeError:
            continue
        bodies[hashlib.sha256(payload).hexdigest()].add(relative)
    for relative in LEDGERS:
        ledger = root / relative
        if not ledger.exists():
            continue
        for row in records(repository_file(root, relative)):
            destination = row["destination"]
            payload = repository_file(root, destination).read_bytes()
            digest = hashlib.sha256(payload).hexdigest()
            if digest != row["destination_sha256"].lower():
                raise ValueError(f"Ledger destination checksum mismatch: {destination}")
            if b"\x00" in payload:
                raise ValueError(f"Recovered body is not text: {destination}")
            payload.decode("utf-8-sig")
            if not row.get("review", "").strip():
                raise ValueError(f"Missing source review: {destination}")
            source_digest = row["source_sha256"].lower()
            bodies[digest].add(destination)
            if digest != source_digest:
                variants[(row["source_path"], source_digest)].add(destination)
    result = []
    for row in catalog:
        if any(column not in row for column in CATALOG_COLUMNS):
            raise ValueError("Catalog is missing required columns")
        digest = row["sha256"].lower()
        exact = bodies.get(digest, set())
        reviewed = variants.get((row["path"], digest), set())
        state = "CATALOG_ONLY_UNRESOLVED"
        if exact:
            state = "EXACT_BODY_AVAILABLE"
        elif reviewed:
            state = "RECOVERED_REVIEWED_VARIANT"
        result.append({**row, "coverage": state, "destinations": ";".join(sorted(exact or reviewed))})
    return result


def render(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=OUTPUT_COLUMNS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    counts = collections.Counter(row["coverage"] for row in rows)
    lines = ["# 研究本文の収録範囲", "",
             "RESEARCH_SOURCE_CATALOG.tsv の既存スナップショットを、Git管理対象のテキスト本文とレビュー済み回収台帳に照合した一覧。",
             "[全行の照合結果](COVERAGE.tsv)から元の相対パス、SHA256、研究ID、保存先を追跡できる。", "",
             "| 状態 | 行数 | 意味 |", "|---|---:|---|",
             f"| EXACT_BODY_AVAILABLE | {counts['EXACT_BODY_AVAILABLE']} | 同じSHA256の本文をリポジトリ内で確認 |",
             f"| RECOVERED_REVIEWED_VARIANT | {counts['RECOVERED_REVIEWED_VARIANT']} | 元SHAと保存版SHAを持つレビュー済み別版を確認 |",
             f"| CATALOG_ONLY_UNRESOLVED | {counts['CATALOG_ONLY_UNRESOLVED']} | 同じ本文やレビュー済み別版の対応を、この検査では確認できていない |", "",
             f"対象は目録の {len(rows)} 行。未解決行にも別名の要約・訂正・出典参照が存在し得る。SHAの文字列が資料中に登場しただけでは本文収録と数えない。",
             "目録のSHAは採録時点の値。研究PCの現在の文書との一致、研究の確かさ、GitHubへの送信完了はこの表だけでは判定しない。",
             "目録作成後に追加された研究や、目録に含まれないファイルの全件把握も別途必要になる。原作素材・保留原資料にはアクセスしない。", "",
             "再生成は `python tools/recovery_coverage.py build`、鮮度確認は `python tools/recovery_coverage.py check`。", ""]
    return {OUTPUT_TSV: stream.getvalue(), OUTPUT_MD: "\n".join(lines)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check"))
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        tracked = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True).stdout.decode("utf-8").split("\0")
        rows = inventory(root, [path for path in tracked if path])
        files = render(rows)
        for relative, content in files.items():
            path = root / relative
            if args.command == "build":
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
            elif not path.is_file() or path.read_text(encoding="utf-8") != content:
                raise ValueError(f"Coverage output is stale: {relative}")
        print(f"{args.command.upper()} PASS ({len(rows)} catalog rows)")
        return 0
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print(f"Coverage error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
