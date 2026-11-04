# B-20261029-1713-T013-UPSTREAM-FOUR-CALL-GROUP-FILTER-01 — historical B/T013 source intake

- research_id: `B-20261029-1713-T013-UPSTREAM-FOUR-CALL-GROUP-FILTER-01`
- owner: B
- tasks: T013 (target candidate, mode1 prepass; T028 reference only)
- observed_at: 2026-10-29; original B study
- source_relative_path: `data/T013_MODE1_UPSTREAM_FOUR_CALLER_GROUP_FILTER_NATIVE_20261029_17H.md`
- source_sha256: `db5fc5bb704e1095f382e0111fec49998717005a2c71cf6ef0a23bc9375e6aef` (authorized-PC original report real SHA256+bytes verified 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, no fresh whole-PE rehash)
- native_va_call_offsets: `0x44AEBF/0x44B700/0x44C705/0x44CF3E→0x44CF80;0x44CF80/0x44CFA0→0x49D1B0;0x44CFAB group vector;0x44CFE1/0x44CFEA,0x44D002,0x44D00B,0x44D027/0x44D02D;0x44D033/35/38/3A indirect vtable+0x68`
- prior_ids_and_corrections: B-20261029-1613-T013-MODE1-VTABLE68-CLASS-DISPATCH-01 four vtable entries known; 18H examines a prepass callback and break queue
- evidence_kind: historical original native STATIC / INFERRED; runtime/type/final action VERIFY
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- new_formal_ready_status: READY0, E MASTER unchanged
- intake_stage: PUBLISHED_INTAKE upon exact GitHub fetch equality, not CURATED

## Source-grounded historical facts

The old native report finds **four** upstream E8 callsites `0x44AEBF/0x44B700/0x44C705/0x44CF3E→0x44CF80`, each conditionally gated by x87 comparisons with manager `+0xD0`, and one comparison direction is reversed. Inside `0x44CF80`, manager `+0xA5/+0x18` controls an optional prepass `0x44CFA0→0x49D1B0`, then `group pointer vector +0x38..+0x3C` is iterated. It skips certain group first-Unit flag combinations, invalid `Unit+0x1867C`, null `Unit+0x1D0`, and (when `Unit+0x18615` nonzero) additional referenced-field zeros. Eligible Units are dispatched through vtable +0x68 with argument1 at `0x44D03A`, already identified in 16H. Note this upstream function itself does NOT check lower-level `Unit+0x1867E` latch, which is checked inside the callee; game-side reachability and x87 unordered handling remain VERIFY.

## Next validation and excluded evidence

Use 18H prepass and callback-drain flow; do not confuse per-unit virtual route with final game target selection. Curator must check the cited source ID/SHA and permitted original x86/V9/DAT, previous corrections and other owner provenance before REF/typed-dictionary/develop semantic adoption. No original game assets, large DB, private paths, or previous denied operation content have been uploaded. This is not a newly measured original gameplay test or a complete G4 settlement boundary.
