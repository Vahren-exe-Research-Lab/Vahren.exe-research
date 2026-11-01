# B-20261029-1813-T013-PREPASS-CALLBACK-BREAK-DRAIN-01 — historical B/T013 source intake

- research_id: `B-20261029-1813-T013-PREPASS-CALLBACK-BREAK-DRAIN-01`
- owner: B
- tasks: T013 (target candidate, mode1 prepass; T028 reference only)
- observed_at: 2026-10-29; original B study
- source_relative_path: `data/T013_MODE1_PREPASS_CALLBACK_BREAK_DRAIN_NATIVE_20261029_18H.md`
- source_sha256: `799811c9d888603f1e31dac30c6160c67df9a0e81bb32f16fe5f8bbf340b64ab` (authorized-PC original report real SHA256+bytes verified 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, no fresh whole-PE rehash)
- native_va_call_offsets: `0x44CF80/0x44CF97/0x44CFA0→0x49D1B0;0x49D1B0..0x49D1C4 begin/end,0x49D1CF→vtable+0x58 at 0x49D1D4,0x49D1D6..0x49D1EA reloaded vector,0x49D1EC..0x49D212 break branch and vtable+0x24,0x49D214..0x49D240 end=begin`
- prior_ids_and_corrections: B-20261029-1713-T013-UPSTREAM-FOUR-CALL-GROUP-FILTER-01 prepass known, but 18H refines queue/drain effects, not a universal battle termination
- evidence_kind: historical original native STATIC / INFERRED; runtime/type/final action VERIFY
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- new_formal_ready_status: READY0, E MASTER unchanged
- intake_stage: PUBLISHED_INTAKE upon exact GitHub fetch equality, not CURATED

## Source-grounded historical facts

Historic native source verifies manager flags `+0xA5/+0x18` can enable a **prepass** before the group-wise virtual +0x68 dispatch. Caller `0x44CFA0` passes an ESI pointer derived from owner `[manager+4]+0x504`, not manager itself, to `0x49D1B0`. In the callee a vector at `ESI+0x1EEBBC/+0x1EEBC0` is scanned; each record can call its own vtable+0x58, with begin/end **reloaded after each callback**, so callback modifications may alter traversal. After this loop, when vector nonempty and a mode field `+0x1EEC3C==2`, it conditionally sends literal `break` via virtual+0x24 on another object. Subsequently it resets the vector's logical end to begin (length zero), not evidence of physically freeing objects. Thus prepass callbacks/drain can occur even if subsequent eligible Unit count is zero. This does not prove actual gameplay battle break, morale, victory, or G4 settlement.

## Next validation and excluded evidence

Recheck all entry prerequisites and remaining six callers of 0x49D1B0 (not covered by 18H), verify queue object lifetime and legal original-game result without assuming all callbacks were executed. Curator must check the cited source ID/SHA and permitted original x86/V9/DAT, previous corrections and other owner provenance before REF/typed-dictionary/develop semantic adoption. No original game assets, large DB, private paths, or previous denied operation content have been uploaded. This is not a newly measured original gameplay test or a complete G4 settlement boundary.
