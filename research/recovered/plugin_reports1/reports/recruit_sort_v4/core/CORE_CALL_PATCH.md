# Core optional managed CALL extension

ABI1 and HK_CoreApi remain unchanged. Extension ID 3/version 1 returns
HK_CallPatchV1 during the owning plugin's init only, using exact Core API
object identity and exact output size. Failure leaves output untouched.
The instance is a monotonic Core-issued token; each method rejects a retired
or unknown instance. Handles retain HKCP generation and owner validation.

Core owns one private HKCP manager using the same fixed HKH registry as
metadata reservations. Install/restore expose no caller-selected owner.
Generic reservation release refuses every active managed reservation handle,
including one guessed by its owning plugin; metadata counts therefore cannot
be decremented by releasing a managed reservation. Metadata reservations with
the same instance remain independently releasable. No manager storage is
exported. Cooperative native ownership is not a malicious-code boundary.

Install is allowed during init and ordinary plugin activity/event callbacks;
it is rejected while stopping or cleanup is pending. Restore remains available
for cleanup. These match the existing reservation/subscription lifecycle gates.
Load/Shutdown/emit retain the existing lifecycle reentry guard. No new callback
is invoked by the production patch backend.

Failed init with any active/recovery managed record retains that module and
earlier dependencies, enters stopping state and returns HK_SHUTDOWN_ERROR.
Shutdown success likewise requires zero metadata reservations, no event owner
activity and no managed records before FreeLibrary. Cleanup retry invokes
shutdown again. Core does not silently restore patches or release ownership.

All standalone CALL_PATCH.md contracts apply: x86 E8+rel32 only, exact five
expected bytes, executable single-page memory, fail-closed restoration, and
retained recovery handles. Core-bound methods use the nonblocking gate in CORE_THREADS.md; callers handle BUSY.
Standalone HKCP calls require caller serialization. Caller must guarantee no thread
executes or mutates the entire span during install/restore. Caller must prove
replacement ABI/lifetime and quiescence before module unload. Core supplies no
thread suspension, callback drain, automatic safe detach or exception isolation.
Tables are usable only while their owning Core DLL remains loaded.

## Verification (2026-10-25)

Actual x86 DLL fixture, Zig 0.14.1, -Wall -Wextra -Werror. Initial RED failed
normal plugin load because extension 3 was unavailable (exit 1), before Core
or header implementation. GREEN: ALL CORE CALL TESTS PASSED.
Only private VirtualAlloc executable pages are patched; no game launched.

Coverage: exact query identity/version/size and unchanged failure output;
shared overlap both directions; manager reservation release refusal (including
same owner), independently released same-owner metadata; restore/reinstall and
stale generation; wrong owner and retired token; exact clean restore and actual
module unload; dirty init/dependency retention; shutdown-success-but-dirty
retention and retry; unknown-byte corruption refuses restore and keeps overlap,
followed by explicit fixture repair and successful cleanup.

No deterministic backend injection is exposed by Core. Post-write partial
Win32 failures cannot be induced reliably through this fixture; standalone
HKCP tests remain the evidence for partial write/flush/protection recovery.
Core tests exercise retained unknown-byte restoration failure, not a claimed
real OS partial-write failure. No game integration or deployment performed.

Regressions passed: reservations, events, original seven Core cases,
multi-plugin, bootstrap, recruit adapter (-Test), and all twelve startup cases.
Startup evidence: startup_fixture/run_40b8a6ce95024413a9016736ddd222df.
All eight existing Core-building scripts link hakushin_call_patch.c.
Standalone component source remains unchanged. No commits or Git operations.
