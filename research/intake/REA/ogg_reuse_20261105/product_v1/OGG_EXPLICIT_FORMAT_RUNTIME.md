# REA-T015 supplemental study: explicit WAV/OGG selection and native voice indexes

2026-11-06 JST. Status: **USER_ACCEPTED_BOUNDED_FORMAT_AND_BATTLE_TRIAL**.

The final candidate supports explicit OGG selection independently of a same-stem WAV, preserves existing WAV selection, and discovers voice files without a manually authored manifest. The user completed the corrected format-test launcher and reported: 「Run-OGG-Format-Test.cmd を実行しました。問題はなかったです」. The corresponding run exited normally and exercised SE, SINGLE and BATTLE OGG buffer creation successfully.

This is a supplemental implementation/evidence study for REA-T015, not a new formal function-dictionary entry. It records the accepted bounded trial, the failures that shaped the implementation, and the remaining limits. It contains no original DAT, audio, raw logs, absolute machine paths, or private database contents. Raw evidence remains local; hashes identify it without redistributing it. No GitHub write or publication is performed by this document.


## Intake metadata

- research_id: REA-T015-OGG-REUSE-20261105
- owner: REA; tasks: T015
- observed_at/source_snapshot: 2026-11-06 JST; exact hashes and run times below
- evidence_kind: STATIC / SYNTHETIC / VERIFY / bounded user-operated runtime observation, separated below
- golden_status: 0 (no broad original-game Golden/strict MATCH certificate)
- ready_status: 0 (no formal research-ledger READY promotion)
- prior_ids: the same REA-T015-OGG-REUSE-20261105 study, its product_v1 and playback/probe supplements
- supersedes/errata: only the historical required-manifest, unimplemented-bridge and full-migration-runtime-pending claims within the tested scope
- curator candidates: REF_AUDIO_VORBIS.md, REF_DAT_BEHAVIOR.md, REF_SCRIPT_VM_CONTEXT.md; six CALLs, three IAT boundaries, native voice filename/gain maps; no shared dictionary edit
- limitations/next_validation: the explicit limits and targeted follow-ups at the end of this report

## Relationship to earlier studies

- [OGG_WAV_MIGRATION.md](WAV_MIGRATION_DESIGN.md) records conversion, original factory ABI observations, and the original-device Buffer8 requirement.
- [OGG_BRIDGE_RUNTIME.md](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/docs/OGG_BRIDGE_RUNTIME.md) records subset acceptance, the earlier category-volume trials, and the first full-migration regression.
- [OGG_VOICE_INDEX_AUDIT.md](OGG_VOICE_INDEX_AUDIT.md) supplies the detailed native evidence for the two startup indexes, directory gain, duplicate insertion, and scoped enumeration boundary.
- [OGG_EXPLICIT_FORMAT_DESIGN.md](OGG_EXPLICIT_FORMAT_DESIGN.md) supplies command identity, suffix construction, cache-key and text-marker evidence.

Those files retain historical “pending” statements. This report supersedes them only for the implementation and runtime scope expressly established below. Earlier assembly observations and narrower evidence limits remain applicable.

## Identity and evidence categories

| Item | SHA256 |
|---|---|
| Supported original EXE | `e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187` |
| Read-only V9 source database used for static crosschecks | `2629cb2f03ecec9927e89892c77f847e4cdba381ab718825c1ca8cfeeef00ede` |
| Final explicit-format DLL | `f41fdb1bd3fa39760e4c075dfd4a3a1b1e3192a31f9c290deb91afdb18800902` |
| Final build/test log | `923583a5c54e454a55db6b972d2778da7e39afbc6244f95a7a146135591ff733` |
| Automatic voice corpus result | `b12f689c088645486229729693af71fadf53ebf759d9e24d6234bbf8fe05b63f` |

The evidence categories are deliberately separate:

1. **Static native evidence:** exact EXE bytes, disassembly and read-only V9 crosschecks support addresses, calling contracts and control flow. They do not independently establish runtime audibility.
2. **Automated tests:** isolated C tests exercise real Windows APIs where appropriate, deterministic failure paths and synthetic native boundaries. They do not replace a game trial.
3. **Read-only corpus checks:** inventory, path selection and OGG-source validation cover the actual files without playing them. They do not prove native decoding of every OGG.
4. **Runtime logs:** patch results, enumeration, selection, native decode and buffer results establish observed execution. They count requests/entries, not unique assets or audible sound pressure.
5. **User observation:** the final no-problems report accepts the requested bounded format/battle session. It is not a fresh quantitative volume measurement or a full-game coverage claim.

The launcher's `hearing_confirmed=false` field is a collection-time default, not a later denial of audibility. The final user response and subsequent analysis record supply the acceptance statement; the immutable run receipt supplies process and file-collection facts.

## What changed after the failed full migration

The first bridge returned OGG-backed original-device buffers from three original factory CALLs. It also adapted the SE root resolver and used an explicit mapping file. That design passed a small mapped subset while physical WAVs remained available.

Removing all original WAVs exposed an earlier dependency. Native startup enumerates `*.wav` and builds both a filename-to-directory map and a filename-to-additive-gain map. A basename battle request whose index entry disappeared fell back to the primary root's `voice/` directory, losing its original subdirectory. The factory therefore received a different path from the exact mapped key. The failed run's filenames were not logged: this path explanation is supported by static control flow, not direct capture of those particular arguments.

Adding manifest aliases at the factory would have repaired only path lookup. The gain lookup happens before the factory and also depends on the missing startup index. The repair instead supplies virtual WAV enumeration entries to the original startup routine, allowing native code to rebuild both maps with its own allocator, insertion policy and directory settings.

The final extension removes the manual-map dependency. A bounded immutable inventory discovers eligible WAV/OGG files, supplies format-specific index names, and leaves the original outer directory order intact. Selection happens at the existing resolver/factory boundaries, after the native cache-key decision.

## Final selection algorithm

The registered SE command is `playSE`; the registered direct voice command is `vc`. This report does not establish arbitrary casing variants or introduce new command names.

| Command argument | Final intended selection |
|---|---|
| `sample` | Native caller appends `.wav`; existing WAV wins, otherwise same-stem OGG may be selected. |
| `sample.wav` | Existing WAV wins; only absence permits same-stem OGG. |
| `sample.ogg` | OGG only, even when a same-stem WAV exists. Missing/failed OGG does not fall back to WAV. |

All three original loaders append `.wav` without recognizing an existing extension. The scoped selector therefore removes exactly one known appended suffix: `sample.ogg.wav` becomes `sample.ogg`, and `sample.wav.wav` becomes `sample.wav`. It does not repeatedly strip suffixes. Extensionless input is outside this helper's contract because native construction already appends the suffix.

Paths are decoded with the applicable Windows code page before extension, separator or case decisions. The selector returns an owned bounded copy and one of INVALID, NATIVE_WAV or OGG. It rejects traversal, absolute paths, malformed components, unsupported extensions and overlong input. CP932 trail bytes resembling a slash or an ASCII letter are not treated as separators or case-folded bytes.

For WAV selection, any present WAV is a precedence barrier. Access/sharing and other non-missing attribute errors also remain native; only file-not-found/path-not-found permits format fallback. Failure to read or decode a selected WAV is not a reason to try OGG. OGG fallback probes use the rooted regular-file validation path. Explicit OGG remains an OGG selection even if the eventual open fails, so its failure is reported without playing a WAV instead.

SE preserves the original WAV search across both roots before considering OGG:

1. Primary WAV.
2. Fallback WAV.
3. Primary same-stem OGG, only if neither WAV exists.
4. Fallback same-stem OGG.

Explicit OGG checks only primary OGG then fallback OGG. With no match, the selected fallback path retains the appropriate native-WAV or explicit-OGG failure behavior. In particular, a fallback WAV beats a primary OGG for a legacy or explicit-WAV request.

The SE resolver stores the selected path and selection kind in UI-owned state. A matching route-3 factory consumes that decision once, avoiding a second suffix normalization. An unmatched factory input is selected normally and clears the pending decision. This matters for legitimate compound filenames. The original command arguments remain the native SE/BATTLE cache keys: `sample`, `sample.wav` and `sample.ogg` are not collapsed before cache lookup.

## Automatic voice inventory, aliases and collision policy

Only the reviewed startup inner `*.wav` search is virtualized. The first-call wrapper requires the exact return RVA `B81A9`, active bridge state, loading state 1, a validated voice-directory pattern and a directory resolved inside the game root. The original outer directory enumeration is unchanged.

The inventory scans immediate voice subdirectories, retains native ordering, and considers WAV presence across the sibling directories before allowing a legacy OGG alias. Consequently an earlier OGG cannot conceal a later WAV under the same ordinary basename. Within each eligible format, original first-wins directory precedence remains in force. The native code associates the selected entry with that directory's gain.

For ordinary names, a physical WAV retains its native entry and gains an explicit-WAV key. An OGG gains an explicit-OGG key; if no corresponding WAV exists across the relevant siblings, it also gains legacy and explicit-WAV fallback keys. These are synthetic enumeration names, not files written to disk. Ordinary physical entries precede supplemental entries, with the reserved-key exception below.

Compound names require an explicit namespace rule. Native keys ending in `.ogg.wav` or `.wav.wav` represent format-qualified requests under the new grammar. Exposing a physical `sample.ogg.wav` directly under that raw key could steal an explicit `sample.ogg` request from a different directory, giving both the wrong path and the wrong gain.

- Such physical compound WAV entries are hidden under their raw reserved keys, but remain in the inventory and receive an appended full-filename alias. For example, the physical `sample.ogg.wav` is reachable through the key `sample.ogg.wav.wav`, generated when the caller requests its full filename.
- An OGG whose stem itself ends in `.ogg` or `.wav` receives only its explicit full-OGG alias. Ambiguous legacy/explicit-WAV fallback aliases are not emitted for that compound stem.
- Nonreserved physical names retain their native precedence. Collision tests model native first-wins insertion and verify the selected directory/gain identity, not just an enumeration count.

This deliberately reserves format-qualified index names; it is not an unrestricted basename guessing rule. A future extension must retain this policy or define and test a replacement before changing it.

Enumeration handles are real unique kernel handles owned by the component, not magic pointer values. Each context owns its real underlying search, if any; end-of-list does not destroy the context before Close. Unowned Next/Close handles pass to the captured original APIs with native LastError behavior. Synthetic end reports `ERROR_NO_MORE_FILES`. Synthetic `WIN32_FIND_DATAA` is zeroed except for a normal-file attribute and the filename. Static inspection established that the targeted loop reads only the directory attribute bit and `cFileName`; it does not open the enumerated file or consume its size, times or alternate name.

Limits are 16 live enumeration contexts, 8 cached voice roots, 32,768 inventoried files and a 32 MiB inventory budget. Inventory errors/cap violations fail the affected context rather than silently dropping names. Failed inventory-close handles remain owned for retry; destruction cannot claim a clean state while such handles remain. The inventory is immutable for the process lifetime; changing voice files requires a new game process.

## Native gain preservation: proof and limit

The [voice-index audit](OGG_VOICE_INDEX_AUDIT.md) identifies the filename-to-directory map at preferred VA `008BE42C` and the filename-to-additive-gain map at `008BE43C`. Native SINGLE/BATTLE gain lookup happens before factory creation. The observed directory settings were small0=200, small1=400, small2=800, small3=1200 and small4=1600; these are native additive values, not independently calibrated output levels.

Virtualizing only the inner filename enumeration lets the same native loop populate both maps. The outer directory order and duplicate insertion remain native. The bridge neither calls the custom-register C++ map routines nor applies a replacement volume after buffer creation. Existing category gain, per-file contribution, clamping and later SetVolume remain with the original engine.

This is a structural preservation argument supported by native control-flow evidence and first-wins path/gain fixture tests. The final game run verifies successful battle routing and user acceptance; it does not numerically measure each gain contribution. Earlier maximum/zero category-volume observations belong to the separate subset trials recorded in [OGG_BRIDGE_RUNTIME.md](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/docs/OGG_BRIDGE_RUNTIME.md). They must not be presented as a fresh slider test of this final DLL.

## Six managed CALL sites and three managed IAT slots

Addresses below are RVAs, added to the actual module base. Preferred VAs use base `00400000`. The supported EXE identity and expected original bytes/pointers are checked before installation; an address alone is not a portable API.

| Purpose | CALL RVA | Original five bytes | Original target RVA | Contract |
|---|---|---|---|---|
| SINGLE buffer factory | `C046E` | `E8 DD 09 00 00` | `C0E50` | Three stack arguments: manager, path, flag; stdcall-compatible `ret 0C`; returned Buffer8 in EAX. |
| BATTLE buffer factory | `C082F` | `E8 1C 06 00 00` | `C0E50` | Same factory contract. |
| SE buffer factory | `C0B81` | `E8 CA 02 00 00` | `C0E50` | Same factory contract. |
| SE root resolver | `C09F1` | `E8 9A 67 F6 FF` | `27190` | cdecl, one path argument; caller cleanup; returned string pointer. |
| Embedded-text suffix find | `34D4D` | `E8 3E 17 FF FF` | `26490` | stdcall, string object/pattern/length; index or -1; `ret 0C`. |
| Embedded-text SINGLE forwarding | `34D8D` | `E8 0E B4 08 00` | `C01A0` | stdcall, manager/name/category; `ret 0C`; caller does not consume a return value. |

| API | IAT slot RVA | Behavior |
|---|---|---|
| FindFirstFileA | `209178` | Scope first calls to the audited startup return address and voice folder. |
| FindNextFileA | `209170` | Intercept owned enumeration handles only. |
| FindClose | `209174` | Close owned contexts; delegate all other handles. |

The IAT sites use ordinary Win32 WINAPI contracts and managed pointer patches, not five-byte relative CALL patches. Captured original pointers are checked against the expected imported APIs, avoiding recursion through the patched game IAT.

Installation is limited to the early bootstrap while loading is active and the original sound manager's device is still absent; the UI thread is captured from the game window. Six CALL patches precede three IAT pointer patches. Rollback restores in reverse order. A recovery state retains reachable code/state and is not interpreted as active bridge behavior. Installed hooks are process-lifetime: arbitrary-thread hot unload is rejected, and DllMain performs no waits or joins.

### Embedded text voice intent

The static parser recognizes a display/voice split using `@`. Its WAV suffix check strips four bytes before forwarding to SINGLE. Merely accepting `.ogg` in that check would lose explicit format intent.

The paired adapters keep a bounded owned copy of a terminal OGG name, let the original substring operation proceed, then restore the explicit name only when the paired SINGLE input matches the expected trimmed name on the captured UI thread. Find clears old intent; SINGLE consumes intent before forwarding, including on mismatch/reentry. Other threads pass through without touching UI state. Native string objects are never modified. The copy callback validates the known 16-byte inline union plus length/capacity fields, reads only the bounded string and terminator, and rejects embedded NULs.

Static checks, dedicated tests and bridge integration tests cover this behavior. **The final accepted runtime log contains no `BRIDGE_TEXT_FIND` or `BRIDGE_TEXT_SINGLE` events.** This session therefore does not establish a game-level embedded-text OGG playback observation, and its `msg` prompts must not be mistaken for evidence that the separate text-marker parser executed.

## Decoder, buffer and request ownership

Native decoding stays on the existing single audio worker. The factory caller receives owned PCM and creates a stopped buffer on the original manager's borrowed DirectSound device. It uses `DSBCAPS_CTRLVOLUME`, copies both Lock regions, Unlocks, queries Buffer8 and releases the temporary base interface. Exactly one Buffer8 reference transfers to the original caller. The bridge does not Play, set category volume, Stop or independently release a successfully transferred original-manager buffer. Native duplicate pools, cache ownership and later playback/release remain intact.

The synchronous request owns its copied path, manual-reset completion event, result and references. At most one request is queued/in flight/uncollected. Caller completion wait is clamped to 5,000 ms. Timeout cancels and releases the caller's reference while an active worker retains valid storage until Finish; queued unclaimed work can be removed immediately. Shutdown rejects admission and wakes pending callers. There is no TerminateThread and no retained caller-stack/output pointer.

The PCM block reserves 16 MiB, even for a smaller decoded clip. The budget checks existing DAT-owned voice buffers plus the staging allocation and prospective output copy against 64 MiB. The UI's `bridge_in_call` guard remains set through original-buffer construction and PCM free; the worker does not start another DAT command while that transferred allocation remains live. A DAT command admitted just before the guard changes completes on the same worker before bridge decoding starts. On timeout, no PCM transfers to the caller, and the worker finishes/frees its owned result before processing another decode.

These limits are not a cap on total game memory: original-manager cached buffers and native index nodes belong to the engine; inventory has its separate budget. The 5-second completion wait is not a 5-second end-to-end latency guarantee, and it does not forcibly interrupt a blocked native call. Cancellation is cooperative between decode operations.

Successful native opens are cleared once after decoding. An ambiguous open failure poisons further native reuse rather than speculatively invoking cleanup; a failed clear also poisons the backend. Such states require process exit and retained code lifetime. Native source handles remain open through decode to exclude ordinary concurrent modification/deletion. Unsupported format changes, malformed reads, cancellation and budget failures return failure without publishing a partial buffer.

The source validator requires a local disk file resolved inside the game root, an OggS signature and a source size from 4 bytes through 16 MiB. Decode accepts mono/stereo signed-16 PCM at 8,000–192,000 Hz, rejects incompatible format changes, and enforces the separate 16 MiB decoded-PCM cap. These are implementation limits, not evidence that every accepted rate has been played in the final trial.

## Automated validation and read-only corpus

The final build ran 14 C suites at both `-O0` and `-O2` for x86 Windows with C11, `-Wall -Wextra -Werror`: logic, DAT, rooted paths, worker, regressions, backend, PCM, factory, manifest helper, selection, request, automatic voice enumeration, text voice and bridge. All 28 runs passed. Actual Core enabled/wrong-host rollback and disabled-plugin smoke tests also passed. The retained manifest unit suite tests shared legacy/canonical helpers; it does not imply a runtime manual-map dependency.

Meaningful coverage includes real DirectSound stopped-state/duplicate/readback behavior; injected COM failures; owned request timeout/completion and producer races; real Windows directory enumeration; CP932 path boundaries; native LastError passthrough; bounded handles and failed-close ownership; sibling WAV precedence; reserved compound-name collisions through a simulated native first-wins index; selection without a map; single-use SE normalization; inline/heap MSVC string copies; text-state mismatch/reentry/foreign-thread cases; exact bytes at all six CALL sites; and rollback failure at every CALL position plus IAT recovery/retention.

A separate read-only utility used the final automatic inventory and selector against the active converted corpus, without loading a manifest or launching the game:

| Voice directory | Physical OGG files | Emitted index names |
|---|---:|---:|
| small0 | 1 | 3 |
| small1 | 189 | 567 |
| small2 | 358 | 1,074 |
| small3 | 4,429 | 13,287 |
| small4 | 306 | 918 |
| Total | 5,283 | 15,849 |

There were 5,283 names in each of the legacy, explicit-OGG and explicit-WAV fallback categories. Every emitted name selected a valid OGG target; unavailable OGG targets were zero. Reported inventory allocation was 927,140 bytes; process handles were 100 before and 100 after. No game file changed. These are emitted entries, not distinct native map keys: duplicate basenames still encounter original first-wins insertion.

The earlier conversion verified 5,972 WAV/OGG pairs, including 689 sound and 5,283 voice files, with hashes and independent full FFmpeg decoding. That establishes conversion integrity, not native playback of every file. The later synthetic fixture intentionally added a mixed WAV/OGG pair and an OGG-only voice basename; the accepted game run's 15,855 enumeration entries are consistent with those six additional names.

## Runtime sequence and corrections

All times in this section are JST on 2026-11-06. Run identifiers are local evidence labels; raw logs are not included here.

| Run | Candidate/stage | Observed result and acceptance boundary |
|---|---|---|
| `024940-110-5eb59ea2`, 02:49:40–02:51:56 | First full mapping; original WAVs retired; DLL `9c8b87...` | Exit 0. SE 57 and SINGLE 1 OGG requests succeeded; 28 BATTLE calls fell back to native and none decoded through the bridge. User reported inaudible battle voices. This was a regression, not acceptance. |
| `031436-384-453fcf75`, 03:14:36–03:16:40 | Scoped enumeration repair, still using the full mapping; DLL `067ec1...` | Exit 0; four CALL and three IAT patches succeeded; 5,283 enumeration entries; 73 successful OGG cycles: SE 53, SINGLE 1, BATTLE 19. A qualified subjective positive observation was recorded; no specific new slider measurement was established. |
| `040606-090-696a94c0`, 04:06:06–04:06:38 | First explicit-format diagnostic; final DLL `f41fdb...`; no manual manifest | Diagnostic DAT parse failure reported at line 5. Exit 0 does not make it a playback test. Both fresh plugin logs were absent; there is no fresh OGG-log hash for this attempt. |
| `040859-173-fbb92d58`, 04:08:59–04:12:21 | Corrected format fixture; same final DLL; no manual manifest | Exit 0, no missing logs and no collection errors. User subsequently reported no problems with the format-test launcher. This is the accepted bounded format/battle trial. |

The 04:06 fixture failure was corrected by removing numeric/slash prefixes from eight diagnostic `msg` labels. The authored fixture hash changed from `bdec9202968c4a0f8c0d0a59e53881a48655604630a39ab3153fdadaa933df3f` to `4a3a5c23a9a3733fc666c8345efbd2fe22ff5e793676449558ae18a160c29ab8`; the DLL did not change. The failure is retained as evidence about the fixture/parser, not relabeled as a decoder or hook failure.

The corrected fixture used synthesized low 440 Hz WAV and high 880 Hz OGG content, including different same-stem content and an OGG-only fallback. Its eight expected observations were low, high, high, low, low, high, high, low across SE and direct voice prompts. The user supplied an overall no-problems response after the requested prompts and short battle, not a separate machine-verified frequency measurement or an answer for each prompt.

### Final accepted log facts

- Six `BRIDGE_PATCH_RESULT=0` and three `BRIDGE_ENUM_PATCH_RESULT=0`; `BRIDGE_EXPLICIT_FORMATS=1`, `BRIDGE_ACTIVE=6` and enumeration activation recorded.
- Five successful scoped enumerations emitted 15,855 entries and closed successfully. One additional first search returned no entries; it is not counted as an open context or assigned an unlogged filename.
- 95 selection records: 88 OGG and 7 native WAV. Route-selection totals were SE 66, SINGLE 8 and BATTLE 21.
- 88 OGG requests: SE 63, SINGLE 4 and BATTLE 21. Every one recorded open return 0, EOF, clear return 0 and bridge buffer result 0.
- Seven native selections were logged separately: SE 3 and SINGLE 4. They do not represent failed OGG requests.
- Recorded native decode formats were mono/stereo with rates 11,025, 22,050 and 44,100 Hz. This does not establish runtime coverage of every supported rate or every converted asset.
- Coarse bridge elapsed values ranged from 0 to 32 ms in this log. GetTickCount resolution, this short session and the absence of a load protocol prevent a latency guarantee.
- No text-voice adapter events occur in this log. No fresh category-volume sweep or quantitative gain measurement is claimed.

The final launcher receipt's `wav_sources_retired=false` describes a mixed-format trial containing newly synthesized WAV fixtures. It must not be read as evidence that the previously retired original WAV corpus was restored. The manual-manifest hash is null because that trial deliberately ran without the old map.

## Hash ledger for local runtime evidence

| Evidence | SHA256 | Bytes |
|---|---|---:|
| 02:49 failed full-migration OGG log | `67459cff02da5dc45c7257f751291b122cdf5867b53ab1e225e23fef19b4ee9a` | 35,004 |
| 03:14 enumeration-repair OGG log | `8bdf0b726fe5059a5ca7a466d92c93dd2f8a45810204722259c51c6e86a27dbf` | 349,446 |
| 04:08 accepted explicit-format OGG log | `04bb1ffa6831913d976c19d63321d3cf3560d3fc1a90bd66c3e35c0fb8e60554` | 983,672 |
| Loader log collected for each of those three runs | `ab09735865300776213836274949ed7a4c78c2eb6b0abf66d2db8843289ca3ed` | 763 |

The loader logs have identical bytes/hashes; per-run collection receipts establish their provenance. Hash equality alone does not establish execution coverage. The 04:06 parse-failure attempt collected neither fresh log; none is fabricated or borrowed from an earlier run.

| Run | `run.json` SHA256 | `analysis.json` SHA256 |
|---|---|---|
| 02:49 | `a22840bfb67fd9e9e070887e16ff43af300e312d1ffeac49c5d9cc6cffd7aeb0` | `68b386e5ff99780d60350335774d07ba6029b1ee486ac622f62055b091ca7f55` |
| 03:14 | `008684973cf417943a17929c4d6702fd7f558bca0e673022564aeb938202a64d` | `cdee9521aaff1daee57d939932f2dbc823455a3a8e941fd3ad7322521baeb864` |
| 04:06 | `717b99979628ca35173391aa33324fe2b359e22d7b54f4dfdd6b5d27d7bb78e0` | `54bbe2202a433c40e054898c2ebf15a86512b87ea9799e850415101f70ecc99a` |
| 04:08 | `e2c1766aad175aeac45735ec9f6f19bcacb9058862befb73c137046a556b9291` | `3c7442e42c3c4b17cd2648d8027e13c14d2c44f4bc768aebfbbf0bbdd2b09579` |

Analysis files are dated interpretations, including later user feedback; they are not substitutes for the corresponding raw logs/receipts. The enumeration-repair DLL was `067ec1d60a7049a3ca6e528f2076603372c71d79167cdfe9bd2f19540163fddc`. The failed full-migration DLL was `9c8b87c31fa168850869a704232edb5888ffbf9d71f00a321075de1f06e28225`. Their mapping file hash was `bcaae783842326bef6aa4365cf95674c25e2c16cd1cbfdbb2d81220ff9d55ca1`; it is historical input, not a final runtime requirement.

## Guidance for the next developer

| Responsibility | Implementation/tests |
|---|---|
| Format and root precedence, one-suffix rule | [selection helper](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/hakushin_ogg_selection.h), [tests](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/test_ogg_selection.c) |
| Automatic index inventory, alias namespaces, handle ownership | [voice enumeration](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/hakushin_ogg_voice_enum.h), [tests](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/test_ogg_voice_enum.c) |
| Embedded text intent and reentry handling | [text adapter](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/hakushin_ogg_text_voice.h), [tests](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/test_ogg_text_voice.c) |
| Owned worker completion and timeout lifetime | [request handoff](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/hakushin_ogg_request.h), [tests](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/test_ogg_request.c) |
| Worker-native decode and original-device buffer construction | [backend](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/hakushin_ogg_backend.h), [factory](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/hakushin_ogg_factory.h), [PCM tests](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/test_ogg_pcm.c), [factory tests](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/test_ogg_factory.c) |
| Exact-host integration, early gate, six CALLs and three IAT slots | [bridge](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/hakushin_ogg_bridge.h), [plugin](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/hakushin_ogg_plugin.c), [integration tests](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/test_ogg_bridge.c) |
| Reproducible strict x86 suite and Core smoke tests | [build script](https://github.com/ButaMonky/HakushinExtensions/blob/5faa5fb93679221350a744e466cc8f51da2fb42d/core/build_ogg_plugin.ps1), invoked with `-Test` |

Keep the native cache key unchanged, normalize only at audited boundaries, and preserve the SE resolver's one-shot selected intent. Keep format collisions in tests that follow an index key all the way to selected path and directory gain. Do not move decoder calls to the UI thread, return a separate-device DAT buffer to the original pool, patch a global resolver indiscriminately, or call the native custom-register string/map helpers through guessed C declarations.

For another EXE or startup sequence, re-establish the host identity, original bytes/pointers, stack contracts, early-install point and metadata consumers. The current addresses and structure offsets are not generalized across versions. For inventory changes, re-test error paths, both real First/Next filtering, failed-close retention, native outer-order preservation and full-filename access to compound assets.

Remaining evidence work should be targeted: a genuine embedded-text OGG marker route; additional mixed/scenario roots and corpus-specific duplicate/gain behavior; longer sessions, save/load and scene transitions; wider native format coverage; and explicit observations of unusual failures or latency. These are limits/future coverage, not a reason to erase the user's completed bounded acceptance or demand a repeat of the same successful trial. No claim is made that every converted asset, every gain, every release path or every future input has been exercised.

## Reuse decision after implementation

The tested EXE's existing Vorbis decoder is reusable from the DLL through the bounded worker-owned open/info/read/clear contract. This does not authorize direct calls to the earlier header/setup clues (005D44C0, 005D57C0, 005D5BD0) as if they were a public decoder API.

| Method | Current conclusion | Cost, intrusion and remaining risk |
|---|---|---|
| A: original decoder plus original effect/voice playback | Implemented for normal SE/SINGLE/BATTLE selection and accepted in the bounded game trial. Preferred for preserving ordinary DAT usage and native volume/pool semantics. | Highest native integration burden: six reviewed CALLs, three scoped IATs, original filename/gain indexes and cache identity. Exact-host-only. Whole-clip decoding adds CPU work and PCM storage; exhaustive cache lifetime/long-session behavior remains unmeasured. |
| B: original decoder, DLL-managed output | Implemented as the separate path/handle DAT API, with earlier two-voice, volume and stop acceptance. | Fewer original playback assumptions but DLL owns queue, voice lifetime, device/buffer management and cancellation. Eight managed voices and bounded PCM. Its independent volume does not automatically track original category controls. |
| C: independent decoder and DLL-managed output | Feasible alternative design, not implemented or runtime-tested here. | Removes dependence on the original decoder ABI but requires shipping/building a codec, its notices and security/format maintenance, plus the same output lifecycle work. Generalized compatibility and performance require separate measurement; no claim that it is faster or universally safer. |

For continuing this exact-version feature, retain A for the original command routes and B for explicitly managed additional voices. C becomes relevant when supporting other EXEs or requiring a different decoder contract. Pitch/reverb/echo are a separate requested discussion, not implemented functionality in this release. Formal dictionary adoption remains with the integration curator.
