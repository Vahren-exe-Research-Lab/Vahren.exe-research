# REA 2026-11-02 11H | F720 exclusion-tree pointer handoff through two support helpers (bounded original x86)
- **research_id:** `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` (existing ID; **0 new research IDs**); supplements the 2026-11-02 10H erratum, not a new F720 discovery.
- **owner/scope:** REA independent / T015-P0; read-only original PE, current V9 read-only and prior B/T028 source comparison. `STATIC` for local native argument and E8 sites; downstream effects/semantics `VERIFY` / `NOT_READY`.
- **Original isolated target:** `rea_lab/targets/hakushin067_Vahren.exe`, independently read and SHA256 = `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; PE image base `0x400000`.
- **Current composite V9:** `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` (read-only); snapshot SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. V9 native_callsite independently verified each of the four E8 edges below; it is not original gameplay evidence.

## Route A: 0x48F9E0 -> 0x4868D0 -> 0x489630
- Original `0x49010D LEA ESI,[EBP+0x1EED30]` and `0x490113 PUSH ESI`, among seven argument pushes, supply **fourth stack argument** to `0x490122 CALL 0x4868D0` (comparison-tree container address; not node/header ownership).
- The `0x4868D0` SEH prologue creates `0x258` bytes of stack displacement before its normal body. At `0x487991 MOV EDX,[ESP+0x268]`, under the ordinary balanced call path, this is the **fourth incoming stack argument**; `0x4879A0 PUSH EDX` makes it the **sixth stack argument** in the seven-push call to `0x4879BF CALL 0x489630`.
- Original E8 target checks: `0x490122 -> 0x4868D0`, `0x4879BF -> 0x489630`, both PASS.

## Route B: 0x490180 -> 0x488290 -> 0x489630
- `0x4901A7 MOV ESI,[ESP+0x4C]` establishes context pointer for this branch. `0x49020B LEA ECX,[ESI+0x1EED30]` and `0x490211 PUSH ECX` supply the **fourth stack argument** for `0x49021A CALL 0x488290` (six pushed arguments in native call).
- The `0x488290` prologue creates `0x194` bytes of stack displacement. `0x488C13 MOV EDX,[ESP+0x1A4]` reads the **fourth incoming stack argument** under the balanced normal path; `0x488C22 PUSH EDX` forwards it as **sixth stack argument** for `0x488C44 CALL 0x489630`.
- Original E8 target checks: `0x49021A -> 0x488290`, `0x488C44 -> 0x489630`, both PASS.

## Byte-window receipts (independently SHA256 hashed, no raw source bytes stored)
- A `0x490100..0x490127` 39B: `8557005065ECFC640FA4277AE6C371A4DBA0D0F2256A1EFA9E00C2CDD7B81698`.
- B `0x487991..0x4879C4` 51B: `76867CAFDACB3A67A6F8D6BDD7EF522D392352ADA252BFCBC128A190E6BED77E`.
- C `0x490203..0x49021F` 28B: `100B8DF2F0316C618F544419EA0AFC4F0D995CF27C739531643114D7FBCAFAA4`.
- D `0x488C13..0x488C49` 54B: `006903E47A678A7C588369161661C909E2E2E21FA8901B10CFC30C8C3EE45799`.
- Original prologues `0x4868D0..0x4868FD` 45B: `4EEB8DBA952D560F838948ECC611114EA8F14374E68497A1602F5413DF5E2CDC`; `0x488290..0x4882BD` 45B: `629C8DA4041EE4F486D2158A300AC2CDF794D616E9E8F77F726395D63389B19D`.
- Destination `0x489630..0x489657` 39B: `7248F384485554F4D6047BE493E9EF0DB7FEFD74E210F8A643D2F1FFFA38F9D4`.

## Precise boundary, correction graph and next cursor
- This confirms **two pointer-carriage paths into 0x489630**, not the creator/writer of the comparison tree, insertion/removal effect, membership, layout identity, or actual original battle reachability. Ghidra pseudoc of 0x489630 shows parameterized tree traversals but is not authoritative ABI for its side effects. Do not conflate F720 exclusion-tree sentinel node+0x19 with outside candidate-tree sentinel node+0x21 or assume 0x489630 writes the exclusion tree.
- Previous `REA_20261024_09H_P0_THREE_TREE_PREDICATE_STATIC.md` and `REA_20261102_10H_P0_F720_ARG2_KEY_ORIGIN_ERRATUM_STATIC.md` remain distinct evidence/correction sources under **the same research ID**. Nearby B/T028 2026-10-28 native tree lookup/flag research is an existing other-owner antecedent, not a new REA finding. No edit to B owner.
- **Next lawful cursor:** limited original x86 inspection of `0x489630` sixth argument's use and mutation callees; reconcile two sentinel offsets and verify whether a writer actually changes context+0x1EED30/34. Then isolate remaining 0x48F9E0 callers. Curator alone can adopt bounded meaning into shared REF/symbols.
- **Do not promote:** independent formal new REA five-method evidence bundles 0, new VERIFIED 0, game Golden PASS 0, strict MATCH 0, READY 0. No REA runner, gameplay, original asset modification, or safety-refused protected/Wave6/18H path used. No shared develop/REF/other-owner/QUEUE/PROGRESS changes.
