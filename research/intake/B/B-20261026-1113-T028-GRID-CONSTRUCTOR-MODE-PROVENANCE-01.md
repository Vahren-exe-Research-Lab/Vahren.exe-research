# B-20261026-1113-T028-GRID-CONSTRUCTOR-MODE-PROVENANCE-01 — 格子constructorのmode初期化・二種類のセットアップcaller
research_id: B-20261026-1113-T028-GRID-CONSTRUCTOR-MODE-PROVENANCE-01
owner: B
tasks: T028
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_SPATIAL_GRID_CTOR_FLAG_PROVENANCE_NATIVE_20261026_11H.md
original_pc_source_sha256: 3775AF918F7F157C78ADB9F605E6F1C2EA151023C8C497D6BBC90685FB8376D3
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x4E4830;0x4E48C6;0x4E4988;0x4E4B30;0x4E4B40;0x41034C;0x48E1FC;0x4B9EB4;0x65D150
offset_mentions_untyped: manager+0x3C,+0x40,+0x44,+0x50,+0x54,+0x58,+0x5C
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261026-1015-T028-SPATIAL-INSERT-TWO-MODES-01;B-20261026-1217-T028-DUAL-GRID-INITIAL-COUNTS-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md;REF_UNIT_EXP_SUMMON.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
先行Bの限定x86報告ではmanager constructorがmode=0を書き、別set-contextの二つの直接callerがALでmode 0/1を選ぶ。gridサイズ・shiftがモードで異なる一方、その正確なゲーム上の役割、間接caller/alias、実行時再設定の完備性は未確定。12Hが128側の初期count導出を補足する。

## Limits and curator next gate
合法な2 callerの到達条件とmode writer全体を限定確認。格子の上書き・解除挙動は実機未検証。

The authorized PC source Markdown SHA-256 was remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. The native instructions, indirect calls, full ABI and actual original-game behavior were **not independently revalidated in this intake**. Addresses are source report references, **not** a new semantic or ABI claim. No original binaries, raw saves, decoded protected material, or other-owner research included. All earlier safety HOLD, missing-source and denied-content gates remain unchanged; G4 external-result commit unproven.
