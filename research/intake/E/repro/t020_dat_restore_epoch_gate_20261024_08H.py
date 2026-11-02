from pathlib import Path
from datetime import datetime
import hashlib, json
base = Path(__file__).resolve().parent.parent
source = base / "data" / "KARATE_X20_20261022" / "manifest.json"
g0_file = base / "rea_lab" / "headless_analysis" / "search_index" / "BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json"
m = json.loads(source.read_text(encoding="utf-8-sig"))
g0 = json.loads(g0_file.read_text(encoding="utf-8-sig"))
exe = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
assert m["binary_sha256_before"]["Vahren.exe"].upper() == exe
assert g0["source_original_exe_sha256"] == exe
battle = datetime.fromisoformat(g0["source_event_first_active_utc"])
applied = datetime.fromisoformat(m["applied_at"])
restored = datetime.fromisoformat(m["restored_at"])
assert battle < applied < restored
assert m["status"] == "RESTORED"
folder = Path(m["root"]) / "a_default" / "script"
changed = m["changed_files"]
assert len(changed) == 8
actual = {k: hashlib.sha256((folder/k).read_bytes()).hexdigest() for k in changed}
assert all(actual[k] == v["before_sha256"] for k,v in changed.items())
assert all(actual[k] != v["after_sha256"] for k,v in changed.items())
assert not (Path(m["root"])/"TEST_MOD_KARATE_X20_ACTIVE.md").exists()
all_dat = m["all_dat_before"]
assert len(all_dat) == 591
assert all((folder/k).is_file() and hashlib.sha256((folder/k).read_bytes()).hexdigest() == v for k,v in all_dat.items())
def verdict(c):
    if not c["exe_ok"]: return "EXE_MISMATCH"
    if not c["time_ok"]: return "PROVENANCE_TIME_UNVERIFIED"
    if c["phase"] == "modified": return "X20_MODIFIED_EXCLUDE"
    if c["phase"] == "restored":
        if not c["changed_dat_hashes_ok"]: return "DAT_HASH_CONFLICT"
        if not c["all_dat_pinned"]: return "EIGHT_ONLY_NOT_FULL_DAT_BASELINE"
        return "SOURCE_CANDIDATE_NOT_GOLDEN"
    if c["phase"] == "pre_mod": return "X20_NOT_CAUSAL_BY_TIME_G1G2_PENDING"
    return "UNDETERMINED"
cases = json.loads((Path(__file__).resolve().parent / "T020_DAT_RESTORE_EPOCH_CASES_20261024_08H.json").read_text(encoding="utf-8-sig"))
assert len(cases) == 7 and len({x["id"] for x in cases}) == 7
for case in cases:
    assert verdict(case) == case["expect"], case["id"]
print("MANIFEST_SHA",hashlib.sha256(source.read_bytes()).hexdigest().upper())
print("G0_REPORT_SHA",hashlib.sha256(g0_file.read_bytes()).hexdigest().upper())
print("CURRENT_CHANGED_DAT_BEFORE_HASH_MATCH",len(changed),"/",len(changed))
print("CURRENT_ALL_DAT_BEFORE_HASH_MATCH",len(all_dat),"/",len(all_dat))
print("X20_TIME_PRE_MOD_G0","TRUE","X20_STATUS",m["status"],"NOTICE_ABSENT",True)
print("SYNTHETIC_T020_FIXTURES",len(cases),"/",len(cases),"PASS; GAMEPLAY NOT RUN; GOLDEN PASS 0; STRICT MATCH 0")
