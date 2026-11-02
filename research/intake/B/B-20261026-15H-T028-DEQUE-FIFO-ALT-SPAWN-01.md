# B historical intake — Alternative-grid and summon-position candidate searches share a deque-like FIFO structure

- Research ID `B-20261026-15H-T028-DEQUE-FIFO-ALT-SPAWN-01`; tasks T028 / T011 cross-reference.
- Original PC owner-report `data/T028_DEQUE_FIFO_ALT_SPAWN_SHARED_NATIVE_20261026_15H.md`; **measured report SHA256** `548A56497537FAE3168CEADEF56457BDFDE994DDDAD58C57377B1C599CC21460` on 2026-11-02 read-only; separate from original PE source hash.
- Owner B; source original ver0.67 PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`, unified V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (both independently rehashed read-only on authorized PC, 2026-11-02).
- Stage: **PUBLISHED_INTAKE / NOT_CURATED** after GitHub readback; older study ID, not a new study or formal READY. Original gameplay Golden PASS=0, strict MATCH=0, dynamic=0; no original game run.

## Evidence and correction/duplicate lineage
- Native owner report: `0x42A590` fills three DWORD output entries and does **not** return a Boolean 0 in EAX. `0x4E8C10` interprets a split-block cursor (2 records/block, each record 8 bytes) and returns an address to a coordinate-like pair. `0x4E8D50` appends to a deque-like sequence and adjusts count.
- `0x4E7770` consumes front records, decrements count and optionally enqueues neighbors with `0x4E8D50`; mode0 decodes the same record form inline. `0x4E70E0` uses the same enqueue/read-head structure in a related route invoked from summon context `0x54F0E1` and another caller `0x547932`. A FIFO/BFS-*like* mechanism is suggested, **not** a proven full shortest-path or spawn ranking.
- **Independent source-byte validation in this intake:** original PE `0x4E8C10` 58-byte SHA256 `2EB094369201A21AFAE60BFE18103DFDE7532666C20CD382B85B49E08C32E994` matched the historical native report. Other calls/branches are prior owner static evidence awaiting bounded recheck.
- Related prior owner study: `B-20261026-1417-T028-ALTGRID-CELLGATE-EIGHTDIR-01` covers cell/8-direction gate. This ID covers queue ownership and cross-route sharing, not an extra discovery of the same callsite.
- Missing: deque allocation failures, true queue invariants, RNG downstream, direction priority, legal runtime reachability and exact semantics of summon position. Next: limited V9/native `0x4E8D50` growth and `0x4E70E0` return contract then legal side-by-side original game.

## Curator checklist
Check source byte SHA, original bounded native evidence, prior research IDs, supersedes/errata, and current develop REF/symbols. Admit only independently verified STATIC facts; do not treat a VA hit or owner report as runtime proof. No refused body, raw binary or game files are attached.
