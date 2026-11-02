"""E/T020 archived capture provenance audit: read-only source files, no native run."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "rea_lab" / "headless_analysis" / "search_index"
EXPECTED_EXE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"

def digest(data):
    return hashlib.sha256(data).hexdigest().upper()

def eligible_summary(obj):
    return (obj.get("origin") == "LIVE_ORIGINAL_READONLY" and
            obj.get("status") == "BATTLE_RETURNED" and
            obj.get("preflight", {}).get("sha256") == EXPECTED_EXE and
            obj.get("full_G1_proven") is False and
            obj.get("external_game_roundtrip_proven") is False and
            obj.get("game_memory_written") is False)

def audit():
    records = []
    errors = []
    sources = sorted(SRC.glob("BATTLE_USER_*_SUMMARY.json"))
    if len(sources) != 7:
        errors.append("summary count changed; manual review required")
    for source in sources:
        raw = source.read_bytes()
        obj = json.loads(raw.decode("utf-8"))
        is_live = eligible_summary(obj)
        is_synthetic = (obj.get("origin", "").startswith("SYNTHETIC_") and
                        obj.get("status") == "SELFTEST_COMPLETE")
        if not (is_live or is_synthetic):
            errors.append(source.name + ": unknown source class")
        listed = obj.get("files", [])
        names = [x["name"] for x in listed]
        if len(names) != len(set(names)):
            errors.append(source.name + ": duplicate receipt names")
        raws = sum("_RAW_" in n for n in names)
        failures = sum("_FAILURE_" in n for n in names)
        if (raws, failures, raws + failures) != (obj.get("structural_captures"),
            obj.get("capture_failures"), obj.get("attempts")):
            errors.append(source.name + ": self-count mismatch")
        if obj.get("full_G1_proven") is not False:
            errors.append(source.name + ": G1 claim changed")
        for item in listed:
            filename = item["name"]
            if Path(filename).name != filename or not filename.startswith(source.name[:-13]):
                errors.append(source.name + ": unexpected receipt path/name " + filename)
                continue
            actual = digest((SRC / filename).read_bytes())
            if actual != item.get("sha256"):
                errors.append(source.name + ": hash mismatch " + filename)
        event_name = obj["event_log"]
        if Path(event_name).name != event_name or not event_name.startswith(source.name[:-13]):
            errors.append(source.name + ": unexpected event log path")
            continue
        event_hash = digest((SRC / event_name).read_bytes())
        records.append(dict(summary=source.name, summary_sha256=digest(raw), origin=obj["origin"],
            class_label="LIVE_SOURCE_CLAIM" if is_live else "SYNTHETIC_SELFTEST",
            raw_count=raws, failure_count=failures, listed_receipts=len(listed),
            event_log=event_name, event_log_sha256=event_hash, full_g1_proven=False))
    return {"research_id":"E-AUDIT-20261029-16H-T020-ARCHIVED-CAPTURE-PROVENANCE-01",
            "classification":"STATIC_ARCHIVED_BYTE_AUDIT_NOT_NATIVE_GOLDEN",
            "records":records,"errors":errors}
class ArchivedCaptureProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()
        cls.rows = cls.result["records"]
        cls.live = [x for x in cls.rows if x["class_label"] == "LIVE_SOURCE_CLAIM"]
        cls.synthetic = [x for x in cls.rows if x["class_label"] == "SYNTHETIC_SELFTEST"]
    def test_01_no_source_integrity_error(self): self.assertEqual(self.result["errors"], [])
    def test_02_all_seven_summaries(self): self.assertEqual(len(self.rows), 7)
    def test_03_live_summary_count(self): self.assertEqual(len(self.live), 3)
    def test_04_synthetic_summary_count(self): self.assertEqual(len(self.synthetic), 4)
    def test_05_live_raw_count(self): self.assertEqual(sum(x["raw_count"] for x in self.live), 8)
    def test_06_live_failure_count(self): self.assertEqual(sum(x["failure_count"] for x in self.live), 5)
    def test_07_synthetic_raw_count(self): self.assertEqual(sum(x["raw_count"] for x in self.synthetic), 4)
    def test_08_pinned_receipt_count(self): self.assertEqual(sum(x["listed_receipts"] for x in self.rows), 20)
    def test_09_event_log_hashes_present(self): self.assertTrue(all(len(x["event_log_sha256"]) == 64 for x in self.rows))
    def test_10_no_g1_golden_claim(self): self.assertTrue(all(x["full_g1_proven"] is False for x in self.rows))
    def test_11_synthetic_not_live(self):
        self.assertFalse(eligible_summary({"origin":"SYNTHETIC_TASK_HOLES_CHILD_WIN32",
           "status":"SELFTEST_COMPLETE", "full_G1_proven":False}))
    def test_12_false_live_origin_not_sufficient(self):
        self.assertFalse(eligible_summary({"origin":"LIVE_ORIGINAL_READONLY",
           "status":"BATTLE_RETURNED","full_G1_proven":False}))

if __name__ == "__main__":
    import sys
    if "--receipt" in sys.argv:
        result = audit()
        result["golden"] = {"dynamic_observed":0,"actual_pass":0,"strict_match":0}
        result["ready_integrations"] = 0
        result["note"] = "Archived summary claims plus source bytes; no new native observation or same-run G1/G2 proof."
        output = Path(__file__).with_name("T020_E_ARCHIVED_CAPTURE_PROVENANCE_RECEIPT_20261029_16H.json")
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("RECEIPT=" + str(output) + " RECORDS=" + str(len(result["records"])) + " ERRORS=" + str(len(result["errors"])))
    else:
        unittest.main(verbosity=2)
