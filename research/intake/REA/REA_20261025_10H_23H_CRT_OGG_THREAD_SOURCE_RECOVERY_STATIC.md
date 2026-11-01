# REA owner historical recovery: 2026-10-25 10–23H, CRT, Ogg and thread

Private owner intake, STATIC/INFERRED and VERIFY; original Golden PASS 0, READY 0, formal new five-method/VERIFIED 0. Twelve historical owner reports; research was performed in October, **not** rerun now. Authorized PC report and available small EVIDENCE JSON SHA256 measured read-only 2026-11-02 JST. Original PE target SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` are historical source receipts, not newly remeasured in this recovery. No PC modification or new REA/game runs. EVIDENCE JSON remains on PC.

### REA-LOCAL-20261025-1040-P0-CRT-NEWMODE-INIT-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_10H_P0_CRT_NEWMODE_INIT_STATIC.md`; actual local report SHA256 `CB97740B2568AAFE745B52AA10ECD9C1777A08C7375A90A19398AF80745A68F2`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `D5E5ACCF6F17BB1D6C69EB7958692C890F238A2B14DB218180E1CBA4A0D426AF` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x68E8C0, 0x68DFE8, 0x5BBA70.
- **Bounded original-source finding:** CRT .data zero-initialized new-mode and encoded new-handler; on ordinary initial state mode=0, decoded handler=NULL and stock new wrapper failure raises bad_alloc. Later hooks/indirect writes not excluded.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-1137-P0-CRT-GLOBAL-XREF-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_11H_P0_CRT_GLOBAL_XREF_STATIC.md`; actual local report SHA256 `3A118E3997DB1C666F96C999F4BB404817527D31D894C7D7257B929DAF6CD93D`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `3CBF7AA917E35914639530FF1153B67D1A457538364E76F6C890063CD421CE37` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x5B9C1C, 0x5C3089, 0x5C3109.
- **Bounded original-source finding:** Direct xrefs to new-mode found only in malloc/calloc/realloc; handler setter direct write/read limited to 0x5BBA70/7C. Realloc/calloc NULL and errno behavior differs from C++ new throwing wrapper; other indirect/externally installed modes unproven.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-1236-P0-REALLOC-OVERFLOW-ERRNO-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_12H_P0_REALLOC_ERRNO_STATIC.md`; actual local report SHA256 `48D828A41A6CAA6FAAD8DC82ED3C289EC52A41B3D55FF929E506777B14420239`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `376B32C95B158E66D81691934CA64FC4C732E46DB5C81CC3392B067F5746CE6C` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x5C30BE, 0x5C311C, 0x5C3122.
- **Bounded original-source finding:** Unsigned bound size<=0xFFFFFFE0 takes HeapReAlloc, otherwise __callnewh and errno=12 on normal return; ptr=NULL delegates malloc, nonnull ptr with size0 frees. Handler can throw or change LastError; real error precedence unobserved.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-1537-P0-PARSE-COUNT-BOUND-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_15H_P0_PARSE_COUNT_STATIC.md`; actual local report SHA256 `F1427B1FDE3668AB80D9A0124BA3A0ED810C2326035C3427DC7867A62FC481F3`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `372F599E3EE05937B7901A775F83B571A4905BF4BE0C6D657081F1DE46FAE27D` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x5CF010, 0x5CF0D6, 0x5CF1D5, 0x5D159A.
- **Bounded original-source finding:** Unique-token parser increments output count; duplicate error frees/reset outputs and returns -133. Later (count+2)*4 allocation and count*4 copy, with no proven input count ceiling. Potential integer/alloc overflow reachability VERIFY.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-1636-P0-PARSE-ERROR-FREE-CALLBACK-GATE-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_16H_P0_PARSE_FAILURE_CLEANUP_STATIC.md`; actual local report SHA256 `9B581EBA898D04D335B5B24D83A524455F8C5114959F4565CDBAC4CC23EA2861`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `E9F17DC6F4D895A04291194D6CFFBEC447E1911C005BED5DF83BAA34F3258BD9` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x5D1587, 0x5D1614, 0x5CFEDF, 0x5CFEEE.
- **Bounded original-source finding:** Native shared epilogue 0x5D1614 array free remains reachable despite earlier Ghidra unreachable-block removal. Error path zeros context[0], thereby disabling FILE callback during cleanup; exception completeness remains VERIFY.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-1736-P0-FILE-CLOSE-CALLBACK-BRIDGE-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_17H_P0_FILE_CLOSE_CALLBACK_STATIC.md`; actual local report SHA256 `55C51334154EBF49CA50EF3B8C18F727ED6AAEF7C0ADC1EAC7C7AC45573E5ACC`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `D3E9218E488A1574DE886E37B5A10CC29C8DF0D6CEFCDABB72EC518289B39B7A` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x5D16C0, 0x5D1701, 0x5D1490, 0x5CFEEE.
- **Bounded original-source finding:** Fopen wrapper transfers _fread/fseek/_fclose/ftell callbacks; context+0x2C8 holds _fclose for this path. Failure wrapper closes FILE, success decoder ownership closes later. Same pointer appears in 10/29 Ogg research, not newly discovered in this recovery.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-1836-P0-OGG-VSLOT10-RELOAD-LIFETIME-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_18H_P0_OGG_VSLOT10_RELOAD_STATIC.md`; actual local report SHA256 `C450041E51EA8959EF1C7936D9F69552D6282D3B625122B70B44CF4DD8E823D7`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `6445B2875233C92197C39BC2DDA004D4B7884D5C1157CD0B8E29C7D91D9DBA26` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x50202A, 0x6395CC, 0x501EB0.
- **Bounded original-source finding:** OggDecoder slot+0x10 maps to conditional old-file cleanup 0x501EB0 before reopen. Constructor returns this even if load fails; PCMDecoder +0x10 is a different method. Upper failure gate later clarified.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-1934-P0-OGG-STREAM-GATE-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_19H_P0_OGG_STREAM_GATE_STATIC.md`; actual local report SHA256 `36D5F6CA9E117AA19439CA46A1D1449A8F70DB5026874DAFFDD0607E0FA404DA`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `4062D350DCD4AEB4662C3778C295E1091A09110A02C1AFF75E7F90948506A39D` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x4BEAFA, 0x502220, 0x502300, 0x50230E.
- **Bounded original-source finding:** Upper stream checks state byte+0x44, not constructor return, and 0x502220 sets +0x44 after buffer/COM setup. __beginthread return is stored without -1 validation before +0x44=1; possible thread-failure gap not measured live.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-2034-P0-OGG-TEARDOWN-THREAD-WAIT-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_20H_P0_OGG_TEARDOWN_THREAD_STATIC.md`; actual local report SHA256 `C738BF9EE231B349CCBEEE84A7BC60A65D0AB22B934BE730B660F81B0E150170`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `8761A74D427BAA90A10B1108103BCF5DBC3BCBD35502F8D04C9AC1A2058ADAD6` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x502160, 0x5021E0, 0x5021AF, 0x501DF0.
- **Bounded original-source finding:** Stop worker before COM/decoder release; Ogg slot+0x10 cleanup then deleting destructor(flag1), with owner+5 guard preventing second _fclose. WaitForSingleObject(handle,100) is 100ms per retry, not 100ms total. Handle leak unproven.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-2134-P0-CRT-THREAD-HANDLE-CLOSE-RACE-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_21H_THREAD_HANDLE_STATIC.md`; actual local report SHA256 `F2468BD31102747E2CB4EB6A8E2030D41F7AC66EBEF53C0C2DE5494DEE80E1D9`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `7409A9670A3858F6B92658FD3F14071653F7C36A109E8F084EE1635B5297F061` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x5B7D14, 0x5B7DAF, 0x5B7C92, 0x5B7C64.
- **Bounded original-source finding:** CRT __beginthread may yield EAX=-1, stored raw by stream +0x48 but success flag set. Normal thread exit path invokes CRT __endthread and CloseHandle, correcting simplistic handle-leak inference from Ogg module alone.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-2234-P0-CRT-START-FAILURE-OWNERSHIP-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_22H_P0_CRT_START_FAILURE_STATIC.md`; actual local report SHA256 `E8E5F71A614AF288EEF0097617F8FD6E49ABD1E6FBE0E81BA88F385380F735FF`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `4C638A2C95752D2938F6841655D6934F2E12E159CCB83794420D6C39437E3FCB` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x5B7D8A, 0x5B7D90, 0x5B7CE2, 0x5B7CED.
- **Bounded original-source finding:** CreateThread success then ResumeThread failure frees PTD but locally shows no CloseHandle; early FLS set failure ExitThread bypasses ordinary CRT __endthread. No real resource leak certified without original-game evidence.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

### REA-LOCAL-20261025-2334-P0-FLS-RETURN-ABI-REFUSAL-STATIC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261025_23H_P0_FLS_ABI_RECOVERY_STATIC.md`; actual local report SHA256 `41934826B046559C29D9E39A8C14F359BF76F56065AD3FF6ECF70D5D4C0FD39F`.
- **PC evidence:** adjacent owner EVIDENCE JSON, local SHA256 `0EC2495ACEB2551A7493496E07D37F15A164A9C03057B84F6A606F0792546BDF` (not uploaded); evidence basename may differ from report.
- **VA/CALL/offset anchors:** 0x5BC522, 0x5BC539, 0x5B7CDD, 0x5B7CE2.
- **Bounded original-source finding:** Previously obtained allowed static observations indicate FLS-set wrapper indirect CALL and caller testing EAX, inconsistent with void pseudo-C. Later composite function query was safety refused (REA-RC-20261025-2334-FLS-FUNCTION-QUERY-SAFETY-01); no denied targets/data obtained/retried, return ABI remains VERIFY.
- **Status:** historical STATIC, conditional INFERRED, VERIFY; no formal REA 5-evidence completed or VERIFIED promotion, original-game Golden/READY = 0. Compare with prior/later owner ID and V9 native x86 before adopting.

## Curation and safety handoff

CRT mode, calloc, realloc, C++ new/throw must not be collapsed to a single NULL contract. Older Spot allocation NULL-retry inference was corrected by the 08H owner report. Ogg/FILE callback, decoder reload and thread cleanup have cross-source overlap with 2026-10-29/30 owner intake; identical VA is a link, not a new native function. The 23H FLS compound-query safety refusal has no result to preserve and is **BLOCKED**; only allowed pre-refusal static FLS CALL/caller claims above. No refused search, Wave6, 2026-11-01 18H evidence, or protected VA was reattempted or published. Curator alone may incorporate into develop REF/symbol dictionaries after source, errata and native verification. New formal VERIFIED 0, original Golden PASS/READY 0. Next old source cursor 2026-10-26 00H.
