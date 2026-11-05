# Explicit audio formats and automatic discovery

> Current bounded acceptance and corrections: [OGG_EXPLICIT_FORMAT_RUNTIME.md](OGG_EXPLICIT_FORMAT_RUNTIME.md). Earlier pending-state passages below are historical snapshots, not the final release status.

2026-11-06. Approved behavior plus read-only native design evidence. Implementation is in progress; native runtime acceptance of this extension remains pending. Isolated component tests do not establish game acceptance.

## Approved selection policy

| Existing command argument | Required behavior |
|---|---|
| `foo` | Use WAV if available; otherwise use the same-stem OGG. |
| `foo.wav` | Use WAV if available; otherwise use the same-stem OGG. |
| `foo.ogg` | Use OGG only, even when a same-stem WAV exists. |

Same-stem WAV and OGG may contain different audio. Explicit OGG must remain independently selectable; it is not an alias for a WAV-first logical stem. Preserve unrelated filenames and distinguish the format in native cache keys. Discovery must work from the distribution's files without requiring a manually authored manifest; an automatically built immutable catalog can retain the existing bounded lookup and ownership model.

For SE, the conservative builder decision preserves the original WAV root search first: primary WAV, fallback WAV, then primary OGG, fallback OGG. Explicit OGG searches only OGG in primary/fallback order. This deliberately lets a fallback WAV beat a primary OGG for extensionless/explicit-WAV requests, preserving existing native WAV selection. It differs from trying both formats in each root before moving to the next root.

For basename voice requests, existing WAVs across the native voice directories must retain priority for extensionless/explicit-WAV requests. Only when no matching WAV exists should the virtual index select a corresponding OGG. Explicit OGG has a separate selection namespace. Preserve the native outer directory order and first-wins rule within each eligible format; do not let an early virtual OGG conceal a later physical WAV. Directory-derived gains must correspond to the selected audio directory.

## Commands and source identity

The canonical registered DAT command is `playSE`: exact string at `006315E8`, loaded by `004A099F`, assigned opcode `21` at `004A09B4`. VM `004A1250` case 21 uses the normal engine sound route. The single voice command is `vc`: string `006317E8`, registration `004A1190..004A11B9`, opcode 4B. Examples for documentation/tests should use `playSE(foo.ogg)` and `vc(foo.ogg)` with actual available stems.

A read-only scan of the current permitted test-copy DAT files found canonical `playSE` and some lowercase `playse` occurrences, plus the authored `vc` acceptance event. That textual inventory does not establish support for every casing variant. No `playSe` or `se(...)` spelling was established by this audit. Do not rename or add unrelated commands as part of audio format support.

EXE SHA256: `e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187`.
Read-only V9 SHA256: `2629cb2f03ecec9927e89892c77f847e4cdba381ab718825c1ca8cfeeef00ede`.
Addresses are preferred VAs at base `00400000`; use RVA plus actual module base.

## Native suffix construction

All three loaders blindly append `.wav`; none of these sites detects an existing extension:

| Purpose | CALL VA and original bytes | Target / contract |
|---|---|---|
| SE `sound/` + argument + `.wav` | `004C09EB`: `E8 60 63 F4 FF` | `00406D50`, cdecl null-terminated list of strings |
| SE root resolution | `004C09F1`: `E8 9A 67 F6 FF` | `00427190`, cdecl one string |
| SINGLE volume key | `004C02B4`: `E8 37 6A F4 FF` | `00406CF0`, first string in ECX, suffix on caller-cleaned stack |
| SINGLE path-index key | `004C037C`: `E8 6F 69 F4 FF` | same custom helper |
| BATTLE volume key | `004C05A7`: `E8 44 67 F4 FF` | same custom helper |
| BATTLE path-index key | `004C075E`: `E8 8D 65 F4 FF` | same custom helper |
| SINGLE indexed directory + name + suffix | `004C0405`: `E8 46 69 F4 FF` | `00406D50`, cdecl |
| SINGLE primary + `voice/` + name + suffix | `004C043B`: `E8 10 69 F4 FF` | `00406D50`, cdecl |
| BATTLE indexed directory + name + suffix | `004C07C5`: `E8 86 65 F4 FF` | `00406D50`, cdecl |
| BATTLE primary + `voice/` + name + suffix | `004C07FB`: `E8 50 65 F4 FF` | `00406D50`, cdecl |

SE uses primary prefix `0068B370` and fallback `0068B38C`. Native `00427190` checks the primary WAV and rebuilds the fallback path on a miss; it does not check fallback existence before returning. SINGLE/BATTLE instead use the startup filename-to-directory map, or primary prefix + `voice/` when that map misses. They do not call the two-root resolver.

Consequently, `foo.ogg` reaches the unmodified factory as `foo.ogg.wav`, and `foo.wav` as `foo.wav.wav`. A bounded adapter can remove exactly the one engine-appended terminal `.wav` when it follows an explicit `.ogg` or `.wav`, preserving the preceding format intent. Repeated unrestricted suffix stripping would change legitimate dotted filenames.

Factory correction alone is insufficient for a basename voice: the preceding path and gain lookups ask for `foo.ogg.wav` or `foo.wav.wav`, so the ordinary `foo.wav` index entry does not match. One design compatible with existing Win32 enumeration hooks is to synthesize explicit-format index aliases in addition to the ordinary entry, allowing native code to build both indexes. These aliases must obey the selection policy above and must not collide silently with real filenames such as `foo.wav.wav`. Test collisions and preserve an explicit, deterministic rule; do not assume aliases are unique.

The helper `00406CF0` is not a standard plain-C ABI. Do not introduce guessed calls to it or to the native C++ map lookup helpers. Existing standard cdecl resolver and stdcall factory boundaries remain preferred adapter points.

## Cache identity

SE `004C0050` and BATTLE `004C04E0` use the original command argument as their cache key. Keep `foo`, `foo.wav`, and `foo.ogg` distinct when their selection semantics can differ. Normalizing all three to `foo` before cache lookup can replay a previously cached WAV for an explicit OGG request. Test both request orders with different WAV/OGG content. SINGLE replaces its current slot, but should obey the same format selection contract.

## Embedded text voice markers also need support

`00434CC0` parses a text/voice form, searches for `.wav`, requires that match to end at the voice-string boundary, strips four characters, then calls SINGLE. Merely enabling `.ogg` in the suffix check would still strip its format intent and incorrectly permit WAV preference.

Two existing CALLs have independently checked standard stack contracts:

- `00434D4D`: `E8 3E 17 FF FF` -> `00426490`, stdcall `(string_object, pattern, length)`, return index or -1, `ret 0C`. The caller tests index+4 == string length at `00434D57..00434D5E`.
- `00434D8D`: `E8 0E B4 08 00` -> `004C01A0`, stdcall `(manager, voice_name, category)`, `ret 0C`. The intervening substring helper removes exactly the four-character suffix; avoid calling that custom helper from new code.

The isolated `hakushin_ogg_text_voice.h` pair of adapters recognizes terminal OGG, retains a bounded owned copy in state owned by the captured UI thread, lets the existing substring operation run, and restores the explicit name only at the paired SINGLE forwarding call when the trimmed name matches exactly. Each UI-thread find clears old pending intent; each UI-thread SINGLE consumes it before forwarding, including on mismatch. Other threads pass through without touching that state. The forwarded name has a call-local copy so reentry cannot overwrite it. Native string objects are not modified; the existing WAV find behavior is forwarded unchanged. Its tests passed x86 O0 and O2 with warnings treated as errors; game acceptance remains pending.

The embedded delimiter is `@`: parser `00425A20` checks byte `40` at `00425AB9`, ignoring DBCS trail bytes. `00425B6D..00425B7A` extracts the suffix after `@` into output string +1C, while `00425B83..00425BB4` extracts the display prefix. `00434CC0` checks the second string for a voice suffix. The structural form is therefore `display text@voice.wav` / `display text@voice.ogg`. Its verified callers are `00476144`, `004D8B0B`, and `004D8D61`; a specific DAT `msg(...)` acceptance route has not been established by these references, so do not equate this marker form with an arbitrary command argument without runtime or registration evidence.

Acceptance must cover SE, direct `vc`, battle voice definitions, and embedded text markers with extensionless/WAV/OGG inputs as applicable; different same-stem audio; both cache orders; original directory gains; native duplicate directory precedence; Japanese/CP932 names; mixed and OGG-only roots; real double-extension filename collisions; missing assets; and unchanged BGM and unrelated commands. Do not silently narrow the requested feature to `vc` alone.
