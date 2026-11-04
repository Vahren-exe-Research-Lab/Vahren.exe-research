# B-20261029-0515-T028-ALFLAG-ONE-SHOT-DRAIN-01 — B historic T028 result/queue research

- research_id: `B-20261029-0515-T028-ALFLAG-ONE-SHOT-DRAIN-01`
- owner: B
- tasks: T028 (result/notification candidates; T012/T013 crossreference only)
- observed_at: 2026-10-29 original owner study
- source_relative_path: `data/T028_DUAL_VECTOR_ALFLAG_AND_DRAIN_NATIVE_V3_20261029_05H.md`
- source_sha256: `b5d46e212bb9c9a93615e72bc0287110d3a685f649f64f4ea56844f7da875024` (authorized PC Markdown real SHA256+bytes measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (previous measured original target, no fresh PE rehash)
- native_evidence_va_call_offsets: `0x48CFCF/0x48CFD5 AL=1→0x5AA6E0,0x48D081/0x48D087 AL=0→0x5AA6E0,0x5AA6E9 N+0x8C,0x5AA6EF/0x5AA709→0x5A9CC0,0x48D2C2/0x48D328/0x48D388→0x417160;three vectors+0x1EEC74/+0x1EEC94/+0x1EECA4`
- prior_ids_and_errata: B-20261029-0415-T028-ALTVECTOR-FIRE-REGISTRATION-JOIN-01 two vectors, 06H AL1 pre-detach; old separate five tuple producer is not duplicate
- evidence_kind: historical original ASM STATIC / old V3 index supplement / INFERRED and VERIFY for ABI, gameplay
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0 / E MASTER unchanged
- intake_status: owner PUBLISHED_INTAKE upon matching GitHub fetch; NOT_CURATED

## Reusable owner research facts

The native source distinguishes first conditional result vector caller at `0x48CFD7` passing **AL=1**, and second `0x48D089` passing **AL=0** into shared `0x5AA6E0`; both send receiver `linkedObject+0x260`, where `receiver+0x8C=AL` is written. On AL1 only, a linked object's vtable+0x64 predicate can cause `0x5AA709→0x5A9CC0` prior-detach geometry path. Both converge to later registration-like branch. After normal processing `0x48C880` logically drains **three separate 0x1C-stride result vectors** at manager offsets `+0x1EEC74, +0x1EEC94, +0x1EECA4` using `0x417160` and end=begin writes. Logical end reset differs from freeing capacity; exception and partial tuple cases may not reach that cleanup. No game evidence all events were consumed, or that either flag necessarily produces "fire" effect.

## Next verification

Review AL1 06H pre-detach and 07H inner/outer rectangle separation; original result settlement/G4 remains VERIFY. Curator must validate permitted current V9 original ASM/DAT and existing corrections before any REF/symbols/develop acceptance. No original game files, large DB, private addresses, or previously refused operation content was uploaded. Static event/queue control is not proof of original game action or G4 external battle settlement.
