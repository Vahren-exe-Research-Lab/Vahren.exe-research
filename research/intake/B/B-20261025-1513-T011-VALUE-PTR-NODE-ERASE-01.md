# B-20261025-1513-T011-VALUE-PTR-NODE-ERASE-01 — B historical Unit / Skill source intake

- research_id: `B-20261025-1513-T011-VALUE-PTR-NODE-ERASE-01`
- owner: B
- tasks: T011
- observed_at: 2026-10-25 15H JST
- source_relative_path: `data/T011_VALUE_POINTER_NODE_ERASE_20261025_15H.md`
- source_sha256: `78ab772ca86b449093f0e380ff3499c25965422dd6b1dc19f18d773e51e41ddf` (PC source original report SHA256/byte count measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target, no new PE rehash during intake)
- evidence_va_call_offsets: `0x4637A0,0x46386C→0x58F7E0,0x463896→0x436680,0x4638A2→0x4A69B0,0x4366AF..0x436701,0x510030,0x51027A..0x5102B7,0x463070`
- prior_ids_and_corrections: B-OFFLINE-20261025-1411-T011-COUNTER-REPLACE-ERASE-01 original absent/unverified; do not fabricate or republish missing material; 16H confirms writer callers
- evidence_kind: historical original ASM STATIC, INFERRED/VERIFY for runtime; current DYNAMIC0
- original_golden: PASS0 / strict MATCH0
- formal_ready: newly READY0 / MASTER update0
- intake_stage: PUBLISHED_INTAKE when GitHub readback equals this summary, NOT_CURATED

## Source-grounded bounded findings

Historical original-PE bounded ASM extends an earlier partially uncollected T011 variable-replacement study. `0x4637A0` creates a **new 32-byte value object**, optionally erases an old key through `0x46386C→0x58F7E0`, then constructs a new 48-byte tree node via `0x436680` and `0x4638A2→0x4A69B0` insert. `0x436680` allocates 0x30 bytes and copies a value-object pointer to `node+0x28` in a known path. Erase `0x58F7E0` can reach `0x510030` for partial deletion or `0x463070` for full tree cleanup. The examined node destroy paths free key-string dynamic storage and the **tree node itself**, without an explicit `node+0x28` pointer free in those bounded functions; this does NOT prove a memory leak or who finally owns the detached value object. Missing 14H primary report remains unresolved; old sequence not recounted as fresh original gameplay.

## Next validation and boundaries

Verify lifetime readers/free callers for value object+0x1C and pointer node+0x28, compare 16H native caller flag distribution and original existing keys, then curator ref. This is a sanitized owner B research record, not independent gameplay or a fully validated API hook signature. Existing source, correction history and permitted V9/DAT require dedicated curator review before develop REF/typed dictionary. Missing original files and earlier denied operations remain separate; no refused output, private identity, original game assets or huge generated DB included.
