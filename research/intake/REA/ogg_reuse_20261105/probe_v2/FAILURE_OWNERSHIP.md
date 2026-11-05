# Open failure ownership — diagnostic v2

Research: REA-T015-OGG-REUSE-20261105. Same original EXE SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187. Native x86 examined on 2026-11-05. Static findings, not failure-path runtime tests.

| Path | Native evidence | Diagnostic policy |
|---|---|---|
| fopen fails | 5D16D9 test;5D16DD EAX=-1;5D16E4 ret; no context construction | Poison conservatively; do not issue extra clear |
| Initial header failure | 5D1584 negative branch;5D1587 datasource=0;5D158D clear | Inner heap/state cleanup performed before wrapper closes FILE |
| Seekable metadata preparation failure | 5D1689 call5D1310;5D1692 tests;5D1695 datasource=0;5D169B clear | Same ownership split |
| Unexpected state after successful initial preparation | 5D166B state comparison;5D1671 returns -131; no clear on this branch | Cannot generalize that every failure leaves empty outer |
| Wrapper receives nonzero status | 5D171C test;5D1720 push FILE;5D1721 close callback | Original FILE is closed by wrapper |
| clear's close guard | 5CFEDF tests datasource;5CFEE3 callback;5CFEEE indirect call | Zeroing datasource suppresses inner file close |

Normal initial preparation publishes state1 at5D1609; that makes the unexpected-state branch unusual, not a license to ignore it under all failures/allocators/corruption. Allocation-failure resilience and all indirect callback behavior are not certified.

Do not issue speculative extra clear after failed open. Diagnostic DLL remains poisoned and requires process exit, retaining the pre-existing conservative policy. A successful open receives exactly one clear; second diagnostic attempt is a fresh open/read/clear lifecycle, not double-clear.

## New-context probe

Two sequential lifecycles on DLL-owned aligned0x2D0 context, maximum16 reads of4096 bytes per lifecycle, signed results and format checked; full outer zero checked after clear without a manual memset between attempts. PCM byte counts, format and FNV1a fingerprints must match between attempts. FNV1a is a reproducibility signal, not a cryptographic proof of audio correctness.

Worker entry is exported stdcall thread procedure; host codec boundaries use explicit cdecl pointers. Original game path and asset path are bound in local settings to the newly supplied OGG test copy. No game execution was performed by the agent while preparing these files.

Launcher refuses other process names, mismatched architectures and an already-loaded diagnostic module. Wrapper additionally requires exact target path and game/DLL/runner/asset SHA256. DLL validates host file SHA256 and four boundary prologues. A new remote thread calls LoadLibraryW, followed by the diagnostic export; module remains loaded until game exit. These operations occur only when user runs Run-Probe.cmd.

Sixty-second launcher waits bound waiting, not native function execution time. Timeout does not kill threads, unload the module or free still-referenced remote arguments. Do not retry in the same process after a timeout. Windows UCRT/host CRT TLS interaction on the new thread is an empirical test condition, not established by normal BGM-worker observations.

Built tests passed: seven read-policy cases; host/opt-in refusal; simulated output cleanup failure/retry; six probe scenarios (bounded reads, open failure without clear, negative read with clear, bad format with clear, empty EOF, oversized return). Runner usage exit2 and non-game refusal103 verified. No original functions were executed by these tests.

Runtime next gate: user starts specified test copy normally with BGM, runs wrapper, confirms PROBE_COMPLETE and continued BGM, then exits. Decoder output playback and DAT path transfer remain separate later stages.
