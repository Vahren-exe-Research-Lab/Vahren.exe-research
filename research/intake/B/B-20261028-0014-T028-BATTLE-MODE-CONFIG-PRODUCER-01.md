# B-20261028-0014-T028-BATTLE-MODE-CONFIG-PRODUCER-01 — B historical T028 battle state intake

- research_id: `B-20261028-0014-T028-BATTLE-MODE-CONFIG-PRODUCER-01`
- owner: B
- tasks: T028 (battle side, candidate/event prerequisites)
- observed_at: 2026-10-28 00H JST
- source_relative_path: `data/T028_BATTLE_MODE_CONFIG_PRODUCER_NATIVE_20261028_00H.md`
- source_sha256: `d6708901880a1e7c85be81c542027506546e443edaf377e5e88577e4bb87aa36` (authorized-PC report actual SHA256 and byte size measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target only; no fresh executable hash)
- native_evidence_va_call_offsets: `0x565B8B/0x565B92/0x565B97→0x402800/0x428010,0x565BCE/0x565BD0/0x565BD5,global+0x683748/+0x683749,0x490A83..0x490AAA,manager+0x1EED43/+0x1EED55,0x491870→0x4922A0`
- prior_ids_and_corrections: B/T028 previous 22–23H death-event list, queue clear and mode consumer; 01H subsequent side flag producer refines AL identity
- evidence_kind: historical original x86 STATIC / V9 saved pseudo-C / INFERRED, VERIFY for full runtime meaning
- golden_status: original Gameplay PASS0 / strict MATCH0 / dynamic0
- ready_status: new formal READY0 / E MASTER unchanged
- intake_status: PUBLISHED_INTAKE when exact readback, NOT_CURATED

## Source-grounded findings

Old original-PE source identifies two separate configuration keys, `@config@player_battle` and `@config@enemy_battle`, loaded via script property helpers and materialized as distinct global bytes `0x683748` and `0x683749`. Their default values differ if absent (player=1, enemy=0). In `0x490590`, manager mode `+0x1EED43` is conditionally derived as **NOT enemy_battle** when AL==0 and manager `+0x1EED55==0`, else **NOT player_battle**. Previous study knew the mode's consumer `0x491870→0x4922A0` and a conditional event queue clear/dispatch; this source joins config producer with the mode writer, not proving actual game side identity. The subsequent 01H source identifies upstream AL as one of the side flags, correcting the placeholder.

## Next validation

Use 01H F54/F55/F56 producer and 02H tree-derived flag; match actual original DAT config and legal battle setup before formal event semantics. Owner B source is the referenced relative path and SHA; the sanitized note is not a new executable/dynamic game test or G4 settlement contract. Curator must independently inspect permitted V9 source, DAT, prior versions and ownership before updating REF/symbols/structs/develop. No original assets, private paths, massive DB or previously denied payloads have been uploaded.
