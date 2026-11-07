# T009 battle_fast duplicate semantics — target native chain

更新: 2026-10-07 継続監査30 checkpoint 2

## 結論
[CONFIRMED-TARGET]
迫真戦記0.67同梱targetでは、context.dat の重複 `battle_fast` は **先勝ち(first insertion wins)**。source line 42の `battle_fast=on` が有効で、line 83の `battle_fast=off` は同一generic property keyの重複として追加されない。runtime effective値は **on**。

## native chain
1. target context inventoryはactive assignment 204 / unique key 203で、唯一のactive duplicateが `battle_fast`:
   - line 42: `battle_fast = on`
   - line 83: `battle_fast = off`
2. T005で確定済みのnamed-structure parserでは、current structure property tableがglobal `0x8797E0` に設定される。
3. special parser registryに `battle_fast` は存在しないため、通常のgeneric property fallback parser VA `0x505210` を通る。
4. `0x505210` はcurrent property tableへ nodeを作り、RB-tree/map insertion helper VA `0x463280` でinsertする。
5. `0x463280` は既存key発見時に既存nodeを返し、candidateを追加/置換しない **insert-if-absent**。したがって同一structure内のgeneric property duplicateはfirst-wins。
6. runtime context string lookup VA `0x46F6F0` は `context` structureとrequested keyをlookup helper `0x465060` へ渡し、保存済みproperty nodeからstring値を返す。
7. battle_fast loader VA `0x45A4D9..0x45A50E` は fallback `off` で `battle_fast` を `0x46F6F0` に問い合わせ、結果を literal `on` と比較して runtime byte `0x8797C8` へ保存する。
8. property tableには最初の `on` が残るため、target runtimeのbattle_fastはtrue/on。

## 注意
- 2017独立parserのContextParseはsource順overwriteでlast-winsだが、これはtarget nativeとは異なる世代/実装。strict targetへ移植しない。
- first-winsを全てのspecial/list propertyへ一般化しない。ここで確定したのは `battle_fast` がgeneric property pathを通ることと、そのduplicate挙動。

## 再実装
- target profileのgeneric structure property tableはinsert-if-absentを基本とする。
- context source assignment列は保持してよいが、effective generic keyは最初の登録を採用する。
- target 0.67では `battleFast=true` を期待値とする。

## 証拠
- `evidence/T009_CONTEXT_INVENTORY.json`
- `data/T005_FORMAL_GRAMMAR.md` の generic property first-wins 確定部
- `exe/T005_SCENARIO_PROPERTY_SEMANTICS.txt`
- `exe/T005_SPECIAL_REGISTRY_LIST.txt`
- `exe/T009_CONTEXT_LOOKUP_HELPER.txt`
- `exe/T009_CONTEXT_DISASM.txt`
