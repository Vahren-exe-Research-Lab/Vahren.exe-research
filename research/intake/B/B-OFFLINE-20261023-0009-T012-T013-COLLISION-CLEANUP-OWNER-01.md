# Collision candidate tree and cleanup tree pointer provenance

- research_id: `B-OFFLINE-20261023-0009-T012-T013-COLLISION-CLEANUP-OWNER-01`
- tasks: T012/T013 (T011 context reference)
- source_relative_path: `data/B_T012_T013_COLLISION_CLEANUP_OWNER_OFFLINE_20261023_0009.md`
- source_sha256: `4d82c9cd51f41db3062274d0d899ee30aa59ea34c51fbf779a62405e43248d54`
- prior_ids: Earlier 2026-10-22 T012/T013 collision and owner cleanup studies; do not count helpers as new
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
- Old B source crosschecked direct sites `0x54C97D` and `0x55268A` for different Missile/SimpleMissile routes into `0x515470`; selected `candidate_context` passes `missile+0x78 → manager+0x1D4 → context+0x1C`, then candidate tree at `context+0x68`.
- Cleanup site `0x515438` instead computes `manager+0x68`, using prior range and erase helper CALLs `0x515445 → 0x579AA0` and `0x51545A → 0x510850`. Different pointer expressions are statically demonstrated but distinct runtime allocations are not proven (aliasing may occur).
- This owner study distinguishes route provenance and cleanups, NOT confirmed hit effects, original-game deletion timing or G4 external postbattle side-effect reconciliation.
- Recheck authorized V9 in indicated original direct caller intervals and `0x515470/0x515420` (where permitted); compare pointer identity and pending queue timing in legal original-game scenarios.

## Proof boundary
Retained original research interpretation with limited static provenance, **not** a new independent x86 byte check, gameplay observation, ABI or persistent state contract. Curator must compare source SHA, per-site original ASM and DAT, prior ID/errata, and all other owners before formal REF/dictionary adoption.
