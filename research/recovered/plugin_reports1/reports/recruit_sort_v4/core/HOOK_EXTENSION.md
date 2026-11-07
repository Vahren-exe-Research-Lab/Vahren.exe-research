# Reservation extension integration plan

ABI1 structures, size/version checks and init signature remain unchanged. New optional Core export discovers a separate versioned reservation table. Only the current init callback can acquire it using its exact Core API address. Core-issued monotonic tokens bind callbacks to instance ownership; arbitrary owner IDs are not accepted.

Tests first: old ABI1, two real plugins, overlap and own release, stale instance after slot reuse, wrong query arguments/output preservation, clean/dirty failed init, shutdown OK with reservations and reserve rejection while stopping. Dirty init Load returns existing HK_SHUTDOWN_ERROR (8), distinct from clean failure HK_INIT_ERROR (6). Bootstrap retained rollback is exercised.

No legacy hook DLL integration, actual patching, UI or game operations. Reservation release never implies native patch removal.

## Acquisition and binding

A plugin receives the unchanged ABI1 HK_CoreApi pointer during init. GetModuleHandleExW(FROM_ADDRESS | UNCHANGED_REFCOUNT, api_pointer) identifies its owning Core module without a hardcoded filename. GetProcAddress resolves optional HakushinCore_QueryExtension. The query accepts exact API object identity only while that plugin init callback is executing, extension ID 1/version 1 and exact output-table size. Failure leaves output untouched. The extension table contains size/version, a Core-issued 64-bit instance token and reserve/release callbacks; there is no caller-selected owner argument.

Tokens monotonically increase across all init attempts, never wrap, and are retired on clean unload. Old tables remain callable only while Core itself remains loaded, and return HKX_STALE_INSTANCE after retirement/reuse. ABI pointer discovery is restricted to current init, so retaining a raw API pointer does not enable later extension acquisition. This is cooperative lifecycle/ownership validation, not a security boundary against a malicious native DLL that can inspect process memory or forge observed tokens. All public Core and bound extension calls use the nonblocking ownership gate described in CORE_THREADS.md. Competing threads receive BUSY without output mutation; callers handle or defer BUSY explicitly.

Reservation methods return HKH_* metadata status or HKX_STALE_INSTANCE/HKX_BUSY. They validate the live instance first and bind its token internally as the reservation owner. During shutdown or unresolved cleanup, all new reservations are refused, while valid releases remain available. The underlying manager still performs no patching or target-memory access.

## Failure and unload contract

Core counts each instance's outstanding successful reservations. Clean failed init returns HK_INIT_ERROR (6) and unloads. Failed init with reservations commits a retained cleanup-pending slot, blocks new loads, keeps DLL/API/token valid and returns HK_SHUTDOWN_ERROR (8). The extension contract requires the plugin shutdown callback to support cleanup even after init failed.

Shutdown success is insufficient when reservations remain: Core returns HK_SHUTDOWN_ERROR and retains that module plus earlier dependencies. Retry invokes shutdown again. Only callback success plus zero reservations allows unload. No reservation is implicitly removed, including failed init. This is metadata cleanup accounting; actual hook restoration/quiescence remains the plugin's future verified obligation. Old ABI1 plugins that never acquire the extension retain their prior behavior.

Bootstrap already calls shutdown after any load error. The real-DLL fixture tests dirty init returning 8, bootstrap rollback also returning 8, ownership/module retention, and a later explicit shutdown that releases the reservation and unloads. No legacy eight-hook plugin or timer lifecycle is integrated.

## Build and verification

Run `build_core_extensions_test.ps1`. It builds actual x86 Core and five extension plugin variants plus an old ABI1 fixture with Zig 0.14.1 `-target x86-windows-gnu -Wall -Wextra -Werror`. RED observed old ABI1 success followed by the first extension plugin failing because Core lacked the extension. GREEN covers wrong query size/version/identity with unchanged output, overlap, cross-owner release denial, own release, stale instance after reuse, clean/dirty init failure, reserve denial while stopping, shutdown-OK-but-dirty retention/retry and bootstrap dirty-init rollback.

Every existing Core-building script now links hakushin_hooks.c. hakushin_abi.h is unchanged. Existing Core, multi-plugin, bootstrap, hooks, manifest and opt-in startup suites are regression targets. Production deployment, UI and game files are outside this stage.

Final verification on 2026-10-25: combined extension, original seven Core cases, multi-plugin, bootstrap, reservation, manifest and twelve startup cases completed with exit code 0. Startup run evidence is under startup_fixture/run_f1b3afbb430647e7a7d5e2d6a7873672. Both production normal startup and diagnostic retained-rollback scenarios passed. No unregistered legacy hook DLL was loaded. Token exhaustion and malicious native-memory forgery are not simulated; neither is claimed to be isolated.

## Claude addendum (2026-10-26)

Reservations owned by a managed HKPP pointer record cannot be released through the Reservations extension (HKH_WRONG_OWNER), mirroring managed CALL records. Owner busy now includes HKPP records for init failure, shutdown and unload.
