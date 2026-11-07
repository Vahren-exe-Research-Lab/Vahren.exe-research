# JSON receipt recovery 1

Base: `68c228b1`. Checked: 2026-11-05. This batch extends portable plain-text reference coverage to the ten explicitly approved 2026-11-01 08H through 16H readback receipt JSON files, including the separate 16H conversation-final receipt.

## Result and boundary

10 exact byte archives; 0 privacy variants; 0 aliases; 0 deferred. All ten approved source SHA256 values and byte counts matched; all ten archive JSON bodies parsed and matched their sources byte for byte. All ten were present with matching hashes in the permitted source catalog. No exact body hash alias appeared in the permitted baseline source manifest, recovery ledger, or this batch. The nine-column `REPORT_LEDGER.tsv` follows the baseline recovery ledger column order. `DEFERRED.tsv` retains its source_path column and has no data rows.

Only the approved original JSON bodies and permitted baseline metadata were read. No referenced native file, script, log, executable, database, handoff, archive, or evidence payload was opened. The receipt bodies contain opaque filenames, declared digests, statuses, and audit counts rather than substantive held native/dependency bodies. Personal root path scan and full review found no personal root token; no transformation or reserialization was applied. Source originals and shared repository files were not changed.

## Observed JSON kinds

All ten are JSON objects. 08H-12H contain four-item `files` arrays; 13H contains a four-entry `files` object map; 14H, 15H, 16H, and conversation-final 16H contain four-item `manifest` arrays. Identifier fields vary: `research_id`, `id` (12H), and `run_id` (13H). `JSON_SCHEMA_RECEIPT.json` records observed top-level shapes only, not a canonical schema. Unknown fields remain archival data.

The reported IDs and filenames label 08H group1E caller AL postcall; 09H group34 weighted sqrt; 10H proximity gate; 11H dual bucket gate; 12H dual-list mode3 vector; 13H distance-sort mode gate; 14H distance comparator boundary; 15H NaN comparator transitivity; and 16H midpoint SAR rounding/overflow. These are metadata correlations, not independently established implementation facts. Each receipt declares four linked artifacts. `CORRELATION_METADATA.json` preserves their reported names and audit metadata without opening them.

## Claim limits and correction data

PASS/readback counts, source checks, assertions, grid-pair counts, and earlier receipt checks are the author's dated offline/static/synthetic or Library audit claims. They do not establish current local synchronization, linked artifact integrity, original-game Golden PASS, strict MATCH, new READY, or native/runtime correctness. No `current_result` field was observed; any future similarly named field must remain an author claim until independently scoped and verified. No pilot or search coverage claim is promoted by indexing these JSON receipts.

The two 16H receipts share the reported research ID and the four artifact filenames, byte counts, and digests, but have different receipt bytes/hashes. The initial receipt reports `library_uploaded: false`, per-entry `library_materialized_readback: false`, and `library_readback: PENDING`. The conversation-final receipt changes the first two statuses to true, replaces the Library readback text with an author PASS 5/5 claim expressly tested before the final receipt update, and adds a Library reference string and count 5. Both are retained separately; neither overrides the other as a current fact. The original Library reference string is retained exactly, including its observed encoding appearance. Neither receipt reports local PC synchronization or original-game validation.

## Evidence files

- `INPUT_SELECTION_RECEIPT.json`: exact approved selection, source hash/size and catalog checks, baseline alias check, decisions and counts.
- `ID_RECEIPT.json`: verbatim reported identifier and identifier field for each receipt.
- `TRANSFORM_RECEIPT.json`: no-transform decisions, equal input/output hashes and zero privacy token offsets.
- `JSON_SCHEMA_RECEIPT.json`: observed JSON shape only.
- `CORRELATION_METADATA.json`: opaque reported linkage metadata; no dereferencing.
- `SHA_VERIFICATION.tsv`: per-source/destination byte, hash and JSON parse results.
- `VALIDATION_RECEIPT.json`: aggregate bounded-review verification.
- `REPORT_LEDGER.tsv`: nine-column recovery record; `DEFERRED.tsv`: empty deferred-source record.
- `archive/`: exact approved receipt byte bodies, each stored once.

## Parent digest links to recovered reports

The40 declared artifacts were compared only with the fixed baseline recovery ledger. Seven declared digests match saved bytes; three others match original-digest receipts whose published bodies are privacy derivatives. The30 unmatched artifact references are not proven missing or unpublished. No linked original, native evidence, script or log was opened. These ten links are not ten newly validated discoveries. See [complete linkage receipt](MANIFEST_LINKS.tsv).

- [B_OFFLINE_20261101_08H_READBACK_RECEIPT.json](archive/B_OFFLINE_20261101_08H_READBACK_RECEIPT.json) → [T011_T013_GROUP1E_ALL25_CALLER_AL_POSTCALL_NATIVE_20261101_08H.md](../../../research/recovered/b_reports/T011_T013_GROUP1E_ALL25_CALLER_AL_POSTCALL_NATIVE_20261101_08H.md) — `EXACT_SAVED_BYTES`
- [B_OFFLINE_20261101_09H_READBACK_RECEIPT.json](archive/B_OFFLINE_20261101_09H_READBACK_RECEIPT.json) → [T011_T013_GROUP34_WEIGHTED_SQRT_AL1_NATIVE_20261101_09H.md](../../../research/recovered/b_batch3/T011_T013_GROUP34_WEIGHTED_SQRT_AL1_NATIVE_20261101_09H.md) — `EXACT_SAVED_BYTES`
- [B_OFFLINE_20261101_10H_READBACK_RECEIPT.json](archive/B_OFFLINE_20261101_10H_READBACK_RECEIPT.json) → [T011_T024_GROUP34_PROXIMITY_RATIO_100TICK_NATIVE_20261101_10H.sanitized.md](../../../research/recovered/b_reports/T011_T024_GROUP34_PROXIMITY_RATIO_100TICK_NATIVE_20261101_10H.sanitized.md) — `ORIGINAL_DIGEST_RECEIPT_ONLY`
- [B_OFFLINE_20261101_11H_READBACK_RECEIPT.json](archive/B_OFFLINE_20261101_11H_READBACK_RECEIPT.json) → [T011_T024_GROUP34_DUAL_BUCKET_ELIGIBILITY_NATIVE_20261101_11H.md](../../../research/recovered/b_reports/T011_T024_GROUP34_DUAL_BUCKET_ELIGIBILITY_NATIVE_20261101_11H.md) — `EXACT_SAVED_BYTES`
- [B_OFFLINE_20261101_12H_READBACK_RECEIPT.json](archive/B_OFFLINE_20261101_12H_READBACK_RECEIPT.json) → [T011_T024_DUAL_LIST_MODE3_VECTOR_NATIVE_20261101_12H.md](../../../research/recovered/b_reports/T011_T024_DUAL_LIST_MODE3_VECTOR_NATIVE_20261101_12H.md) — `EXACT_SAVED_BYTES`
- [B_OFFLINE_20261101_13H_READBACK_RECEIPT.json](archive/B_OFFLINE_20261101_13H_READBACK_RECEIPT.json) → [B-OFFLINE-20261101-13H-T011-T024-DISTANCE-SORT-MODE-GATE-01.md](../../../research/intake/B/B-OFFLINE-20261101-13H-T011-T024-DISTANCE-SORT-MODE-GATE-01.md) — `ORIGINAL_DIGEST_RECEIPT_ONLY`
- [B_OFFLINE_20261101_14H_READBACK_RECEIPT.json](archive/B_OFFLINE_20261101_14H_READBACK_RECEIPT.json) → [B-OFFLINE-20261101-14H-T011-T024-DISTANCE-COMPARE-BOUNDARY-01.md](../../../research/intake/B/B-OFFLINE-20261101-14H-T011-T024-DISTANCE-COMPARE-BOUNDARY-01.md) — `ORIGINAL_DIGEST_RECEIPT_ONLY`
- [B_OFFLINE_20261101_15H_READBACK_RECEIPT.json](archive/B_OFFLINE_20261101_15H_READBACK_RECEIPT.json) → [T011_T024_DISTANCE_NAN_COMPARATOR_NONTRANSITIVE_OFFLINE_20261101_15H.md](../../../research/recovered/b_batch6/data/T011_T024_DISTANCE_NAN_COMPARATOR_NONTRANSITIVE_OFFLINE_20261101_15H.md) — `EXACT_SAVED_BYTES`
- [B_OFFLINE_20261101_16H_READBACK_RECEIPT.json](archive/B_OFFLINE_20261101_16H_READBACK_RECEIPT.json) → [T011_T024_NATIVE_MIDPOINT_SAR_ROUNDING_OVERFLOW_OFFLINE_20261101_16H.md](../../../research/recovered/b_batch6/data/T011_T024_NATIVE_MIDPOINT_SAR_ROUNDING_OVERFLOW_OFFLINE_20261101_16H.md) — `EXACT_SAVED_BYTES`
- [B_OFFLINE_20261101_16H_READBACK_RECEIPT_CONVERSATION_FINAL.json](archive/B_OFFLINE_20261101_16H_READBACK_RECEIPT_CONVERSATION_FINAL.json) → [T011_T024_NATIVE_MIDPOINT_SAR_ROUNDING_OVERFLOW_OFFLINE_20261101_16H.md](../../../research/recovered/b_batch6/data/T011_T024_NATIVE_MIDPOINT_SAR_ROUNDING_OVERFLOW_OFFLINE_20261101_16H.md) — `EXACT_SAVED_BYTES`

## Later recovery of declared evidence

[EvidenceJSON follow-up](../json_evidence2/README.md) now preserves nine declared artifacts and proves ten declarations against saved bytes (thetwo16Hreceipts share oneartifact). The earlier MANIFEST_LINKS table remains a fixed historical comparison, not current missing-file status. The follow-up table and its limits distinguish the combined17/3/20 result without claiming original-game validation.
