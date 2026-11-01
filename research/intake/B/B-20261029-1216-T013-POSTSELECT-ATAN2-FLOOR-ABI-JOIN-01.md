# B-20261029-1216-T013-POSTSELECT-ATAN2-FLOOR-ABI-JOIN-01 — historical B/T013 source intake

- research_id: `B-20261029-1216-T013-POSTSELECT-ATAN2-FLOOR-ABI-JOIN-01`
- owner: B
- tasks: T013 (target candidate, mode1 prepass; T028 reference only)
- observed_at: 2026-10-29; original B study
- source_relative_path: `data/T013_POSTSELECT_ATAN2_FLOOR_ABI_JOIN_NATIVE_20261029_12H.md`
- source_sha256: `1feb0c9befb069674e3501f336bbdda2db6a33a01f370446db2d6709e6f2e64e` (authorized-PC original report real SHA256+bytes verified 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, no fresh whole-PE rehash)
- native_va_call_offsets: `0x57DA81..0x57DA93 five PUSH;0x4F93A1/A5/AA/B4/BA D1/D2;0x4F93C0/C8/CC→0x5E743A;0x5E743F E9→0x5E4F10;0x4F93D1/E3/E9/F2→0x5D1D90/FA→0x5D1B80;0x4F940E/19/23`
- prior_ids_and_corrections: B-20261029-1112-T013-ANGLE-QUADRANT-CORRECTION-NATIVE-01; older T028 atan2 helper source already proves CRT internal FPATAN (not re-counted)
- evidence_kind: historical original native STATIC / INFERRED; runtime/type/final action VERIFY
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- new_formal_ready_status: READY0, E MASTER unchanged
- intake_stage: PUBLISHED_INTAKE upon exact GitHub fetch equality, not CURATED

## Source-grounded historical facts

Historical original x86 stack accounting resolves five actual inputs to `0x4F93A0` at `0x57DA93`: it constructs signed integer deltas `D2=(caller EBX)-(caller EAX)`, `D1=(caller EDI)-(caller ESI)`, then loads D1/D2 into x87 at `0x4F93C0/C8` before an angle helper `0x5E743A`. That helper uses a tail **JMP** `0x5E743F→0x5E4F10`, not a direct CALL. Normal finite input semantics are compatible with atan2(D1,D2) (independent T028 prior) and a four-sector index approximating `floor((atan2(D1,D2)+π+optional π/4)/(π/2)) mod4`; stored floating constants have finite binary approximation. The `0x5D1D90` conversion performs floor-like treatment of ordinary finite positive/negative values on a specific fast branch, but alternate FPU/control and NaN/Inf/overflow are VERIFY. This does not prove the coordinate arguments are actual live game Unit positions or movement destinations.

## Next validation and excluded evidence

Validate specific native stack, hidden registers, four-sector table writer and finite corner cases; do not promote pseudo-source floor for all CPU/inputs. Curator must check the cited source ID/SHA and permitted original x86/V9/DAT, previous corrections and other owner provenance before REF/typed-dictionary/develop semantic adoption. No original game assets, large DB, private paths, or previous denied operation content have been uploaded. This is not a newly measured original gameplay test or a complete G4 settlement boundary.
