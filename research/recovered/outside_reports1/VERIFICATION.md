# Verification

Verified on 2026-11-05.

| Check | Observed result |
|---|---:|
| Exact approved literal source paths | 13 |
| EXP / wiki authored documents | 8 / 5 |
| Current original source bytes | 254,703 |
| Complete / partial body reviews | 13 / 0 |
| Unopened preholds / whole-file deferrals | 0 / 0 |
| Accepted nine-column ledger rows | 13 |
| Exact complete body copies | 13 |
| Privacy variants / token edits | 0 / 0 |
| Baseline / within-batch aliases | 0 / 0 |
| Current size and historical SHA/size pins matched | 13 / 13 |
| Baseline recovery ledger rows | 1,576 |
| Metadata input pins | 6 |

All accepted bodies decode as strict UTF-8. Each source was pinned before recovery, rechecked during acquisition and compared byte-for-byte with the destination readback. Source and destination hashes, first-line bytes, complete content and mixed/original line endings are preserved without normalization.

Final verification checks the exact approved source-path set and order, relative-path digests, unique source hashes and destinations, root-compatible nine-column schema, matching source/destination bytes, accepted/identity/selection agreement, current sizes, historical catalog pins, all six input versions, privacy residue and absence of scratch scripts. Both deferral and transformation tables are empty apart from their headers.

Published metadata yielded no exact source-path/SHA hold before review. Full body review found no substantive held dependency or original full-script/asset body; opaque historical mentions and caller-only references were kept within the independent authored scope. Complete review does not include linked targets or a missing/refused draft continuation.

These are acquisition and identity checks only. No linked payload reads, native operations, runtime/Golden tests, original/shared/root writes or Git changes were used.
