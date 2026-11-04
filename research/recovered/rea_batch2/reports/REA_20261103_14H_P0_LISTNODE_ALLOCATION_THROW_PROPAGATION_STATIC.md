# REA 2026-11-03 14H | list-node allocation failure -> C++ exception (STATIC / VERIFY)

- Work ID: `REA-20261103-14H-P0-LISTNODE-ALLOC-THROW-STATIC`; owner REA / P0-T015; existing ID `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` (13H continuation), new unique IDs **0**.
- Scope: authorized read-only original PE32 and unified V9 SQLite; no new REA decompilation, actual game execution, forbidden VA/extraction, or other-owner/develop changes.
- Native source: `rea_lab/targets/hakushin067_Vahren.exe`; measured 2026-11-03 14H SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
- V9 source: `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`; measured 2026-11-03 14H SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`; read-only SQLite queries.
- Previous owner 13H source: `rea_lab/decomp_task/REA_20261103_13H_P0_CLEANUP_CHILD_DETACH_DELETE_BRANCH_STATIC.md` SHA256 `5E3DB1340A871C4F2CE8EC44E3C9137AAEB43F6280A7982CE93E28A7D1F7F6FD`, independently rehashed this run.

## Distinct bounded native findings (source-backed; same existing ID)
1. The nonzero `[child+0x14]` branch of `0x562B00` directly calls `0x4C52D0` at `0x562B1B`; on *ordinary return*, subsequent `0x562B40` saves EAX as a linked node and `0x562B43` dereferences `[eax+4]`, with no caller-side null check. This does NOT establish a live null dereference.
2. `0x4C52D0` requests `0x0C` bytes via `0x5B6C2B` (`0x4C52D5`), tests EAX at `0x4C52DD`, and branches to `0x4C5303` if zero (`0x4C52DF je`). Only the nonzero arm stores node fields `[eax]`, `[eax+4]`, `[eax+8]` and returns via `0x4C5300 ret 0x0C`.
3. The zero arm constructs an exception object through `0x5B65BB` at `0x4C5314`, then calls `0x5B864E` at `0x4C532B`. V9 labels that function `__CxxThrowException@8`; its native `0x5B8690` calls IAT `0x60913C = KERNEL32!RaiseException`, and `0x4C5330` is `INT3`. Therefore the explicitly decoded allocation-zero arm is an exception-raising path, **not an ordinary `return NULL` path**. No runtime exception or handler outcome was observed.
4. Allocation helper `0x5B6C2B` calls V9 `_malloc` at `0x5B6C45 -> 0x5B9BC8` and includes retry/handler branches. A prior helper-side raise/termination remains possible; do not infer that the raw allocator always returns zero on failure or that all exceptions escape the whole program.
5. Correction / erratum vs 13H: `0x562B00`'s no-null-check list linking is real native STATIC, but cannot be cited as evidence of an actual NULL crash on the allocation-failure path. Exact exception type, catch/finally coverage, list consistency on exceptions, allocation failure reachability and original gameplay remain VERIFY.

## Native receipts and Ghidra V9 concordance
- Window `0x4C52D0..0x4C5330` (96 B) SHA256 `4187781E1F90E57BE3BE93CC30ECBEB96907653C3A1512960444E422329DB6F7`; `0x5B864E` (76 B) SHA256 `7E74CE0CBE6AE9186EF77ABDB5E89EB38B390841B925055463315A39F5074F1D`; `0x5B6C2B` (127 B) SHA256 `905AC4847B6F7AFA15CE35F1C9E0A1AF44A3E11439728BB505616808145D8859`.
- Selected original PE opcode/E8 rel32/target vs indexed V9 native_callsite: `0x562B1B->0x4C52D0` (`E8B027F6FF`), `0x4C52D5->0x5B6C2B` (`E851190F00`), `0x4C5314->0x5B65BB` (`E8A2120F00`), `0x4C532B->0x5B864E` (`E81E330F00`), `0x5B6C45->0x5B9BC8` (`E87E2F0000`): **5/5 matches**; `verified_abi=0` for involved V9 functions. These are NOT five formal REA evidence bundles.
- V9+native observation is STATIC. The precise exception type/catch state, live cleanup/callback target at `0x562B56`, global list ownership, original-game crash and mode-2 reachability remain VERIFY. No new formal five-method VERIFIED; old 64/64 not rerun. Original Golden PASS=0, strict MATCH=0, READY=0.

## Intake / curator / resume
- Dedup: prior 11H/12H/13H share the existing historical study ID; this is an **erratum and additional STATIC meaning**, not a new discovery ID. `develop/symbols.tsv` has no matching `0x4C52D0/0x562B00` address entry in the current targeted read; full cross-owner semantic review belongs to curator.
- Publish only on PRIVATE owner existing Draft PR intake; readback is required before claiming PUBLISHED_INTAKE. NOT CURATED; do not change `develop`, `REF_*`, `symbols.tsv`, or `structs.tsv`.
- Curator review: recheck original PE window hashes, five E8/V9 rows, exception IAT mapping and 13H apparent-null-risk wording; distinguish throw path from a measured crash and compare B/E/REF duplicates. Selectively adopt the corrected STATIC claim only.
- Next lawful cursor: inspect bounded exception/SEH handling upstream of `0x562B1B` and separately live `0x562B56` vptr +8 target/side effects, without touching any Wave6/18H/protected refusals.
