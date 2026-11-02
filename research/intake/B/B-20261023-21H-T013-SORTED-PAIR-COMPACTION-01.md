# B-20261023-21H-T013-SORTED-PAIR-COMPACTION-01 — Troop-sorted Unit traversal versus packed coordinate-pair ordinal

research_id: B-20261023-21H-T013-SORTED-PAIR-COMPACTION-01
owner: B
research_tasks: T013
source_observed_at: historical B report dated 20261023 (original report, not a new discovery)
source_relative_path: data/T013_TROOP_SORTED_PAIR_COMPACTION_NATIVE_20261023_21H.md
source_report_sha256: 350626A989D348050474C2266ECA4A43C3FBC00E866575A30D75A68CBB5D46A6
source_sha256_reverified: 2026-11-03; authorized research-PC read-only Get-FileHash exact match
original_isolated_exe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (whole-file identity checked this run; player installation untouched)
unified_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE (identity checked this run; native meaning not newly decoded)
evidence_classification: STATIC original-window observations in owner report; historic V3 secondary; VERIFY runtime
Golden_original_game_PASS: 0 new
strict_MATCH: 0 new
READY_new_formal: 0; historical owner-only claims do not create E/MASTER READY
intake_stage: owner-only source preservation on existing private Draft PR; NOT automatically CURATED

## One-paragraph searchable summary (source-reported, bounded)
Owner original-PE windows report separate traversal and assignment ordinals: skipped Unit candidates advance the Unit index without consuming an 8-byte coordinate-pair slot. A second reported path lacks one additional filter. The stable-order inference applies only to small insertion-sort range, not every sorting algorithm or original-game deployment behavior. The previously denied destination/callee inspection remains excluded.

## Native/DAT search hooks (not newly validated ABI)
- Permitted address mentions from this historical owner report: 0x5697F5, 0x5697F8, 0x569801, 0x56981F, 0x569823, 0x569832, 0x569838, 0x569946, 0x569949, 0x569960, 0x569964, 0x569970, 0x569976, 0x44D6A0.
- Offsets/field references: Unit+0x1867C/+0x1F9; pair stride 8 bytes; two independent ordinals.
- Historical links / dedup / correction review: Historical Unit+0x1BC sort-key notes; current V9 proof not inferred from old V3 metadata.
- The above are search/provenance hints only; do not infer native execution, code completeness, ABI or gameplay from this note.

## Limitations, safety and next checks
- Original source: `data/T013_TROOP_SORTED_PAIR_COMPACTION_NATIVE_20261023_21H.md` (PC-only original report, not copied verbatim). Only source report bytes were SHA-rehashed this run. Fresh independent ASM/DAT semantic checks and real original-game Golden were NOT run.
- No refused operation, denied evidence/body, protected native window, or other-owner content was read for this intake; blocked sources remain BLOCKED, not replaced by this note. This file never copies denied bytes.
- Correction and predecessor IDs are pointers, not proof that related IDs share meaning or that an older claim has been superseded.
- Next: Independent current V9 bounded caller validation, eligible original-game formation test with excluded candidates; no inference about denied target implementation.
- Curator action: compare exact source SHA, allowed original ASM/CALL/offset/DAT, current `develop` REF/dictionary, prior errata and selective evidence before any official CURATED_STATIC record. Never merge the divergent owner PR wholesale.
