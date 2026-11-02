# B-20261031-06H-T011-TRAINING-COUNT-PROVENANCE-01 — B owner historical source intake (verified provenance)

- research_id: `B-20261031-06H-T011-TRAINING-COUNT-PROVENANCE-01`
- owner: B; tasks: T011; source_observed_at: 2026-10-31 06H JST
- source_relative_path: `data/T011_TRAINING_COUNT_PROVENANCE_NATIVE_20261031_06H.md`
- source_sha256_verified_readonly_2026-11-02: `78FFB6534F0B999C734DA7FB5E4040F0C4C8AE7CE1A74232B94B89D623B20D8A`; source_bytes: 6472
- original_PE_SHA256_verified_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy; not executed)
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; strict_MATCH: 0; original_dynamic_observed_new: 0
- owner_ready_scope: NOT READY; newly promoted READY=0; intake_status: PUBLISHED_INTAKE only after GitHub readback; new formal CURATED in this run: 0
- VA/CALL sample (role scoped by owner source, not auto ABI): 0x472081;0x595320;0x4722D3;0x47238E;0x4723A0;0x58A650
- offsets (untyped until validated): Power+0xD8;skill+0x2B0;node+0x10
- prior_ids/errata: B-20261031-07H-T011-TRAINING-LEADER-BONUS-MEMO-01 (subsequent correction)
- develop curation relationship: DEVELOP_REF_STATIC_SCOPE_ALREADY_PRESENT; REF_UNIT_EXP_SUMMON.md and symbols.tsv

## Owner research evidence (sanitized source-derived summary)
Original x86 0x472081 calls 0x595320 for normalized training_up baseline, sourced from Power override or scenario. The 0x4722D3 and 0x47238E branches add candidate values to base, and 0x4723A0 stores the resulting count. Original DAT snapshot scenario1.dat:30 reports training_up=2 with SHA256 F85C127D452FA5E78DB828EDACC36159EC6450B74F4EBB03DC975B5B3AD6F649. Realized training/EXP changes are not demonstrated.

## Correction and supersession boundary
07H narrows earlier uncertainty: the +0x10 memo value and Skill+0x2B0 source are the same leader-derived bonus, not two independently verified skill effects. Existing 2026-10-11 §61/62.1 helper semantics not a new discovery.

## VERIFY / safety / next
- Limitations: Max-level gates, signed arithmetic, overflow, reachability and native-versus-game outcome remain VERIFY. Modified test DAT cannot substitute for legal original Golden.
- Next legal verification: Read linked 07H evidence and pre-existing REF/SMB symbols before any new semantic curation; legal gameplay training baseline tests still needed.
- Original owner report sections and original PE windows are the evidence source. This summary does **not** independently redecompile or establish full C++ types, native ABI, game behavior or a safe G4 battle-result commit contract.
- No raw EXE/DAT/SAVE/ZIP, user identity/absolute host path, credentials, denied source body, or experimental game execution included. Blocked operations remain blocked; no other owner, shared REF, dictionary, MASTER or develop changes were authorized.
