# B-20261029-1310-T013-POSTSELECT-DUAL-DISTANCE-FPU-GATE-01 — historical B/T013 source intake

- research_id: `B-20261029-1310-T013-POSTSELECT-DUAL-DISTANCE-FPU-GATE-01`
- owner: B
- tasks: T013 (target candidate, mode1 prepass; T028 reference only)
- observed_at: 2026-10-29; original B study
- source_relative_path: `data/T013_POSTSELECT_DUAL_DISTANCE_X87_GATE_NATIVE_20261029_13H.md`
- source_sha256: `32b7e444a5fb4ac16f70173e1affcb81778b13d24e98b4e5353b51aef9ec6837` (authorized-PC original report real SHA256+bytes verified 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, no fresh whole-PE rehash)
- native_va_call_offsets: `0x57DA9C..0x57DAB6 D distance;0x57DAC5 default S=2147483647.0,0x57DABF/CF candidate gate,0x57DAD8..0x57DB08 S distance,0x57D9F5/FC clock<=100,0x57DB1A/20/24/27/29/2D/30/32/38,0x63B298=500.0,0x63B038=1000.0`
- prior_ids_and_corrections: 11H 500/1000 constants,12H atan2/floor and old T013 clock source already known; new point is x87 status truth table and second distance sentinel
- evidence_kind: historical original native STATIC / INFERRED; runtime/type/final action VERIFY
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- new_formal_ready_status: READY0, E MASTER unchanged
- intake_stage: PUBLISHED_INTAKE upon exact GitHub fetch equality, not CURATED

## Source-grounded historical facts

Old original-PE source derives a primary Euclidean-distance-like D from signed32 squared X/Y differences and conversion helper, and a SECOND distance-like S from an optional nonnull candidate with `candidate+0x1867E==0`; otherwise S defaults to **double 2147483647.0** at `0x63B0D0`. A signed clock `manager+0x1EED64<=100` selects direct downstream correction. For clock>100, x87 `FCOMP` with 500.0 and conditional TEST AH/parity checks form a bounded finite, ordered condition **D>500 AND S<=D** to enter the correction route; unordered/NaN and huge integer-overflow cases differ. Thus for normal finite values the correction condition is `(clock<=100) OR (D>500 AND S<=D)`, contingent on the outer eligibility already passing. This report purposely leaves the previously safety-denied downstream callee body untouched, and DOES NOT claim final target or movement.

## Next validation and excluded evidence

Check only safe bounded V9 upstream expressions and x87 flags, compare 14H output alias/trigonometric branch; never inspect refused downstream callee interior. Curator must check the cited source ID/SHA and permitted original x86/V9/DAT, previous corrections and other owner provenance before REF/typed-dictionary/develop semantic adoption. No original game assets, large DB, private paths, or previous denied operation content have been uploaded. This is not a newly measured original gameplay test or a complete G4 settlement boundary.
