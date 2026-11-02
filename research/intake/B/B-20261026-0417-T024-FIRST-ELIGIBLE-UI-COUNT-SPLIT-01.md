# B-20261026-0417-T024-FIRST-ELIGIBLE-UI-COUNT-SPLIT-01 — mode別の初回eligible owner/全owner UI候補数計算差
research_id: B-20261026-0417-T024-FIRST-ELIGIBLE-UI-COUNT-SPLIT-01
owner: B
tasks: T024,T013
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T024_FIRST_ELIGIBLE_UI_COUNT_SPLIT_NATIVE_20261026_04H.md
original_pc_source_sha256: 77D24D0DB964A9731E368990406284B7238BF3F032B2F3489179FD534935FA05
sha_checked_at: 2026-11-03 JST on authorized PC read-only SHA256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED_UI,VERIFY
source_address_mentions: 0x41EF50;0x41EFE9;0x41F0C1;0x41F0CF;0x41F0E2;0x41F3BA;0x41F5AD;0x41F5E9
offset_mentions_untyped: owner+0xC;owner+0x10;Unit+0x8C;Unit+0x1F8;owner+0x1C
prior_research_ids_for_crosslink: B-20261026-0310-T024-MODE-PARAM-FILTER-TWO-CALLERS-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Distinct owner-reported historical scope
A historical static x86 report on `0x41EF50` distinguishes a mode0 candidate-display branch that selects **the first eligible owner** and counts that owner's inner elements plus a base offset, from a nonzero-mode branch that counts **eligible owners** across an outer vector plus the same base. Both later cap a presented count. Subsequent branches enumerate the single selected owner's inner items versus multiple owners for display. This is owner-described UI/list population, **not** evidence of AI attack-target count or completed battle behavior. Any earlier V3 details are legacy background only; source must be checked against current V9 and original PE before curation.

## Curator verification gate
Independently verify current V9 calls and original x86 branch relation, the zero-length inner vector guard, and legal old-game display counts under mode changes. Prior fallback/27-cap evidence is not new.

This private B intake note records the existing owner source at an independently remeasured file SHA256; original ASM/DAT semantics were **not** independently confirmed in this intake. PE and unified V9 SHA checks establish only identity. No actual game Golden or strict MATCH, no new READY, no G4 external-result bridge proof, and no other-owner, develop REF/dictionary or forbidden source material was published.
