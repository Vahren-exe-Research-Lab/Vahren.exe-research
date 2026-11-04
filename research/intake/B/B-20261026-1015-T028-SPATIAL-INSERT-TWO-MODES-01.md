# B-20261026-1015-T028-SPATIAL-INSERT-TWO-MODES-01 — 空間セル登録のmode別範囲処理とvector挿入候補
research_id: B-20261026-1015-T028-SPATIAL-INSERT-TWO-MODES-01
owner: B
tasks: T028
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_SPATIAL_INSERT_TWO_MODES_NATIVE_20261026_10H.md
original_pc_source_sha256: E907F9054B599F958F25DD3AA9617E2731FAE214BDC74AEBCCB8D0FF4B33F7C8
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x4E4EA0;0x4E4EAA;0x4E4F3C;0x4C1290;0x4C12F0;0x4E4C95;0x5445CA;0x575062
offset_mentions_untyped: manager+0x3C,+0x48,+0x4C,+0x50,+0x5C;Unit+0x220,+0x224
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261026-1113-T028-GRID-CONSTRUCTOR-MODE-PROVENANCE-01;B-20261026-09H-T028-SPATIAL-GRID-DUAL-ERASE-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md;REF_UNIT_EXP_SUMMON.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
B既存限定元ASM報告はmanager mode!=0でポインタcellへの単体storeと範囲外早期return、mode0でclamp後のcell-vector appendを区別する。境界外到達や同セル衝突、実際の死亡・移動後の一貫性はVERIFY。register ABIやゲームバグは確定しない。

## Limits and curator next gate
constructorの合法count/modeと単体storeのcollision条件、解除側との整合を別証拠で検査。

The authorized PC source Markdown SHA-256 was remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. The native instructions, indirect calls, full ABI and actual original-game behavior were **not independently revalidated in this intake**. Addresses are source report references, **not** a new semantic or ABI claim. No original binaries, raw saves, decoded protected material, or other-owner research included. All earlier safety HOLD, missing-source and denied-content gates remain unchanged; G4 external-result commit unproven.
