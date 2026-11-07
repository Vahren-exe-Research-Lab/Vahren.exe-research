# DAT routine event bus (candidate, 2026-11-03)

Status: implemented on local branch `feat/dat-routine-bus-multientry-20261103`.
Three-entry implementation passes O0/O2 synthetic tests. The original
`battleEvent`/`dead_event` **routing** was observed independently, and
a candidate DLL passed an initial-title installation smoke test in the
diagnostic game copy. A real `hk_` callback during battle has NOT yet
been verified; do not mistake hook installation for end-to-end delivery.

## Purpose

HakushinDatUiSelector already owns the five-byte E8 CALL at RVA
`0x33B62` (entry A). It now additionally reserves combat entry C
(RVA `0x9356A`) and third entry B (RVA `0x33754`) with the **same
Core-managed CALL patch owner**, rather than conflicting with a second
EXP plugin. All three call original `0x4A1250`.
A dispatches both selector requests and the optional event; B and C
dispatch **only the event**, never launching selector UI.
This is a notification **before** the original DAT dispatcher executes,
not a replacement/skip instruction. The original function is always
tail-forwarded, including when no consumer exists or event delivery fails.

The producer accepts the known ScriptFunc vptr / exact `routine` string,
one literal string expression, name length 4..31 bytes, prefix `hk_`,
and a verified `wduc_resolve` evaluator-to-VM relation. It rejects
`hk_ui_select_v1` through `hk_ui_select_v4` (owned by selector itself).
Malformed or unreadable objects and any unverified context fail closed.
The producer executes on the **original DAT-calling thread**; combat
calls are not silently dropped merely because the thread differs from
the UI thread. Its `off_ui_thread` counter exposes those occurrences.
Consumers must validate the original VM/context and thread themselves.
No queued/asynchronous delivery is supplied.

Public contract: `core/hakushin_dat_routine_bus.h`.
Event type: `HK_DAT_ROUTINE_EVENT` (0x484B4452, "HKDR").
Payload: `HK_DatRoutineEventV1` (`size`, `version`,
`evaluator`, `vm_context`, `thread_id`, `name[32]`).
The name is an owned NUL-terminated copy; addresses are borrowed x86
pointers whose validity does not outlive the callback. Payload size
is 52 bytes, within Core's 64KB event payload limit.
The separate `HK_DatRoutineBusStatusV1` export reports `site_mask`,
`site_failed_mask`, `enabled`, `emitted`, `emit_failed` and
`off_ui_thread`. Site bits are A=1, C=2, B=4. A and C are required
for the observed scenario; a missing site must not be treated as full
coverage.
## Consumer outline

Include `hakushin_extensions.h` and `hakushin_dat_routine_bus.h`.
In `HakushinPlugin_Query`'s init callback, use Core's
`HakushinCore_QueryExtension(api, HK_EXTENSION_EVENTS, HK_EVENTS_VERSION,
sizeof(events), &events)`. Then call:

```c
static HK_EventsV1 events;
static HKE_Handle subscription;

static void HKE_CALL receive(uint32_t type, const void *payload,
                             uint32_t len, void *user) {
 (void)user;
 if(type != HK_DAT_ROUTINE_EVENT ||
    len != sizeof(HK_DatRoutineEventV1) || !payload) return;
 const HK_DatRoutineEventV1 *e = payload;
 if(e->size != sizeof(*e) || e->version != HK_DAT_ROUTINE_VERSION) return;
 if(strcmp(e->name, "hk_exp_v1") == 0) {
  /* Input/return variables and engine calls need a separately validated ABI. */
 }
}
/* During init, after a successful QueryExtension: */
events.subscribe(events.instance, HK_DAT_ROUTINE_EVENT,
                 receive, NULL, &subscription);
/* Before a clean plugin shutdown: unsubscribe or cancel_owner. */
```

Each plugin obtains its *own* Core extension instance in its init callback.
A consumer must return normally, never throw/longjmp from a callback,
never retain pointers past the callback, and must avoid recursive emit.
The Core extension can reject emits with BUSY; the producer counts failures
and continues the original call. Game memory mutation and invoking native
`0x49E780` inside the script dispatch frame remain unverified and must
be enabled only after explicit battle-thread/lifetime/ABI confirmation.
## Coverage and tests

2026-11-03 17:51 x32dbg trace (`dat_entry_trace_20261103_b.log`)
confirmed that combat `battleEvent` (260+ executions) and
`dead_event` (1 observed) use **entry C at 0x49356A**. The same trace
observed A outside battle, B zero times. This is evidence of the
original EXE control flow, **not** a runtime test of the modified DLL.

Static bytes verified against SHA-256 E8DAC301...767187:
- A: `00433B62: E8 E9 D6 06 00`
- C: `0049356A: E8 E1 DC 00 00`
- B: `00433754: E8 F7 DA 06 00`

Each targets `0x4A1250` with the same ECX/stack contract; hook calls
tail-forward unchanged to that function. Hooks are installed at the
initial-title safe point, each using an independent managed reservation.
A failure cannot be repaired by patch chaining or hot-unpatching.
If C or B is unavailable, A remains usable and the status records
partial coverage. A `HKCP_RECOVER` forces a retained failure state.
Thread quiescence for all three sites is an installation prerequisite,
not proven by synthetic tests.

`core/build_dat_routine_bus_test.ps1` runs x86 O0/O2:
- bounded synthetic AST/parser tests, including SSO/heap-backed names,
  reserved exclusions, malformed input, 31-byte limit, and unmodified
  output after rejection;
- real HKE synchronous event subscription/delivery/unsubscribe;
- the actual selector's native dispatcher + fake original routine,
  confirming tail-forward on successful/failed/missing event and
  non-UI-thread calls for A/C/B;
- a fake managed patch backend checking all three exact byte strings,
  targets, per-site reservations, success, conflict, mismatch, busy
  and retained recovery behavior.

`core/build_dat_ui_selector.ps1 -Test -AutoArm` verifies legacy
selector behavior in private synthetic memory. This is **not** a game
acceptance test. Inspect `HakushinDatUiSelector_BusStatus` for
enabled, emitted, emit_failed, off_ui_thread, site_mask and
site_failed_mask metrics in a **new-process, diagnostic-game** test.
The EXP consumer `hk_exp_v1` has not been wired into the event yet.
Live subscriber calls into original `0x49E780`, DAT variable updates,
and battle-start/finish lifetime remain separate integration work.
The legacy dispatcher guard prohibited arbitrary re-entrant native
calls; callbacks must return normally, never throw, longjmp, load/unload
the Core or emit recursively. No general native-call safety guarantee
is implied by this event bus.

## Diagnostic game smoke (2026-11-03)

- Source build: `core/build_dat_ui_input_candidate.ps1 -Test`
  with `HK_ENABLE_INPUT_CAPTURE` and `WORK_DAT_UI_AUTO_ARM`.
  The 351/351 input-provider tests passed in both O0 and O2 builds.
- Candidate SHA-256: `12D08AEE0B1D840EF0055A6EB7A83F1A766F7B5FFF4DE9FEAF3C1BEB116C549E`.
- Original EXE SHA-256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
- Diagnostic PID 30612: `auto_arm_accepted`, then installed site C
  (mask 2), site B (mask 4), A (mask 1). `patch_active mask=7
  failed_mask=0`. Native hover and input-provider initialization also
  logged success. No battle occurred in this smoke.
- The first attempt (short 30-second window) ended before auto-arm;
  the next run reached the title and activated all three patches.
- Post-exit DLL lock required a delayed separate restore. Final hashes
  match the pretest DLL (`5B2585EE...`) and manifest (`057FCED7...`).
  No new DLL remains in the diagnostic game copy.
- Evidence: `dev_lab/_work/summon_exp_20261103/`, specifically
  `diag_smoke_multientry_20261103_b/` and the game-local
  `HakushinDatUiSelector.30612.log`. Do not copy game assets or saves
  into GitHub. Live battle callback testing is still pending.
