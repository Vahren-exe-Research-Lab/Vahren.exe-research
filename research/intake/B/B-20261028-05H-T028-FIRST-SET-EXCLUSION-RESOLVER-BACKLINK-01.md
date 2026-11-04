# B-20261028-05H-T028-FIRST-SET-EXCLUSION-RESOLVER-BACKLINK-01 — existing B/T028 source-recovery intake

- research_id: `B-20261028-05H-T028-FIRST-SET-EXCLUSION-RESOLVER-BACKLINK-01`
- owner: B
- tasks: T028 (battle-side, postresult candidate research)
- observed_at: 2026-10-28 05 JST
- source_relative_path: `data/T028_FIRST_SET_EXCLUSION_RESOLVER_BACKLINK_NATIVE_20261028_05H.md`
- source_sha256: `3639e2e999b213b651002e48dbec2b0f36d9d6a19cbca6a1b1d8e30fdde6a807` (PC original Markdown SHA256 and byte length independently checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's verified original source reference; not a new PE rehash)
- evidence_va_call_offsets: `0x493AD1→0x498EE0,0x494917/0x495015/0x49526C/0x4958A7/0x495A1D→0x44D070,0x4948F8/0x494FF6/0x49524D/0x495888/0x4959FE→0x467DE0,0x467E30 writes +0x1A4`
- prior_ids_and_corrections: B-20261028-0410-T028-TEMP-SET-INSERT-ABI-01 first set producer, known generic T013 0x44D070; later 06H proves pointer-valued key
- evidence_kind: historical native STATIC / Ghidra INDEX, INFERRED and runtime VERIFY
- golden_status: original-game PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY0; formal E MASTER update0
- intake_status: PUBLISHED_INTAKE when exact GitHub readback; not CURATED

## Owner's reusable static findings

Historical native static source traces FIVE exclusion gates after building a first temporary integer-key set. Each path resolves a record name through `0x467DE0`, then uses `0x44D070` with ECX as set pointer, EBX as key pointer and EAX as iterator output. A found iterator different from header causes that local candidate path to SKIP, so membership is a **negative eligibility gate**, not a hit-effect creator. Earlier name lookup `0x467DE0` can write the resolved record's `+0x1A4` backlink to the owner context on hit BEFORE exclusion. The generic key lookup helper's independent meaning is old T013 evidence and not recounted. Actual key type, candidate effects, and same manager across callsites remain VERIFY.

## Validation and ownership limits

Review 06H pointer-key ABI and 07H roster producer; validate this exclusion's actual Unit/owner identity and side effects in permitted V9/unchanged original DAT before any G4 settlement claim. This is a sanitized historical B-owner source study with relative proof path/SHA, not an independently re-executed original game test or verified G4 settlement boundary. Dedicated KB curator must inspect native source and corrections within authorized evidence before changing canonical REF/symbols/structs/develop. No raw EXE/DAT/MAP/SAVE/ZIP, generated DB, user path or refused content are present.
