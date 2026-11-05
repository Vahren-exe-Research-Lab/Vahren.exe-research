# Verification

Verified on 2026-11-05 against the literal approved selection and pinned baseline metadata.

| Check | Observed result |
|---|---:|
| Approved source paths | 26 |
| Current original source bytes | 874,085 |
| Current size pins matched | 26 / 26 |
| Complete authored-body reviews | 24 |
| Partial noncontiguous scope reviews | 2 |
| Unopened preholds | 0 |
| Accepted nine-column rows / complete bodies | 23 |
| Whole-file metadata deferrals | 3 |
| Exact copies / full privacy variants | 16 / 7 |
| Privacy token edits: home / account | 19 / 1 |
| Baseline / within-batch aliases | 0 / 0 |
| Catalog exact matches / current-version differences | 15 / 3 |
| Without a catalog hash pin | 8 |
| Pinned baseline ledger rows | 1,545 |

Every accepted body is strict UTF-8. Destination readback checks the complete original or complete privacy derivative, original first-line bytes and all original line endings; mixed CRLF/LF is retained. For every edit, final verification checks original source SHA, destination SHA, UTF-8 half-open token span, token SHA, original prefix/suffix SHA, replacement length and reconstruction from every unchanged intervening byte. The delegated selector-index edit at original UTF-8 offset 66,572, length 14, is independently cross-checked against its reviewer token/prefix/suffix proofs.

All 26 exact source paths partition uniquely into 23 accepted and three deferred rows. All three deferral destinations stay blank. Each nonempty provenance path is checked for exact membership in the approved selection, so no duplicated-prefix or invented source path is introduced. Partial review boundaries distinguish the first 50 lines plus identified scope-match lines from sparse scope matches; unreviewed remainder is not described as a full review. Held files retain metadata only.

Four input receipts pin the selection, source manifest, catalog and exact baseline recovery ledger used. Current original SHA observations are separately pinned before body generation and rechecked at final verification. Three older catalog mismatches are recorded as current-version differences, not silently replaced or treated as failed acquisition.

The final check verifies all artifact rows, body hashes and transformations, accepted/deferred coverage, catalog/current versions, input pins, unique destinations, privacy residue and absence of builder scratch. Only this intake folder was written. No original/shared/root/Git write, linked evidence read, native operation, cleanup, test rerun or new Golden/READY claim occurred.
