# B-20261031-14H-T013-RANK-CLEANUP-UNIT8-CALLCHAIN-01 — B historic T013 source intake

- research_id: `B-20261031-14H-T013-RANK-CLEANUP-UNIT8-CALLCHAIN-01`
- owner: B
- tasks: T013 (Battle candidate targeting and ordering)
- observed_at: 2026-10-31 14H JST
- source_relative_path: `data/T013_RANK_CLEANUP_TO_PERUNIT_EVENT_CALLCHAIN_NATIVE_20261031_14H.md`
- source_sha256: `f2cb56a3be2401b93a6a62a21f8f942a27ce710c34a9860ebaecf03a2ec30e19` (2026-11-02 JST actual PC report UTF-8 byte SHA256 and file-size verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (prior source target; executable not independently rehashed this intake)
- evidence_va_call_offsets: `0x448E90;0x4492CF/0x4492DB→0x5B6BBB;0x4492FB→0x510850;0x449305→0x5B6BBB;0x449792/0x449959→0x448E90;0x44982B/0x44999D→0x577A20;Unit+0x1867C,+0x8C/+0x1F8/+0x1F9`
- prior_ids_and_corrections: B-20261031-12H-T013-DUAL-SCORE-COMPARATORS-01 and 13H tie correction known, no repeated E8/rank counts
- evidence_kind: historical source STATIC original ASM / V9-index CALL and INFERRED where described, VERIFY for final semantics; original game DYNAMIC=0
- golden_status: original gameplay PASS 0, strict MATCH 0
- ready_status: newly formal READY 0; E MASTER changes 0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback, not CURATED

## Reusable historical findings

Historical original-PE STATIC shows `0x448E90` rank-scoring function cleans transient candidate-vector memory via `0x4492DB`, a temporary tree range via `0x4492FB`, then tree-head through `0x449305`, before a return. No terminal target pointer return was established in this function. After two distinct schedulers call `0x448E90`, each loops over a Unit pointer vector and reaches `0x577A20` with EDX=8 and ECX=Unit under different gates: scheduler A `0x449792...` has extra mode==0 map checks before `0x44982B`, while scheduler B `0x449959...` calls `0x44999D` via a different eligibility chain. Nonzero `Unit+0x1867C` skips local routing. The recipient function has additional `Unit+0x8C/+0x1F8/+0x1F9` gates and conditional RNG / dispatch. This is **post-rank per-unit routing**, not proof final target selection, successful Skill execution, or gameplay.

## Provenance and next verification

Review 15H downstream kind8 report; independently verify allowed scheduler entry and 0x577A20 CALL conditions with V9 and source, avoiding conflation with final G4 writeback. This is a sanitized owner report summary with original relative source and measured SHA, not a new full disassembly or dynamic game validation. Dedicated KB curator alone may compare permitted V9 ASM/DAT, earlier contradictory findings, source ID and correction lineage before entering REF/typed dictionaries/develop. No game executable, DAT, SAVE, giant DB, personal data or refused material included.
