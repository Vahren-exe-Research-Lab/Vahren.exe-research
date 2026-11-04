# B-20261026-1217-T028-DUAL-GRID-INITIAL-COUNTS-01 — 空間モデル初期値と二層格子の個別幅
research_id: B-20261026-1217-T028-DUAL-GRID-INITIAL-COUNTS-01
owner: B
tasks: T028
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_DUAL_GRID_INITIAL_COUNT_SOURCE_NATIVE_20261026_12H.md
original_pc_source_sha256: 84C767F1CAA41F703EFDC06873A79C7C0DCC74C6BB031FCCB6EDC3CB96365108
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x65D150;0x4B9E50;0x4B9E73;0x4B9E93;0x4B9EB4;0x4BBC90;0x4E4830;0x4E485F;0x4BBD02
offset_mentions_untyped: GameModel+0x10,+0x24,+0x28,+0x2C;NewGameModel+0x50,+0x54,+0x58,+0x5C
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261026-1113-T028-GRID-CONSTRUCTOR-MODE-PROVENANCE-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md;REF_UNIT_EXP_SUMMON.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
過去Bの限定x86/PE.data確認では初期W=16320の読み出しから、基底側のtrunc(W/128)+1=128と上位側のtrunc(W/64)+1=256が別々に生成される。先行11Hに記された64系のみの説明を二系統へ訂正。実行時W不変・格子の用途・合法MAP寸法は未確認。

## Limits and curator next gate
許可されたglobal Wの間接writer、startupから実戦までの値域、二層gridの実consumerを独立確認。

The authorized PC source Markdown SHA-256 was remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. The native instructions, indirect calls, full ABI and actual original-game behavior were **not independently revalidated in this intake**. Addresses are source report references, **not** a new semantic or ABI claim. No original binaries, raw saves, decoded protected material, or other-owner research included. All earlier safety HOLD, missing-source and denied-content gates remain unchanged; G4 external-result commit unproven.
