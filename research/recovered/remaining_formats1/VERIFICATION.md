# Verification

PASS, 2026-11-05 JST. Checks used only authorized repository metadata and generated audit tables; originals were not restatted or read during verification.

- Selection equality and order: 1,115 unique path digests exactly match the published CATALOG_ONLY_UNRESOLVED selection.

- Historical SHA, byte size, owner and coverage fields: match their selected catalog rows; current SHA stays NOT_MEASURED for every row.

- Presence and size totals: 1,115 regular files; nine size changes, 1,106 equal-size content-unverified rows; no missing, inaccessible, reparse or containment failures.

- State partition: 71 hold metadata + 10 other/pending + 30 current unreviewed Markdown + 24 old Markdown outside current selected folders + 980 other-format unknown-content paths = 1,115.

- Supplemental tables: 81 exact prior-deferral paths, 24 old Markdown scope gaps and eight filename-only leads; owner/extension and every COUNTS dimension sum to 1,115.

- Current Markdown comparison: 44 unreviewed = 30 old unresolved paths + 14 NOT_IN_CATALOG_SNAPSHOT paths.

- Input integrity: all 49 recorded metadata input byte sizes/SHA256 values rechecked, all byte-identical to pinned baseline metadata.

- Original access boundary: the single bounded metadata pass used 1,135 lstat calls including shared containment/reparse-check ancestors; no directory enumeration, source body reads, source hash measurement, linked target fetch, execution or original mutation.

- Privacy: two complete auth-like relative filenames replaced with path-digest pseudonyms; no original private filename, profile path, credential-shaped string or absolute source path occurs in outputs.

The current filesystem observation is metadata only. Size equality and historical SHA equality to older records are not proof of current-byte identity. Existing hold/pending labels remain historical review metadata, with no new native-acquisition or refusal assertion. There is no accepted-body REPORT_LEDGER: this audit adopts zero bodies and makes no semantic recovery claim.
