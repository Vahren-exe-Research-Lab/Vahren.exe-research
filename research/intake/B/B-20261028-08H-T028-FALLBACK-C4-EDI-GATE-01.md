# B-20261028-08H-T028-FALLBACK-C4-EDI-GATE-01 — existing B/T028 source-recovery intake

- research_id: `B-20261028-08H-T028-FALLBACK-C4-EDI-GATE-01`
- owner: B
- tasks: T028 (battle-side, postresult candidate research)
- observed_at: 2026-10-28 08 JST
- source_relative_path: `data/T028_SHARED_FALLBACK_INIT_C4_EDI_GATE_NATIVE_20261028_08H.md`
- source_sha256: `a10faad5cab918a546c36c47cb44b6aee13a235865618e88f988e8ecfc61e7ca` (PC original Markdown SHA256 and byte length independently checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's verified original source reference; not a new PE rehash)
- evidence_va_call_offsets: `0x582AA0/0x582C1E/0x582C23/0x582C29,shared fallback+0xC0/+0xC4=100 on initialization,0x4942FC/0x494655 XOR EDI,EDI,0x494886/0x49488A..0x494895,0x591794`
- prior_ids_and_corrections: B-20261028-07H-T028-NAMED-RESOLVER-SENTINEL-ROSTER-SEED-01 (EAX!=EDI unresolved); 09H proves shared backlink +0x1A4 rebinding
- evidence_kind: historical native STATIC / Ghidra INDEX, INFERRED and runtime VERIFY
- golden_status: original-game PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY0; formal E MASTER update0
- intake_status: PUBLISHED_INTAKE when exact GitHub readback; not CURATED

## Owner's reusable static findings

Historical original x86 resolves the 07H EAX/EDI comparison on the specifically examined path. The initializer `0x582AA0` writes numeric 100 at shared fallback object `+0xC0` and `+0xC4`; this is **initialization state**, not proof +0xC4 is forever 100. Upper caller branches `0x4942FC` and `0x494655` each zero EDI, with no intervening write on the documented route. Hence `0x494886 CMP EAX,EDI` is effectively a nonnull EAX test there. Because miss returns NONNULL fallback, it can enter adjustment `100−[EAX+0xC4]`; immediately initialized fallback yields delta0. A later writer might change +0xC4. No real-game loyalty/morale or full alias contract is established.

## Validation and ownership limits

Check other permitted +0xC4 writers, 09H fallback reuse/rebinding, and normal original game observability before interpreting numeric changes. This is a sanitized historical B-owner source study with relative proof path/SHA, not an independently re-executed original game test or verified G4 settlement boundary. Dedicated KB curator must inspect native source and corrections within authorized evidence before changing canonical REF/symbols/structs/develop. No raw EXE/DAT/MAP/SAVE/ZIP, generated DB, user path or refused content are present.
