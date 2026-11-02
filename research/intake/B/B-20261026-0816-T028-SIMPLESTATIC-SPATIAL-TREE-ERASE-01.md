# B historical intake — SimpleStaticUnit death finalizer conditionally erases spatial-tree entries

- Research ID `B-20261026-0816-T028-SIMPLESTATIC-SPATIAL-TREE-ERASE-01`; tasks T028 / T011,T012 cross-reference.
- Original PC owner-report `data/T028_SIMPLESTATIC_SPATIAL_TREE_ERASE_NATIVE_20261026_08H.md`; **measured report SHA256** `89866E1688AC3440B2C8E6C4123204BEBD8C02F30194F690A8EC76814C177D2B` on 2026-11-02 read-only; separate from original PE source hash.
- Owner B; source original ver0.67 PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`, unified V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (both independently rehashed read-only on authorized PC, 2026-11-02).
- Stage: **PUBLISHED_INTAKE / NOT_CURATED** after GitHub readback; older study ID, not a new study or formal READY. Original gameplay Golden PASS=0, strict MATCH=0, dynamic=0; no original game run.

## Evidence and correction/duplicate lineage
- Owner native chain: `0x55B030` checks Unit `+0x1867C` then sets this byte and calls `0x49D9F0`, followed by `0x4E4F60`. `0x49D9F0` can skip work based on manager/object `+0x1EED40`; otherwise it transforms Unit `+0x220/+0x224` into 32-unit grid indices and scans a clipped **4×4 maximum**, upper-bound-exclusive neighborhood (not 5×5).
- Grid key appears to pack 16-bit X/Y into a DWORD. Native path `0x49DB29→0x510C20` erases a tree node, where the latter repairs links/decrements node count. This is **spatial-container maintenance**, not proof of visible removal timing or death/morale gameplay side effects.
- **Independent original-PE byte check:** `0x49D9F0` 355-byte SHA256 `1AA05D1AE7EA1977D3F9CA1CA56F71E7DEC5B1D75AABBF0A3CE7DBA09BDFBB58` matched historical source. Other listed sites are prior owner static assertions.
- Prior B 07H already covered the finalizer call and death flag; do not recount it as a new finding. Unknown: tree owner/identity per cell, multiple Units per cell, game coordinate normalization, death timing and G4 results commit. Next: legal read-only source of manager flag and original-game death-boundary comparison.

## Curator checklist
Check source byte SHA, original bounded native evidence, prior research IDs, supersedes/errata, and current develop REF/symbols. Admit only independently verified STATIC facts; do not treat a VA hit or owner report as runtime proof. No refused body, raw binary or game files are attached.
