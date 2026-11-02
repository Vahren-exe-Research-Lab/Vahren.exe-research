"""E T020 standalone static branch-fixture checker, not original gameplay."""
import json
from pathlib import Path

FIXTURE = "T020_FASTSIM_NONZERO_TAIL_FIXTURES_20261023_2052.json"

def classify(case):
    ret = case["sim_return"]
    flag = case["flag_1ef175"]
    base = {"finish_bool": None, "call_48eee0": None, "golden_pass": False}
    if ret is not None and (type(ret) is not int or not -(2**31) <= ret < 2**31):
        return dict(base, route="INVALID_TYPE")
    if flag is not None and (type(flag) is not int or not 0 <= flag <= 255):
        return dict(base, route="INVALID_TYPE")
    if ret is None:
        return dict(base, route="VERIFY_RET")
    if ret == 0:
        return dict(base, route="DRAW_ONLY", call_48eee0=False)
    return dict(base,
                route="FINISH_EXPECTED" if ret in (1, 2) else "FINISH_UNEXPECTED_RET",
                finish_bool=(ret == 1), call_48eee0=None if flag is None else flag == 0)
def run():
    obj = json.loads(Path(__file__).with_name(FIXTURE).read_text(encoding="utf-8"))
    cases = obj["cases"]
    ids = [x["case_id"] for x in cases]
    assert len(ids) == len(set(ids)), "duplicate fixture case ids"
    failures = [{"id":x["case_id"],"got":classify(x),"expected":x["expected"]}
                for x in cases if classify(x) != x["expected"]]
    result = {"id":obj["study_id"], "total":len(cases),
              "passed":len(cases)-len(failures), "failed":failures,
              "tier":obj["tier"], "native_gameplay_pass":0, "strict_match":0}
    print(json.dumps(result, ensure_ascii=False))
    if failures:
        raise SystemExit(1)

if __name__ == "__main__":
    run()
