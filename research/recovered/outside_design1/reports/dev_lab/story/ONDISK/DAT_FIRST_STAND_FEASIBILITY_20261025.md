# ON-STAND-005｜DAT優先でのスタンド自動発現と奪取：実証境界

2026-10-25 JST / OWNER: ONDISK storyのみ / 状態: STATIC SOURCE + PARSER PASS、GAME LIVE NOT RUN。
原作の Vahren.exe / 本編 DAT / 共有 MASTER / 他レーンのコードは変更していない。

## 決定と未解決を混同しない
- [USER_FIXED / 2026-10-25再確認] 召喚者中心の射程外へ移動しない、親とスタンドのHP/被ダメ完全共有。
- [USER_FIXED / 2026-10-25再確認] スタンド自身のパンチなどは物理攻撃として使用可能であり、**他のスタンドにも有効**。**普通の人間の物理攻撃はスタンドに通用しない**。旧『スタンド自身の物理攻撃不可』は撤回済み。
- [USER_DESIRED] 戦闘開始時の自動召喚、終盤の敵によるスタンド奪取。
- [LATEST] 攻撃側の完全な仕様・DAT候補は `STAND_DAMAGE_MATRIX_20261025.md`、追従の最新は `FOLLOW_AI_RESEARCH_20261025.md` にあり、本資料の旧プロトタイプ解説より優先。
- [PROPOSED] DATで大部分を動かし、DATでは証明困難なHP同期と厳密な追従だけにフックを最小化する。

## 現物で確認した、再利用しやすいDAT
- `scenario1.dat` L29: `fight = fev1`。他の既存スクリプトが通常戦闘イベントを所有している。
- `100_イベント汎用/event_battle.dat` L1-9: `event fev1`。既存処理を置換/上書きしない。
- `50_その他新システム/siki_iwana.dat` L25-45: **独立した `story` + `fight = on`** で戦闘開始処理ができる。
- `30_スキル/F22_召喚を使ったトーク.dat` L231-251: 独立 `story fight=on`→`battleEvent`→`rif`→`skillTroop` の実例。
- `100_イベント汎用/event_battle.dat` L376-379: `skillTroop(znm,znm_board,dead_ok)` 強制スキル発動の実例。
- `10_ユニット/B_2323_リュージ騎士団.dat` L198-213: `func=missile`→`func=summon` + `add=` の実例。
- `Ai戦闘制御_軍楽隊なし版.dat` L554等: `removeSkill` と `addSkill` の実例。
- `10_ユニット/B_2_クレイジーサイコホモ.dat` L324等: `getLife(boss)<50` で段階的なボス強化。
- `10_ユニット/24_ヒューマンダストクルセイダース.dat` L1-53: ONDISKは `starchira` を既に使い、Lv25で `sp_world_ondisk` を覚える。原作のスタンドは別召喚Unitではない。
- `20_クラス/24_26_ONDISK_二軍_原理.dat` のa240系に召喚可能数の明示なし。 `context.dat` L162は `unit_summon_min=0`。**自動召喚はまず召喚枠不足を解決する必要がある**。

## 追加で確認したエンジンの公開仕様
- `story ... { fight=on }` またはscenarioのfightイベントから `battleEvent(...)` を登録できる。battle eventの `if` は一回、`rif` は繰り返し。
- `skillTroop(unit,skill)` は強制発動。 `func=summon` の `yorozu=troop3` はプレイヤー術者の独立召喚部隊操作。
- `getDistance(unit,unit)` は距離、`moveTroopFix(stand,owner)` は追尾**指示**（上限を瞬時に保証しない）。
- `removeSkill(unit,skill)` は戦闘スキルを削除。`removeTroop` は戦場部隊を消去。`skillTroop(thief,summon)` で敵が模倣Unitを召喚する。
- `getLife(unit)` は残りHP百分率のみ。戦闘中の「別Unitに受けた1ダメージを親HPから正確に減らす」命令は現時点で見つかっていない。
- `func=status,type=1,attr=summon_max,time=1` は召喚枠を自分に増やす候補。実際に `addSkill` 直後の召喚に適用されるかはLIVE-VERIFY。
- 出典: https://w.atwiki.jp/vahren_ency/pages/832.html , /944.html , /405.html , /379.html

## 作成した隔離DAT
- `stand_proto/stand_summon_fixture.dat`: skill×3（召喚起点・召喚本体・`standhit`打撃）＋stand class、`yorozu=troop3`、`satellite=64`。
- `stand_proto/stand_autostart_theft_fixture.dat`: 個人召喚枠buff／`story fight=on`／`battleEvent`／`skillTroop`による一回限りの発現、エンジン内蔵`satellite=64`による追従、半HPの仮敵が発動する「奪取演出」。
- 「奪取」は`removeSkill`で元使い手の技能を無効化→`removeTroop`でスタンドを消去→敵が**別IDのクローンを召喚**。本物のUnit親ポインタ移転ではない。
- 【注意】攻撃ヒットで奪うのではなく **仮敵HP半分で発火する scripted prototype**。Hit検出と対象への紐付けは未実装。
- DAT parserで各定義を抽出できても、Vahren.exeで動く証拠ではない。既存原作スキル/本体は変更しない。

## スタンド再現の二案
A. [別Unit・独立操作] DAT-firstの本命。見た目・強制召喚・模倣奪取は可能性大。射程は断続的な追尾のみ、正確な被弾共有不可。
B. [術者本人の技能+スタンド画像] 本物のHP共有（術者1Unitだけ）・スキルを奪う演出はDATだけで可能性大。ただし独立した可動/標的/被弾ユニットがない。
優先推奨: Aを組み立て、厳密なHP/射程/特定Stand親子関係のみ最小DLL拡張。BはDAT完全版が必要なら代替。

## 失敗させない実機試験
1. 隔離したスクリプト読込で `on_stand_capacity` が召喚枠1を与えるか、戦闘直後にスタンドが一度だけ出るか。試験失敗なら元Unitの`summon_max=1`の隔離パッチ。
2. 召喚する部隊`on_stand_star`が `yorozu=troop3`でプレイヤー操作可能か。`getDistance`で可視的に距離取得できるか。
3. `satellite=64` の追従を術者の移動・敵追跡・直接プレイヤー指示・障害物で実測。Rを越えない保証ではない。`moveTroop`との比較は隔離fixtureでのみ実施し混用しない。
4. boss 50%到達→ONDISK技能削除、stand消去、bossの複製召喚。勝利/退却/戦闘再入場時の技能回復・HP・召喚枠のリセットを確認。
5. 呪文ヒットで奪取する本番仕様は別Task。 `afterhit` と `countSkill` によるmarker案は標的ID取り違えのリスクが高いため、未完成。
6. 召喚Unit死亡→本体へ正確にダメージ転送できるかはDATに根拠不足。DLL側戦闘ダメージhook経路の所有者に契約照合が必要。

## 完成境界
現在達成したのは**原作・公開資料調査 + Synthetic DAT/parser静的検査**。原作ゲーム本編での召喚/追尾/奪取/HP共有の成功は0件。次チャットでもLIVEと報告しない。