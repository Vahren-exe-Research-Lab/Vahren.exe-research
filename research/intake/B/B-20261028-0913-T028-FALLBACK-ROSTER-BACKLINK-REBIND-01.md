# B-20261028-0913-T028-FALLBACK-ROSTER-BACKLINK-REBIND-01 — existing B/T028 source-recovery intake

- research_id: `B-20261028-0913-T028-FALLBACK-ROSTER-BACKLINK-REBIND-01`
- owner: B
- tasks: T028 (battle-side, postresult candidate research)
- observed_at: 2026-10-28 0913 JST
- source_relative_path: `data/T028_SHARED_FALLBACK_ROSTER_BACKLINK_REBIND_NATIVE_20261028_09H.md`
- source_sha256: `5ab6bf97a5edf07ce097b25b59932ab058fb421d538a277f8d0dbfa5ef7f80dc` (PC original Markdown SHA256 and byte length independently checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's verified original source reference; not a new PE rehash)
- evidence_va_call_offsets: `0x582AA0 initial +0x1A4/+0x1D0=0,0x591762/0x59176B→0x582AA0,0x59177D/0x591783/0x591788/0x59178E/0x591794,shared 0xB05A28+0x1A4/+0x74/+0x77;0x5882F0 candidate roster`
- prior_ids_and_corrections: B-20261028-07H-T028-NAMED-RESOLVER-SENTINEL-ROSTER-SEED-01, 08H +0xC4 default; this report adds repeated fallback re-binding
- evidence_kind: historical native STATIC / Ghidra INDEX, INFERRED and runtime VERIFY
- golden_status: original-game PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY0; formal E MASTER update0
- intake_status: PUBLISHED_INTAKE when exact GitHub readback; not CURATED

## Owner's reusable static findings

Historic original ASM confirms shared fallback object constructor initially sets `+0x1A4` and `+0x1D0` zero, but every name-resolution MISS through `0x5916E0` subsequently assigns fallback `+0x1A4` from the caller's input `+0xE0` and clears flags `+0x74/+0x77`, returning the shared pointer. Thus a shared fallback reference may be **rebound on successive misses**, not a permanently fixed owner. Old 07H `0x5882F0` seeds roster candidate with its source and iterates name list; whether shared fallback ever becomes a live roster candidate is unproven. Direct reference search saw two global fallback references, but cannot exclude indirect +0xC4 writers and lifetime consumers. This is bounded STATIC/INFERRED, not evidence of an observed battle outcome.

## Validation and ownership limits

Verify permitted V9 fallback caller/readers, input+0xE0 object type, alias safety and postbattle owner restoration separately; compare other evidence and errata. This is a sanitized historical B-owner source study with relative proof path/SHA, not an independently re-executed original game test or verified G4 settlement boundary. Dedicated KB curator must inspect native source and corrections within authorized evidence before changing canonical REF/symbols/structs/develop. No raw EXE/DAT/MAP/SAVE/ZIP, generated DB, user path or refused content are present.
