# REA historical source preservation: ArmyChip manager ownership and Spot allocator/EH, 2026-10-24 20H–2026-10-25 08H

**Owner:** REA independent; **stage:** PRIVATE owner intake / PUBLISHED_INTAKE only after verified GitHub readback / STATIC and conditional INFERRED or SYNTHETIC / VERIFY / NOT CURATED / NOT READY. These are 14 existing historic research IDs, **not** 14 newly analyzed native functions and not an original-game run.

Source SHA256 values below were measured read-only from the authorized PC's own `rea_lab/decomp_task` files on 2026-11-02 JST. Each source report is retained on PC; GitHub holds a substantive, sanitized source/claim/errata/next-verification crosswalk. The EVIDENCE JSON hashes below refer to PC-only files and are *not* uploaded. Original PE owner-reported SHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; unified V9 owner-reported SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. This recovery did **not** re-hash original PE/V9, rerun old audits, run REA/Ghidra or test the game. Existing historical 64/64 five-method Wave1–5 is not newly measured.

### REA-LOCAL-20261024-20H-P0-ARMYCHIP-CHILD-VCALL-ORDER-STATIC-01

- **Date / owner:** 2026-10-24 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261024_20H_P0_ARMYCHIP_CHILD_VCALL_ORDER_STATIC.md` / freshly rehashed SHA256 `10ADFCFD0FB9F509CEB6D93BD55D05BF4F1F74D5741EF6DC30F354FFED681A82`.
- **PC-only evidence SHA256:** `BAA5E66C6235E2304B5F37C0A73B6BEF589476A31910B59F14778C68FC96CF7C`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x5B0A50; 0x5B0B53/+0x34, 0x5B0B5C/+0x08, 0x5B0B77/+0x48, 0x5B0B91/+0x44; 0x4BC9C0.
- **Original owner's static meaning:** ArmyChipBuilder iterates child pointer vector +0x14/+0x18 and performs four FF D0 indirect child vptr calls. +0x08 nonzero AL triggers manager unregister(flag0); +0x48 nonzero AL routes 0x4C3E40; +0x44 zero AL queues child at 0x4C2440, while nonzero clears child+0x6C. One unconditional 0x4BC9C0 call follows each element. Direct E8 caller count cannot resolve these FF D0 targets.
- **Errata, limitations, next check:** No all-class virtual target proof here; per-class resolution follows at 21H. A separate prior CLI target refusal was not rerun and forbidden target artifacts are not preserved.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261024-2035-P0-CHILD-VCALL-AL-BRANCH-MATRIX-STATIC-01

- **Date / owner:** 2026-10-24 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261024_2035_P0_CHILD_VCALL_BRANCH_MATRIX_STATIC.md` / freshly rehashed SHA256 `3EFF956B8DCB214D8C6669A6C69A21F8A62729272DA6FFD756E3D4D615321AB8`.
- **PC-only evidence SHA256:** `2E3B782210A60137299015D54BD8FFD52E4A2A909B910935369149D56344D6A7`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x5B0B5C, 0x5B0B60, 0x5B0B77, 0x5B0B7B, 0x5B0B91, 0x5B0B95.
- **Original owner's static meaning:** Computed four signed 8-bit short-branch destinations and a three-AL-return conditional table for the child virtual calls, making clear that the three gates execute sequentially on normal return, not as a short-circuit expression.
- **Errata, limitations, next check:** Truth table is SYNTHETIC branch-combinatorics only, not eight observed runtime cases; 21H resolves one ArmyChip-vptr-specific (1,0,0) result. No new source-code branch measured.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261024-2137-P0-ARMYCHIP-CHILD-RTTI-VCALL-TARGET-STATIC-01

- **Date / owner:** 2026-10-24 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261024_2137_P0_ARMYCHIP_CHILD_RTTI_SLOT_STATIC.md` / freshly rehashed SHA256 `6D62F854148A7E580F7C266BEF2CF8DBE2CA250CC8E4F6923A5CD51CBAB48D4A`.
- **PC-only evidence SHA256:** `5123F0F31B7D8A6B228B5C11EED36FD793B3CD925F8E3AF06D054C7555352AA1`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x5B0EA0, 0x5B0F42, vtable 0x63AE74, 0x4BBBD0, 0x431910, 0x43B5A0.
- **Original owner's static meaning:** Identifies created child's RTTI as ArmyChipBuilder::ArmyChip with vtable 0x63AE74; resolves +0x34 to RET-only 0x4BBBD0, +0x08 to AL=1 0x431910, +0x48 and +0x44 to AL=0 0x43B5A0. For unchanged vptr this narrows earlier theoretical (AL8,AL48,AL44) combinations to (1,0,0), yielding conditional manager flag0 removal and delayed queue addition.
- **Errata, limitations, next check:** Does not prove arrays never include other polymorphic types; previous safety-refused search target remains unprobed.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261024-2238-P0-ARMYCHIP-VECTOR-LIFETIME-STATIC-01

- **Date / owner:** 2026-10-24 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261024_22H_P0_ARMYCHIP_VECTOR_LIFETIME_STATIC.md` / freshly rehashed SHA256 `64578FE1B67705DCB6B0329A5BA703E2DD2F8F105AB51FB970E0E3710958935E`.
- **PC-only evidence SHA256:** `E18C3B50698453C3394933A6B5A469A2CC1E86B5A79CE2F49464E647C84BE60D`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x5B0880, 0x5B0980, 0x5B09A0, 0x5B0A0E, 0x5B0EA0, 0x4C1290.
- **Original owner's static meaning:** Builder child-vector begin/end/capacity at owner+0x14/+0x18/+0x1C are initialized to null; parent destructor 0x5B09A0 frees vector allocation and clears fields without a direct child-destructor call within that function. Distinguishes parent container memory from individually allocated child objects.
- **Errata, limitations, next check:** Absence of direct child destructor in bounded parent destructor does not prove a leak: another owner may destroy children; investigate manager queue.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261024-2334-P0-ARMYCHIP-CHILD-DTOR-OWNERSHIP-STATIC-01

- **Date / owner:** 2026-10-24 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261024_23H_P0_ARMYCHIP_CHILD_DTOR_STATIC.md` / freshly rehashed SHA256 `9E3AEF1E126582E4D1F81BB9E2F54E83F733912AD5FDC4FBC786945456CBF738`.
- **PC-only evidence SHA256:** `701D76AD3CA43AE70A765E2BF51025976C77D29CB6FDDA3E0CA0C97B49986A1B`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x5B1310, 0x5B1313, 0x5B1330, 0x5B1320, 0x5B1359, 0x5B13BC.
- **Original owner's static meaning:** Child vtable+0 destructor wrapper 0x5B1310 calls cleanup 0x5B1330 then conditionally frees own object memory when delete-bit flag set. Child body frees internal linked structures; no direct E8 callers were known. Separate the child object memory from parent vector allocation.
- **Errata, limitations, next check:** No direct-E8 callers does not imply never used; 10/25 00H resolves an indirect manager deletion route.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261025-00H-P0-ARMYCHIP-DEFERRED-OWNER-VCALL-GATE-STATIC-02

- **Date / owner:** 2026-10-25 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261025_00H_P0_ARMYCHIP_OWNER_QUEUE_DESTRUCTOR_STATIC.md` / freshly rehashed SHA256 `B348032C1A268C66C8F205E673D3A398D0AE2BE173050B87707D3E39D18D6DA3`.
- **PC-only evidence SHA256:** `B994F8011695CE94869B8A2CD0F85C6CEBE54A823BCCEBA916662C0A20B0935E`; `569498AFEC9B5B7E1A3342EB06C7BE7B8BA27DEFF2133FF36C75B4D3166CD136`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. Earlier exploratory 55/56 audit FAIL and its raw JSON are SUPERSEDED, not a validated third evidence set.
- **Native VA / CALL / offset anchors:** 0x5B0B5C, 0x4C22B0, 0x4C2440, 0x4C24B0, 0x4C27C1, 0x4C2825.
- **Original owner's static meaning:** Child +0x08(AL=1) triggers active-manager removal, and +0x44(AL=0) enqueues child into manager+0x44/+0x48. Manager loop later issues vptr+0 indirect destructor with PUSH 1 at 0x4C2825; if child remains ArmyChip vptr, this dispatches 0x5B1310. Parent enters different conditional +0x54/+0x58 queue, with vptr+0x14 predicate before 0x4C27C1 deletion.
- **Errata, limitations, next check:** Two delayed queues do not certify no double-free or runtime manager identity; the exploratory candidate-counting result 55/56 FAIL was corrected by a narrower 35/35 historical gate audit.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261025-0131-P0-ARMYCHIP-MANAGER-TRANSFER-EXITGATE-STATIC-01

- **Date / owner:** 2026-10-25 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261025_01H_P0_ARMYCHIP_MANAGER_GATE_STATIC.md` / freshly rehashed SHA256 `3A96013A65A8B2EEF46F0915C0A165FA362EF91603BF4E7A8B4B4097D8AEB471`.
- **PC-only evidence SHA256:** `F3886EBE89F9F05E088907EB68A933D003CC66C8B72A97413F527DC3B96E3B59`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x5B06EA, 0x5B0843, 0x5B0B42, 0x4C2980, 0x4C28D0, 0x4C2780.
- **Original owner's static meaning:** Builder+0x24 stores owner X, both builder registration and later child queue handling derive manager M from [[X+0x0C]+4]+0x0C. An owner waiting vector (+0x64/+0x68) transfers into active vector (+0x2C) through 0x4C28D0, and +0x44/+0x54 delayed deletion processing is after a nonzero exit gate in 0x4C24B0.
- **Errata, limitations, next check:** Same manager derivation formula is conditional on owner X remaining unchanged; 02H finds separate caller-supplied X values. It is not proved both manager roots are identical at runtime.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261025-0236-P0-ARMYCHIP-TWO-OWNER-RETURN-STATIC-01

- **Date / owner:** 2026-10-25 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261025_02H_P0_OWNER_ARG_STATIC.md` / freshly rehashed SHA256 `C85C14A1101D7F0B70201BEF8B946277F93603400C9A1EE0DE8C6D9F3A2D8611`.
- **PC-only evidence SHA256:** `20A53D35838BEFE1808C954336EBED10170A6ED2629A3446E310A0497BED4D60`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x4917B3, 0x491E99, 0x5B0680, 0x597BA0, 0x5B06EA, 0x5B06ED.
- **Original owner's static meaning:** Two x86 rel32 callers of builder ctor 0x5B0680 supply potentially different owner X from 0x597BA0 EAX return. The ctor uses ECX as a separate object pointer and copies owner stack argument to builder+0x24, ECX to +0x28. Corrects V9's `void` pseudocode expectation for 0x597BA0, whose return EAX is actively consumed.
- **Errata, limitations, next check:** No universal equality between two owner X values or between their manager and root global. Producer register/spot cache and dynamic ABI require more testing.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261025-0336-P0-SPOT-RESOLVER-EAX-CACHE-STATIC-01

- **Date / owner:** 2026-10-25 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261025_03H_P0_SPOT_RETURN_STATIC.md` / freshly rehashed SHA256 `C625E5EC40D966A523A66E866C8F9BB21F4B9D87309833E4D03E83A3DB751C95`.
- **PC-only evidence SHA256:** `4AA456C27E33A42834677C70E4611AC6785B031975AA42F485B3C4C1A5377206`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x49E490, 0x49E524, 0x49E530, 0x597BA0, 0x597BDF, 0x597BE6, 0x597C74.
- **Original owner's static meaning:** 0x49E490 returns resolved Spot-pointer or EAX=0 on tree-end; 0x597BA0 first uses lookup hit, otherwise shared global cache [0xAC0990], otherwise constructs fallback object and stores return in cache. Both helpers' EAX returns contradict simplistic `void` Ghidra pseudotypes.
- **Errata, limitations, next check:** Do not assume a successful return is a fully initialized/live Spot without caller contract; original malloc failure->normal-NULL fallback explanation is corrected by 08H allocator throw behavior.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261025-0433-P0-SPOT-CACHE-ATEXIT-OWNER-SPLIT-STATIC-01

- **Date / owner:** 2026-10-25 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261025_04H_P0_CACHE_ATEXIT_SPLIT_STATIC.md` / freshly rehashed SHA256 `26EF919F78AF574B11F4B1E0AF37500BC4FC057476411C8370569F986A8FB1EE`.
- **PC-only evidence SHA256:** `238239D442D3399EFE2D7C7739A0C8EEC01C6E65ACDC2A171BE631B640F914C0`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x597BF9, 0x597C12, 0x597C1C, 0x608C20, 0x432DF0, 0x597C3D.
- **Original owner's static meaning:** atexit callback 0x608C20 registered by _atexit releases separate helper at global 0xB0B008, not directly the Spot fallback cache [0xAC0990]. Distinguishes helper allocation/throw from 0x36C Spot allocation check.
- **Errata, limitations, next check:** Later 08H refines interpretation of 0x36C allocation-failure NULL branch: normal return of stock allocator is nonnull, otherwise new-handler or exception.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261025-0535-P0-SPOT-EH-UNWIND-GUARD-STATIC-01

- **Date / owner:** 2026-10-25 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261025_05H_P0_SPOT_EH_UNWIND_STATIC.md` / freshly rehashed SHA256 `C507C2FEAC55580089A85769874638902BADC86E3D3493C055A7A61D98DD822D`.
- **PC-only evidence SHA256:** `C7EBC68AD47F631C7899893AE16063EB597F84B1473B7A2FF2C34DCCC05DEFB0`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x597BA0, 0x5F8B70, 0x5F8B7E, 0x5B6BBB.
- **Original owner's static meaning:** MSVC C++ EH state0 unwind callback clears bit0 only of helper initialization guard; state1 callback uses EBP-frame local [EBP-0x10] as pointer to free. Distinct state/action map separates helper guard reset from Spot allocation cleanup.
- **Errata, limitations, next check:** EBP identity and actual pointer slot are proven only for standard state1 unwind in 07H; no real exception injection or double-free measurements.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261025-0636-P0-SPOT-EH-FRAME-SLOT-STATIC-01

- **Date / owner:** 2026-10-25 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261025_06H_P0_SPOT_EH_FRAME_STATIC.md` / freshly rehashed SHA256 `853852B9384E27D1B2C955A9F1DE2BB4DE5A7562310B019801CD0FDA9C9DCBEB`.
- **PC-only evidence SHA256:** `9AFAEB2CC7396FE6E5C6A7201AA41565D779A6431CF33781088E3819438208CC`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x597C45, 0x597C49, 0x5F8B7E, 0x5F8B82.
- **Original owner's static meaning:** Based on entry ESP=S, 0x597C45 stores the Spot allocation result at S-0x10; 0x597C49 sets EH state=1 at S-0x04. The cleanup funclet reads [EBP-0x10] and passes it to free. Condition for same pointer requires proving the EH funclet EBP base.
- **Errata, limitations, next check:** 07H resolves funclet EBP=S in legal standard unwind; initial 06H unproven frame identity must not be treated as already VERIFIED.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261025-0736-P0-SPOT-EH-FUNCLET-EBP-STATIC-01

- **Date / owner:** 2026-10-25 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261025_07H_P0_EH_FUNCLET_FRAME_STATIC.md` / freshly rehashed SHA256 `39C78A5729AF27B521C904D0CEC6B4C3DCAC6AE304B2B42E3048E057E0B45D8D`.
- **PC-only evidence SHA256:** `7AE4785960D8E8C0AE83CFB9ECC51FD03FBBA19FEBC2B1C55F9C579F3158105D`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x597BBA, 0x5B9D3C, 0x5BFB10, 0x5BFB2B, 0x5F8B7E.
- **Original owner's static meaning:** Tracks EH registration node S-0x0C through __FrameUnwindToState and __CallSettingFrame, assigning funclet EBP=node+0x0C=S. Thus standard state1 unwind passes exactly the malloc pointer previously saved at S-0x10 to the free funclet, conditionally.
- **Errata, limitations, next check:** Only conditional standard EH state1 static stack-frame contract, not runtime frequency or full hook ABI; failed allocation/constructor exceptions unobserved.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

### REA-LOCAL-20261025-0836-P0-SPOT-ALLOC-NEWH-THROW-STATIC-01

- **Date / owner:** 2026-10-25 / REA.
- **Source MD:** `rea_lab/decomp_task/REA_20261025_08H_P0_ALLOCATOR_NEWH_STATIC.md` / freshly rehashed SHA256 `431422E0A4203F7914F18058B50843FEB2B8EC42E919DBFD828843390A527B42`.
- **PC-only evidence SHA256:** `81ADFED4FBC37C3B74466F71B2C44A70CE1EDD7795BD8A06DA0DC4B8305AA4E1`. The basename of evidence JSON is source-specific (especially 10/25 00H); the SHA is a receipt, not its machine-extracted data. 
- **Native VA / CALL / offset anchors:** 0x5B6C2B, 0x5B6C35, 0x5B6C4F, 0x5BBA77, 0x5B6CA5, 0x597C53.
- **Original owner's static meaning:** Stock 0x5B6C2B allocation wrapper returns normally only with EAX nonnull; on malloc failure it calls new-handler and retries or throws bad_alloc via 0x5B864E. Therefore 03H/04H/06H prior inference 'Spot malloc fails => 0 return => cached NULL and retry next call' is not normally reachable through this original allocator. Preserve original NULL check presence, but supersede claimed normal failure path.
- **Errata, limitations, next check:** Alternative hooked allocators, handler exceptions and original-game failure injection are not measured; dynamic Golden PASS=0.
- **Grade:** STATIC/INFERRED as applicable; original live DYNAMIC=not observed, Golden PASS=0, READY=0, formally newly VERIFIED=0, new five-method evidence set=0. Check V9/original x86 and prior/later source IDs before formal adopting.

## De-duplication, correction, safety and curator handoff

- This chain advances 20H four indirect calls -> 2035 synthetic branch matrix -> 2137 ArmyChip RTTI resolution -> 22–23H vector/child-dtor distinction -> 10/25 00H delayed manager destructor -> 01–02H conditional manager owner equality. Overlapping native calls are **one x86 feature**, not many independently new functions.
- 10/25 03–08H follows Spot resolver EAX + global helper callback -> state0/1 exception unwind -> verified registration-frame arithmetic -> **08H allocator correction of the earlier normal NULL/fallback hypothesis**. Keep superseded historical source, do not erase it.
- 10/24 21H records an older safety-refused CLI search: this recovery did not re-request that evidence or the target through another path; forbidden materials are not included. Refused Wave6, Nov 1 18H partial evidence, protected VA block excluded. No original game, unredacted personal path, SQLite file, binary, generated raw audit log, or denied evidence posted.
- Formal five-method complete sets added=0, officially VERIFIED delta=0, real Golden PASS=0, strict MATCH=0, READY=0, curated develop additions by this REA owner=0. Knowledge curator alone may adopt validated semantic deltas into `REF_*`/dictionaries/develop after native source comparisons, privacy/manifest/test gates.
- **Next chronological older source after this batch:** 2026-10-25 10H (check 09H naming/provenance and actual owner source IDs before continuing); separate ongoing 10/30 cursor belongs to scheduled owner workflow.
