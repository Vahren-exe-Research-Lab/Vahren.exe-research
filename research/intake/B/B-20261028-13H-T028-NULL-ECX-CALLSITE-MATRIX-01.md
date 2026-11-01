# B-20261028-13H-T028-NULL-ECX-CALLSITE-MATRIX-01 — historical B/T028 source intake

- research_id: `B-20261028-13H-T028-NULL-ECX-CALLSITE-MATRIX-01`
- owner: B
- tasks: T028 (battle object/roster and candidate routing)
- observed_at: 2026-10-28; research PC original report
- source_relative_path: `data/T028_NULL_ECX_CALLSITE_PRODUCER_MATRIX_NATIVE_20261028_13H.md`
- source_sha256: `d82737d1e2413d29521bbf73a24810aa140779b1b5f636211988863c93177979` (actual PC Markdown bytes and size verified against source metadata 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's static source target; not rehashed as PE this intake)
- native_evidence_va_call_offsets: `0x494233/0x494618/0x495120/0x49516A/0x497781/0x49BCF6→0x497BB0,0x49422F XOR ECX,0x49460F LEA ECX,0x49511C XOR ECX,0x495161 LEA ECX,0x497779 XOR ECX,0x49BCF2 XOR ECX,0x497C17/0x497C21/0x497C31`
- prior_ids_and_corrections: B-20261028-11H-T028-CANDIDATE-VECTOR-VS-SECOND-SET-01 two vector callers, 12H null-path owner cleanup; do not count them twice
- evidence_kind: historical original ASM STATIC / INFERRED / runtime VERIFY
- original_golden_status: PASS 0 / strict MATCH 0 / DYNAMIC 0
- formal_ready_status: new B READY0; MASTER formal update0
- intake_stage: PUBLISHED_INTAKE only on exact GitHub readback; NOT_CURATED

## Historical source-grounded facts and proof limits

Historical original-byte survey enumerates exactly SIX **direct E8 callers** into `0x497BB0` in the bounded index and decodes the immediately preceding ECX producer: four sites `0x494233,0x495120,0x497781,0x49BCF6` explicitly `XOR ECX,ECX`, whereas two sites `0x494618,0x49516A` pass `LEA ECX,[ESP+0x98]` after argument pushes (nonnull local vector, not second set). The callee's null branch `0x497C17` is reached ONLY when candidate flags `+0x75/+0x77` are both zero; therefore four null caller sites do NOT imply all unconditional destruction. Additional entrance constraints differ: `0x495120` executes after name-resolution hit; `0x497781` after `+0x7A=0` and clearing `+0x1B0`, without proof of `+0x75/+0x77` both zero. This is a control-flow input classification, not four confirmed morale/death events.

## Next validation / G4 caveat

Review 14H alternate flags deciding display message and numeric duration, investigate legal producer/consumer conditions and actual second-set use. This is a sanitized re-usable B-owned study with actual original report SHA, not new independent original-game test, ABI closure or external battle result post-commit proof. Dedicated curator alone may admit verified semantic facts into develop REF/dictionary. No game EXE/DAT/SAVE/ZIP, generated DB, private paths or refused content uploaded.
