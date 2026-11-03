"""E/T020 archived original watcher pointer phase audit; source read-only, not Golden."""
import collections
import hashlib
import json
import pathlib
import unittest
from datetime import datetime

BASE = pathlib.Path(__file__).resolve().parents[1] / "rea_lab/headless_analysis/search_index"
SOURCES = {
    "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl":
        ("9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7", 234),
    "BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl":
        ("1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46", 85),
}

def audit(name, pinned_hash, expected_rows):
    raw = (BASE / name).read_bytes()
    assert hashlib.sha256(raw).hexdigest().upper() == pinned_hash, "SOURCE_HASH_CHANGED"
    rows = [json.loads(s) for s in raw.decode("utf-8").splitlines() if s.strip()]
    assert len(rows) == expected_rows, "ROW_COUNT_CHANGED"
    samples = []
    for row in rows:
        state = row.get("state", row.get("initial", row.get("snapshot")))
        if not isinstance(state, dict):
            continue
        ptr = state.get("battlefield_ptr", "0")
        ptr = int(ptr, 16) if isinstance(ptr, str) else int(ptr)
        samples.append((datetime.fromisoformat(row["utc"]), state, ptr, row.get("label"), row.get("kind")))
    active = [t for t, st, ptr, label, kind in samples if st.get("mode") == 2 and st.get("active") == 1]
    assert active, "NO_ACTIVE_OBSERVATION"
    first, last = min(active), max(active)
    counts = collections.Counter()
    examples = {}
    for t, st, ptr, label, kind in samples:
        if st.get("mode") != 1 or st.get("active") != 0:
            continue
        phase = "BEFORE_FIRST_ACTIVE" if t < first else ("AFTER_LAST_ACTIVE" if t > last else "WITHIN_ACTIVE_SAMPLE_SPAN")
        counts[phase + ":all_strategy"] += 1
        if ptr:
            counts[phase + ":ptr_nonzero"] += 1
            examples.setdefault(phase, {"utc": t.isoformat(), "label": label, "kind": kind, "attack_count": st.get("attack_count")})
        if st.get("attack_count", 0) > 0:
            counts[phase + ":attack_positive"] += 1
        if label == "PREPARED_WAR_MAP":
            counts[phase + ":prepared_label"] += 1
    return {"file": name, "sha256": pinned_hash, "rows": len(rows), "first_active_sample": first.isoformat(), "last_active_sample": last.isoformat(), "counts": dict(sorted(counts.items())), "pointer_examples": examples, "classification": "ARCHIVED_OBSERVATION_NOT_GOLDEN"}

class ArchivedPointerLifecycle(unittest.TestCase):
    def test_two_source_byte_pins_and_independent_phases(self):
        for name, (sha, rows) in SOURCES.items():
            with self.subTest(name=name):
                d = audit(name, sha, rows)
                self.assertEqual(d["rows"], rows)
                self.assertEqual(d["classification"], "ARCHIVED_OBSERVATION_NOT_GOLDEN")
                self.assertGreater(sum(v for k,v in d["counts"].items() if k.endswith(":ptr_nonzero")), 0)
                print("PREPOST_AUDIT", json.dumps(d, ensure_ascii=False, sort_keys=True))
    def test_reject_wrong_source_hash(self):
        name, (sha, rows) = next(iter(SOURCES.items()))
        with self.assertRaisesRegex(AssertionError, "SOURCE_HASH_CHANGED"):
            audit(name, "0"*64, rows)
    def test_reject_wrong_row_count(self):
        name, (sha, rows) = next(iter(SOURCES.items()))
        with self.assertRaisesRegex(AssertionError, "ROW_COUNT_CHANGED"):
            audit(name, sha, rows+1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
