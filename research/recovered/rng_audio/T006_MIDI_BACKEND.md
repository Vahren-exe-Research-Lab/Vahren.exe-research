# T006 DirectMusic MIDI backend evidence (2026-10-07)

## [CONFIRMED-TARGET] backend identity
- Bundled target contains the exact COM GUIDs for CLSID/IID DirectMusicPerformance8, DirectMusicLoader8, DirectMusicSegment8, plus GUID_StandardMIDIFile; `T006_MIDI_GUID_PROBE.txt` records their in-image addresses.
- Audio-manager initialization CoCreateInstance's `CLSID_DirectMusicLoader` + `IID_IDirectMusicLoader8` into manager `+0x6C`, and creates a pool of `IDirectMusicPerformance8` objects into the array at manager `+0x70`.
- The generic non-OGG/non-MP3 branch beginning at `0x4BEE7E` is therefore the MIDI/DirectMusic branch, not PCMDecoder/WINMM playback.
- `0x630028='ogg'`, `0x63002C='mp3'`, and `0x630030='a_system/reset.mid'` were read directly from the bundled EXE.

## [CONFIRMED-TARGET] load / play path
- `openAudioCore` first diverts `ogg` to OggDecoder and `mp3` to DirectShow. All other extensions/no-extension cases fall into the DirectMusic branch.
- The DirectMusic branch resolves the filename again, converts the resolved narrow string to wide text with `MultiByteToWideChar`, then invokes loader vtable `+0x38` with `CLSID_DirectMusicSegment`, `IID_IDirectMusicSegment8`, the path, and output segment pointer.
- This call shape matches `IDirectMusicLoader8::LoadObjectFromFile`; target HRESULT<0 enters `audioStopOrReset(1)` and abandons playback.
- Segment vtable `+0x18` is called with either 0 or 1000 according to the playback-repeat flag. The IDirectMusicSegment8 vtable layout identifies this slot as `SetRepeats`.
- Segment vtable `+0x4C` is invoked with `GUID_StandardMIDIFile` and zeroed parameter selectors, matching the segment `SetParam` slot.
- Playback later goes through an `IDirectMusicPerformance8` instance and segment pointer; the performance call at vtable `+0xB4` uses flags including `0x4000`, consistent with the DirectMusic segment-play path.

## [CONFIRMED-TARGET] reset / missing-file behavior
- Literal `a_system/reset.mid` is wired into a special DirectMusic reset path guarded by target global byte `0x8797CB`; it is separate from ordinary MP3/OGG transport.
- If an extensionless request has no `.mid/.mp3/.ogg` candidate, `playbackCore` leaves the original extensionless string and reaches this generic DirectMusic branch.
- The resolver then returns an empty path; DirectMusic segment loading fails and the native failure branch calls `audioStopOrReset(1)`. The script dispatcher itself does not Yield for this failure.

## [REIMPLEMENT / VERIFY]
- Strict compatibility requires a DirectMusic-compatible semantic adapter for MIDI: loader/segment/performance lifecycle, repeat count, failure reset, and reset.mid behavior must not be approximated as the MP3/OGG path.
- Dynamic golden tests should still pin audible/current-track behavior after a missing MIDI load and the precise purpose/timing of the `0x8797CB` reset.mid branch.
- Evidence: `T006_AUDIO_HELPERS.txt`, `t006_audio_helpers.py`, `T006_MIDI_GUID_PROBE.txt`, `T015_IMPORT_MAP_608F_6099.txt`.