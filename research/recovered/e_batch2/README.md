# E authored-report recovery batch 2

Checked 2026-11-05 against baseline 43233091. This batch contains 45 approved literal source paths, 40 distinct authored Markdown bodies, five source-path aliases and zero deferred approved paths.

38 new bodies are exact byte copies; two new bodies are complete privacy-only derivatives. Four exact-copy aliases use ALREADY_PRESENT_EXACT_ALIAS. The remaining alias points to the complete privacy derivative of the wrapper fingerprint report and uses CONTENT_REVIEWED_VARIANT, because its destination SHA differs from its original source SHA. Thus the root-format ledger has 38 CONTENT_REVIEWED_EXACT rows, four ALREADY_PRESENT_EXACT_ALIAS rows and three CONTENT_REVIEWED_VARIANT rows. The five aliases create no duplicate body files. No source SHA matched baseline SOURCE_MANIFEST metadata.

## Scope and review

The sole direct input path list was the parent-approved 45-row batch TSV. Every approved path was checked against current RESEARCH_SOURCE_CATALOG metadata (E owner, SHA256, byte count), then hashed from the read-only source. All 40 unique bodies received complete bounded text review; the five repeated source bodies were verified by full-byte identity. UTF-8 decoding was strict. Per-report review findings are recorded in REPORT_LEDGER.tsv. Synced project files and original research files were not edited.

The binding research/recovered/e_reports/SCOPE_AUDIT.md exclusions remain in force. Excluded reports, native/code payloads, linked reports, JSON, logs, scripts, SQLite, archives, HANDOFF sources and game files were not opened or executed for this recovery. References to held native addresses inside these allowed reports are historical BLOCKED continuity statements, not newly acquired native evidence. No broad source search, related-source expansion, Git operation, build, shared code/dictionary update or root-ledger edit was performed.

SOURCE_MANIFEST.tsv and RESEARCH_SOURCE_CATALOG.tsv were used only as permitted metadata. No baseline canonical SHA match was found; canonical destinations in this batch were created once per source-body SHA. Parent integration remains separate.

## Evidence boundaries

These are historical authored reports, including design-only work, synthetic acceptance tests, source-document crosswalks and reported replays of archived native observations. Historical PASS counts are retained as report claims; recovery executed none of those tests and did not reproduce their underlying evidence. Counts overlap across generations and must not be summed as independent original battles or new tests.

The reports distinguish static CALL reachability, registration, callback, UI display, script effect and strategic World changes. They also distinguish sampled mode/active windows, SAVE provenance, battle epochs, MAP and deployed roster identity. A matching SHA, PID, pointer, label, counter or schema does not establish actual same-battle Golden evidence.

Recovery adds zero native/runtime observations, zero actual Golden PASS, zero strict MATCH and zero formal READY. Old MASTER/checkpoint values are historical report context, not current project status. Stored partial original observations are not erased or promoted.

## Files and privacy proof

- REPORT_LEDGER.tsv: nine parent integration columns; paths are original-relative and repository-relative.
- IDENTITY_RECEIPTS.tsv: per-path current source SHA/size, catalog checks, destination readback SHA/size and alias status.
- TRANSFORM_RECEIPTS.tsv: two complete transformations. Only one personal absolute-path token per unique body was replaced; the original token is represented by its byte length and SHA, never reproduced in metadata.
- DEFERRED.tsv: header only; zero approved paths deferred. Earlier exclusions are outside this batch and remain excluded.
- reports/: 40 canonical Markdown body files preserving all source text except the two documented privacy substitutions.

For both derivatives, expected destination bytes were independently regenerated from the entire current UTF-8 source with the single literal substitution and compared byte-for-byte against readback. Every other source/destination pair was compared byte-for-byte. All 45 source hashes were checked again after copying. Generated bodies and metadata were scanned for personal absolute home paths.

## Input identity receipts

- Approved batch TSV SHA256: 0a050f05ad4e33ccd7ad8eeb7284a3aeb26c67b653b02172e0e3768db18c2270
- RESEARCH_SOURCE_CATALOG.tsv SHA256: f14e3bd401a836039f678e9238c6490e2200385efb0fbb602e62f626ec679cf4
- SOURCE_MANIFEST.tsv SHA256: 856937e4b37ac8975d3b90b62c55184041e917376148c3c20e7845d1f05e55c2

Final verification: 45 ledger rows, 40 unique destinations, five aliases, 38 exact new bodies, two privacy-only new bodies, zero deferred; all source and destination identities matched and complete transformation equality passed.
## Navigation

[New reviewed reports](reports/) · [Source path and alias ledger](REPORT_LEDGER.tsv)
