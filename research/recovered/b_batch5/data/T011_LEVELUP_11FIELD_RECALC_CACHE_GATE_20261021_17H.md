# 新B T011｜レベル到達時の11フィールド更新と条件付き関連キャッシュ再構築（2026-10-21 17時台）
- 研究ID: `B-20261021-17H-01`。owner=B/T011（T012参照）。`STATIC / INFERRED / VERIFY / NOT READY`。新Task DONE0、B READY0、E統合0。
- 対象原作: ver0.67の記録SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。今回はBUILD_MANIFEST.jsonから確認、原作EXE再ハッシュ・起動なし。
- 根拠: 既存Ghidra検索基盤`search.py function 0x58A650 / 0x58AFA0`と`callers`、保存擬似C; search_index BUILD_MANIFEST=PASS。code SHA `0x58A650=6B530AC4D4372949EB50315A602773E539D3BAC1BB7308923AD87342CDF8F634`; `0x58AFA0=01C7EACF4F340752F6CEC151D27AE8D2CFA6A31D19143F76E21A65BB93129033`。
- 追加ASM独立照合・原作DAT個別Skill到達・CPU実負荷計測・Gameplay動的実行なし。callsiteはGhidra直接CALL索引であり間接到達網羅ではない。

## 1. EXP閾値処理の11個の関連field
1. `0x58A650`入口はGhidra擬似Cで`*(uint*)(Unit+0x170) <= *(uint*)(Unit+0x16C)`の**unsigned**閾値判定。従来T011 03:09資料の既存知見で再計上しない。
2. `level_max`設定読込後、0なら`0x0046F4C0(Unit+0x1A4,100)`を採用する候補経路。上限の実効値や比較対象が意図する設定意味はVERIFY。未到達ならレベル上昇しない。
3. レベル上限を満たす場合、`Unit+0x168`を先に1増加し、11個のフィールドへの**ポインタ**をstackに構築する。候補集合は`Unit+{0x178,0x17C,0x180,0x184,0x188,0x18C,0x190,0x194,0x198,0x19C,0x1A0}`（計11）。
4. 対象ポインタは`uStack_164`を4ずつ増やし`uStack_164 < 0x2C`で11周する擬似C。stack上の`+0x190/+0x194`格納順は通常の昇順と異なって見えるため、元ASM・ABI上の配置順はVERIFY。
5. 各周回はclass/property検索(`FUN_00464290/FUN_004647D0`)を経由して`**(int**)((int)aiStack_118+index) += iVar7`を行う。条件付きで別の取得値に上限調整する分岐もあるが、全11個が無条件に同じ値だけ上昇する証明ではない。小数丸め`0x5D1B80`・対象キー・offsetごとのgame表示名はVERIFY。

## 2. レベルごとに関連定義を再評価する候補
6. 11fieldループの後に直接CALL `0x58AE65→0x58AFA0`、続いて`0x58AE6C→0x58A400`があり、その後に`+0x170<=+0x16C`の条件へ戻る。閾値が連続成立すれば1回の入口で複数levelを処理する構造候補。再計算・キャッシュ処理の順序をまとめて最後に1回にする実装は原作と差異を生む可能性がある。
7. `0x58AFA0`の保存擬似C前段は`(local_64==0) || (Unit+0x168 < local_18)`でloopを抜け、成立しない場合に`0x58C0E0`へ進む。直後の`0x469390()`非zero枝でtree sentinelと見られる`Unit+0x15C`指す構造を初期化し、`Unit+0x160=0`を書き、`0x586320`等を実行する。これは条件付き変更であり、**毎level必ず全Skillが消える**と断定できない。
8. 同関数の後段にはclass/property検索と`0x58F7E0`, `0x463280`（既知の木登録候補）がある。該当routeはclass/skill再構築の候補だが、effective Skill内容・見えるUI・runtime identity・副作用は未確定。
9. `0x58A650`への直接CALLは`0x4723DE(0x471E80)`, `0x4AB49B(0x4A7A90)`, `0x551FD3(0x551E50)`の3箇所。うち`0x551E50`経由は先行B研究と重複するため新発見として再加算しない。
10. `0x58AFA0`は直接CALLが9site/7caller関数:`0x460940`2箇所、`0x4667B0`、`0x4F9510`2箇所、`0x575110`、`0x582D90`、`0x588470`、`0x58A650`。これは複数の入口で参照される静的事実で、gameplayでの到達は不明。

## 3. 既存差分・検証と再開
- 03:09の`B-OFFLINE-20261021-0309-01`はexp-like fieldと閾値関数の前後関係、今朝09時台までの研究はunit生成系。本件の**新規限定部分**は11field更新loop・その後の条件付き`+0x15C/+0x160`再構築候補・3caller/9callerのsite inventory。元IDは再計上しない。
- PC B所有`T011_DATA_MODEL.md`の既存節末尾と、B data/*.mdで`58AFA0`の検索（本日PC回収資料のみヒット）を先行。最新E checkpoint195、owner変更なし。全Task/全史料の意味的重複未網羅につきNOT READY。
- GOLDEN DESIGNED/NOT RUN: 原作合法UIでLv閾値前後、1回で2段階上昇、Lv上限、class/change境界、技能リストbefore/after、11field相当の表示stats/HP/MPと次tickを同EXE/DAT/SAVE/map/seed/input/capture SHAで比較。不可視内部treeのみのfixtureはINELIGIBLE。旧原作Gameplay Golden PASS=0、strict MATCH=0。
- 未解決P0: 11field配列の本当のASM順序とgame表示名、class変更判定`0x469390`の戻り意味、`0x58AFA0`での+0x15C ownerと参照保持、`0x58F7E0`/0x463280登録の結果、level_max=0やoverflow・RNG、経験値共有/召喚Unitの継承。
- 次: 原作既保存ASMの許可済み窓で`0x58AFA0`の+0x15C clear分岐と`0x58A650`11offsetの実store順が既存にあるか調査。無ければSTATIC/VERIFYのまま。拒否済み0x5710C0範囲、08時コピー拒否、17:14間接SQL拒否には触れない。
- 保存境界: B data/研究本文とB HANDOFFへの新規IDメタデータのみ、MASTER/他lane/rea_lab/dev_lab/原作/EXE/Git/Work/設定/スケジュール変更0。回収19ファイルとは別の新規研究1件。