# B-20261025-1615-T011-WRITER-CALLSITE-54-INSERT-FLAG-01 — B historical Unit / Skill source intake

- research_id: `B-20261025-1615-T011-WRITER-CALLSITE-54-INSERT-FLAG-01`
- owner: B
- tasks: T011 (A/VM caller semantics not owned by B)
- observed_at: 2026-10-25 16H JST
- source_relative_path: `data/T011_VARIABLE_WRITER_CALLS54_INSERT_FLAG_NATIVE_20261025_16H.md`
- source_sha256: `1a0c6dd3c44cb2078f682ce04accc4da968a37be90d7ee610a41f283b1df8880` (PC source original report SHA256/byte count measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target, no new PE rehash during intake)
- evidence_va_call_offsets: `0x4637A0 54 E8 callers,0x4321B0/0x441200/0x45BE10/0x466F60/0x46B3A0/0x46B8D0/0x46BB80/0x46C710/0x4A7A90/0x4AE0F0,0x46386C/0x463896/0x4638A2,0x4A69B0 flag`
- prior_ids_and_corrections: B-20261025-1513-T011-VALUE-PTR-NODE-ERASE-01; absent old 14H source and generic 0x4A69B0 tree insert not re-counted
- evidence_kind: historical original ASM STATIC, INFERRED/VERIFY for runtime; current DYNAMIC0
- original_golden: PASS0 / strict MATCH0
- formal_ready: newly READY0 / MASTER update0
- intake_stage: PUBLISHED_INTAKE when GitHub readback equals this summary, NOT_CURATED

## Source-grounded bounded findings

Historical original-PE E8 source enumerated **54 direct callsites to variable writer `0x4637A0` across 10 caller functions**. Counts: `0x4321B0:1`, `0x441200:1`, `0x45BE10:11`, `0x466F60:1`, `0x46B3A0:1`, `0x46B8D0:1`, `0x46BB80:1`, `0x46C710:1`, `0x4A7A90:2`, `0x4AE0F0:34`. The historical study recovered a subset of argument flags explicitly; **47 sites had pseudo-C no-argument signature**, so cannot be assigned all flag==1 or a permanent save scope. The writer's flag-nonzero branch checks/erases existing key via `0x46386C`, creates a fresh node at `0x463896`, inserts at `0x4638A2`; a successful insertion flag is only local success, not proof no leaks, no duplicates, or durable ownership across all callers. Individual VM opcode semantics remain A owner; this B report only preserves caller/native flag provenance.

## Next validation and boundaries

Curator verify E8 source identity and selected ABI callsites; B investigate permitted value lifetime and G4 state scope without changing A/VM owner evidence. This is a sanitized owner B research record, not independent gameplay or a fully validated API hook signature. Existing source, correction history and permitted V9/DAT require dedicated curator review before develop REF/typed dictionary. Missing original files and earlier denied operations remain separate; no refused output, private identity, original game assets or huge generated DB included.
