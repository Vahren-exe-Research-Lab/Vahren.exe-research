# E T020: synthetic-only selector/path check; no native gameplay or PC mutations.
import json
from pathlib import Path

def classify(c):
    m1, m2, flag, selector, ret = (c[k] for k in ("modeL","modeR","flag19c","selector","ret"))
    if ret is not None and (m1 is False or m2 is False or flag == 0 or
                            (m1 is True and m2 is True and flag is not None and selector not in (None,0))):
        return "CONFLICT_NONEXEC_RESULT"
    if m1 is None or m2 is None:
        return "VERIFY_MODE"
    if m1 is False or m2 is False:
        return "MODE_RECOVERY_452FF0"
    if flag is None:
        return "VERIFY_FLAG"
    if flag == 0:
        return "EARLY_RETURN_NO_SIM"
    if selector is None:
        return "VERIFY_SELECTOR"
    if selector != 0:
        return "VM_BRANCH_NO_SIM"
    return {0:"DRAW_REQUEST_NOT_G3",1:"FINISH_BOOL_TRUE_NOT_G3",
            2:"FINISH_BOOL_FALSE_NOT_G3",None:"VERIFY_RET"}.get(ret,"VERIFY_UNKNOWN_RET")

def main():
    p = Path(__file__).with_name("T020_FASTSIM_SELECTOR_PRIORITY_CASES_20261023_1952.json")
    j = json.loads(p.read_text(encoding="utf-8"))
    ids = [x["case_id"] for x in j["cases"]]
    assert len(ids) == len(set(ids)), "duplicate cases"
    failures = [(x["case_id"], classify(x), x["expected"]) for x in j["cases"] if classify(x) != x["expected"]]
    print(json.dumps({"id":j["id"],"total":len(ids),"pass":len(ids)-len(failures),"fail":failures,"tier":j["tier"]},ensure_ascii=False))
    assert not failures
if __name__ == "__main__":
    main()
