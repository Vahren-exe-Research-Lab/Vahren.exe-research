# E acceptance recovery scope audit

Checked 2026-11-05. Initial content batch selection omitted the explicit pre-existing 2026-10-31 09H-11H exclusion. The tool returned these three excluded authored-report texts:

- `tests/T020_E_T011_BULK_ERASE_ACCEPTANCE_20261031_09H.md`
- `tests/T020_E_T011_PARTIAL_ERASE_ACCEPTANCE_20261031_10H.md`
- `tests/T020_E_T011_SUCCESSOR_BEFORE_ERASE_ACCEPTANCE_20261031_11H.md`

No excluded report was copied or used for summaries, relationships, source selection, verification, or reconstructed evidence. The selection error was reported to the parent curator. Subsequent T013 batches had already completed before the parent hold arrived; further new content reads stopped at the hold. The parent reviewed and expressly approved only the 28 literal paths below for byte-copy and readback. This audit contains identifiers and operation-level facts only, no excluded excerpts.

The final copy process used this literal allowlist directly, checked catalog owner/size/SHA, root-ledger source and SHA exclusion, exact HEAD Markdown SHA exclusion, excluded date/hour/name checks, and metadata-only HOLD21 basename/stem intersections. No referenced native sources, probes, original game files, DBs or archives were opened or executed. The excluded authored-report reads are the scope error explicitly recorded above. DEFERRED.tsv records the three excluded paths and two incomplete encoding reviews.

## Corrected literal allowlist

- `tests/T020_E_T013_ALT_LIST_RESET_ACCEPTANCE_20261031_22H.md`
- `tests/T020_E_T013_BTLLIMIT_CLOCK_ACCEPTANCE_20261031_02H.md`
- `tests/T020_E_T013_BUCKET_MERGE_ACCEPTANCE_20261031_16H.md`
- `tests/T020_E_T013_CATEGORY_WEIGHT_RNG_ACCEPTANCE_20261031_00H.md`
- `tests/T020_E_T013_CATEGORY_WRITER_ACCEPTANCE_20261030_23H.md`
- `tests/T020_E_T013_COORD_GATE_RECT_ACCEPTANCE_20261101_00H.md`
- `tests/T020_E_T013_DRAIN_RESTORE_CAP_ACCEPTANCE_20261031_17H.md`
- `tests/T020_E_T013_DUAL_SCORE_SIGNED_ACCEPTANCE_20261031_12H.md`
- `tests/T020_E_T013_EFFECTIVE_CONTEXT_ACCEPTANCE_20261031_03H.md`
- `tests/T020_E_T013_EMPTY_REPOPULATE_ACCEPTANCE_20261030_20H.md`
- `tests/T020_E_T013_EQUAL_RANGE_ERASE_ACCEPTANCE_20261030_19H.md`
- `tests/T020_E_T013_FIXED_ANCHOR_CORRECTION_ACCEPTANCE_20261031_13H.md`
- `tests/T020_E_T013_HALFBIAS_RNG_EXHAUSTIVE_ACCEPTANCE_20261031_01H.md`
- `tests/T020_E_T013_HEAD_SENTINEL_COORD_ACCEPTANCE_20261031_21H.md`
- `tests/T020_E_T013_KIND8_PREQUEUE_ACCEPTANCE_20261031_15H.md`
- `tests/T020_E_T013_LABEL_WEIGHT_FANOUT_ACCEPTANCE_20261031_04H.md`
- `tests/T020_E_T013_MODE2_DUALGATE_ACCEPTANCE_20261030_15H.md`
- `tests/T020_E_T013_MODE2_PRIMARY_ACCEPTANCE_20261030_14H.md`
- `tests/T020_E_T013_MODE2_RANGE_UNIT_ACCEPTANCE_20261030_18H.md`
- `tests/T020_E_T013_MODE3_EBX_ACCEPTANCE_20261031_05H.md`
- `tests/T020_E_T013_OFF_EXACT_VSLOT_ACCEPTANCE_20261101_02H.md`
- `tests/T020_E_T013_PAIRWISE_DISTANCE_ACCEPTANCE_20261030_16H.md`
- `tests/T020_E_T013_POSTRANK_UNIT8_ACCEPTANCE_20261031_14H.md`
- `tests/T020_E_T013_POSTREFILL_ACCEPTANCE_20261030_21H.md`
- `tests/T020_E_T013_RECT_BOOL_WINAPI_ACCEPTANCE_20261031_23H.md`
- `tests/T020_E_T011_CACHE_LIFECYCLE_ACCEPTANCE_20261031_08H.md`
- `tests/T020_E_T011_LEADER_CACHE_ACCEPTANCE_20261031_07H.md`
- `tests/T020_E_T011_TRAINING_BRANCH_ACCEPTANCE_20261031_06H.md`
