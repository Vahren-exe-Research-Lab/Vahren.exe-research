# B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01 — B owner historical source intake (verified provenance)

- research_id: `B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01`
- owner: B; tasks: T011; source_observed_at: 2026-10-31 10H JST
- source_relative_path: `data/T011_TRAINING_PARTIAL_ERASE_NATIVE_20261031_10H.md`
- source_sha256_verified_readonly_2026-11-02: `FCFE8992BE8EA58636A958E8BA0E4D615F6EAC4E9DB2455EE45C5B07D0187EF6`; source_bytes: 3943
- original_PE_SHA256_verified_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy; not executed)
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; strict_MATCH: 0; original_dynamic_observed_new: 0
- owner_ready_scope: NOT READY; newly promoted READY=0; intake_status: PUBLISHED_INTAKE only after GitHub readback; new formal CURATED in this run: 0
- VA/CALL sample (role scoped by owner source, not auto ABI): 0x4DEC70;0x4DEC74;0x4DEEBB;0x4DEEC0;0x4DEFCF;0x4F8F70
- offsets (untyped until validated): node+0x15;tree+0x8
- prior_ids/errata: B-20261031-09H-T011-TRAINING-CACHE-BULK-ERASE-NATIVE-01
- develop curation relationship: DEVELOP_REF_STATIC_SCOPE_ALREADY_PRESENT; REF_UNIT_EXP_SUMMON.md and symbols.tsv

## Owner research evidence (sanitized source-derived summary)
Partial node eraser 0x4DEC70 validates an iterator-related byte +0x15 before candidate removal. At 0x4DEEBB it frees a target node, then conditionally decrements map+0x8 and returns an iterator candidate via output pointer. Generic tree rebalancing calls are present but not ABI-proven. Normal T011 cleanup can take bulk eraser instead.

## Correction and supersession boundary
Separates partial per-node path from 09H full-range erase; another independently safety-blocked context was not reexamined.

## VERIFY / safety / next
- Limitations: Invalid iterator behavior, exact C++ type, iterator stability/exception propagation and runtime invocation VERIFY.
- Next legal verification: 11H explains pre-delete successor preservation; curator must retain bounded STATIC/VERIFY.
- Original owner report sections and original PE windows are the evidence source. This summary does **not** independently redecompile or establish full C++ types, native ABI, game behavior or a safe G4 battle-result commit contract.
- No raw EXE/DAT/SAVE/ZIP, user identity/absolute host path, credentials, denied source body, or experimental game execution included. Blocked operations remain blocked; no other owner, shared REF, dictionary, MASTER or develop changes were authorized.
