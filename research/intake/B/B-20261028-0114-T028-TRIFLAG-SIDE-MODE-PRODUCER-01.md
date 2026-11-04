# B-20261028-0114-T028-TRIFLAG-SIDE-MODE-PRODUCER-01 — B historical T028 battle state intake

- research_id: `B-20261028-0114-T028-TRIFLAG-SIDE-MODE-PRODUCER-01`
- owner: B
- tasks: T028 (battle side, candidate/event prerequisites)
- observed_at: 2026-10-28 01H JST
- source_relative_path: `data/T028_TRIFLAG_SIDE_MODE_PRODUCER_NATIVE_20261028_01H.md`
- source_sha256: `e2b8a6ac9d364ed314e247885d6b37ba7a1f8dee22041b577eb1802ee98c5a5a` (authorized-PC report actual SHA256 and byte size measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target only; no fresh executable hash)
- native_evidence_va_call_offsets: `0x490632 manager+0x1EED54/+0x1EED55,0x49063B manager+0x1EED56,0x49067C/0x4909E3/0x4909EF/0x490A43/0x490A4E,0x490688,0x490A5A..0x490A77,manager+0x1EED44/+0x1EED48`
- prior_ids_and_corrections: B-20261028-0014-T028-BATTLE-MODE-CONFIG-PRODUCER-01, later 02H discovers one flag's tree writer
- evidence_kind: historical original x86 STATIC / V9 saved pseudo-C / INFERRED, VERIFY for full runtime meaning
- golden_status: original Gameplay PASS0 / strict MATCH0 / dynamic0
- ready_status: new formal READY0 / E MASTER unchanged
- intake_status: PUBLISHED_INTAKE when exact readback, NOT_CURATED

## Source-grounded findings

Historical native bytes separate three manager flags: `+0x1EED54` and `+0x1EED55` cleared together by `0x490632`, while `+0x1EED56` cleared independently. Various earlier checks can set F54 or F55 and may set F56 separately. The input AL at `0x490A83` from 00H mode writer is **manager F54** loaded at `0x490688`. Three static manager-state cases: F54!=0 chooses side pointer pair `+0x1E8630/34` and uses NOT player_battle; F54=0,F55!=0 chooses `+0x1E8634/30` and also NOT player_battle; both zero choose `+0x1E8634/38` and NOT enemy_battle. These are pointer routing categories, not verified names enemy/player faction, morale or actual outcome. Flag F56 consumer remains unidentified.

## Next validation

Compare 02H key-match flag producer, 03H two temporary sets and game battle side/queue effects; do not rename raw flag bytes prematurely. Owner B source is the referenced relative path and SHA; the sanitized note is not a new executable/dynamic game test or G4 settlement contract. Curator must independently inspect permitted V9 source, DAT, prior versions and ownership before updating REF/symbols/structs/develop. No original assets, private paths, massive DB or previously denied payloads have been uploaded.
