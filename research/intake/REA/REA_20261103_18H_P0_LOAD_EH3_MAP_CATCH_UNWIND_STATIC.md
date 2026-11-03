# REA 2026-11-03 18H | native load EH3 metadata, catch-all entries and unwind map (STATIC / VERIFY)

- **Work:** `REA-20261103-18H-P0-LOAD-EH3-CATCH-STATIC`; REA owner, existing original study ID `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01`, **new independent research IDs 0**. A/T014 `A-20261012-1612-01` is a reference only.
- **Observed:** 2026-11-03 18:44 JST; original ver0.67 native PE32 `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; existing read-only Ghidra V9 SQLite `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`, both freshly hashed this run.
- **Prior source:** `rea_lab/decomp_task/REA_20261103_17H_P0_LOAD_SEH_FRAME_V9_FRAGMENT_SEAM_STATIC.md` SHA256 `D191A4209368719314E38B485B648B806BD1F515FF68608D2441AB6DC217C41E`; existing REA Draft PR #16, plus A/T014 native probe and curator `REF_SAVE_PERSISTENCE.md` / `symbols.tsv` / `REF_BATTLE_TAKEOVER.md` read-only review.
- **Method:** authorized PE `.text/.rdata` exact byte windows, `pefile` and x86 Capstone, V9 `mode=ro` targeted `functions`/`native_callsite`; no REA rerun, game launch, memory mutation, other owner writes, or refused source reaccess.

## New bounded native findings

1. 17H found `0x45E800 push 0x5FD61C` before SEH registration. The actual `.text` wrapper at `0x5FD61C..0x5FD646` reads EH frame offsets `[edx-0xFC]`/`[edx+0xC4]`, invokes `0x5B6513` twice for cookie checks, sets `EAX=0x655030`, then tail-jumps `0x5B8B1E` (native C++ EH dispatcher). V9 already labels it `EH_FH3_WRAPPER_005FD61C`, `verified_abi=0`. This is a compiler EH wrapper, NOT a gameplay callback.
2. At `.rdata 0x655030`, a 36-byte x86 EH3 FuncInfo-style header has magic `0x19930522`, max unwind-state count `30`, unwind map `0x654EF8`, try map count `2`, try map `0x655008`, no separate IP-to-state map, flags `1`. The bounded 30-entry map includes cleanup-action addresses and some zero actions; metadata is STATIC and does not identify dynamic reached state.
3. Both 20-byte try-map records have one handler: `(tryLow=4,tryHigh=4,catchHigh=5,handlerArray=0x654FE8)`, and `(tryLow=6,tryHigh=16,catchHigh=17,handlerArray=0x654FF8)`. Their 16-byte handler records each have `adjectives=0x40`, null `pTypeDescriptor` and `dispCatchObj=0`: handler addresses `0x45EAFC` and `0x45F933`, respectively. V9 already names both `Catch_All@`, so do not count new function names/IDs.
4. Native handler windows at `0x45EAFC` and `0x45F933` each call `0x5B71DD`, `0x5B6522`, then `0x5B864E` after setting local vptr `0x63852C` and passing metadata `0x641904`. This **limits** the earlier 'catch unknown' statement: catch-all *entries exist*, but their throw-helper path does **not** prove a swallowed exception, rollback, successful save-load, or that `0x45F5F9 -> 0x563ED0` is caught here. Precise exception translation/propagation is VERIFY.
5. Original relative E8/JMP bytes matched existing V9 `native_callsite` for wrapper `0x5FD62B/638/642` **3/3** (2 E8 + 1 tail E9), and the two catch blocks `0x45EB00/0B/20`, `0x45F937/942/957` **6/6** E8. **9/9 targeted entries matched**, none are new five-method REA bundles.

## Reproducible native receipts (SHA256 of exact virtual-address windows)

- `0x5FD61C+43`: `A4BEFD14580CF3B6B0453AAB19835E5BD86BC2DEC7169652B14956FEAB6E5C01`
- `0x655030+36`: `BD093D90850E3D5A269117B053F04879024F83ABB1135BC33660ECA43C0A058C`
- `0x654EF8+240`: `E65F98FD8BD3A46BF1BE1FCDABF40B5FA06A11F13704D92996F685D72D1602E7`; `0x655008+40`: `CE553E058FEA331336C6F67CA9024544E2CD94F215D1F084C6E989448D7F564D`
- `0x654FE8+16`: `990FFDFBE2720E78700C109CBCAE7041BD07212AEFFA63D36A2F4FA7F397E2E3`; `0x654FF8+16`: `207CC8AA59CA5F0C667F5E07205298FFA5423AB6FEE0CCA5AF58623C0DD33C3E`
- `0x45EAFC+41`: `FEB71070F98E9581955D90B7E191D8DD751B4C49F9A4D04CE06B83F87E9B3675`; `0x45F933+41`: `DDF1EFF297B762CD4481C49DC7E52DA9A517F1075E56AE3101998F581F9FFCE9`

## Duplicate, confidence, curator gate, next lawful cursor

- **Duplicate scan:** current private `develop/symbols.tsv`, `REF_BATTLE_TAKEOVER.md`, `REF_SAVE_PERSISTENCE.md` have no exact `0x5FD61C/0x655030/0x45F933/0x45EAFC` text matches; local `kb.py docs` reports the 17H entry `0x5FD61C` in A/T014 probe, but no prior indexed `0x655030` or `0x45F933` match. Existing V9 labels and original ID are retained; do not treat zero text hits as proof of complete novelty.
- **STATIC:** byte-receipted EH3 header, two try/catch-all metadata entries, 30 unwind-map entries, two wrapper calls plus E9 and six handler E8 concordances. **INFERRED:** C++ exception translation/rethrow meaning; **VERIFY:** actual current EH state at callsite `0x45F5F9`, whether either catch handler intercepts that callback's exception, unwind side effects, cleanup guarantees, vptr+8 producer and real gameplay reachability.
- **No promotion:** new formally five-method VERIFIED `0` (previous archived `64/64` not rerun), original-game Golden PASS `0`, strict MATCH `0`, READY `0`. Prior Wave6, absent older 18H evidence and protected VA remain untouched. No original binary/DB/raw log or sensitive paths enter private GitHub.
- **Status:** source-owner `PUBLISHED_INTAKE` only after matching GitHub file/manifest readback; otherwise `UNSYNCED`. **Not CURATED.** All `develop`, `REF_*`, `symbols.tsv`, `structs.tsv`, other-owner and existing branches unchanged.
- **Curator:** independently confirm both source SHA, native eight metadata/window SHA and 9 V9/native call rows; review correction to 17H 'handler unproven' and overlap with A/T014 before selective adoption under the existing study ID only.
- **Next lawful cursor:** identify instruction-exact EH state covering `0x45F5F9` against the 2 native try ranges and actual exceptional continuation; separately inspect legal child `vptr+8` producer. No dynamic catch, crash, leak or rollback claim without an independent authorized measurement.