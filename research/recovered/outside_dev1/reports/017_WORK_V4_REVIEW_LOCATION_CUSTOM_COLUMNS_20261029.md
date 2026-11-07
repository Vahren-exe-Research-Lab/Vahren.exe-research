# v4 readonly review: location and DAT-defined numeric columns

Date: 2026-10-29. Reviewer: Work subagent generic5_adapter. Scope: source/document review only; no source edits, binary analysis, game operations, build, or new runtime tests. Existing ACTUAL results below are attributed to FINDINGS, not rerun here. This is a review record, not a new handoff.

## Reviewed state

Source root: `[USER_HOME]/Documents/迫真戦記/_REDEV_RESEARCH/data/recruit_sort_v4`.
Evidence: patch README_APPLY §§8–9; v4/DAT_UI_V4_SPEC; PEER_SCRIPT01_FINDINGS §§90–92; current runtime, visuals, v4 reader and grid; old location/presentation implementation and DAT generator.
SHA-256 rechecked after interruption, unchanged:
- core/dat_ui_v3_runtime.h: 118558E336F3F7616296B2FDD0C2CD439999DB46A8048EAE33D82D622C786212
- core/dat_ui_v4_visuals.h: 126E004A2E00E4BC53466186F10837DB9BAFE349EFE95B45319F2760EB2DE6A6
- src/work_dat_ui_v4.h: 508E006E073B6848ADC21BBAB07E08BDCF17D1C84DA5B8B06FD8D8AA75A297B8
- src/work_dat_ui_grid.h: D343CAC15A7D0E8D0C3A2A93291A654F1A9E1E764A174A9A92F4E2588838CEA3
- src/work_selector_location.h: 3CBF0CF0061C67FE2391B9941503435C1092D0F5440F2E6559B4EC8F6671C5B1
- patch/v4/DAT_UI_V4_SPEC.md: 9C36955356E7B4C632DC527E595A01D80AEE974F130C0FF92C780A3AE0444E6C

## Assessment

The explicit DAT request approach is implemented beyond a UI mockup: v4 captures 1..512 unit IDs, up to 8 numeric columns chosen from 12 built-in stats, and uses a two-choice native anchor plus an eight-per-page DAT fallback. Original candidate order remains the returned row identity through sorting/search. §§91–92 report 17/234-unit, general-unit, and lecture/student-through-execution checks. This does not establish arbitrary MOD/fullscreen correctness.
The prior successor fix remains in selector_v3_tick: after v3_show fails, revoke occurs only when active_serial still equals v3_serial. Grid partial-population failure safeguards also remain: failed initial fill destroys the grid; failed refill leaves an inert, cleared list with confirmation disabled. No rerun was done in this review.
Current v4 does NOT accept `heading=@variable`; wdu4_parse_column accepts only its stat whitelist. Location is not included. WDU3_GridInput still holds only int32 numeric extra columns. Native details are present; explicit hover-description routing from the older preview is not present in the reviewed v4 runtime/visuals.
The unresolved DirectInput click-through is material: disabling the owner window does not prevent the game polling the same mouse click. Side placement reduces overlap but is not a fullscreen solution. Lifetime validation prevents stale writes, but cannot stop the underlying DAT choice from advancing. Do not report this as fully solved input ownership.

## A. Reuse location correctly

work_selector_location_read is a useful existing adapter, but its output is a bounded CP932 spot TAG, not the displayed place name. It validates UI thread, definition/context ownership before and after a native location call. It must run in the UI presentation phase with request serial/opening/lifetime guards, not inside the read-only wdu4_pass/dispatcher snapshot capture.
The old pipeline resolves display names separately: dev_lab/src/hakushin_compat/work_selector_spot_names.py parses installed spot declarations and inheritance, then work_selector_presentation.py sends an SPN1 tag/name dictionary; src/work_selector_ingame_preview.h calls work_presentation_spot_name after location_read. That dictionary is not supplied by the new standalone v4 request. Its source explicitly does not override runtime rename rules.
Recommended incremental contract:
1. Add an explicitly typed built-in column `所在地=location`; keep current numeric stat columns unchanged. Extend grid cell storage/comparison/rendering for text, with stable DAT-order ties and missing locations last in both sort directions. Do not encode locations as integer pseudo-stats.
2. Resolve unit ID afresh in the active request context, invoke existing location adapter on the actual UI thread, then copy the resulting tag into request-owned storage. Recheck serial/epoch after each native call. A missing spot is unavailable, not proof that the unit is a roamer. No native pointer persists across requests.
3. For display names, either receive an optional DAT-supplied pair of bounded tag/name lists (suggested names @hk_ui_spot_ids / @hk_ui_spot_names), or reuse an explicitly supplied SPN1 dictionary as an optional adapter. Validate equal lengths, unique tags, encoding and bounded names. Unknown names show a clearly labelled location tag or unknown, not a guessed place name.
4. Prefer DAT-provided labels to reintroducing mandatory Python DAT scanning. A future verified runtime place-name resolver would improve runtime-rename accuracy, but none was established by these reviewed sources. Avoid inferring an offset/function now.
5. Location is presentation metadata, not a new eligibility filter. DAT still owns candidate membership. If location affects caller eligibility, DAT must construct the candidate list accordingly. Unit/context freshness remains mandatory at commit; do not turn failed name lookup into an automatic selection or candidate substitution.
6. Own/free dictionary and UTF-16 row strings with the request/grid. Preserve the source row -> ID mapping. Recompute locations on each new request; do not hold global stale definition/spot pointers.

## B. DAT custom numeric column proposal

Define `heading=@refs` narrowly: @refs is a DAT string list containing NUMERIC VARIABLE NAMES in exactly the original candidate order. It is not an expression, numeric scalar replicated over rows, unit->global mutable dictionary, or a list sorted independently from candidates. Values are signed int32. This directly generalizes the already established v3 numeric-reference contract.
Conceptual DAT example (the new heading token still requires a lexer/real-DAT fixture): set(bonus_0,30); set(bonus_1,-5); setv(@bonus_refs,bonus_0); addv(@bonus_refs,bonus_1); setv(@hk_ui_columns,講師補正=@bonus_refs). Two candidates imply exactly two references. Ordinary `HP=hp` can coexist in the same 8-column request.
Implementation boundaries:
- Extend parser output from stat_of to a column descriptor: STAT(stat-index), CUSTOM_NUMERIC(list-name), later LOCATION. Bound names and reject malformed/ambiguous descriptors. Preserve existing accepted syntax and heading uniqueness. Do not evaluate DAT expressions or create missing variables.
- First capture the fixed input vectors, then collect each referenced list from the same VM string map. Every custom list must have exactly N entries. Each entry names a numeric cell; reject missing, invalid or control/output-reserved names. Require bounded native record/value addresses and reject address aliases with all seven output cells, not just textual name collisions.
- Duplicate references across rows/columns can represent equal values legitimately; deduplicate map requests, retain a per-cell reference index. A repeated reference must never trigger wdu3_map's duplicate-request rejection accidentally. A strict no-duplicate API would also be implementable, but unnecessarily burdens DAT producers.
- Important bound: current wdu3_map permits at most 196+6+49+4 = 255 requested keys. v4 may need 512*8+7 = 4103 distinct numeric keys. Do not simply pass 4096 refs to it or remove the guard. Extract a bounded collector with an explicit request-limit parameter, retain v3's 255 wrapper limit, and give v4 a documented 4103 maximum with checked allocation sizing and existing cycle/map-count validation. Traverse once per map/pass, not once per cell.
- Use heap-owned snapshot storage for the potentially large reference-name/address tables. Capture column kind/name, ordered refs, resolved addresses and values, and compare two captures. At commit repeat the capture and compare to the displayed snapshot under the existing serial/epoch guards. A changed reference to an equal-valued different cell must be detected; copying only values is insufficient.
- Repeated captures remain non-atomic and do not solve ABA; existing UI-thread/lifetime ownership is still necessary. No arbitrary game functions run during this pure capture. No writes to unit stats are needed.
- Feed validated values into the existing grid's numeric row-major storage; sorting and return IDs need no semantic change. A malformed custom column rejects the enhanced request and preserves the native paged fallback. Missing values must not silently become zero.
- Keep @hk_ui_values absent/empty for v4 compatibility: hk_ui_pick_unit currently clears that v3 input. The caller owns the new arbitrary @refs lists and numeric variables; the wrapper must not erase unrelated lists. Before each call the caller rebuilds candidates and refs together. hk_ui_columns/title/sort are already cleared on wrapper return.
- Make unsupported extended syntax fail closed on older plugins and fall back natively; do not silently ignore it. An extension/capability marker can document the new contract without changing Core ABI, but any new wire/API identifier should be agreed before code changes.
- The education adapter must separately change its production of compensation scores. Adding custom columns alone does not eliminate existing temporary magdef/setStatus usage in original education DAT. Copy the already computed score into dedicated variables, pass them, and preserve education decisions/restoration until the adapted DAT is validated. DLL neither recomputes nor predicts educational rules.

## Minimal implementation/test sequence

1. Custom numeric column first: pure parser/reader regression with 2 rows, mixed built-in/custom columns, -5/30; same original IDs after ascending/descending/third-click reset. Real DAT fixture proves token preservation and variable reading. No new function dispatch or anchor model is needed.
2. Boundary tests: N mismatches; unknown numeric/list vars; aliases to every output by name and address; changed reference with equal numeric value; repeated refs; INT32_MIN/MAX; 512x8 and 4103 unique keys; snapshot mutation between passes; map corruption; rejected request leaves outputs untouched.
3. Run existing successor and partial-grid-fill regressions, plus v3 unchanged-contract suites. Test cancel, required re-ask, plugin disabled, and custom validation rejection through native fallback. Extend the two anchor choice fixtures, not the abandoned 49-choice model.
4. Add typed location column and adapter test separately: UI thread mismatch, request replaced during native call, unknown tag/name, duplicate dictionary tags, null location, general units, literal CP932 trail-byte cases, and ascending/descending unknown ordering. Verify no unit selection or education execution during presentation.
5. Game tests on diagnostic copy: lecturer/student/custom score identity and one item selection; then fullscreen/overlap input ownership, focus switch, detail/hover and cancellation. The current side-position workaround must not be accepted as fullscreen proof.

## Documentation correction and remaining scope

DAT_UI_V4_SPEC §6 says disable by changing a '4th 1'. Actual core/hakushin_manifest.c:78-80 reads enabled from fields[2], order from fields[3], API from fields[4]. Correct instruction: change the THIRD pipe-separated field immediately after the DLL filename from 1 to 0; preserve load order/API/hash. No document source was edited during review.
New native location display names, complete DirectInput isolation/fullscreen behavior, hover descriptions, dynamic assets outside a_default, and unchanged outcome under every education update are not established by the reported v4 tests. Basic detail display is distinct from skill/terrain hover explanations.
Conclusion: reuse v4's explicit DAT request, stable row identity, reader/fallback and visuals. Add custom numeric references and typed location as small independent extensions. Do not restore education detection/parsing or unit-stat mutation as a generic data transport. Preserve existing v3 fixes and verify input ownership before calling the UI a complete game-internal replacement.

## 2026-10-29 addendum: StatusWnd detail modes and action suppression (readonly)

Review pre-append SHA-256: 5CDD82FD9FEF2839AA2EA25137117C7D6C9C2F846767DFAD84FB4E780A719026.
Scope: saved source/Ghidra pseudocode, current adapters, queue and FINDINGS §93. No source edits, game operations, new breakpoints, native calls or executable analysis were performed by this reviewer. Human ACTUAL below comes from §93 and parent relay; it is not a subagent live test. Mode contract discussed here assumes 0=off, 1=view-only/default, 2=explicit native actions; wire semantics must be fixed by the implementing owner.

### Evidence inventory and provenance
- src/work_selector_native_detail.h SHA CA2E2C3320BED92DB0814285434D2C11D73654E4667DD720147F923DAE23CE4F.
- src/work_selector_skill_hover.h SHA 46EE9A8B0E0D4D9B6F76FD7F141787EF92B743DFF9CB5D69FAF70F617151BCF8.
- tests/work_hover_coordinates_20261026.json SHA 902B33EECB5A7A431092E1BA270E7059E1C7F6AB838CE922F5C70E1BAD4017A3.
- Saved functions root: rea_lab/headless_analysis/full_pseudoc_20261020/functions/.
- 0055/0055BC60.c SHA CCD03C646F6CE9422B7AF5A311C994E6247EED0B3E38252B1165F464444AF3C4.
- 0056/00560650.c SHA 700488DCF80867EDBF2239C45C513D2BF12D6FFF815003599BEDB3E6C00F90D0.
- 0056/00560CA0.c SHA 47195285DC4A1F56A1B49B0E884597FB28166BFE9339FE14B51A0FEC6D5B0C49.
- 0056/00561120.c SHA DDB3918629ED06D3842227F76AE5ED7DEFBF5A60C2BCD7E57C1186C5B73CF414.
- Further saved evidence: 0055B5B0.c, 0055B320.c, 0055B430.c, 0055BAB0.c; tests/work_detail_abi_existing_20261023.txt, work_detail_hover_canonical_20261026.json, work_skill_hover_host_review_20261026.json.
- REA tool inventory IS exposed in this subagent: tools.mcp__rea__binary_session, tools.mcp__rea__open_binary, tools.mcp__rea__procedure_assembly, tools.mcp__rea__analyze_function. binary_session reported open:false, Ghidra 12.1.4 available at C:/Tools/ghidra_12.1.4_PUBLIC, REA 6.7.0. No binary was opened: saved evidence sufficed for this review. A root inventory mismatch is not proof that REA/Ghidra is unavailable.

### Distinct instances and opening/closing contracts
1. TempStatusWnd instance 0x8BCD48, vtable 0x639CD4, target self+0x1B8=0x8BCF00, visible self+0x84=0x8BCDCC. Existing adapter owns this exact instance/vtable/target/epoch, checks UI thread and reentrancy. Verified opening 0x55BAB0 ABI from saved assembly: EAX=display, ECX=y, EDX=x, stack=definition, RET 4. It calls 0x55BC60 with arg 0 and normal opening performs synchronous rendering; an early hide-only path exists. Hide 0x55B590 uses ECX=self, stack 0, RET 4. Do not transfer these contracts to another function merely because it opens details.
2. Ordinary StatusWnd instance 0x67E978, vtable 0x639C5C, target 0x67EB30. Saved 0x55B5B0 is an ordinary opening route, directly called from saved 0x4CA260 and 0x41A7A0. It closes Temp and several other windows, changes target/location-related state, positions/redraws views and may call 0x418EE0. Ordinary hide 0x55B430 also has map/window side effects. Exact 0x55B5B0 ABI is not established by its decompiler signature (unaff_retaddr and recovered arguments are not trustworthy). It is not a drop-in 0x55BAB0 replacement.
3. Owner chain self+0x98 -> owner+4 -> context is relevant to detail text and hover. The visible definition self+0x1B8 is distinct from context+0x1B8 used by ordinary hover. A target pointer alone does not establish a valid owner/context or input lifecycle.

### Human ACTUAL and interpretation, kept separate
FINDINGS §93 now records image base 0x00A30000 for that run. Thus source VA +0x630000 matches the reported live 0x00B8BC60 and 0x00B8D8F6..0x00B8D9FC. This delta is run-specific and must never become a fixed runtime address.
- Both own/other faction detail assembly calls had [esp+4]=0 at 0x55BC60. This argument is not a button-on/off selector.
- The 0x55D712 group was not taken in these cases. After 0x55D8F6, 0x583CF0 produced non-null values that differed by unit, even within the same faction. A location/affiliation object is inferred; its displayed name was not verified.
- 0x597B00 return was stable per faction; return+0x1D was 1 for player faction, 0 for two other factions and an allied faction. This strongly supports player-faction eligibility in this path. §93 calls it a player-faction flag; this review retains the narrower observed sample and does not claim every semantic use of +0x1D is proven.
- War object 0x8BA538, created at 0x5A4100, has visible +0x84 (0x8BA5BC) and state +0xA4 (0x8BA5DC). State 0x80000008 was also present normally; visible became 1 during deployment-unit selection. Player detail then had no action buttons. The combined gate occurs in about 30 sites. Neither byte[0x8BA5BC] nor faction+0x1D may be repurposed for selector suppression.
- Player detail followed 0x55D93A (employment flag +0x1C4), 0x55D99C (dismissal +0x1C6), 0x55D9BB, then 0x55D9FC. 0x55D9DD item construction was not taken. Rebuild entry 0x55D8F6 occurred roughly 10 times per opening: one-shot post-open clearing will not remain effective.
- §93 also attributes to the user that event-time detail/skill explanation is a NEW feature, not established original behavior. A solution must preserve the DAT continuation rather than treating original event-time hover as a baseline.

### Flags are draw outputs and input gates, not standalone safe hiding API
Saved 0x55BC60 line 99 clears the DWORD at self+0x1C4, then final button paths draw via 0x455520 and set individual bytes. The four flags are +0x1C4 employment, +0x1C5 extract-vassal, +0x1C6 dismissal, +0x1C7 item. Temp identity, context+0x208/+0x20C, context flag +0x1EF4BE, location/faction/war gates and DAT noemploy_unit/noremove_unit/noitem_unit all contribute. Existing native restrictions must remain authoritative in mode 2.

Cross-reference matrix from saved pseudocode:
- 0x55BC60 lines 879..1015: draws and sets flags. Suppressing flags AFTER drawing does not erase already painted buttons; suppressing drawing only leaves possible active inputs.
- 0x560650 lines 44..89: mouse-down guard requires self+0x1BC == 0x80000008 and war gate; reads all four flags; index 0 accepts 1C4 OR 1C5, index 1 requires 1C6, index 2 requires 1C7. It stores pressed index into self+0x1BC and draws pressed edge.
- 0x560650 lines 89 onward: with 1C7 enabled, clicking skill rectangles can enter a mutation path and remove stored skill/item entries from definition vectors. Mode 2 is not restricted to the three bottom buttons.
- 0x560CA0 lines 43..125: mouse-up consumes previously stored self+0x1BC and resets it. It tests the war gate, but index 1 DOES NOT recheck 1C6 before dismissal logic. Index 0 checks 1C4; when false, it proceeds toward extract_vassal without rechecking 1C5. Index 2 does recheck 1C7.
- 0x561120 lines 116..138: button hover explanations check 1C4/1C5, 1C6, 1C7 respectively, using hover index self+0x1C0. Seven non-skill regions plus skill rectangles share this routine. Other regions may need valid owner context independent of button flags.

Consequence: clearing 1C4..1C7 alone while a press is pending can still allow an action on mouse-up, or redirect an index-0 press from employment into extract_vassal. Clearing only flags after each render is not a safe complete patch. This is a static control-flow finding, not a reproduced destructive action.

### Required design gates before implementation
- Suppress only when the exact detail instance/definition/context belongs to the live selector request and mode is view-only; serial/epoch + UI thread + no foreign takeover must agree. Outside that ownership, original drawing/input must remain untouched.
- At each rebuild, prevent action rendering and matching hit-tests together, before input can be delivered. Do not paint over a live button or assume a disabled owner HWND blocks DirectInput.
- Pending press self+0x1BC and hover self+0x1C0 require an explicit lifecycle: entering view-only must not inherit a native press, and its later mouse-up must be consumed/denied without executing native action. Transitioning/releasing ownership must not replay an old press. Exact hook/cleanup instruction boundaries remain unverified and are not proposed as implemented.
- A native shared predicate or a narrow instance-aware branch gate could reduce duplicated policy, but the existing war predicate cannot be forced globally. Confirm the branch, calling convention, preserved registers/flags, redraw cleanup and mouse-down/up ownership with instruction evidence before modifying it.
- Existing skill-only hover adapter is useful but is not full ordinary StatusWnd behavior. It rejects seven generic rectangles, validates ownership, converts coordinates, calls hover 0x561120 and clears 0x562140 only while owned. Blindly enabling Temp vtable dispatch +0x1C/+0x50 would expose mutation handlers. Full owner lifetime remains necessary for face/movement/non-skill descriptions.
- Coordinates evidence establishes ScreenToClient on the same DPI context with matching positive client/render dimensions. Fullscreen or DPI mismatch has not been proven; reject unsupported geometry rather than forward guessed coordinates.

### Mode 2 consequences
An explicit DAT mode can request native action controls, but it must not bypass native faction, war or DAT restrictions. Employment, dismissal, extract-vassal and item/skill changes can invalidate the candidate list, definition lifetime, score vectors and current event assumptions. After such an action the old snapshot cannot simply be confirmed. A conservative first implementation would reject/close the pending request and return an explicit rebuild/retry outcome; DAT reconstructs eligibility, values and candidates before reissuing. Re-resolving an ID alone is insufficient to prove it remains eligible. This contract must be agreed before mode 2 is released.

### Minimal next observation, no new breakpoint request
At already established stops, record EIP and run-specific module base; at 0x55BC60 entry record ECX=self, [esp+4], [self+0x1B8] and owned/non-owned context. At the human-confirmed button path EDI=self, record [EDI+0x1B8], bytes +0x1C4..1C7, DWORD +0x1BC/+0x1C0 before/after reconstruction. For helper returns, EAX and bounded return+0x1D suffice; do not mutate faction/war flags. Mid-function register assignments beyond ACTUAL EDI are not inferred from pseudocode. No game or debugger manipulation was done for this addendum.

## Focused instruction-boundary addendum (2026-10-29; STATIC only)

Review pre-append SHA256: 09477C1B1D43CA1397EDC9335362FC36CF55E30AE285C08879B0D7A17AE74E85.
Scope: no production source, DLL, manifest, original DAT/EXE/save, game, debugger or registry changes. No ACTUAL success claim. Parent reports debugger/game closed; historical observed instances are not substituted for a current observation.

### Evidence acquisition and provenance
REA tools available in this agent were mcp__rea__binary_session, open_binary, procedure_assembly and analyze_function. Opening the existing Ghidra .gpr with REA open_binary returned target_unavailable/unsupported_target/file_format_rejected (unsupported binary header): this is a project-format limitation, not evidence that REA is absent and not a permission refusal. No REA binary target was opened.

To reuse analysis without a new binary import, two scripts read the existing Hakushin067_AtexitTailRepair_20261023 project with Ghidra 12.1.4 analyzeHeadless -process hakushin067_Vahren.exe -noanalysis -readOnly. Both completed exit 0. Scripts checked program SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 and wrote new bounded instruction/reference evidence. They did not save project edits.

Evidence in this same v4 directory:
- WorkStatusBoundaryExtract.java: 0D7DFDA2F23CEBB3D7E7C9FC348F67D04BA695224AC49335C3A879B6CF5FCA2C
- work_status_boundary_existing_20261029.txt: 52011CD25F7F1B2146A2E01DF9CD14AA57EBF7D5252FD494D38C49E73FE51DD9
- work_status_boundary_existing_20261029_console.txt: DFAA2C824D6497CE91EA47F22C8A5F49711B03348EA48ED4171A4B8B78B0A631
- WorkStatusBoundaryTailExtract.java: B6B37B00679F644DDEC2C9165EE2F0CA4E79B49D049C209BD3775F48AC4690B0
- work_status_boundary_tail_existing_20261029.txt: 8BD1041A515A919112BFA0ABEB4143FF85D0B0EA717E4F78623C7FB1D49F6D4D
- work_status_boundary_tail_existing_20261029_console.txt: E6A9A78E77FDFA8262BD7B7AFA4CBB28EB185F958EC93E93AEB15C521B8381DE

### Exact callable boundaries and limitation of ordinary managed CALL
Normal open 0x55B5B0 consumes one stack definition argument and returns RET 4 at 0x55BAA7 (entry stack argument read is original [ESP+4], after local allocation/pushes [ESP+6C]). References are direct CALLs at 0x41AFCB and 0x4CA708. This resolves the earlier stack ABI uncertainty; it does NOT establish that its map/window-changing side effects are safe inside a suspended DAT event.

Render/rebuild 0x55BC60 receives ECX=self plus one stack argument, returns RET 4 at 0x55DA4C. Direct incoming CALL sites found: 0x4A5B78, 0x414D30, 0x55B8EA, 0x55BB24, 0x4D87A1, 0x412199, 0x56294D, 0x562A06, 0x560C64. Patching only the normal-open caller misses independent rebuilds.

0x560650 down and 0x560CA0 up have references in normal/Temp vtable data at 0x639C98/0x639D10 and 0x639C9C/0x639D14. Hover 0x561120 has vtable data reference 0x639CA0; clear 0x562140 has 0x639CA4/0x639D1C. Existing dispatch includes indirect virtual calls; these are not direct E8 CALL sites. Core hakushin_call_patch.c accepts 5-byte E8 CALLs only. Replacing a normal render call with an ordinary wrapper alone cannot guarantee suppression of queued input actions.

### One narrower candidate if ordinary StatusWnd is required
Instruction evidence gives a common point inside every 0x55BC60 rebuild:
- 0x55BCCA clears DWORD [self+0x1C4], before the later action branches.
- 0x55D54F loads EDI=self; 0x55D553 moves ECX=EDI.
- 0x55D555 E8 16 05 00 00 calls 0x55DA70 (ECX=self, no stack arguments, RET at 0x560640).
- 0x55D55A compares EDI with Temp singleton 0x8BCD48; equal jumps at 0x55D560 to 0x55DA0C, bypassing the button body.
- 0x55DA0C is the existing no-button continuation. It tests the original argument, optionally calls 0x453C20 with the correct self, and reaches normal SEH/stack cleanup and RET 4.

An exact-owned, mode-1-only specialized thunk at managed CALL 0x55D555 could call original 0x55DA70 and then continue at 0x55DA0C instead of normal return 0x55D55A. This would skip both action painting and the writes that enable action hit tests, on every rebuild, without altering the vtable, player/war flags or unrelated instances.

This is a CANDIDATE, NOT a ready patch: redirecting the call continuation requires a specialized assembly thunk, ABI/register/stack/SEH proof and lifecycle tests beyond ordinary Core CALL management. Do not fake EDI=Temp: later cleanup uses that pointer. Preserve original 0x55DA70 output/register state and exact unowned/mode-2 continuation. Revalidate ownership after the original callee in case of reentrancy. Expected bytes and both continuation boundaries must be host-version checked.

Before mode 1 can acquire an ordinary detail instance, self+0x1BC must be the no-press sentinel 0x80000008; reject BUSY rather than clear a foreign/pending press. Under continuous owned button suppression, native down cannot arm its three action indices and item/skill mutation is disabled by 1C7=0. However, the earlier mouse-up non-recheck finding remains: entry/exit ownership, all writes to the press field and any queued down/up must be demonstrated. Thus this candidate is not yet a complete input-safety proof. No production implementation was performed.

### Prefer the smaller pinned-preview investigation first
Current core/dat_ui_v4_visuals.h and work_selector_native_detail.h still open 0x55BAB0/Temp, using EAX display value 0x80000008, ECX y, EDX x, stack definition. Their tick checks epoch/target/lifetime and does not close merely on mouse leaving a row. The native Temp branch already avoids the action body. This is a viable alternative only if the actual interaction is pinned on row click and remains visible while the cursor moves into it. The display sentinel is not proven to mean infinite persistence: 0x55BAB0 substitutes a default from self+0xE4 and stores +0xE0. Do not claim pinning solely from this constant.

Historical human observations in FINDINGS §93 include visible buttons. Without that run's DLL identity and actual self, they cannot prove that current source uses ordinary StatusWnd. Keep this provenance discrepancy open; do not silently replace Temp with normal open based on a displayed caption.

Existing explicit hover adapter can potentially be extended without enabling Temp's native down/up dispatch:
- 0x561120 receives ECX=self and two coordinate stack arguments, RET 8; 0x562140 receives ECX=self, RET.
- 0x56117A reads owner=[self+0x98], context=[owner+4], and stores ADDRESS context+0x1B8 as a text-expansion context. This is distinct from the unit definition at self+0x1B8.
- Generic indices 0..2 are action tooltip regions and must remain excluded in buttonless mode. Indices 3..6 and skills provide further descriptions, but require their own rectangle, unit-string/container and owner-context validation.
- Current work_selector_skill_hover.h rejects all seven generic regions. Its context+0x1B8 read only proves bounded readability, not equality with the active request VM or complete validity of all text structures used by generic hover.
- Hover/clear mutate shared tooltip windows and owner lists. Clear while still exclusively owned BEFORE row switch/close; after foreign takeover, do not clear someone else's tooltip.
- Do not turn on Temp virtual hit-test gates +0x1C/+0x50, since that would expose action paths. Forward only validated hover/clear on the UI thread.

Recommendation: first establish pinned Temp lifetime and add safe explicit non-action hover if feasible. It reuses existing native rendering and avoids normal-open side effects and a continuation thunk. If Temp cannot remain pinned using a verified narrow mechanism, choose the ordinary StatusWnd candidate only after the listed input/lifecycle proof. Both routes must satisfy the same visible behavior; merely showing a transient tooltip is not acceptable.

### Mode contract and smallest future ACTUAL checks
Mode 0: no detail. Mode 1 (default): row-click pinned detail, no mutation controls, native explanation hover reachable by moving inside. Mode 2: explicit DAT request for native controls, still subject to original restrictions; mutations invalidate eligibility and the request snapshot and require an agreed rebuild/retry contract before selection can commit.

No immediate restart is requested. When normal testing next reaches a detail:
1. Record deployed DLL SHA, request epoch/tag, detail self, definition, owner/context, visible state and +0x1BC/+0x1C0; distinguish Temp versus ordinary singleton. Use relocation from that run only.
2. Click a row, move directly into its skill/face/movement regions and wait; verify pinned identity, explanations and that moving out of the row alone does not hide it.
3. On row switch/cancel, verify old explanations clear once, old definition is not reused and original event resumes once.
4. For a later ordinary-mode-1 prototype, prove flags 1C4..1C7 remain zero through repeated rebuilds, no pending press is inherited, and unowned native details are unchanged. Do not test destructive controls merely to prove absence.
5. Mode 2 requires separate explicit action tests with a disposable save/copy and fresh-candidate validation; a successful hover test is not sufficient.

All addresses above are original static VAs, not current live addresses. Current source, static evidence and prior human ACTUAL observations remain separately labelled.

## Location presentation adapter implemented (2026-10-29; synthetic validation only)

Owned production file: core/dat_ui_v4_visuals.h only. No grid/runtime/v4 schema changes, no original files/game/deployment changes. Existing src/work_selector_location.h reused without edits (SHA256 3CBF0CF0061C67FE2391B9941503435C1092D0F5440F2E6559B4EC8F6671C5B1). Root confirmed ownership; generic_wrapper_review notified when frozen.

Pre: visuals SHA256 126E004A2E00E4BC53466186F10837DB9BAFE349EFE95B45319F2760EB2DE6A6, length 10053, mtime UTC 2026-10-28T14:24:22.4040000Z. Backup: this directory/dat_ui_v4_visuals.h.pre_work_location_20261029.
Post: visuals SHA256 11989EA4C50923CFAF7DB56295873BADDAF3F06EA71E962A1F17F1B87B702147, length 13122, mtime UTC 2026-10-28T22:35:20.3927306Z. Source frozen after final dedicated tests.

API for root integration:
- V4LocationCell { int kind; char tag[256]; wchar_t text[272]; }
- v4_location_for_unit(uint32_t vm,uint32_t def,V4LocationCell *out)
- return WORK_LOCATION_OK=1: kind V4_LOCATION_TAG_ONLY=1, text is UTF-16 "ID: <native CP932 tag>".
- return WORK_LOCATION_UNAVAILABLE=0: kind 0, empty tag, text "未取得". This does not infer roaming or a special location.
- return WORK_LOCATION_ERROR=-1: output unchanged. Root must initialize error display, never use a previous row's cell.
- v4_location_cell_read provides injectable adapter/formatting tests; WORK_V4_LOCATION_ONLY isolates this block for tests and is not used by the live runtime.

The live wrapper checks UI thread, bounded VM/base, manager, a nonreentry flag and exact 16-byte original 0x583CF0 prologue. Pure adapter additionally verifies def+1A4 == vm+1B8 before/after native query, reuses all native location helper context/spot/thread validation, and strictly decodes CP932. A legal CP932 trailing 0x5C is treated as character data. No display-name resolver or runtime-rename rule is invented.

ABI evidence: WorkLocationABIExtract.java read only original-hash-matched saved Ghidra project with -noanalysis -readOnly, exit 0; output work_location_abi_existing_20261029.txt SHA256 2B6BC41397058CE97564F33F0B386DF7F82C14A3AB6274E506F0C7C4C91029BD. Entry 0x583CF7 MOV EDI,EAX confirms definition input; return paths 0x583D3E/0x583DAE/0x583DB8 are RET with result EAX. First 16 bytes: 83 EC 08 53 55 56 57 8B F8 83 BF 94 00 00 00 00. Existing wrapper preserves integer registers/flags except EAX. New inspection only reused this one 201-byte saved function.

Actual test evidence:
- Baseline shim from existing raw-tag adapter: RED O0/O2 18 PASS, 7 FAIL, exit 1. Missing features were explicit tag labeling, exact active VM validation, unavailable presentation and strict CP932 rejection.
- New cell helper: GREEN O0/O2 23 PASS, 0 FAIL, exit 0. Cases include unknown location, invalid CP932, valid multibyte trail 0x5C, 255-byte tag, manager/context/thread mismatch, mutation during native call, reentry and bounded VM.
- Full visuals include + live wrapper rejection tests: O0/O2 exit 0 (invalid prologue, wrong UI thread, overflow VM, reentry). No real native function was executed in these tests.
- Existing test_work_selector_location.c with -UNDEBUG: O0/O2 exit 0, including its existing x86 ABI loop.
- Reproducible dedicated build: build_work_v4_location_cell_test.ps1 SHA256 4B5E270D97A0E8FC859AC3AD996FA7B0D260D1A8DB243388EFBA4E04FCF0E867.
- test_work_v4_location_cell.c SHA256 22CA66F91338AD2017DD717F48972E2B3720087270EECDD7A732EE91D35B48C8.
- test_work_v4_location_live_guards.c SHA256 E7234D45366EF4E29D8669C718CFFC996CD4571B32D7A1E6A29104F322A9EF70.
- An initial test link attempt omitted hire_ui_native_readonly.c and failed undefined HkReadNativeTag; fixed build input before baseline RED. It is not a product regression.

Runtime/grid integration still belongs to root: add a text column explicitly labelled "所在地ID（表示名未確認）"; call the adapter during UI presentation only, not DAT snapshot capture; validate request serial/definition lifetime before/after native query and discard rows from a superseded request. Copy cell strings into owned presentation memory. Sorting must preserve unit-row identity and distinguish unavailable/error. The adapter neither changes candidate eligibility nor proves current eligibility at commit. Native location queries may allocate temporarily. Whole-plugin compilation and real game location display remain root integration tests, not completed by these synthetic cases.

## Core ABI integration correction (2026-10-29)

The first location adapter's isolated full-visuals fixture did not include Core ABI. Actual production compilation found HK_OK redeclared by hire_ui_extension.h and core/hakushin_abi.h. This was a missed integration dependency, not an unused-function-only problem. Root authorized a narrow dependency split. No enumerator undef/renaming macro or fake include guard was used.

Changes:
- New src/work_native_tag_reader.h: internal WntReadNativeMemory callback and header-only wnt_read_native_tag, unique WNT_READ_OK=0 / WNT_READ_INVALID=1. Bounded string logic extracted unchanged from HkReadNativeTag.
- src/work_selector_location.h now depends only on this internal reader, not the entire old hire public API. Its callback signature and WorkLocationOps layout remain equivalent.
- src/hire_ui_native_readonly.c retains external HkReadNativeTag(HkReadNativeMemory,void*,uintptr_t,char[256],uint32_t*) and return values; implementation delegates to the extracted inline. Other native-readonly functions unchanged.
- core/dat_ui_v4_visuals.h marks v4_location_for_unit static inline, suitable for its optional header-only API. No runtime integration added here.
- Protected bridge/Python files were not edited. No original/game/deployment changes.

Evidence:
- Actual core/dat_ui_selector_plugin.c with -O2 -std=c11 -Wall -Wextra -Werror -target x86-windows-gnu: RED exit1, HK_OK redefinition in location_core_abi_red.stderr.txt.
- After dependency split, compile exposed unused v4_location_for_unit under strict warning policy (preserved location_core_abi_unused_red.stderr.txt). Corrected with static inline, not warning suppression in the production build.
- Actual production TU GREEN compile exit0: location_core_abi_green.stdout.txt/.stderr.txt; stderr empty.
- Formal core/build_dat_ui_selector.ps1 -OutputDirectory <this-dir>/location_core_link_green: DLL link exit0; location_core_link_green.stderr.txt empty. This is an undistributed artifact, not installed.
- Dedicated v4 location cells O0/O2 each23 PASS/0 FAIL; full visuals live-entry guard tests O0/O2 PASS.
- Existing test_work_selector_runtime_metadata.c, test_work_selector_stats.c and test_work_selector_location.c with -UNDEBUG O0/O2 all exit0. These exercise external native-readonly users, failure-preserving strings, signed values, mutation/cycles and original location ABI. Logs named *_abi_split_O0/O2.txt.
- generic_wrapper_review notified source freeze before its default/AUTO full-suite rerun; its broader suite results belong to that agent.

Final source identities:
- visuals: 11989EA4C50923CFAF7DB56295873BADDAF3F06EA71E962A1F17F1B87B702147 -> 160121E650CA662FE0EAE37EB9120AF1832FEE77BD1B35398FEF536E535AA722; UTC 2026-10-29T00:13:37.5125669Z.
- location: 3CBF0CF0061C67FE2391B9941503435C1092D0F5440F2E6559B4EC8F6671C5B1 -> B64E1E32047E4695F6C6217DFFADF17C6B22EBB7CFC0B9C9EDD0950A6F1CD6DD; UTC 2026-10-29T00:05:53.4622508Z.
- native_readonly: AAB8F5D410F25FC35CF4BA24F1C75A35E1172828B27C32999663E577AF29478A -> 17F77D386FA59570277C70D126C0B8185CB2718E86BAC76627E2BF5E3DCE8A42; UTC 2026-10-29T00:05:53.4748442Z.
- new tag reader: 20872BF2F2C51FBA35F03AFD2B7BF07A7516950FC10266FE5BB3A2D81CFADF0E; UTC 2026-10-29T00:05:52.6125647Z.
Pre-split existing-source copies are work_selector_location.h.pre_core_abi_split and hire_ui_native_readonly.c.pre_core_abi_split in this directory. Previously stated TAG_ONLY/unknown semantics remain unchanged.


## Owned ordinary StatusWnd: complete buttonless boundary review (2026-10-29, readonly)

Pre-append review SHA256: 03668208835FE497A060A55674727E293E96D77B742F9D0A2833C36EA168A3BC.
This review reuses saved original-hash E8DAC301050C8E630D7E0CE93AEefd95E641207D9C0576017F62BA46A8767187 pseudocode and work_status_boundary_existing_20261029.txt (52011CD25F7F1B2146A2E01DF9CD14AA57EBF7D5252FD494D38C49E73FE51DD9) / work_status_boundary_tail_existing_20261029.txt (8BD1041A515A919112BFA0ABEB4143FF85D0B0EA717E4F78623C7FB1D49F6D4D). No new binary analysis, game operation or source change. Static VAs require per-run relocation. Human observations from previous deployed versions remain separate.

Verified ABI/boundaries:
- 55B5B0 ordinary open: stack definition argument, RET4. Pseudocode prototype alone is unreliable. It sets singleton 67E978 target at +1B8, calls 55BC60, positions/shows/refreshes. It also changes map/other windows and shared tooltip state; it is not an isolated presentation operation.
- 55BC60 construction: ECX=self, one argument, RET4; clears DWORD flags self+1C4 at entry. At 55D54F EDI=self; 55D553 ECX=EDI; 55D555 E8 16 05 00 00 calls 55DA70. The latter takes ECX=self and RET0.
- Immediately following, 55D55A compares EDI to Temp singleton 8BCD48, and 55D560 branches to 55DA0C, bypassing action construction. 55DA0C retains original redraw-argument/SEH/stack-cookie cleanup and 55DA4C RET4. This is a concrete existing buttonless continuation, not a reason to falsify EDI or a global identity.
- 560650 down uses ECX=self and RET0xC (button and two coordinates). 560CA0 up uses ECX=self and RET8; 561120 hover similarly RET8; 562140 clear takes ECX=self and RET0. Input functions are referenced by vtable data, not E8 calls at those references.
- 521560 normal input routing calls virtual +28 down, +2C up, +30 hover, +34 clear, +38 wheel. Up is issued to player+428 capture before that pointer is cleared; hover ownership is player+42C. Saved assembly confirms 521614 FF D2 up and 52169F FF D0 wheel. Core managed CALL cannot directly substitute these two-byte indirect calls.

Why flags-only suppression is insufficient:
- Down can mutate item/skill lists when +1C7 is true, in addition to the three bottom buttons.
- Up loads +1BC prior press index, resets it, redraws and hit-tests indexed button rectangle. Index1 reaches dismissal without rereading +1C6; index0 without +1C4 takes the other extraction action. Thus clearing 1C4..1C7 after construction does not retire a prior captured press.
- Acquire only with no native capture/pending press and no foreign tooltip owner. Do not inherit a down event, restore old pressed state, or enable native down/up while mode1 owns the detail.

Minimal complete candidate (design, NOT validated implementation):
1. One Core-owned construction CALL at RVA15D555. After calling original 55DA70, only a still-owned normal singleton, exact request generation/definition/owner/UI thread and mode1 may use the existing 55DA0C continuation. All other instances/modes return normally to 55D55A. This needs a dedicated assembly continuation adapter preserving original callee register/flags/stack effects and testing SEH/stack-cookie paths; ordinary C return-site guessing is unacceptable. Reentrant ownership loss during original drawing must not suppress unrelated rendering.
2. One Core-owned frame CALL at RVA121AF0 (original RVA121560, expected E8 6B FA FF FF), reusing the proven integer/flags/FX-preserving frame thunk. While the selector exclusively owns input, consume that frame and explicitly forward validated hover/clear only to the pinned detail. Never send down/up/wheel to ordinary native dispatch in mode1. Outside ownership tail-call original. This is a scoped modal broker, not mutation of global war/faction flags or vtables. Confirm this frame covers all native input entry paths before claiming complete suppression.
3. A tooltip cleanup lease independent of cursor/focus visibility, with clear-before-switch/hide/commit/cancel/shutdown. Shared tooltips mean repeated null/foreign guards are not sufficient to justify destructive cleanup. Handle lost ownership as recorded debt/quarantine, never clear a foreign target.
4. Ordinary open side effects must be explicitly bounded: prefer proving a narrow safe show/setup path, or accept/validate 55B5B0 only in an isolated UI-owned session with known prior state. No safe snapshot-and-restore of all its side effects has been proven. Close/hide must preserve original event wait and retire all owned explanation windows.

Remaining implementation blockers:
- No live evidence that ordinary open is compatible with the active DAT choice VM and existing request owner; no proof that full generic hover contexts are valid for every selected candidate.
- No verified cross-handler/other-thread path audit proving the frame broker sees every action input. The vtable-only refs and common dispatcher are promising, not exhaustive proof.
- No production continuation thunk yet; the construction skip preserves existing exit path but must be tested against exact binary bytes and all construction callers, repeated rebuilds, nested calls and owner loss.
- Existing Temp helper remains a partial alternative only if pinned lifetime plus full non-action hover are proven. Skill-only Temp does not meet the user's full description requirement. Mode2 stays disabled until action-induced candidate changes and commit revalidation are designed/tested.

Smallest future verification sequence: synthetic frame ownership/preserved-register/continuation tests first; then disposable diagnostic copy with no action input forwarded, record DLL/hash/request/self/owner/definition/+1BC/+1C0/capture on acquisition; verify repeated rebuilds never draw controls, row click remains pinned, skills/class/movement/face/ability descriptions work, and clear-on-focus-out/switch/cancel works. Unowned ordinary details must retain their controls. Do not modify faction +1D, war visibility/state, native vtables, or simulate destructive actions simply to prove absence.
