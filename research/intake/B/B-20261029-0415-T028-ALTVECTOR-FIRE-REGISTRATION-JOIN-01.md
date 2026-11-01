# B-20261029-0415-T028-ALTVECTOR-FIRE-REGISTRATION-JOIN-01 — B historic T028 result/queue research

- research_id: `B-20261029-0415-T028-ALTVECTOR-FIRE-REGISTRATION-JOIN-01`
- owner: B
- tasks: T028 (result/notification candidates; T012/T013 crossreference only)
- observed_at: 2026-10-29 original owner study
- source_relative_path: `data/T028_ALTERNATE_VECTOR_FIRE_REGISTRATION_CROSSJOIN_V3_20261029_04H.md`
- source_sha256: `3cb3608a9b12e2df144a201ef3799539197fb1755b78ffec86d0964f36000a53` (authorized PC Markdown real SHA256+bytes measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (previous measured original target, no fresh PE rehash)
- native_evidence_va_call_offsets: `0x48CFB7/0x48D069→0x49E490;0x48CFD7/0x48D089→0x5AA6E0;0x5AA7B1→0x4BC920,0x5AA790→0x4C2240,0x5AA7A7→0x4C3DC0,0x5AA7D1→0x416E80,0x5AA7DD→0x416B90`
- prior_ids_and_errata: Prior 03H broken tuple out-of-range research was incomplete and remains HOLD/VERIFY; 05H later confirms literal AL1/AL0 and three-vector drain
- evidence_kind: historical original ASM STATIC / old V3 index supplement / INFERRED and VERIFY for ABI, gameplay
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0 / E MASTER unchanged
- intake_status: owner PUBLISHED_INTAKE upon matching GitHub fetch; NOT_CURATED

## Reusable owner research facts

The historical owner study finds two **different** result vectors in manager at `+0x1EEC94..+0x1EEC98` and `+0x1EECA4..+0x1EECA8`, each processed conditionally by `0x48C880`. In both paths `0x49E490` prepares a record/name lookup, followed by a vtable+0x64 guard and eligible `0x5AA6E0` effect helper at `0x48CFD7/0x48D089`. The helper's later registration-like `0x5AA7B1→0x4BC920` and string literal `spot_fire` are static cross-links, NOT proof that a fire, morale, or retreat state visibly executes. Initial study used an old V3 static index for some callee pseudocode; actual ABI, owner alias and exact effect are VERIFY. The subsequent 05H report clarifies that these two callers supply opposite AL flags.

## Next verification

Use 05H native AL1/AL0 and normalized source/destination vector, and 06H permitted downstream geometry without treating V3 text as original-game proof. Curator must validate permitted current V9 original ASM/DAT and existing corrections before any REF/symbols/develop acceptance. No original game files, large DB, private addresses, or previously refused operation content was uploaded. Static event/queue control is not proof of original game action or G4 external battle settlement.
