# Runtime custom columns + location integration — 2026-10-29

Root supplied frozen core/dat_ui_v3_runtime.h SHA fd1f213c06ccb82ad170e5e6821cf57ecf20ecaaa2b38c1f1d4013f9e86a0b60. This agent did not change runtime. The dedicated runtime fixture was inspected before execution: private memory / executable stubs / own transparent synthetic window only. It writes synthetic PNGs beside its own EXE (inside existing patch/v4), reserves a unique diagnostic TEMP log, and never connects to a game. No permanent deletion.

## Result

Zig 0.14.1, x86-windows-gnu, C11, -Wall -Wextra -Werror, -UNDEBUG:
- default O0: 76/76 checks PASS, build/run exit 0
- default O2: 76/76 checks PASS, build/run exit 0
- WORK_DAT_UI_AUTO_ARM O0: 76/76 checks PASS, build/run exit 0
- WORK_DAT_UI_AUTO_ARM O2: 76/76 checks PASS, build/run exit 0

All four stdout summaries also report closes=5, names=354, frees=179. The runner requires the literal PASS count marker as well as exit 0; empty output cannot pass. Captured source hashes and mtimes for runtime, fixture, plugin, lifetime, visuals, grid and reader were identical before/after.

Evidence prefix: WORK_RUNTIME_CUSTOM_LOCATION_GREEN_FLUSHED_20261029. The .results.json has exact compiler commands, exit codes, summary_present and executable hashes. .before.json/.after.json contain source metadata. Individual .build.stdout.log/.build.stderr.log and .run.stdout.log/.run.stderr.log are retained. Final runner PID 11444 exited 0.

The root's earlier RED evidence was WORK_RUNTIME_CUSTOM_LOCATION_RED_20261029_100438.run.log: two failures for missing location column/unknown text. DAT custom columns already passed in that run. GREEN verifies custom value sort maps back to the original unit and modified custom values reject commit, plus explicit unknown location fallback.

## Missing summary investigation / narrow fixture correction

Initial unmodified fixture builds/runs all returned 0 but stdout was empty; these initial records (WORK_RUNTIME_CUSTOM_LOCATION_GREEN_20261029.*) are NOT sufficient evidence of all checks passing and are superseded by FLUSHED runs.

An isolated diagnostic copy inserted stderr progress at each CHECK without changing expectations. All 76 checks and the final summary boundary were reached with fails=0. A second diagnostic added fflush(stdout): the stdout summary appeared and flush returned 0. This rules out failure to reach the summary in that diagnostic run. The precise CRT/buffering/Windows teardown cause remains unproven; no game crash or Windows GUI-specific mechanism is claimed.

Root authorized a narrow fixture change: include errno.h and explicit fflush(stdout) after existing final messages; on EOF report ferror/errno to stderr and return 2. No CHECK expectations or runtime behavior changed. Date comment records the reason.

Fixture pre-change SHA 3e42d0893d72124fb9f74650d49a02a0cdb6634c058777845c7dd7b25b9fb508, mtime_ns 1793235730190143400.
Fixture post-change SHA 843443fe1999ab8ccab112e4e201bd4720de5ff6a46148084d9885aa8d273baf, mtime_ns 1793241180261048000.
Backup test_dat_ui_v4_runtime.c.pre_flush_20261029, metadata WORK_RUNTIME_FLUSH_20261029.json. Source was read back after edit. The diagnostic copy/scripts/logs remain in patch/v4 and are not product sources.

## Boundary

SYNTHETIC coverage only. No DAT execution, original native resumption, game deployment, save changes or ACTUAL claims. Independent reviewer was informed that source is frozen and formal full-suite builds can proceed.
