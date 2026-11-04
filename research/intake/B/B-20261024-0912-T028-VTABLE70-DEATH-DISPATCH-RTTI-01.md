# B-20261024-0912-T028-VTABLE70-DEATH-DISPATCH-RTTI-01 — B owner historical source intake (verified provenance)

- research_id: `B-20261024-0912-T028-VTABLE70-DEATH-DISPATCH-RTTI-01`
- owner: B; tasks: T028,T012,T011; source_observed_at: 2026-10-24 09:12 JST
- source_relative_path: `data/T028_VTABLE70_FOURCLASS_DEATH_DISPATCH_RTTI_NATIVE_20261024_0912.md`
- source_sha256_verified_readonly_2026-11-02: `DEE9D0671B79F2F37EBD6B8A8E4243722B1DE941D1FB6B3B78E0DABE9F1FCA5A`; source_bytes: 5329
- original_PE_SHA256_verified_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy; not executed)
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; strict_MATCH: 0; original_dynamic_observed_new: 0
- owner_ready_scope: historical owner NOT READY; newly promoted READY=0; intake_status: PUBLISHED_INTAKE only after GitHub readback; new formal CURATED in this run: 0
- VA/CALL sample (role scoped by owner source, not auto ABI): 0x63A4BC;0x63A9E4;0x63A85C;0x63A8E4;0x544790;0x578370;0x55ABA0;0x55B060;0x55ABBF;0x55B07D
- offsets (untyped until validated): vtable+0x70;Unit+0x90;Unit+0x1867C;COL+0x0C
- prior_ids/errata: B-20261013-1905-01
- develop curation relationship: NO_EXACT_ID_IN_REVIEWED_DEVELOP_REFS

## Owner research evidence (sanitized source-derived summary)
Source-original PE RTTI maps SimpleUnit table 0x63A4BC to slot+0x70=0x544790; Unit table 0x63A9E4 to 0x578370; StaticUnit 0x63A85C to 0x55ABA0; SimpleStaticUnit 0x63A8E4 to 0x55B060. Bounded native StaticUnit and SimpleStaticUnit paths gate on +0x1867C and subtract damage at +0x90 before HP threshold branches. A direct-CALL search returning none cannot disprove indirect virtual dispatch. The source report [TABLE ...], [NATIVE ...], [RDATA SHA] gives PE pointer and RTTI evidence.

## Correction and supersession boundary
ERRATUM: historical B-20261013-1905-01 mislabeled vtable 0x63A9E4 as SimpleUnit; RTTI identifies it as Unit. SimpleUnit is 0x63A4BC. Preserve vtable raw entries; correct type labels only.

## VERIFY / safety / next
- Limitations: Actual runtime vptr, virtual dispatch reachability, death effects, HP/UI/RNG and postbattle world-state/EXP commit have no legal original-game Golden. Do not elevate RTTI class label to validated game event.
- Next legal verification: Curator verify original PE table/RTTI and register erratum against HP-lifebar report; independently establish indirect virtual callers and battle-exit consequences.
- Original owner report sections and original PE windows are the evidence source. This summary does **not** independently redecompile or establish full C++ types, native ABI, game behavior or a safe G4 battle-result commit contract.
- No raw EXE/DAT/SAVE/ZIP, user identity/absolute host path, credentials, denied source body, or experimental game execution included. Blocked operations remain blocked; no other owner, shared REF, dictionary, MASTER or develop changes were authorized.
