# Pinned Temp non-action hover: isolated helper handoff
2026-10-29. Not deployed, not connected to runtime. No native input actions, original memory writes, game operation or new original analysis.

## Owned files
- New src/work_selector_detail_hover.h SHA256 599507294119C4B15823991B42B25252E163572205309C178406ED813D866F85
- This directory/test_work_selector_detail_hover.c SHA256 8294C8B91B53E2B8428ED3D301749EFF87A4A4370BB0BA2B14904F02AA257247
- This directory/build_work_selector_detail_hover_test.ps1 SHA256 7959DE48949C9FA8AC25430216A18BAD90922D81D67EF6955E9BB15D28549886

Unchanged reused headers:
work_selector_skill_hover.h 46EE9A8B0E0D4D9B6F76FD7F141787EF92B743DFF9CB5D69FAF70F617151BCF8
work_selector_native_detail.h CA2E2C3320BED92DB0814285434D2C11D73654E4667DD720147F923DAE23CE4F

## Why the old helper was skill-only
The native handler is not a pure tooltip renderer. Generic paths use [self+98]->+4 context and context+1B8 text expansion state as well as unit definition members, while clear/hover update shared native tooltip windows. Merely removing the seven-region rejection would let unvalidated paths execute. It also creates false confidence about native down/up safety. The new helper therefore exposes only hover/clear and requires a mandatory host guard.

## Actual synthetic evidence
- Initial baseline shim reused unchanged work_skill_hover_move/cancel and compiled successfully. RED O0/O2: 41 PASS, 17 FAIL, exit 1 each (test_full_detail_hover_red-O*.txt). Failures included four non-action regions being rejected, context mismatch and missing host guard.
- Initial new helper GREEN: 175 PASS, 0 FAIL, O0/O2 exit 0.
- Added guard-epoch transition regression: RED O0 197 PASS, 1 FAIL exit 1, preserved as test_full_detail_hover_epoch_red-O0.txt. It detected coordinate conversion after guard changed request epoch. Added immediate epoch recheck.
- Final helper GREEN O0/O2: 196 PASS, 0 FAIL, exit 0 each. Check count includes callback invariants and is not a feature completion percentage.
- Existing skill hover regression, including existing x86 ABI fake callees: O0/O2 with -UNDEBUG, both exit 0. Initial O2 strict compilation without -UNDEBUG failed unused-parameter warnings because Zig disables assert there; assertions explicitly enabled for the actual passing rerun. No legacy test source edited.
- Earlier fake memory fixture pointer arithmetic was corrected before collecting baseline RED; that fixture panic is not product RED evidence.
- Actual native fixed lifetime, explanations, coordinate/DPI validity, pointer lifetime and original tooltip exclusivity are NOT proven by synthetic tests.

## Helper contract
Initialize WorkFullDetailHover with the owned WorkNativeDetail, existing WorkSkillHoverOps, exact expected VM and owner pointers, and a mandatory WorkFullDetailGuard.
guard(ctx,vm,target,epoch,region):
- region -1 checks exclusive ownership/lifetime/UI/geometry lease.
- region 0..2 never reaches the guard/native hover; action regions are always UNSUPPORTED.
- region 3..6 is an individually approved generic region.
- region 7..106 denotes a skill rectangle (index+7).
- 1 means safe now; 0 means not supported; negative means transient/error.
The callback must not mutate game state or pump messages. It executes with reentry locks. Post-callback identity and request epoch are rechecked. No permissive default guard exists.

The helper verifies exact owner/context pointers in addition to the existing Temp vtable/target/visibility/UI-thread checks. Different owner/context is sticky LOST; it must not clear foreign shared tooltip state. A failed clear retains cleanup debt. An outside point clears only tooltip, never closes the detail. Rectangles use native first-hit ordering; action/generic overlap cannot fall through into a skill underneath. Invalid rectangles/counts reject. Same-pointer foreign reuse cannot be detected by pointer checks: host exclusivity remains mandatory.

## Proposed root integration delta (not applied)
1. core/dat_ui_v4_visuals.h: include new helper and hold one WorkFullDetailHover plus initialization/owner/VM/request lease state.
2. Reuse existing skill ABI callbacks for convert, hover, clear; do not create new naked assembly or vtable dispatch. Bind the existing STA-safe host call guards, not naked callbacks without host exclusion.
3. After successful detail open and verified expected native owner/context, initialize the helper. The definition ownership check def+1A4==vm+1B8 is separate; do not confuse that container with [self+98].
4. In existing UI-thread tick, when the detail is pinned and currently owned, acquire game-client coordinates using GetCursorPos/ScreenToClient under the SAME DPI context. Verify positive client dimensions equal original render dimensions; do not invent scaling. Call move only with matched geometry. Losing focus, unsupported geometry, or leaving the detail should cancel the tooltip while preserving the pinned detail.
5. Row-click selects the pinned detail. Mouse moving away from the row must not trigger detail_close. Confirm event routing uses actual selection changes, not hover selection or transient leave handlers.
6. At the top of v4_detail_close, BEFORE native close/hide, call full_detail_hover_cancel. ERROR means retain detail/cleanup obligation and do not free or confirm. LOST means do not clear foreign tooltips; follow existing root lost-ownership policy. Commit, cancel, row switch and shutdown all pass this same ordering.
7. On epoch transition, clear before v4_detail_tick can hide the old native preview. Do not allow the native-detail tick to close first and then call hover clear.
8. Never silently reset/reinitialize an active or LOST hover helper to erase debt. Deinit only after successful cleanup or documented foreign-takeover reconciliation.
9. Native mode 2 remains disabled and requires its separate StatusWnd/action/mutation contract.

## Host work still required before live hookup
- Pin/exclude original tooltip writers for the lifetime of the borrowed native handler. Prove no message pumping and no original down/up/action routing is enabled.
- Verify [self+98] owner and [owner+4] VM are the request's actual live objects. Readability alone is insufficient.
- Per-region guard must validate its actual definition strings/containers and request lifetime; returning true for all 3..6 is not justified by this helper.
- Use saved native rectangles as capability boundaries. There is no arbitrary ability/stat tooltip synthesis here: requested ability explanations outside known native regions remain UNSUPPORTED.
- Generic region labels (movement/class/face/etc) must be tied to static switch/actual geometry evidence before presenting them as enabled features.
- Exact fixed visible lifetime of Temp remains unproven: EAX=80000008 substitutes a native default, not proven infinite pinning.
- Report unsupported areas explicitly rather than dispatching guessed hover coordinates.

This is a narrow integration proposal, not an applied runtime diff: root owns runtime/visuals and must supply the actual lease/region preflights before compiling a live variant.

## Independent integration review — 2026-10-29 (auto_arm_integration)

Verdict: the isolated helper is a useful policy-enforcing primitive, but the current v4 runtime is not yet a safe host for it. Do not connect a timer with a guard that returns true for every non-action region. This review read saved source/analysis only; no game, debugger, executable analysis, deployment, or test execution. The earlier synthetic results above remain synthetic, not native verification.

### Existing evidence that can be reused
- `src/work_selector_skill_hover.h` and `tests/hover_abi_20261026.json`: verified x86 convert/hover/clear conventions, first-hit ordering, 100 skill slots, transport success distinct from clear's normal EAX=0. Keep those wrappers; do not invent a new native-call ABI.
- `src/work_selector_hover_context.h`: Player anchor is Temp+0x9C; Player+4 is the owning VM and Player+0x194 is VM+0x504. Temp+0x98 is a different owner chain. The new exact owner/VM checks are useful, but cannot replace request/lifetime generation checks.
- `src/work_selector_hover_integration.h` and its host receipt: a previous **skill-only** implementation uses the Core-owned CALL at RVA0x121AF0, validates return RVA0x121AF5 and calls original RVA0x121560 on fallback. It preserves ABI/FX state and confines handling to mode1. Its host-window, occlusion, UI-thread and geometry checks are reusable design material, not a drop-in v4 lease.
- `tests/work_hover_ownership_20261026.json`, final synchronous-boundary and thread reviews: ordinary Player dispatch runs on the game HWND creator thread. Synchronous handling after completed upstream work is reasonable; prior scale/scroll updates do not by themselves make that boundary unsafe. Bypass paths, prior hover ownership, reentrancy and later writers still need lifecycle handling. EnableWindow(FALSE) alone does not stop DirectInput/native task dispatch.
- `tests/work_hover_coordinates_20261026.json`: GetCursorPos/ScreenToClient and matching game/client dimensions are supported. Identity mapping remains bounded evidence, not arbitrary DPI/fullscreen scaling permission. Detail-open return alone does not prove visible/draw-ready rectangles.

### Integration blockers in current runtime (not changes made by this review)
1. **Cleanup outcome must govern teardown.** `v3_surface_close` calls `v4_detail_close` but ignores its result and proceeds to re-enable the game and destroy the surface. `selector_v3_supersede` likewise does not stop on close failure. Adding retained hover debt requires a close/retire state: clear owned tooltip, close owned detail, then release input/window ownership. An ERROR must not silently disappear; LOST must not clear a foreign tooltip. The current calls are acceptable only under their existing narrower contract, not evidence for the new contract.
2. **Epoch/owner teardown ordering.** `v4_detail_tick` may close on an epoch mismatch, while `WM_NCDESTROY` invokes unconditional `v4_detail_abandon`. New hover debt must be reconciled before native hide and before ordinary modal teardown. On actual owner destruction, do not call native memory through an invalid owner; record explicit foreign/teardown loss rather than resetting the helper as if cleanup succeeded.
3. **Separate hover eligibility from cleanup authority.** The helper uses guard(region=-1) both before move and cancel. If that guard merely returns unsupported when focus or geometry changes, active tooltip debt cannot be cleared by cancel. Define a retained cleanup-capable ownership lease independently of cursor/foreground eligibility; cancel at a safe boundary while that lease still holds. Do not weaken owner/lifetime checks just to make cancellation succeed. Do not unconditionally reinitialize an active/lost helper.
4. **Pinned detail is not established.** `v4_detail_open_call` passes 0x80000008, which is a native default sentinel, not proven permanent pinning. Verify native lifetime/visibility and row-change behavior before advertising a fixed panel. Do not enable Temp's native input eligibility fields: that can expose native down/up actions as well as hover.
5. **No blanket generic-region guard.** Saved `00561120.c` branches3..6 call contextual string expansion and container operations. In particular branches5/6 walk generated collections and can reach the saved nonreturning bounds failure path. Several call arguments are absent from the saved pseudocode. Exact owner+4/VM equality and readable rectangles do not establish those transitive preconditions. This review cannot honestly assign all branch names or approve all four paths. Keep 3..6 unsupported until each dependency/label is separately evidenced. Regions0..2 remain blocked regardless.
6. **Skill data needs a host preflight too.** Count<=100 and valid rectangles are necessary, not sufficient: verify current target/draw generation and the selected native skill string/container, including bounded small-string/heap-string validity, in the same VM/request lease. A native callback without message pumping does not alone exclude other native writers between ticks.

### Concrete smallest integration
A. First wire lifecycle/state diagnostics with native hover disabled: captured image/base, actual game HWND/thread, exact VM/owner/target, modal serial, native-open epoch, lifetime epoch, draw-ready geometry, and cleanup status. Exercise row switch, right-click, focus loss, surface destruction and request supersession through synthetic host tests.
B. For the first opt-in native trial, allow **only skill regions>=7** after the above checks, retain generic3..6 as unsupported and action0..2 blocked. Prefer the already studied synchronous Core CALL boundary to a new timer-driven competing writer. Keep original dispatch on nonowned paths; retire an existing Player+0x42C hover before claiming ownership. Clear-before-fallback must be explicit; do not retain a native tooltip while handing input/writer authority back.
C. Keep ordinary pinned-detail visibility separate from tooltip visibility. Mouse-out clears tooltip only; row change closes old tooltip/detail in order. Failure prevents commit/ordinary teardown until resolved or explicitly reconciled as foreign takeover. Focus return must not resurrect an old epoch.
D. Only after those checks pass, add **one** generic region whose exact native arguments, strings/containers, output ownership and first-hit rectangle have been proved. No generic catch-all branch.
E. Native verification should compare selected row vs detail vs hovered skill, repeated row changes, alternate-window focus loss/return, right-click, normal confirm/cancel and title/load transitions. Capture actual native return/cleanup diagnostics, not only callback counters. Fullscreen/DPI variants remain unsupported until tested.

Review evidence: `WORK_HOVER_INTEGRATION_REVIEW_BEFORE.json` and `WORK_HOVER_INTEGRATION_REVIEW_AFTER.json` record hash/mtime. No source was changed. This recommendation does not require re-analysis of the entire executable.

## Cleanup authority and precise v4/frame integration review — 2026-10-29 (generic5_adapter)

READONLY SOURCE REVIEW; no game/debugger, native analysis, source edits, build or deployment in this task. The prior synthetic helper tests remain unchanged and do not prove a live lease. This extends the independent review above with an implementable state contract, not approval to activate hover.

### Checked version and the existing boundary

Reviewed visuals SHA256 160121E650CA662FE0EAE37EB9120AF1832FEE77BD1B35398FEF536E535AA722; full helper 599507294119C4B15823991B42B25252E163572205309C178406ED813D866F85; skill helper 46EE9A8B0E0D4D9B6F76FD7F141787EF92B743DFF9CB5D69FAF70F617151BCF8; native detail CA2E2C3320BED92DB0814285434D2C11D73654E4667DD720147F923DAE23CE4F; legacy integration BCD5ABC68C91CAE4DEA3BA32D3662F9DDA223A60BE59227F4B5BFC5164FB4944; context 91F33091766205EABABF6DA6C4B419277A9F16FB36B15ED8543AB387D97FC9FD; thunk BAD5A4231A932E87645C8C2C424D99D6E3CCCD1C78FB13494061251D8502BC60. Plugin hash 36EFFC6B1C4469E79CEAEBC0105BC38CCB7DFA45FE7A4480F69289D93CAA6008. Runtime h 4FC33743D151B6047F800AAF354D86C3C901F665FA08188D8CF606148320584F. Parent is editing v3 runtime concurrently; snapshot SHA FD1F213C06CCB82AD170E5E6821CF57ECF20ECAAA2B38C1F1D4013F9E86A0B60 at UTC 2026-10-29T01:14:22.6828239Z, so references below are function names and must be rebased on parent's final version.

Existing legacy installation is WorkSelectorHover_Install in src/work_selector_hover_integration.h:
- Core CALL RVA 0x121AF0, expected E8 6B FA FF FF, original RVA 0x121560, exact return RVA 0x121AF5. These correspond to original preferred VAs 0x521AF0/0x521560/0x521AF5, not addresses to hardcode in a relocated process.
- WORK_SELECTOR_HOVER_DISPATCH_DEFINE receives incoming ECX player and call return address; false tail-forwards original with preserved entry state, true returns AL=1. It saves/restores GPR/flags/x87/MMX/SSE and requires FXSR/SSE. This is not an arbitrary timer callback and not merely a graphics frame hook.
- Existing WorkSelectorHover_Install belongs to legacy bridge/plugin. v4 currently has no connection to this CALL. Current v4 scheduling is WH_GETMESSAGE PM_REMOVE -> selector_tick; worker posts WM_NULL each 100ms when selector_work_pending. v3 active-binding checks additionally throttle at 200ms.
- The legacy callback's packet/presentation globals, work_preview_parent and work_preview_native_detail cannot be reused as v4 authority. Extract/reuse ABI thunk and pure context/geometry validation, not the entire legacy integration include. That include also has legacy HK_OK macro accommodation; do not add it wholesale to the Core TU.
- If the legacy plugin already reserves/patches this CALL, a second install must fail or use a single Core/broker owner with exclusive dispatch arbitration. Never double-hook or chain an unverified installed target. Require an inactive legacy owner before the small v4 spike.

### Separate three permissions

A. **May display/hover now**: native UI thread, current request/candidate identity, current detail draw-generation/target, visible game/detail, acceptable foreground and uncovered cursor, validated geometry/coordinate mapping, approved hotspot and bounded text/container. Focus loss, cursor-out and filtering may remove A immediately.

B. **May clear our old tooltip now (cleanup authority)**: same native image/module instance, pinned DLL, same UI thread, exact Temp instance and owner/VM identity, still-live native owner/VM and detail object, exclusive shared tooltip-writer lease, same acquired ownership generation; no native dispatch writer handoff since acquisition. B MUST NOT depend on candidate still being eligible, foreground, cursor inside, table HWND still visible, or current sort order. Those changes require cleanup, not loss of permission to clean.

C. **May advance DAT**: current request/anchor/output cells pass existing fresh binding and consume/store protocol AND our tooltip/detail are fully retired. B is not C. Losing C does not authorize global tooltip mutation, and losing A does not necessarily lose B.

Existing full helper guard(region=-1) must implement B only; place A at the host dispatch gate and per-region checks. Its current identity function still checks detail visible via work_skill_hover_validate. Therefore if native hide already made Temp invisible, this helper cannot clear afterward even with the right pointers. This is a real ordering limitation: clear BEFORE hide/automatic disappearance; do not solve it by blindly loosening the visibility/owner checks. If automatic disappearance occurs before clear, quarantine and establish separate safe clear evidence or explicit native lifecycle reconciliation.

### Proposed local lease record and state transitions (not code)

Lease stores: monotonically increasing generation, acquired request serial, native lifetime/open epochs, base/image identity, main HWND + creator thread, Temp instance, exact owner pointer + VM, target definition, validated draw generation, and flags tooltip_dirty/detail_owned/in_native_call/retire_requested. Also retain a reason and retiring serial independently of current successor request. A pointer/epoch equality snapshot alone is not a grant of exclusive writer ownership.

States:
1. IDLE: no debt, no claim.
2. DETAIL_ONLY: owned fixed detail, no tooltip debt.
3. HOVER_DIRTY: set BEFORE native clear/hover may mutate globals, not after success only.
4. RETIRING: no new hover/open/confirm; clear using B, then hide detail; only after both success release modal input/writer ownership. Focus loss can clean tooltip then return to DETAIL_ONLY, preserving fixed detail, rather than retiring whole table.
5. QUARANTINED: B temporarily unprovable/clear failed; retain debt, bounded diagnostic and UI-thread retry only while B can be re-established before native writer handoff. Do not call the original dispatcher after claiming it is clean.
6. LOST_FOREIGN/OWNER_DESTROYED: do not clear foreign/freed native state; retain a terminal unresolved-cleanup diagnostic (not a successful clear). Stop all native preview callbacks. Reconcile via known native lifecycle/reset before acquiring a new generation. Module remains pinned.

No silent reinit resets HOVER_DIRTY/QUARANTINED/LOST. Do not use legacy work_hover_host_cancel unchanged: it calls work_skill_hover_lost on any unsafe/failing cancel, even a transient validation failure, and drops active debt. New strict ERROR vs LOST handling is required.

Before initial acquisition, Player+0x42C previous_hover and +0x428 capture must be clear (legacy context guard already checks this), and all relevant native tooltip writers must be excluded for the lease. If occupied, refuse acquisition and leave native handling alone; do not clear somebody else's tooltip to obtain it. A successful context sample is documented as preflight, not lease. A full native lifetime invalidation is not a harmless loss of A: it may invalidate B too, requiring cleanup before that event or no native calls afterward.

### Exact integration touch points for parent

- **Plugin installation**: install/reserve the single legacy CALL under the same exact image and safe initialization preconditions as other Core hooks; immutable original target and sticky retained failure. Expose only capability after complete install. No vtable/global state writes. Feature remains opt-in.
- **Frame CALL callback**: check UI thread and exact return RVA first; reject recursion; identify exclusive lease. With no lease tail-forward original. With valid owned lease perform only synchronous bounded preflight/hover/clear, no DAT parsing/WIC/file IO/UI creation/DestroyWindow/message pumping. Inside owned detail, consume permitted hover; denied action0..2 or unsupported generic3..6 must not fall through to native detail actions. Before any fallback to original, resolve owned tooltip debt or revoke native-hover capability through a defined quarantine path; original dispatch must never be falsely treated as harmless cleanup.
- **v4_on_select / v4_detail_show**: turn selection into requested row identity. Before replacement clear old tooltip, then hide old detail. Open new detail only after retirement succeeded and serial/lifetime revalidated. Do not overwrite the lease with the next row on failed close. Wait for visible draw-ready snapshot before hover.
- **v4_detail_close / v4_detail_tick**: funnel all hides, including epoch-mismatch tick, through one retire routine. Current work_native_detail_tick can invoke hide internally on mismatch; calling it directly bypasses tooltip cleanup. Do not merely insert cleanup in the user-close path.
- **v3_surface_close / v3_chosen**: current close ignores v4_detail_close failure then EnableWindow/DestroyWindow; incompatible with new debt. Gate ordinary teardown and DAT commit on retirement completion. Because chosen closes its surface first, it must not restore original native-input/writer eligibility before clear+hide succeeds. Store a pending operation token rather than keeping a raw callback stack alive. After asynchronous retirement, full fresh binding must run again before consume/store. User cancel may retire overlay while leaving native anchor pending.
- **selector_v3_supersede**: current dispatcher observation invokes v4_detail_close while script continues, and ignores result. A newly dirty tooltip requires cleanup before known event/lifetime side effects, not a later tick against dead VM. Pure revocation/request publication remains safe; deferred UI cleanup only works if native ownership remains proven. Do not claim complete supersede safety until the exact before-destruction boundary is established or native hover is disabled for that path.
- **selector_v3_pre_tick / selector_v3_tick / selector_tick work_pending**: retry cleanup before showing successors and before v1/v2 captures enabled state. Final scheduling must be OR of v1/v2 work, v3/v4 work AND independent cleanup debt, not merely active v4. Current sites set pending=0 for retired serials; audit all those writes together. Avoid the 200ms binding throttle for urgent cleanup.
- **WM_NCDESTROY**: true external owner destruction cannot safely call native clear/hide. Mark teardown-loss with lease diagnostic before abandoning native pointers. Do not claim successful clear or allow a subsequent same-address owner to inherit old authority. Ordinary explicit destroy should occur only AFTER successful cleanup.
- **probe_shutdown**: current DLL stays pinned and returns HK_BUSY. Preserve that; shutdown must not pretend unload-safe if lease/debt/callbacks remain. A new success return needs callback drain/restore proof, beyond this spike.

### Compatibility with the user's fixed-detail requirement

A skill-only Temp trial is a defensible *partial proof*, not completion: row click must create a fixed detail, cursor may leave the row and enter its skill icons, and tooltip-out should clear tooltip without closing the detail. No synthetic hover on the row can stand in for this. Native Temp's fixed visible lifetime under normal dispatch and focus changes is still unproved from the current 0x80000008 sentinel alone.

The first trial can meet the fixed row/cursor/skill subset only after lease and pinning evidence. It explicitly does not meet face/class/movement/capability explanations; generic3..6 remain disabled until exact dependent contextual text/collections are proven. It also does not implement explicit mode2 StatusWnd action buttons. Keep these as separate OPEN items, not silently satisfied by Temp. Do not force native active/input flags to make Temp interactive.

### Minimal next tests before native activation

Synthetic host tests should drive the actual retirement integration, not merely a duplicate enum model: clear failure prevents hide and commit; hide failure preserves remaining debt; A false/B true on focus loss clears once; row A->B does not open B on unresolved A; stale callback cannot retire successor; visible=false while dirty becomes quarantine without unsafe clear; reentrant callback cannot replace lease; lifetime/context swap becomes terminal loss without foreign clear; pending-work stays set after request retires; external WM_NCDESTROY makes no native call; Core CALL collision refuses before publication; unowned fallback is exactly original. Then run actual production TU compile/link. Existing helper tests can be reused for ABI/first-hit/epoch checks.

I did not add an independent cleanup-state header here: it would encode state transitions but cannot establish the missing native writer/lifetime authority, and another unattached state machine would duplicate the host transition work parent must perform. The concrete useful next implementation is a narrowly owned runtime retirement integration with native hover still disabled; only after those tests and ownership observations should the opt-in skill callback be connected. This review introduces no completion claim and no new game patch.

Scheduling formula clarification: pending = legacy_request_work OR generic_request_work OR cleanup_debt. Cleanup debt is an independent OR term, never gated by an active request. The retained/quarantine states above are design requirements, not a proven way to suppress all native writers; if that ownership cannot be established, do not activate this native-hover spike.


## Independent cleanup-authority adapter (2026-10-29 resumed)
Implemented new src/work_detail_cleanup.h only; no runtime/grid/visuals changes, hooks, native addresses or game operations. This advances the earlier authority design without claiming StatusWnd suppression or full hover is proven. Existing native adapters remain unconnected. Design chosen under parent's explicit independent-helper authorization.

API contract:
- WdcToken captures epoch, VM, detail self and target. acquire requires nonzero identity, native capture==0, and native press sentinel80000008; host must supply a real exclusive lifetime/tooltip lease, not readable-pointer inference.
- WdcOps provides lease/clear/hide/hover. Lease validation is separate from can_hover (focus/cursor/region/current-request permission) and must remain possible after hide. Return OK1/RETRY0/LOST-1. Callbacks execute with reentry lock.
- wdc_frame only invokes hover/clear, marks dirty BEFORE native hover and revalidates after callbacks. Focus/cursor loss clears explanation but leaves pinned detail and modal input ownership.
- wdc_retire marks RETIRING, clears explanation before hide, and retains debt on transient failure. Clear failure prevents hide; hide failure does not repeat already successful clear. hide must be retry-safe because a failure may follow a partial native effect. Only OK permits disposal/reuse.
- Foreign takeover is terminal FORElGN: no more native cleanup calls; dirty state is retained for diagnosis. No recovery/reset API silently discards this state. Host must quarantine and establish safe recovery independently.
- input_policy returns FORWARD only in IDLE, CONSUME while owned/retiring, BLOCKED after ownership loss. BLOCKED is a recovery requirement, NOT permission to send native action input. No down/up/wheel callbacks exist. No code can infer that the frame CALL has covered every native input source.
- Initialization is only for fresh/unpublished storage; do not reinitialize live/lost state. Struct fields are internal state and callbacks must not modify them or pump messages.

Test evidence (actual Windows x86, -Wall -Wextra -Werror):
- Tests written before adapter. Test-only null-service baseline work_detail_cleanup_baseline.h returns no acquired service; explicitly NOT a historical production implementation. O0/O2 each24 PASS67 FAIL, exit1. This is new-feature contract RED, not evidence of a preexisting product regression.
- Production independent adapter O0/O2 each113 PASS0 FAIL, exit0. Tests cover clear-before-hide order, dirty-before-hover, repeated cancel idempotence, focus-out keep-pin, transient lease failure retaining debt, clear failure blocking hide/hover/switch, hide retry without duplicate clear, foreign takeover before/during each callback, failure after native hover may have mutated state, callback reentry, capture/press guards, missing callbacks.
- Logs: test_detail_cleanup_red-O0/O2.txt and test_detail_cleanup_green-O0/O2.txt; runner build_work_detail_cleanup_test.ps1. Null-service baseline is only in this evidence directory; not included in production build.
- No broad product suite result is claimed: new adapter has no production callers. Existing runtime/native adapter tests unchanged. Parent integration must add call-site lifecycle tests before enabling this helper.

Frozen identities:
- src/work_detail_cleanup.h SHA256 7D24899A6446B6DD73DE3C162714DC1D76775C7E79BD642C4314C73CB1ACCD92.
- test_work_detail_cleanup.c 17BBCF19F9B83D509CB3130C25103B2639D8E4B62BB390617A560B30CDDD5622.
- build_work_detail_cleanup_test.ps1 B62EADFFBB733F53F1734EE403A71DA318721DAB68AE1BE89F9065A8BA65CE5C.
- work_detail_cleanup_baseline.h 0C7F69CCE67B9FF1EA449495656D88A2E295192FF2D47454C4BA8893197F8254.

Integration still requires the two managed-CALL proposal's native proof. This helper does NOT suppress button construction, grant lease authority, validate generic native text containers, choose a StatusWnd instance, open/hide native windows itself, or prove whole-game input isolation. The 55D555 continuation adapter and 55B5B0 side-effect boundaries remain unimplemented. Mode2 is still not enabled.
