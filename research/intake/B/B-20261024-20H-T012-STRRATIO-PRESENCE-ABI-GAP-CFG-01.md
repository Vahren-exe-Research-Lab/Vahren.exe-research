# B-20261024-20H-T012-STRRATIO-PRESENCE-ABI-GAP-CFG-01 — source-preserved B research

- research_id: `B-20261024-20H-T012-STRRATIO-PRESENCE-ABI-GAP-CFG-01`
- owner: B
- tasks: T012
- observed_at: 2026-10-24 20H JST
- source_relative_path: `data/T012_STR_RATIO_PRESENCE_ABI_AND_SPARSE_CFG_NATIVE_20261024_20H.md`
- source_sha256: `5f786c52427e6810e60fee2d05099b381b1e72787eedf1404addff88f2f862d2` (actual authorized research-PC Markdown byte SHA-256 rechecked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no fresh PE hash in this intake)
- original_source_kind: saved original-PE ASM / V9 or historical index / normalized DAT, as attributed below; current independent runtime = VERIFY
- evidence_va_call_offsets: `0x59CDAA,0x59CDCA,0x59CDCF,0x59CDD1,0x59CDE8,0x464290,0x4647D0,0x46444B, Skill+0x288`
- prior_ids_and_errata: B-OFFLINE-20261024-17H-T012-STR-RATIO-PRESENCE-RET50-01; B-20261024-1917-T012-PRESENCE-GHIDRA-SPARSE-BODY-GAP-01
- supersedes: only expressly mentioned source corrections; other older interpretations remain linked
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: newly READY 0 / formal E MASTER update 0
- intake_stage: OWNER_STAGED; only a successful exact GitHub readback establishes PUBLISHED_INTAKE; not CURATED

## Reusable research evidence

Old original-PE static check for `str_ratio` existence at caller `0x59CDAA..0x59CDD1` sets registers and two stack args before `0x59CDCA→0x464290`, then examines AL. A false result skips the value getter and retains the in-path initialized `Skill+0x288=1.0`. A true result branches to `0x59CDE8→0x4647D0` and stores scaled integer data into `Skill+0x288`; actual property and parent lookup eligibility remain VERIFY. Original `0x464290` has a first header search, second candidate search and bounded super traversal. The 19H five-byte Ghidra body gap `0x46444B..0x46444F` is not a newly discovered semantic block; the historic source found no direct branch-to-gap in its bounded static check. No claim of actual runtime parent depth or damage.

## Limits and next validation

Revalidate specific native stack/hidden-register ABI in V9, limit to accepted DAT and prior 17H/19H corrections; do not promote game behavior. The old owner source and cited sites are the verification authority; this text is a sanitized reusable research note, NOT a new native experiment, complete game-engine contract, or G4 result transaction proof. Independent curator must check original SHA, permitted V9 ASM/DAT, earlier REF/dictionary confidence and correction lineage before adopting semantic facts. No raw executable, original game assets, absolute private paths, token/logs, denied-operation content or large database is published.
