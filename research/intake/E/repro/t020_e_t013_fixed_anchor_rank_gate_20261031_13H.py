"""E/T020: original-x86 bounded checks and corrected conditional synthetic rank model.
This never executes the original game; fixture is NOT original gameplay Golden.
"""
from pathlib import Path
from itertools import product
import hashlib
import json
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
OUT = Path(__file__).with_name("T020_E_T013_FIXED_ANCHOR_CASES_20261031_13H.json")
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
SENTINEL, FLOOR = -2147483640, -2147483547
WINDOWS = [
    (0x447240, 0x44727A, "A69CBAFBFE589DA7988FB807B026B8CACC7D30E9FA9FF007DC1B10B9FF72F331"),
    (0x44926E, 0x4492DF, "3CF44C9137C3B786C69EDA6367EBFD4674A02C40F3971FDC882C082DFBA7EF06"),
    (0x47BB50, 0x47BC52, "6FF853BA3CCFC24065C59060A65C06E441D4BFC901ED089D8AAE140D0815B949"),
    (0x44D6A0, 0x44D770, "904577096C9D036CCF8755426C8E578CF5B372A982737BAEDF0706AFDFF52162"),
    (0x449296, 0x4492CE, "6B0A84C91E31C0A6388411738647EF2403D21AE7B0D9E108E96AEF7E82706B09"),
    (0x44926E, 0x44927F, "7FA3785ADE35BD13730661181AD2AEDB888C833D1E23EEAC6843C3CED0711C88"),
]

def rank_steps(scores):
    anchor, rank, steps = SENTINEL, 10000, []
    for score in scores:
        if anchor == SENTINEL:
            anchor = score
        if score != anchor:
            rank -= 1
        steps.append({"score": score, "anchor": anchor, "counter": rank,
                      "stored": rank if score > FLOOR else None})
    return steps

def legacy_prev_steps(scores):
    prev, rank, results = None, 10000, []
    for score in scores:
        if prev is not None and score != prev:
            rank -= 1
        prev = score
        results.append(rank)
    return results

def main():
    original = TARGET.read_bytes()
    assert hashlib.sha256(original).hexdigest().upper() == EXE_SHA
    pe = pefile.PE(data=original, fast_load=True)
    imagebase = pe.OPTIONAL_HEADER.ImageBase
    for start, end, expected in WINDOWS:
        native = pe.get_data(start - imagebase, end - start)
        assert len(native) == end - start
        assert hashlib.sha256(native).hexdigest().upper() == expected, hex(start)
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    for site, dest in ((0x449276, 0x47BB50), (0x47BBF6, 0x44D6A0),
                       (0x47BB83, 0x47BCC0)):
        decoded = list(decoder.disasm(pe.get_data(site - imagebase, 5), site))
        assert len(decoded) == 1 and decoded[0].mnemonic == "call", hex(site)
        assert int(decoded[0].op_str, 16) == dest, hex(site)
    values = (-2147483648, SENTINEL, FLOOR - 1, FLOOR, FLOOR + 1,
              -1, 0, 8, 20, 2147483647)
    fixtures, comparisons = [], 0
    for mode in (0, 1, 2, 3):
        for triple in product(values, repeat=3):
            records = [{"a0c": x if mode == 2 else 777,
                        "a10": x if mode != 2 else -777} for x in triple]
            scores = [r["a0c" if mode == 2 else "a10"] for r in records]
            assert scores == list(triple)
            steps = rank_steps(scores)
            assert all(step["stored"] is None if x <= FLOOR
                       else step["stored"] == step["counter"]
                       for x, step in zip(scores, steps))
            if scores[0] != SENTINEL:
                independent = [10000 - sum(x != scores[0] for x in scores[:i+1])
                               for i in range(len(scores))]
                assert [x["counter"] for x in steps] == independent
            if [x["counter"] for x in steps] != legacy_prev_steps(scores):
                comparisons += 1
            fixtures.append({"mode": mode, "input_ordered_scores": list(scores),
                             "counter": [x["counter"] for x in steps],
                             "stored": [x["stored"] for x in steps]})
    anchors = [
        ([20, 20, 8, 8], [10000, 10000, 9999, 9998]),
        ([20, 8, 8, 8], [10000, 9999, 9998, 9997]),
        ([20, 20, 20], [10000, 10000, 10000]),
        ([SENTINEL, 20, 20], [10000, 10000, 10000]),
        ([SENTINEL, SENTINEL, 7, 7], [10000, 10000, 10000, 10000]),
        ([20, FLOOR, FLOOR], [10000, 9999, 9998]),
        ([20, FLOOR + 1, FLOOR + 1], [10000, 9999, 9998]),
        ([20, -2147483648, -2147483648], [10000, 9999, 9998]),
    ]
    for mode in (0, 1, 2, 3):
        for scores, expected in anchors:
            steps = rank_steps(scores)
            assert [s["counter"] for s in steps] == expected
            fixtures.append({"mode": mode, "anchor_case": scores,
                             "counter": expected, "stored": [s["stored"] for s in steps]})
    payload = {
        "research_id": "E-AUDIT-20261031-13H-T020-T013-FIXED-ANCHOR-CORRECTION-01",
        "owner": "E/T020", "status": "STATIC/CONDITIONAL_SYNTHETIC/VERIFY/NOT_READY",
        "source_owner_id": "B-20261031-13H-T013-SORT-ANCHOR-TIE-CORRECTION-01",
        "source_pe_sha256": EXE_SHA, "native_windows_verified": len(WINDOWS),
        "native_calls_verified": 3, "synthetic_pass": len(fixtures),
        "counterexamples_to_previous_group_rule": comparisons,
        "original_game_dynamic_observed": 0, "actual_golden_pass": 0,
        "strict_match": 0, "fixtures": fixtures,
        "limits": "Rank transform on supplied ordered-score list only. No original game execution; no proof of 33+ sort stability, final target or valid candidate reachability."
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":"))+"\n", encoding="utf-8")
    actual = OUT.read_bytes()
    assert json.loads(actual.decode("utf-8"))["synthetic_pass"] == len(fixtures)
    print(json.dumps({"native_pe_sha_match": True, "window_pass": len(WINDOWS),
                      "call_pass": 3, "synthetic_pass": len(fixtures),
                      "prev_group_rule_counterexamples": comparisons,
                      "fixture_sha256": hashlib.sha256(actual).hexdigest().upper(),
                      "fixture_bytes": len(actual), "golden": 0}, ensure_ascii=True))

if __name__ == "__main__":
    main()
