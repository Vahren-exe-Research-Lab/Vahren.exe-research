# Bootstrap implementation plan

1. Add host integration tests that parse full config before loading, exclude disabled entries, enforce dependency order, reject occupied Core, and roll back failed starts.
2. Observe RED against a bootstrap scaffold; then implement using bounded manifest plan and Core function pointers.
3. Add only an idle query to existing Core, so bootstrap can reject any occupied/retrying Core before claiming it.
4. Build/run x86 fixtures and existing Core suites.

Ownership: caller serializes all Core/bootstrap calls across threads and keeps runtime function pointers/DLL and logging callback alive. Bootstrap starts only with idle Core and owns its entire loaded stack until shutdown succeeds. A failed rollback leaves ownership retained for explicit shutdown retry; caller must not unload Core. No game launch, deployment, hooks, scan or automatic DLL discovery.

## Implemented interface

`HK_BootstrapStart` accepts a zero-initialized context, Core runtime function pointers, config bytes/length, an explicitly authorized dedicated plugin directory, logger and result storage. It parses the entire manifest and constructs every planned UTF-16 path before calling Core Load. Only enabled planned basenames are passed to Core, in dependency order. Directory must be a drive-absolute Windows path; GetFullPathNameW canonicalizes it without depending on cwd. Each joined path is limited to 1023 UTF-16 code units. UNC/device paths are currently unsupported. Config file reading is left to the caller.

Core gains only the read-only `HakushinCore_IsIdle` export and matching typedef. Bootstrap rejects any occupied or retrying Core before acquiring ownership. This check is not an atomic claim and adds no thread safety: caller must serialize all access, and no external Core calls may interleave while bootstrap owns it. Runtime DLL/function pointers, context and log callback must stay alive until BootstrapShutdown succeeds. An empty enabled plan does not acquire ownership.

On load failure, later entries are never started. Bootstrap immediately requests reverse-order Core shutdown. If rollback succeeds it returns HKB_CORE with the original `core_status`, clears ownership and leaves Core idle. If rollback fails it returns HKB_RETAINED with both original and rollback statuses, sets `result.retained=1`, and retains ownership. Retry `HK_BootstrapShutdown`; never unload Core while ownership remains. `result.started` counts successful starts before failure, not currently retained modules. `retained` flags a failed rollback, not an ordinary successful running state; use `ctx.owned` for lifetime ownership. Nested bootstrap calls during logging/load/rollback/shutdown return HKB_BUSY. Callback exceptions/crashes remain unsupported.

Authorization is supplied explicitly as `authorized==1`; it is the caller's trust decision, not a security boundary. Before any plugin LoadLibrary, this layer opens every enabled file and checks bounded DOS/PE headers, i386 machine, PE32 optional header, DLL flag and basic header/section-table bounds. It does not verify signatures, hashes, symlinks/reparse points or replacement races. Core is already loaded by its owner before bootstrap is invoked. Native dependency DLL resolution may execute additional trusted dependencies; manifest allowlisting governs explicitly requested plugin entry DLLs. No plugin crash isolation, hook implementation or game deployment is provided.

## Verification

Build command: `& '<研究ルート>/data/recruit_sort_v4/core/build_bootstrap_test.ps1'`. The script uses Zig 0.14.1 `cc -target x86-windows-gnu -Wall -Wextra -Werror`; it builds Core and fixture DLLs, then links `hakushin_bootstrap.c hakushin_manifest.c fixture_bootstrap.c` with `-municode` into fixture_bootstrap.exe.

The initial scaffold failed the malformed-tail config assertion. Implemented integration tests cover zero initialization on malformed config, disabled exclusion, authorization/path rejection, dependency order, missing DLL followed by a never-started dependent, failed init with clean rollback, failed rollback retaining both modules and retry, occupied Core rejection without touching its existing module, and callback reentry. Bootstrap and all seven existing Core fixtures passed; the multi-plugin regression is run in the same verification sequence.

## All-file preflight

Preflight reads only fixed DOS (64-byte), PE signature/COFF (24-byte) and PE32 optional (224-byte) headers. It bounds e_lfanew to 64..1048576, section count to 1..96, optional-header size to 224..4096, and checks header/section-table end against actual file length and SizeOfHeaders. Non-i386/PE32 returns HKBP_ARCH; invalid/truncated headers return HKBP_FORMAT; file open failure returns HKBP_FILE. The result includes the failing plan index and HKB_PREFLIGHT. No plugin is started and no rollback is needed when preflight fails. This is basic architecture/format screening, not a full Windows PE loader verifier.

Tests added missing, malformed and a real compiled x64 DLL as later entries, each asserting zero earlier initialization. This regression first failed before preflight was implemented. Runtime rollback cases use valid x86 DLLs whose init returns failure, so both clean rollback and retained failed rollback still execute. File handles close after preflight; the authorized directory must remain trusted and unchanged through loading. Dependencies of plugin DLLs are not recursively PE-preflighted.

Final review tests also reject an actual x86 executable built with a .dll filename (DLL flag absent), and accept disabled missing/malformed entries without any Core load log, initialization or active module. The EXE fixture build-script insertion initially failed due to a Local tunnel connection error; the next test correctly reported the missing fixture, then after retrying the verified edit the complete bootstrap suite passed. Final bootstrap run exited 0. The preceding combined bootstrap/Core/multi/manifest run also exited 0. All implementation/host builds use x86; only the deliberately rejected architecture fixture is built x86_64.

Startup diagnostics follow-up: failed_index is now assigned on Core load/init rejection as well as preflight failure. A regression test rejects an init-failing second plugin and requires failed_index==1; it failed before the assignment and passed afterward. Index refers to the resolved plan order and is only meaningful for failure results.

## Claude addendum (2026-10-26)

For entries with has_sha256, preflight hashes the whole file (limit 64 MiB) through a handle opened with FILE_SHARE_READ only and returns HKBP_HASH (4) on mismatch before any Core call. Every successfully preflighted handle stays open until the load loop finishes, so the verified file cannot be modified or replaced before LoadLibraryExW. This still does not cover transitive native dependencies of the plugin.
