# Skill +0x9F5 production, copy/reparse and downstream gates

- research_id: `B-OFFLINE-20261022-1715-T011-T012-SKILL9F5-WRITER-CONSUMER-01`
- tasks: T011 / T012
- source_relative_path: `data/B_T011_T012_SKILL9F5_WRITER_CONSUMER_OFFLINE_20261022_1715.md`
- source_sha256: `0d1e72bf3b774fe9e2230b27839d74b212fca7bc4c451f2632356a5dc3b9c59c` (actual authorized PC text hash, matched recovered source manifest)
- prior_ids_and_relationships: B-OFFLINE-20261022-1609-T012-MISSILE-POSTREGISTER-01; B-20261019-0408-01 (prior downstream Skill interpretation); no unverified prior correction is overridden
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
- Historical saved pseudo-C associates a large record allocation (`0xA20`) and initialization with `0x599BD0`, `0x599900` and Skill record `+0x9F4/+0x9F5`. `0x599BD0` writes `+0x9F5` after parsing-related branching; hidden registers/void-decompiled return values make the exact DAT condition VERIFY.
- In `0x46FB00`, recorded CALL `0x46FC13→0x46FCE0` (copy) precedes `0x46FC3E→0x599BD0` (reparse), so persistence of the copied byte cannot be assumed.
- Saved CALL map lists `0x582032`, `0x549F42`, `0x54C723`, `0x54D430` as `0x54DA10` users, with prior `0x580280` gate retained as known. The numerical selection helper `0x54D970` had no direct caller in the old index; meaning and reachability remain VERIFY.
- This is old-index STATIC/INFERRED evidence. No fresh original ASM, native ABI, DAT truth condition or end-to-end hit/damage observation was performed in this intake.

## Minimal reproduction/check
Re-open the source report and owner evidence under the authorized PC; inspect current V9 around `0x599BD0,0x46FB00,0x54DA10,0x54D970` and verify copy, parsing and indirect calls independently. Preserve distinctions between Skill record and Missile records.
