# Bounded authored search-report recovery

This intake selects exactly 87 Markdown paths from the coordinator's approved selection (550,026 original bytes). It recovers 72 complete authored documents: 59 byte-exact bodies and 13 complete privacy variants with 14 literal home-prefix substitutions. There are no baseline or within-batch aliases and no duplicate bodies. Fifteen whole documents are metadata-only deferrals. Eighty-two bodies received full bounded review; five exact same-study reports were preheld without opening their bodies. Hashing a preheld file is metadata measurement, not body review.

The coordinator-supplied baseline is `2a6af7b389d82a92b85bef475aaf981d31d1990d`, branch `work/kb-residual-reports-20261105`. The baseline recovery ledger contains 1,395 rows. INPUT_RECEIPTS.tsv pins the exact selection and three baseline metadata inputs used here; it does not claim a Git checkout was independently verified. All 87 measured sizes match the supplied current metadata; all 31 catalog-pinned hashes and sizes match. The other 56 have no catalog hash pin, rather than a catalog mismatch.

## Receipts and roles

- REPORT_LEDGER.tsv contains only the 72 accepted rows in the root's nine-column schema. Original-source SHA and destination SHA are separate; privacy variants must not be mistaken for exact original bodies.
- DEFERRED.tsv contains all 15 source paths, current hashes and sizes, review mode, concrete held scope, and an approved-document provenance path. Its destination columns remain blank: no held body or excerpt is copied.
- SELECTION_RECEIPTS.tsv covers all 87 literal paths and distinguishes complete body review from hash-only preholds, current observations from catalog pins, and baseline SHA matches.
- IDENTITY_RECEIPTS.tsv identifies each document by its exact source path and document stem. A stem is not a new canonical study ID; similarly named or same-ID historical revisions remain separate byte versions.
- TRANSFORM_RECEIPTS.tsv records all 14 privacy token edits, original UTF-8 half-open byte offsets, token hashes, original prefix/suffix hashes and destination hashes.
- reports/ preserves the selected index-relative directory structure. Indexes, handoffs, guides and receipts retain their authored roles. Their links and commands are historical text, not an assertion that linked payloads were acquired or instructions to execute.

## Scope and deferrals

Only the literal 87 approved authored Markdown files were eligible. No linked files, native executables, scripts, JSON/log evidence, databases, assets, save data or archive bodies were opened or executed. No original files, shared metadata, code or Git state were changed, and no cleanup or game operation was performed. The approved HANDOFF authored body was reviewed as data; references were not followed.

The whole-file deferrals cover substantive retained/refused 4C28D0 active-task traversal, NULL-slot/pause gates, live frames and continuation dependencies, plus the Stage14 composite's held 5BC860 initialization internals. Stage10, Stage16, Stage17, Stage5 and the P0 scheduler report were preheld from exact same-study references in already reviewed approved documents. Other composite files were deferred after bounded review established substantive held content. No partial extracts were retained. Caller-only references and independent historical operation receipts did not automatically trigger a hold. No blanket hold was inferred from Stage15, report, cleanup or handoff titles.

## Interpretation and source quality

All native/static/dynamic PASS, synthetic PASS, readiness, completion, cleanup and Golden statements remain the original authors' dated claims. Recovery adds no native or runtime evidence, READY/DONE status, Golden credit, result-commit proof or current implementation authority. Current REF limits and prior held scopes remain in force.

Historical index revisions disagree by design. V9's SQLite composite, earlier Ghidra revisions and publication failures are distinct states. Same-ID pre-correction and corrected documents retain separate hashes. The 3,024 presumed E8 edges were later distinguished as 2,040 E8 plus 984 JMP edges; compiler/EH function counts do not measure game-feature coverage. The 48D6A0 body-range correction uses split ranges rather than entry-plus-size arithmetic. Old and corrected map color offsets are preserved as authored, including correction prefaces.

Battle stage observations remain limited samples. Task capture capacities and snapshot budgets are collector limits; raw counters are not atomic, missing HP/MP observations are not zero-filled, shared record aliases are not persistent identities, and unexpected Unit additions are not automatically summon proof. The P0 G3 NOOP and controlled worker exit receipts do not establish full G1/G2/G4/G5/G6, an OS crash recovery, original flags/SEH preservation or an external result commit. ACK and native commit are different; the integration review identifies older terminology and later revisions instead of silently rewriting them.

The cleanup reports describe different dates and outcomes. The blocked attempt, later content-reconstruction claim, and later recovery-artifact disposal notice remain historical records. The first line of GAME_COPY_CLEANUP_COMPLETED_20261101.md and much of GAME_COPY_RECOVERY_DISCARDED_20261101.md contain literal question marks already present in their strict UTF-8 source bytes. These are preserved without reconstruction or guessed translation. No archive existence or recoverability was independently checked.

Privacy variants replace only complete literal personal home prefixes with `[USER_HOME]`. Every other byte, including line endings, obsolete instructions, question marks and authored code examples, is preserved. No summary substitutes for an accepted body.
