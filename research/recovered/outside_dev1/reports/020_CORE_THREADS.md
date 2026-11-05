# Nonblocking Core ownership gate

All public Core status/lifecycle exports and all bound reservation, managed CALL,
and event methods enter a process-local atomic ownership gate before touching
mutable Core state or validating arguments/instance tokens. A competing thread
returns existing HK_BUSY or HKX_BUSY immediately without waiting or changing outputs.
BUSY takes precedence over invalid arguments/stale tokens during contention. There
is no automatic retry: callers explicitly defer or handle BUSY. DllMain is stateless.

The Windows thread ID owner is claimed using InterlockedCompareExchange. Only the
owner touches recursion depth; final leave releases using InterlockedExchange.
Ownership spans logging, loader calls, plugin init/shutdown and event callbacks.
Same-thread recursion enters the gate, while existing in_progress restrictions
still reject nested Load, Shutdown and emit. Init query/reservation and callback
self-unsubscribe remain allowed. QueryExtension requires exact init API identity
on the owning init thread. ABI1 and all extension structures are unchanged.

Bound extension methods retain their existing mixed HKX/manager status convention.
HKX_BUSY is numeric 7, which overlaps existing manager status values (including
HKCP ownership errors). No new enum or disambiguating status API is added. Treat
nonzero install results as failure, do not consume an output handle on contention,
and retain existing recovery/ownership obligations. BUSY never supplies a new handle.

This gate serializes Core metadata only. It does not suspend patched target threads,
prove patch atomicity, drain timers/callbacks, establish unload quiescence, or make
standalone HKH/HKCP/HKE entry points thread-safe. Callbacks must return normally;
exception/longjmp/thread termination and owner-death recovery are outside contract.
Core must remain loaded while its function pointers are used. No recruit adapter,
game deployment, or hot unload changes are included.

## Verification (2026-10-25)

build_core_threads_test.ps1 uses bundled Zig 0.14.1, x86-windows-gnu and
-Wall -Wextra -Werror to build a real Core DLL, plugin DLL and host under
core_threads_fixture. Event barriers hold init and then an emit callback while
a competing thread invokes every public Core API and each bound extension method.
It checks exact init identity cross-thread rejection, unchanged query/reservation/
CALL/event outputs on BUSY, successful calls afterward, same-thread self-unsubscribe,
lifecycle/emit reentry restrictions, and release after invalid Load. Test barriers
and joins have 10-second bounds.

RED before implementation: FAIL at query(identity,2,1,sizeof(out),&out)==HKX_BUSY;
the unguarded Core returned success during another thread's init. GREEN after
implementation: all three focused PASS lines. Regression suites passed with exit 0:
build_core_extensions_test.ps1, build_core_events_test.ps1, build_core_call_test.ps1,
build_test.ps1 (seven Core cases), build_multi_test.ps1, build_bootstrap_test.ps1.
This is deterministic two-thread overlap evidence, not stress or native unload proof.
