# B-20261031-11H-T011-PARTIAL-RANGE-SUCCESSOR-PRESERVE-01 — B owner historical source intake (verified provenance)

- research_id: `B-20261031-11H-T011-PARTIAL-RANGE-SUCCESSOR-PRESERVE-01`
- owner: B; tasks: T011; source_observed_at: 2026-10-31 11H JST
- source_relative_path: `data/T011_TRAINING_PARTIAL_RANGE_SUCCESSOR_PRESERVE_NATIVE_20261031_11H.md`
- source_sha256_verified_readonly_2026-11-02: `C391E96E951C1C22E1D02F03C12ECD4E0F7C1F39F1E746316E201C04217F0631`; source_bytes: 4904
- original_PE_SHA256_verified_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy; not executed)
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; strict_MATCH: 0; original_dynamic_observed_new: 0
- owner_ready_scope: NOT READY; newly promoted READY=0; intake_status: PUBLISHED_INTAKE only after GitHub readback; new formal CURATED in this run: 0
- VA/CALL sample (role scoped by owner source, not auto ABI): 0x4DEF6A;0x4DEF74;0x4DEF78;0x4DEF9A;0x4DEFB0;0x4DEFC4;0x4DEFCF;0x4DEFD4;0x4DEFDC
- offsets (untyped until validated): left+0x0;parent+0x4;right+0x8;node+0x15
- prior_ids/errata: B-20261031-09H-T011-TRAINING-CACHE-BULK-ERASE-NATIVE-01;B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01
- develop curation relationship: DEVELOP_REF_STATIC_SCOPE_ALREADY_PRESENT; REF_UNIT_EXP_SUMMON.md and symbols.tsv

## Owner research evidence (sanitized source-derived summary)
Partial-range iteration distinguishes empty begin==end, saves current, finds successor using right subtree or ancestors, stores next iterator, then passes old current to 0x4DEC70. 0x4DEFD4 resumes from precomputed successor after deletion; raw stale node is not used as the next iterator on normal path. This does not establish behavior for malformed trees or exceptional conditions.

## Correction and supersession boundary
Details 09H partial branch and 10H per-node deletion; prior full-range facts not new.

## VERIFY / safety / next
- Limitations: All native ABI signatures, race/reentrancy, abnormal iterator and runtime gameplay effect remain VERIFY. No denied material recovered.
- Next legal verification: Formal KB owner has already noted bounded STATIC in REF/symbols; future work is legal Golden for EXP and summon parent settlement.
- Original owner report sections and original PE windows are the evidence source. This summary does **not** independently redecompile or establish full C++ types, native ABI, game behavior or a safe G4 battle-result commit contract.
- No raw EXE/DAT/SAVE/ZIP, user identity/absolute host path, credentials, denied source body, or experimental game execution included. Blocked operations remain blocked; no other owner, shared REF, dictionary, MASTER or develop changes were authorized.
