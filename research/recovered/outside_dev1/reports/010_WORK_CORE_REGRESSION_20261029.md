# Windows Core/loader regression — 2026-10-29

Scope: 16 previously unrun Core/loader scripts plus standalone managed render-pointer test. Synthetic fixtures only; no game/debugger operation, original EXE/DAT/save or diagnostic-copy changes.

## Isolation and evidence
- Inspected scripts and 55 source/header/DEF dependencies for process targets, file writes and deletion.
- Copied exact sources to `core_reg_20261029/`; only isolated script Zig paths were changed to the installed Zig 0.14.1 executable.
- Copied source hashes verified; original 70 source/script SHA-256 and mtimes matched before/after.
- `WORK_CORE_PREFLIGHT.json`: dependency inventory and side-effect review.
- `core_reg_20261029/copies.json`: original/copy hashes.
- `core_reg_20261029/results.json`: exact commands and exit codes.
- `core_reg_20261029/summary.json`: results, skip, original-state check, output artifact hashes.
- Per-suite stdout/stderr retained. All 19 executed build/run steps exited 0; every stderr log was empty. Stdout PASS lines read back.
- Local process session 5892 finished, exit 0. No active build remains.

## Results
PASS: build_test (7 scenarios), build_multi_test, build_hooks_test, build_events_test (130 checks), build_call_patch_test, build_core_call_test, build_core_events_test, build_core_extensions_test, build_core_threads_test, build_manifest_test, build_bootstrap_test, build_proxy_test (production/diagnostic), build_proxy_import_test, build_startup_test (12 scenarios), build_claude_loader_patch_test.
Claude patch subtests: PTR 82/82, manifest/SHA 16/16, PTR integration 17/17, hash/pinning 41/41, loader_wait 9/9.
Standalone managed render-pointer: PASS 10/10 after separate Core/plugin/host builds.

## Not executed
`core/build_startup_logger_test.ps1` remains SKIPPED: `core/fixture_startup_logger.c:53` calls `DeleteFileW(log_path)`. User requires recoverable deletion; parent instructed not to execute suites containing permanent deletion. No fixture source was altered in this task.
This is **15/16 requested scripts PASS, 1 SKIP, plus standalone render-pointer PASS**, not a claim that every repository test is complete. Other legacy selector/recruit/helper/hover suites are outside this follow-up.
Golden/MATCH and game verification are unaffected.

## Follow-up: startup logger completed
Parent subsequently authorized the narrowly scoped fixture change. `core/fixture_startup_logger.c` now reserves a PID/sequence log with CREATE_NEW and retains it; GetTempFileNameW/DeleteFileW were removed. Formatting, bounded-read and exact emitted-content expectations remain unchanged. Dated comment added; original build script unchanged.
- Before SHA-256: 018e1112fbd3f6077b2899676b0405fab8e38c31c6e68cc5cd4491ababfaac44
- After SHA-256: f743175feb0f4f26606c69f7f33877b7fa39eceff6daec8406c0e34d1a4206e4
- RED: static log-preservation contract exit 1 on old source; unsafe old fixture was not executed.
- GREEN: Windows existing build script (isolated source-identical copy, absolute Zig path only) exit 0, LOGGER failures=0.
- Extra O2 same-process double-run: exit 0, LOGGER failures=0 twice. Two distinct same-PID logs retained; previous log hash/mtime unchanged.
- Evidence: `logger_preserve_20261029/` contains before/after metadata, backup, diff, commands, stdout/stderr, hashes and all three retained logs.
- All results/source read back. Session 22912 completed. No game/deployment or production runtime change.
Coverage is now **16/16 requested Core/loader scripts PASS plus standalone render-pointer PASS**; this is still not a claim that every legacy plugin or repository suite was run.
