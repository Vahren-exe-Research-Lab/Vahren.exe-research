"""E/T020: archived pointer identity across observed mode epochs; NOT Golden."""
import hashlib
import json
import pathlib
import unittest

BASE = pathlib.Path(__file__).resolve().parents[1] / "rea_lab/headless_analysis/search_index"
PIN = {
    "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl":
        ("9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7", 234),
    "BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl":
        ("1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46", 85),
}

def summarize(name, expected_sha, expected_rows):
    raw = (BASE / name).read_bytes()
    if hashlib.sha256(raw).hexdigest().upper() != expected_sha:
        raise AssertionError("SOURCE_SHA_MISMATCH")
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    if len(rows) != expected_rows:
        raise AssertionError("ROW_COUNT_MISMATCH")
    states = [(r["utc"], r.get("state", r.get("initial", r.get("snapshot"))))
              for r in rows]
    states = [(t, s) for t, s in states if isinstance(s, dict)]
    active = [(t, s) for t, s in states if s.get("mode") == 2 and s.get("active") == 1]
    if not active:
        raise AssertionError("NO_ACTIVE_SAMPLE")
    first, last = active[0][0], active[-1][0]
    active_ptrs = {s["battlefield_ptr"] for _, s in active}
    if len(active_ptrs) != 1:
        raise AssertionError("ACTIVE_POINTER_NOT_SINGLETON")
    ptr = next(iter(active_ptrs))
    strategy = lambda s: s.get("mode") == 1 and s.get("active") == 0
    pre = [(t, s) for t, s in states if t < first and strategy(s)]
    post = [(t, s) for t, s in states if t > last and strategy(s)]
    changes = [(t, prev["battlefield_ptr"], cur["battlefield_ptr"], cur["mode"], cur["active"])
               for (old_t, prev), (t, cur) in zip(states, states[1:])
               if prev["battlefield_ptr"] != cur["battlefield_ptr"]]
    result = {
        "rows": len(rows), "active_ptr": ptr, "active_samples": len(active),
        "pre_strategy": len(pre), "pre_same_ptr": sum(s["battlefield_ptr"] == ptr for _, s in pre),
        "post_strategy": len(post), "post_same_ptr": sum(s["battlefield_ptr"] == ptr for _, s in post),
        "pre_unique_ptrs": len({s["battlefield_ptr"] for _, s in pre}),
        "pointer_changes": len(changes),
        "changes_outside_pre_strategy": sum(t >= first or mode != 1 or on != 0
                                            for t, old, new, mode, on in changes),
        "first_pre_same_ptr_utc": next((t for t, s in pre if s["battlefield_ptr"] == ptr), None),
        "verdict": "VERIFY_NOT_GOLDEN",
    }
    return result

class EpochIdentityRegression(unittest.TestCase):
    def source(self, index):
        name, (sha, n) = list(PIN.items())[index]
        return summarize(name, sha, n)

    def test_watch1_pointer_epoch_reuse(self):
        d = self.source(0)
        self.assertEqual((25, 1, 104, 20, 19, 0),
            (d["active_samples"], d["pre_same_ptr"], d["post_same_ptr"],
             d["pre_unique_ptrs"], d["pointer_changes"], d["changes_outside_pre_strategy"]))

    def test_watch2_pointer_epoch_reuse(self):
        d = self.source(1)
        self.assertEqual((35, 2, 4, 2, 1, 0),
            (d["active_samples"], d["pre_same_ptr"], d["post_same_ptr"],
             d["pre_unique_ptrs"], d["pointer_changes"], d["changes_outside_pre_strategy"]))

    def test_identity_not_golden(self):
        for i in range(2):
            d = self.source(i)
            self.assertEqual("VERIFY_NOT_GOLDEN", d["verdict"])
            self.assertGreater(d["pre_same_ptr"], 0)
            self.assertEqual(d["post_strategy"], d["post_same_ptr"])
            print("EPOCH_IDENTITY", i, json.dumps(d, sort_keys=True))

    def test_reject_bad_source_sha(self):
        name, (_, n) = next(iter(PIN.items()))
        with self.assertRaisesRegex(AssertionError, "SOURCE_SHA_MISMATCH"):
            summarize(name, "0" * 64, n)

    def test_reject_bad_row_count(self):
        name, (sha, n) = next(iter(PIN.items()))
        with self.assertRaisesRegex(AssertionError, "ROW_COUNT_MISMATCH"):
            summarize(name, sha, n + 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)