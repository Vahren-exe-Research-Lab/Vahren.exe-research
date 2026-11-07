# ONDISK｜タスク・未解決
## 優先順位の変更（2026-10-26 / ON-019）
**P0：スタンドのルールが先**。以下はすべて原作ゲーム実機での判定を必要とする。
- [ ] STAND-P0-01: 自動召喚・再召喚禁止・本体死亡時消滅と戦闘終了時の技能復帰（NOT RUN）。
- [ ] STAND-P0-02: `satellite`に加えて術者中心の絶対射程Rを移動/AI/プレイヤー操作/ノックバック時にも保証（NOT RUN）。
- [ ] STAND-P0-03: 現在術者とのHP双方向同期、スタンド側被弾・回復・死亡、奪取後に新術者へHP参照再リンク（NOT RUN）。
- [ ] STAND-P0-04: 通常物理攻撃0、専用`standhit`はスタンドにも人間にも有効、既存連続攻撃と整合（NOT RUN）。
- [ ] STAND-P0-05: DISC奪取→元スタンド即消滅→別人材へ技能→別人材が自動召喚→戦闘終了の全状態復帰（NOT RUN）。
**P1**：原作DATで戦闘イベント、召喚枠、NPC AI、セーブ/ロード整合を確認し、P0の不足分だけ小さいエンジン連携を検討。
**P2（完成を妨げない）**：TNOKのポケモン等、一般召喚の重複ゼロ・個体単位の完全所有者追跡・飛行中のボール完璧なキャンセル。一般召喚は同一トークンが複数体いても可。旧ON-STAND-009/010の厳密個体追跡研究は資料として保持し、必須作業から延期。無関係な通常ユニットを削除する案は引き続き不可。

- [x] ON-STORY-001: Git管理可能なストーリー用フォルダと、引継ぎ資料を作る。
- [x] ON-STORY-002: USER_FIXED / USER_CANDIDATE / PROPOSED / ORIGINAL_CONFIRMEDを分類。
- [x] ON-STAND-001: 移動拘束・HP共有・スタンド自身の物理攻撃／普通の人間の物理攻撃無効の独立動作試作。総48件中戦闘24件PASS。
- [x] ON-STAND-002: 原作の召喚Skillを参考に隔離fixtureを作成。現在4宣言（召喚2・パンチ1・クラス1）を既存DAT parserで認識（静的検証のみ）。
- [x] ON-STAND-006-STATIC: `attribute.dat` の既存属性構造、独立 `standhit` 追加の可能性、ゴースト物理耐性、専用打撃と敵スタンドの耐性を調査。静的試作とPythonテストPASS。実機はNOT RUN。
- [ ] ON-STAND-006-LIVE: 隔離した原作エンジンで `standhit` 追加DATを読込、通常武器・スタンドパンチ・魔法の被ダメージと射程、耐性10で残HP0変化を検証。
- [x] ON-STAND-005-STATIC: 独立`story fight=on` + `battleEvent` + `skillTroop`開幕自動召喚、召喚上限buff、追尾、仮ボス50%HPでの奪取演出DATを作成。既存DAT parser構文PASS。研究は`DAT_FIRST_STAND_FEASIBILITY_20261025.md`。
- [ ] ON-STAND-002-LIVE: fixtureを隔離環境で実際にロード・召喚して動作確認（NOT RUN）。
- [ ] ON-STAND-005-LIVE: 開幕1回召喚、操作、射程・召喚上限、スタンド奪取演出、終了時の技能復帰を実機確認（NOT RUN）。
- [x] ON-STAND-007-STATIC: 遠野（toono）がONDISKのスタンド召喚スキル等を剥奪し、生存する遠野側の別の部隊長に付与・強制再召喚するDAT案を作成。`STAND_DISC_TRANSFER_DAT_20261025.md`、DAT＋13件（依存閉包含む）。既存35と合計48 PASS。ゲーム実機はNOT RUN。
- [ ] ON-STAND-007-LIVE: 自動召喚が成功するか、遠野HP65%で生存する別味方へ1回譲渡できるか、受領者AIのスタンド行動・再召喚、戦闘終了後の技能残留・SAVE/LOAD、召喚枠を隔離実機で確認。
- [ ] ON-STAND-007-RETURN: 奪還・味方受領者が倒れた場合・遠野撃破後の技能復帰とラスボス演出連結を仕様化。
- [x] ON-STAND-008-STATIC: `STAND_DISC_GENERIC_TRANSFER_FEASIBILITY_20261025.md`に戦闘限りの借用、元スキルDAT無改変、スタンドとポケモンの処理区別、HP再リンク、召喚個体の精密消去とリスクを整理（DESIGN、実機0）。
- [ ] ON-STAND-008-LIVE: 戦闘中に既知の通常技能/既存召喚技能を移し、戦闘終了で元術者復帰・受領者から技能消失・セーブ保持・他の術者の同種召喚体を巻き込まないことを実機確認。
- [ ] ON-STAND-008-DYNAMIC: `@skill`識別子を `removeSkill/addSkill/skillTroop` の動的引数に渡せるかと、複合 `next/add2` の召喚子個体を元術者に紐付ける方法を確定。安全性チェック拒否済の原作DAT横断検索を迂回再試行しない。
- [x] ON-STAND-009-SOURCE: 原作ver0.67でTNOKのLv5/15/25の`sp_chikorita1/2/3`を追跡し、`next_last=on`のモンスターボール経由で`chiko/chiko2/chiko3`召喚と判明。詳細`TNOK_CHIKORITA_RECALL_20261025.md`。
- [x] ON-STAND-009-PROTOTYPE: 召喚者＋根Skill＋召喚個体ID、投射物IDとキャンセル状態を管理する`stand_proto/summon_ownership_ledger.py`。同型他術者保護・進化後・飛行中・借用後再召喚・戦闘終了復帰の新テスト13件PASS。既存48+13=61/61、実機0。
- [ ] ON-STAND-009-INTEGRATE: 原作召喚処理の責任者を特定する既存B/T011,T012証拠を照合し、個体と根技能IDを取得する境界を設計。原本ゲームでの個体別消滅・飛行中ボール停止・後続召喚を実験。DATの全クラス消去は本番に採用しない。
- [x] ON-AI-001-STATIC: 戦闘AIのDAT/EXE構造を横断照合。`BATTLE_AI_ARCHITECTURE_20261025.md`にcontext、Unit探索、技能、CPU陣形、ONDISK専用wait/com、satelliteを保存。既存研究T013を参照し二重計上なし。実機はNOT RUN。
- [ ] ON-AI-002-LIVE: 通常Unit/後衛/召喚スタンドで近傍探索、追従、手動命令干渉、スキル発動タイミングを隔離実機で比較（NOT RUN）。
- [ ] ON-STAND-003: DLL/新戦闘エンジンとのUnit ID・tick・ダメージ通知・死亡通知の接続契約。
- [ ] ON-STAND-004: 本編非破壊の実機戦闘・セーブテスト（現在NOT RUN）。
- [ ] ON-STORY-003: 口マン爺、ビリー、田所、遠野、おっちゃんの原作Unit / Power / lore照合。
- [ ] ON-STORY-004: 壁の目・進軍路・遠野への出征動機の確定。
- [ ] ON-STORY-005: 田所が仲間になる条件と時間停止認識の伏線。
- [ ] ON-STORY-006: イベント発火条件・NPC台詞・ストーリー分岐。
- [ ] ON-ART-001: 漫画風カットイン／コマ割り／画像・音声制作。
- [x] ON-STAND-010-STATIC: 原作Unitの召喚子vector +0x178/17C/180、登録0x5774A0、上限判定0x577600、死亡時element_lost処理0x5445E0/575A60を既存V9解析で突合。独自親子管理の新設方針を撤回。証拠資料 SUMMON_PARENT_NATIVE_DAT_BOUNDARY_20261025.md。
- [ ] ON-STAND-010-DAT-LIVE: TNOK一人がchiko系を使う隔離戦闘で、storeAliveUnit/個体別removeTroopと飛翔中ballの残存を観測。他の術者が同種を出した場合の巻き添え禁止をテスト。
- [ ] ON-STAND-010-ADAPTER: 完全汎用DATが不成立と確定した場合のみ、既存親子vectorを使う最小DLL/戦闘エンジン連携を設計。別の独自親子台帳は作らない。
- [x] ON-STAND-011-STATIC: 召喚物を固有（ONDISKスタンド/チコリータ）と量産（いんゆめくん/ALC役クッキー☆声優の歳納人形）に分類。F20_summon.datで`member=*7`、CPU用派生技能`s_inyume_com0/1/2`・`s_toshino_com0/1/2`を確認。資料`SUMMON_DISC_REMOVAL_POLICY_20261026.md`、安全側モデル`stand_proto/summon_removal_policy.py`＋新9件PASS、累計70/70（原作実機0）。
- [ ] ON-STAND-011-LIVE: 技能を奪ったCPUいんゆめ/歳納人形使いの派生技能も使えなくなるか、既存召喚物を消さずに新規召喚だけ停止できるか原作コピーで確認。
- [ ] ON-STAND-011-UNIQUE-LIVE: 固有スタンド/チコリータを一括消去する時、指定されたクラスと部隊に与える影響を隔離実機で確認。DAT消滅の実機成功は未確認。

- [x] ON-STAND-012-RULE: ユーザー最終確定の「単体生成型は消滅／量産型は出現済みを残す」を**召喚技能の設計上の生成数**で分類。戦闘中の同名個体数を使わない。単体型は同名複数でも一括消去許容、量産型は残数1でも残す。資料 SUMMON_DISC_REMOVAL_POLICY_20261026.md と STAND_SPEC.md に記録（ルールのみ、実機未検証）。
- [ ] ON-STAND-012-LIVE: 召喚元技能の分類・奪取時の一回限り消滅・受領者再召喚を、単体型同名複数と量産型残数1の両条件で隔離実機試験。CPU派生再付与・戦闘終了後リセットも確認。

- [x] ON-STAND-013-DESIGN: 戦闘中の技能喪失/付与に合わせた情報パネル・スキル操作欄の表示仕様を提案（SKILL_THEFT_UI_SYNC_SPEC_20261026.md）。原作 addSkill/removeSkill と付与技能アイコン装飾、reloadMenuの用途を照合。UI自動更新は未証明。
- [ ] ON-STAND-013-LIVE: 情報パネルを開いたまま/再選択した際に addSkill/removeSkill がスキル表示へ反映されるかを隔離実機で確認。操作スキル欄、CPU派生技能、戦闘終了/次戦闘/セーブの復帰も検証する（NOT RUN）。

- [x] ON-STAND-014-STATIC: 原作CPU戦闘AI（Ai戦闘制御_軍楽隊なし版.dat）で removeSkill と addSkill→eraseSkill の戦闘限定差替えを確認。617/617/111は命令文字列の静的出現数、動作試験件数ではない。仕様Wikiの戦略/戦闘関数差を照合し、SKILL_BATTLE_SCOPE_NATIVE_DAT_20261026.mdに保存。
- [ ] ON-STAND-014-LIVE: 受領者の一時付与が戦闘中のみ発動し、戦略の所持技能に残らないこと、元から同じスキルを持つ受領者を誤削除しないこと、リーダースキル由来の能力、再選択時/開いたままの情報パネル、退却/SAVE/LOAD復帰を原作コピーで検証。

- [ ] ON-STAND-014-MIDBATTLE: 原作の実例は戦闘開始時のfight=on。中盤のbattleEventでremoveSkill / addSkill→eraseSkillが発動するか、戦闘情報パネルの開閉中にアイコンが同期するかを検証（未実施）。
- [x] ON-STAND-015-STATIC: 「放置で恒久強化されるボス」候補を追加。原作 world イベント getTurn/isNewTurn の5/10/15TごとのCPU成長、ワールド addSkill、永続型 addStatus/addLevel と数値変数のセーブ仕様を照合。event_world.datの同ターン複数回world評価の注意も発見。設計案 PERSISTENT_BOSS_ESCALATION_PROPOSAL_20261026.md。設定はUSER_CANDIDATE、原作実機0。
- [ ] ON-STAND-015-LIVE-IF-ADOPTED: 候補として採用後、段階フラグを使い一ターン1回だけ addSkill/addLevel/addStatus を適用し、戦闘、次のターン、セーブ/ロード、転職、死亡/再登場時の重複と保持を隔離環境でテスト。通常の戦闘限定DISCを無断で永続化しない。

- [x] ON-STAND-016-STATIC: CPU対CPU簡略戦闘でのDISC奪取のDAT-first候補を調査。Wikiのworld戦闘終了呼出、storeBattleSpot/AttackPower/DefensePower（簡略戦闘後も可）、storeTodoUnit/AliveUnit（簡易可）、原作シナリオの実使用を照合。通常戦闘用AIはisWorld()==0条件かつCOM対COMで制御しない箇所があることを確認。資料 SIMPLIFIED_CPU_BATTLE_DISC_RESEARCH_20261026.md。候補仕様で実機NOT RUN。
- [ ] ON-STAND-016-LIVE-BATTLE-RECORD: 原作コピーのCPU対CPU簡略戦闘のworldイベント呼出回数・タイミング・直前戦闘recordの寿命、同じturn中の連戦と重複を観測。
- [ ] ON-STAND-016-LIVE-PARTICIPANTS: 簡略戦闘でstoreTodoUnit/AliveUnitに参加者が入り、戦闘終了worldイベントでも取得可能かを観測。不可なら参加者を保存できる正式な前段フック／最小アダプタを検討する。勢力一致だけで盗まない。
- [ ] ON-STAND-016-LIVE-PERSISTENCE: ボス本人が参加して条件を満たしたCPU対CPU戦闘後に既知技能を一つだけ獲得するDAT試験、次戦/次ターン/SAVE/LOAD/転職確認。通常戦闘の同じ報酬を二重に与えない。
- [ ] ON-STAND-016-AUTORESOLVE-POWER: 獲得済み技能が簡略戦闘の勝敗計算に反映されるかは別研究。獲得した技能が**その戦闘を遡って強化しない**ことに注意。

## 注意と保留
- [USER_FIXED / 2026-10-25] 解釈は確定：**普通の人間の物理攻撃はスタンドに無効**、スタンドは物理攻撃可能でスタンド同士の打撃も有効。攻撃側禁止という旧解釈は破棄。
- 射程R、範囲攻撃時の重複判定、召喚解除、HP以外の状態共有、消滅/復活/EXPは未確定。
- 既存dev_lab Gitは多数dirty。**story以外をadd/commitしない。**
- `git remote`は空。GitHub push完了とは言わない。
