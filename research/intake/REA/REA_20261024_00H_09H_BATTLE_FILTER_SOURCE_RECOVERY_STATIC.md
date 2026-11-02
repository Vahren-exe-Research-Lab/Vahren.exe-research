# REA historical 2026-10-24 00H–09H: source-preserving battle-filter ABI recovery

Owner: REA / T010,T015/T031-related static research. **PRIVATE owner intake / NOT CURATED / NOT READY.** Nine distinct older REA report IDs, no newly discovered native functions, no new runner or Golden tests. The 02H source ID `REA-LOCAL-20261024-02H-P0-F720-MAP-FILTER-ABI-STATIC-01` already appears in develop `REF_BATTLE_TAKEOVER.md` with exact matching report SHA256 `E8D60E3A7EABB1E6D8844BFED22E4E2D1C94070F6559CA2101B1EF7699014907`; **linked as curated predecessor, not re-published or re-counted here**.

All nine owner reports and nine corresponding small EVIDENCE JSON files exist on the authorized research PC. Both sets were independently SHA256 hashed by read-only file operations on 2026-11-02 JST. The report's own static instruction/E8 tests are historical; we did **not** rerun 9 native instruction audits, V9 search, REA 5-method acquisition or original gameplay. Target PC PE historic SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`, unified V9 archived SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. Early reports sometimes used V3; never promote its uncorrected inference above V9/original x86. Original PE and V9 were **not independently rehashed in this recovery**. All EVIDENCE JSON, binaries, user-local paths and generated databases remain on the PC only.

## Evidence and normalized owner-source records

### REA-LOCAL-20261024-0043-P0-DEMOPERSON-PAIR-INIT-ABI-STATIC-01

- **Owner/time/state:** REA independent / 2026-10-24 0043 JST / STATIC (limited native-source instruction history), INFERRED where stated, VERIFY; Golden PASS 0, READY 0.
- **Owner source:** `rea_lab/decomp_task/REA_20261024_0043_P0_DEMOPERSON_PAIR_INIT_ABI_STATIC.md` / SHA256 `EC0E1D91966008B19C977DF2459B6702AB210DED412C8609FDA0D011370EB493` (read-only file hash this recovery).
- **Original evidence:** `rea_lab/decomp_task/REA_20261024_0043_P0_DEMOPERSON_PAIR_INIT_ABI_EVIDENCE.json` / SHA256 `58402D4D09069111BAA4156883DC896C1EE9A00AD82A04CBFEAFDB2E991CD505` (not copied to GitHub).
- **VA and CALL/offset anchors:** 0x514A80, 0x40F3D6, 0x40F3F3.
- **Principal source-backed meaning:** Main DemoPerson vtable 0x638030 slot +8 points to 0x514A80: ECX=this, three stack arguments, RET 12. The two source objects receive cross-links at +0x1C, side bytes 0/1 at +0x18 and +0x20 initialized to 100. Indirect virtual calls cannot be counted through direct-E8 caller inventory.
- **Limitations and next validation:** Runtime object type, source lifetime, early-return behavior and equivalence to battle roster have not been proven.
- **Correction chain:** earlier owner hours are antecedent, not repeated evidence; 02H F720 ABI is already curated in develop, 03H–09H narrow its caller/generator assumptions. No formal REA five-method VERIFIED promotion.

### REA-LOCAL-20261024-0137-P0-DEMO-VSLOT0C-SOURCE-TAIL-STATIC-01

- **Owner/time/state:** REA independent / 2026-10-24 0137 JST / STATIC (limited native-source instruction history), INFERRED where stated, VERIFY; Golden PASS 0, READY 0.
- **Owner source:** `rea_lab/decomp_task/REA_20261024_0137_P0_DEMO_VSLOT0C_SOURCE_TAIL_STATIC.md` / SHA256 `842397FAEFFFD3860FDE70A46CC024D608FA5AA69B4C4442146727889BE48ED0` (read-only file hash this recovery).
- **Original evidence:** `rea_lab/decomp_task/REA_20261024_0137_P0_DEMO_VSLOT0C_SOURCE_TAIL_EVIDENCE.json` / SHA256 `A797B683BF88311189F9041D54ABC0AEB7006413549AE3FA0F7171435296D686` (not copied to GitHub).
- **VA and CALL/offset anchors:** 0x583CE6, 0x597B00, 0x4103D5, 0x4103E2, 0x447810.
- **Principal source-backed meaning:** Corrects 0x583CE6 to E9 tail-JMP, not E8 CALL; +0x0C virtual calls at 0x4103D5 and 0x4103E2 occur after +0x08 initialization with intervening work. Main vtable+0x0C=0x447810; source pointer+0x14 conditionally affects +0xA5 via RTTI.
- **Limitations and next validation:** No proof that all runtime dynamic types have that exact vtable or that mid-sequence exits cannot occur.
- **Correction chain:** earlier owner hours are antecedent, not repeated evidence; 02H F720 ABI is already curated in develop, 03H–09H narrow its caller/generator assumptions. No formal REA five-method VERIFIED promotion.

### REA-LOCAL-20261024-03H-P0-F720-NULLABLE-CALLER-CONTRAST-STATIC-01

- **Owner/time/state:** REA independent / 2026-10-24 03H JST / STATIC (limited native-source instruction history), INFERRED where stated, VERIFY; Golden PASS 0, READY 0.
- **Owner source:** `rea_lab/decomp_task/REA_20261024_03H_P0_F720_CALLER_NULL_CONTRACT_STATIC.md` / SHA256 `DABA032A4DB9821DEE5DE5BA92E9BB3BE7BAE87EEC888B264FB02A0438153EA3` (read-only file hash this recovery).
- **Original evidence:** `rea_lab/decomp_task/REA_20261024_03H_P0_F720_CALLER_NULL_CONTRACT_EVIDENCE.json` / SHA256 `78F8B1FCA145FD33552AD68F09A0FF2D23FE8CA71484ED539BDECC9D35B4911C` (not copied to GitHub).
- **VA and CALL/offset anchors:** 0x48F720, 0x4901C1, 0x40F393, 0x48FBD9, 0x4F66ED.
- **Principal source-backed meaning:** After nullable 0x48F720, caller 0x4901C1 does check EAX against zero before +0x94 access; 0x40F393 -> 0x583C70, 0x48FBD9 -> 0x583C70 and 0x4F66ED -> 0x583C70 have no equivalent local guard. All seven original rel32 E8 callers were compared by the source owner.
- **Limitations and next validation:** A possible unguarded dereference is conditional; valid-game reachability and upstream non-null invariants remain VERIFY. Supersedes any global claim that all callers lack null guards.
- **Correction chain:** earlier owner hours are antecedent, not repeated evidence; 02H F720 ABI is already curated in develop, 03H–09H narrow its caller/generator assumptions. No formal REA five-method VERIFIED promotion.

### REA-LOCAL-20261024-04H-P0-F720-OWNER-PROVENANCE-STATIC-01

- **Owner/time/state:** REA independent / 2026-10-24 04H JST / STATIC (limited native-source instruction history), INFERRED where stated, VERIFY; Golden PASS 0, READY 0.
- **Owner source:** `rea_lab/decomp_task/REA_20261024_04H_P0_F720_OWNER_PROVENANCE_STATIC.md` / SHA256 `6FE0B7F3068BE34E4AB547B8C46F1270F4658A8D8BAD682B43BA7226EFFDDEE2` (read-only file hash this recovery).
- **Original evidence:** `rea_lab/decomp_task/REA_20261024_04H_P0_F720_OWNER_PROVENANCE_EVIDENCE.json` / SHA256 `78A87FEFA52A1136FE8AF14CF0FD62A8810899459D227B948E3ACCB3A483CBB1` (not copied to GitHub).
- **VA and CALL/offset anchors:** 0x40D0B4, 0x40F38D, 0x48F723, 0x49AF10.
- **Principal source-backed meaning:** The 0x40D0A0 owner sets global [0x8B8E4C] from context+0x1EED20 before 0x40F320 reads it; selection-list and comparison-tree context are distinct. 0x49AF10 has a clearing/self-linked sentinel initialization of a related list, but not a demonstrated empty list at the later 0x40F393 call.
- **Limitations and next validation:** Do not interpret potential empty state as a proven original-game crash; trace intervening list population/owner changes.
- **Correction chain:** earlier owner hours are antecedent, not repeated evidence; 02H F720 ABI is already curated in develop, 03H–09H narrow its caller/generator assumptions. No formal REA five-method VERIFIED promotion.

### REA-LOCAL-20261024-0541-P0-RESET-REBUILD-F720-STATIC-01

- **Owner/time/state:** REA independent / 2026-10-24 0541 JST / STATIC (limited native-source instruction history), INFERRED where stated, VERIFY; Golden PASS 0, READY 0.
- **Owner source:** `rea_lab/decomp_task/REA_20261024_0541_P0_LIST_REBUILD_F720_STATIC.md` / SHA256 `9D3E9BC4387B36DD9F8AE3AD3DE3C4EC545C94DBA18177A29BA10814B9DBB4BA` (read-only file hash this recovery).
- **Original evidence:** `rea_lab/decomp_task/REA_20261024_0541_P0_LIST_REBUILD_F720_EVIDENCE.json` / SHA256 `770DAF331D49EE2697B9904F10A2050237B41230E0CA56B6B21E12FB8FE0CDA4` (not copied to GitHub).
- **VA and CALL/offset anchors:** 0x48FBB9, 0x48FBD1, 0x48FBD9, 0x498E60, 0x498F90, 0x476830.
- **Principal source-backed meaning:** The 0x48F9E0 list is cleared/reset, but its 0x48FBD1 call to 0x498E60 rebuilds from input before the 0x48FBD9 call to nullable 0x48F720. 0x498F90 -> 0x476830 connects normal first insertion/count increase.
- **Limitations and next validation:** Corrects overbroad empty-after-clear inference; whether source input is empty at runtime and allocation/exception failures remain unverified.
- **Correction chain:** earlier owner hours are antecedent, not repeated evidence; 02H F720 ABI is already curated in develop, 03H–09H narrow its caller/generator assumptions. No formal REA five-method VERIFIED promotion.

### REA-LOCAL-20261024-06H-P0-F9E0-SOURCE-ABI-STATIC-01

- **Owner/time/state:** REA independent / 2026-10-24 06H JST / STATIC (limited native-source instruction history), INFERRED where stated, VERIFY; Golden PASS 0, READY 0.
- **Owner source:** `rea_lab/decomp_task/REA_20261024_06H_P0_F9E0_SOURCE_ABI_STATIC.md` / SHA256 `946CC0AC3BB7BCE6D62B91AC91F6FE36E48D9C8DF0A4E8F111E5610E3FCB6DCA` (read-only file hash this recovery).
- **Original evidence:** `rea_lab/decomp_task/REA_20261024_06H_P0_F9E0_SOURCE_ABI_EVIDENCE.json` / SHA256 `79107E1B43CE877B59B7541FAEA89395599A47E8CAF329C3C32B84C691770C24` (not copied to GitHub).
- **VA and CALL/offset anchors:** 0x48F9E0, 0x48FA12, 0x48FBB5, 0x48FBCA, 0x490174.
- **Principal source-backed meaning:** 0x48F9E0 uses ECX plus two distinct 4-byte stack parameters and RET 8. The input container is the second stack argument; 0x498E60 rebuilds from that input. Distinguish destination cleared before rebuild from input possibly empty at 0x498E65.
- **Limitations and next validation:** All five higher-level callers need complete upstream nonempty/exception analysis before treating the rebuilt output as invariant.
- **Correction chain:** earlier owner hours are antecedent, not repeated evidence; 02H F720 ABI is already curated in develop, 03H–09H narrow its caller/generator assumptions. No formal REA five-method VERIFIED promotion.

### REA-LOCAL-20261024-07H-P0-B136-FIRST-INSERT-INVARIANT-STATIC-01

- **Owner/time/state:** REA independent / 2026-10-24 07H JST / STATIC (limited native-source instruction history), INFERRED where stated, VERIFY; Golden PASS 0, READY 0.
- **Owner source:** `rea_lab/decomp_task/REA_20261024_07H_P0_B136_FIRST_INSERT_STATIC.md` / SHA256 `83FD188C6B7D4D421DBC53BE354733F9BA90B40275071BC5D48D257FB491EDAC` (read-only file hash this recovery).
- **Original evidence:** `rea_lab/decomp_task/REA_20261024_07H_P0_B136_FIRST_INSERT_EVIDENCE.json` / SHA256 `9312BBA16BC6B8A01073663487A62F740833614D2309BBD817C6DA7E6E4A06A6` (not copied to GitHub).
- **VA and CALL/offset anchors:** 0x47D770, 0x47D932, 0x47D942, 0x476720, 0x47D9B6.
- **Principal source-backed meaning:** 0x47D770 initializes B136A8 header/sentinel and attempts at least one insertion via 0x476A50 and 0x476720 before passing it to 0x48F9E0 at 0x47D9B6. Normal successful insertion increments count at 0x4768AE/AF.
- **Limitations and next validation:** Narrows earlier empty-input concern for this caller only; allocation failure, exception, reentry, other caller routes not ruled out.
- **Correction chain:** earlier owner hours are antecedent, not repeated evidence; 02H F720 ABI is already curated in develop, 03H–09H narrow its caller/generator assumptions. No formal REA five-method VERIFIED promotion.

### REA-LOCAL-20261024-08H-P0-NESTED-MAP-NONEMPTY-TRANSFER-STATIC-01

- **Owner/time/state:** REA independent / 2026-10-24 08H JST / STATIC (limited native-source instruction history), INFERRED where stated, VERIFY; Golden PASS 0, READY 0.
- **Owner source:** `rea_lab/decomp_task/REA_20261024_08H_P0_NESTED_MAP_COUNT_TRANSFER_STATIC.md` / SHA256 `AB0097FB066881AC46BD829D2DA131E14CCB2A5E734A127CD995DC325EF185CF` (read-only file hash this recovery).
- **Original evidence:** `rea_lab/decomp_task/REA_20261024_08H_P0_NESTED_MAP_COUNT_TRANSFER_EVIDENCE.json` / SHA256 `3EF92D00DF08A75C5E106D553485D92BF6855D28712409444295AA5968161CC4` (not copied to GitHub).
- **VA and CALL/offset anchors:** 0x47D908, 0x5158E0, 0x476700, 0x476B39, 0x476CCF.
- **Principal source-backed meaning:** The transient inner tree in 0x47D770 is initially empty then receives an insertion via 0x5158E0; count copying at 0x476B39/3F and 0x476CC9/CF transfers the inner count into the outer node +0x18. This supplies the earlier 0x48F720 nonzero-filter candidate in the successful path.
- **Limitations and next validation:** The inner-count==1 inference requires allocation/insert success and no exceptions; a live battle-run invariant has not been measured.
- **Correction chain:** earlier owner hours are antecedent, not repeated evidence; 02H F720 ABI is already curated in develop, 03H–09H narrow its caller/generator assumptions. No formal REA five-method VERIFIED promotion.

### REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01

- **Owner/time/state:** REA independent / 2026-10-24 09H JST / STATIC (limited native-source instruction history), INFERRED where stated, VERIFY; Golden PASS 0, READY 0.
- **Owner source:** `rea_lab/decomp_task/REA_20261024_09H_P0_THREE_TREE_PREDICATE_STATIC.md` / SHA256 `08CF585E54B45C6B917E41DA4BFD44BB6DF98474312F90803C5DC50714114F7D` (read-only file hash this recovery).
- **Original evidence:** `rea_lab/decomp_task/REA_20261024_09H_P0_THREE_TREE_PREDICATE_EVIDENCE.json` / SHA256 `4B38228C2BDCA4E382126DCD71D34217A1DFF5562DC135EB0CC19CC4F3F3A8BD` (not copied to GitHub).
- **VA and CALL/offset anchors:** 0x48F720, 0x48F752, 0x48F773, 0x5657AF, 0x5158E0.
- **Principal source-backed meaning:** Three different RB-tree node/sentinel layouts must not be collapsed into one generic layout. 0x48F720 compares exclusion keys as unsigned 32-bit values; a successful lookup may still return numeric zero if a stored node payload is zero, distinct from 'no candidate' zero.
- **Limitations and next validation:** The real producer for zero payload and valid gameplay reachability are VERIFY; avoid promoting a new unconditional crash claim.
- **Correction chain:** earlier owner hours are antecedent, not repeated evidence; 02H F720 ABI is already curated in develop, 03H–09H narrow its caller/generator assumptions. No formal REA five-method VERIFIED promotion.

## 2026-11-02 10H: 09H key-source erratum — one caller, original-PE STATIC, no new research ID

- **Owner/correction link:** existing `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` only; **new source research IDs = 0**, `errata_of` that study's "source of 0x47D8EB [ESP+0xE0] unknown" item. The preexisting general `0x48F720` dual-zero-return proof and three distinct sentinel offsets **remain valid**.
- **New PC owner report:** `rea_lab/decomp_task/REA_20261102_10H_P0_F720_ARG2_KEY_ORIGIN_ERRATUM_STATIC.md`, readback SHA256 `A79137B9F8D14A414E72455E70A55690A0918F9C2849C3D6DFCF3BDA40D682D7`. Its two original-source receipts were rehashed: 09H Markdown `08CF585E54B45C6B917E41DA4BFD44BB6DF98474312F90803C5DC50714114F7D`, evidence JSON `4B38228C2BDCA4E382126DCD71D34217A1DFF5562DC135EB0CC19CC4F3F3A8BD`. Original isolated PE independently SHA256-rehashed to `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; **not** a fresh V9 DB rehash, and no original gameplay.
- **Exact argument origin, native x86 (19 independently checked instruction sites):** `0x47D770` three SEH pushes, `0x47D77E SUB ESP,0xB8`, `0x47D784..87` four register pushes, and `0x47D78F` cookie push yield frame delta `0xD8`. `0x47D79D MOV EBP,[ESP+0xE0]` consequently reads **entry-SP+8 = incoming stack argument 2**, not an anonymous local. Transient PUSH/ADD pairs `0x47D826/833` and `0x47D8AF/BE` balance; `0x47D877 PUSH EAX` is consumed by `0x436340`'s native `0x4363DC RET 4` (its EBP is saved/restored). Thus `0x47D8EB LEA EAX,[ESP+0xE0]` addresses the same argument-2 stack slot.
- **Propagation to key:** `0x47D8F2 PUSH EAX` and direct `E8 0x47D8FE→0x565780` pass its address. Callee native `0x5657AF MOV EDX,[ESP+0x10]`, `0x5657B3 MOV EDX,[EDX]`, `0x5657B5 MOV [ECX],EDX`, `0x5657BA RET 4` copy **argument 2's value** into the new inner-node key `+0x0C`. Direct `E8 0x47D90C→0x5158E0` inserts in the transient tree on normal allocation success. Earlier 08H source `AB0097FB066881AC46BD829D2DA131E14CCB2A5E734A127CD995DC325EF185CF` independently traced the successful count/copy path; not independently rerun here.
- **Scoped nonzero condition:** `0x47D98A CMP [EBP+0x94],0` / `0x47D991 JE 0x47DA04` precede `E8 0x47D9B6→0x48F9E0`. On the nonfaulting normal branch, with ordinary EBP callee preservation, the seeded pointer-key cannot be zero; this does **not** prove the exclusion tree accepts it or that `0x48F720` returns a nonzero value in all callers. Other callers, exception/allocator paths, execution-time mutation, semantic pointer identity and runtime input validity stay **VERIFY**.
- **Read-only checks:** 19 Capstone instruction comparisons + 4 native E8 relative-destination checks + 2 original owner file SHA matches; a targeted independent static check, **not** 25 new functions, not formal REA five-method evidence, and not Golden. New five-method bundles 0, VERIFIED 0, original Golden PASS 0, strict MATCH 0, READY 0. PUBLISHED_INTAKE **erratum** only; independent curator must assess before `REF_*`/dictionary adoption.
- **Next unresolved:** `context+0x1EED30/34` unsigned exclusion-tree writer/membership at the normal call site and other `0x48F9E0` caller provenance; no denied Wave6/18H/protected target involved.

## Safe search/curation gates

- **Duplicate policy:** All nine are historical source IDs, not nine unrelated native functions. Compare by ID, VA, source SHA and exact alternative assertions before adopting any into `REF_BATTLE_TAKEOVER.md` or `symbols.tsv`. Do not duplicate the already-curated 02H source. Historical 00H/01H source extends previous 10/23 DemoPerson research; 03–09H sources are a progression from 02H nullable-return discovery to upstream constraints and zero-payload ambiguity.
- **Status:** owner source preservation only (PUBLISHED_INTAKE upon verified GitHub readback). CURATED is reserved for dedicated KB curator; no direct develop/REF/dictionary change. Formal five-method new bundles 0, VERIFIED delta 0, old Wave1–5 64/64 historical only, original Golden PASS 0 / strict MATCH 0 / READY 0. Revisit remaining October 23/24 20–23H reports by oldest-first source-ID comparison, subject to ownership/privacy/safety.
- **Safety:** No denied Wave6/11-01 18H materials, protected 0x5710C0–0x571500 targets, original game data, raw local paths or credentials. No source files, PC master/queue, Ghidra DB, other owner worktrees or original EXE were modified.


## 2026-11-02 11H: two original-x86 exclusion-tree argument forwarding paths (same 09H ID)

- **Owner / existing research ID:** REA / `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01`. This is a source-backed **STATIC addendum**, not a new research ID, function, verified REA Wave, curated statement or gameplay finding; preserve earlier 09H three-tree and 10H key-producer correction without overwriting either.
- **Original owner source on research PC:** `rea_lab/decomp_task/REA_20261102_11H_P0_F720_EXCLUSION_TREE_INDIRECT_CALLFRAME_STATIC.md`, newly created and independently read back on 2026-11-02 JST. Source SHA256 `3828D43A3FA4B902F5DAFE45A6E67EA6D3B9680F653906A22EB007D3137CD4DB`. Do not substitute this source report for the actual isolated PE. Original target SHA256 read back `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; current composite V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`.
- **Route A / native stack proof:** `0x49010D LEA ESI,[EBP+0x1EED30]`; `0x490113 PUSH ESI` supplies the **fourth stack argument** for direct E8 `0x490122→0x4868D0`. The 0x4868D0 SEH/register frame displacement `0x258` makes `0x487991 MOV EDX,[ESP+0x268]` its fourth incoming argument on the balanced path; `0x4879A0 PUSH EDX` forwards it as the **sixth** of seven arguments for E8 `0x4879BF→0x489630`.
- **Route B / native stack proof:** `0x4901A7 MOV ESI,[ESP+0x4C]` establishes the context in 0x490180; `0x49020B LEA ECX,[ESI+0x1EED30]` and `0x490211 PUSH ECX` supply fourth argument for E8 `0x49021A→0x488290`. Its SEH/register frame `0x194` gives `0x488C13 MOV EDX,[ESP+0x1A4]` as fourth incoming argument; `0x488C22 PUSH EDX` forwards it as sixth for E8 `0x488C44→0x489630`. These are the two independently sourced **pointer-carriage** chains; neither establishes the actual exclusion-tree writer.
- **Independent bounded receipt:** exact original-PE E8 rel32 destinations **4/4 PASS**; saved source includes seven native byte-window SHA256 hashes covering both caller chains, both callee prologues and the 0x489630 prologue. Two core transfer-window hashes: `0x487991..0x4879C4` = `76867CAFDACB3A67A6F8D6BDD7EF522D392352ADA252BFCBC128A190E6BED77E`, `0x488C13..0x488C49` = `006903E47A678A7C588369161661C909E2E2E21FA8901B10CFC30C8C3EE45799`. No new full function decompilation or game execution. Other-owner B/T028 earlier `0x4907C0` / `0x4939AE` lookups remain separate prior evidence, not a new REA discovery.
- **Important VERIFY boundary:** following the address into 0x489630 does **not** show a write to context+0x1EED30/34, actual map membership, node layout equivalence, a nonnull global invariant or original gameplay reachability. F720 exclusion-node sentinel `+0x19` and outer candidate-node sentinel `+0x21` must not be conflated; V9 reconstructed `param_6` semantics alone do not establish native writer ownership. Next legal cursor is the 0x489630 sixth-stack-argument use/indirect mutation sites (bounded original ASM), then other 0x48F9E0 callers. Curator alone handles REF and dictionary admission.
- **State:** PUBLISHED_INTAKE / STATIC / VERIFY / NOT_CURATED / NOT_READY. Formal new five-method REA verified bundles **0**, new VERIFIED **0**, original-game Golden PASS **0**, strict MATCH **0**, READY **0**. No protected VA/Wave6/18H refusal bypass; no developer branch, REF, dictionaries, QUEUE/PROGRESS, original assets, or other-owner modifications.

---

**2026-11-02 12H source readback receipt:** authorized PC owner Markdown SHA256 `D604EE21C9366711232A2C447B061820A6661BD8DFE4F776309F8425A530D52A`. Full sanitized owner report below, same original 09H research ID; not a new research ID or CURATED.

# REA 2026-11-02 12H | exclusion-tree sixth-argument use in 0x489630 / downstream arg8 filter
- **research_id:** `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` (existing owner ID; **new research IDs 0**).
- **owner / task:** REA independent / P0 T015. Addendum to 10/24 09H and 11/02 10H/11H source; no separate independent function claim.
- **stage / confidence:** original-PE `STATIC` bounded stack/unsigned lookup and direct E8; direct/indirect writer identity, pointer alias side effects, runtime reachability, Golden remain `VERIFY`; `NOT_CURATED / NOT_READY`.
- **original source:** `rea_lab/targets/hakushin067_Vahren.exe`, independently hashed SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
- **read-only V9:** `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`, independently hashed SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`, used only for bounded function/callsite cross-check; not an ABI authority.
- **prior source:** `rea_lab/decomp_task/REA_20261102_11H_P0_F720_EXCLUSION_TREE_INDIRECT_CALLFRAME_STATIC.md`, SHA256 `3828D43A3FA4B902F5DAFE45A6E67EA6D3B9680F653906A22EB007D3137CD4DB`, linked via same research ID (not superseded).
## Original x86, argument and effect boundary
- `0x489630` after SEH/register/cookie prologue has normal ESP displacement `0x88`: `0x48974D MOV EAX,[ESP+0xA0]` reads **sixth incoming stack argument** (`entry ESP+0x18`); `0x489762 PUSH EAX` is first of eight pushed arguments to `0x48977F E8→0x489DB0`, making the same tree-container pointer the **eighth callee stack argument** (on balanced ordinary path).
- `0x489630` also reads the sixth argument at `0x489893 MOV ECX,[ESI+4]` after `0x48988C MOV ESI,[ESP+0xA0]`. `0x489899 CMP BYTE PTR [EAX+0x19],0`, `0x4898A0 CMP [EAX+0x0C],EBX`, `0x4898A3 JAE`, `0x4898BF CMP EBX,[ECX+0x0C]`, `0x4898C2 JB` implement an unsigned-order membership/predicate path, not a proved insertion.
- A second direct read-only traversal starts `0x489A21 MOV EDX,[ESP+0xA0]` and `0x489A28 MOV EDI,[EDX+4]`; its node comparisons use sentinel `+0x19`. Separate outer-candidate lookup at `0x489A62` uses node `+0x21`, so the 09H three-layout distinction remains necessary.
- `0x489DB0` after its `0x5C` stack displacement reads arg8 at `0x489EA0 MOV ESI,[ESP+0x7C]`, then `0x489EA4 MOV ECX,[ESI+4]`, `0x489EAA CMP BYTE PTR [EAX+0x19],0`, `0x489EB6 JAE`, `0x489EE2 JB`. It checks another unsigned-order membership path, rather than establishing a writer to the forwarded tree.
- Separate `0x489630` `0x489BF9→0x565780` and `0x489C07→0x5158E0` operate on a newly allocated **local inner tree**. `0x489DB0` `0x489E11/1B` and `0x489E2D/37` use `0x565780/0x5158E0` on actor-owned containers, not the explicitly forwarded exclusion-tree pointer. Other side effects and aliases remain VERIFY.
- **Bounded negative evidence only:** inspected direct dereferences of the sixth/arg8 tree-container pointer are reads/comparisons; **no direct store through that pointer was seen in these windows**. This does NOT prove global immutability, absence of aliasing or indirect mutation elsewhere, or membership at `0x48F720`. Actual producer/writer of `context+0x1EED30/34` is still unresolved.
## Independently repeatable read-only receipt
- Hash-checked original PE and V9; Capstone exact native instructions **17/17**, original E8 rel32 targets matched V9 native_callsite **7/7** (including `0x48977F→0x489DB0`); two V9 function rows observed (sizes 1887/1413 bytes). No new REA runner, Ghidra decompilation, game or synthetic Golden.
- Window hashes SHA256: `0x48974D..0x489780` `E9B58667E0FC64CB3D12E9D9E290FEBCE63DC1414F7D53E383078F5E71162520`; `0x489893..0x4898E8` `A815BC79BDD196EA5D69E1ECBB8291FB2A191F3053B0BBFE8B85C5D418B9F03F`; `0x489A21..0x489AB5` `733BB1E62748484BD7C7E2D3053EB402B9747759BF3234F7C661D154DD8DFE1A`; `0x489EA0..0x489F00` `2EDF58E3C46DCCED6FCC3C250DB7EBB6514165062D008FF1969041C477C64246`.
- **Next lawful cursor:** identify true `context+0x1EED30/34` tree writer via bounded original-x86 callers/field xrefs, then inspect other `0x48F9E0` callers and corrections; original gameplay remains untested.
- **Gates:** new formal five-method REA VERIFIED 0, Golden PASS 0, strict MATCH 0, READY 0, no curated adoption claimed; historical Wave1-5 64/64 unchanged. No protected `0x5710C0..0x571500`, refused Wave6/18H or original game touched. No edits to shared develop/REF/dictionaries, other owners, QUEUE/PROGRESS.

---

**2026-11-02 12H owner correction receipt:** PC source SHA256 `ACAA0D4BA0427FF2A9DDF21003F34AAEA87CCF7798CDFCEB3D658FDCC43C9F0A`; same existing REA 09H research ID, curation pending. Source-backed reset writer finding follows.

# REA 2026-11-02 12H | F720 exclusion-tree reset writer identified at 0x48FB96 → 0x4F8ED0
- **research_id:** `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` (existing; **new research IDs 0**); owner REA / P0, addendum + erratum to 11H/12H “tree writer unknown” boundary.
- **evidence:** bounded original PE32 x86 `STATIC` plus read-only V9 direct-E8 crosscheck. Target `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`.
- **prior source:** `rea_lab/decomp_task/REA_20261102_12H_P0_F720_EXCLUSION_TREE_FILTER_ARG8_STATIC.md` SHA256 `D604EE21C9366711232A2C447B061820A6661BD8DFE4F776309F8425A530D52A`. Earlier 10/24 09H, 11/02 10H/11H reports and all their independent conclusions remain linked.
## Direct native x86 mutation: scoped tree clear/reset, NOT an insert producer
- In `0x48F9E0`, `0x48FB84 LEA EDI,[EBP+0x1EED30]` points **EDI** to the comparison-tree container; `0x48FB96 E8→0x4F8ED0` retains that implicit EDI pointer. This is a direct native caller/callee contract, not a guessed Ghidra prototype.
- `0x4F8ED0 MOV EAX,[EDI+4]`, `0x4F8ED4 MOV EBX,[EAX+4]`, `0x4F8ED7 CMP BYTE PTR [EBX+0x19],0`, `0x4F8EDE JNE 0x4F8EFE`: a node-sentinel test; nonempty chain calls `0x4F8EE6 E8→0x501C10` for nested cleanup, then `0x4F8EEE E8→0x5B6BBB` for node release, advancing until sentinel. This is more than read-only membership testing.
- Clear end `0x4F8F01 MOV [EAX+4],EAX`, `0x4F8F07 MOV [EAX],EAX`, `0x4F8F0D MOV [EAX+8],EAX` sets the header links to itself; `0x4F8F10 MOV [EDI+8],0` sets container count zero. For caller EDI=`context+0x1EED30`, this last write is `context+0x1EED38=0`. Header access is `[EDI+4]` (context+0x1EED34).
- Therefore **one original-x86 writer of the exclusion-tree state is established: the clear/reset path**. Correction of 11H’s broad “writer unknown”: the **insert/create/population key path is still unknown**, as are original-game reachability, time/order and alias effects. The `0x489630` sixth-argument usage remains bounded as read/predicate in previously inspected windows; both facts can coexist.
## Independent verification, limitations, and curator handoff
- PE and V9 file SHA independently recomputed. Capstone exact original-ASM checks **23/23 PASS**; direct rel32 E8 + V9 native_callsite `0x48FB96→0x4F8ED0`, `0x4F8EE6→0x501C10`, `0x4F8EEE→0x5B6BBB` **3/3 PASS**. V9 `0x4F8ED0` function size 73 bytes. Other indexed E8 callers `0x43289B`, `0x49B075`, `0x4F8BB7` use the same helper but their tree-container identities have not been established here.
- Native byte-window SHA256: `0x48FB84..0x48FB9B` = `1292688AABDE04821A6C696D6764CF223323BEA53742D7DF5C3AC2964A3A7338`; `0x4F8ED0..0x4F8EF4` = `A0F3BE18BCDE4F5DFBD55B60D3D61AA56602A340CF10915681138922C5FDC2AD`; `0x4F8EFE..0x4F8F19` = `A607891E78076B7632DE2E5510D6B0A635934387D29987F08A85D4C9A2F0DE80`.
- **Do not infer:** absence/presence of exclusion keys at `0x48F720` on any real frame, all other writers, nonnull invariant, crash, global lifetime, exception safety, or actual Golden. `0x501C10` payload/subtree lifetime semantics need a separate bounded audit before equating this to all destructor side effects. No new complete REA five-method evidence or formal VERIFIED. Historic Wave1–5 64/64 unchanged; Golden PASS 0, strict MATCH 0, READY 0.
- **Next lawful cursor:** prove the exclusion-tree **insertion/population** source and writer (including alias escape via 0x491870/0x40D0A0 only with native evidence), then identify actual `0x48F9E0` caller ordering. Dedicated KB curator only may integrate into `develop` REF/symbols after independent verification; this owner report is `PUBLISHED_INTAKE / STATIC / VERIFY / NOT_CURATED`.
- **Safety:** refused Wave6/18H and protected VA untouched, no original-game/REA/Ghidra run, no writes outside REA-owned report and permitted private intake branch, no QUEUE/PROGRESS/other-owner/REF/develop edits.
