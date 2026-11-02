#!/usr/bin/env python3
"""E T020: only synthetic routing/provenance tests; never game Golden."""
import json
import sys
from pathlib import Path

def verdict(c):
    if c.get("dual_commit"): return "BLOCK_DOUBLE_COMMIT"
    if c.get("cross_window"): return "BLOCK_CROSS_WINDOW"
    if c.get("claim_golden") and not c.get("witness_complete"): return "BLOCK_PROOF_PROMOTION"
    if not c.get("process_epoch_verified", True): return "VERIFY_PROCESS_EPOCH"
    if c["family"] != "fastsim": return "VERIFY_NON_FASTSIM_ROUTE"
    rc = c.get("return_code")
    if c.get("cause") == "loop_limit500" and rc != 0: return "BLOCK_500_LIMIT_CONFLICT"
    if rc == 0:
        return "BLOCK_FALSE_FINISH" if c.get("claim_native_finish") else "STATIC_RETURN0_D220_NO_FINISH"
    if rc in (1, 2):
        expected_bool = (rc == 1)
        if c.get("claim_native_finish") is False: return "BLOCK_MISSING_FINISH"
        if c.get("claimed_finish_bool") is not None and c["claimed_finish_bool"] != expected_bool:
            return "BLOCK_BOOL_CONFLICT"
        return "STATIC_FINISH_BOOL1_MEANING_VERIFY" if expected_bool else "STATIC_FINISH_BOOL0_MEANING_VERIFY"
    return "VERIFY_UNKNOWN_CODE"

def main(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    assert doc["evidence_class"] == "SYNTHETIC_NEGATIVE_FIXTURES_NOT_GAMEPLAY"
    cases = doc["cases"]; assert len({c["id"] for c in cases}) == len(cases)
    mismatches = [{"id":c["id"],"expected":c["expected"],"actual":verdict(c)}
                  for c in cases if verdict(c) != c["expected"]]
    print(json.dumps({"total":len(cases),"passed":len(cases)-len(mismatches),
                      "failed":len(mismatches),"mismatches":mismatches,
                      "gameplay":"NOT_RUN","actual_golden_pass":0,"strict_match":0},ensure_ascii=False))
    return 1 if mismatches else 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_suffix(".json"))))
