# OGG-only test-copy migration — follow-up design, 2026-11-06

Status: ASSET_CONVERSION_VERIFIED / SUBSET_SE_SINGLE_ACCEPTED_BATTLE_PENDING.
The original DAT-path plugin's world-event playback has passed bounded runtime/user acceptance.
This separate follow-up is authorized by the user's request to convert all WAV files and play the isolated copy. Permission to delete original WAVs is present, but deletion is not useful until existing callers are routed successfully.

## Inventory

5972 WAVs, 2348958298 bytes: sound689 + voice5283.
All were readable by the standard RIFF/WAVE reader. Mono/stereo, rates8000..192000, including one40000Hz source. No source exceeds the existing16MiB decoded signed16 PCM limit.
The local converter uses FFmpeg libvorbis quality5, preserves channel/rate, checks output codec/format/duration (<=50ms tolerance), decodes each output fully with FFmpeg -xerror, and records before/after SHA256. Source WAVs remain, and existing OGGs are never overwritten.
This proves conversion/readability with FFmpeg, not successful decoding of every asset by the old native Vorbis implementation.

## Preserve original sound behavior

The tested method-B DAT plugin owns eight voices with its own controls. Replacing every original SE/voice trigger with its asynchronous Submit call would lose original duplicate pools, per-category volume, single-voice replacement and battle recency behavior unless these were all reimplemented.

Preferred next experiment: replace only the original WAV buffer factory at its three known direct CALL sites, using an explicit asset manifest, and return a compatible original-device DirectSoundBuffer8. Leave original play/stop/volume/cache ownership above the factory intact.
This is a separate method-A bridge candidate; it is not an already verified raw-PCM function in the original engine.

Known sites (preferred base400000):
- 4C046E E8 DD090000 ->4C0E50, single voice, pushes flag1/path/manager.
- 4C082F E8 1C060000 ->4C0E50, battle voice, pushes flag1/path/manager.
- 4C0B81 E8 CA020000 ->4C0E50, SE cache, pushes flag0/path/manager.
- Factory epilogue4C11DF returns interface pointer in EAX;4C11FB ret0C. Static stdcall-compatible three-stack-argument contract. Confirm all three real callers before replacing.

### New concrete native crosschecks

Original EXE SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187.
V9 database entry remains uncorrected pseudocode (its void return is already known wrong); fresh bytes were disassembled from each containing function's actual entry, not arbitrary mid-instruction addresses.
Local native excerpt SHA256 4a43f8ce81bf711a1c18697e31619f5c23d16c145ef5428ef658548813f655d8.

- 4C0E64 captures first stack arg and4C0E79 stores it to local+24.
- 4C10F9 loads that manager,4C10FD dereferences its first DWORD: original DirectSound device at manager+0.
- 4C1116 sets DSBUFFERDESC flags80 (CTRLVOLUME),4C1125 calls device vtable+0C CreateSoundBuffer.
- 4C1144 pushes GUID60971C; its bytes49a425682475824d920f50e36ab3ab1e equal IID_IDirectSoundBuffer8 in the local dsound.h. QI4C114C, base-interface Release4C1158, return the queried interface at4C11DF.
- Original SE pool duplicates through the same manager+0 device, call4C0CEF (vtable+14), then QI Buffer8 at4C0D04 and temporary Release4C0D12.
- Therefore do not hand the existing standalone plugin's separate-device buffer to this pool. Construct using the borrowed original device and transfer exactly one Buffer8 reference to the original manager.
- The bridge must not start the buffer or independently dispose a successfully returned buffer. Original callers own volume, Play and later Release. Every failure returns null and releases all DLL-created temporary interfaces/PCM.
- Use COM operations from a complete C implementation, never jump into4C1125/4C1177 with fabricated local frames.

### Path selection is a separate gate

Existing4C0960 constructs sound/name + suffix and calls00427190 before the factory. V9 function00427190 first builds a path using global prefix68B370, checks FindFirstFileA, and if missing rebuilds using fallback prefix68B38C. It returns shared scratch AC2018.
Thus simply deleting WAVs and swapping .wav to .ogg after the resolver may choose a different source root. Explicit manifest resolution must reconstruct the original search precedence using existing OGG availability, or the affected resolver callers must also be adapted. Copy scratch path before later engine calls. Do not globally hook the shared resolver without enumerating its non-audio users.
Voice preprocessing flag1 also remains relevant to unmapped/native assets. Mapped converted normal OGGs bypass that WAV preprocessing; unmapped inputs should preserve original behavior.

## Implementation gates and order

1. Preserve the accepted DAT plugin and current asset conversion receipts.
2. Observe original loader entry/returns for SE, single voice and battle voice in a fresh isolated run: manager/device/path/flag/thread, caller return, returned Buffer8 and stack preservation. No manual internal calls.
3. Prove path precedence with WAVs absent in a tiny fixture, including non-default scenario roots, Japanese names, mixed case, missing map, and duplicate basenames.
4. Extract a worker-owned decode-to-PCM operation from the tested adapter. The current HkOggPlay creates its own DS device and plays immediately, so it cannot be returned directly as a factory.
5. Implement a bounded synchronous factory request with owned path, per-request completion and explicit lifetime. Decoder work stays on its single worker. Prevent reentry/deadlock with the DAT callback/worker and shutdown; no waits in DllMain.
6. On caller thread, create/lock/copy/unlock/QI with the original device and return one stopped Buffer8. Fake-COM tests must cover two lock regions, all partial failures, QI reference balance, pool duplicate and original volume/stop.
7. Reserve only reviewed three CALL sites through existing Core patch ownership at a proven safe installation point. Determine whether any required WAVs are loaded/cached BEFORE the title-time hooks. Deleting those early assets before an effective hook could create permanent null cache entries.
8. Start with a small mapped subset and original WAVs still available; observe no double playback. Then switch the explicit manifest for all converted assets, remove the WAVs within the authorized copy, and verify source-resolution misses are zero.
9. Real tests: title/UI, campaign, battle SE bursts, conversation/selection/attack/death voices, original category volume sliders, save/load, scene transitions, repeated entry/exit. Log manifest hits/misses, decoder failures, high-water PCM, and original buffer ownership.
10. Only then describe the game as fully OGG-backed. The current accepted DAT plugin does not establish this claim.

No bridge code, live CALL patch or original-manager call has been executed in this follow-up. Formal dictionary adoption remains curator-owned.

## Completed conversion receipt

5972/5972 succeeded,0failed; output 245471643 bytes versus 2348958298 source bytes (89.55% reduction). Every output passed format/duration and full FFmpeg decode checks. Manifest SHA256 d813381ab9df283715454df8fb40136fb2878bcb526162b89a1652145d2d94ef; converter SHA256 1dd6ddcddaeb790ff577b83ad38cb92a0f9bdad69eb04896c598762f0ea6ed4f. Original source WAVs remain pending bridge integration. No assertion that the game uses these outputs yet.
V9 source database SHA256 freshly checked:2629cb2f03ecec9927e89892c77f847e4cdba381ab718825c1ca8cfeeef00ede.

## Partial loader observation and debugger correction (2026-11-06)

User stopped the observation before combat because x32dbg repeatedly paused. This is a partial run, not a successful battle/voice trial. Raw local log SHA256 c7883fb34374d43bad2d39e4eb1d31092afada94f06088388cb38cb9cad4faea (6583 bytes); raw logs and user-specific paths are not uploaded.

At module base600000, thread8868, the SE factory CALL/RETURN pair (RVA C0B81/C0B86) was observed twice, for cursor8.wav and decide1.wav:
- manager ABE3A0, manager+0 device1B40848, flag0.
- ESP10FF590 before CALL ->10FF59C after return: +0C, supporting three callee-cleaned stack arguments.
- EBP ABE3A0 / EBX0 / ESI CC2019 / EDI10 unchanged across both calls.
- Non-null EAX17B6E880 and17B9D830 respectively; both first DWORDs67671568.
These are run-specific addresses. The pointer/vtable observations alone do not prove the COM IID; Buffer8 identification remains supported by the separate static QI GUID evidence above. The two SE observations do not establish all voice-path ABI, concurrency, ownership or shutdown behavior.

Explicit pause records repeatedly identify E06D7363 CPP_EH_EXCEPTION, first chance. Some exception metadata references UIAutomationCore. This identifies the immediate debugger pause trigger, not the ultimate exception cause or a game crash. Older OGGPROBE FILL_RETURN/SE_ENTRY probes were also active. Their log-only breakpoint hit notifications must not be counted as proof of debugger pauses. The v1 log ends after one breakpoint deletion, without END or LogRedirectStop; complete cleanup is not established.

Revised local observation scripts (v2, NOT runtime-verified):
- Disable only the five known old OGG probes at RVAs C0050/C01A0/101FE8/1023E0/1CFE00, retaining their definitions.
- User creates the E06D7363 first-chance exception breakpoint once from the command bar, outside the script, to avoid duplicate-creation aborting script execution.
- Set its break condition to ex.firstchance()==0 and fast resume1. First-chance notifications pass to the debuggee; unhandled/second-chance notifications and unrelated exception codes retain stopping behavior.
- Keep six WAV probes log-only, fast resume0, silent1, maximum32 logs per site.
- Stop script ensures each software probe exists before deleting it, closes the capture before deleting the temporary exception breakpoint. Therefore a missing exception breakpoint on repeated cleanup cannot leave the log redirect open.
- Start SHA256 f4445241684a521520b751f39155fa75edacfb35cb40a0f90e158153eefa7d49; stop SHA256 e8d963b928fca8edb257abdad5c2ad2dfdabae5b474d8702020f362d9eae9ec5.
- No bridge implementation, WAV deletion or forced internal call was performed. SINGLE/BATTLE observations remain pending.

Debugger behavior references: [exception breakpoint scope](https://help.x64dbg.com/en/latest/commands/breakpoint-control/SetExceptionBPX.html), [condition](https://help.x64dbg.com/en/latest/commands/conditional-breakpoint-control/SetExceptionBreakpointCondition.html), [fast resume](https://help.x64dbg.com/en/latest/commands/conditional-breakpoint-control/SetExceptionBreakpointFastResume.html). Pass-through behavior additionally crosschecked against current upstream debugger.cpp: default DBG_EXCEPTION_NOT_HANDLED in cbDebugEvent and early false-condition fast-resume return in cbGenericBreakpoint, without continuation-status override. Actual installed-version behavior still requires the next user run.


## v2 runtime observation: SE and battle factory contract (2026-11-06)

Status: SE_AND_BATTLE_FACTORY_ABI_OBSERVED / SINGLE_RUNTIME_PENDING / BRIDGE_NOT_IMPLEMENTED.

The user completed another normal-play diagnostic. The saved capture contains 32 SE CALL/RETURN pairs and 32 BATTLE CALL/RETURN pairs (the configured per-site cap); no SINGLE pairs. This validates the original WAV factory behavior, not playback of converted OGG assets through the proposed bridge.

Evidence: local wav-bridge-v2.log SHA256 e98133b282c696c31862808681bd2d84a02429e1c6bae764c8719912c2a5e667, 2188136 bytes, 40329 lines. Original EXE SHA256 was checked again and remains e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187. Raw logs, screenshots, original assets and private machine paths are not uploaded.

### Observed contract

| Property | SE (32 pairs) | Battle (32 pairs) |
|---|---|---|
| Factory CALL / return RVA | C0B81 / C0B86 | C082F / C0834 |
| Captured thread ID | 604 | 604 |
| manager | ABE3A0 | ABE3A0 |
| manager+0 device | 035B0848 | 035B0848 |
| third stack argument | 0 | 1 |
| ESP after minus before CALL | +0C in all32 | +0C in all32 |
| EBX, EBP, ESI, EDI | preserved in all32 | preserved in all32 |
| EAX non-null | 31 | 32 |
| first DWORD of non-null result | 65B01568 | 65B01568 |

Addresses other than RVAs are run-specific. User's x32dbg screenshot labels main thread1540 decimal (=604 hex), matching all observed factory calls. This does not establish thread safety for arbitrary DLL callers. Combined with the static three stack arguments and ret0C, observations support the stdcall-compatible factory adapter; they do not permit reusing an unrelated decoder ABI.

One SE call at capture lines954/956 requests a_default/sound/none.wav and returns EAX0, with the same +0C stack cleanup and preserved registers. Both none.wav and none.ogg are absent in the diagnostic copy at inspection. Preserve the factory's null-result behavior; do not fabricate an audio buffer or treat every missing map entry as a decoder fault. This evidence does not establish a special built-in meaning for the string 'none'.

The log includes battle voice paths with advance/join/dead names. Names alone are not a full classification of user-visible behavior. No fresh user audibility/volume acceptance claim is inferred from these pointer observations. Existing accepted DAT playback evidence remains separate.

### Debugger and capture limits

No old OGGPROBE records or E06D7363 notifications appear in this capture. One explicit debugger pause follows the manual pause message near the end. Fast resume suppresses exception reporting, so absence of those notifications does NOT prove no handled C++ exceptions occurred. Other researchers' NAME2UNIT/SETTLE probes remain present and were not changed.

The saved file does not contain END. After cleanup was requested, the user supplied a screenshot of stop script line17 failing because the E06D7363 exception breakpoint no longer exists. This is after the script's log-close command; it is not a game/decoder error. Do not require another combat run or infer missing observations from this repeated-cleanup error. Durable log END and complete cleanup are not independently proved by the captured file; absence of the temporary exception breakpoint is directly shown in the UI evidence. Future capture tooling should use a separate durable cleanup receipt rather than rely exclusively on a log line immediately before closing redirection.

### Additional static work and correction

Correction to the earlier path-selection paragraph: the resolver is **00427190**, not the mistyped **04C27190**. V9 entry0x00427190 contains the two-prefix FindFirstFileA logic, and the pseudocode for004C0960 calls FUN_00427190. Prefix addresses68B370/68B38C and scratch AC2018 are unchanged. This is a report correction, not a formal dictionary update.

SINGLE runtime remains unobserved, but its next investigation targets are narrowed:
- native CALL00434D8D ->004C01A0 (containing function00434CC0);
- native CALL004A1BD0 ->004C01A0 (VM dispatcher004A1250; V9 places the call in case0x4B with a volume/global-enable gate; command identity still requires corroboration);
- native CALL00578737 ->004C01A0 (containing function00578370; V9 shows flag1 and a separate volume/global-enable gate).
These direct CALL bytes, the three factory CALLs and ret0C were rechecked against the exact EXE. Local native excerpt SHA256 c9c073fbeed6e35108a58dbbd8fdc54734d219be99af0eb698b712863ae89d2f.

V9 for004C01A0 shows the single-slot behavior: stop/release old manager+34 buffer, clear slot; create through004C0E50 with flag1; if non-null, set volume and Play, then store interface at manager+34 and volume at manager+38. This is static supporting evidence, not a completed SINGLE runtime trial.

### Effect on implementation plan

SE and battle observation gates are now satisfied for the bounded captured paths, including a native null-result case. Keep the same factory signature candidate, borrowed original device, and one stopped Buffer8 reference transferred to the original caller. Keep Play/volume/later Release with the original caller. Do not replace the existing eight-voice DAT API with this synchronous factory interface.

Before all-WAV removal: resolve scenario-root precedence with absent WAVs; confirm installation before relevant cache fills; implement bounded worker decode requests and cancellation/ownership; validate returned original-device buffers and failure paths; then test the currently unobserved SINGLE route. No bridge code or live patch was installed by this observation.


## Implemented bridge candidate and isolated subset installation (2026-11-06)

Status: BRIDGE_CANDIDATE_BUILT_AND_INSTALLED / REAL_GAME_RUNTIME_PENDING.
Historical observation sections above describe the earlier, unimplemented state.

Source: HakushinExtensions worktree branch feat/ogg-audio-20261105, local commit c78b09647579bcd1aae7440f2c7caed8de811174 (product branch not pushed).
Built/installed DLL SHA256 9c8b87c31fa168850869a704232edb5888ffbf9d71f00a321075de1f06e28225.
Initial explicit map:63 unique keys from prior observed SE/BATTLE paths plus the SINGLE test voice; SHA256 34599cd8ff6b636aa03bcbfbffb4ba7c417144a3d210d884aaea03e4406d95b1,4396 bytes,ACP932. Full5972-entry map is prepared separately (SHA256 bcaae783842326bef6aa4365cf95674c25e2c16cd1cbfdbb2d81220ff9d55ca1); not selected.
All original WAVs remain. Six installed files were backed up and read-back hash verified. No game was launched by the agent, and no bridge audibility acceptance is claimed.

### New static evidence: SINGLE trigger and earliest installation

The existing DAT command is vc: native004A1190 loads the string at006317E8,004A11A5 assigns opcode0x4B,004A11B9 inserts it. Dispatcher CALL004A1BD0 reaches004C01A0. A normal authored vc(small3/sp_go) event was prepared; no manual native-function call is needed.

The proxy's DirectInput8Create calls HK_StartupTry -> Core_Load -> plugin_init before forwarding to the real DirectInput factory. Native chain00555AD0 ->004B78C0 ->004B9E50 ->004EE0C0 ->004BCDD0 reaches this bootstrap. In004B78C0, input construction precedes CALL004B7D08 ->004BF930, which creates the original sound device. Thus synchronous plugin_init patch installation can precede all device-dependent factory calls.

- Main HWND: preferred008797FC/RVA4797FC; CreateWindowExA call005557D8, store005557E0, before call00555918 to loader coordinator00555CD0.
- Loading flag: DWORD at0087983C/RVA47983C; store1 at00555D69, clear at00555E15 after loader join.
- Original sound manager:008BE3A0/RVA4BE3A0, zero-filled image tail before initialization; device at+0.
- The loader normally runs in a created worker thread, with an inline alternative. Initialization thread MUST NOT be required to equal UI thread.
- Production gate: exact host identity already accepted; loading==1; device==0; original HWND has current-process owner. Capture its UI thread separately. Refuse late activation; do not use the EXP plugin's later title/message-hook route.
- Additional scoped SE resolver CALL:004C09F1 bytes E8 9A 67 F6 FF ->00427190, cdecl; caller cleans stack at004C09F8. Only this site is patched, not the shared resolver globally.

These are static ordering/ABI findings. Actual runtime installation at that point is the next trial's first gate.

### Implemented interfaces and ownership

- hakushin_ogg_backend.h: HkOggDecodePcmCancel(path,live_bytes,out,cancel) returns owned CAP-sized HKO_PCM without creating an audio device or playing. HkOggFreePcm releases it. Native open/info/read/clear remain worker-only.
- hakushin_ogg_factory.h: hko_make_original_buffer borrows original IDirectSound, creates CTRLVOLUME secondary buffer, copies both Lock ranges, Unlocks, queries Buffer8, releases temporary base reference and transfers one stopped Buffer8. Original callers retain volume/Play/duplicate/later Release.
- hakushin_ogg_manifest.h: owned bounded ACP TSV,8192-entry limit, Unicode-aware case/separator comparison (CP932 trail bytes preserved), explicit source/target mapping. Scenario-root selection precedes fallback even without WAVs. Existing primary WAV is a precedence barrier; it does not authorize silent playback fallback for an explicitly mapped missing OGG.
- hakushin_ogg_request.h: one owned queued/inflight request, copied path, completion event, producer/worker references, bounded5000ms wait and cancellation. Timeouts retain worker-owned state until completion; no caller stack pointers survive.
- hakushin_ogg_bridge.h: three stdcall-compatible factories plus scoped cdecl resolver; UI-thread mapped playback, original fallback for unmapped/unsupported-thread paths. Worker prioritizes bridge requests and defers new DAT commands through the entire caller PCM-free/buffer-transfer interval.
- Transient memory remains bounded by16MiB per decoded clip and64MiB including existing DAT buffers plus staging/new copy. Transferred original-manager caches are owned by the original engine and are not covered by the DAT eight-voice budget.
- Optional [bridge] enabled=1; immutable HakushinOgg.manifest.tsv. Existing routine(hk_ogg_v1) API remains independent.
- Four managed Core CALL patches install with exact expected bytes; rollback retains ownership if incomplete. Active bridge is process-lifetime; hot shutdown returns HK_BUSY rather than unpatching from an arbitrary thread.

### Verification and fixes

All11 OGG test programs passed at O0 and O2, plus actual Core disabled/wrong-host tests. New tests exercise native-decode substitutes and cleanup, real DirectSound stopped-buffer readback/duplication after original release, split Lock failure ownership, manifest selection, request timeout/producer races, four-site rollback, early loader-thread gate, non-UI fallback, restore failure and HKCP_RECOVER retention. Seven manifest-generator Python tests pass; all5972 generated map entries loaded and resolved with the native C parser. Launcher syntax and isolated mock-launch tests pass; they did not start the real game.

Independent review corrections were demonstrated failing before fixes:
1. RECOVER retention sentinel -1 must not enable adapters; mapped execution requires active==1.
2. Once recognized as mapped, unavailable-worker and reentrant/busy calls return null with error logs. They must not pass an already selected OGG to the original WAV parser or silently replay the old WAV.

The broader existing Python discovery had16 errors from missing tools/claude_lecture_v4.dat in unrelated installer/package/profile tests; exact test identifiers are preserved locally. This fixture was not added or altered.

### Next user trial

A separate launcher checks EXE/DLL/map hashes, archives previous OGG/loader logs, starts the game normally and collects fresh logs plus exit receipt after normal exit. The authored one-shot world event uses vc for SINGLE coverage. User checks short battle, BGM, effects/voices and category volume. No x32dbg, screenshots or repeated breakpoints are required.

Pending: observed BRIDGE_ACTIVE=4 before relevant sound creation; native decode of actual subset assets; SINGLE/BATTLE/SE result0 and user audibility; original category volume/cache/duplicate behavior; no regression in BGM/game operation. Only after subset acceptance should the full map and WAV-removal phase proceed. Formal function-dictionary adoption remains curator-owned.


## First subset runtime: SE + SINGLE accepted, battle pending (2026-11-06 JST)

Status: SUBSET_SE_SINGLE_RUNTIME_ACCEPTED / BATTLE_RUNTIME_PENDING.

User completed a normal launcher run from02:22:02 to02:22:42 JST, PID40604, exit code0. They explicitly confirmed the test voice was audible and BGM/effects/game operation had no problem; they had NOT entered a battle. This is bounded acceptance of the exercised paths, not acceptance of all63 mapped clips or all5972 converted assets.

Identity: product source c78b09647579bcd1aae7440f2c7caed8de811174; DLL9c8b87c31fa168850869a704232edb5888ffbf9d71f00a321075de1f06e28225;63-entry map34599cd8ff6b636aa03bcbfbffb4ba7c417144a3d210d884aaea03e4406d95b1. Fresh OGG log SHA2566eac1cd32a5a3d6984b1a3d03013c7babd9fbd11a18c1f14af4a32a26407ecf5,4499 bytes,86 lines; loader log ab09735865300776213836274949ed7a4c78c2eb6b0abf66d2db8843289ca3ed. Launcher collected both without missing logs or collection errors. Private paths/raw logs remain local.

- Four BRIDGE_PATCH_RESULT=0, then BRIDGE_ACTIVE=4 before first mapped call: early integration succeeded in this run.
- Six mapped SE calls (route3), one mapped SINGLE call (route1); zero battle calls (route2).
- All seven native opens returned0, reached EOF and cleared once with return0.
- All seven bridge buffer results returned0; total decoded PCM366354 bytes. Formats observed: mono22050/44100 and stereo44100.
- Patch installation thread42584, decoder thread31248, factory caller thread36716 (decimal runtime IDs). This concretely confirms the design's separate initialization/decoder/game-thread roles; an init-thread-equals-UI gate would have been wrong.
- Six coarse elapsed tick readings were0ms and one16ms. These GetTickCount observations do not prove zero decode latency or establish load-test performance.
- One original SE fallback (BRIDGE_NATIVE route3) occurred. Its filename is not logged, so do not identify it as none.wav without evidence.
- No mapped error/poison events. Process exit0 does not independently prove every original cached buffer's Release path; active patch lifetime remains process-scoped.

Next trial uses the unchanged DLL, map, event and launcher. User was instructed to enter one battle, issue movement/attack commands, check battle voices/effects/BGM and category-volume behavior, then exit normally. Full map/WAV removal remains gated on the battle trial. No new game mutation or rebuild was needed for this continuation.
