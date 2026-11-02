# B-20261027-0411-T028-CACHE-INSERT-CALLER-SPLIT-01 — 経路キャッシュ挿入結果と別所有mapの共有primitiveの分離
research_id: B-20261027-0411-T028-CACHE-INSERT-CALLER-SPLIT-01
owner: B
tasks: T028,T011
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_CACHE_INSERT_RESULT_NOT_CONSUMED_AND_SHARED_HASH_NATIVE_20261027_04H.md
original_pc_source_sha256: 72D7D665869215D132A8C8D3141D7378A7CEE80A433B12F37C8B2741F5526600
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x4EC4BD;0x4ED350;0x4EC4CC;0x4EC640;0x4FC710;0x4FACA0;0x4FAE99;0x4FAF20;0x54F0B1;0x5797C6
offset_mentions_untyped: result+0x4;route_order+0xAC;other_map+0x10C
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261027-03H-T028-CACHE-UNIQUE-INSERT-ROLLBACK-01;B-20261027-0216-T028-CACHE-ERASE-PAYLOAD-OWNER-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md;REF_UNIT_EXP_SUMMON.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
既存Bの限定元ASM報告では、route-cache側callerはunique-insertの戻りフラグを参照する分岐を挟まずにorder-list appendへ進む。一方、別object側mapも共通insert helperを使用するが、mapとroute-cacheが同じ所有者・寿命とは示されない。03Hのgeneric重複rollbackとcaller側消費は区別する。

## Limits and curator next gate
許可範囲の元ASMで返却構造のalias consumer、重複key到達性、別mapの所有・寿命を限定検査。全cacheで重複しないとは断定しない。

The authorized PC source Markdown SHA-256 was remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. The native instructions, indirect calls, full ABI and actual original-game behavior were **not independently revalidated in this intake**. Addresses are source report references, **not** a new semantic or ABI claim. No original binaries, raw saves, decoded protected material, or other-owner research included. All earlier safety HOLD, missing-source and denied-content gates remain unchanged; G4 external-result commit unproven.
