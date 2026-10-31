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


## 4. Codebook/look-record ownership and teardown (REA 10H)
- REA-LOCAL-20261031-10H-P0-VORBIS-CODEBOOK-OWNERSHIP-TEARDOWN-STATIC-01 (REA/T015), source rea_lab/decomp_task/REA_20261031_10H_P0_VORBIS_CODEBOOK_OWNER_STATIC.md and matching EVIDENCE.json.
- Original 0x5D5922 calls 0x5D9F40: 0x5D9F55 stores a source codebook pointer at look record+0x0C. Owner slots are in inner+0x720; 0x38-byte look records in inner+0xB20 hold an inferred borrowed pointer without a locally observed refcount operation.
- After successful 0x5D5B51 -> 0x5DA070 conversion, 0x5D5B60 frees the source and 0x5D5B6C zeroes its owner slot. Failure cleanup revisits only remaining non-null owner slots. 0x5D9ED0 frees owned look+0x10/+0x14/+0x18/+0x1C/+0x20 fields, then zeroes the look record, but does not separately free +0x0C.
- 0x5D3DE0 tears down source codebooks, look records and the parent. Normal unique-pointer sequential behavior is narrower than a proof against aliasing, exceptions, incomplete initialization or asynchronous access.

## 5. Conversion clears borrowed field and has conditional allocation gates (REA 11H)
- REA-LOCAL-20261031-11H-P0-VORBIS-LOOK-CONVERSION-ALLOCATION-GATES-STATIC-01 (REA/T015), source rea_lab/decomp_task/REA_20261031_11H_P0_VORBIS_LOOK_CONVERSION_STATIC.md and matching EVIDENCE.json, corrects a possible 10H overinterpretation: 0x5DA070 starts with memset(look,0,0x38) at 0x5DA07C..82, clearing the former +0x0C borrowed field before normal source free.
- The first allocator result has an explicit 0x5DA0E9/EB NULL check and error -1. Four later allocations (0x5DA1A7/0x5DA224/0x5DA255/0x5DA2D4) lack immediate local NULL checks; subsequent writes are input-conditional, while zero-entry cases skip those steps. Crash/exploitability is NOT proven.
- All 7 recorded 10H and 8 recorded 11H source PE windows independently matched SHA256 in read-only verification. Historical one-shot owner audits recorded 46/46 and 52/52; when evidence already exists their uniqueness gates cause 45/46 and 51/52 on rerun without any original ASM mismatch or evidence overwrite.
- Both research IDs remain STATIC with INFERRED/VERIFY failure semantics; ABI, aliasing, true allocation-failure reachability and gameplay effects are unverified. Golden PASS=0, strict MATCH=0, owner READY unchanged. The source reports are intentionally outside shallow text indexing and explicitly linked.

## 6. Type3 comment array and cleanup boundary (REA 06H; predecessor 05H)
- Owner ID REA-LOCAL-20261031-06H-P0-VORBIS-COMMENT-SENTINEL-TEARDOWN-STATIC-01, T015; owner source rea_lab/decomp_task/REA_20261031_06H_P0_VORBIS_COMMENT_SENTINEL_TEARDOWN_STATIC.md plus corresponding EVIDENCE.json. This is a DIFFERENT delta from the 05H allocation-null warning, not an additional claim of the same warning.
- Original 0x005D4030 allocates comment pointer and length arrays with calloc(count+1,4); when successful, the extra element is zero initialized, not a (count+1)-th valid comment. The structure stores pointer array +0, lengths +4, signed count +8 and vendor +0xC.
- The static cleanup function 0x005D3D00 visits nonnull element pointers while index<count, frees the arrays/vendor, then zeroes +0/+4/+8/+0xC. This supports conditional cleanup of a partially filled valid array; it does NOT fix a preceding null allocation write or establish double-free freedom for aliased/corrupt states.
- Byte-copy helper 0x005D3CB0 returns directly for zero count; for positive count, it stores a low byte from bitreader 0x005E6E10 without checking a negative return in this helper. Parent packet-length checks and malformed-input reachability remain VERIFY.
- V9 function 0x005D3D00 has two disjoint body ranges 0x005D3D00..0x005D3D19 and 0x005D3D20..0x005D3D77. The 0x005D3D1A..0x005D3D1F padding must NOT be mistaken for a missing native function body; previous 06H static-audit span error was corrected by the REA owner.
- Independent authorized PE bytes for 28/28 saved assembly sites matched readback; original ver0.67 PE SHA is at this document's top. State: STATIC for bounded ASM, INFERRED/VERIFY for repeated-cleanup safety and error propagation; formal REA 5-method COMPLETE added=0, Golden PASS=0, strict MATCH=0, READY unchanged.

## 7. Codebook malloc(0), conditional null paths and cleanup (REA 09H; predecessors 08H/10H)
- Owner ID REA-LOCAL-20261031-09H-P0-VORBIS-CODEBOOK-MALLOC-CLEANUP-STATIC-01, T015; source rea_lab/decomp_task/REA_20261031_09H_P0_VORBIS_CODEBOOK_MALLOC_CLEANUP_STATIC.md plus matching EVIDENCE.json. The 10H owner-map and 11H look converter above are extensions; do not double-count their repeated callsites.
- Native E8 0x005DA604/0x005DA6D6 both call CRT allocator 0x005B9BC8 and store codebook +0x08; E8 0x005DA811 similarly stores +0x20. Under positive element counts the follow-on indexed writes lack locally demonstrated null checks; actual allocator-failure effects are not dynamically reproduced.
- 0x005D9E70 checks marker+0x24, conditionally frees nonnull +0x20 and +0x08 fields, clears 10 dwords and releases the structure. Its later cleanup cannot retroactively guard a failed allocation's earlier write. Caller ownership/aliasing remain VERIFY.
- The CRT wrapper 0x005B9BC8 normalizes malloc(0) to a size-one request, and a nonzero allocation-failure/new-handler retry path exists. Therefore zero element count alone does NOT imply a null returned pointer; behavior on ultimate OOM remains VERIFY.
- Independently matched original PE 29/29 saved assembly opcode sites and 3/3 direct E8 allocator targets. The report's own 48/48 checks remain static-only and are not gameplay compatibility tests. Golden PASS=0, strict MATCH=0, no formal READY or full replication-rate claim.
