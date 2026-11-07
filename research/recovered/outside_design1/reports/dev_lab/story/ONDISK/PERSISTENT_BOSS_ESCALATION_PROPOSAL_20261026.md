# ON-STAND-015｜放置すると永続的に強化されるボス（候補案）
更新：2026-10-26 JST｜状態：USER_CANDIDATE / STATIC FEASIBILITY。既存ストーリーの確定設定ではない。原作DAT/EXEは変更しない。

## 発想と現時点の判断
- [USER_CANDIDATE] スキル奪取・付与を戦闘終了後も永続化し、放置すると次々と能力を集めて強くなるボス。
- [CONFIRMED DAT API] addSkill(unit,skill) はユニットの技能リストを変更する（戦略側のイベントでも実使用）。set/addSkill/removeSkill/eraseSkillの戦略・戦闘区別は SKILL_BATTLE_SCOPE_NATIVE_DAT_20261026.md。
- [CONFIRMED DOC] unit構造体Wikiは宝箱/addSkillで獲得した技能は転職で残ると説明。数値変数はセーブされる。永久強化の記録にゲームセーブ内の数値フラグを使う。global.savへのgwriteは別セーブへ波及し得るため不採用。
- [CONFIRMED ORIGINAL] event_world.datの isNewTurn/getTurn (L74以降、L796/853/893) でターン限定処理、addLevel (L818等) でCPU強化が実在。event_world.dat L1748 の addSkill(fmrim,b_fmrim_astk,b_fmrim_bb,b_medama) もワールド側のスキル付与事例。特定の新ボスに適用できたという意味ではない。
- [IMPORTANT] event_world.dat L71–84の原作コメントは「背景付きイベントによりworldイベントが二重読み込みされ、2回目もisNewTurnの条件を満たす」問題を警告。**同一ターン多重実行を避けるステージ/処理済ターンのフラグが必須**。
- [UNVERIFIED] addSkillしたボスの技能が、原作ゲームでのSAVE/LOAD、転職、死亡・再出現、イベントによる再構成を跨ぐ全状態で残るかは未実機検証。

## 追加候補：CPU対CPU簡略戦闘でも能力収集（ON-STAND-016 / 2026-10-26）
- [USER_CANDIDATE] 単にターン経過で成長するだけでなく、ボスがCPU他勢力との簡略戦闘を繰り返して能力を収集し、プレイヤーと遭遇したときに思いもよらぬ技能を獲得している展開。
- 公開Wikiのscenario.worldは戦闘終了時も呼ばれる。storeBattleSpot/AttackPower/DefensePowerは簡略戦闘後に使用可能。storeTodoUnit/AliveUnitは簡易可だが**終了後worldで参加者が見えるかは未確認**。通常のfight/battleEventの技能命中処理と混同しない。
- 簡略戦闘ではボスと技能保有者の参加＋勝敗/生存を条件に事後イベントで**取得技能をボスへ恒久追加**する案。能力が当該戦闘の勝敗に反映されるのではなく、次戦以降の増強となる。
- 原作で参加人物・勝敗・戦闘ユニークIDが取れない場合は、勢力名だけで勝手に奪うことはしない。具体的技命中、被害者からの永久削除、簡略戦闘計算に新能力を利用する方法は別の研究。
- 詳細な証拠、タイミング・二重計上・ネイティブ拡張の境界は SIMPLIFIED_CPU_BATTLE_DISC_RESEARCH_20261026.md。

## 最小構成：DATで永続成長
- ワールドイベントの isNewTurn と getTurn、現在の段階を保持する数値変数 boss_growth_stage で一度だけ判定。
- たとえば（全部PROPOSED）：第1段階（5ターン）＝新魔法、第2段階（10ターン）＝新召喚、第3段階（15ターン）＝強い防御/遠距離、第4段階（20ターン）＝最終能力。
- 各段階で addSkill(boss,stage_skill) と必要に応じ addStatus(boss,attack,値)/addLevel(boss,値) を利用。段階更新 set(boss_growth_stage,N) は**実行が成立した場合に一度だけ**実施。すでに所持する技能は重複追加しない。
- スキルだけでなく、レベルとステータスが上がるパターンも原作コマンドで成立し得る。
- ボスが不在/死亡、プレイヤー勢力に参加、すでに討伐済み、またはシナリオ対象外なら増強しない条件が必要。
- **「放置で強化」**を、単に経過ターンならT=5/10/15/20でよい。ボスが出現してからの経過時間なら出現時ターンを保存して差分判定が必要。
- ミッションにしたい場合は、補給拠点や弟子を攻略すると成長が遅れる/新技能が得られないなど、プレイヤーの対抗手段を明示する。

## もう一つの構成：永久DISC技能吸収
- 能力を盗まれてもその戦闘だけ失う既存方針（ON-017）とは別の、**特殊ボス限定の永続奪取ルール**として扱う。
- ボス側は addSkill で獲得技能を保存する。元のキャラまで永久に奪う場合、eraseSkillで消しても既存class.skillやunit.learnから再取得される可能性があり、元技能構造との整合確認が必要。
- 当初は**ボスが段階的に新技能を覚えるだけ**にする方が簡単で安全。通常DISCはこれまで通り戦闘限定。新たな永続技能獲得は大ボスの固有ルールとする案。
- 「奪われた技能は被害者から永久に消えた」まで実装する場合は、元スキルの再付与経路（転職、レベルアップ、リーダースキル）とSAVE/LOADを別途検証。

## 難易度調整・演出（候補）
- 無限に攻撃/HPを増やすより、段階数を4～5に制限し、各段階で技の性質が変わる。単純な耐久増だけでは理不尽になる。
- プレイヤーに進行を告知（噂/情報イベント/ボスの技能欄）。未告知の突然の壊滅的強化は避ける。
- 通常の召喚技は元技能DAT無改変、スタンドはHP共有・射程・物理攻撃耐性とDISCルールを引き続き厳格にする。

## 参考・検証
- https://w.atwiki.jp/vahren_ency/pages/696.html (addSkill/addStatus、数値変数のセーブ、worldイベント)
- https://w.atwiki.jp/vahren_ency/pages/379.html (転職時にもaddSkillで追加したスキルが残る)
- https://w.atwiki.jp/vahren_ency/pages/399.html (isNewTurn/getTurn)
- https://w.atwiki.jp/vahren_ency/pages/614.html (数値変数のセーブ・set)
- 技能の追加処理、ターンイベント、セーブ/ロード、状況別重複、イベント二重発火は独立テストと隔離原作実機で検証が必要。現段階では新ゲームMOD実装なし/実機PASS0。