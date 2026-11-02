# B-20261027-1010-T013-HEAL-FINISH-UNREGISTER-POOL-REUSE-01 — Heal終了時の解除呼出とTask一覧空きの整理候補
research_id: B-20261027-1010-T013-HEAL-FINISH-UNREGISTER-POOL-REUSE-01
owner: B
tasks: T013,T012
domain: DAMAGE_STATE_EFFECT
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T013_HEAL_FINISH_UNREGISTER_POOL_REUSE_NATIVE_20261027_10H.md
original_pc_source_sha256: 4EECF4C3EB91B83D03F182E18B6FEC8C3564D4394356D9B7F1BD095EB6E0681C
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x54E4C9;0x54E4F8;0x54E5BB;0x54E5EE;0x4C22B0;0x4C28D0;0x4C2942;0x4C2999;0x4BC9C0
offset_mentions_untyped: effect+0x6C;holder+0x4;manager+0x3C;vtable+0x34,+0x44,+0x48
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261027-09H-T013-HEAL-DEFERRED-TICK-DISPATCH-01
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_SKILL_POST_ACTION.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
B過去レポートは特定のHeal終了分岐からTask解除・別登録先の削除へ至る複数の直接CALLと、管理体の条件付きNULL-slot compactionを関連付ける。ただし全効果が必ずそのtickで終了する、pool再利用が安全、元HPが変わった等は証明していない。

## Limits and curator next gate
pool lifetime、active/pending同一インスタンス、効果終了の実機時間差と再入を個別に確認。

The authorized PC source Markdown SHA-256 was independently remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. Previously reported native instructions, indirect calls, full ABI and original-game behavior were **not independently revalidated by this intake**. Numeric addresses refer to prior source mentions, not a newly proven call contract. No original binaries, raw saves, protected evidence, or other-owner material was published. Prior safety HOLD, missing-source and denied-operation gates remain; G4 external-result settlement not proven.
