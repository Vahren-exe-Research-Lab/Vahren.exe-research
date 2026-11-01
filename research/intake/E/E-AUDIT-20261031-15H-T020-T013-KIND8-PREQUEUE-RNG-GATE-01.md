# E-AUDIT-20261031-15H-T020-T013-KIND8-PREQUEUE-RNG-GATE-01 — RNG producer precedes queue count<2 skip

- **Upstream ID:** `B-20261031-15H-T013-KIND8-RANDOM-PAYLOAD-QUEUE-01` (B owner; **do not duplicate discovery**).
- **E source:** `tests/T020_E_T013_KIND8_PREQUEUE_ACCEPTANCE_20261031_15H.md`; SHA256 verified 2026-11-01 `EDB29972F9CC7A6FAB72A94BBE531A18EFD3FB83896DBB0F8117BD4D3E1A1339`.
- **B source:** `data/T013_KIND8_RANDOM_PAYLOAD_QUEUE_NATIVE_20261031_15H.md`; SHA256 verified 2026-11-01 `FAEF6FDEF83E746CD0F27A5E601A6662D97A23ECF7757F2A3FD1F7C94F58C03B`. Upstream report is referenced, not reproduced.
- **Source snapshot:** 2026-10-31 (JST), private PC read-only source recheck 2026-11-01 23:52 JST.
- **Owner / task:** E / T020, T018-T019 cross-check. Upstream owner B/T011 or B/T013 as separately identified; not a new B native finding.
- **Engine basis:** previously authenticated read-only PE copy, original SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. This run independently rehashed the E and B report files, **not** the original PE or native windows.
- **Evidence class:** historical STATIC byte attestations and conditional SYNTHETIC regression; INFERRED native semantics require follow-up. Gameplay DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0; official READY=0.
- **Legal Golden gate:** unchanged old EXE and authenticated pre-karate-20x DAT, same-run G0 normal battle UI, G1 immediate prebattle SAVE bytes/SHA plus input timeline, G2 real MAP SHA and three sides plus ordered deployed Unit/Troop; G3 visible outcome and G4 World change. None acquired here.
- **Original source controls:** no original EXE/DAT/MAP/SAVE/ZIP, runtime screenshots, generated DB, or other owner's full report included. No forbidden/refused research payload reattempted. `PUBLISHED_INTAKE / NOT_CURATED` applies to this E-specific cross-check, and does not reverse any independently curated B native entry.

## E-owned result (historical evidence; no new test run)
Historical static native proof: kind8 0x577D82→0x5A3DF0 builder before 0x577DCB→0x579EB0 queue; producer internal RNG 0x5A3E55 precedes queue unsigned count<2 gate at 0x579F04/07 **if reached**. Therefore count0/1 post-queue skip does not imply no earlier RNG request; neither assures actual seed mutation. Historical byte checks 4 windows/4, E8 9/9 and instruction anchors 3/3, 80/80 abstract synthetic cases. Model sample*100/32768 is rational; native converted integer left null because x87 rounding/ABI not proven. Unit+0x18654 identity is conditional, not UI evidence.

## VA / CALL / offsets
0x577D82→0x5A3DF0; 0x577DCB→0x579EB0; 0x5A3E55,0x579F04,0x579F07; Unit+0x18650/+0x18654, record+0x28.

## T019 and acceptance state
No newly proven original-game Wiki/DAT/EXE contradiction. GameClear DAT13 versus TXT2 is previously resolved **search-scope difference**, while TXT loading, script2 priority, phase flags and later gwrite behavior remain VERIFY. A provenance-bound or interpretation correction is **not** an observed game defect. Existing formal MASTER checkpoint196/READY596 (A115/B229/C136/D116); 34 Task 9/21/4 previously reported, not freshly reclassified; no new official READY integration.

## KB_CANDIDATE / next
`E-AUDIT-20261031-15H-T020-T013-KIND8-PREQUEUE-RNG-GATE-01` cross-references `B-20261031-15H-T013-KIND8-RANDOM-PAYLOAD-QUEUE-01` as E-only acceptance/correction. Existing KB name/entry must be checked against source and corrected studies; no automatic symbol/REF/manifest update. Clarify count producer and integer conversion via B-owned source, original-game RNG/visible event via legal UI only.
