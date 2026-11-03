"""Read-only normalized-source GameClear census with conservative comment gates (STATIC only)."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
spec = json.loads((root / "tests/T020_GAMECLEAR_CENSUS_SCOPE_20261021.json").read_text(encoding="utf-8-sig"))
source_root = root / spec["source_root"]
receipts = []
for rel, positions in spec["expected"].items():
    file = source_root / rel
    raw = file.read_bytes()
    lines = raw.decode("utf-8-sig").splitlines()
    digest = hashlib.sha256(raw).hexdigest().upper()
    assert all(0 < n <= len(lines) and "setGameClear" in lines[n-1] for n in positions), rel
    if rel in spec["sha256"]:
        assert digest == spec["sha256"][rel], rel
    in_block = False
    states = {}
    for n, line in enumerate(lines, 1):
        s = line.lstrip()
        if s.startswith("/*"):
            in_block = True
        kind = ("BLOCK_COMMENT" if in_block else
                "LINE_COMMENT" if s.startswith("//") else
                "SWITCH_DEPENDENT" if s.startswith("/+") else
                "CODE_CANDIDATE")
        if n in positions:
            states[n] = kind
        if in_block and "*/" in s:
            in_block = False
    for n in positions:
        receipts.append(dict(path=rel, line=n, kind=states[n],
                             text=lines[n-1].strip(), source_sha256=digest))
assert len(receipts) == 15
assert len({(r["path"], r["line"]) for r in receipts}) == 15, "duplicate source coordinates"
assert sum(r["path"].endswith(".dat") for r in receipts) == 13
assert sum(r["path"].endswith(".txt") for r in receipts) == 2
assert all(r["kind"] == "CODE_CANDIDATE" for r in receipts), "comment status changed; manual review"
report = dict(id="E-T020-20261021-1749-GAMECLEAR-DIRECTIVE-RECEIPTS-01",
              type="STATIC_NORMALIZED_SOURCE_ONLY", source_exe_sha256=spec["source_exe_sha256"],
              parser_limit="Only leading //, /+, /* and matching */; not engine lexer/execution proof",
              receipts=receipts, gameplay="NOT_RUN", actual_golden_pass=0, strict_match=0)
out = root / "tests/T020_GAMECLEAR_DIRECTIVE_RECEIPTS_20261021_1749.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print("PASS", len(receipts), {k: sum(r["kind"]==k for r in receipts)
                              for k in ("CODE_CANDIDATE","BLOCK_COMMENT","LINE_COMMENT","SWITCH_DEPENDENT")})
print("REPORT", out)
