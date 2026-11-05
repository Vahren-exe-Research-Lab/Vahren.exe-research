# Original voice index audit after WAV removal

> Current bounded acceptance and corrections: [OGG_EXPLICIT_FORMAT_RUNTIME.md](OGG_EXPLICIT_FORMAT_RUNTIME.md). Earlier pending-state passages below are historical snapshots, not the final release status.

2026-11-06. Static diagnosis and scoped repair design. This audit did not modify the game, install patches, call native internals, or edit the formal dictionary. Full runtime acceptance of the proposed repair remains pending.

## Evidence identity and reported regression

Freshly verified SHA256:

- Original EXE: `e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187`.
- Read-only V9 SQLite source: `2629cb2f03ecec9927e89892c77f847e4cdba381ab718825c1ca8cfeeef00ede`.

Native snippets were decoded from that exact EXE using Capstone and checked against V9 functions `004B78C0`, `004C04E0`, `004C01A0`, `00438D40`, `00439E00`, `004C1200`, `004BB430`, and `0043A2A0`. Addresses below are preferred VAs at image base `00400000`; production addresses must add the stated RVA to the actual module base.

The implementation owner reported a full-manifest run with original WAVs absent: successful SE and explicit-path SINGLE calls, but 28 battle factory calls fell back to native behavior and the user heard no battle voices. The reported battle thread matched the successful UI thread. These observations motivated the audit; this note does not reproduce or independently re-analyze the raw run log.

## Root cause: two WAV-only startup indexes

Startup function `004B78C0` enumerates voice directories and then files in each directory. At `004B8195`, `68 50 01 63 00` pushes string `00630150`, whose exact bytes are `2A 2E 77 61 76 00` (`*.wav`). `004B819A`, `E8 51 EB F4 FF`, calls the two-string concatenation helper `00406CF0`. The first string is in ECX; the suffix is one caller-cleaned stack argument. The resulting pattern is passed to FindFirstFileA. OGG filenames do not enter this scan.

For each non-directory WAV entry, the original loop builds two separate maps:

| Map | Preferred address | Manager offset | Construction |
|---|---|---|---|
| Filename to directory prefix | `008BE42C` | `8C` (sentinel/head at `90`) | `004B8230` builds the filename/prefix pair; `004B8247` allocates the map node; `004B8256` inserts it |
| Filename to configured additive volume | `008BE43C` | `9C` (sentinel/head at `A0`) | `004B8317` looks up the current directory label in sound settings; `004B83FE` builds the filename/value pair; `004B8427` inserts it |

Relevant exact CALL bytes:

- `004B8230`: `E8 FB 31 00 00` -> `004BB430`.
- `004B8247`: `E8 54 20 F8 FF` -> `0043A2A0`.
- `004B8256`: `E8 A5 1B F8 FF` -> `00439E00`.
- `004B83FE`: `E8 6D 8B 05 00` -> `00510F70`.
- `004B8427`: `E8 54 AE FA FF` -> `00463280`.

WAV removal therefore removes both filename routing and the associated per-file gain data from native startup, even though the OGG files and bridge manifest remain present.

## Battle routing and volume consequences

`004C04E0` first forms `<voice argument>.wav` and looks it up in the path map. `004C0784`, `E8 B7 85 F7 FF`, calls `00438D40` with EAX=&manager+8C, EDI=&temporary MSVC string, and one stack argument for the output node; the function returns with `ret 4`. This is a custom register contract, not a plain C call.

If a directory mapping exists, `004C07C5`, `E8 86 65 F4 FF`, calls cdecl concatenator `00406D50` with directory prefix, voice argument, `.wav`, and null terminator. If the map misses, `004C07FB`, `E8 50 65 F4 FF`, calls the same function with primary prefix `0068B370`, `voice/`, voice argument, `.wav`, and null terminator. The latter branch does not use fallback prefix `0068B38C`.

Thus an ordinary basename becomes `<primary>voice/<basename>.wav`, losing its subdirectory. It no longer matches an exact manifest key for `<primary>voice/<subdirectory>/<basename>.wav`. SINGLE `vc` with a subdirectory already included in its argument can still work, explaining the observed difference without invoking a thread mismatch.

Volume is computed before the factory call. Battle `004C05A7` forms the filename plus `.wav`; `004C05E9` selects manager+9C; `004C05FB`, `E8 00 0C 00 00`, calls `004C1200`. A hit contributes the node's signed DWORD at +28; a miss contributes zero. Native code then combines that value with `default_btl` and the manager's category setting and clamps it before SetVolume. SINGLE's analogous per-file lookup is `004C0304`, `E8 F7 0E 00 00`. Both lookup sites use EAX map / EDI string / stack output-node / `ret 4`; ordinary category lookups are separate calls.

The permitted local sound settings contain directory gains: small0=200, small1=400, small2=800, small3=1200, small4=1600. Only these factual numeric settings are recorded here, not the original DAT content. Explicit filename aliases in the bridge manifest would repair routing but would not restore these native gain contributions. Correcting gain after buffer construction would also conflict with the original caller's subsequent SetVolume.

## Duplicate filenames

Path insertion is first-wins. In `00439E00`, the duplicate branch at `00439F39` destroys the newly allocated candidate, `00439F49` returns the existing node, and `00439F4B` sets the insertion flag to zero. It does not replace the existing directory prefix.

A read-only call to the actual FindFirstFileA/FindNextFileA APIs over the permitted copy's outer voice directory scan returned small3 before small4 (ordinals 6 and 7 including dot entries). Therefore those two directories preserve small3 as the first path candidate for their shared filename. The implementation owner separately reported that the duplicate source WAV contents match; equal audio content alone is not semantic equivalence because the directory gains differ. Retaining the original outer directory enumeration is preferable to inventing a duplicate policy.

## Scoped virtual WAV enumeration contract

The proposed repair virtualizes only the inner WAV filename scan. Its first-call wrapper checks the exact caller return RVA `B81A9`; unrelated first calls forward unchanged. Next and Close wrappers act only on their own tracked enumeration handles. All three wrappers use the ordinary Win32 WINAPI ABI; no custom native lookup call is required.

| API | IAT VA / RVA | Inner CALL VA and original bytes | Return VA / RVA |
|---|---|---|---|
| FindFirstFileA | `00609178` / `209178` | `004B81A3`: `FF 15 78 91 60 00` | `004B81A9` / `B81A9` |
| FindNextFileA | `00609170` / `209170` | `004B848E`: `FF 15 70 91 60 00` | `004B8494` / `B8494` |
| FindClose | `00609174` / `209174` | `004B84AE`: `FF 15 74 91 60 00` | `004B84B4` / `B84B4` |

The PE import table identifies all three as KERNEL32 imports. They are six-byte indirect calls: use managed IAT pointer patches, not the existing five-byte relative CALL mechanism. Validate the expected original API pointers and retain the same exact-host and early-bootstrap gate used by the bridge. Partial patch recovery must retain the wrappers and their state while any installed pointer can still reach them.

The complete inner loop `004B81C0..004B8481` uses only:

- `dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY` to skip directories (`004B81C0` tests bit 10h).
- `cFileName`, copied into native strings used to populate the two indexes.

It does not consume file size, timestamps, alternate filename, or file contents, and does not open the enumerated voice file. Its calls are string operations, map allocation/insertion/lookups, and allocation cleanup. Virtual entries can therefore provide an exact ACP WAV filename with the directory bit clear; unused metadata can be initialized to zero.

The inner find handle is stored at stack+2C. FindNextFileA is called until false and FindClose follows once. A failed first call also reaches FindClose(INVALID_HANDLE_VALUE), which should retain native passthrough behavior. Keep virtual handle state alive after end-of-enumeration until Close; support an early Close without leaking the real underlying enumeration.

The outer directory scan must remain unchanged: its Next call is `004B8105` / return `004B810B`, and Close is `004B8115` / return `004B811B`. This retains the game's directory order, first-wins resolution, and the native association between each directory and its sound setting.

Recommended merge policy within each requested directory: return original WAV results unchanged first, then explicit manifest WAV entries missing from that real enumeration. Match the immediate parent directory only, not recursive descendants; suppress real/virtual duplicates using the existing pathname encoding and comparison rules. Keep the manifest immutable for every live enumeration. Do not globally alter FindFirstFileA behavior or synthesize arbitrary unlisted basenames.

## Validation still required

This is static support for the repair, not proof that the new enumeration implementation works. Focused tests should cover absent WAVs, mixed real/virtual entries, duplicate suppression, exact caller restriction, unrelated/outer handles, independent enumeration positions, end-of-list lifetime, early Close, empty results, failure cleanup, and partial IAT-install rollback/retention. A fresh game run must then confirm that full-manifest battle voices use bridge buffers and preserve the original directory-based gains with WAVs absent. User audibility and category-volume acceptance remain separate from successful factory return values.
