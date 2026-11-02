"""E/T020: bounded native receipts + conditional RNG score boundary regression."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
import pefile

root = Path(__file__).resolve().parents[1]
raw = (root / "rea_lab/targets/hakushin067_Vahren.exe").read_bytes()
exe_sha = sha256(raw).hexdigest().upper()
assert exe_sha == "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
b_detail = root / "data/T013_CANDIDATE_A14_PER_NODE_RANDOM_SCORE_NATIVE_20261031_19H.md"
b_sha = sha256(b_detail.read_bytes()).hexdigest().upper()
assert b_sha == "01AF13E11C52A77B5D32ECEF86FE5C40FE6B019E07D853B822B04D2349168A84"
pe = pefile.PE(data=raw, fast_load=True)
imagebase = pe.OPTIONAL_HEADER.ImageBase
windows = (
    ("other_caller", 0x577AA7, 0x577AD8, "B90E42188B88AA6FA2830CE5763E959A99CBE7F9BA7FD67C2D99966E1AE47246"),
    ("kind8_caller", 0x577D2D, 0x577D74, "15CFD4B0AF840D29F141E14429ECE32537CE9DCA18490D01A7ADCA28397B5315"),
    ("a14_writer", 0x57A7D0, 0x57A826, "2C7437ADEE9FED5EF3D3E798F6567FEB237391661EDAD33B4B7ACB35E0BBFFC8"),
    ("comparator", 0x5A3EA0, 0x5A3F14, "3B4F8BAD40BC85B76D885783D3B62D8DDC1DC20E484378E9EFB6A6E87BDA5912"),
)
for name, start, stop, digest in windows:
    assert sha256(pe.get_data(start-imagebase, stop-start)).hexdigest().upper() == digest, name
calls = ((0x577AA7, 0x57A7D0), (0x577D47, 0x57A7D0),
         (0x57A7E3, 0x5B6EAB), (0x57A7FC, 0x5D1B80))
for site, target in calls:
    b = pe.get_data(site-imagebase, 5)
    assert b[0] == 0xE8 and site+5+int.from_bytes(b[1:], "little", signed=True) == target, hex(site)
hist = Counter()
for r in range(32768):
    value = -4 - int(r * (-8.0/32768.0))  # hypothesis: ftol truncates toward zero
    assert value == (r // 4096) - 4
    hist[value] += 1
assert set(hist) == set(range(-4, 4)) and set(hist.values()) == {4096}
threshold = -2147483547  # signed interpretation of 0x80000065
score_pairs = ((-2147483648,-2147483648),(-2147483548,-2147483546),
               (-2147483547,-2147483547),(-2147483546,-2147483548),
               (-1,1),(0,0),(9,-9),(2147483647,2147483646))
rpoints = (0,4095,4096,8191,8192,16383,16384,32767)
cases = []
for mode in (0, 1, 2):
    for primary, secondary in score_pairs:
        for raw_rng in rpoints:
            base = primary if mode == 2 else secondary
            jitter = (raw_rng // 4096) - 4
            enabled = base > threshold
            signed32 = lambda n: ((n + 2**31) % 2**32) - 2**31
            score = signed32(base + jitter) if enabled else base
            cases.append(dict(mode=mode, base_a0c=primary, base_a10=secondary,
                              raw_rng=raw_rng, expected_a14=jitter,
                              a14_gate=enabled, expected_score=score))
draw_cases = [dict(node_count=n, expected_draws=n, comparator_result="NOT_OBSERVED")
              for n in (0,1,2,26)]
assert len(cases) == 192 and len(draw_cases) == 4
result = dict(research_id="E-AUDIT-20261031-19H-T020-T013-A14-DRAW-BOUNDARY-01",
              evidence="STATIC SOURCE SHA ONLY + CONDITIONAL SYNTHETIC MODEL",
              status="VERIFY / NOT READY / GOLDEN_NOT_RUN",
              exe_sha256=exe_sha, b_detail_sha256=b_sha,
              windows_verified=len(windows), e8_sites_verified=len(calls),
              raw_values_checked=32768, a14_histogram=dict(sorted(hist.items())),
              conditional_score_cases=cases, conditional_draw_cases=draw_cases,
              actual_gameplay_dynamic_observed=0, actual_golden_pass=0, strict_match=0)
dest = root / "tests/T020_E_T013_A14_RNG_BOUNDARY_CASES_20261031_19H.json"
dest.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
assert json.loads(dest.read_text(encoding="utf-8"))["raw_values_checked"] == 32768
print("PASS STATIC 4/4 SHA 4/4 E8; SYNTHETIC 32768/32768 RAW + 192 SCORE + 4 DRAW; GOLDEN 0")
