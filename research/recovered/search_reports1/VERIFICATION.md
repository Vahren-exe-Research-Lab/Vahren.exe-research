# Verification

Verified on 2026-11-05 against the exact approved selection and the pinned baseline metadata.

| Check | Observed result |
|---|---:|
| Approved literal source paths | 87 |
| Current total original bytes | 550,026 |
| Current sizes equal approved metadata | 87 / 87 |
| Catalog-pinned SHA and size matches | 31 / 31 |
| Without catalog hash pins | 56 |
| Complete authored UTF-8 body reviews | 82 |
| Same-study preholds, body not opened | 5 |
| Accepted nine-column ledger rows | 72 |
| Whole-file metadata deferrals | 15 |
| Exact accepted body copies | 59 |
| Full privacy body variants | 13 |
| Proven privacy token replacements | 14 |
| Baseline/within-batch aliases | 0 / 0 |
| Baseline recovery ledger rows pinned | 1,395 |

All accepted destinations were read back and compared with either complete original bytes or the complete reconstructed privacy variant. Every source hash, destination hash, original token span/hash, original prefix/suffix hash, intervening byte sequence and final reconstruction is independently checked by the final receipt verification. Original UTF-8 decoding is strict; no line-ending normalization is used. Held destinations remain blank and no held bodies are written. Selection receipts distinguish body reviews from hashing-only preholds.

The final verification also checks exact source-path coverage and accepted/deferred partition, nine-column schema, unique destinations, strict UTF-8 bodies, privacy residue, source/current size pins, catalog pins, input versions and matching identity/selection records. These are document acquisition/identity checks, not game tests. No native operations, linked evidence reads, test reruns, cleanup, Git commands or shared/root writes were used.

Metadata correction: removed a duplicated index prefix from ten self-source provenance paths in DEFERRED.tsv. All 15 nonempty provenance paths were checked for exact membership in the approved 87-path selection, without opening those paths. Counts, source/body hashes, other deferral fields and all accepted body bytes are unchanged.
