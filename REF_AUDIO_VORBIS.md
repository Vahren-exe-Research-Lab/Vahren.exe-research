# Native Ogg/Vorbis header parsing — curated REA/T015 source map

Scope: original ver0.67 PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; composite V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`.
All findings below are bounded original-x86 **STATIC**. Branch reachability under real allocation failure, ABI, crash behavior, recovery, and observed gameplay remain **VERIFY**. Original-game Golden PASS **0**, strict MATCH **0**; owner READY **0**.

## 1. Parent header-error mapping (04H, not another router discovery)
- `0x005CF010` calls header router `0x005D44C0` at `0x005CF167` and `0x005CF279`. The first call's nonzero result goes through `0x005CF1E9` (`EDI=-133`) and cleanup, masking the specific router error; the second preserves its return value in `EDI` and returns it through `0x005CF206`. Do not assume all Ogg header errors retain their original code.
- Both branches converge on native cleanup calls `0x005CF1F2 -> 0x005D3DE0`, `0x005CF1FB -> 0x005D3D00`, with state `outer+0x58=2` at `0x005CF20A`. Separate packet-I/O error paths must not be attributed to router behavior.
- Source/owner: REA ID `REA-LOCAL-20261031-04H-P0-VORBIS-PARENT-ERROR-NORMALIZATION-STATIC-01`; `rea_lab/decomp_task/REA_20261031_04H_P0_VORBIS_PARENT_ERROR_NORMALIZATION_STATIC.md`. Existing 02H/03H header-router/type results are antecedents, not newly counted findings. Original-PE window `0x5CF150..0x5CF290` independent SHA256 `62AF0C962E6B1D7BFA3AD2E13467BE1C07F8220EC001E24F9B7CE5002A569CD2`.

## 2. Type3 comment parser and conditional allocation guards (05H)
- `0x005D4030` parses a type3 comment header. Its native `0x005D4061` calls `_calloc` (`0x005D1C71`) and stores the result to `ESI+0xC`; for vendor length >0 it writes through that pointer at `0x005D407D` without a preceding local null check. A length-zero branch bypasses this write. **Potential null-write path is static, not a measured game fault.**
- With comment count >0, two further allocation calls `0x005D40BE`/`0x005D40C8` precede array stores `0x005D4112`/`0x005D411C` without local null checks; per-comment calloc at `0x005D4115` feeds the later `0x005D3CB0` helper. The zero-vendor/zero-count route and subsequent type5 vendor-pointer check (`0x005D455B`) are conditional and untested dynamically.
- CRT `_calloc` (`0x005D1C71`) calls `0x005C303C`, which invokes heap allocation and checks for null at `0x005C3085`. These CRT helpers were already identified in V9; do **not** count them as two new game-semantic discoveries or auto-rename them.
- Source/owner: REA ID `REA-LOCAL-20261031-05H-P0-VORBIS-CALLOC-NULL-GATE-STATIC-01`, `rea_lab/decomp_task/REA_20261031_05H_P0_VORBIS_CALLOC_NULL_GUARD_STATIC.md` and its evidence JSON (owner static QA 56/56; no gameplay). Independent PE-window SHA256 `0x5D4030..0x5D4160` = `6F8B35B6949E04FCD340738CFCBBEAA66DDE342ED16FD320783ACF9978EE25E7`. V9 name/address is an index, not a passed Golden test.

## 3. Remaining validation and indexing boundary
- REA research under `rea_lab/decomp_task/` is **outside** the intentionally shallow `research_index.py` corpus; neither the 04H nor the 05H original text was silently bulk-indexed. These explicit source links are curated read-only references, not full-text inclusion.
- Confirm real input states, allocator/new-handler lifetime and parent handling in separately authorized tests; do not equate native potential null dereference with demonstrated exploitability, reproduction or safe failure. Owner's synchronized 5-method completeness and E-MASTER READY counts remain unchanged.
- Preserve earlier 04H index-path ENOENT and 05H PowerShell CLI argument encoding error as **OTHER/VERIFY**, not as missing findings or a safety refusal. Do not reroute blocked evidence through another tool or path.
