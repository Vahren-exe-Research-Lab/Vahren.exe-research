# T033 legacy scenario identity native notes

Target: bundled 迫真戦記 0.67 Vahren.exe, read-only static analysis.

## 1. current scenario persistence
[CONFIRMED-TARGET]
- new-game/scenario initializer VA 0x45C1A2..0x45C1BE takes engine scenario runtime string `engine+0x34` and writes it to persistent symbol `@scenario` via 0x463610.
- normal-load VA 0x45F01D..0x45F034 performs the inverse: fetch `@scenario` through 0x463CA0 and copies its string into engine `+0x34`.
- Therefore scenario identity is a persisted string, not only an ephemeral pointer to a declaration node.

## 2. undeclared ID lookup behavior
[CONFIRMED-TARGET]
- immediately after restoring `engine+0x34`, normal-load uses generic field accessor 0x4647D0 with structure kind `scenario` and a property key such as `zone`.
- 0x4647D0 first resolves the top-level structure registry, then searches the requested structure identifier. If the structure id is absent, VA 0x4649C6..0x464A24 constructs the normal empty/default field result and returns; this lookup path does not itself hard-crash.
- if structure exists but the field is absent, the accessor follows the `super` chain up to 0x32 iterations before returning empty/default.
- Thus a save carrying an undeclared scenario string can at least pass this individual lookup boundary; whether the whole load/world reconstruction remains playable depends on later consumers and saved runtime graph state.

## 3. T033 implication
- rsc2-rsc5 have no `scenario <id>` declaration in the 0.67 release corpus, but they cannot be deleted merely because current parser input lacks declarations.
- old-save/current-load compatibility must be tested separately: current scenario string is restorable, and missing definition lookup is tolerant at this boundary.
- current new-game reachability still requires scenario-select/registry enumeration proof.

[EVIDENCE]
- `T014_NORMAL_LOAD_PROBE.txt`
- `T009_SCENARIO_CONTEXT_FOCUS.txt`
- `T005_FIELD_LOOKUP_FULL.txt`
- `T005_SCENARIO_REGISTRATION_PROBE.txt`
