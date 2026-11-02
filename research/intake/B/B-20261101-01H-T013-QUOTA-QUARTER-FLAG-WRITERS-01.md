# B-20261101-01H-T013-QUOTA-QUARTER-FLAG-WRITERS-01 — quota/quarter_view設定キーと座標変換flagの有限writer候補
research_id: B-20261101-01H-T013-QUOTA-QUARTER-FLAG-WRITERS-01
owner: B
tasks: T013,T028
domain: TARGET_SELECTION
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T013_GLOBAL65BD9E_QUOTA_QUARTER_WRITERS_NATIVE_20261101_01H.md
original_pc_source_sha256: 35BABF2BE5C00B052BDCDC907431A96398349A15163C03629AAD008819E81B8E
sha_checked_at: 2026-11-03 JST, authorized PC, read-only SHA256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR,INFERRED,VERIFY
source_address_mentions: 0x459610;0x45A21D;0x45A22C;0x45A33C;0x45A343;0x65BD9E
offset_mentions_untyped: global_flag;loader_local_flag
prior_research_ids_for_crosslink_not_automatic_supersedes: none confirmed
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_BATTLE_TAKEOVER.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historic B study's bounded meaning
既B原作V9/元ASM報告は設定文字列quota_view/quarter_viewと0x65BD9Eのclear/conditional setに関連する局所writerを示す。値0/1の静的代入は認められるが、設定→戦闘候補・座標演算・表示の全副作用は未実証。

## Reproducibility and independent next validation
Owner original report path and SHA256 were remeasured read-only on authorized PC. Isolated game PE and current unified V9 SQLite hashes also matched; these are identity gates, not independent original ASM or DAT semantics validation. Any legacy pre-V9 pseudo-C or old owner READY is prior limited evidence, not a canonical V9 ABI, original-game Golden or new READY. Prior report meaning and this summary require selective curator review. Reported VA×ID are textual source mentions, not address-role or type guarantees. Related research IDs indicate context, not automatic supersedes.

Next allowed verification: 設定組合せからflag writerと合法原作候補計算・画面座標表示への影響を独立検証。

Never use or recreate a refused operation/content, protected address, or unverified original-game behavior. Original-game Golden PASS0, strict MATCH0, new READY0, formal CURATED0; G4 external-result settlement not proven. Not part of develop/REF/structs/symbols until curator independently adopts.
