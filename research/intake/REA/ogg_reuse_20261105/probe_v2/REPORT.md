# REA-T015-OGG-REUSE-20261105 — DLL bounded decode runtime follow-up

Owner REA; 2026-11-05 JST; PUBLISHED_INTAKE / NOT_CURATED. Same research ID and Draft PR #16.

## Conclusion

The user-operated diagnostic DLL completed two sequential open → 16 reads → clear cycles using existing Vahren.exe OGG/Vorbis routines on one DLL worker. Each cycle produced 45,824 bytes, stereo 44,100 Hz signed 16-bit PCM, FNV-1a32 1439854910. Open/clear returned 0. The same caller-owned 0x2D0 outer backing was reused sequentially and was zero before/after each cycle. This is bounded runtime evidence for decoder-only reuse (design B), not product readiness.

The user confirmed the game remained operable afterward. Uninterrupted BGM during the diagnostic was not confirmed. This was the user's explicitly authorized original installation, not a certified isolated diagnostic copy.

## Evidence and provenance

[Summary](RUNTIME_SUMMARY.json): 232 events, one worker thread, final END recorded. [Parser](analyze_probe.py): preserved exact research utility; re-run during preservation and generated JSON matched the stored summary. Invoke without Python -O: `python analyze_probe.py LOCAL_LOG LOCAL_RECEIPT OUTPUT_JSON`. Inputs remain local.

[Source hash manifest](SOURCE_MANIFEST.json): all 12 diagnostic source files rehashed and matched; source contents are excluded. [Source receipts](SOURCE_RECEIPTS.tsv) records measured byte hashes. Raw log: 12,347 bytes, SHA256 `925881aa1b791fa9c113ede5d9afc859e93ca796d5c3c01b64d5b33b77846b9c`; excluded from upload. Measurement date 2026-11-05.

Target EXE SHA256 `e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187`; DLL SHA256 `400f7795e0fce63d96e4f460c52cb30a0818c48e2856c0471d77cf0695c8681a`. Source snapshot is local probe-v2 package; publication parent `c5c8fb787b5639e4d9c8b7e6428f1d099af9bb8d` preserves the earlier ABI3 receipt commit after e405a0150194aef0bf5e7be27e2e39108655137f.

## Function and ownership boundary

| VA | Prior static/native candidate ABI | Runtime scope |
| --- | --- | --- |
| 0x005D16C0 | cdecl open(path, outer 0x2D0); host FILE and internal allocations, caller backing | Two opens returning 0 |
| 0x005D0F70 | cdecl info(outer, index); borrowed info | channels=2, rate=44100 |
| 0x005D12E0 | cdecl read(outer, output, length, 0, 2, 1, section_out); signed byte result | 16 positive reads per cycle, <=4096, frame-aligned, section=0 |
| 0x005CFE00 | cdecl clear(outer); releases internals, zeros caller backing | Exactly one clear per successful open; return 0 and zero outer afterward |

Per-cycle read results: 2304,4096,4096,4096,2304,512,512,512,512,2304,4096,4096,4096,4096,4096,4096. The request ceiling 65,536 bytes is not the produced count. Equal FNV is a repeatability fingerprint, not byte-for-byte equality or reference-decoder proof.

This was not two clears on one open and not two simultaneous DLL contexts. Runtime demonstrates these calls for this input/worker only, not complete ABI certification, leak freedom, or general host CRT/TLS thread safety.

## Failure ownership remains STATIC / VERIFY

[FAILURE_OWNERSHIP.md](FAILURE_OWNERSHIP.md) is preserved unchanged as a historical pre-run static note. Its final “Runtime next gate” paragraph is superseded only by the successful bounded observation here; “test copy” is planning language, not evidence of isolation.

Header failure: 0x5D1587 datasource=0, 0x5D158D clear. Seek-preparation failure: 0x5D1695 datasource=0, 0x5D169B clear. Wrapper failure FILE close: 0x5D1721. Unusual state!=1 at 0x5D1671 returns -131 without that inner cleanup; normal preparation sets state=1 at 0x5D1609. Do not generalize all failed opens as zeroed contexts or add speculative extra clear. Failure poison remains required in the diagnostic. Neither cycle exercised failure paths.

## Prior relationship and remaining work

Earlier [design](../REPORT.md) and [ABI3 normal-BGM observation](../abi3/REPORT.md) remain historical sources under this same ID. Their “DLL-created context untested” status is narrowly superseded here. Playback and robustness limitations remain.

Actual audio output, EOF, malformed/truncated/missing input, seek/loop, volume, stop/cancellation, DAT routine dispatch, simultaneous DLL contexts, leak/handle balance and cross-session robustness are untested. Subsequent game operability is a user observation; BGM continuity is unknown. Golden / strict MATCH / READY: NOT_ESTABLISHED.

Next: bounded user-operated audio-output diagnostic with build/host checks, one worker, conservative failure ownership; record audible output and continued BGM separately. EOF and controls require separate tests. Design A still needs the existing WAV/SE PCM adapter and ownership proved; design C remains the independent decoder alternative. No production implementation approval follows from this evidence.

Curator handoff: candidate scoped runtime provenance for 0x5D16C0, 0x5D0F70, 0x5D12E0, 0x5CFE00 and outer 0x2D0. Existing owner INDEX enables ID/VA/filename discovery. Formal recovery ledger, dictionaries, REF, relations and generated search adoption remain curator work. Develop/shared dictionaries are untouched. No product source/binaries, original EXE/DAT/audio, private absolute paths or raw logs are uploaded.
