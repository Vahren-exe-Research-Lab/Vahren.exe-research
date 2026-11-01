# E-AUDIT-20261031-16H-T020-T013-BUCKET-MERGE-SIGNED-GATE-01 — 26-list bucket merge and signed threshold

- **Upstream ID:** `B-20261031-16H-T013-BUCKET-LIST-MERGE-COMPARATOR-01` (B owner; **do not duplicate discovery**).
- **E source:** `tests/T020_E_T013_BUCKET_MERGE_ACCEPTANCE_20261031_16H.md`; SHA256 verified 2026-11-01 `D3FD0A6CC920785B335FF13B96637E518301646FD31EA8F44D87BD2C8E30588A`.
- **B source:** `data/T013_BUCKET_LIST_MERGE_COMPARATOR_NATIVE_20261031_16H.md`; SHA256 verified 2026-11-01 `C9E9AE4017DB40F4810E32CB45419EE2390028757BBE38843DC0E1AE3A8CA621`. Upstream report is referenced, not reproduced.
- **Source snapshot:** 2026-10-31 (JST), private PC read-only source recheck 2026-11-01 23:52 JST.
- **Owner / task:** E / T020, T018-T019 cross-check. Upstream owner B/T011 or B/T013 as separately identified; not a new B native finding.
- **Engine basis:** previously authenticated read-only PE copy, original SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. This run independently rehashed the E and B report files, **not** the original PE or native windows.
- **Evidence class:** historical STATIC byte attestations and conditional SYNTHETIC regression; INFERRED native semantics require follow-up. Gameplay DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0; official READY=0.
- **Legal Golden gate:** unchanged old EXE and authenticated pre-karate-20x DAT, same-run G0 normal battle UI, G1 immediate prebattle SAVE bytes/SHA plus input timeline, G2 real MAP SHA and three sides plus ordered deployed Unit/Troop; G3 visible outcome and G4 World change. None acquired here.
- **Original source controls:** no original EXE/DAT/MAP/SAVE/ZIP, runtime screenshots, generated DB, or other owner's full report included. No forbidden/refused research payload reattempted. `PUBLISHED_INTAKE / NOT_CURATED` applies to this E-specific cross-check, and does not reverse any independently curated B native entry.

## E-owned result (historical evidence; no new test run)
Native 0x579EB0 handles 26 buckets of 12-byte list structures, comparator path chooses +0xA0C in mode2 vs +0xA10 otherwise, and signed JLE suppresses +0xA14 addition at or below -2147483547. Historical byte checks 3/3, E8 CALLs 10/10 and instruction anchors 14/14. E synthetic 198/198 (144 score projections+54 distinct-list count conservation) PASS. No final attack/target or comparison precedence is proved. Additional CALL 0x57A8EC→0x5B6BBB and 0x4C5819→0x5B5B6D noted in E report, semantics UNKNOWN. Prior rank and kind8 RNG studies must not be counted again. **KB check this run:** 0x579EB0 already curated in existing knowledge as BattleCandidate_MergeBucketLists; this E acceptance fixture is the uncurated delta, not a new symbol.

## VA / CALL / offsets
0x579EB0,0x57A830,0x5A3EA0,0x4C5800,0x57A8EC→0x5B6BBB,0x4C5819→0x5B5B6D; candidate+0xA0C/+0xA10/+0xA14.

## T019 and acceptance state
No newly proven original-game Wiki/DAT/EXE contradiction. GameClear DAT13 versus TXT2 is previously resolved **search-scope difference**, while TXT loading, script2 priority, phase flags and later gwrite behavior remain VERIFY. A provenance-bound or interpretation correction is **not** an observed game defect. Existing formal MASTER checkpoint196/READY596 (A115/B229/C136/D116); 34 Task 9/21/4 previously reported, not freshly reclassified; no new official READY integration.

## KB_CANDIDATE / next
`E-AUDIT-20261031-16H-T020-T013-BUCKET-MERGE-SIGNED-GATE-01` cross-references `B-20261031-16H-T013-BUCKET-LIST-MERGE-COMPARATOR-01` as E-only acceptance/correction. Existing KB name/entry must be checked against source and corrected studies; no automatic symbol/REF/manifest update. B retains comparator ABI/secondary priority; E requires lawful G0/G1/G2 and UI-visible target output.
