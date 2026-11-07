# ONDISK編｜CURRENT HANDOFF
最終更新: 2026-10-26 JST。次のチャット/AIは**最初にこのファイルとMASTER.mdを読む**こと。
## 正本の場所
`[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab\story\ONDISK\`
入口：`../README.md`。下位：PLOT / CHARACTERS / STAND_SPEC / TASKS / stand_proto。
## 最新方針（2026-10-26 / ON-019：最優先）
**一般召喚の個体重複は許容**。ポケモン等の全召喚個体に新規所有台帳を作り、唯一性を完全保証する作業は P2 に延期。TNOKのチコリータは奪取時の消滅を基本的に目指すが、一般召喚で一時的に同種が複数存在する状況は完成ブロッカーにしない。**無関係の一般部隊を破壊する誤削除は容認したわけではない**。

**スタンドだけP0で厳格**：戦闘開始の自動召喚、絶対射程R、術者との単一HP、通常人間の物理無効・スタンド物理攻撃有効、DISC奪取時の即消滅、受領者を新しい召喚者・HP共有先として再召喚、戦闘終了の技能復帰。ユーザー確定と提案・未決を分類した**現行正本は STAND_SPEC.md の2026-10-26節**。単なる `satellite` 追従や独立Pythonテストだけで完成扱いしない。

## 2026-10-26最新版：ON-020 固有と量産の削除ルール
**優先して読む：SUMMON_DISC_REMOVAL_POLICY_20261026.md**。ユーザーはチコリータ/スタンドのような固有型なら、同名召喚物の一括消去を許容。一方、いんゆめくん`s_inyume`と**ALC役クッキー☆声優**の`s_toshino`（歳納人形）は多数召喚され、同名全消去は危険。一般量産型は**既存トークンをそのまま残し、今後の召喚を止める**ことを第一候補とする。原作CPUは`s_inyume_com0/1/2`、`s_toshino_com0/1/2`へ技能を変更するため、根元スキルだけでなくCPU用技能群すべてが封印対象。固有型の全消滅はゲーム実機未確認でありDAT構文と誤認しない。隔離Policyモデル`stand_proto/summon_removal_policy.py`＋新テスト9件、総70件PASS。元チコリータ同型他術者保護の旧厳密ルール（ON-018）はON-020で**完了必須条件から解除**。

[USER_FIXED / ON-021 2026-10-26] **「単体／量産」は現在の出現数ではなく元の召喚技能の定義で判定**。チコリータ・スタンド（単体召喚型）は同名が複数あっても消滅候補。いんゆめくん・歳納人形（量産型）は残数が1体でも消さず、根技能とCPU派生の新規召喚を封印。元ゲームのremoveTroopの挙動自体は実機未検証。SUMMON_DISC_REMOVAL_POLICY_20261026.md参照。

[2026-10-26 ON-022 / UI検討中] 技能奪取・付与時、戦闘中ユニット情報パネルと選択時のスキルアイコンを、戦闘で利用可能な技能へ追従させることを提案。奪取された側は非表示、受け取り側は表示、戦闘終了は元へ。元エンジンの技能増減DAT命令は存在するが、開いたままのパネルの即時再描画は未実証。reloadMenu(on)は勢力メニュー用で戦闘情報の更新命令ではない。最新仕様資料 SKILL_THEFT_UI_SYNC_SPEC_20261026.md。提案を原作の動作済み機能と混同しない。

[2026-10-26 ON-023 / USER_CANDIDATE] 「放置するとどんどん強化されるボス」と永続化DISCが面白い、という提案。まだ誰をボスにするか、仕様は未確定。原作では addSkill は所持技能を恒久追加し得る、world イベント isNewTurn/getTurn、addLevel、addStatus と、セーブされる数値フラグが存在。event_world.dat L71～84はワールドイベントが同じ新ターンで二重評価され得ることを警告。段階フラグとターンラッチを必須設計候補とする。**一時DISC仕様ON-017は変更しない**。参考 PERSISTENT_BOSS_ESCALATION_PROPOSAL_20261026.md。

- [ON-024 / USER_CANDIDATE / 2026-10-26] CPU同士の簡略戦闘でスキルを獲得するボスを提案。既存の戦闘中battleEventだけでは簡略戦闘対応にならないため、簡略戦闘の結果をワールドイベントへ渡す別経路を設計。Wikiはworldイベントが戦闘終了時に走ること、簡略戦闘後のstoreBattleSpot/AttackPower/DefensePowerをサポートすることを明記。storeTodoUnit/AliveUnitも簡略可だが**戦闘終了後に参加個体が取れるか不明**。実戦場の誰の技能が命中したかは再現せず、戦闘結果による疑似奪取を候補とする。ボス本人/被害者の参戦確認・同一戦闘の二重報酬防止・奪取後の恒久技能・次戦効果を分ける。SIMPLIFIED_CPU_BATTLE_DISC_RESEARCH_20261026.mdを参照。実機PASS0。

## ユーザー確定事項の最短要約
- ONDISKが「幽霊」を恐れて牢に籠る。帰国した**口マン爺（ロマン爺）**がスタンドを説明。牢から救い出す人物も。
- 遠野がラスボス。大陸を一周する長征。田所は仲間として遠野と対峙。
- 終戦：遠野の「正真正銘ッ！最後の時間停止だッ！！！」→田所をキス→止まった時の十秒→時間が動いても田所が応じたキスが続き、軍勢は武器を下ろす。憎悪と愛を両方描く。
- 候補：壁の目の隆起／レスリングの先代勇士とロマン爺の「柱の男♂」の縁／犬おっちゃん／板倉の牢破り。**確定扱い禁止**。
- [USER_FIXED] 戦闘冒頭でスタンド自動召喚。**遠野がそのスタンドの召喚スキルを奪い、遠野側の別の味方に渡す**。本番発動条件や奪還条件は未決定。
- [USER_FIXED / ON-017] スキル喪失・借用は**その戦闘限り**。元のスタンドは奪取時に消す。受け取り手がスキル付与後に召喚したスタンドは**受け取り手のHPを正本**として同期し、追従・射程・物理耐性を引き継ぐ。既存ポケモン召喚技を含め技能DAT無改変で利用したい。既存ポケモンにはスタンド固有HP同期を適用しない。
- [USER_FIXED / ON-018] **TNOKのチコリータ召喚技を奪うと、召喚済みの固有チコリータ系を消す**。2026-10-26のON-020により同名一括削除を許容し、同型他術者の個体別保護を完成条件から外した。TNOKの技は`sp_chikorita1/2/3`→飛翔ボール`next`→`_nt`→`chiko/chiko2/chiko3`。飛行中のボールの遅延召喚にも対処。
- スタンド：[USER_FIXED / 2026-10-25再確認] 術者から半径Rを超えて移動しない。**スタンド自身は物理攻撃でき、敵スタンドにも有効**。**普通の人間による物理攻撃はスタンドへ無効**。親子はHP・被ダメージを完全共有。以前の『スタンドの物理攻撃禁止』という解釈は誤り。
## 今回の作業・実装ステータス
- story正本Markdown：LOCAL SAVED。
- 原作照合：`unit ondisk` の既存連続パンチ `starchira` は Unit召喚ではない。原作`func=summon`スキルは存在。
- `stand_proto/stand_runtime.py`：純Python試作。射程制限、正本HP共有、回復、死亡と子消滅、二重通知防止、**普通の人間からスタンドへの物理攻撃無効／スタンド同士の物理攻撃可能**。
- `stand_proto/test_stand_runtime.py`等：スタンド関連48件PASS、TNOKの一般召喚モデル13件PASS、総61/61 PASS（2026-10-25までの既存試作）。**原作実機テスト0件**。2026-10-26以降はP0スタンドルールを優先して実機検証する。
- `stand_proto/stand_summon_fixture.dat`：既存native DAT parserで skill×2＋class×1の宣言を正常認識。
- `stand_proto/stand_autostart_theft_fixture.dat`：独立fight hook、開幕強制召喚、個人召喚枠buff、追尾、敵50%HPでの技能削除とコピー召喚。全7宣言がparser静的検証PASS、ゲーム実機未試験。
- `DAT_FIRST_STAND_FEASIBILITY_20261025.md`：DAT-first自動召喚/奪取案。
- `STAND_DAMAGE_MATRIX_20261025.md`：**最新版の攻撃/防御契約**。`attribute.dat` の既存定義に `standhit=スタンド打撃*659` を後で追加する構成（原作は未変更）。スタンドの耐性と物理パンチを区分。
- `FOLLOW_AI_RESEARCH_20261025.md`：`satellite`追従とCPUのAI制御DAT／既存V9関数証拠。
- `BATTLE_AI_ARCHITECTURE_20261025.md`：**戦闘AIの全体像の正本**。context値、T013保存の探索／標的優先／技能選択、CPU編隊AI全4DAT、ONDISK待機技能、原作の限界、スタンドへの連結順を独立整理。原本全てread-only。
- [USER_FIXED] スタンドは戦闘開始時にDATから自動発現。**ラスボス遠野がONDISKのスタンド召喚スキルを奪い、遠野陣営の別の味方に付与**する（疑似方式可）。
- **最新版** `stand_proto/stand_disc_transfer_fixture.dat`：開幕自動召喚＋遠野が使う無ダメージ奪取演出FX＋赤青全軍から同陣営・生存中の別リーダーを選び、`removeSkill`→`addSkill/eraseSkill`で移譲→`skillTroop`で再召喚。旧 `stand_autostart_theft_fixture.dat` はコピー式・固定デモで同時ロード禁止。
- `STAND_DISC_TRANSFER_DAT_20261025.md`：従来の**特定技能固定の試作**、試験48/48と実機未検証事項。新DISC DATは`on_stand_capacity`も自身で定義する。
- **最新版設計 `STAND_DISC_GENERIC_TRANSFER_FEASIBILITY_20261025.md`**：ON-017の戦闘限定・あらゆる召喚技の無改変移譲・スタンドの新術者HPリンク。技能ID変数化・召喚個体別消去・戦闘後復帰の原作実機証拠は未取得。従来の48/48を汎用技成功と誤認しない。
- **ON-018の現物解析 `TNOK_CHIKORITA_RECALL_20261025.md`**：TNOK原作Lv5/15/25の技・`next`と`add`の3段階、既存召喚物の正確な消去、同型他術者の保護、進化・飛行中のモンスターボール中止。独立実装`stand_proto/summon_ownership_ledger.py`＋`test_tnok_chikorita_recall.py`。全スタンドプロトタイプ累計61件PASS（新13件）、**実機0件**。
- 実機召喚・DLL hook・新戦闘エンジン統合・SAVE連携・GUI：NOT RUN / NOT INTEGRATED。
- Git：dev_lab mainに既存多数dirty。remote未設定。GitHubへpushしたとは主張しない。
- **[ON-STAND-010新発見] SUMMON_PARENT_NATIVE_DAT_BOUNDARY_20261025.md**：既存Ghidra V9で召喚親子リンクを検証。親Unit+0x178/17C/180＝子ポインタ一覧、0x5774A0＝子登録、0x577600＝子数を用いた召喚上限判定、0x5445E0/575A60＝親死亡時element_lostに従う子消滅。**既存原作に親子管理あり、新規台帳不要**。一方、DATから親ごとの子一覧を取得・生きたまま消去する公開命令は未確認。TNOK専用DAT限定試験と完全汎用最小DLLを分ける。実機0件。
- **[ON-STAND-014 / 2026-10-26]** 戦略/戦闘スキルリストの違いを確認。仕様Wikiで removeSkill は戦闘シーン用、addSkillは恒久スキルリストに追加、eraseSkillは所持技能から消去。原作Ai戦闘制御_軍楽隊なし版.datは addSkill 617、eraseSkill 617、removeSkill 111箇所（静的出現数）使用。L1155-1161ではONDISKのsp_ondiskを removeSkill、wait_ondisk/com_ondiskを addSkill→eraseSkillで戦闘限定差替えする。**技能の戦闘限定奪取・付与は既存DAT技法で実現可能性高い**。ただしリーダースキル由来の技能、受領者が元から持つ技能、情報パネル・SAVEは要実機検証。SKILL_BATTLE_SCOPE_NATIVE_DAT_20261026.mdを正本に追加。

## 最優先の確認／問題
1. [RESOLVED] 物理の誤解は修正済み。**スタンド自身の通常物理攻撃は可能／敵スタンドに有効／普通の人間からの物理被ダメージは無効**。攻撃者種別と攻撃属性を区分している。既存`starchira`の新属性への統合は要検証。
2. 射程R、地形障害との追従、範囲攻撃同時命中、MP/状態異常/EXP/召喚数と解除条件が未確定。
3. 制御ロジックは実ゲームに接続されていない。最初から原作DATを書き換えて動かさない。
4. CPU指揮の`Ai戦闘制御_*`全4DATと通常Unit AIの違いはBATTLE_AI_ARCHITECTURE参照。ONDISKには`sp_ondisk`→`wait_ondisk/com_ondisk`既存差替えがあるが、`sp_world_ondisk`や新スタンドは別。
## 安全な再開
1. Git statusと原作ファイルを読み取りで照合。
2. `python -m unittest discover -s story/ONDISK/stand_proto -p "test_*.py" -v` を実行してから既存単体テストを拡充する。
3. 原作スタンド召喚・射程制約・HPイベントの入出力契約を確認し、隔離fixture／ゲームadapterを作る。
4. 本編DAT・EXE・MASTER_LEDGER・他研究レーンは変更せず、担当境界で統合提案する。
## 作業障害記録
- REC-ON-001 2026-10-25: 長いWindowsコマンドがENAMETOOLONGとなり不成功。短いDirectory作成コマンドと25行単位の書込へ切替成功。元ゲームへの影響0、重複書込の有無は読み戻しで検証。