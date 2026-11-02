"""E/T020 non-destructive inventory: 2026-10-25..27 PC artifact bytes + prior Library pins."""
from pathlib import Path
import hashlib, json, re
from collections import Counter
BASE = Path(__file__).resolve().parent
OUT = BASE / "T020_E_PC_20261025_27_BYTE_INVENTORY_20261029_05H.json"
SOURCE = BASE / "E_OFFLINE_SYNC_20261029" / "T020_E_LIBRARY_SOURCE_MANIFEST_20261029_04H.json"
STAGING = BASE / "E_OFFLINE_SYNC_20261029"
PIN_NAME = "T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149_LIBPIN_7D574F25.json"
VALID_PREFIX = ("T018_", "T020_", "t020_")
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def main():
    candidates = sorted((p for p in BASE.iterdir() if p.is_file() and
        p.name.startswith(VALID_PREFIX) and re.search(r"2026102[567](?!\d)", p.name)), key=lambda p: p.name)
    items, json_errors = [], []
    for p in candidates:
        raw = p.read_bytes()
        row = {"file": p.name, "sha256": hashlib.sha256(raw).hexdigest().upper(), "bytes": len(raw),
               "date_tag": re.search(r"2026102[567]", p.name).group(0)}
        if p.suffix.lower() == ".json":
            try: json.loads(raw); row["json_parse"] = "PASS"
            except (ValueError, UnicodeError) as e:
                row["json_parse"] = "REVIEW"; json_errors.append({"file": p.name, "error": type(e).__name__})
        items.append(row)
    src = json.loads(SOURCE.read_bytes())["items"]
    checked = []
    for r in src:
        q = STAGING / r["name"]
        ok = q.is_file() and q.stat().st_size == r["bytes"] and digest(q) == r["sha256"]
        checked.append({"name": r["name"], "identical_original_name": ok})
    pin = STAGING / PIN_NAME
    pin_hash = digest(pin) if pin.is_file() else None
    pin_match = pin_hash == "7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA"
    dates = dict(sorted(Counter(x["date_tag"] for x in items).items()))
    doc = {"research_id": "E-AUDIT-20261029-05H-T020-PC-SOURCE-INVENTORY-01",
           "status": "STATIC_BYTES / VERIFY / NOT READY",
           "scope": "PC top-level tests: T018/T020/t020 date-tag 20261025..27",
           "items": items, "invalid_json": json_errors,
           "previous_library_source_count": len(checked),
           "previous_library_original_name_matches": sum(x["identical_original_name"] for x in checked),
           "previous_library_name_mismatches": [x["name"] for x in checked if not x["identical_original_name"]],
           "canonical_alias_sha256": pin_hash, "canonical_alias_match": pin_match}
    payload = (json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if OUT.exists():
        assert OUT.read_bytes() == payload, "EXISTING_MANIFEST_DIFF; manual review required"
    else:
        with OUT.open("xb") as stream: stream.write(payload)
    assert OUT.read_bytes() == payload, "READBACK_FAILED"
    print(json.dumps({"file_count": len(items), "dates": dates, "json_parse_review": json_errors,
                      "source_original_name_matches": doc["previous_library_original_name_matches"],
                      "source_original_name_mismatches": doc["previous_library_name_mismatches"],
                      "canonical_alias_match": pin_match, "manifest_sha256": digest(OUT),
                      "manifest_bytes": len(payload)}, ensure_ascii=False))
if __name__ == "__main__": main()
