# B-20261031-07H-T011-TRAINING-LEADER-BONUS-MEMO-01 — B owner historical source intake (verified provenance)

- research_id: `B-20261031-07H-T011-TRAINING-LEADER-BONUS-MEMO-01`
- owner: B; tasks: T011; source_observed_at: 2026-10-31 07H JST
- source_relative_path: `data/T011_TRAINING_LEADER_BONUS_MEMO_NATIVE_20261031_07H.md`
- source_sha256_verified_readonly_2026-11-02: `FA2E1295E2C93A15482F6DB4A3B4AF3F03935054EF5959E6F3D1D2AB2167499C`; source_bytes: 6210
- original_PE_SHA256_verified_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy; not executed)
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; strict_MATCH: 0; original_dynamic_observed_new: 0
- owner_ready_scope: NOT READY; newly promoted READY=0; intake_status: PUBLISHED_INTAKE only after GitHub readback; new formal CURATED in this run: 0
- VA/CALL sample (role scoped by owner source, not auto ABI): 0x4722BE;0x4722D3;0x4723A8;0x4723BC;0x4F8A80;0x4ED3B0;0x474A80;0x583DC0
- offsets (untyped until validated): node+0xC;node+0x10;Skill+0x2B0;local+0x94
- prior_ids/errata: B-20261031-06H-T011-TRAINING-COUNT-PROVENANCE-01
- develop curation relationship: DEVELOP_REF_STATIC_SCOPE_ALREADY_PRESENT; REF_UNIT_EXP_SUMMON.md

## Owner research evidence (sanitized source-derived summary)
0x583DC0 supplies candidate leader; temporary tree lookup 0x4F8A80 keys by leader pointer. On hit, node+0x10 holds the cached training bonus B. On miss, the leader Skill training bonus from +0x2B0 is used and an allocated (leader pointer,B) pair is passed through 0x4ED3B0/0x474A80 for insertion. This memo is not permanent Unit identity.

## Correction and supersession boundary
Supersedes 06H interpretation that node+0x10 and Skill+0x2B0 might denote separate effects; their meanings connect through the same temporary leader-bonus cache. Earlier dev_lab §62.1 training leader meaning is prior art.

## VERIFY / safety / next
- Limitations: Map lifetime, invalid pointers, duplicate keys, overflow, side effects and legal training observed outcomes remain VERIFY.
- Next legal verification: Correlate temporary-map initialization/cleanup studies 08H–11H; do not count as new develop CURATED or Golden.
- Original owner report sections and original PE windows are the evidence source. This summary does **not** independently redecompile or establish full C++ types, native ABI, game behavior or a safe G4 battle-result commit contract.
- No raw EXE/DAT/SAVE/ZIP, user identity/absolute host path, credentials, denied source body, or experimental game execution included. Blocked operations remain blocked; no other owner, shared REF, dictionary, MASTER or develop changes were authorized.
