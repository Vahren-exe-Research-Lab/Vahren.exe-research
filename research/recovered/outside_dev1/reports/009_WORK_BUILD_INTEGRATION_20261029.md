# Work v4/v5 build integration — 2026-10-29
Scope: build/test-only integration of Claude README §8–9. No product runtime/header edits, game operations, deployment, original EXE/DAT/save edits, or package-file replacement.

## Changes
- core/build_dat_ui_selector.ps1: require dat_ui_v4_visuals.h; ole32 remains dynamically loaded. Add actual v4 adapter, auto-arm edge, and v3 component fixtures to -Test at O0/O2, including -AutoArm runs.
- Copy v4/test_work_dat_ui_v3.c byte-for-byte to tests/test_work_dat_ui_v3.c (previously absent). Both SHA256 e654614422a022bf28987babda4dec6d9b856970082b37edf73047d57781f800. Includes refer to installed ../src headers.
- core/test_dat_ui_auto_arm_edge.c and core/test_dat_ui_v4_runtime.c: replace DeleteFileW setup/cleanup with PID+run unique CREATE_NEW logs retained for review. The user's preservation instruction takes precedence over fixture cleanup. CHECK expressions remain byte-equivalent after trimming line indentation; expectations unchanged.
- AUTO build exposed a pre-existing PowerShell single-value splat issue. Untyped $defines produced Zig "error: -: unrecognized file extension". Explicit [string[]] fixes flag forwarding. RED evidence retained; production C unchanged.

## Windows / Zig 0.14.1 results
- Initial default: WORK_BUILD_default_20261029_011322, exit 0.
- AUTO RED: WORK_BUILD_auto_20261029_012426, exit 1 before fixtures; no DLL.
- Final AUTO GREEN: WORK_BUILD_auto_20261029_014026, exit 0.
- Final default GREEN: WORK_BUILD_default_20261029_015017, exit 0.
- Each GREEN run: guard PASS; native O0/O2 PASS; v4 runtime 68/68 at O0/O2; auto-arm edge 10/10 at O0/O2; v3 components 87/87 at O0/O2. Final stderr files empty.
- auto-arm edge fixture defines AUTO internally even in default mode, deliberately exercising the opt-in logic. Default production DLL still has no AUTO flag.
- Every run JSON captures exact command, source/header hashes+mtime before/after, exit, and DLL hash. sources_unchanged=true throughout.

## Final formal artifacts (not deployed)
- Default: WORK_BUILD_default_20261029_015017_artifacts/HakushinDatUiSelector.dll, 291840 bytes; SHA256 4aa79e15dc8e7456f20f3de907668f7a75b42c6db0c3b533031c902ee950f5b5.
- AUTO: WORK_BUILD_auto_20261029_014026_artifacts/HakushinDatUiSelector.dll, 293376 bytes; SHA256 196d0544d3e1d4ba97d4545d7700b74e80914621ca33077fdd7b5e038df00645.
- Original backups: *.pre_work_build_20261029. Before/after metadata: WORK_BUILD_BEFORE_20261029.json and WORK_BUILD_AFTER_20261029.json. Review diffs: *.work_build_20261029.diff.
- Final build-script SHA256 671e678079c026e404e9a5580a56b58f4ae1d7e6c88db5350ef511a97b01294f.

These are synthetic tests of actual adapter code using private memory and test windows. They do not prove game event resumption, DirectInput isolation, fullscreen behavior, real auto-arm ordering, or crash resolution. Golden/MATCH is not increased. Runtime/game validation remains Root's responsibility.
