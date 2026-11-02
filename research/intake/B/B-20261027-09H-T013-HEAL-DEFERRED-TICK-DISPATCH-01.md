# B-20261027-09H-T013-HEAL-DEFERRED-TICK-DISPATCH-01 — Heal予約登録と後続Task tickの条件付き関係
research_id: B-20261027-09H-T013-HEAL-DEFERRED-TICK-DISPATCH-01
owner: B
tasks: T013,T012
domain: DAMAGE_STATE_EFFECT
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T013_HEAL_DEFERRED_TICK_DISPATCH_NATIVE_20261027_09H.md
original_pc_source_sha256: 71B5971ADFD9A8D1AB5059CB05F804D8EEF27B747574544CC2BF68667744C9DD
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x54E2DE;0x4C2240;0x4C2714;0x4C28D0;0x4C2933;0x4C2999;0x54E420;0x54E31F
offset_mentions_untyped: vtable+0x4,+0x8,+0x24;holder+0xC;manager+0x64,+0x68
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261027-08H-T013-EFFECT-VTABLE-TICK-JOIN-01
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_SKILL_POST_ACTION.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
Bの先行限定x86調査では、Healに関する登録条件とTask tickでの仮想slot+4呼出・pending queue mergeの順番が示される。pending追加と同一active-list走査での実行は同義ではなく、各管理体が同じインスタンスか、いつ回復が反映されるかはVERIFY。Task/VM所有のP0実装は変更しない。

## Limits and curator next gate
許可されたowner T013の元CALLとholder/managerの同一性を別証拠で検査し、HP/MP/RNGや最終対象効果は原作比較まで未確定とする。

The authorized PC source Markdown SHA-256 was independently remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. Previously reported native instructions, indirect calls, full ABI and original-game behavior were **not independently revalidated by this intake**. Numeric addresses refer to prior source mentions, not a newly proven call contract. No original binaries, raw saves, protected evidence, or other-owner material was published. Prior safety HOLD, missing-source and denied-operation gates remain; G4 external-result settlement not proven.
