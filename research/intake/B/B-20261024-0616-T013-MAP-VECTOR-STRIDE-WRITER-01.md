# B historical research intake — case8 map values: 28-byte string vector clone, source/owner pointers and registration candidate

- ID: `B-20261024-0616-T013-MAP-VECTOR-STRIDE-WRITER-01`; owner B; tasks T013.
- Source report: `data/T013_CASE8_MAP_VECTOR_STRIDE_WRITER_NATIVE_20261024_06H.md`, source Markdown SHA256 `ECE64E96DE59AD795CA8D605703144737E2E7D31AE4F07D2C970B3A7DCE1CA36` **independently measured on authorized PC 2026-11-02** (read-only). Historical study ID, not new discovery.
- Target original PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; unified V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (both rehashed read-only this intake). Use V9 as static index only; native proofs are scoped below.
- Stage: **PUBLISHED_INTAKE / NOT_CURATED** after exact GitHub readback. Original Gameplay Golden PASS=0, strict MATCH=0, new READY=0, DYNAMIC=0.

## Bounded research claims, source/errata and future check
- Bounded original native `0x49C915→0x42E8E0`: map node `+0x28` 3-pointer value-vector descriptor passed to deep-copy; `0x42E8E0` operates in `0x1C` element strides and calls `0x430300`. The `0x430300` helper performs string-element copying and `+0x1C` iteration.
- Map node descriptor `+0x28/+0x2C/+0x30` has begin/end/cap-end-like fields; actual C++ allocator/type are not established. `0x49C54F` previous getter covers **first** string only; `0x49C915` and `0x49CC59` are full-vector clone sites; do not collapse these operations.
- Owner reports a separate put/replace candidate `0x49CD60`: append `0x415530`, key-range lookup `0x49F1F0`, erase candidate `0x49EE60`, key+vector cloning `0x49F730`, node creation `0x49FE30`, map insert `0x49F7D0`. The `0x49FF70` branch moves vector pointers into the new pair, clearing the old pointer slots; memory ownership in errors remains VERIFY.
- **Independent original-PE byte check in this intake:** `0x42E8E0` 192-byte window SHA256 `10AC8C0B3D5B3FD6237E7672781BF05DA52D30FE150DEDAB2243A89577F639F9` matched the old report. Other cited native windows were not separately revalidated in this run.
- Prior work: `B-20261024-0415-T013-CASE8-MAP-EXACT-LOOKUP-OUTPARAM-01` (map lookup), and prior 05H first-element getter (source-only link). Full value vector contents, duplicate-key policy, writer command, exception and gameplay remain VERIFY. Golden PASS0.

## For selective KB admission
The curator must independently check cited source MD SHA and original bounded ASM sites, correlate prior IDs/errata, and admit only confirmed facts into REF/symbols. Address mentions are search leads, not automatically verified ABI or runtime. No raw EXE/DAT/MAP/SAVE or refused research content is stored here.
