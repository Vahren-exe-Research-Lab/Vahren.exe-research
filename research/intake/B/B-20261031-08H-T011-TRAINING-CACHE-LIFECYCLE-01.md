# B-20261031-08H-T011-TRAINING-CACHE-LIFECYCLE-01 — B owner historical source intake (verified provenance)

- research_id: `B-20261031-08H-T011-TRAINING-CACHE-LIFECYCLE-01`
- owner: B; tasks: T011; source_observed_at: 2026-10-31 08H JST
- source_relative_path: `data/T011_TRAINING_CACHE_INIT_ERASE_DUPLICATE_NATIVE_20261031_08H.md`
- source_sha256_verified_readonly_2026-11-02: `B79044AE9C8AE40FE3F59E06DD056E0D73DAABEC3D98B784C628737A2EACE1EF`; source_bytes: 5664
- original_PE_SHA256_verified_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy; not executed)
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; strict_MATCH: 0; original_dynamic_observed_new: 0
- owner_ready_scope: NOT READY; newly promoted READY=0; intake_status: PUBLISHED_INTAKE only after GitHub readback; new formal CURATED in this run: 0
- VA/CALL sample (role scoped by owner source, not auto ABI): 0x472091;0x49ED90;0x4726C1;0x4DEF40;0x4726D9;0x474B30
- offsets (untyped until validated): local+0x94;local+0x98;node+0xC;node+0x10;node+0x15;map+0x8
- prior_ids/errata: B-20261031-07H-T011-TRAINING-LEADER-BONUS-MEMO-01
- develop curation relationship: DEVELOP_REF_STATIC_SCOPE_ALREADY_PRESENT; REF_UNIT_EXP_SUMMON.md and symbols.tsv

## Owner research evidence (sanitized source-derived summary)
At 0x472091 the caller initializes a temporary training-bonus tree. 0x49ED90 allocates 24-byte sentinel and self-links children/parent; 0x4726C1 calls 0x4DEF40 for range deletion and 0x4726D9 frees sentinel. Duplicate-key insert path 0x474B30 can discard the incoming node, while current unit's precomputed base+B need not depend on insert success.

## Correction and supersession boundary
Extends 07H cache hit/miss and 10/11 dev_lab prior note; generic tree semantics and exception cleanup are not independently established.

## VERIFY / safety / next
- Limitations: All exit/exception paths, exact map type and multi-turn lifecycle remain VERIFY. No observed game EXP.
- Next legal verification: Link bulk erase 09H and partial 10H–11H; avoid declaring safe memory lifecycle in every path.
- Original owner report sections and original PE windows are the evidence source. This summary does **not** independently redecompile or establish full C++ types, native ABI, game behavior or a safe G4 battle-result commit contract.
- No raw EXE/DAT/SAVE/ZIP, user identity/absolute host path, credentials, denied source body, or experimental game execution included. Blocked operations remain blocked; no other owner, shared REF, dictionary, MASTER or develop changes were authorized.
