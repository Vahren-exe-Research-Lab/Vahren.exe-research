# E-AUDIT-20261031-09H-T020-T011-BULK-ERASE-BOUNDARY-01 — full vs partial range erase boundary

- **Upstream ID:** `B-20261031-09H-T011-TRAINING-CACHE-BULK-ERASE-NATIVE-01` (B owner; **do not duplicate discovery**).
- **E source:** `tests/T020_E_T011_BULK_ERASE_ACCEPTANCE_20261031_09H.md`; SHA256 verified 2026-11-01 `97C6FF82814759FE26980B65B88144BAB27D5CA1001B5137F484E618D7DD7DCC`.
- **B source:** `data/T011_TRAINING_CACHE_FULL_RANGE_ERASE_NATIVE_20261031_09H.md`; SHA256 verified 2026-11-01 `C54054A10AE7834D10DAA45129B80100048CD98CDAE286324C91E9F784DF24AC`. Upstream report is referenced, not reproduced.
- **Source snapshot:** 2026-10-31 (JST), private PC read-only source recheck 2026-11-01 23:52 JST.
- **Owner / task:** E / T020, T018-T019 cross-check. Upstream owner B/T011 or B/T013 as separately identified; not a new B native finding.
- **Engine basis:** previously authenticated read-only PE copy, original SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. This run independently rehashed the E and B report files, **not** the original PE or native windows.
- **Evidence class:** historical STATIC byte attestations and conditional SYNTHETIC regression; INFERRED native semantics require follow-up. Gameplay DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0; official READY=0.
- **Legal Golden gate:** unchanged old EXE and authenticated pre-karate-20x DAT, same-run G0 normal battle UI, G1 immediate prebattle SAVE bytes/SHA plus input timeline, G2 real MAP SHA and three sides plus ordered deployed Unit/Troop; G3 visible outcome and G4 World change. None acquired here.
- **Original source controls:** no original EXE/DAT/MAP/SAVE/ZIP, runtime screenshots, generated DB, or other owner's full report included. No forbidden/refused research payload reattempted. `PUBLISHED_INTAKE / NOT_CURATED` applies to this E-specific cross-check, and does not reverse any independently curated B native entry.

## E-owned result (historical evidence; no new test run)
T020 acceptance split: full-range begin==head.leftmost and end==head proceeds via 0x4DEF57→0x4ED030; nonfull path may use 0x4DEFCF→0x4DEC70. Independent historical E evidence attested native windows 4/4 and E8 destinations 6/6. Historical 72/72 conditional abstract cases (24 full,48 partial) check branching and model-only tree-free ordering; do **not** prove real tree lifetime or game-reachable partial deletion. Source-range metadata uses mixed inclusive/exclusive end conventions across B windows; SHA-specific lengths 70/168/73/53 bytes avoid a false T019 engine discrepancy.

## VA / CALL / offsets
0x4726A0,0x4726C1,0x4DEF40,0x4DEF57,0x4DEFCF,0x4DEC70,0x4ED030,0x49F6A0; CALL 0x4DEF57→0x4ED030, 0x4DEFCF→0x4DEC70; tree count +0x8, sentinel +0x15.

## T019 and acceptance state
No newly proven original-game Wiki/DAT/EXE contradiction. GameClear DAT13 versus TXT2 is previously resolved **search-scope difference**, while TXT loading, script2 priority, phase flags and later gwrite behavior remain VERIFY. A provenance-bound or interpretation correction is **not** an observed game defect. Existing formal MASTER checkpoint196/READY596 (A115/B229/C136/D116); 34 Task 9/21/4 previously reported, not freshly reclassified; no new official READY integration.

## KB_CANDIDATE / next
`E-AUDIT-20261031-09H-T020-T011-BULK-ERASE-BOUNDARY-01` cross-references `B-20261031-09H-T011-TRAINING-CACHE-BULK-ERASE-NATIVE-01` as E-only acceptance/correction. Existing KB name/entry must be checked against source and corrected studies; no automatic symbol/REF/manifest update. B owner to prove legitimate partial erase reachability; E to verify same-run legal G0/G1/G2.
