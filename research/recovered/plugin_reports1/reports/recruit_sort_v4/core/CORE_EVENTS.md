# Core optional synchronous events extension

ABI1 hakushin_abi.h and HK_CoreApi are unchanged. Extension ID 2/version 1
returns HK_EventsV1 only during the current plugin init, using the exact
Core-owned API object identity and exact output-table size. Unsupported
version/ID, invalid identity/size, and calls outside init leave output untouched.

The table binds subscribe, unsubscribe, cancel_owner and emit to one monotonic
Core-issued instance token. There is no caller-selected owner argument.
Every method validates the live instance before acting; clean unload retires
the token even when its slot is reused. Tables are callable only while the
owning Core DLL remains loaded. This is cooperative native-plugin ownership
validation, not protection against malicious code inspecting or forging tokens.

Event IDs are generic nonzero integers. No game event names, hooks, observer
or game behavior are introduced. The standalone dispatcher remains unchanged.
Its 64-subscription capacity, generation handles, registration order, snapshot
mutation, 65536-byte payload limit and borrowed synchronous payload contract
apply. Methods return HKE_* dispatcher status, or HKX_STALE_INSTANCE/HKX_BUSY
for lifecycle rejection; these numeric families are not globally disjoint.

Core holds its lifecycle guard for the complete emit, through all callbacks,
including after the last subscription removes itself. Nested emits and
Core Load/Shutdown callback reentry are rejected. Emit is also rejected
during init, shutdown, unresolved cleanup, or any other Core lifecycle call.
Subscribe is allowed during init and normal callbacks, but rejected while
stopping/shutting down. Unsubscribe and cancel_owner remain available for
cleanup. Core never silently cancels plugin subscriptions.

Failed init with live subscriptions retains that DLL and earlier dependencies,
sets cleanup-pending/stopping and returns HK_SHUTDOWN_ERROR. Clean failed init
unloads and returns HK_INIT_ERROR. Shutdown callback success also requires zero
reservations and HKE_OwnerBusy false before unload. This includes active callback
ownership, even after self-removal. Cleanup retry calls shutdown again.
IsIdle remains BUSY during callbacks/lifecycle, while any plugin is loaded,
and while cleanup is pending; it is OK after complete clean shutdown.

Core-bound access uses the nonblocking ownership gate in CORE_THREADS.md.
Competing threads receive HKX_BUSY with unchanged outputs. Standalone HKE APIs
require caller serialization. Callbacks must return normally. No exception/crash/longjmp isolation,
queue, forced unload, or native hook restoration is supplied.

## Verification, 2026-10-25

build_core_events_test.ps1 builds real x86 DLLs and a host using Zig 0.14.1,
-target x86-windows-gnu -Wall -Wextra -Werror. Test-first RED: old ABI1 plugin
loaded/unloaded successfully, then the first event plugin load failed because
Core did not yet expose events. After integration: ALL CORE EVENTS TESTS PASSED.

The fixture covers exact identity/version/size and unchanged failure output,
query outside init, legacy ABI1, cross-instance unsubscribe refusal, invalid
and retired instance tokens, synchronous payload delivery, recursive emit
rejection, self-unsubscribe, Load/Shutdown attempts inside callbacks, no repeat
delivery, stopping gates, clean failed init, dirty failed init with dependency
retention, shutdown-success-but-dirty retention and cleanup/retry.

Regression results: reservation extension suite PASS; original seven Core
cases PASS; multi-plugin suite PASS; bootstrap suite PASS; twelve startup cases PASS. Startup evidence:
startup_fixture/run_855d36a4d71147c5840858a576917d10.
All existing Core-building scripts now link hakushin_events.c, including the
recruit build and startup fixture. No deployment was performed.

Limitations: synthetic DLL fixtures only; no game execution, game fix,
real engine event timing, concurrency/exception isolation or malicious native
memory forgery validation. Token exhaustion is not simulated.
