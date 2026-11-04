# B-20261024-0015-T013-TROOP-MODE-EXPR-DEDUP-01 — case8式評価・Troop共有mode適用前の重複排除候補
research_id: B-20261024-0015-T013-TROOP-MODE-EXPR-DEDUP-01
owner: B
tasks: T013,T011,T024
domain: TARGET_SELECTION
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T013_TROOP_MODE_EXPR_RTTI_DEDUP_NATIVE_20261024_0015.md
original_pc_source_sha256: 623ADFC2F53703DC931DD7B8F68FE3E50FE143D0C2F7312F83D785FCFB2549C4
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x4B5973;0x4B5976;0x49CCA0;0x49CD4F;0x463CA0;0x476240
offset_mentions_untyped: Unit+0x1D0;context+0xC;mapEntry+0x1C
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261024-0110-T013-CASE8-LIVE-TREE-VECTOR-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md;REF_UNIT_EXP_SUMMON.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
The prior B report relates case8 mode expression/RTTI and string map lookup to a loop that avoids repeating a setter operation for a shared Troop key. Input value range, candidate ordering, missing-string side effects, real Troop identity, final target and original game behavior remain VERIFY. No full ABI or dynamic semantics are concluded.

## Curator next gate
Independently compare allowed original ASM and raw DAT/effective input to owner source and preceding case8 corrections; inspect candidate order and legitimate shared-Troop alias cases. An address mention is not a native or runtime proof.

The authorized PC source Markdown SHA-256 was independently measured. PE and unified V9 SHA-256 confirm identity only, **not** a new ASM or original-game validation. No original binaries, raw saves, protected evidence, or other-owner content included. Previous HOLD, missing-source and denied-operation gates remain; G4 result settlement unproven.
