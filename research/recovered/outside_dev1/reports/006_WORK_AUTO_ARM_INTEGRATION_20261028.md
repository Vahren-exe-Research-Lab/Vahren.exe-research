# Auto-arm integration checkpoint — 2026-10-28

- Owner: auto_arm_integration; source frozen for root integration/review. No game/debugger/Git/deployment operations.
- Baseline plugin mtime 1793032353209, SHA256 6e30fe0dd446e5c861fd139ffa957fe8bcc9dccb30ff2ff916e6021b11c6c187; exact match with README_APPLY §5.
- Exact hunk application (without Git) preserves mixed newlines. Patched plugin SHA256 432f033a1bf5491a0abbfbe5678d0d4867222bb654150190a19128ca5c98b83f; exact advertised result.
- Baseline native fixture mtime1793086039450, SHA2561677d537d5484c73f07674a5022ba4a3d59af1a9515424a839130fb4c8859224.
- Native fixture deviation: preserve all existing logs; use CREATE_NEW with PID plus bounded run suffix instead of DeleteFileW. Expectations unchanged; no truncation/deletion. Patched SHA2567eed2b4172f26df7965a05c8c22da3a8c6804ff8997501fb64a650d5bde19f21.
- Build script adds optional -AutoArm. Define is supplied to guard fixture, both native fixtures, and DLL. Default has no extra define. SHA256ce48ba9bfa7c6b21195412f67c7693aba29d7ecc67c618a6c6ef15f3049afac8.
- Exact production auto-arm block extracted to isolated Windows x86 test; baseline no-auto behavior RED exit1; patched GREEN O0/O2 exit0. Coverage: 30 samples and 500ms independently required, loading/scene/read resets, armed BUSY retry without duplicate accepted log, terminal states, clock rollover. Native read/clock/install dependencies are simulated; this does not prove actual title routing or live install safety.
- Stale diagnostic setup extracted unchanged from baseline/current fixture: baseline RED exit1 (old log reused); current GREEN2 O0/O2 exit0, preserving original file and fresh files across repeated invocation. First GREEN harness O2 compile failed because assertions were disabled; corrected runner with -UNDEBUG, retained STALE_GREEN.log for audit.
- Backups: base_dat_ui_selector_plugin.c, base_test_dat_ui_selector_native.c, base_build_dat_ui_selector.ps1. Evidence: RED.log, GREEN.log, STALE_RED.log, STALE_GREEN.log, STALE_GREEN2.log.
- Full build_dat_ui_selector.ps1 -Test default/AUTO intentionally not run while sibling edits shared adapter headers. Root runs after source freeze.
- ACTUAL still pending: initial title auto_arm_wait -> auto_arm_accepted -> patch_active, normal asynchronous and xp.txt synchronous load. Existing PID9080 remains untouched. No claim of crash fix or completed generic UI; Golden/MATCH unchanged.
- Minor diagnostic caveat: exact Claude patch leaves existing init_pending/manual_arm_identity messages mentioning manual-only/no-auto even in AUTO build. auto_arm_wait/accepted later identify actual route; root may revise those two messages if desired after exact-patch hash checkpoint.
