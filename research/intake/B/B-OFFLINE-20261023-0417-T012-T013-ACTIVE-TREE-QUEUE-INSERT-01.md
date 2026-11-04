# BattleWnd active tree insertion provenance versus owner registry

- research_id: `B-OFFLINE-20261023-0417-T012-T013-ACTIVE-TREE-QUEUE-INSERT-01`
- tasks: T012 / T013
- source_relative_path: `data/B_T012_T013_BATTLEWND_ACTIVE_TREE_INSERT_OFFLINE_20261023_0417.md`
- source_sha256: `da73199a61768c85bbf0c6dd327cd6b3ec7055bb47f2f7bb814a8fb14b8e1ae9` (actual authorized PC text hash, matched recovered source manifest)
- prior_ids_and_relationships: Earlier owner T012/T013 global-versus-owner queue probes; B-20261023-0417 recovery record; no unverified prior correction is overridden
- supersedes: none asserted; existing conflicting findings require curator errata review
- owner: B
- observed_source_status: historical owner study, STATIC / INFERRED / VERIFY; no new source discovery in this intake
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (previous verified source identification, not a new PE rehash in this run)
- verified_at: 2026-11-02 JST; original report SHA-256 recalculated from authorized PC text bytes and matched the safe recovery manifest
- golden_status: original game PASS 0; strict MATCH 0; DYNAMIC 0
- ready_status: newly confirmed READY 0; E MASTER formal promotion 0
- intake_status: PUBLISHED_INTAKE only after GitHub exact-text readback; NOT automatically CURATED
- safety: excluded pre-existing denied evidence and protected ranges; no prohibited payload, raw game assets or private paths
- limitations: This is a sanitized re-usable summary of an old source report. It does not prove live gameplay, exact ABI, object lifetime or G4 postbattle writeback. Curator must compare the current develop REF/dictionaries, source correction lineage and original ASM before admitting any new semantics.

## Preserved source findings
- Original-byte study distinguished BattleWnd active tree `+0x248`, header `+0x24C`, and per-missile owner path rather than treating them as one registry.
- The source identified `BattleWnd=0x8B8C90` and writes `0x580F24: [generated+0xA8] = 0x8B8C90` and `0x548DBD: [generated+0xA8] = 0x8B8C90`; old native source maps insertion into the global tree and later `0x40E2F0` search/deletion.
- Owner-index registration has an additional Skill `+0x1FD` gate, which does not prove identical conditions for global registration. Alias/lifetime, active-queue execution, target-contact side effects and G4 relevance are VERIFY; no complete battle-result contract is demonstrated.

## Minimal reproduction/check
Read original B ASM and the relevant T012/T013 evidence; inspect `0x51D260,0x580F24,0x548DBD,0x40E2F0` in current V9 and compare registration/deletion triggers. Do not equate static queue registration with rendered or applied damage.
