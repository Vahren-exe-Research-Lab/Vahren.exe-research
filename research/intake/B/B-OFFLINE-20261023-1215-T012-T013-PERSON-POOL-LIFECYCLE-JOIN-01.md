# Person candidate vector lifecycle is distinct from death cleanup vectors

- research_id: `B-OFFLINE-20261023-1215-T012-T013-PERSON-POOL-LIFECYCLE-JOIN-01`
- tasks: T012/T013
- source_relative_path: `data/B_T012_T013_PERSON_POOL_LIFECYCLE_OFFLINE_20261023_1215.md`
- source_sha256: `7bdea3e0e2fd16345ebfb84d759d3714e3e586b9792b3f4d061d97dee5c2dcf3`
- prior_ids: B-OFFLINE-20261023-1109-T012-T013-UNIT-VSLOT70-LIVEVECTOR-01 (prior candidate loop), old group/death research
- owner: B
- observed_at: historical owner study, recovered 2026-11-02 JST
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, not new executable hash measurement)
- source_verification: authorized PC Markdown UTF-8 SHA-256 and byte length recalculated during this recovery; matched safe recovery catalog
- supersedes/errata: no override of another source; verify existing corrections against develop REF
- evidence_kind: historical STATIC-ASM/STATIC-GHIDRA when expressly attributed, INFERRED/VERIFY; NO new native independent check in this intake
- golden_status: original gameplay PASS 0, strict MATCH 0, DYNAMIC 0
- ready_status: newly READY 0, E MASTER update 0
- intake_status: PUBLISHED_INTAKE after exact GitHub readback; NOT CURATED by this owner
- restrictions: exclude prior safety-refused records and locations; no original binaries, internal DB, credentials, private machine identity or unapproved data.

## Reusable historical evidence, corrections and limits
- Old Ghidra pseudo-C distinguishes `Person+0x48/+0x4C/+0x50` vector initialization `0x514740`, logical clear `0x5149C0`, per-element virtual cleanup `0x514AA0`, and container destructor candidate `0x5148A0`.
- A death path `0x575DF0 → 0x5684B0` works on a GROUP vector; adjacent `0x575E2E → 0x4C22B0` operates another manager vector. These are NOT proven aliases of the Person+0x48 candidate list that `0x547DB0` traverses.
- Historic report checked 15 pseudo-C SHA entries, 32 markers, 6 direct calls from OLD index, and noted no fresh original-PE ASM direct check. Therefore any live vector compaction, skipped next target or actual unit death consequence is VERIFY, not established.
- Recheck: authorized V9 for `0x514740,0x5149C0,0x514AA0,0x5148A0,0x5684B0,0x4C22B0`, confirm ownership and whether one legally observed target deletion changes the list before next dispatch. G4 death/EXP writer contract remains unproved.

## Proof boundary
Retained original research interpretation with limited static provenance, **not** a new independent x86 byte check, gameplay observation, ABI or persistent state contract. Curator must compare source SHA, per-site original ASM and DAT, prior ID/errata, and all other owners before formal REF/dictionary adoption.
