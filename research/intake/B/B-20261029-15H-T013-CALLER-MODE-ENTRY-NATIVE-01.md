# B-20261029-15H-T013-CALLER-MODE-ENTRY-NATIVE-01 — historical B/T013 source intake

- research_id: `B-20261029-15H-T013-CALLER-MODE-ENTRY-NATIVE-01`
- owner: B
- tasks: T013 (target candidate, mode1 prepass; T028 reference only)
- observed_at: 2026-10-29; original B study
- source_relative_path: `data/T013_POSTSELECT_FOUR_CALLER_MODE_NATIVE_20261029_15H.md`
- source_sha256: `e223128b8332cdd52a35368fdcd3640a8ff5e0edc089fb712b8385de66664e26` (authorized-PC original report real SHA256+bytes verified 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, no fresh whole-PE rehash)
- native_va_call_offsets: `0x544D10/0x544D1A/0x544D23..0x544D9C→0x57D8B0 mode1;0x578110/0x578149..0x5782B9→0x57D8B0 mode1;0x545CA2/0x57B35B mode0;0x57D9B7/0x57D9CE/0x57D9D2→0x5146B0/0x57D9E2→0x40ED80/0x57D9E9`
- prior_ids_and_corrections: Older B-20261021-1914-01 had four caller site names; 10/15 mode0 known; 16H vtable dispatch proves lack of E8 direct caller does not mean unreachable
- evidence_kind: historical original native STATIC / INFERRED; runtime/type/final action VERIFY
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- new_formal_ready_status: READY0, E MASTER unchanged
- intake_stage: PUBLISHED_INTAKE upon exact GitHub fetch equality, not CURATED

## Source-grounded historical facts

Historic native study isolates two mode1 callers: routine `0x544D10` checks `Unit+0x1867E` latch and on initial unset path sets that byte and `+0x1867F`, writes `+0x1E550=1.0` and sentinel coordinates, then pushes mode=1 to `0x57D8B0`. Routine `0x578110` similarly checks latch and can prepare a retreat-like string/other state before mode1 call. Two already-known mode0 callsites `0x545CA2` and `0x57B35B` pass zero, with return AL branch. Shared callee `0x57D9B7` tests mode param: mode1 skips a local gate using two helpers `0x5146B0` and `0x40ED80` that mode0 may consult, but does NOT bypass earlier eligibility, clock, distance or subsequent gates. No inference that mode1 always succeeds or means confirmed retreat.

## Next validation and excluded evidence

Verify original caller class/indirect vtable (16H), upstream group filter (17H) and return-AL consumption, keep actual action UNKNOWN. Curator must check the cited source ID/SHA and permitted original x86/V9/DAT, previous corrections and other owner provenance before REF/typed-dictionary/develop semantic adoption. No original game assets, large DB, private paths, or previous denied operation content have been uploaded. This is not a newly measured original gameplay test or a complete G4 settlement boundary.
