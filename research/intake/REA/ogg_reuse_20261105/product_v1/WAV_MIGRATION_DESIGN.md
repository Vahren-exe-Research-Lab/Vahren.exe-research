# OGG-only test-copy migration — follow-up design, 2026-11-06

Status: ASSET_CONVERSION_VERIFIED / BRIDGE_NOT_IMPLEMENTED.
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

Existing4C0960 constructs sound/name + suffix and calls4C27190 before the factory. V9 function4C27190 first builds a path using global prefix68B370, checks FindFirstFileA, and if missing rebuilds using fallback prefix68B38C. It returns shared scratch AC2018.
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