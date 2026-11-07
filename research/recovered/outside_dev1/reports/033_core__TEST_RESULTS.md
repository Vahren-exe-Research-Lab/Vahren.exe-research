# Verification — 2026-10-25

Command: `& '[USER_HOME]/Documents/迫真戦記/_REDEV_RESEARCH/data/recruit_sort_v4/core/build_test.ps1'`

Zig 0.14.1; target `x86-windows-gnu`; every compile used `-Wall -Wextra -Werror`.

Observed output:
```
PASS fixture expected=0 logs=5
PASS fixture expected=3 logs=2
PASS fixture expected=3 logs=2
PASS fixture expected=6 logs=2
PASS fixture expected=9 logs=1
PASS fixture expected=4 logs=2
PASS fixture expected=0 logs=6
ALL CORE FIXTURES PASSED
```

Before implementation, host failed at `core!=NULL` because Core did not exist (exit 1). A shutdown-retention assertion was also observed failing against the normal plugin before adding the shutdown-failure fixture variant. Final suite verifies real DLL residency and removal with GetModuleHandleW. This tests cooperative native plugins, not malicious or crashing plugins. Existing selector/game tests were outside this isolated fixture and were not run; no selector code was touched.

## Reentry regression follow-up

A host log callback now probes nested Load and Shutdown during every lifecycle log. Before the guard, the suite failed with `FAIL callback reentry must return HK_BUSY`. Export wrappers now guard the complete operation, including cleanup and FreeLibrary, and clear the guard on every normal return. The seven-case full build/test suite then passed again. Runtime module residency checks remain enabled. Header also rejects non-x86 compilation. This does not add thread synchronization or exception recovery.

## Multi-plugin lifecycle follow-up

`build_multi_test.ps1` first failed against single-module Core at the new-plugin init-failure assertion (old Core returned HK_BUSY merely because a was already loaded). After fixed-slot implementation it printed `ALL MULTI-PLUGIN TESTS PASSED`. Actual DLL event order was asserted as `init:a;init:b;stop:b:fail;stop:b;stop:a;`. Both modules remain resident after b fails shutdown; new loads are rejected until retry completes. Distinct logger addresses verify earlier API storage is not overwritten. The test also rejects duplicate IDs and the same loaded module under a different expected ID, verifies earlier-plugin survival after a new init failure, and reloads after completed shutdown. Maximum capacity is bounded in code at 32; this two-plugin integration test does not exhaust 32 actual DLL slots.

Combined multi-plugin plus existing seven Core fixtures completed with exit code 0 on 2026-10-25; final output included both `ALL MULTI-PLUGIN TESTS PASSED` and `ALL CORE FIXTURES PASSED`. Reentry probes remained enabled in all seven original cases.
