# E-AUDIT-20261031-11H-T020-T011-SUCCESSOR-BEFORE-ERASE-01 — save next iterator before deletion

- **Upstream ID:** `B-20261031-11H-T011-PARTIAL-RANGE-SUCCESSOR-PRESERVE-01` (B owner; **do not duplicate discovery**).
- **E source:** `tests/T020_E_T011_SUCCESSOR_BEFORE_ERASE_ACCEPTANCE_20261031_11H.md`; SHA256 verified 2026-11-01 `164EF3C77941FB985E8DC6119AD4EB371B0C8D8C50C35B7A2AEB69FC76A79182`.
- **B source:** `data/T011_TRAINING_PARTIAL_RANGE_SUCCESSOR_PRESERVE_NATIVE_20261031_11H.md`; SHA256 verified 2026-11-01 `C391E96E951C1C22E1D02F03C12ECD4E0F7C1F39F1E746316E201C04217F0631`. Upstream report is referenced, not reproduced.
- **Source snapshot:** 2026-10-31 (JST), private PC read-only source recheck 2026-11-01 23:52 JST.
- **Owner / task:** E / T020, T018-T019 cross-check. Upstream owner B/T011 or B/T013 as separately identified; not a new B native finding.
- **Engine basis:** previously authenticated read-only PE copy, original SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. This run independently rehashed the E and B report files, **not** the original PE or native windows.
- **Evidence class:** historical STATIC byte attestations and conditional SYNTHETIC regression; INFERRED native semantics require follow-up. Gameplay DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0; official READY=0.
- **Legal Golden gate:** unchanged old EXE and authenticated pre-karate-20x DAT, same-run G0 normal battle UI, G1 immediate prebattle SAVE bytes/SHA plus input timeline, G2 real MAP SHA and three sides plus ordered deployed Unit/Troop; G3 visible outcome and G4 World change. None acquired here.
- **Original source controls:** no original EXE/DAT/MAP/SAVE/ZIP, runtime screenshots, generated DB, or other owner's full report included. No forbidden/refused research payload reattempted. `PUBLISHED_INTAKE / NOT_CURATED` applies to this E-specific cross-check, and does not reverse any independently curated B native entry.

## E-owned result (historical evidence; no new test run)
Read-only original E report attested [0x4DEF6A,0x4DEFE5) 123-byte window SHA and direct CALL 0x4DEFCF→0x4DEC70. E synthesized 432 BST ordered-range first-step cases: 96 empty,12 whole-range handled in separate bulk branch,324 partial (right-descent154,ancestor170). All 432 passed historically. The model does **not** emulate native red-black tree unlink, memory safety, invalid sentinel or legitimate training-cache lifecycle. Local pointer capture 0x4DEF9A/0x4DEFC4, deletion 0x4DEFCF and restore 0x4DEFD4 are conditional STATIC/INFERRED.

## VA / CALL / offsets
0x4DEF6A,0x4DEF74,0x4DEF9A,0x4DEFC4,0x4DEFC8,0x4DEFCF,0x4DEFD4,0x4DEFDC; node links +0/+4/+8 and flag+0x15.

## T019 and acceptance state
No newly proven original-game Wiki/DAT/EXE contradiction. GameClear DAT13 versus TXT2 is previously resolved **search-scope difference**, while TXT loading, script2 priority, phase flags and later gwrite behavior remain VERIFY. A provenance-bound or interpretation correction is **not** an observed game defect. Existing formal MASTER checkpoint196/READY596 (A115/B229/C136/D116); 34 Task 9/21/4 previously reported, not freshly reclassified; no new official READY integration.

## KB_CANDIDATE / next
`E-AUDIT-20261031-11H-T020-T011-SUCCESSOR-BEFORE-ERASE-01` cross-references `B-20261031-11H-T011-PARTIAL-RANGE-SUCCESSOR-PRESERVE-01` as E-only acceptance/correction. Existing KB name/entry must be checked against source and corrected studies; no automatic symbol/REF/manifest update. Native sentinel/ABI remains B-owned VERIFY; avoid claiming full repeated erase proven.
