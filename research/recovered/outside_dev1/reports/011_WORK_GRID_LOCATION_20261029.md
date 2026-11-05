# Optional location column — Work 2026-10-29

Scope: source header src/work_dat_ui_grid.h and dedicated tests/build only. No runtime, game, debugger, deployment, DAT, EXE or save edits. Parent owns runtime integration.

## Interface and behavior

Append to zero-initialized WDUG_Input: location_title (const wchar_t*) and locations[WDUG_MAX_ROWS] (const wchar_t* each). NULL location_title disables the feature and ignores all location pointers. Non-NULL title must be nonempty and fit the existing 65-wide-character heading limit. NULL or empty row location displays blank. Each row is copied, allowing 271 UTF-16 code units plus NUL (WDUG_LOCATION_CAP=272). Longer input rejects creation.

The new text column follows all numeric columns; eight numeric columns remain supported. Column index is columns+1. Header clicks ascend, descend, then restore original DAT order. Equal location labels retain original source-row order. Initial sort_column=columns+1 with location enabled selects location; existing 0=DAT-order convention remains. Search includes optional location, name and ID; Japanese text and case-insensitive matching use the existing CompareStringOrdinal model.

All callbacks continue returning original source-row indexes. New subitem failure uses existing damaged/Cancel-only behavior. Added native column insertion failure aborts grid creation. Existing image ownership, deferred completion, event/native guards remain unchanged. WDUG_State grows by about 272 KiB and is still heap-allocated; WDUG_Input grows by 2 KiB in 32-bit builds.

## Evidence

Baseline SHA-256: d343cac15a7d0e8d0c3a2a93291a654f1a9e1e764a174a9a92f4e2588838cea3
After SHA-256: ba9b0259726539ed501a6140c291f01854822e659b83fe417422b1ee9e2de509
Before mtime_ns: 1793197461221267900
After mtime_ns: 1793232336564854400

Backup work_dat_ui_grid.h.pre_location_20261029 was saved before editing. WORK_GRID_LOCATION_BEFORE.json and WORK_GRID_LOCATION_AFTER.json contain path, mtime and hashes. WORK_GRID_LOCATION_20261029.diff contains the exact source delta.

Windows, Zig 0.14.1, x86-windows-gnu, -Wall -Wextra -Werror, O0/O2:
- Before change: new location behavior fixture 17/40 PASS, 23 failures, exit 1 at each optimization. This is a running RED test, not a compile error.
- After change: location fixture 40/40 PASS, exit 0 at each optimization.
- Existing failure/cancellation fixture 73/73 PASS, exit 0 at each optimization.
- Existing v3 snapshot/grid/mapping fixture 87/87 PASS, exit 0 at each optimization.
- Final combined runner PID 6968 completed exit 0. Build/run exit codes and executable SHA-256 are in WORK_GRID_LOCATION_GREEN_RESULTS.json, with per-suite stdout/stderr logs. RED_RESULTS.json similarly records baseline runs.

The dedicated tests cover empty/NULL/Japanese/271-character locations, overlength rejection, eight numeric columns plus location, sorting/filtering and source-index commit, default compatibility, and a forced location-cell update failure. Existing v3 expectations were not changed. New expected behaviors are dated in the dedicated fixture.

The first runner launch failed before compilation because Windows PowerShell misdecoded a BOM-less script containing Japanese absolute paths; the runner was corrected to derive paths from its own directory. This launch issue is not counted as the behavioral RED result.

## Limits / next action

Synthetic Win32 controls and private fixture data only; no original-game ACTUAL/Golden/MATCH claim. Root must pass fresh authoritative location strings from runtime, run full integration builds, and verify game behavior. This header is an internal source interface, not a promise of binary ABI compatibility with previously compiled WDUG_Input users. Compile all consumers against the updated header. Source frozen after the above hash.
