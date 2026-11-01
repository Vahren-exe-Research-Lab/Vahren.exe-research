# E-AUDIT-20261031-10H-T020-T011-PARTIAL-ERASE-GUARD-01 — partial erase iterator and count gate

- **Upstream ID:** `B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01` (B owner; **do not duplicate discovery**).
- **E source:** `tests/T020_E_T011_PARTIAL_ERASE_ACCEPTANCE_20261031_10H.md`; SHA256 verified 2026-11-01 `8CB2955649DFB0718B172476648FFD57C3DF0E5CA9037575D22D8F03E022F6F7`.
- **B source:** `data/T011_TRAINING_PARTIAL_ERASE_NATIVE_20261031_10H.md`; SHA256 verified 2026-11-01 `FCFE8992BE8EA58636A958E8BA0E4D615F6EAC4E9DB2455EE45C5B07D0187EF6`. Upstream report is referenced, not reproduced.
- **Source snapshot:** 2026-10-31 (JST), private PC read-only source recheck 2026-11-01 23:52 JST.
- **Owner / task:** E / T020, T018-T019 cross-check. Upstream owner B/T011 or B/T013 as separately identified; not a new B native finding.
- **Engine basis:** previously authenticated read-only PE copy, original SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. This run independently rehashed the E and B report files, **not** the original PE or native windows.
- **Evidence class:** historical STATIC byte attestations and conditional SYNTHETIC regression; INFERRED native semantics require follow-up. Gameplay DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0; official READY=0.
- **Legal Golden gate:** unchanged old EXE and authenticated pre-karate-20x DAT, same-run G0 normal battle UI, G1 immediate prebattle SAVE bytes/SHA plus input timeline, G2 real MAP SHA and three sides plus ordered deployed Unit/Troop; G3 visible outcome and G4 World change. None acquired here.
- **Original source controls:** no original EXE/DAT/MAP/SAVE/ZIP, runtime screenshots, generated DB, or other owner's full report included. No forbidden/refused research payload reattempted. `PUBLISHED_INTAKE / NOT_CURATED` applies to this E-specific cross-check, and does not reverse any independently curated B native entry.

## E-owned result (historical evidence; no new test run)
Original E study separately attested [0x4DEC70,0x4DEEE2) 626-byte window and seven outgoing direct CALLs. Native branch uses byte[node+0x15] invalid-iterator guard, deletion-free site 0x4DEEBB, conditional tree count decrement and output iterator candidate; ABI, rebalance and reachability remain VERIFY. Historical 240/240 conditional synthetic tests, only 20 abstract cases eligible for **further** partial-branch review, none for original Golden. Error-report helper must not be asserted to throw without proof. Prior 09H bulk deletion is not a second discovery.

## VA / CALL / offsets
0x4DEC70,0x4DEC74,0x4DEC7F,0x4DEC8E,0x4DEEBB,0x4DEED6; CALL 0x4DEFCF→0x4DEC70; node+0x15, tree+0x8.

## T019 and acceptance state
No newly proven original-game Wiki/DAT/EXE contradiction. GameClear DAT13 versus TXT2 is previously resolved **search-scope difference**, while TXT loading, script2 priority, phase flags and later gwrite behavior remain VERIFY. A provenance-bound or interpretation correction is **not** an observed game defect. Existing formal MASTER checkpoint196/READY596 (A115/B229/C136/D116); 34 Task 9/21/4 previously reported, not freshly reclassified; no new official READY integration.

## KB_CANDIDATE / next
`E-AUDIT-20261031-10H-T020-T011-PARTIAL-ERASE-GUARD-01` cross-references `B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01` as E-only acceptance/correction. Existing KB name/entry must be checked against source and corrected studies; no automatic symbol/REF/manifest update. B to prove partial iterator preconditions; legal G0/G1/G2 remains missing.
