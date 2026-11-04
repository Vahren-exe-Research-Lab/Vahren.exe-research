# B-20261028-07H-T028-NAMED-RESOLVER-SENTINEL-ROSTER-SEED-01 — existing B/T028 source-recovery intake

- research_id: `B-20261028-07H-T028-NAMED-RESOLVER-SENTINEL-ROSTER-SEED-01`
- owner: B
- tasks: T028 (battle-side, postresult candidate research)
- observed_at: 2026-10-28 07 JST
- source_relative_path: `data/T028_NAMED_RESOLVER_SENTINEL_ROSTER_SEED_NATIVE_20261028_07H.md`
- source_sha256: `04fe1739a9f93f06b724e1454da4e936e8e604c334585adda3ab6f2a7e904863` (PC original Markdown SHA256 and byte length independently checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's verified original source reference; not a new PE rehash)
- evidence_va_call_offsets: `0x5882F0/0x58834D..0x5883C1,source+0xD4/+0xD8 stride0x1C,0x5883B4→0x467DE0,0x5916E0/0x59173B→0x402800/0x591746→0x467DE0/0x59176B→0x582AA0/0x591794,global fallback 0xB05A28`
- prior_ids_and_corrections: B-20261028-06H-T028-LOYAL-DOWN-POINTER-KEY-GATE-01, corrected by 08H initial +0xC4 and EDI zero and 09H fallback backlink rebinding
- evidence_kind: historical native STATIC / Ghidra INDEX, INFERRED and runtime VERIFY
- golden_status: original-game PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY0; formal E MASTER update0
- intake_status: PUBLISHED_INTAKE when exact GitHub readback; not CURATED

## Owner's reusable static findings

Historical native source finds `0x5882F0` initializes an output roster candidate with **source self pointer as a first element**, then scans a `0x1C`-stride name-record vector `source+0xD4/+0xD8`, resolves each via `0x467DE0` and appends nonzero resolved pointers. This is not a unique list guarantee. Another resolver `0x5916E0` returns matched object pointer on a hit, but on miss uses one-time lazy initializer `0x582AA0` and returns a shared **NONNULL fallback object** at `0xB05A28` rather than NULL. The caller `0x494886` compares EAX against EDI; 06H's tentative `nonNULL` interpretation required EDI proof and is specifically bounded by the 08H report. Object C++ type, ownership, reuse, exact result changes and game behavior remain VERIFY.

## Validation and ownership limits

Read 08H native fallback initial values and EDI=0 proof, 09H per-miss owner reference updates; verify callsite identity using permitted V9/primary source. This is a sanitized historical B-owner source study with relative proof path/SHA, not an independently re-executed original game test or verified G4 settlement boundary. Dedicated KB curator must inspect native source and corrections within authorized evidence before changing canonical REF/symbols/structs/develop. No raw EXE/DAT/MAP/SAVE/ZIP, generated DB, user path or refused content are present.
