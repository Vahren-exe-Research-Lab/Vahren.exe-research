# ON-STAND-016｜CPU同士の簡略戦闘でもDISC奪取・永続成長するボス（研究）
2026-10-26 JST。状態：ORIGINAL DAT STATIC CONFIRMED + WIKI SCRIPT API CONFIRMED / GAMEPLAY NOT RUN。ユーザーの発想はUSER_CANDIDATEであり完成企画への採用未確定。
対象は迫真戦記ver0.67。原作DAT/EXE、研究A～F・REA・MASTER_LEDGER等は未変更。

## ユーザーの発想と要点
CPU勢力同士の戦闘は画面を開かず「簡略戦闘」で処理される場合がある。そこでも、スタンド能力等を奪うボスが戦闘を重ねるほど能力を収集し、次にプレイヤーが遭遇したときに新しい技能を保持する仕組みを作りたい。
**通常戦闘の実ヒットによるDISC奪取**と**簡略戦闘の事後判定によるDISC獲得**は別アダプタにして、最終的な技能取得・同名分身/スタンドルールは共通化する。
- 実技能のヒット判定が簡略戦闘でも個々に評価される、という証拠はない。原作fight/battleEventだけが簡略戦闘で必ず呼び出される、とも証明されていない。
- だから簡略戦闘では、**戦闘参加＋勝敗/生存＋既知の奪取可能技能**に基づくイベント判定で疑似再現を推奨する。
- この獲得処理は**戦闘結果が確定したあと**。獲得した新技能がその直前の簡略戦闘のダメージ・勝敗を変えることはできない。次回の戦闘以降に活躍することを狙う。

## 簡略戦闘でも使える公開DAT API（原作Wiki）
- scenario.worldのeventは「ターン進行時および**戦闘終了時**」に評価される（ヴァーレントゥーガWiki https://w.atwiki.jp/vahren_ency/pages/696.html /pages/534.html）。
- storeBattleSpot(@v): 直前の戦闘領地。**簡易戦闘後でも正確に代入**。
- storeAttackPower(@v), storeDefensePower(@v): 直前の攻撃側/防衛側ホスト勢力。**簡易戦闘でも代入**。
- clearBattleRecord(): 上記「直前の戦闘記録」を消す。原作/他イベントが同じ記録を参照するため、本拡張が勝手に呼ぶのは危険。
- storeAliveUnit(unit/class,@v), storeTodoUnit(unit/class,@v): **簡易戦闘可**の戦闘Unit列挙。後者は死亡者も含む。ただし「現在の戦闘シーン」が前提なので、**戦闘終了後world呼出時にも参加者が保持されるかは未確認**。戦場用のstoreRectUnitは明示的に**簡易戦闘不可**。
- isWorld(): 世界地図／簡易戦闘中で1。isEvent(): 戦場で1。worldへ復帰した通常戦闘もisWorld=1になり得るため、**isWorldだけで簡略戦闘と通常戦闘の事後イベントを識別しない**。
- isNpc(勢力A,勢力B): 両側ともCPU勢力なら1。isWarは過去の交戦履歴であり「直前戦闘で勝ったか」ではない。直前攻撃側はisInvade（条件制約あり）。
- set/数値変数とaddSkillは戦略側永続技能成長に利用。文字変数（@xxx）は通常セーブされないので、過去のDISC獲得技能名を長期保持する場合は数値フラグ・所持技能などへ写す。Wikiはsetud/storeudで文字列保存もサポート。
URL: https://w.atwiki.jp/vahren_ency/pages/614.html , https://w.atwiki.jp/vahren_ency/pages/399.html , https://w.atwiki.jp/vahren_ency/pages/696.html , https://w.atwiki.jp/vahren_ency/pages/534.html

## 迫真戦記ver0.67の使用例（原本読取確認）
- a_default/script/100_イベント汎用/event_battle.dat L1-8: fight入口fev1でisEvent()の両値を許し、他のシナリオ戦闘イベントを呼ぶ。
- a_default/script/Ai戦闘制御_軍楽隊なし版.dat L307-333: fight=onのstory change_form_battleが、isWorld()==0を条件に本格CPU陣形処理を開く。L407付近には **「COM同士の戦いでは起こさない」** コメントあり。既存陣形制御のbattleEventを簡略戦闘に流用してはならない。
- 同ファイル L419-422、L491-494: storeAttackPower/storeDefensePowerによりホスト勢力を判定。勢力情報は実ユニット参加の証明ではない。
- a_default/script/2001_イベント_ボス/event_51_ボス死亡時.dat L126-141: storeAttackPower + storeDefensePowerで直前戦闘勢力を取得する実例（このイベントの発火時相は別）。
- a_default/script/45_内政_防衛兵器/siege_system.dat L84-118: 攻撃/防衛ホストの勢力に応じ処理を分岐。
- a_default/script/event_world.dat L71-84: **worldイベントが同じ新ターン判定で複数回評価**される場合の対策を説明。戦闘後イベントでも同じ結果の二重付与を必ず防ぐ。
- a_default/script/event_world.dat L1748: world経路でaddSkill(fmrim,...)を実際に使用。

## 推奨する二経路と共通DISC取得処理
【通常戦闘での実ヒット】
Hit → attacker/victim確定 → 対象の戦闘用技能剥奪 → 召喚物（単体型のみ）の消滅 → 戦闘中の付与 → 必要なら次ターン以降の永久報酬へ記録。

【CPU同士の簡略戦闘】
簡略戦闘の結果確定 → 戦闘領地と攻防ホストを取得 → **実際の参加ユニット（ボス・被害者）と勝敗/生存を確認** → 技能/確率・対象選定（スキルIDは既知でよい） → addSkillなどによりボスへ一つ報酬 → 保存済みの重複防止フラグを更新 → 次戦以降でその技能を使う。

「ボスが所属する勢力が戦争した」だけで離れた場所のボスに全敵技能が自動転送される誤仕様にはしない。もし「配下が技能DISCを持ち帰る」別仕様ならボス本人が不在でも可だが、そのルールはまだPROPOSED。
勝敗は領地の占領先と双方の戦闘結果で評価する候補。ただし **防衛側が領地を守っただけで明確な圧勝とは限らない**。同一turn・同一spot・攻防powerの単純キーでは別の戦闘が重複し得る。ネイティブ戦闘IDまたは独立イベント通番の取得を実機で検証。
キャラクターの所持していない技能まで奪取できると主張しない。未知/汎用skillTagパラメータで動的追加できるかも未確認。候補技能を定義した対応表を優先。
**一回の簡略戦闘につき最大1技能**、実際にその被害者が所有すること、技能が未取得であること、戦闘時点に参加者がいることを判定する案（PROPOSED）。ボスの勝利が必須か、敗北でも生存すれば奪えるか、譲渡元の恒久技能を本当に削除するかは未決。

## 実装とリスクの切り分け
| 仕組み | 必要技術 | 判定 |
|---|---|---|
| 概略戦闘後にワールドイベント実行 | DAT world + battle record | 仕様Wikiあり、原作個別実機 NOT RUN |
| CPU攻防の所属勢力・戦場領地取得 | DAT storeAttackPower/DefensePower/BattleSpot | 簡略戦闘でも取得可能との文書証拠あり |
| 本当に戦ったボス・被害者の正確な参加 | DAT storeTodoUnit/AliveUnit（簡易可）／事前捕捉 | **事後worldで有効か未確認** |
| 当該戦闘での勝敗・倒した相手・ヒット判定 | 戦場獲得/被害情報の検証、場合によってnative | 現時点で完全な技命中再現証拠なし |
| ボスの新技能を恒久取得 | DAT addSkill + 永続フラグ | 元ゲームに戦略側addSkillの実例あり |
| 技能を奪われた側から永久削除 | DAT eraseSkill + class/learn再習得検証 | 入手より難しく、デフォルト未採用 |
| 新技能を簡略戦闘そのものの勝敗計算へ反映 | 簡略戦闘算定式の調査/修正 | **別課題**。既存技能が計算に使われるか未確認 |
| スタンドのHP同期・物理無効・絶対射程 | 通常戦闘側別ルール | 既存P0条件を崩さない |

## 最低限の検証（原作EXE/DATはコピーで実施）
1. CPU-AがCPU-Bへ侵攻し簡略戦闘。worldイベントが戦闘後に何回走るかを記録。直前戦闘spot/攻防ホスト取得・clearBattleRecordなしの寿命を確認。
2. 簡略戦闘でのstoreTodoUnit/AliveUnitをイベント中・world後に読む。ボスと被害者の参加を確定できるか調べる。**不明なら勝手に獲得を許可しない**。
3. 攻撃成功、攻撃失敗、時間切れ、防衛維持、部隊全滅、退却、援軍参加、連続２戦、ロード直後を区別して勝敗・重複を確認。
4. 当該ボスが実際に参加して勝利した時だけ、既知技能1つをaddSkillで永久取得する。次戦・次ターン・SAVE/LOAD・転職・死亡後でも無断増減しないか観測。
5. 本格戦闘で実ヒットのDISC奪取とワールド側事後報酬が二重に発生しないように共通IDを付ける。
6. UIのスキル追加表示はSKILL_THEFT_UI_SYNC_SPEC_20261026.md、戦闘限定/永続はSKILL_BATTLE_SCOPE_NATIVE_DAT_20261026.mdを参照。固有型と量産型の召喚物扱いはSUMMON_DISC_REMOVAL_POLICY_20261026.mdを継承。

## 追加調査後も未確定
- worldイベントの戦闘終了後の実際の呼出タイミング（領地支配更新・Unit所有/戦場ロスターデータ消去との前後）。
- 「CPU同士の簡略戦闘」でもfight=onが呼ばれるか（誤用防止のため未実証とする）。
- storeTodoUnit/AliveUnitの「簡易可」が世界イベントの**戦闘終了後**にまで及ぶか。
- 現行の原作簡略戦闘が所持技能の効果を勝敗計算にどう考慮するか。
- uniqueな戦闘結果IDをDATから取れるか。戦闘毎の重複防止は実機で要設計。
- 今回は対象DATもEXEも未修正、原作CPU vs CPU実機テスト0件。設計・静的確認だけで実装完了とは扱わない。