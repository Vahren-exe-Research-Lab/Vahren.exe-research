# REA-T015-OGG-REUSE-20261105 — Core plugin candidate, 2026-11-06

Status: OWNER_INTAKE / NOT_CURATED / PRODUCT_CANDIDATE / DAT_RUNTIME_PENDING.
Continuation of the existing study, not a new native-function verification count.
Predecessor evidence: KB c366e743e5a0571cba4266dedf5621ec5884ca84, playback_v4/REPORT.md.

## New evidence and correction

The user restored the usual Windows game volume and reported it is now fine. This supersedes only the prior “restoration unconfirmed” status. It is not a new instrumented volume measurement.
The user authorized DLL construction after the diagnostic, then requested eventual conversion of all WAV assets in the isolated OGG test copy for play testing. Bulk conversion has NOT been performed. Conversion alone will not redirect the original WAV loaders; SE/voice call-site integration remains a separate follow-up.

The existing loader source was verified in ButaMonky/HakushinExtensions, main/base f5f89aaaf82ba9a46ea2d4f2cf17b30a482e5d4e. A separate managed worktree/branch feat/ogg-audio-20261105 contains local source commit **92c832e64c1da213c4872bcafad3550b758588d4**. Product source is committed locally, NOT asserted published to GitHub.
Built x86 HakushinOgg.dll SHA256 **da159ae750ad9010acc0a5153c0de7fba825d3290f4262d5c73710fce33a0164**. No binary is included in this knowledge-base intake.

## Concrete design

Method B selected: original open/info/read/clear + DLL-owned DirectSound secondary buffers.
- Original EXE SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187, disk hash + loaded PE32/prologue guards.
- cdecl open RVA1D16C0, info RVA1D0F70, read RVA1D12E0, clear RVA1CFE00.
- DLL owns zeroed 16-byte aligned outer0x2D0. Successful open -> clear exactly once. Failed open is poison/restart, no guessed clear.
- One dedicated worker serializes native calls. Whole-file PCM16LE, 1–2ch, 8–192kHz; original BGM remains independent.
- DirectSound secondary-only volume/stop. No primary/session/waveOut volume mutation.
- Core ABI1 Query/init/shutdown, own HK_EventsV1 subscription. Existing selector emits routine(hk_ogg_v1), then original dispatcher proceeds.
- Callback verifies known VM base+4BE2F0 and evaluator relation, bounded-copies numeric map +4C4 and one-element string array +1E8B40. No VM pointer is queued.
- DAT @hk_ogg_path carries the relative path; routine itself remains a notification, not a new arbitrary-argument API.
- Commands play/stop/volume/stop-all/poll; accepted handle is positive and never reused within a process. result0 means accepted; asynchronous state/error must be polled.
- 8 voices, FIFO32, 1023-byte ACP path, source16MiB, PCM16MiB per voice,64MiB counted PCM including staging/transfer duplication.
- Canonical root confinement, lossless ACP conversion, read handle held throughout native decode; trusted local assets.
- Module pins at initialization; worker joins before subscription removal. No forced termination or hot unloading.

## Implementation files at product commit

core/hakushin_ogg_plugin.c/.h/.def; core/hakushin_ogg_logic.h; core/hakushin_ogg_dat.h; core/hakushin_ogg_backend.h; core/hakushin_ogg_decode.h; core/hakushin_ogg_ds.h; core/hakushin_ogg_path.h; core/build_ogg_plugin.ps1.
Authored DAT library and acceptance event: dat/HakushinOgg_v1.dat, dat/HakushinOgg_acceptance.dat.
Documentation: docs/OGG_PLUGIN.md, docs/OGG_PLUGIN_PLAN.md.
Install/restore/logging launcher: tools/install_ogg_candidate.ps1, tools/restore_ogg_candidate.ps1, tools/run_ogg_candidate.ps1.
The design document snapshot is preserved beside this report.

## Independent review findings reproduced and fixed

1. Core does not call plugin shutdown after failed init. Explicit rollback now retains its owned subscription until worker join, then unsubscribes/closes.
2. Native backend's implicit reaping could invalidate a still-owned logical handle. Logical worker is sole completion/release owner; absent buffer completion is idempotent.
3. Poison exit could admit work after queue drain. STOPPING is now published under the queue lock before draining.
4. Invalid DAT snapshot could retain previous result0. Failure writes error -105 when reply cells are available; authored wrappers set sentinel -103 before notifying.
5. PCM budgeting omitted simultaneous staging/new DirectSound copies. Budget includes both, with overflow-safe checks; buffer bytes counted as soon as allocation succeeds.

The failing regression tests were observed before fixes. Six suites pass in O0 and O2 with warnings-as-errors:
- queue limits, stale handles and validation;
- synthetic MSVC string/array/number layout and owned path copy;
- relative paths, Japanese ACP path, ordinary writer/deletion exclusion;
- actual consumer/worker with fake backend and fake VM, no original decoder;
- failure replies, absent-buffer completion and poison admission;
- silent actual DirectSound with synthesized zero PCM/fake host ABI, natural-end ownership and peak PCM budget.
Actual Core fixture additionally passes disabled load/shutdown and enabled WRONG-HOST init rejection with final CLOSED/unsubscribed/queue0. This is not a real-game decoder invocation.

## Installation and pending acceptance

Final candidate installed ONLY in the user-authorized isolated OGG test game. Manifest hashes and original backup hashes verified. Restore tool was executed successfully and final candidate reinstalled. Original loader/other plugin binaries, original EXE and original audio are unchanged.
A local-only hook at event wev1 calls the authored acceptance event once per new game. The supplied launcher starts a new ordinary game session and collects logs on normal exit. The agent has NOT launched the original game for this product candidate.
Test requests: start a fresh 動乱 scenario, select faction, observe one loop/two loops/per-voice volume/one stop/stop-all, poll state2 then state4 with errors0, BGM continuity and later game operation.

Remaining: actual DAT path literal parsing and bus delivery, world/battle producer coverage, repeated scenario transitions, malformed assets, long sessions, device loss, broader concurrency, allocator leak balance, and transparent coverage of all original WAV sound/voice calls. Synthetic PASS and earlier playback-v4 evidence must not be promoted to product acceptance.
No research dictionary/develop edit; formal ABI/function adoption remains curator-owned. No original EXE/DAT/audio, raw personal logs or local absolute paths uploaded.
