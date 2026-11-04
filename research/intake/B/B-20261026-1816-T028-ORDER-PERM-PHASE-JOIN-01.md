# B-20261026-1816-T028-ORDER-PERM-PHASE-JOIN-01 — 代替移動・召喚配置の方位候補順と開始引数の交差参照
research_id: B-20261026-1816-T028-ORDER-PERM-PHASE-JOIN-01
owner: B
tasks: T028,T011
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_DIRECTION_PERM_ROTATION_NATIVE_20261026_18H.md
original_pc_source_sha256: 4BE6776BBC1745B46D0DC665802BC9762F2F2D24C28FF7DFE21150D7979D2289
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x62DD68;0x62DD20;0x4E78D7;0x4E7232;0x54F0D3;0x54F0E1;0x579823;0x579831;0x4E7770;0x4E70E0
offset_mentions_untyped: Unit+0x18688;Unit+0x1E4AC
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261026-1614-T028-VISITED-TREE-DEDUPE-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md;REF_UNIT_EXP_SUMMON.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
以前のB元PE/DATA報告に、8方向の巡回候補順P=(0,-1,+1,-2,+2,-3,+3,+4)と開始方向値dの組み合わせがある。限定された合法dでは(d+P[i]) mod 8の候補順だが、探索時の更新や遮蔽物により最終移動・召喚位置は確定しない。既知方向テーブルの再発見とは数えない。

## Limits and curator next gate
Unit開始値の実producer/更新・skip条件と正規シーンでの候補優先順位を独立照合。

The authorized PC source Markdown SHA-256 was remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. The native instructions, indirect calls, full ABI and actual original-game behavior were **not independently revalidated in this intake**. Addresses are source report references, **not** a new semantic or ABI claim. No original binaries, raw saves, decoded protected material, or other-owner research included. All earlier safety HOLD, missing-source and denied-content gates remain unchanged; G4 external-result commit unproven.
