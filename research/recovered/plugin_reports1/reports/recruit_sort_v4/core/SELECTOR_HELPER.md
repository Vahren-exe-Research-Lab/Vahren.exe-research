# Explicit selector helper autostart

## Focused relocatability plan (2026-10-26)
1. Add a real synthetic-child fixture for explicit `./` and `.\\` settings, package
   relocation under Japanese/spaced names, and an unrelated current directory.
2. Resolve only these explicit relative settings against the validated game directory;
   preserve drive-absolute settings, pins, UTF-16 configuration and launch lifecycle.
3. Reject traversal, ambiguous separators, drive-relative/network/device paths and
   overlong paths; retain trusted-config assumptions (no reparse-point sandbox claim).
4. Run the native helper suite and record results and owned source hashes.

This section describes source behavior and fixtures. Deployment status is recorded
separately in the integration receipts; this change performs no deployment.

The adapter waits for the native installer to finish with `HSA_ACTIVE`. Its
non-UI route worker then makes at most one helper-launch attempt for this game
process. Once installation is in progress, the worker retains completion observation
even after the routing deadline, so a late ACTIVE result still launches once.
Missing/disabled configuration leaves the native plugin active and logs
`helper_disabled`. Failure never retries, changes commit policy, or shuts down
the game. No launch occurs while installation is pending/installing/failed.

Copy the disabled example to the game folder as `HakushinSelectorHelper.ini` only
when configuring this feature. In `[selector_helper]`, explicitly set `enabled=1`,
`executable` (Python), `entrypoint` (`selector_helper_entry.py`), `source_root`
(directory containing `hakushin_compat`), and the two exact SHA256 pins
`executable_sha256`/`entrypoint_sha256`. These three paths accept drive-absolute
local paths or explicit `./` and `.\` prefixes relative to the validated game
folder, independently of the current working directory. For example:
`executable=.\HakushinPlugin\helper\runtime\python.exe`,
`entrypoint=.\HakushinPlugin\helper\selector_helper_entry.py`, and
`source_root=.\HakushinPlugin\helper\src`. Use one separator style per relative
setting. Drive-absolute settings use the unchanged original path validator,
including Windows slash/backslash, dot/parent normalization and trailing directory
separator support. Bare relative, drive-relative and UNC/device settings remain
rejected. Strict component checks apply only to explicit dot-relative settings:
dot/traversal components, repeated/mixed separators, trailing separators/dots/spaces
and invalid filename characters are rejected. The resolved path and required watcher path must fit below MAX_PATH.
Invalid/missing required values fail closed. This is trusted configuration and
lexical validation, not a filesystem sandbox or protection against reparse points.
Save the INI as **UTF-16 LE with BOM** (the example already uses this encoding).
UTF-8, ANSI, and missing BOM are explicitly rejected as `helper_config_encoding_invalid`.
This preserves Japanese and characters outside the Windows system code page.
Paths below MAX_PATH only. No machine-specific paths are embedded in code.

This config is trusted opt-in: **the complete configured Python installation and
source root are trusted**, not just the two pinned files. Pins do not attest every
imported source or Python dependency. The entrypoint prepends that source root;
the child uses Python `-I` to ignore Python environment/cwd/user-site inputs.
Use the runtime where the existing display-only watcher and Pillow work.

Launch uses direct `CreateProcessW` with an explicit executable path, Windows
argument quoting, `CREATE_NO_WINDOW`, hidden startup, and no inherited handles.
No shell, injection, EXE/DAT/save edit, or selection commit occurs. The worker
holds read-only exe/entrypoint file handles until child exit, preventing their
replacement between validation and Python opening the script. This can block
updates to those two files while the game/helper is running. No hot reload.

Fixed child scope: current game PID and directory, existing display-only watcher,
`--until-game-exits`. Automatic startup has no elapsed-time expiry. The watcher
ends when its original process handle reports exit or a safety/policy stop occurs.
Diagnostic runs retain bounded `--seconds 1..3600` (direct watcher default: 300);
the two lifetime options are mutually exclusive. It is not restarted after failure. Existing per-process
history/mutex and all capture guards remain authoritative. Game termination is
observed by the watcher; the adapter never terminates the game or helper.

`HakushinSelectorPlugin.log` reports disabled/config/hash/create failures and
`helper_started`/`helper_exit`. Started or exit code zero is **not readiness**.
`HakushinSelectorHelper.log` contains the watcher output; `prewarm_ready` confirms
static preparation, and actual display still requires its display-return event
and user verification. `prewarm_failed` means no watcher began even if exit zero.

Build `build_selector_plugin.ps1 -Test`, then `test_selector_helper.ps1`, and run
`python -m unittest discover -s . -p test_selector_helper_entry.py` from this
directory. Fixtures use only a synthetic child executable; they do not require
real Python for native launch testing and never launch/attach the game.

Checkpoint 2026-10-26: launcher, adapter route integration, disabled example and
entrypoint implemented. Native helper fixture, existing adapter fixture suite,
and three entrypoint tests all passed after lock-retention changes. Independent
review and real-game verification remain pending. No deployment/game operation.
