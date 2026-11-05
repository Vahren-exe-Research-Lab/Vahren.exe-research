# T017 BGM property consumer semantics (2026-10-07)

## Event `bgm = none`
[CONFIRMED-TARGET] Battle playback core `0x48F080` has a dedicated event-property branch. At `0x48F342` it requests key `bgm` with structure kind `event` through `0x4647D0`; the returned string is copied unchanged into the common custom-BGM temporary.
[CONFIRMED-TARGET] At `0x48F443` only an empty result skips the custom path. Any non-empty value is passed at `0x48F473` to playback core `0x4BDE40`. There is no comparison with literal `none` in this branch.
[CONFIRMED-TARGET] `0x4BDE40` treats a dotless name generically: probe `.mid -> .mp3 -> .ogg`, then the generic DirectMusic failure/reset path when all candidates are absent. FULL assets contain no `none` stem.
[HAKUSEN] All six static `bgm = none` occurrences are battle/event setup. Representative events also explicitly call `playBGM(none)` before selecting a real event track.
[REIMPLEMENT] Do not implement event-property `none` as a parser keyword. Preserve it as an ordinary non-empty identifier and let normal audio resolution/failure semantics silence/reset BGM.
[VERIFY] Exact final AudioState equivalence to `stopBGM` remains dynamic-only; the route into the missing-name reset path is static-confirmed.

## Spot `bgm = @`
[CONFIRMED-TARGET] Sole RHS `@` is a distinct generic-assignment case, not an ordinary nonnumeric token: `0x50537A -> 0x503460` returns nonnumeric sentinel `0x80000008`; the parser then compares the token with exact `@` (`0x62C42C`). On match it copies literal `"@"` to the field-node string but skips storing the sentinel, leaving node scalar/type slot `+0x20=0`. This is the target-era representation of the explicit-null/suppressor marker.
[CONFIRMED-TARGET] Spot BGM resolves key `bgm` via `0x597A20 -> 0x4693F0`. `0x4693F0` constructs `bgm@<variant>`, asks `0x464290` whether that property exists across the structure/super chain, and if present returns it through `0x4647D0`; only when absent does it request base `bgm`. Thus a qualified `@` suppresses base fallback, and a child/base `@` found by `0x4647D0` suppresses parent fallback.
[CONFIRMED-TARGET] `0x4647D0` returns a found field by copying node string `+4` and scalar `+0x20` unchanged. It does not normalize RHS `@` to empty. In the battle spot branch, `0x48F3CE -> 0x597A20` copies that string; `0x48F443` tests its length and any non-empty value goes to `0x4BDE40` at `0x48F473`. Therefore `bgm=@` reaches the normal audio resolver as literal `@`, not empty string. With no `@` audio asset, it follows the ordinary missing-name resolver/reset semantics. This is analogous in outcome, but not representation, to an explicit no-BGM marker.
[CONFIRMED-TARGET] The literal `@` at `0x633DB8` inside `0x4693F0` is the property-name qualifier separator and is distinct from RHS explicit-null token address `0x62C42C`.
[REIMPLEMENT] Preserve a tri-state property model (`Unset / ExplicitNull(@) / Value`) for merge semantics, but do not globally rewrite ExplicitNull to empty text before target-compatible consumers. Generic property selection is qualified-key-over-base, with each lookup current-structure-over-super-chain; a found ExplicitNull stops fallback. Consumer-specific handling may then observe the literal marker.
[VERIFY] Exact audible/current-track state after missing literal `@` remains part of the same dynamic audio reset fixture as other missing dotless names; the static parser/merge/consumer route is now closed for spot BGM.

## Evidence
- `exe/T017_BGM_PROPERTY_XREFS.txt`
- `exe/T017_BGM_PROPERTY_CONSUMER.txt`
- `exe/T017_BGM_PROPERTY_FALLBACK.txt`
- `exe/T006_AUDIO_HELPERS.txt`
- `data/T005_FORMAL_GRAMMAR.md`
- `data/T017_BGM_REFERENCE_AUDIT.txt`
