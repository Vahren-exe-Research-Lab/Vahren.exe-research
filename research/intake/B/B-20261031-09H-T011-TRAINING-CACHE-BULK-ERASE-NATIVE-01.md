# B-20261031-09H-T011-TRAINING-CACHE-BULK-ERASE-NATIVE-01 — B owner historical source intake (verified provenance)

- research_id: `B-20261031-09H-T011-TRAINING-CACHE-BULK-ERASE-NATIVE-01`
- owner: B; tasks: T011; source_observed_at: 2026-10-31 09H JST
- source_relative_path: `data/T011_TRAINING_CACHE_FULL_RANGE_ERASE_NATIVE_20261031_09H.md`
- source_sha256_verified_readonly_2026-11-02: `C54054A10AE7834D10DAA45129B80100048CD98CDAE286324C91E9F784DF24AC`; source_bytes: 5331
- original_PE_SHA256_verified_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy; not executed)
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; strict_MATCH: 0; original_dynamic_observed_new: 0
- owner_ready_scope: NOT READY; newly promoted READY=0; intake_status: PUBLISHED_INTAKE only after GitHub readback; new formal CURATED in this run: 0
- VA/CALL sample (role scoped by owner source, not auto ABI): 0x4726C1;0x4DEF40;0x4DEF57;0x4ED030;0x49F6A0;0x4DEFCF;0x4DEC70
- offsets (untyped until validated): node+0x15;tree+0x4;tree+0x8
- prior_ids/errata: B-20261031-08H-T011-TRAINING-CACHE-LIFECYCLE-01
- develop curation relationship: DEVELOP_REF_STATIC_SCOPE_ALREADY_PRESENT; REF_UNIT_EXP_SUMMON.md and symbols.tsv

## Owner research evidence (sanitized source-derived summary)
0x4DEF40 checks full-range begin==head-leftmost/end==head and can call 0x4ED030 (bulk clear) then return. On other ranges, 0x4DEFCF invokes 0x4DEC70 (per-node fallback). 0x4ED030 and 0x49F6A0 recursively/iteratively free a tree and restore sentinel links/count. These are separate branches, not proof the partial eraser always runs at ordinary training end.

## Correction and supersession boundary
Refines 08H undifferentiated cleanup description. Tree exception guarantees and all ownership states remain unverified.

## VERIFY / safety / next
- Limitations: ABI, malformed tree, allocation failures and all exit path coverage VERIFY; game Golden=0.
- Next legal verification: Cross-check 10H partial helper and 11H iterator preservation before engine port; static curation already exists.
- Original owner report sections and original PE windows are the evidence source. This summary does **not** independently redecompile or establish full C++ types, native ABI, game behavior or a safe G4 battle-result commit contract.
- No raw EXE/DAT/SAVE/ZIP, user identity/absolute host path, credentials, denied source body, or experimental game execution included. Blocked operations remain blocked; no other owner, shared REF, dictionary, MASTER or develop changes were authorized.
