# E-AUDIT-20261031-13H-T020-T013-FIXED-ANCHOR-CORRECTION-01 — fixed-anchor tie interpretation correction

- **Upstream ID:** `B-20261031-13H-T013-SORT-ANCHOR-TIE-CORRECTION-01` (B owner; **do not duplicate discovery**).
- **E source:** `tests/T020_E_T013_FIXED_ANCHOR_CORRECTION_ACCEPTANCE_20261031_13H.md`; SHA256 verified 2026-11-01 `157AD16C3163FDB6124564113BDF2BF63E9CA655146B25C784246C36F6D82785`.
- **B source:** `data/T013_DUAL_SCORE_SORT_ANCHOR_TIE_CORRECTION_NATIVE_20261031_13H.md`; SHA256 verified 2026-11-01 `6C09EA760DEB4FDD6C6793648833D22C2B246A94A8AEB82BB8C9FB6FAFA9CB18`. Upstream report is referenced, not reproduced.
- **Source snapshot:** 2026-10-31 (JST), private PC read-only source recheck 2026-11-01 23:52 JST.
- **Owner / task:** E / T020, T018-T019 cross-check. Upstream owner B/T011 or B/T013 as separately identified; not a new B native finding.
- **Engine basis:** previously authenticated read-only PE copy, original SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. This run independently rehashed the E and B report files, **not** the original PE or native windows.
- **Evidence class:** historical STATIC byte attestations and conditional SYNTHETIC regression; INFERRED native semantics require follow-up. Gameplay DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0; official READY=0.
- **Legal Golden gate:** unchanged old EXE and authenticated pre-karate-20x DAT, same-run G0 normal battle UI, G1 immediate prebattle SAVE bytes/SHA plus input timeline, G2 real MAP SHA and three sides plus ordered deployed Unit/Troop; G3 visible outcome and G4 World change. None acquired here.
- **Original source controls:** no original EXE/DAT/MAP/SAVE/ZIP, runtime screenshots, generated DB, or other owner's full report included. No forbidden/refused research payload reattempted. `PUBLISHED_INTAKE / NOT_CURATED` applies to this E-specific cross-check, and does not reverse any independently curated B native entry.

## E-owned result (historical evidence; no new test run)
Critical explicit E/B 12H correction. Rank anchor EDI is changed only while sentinel; on later scores unequal to retained anchor, EBP is decremented even for consecutive equal lower scores. Historical 4032/4032 synthetic cases PASS, 1044 disagree with intentionally obsolete preceding-item tie grouping; neither number is gameplay. Anchors: [20,20,8,8]→[10000,10000,9999,9998], [20,8,8,8]→[10000,9999,9998,9997], [20,20,20] constant10000. Signed threshold may skip rank write **after** decrement; unknown output remains null. Native E source historically checked six windows, 3 direct E8 targets.

## VA / CALL / offsets
0x449276→0x47BB50; 0x47BBF6→0x44D6A0; 0x44927E,0x449280,0x449285,0x4492AF,0x4492B7,0x4492BB,0x4492BF; candidate+0xA0C/+0xA10.

## T019 and acceptance state
No newly proven original-game Wiki/DAT/EXE contradiction. GameClear DAT13 versus TXT2 is previously resolved **search-scope difference**, while TXT loading, script2 priority, phase flags and later gwrite behavior remain VERIFY. A provenance-bound or interpretation correction is **not** an observed game defect. Existing formal MASTER checkpoint196/READY596 (A115/B229/C136/D116); 34 Task 9/21/4 previously reported, not freshly reclassified; no new official READY integration.

## KB_CANDIDATE / next
`E-AUDIT-20261031-13H-T020-T013-FIXED-ANCHOR-CORRECTION-01` cross-references `B-20261031-13H-T013-SORT-ANCHOR-TIE-CORRECTION-01` as E-only acceptance/correction. Existing KB name/entry must be checked against source and corrected studies; no automatic symbol/REF/manifest update. Curator must retain B13/E13 erratum linkage, not mislabel this a proven game bug; sort input order/33+ remain VERIFY.
