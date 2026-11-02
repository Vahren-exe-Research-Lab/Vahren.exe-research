# E/T020: original PE byte provenance + independent Win32 API boundary matrix.
# STATIC/API SYNTHETIC ONLY; does not start Vahren.exe or claim gameplay Golden.
from pathlib import Path
from hashlib import sha256
import ctypes
import json
import pefile

ROOT = Path(__file__).resolve().parents[1]
PE = ROOT / 'rea_lab/targets/hakushin067_Vahren.exe'
B_REPORT = ROOT / 'data/T013_RECT_INSET_BOOLEAN_NATIVE_20261031_23H.md'
OUTPUT = ROOT / 'tests/T020_E_T013_RECT_BOOL_WINAPI_CASES_20261031_23H.json'
EXPECTED_PE = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
EXPECTED_B = '356C4A947976A349342CAF1B6819A2E363FCE129E9F1996AC445283B57B321BB'
raw = PE.read_bytes()
assert len(raw) == 2910720 and sha256(raw).hexdigest().upper() == EXPECTED_PE
assert sha256(B_REPORT.read_bytes()).hexdigest().upper() == EXPECTED_B
pe = pefile.PE(data=raw, fast_load=True)
def code(va, size): return pe.get_data(va - pe.OPTIONAL_HEADER.ImageBase, size)
regions = [(0x4C1860,182,'5A87CBE8182C022A3A588F4CF7E9EF99BFC2A4630A75593F24A96F1CDD71B609'),
           (0x4E34E0,27,'ADB8204CE6AF664473D0592988F8FDA1E2E8F1CE01672957C87909058247871B')]
for va, size, digest in regions:
    assert sha256(code(va, size)).hexdigest().upper() == digest, hex(va)
for site, target in [(0x57D994,0x4C1860),(0x57DE95,0x4C1860),(0x4C1899,0x4E34E0)]:
    inst = code(site, 5)
    assert inst[0] == 0xE8 and site + 5 + int.from_bytes(inst[1:], 'little', signed=True) == target
class RECT(ctypes.Structure):
    _fields_ = [('left',ctypes.c_long),('top',ctypes.c_long),
                ('right',ctypes.c_long),('bottom',ctypes.c_long)]
class POINT(ctypes.Structure):
    _fields_ = [('x',ctypes.c_long),('y',ctypes.c_long)]
u = ctypes.WinDLL('user32.dll', use_last_error=True)
u.InflateRect.argtypes = [ctypes.POINTER(RECT),ctypes.c_int,ctypes.c_int]
u.InflateRect.restype = ctypes.c_int
u.PtInRect.argtypes = [ctypes.POINTER(RECT),POINT]
u.PtInRect.restype = ctypes.c_int
cases = []
for margin in (0,100,200,400,600):
    for wi in range(4):
        for hi in range(3):
            w = max(0,2*margin-1) if wi == 0 else 2*margin + (0 if wi==1 else 1 if wi==2 else 201)
            h = max(0,2*margin-1) if hi == 0 else 2*margin + (1 if hi==1 else 201)
            left,top = -740 + wi*5, -380 + hi*9
            right,bottom = left+w, top+h
            L,T,R,B = left+margin,top+margin,right-margin,bottom-margin
            points = [(L-1,T),(L,T),(R-1,B-1),(R,B-1),
                      (L,B),(R,T),(R-1,T),(L,B-1)]
            for x,y in points:
                expected = L <= x < R and T <= y < B
                rect = RECT(left,top,right,bottom)
                if margin: assert u.InflateRect(ctypes.byref(rect),-margin,-margin) != 0
                actual = int(u.PtInRect(ctypes.byref(rect),POINT(x,y))) == 1
                assert actual == expected, (margin,(w,h),(x,y),actual,expected)
                cases.append({'id':f'RECT-{len(cases)+1:04d}','margin':margin,
                              'rect':[left,top,right,bottom],'point':[x,y],
                              'expected':expected,'win32_api_observed':actual,
                              'source':'SYNTHETIC_API_NOT_GAMEPLAY'})
assert len(cases)==480 and len(set(c['id'] for c in cases))==480
OUTPUT.write_text(json.dumps({'research_id':'E-AUDIT-20261031-23H-T020-T013-RECT-INSET-WINAPI-01',
                              'native_pe_sha256':EXPECTED_PE,'cases':cases},
                             ensure_ascii=False,indent=2),encoding='utf-8')
reread=json.loads(OUTPUT.read_text(encoding='utf-8'))
assert len(reread['cases'])==480 and reread['cases']==cases
print('PASS: PE regions 2/2; direct E8 3/3; Win32 API vs half-open oracle 480/480')
print('API_ONLY SYNTHETIC: gameplay DYNAMIC=0 GOLDEN=0 STRICT_MATCH=0 NOT_READY')