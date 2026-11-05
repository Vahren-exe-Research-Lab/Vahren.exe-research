# REA-T015-OGG-REUSE-20261105 — playback-v3 and volume-isolation correction

Owner REA; observed 2026-11-05 JST. PUBLISHED_INTAKE / NOT_CURATED. Existing Draft PR #16. Golden / strict MATCH / READY: NOT_ESTABLISHED.

## Conclusion

Existing host decoder reuse plus audible DLL output was observed. **The v3 WinMM sink fails the independent BGM/voice-volume acceptance gate; do not proceed to DAT integration with this sink.** Successful HkOggSetVolume / waveOutSetVolume return values are not evidence of independent per-voice volume.

Two sequential full decodes each produced 1,007,616 bytes / 251,904 frames of stereo 44,100 Hz signed 16-bit PCM (about 5.7121 seconds): 472 positive reads, then EOF0, clear0. Two DLL output voices were active during the scenario; volume/stop APIs returned0 and final END0 was recorded. This is concurrent output playback, not concurrent decoder contexts.

The user heard added audio, confirmed BGM continued, added audio stopped and the game remained operable, but suspected BGM became quieter. That concern remains part of the result.

## Decoder evidence

[Summary](RUNTIME_SUMMARY.json), [parser](analyze_playback.py), [source hashes](SOURCE_MANIFEST.json), [receipts](SOURCE_RECEIPTS.tsv). Parser re-run exactly reproduced the summary; all 18 local source hashes matched. Raw log: 55,821 bytes / 1,024 events, SHA256 c1fdb8c5b0df39e5f3b6ea9037db647ee8213da23be26a6ccc24bfcde9f0b21f.

Target EXE SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187; DLL SHA256 e7570b677c7f6ec6000b626825de62d62106938fcd47ac5a04c32a01288f3bf6.

Prior cdecl boundary candidates: 0x005D16C0 open(path, caller-owned outer 0x2D0), 0x005D0F70 borrowed info, 0x005D12E0 signed PCM read, 0x005CFE00 clear. This normal-input run adds EOF and actual audio output to the prefix-only probe. It does not certify every ABI/error/thread path. Host FILE/internal allocations remain host-owned; output PCM/voices are DLL-owned.

Read histogram per cycle: 512×224, 1280×1, 2304×67, 4096×180, EOF0×1. Playback positions progressed for both voice IDs. Configured loop flags and position progression are not independent evidence of audible loop-boundary correctness. No v3 PCM content hash/reference-decoder comparison.

[BUILD_RECEIPT.json](BUILD_RECEIPT.json) is preserved historical pre-run evidence; its BUILT_NOT_RUN_IN_GAME wording is superseded only for this scenario. Runtime receipt source_sha256 is the input asset digest, not an aggregate implementation-source hash; implementation identity is SOURCE_MANIFEST.json.

## Volume audit and corrected interpretation

[Sanitized summary](volume_audit/SUMMARY.json), [read-only helper](volume_audit/read_session_volume.c), [silent waveOut test](volume_audit/test_wave_volume.c).

A read-only audit after v3 found the game session master=0.0499885567, mute0, channel volumes1/1. This agrees numerically with the last DLL5% request quantized as floor(0.05×65535)=3276, then 3276/65535≈0.0499885557. Before-volume is unknown: this supports shared attenuation but does not establish an exact before/after change or exclusive causation.

In a separate silent process on the same PC, two waveOut handles initially returned FFFFFFFF. Setting the first to 0CCC0CCC made the second return 0CCC0CCC. Restoring the first saved value returned0; no subsequent GetVolume verified restored state. No audio buffer was submitted. Original game volume was not changed by this separate test. **WaveOut handle volume is not independent in this environment.**

Legacy APIs assign streams to the process-specific default session, and legacy volume calls can affect application-volume state. [Microsoft: Audio Events for Legacy Audio Applications](https://learn.microsoft.com/en-us/windows/win32/coreaudio/audio-events-for-legacy-audio-applications). Session volume/mute applies to every stream in that session. [Microsoft: Audio Sessions](https://learn.microsoft.com/en-us/windows/win32/coreaudio/audio-sessions). Consulted 2026-11-05. These support the shared-session explanation; the local two-handle test directly demonstrates the independence failure.

## DirectSound candidate: separate synthetic observation

[Silent DirectSound test](volume_audit/test_ds_volume.c) includes the read-only helper. It created its own hidden window, DSSCL_NORMAL device and two software secondary buffers with CTRLVOLUME, filled them with zero PCM, and played both looping. No primary buffer was modified.

Before: buffer volumes0/0, session master1, mute0, channels1/1. After SetVolume(-3000) on the first: buffers -3000/0, session master still1, mute/channel values unchanged. DS_RESULT0 and HRESULT0. This demonstrates independent secondary-buffer control for this separate synthetic process/environment, **not yet inside Vahren.exe**. The result supports a replacement sink candidate; it is not a validated game-integrated fix. The test return code checks buffer values, while session stability is additionally verified from the recorded audit values.

## Prior relationship and remaining work

[Original design](../REPORT.md), [ABI3](../abi3/REPORT.md), [probe-v2](../probe_v2/REPORT.md) remain historical under the same ID. Earlier audio-output/EOF-untested statements are superseded only for this normal-file v3 run. Any interpretation of successful volume calls as per-voice independence is corrected here.

Design B decoder feasibility is strengthened; replace/validate the sink before DAT work. DirectSound secondary buffers have bounded synthetic support; software PCM gain remains another design candidate. Neither is declared implemented/verified in the game by this package.

Remaining: game-integrated volume isolation with before/during/after BGM session measurements, individual voice control, malformed/missing/truncated inputs, concurrent DLL decoders, leaks/handles, cancellation races, long sessions, audible loop boundaries and DAT path/control integration. Failure poison from prior ownership research remains; successful clears do not justify extra clear after failed open.

User-authorized installed-game run, not certified isolated. Owner INDEX supplies ID/VA/filename discovery; formal ledger/REF/dictionary/relations/generated-search adoption remains curator work. Develop/shared dictionaries unchanged. Raw logs, process IDs, private absolute paths, original EXE/DAT/audio and diagnostic implementation/binaries excluded. Only standalone audit/silent-test sources are published.
