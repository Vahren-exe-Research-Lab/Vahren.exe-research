# HakushinOgg — DAT OGG playback candidate

Status: implemented candidate; real DAT-to-plugin acceptance remains pending.
Product base: HakushinExtensions f5f89aaaf82ba9a46ea2d4f2cf17b30a482e5d4e.
Research: REA-T015-OGG-REUSE-20261105, knowledge-base c366e743e5a0571cba4266dedf5621ec5884ca84.
The earlier playback-v4 diagnostic proved the native decoder + separate DirectSound route in the original process. It did not test this Core plugin or its DAT adapter.
The user subsequently restored their usual Windows game volume; the reported low startup volume is no longer an open blocker.

## Architecture

```text
DAT routine(hk_ogg_v1)
 -> existing selector routine bus (original routine still executes)
 -> receive: validate VM/thread, copy bounded numeric/path values, return handle
 -> fixed owned FIFO (32)
 -> dedicated audio worker
 -> source path/file guard
 -> original open -> info -> read until EOF -> clear
 -> DLL-owned DirectSound secondary buffer (up to 8 voices)
 -> poll / volume / stop / natural completion
```

No decode in DllMain or DAT callback. No VM pointers survive the callback.
This is method B: original decoder, DLL-owned output and lifetime.
Method A still requires the original WAV manager/ownership ABI and a PCM insertion route; it is not used.
Method C (independent decoder) is a fallback for other EXE versions or unresolved native decoder behavior.

## Native boundary

Only SHA256 `e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187` is accepted.
RVA is relative to the actual loaded module, not an assumed fixed base.

| Operation | RVA / preferred VA | x86 cdecl contract |
|---|---|---|
| open | 1D16C0 / 005D16C0 | int(const char *ACP_path, void *outer) |
| info | 1D0F70 / 005D0F70 | const int *(void *outer, int link), link=-1 |
| read | 1D12E0 / 005D12E0 | int(void *, char *, int capacity, int bigendian, int word, int signed, int *section) |
| clear | 1CFE00 / 005CFE00 | int(void *outer) |

The DLL owns a zeroed, 16-byte aligned 0x2D0 outer context; host allocations/FILE are released only through host clear after a successful open. Failed open poisons the service: cleanup is not guessed, and restart is required. Successful open is cleared exactly once, including decode failure/cancellation. Negative decode returns, format changes, invalid counts and partial frames are rejected. Format: signed 16-bit little-endian PCM, 1–2 channels, 8000–192000 Hz. info[1]=channels, info[2]=rate. read flags=0,2,1.

All native/DirectSound operations run serially on one DLL worker; the original BGM can run concurrently as in the earlier diagnostic. Broader concurrency, malformed-stream and device-loss coverage remain incomplete.
Internal header/init helpers 005D44C0/005D57C0/005D5BD0 are not public entry points and are never called directly here.

DirectSound uses its own hidden window, DSSCL_NORMAL, secondary buffers with per-buffer volume. The DLL never sets primary/session/WinMM volume. Volume is 0–100 percent amplitude mapped to DirectSound attenuation. Stop releases only the selected owned buffer. Loop repeats the whole decoded PCM; gapless Vorbis metadata loops are not implemented.

## DAT contract

Install the authored `dat/HakushinOgg_v1.dat` into the game's script directory. The selector routine bus must already be active. Subscription alone does not prove producer installation.
Example (literal-path parser acceptance is part of the pending game test):

```text
routine(hk_ogg_setup)
setv(@hk_ogg_path,a_default/voice/line.ogg)
set(hk_ogg_volume,40)
set(hk_ogg_loop,0)
routine(hk_ogg_play)
set(my_voice,hk_ogg_voice)
// Later, in another event:
set(hk_ogg_voice,my_voice)
routine(hk_ogg_poll)
// Or routine(hk_ogg_stop), routine(hk_ogg_volume), routine(hk_ogg_stop_all).
```

Do not spin waiting in DAT. Poll in a later event/frame after the worker can run.
The wrappers reset result=-103 before notification so a missing bus cannot look like an earlier success.
The path array must have exactly one element, max 1023 bytes in the game ACP, no embedded NUL.
The main VM must be base+4BE2F0 with the checked evaluator relation at +504.
Numeric map +4C4 and string-array map +1E8B40 follow the existing EXP implementation; MSVC strings use size+16/capacity+20, inline capacity<16, and array elements stride28.

| Variable | Meaning |
|---|---|
| hk_ogg_op | 1 play, 2 stop, 3 volume, 4 stop-all, 5 poll |
| hk_ogg_voice | positive handle returned for play; input for controls/poll |
| hk_ogg_volume | 0–100, per added voice |
| hk_ogg_loop | 0 or 1, at play time |
| hk_ogg_result | immediate request result; zero means accepted, not audible |
| hk_ogg_state | 1 queued, 2 playing, 3 ended, 4 stopped, 5 failed |
| hk_ogg_error | asynchronous backend error |

Handles are monotonically allocated positive 31-bit IDs, never reused in a process. Terminal slots may be reused; a previous handle then returns -102.
Multiple calls copy their paths immediately; changing DAT variables afterward cannot change an already queued command.
Controls are FIFO, including stop-all. Stopping during a decode waits for that bounded decode; it is not a preemptive voice cancellation.
Game exit is the supported DLL update/unload boundary. A clean Core shutdown first rejects new work, wakes/cancels and joins the worker, then unsubscribes/closes handles. Failed rollback retains the Core-owned subscription and pinned module, rather than unloading executing code.

## Bounds and errors

- 8 voice slots, 32 commands, source file <=16 MiB, decoded PCM <=16 MiB per voice.
- Maximum 64 MiB counted PCM allocations, including the temporary 16 MiB staging allocation and the new DirectSound copy during transfer. This is not a total process/codec/driver memory limit.
- Relative local-drive paths confined to the canonical game root; rejects parent traversal, absolute/UNC/device paths, ADS, unsafe components and lossy ACP conversion. A read handle remains open through host decoding to exclude ordinary writers/deletion.
- Full-file decode before playback; short effects/voices are intended. No streaming/cache, automatic WAV substitution, or resampling.
- -100 invalid argument, -101 capacity, -102 stale ID, -103 not ready/no callback, -104 path/source rejection, -105 VM shape, -106 transient lock busy.
- Backend: -10 not initialized, -11 wrong thread, -12 argument/resource, -13 host identity, -14 opt-in, -15 failed open (restart), -16 format, -17 memory/PCM cap, -18 decode, -19 DirectSound, -20 native voice cap, -21 poisoned/cleanup (restart), -22 shutdown cancellation.
- Trusted game assets only. The old native decoder is not a security boundary for hostile OGG data. A native call that never returns cannot be interrupted safely; no forced thread termination is attempted.
- Device loss is reported. Automatic device recovery is not implemented.

## Build and verification

Run `core/build_ogg_plugin.ps1 -Zig <zig-0.14.1.exe> -Test`.
Build: x86-windows-gnu, C11, warnings-as-errors. Output is ignored by Git.
O0/O2 tests cover queue/backpressure/handle reuse; SSO/heap path copies; malformed DAT; callback-to-worker with a fake decoder; shutdown admission; natural completion ownership; PCM budget; Japanese paths and writer/delete exclusion.
A silent real DirectSound test uses synthesized zero PCM and fake host functions, never original engine calls.
An actual Core fixture checks disabled load/shutdown and enabled wrong-host rejection/rollback.
Independent review found lifecycle, duplicate-reaping, failure-reply and peak-memory bugs; regression tests reproduced them before fixes.

Still pending: actual game DAT parse and notification at world/battle entries; repeated scenario changes; long sessions; simultaneous battle producers; outside-root junction fixture; actual device-loss recovery behavior. Earlier v4 audio evidence must not be reported as these tests passing.

## Candidate installation and acceptance

`tools/install_ogg_candidate.ps1` requires an explicit game root and test OGG relative path. It checks the exact EXE SHA, refuses a running Vahren, verifies existing plugin manifest hashes, adds a dependent hakushin.ogg row, and backs up each affected file locally. It leaves the common loader and other plugin binaries unchanged.
The optional test hook is only in the authorized diagnostic copy: world event wev1 calls the authored acceptance event once per fresh game. No game assets or modified original DAT are committed.
Start a fresh 動乱 scenario and choose a faction. Follow the five text prompts: one loop, two loops, volume, individual stop, stop-all. Each poll should show state2 during play and state4 after stop, with result/error0. Confirm original BGM and normal game operation; close normally.
Logs: game-root HakushinOgg.log plus loader/selector logs. Do not upload raw personal paths/game content. The restore tool verifies installed hashes before restoring backups.