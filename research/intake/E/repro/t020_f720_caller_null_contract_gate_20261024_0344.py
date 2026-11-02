"""E T020 synthetic guard. Does not execute the original game or assert a crash."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REA = ROOT / "rea_lab" / "decomp_task"
HERE = Path(__file__).resolve().parent
STEM = "REA_20261024_03H_P0_F720_CALLER_NULL_CONTRACT_"
RESEARCH = {
    "STATIC.md": "DABA032A4DB9821DEE5DE5BA92E9BB3BE7BAE87EEC888B264FB02A0438153EA3",
    "EVIDENCE.json": "78F8B1FCA145FD33552AD68F09A0FF2D23FE8CA71484ED539BDECC9D35B4911C",
}
CASES = HERE / "T020_F720_CALLER_NULL_CONTRACT_CASES_20261024_0344.json"
EXPECTED_SOURCE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
SITES = {"0x40F393", "0x434EF3", "0x48FBD9", "0x4901C1", "0x4905F2", "0x49381E", "0x4F66ED"}
DIRECT_UNGUARDED = {"0x40F393", "0x48FBD9", "0x4F66ED"}
MODE_GATED = {"0x4905F2", "0x49381E"}

def classify(c: dict) -> str:
    site, ret = c["site"], c["synthetic_return_value"]
    if c.get("claim_crash"):
        return "REJECT_CRASH_CLAIM"
    if c.get("claim_g2"):
        return "REJECT_G2_CLAIM"
    if c.get("claim_executed"):
        return "REJECT_OBSERVED_CLAIM"
    if ret is None:
        return "RETURN_VALUE_UNOBSERVED"
    if site == "0x434EF3":
        return "DOWNSTREAM_NOT_FULLY_AUDITED"
    if site == "0x4901C1":
        return "STATIC_NULL_SKIP_IF_REACHED" if ret == 0 else "STATIC_NONNULL_BRANCH"
    if site in MODE_GATED and ret == 0:
        return "MODE_GATE_NOT_NULL_GUARD"
    if ret == 0 and site in DIRECT_UNGUARDED:
        return "STATIC_NULL_FLOW_RISK_NOT_CRASH"
    return "NONNULL_PATH_NOT_GOLDEN"

def main() -> None:
    for suffix, expected in RESEARCH.items():
        actual = hashlib.sha256((REA / (STEM + suffix)).read_bytes()).hexdigest().upper()
        assert actual == expected, f"REA receipt changed: {suffix}"
    evidence = json.loads((REA / (STEM + "EVIDENCE.json")).read_text(encoding="utf-8"))
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    assert cases["source_id"] == evidence["research_id"]
    assert cases["source_sha256"] == evidence["source"]["sha256"] == EXPECTED_SOURCE
    assert set(evidence["direct_callers"]) == SITES
    assert evidence["verification"]["selected_machine_bytes_pass"] == 24
    assert evidence["verification"]["rel32_targets_pass"] == 9
    assert evidence["verification"]["game_executed"] is False
    assert evidence["state"] == "STATIC_VERIFY_NOT_READY"
    rows, seen = cases["cases"], set()
    for row in rows:
        assert row["case_id"] not in seen
        seen.add(row["case_id"])
        assert row["site"] in SITES and row["synthetic_return_value"] in (None, 0, 2, 7, 8, 9)
        observed = classify(row)
        assert observed == row["expected"], (row["case_id"], observed, row["expected"])
    assert len(rows) == 20
    print(f"PASS source_SHA_2/2; caller_sites={len(SITES)}/7; synthetic={len(rows)}/20")
    print("STATUS STATIC_RECEIPT_VERIFIED / SYNTHETIC_ONLY / GAME_NOT_RUN / GOLDEN_0 / STRICT_0 / NOT_READY")

if __name__ == "__main__":
    main()
