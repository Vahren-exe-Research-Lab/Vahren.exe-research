# Standalone synchronous event dispatcher fixture

This is source-only infrastructure and a synthetic dispatcher fixture. It is
not a hooked battle observer and does not observe, patch, launch or control
the game. No Core ABI function table or DLL lifecycle integration is present.

## Contract
- Zero-initialize registry storage once, then call HKE_Init. Operations before
  initialization fail. Reinitializing a live registry is rejected (BUSY during
  emit). Never reset, copy, move or edit live registry storage.
- At most 64 live subscriptions. Nonzero uint64 owner, nonzero uint32 event
  type, callback and output handle are required. Context may be NULL.
- Callbacks use x86 C cdecl. The fixture requires 32-bit pointers at compile
  time. This header is internal infrastructure, not a new Core DLL ABI export.
- Handles contain slot and uint64 generation. Wrong-owner removal fails;
  stale handles cannot remove reused slots. Owner tokens are bookkeeping,
  not a security boundary.
- Emit is synchronous. Payload is borrowed only for the callback invocation;
  NULL is valid only with length zero. Length must be <=65536 bytes. Caller
  guarantees the pointer names at least that many readable bytes and remains
  valid until Emit returns. Dispatcher cannot validate arbitrary memory.
- Matching callbacks run in registration order, including after slot reuse.
  Emit snapshots subscription identity/order before calling user code.
  Subscriptions added during emit start on the next emit. Removing a pending
  subscription skips it, even if its slot is immediately reused.
- Subscribe, Unsubscribe, CancelOwner and OwnerBusy are allowed in callbacks.
  Emit reentry on the same registry returns BUSY; no recursive dispatch queue.
- CancelOwner removes current subscriptions only; it is not a permanent owner
  ban, and the owner can subscribe again. It never stops an executing callback.
- OwnerBusy is true while subscriptions exist OR that owner's callback is
  executing, including after self-unsubscribe or cancellation. Callback return
  clears execution ownership. This is not a forced-unload mechanism.
- The caller serializes every access across threads. All callbacks must return
  normally; there is no exception, crash or longjmp isolation. The caller owns
  callback/context/payload lifetime and safe module-unload coordination.
- Neither registration sequence nor generation wraps. A max-generation slot
  is retired after removal. Registration sequence exhaustion rejects further
  subscriptions. Outputs remain unchanged on failure. No allocation or queue.

## Verification
Run build_events_test.ps1 from PowerShell. It builds only hakushin_events.c
and fixture_events.c with the existing Zig 0.14.1 compiler, target
x86-windows-gnu, C11, -O2 -Wall -Wextra -Werror, then runs event_fixture.exe.
Result is saved to event_fixture_result.txt. No game executable is involved.

2026-10-25: PASS event dispatcher: 121 checks.
Before implementation, the fixture compiled but failed linking with missing
HKE symbols (expected test-first failure). The completed fixture covers
initialization, invalid inputs and unchanged outputs, owner/generation checks,
64-slot capacity, slot retirement and sequence exhaustion, payload limits,
type filtering, registration order and slot reuse, snapshot mutation,
pending callback removal, self-removal, cancellation, owner busy lifetime,
and reentrant emit rejection. Overflow cases inject boundary values only in
fixture-owned storage; production callers must not edit registry fields.

Limitations: these tests verify a standalone in-process synthetic dispatcher.
They establish no game event timing, hook location, engine safety, DLL unload
safety, or ABI compatibility with a future Core integration.

Review follow-up (2026-10-25): release fixture PASS 130 checks. Added a
sole-subscription self-unsubscribe case: OwnerBusy remains true inside the
callback without CancelOwner or another live subscription, becomes false
after callback return, and later emit does not invoke it. Added last valid
slot generation (UINT64_MAX-1 -> UINT64_MAX), successful removal, stale handle
rejection and selection of a different slot after retirement.
