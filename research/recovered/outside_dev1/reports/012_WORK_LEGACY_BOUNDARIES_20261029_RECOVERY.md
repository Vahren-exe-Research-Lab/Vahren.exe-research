# Legacy selector/hover regression recovery — 2026-10-29

Recovered the interrupted run without repeating completed cases. Scope: synthetic Windows x86 Zig 0.14.1 regression only; no source edits, deployment, game operations, elevated execution, or file deletion.

| Suite | O0 | O2 |
|---|---|---|
| native_detail | PASS, recovered | PASS, recovered |
| presentation | PASS, recovered | PASS, recovered |
| panel_custom_column | PASS, recovered | PASS, recovered |
| hover_context | PASS, recovered | PASS, recovered |
| skill_hover | PASS, recovered | PASS, recovered |
| hover_host | PASS, newly run | PASS, newly run |
| hover_dispatch | Compiled; launch blocked by Windows error 740 | Not attempted |

Total: 12/14 executed and passed, each build/run exit 0 with explicit PASS output. Do not describe this as all 14 passing. Dispatch O0 CreateProcess required elevation; no retry, renaming workaround, or elevation was performed. Dispatch O2 was not reached by the original runner. This is an execution limitation, not a failed assertion.

The original PID 14264 was absent on resume. Recovery runner PID 4536 completed exit 0 in 2.93 seconds. Tracked dependency SHA-256 and mtimes matched both the pre-pause snapshot and the recovery before/after snapshots. No dependency drift was observed.

Evidence: WORK_LEGACY_BOUNDARIES_20261029.results.json retains the original 10 completed cases; WORK_LEGACY_BOUNDARIES_20261029.recovered.json includes their saved stdout/stderr, both additional host runs, and exact missing-case states. Per-case build/run logs retain their existing names. Recovery before/after JSON records file SHA-256 and mtime_ns. The original interrupted runner remains unchanged.

A preliminary process query incorrectly expanded a nested PowerShell expression and returned command errors; it did not modify state. The subsequent direct ProcessId query successfully confirmed absence. This query error is unrelated to the test results.
