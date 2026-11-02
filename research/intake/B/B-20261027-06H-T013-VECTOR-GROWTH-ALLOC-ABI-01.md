# B-20261027-06H-T013-VECTOR-GROWTH-ALLOC-ABI-01 — 支援候補vector拡張と容量不足時allocator経路
research_id: B-20261027-06H-T013-VECTOR-GROWTH-ALLOC-ABI-01
owner: B
tasks: T013
domain: TARGET_SELECTION
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T013_VECTOR_GROWTH_ALLOC_ABI_NATIVE_20261027_06H.md
original_pc_source_sha256: BF9F7A9DA082EF0A0E9969394439EF970DA7E1F661B03EFDD6823EF7FF82E66B
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x57CFD0;0x57D04B;0x57D070;0x57D075;0x515750;0x515790;0x5157A1;0x5B6C2B
offset_mentions_untyped: candidate_stride=24;vector_begin,end,capacity
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261027-0514-T013-SUPPORT-CACHE-REBUILD-VECTOR-01
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_SKILL_POST_ACTION.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
既存B報告によれば支援候補の24-byte stride vectorは容量不足時に別のallocator helperへ移り、要素数の範囲を検査する。元の元ASM範囲は限定的であり、例外時の既存配列維持、構造体正式ABI、最終Heal対象と原作実作用はVERIFY。

## Limits and curator next gate
合法な例外・vector commit境界と最終target consumerを限定照合する。

The authorized PC source Markdown SHA-256 was independently remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. Previously reported native instructions, indirect calls, full ABI and original-game behavior were **not independently revalidated by this intake**. Numeric addresses refer to prior source mentions, not a newly proven call contract. No original binaries, raw saves, protected evidence, or other-owner material was published. Prior safety HOLD, missing-source and denied-operation gates remain; G4 external-result settlement not proven.
