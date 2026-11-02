"""E/T020: read-only 2026-10-22 prepatch DAT byte pins; not original Golden proof."""
import argparse
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "KARATE_X20_20261022" / "manifest.json"
HEX64 = re.compile(r"[a-fA-F0-9]{64}\Z")

def valid_hash(value):
    return type(value) is str and HEX64.fullmatch(value) is not None

def classify(expected, actual):
    if not valid_hash(expected):
        return "INVALID_PIN"
    if actual is None:
        return "MISSING"
    if not valid_hash(actual):
        return "INVALID_ACTUAL"
    return "MATCH" if expected.lower() == actual.lower() else "DRIFT"

def safe_relative(value):
    if type(value) is not str or not value:
        return False
    path = Path(value)
    return (not path.is_absolute() and
            not any(x in ("", ".", "..") for x in path.parts) and
            path.suffix.lower() == ".dat")

def epoch_admission(capture_sha, current_sha, process_load_proven):
    if not valid_hash(capture_sha) or not valid_hash(current_sha):
        return "INVALID_SOURCE_PIN"
    if capture_sha.lower() != current_sha.lower():
        return "SOURCE_EPOCH_MISMATCH"
    if process_load_proven is not True:
        return "PROCESS_LOAD_EPOCH_UNVERIFIED"
    return "SOURCE_EPOCH_STATIC_PIN_ONLY_NOT_GOLDEN"

def audit_current():
    manifest_raw = MANIFEST.read_bytes()
    record = json.loads(manifest_raw.decode("utf-8-sig"))
    root = Path(record["root"]) / "a_default" / "script"
    pins = record["all_dat_before"]
    changed = record["changed_files"]
    totals = {"MATCH": 0, "DRIFT": 0, "MISSING": 0,
              "INVALID_PIN": 0, "INVALID_ACTUAL": 0, "UNSAFE_PATH": 0}
    diffs = []
    current_digests = {}
    changed_pin_results = {}
    for name, expected in sorted(pins.items()):
        if not safe_relative(name):
            verdict, actual = "UNSAFE_PATH", None
        else:
            path = root / name
            if path.is_symlink():
                verdict, actual = "UNSAFE_PATH", None
            elif not path.is_file():
                verdict, actual = "MISSING", None
            else:
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                verdict = classify(expected, actual)
        totals[verdict] += 1
        if verdict == "MATCH":
            current_digests[Path(name).as_posix()] = actual
        if verdict != "MATCH":
            diffs.append({"relative_path": name, "reason": verdict,
                          "current_sha256": actual})
        if name in changed:
            patched = changed[name]["after_sha256"]
            changed_pin_results[name] = {
                "baseline": verdict,
                "still_patched": actual is not None and
                valid_hash(patched) and actual.lower() == patched.lower()}
    current_set = {p.relative_to(root).as_posix() for p in root.rglob("*")
                   if p.is_file() and p.suffix.lower() == ".dat"}
    expected_set = {Path(n).as_posix() for n in pins}
    untracked = sorted(current_set - expected_set)
    payload = b"".join(n.encode("utf-8") + bytes([0]) +
                       current_digests[n].encode("ascii") + bytes([10])
                       for n in sorted(current_digests))
    fingerprint = hashlib.sha256(payload).hexdigest()
    prior_fp = "8256A6BFE879A5E2FDC2665B845C3F5D6C8AEF0BF8323E52C4D2E23F507B31B3"
    complete = (totals["MATCH"] == len(pins) and not untracked and
                len(changed_pin_results) == len(changed))
    known_extra = "6000_スキルテスト/work_observation.dat"
    source_set_590 = (len(current_set) == 590 and not untracked and
                      totals["MATCH"] == 590 and totals["MISSING"] == 1 and
                      {Path(x["relative_path"]).as_posix() for x in diffs}
                      == {known_extra} and fingerprint.upper() == prior_fp)
    return {
        "research_id": "E-AUDIT-20261029-10H-T018-T020-DAT-EPOCH-BASELINE-PIN-01",
        "evidence_class": "STATIC_CURRENT_BYTES_VS_20261022_PREPATCH_MANIFEST",
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "claimed_restore_state": record.get("status"),
        "claimed_restore_at": record.get("restored_at"),
        "pin_count": len(pins),
        "modified_file_count": len(changed),
        "counts": totals,
        "current_dat_count": len(current_set),
        "untracked_files": untracked[:25],
        "nonmissing_source_set_sha256": fingerprint,
        "prior_20261025_590_source_set_sha256": prior_fp,
        "matches_prior_590_fingerprint": source_set_590,
        "modified_pins": changed_pin_results,
        "difference_sample": diffs[:25],
        "difference_count": len(diffs),
        "verdict": ("PREPATCH_DAT_BYTE_MATCH_NOT_NATIVE_PROOF" if complete
                    else "CURRENT_590_MATCHES_PRIOR_STATIC_SET_NOT_ARCHIVE_PROOF"
                    if source_set_590 else "DAT_BASELINE_INCOMPLETE_OR_DRIFT_VERIFY"),
        "original_dynamic_observed": 0,
        "actual_golden_pass": 0,
        "strict_match": 0,
        "ready": False,
    }

class SyntheticTests(unittest.TestCase):
    def test_sha_match(self):
        self.assertEqual(classify("a" * 64, "A" * 64), "MATCH")
    def test_sha_drift(self):
        self.assertEqual(classify("a" * 64, "b" * 64), "DRIFT")
    def test_sha_missing(self):
        self.assertEqual(classify("a" * 64, None), "MISSING")
    def test_non_hash(self):
        self.assertEqual(classify(True, "a" * 64), "INVALID_PIN")
    def test_relative_safe(self):
        self.assertTrue(safe_relative("group\\item.dat"))
    def test_relative_escape(self):
        self.assertFalse(safe_relative("..\\elsewhere.dat"))
    def test_absolute_rejected(self):
        self.assertFalse(safe_relative("C:\\outside.dat"))
    def test_non_dat_rejected(self):
        self.assertFalse(safe_relative("sample.exe"))
    def test_epoch_hash_mismatch(self):
        self.assertEqual(epoch_admission("a" * 64, "b" * 64, True), "SOURCE_EPOCH_MISMATCH")
    def test_epoch_process_unknown(self):
        self.assertEqual(epoch_admission("a" * 64, "a" * 64, None), "PROCESS_LOAD_EPOCH_UNVERIFIED")
    def test_epoch_invalid_hash(self):
        self.assertEqual(epoch_admission("fake", "a" * 64, True), "INVALID_SOURCE_PIN")
    def test_epoch_no_golden_promotion(self):
        self.assertEqual(epoch_admission("a" * 64, "a" * 64, True), "SOURCE_EPOCH_STATIC_PIN_ONLY_NOT_GOLDEN")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--save-e-receipt", action="store_true")
    ns = parser.parse_args()
    if ns.audit:
        receipt = audit_current()
        receipt["gate_source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        if ns.save_e_receipt:
            target = ROOT / "tests" / "T020_E_DAT_EPOCH_BASELINE_READBACK_20261029_10H.json"
            target.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n",
                              encoding="utf-8")
        print(json.dumps(receipt, ensure_ascii=True, indent=2))
    else:
        unittest.main(argv=["t020_dat_epoch_gate"], exit=False)

