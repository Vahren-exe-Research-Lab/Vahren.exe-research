# E/T020 synthetic acceptance for B-20261031-06H-T011; original gameplay NOT RUN
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ID = "E-AUDIT-20261031-06H-T020-T011-TRAINING-COUNT-GATE-01"
def normalize(power, scenario):
    raw = power if power != 0 else scenario
    return 0 if raw < 0 else 1 if raw == 0 else raw

def predict(power, scenario, path, modifier, eligible):
    if not eligible:
        return {"state": "EARLY_SKIP", "base": None, "count": None, "positive": None}
    base = normalize(power, scenario)
    addition = 0 if path == "NONE" else modifier
    count = base + addition  # bounded synthetic values; native overflow untested
    return {"state": "COUNT_REACHED", "base": base,
            "count": count, "positive": count > 0}

anchors = [
    (-3, 2, "NONE", 0, True, 0),
    (0, 0, "NONE", 0, True, 1),
    (0, 2, "DIRECT", 4, True, 6),
    (2, -3, "TRAINING", -3, True, -1),
    (-3, 2, "DIRECT", 4, True, 4),
    (2, 2, "TRAINING", 4, False, None),
]
for power, scen, path, delta, eligible, expected in anchors:
    assert predict(power, scen, path, delta, eligible)["count"] == expected

cases = []
for power, scenario, path, modifier, eligible in product(
    (-3, 0, 1, 2), (-3, 0, 2), ("NONE", "DIRECT", "TRAINING"), (-3, 0, 4), (False, True)
):
    outcome = predict(power, scenario, path, modifier, eligible)
    if eligible:
        assert outcome["base"] == normalize(power, scenario)
        assert outcome["count"] == outcome["base"] + (0 if path == "NONE" else modifier)
        assert outcome["positive"] is (outcome["count"] > 0)
    else:
        assert outcome == {"state": "EARLY_SKIP", "base": None, "count": None, "positive": None}
    cases.append(dict(power=power, scenario=scenario, path=path,
                      modifier=modifier, eligible=eligible, expected=outcome))
assert len(cases) == 216 and len({(x["power"],x["scenario"],x["path"],x["modifier"],x["eligible"]) for x in cases}) == 216
assert sum(x["expected"]["state"] == "EARLY_SKIP" for x in cases) == 108
assert sum(x["expected"]["positive"] is True for x in cases) > 0
fixture_path = HERE / "T020_E_T011_TRAINING_BRANCH_CASES_20261031_06H.json"
fixture_path.write_text(json.dumps({"research_id": ID, "status": "SYNTHETIC/VERIFY/NOT_READY",
    "source_id": "B-20261031-06H-T011-TRAINING-COUNT-PROVENANCE-01",
    "cases": cases}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
rebuilt = json.loads(fixture_path.read_text(encoding="utf-8"))
assert rebuilt["research_id"] == ID and rebuilt["cases"] == cases
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest().upper()
src = Path(__file__)
b_detail = HERE.parent / "data" / "T011_TRAINING_COUNT_PROVENANCE_NATIVE_20261031_06H.md"
receipt = {"research_id": ID, "fixture_count": len(cases), "anchor_checks": len(anchors),
           "skipped": 108, "eligible_model_cases": 108,
           "source_detail_sha256": sha(b_detail), "runner_sha256": sha(src),
           "fixture_sha256": sha(fixture_path),
           "status": "SYNTHETIC_EXECUTED/STATIC_SOURCE/VERIFY/NOT_READY",
           "dynamic_observed": 0, "actual_golden_pass": 0, "strict_match": 0}
receipt_path = HERE / "T020_E_T011_TRAINING_BRANCH_READBACK_20261031_06H.json"
receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
assert json.loads(receipt_path.read_text(encoding="utf-8")) == receipt
print(json.dumps(receipt, ensure_ascii=False))
