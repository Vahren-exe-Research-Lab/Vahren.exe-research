# B historical intake — Route planner result is [begin,end) 8-byte record range, not one coordinate pair

- Research ID `B-20261027-0013-T028-ROUTE-LIST-RANGE-ABI-CORRECTION-01`; tasks T028 / T012 cross-reference.
- Original PC owner-report `data/T028_ROUTE_LIST_RANGE_ABI_CORRECTION_NATIVE_20261027_00H.md`; **measured report SHA256** `661203D0139037D26B3C7C61D80CB5B7042C4937D40D918B76A6ACCF1CD09F76` on 2026-11-02 read-only; separate from original PE source hash.
- Owner B; source original ver0.67 PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`, unified V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (both independently rehashed read-only on authorized PC, 2026-11-02).
- Stage: **PUBLISHED_INTAKE / NOT_CURATED** after GitHub readback; older study ID, not a new study or formal READY. Original gameplay Golden PASS=0, strict MATCH=0, dynamic=0; no original game run.

## Evidence and correction/duplicate lineage
- **Corrects historical B 2026-10-26 23H interpretation:** first two DWORD values returned by `0x4EC1E0` are consumed here as *begin/end pointers* to an ordered range of 8-byte route records, **not** a final X/Y coordinate.
- Static caller `0x576AAC→0x4EC1E0` then reads output `[EAX], [EAX+4]` and passes pointers via `0x576AC3→0x57A690`. That helper resets the Unit `+0x186B0` route list and calls `0x57A910` to construct ordered nodes with stride 8. Later `0x576AD2→0x579900` appends the requested destination record; do not equate route-element storage with direct Unit position writes.
- **Independent original-PE check:** `0x57A690` 70-byte SHA256 `0CFA6F48E0A35612C16E9B83CFF9B27E9B7A64A5E409CE09BCB66644ABDE63D0` matched source report. Additional window and callsite claims remain earlier owner static scope.
- Earlier B 23H snapshot of requested input and original Unit `+0x214/+0x218` remains a separate, narrower fact; the old *returned X/Y* human description is **superseded** by this correction.
- Unknown: route ownership, empty/failure reaches, list exception atomicity, true reached position, precise ABI and dynamic gameplay. Next: legal original same-SAVE route length/order/destination and next-tick comparison, preserving no confirmed READY.

## Curator checklist
Check source byte SHA, original bounded native evidence, prior research IDs, supersedes/errata, and current develop REF/symbols. Admit only independently verified STATIC facts; do not treat a VA hit or owner report as runtime proof. No refused body, raw binary or game files are attached.
