# B-20261026-0511-T024-UI-THREE-RESERVED-SIBLING-GATE-01 — 候補UI描画の予約枠と兄弟要素フィルタ粒度
research_id: B-20261026-0511-T024-UI-THREE-RESERVED-SIBLING-GATE-01
owner: B
tasks: T024,T013
domain: BATTLE_MORALE_ROUTE
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T024_UI_THREE_RESERVED_SIBLING_GATE_NATIVE_20261026_05H.md
original_pc_source_sha256: 722ED0FA8230BE8DCBBA4DF3A53C662A6691D553DC544539641B73CCCCE18240
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x41F5AD;0x41F5E9;0x41F5F5;0x41F601;0x41F60C;0x41F613;0x584970
offset_mentions_untyped: child+0x1C8;child+0x8C;child+0x1F8
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261025-2213-T024-TEMP-SELECTION-UI-ADAPTER-01
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_SKILL_POST_ACTION.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
元のB限定x86レポートは描画可能な可変枠と先頭子候補のgateとを区別し、後続要素の同じgateが局所ループに見えないと指摘する。最終表示内容、無効Unitの可視性、AI実際の候補選択やクラッシュは未実証。UI資料はBのT024所有範囲だけ保全。

## Limits and curator next gate
レンダリング下位calleeが無効childをskipするか、合法入力が何かを範囲限定で検証。

The authorized PC source Markdown SHA-256 was independently remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. Previously reported native instructions, indirect calls, full ABI and original-game behavior were **not independently revalidated by this intake**. Numeric addresses refer to prior source mentions, not a newly proven call contract. No original binaries, raw saves, protected evidence, or other-owner material was published. Prior safety HOLD, missing-source and denied-operation gates remain; G4 external-result settlement not proven.
