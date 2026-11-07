# T006 Audio backend / EOF evidence (2026-10-07)

[CONFIRMED-TARGET] MP3 backend
- openAudioCore MP3 branch creates CLSID_FilterGraph and queries IGraphBuilder / IMediaControl / IMediaSeeking / IMediaEvent / IBasicAudio.
- GUIDs resolved from target: FilterGraph e436ebb3-524f-11ce-9f53-0020af0ba770; IMediaControl 56a868b1-0ad4-11ce-b03a-0020af0ba770; IMediaEvent 56a868b6-0ad4-11ce-b03a-0020af0ba770; IBasicAudio 56a868b3-0ad4-11ce-b03a-0020af0ba770; IMediaSeeking 36b73880-c2c8-11cf-8b46-00805f6cef60; IGraphBuilder 56a868a9-0ad4-11ce-b03a-0020af0ba770.
- audioApplyVolume 0x4BF630 calls IBasicAudio vtable +0x1C = put_Volume for the DirectShow branch.
- audioPredicateA 0x4BF6A0 calls IMediaEvent::GetEvent(timeout=1ms), checks HRESULT, frees params, and returns true only for event code 1 (EC_COMPLETE).
- audioActionA 0x4BF720 performs IMediaControl::Stop -> IMediaSeeking::SetPositions(start=0) -> IMediaControl::Run.
- Normal playBGM passes playback arg3=1, stored as player +0x0A=1; therefore MP3 EC_COMPLETE is consumed by predicateA and current track is restarted in-place.
- loopBGM passes playback arg3=0, so +0x0A=0; EC_COMPLETE falls through to playlist transition rather than same-track DirectShow restart.
- audioPredicateB 0x4BF780 calls IMediaEvent::GetEvent(timeout=1ms) and treats eventCode==1 as transition-ready. It does not check GetEvent HRESULT or call FreeEventParams on this path; uninitialized/stale output behavior is a native edge to preserve/test.

[CONFIRMED-TARGET] OGG backend / EOF
- extension literal "ogg" selects the custom OGG branch.
- OggDecoder constructor 0x501E20 writes vtable 0x6395CC, matching target RTTI OggDecoder.
- OGG playback uses wrapper object at player +0xA0 and marks player byte +0x09=1.
- audioPredicateB sees +0x09 and calls wrapper status 0x502580; transition occurs when wrapper status reports the custom stream end condition.
- wrapper thread 0x5023E0 maintains +0x58 state and +0x54 position/end marker; status compares DirectSound-buffer cursor/progress against these values.
- OGG EOF decision is therefore volume-independent at the engine predicate level.

[ROOT-CAUSE STATUS: VERIFY]
- UI/master volume 0 only maps gain to effective -9600; no direct stop/reopen call exists in the setter.
- Both MP3 and OGG EOF predicates are transport/progress based, not volume-value based.
- Repeated replay mechanism is confirmed (EC_COMPLETE or OGG EOF -> reset/restart/playlist reopen), but a zero-volume-specific trigger is not statically proven.
- Dynamic trace should capture GetEvent HRESULT/eventCode, player +8/+9/+0A, OGG +0x54/+0x58, stop/reset and reopen calls while toggling UI volume 100 -> 0.
