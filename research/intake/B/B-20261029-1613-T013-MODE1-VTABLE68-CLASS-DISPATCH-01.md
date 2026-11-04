# B-20261029-1613-T013-MODE1-VTABLE68-CLASS-DISPATCH-01 — historical B/T013 source intake

- research_id: `B-20261029-1613-T013-MODE1-VTABLE68-CLASS-DISPATCH-01`
- owner: B
- tasks: T013 (target candidate, mode1 prepass; T028 reference only)
- observed_at: 2026-10-29; original B study
- source_relative_path: `data/T013_MODE1_VTABLE68_CLASS_DISPATCH_NATIVE_20261029_16H.md`
- source_sha256: `2ec0a219281380c181587592a7bed052311a371c0dcda8ec95146fedc3677555` (authorized-PC original report real SHA256+bytes verified 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, no fresh whole-PE rehash)
- native_va_call_offsets: `SimpleUnit vtable 0x63A4BC+0x68→0x544D10,StaticUnit 0x63A85C+0x68→0x578110,SimpleStaticUnit 0x63A8E4+0x68→0x578110,Unit 0x63A9E4+0x68→0x578110;0x44CF80 and 0x44D033/35/38/3A indirect CALL`
- prior_ids_and_corrections: B-20261029-15H-T013-CALLER-MODE-ENTRY-NATIVE-01 has two functions with zero direct E8 callers; this source establishes virtual entry, not live call reachability
- evidence_kind: historical original native STATIC / INFERRED; runtime/type/final action VERIFY
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- new_formal_ready_status: READY0, E MASTER unchanged
- intake_stage: PUBLISHED_INTAKE upon exact GitHub fetch equality, not CURATED

## Source-grounded historical facts

Original PE vtable slot +0x68 is decoded for four RTTI-labeled classes: `SimpleUnit`→`0x544D10`, while `StaticUnit`, `SimpleStaticUnit` and `Unit`→`0x578110`. The source verified corresponding native constructor vptr writes and Ghidra class labels separately. A common caller at `0x44CF80` has a native **indirect virtual CALL** `0x44D033 MOV EDX,[ECX]`, `0x44D035 MOV EAX,[EDX+0x68]`, `0x44D038 PUSH 1`, `0x44D03A CALL EAX`. Therefore E8 caller-count zero for these functions does not establish dead code. Candidate Unit predicates and real runtime class identity remain VERIFY; earlier 15H mode1 setup is not counted as new. Literal retreat-like string does not prove true morale/retreat behavior.

## Next validation and excluded evidence

Review 17H four upstream E8 callers and class-specific Unit filters, compare original runtime vptr identity only if lawful fixtures exist. Curator must check the cited source ID/SHA and permitted original x86/V9/DAT, previous corrections and other owner provenance before REF/typed-dictionary/develop semantic adoption. No original game assets, large DB, private paths, or previous denied operation content have been uploaded. This is not a newly measured original gameplay test or a complete G4 settlement boundary.
