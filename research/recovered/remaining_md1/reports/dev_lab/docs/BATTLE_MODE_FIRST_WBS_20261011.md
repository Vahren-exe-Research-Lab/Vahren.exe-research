# 迫真戦記 ver0.67 戦闘モード最優先の再開発計画

## 現在の優先方針 — WORK-HIRE-UI-DLL-PROTOTYPE-20261019
最新ユーザー指示は「原作EXEを最大限利用し、DATで可能な機能はDAT、必要箇所だけDLL等で拡張」。戦闘別EXEは実証後に選ぶ選択肢であり、必須の直近主線ではない。直前WORK-EXTERNAL-BATTLE-POLICYの別EXE最優先記述より本節を優先。
最初の実装対象: save1ロード→人材雇用。左は所属人材、hoverで右の雇用対象を絞る（ユーザー確認）。右は雇用可能優先/原作順切替、同区分内元順保持。左は名前横に静止チップ。既存hover/雇用条件/費用/対象対応を保つ。今回DLL作成・ビルドまで明示依頼あり。戦略全再実装や全EXE逆コンパイルは行わず、既存研究と部品を再利用する。

## 最新方針 — WORK-EXTERNAL-BATTLE-POLICY-20261019
ユーザー承認による方針転換。過去の全EXE復元・独立戦略再実装を主目的とする指示より本節を優先する。

最上位目標: 原作Vahren.exeを戦略・ストーリー・既存イベント・保存の実行役として残し、DLLによる接続層を介して戦闘開始情報を別のWindows戦闘EXEへ渡す。新戦闘EXEで原作DAT/MAP/画像/音声を使った戦闘を実行し、結果を適切に原作へ反映して物語を続けられる、保守・拡張可能な構成を完成させる。原作EXEへの依存を許容する。DLLで原作戦闘が自動的に別プロセスへ移るとは扱わない。

- 基準動作: ダメージ式/能力/耐性/回復/状態異常/EXP/成長、技能条件と処理順、DAT継承、移動/射程/AI、弾/アニメ/音声等を既存証拠に沿って再現する。内部stack/Task/allocatorの一致は不要。未知のゲーム効果を黙って省略しない。
- 必須拡張1: 召喚Unitが獲得したEXPを召喚者へ還元できる。還元率・親の死亡/消滅・多段召喚・本人獲得分との重複・戦闘後LvUpの扱いを明示的なデータ仕様とする。未合意の数値を固定しない。
- 必須拡張2: 戦闘中にマップチップ/地形をイベント等から変更できる。見た目だけでなく通行/移動コスト/経路の再計算、変化地点のUnit、必要な射程/衝突への影響を整合させる。変化の戦闘外持越しは要件確認後に定める。
- 原作基準と拡張を分離し、拡張は明示設定で有効化する。特定キャラクター名への専用処理を避け、既存シナリオを無断で変えない。
- 境界契約: 出撃Unit/部隊ID、補正済み能力/技能、MAP、戦闘条件とイベント状態を識別して受け渡す。戦闘中イベント/増援/会話の実行主体、原作の進行停止/復帰、死亡/EXP/LvUp/領地等の結果適用主体を定義し二重処理を防ぐ。通信失敗や別EXE異常終了時に不完全な結果を適用しない。生ポインタの別プロセス流用をしない。
- 工程順: (1)既存開始/終了証拠から接続点を選定 (2)隔離した試験環境で原作→別EXE→試験結果→原作戦略復帰の往復を実証 (3)既存戦闘コードを再利用して一戦完走 (4)召喚EXP還元と動的地形を実装・検証 (5)戦闘中イベントと代表シナリオ、保存/再開を検証 (6)他MODへ対応拡大。往復試験だけを戦闘再現成功と呼ばない。
- 再利用: DAT/MAP/Unit/技能/数式/移動/弾/GUI/観測/テストと開始・死亡・終了解析を保持。戦略側コードは契約確認資料として利用し、全面書直しや不要な全EXE逆コンパイルをしない。
- 完了条件: 実際の操作/敵AI/戦闘/勝敗、結果の一度だけの反映と原作物語継続、二つの拡張の動作、代表戦闘の安定性を実証する。STATIC/SYNTHETIC/DAT_DERIVED/ACTUAL/GOLDEN/MATCHを区別し、未比較を明記。
- 原本read-only、他担当所有権、禁止Git操作、Local優先/Remote無断切替禁止、既存安全拒否の迂回禁止は維持。今回の目標変更自体は原本改変・過去拒否の解除・新しいフック実行の実証ではない。
- 今回は方針文書のみ変更。アプリgoal本文は直接編集APIなし、取得時pausedの旧本文のまま。旧目標をcompleteに偽装して置換しない。開発再開時は本方針と最新ファイルを優先する。


**適用版:** 2026-10-11 / WBS v1.2。状態・依存・変更履歴の正本は同じdocs内の `DECOMP_TASK_LEDGER_20261011.md` の `BF-01～BF-18`。本文は実装契約と次の作業順をまとめた設計書であり、二重の進捗台帳ではない。

## 目的と完了の境界

最初の完成目標は原作データによる通常戦闘の一戦完走。長期目標には物語・戦略復帰、イベント、音声・演出、保存再開と他MODへの拡張も含む。数式・技能・判断・体感を正確にし、内部メモリ/旧描画API/旧音声APIの一致は要求しない。既存の原作素材と確認済み処理を再利用し、未対応仕様を明示する。

### スコープ判定

| 対象 | 必須とする結果 | やらなくてよいこと |
|---|---|---|
| 通常の戦場・地形 | 原作stage/mapの地形と障害物、初期位置・collision、可視画像 | 原作GPUドライバや描画関数ABI |
| ユニットの操作 | 選択/命令/移動/攻撃/停止/退却/範囲選択、速度・pause、グループ | 古いウィンドウサイズや不便な配置のコピー |
| Unit/Skill | 定義・継承・全ゲーム内実使用の効果、射程・発動条件・MP・cooldown・投射・状態変化 | 一万超のskill宣言を個別の関数1個ずつで書くこと |
| 戦闘CPU | 同条件で目標、行動、攻撃/治療/支援/撤退を選ぶ順序・乱数 | 強さだけ似た別AIへの置換 |
| BattleEvent | if/rif、wait、戦闘開始/援軍/勝敗/撤退・時間切れ | ストーリー・内政イベントの画面一式 |
| 視覚 | Unit chip・モーション・弾・ヒット・HP/MP・戦闘スキルの効果が判断可能 | 元DirectShow/DirectMusic再生・BGM/SEの出音一致 |
| RTS固有ルール | **後段**：通常戦闘のcoreを共用するが、HQ/MP/生産/波状AIを後から追加 | 通常戦闘の初回完成に先行させること |
| 戦略/物語/内政 | battle開始に必要な参加軍/seed/mapを外部から受け取るadapterだけ定義 | Campaignを完成させてから戦闘へ進むこと |

**通常戦闘を初回対象とし、独立RTSの1v1rts1.mapを代表例として誤認しない。** 原作battle内部が共有する処理は再利用し、RTS特有のscriptは別task `WD-04` へ後続。

## 原作資産と既存解析成果の棚卸し

- **stage:** 151 `.map`のbyte-exact読込（`T007_MAP_FORMAT.md`, `map_codec.py`）。通常map `s1.map` は110×110、terrain 12,100件、scenery 446件、配置marker12件。`@`は動的参照候補であり、配置markerを実戦参加Unit/チーム/HP/MPに直結しない。
- `1v1rts1.map` は140×55、terrain7,700、RTS配置marker2で通常のmapと異なる。`sdrama.map` は110×110の12,100 cellに対し地形entry12,082。空セル18件を原作情報なしに推定補完しない。
- **画像:** `T008_IMAGE_FORMAT.md` と `image_codec.py`、chip atlas / rectangle / BGRA color key等のreaderがある。**rendererでの可視出力、draw順、layer priorityとanimation時刻はこれから**。
- **技能:** `evidence/T005_DECL_INVENTORY.json`の原スクリプト590ファイルにはskill宣言**16,554件**、親指定skill**13,049件**。これは**個別の実効技能16,554種類でも、実装関数16,554個が必要な証拠でもない**。重複、親からの派生、未到達・特殊skillを区別する`BF-02`が先。基本funcの候補はネイティブ研究`T012`の1 sword、2 missile、3 heal、4 summon、5 charge、6 statusであり、必ず他の特殊属性/各script効果も追う。
- **battle tick/AI:** `battle_clock.py`, `battle_root.py`, `search_cadence.py`, `targeting_subset.py`, `synthetic_ai_scene.py`等は**限定・合成モデル**。原作の移動・action/pool選択・戦闘シーンと同一だとまだ証明していない。
- **damage/status:** `main_decomp_attack_expression.py`は原nativeの`2-R`を反映した数学式、`main_decomp_ftol_sse_subset.py`は一部x87/SSE後段、各status/negative_heal/afterhit/knock/rangeも限定モデル。既存`typed_damage_fragments.py`の旧`1-R`は誤解析だったため、統合時は修正済み式を正本候補にする。原作と同seed実測は未。
- **T005/VM:** `peer_script01_native_flow_vm.py`はイベント局所挙動を回収しているが、battleEventの実例とUnit操作を結合する必要がある。

## アーキテクチャ：戦闘を単独ゲームとして起動

```text
battle fixture / 戦闘開始引数
  map_id, alliances, participants, initial HP/MP, skill loadout, seed, battle rules
                │
                ▼
       Battle Data Import (BF-01～03)
                │
                ▼
        BattleSimulationCore  ←── BattleCommands
       ├─ tick clock & RNG      (BF-07,08)
       ├─ unit movement/field
       ├─ skill dispatcher      (BF-09,10)
       ├─ target/AI decisions   (BF-12)
       └─ battleEvent/victory   (BF-13)
                │
       immutable Snapshot + Event Trace
                │
                ▼
         BattleRenderer / UI     (BF-04～06,11)
          ├─ terrain and chips
          ├─ camera, markers, UI
          ├─ projectile/effect
          └─ OPTIONAL sound sink (default disabled)
```

**不変条件:** Camera移動、画面fps、ボタンの表示更新やsound sinkはsimulation seed/tick/乱数消費と独立。BattleSimulationは描画やWindowsイベントなしで同入力に対して同じtraceを出せる。Unitやskillの命令入力と画面操作はcommand boundaryで分離する。未解明native関数を推測で確定・skipせず、未実装ステータスを付ける。

## Battle First の達成ゲート

| Gate | 完了が確認できるもの | 元WBSサブタスク | 現在 |
|---|---|---|---|
| BG0 | 実戦闘mapの描画入力マニフェストを取り出せる | BF-01 | **PASS：データのみ** |
| BG1 | 通常戦闘を新ウィンドウに表示 | BF-04、05 | NOT YET |
| BG2 | 実Unitを表示し、選択・移動・攻撃命令を操作 | BF-03、06、07 | NOT YET |
| BG3 | 6基本skill系統・実使用派生が行動と画面に反映 | BF-08～11 | NOT YET |
| BG4 | 戦闘CPU・イベント・勝敗が機能 | BF-12、13 | NOT YET |
| BG5 | 通常戦闘1戦を実機Windowsで完走 | BF-14 | NOT YET |
| BG6 | ゲーム中の戦闘スキル、CPU判断、戦闘結果の原作一致を測定・監査 | BF-15～18 | NOT YET |

`BG0`はplayableの進捗ではなく、ゲーム画面に接続できるデータ契約の完了。原作実機golden0、厳密比較PASS0をそのまま維持する。

## 初回の実装結果：BF-01

- **新規ソース:** `dev_lab/src/hakushin_compat/battle_stage_view_manifest.py`。原stageを読み込み、地形(kind0)・scenery(kind1)・動的配置marker(kind>=2)をx/y/順序/元kind/方向/隊形候補と一緒に連続描画entryへ出力。SHA256と各種件数、空地形セル数、`@`マーカー数を持つ。入力mapのbasenameを限定。チームや実Unit生成をしていない。
- **専用回帰:** `dev_lab/tests/test_battle_stage_view_manifest.py` は10/10 PASS(exit0)。実物通常`s1.map`、RTS`1v1rts1.map`、欠落地形の`sdrama.map`、合成セル重複・順序・境界検査。
- **呼出例:** PowerShellで dev_lab/src を `PYTHONPATH` に指定して `python -m hakushin_compat.battle_stage_view_manifest s1.map` と実行すれば概要JSONを標準出力（原資料へ書込なし）。`--all-entries`を追加すると全描画entry JSONを出力。これは元画像の描画アプリ・戦闘シミュレーションではない。
- BF-01完了の意義は「画面レンダラーが原作実stageを安全に読み取れる境界を確保」。**まだ動く戦闘画面は存在しない**。性能/原作音声/入力の実装を主張しない。

## 次に実施する順序

**主経路（画面優先）：** BT-01（PCに適した新レンダラー選定）→BT-02/03（独立起動）→BF-04/05（`s1.map`の描画）→BF-06/07（Unitの表示と命令）。タイトル画面は不要。新EXEの起動を原作EXEの再利用・パッチで代用しない。

**並行のゲーム性経路：** BF-02（skill宣言と親継承を分類）→BF-03（Unit/Skillの実戦闘fixture）→BF-08（tickと移動）→BF-09/10（skill実作用）→BF-12/13（AI/勝敗）→BF-14（プレイ可能）→BF-15/16/17/18（原作比較と全効果網羅）。BF-11（skillの画面演出）はrenderとの結線で行う。

**元の戦略・ストーリーとの接続:** 完了後は本戦闘起動APIへ外部`BattleRequest`と返り`BattleResult`を渡すだけにする。これにより、後日キャンペーン/内政/ストーリーを作っても戦闘coreの計算・AIを変更する必要がない。

## 新発見・誤解析とタスク管理

スキル種別が増えた、式が誤っていた、CPUの判定経路が不明だった、通常戦闘とRTSで挙動が違った場合は、新しく独立条件を追加/分割してWBSの未使用BF-IDを使う。既存IDは維持し、acceptance/依存/「観測がない箇所」の変更記録を残す。`DECOMP_TASK_VALIDATE_20261011.py`のBG0～BG6とDAG/重複/参照整合を都度実行する。

**安全:** 元EXE・原save・原ZIPはread-only。A〜E研究レーンおよびpeer所有コードは編集しない。過去の拒否済み逆解析を別ツール等で再試行しない。Remote/Git/push/automation/Windows設定を変更しない。比較検証なしに`STRICT_MATCH`を名乗らない。



## Work統合checkpoint WORK-RESUME-20261013-997（2026-10-13）
- 上記初回BF-01記録は履歴。現状は原MAP/Unitのread-only snapshotをWindowsへ表示する基盤があり、BG1は部分実装。BG2の命令操作・BG3全技能・BG4継続戦闘/勝敗・BG5完走・BG6原作同条件比較は引き続き未達。
- BF-08～10: 新F停止を確認してWorkが引継ぎ。通常AI m_heal→単回MP減算→効果pool再利用→551490発動率/一時領域→551574属性分岐を既存Task continuationへ接続。最新停止55159E→415530(ret5515A3)。文字列copy/属性列/HP効果→54E31C→57FA9E/正常UnitRETが次の直列依存。広域997PASS/FAIL0/ERROR0、専用追加9PASS。全suite/既知2FAILは別。
- BF-14～18: PyInstaller新EXE2ケースがfresh sourceと全JSON一致したが、両exit3=VERIFY。通常戦闘完走・操作GUI・原作Gameplay Golden/strict MATCHは未達/0。静的試験を実機一致へ算入しない。
- G1～G8基準は固定CHATGPT_CURRENT_HANDOFF末尾と監査JSONへ同期。共有WORK_REQUEST_QUEUEを始業/終業時にWork単独更新し、A～E/REA/Claudeからの局所READYを依頼全体CLOSEDと混同しない。


## Work統合checkpoint WORK-ATTRIBUTE-COPY-20261013-1004
- BF-08～10: 実DAT m_healの正規技能経路へ既確保SSO属性copyの正常帰還を接続、55159Eから551653へ進行。容量不足415AA0は停止。MP/RNG/Task順序を維持し、実HP/追加効果/親Unit returnはまだ未接続。
- 検証: 新規7PASS、広域1004PASS/FAIL0/ERROR0、新EXE2ケースfresh source一致（exit3 VERIFY）。全suite既知2FAILは別、原作Golden0/MATCH0。
- G1部分/G2未達/G3・G4・G6部分/G5・G7・G8未達。次は551653属性index→550D80→551924実効果を+D/E=1/1 contextで接続。保存証拠・既存モデルを再利用し、単独heal呼出で未知後段を飛ばさない。


## Work統合checkpoint WORK-CORE-HP-REFRESH-20261013-1023
- BF-08～10/G3: 通常AI支援Skillの同Task経路でDAT属性/効果量→実Unit HP writer→既知refresh早期returnを接続。m_heal魔力542→回復1084、HP1→1085。MP/RNG/Task順を維持しEXP直前551C6Aに停止。実行範囲拡張であり、通常戦闘完走ではない。
- 新規19PASS・関連99PASS・20module広域1023PASS/FAIL0/ERROR0。新EXE2ケースfresh source一致/期待VERIFY。元FPU・全runtime初期化・special未指定・EXP後段/E effects/正常UnitRETはVERIFY。Golden0/MATCH0、全suite既知2FAIL未検証。
- G1部分/G2未達/G3・G4・G6部分/G5・G7・G8未達。次は551C6A→551E50→HP+D8→E1追加効果を既存EXP/flash契約で接続し、親Skill/Task復帰へ進む。共有キューB1734/1740・C1724・D1732受領と同期。


## WORK-AWARD-FLASH-20261013-1041 実行経路checkpoint
- 正規支援551C6A EXP→HP補正→DAT flash5→551CA1を接続。count明示時のみring/4DFBB0直前へ再開、child未帰還。新規18/関連114/広域1041PASS、EXE2ケース自己照合、Golden0/MATCH0。G1部分、G2未達、G3/G4/G6部分、G5/G7/G8未達。
- 次は6F0依存を保持しB1850/1858/1901と既存refresh_hit_lifebar→551D40/551E4A→54E31C。詳細は固定handoff1041と共有依頼キュー。


## WORK-CORE-RETURN-20261013-1056 実行経路checkpoint
- 551CF2→既存HPbar/早期復帰577100→raw回復量記録→単一inline属性cleanup/入口捕捉cookie検査→551E4A/54E31Cへ接続。元flash5通常枝の6F0依存は未解消、試験の8D1/既存timer/stackは明示SYNTHETIC。
- 新規15/関連45/広域1056PASS、EXE2ケース自己照合。G1部分、G2未達、G3/G4/G6部分、G5/G7/G8未達、Golden0/MATCH0。次はB1825等の54E31C親処理、独立候補REA DEATH60/FlashObj Task。詳細は固定handoff/共有キュー。


### WORK-POSTCORE-RETURN-20261013-1075
通常戦闘支援経路を54E31Cから条件付き54E3E1→57FA9Eへ延長。list非空は実抽選後virtual直前停止、矩形は実HOST USER32.PtInRect、phase0は未確定定数前停止。新規19/広域1075PASS、EXE2ケース自己照合。G1/3/4/6部分、G2/5/7/8未達、原作Golden0/MATCH0。次は57FA9E追加技能→57BE30→親UnitRETURN。詳細と依頼は固定handoff/WORK_REQUEST_QUEUE同checkpointを正本とし、合成runtime bindingをDAT既定値と混同しない。


### WORK-SUPPORT-FINALIZE-20261013-1090
支援54E0B0帰還後に追加技能vector/optional gateを接続し、共通57BE30優先度/待機writerを実Unitへ適用。後段は57BF54特殊node確保前で停止。新規15/関連27/広域1090PASS、EXE2ケース自己照合。G1/3/4/6部分、G2/5/7/8未達、原作Golden0/MATCH0。次依存565780/5469B0/40EBE0・実stack/list解放と、実DAT special未指定/default。詳細は固定handoff/共有キュー同checkpoint。


### WORK-SUPPORT-SPECIAL-PHASE-20261013-1109
通常戦闘支援経路はDAT由来回復後のphase0乱数1回→特殊技能登録木→57BE30実帰還→57FC19へ延長。新規19/広域1109PASS、EXE2ケース自己照合。木正常挿入/明示stack/仮定FPU限定であり、親候補list解放/UnitRETURN・通常flash・全Task進行は未完。G1/G3/G4/G6部分、G2/G5/G7/G8未達、Golden0/MATCH0。次工程は保存済み57F570入口と57FC19→57FC59、詳細は固定handoff/WRQ同checkpoint。既知全体2FAIL未再実行。


### 新方針の実装計画（Work自身が実行）
設計: 意味ベースの戦闘コアに既存DAT/Unit/数式を結合し、画面はimmutable snapshotを描き意味ベース命令を渡す。native_battle_sessionの内部PC継続を新ループに使わない。旧証拠fixtureとTrialBattleは保存し、試遊版の仮HP/攻撃/AIは流用しない。
現行確認: native_battle_viewは停止snapshot、battle_windowは素材MAP表示、playtest_game/rulesは仮ルール。peer_script01_native_definitionsはDAT/UnitStatBlock/成長、native_dat_damage_adapter/native_damage_computeは実Skillと数式、native_dat_heal_adapterは回復、native_battle_outcomeは勝敗意味、peer_script01_battle_endはClaude所有の戦略IF。
- [ ] 1. Work所有battle_runtime.pyと専用testを追加。BattleActor/Deployment/Command/Frameを意味で定義し既存create_definition/unit_stat_blockでDAT生成。部隊/level_bonus/HP状態/scenarioは明示し、手動設定した検証戦闘と原作の合法出撃を区別。consti/技能/成長保持、stack/heap不要。
- [ ] 2. tick/命令接続。描画FPSと時間を分離、pause/速度で二重実行しない。既存地形/移動タイプ/速度/射程の意味を再利用、新pathfinderの差は体感比較対象。速度換算/間隔は根拠確認。
- [ ] 3. 実Skill攻撃/回復を数式へ結合。対象/条件/MP/間隔/命中/耐性/HP/EXP、死亡による行動停止/部隊/勝敗を実装。原作vtable破棄待ちは不要だが召喚/死亡技能/戦略副作用は省略不可。未対応は診断。
- [ ] 4. battle_runtime_view.pyへlive接続。既存素材MAP/Unit描画を再利用し選択/移動/攻撃/停止/pause/速度、HP/MP、弾/命中/回復を表示。VA入力を要求しない。新入力基盤と原作体感比較は別。
- [ ] 5. 実DAT/MAP複数Unit→死亡→勝敗の統合、Windows画面/EXEを確認。その後Claude戦略API/イベント/EXP/LvUpへ。原作比較無しではGolden/MATCH増加不可。
レビュー重点: DAT missing/@、親/成長、味方/敵/死亡、pause再開二重適用、召喚/連鎖の誤変換、演出と効果時点、未対応イベントの黙殺。
観測: 既存資料から不足だけ絞って短い操作/録画を依頼する。原作/セーブ変更なし。Vahren701.zipを原作へ上書きしない。現在ネイティブGUI操作可否は未確認。


### WORK-SEMANTIC-ROSTER-20261013 実装進捗
Task1のDAT生成/Actor/immutable snapshotは実装済（新規5/関連113PASS）。Command/Frame、live表示/時間/行動/勝敗は未接続。Task1全体をDONEにしない。次は原作MAPとこのrosterを画面へ接続し、動作可能範囲を広げる。


### WORK-SEMANTIC-VIEW-20261013
Task4のlive snapshot表示/情報選択/カメラを新runtimeに接続、原作MAP/3Unitで実Windows/新EXE確認。新規4/関連17PASS。Task2/3の時間/移動/攻撃/AI/勝敗は未接続。地形stairN/stairoff表示未解決。次は意味ベースMove/Stopと既存速度/地形計算→view入力。詳細固定handoff同checkpoint。

## WORK-SEMANTIC-TERRAIN-20261013
Task2部分: 実MAPの12100セル/33movetypeをRuntimeRoster.terrainへ接続。関連46PASS、source Windows起動確認。経路/衝突/時間/Move/Stopは未接続。画像stairN問題は既知step合成未実装。EXE更新は次の実行工程の区切り。詳細は固定handoff同checkpoint。

## WORK-SEMANTIC-CLOCK-GEOMETRY-20261013
Task2部分: DAT radius/radius_press→新UnitとBattleClock host時間adapterを接続。Space停止/再開と速度選択を実装。新規10/関連69PASS、新EXE build/Windows起動成功。Unit更新/移動/攻撃/AI/勝敗未接続。主線は同handoff末尾の通常Move/Stopと衝突入力、旧ABIの復帰解析ではない。


### 限定移動の統合設計（Work実装中）
既存DAT速度/軌道と新A*を結合し、Move/StopをGUIから実Unitへ渡す。未解決sceneryの描画範囲、高低差/特殊field、未知radiusはguardとして進入拒否。guardは原作衝突形状ではなく未対応領域の保守的除外。Unit重なりも半径和の保守的guardで押し合い未再現を明示。未検証を互換完了としない。時計は各tickに移動更新を呼び、停止中は進めない。普通戦闘の倍率1のみ、特殊dungeon未対応。


### WORK-SEMANTIC-MOVEMENT-20261013
限定Move/StopをDAT速度・新A*・GUI/時計へ接続し関連77PASS、source/EXE実移動・入力イベント停止確認。G2部分、G5未達。衝突guardは暫定で原作押し合い/高度未対応。詳細は固定handoff同checkpoint。最初の互換対象勢力をユーザー指定の迫真空手道場po2（長編ストーリー）とする。poo2別シナリオと区別。次はpo2開始/出撃の既存戦略IF照合と実技能/攻撃の意味ベース実行統合。


### 技能連鎖の入力統合（Work実装中）
迫真空手道場のsw_karate0はstr attack*0からnext→joint_skill/next3へ分岐し、karate_gunもnext3多段。単一rootのダメージだけを実行しない。既存NativeRegistriesを使い、継承後のscalar/listと由来、next/next3/pair_next/just_next/afterhitの参照を失わないruntime技能bookをUnitへ接続。next2等の未確認種別はraw保持して実行済としない。循環を検出して有限グラフ化、順序と重複は保持。GUIに元DATの技能名/helpの確認を追加するが、発動は未接続と明示。以後このbookを技能executorの入力に使用し、待機/連撃/next_first/next_lastは既存保存証拠で意味を確定してから実行する。


### WORK-SEMANTIC-SKILL-INPUTS-20261014
技能参照bookを実Unitへ接続し元DATの説明表示を追加。構造と実DATの新規7、関連75PASS、source/EXE全JSON・PNG一致。試験3体41root/137技能/115参照、next2未確定5。これは発動/時刻/命中の実装完了ではない。次はsw_karate0の待機→連撃→子技能を既存Rush tickの意味で実行しダメージ/演出へ接続。G5未達、原作Golden0/MATCH0。


### 連撃の意味ベース時間更新（Work実装中）
既存5501A0 intervalとB1218発射後count、B1930 raw interval正規化を再利用。新RushSequenceは原作アドレス/Task pool不要で、発射callbackが正常終了してからordinalを進める。callbackは実子生成/必要post-linkを担当し、未接続なら登録拒否、実行例外はfaultとして二重実行禁止。RuntimeRoster.tickへ移動→作成順action更新を接続。これは既存通常Unit処理の後に生成済Rushを処理する限定構成で、混合全Taskの互換完了ではない。初回待機はfactoryがinterval値で初期化する事実に合わせる。生DATのrush/rush_intervalは明示literalのみで、missing/@既定値はVERIFY。射撃コールバックの完成・元AIからの合法admissionは別工程、GUIへ仮ダメージを追加しない。


### WORK-SEMANTIC-RUSH-TIMING-20261014
明示発動済みRushの時間更新をroster/GUI時計入口へ接続、新規10/関連49PASS。初回/間隔/子callback後count、再入・faultの二重実行防止とconsumer停止を検証。実DAT＋合成emitterのsource windowで1/5tick call、新EXEはjob無し起動確認。攻撃発動/弾/HP変化のプレイ範囲は未拡大。次の成果基準を通常攻撃一回の実効果へ固定し、説明UIや独立helperだけで区切らない。G5未達。


### WORK-RESOLVED-CHILD-IMPACT-20261014
直接所持rootから明示解決済child impactへの参照経路検証を既存damage_skill_resolvedへ追加。関連120PASS。DAT親子関係は発動/命中証明ではなくGUI攻撃は未接続。田所sw_karate0の発動/子弾/命中の不足仕様はClaude限定依頼OPEN、Workは実装を担当。戦闘完成優先、G5未達。


### WORK-LIVE-EFFECT-BRIDGE-20261014
既存効果sessionと新ActorのHP/MP/stats/耐性/definition/RNGを共有し、解決済child命中のHP/EXPを表示へ接続。149PASS、新EXEbuild/起動成功。GUI命令/飛翔/命中自体は未接続、G5未達。ユーザー提供のマップテストsci_mtを比較入口として優先。unit_mt等の専用設定は通常po2と区別する。


### WORK-YAJU-ROOT-CONTRACT-20261014
Claude §80受領。倍率0 rootでも計算/RNG/handlerを省略しない回帰試験を追加、関連3PASS。弾初期位置・速度・生成tickは観測依頼へ分離。GUI攻撃は未拡大、G5未達。次は保存Missile待機/next3意味と共通生成入力を接続。固定handoff同checkpoint参照。


### WORK-MISSILE-WAIT-20261014
実DATの弾ごとのwait_timeをRuntimeActions/Roster時計へ接続。音呼出→次更新本体、失敗再実行防止。160PASS。生成位置・速度・実命中・プレイヤー発動は未接続でG5未達。EXE未更新。次はjoint寿命→next3と共通factory。固定handoff同checkpoint参照。


### WORK-JOINT-NEXT3-20261014
解決済み静止joint寿命→next3全順序/重複保持・親target継承をRuntimeActionsへ接続。実DAT Rushから2組の子生成要求を確認、29PASS。EXE更新/2frame起動成功、EXE内攻撃試験ではない。葉factory/飛翔/命中未接続、G5未達。詳細=固定handoff同checkpoint。


### WORK-LIVE-OBSERVATION-20261014
WRQ-20261014-CLAUDE-YAJU-ATTACK / P0 / PARTIAL。§81更新observerを利用して原作交戦中の第2ログ取得成功（9弾tag/10904snapshot、非同時読取あり）。詳細は固定handoff同checkpointと_work/work_live_observation_20261014_02_summary.json。生成入力/速度/時刻契約はログ分析前につき未確定、CLOSEDではない。Claude向け追加修正候補: attack_activityのflag0/負index判定、task pointer再利用時cache再検証。今は新チャット送信なし。Workはログ分析と実弾factory統合を優先。Golden/MATCH0。


### WORK-LIVE-MOTION-ANALYSIS-20261014
CLAUDE-YAJU-ATTACK / P0 / PARTIAL維持。WorkがACTUALログ02を分割・座標仮説比較し不一致も保存。参照=_work/work_live_observation_20261014_02_motion.json/固定handoff同checkpoint。次P0は普通弾の位置更新・終了順を保存54BA00と実測で照合して共通executorへ接続。torn=falseでも途中状態あり、観測segmentを発射数とみなさない。追加チャット依頼/ユーザー操作要求なし。Golden/MATCH0。


## WORK-CONTROLLED-DAT-AUTHORIZATION-20261014
- ユーザーが展開済み迫真戦記の改変を明示許可（ZIP版があるため）。試験用DATの編集を希望。以前の原本read-only指示に対する展開済みデータの例外として記録。ZIP原本・他AI所有ファイル・安全拒否/別経路迂回禁止は維持。EXEパッチは今回必要なし。現在まだDAT変更0。
- 実ファイル確認: game/a_default/script/6000_スキルテスト/0maptest.dat（CP932/167行）。sp_mt map=sKamakura_prot_wide5/member=inyume_st,hideshine,annyui。sp_mt2 member=a0003*20,unit_mt。unit_mt:unit_stはboat_gun、unit_st:yajuは異常に高いHP/回復等を設定。event_test.dat be_stはsiege_systemを実行。単純にmemberだけ減らしても技能/召喚/防衛兵器を排除できない。
- 次P0の試験DAT: 元技能sw_karate0は変更せず、攻撃役/静止標的/所持技能/召喚・部隊員/戦闘イベントを明示限定する。継承とclass由来技能を既存パーサーで検証し、変更前バックアップ+SHA+復元手順を用意。原作実行中のデータ差し替えは避け、適用準備完了後に再起動手順を伝える。準備前にユーザーへ再戦を要求しない。試験DAT由来の能力を通常yajuと同一視しない。
- 保存54BA00の追加確認: 8188..8192で更新count増加、8435..8454で距離終端/finished/終了step、8575..8623で命中処理、その後8625以降で移動枝。8868..8874は変位整数化と小数残余差引。前ログの終了時travelと矩形の差を単純な測定誤差として消去しない。未確定FPU引数/角度/初期化は未実装のまま。native普通弾移動executor追加は未完。
- 今回source/test/build変更なし、前126PASSは今回再実行なし。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。次は制御DATの継承検証と既存弾数値契約の接続。許可範囲は実データ試験条件に限定して扱い、拒否コード新取得への包括承認としない。


### WORK-CONTROLLED-OBSERVATION-20261014
CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。ユーザー許可の新規DATで空手1技能/2Unitだけの原作戦闘が起動、45秒ACTUALログ取得。参照=固定handoff同checkpoint、_work/work_controlled_observation_20261014_01_summary.json、work_observation_deployment.json。生成/命中/数式の新engine統合は未完、Golden/MATCH0。追加解析チャット送信なし。
WRQ-20261014-DAT-DELIMITER / 担当未予約（Workが所有確認後に処理） / P1 / OPEN。停止=既存parse_script_text。scenarioのpower/spot/roam後にセミコロンを欠く候補をmodelが許容し原作は112行で拒否。未完=文法差分の最小再現と修正、参照=deployment.json旧/新SHAとユーザー画像。モデルparse成功を原作load成功とみなさない。現行試験DATは修正済/原作出撃確認済。


### WORK-CLAUDE-817-SCHEDULING-20261014
CLAUDE-YAJU-ATTACK / P0 / PARTIAL。§81.7受領/元log SHA一致、実DAT生成連鎖の時刻回帰30PASS。全frame無欠落はWork未証明、生成次frame更新は観測された連鎖の範囲で支持。参照=固定handoff同checkpoint、test_battle_runtime_skills.py::ObservedKarateSchedulingTests。停止=普通弾生成角度/RNG/丸め/命中順。UserはPowerShell観測協力可能、今は追加操作不要。Golden/MATCH0。


### WORK-RESOLVED-LINEAR-MISSILE-20261014
通常弾の解決済み更新枝をRuntimeActionsへ統合。実DAT連鎖→飛翔→命中callback→終了、独立context経由HP/EXP処理の関連155PASS。EXE build/2Unit画面2frame起動成功（弾jobは起動試験対象外）。初期化・命中候補選択・GUI発射/描画は未接続。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。次P0=汎用factory/候補選択/命中演出adapter。詳細は固定handoff同checkpoint。


### WORK-LINEAR-LAUNCH-UNIT-HIT-20261014
G3/G4部分前進: 実DAT motion入力→観測支持の明示数値profile→弾更新→矩形/陣営Unit候補判定→native効果処理を合成配置の統合試験で接続、166PASS。初期化/候補列挙/描画/GUI発動未接続。新EXE buildとCLI起動確認、GUI再試験なし。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。次P0=実Unit候補adapterと生成・命中演出。

### WORK-LIVE-ROSTER-PROJECTILE-20261014
G3/G4部分前進: 実DAT普通弾→live Unit矩形判定→共有HP/EXP→next演出要求をRosterへ統合。177PASS、EXEbuild/CLI成功。発射初期化/候補順/GUI発動/画像音/AI/戦闘完走は未達。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。次は既存連鎖の生成入力と実表示を結び、操作から一攻撃を完走させる。長時間ログ増量より取得済み証拠の実装を優先。

### WORK-LIVE-PROJECTILE-DISPLAY-20261014
G1/G3表示経路前進: 通常弾のlive状態をread-onlyで既存GUIへ渡し、原作拳画像の寸法/回転/alpha/消滅を表示。source Windows2frame/実DAT弾1体確認、185PASS、新EXEbuild/CLI確認。命令発射/animation/音/全draw順は未達。次は保存ACTUAL52組と54BA00/54D8E0を使い、命中childの静止4コマ演出→終了を実装。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。

### WORK-HIT-ANIMATION-LIFECYCLE-20261014
実DAT子命中/HP更新→移動前centerの命中演出→4コマtick→寿命終了を統合試験で接続、174PASS、ガード変更後37PASS。source GUIで原作画像表示、EXEbuild/CLI成功。音は候補要求のみ、生成角/汎用factory/GUI発動未達。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。次は生成契約・音RNGを満たして通常攻撃の操作経路へ接続。

### WORK-RUNTIME-SOUND-AND-CHILD-ANGLE-20261014
原作音候補のRNG消費を既存数値モデルで接続し、共有戦闘RNG→音要求→Windows WAV backendへ。親表示角をchildへ伝達、実DAT命中統合177PASS。音混合/定位は未比較。新EXEbuild/CLI確認。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。次は汎用factoryとroot-chain poseをまとめ操作発動へ接続、Golden0/MATCH0。



### WORK-RESOLVED-HIT-FACTORY-20261014
命中後の普通nextを実Unit技能来歴から検証し、実DAT寸法/画像/寿命/音を本体factoryへ統合。178PASS、source WindowsのHP/EXP→演出/音確認、新EXEbuild/CLI成功。発射位置/角度RNGと合法発動は未解決。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。次はroot→Rush→joint→leafを操作発動へ接続。


### WORK-RUNTIME-RANDOM-RUSH-20261014
既存の連撃角度/RNG計算をRuntimeActions/実Rosterへ接続。登録・待機では乱数を消費せず各弾生成で共有RNGを1回使用。関連187PASS、召喚guard後35PASS、新EXEbuild/CLI確認。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。次はsword受付からroot効果/MP/突進/子生成を操作経路へ結ぶ。Golden0/MATCH0。


### WORK-SWORD-ROOT-PREFIX-20261014
通常sword受付の限定prefix→向き/MP→rootダメージを本体へ接続、184PASS。後続未接続のため攻撃成功にせず保存continuationでtick停止。EXEは前版/今turn GUI未実施。次はR4..R8へ継続しrootを再実行しない。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。


### WORK-SWORD-NEXT-AND-LUNGE-EVIDENCE-20261014
root後の音→連撃登録を再実行なしで接続、50PASS。突進は通常移動と異なり地上座標固定/矩形更新の特殊枝であることを既存観測と保存5795E0で確認。経路1種類のみ、生成式一般化は未証明。次は特殊window更新→slide/pair/post。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。EXE/GUI今turn未実施。


### WORK-SPECIAL-TRAJECTORY-CONSUMER-20261014
特殊突進の解決済み経路→矩形/索引/子表示→終端cleanupを既存Unit更新へ接続。共有実DAT Unitの命中矩形にも反映、関連480PASS＋追加統合後58PASS、新EXEbuild/CLI確認。新GUIはなおground座標表示、突進可視化/経路生成/root完了は未接続。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。

### WORK-LIVE-UNIT-DISPLAY-POSE-20261014
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。特殊motionのlive矩形→新GUI表示poseを接続、ground維持。関連69PASS、source Windows画像2Unit/20frame確認、EXEbuild/CLI成功。停止=VERIFY_SWORD_SLIDE、未完=579290生成式/子pose/pair/post/GUI攻撃。参照=固定handoff同checkpoint・_work/unit_pose_verification.json・保存B1253-01契約。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。追加依頼送信なし。

### WORK-SWORD-SLIDE-BUFFER-20261014
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。実DAT slide_speed→解決済み幾何入力から往復buffer生成→共有Unitへ接続。関連104PASS、生成/消費統合後527PASS、EXEbuild/CLI成功。停止=VERIFY_SWORD_PAIR。未完=距離/角度/trig前段・pair_next factory・57BE30・GUI攻撃。参照=固定handoff同checkpoint・_work/sword_slide_verification.json/evidence.json・保存B1253-01。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。新規依頼送信なし。

### WORK-SWORD-PAIR-JOINT-20261014
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。初期化済み不可視jointのlive caster追従→next3順序/子pose/来歴を本体接続。R7は明示生成RNG receiptを照合しVERIFY_SWORD_POSTへ、関連146PASS/EXEbuild・CLI成功。元initializer入力/乱数は未解明、合成receiptを原作実測としない。停止=57BE30、未完=R6幾何前段/R7初期化/子のcenter=end・swing描画/GUI発動。参照=固定handoff・_work/sword_pair_verification.json/observed_pose.json。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。新規依頼送信なし。


### WORK-SWORD-POST-VALUES-20261014
通常swordのR8前段を実DAT slow_per/slow_time→共有Unitへ接続。関連150PASS/FAIL0/ERROR0、新EXE build/CLI成功。待機・cooldownは未解明slotの明示入力を必須とし、後段未処理で停止を維持。 G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。次はpost後段と実入力の接続。GUI攻撃/一戦完走の達成とはしない。

- 後段依存の追加照合: Claude peer_script01_native_definitions.py:461/1057/1104のdef.talent_on=+75、special_77=+77をread-only確認。linked判定はこの既存意味を使える。Skill4CはB-20261013-1740-01（data/T011_SPECIAL_PROPERTY_SKILL4C_20261013.md）でspecial=on→1/整数→その値が確定済み。ただしoff/欠落のnative numeric値は同契約でもVERIFY。rootで省略されるから0と推測しない。Unit238/1F8/1F9の生成writerは今回ソース検索で未接続、次回この入力を解く。新しい仮defaultや後段skip実装は追加しなかった。


### WORK-SWORD-POST-TAIL-20261014
実DAT special・実defのtalent_on/special_77を発動後分岐へ接続。追加処理不要の枝は技能本体return AL1まで進み、VERIFY_SWORD_OUTER_ACTIONへ。関連155PASS/FAIL0/ERROR0、新EXE build/CLI成功。 G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。次は外側行動・同一tick接続。元EXE可視互換は未証明、Golden0/MATCH0。


## WORK-LIVE-MOTION-BINDING-RECOVERY-20261016
実UnitのHP/MP/能力値共有mappingを通常移動・吹き飛ばし継続処理がclearして例外になる不具合を修正。native_unit_motion.pyの段階state反映をupdateに変更。RuntimeRoster.advance_resolved_unit_motionで移動後の命中/描画位置publicationも更新し、stale geometryを検出する。未完cast中は進めず、57AD3C到達をAI完了にしない。
- 前回保存済みの製品2fileとtest1fileを検証JSONのSHAと照合し一致。関連8module581PASS/FAIL0/ERROR0、63.625秒（記録値）。今回再実行ではなく既存terminal結果の回収。参照=_work/live_motion_binding_verification.json。実DAT Unitと合成2点経路/knock fixtureを使用、原作実機比較ではない。全suite未実施、既知sourcebook2FAIL未解消。
- 前回GUI起動は自動承認サービスの利用制限で未実行。今回は同じLocal経路の読取/プロセスが成功し記録回収。今回修正を含むEXE build/GUI検証はこのcheckpoint時点で未実施。従来EXEはPOST-TAIL版。
- G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Gameplay Golden0/strict MATCH0。原本/Claude source非編集。HEAD be45dc2d563dcc1885a3caf4e3c8af43f6b8619b。
- 次: 現行sourceのbuild/GUI確認、外側行動returnとmotion/弾更新の統合。Unitflag producer・R6幾何・R7初期化RNG・wait/cooldown・26Cを未知のまま既定値化しない。追加EXE解析は保存成果を先に照合しREA MCP/Ghidraを優先検討、拒否範囲は再取得しない。

- 同checkpoint追記: 現行EXE build exit0/CLI --help exit0、SHA d2db89ad54eb8d22e0b26852a6b6d7f0df4d54322ec5f376e2384ec1cb6bb91a。_work/live_motion_build_verification.json。source Windows GUIもexit0、実DAT2Unitを合成2点経路で更新後20frame一時停止表示、描画位置(272,260)→(288,264)、sprite欠落0/pose gap0。PNG読み戻し確認。_work/live_motion_view_result.json/live_motion_view.png。GUIはsource、EXE内戦闘の試験ではない。海上は合成配置、地形一致を主張しない。stairN/stairoff静的素材解決は残存。初回GUIはPowerShell日本語encoding未指定で素材path読取失敗1回、UTF-8明示後成功。製品source変更なし。次は外側行動returnと同一tick統合。Golden0/MATCH0。


## WORK-SWORD-OUTER-RETURN-20261016
- 前turnはREA紹介への回答のみで開発state変更なし(NO_PROGRESS)。今回は最新handoff/WRQ/Git dirtyを確認しWork本体battle_runtime.py/testsのみ変更。原本/Claude所有ファイル非編集、新規EXE解析なし。
- RuntimeRoster.resume_resolved_sword_outer_actionを追加。既存native_unit_ai.resume_selected_skill_post（57E610/577600/571A40/57B375）を再利用し、技能本体AL1済みかつ追加操作処理不要の枝だけ_sword_prefixesを解除。実HP/MP/EXP/RNG/弾登録を再実行しない。local frameは制御値で、元stack/allocation再現を要求しない。
- 操作側577600が必要ならVERIFY_SWORD_OUTER_CONTROLLEDで停止、未実行の副作用をreturnと偽らない。Unit1863C/8C/1F8は既存live値を要求し欠落を0としない。重複resume拒否。
- 実DAT root→Rush→slide→pair→post→outer return→次tickのRush1発目まで既存統合testを延長。R6幾何/R7生成RNG/flag/wait/cooldownは明示SYNTHETIC条件、GUIから発動可能になったとはしない。特殊motionと弾の同一tick接続は次工程。
- TEST: 新規3件missing API ERROR3を確認→実装。初段Roster37PASSだが存在しないtest_native_unit_ai指定でloader ERROR1、指定修正後4module496PASS/FAIL0/ERROR0、61.141秒、PID10728 exit0。_work/sword_outer_verification.json。全suite未実施、既知sourcebook2FAIL未解消。以前581と合算しない。
- EXE build/CLI --help exit0、SHA 9a0507a003419b1e0afd0f6c1e147d8c69b86c4ab02a96f3c099e90017419a7b。_work/sword_outer_build.log。今回GUI/原作実機比較未実施、Gameplay Golden0/strict MATCH0。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。
- 次P0: 保存577600操作側契約とUnitflag生成を照合し、プレイヤー発動に必要な副作用を接続。特殊motionと既存弾queueの順序/初回更新を統合する。R6幾何・R7初期化/RNG・wait/cooldown/26C未知を黙って既定値化しない。拒否範囲維持。REA/Ghidraは新規不足仕様の調査時に優先検討、既存証拠の再取得不要。


## WORK-CONTROLLED-POST-DEPENDENCIES-20261016
- 前goal turn=outer return実装/496PASS/build/checkpointでPROGRESS。今回保存B契約とGhidra疑似codeを照合。製品source変更/テスト再実行/EXE buildなし。最新検証は前checkpoint496PASS/FAIL0/ERROR0、Golden0/MATCH0。
- 保存T013_POST_ACTION_SKILL_577600_CONTRACT_20261013.mdとexe/T013_POST_ACTION_SKILL_577600_20261013.txt、T012_ACTION_FRAME_RESET_SPATIAL_POSTSELECT_ORDER_20261014.mdを再利用。577600の返ALをcaller成功値へコピーしてはならず、後続571A40/条件56BA80は別処理。通常枝は44D070照合→special使用回数5799D0→候補再構築576450→必要なら579BA0属性filter→候補count→選択/rearm。これを省略して操作枝を解除しない。
- 保存zipのdecomp_0044xxxx.c 44D070はunsigned整数keyのtree完全一致検索で、見つからなければsentinelを返す。577600のcaller key/map入力は疑似Cで失われており未確定。decomp_0057xxxx.c 576450は候補listをclearしてsource範囲から再構築、577600中の呼出後の18654が技能切替可否に影響する。内部list形状は新設計可能だが候補順/内容は保持が必要。
- REA MCP binary_sessionは成功、server rea-agents6.5.0。open=false、Ghidra provider not_configured: GHIDRA_INSTALL_DIR未設定、analyzeHeadless/native decompiler未検出。これは接続不能や安全拒否ではなくprovider設定不足。現在のREAによる新規native解析はBLOCKED、保存Ghidra資料は使用可能。設定変更/新規install/原本読取/拒否範囲再試行は実施していない。
- 次P0: 577697の44D070 callerについてkey/mapの保存assemblyを限定検索、なければ既存Ghidraの場所と版を確認しREA provider接続を修復する。576450/579BA0は既存B2356-02/B0718-02契約を再利用してsemantic candidate listへ接続。新規原本解析はこの不足だけ。現在G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。戦闘完走/GUI攻撃未達。


## WORK-SWORD-SYMBOLIC-SLOW-20261016
- 前turnはREA設定保存でPROGRESS。REA binary_session再確認では同じ旧サーバー起動時刻/未設定状態、再接続はまだ。設定待ちだけで止めず保存証拠で独立DAT処理を接続。
- battle_runtime.pyのresume_resolved_sword_postでslow_per=on/offを受入。保存generic parser50536A/505381..5053C3の非数値cache0、Ghidra decomp_0059xxxx.c:9201の初期zero判定と9555..9565(sword59CC3B)の最終補正を結合。最終倍率は両者1.0、前段のon=-1/off=1をそのまま使わない。slow_time symbolic/式/@/listは未解明のまま拒否維持。元DATやClaude source非編集、FPU全体profile変更なし。
- TEST: 既存境界testを拡張、変更前ERROR1（未対応拒否）→変更後runtime/skills44PASS/FAIL0/ERROR0、56.995秒、PID11104 exit0。HP/MP/EXP/RNG不変と既存数字80/0/待機overflowも確認。_work/sword_symbolic_slow_verification.json。DAT_DERIVED+SYNTHETICで原作実機比較なし。全suite/新EXE build/GUIは今回未実施、EXEは前outer-return版のまま。以前496/581と合算しない。
- G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。次P0はREA再接続確認→577697の検索key/map不足確認→操作側候補再構築/切替、続いてmotion/弾更新の同一tick統合。再接続前は保存資料を利用し拒否範囲を迂回しない。


## WORK-REA-RECOVERY-CONTROLLED-KEY-20261018
- Local直結MCPで固定handoff/WRQを読取成功。以前Compact tunnelのtimeoutは現在のLocal読取には再現せず。旧PID9076 session消失、Java processなし。保存REA JSONは完成したエラー応答でprovider_timeout/330000ms/Ghidra startup deadline elapsed。SHA256=30c3336bf696fd9545b76c3567e435d4d234f041a152ac7abfb88b663caed5fa。解析成功/実行継続中とは扱わない。同じ全体解析再実行0。
- 現REA MCP6.5.0起動2026-10-18T04:41:15.052Z、Ghidra12.1.4/Java21 availableをbinary_sessionで確認。旧not_configuredは解消。新target未open、新しい全体Ghidra解析なし。
- STATIC限定read-only: 原本と同SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187の既存rea_lab/targets/hakushin067_Vahren.exeをpefile/Capstoneで577600..577686および577680..5776B8のみ確認。timeout後の限定調査であり安全拒否範囲の再試行なし。範囲SHAは824f62d6bb9fd7635f6b43f520991012d013b2b08cbb8bf2654278b105c3aaa2と34b3a3984f324663e1d6184386c5b46c9c7e05d563185428ce8cad1496d67eaa。
- 確定: prolog push ecx/ebx/ebp/esi/edi後の[esp+1C]は第2引数Skill pointer。577623 mov ebx,[esp+1C]、577686 mov esi,[ebx+40]。577697 lea ecx,[ebp+1865C]、57769D lea ebx,[esp+1C]、5776A1 lea eax,[esp+18]、5776A5 call44D070、5776AA mov eax,[eax]、5776AC cmp eax,[ebp+18660]、5776B2 je577706。従って既保存44D070 unsigned pointer-key完全一致契約への入力はUnit+1865C mapとSkill引数pointer。旧B要約の『577697 call』は準備位置で実callは5776A5。map producer/技能所有集合の生成は未接続、意味上の集合lookupへ実装可能だが未確認集合を捏造しない。
- 最新B HANDOFF末尾を参照: B-20261018-1328-01 a0054直接2技能宣言等はSOURCE限定READY、合法取得/共有cooldownはVERIFY。この成果を577600 map producer確定とは扱わない。B安全拒否0911/1110等は維持、他所有資料非編集。HEAD be45dc2d563dcc1885a3caf4e3c8af43f6b8619b、既存dirty維持。
- 今回製品変更/テスト/build/実機なし。最新製品検証44PASS、EXEはouter-return版のまま。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Gameplay Golden0/strict MATCH0。
- 次P0: battle_runtime.py resume_resolved_sword_outer_actionのcontrolled枝へ、実効技能所有集合lookup・候補再構築576450・必要579BA0 filterを接続。後続571A40/条件56BA80を飛ばさない。保存済native_unit_aiとB契約を再利用し、map producer/候補入力の未確定だけ照合する。motion/弾同一tick統合へ続く。


## WORK-SKILL-LIFECYCLE-POST-UI-20261018
- 577600統合前に検索集合と候補sourceの生成/削除を照合。既保存Ghidra decomp_0057xxxx.c FUN_574E30はsource vector18640..18644から最初の一致を除去、候補list18650/654から一致全件除去、579AA0/510850で1865C集合から除去。static疑似Cのみ、原作実機ではない。
- 限定STATIC x86 574D70..574E30（同原本SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187、範囲SHA174ee756b101bb9349d1095bea29caebfed74d66d40ad10d97885c4943706f02）。574D7F lea ebx,[Unit+1865C]→565780 node payload=Skill引数→5158E0登録が両順序枝に先行。第3引数非0は18640 vector先頭側insertとcandidate先頭insert、0は末尾側append。node生成565780保存疑似Cはpayload+0C=Skill。集合と順序付き候補を区別し、重複を集合で消さない。DAT生成での574D70呼出順/第3引数は未照合、definition.skillsだけを無条件同一視しない。
- 保存Ghidra FUN_576450/5764A0は候補clear後source rangeを先頭から順にcopy。乱数/MP callはその保存局所にはない。既B契約再利用で新解析件数に重複加算しない。
- 保存Ghidra FUN_56BA80は表示有効global gate、選択Troop/Unitの1F9走査、DrawEdgeと操作panel virtual calls/56BE50/453C20等。新設計ではpanel refresh通知に置換する候補。全calleeの作用を今回確定したとはしないため『ゲーム副作用なし』やcontrolled return完成とはまだしない。元GUIコンテナ/Win32 GDIの逐語復元を完成条件に戻さない。
- 製品ソース/テスト/build変更なし。意図したcontrolled統合は入力生成の不足が判明したため未実装。既存44PASSは過去結果で今回再実行0。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。
- 次は既存保存コードの574D70 callerでDAT実効Skill列→順序付きsource/検索集合の対応を限定照合し、battle_runtime.pyのcontrolled continuationへ直接つなぐ。元heap/list ABIを新実装の入力要件にしない。56BA80は新GUI更新境界として切り分け、callee未知を記録する。

- 同checkpoint追加照合: 保存Ghidraで574D70の直接callerはScript_DispatchWorldCommand 4AB94B（動的追加）。初期生成は571B70内5739B1 lookup→5739CA vector append→5739D2/5739E0 tree登録。kind6は通常登録skip、kind5はUnit130が0の時だけ別slot格納、その他は既登録を除いた最初の出現順。sword134、MP0 missile135/MP非0 missile136、heal137、summon138、special>0なら139を立てる。原作初期列をdefinition.skillsと同一視する前にClaude findings§24前後の実効技能生成結果とこの後段filterを結合する。静的疑似Cのレジスタ復元欠落は残る。新原本解析は追加なし。
- 最優先再開位置を更新: recovered_source/peer_script01_ghidra_named_decomp_20261011.zip のdecomp_0057xxxx.c L2132..2205、Claude findings L672以降、battle_runtime.py bind_effect_session。初期選択候補の実DAT生成→controlled postへ接続。574D70は初期生成そのものではなく動的追加なので再調査の主対象にしない。


## WORK-RESOLVED-UNIT-SKILL-CHOICES-20261018
- 実装: battle_runtime_skills.pyにRuntimeSkillChoices/initialize_skill_choices、battle_runtime.pyにinitialize_resolved_unit_skillsとskill_choices保存、begin_resolved_sword_prefixの所有チェック接続を追加。既存の定義/HP/MP/RNG共有経路は維持。
- 入力は解決済みUnit技能列を明示供給。def.skillsを自動で部隊補正済みとみなさない。保存571B70:5739B1..573AE6に基づきkind6除外/最初のkind5をcharge slot/他kindの最初出現順を保持、candidateはsourceの同順copy。正の能力bit134..139のみlive Unitへ反映し、未確定のconstructorゼロ値・first-skill26D/1A4は捏造しない。未知func/非literal MP/未登録Skillは拒否。初期化はonce-only、未完cast中拒否、事前検証失敗でpublishしない。
- 生成済choicesがあればroot攻撃のowned判定はその集合を使用。未初期化時の従来def所有チェックは既存限定経路として残存。resolved Unit技能列を自動生成してbind_effect_sessionから渡す経路、controlled577600候補切替、動的技能変更は未接続。GUI攻撃完了や全Unit初期化完成とは扱わない。
- TEST: 新規4件。専用2件RED(未実装assert FAIL2)→PASS2。runtime/skills関連2module48PASS/FAIL0/ERROR0、205.141秒、LocalPID39648 exit0(runtime210.44秒)。実DAT yajuの列を明示fixtureとして供給しcharge/status/MP0非0/special/重複/順序/所有から除外された攻撃の拒否、HP/MP/EXP/RNG不変、失敗時非公開を検証。DAT_DERIVED+SYNTHETICで部隊技能生成そのものや原作実機一致の証明ではない。
- 全suite/広域回帰/新EXE build/GUI未実施。既知sourcebook2FAIL未解消。EXEは旧outer-return版。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。原本/Claude/A-E資料非編集、Git操作禁止維持。
- 検査注意: 無限定git diff --checkは既存CRLF資料を大量のtrailing whitespaceとして出力。今回のコード合否に使わず他owner一括整形0。4変更PythonファイルのAST parse成功。次回は対象限定・出力上限付き検査にする。
- 次P0: 571B70の技能列前処理（部隊由来追加/除外、58DA40）をClaude既存生成と照合し、この初期化へ供給する。併せてsource/owned/candidatesを577600 controlled continuationへ接続。内部heap addressやlist nodeの一致を新しいAPI要件にしない。新規原本解析は不足だけ、580280等拒否範囲維持。


## WORK-AUTO-LEADER-SKILL-CHOICES-20261018
- RuntimeRoster.bind_effect_sessionで通常self-leading Unitの実DAT def技能列を自動でinitialize_skill_choicesへ接続。明示的なinitialize_unit_skills=Falseはcaller解決待ちとしてunit_skill_gapsへ。neutral_78/roam_spot/別leaderは既定の自己def列で代用せずleader/member augmentation VERIFY。gapがあるUnitのroot sword開始は効果/MP/RNG commit前に拒否。解決済み列を明示初期化すればgapを解除する。
- 保存Ghidra571B70 L1963..1967: DWORD+134とWORD+138を0化するため、既存初期化APIも134..139の全6bitを生成結果へ設定。正bitのみだった前checkpointの制限をここで解消。130chargeはsemantic tag保存、旧pointerを要求しない。未解決1A4/+26D、操作flag1F8等は補完しない。
- 限定x86 read-only 5734BE..573527、同原本SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187、範囲SHA9e6339835c8a07c3b1dcdc10de04b2b1ec46c3beca56394ff530d42be6bd9fa4。5734BE ECX=Unit1C8→+EC→42E8E0でdef列copy、5734E5/EF def78/94 gate、573507..517別leader比較。保存疑似Cの5736AB以降はneutral/roam時member補正、それ以外の通常selfleaderは両augmentationをskip。配下/中立の未実装範囲をselfleaderで成功扱いしない。
- 追加read-only既存Ghidra: constructorはUnit18638/1863CにAAFBB8を設定。56B650保存疑似CはAAFBB8+40(AAFBF8)=8。選択なしは通常DAT技能/nullではなく組込みkind8。attr/+120/+4C等は未確定、577600の普通技能集合lookupを一律適用しない。新規原本取得なし（このkind8照合は保存zipのみ）。
- TEST: 新規2件RED=未実装keyword TypeError2→実装。runtime/skills/actions関連3module79PASS/FAIL0/ERROR0、189.000秒、PID42540 exit0(runtime193.06秒)。実DAT yaju/kmr通常leader初期化、charge/6capabilitybits、配下gapと攻撃前拒否、既存発動・回復・効果・action schedulerを回帰。DAT_DERIVED+SYNTHETIC、旧EXE比較ではない。全suite/広域は未実施、既知sourcebook2FAIL未解消。
- BUILD: PyInstaller exit0/108.0秒、CLI --help exit0、EXE SHA33d1fceacc4203b5373230420f23d15166e23800ab22df06a1ffe4a0d01ac2d6。_work/unit_skill_choices_build.log/verification.json（実名unit_skill_choices_build_verification.json）。source/test4file SHA前後一致。GUI/EXE内の戦闘実行は未実施。GUI mainはまだeffect_sessionを自動bindしないので、これはコアAPI初期化の接続でありGUI攻撃完成ではない。
- G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。Golden0/MATCH0。原本/Claude/A-Eソース非編集。今回Work変更=src/hakushin_compat/battle_runtime.py、tests/test_battle_runtime.py。前checkpointのruntime_skills/helperもbuildへ収録。
- 次P0: 組込みkind8選択の意味(+120/+4C/属性)を保存証拠から限定照合→semantic selected/previous state→577600候補再構築/切替→UI更新通知。部隊配下の技能付与は既存583F40/5842F0/5882F0成果を確認して実装。kind8をnullや通常root技能に置換しない。motion/弾同一tick、GUI入力、戦闘完走は引続き未接続。


## WORK-STANDARD-SELECTION-RESTORE-20261018
- 前turnのREA xrefsは300秒MCP timeout後JavaPID22424終了確認済。同要求の再起動なし。Localで同SHA原本解析copyのAAFBB8 literal参照位置だけ検索し、未拒否startup 603A70/608630各32byteを限定読取。603A70 pushAAFBB8→599600 ctor、608630→467A40 destructor。603A70範囲SHA6f0cc09a81e08c9082e480a0795fcfa15c2e9c16df8354ec78709c7b6a6abf1e、608630範囲SHA6ae666637e9b677f8ebe06ac6d3af78abd2061f3ac2a0bf20da6214ca068b505。対象SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。
- 保存Ghidra599600でattr110空/120=0、末尾599900でspecial4C=0。56B650の限定命令照合で56B83CがAAFBB8+40=8を設定、402800の属性書込先はAB1138/AADE38/AB1B68/AB2598/AAF288/AB2FB8/AAE868/AB0718でありAAFCC8ではない。56B650..56BA80範囲SHA4a8be4b0a8453aa78c7ec941e4dd0b6a9b79b3395e5b12082d1c6db422917290。通常選択はkind8/空属性/special0として確定（STATIC、実機観測なし）。
- 実装src/hakushin_compat/battle_runtime.py: bind_effect_sessionが既存の明示値を保存しつつ18638/1863Cを通常選択tokenで初期化。旧pointer literalは互換adapter内tokenであり新heapのaddress入力要件ではない。resume_resolved_sword_standard_selectionをcontrolled continuationへ追加。通常→通常のみ、所有技能source全順序をcandidateへ復元。emptyは577600 AL0、それ以外AL1。どちらもcallerがALを無視し571A40→56BA80へ進むためVERIFY_SWORD_OUTER_UIで保持。HP/MP/EXP/RNG/timer再実行なし、二重再開拒否、未完castのtick停止維持。他の選択/過去選択値・配下skillgapは拒否。
- TEST tests/test_battle_runtime.py新規2件: 未実装でERROR2（18638/1863Cなし、45.817秒PID42424 exit1）→runtime/skills/actions 3module81PASS/FAIL0/ERROR0、178.399秒、PID42080 exit0(runtime182.55秒)。DAT_DERIVED+SYNTHETIC。全suite/広域/EXE再build/GUI実行は今回未実施。前EXEはこの差分未収録。既知sourcebook2FAIL未解消、Golden0/MATCH0。
- 次P0: 56BA80/56BE50の表示用技能一覧再構築を新UI状態通知へ置換し、操作側の行動returnへ接続。保存56BA80は選択部隊・Unit1F9に応じpanel表示/DrawEdge、56BE50は577EE0を呼び表示可能技能を収集・描画。577EE0はsource18640からspecial使用回数/現在選択/summon容量で返却vectorを構成。56F130は一時tree処理。表示更新を無条件no-opと断言せず必要なUI状態契約を作る。原GDI/container/heap一致は目標でない。
- 完成ゲートG1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。WRQ-20261014-CLAUDE-YAJU-ATTACK PARTIAL、停止VA56BA80（通常→通常限定577600復元接続）。他ownerソース/原本非編集、禁止Git操作なし。


## WORK-CONTROLLED-RETURN-UI-20261018
通常→通常のcontrolled postから次tick復帰を接続。UIはrevision通知方式へ。関連93PASS、EXE build/helpとWindows停止画面2frames確認。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。GUI発動/AI/勝敗/戦略復帰未接続。詳細は固定handoff同checkpoint。


## WORK-RUNTIME-DAMAGE-BINDINGS-20261018
実context最低ダメージ1/耐性係数と通常Unit命中処理をRuntimeRosterへ接続。関連103PASS、新EXE build/help。GUIからの攻撃開始と通常戦闘完走は未達。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。


## WORK-RUNTIME-ROOT-DAT-20261018
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。root rush/damageを実DATから取得、呼出側不一致をcommit前拒否。関連105PASS、新EXE build/help成功。GUI攻撃/初期context/AI/戦闘完走は未達。固定handoff同checkpoint参照。Golden0/MATCH0、依頼CLOSED化なし。


## WORK-OBSERVED-MISSILE-CONTEXT-20261018
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。保存ACTUAL弾記録でD/E=1/1とother=selfを確認。命中contextから参照有無を導出し発射前に矛盾拒否、関連88PASS。root初期context/GUI攻撃等は未完、今回EXE未build。固定handoff同checkpoint参照。Golden0/MATCH0。


## WORK-SEMANTIC-SWORD-AIM-20261018
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。公開Unit位置→semantic方向/角度→root/連撃への捕捉角継承を接続。関連93PASS＋拡張1件PASS（重複あり）、原作保存27例のdirection不一致0。新EXE build/help成功、GUI実行なし。厳密数値一致/戦闘完走未達。詳細は固定handoff。


## WORK-SEMANTIC-SWORD-SLIDE-20261019
実Unitの捕捉位置と解決済み半径、実DAT slideから既存往復経路生成へ接続。関連131PASS、build/help成功。GUI攻撃/AI/一戦完走未達、G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。半径未解決は拒否。Astra medium継続、high候補はWRQに集約。


## WORK-INITIAL-UNIT-GEOMETRY-20261019
初期矩形→実DAT半径→live Unit生成→突進の接続を確認。88PASS＋既存拡張1PASS。GUIからの初期矩形供給/攻撃は未完、G5/G7/G8未達。EXE未更新、Golden0/MATCH0。


## WORK-RESEARCH-INTAKE-20261019

- ユーザーの研究資料活用確認を受け、A/B/C/D HANDOFF末尾、E cp187、Claude findings末尾、REA古いPROGRESSだけでなく新しいQC/復旧監査を横断読取。A末尾20261014-0302、C20261016-0122、D20261016-0137、B新着20261019-0117、REA2340/0034を確認。最新成果すべての統合完了とは主張しない。
- 重要な未統合証拠: B0117のcaller分類から既存exe/T012_DAMAGE_CALLER_CONTEXTS.txtを直接照合。UTF16 BOMの保存テキスト。VA57E7A5 lea context=Unit+7C、57E7A8 source=Unit、57E7AA context+8=Skill、57E7AD other=0、57E7B4 WORD+C=0x100(C0/D1)、57E7BA BYTE+E=1。context+Fの書込はこの窓にない。これまでroot context全体を観測待ちとしていたのは拾い上げ不足。次はこの15byteの既存確定書込をroot adapterへ接続し、+Fのconsumer有無を既存モデルで確認。新規拒否済57E650本体取得はしていない。
- B0117の正式READYマーカー保存は安全拒否でBLOCKED/NOT READY。Workはその正式状態を昇格・代理保存しない。今回の実装判断の出所はWorkが直接読んだ既存caller命令であり、B正式台帳を修正しない。
- REA 20261018-21H/2340 QC: 527ED0選択解除prefixはWorkと整合。527F27以後UI帰還、5685FD mode2判定→4C22B0(delete0)→56861A→死亡側575F71/575F91復帰が未接続候補。PROGRESS/QUEUEのEPERMによる古い表示だけを最新状態とみなさない。REA0034 preflight拒否は維持し、代理再実行しない。
- Aはイベントclock/区切り文法、CはWorld入口変数と子event、Dは旧DirectMusic初期化/終了ABIが最新末尾。現在の攻撃入口を直接解除する資料ではなく、物語接続/音声参照として保持。新エンジンの内部実装を旧COM ABIへ戻さない。
- 次の優先度を変更: root contextの既存確定書込の実装接続→死亡/選択解除の復帰不足→初期描画矩形の素材由来接続。新規広範解析より保存済み未統合契約を優先。追加観測要望はparent PARTIAL維持、root書込15byteはSTATICで解決し、観測はruntime比較用途へ縮小。今回の横断照合による新テスト/buildなし、直前88PASS+既存拡張1PASSを流用計数しない。Golden0/MATCH0。


## WORK-ROOT-CONTEXT-INITIALIZER-20261019
通常攻撃root contextの確定書込を製品へ接続、E1の補助効果VERIFY維持、95PASS＋拡張重複1PASS、新EXE build/help成功。G5/G7/G8未達。死亡後の選択解除復帰へ進む。


## WORK-TROOP-SELECTION-RETURN-20261019
部隊更新: 選択解除済み二枝からの表示通知・returnを接続。GUI/親死亡/一戦完走は未達。24PASS、DAT runner4PASS、関連3module340PASS/FAIL0/ERROR0（最終runner差分は別4件、重複あり）。次=selected非empty/normal controlled UI return→死亡側の二つの部隊更新と再読条件の接続。固定handoff参照。


## WORK-TROOP-LIVE-UI-RETURN-20261019
部隊更新の残UI2枝と選択解除の再呼出しに対応。35PASS＋最終27PASS（重複）。前回340PASSは今回再実行していない。次=死亡側からの2callと前段graph接続。GUI/一戦完走ゲート未達。固定handoff参照。

## WORK-DEATH-EMBEDDED-WINDOWS-20261019
死亡graphの埋込window解除3個を接続、98PASS、新EXE build/help成功。停止575F15。子効果解除と部隊更新から親死亡への接続が次。一戦完走未達、G1/G2/G3/G4/G6 PARTIAL・G5/G7/G8未達。固定handoff参照。

## WORK-DEATH-GRAPH-RETURN-20261019
確認済み通常死亡枝の子解除・部隊更新・本体解除returnを統合。実DAT入力の明示到達試験と合成部隊分岐、最終353PASS、新EXE build/help成功。GUI起動はeffect session未生成、移動操作まで。次は製品起動/攻撃から既存部品を結ぶ工程と致死前段。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。固定handoff末尾の条件・未完範囲を優先。

## WORK-RUNTIME-EFFECT-BINDING-20261019
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work統合 / P0 / PARTIAL。GUI起動→既存effect session/共有Unit状態/実DAT技能・damage contextを接続。Unit185FCはhasexp*levelとSTATIC確定し実装（5732AB..5732D0/62820C）。未完=初期描画矩形、残action状態、受付/子生成/攻撃GUI、致死/AI。参照=固定handoff同checkpoint。28PASS、EXE Windows表示3体・14tick確認、戦闘完走なし。既存REA-DEATH依頼はPARTIAL維持。追加の広範解析/ユーザー操作は不要、死亡観測準備OPEN。

## WORK-RUNTIME-INITIAL-GEOMETRY-20261019
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work統合 / P0 / PARTIAL。普通のDAT表示画像+w/h/sub_image_even→半径/命中矩形→移動後の再公開/表示寸法を接続。原作画像alias解決の全互換は未証明、特殊画像はVERIFY。59件最終PASS＋同一本体の他46件PASS（単一105PASSではない）、EXE実画面で108px移動・pose不整合0。停止=残Unit初期値/受付/root/Rush/pair/攻撃入力、致死/AI/勝敗。参照=固定handoff同checkpoint。既存REA-DEATH PARTIAL/死亡観測準備OPEN維持。画像比較は今後の短時間観測候補（Workが条件と手順を用意するまでユーザー操作依頼なし）。

## WORK-RUNTIME-FRESH-HIT-STATE-20261019
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。fresh8C/8D/8E/1A8を既存STATICからGUI Unitへ接続、24PASS。停止=初回被弾HPバーadapter(577100)→survivor return→root/Rush/子生成/入力。fixture185F4=1で回避しない。既存REA-DEATH PARTIAL、ユーザー死亡観測準備OPEN。EXE今回未build。固定handoff同checkpoint参照。

## WORK-RUNTIME-HIT-PRESENTATION-20261019
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。初回HP表示を新GUIへ接続、旧window依存を除きsurvivor/counter復帰、表示timer150を新host tickへ。関連123PASS+最終専用1PASS（重複）、新EXE build/help/起動成功。停止=実攻撃命令→DAT numeric/tail→Rush/joint/linear生成。REA-DEATH PARTIAL/死亡観測準備OPEN、追加ユーザー操作なし。固定handoff同checkpoint参照。

## WORK-DAT-ROOT-DAMAGE-INPUTS-20261019
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。special/rush/flash/rangeと実Unit/contextを攻撃入力へ接続、実DAT rootをdamage fixtureなしで実行、71PASS。停止=EXP有効子技能の段階別丸め→Rush/joint/linear factories→攻撃命令。WRQ-B-NUMERICは既存成果を再利用しWork側EXP caller契約を照合（追加の広範解析依頼なし）。REA-DEATH PARTIAL/死亡観測準備OPEN。ユーザー操作不要。固定handoff同checkpoint参照。

## WORK-DAT-CHILD-STAGED-EXP-20261019
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。保存551E50の第1段ceil/第2段truncを区別した明示仮定profileで、実DAT子技能のHP減少/EXP付与/survivor表示まで接続。関連208PASS。原作FPU比較未実施、Golden0/MATCH0。次停止=linear launchの実DAT自動入力→Rush/joint/pair→攻撃命令。REA-DEATH PARTIAL、死亡観測準備OPEN。今はユーザー操作不要、必要時に条件と秒数を提示。固定handoff同checkpoint参照。

## WORK-LINEAR-DAT-IMPACT-20261019
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。弾の実命中時にDAT/対象からdamage入力を自動接続。実DAT2弾→HP/EXP/被弾/子生成要求→消滅まで複数tick検証、関連108PASS。新EXE build/help/Windows起動3Unit・8ticks成功、攻撃GUIは未接続。次=Rush emit→joi/joi2 factory→linear→攻撃命令。REA-DEATH PARTIAL/死亡観測準備OPEN。追加操作不要。固定handoff同checkpoint参照。

## WORK-STATIONARY-JOINT-CHAIN-20261019
WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。生成済みjoiの待機→追従→joi2固定位置→next3順の3弾→damage/EXPを接続、関連99PASS。停止=Rush emit時の初期化契約（start_random_degreeと生成時RNG/pose）→root/pair/攻撃命令。580280拒否維持。REA-DEATH PARTIAL/死亡観測準備OPEN、ユーザー操作不要。固定handoff同checkpoint参照。

## WORK-LINEAR-BRANCH-GUARDS-20261019
通常linearへの未対応hard/onehit/bom/wait_time混入を防止、100PASS。WRQ-20261019-CLAUDE-JOINT-INIT OPEN（既存資料/観測優先、今のユーザー操作不要）。生成初期値/RNGと攻撃入力は未完、固定handoff同checkpoint参照。

## WORK-RUNTIME-HOLD-VIEW-20261019
Work / P0統合 / PARTIAL。未完戦闘処理でGUIを保持しpause、再実行を防止、診断receiptを出力。関連56PASS、新EXE build/help成功、人工停止条件のソースWindows画面3frames/tick0/状態保持を確認。WRQ-20261019-CLAUDE-JOINT-INIT OPEN、REA-DEATH PARTIAL、死亡観測準備OPEN維持。固定handoff同checkpoint参照。

## WORK-LIVE-SUPPORT-CANDIDATES-20261019
Work回復統合 / PARTIAL。実Unitの候補順/除外/現在距離を既存属性選択へ接続、127PASS＋新規専用1PASS（別method）。owner選択/発動gate/post-core/GUIは未完。WRQ-20261019-CLAUDE-JOINT-INIT OPEN、REA-DEATH PARTIAL維持。固定handoff同checkpoint参照。

## WORK-SUPPORT-INITIAL-STATE-VERIFIED-20261019
Work / PARTIAL。状態ゲージBC..D4とheal_max D8は既存Unit生成→共有limitsに接続済みと検証。再実装不要。view/support55PASS、製品コード変更なし。残りowner候補/confusion/global gate/cooldown/post-core。JOINT-INIT OPEN/REA-DEATH PARTIAL維持。固定handoff末尾参照。

## WORK-SUPPORT-OWNER-SELECTION-20261019
Work / PARTIAL。実Unit混乱→owner選択→共有RNG→部隊所属/距離候補生成を接続、関連123PASS。owner/globalは明示binding、cooldown/post-core/GUI未接続。JOINT-INIT OPEN/REA-DEATH PARTIAL維持。固定handoff末尾参照。

## WORK-SHARED-SKILL-COOLDOWN-20261019
Work / PARTIAL。共有keyed cooldownのpost登録・deferred発動gate・AI-due減算を接続、関連124PASS。EXE build/help成功。WRQ-20261013-B-SKILL参照: gun_delay raw aliasは210/214へのproducer証明ではなくmapping VERIFY、拒否624DD0/624DE4の新取得依頼なし。owner/global/caller終了/GUI未完。JOINT-INIT OPEN/REA-DEATH PARTIAL維持。固定handoff末尾参照。

## WORK-SUPPORT-CONTEXT-BINDING-20261019
Work / PARTIAL。実DAT context→召喚対象gate/混乱確率→支援候補をGUI初期化から接続、125PASS。Skill210/214入力の旧拒否624DD0/624DE4は限定再審査のユーザー回答待ち・未再試行（各NULまで最大32bytes、同Local、SHA確認、read-only）。owner/caller終了/GUI発動未完。JOINT-INIT OPEN/REA-DEATH PARTIAL維持。固定handoff末尾参照。

## WORK-HEAL-CONTINUATION-HOLD-20261019
Work / PARTIAL。回復core未完後のACTIVE誤復帰を修正、trace保持/再適用と終了skipを防止。旧heal→finish試験は後段未完を飛ばしていたため完成証拠から除外。関連186PASS、EXE build/help/Windows3Unit・7ticks成功、GUI攻撃/回復未実施。次=post-core再開。624DD0/624DE4限定再審査は回答待ち・未再試行。JOINT-INIT OPEN/REA-DEATH PARTIAL維持。

## WORK-HEAL-CALLER-ROUTE-AUDIT-20261019
Work / PARTIAL。回復stageのcallerを訂正: Session.healはSimpleUnit545CC0/547AF0系、normal Unit57F570/54E0B0後段とは別。metadata/continuationへ反映、198PASS。共通効果計算は再利用し、次は通常Unit経路を優先。Skill268 property名/後段未確定。624DD0/624DE4限定再審査は回答待ち・未再試行。JOINT-INIT OPEN/REA-DEATH PARTIAL維持。

## WORK-SUPPORT-LIVE-LINK-20261019
Work / PARTIAL。支援候補のruntime1D0更新追従を修正、125PASS。通常Unitのearly/late MP gateは1F8/8C依存でSimpleUnitと区別。571B70の初期クリア後writerがあるため1F8をゼロ仮定しない。次=normal Unit操作状態/技能入力binding。624DD0/624DE4限定再審査回答待ち・未再試行、JOINT-INIT OPEN/REA-DEATH PARTIAL維持。

## WORK-CONTROL-INIT-EVIDENCE-20261019
通常勢力戦の操作初期化bindingをP0継続。保存nativeの本人/leader def74・troop20・power1D→1F8、@mode_auto→1F9を照合。btl_semiauto一律適用禁止、放浪枝分離。固定handoff同checkpoint参照。資料照合のみで遊べる範囲/ゲート不変。

## WORK-FACTION-CONTROL-BINDING-20261019
勢力戦のStrategyWorld→Unit操作flags→normal回復MP gate bridgeを実装、専用2/関連127PASS。部隊control/autonomousは明示入力、現GUI初期化から未呼出。次は戦闘初期化による共有world・部隊情報供給。完成ゲート不変。固定handoff同checkpoint参照。

## WORK-DEPLOYMENT-CONTROL-STARTUP-20261019
明示配置の操作設定をGUI初期化へ接続、128PASS、EXE build/help/Windows画面成功。source=DEPLOYMENT_DECLARED、campaign_initialized=false。原作DAT勢力実在は検証、部隊編成/自律flagは宣言条件。G5/G7/G8未達、次=実Skill発動/効果後段。

## WORK-SKILL-ADMISSION-DEPENDENCY-20261019
normal Skill/DAT admissionのP0依存を確認。Skill210/214項目名の限定再審査はユーザー承認待ち。未確定値をゼロで通過させない。SimpleUnit回復をnormal代用しない。コード/完成ゲート変更なし、固定handoff同checkpoint参照。

## WORK-TUTORIAL-FIELD-IMAGES-20261019
原作tutorial.mapのサブフォルダfield画像aliasを読み込むよう修正、622マスの画像参照を解決。37PASS、新EXE起動/描画確認。地形高さ/階段/AI/戦闘完走は別未完。固定handoff同checkpoint参照。

## WORK-LIVE-PLAYER-MOVEMENT-CONTROL-20261019
G2 PARTIAL: live操作権限→移動/停止へ接続、左右固定判定撤去。実DATと新EXEでside1操作Unitの移動到着、専用9/関連109PASS。攻撃命令と原作移動/衝突の完全比較は未達。G1/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。固定handoff参照。

## WORK-SWORD-C4-ADMISSION-20261019
G3 PARTIAL: cost!=0時のlive C4状態gateをroot発動へ追加、拒否時副作用なし、112PASS。GUI技能発動/一戦完走の達成ではない。全ゲート据置。EXEは前turn版、今回変更未build。

## WORK-LETHAL-INTEGRATION-PLAN-20261019
G5未達の主依存を更新: 致死前段5785A3→588470共有戦略状態→既存disable→5789F2後event/return→damage tail→outcome。既存解除単体の再実装を避ける。Gates据置、前turn修正EXE再build済み、今回ゲーム動作の新規達成なし。

## WORK-LETHAL-DISPLAY-MERIT-20261019
致死計算から数字表示要求保持、共有指揮者def/部隊先頭Unitへの功績加算resumeを接続。283PASS・build/help成功。新host表示要求はGUI未接続。G5未達、次57860C dead/break→corpse→588470→disable/event→damage tail/勝敗。Gates/Golden/MATCH据置。

## WORK-LETHAL-DAT-PRESENTATION-20261019
死亡時DAT出力要求の接続がPARTIAL。実DAT kmrと合成継承gateを285関連試験で確認、画面/音声再生は未確認。G5未達。次578929 lost_corpse/登録カウンタ/scream→588470。原作Golden0/MATCH0。

## WORK-CORPSE-EXISTING-CONTRACT-20261019
既存REA契約を再利用する順序へ更新。corpse生成→次eligible tick→期限と遅延→通知→count減算→登録解除。死亡音はscream override/fallbackと4BA020 gateを持ち、通常skill音ランダムAPIと別。今回製品進捗なし。G5未達継続。


## WORK-CORPSE-LIFETIME-GUN-DELAY-BINDING-20261019
- 前turnはlive PID43820の最終結果295PASSを回収したためPROGRESS。今回開始/終了時固定handoff/WRQとGit dirty確認。製品変更はWork所有battle_runtime_actions.py/native_battle_session.py/battle_runtime_skills.py/battle_runtime.pyおよび対応testのみ。他owner source・原本・禁止Git操作なし。
- CorpseSequenceを既存RuntimeActions更新へ接続。elapsed/expired signed32更新、threshold/delay比較、通知成功後のみ登録除去。lost_corpse=0はabs幅+8、非0は明示的なresolved lifetime必須。animate/notify callback必須、通知例外はfault保持し再実行しない。生成中の同passでは更新しない。corpse_countはnewhost登録数であり旧engineメモリbindingとは別。実描画/fade/通知UIのconsumerは未接続。
- BattleSession.begin_resolved_lethal_corpse: 実DAT lost_corpseと共有Unit矩形を入力し空breakの578929から一度だけ登録、pending contextを保持し4E081F LEThAL_CORPSE_SOUND_VERIFYで停止。588470/afterdeath/disable/EXPへ飛ばさない。音声・戦略・死亡handler returnは未完、Session VERIFY中の通常tickは引き続き停止。旧4E0610全機能完成ではない。
- Corpse新規4method（actions3/session1）。RED確認後actions+timeline39PASS。関連6module295PASS/FAIL0/ERROR0 PID43820 exit0、43.818秒。実DAT kachop/kmr由来+合成致死runtime/表示callback。STATIC/SYNTHETIC/DAT_DERIVED、原作観測なし。
- ユーザーが質問call_b9fbe2be8f2546b8acf94ca26bafd392へ『全て許可します』と回答。質問対象の2文字列だけに限定し同Desktop Commander Localで再審査・読取成功(PID30664)。既存rea_lab/targets/hakushin067_Vahren.exe SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187を照合。0x624DD0(file0x2241D0)と0x624DE4(file0x2241E4)はいずれもhex67756e5f64656c617900='gun_delay'+NUL、各10bytes。各最大32bytes/NUL終端の承認範囲内、実行/書換なし。他拒否範囲の包括承認と解釈せず再試行0。今回REA provider起動は行わず、明示承認された同Local経路のみ。
- 保存B T011_STRUCTURE_DISPATCH_PROBE.txt L14042..14083 (59C1BA..59C253)と照合: 同一gun_delayからScriptData+20→Skill210、+4文字列→Skill214。従来のraw aliasとcompiled slotの対応不足をここで解消。506AD0の保存疑似C/既存peer _own_value/_list_itemを利用、他担当parserは変更しない。
- skill_cooldown_inputsで同kind継承/明示空/欠落を読み、ASCII共有キーとsigned待機値を供給。複数item/不正倍率/数値だけ/@*N/非ASCII encoding等の非対応形はVERIFY。dat_skill_cooldown_gateは既存deferred live gateへ接続。sword postのcooldown引数とwriter keyを省略するとDATから取得し、明示Noneは従来どおり拒否。20C waitはまだ明示入力。skill所有/通常発動全条件はこのAPI単体で認可しない。
- 実DAT b_heal/cook_heal/dango1がb_heal*3を共有し、同Unitのpostwriter→deferred gate→4回のAI-due decrement→解除、別Unit非共有を検証。postwriter部分はstage fixtureであり実heal全行動ではない。実sw_karate0のmissing gun_delay→0もpostへ接続。nativeタイマーのrender-frame自動減算は行わない。
- gun_delay新規2method。RED1FAIL/1ERROR PID23340→初回回帰2ERROR(接続先取り違え、None扱い)→修復途中SyntaxErrorを修復→122PASS PID29096。その後writer実DATキー経路/非対応形検出を強化し最終122PASS/FAIL0/ERROR0 PID32808 exit0、64.751秒。AST8正常。295と122は重複あり、合算しない。全体suite未実施、既知sourcebook2FAIL未解消。
- Corpse反映EXE build/help成功PID35320(44.06秒)の後、gun_delayも含む最終build/help成功PID28680(55.84秒)。EXE SHA cb5a1833d74ccfa01289fd4641622cdcdaa74798688fe18e03e57fba293d7c79。8source/test SHA前後一致。_work/gun_delay_binding_build.log/_help.txt/_build_verification.json保存。今回GUI実行/原作観測なし、ビルド成功を戦闘完走としない。
- G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。操作可能な戦闘完走範囲の追加達成なし。実行入力と死亡継続の接続範囲を拡張した段階。
- 次P0: gun_delay実入力を通常支援/攻撃admissionの既存呼出へ渡し、20C wait/外側action帰還の保存契約を照合。別主線は4E081F scream選択/発行→既存588470と共有戦略world→afterdeath/disable/event→damage return/EXP/勝敗。JOINT-INIT OPEN、REA-DEATH PARTIAL。非0 corpse FPU/演出・終了通知/UI・共同戦略state等VERIFY。追加ユーザー操作/high要求なし。

## WORK-NORMAL-SUPPORT-DAT-GATE-20261019
WRQ-20261013-B-SKILL / Work / P0 / PARTIAL。実DAT gun_delay→通常Unit57F570入口→共有待機値判定をTask継続経路へ接続。正値は57E5F0 recovery、欠落/非正は57F685候補生成前で停止。関連236PASS、新EXE build/help成功。未完=GUI RuntimeRoster共有辞書の自動供給、通常selection/core後段/20C wait/outer帰還。固定handoff同checkpoint参照。REA-DEATH PARTIAL/JOINT-INIT OPEN、旧拒否維持、2文字列取得サブ課題CLOSED。追加ユーザー操作・high依頼なし。


## WORK-EXTERNAL-BATTLE-POLICY-20261019 — 工程差替え
旧WBSは再利用資産/履歴として保持。直近P0は接続往復実証、その後別EXEで一戦完走、必須拡張2件、原作物語復帰/代表シナリオ検証。原作戦略の全面再実装を必須工程から外す。接続実証未達のため新方式の実現性を検証済みとはしない。

次工程は雇用UIの原作接続実証。戦闘関連の既存WBSは資産/未完工程として保持。今回DLL基盤だけでゲーム機能ゲートを達成扱いしない。

## WORK-HIRE-UI-NATIVE-ROW-CONTRACT-20261019
WRQ-20261019-WORK-HIRE-UI | Work | P0 | PARTIAL。STATICで4D78F0押下gate(+1480)、4D79C0選択index/ID対応、4D4A50の全員一覧時flag=0・count最大100を確認。単一flagで全員一覧のhireableを代用不可。停止VA=516450/517FA0雇用者候補modeと586080 ABI。参照=固定handoff同checkpoint。DLL変更/実機接続なし。次=保存証拠で全員一覧と候補列挙契約を確定。

## WORK-HIRE-UI-ACTUAL-HOVER-20261019
WRQ-20261019-WORK-HIRE-UI | Work | P0 | PARTIAL。ACTUAL read-only2状態取得。全17人→KMR選択後も17人、kusomusume先頭/唯一press_gate1。選択人材の候補優先は原作既存。未完=全員一覧での所属人材候補の合成/左chip、左固定681468 count0と表示5人の不一致解消。参照=固定handoff同checkpointと_work/hire_ui_live_snapshot_01.json/_02_kmr.json。DLL原作接続なし。

## WORK-HIRE-SORT-ONLY-20261019
ユーザー最新訂正: キャラチップ表示は別機能への要望であり、今回の対象から除外。直近P0は右側全員一覧の雇用可能者優先と原順復帰のみ。KMR等選択時の原作優先表示を再利用。左chip描画/資産解決は追わない。左所属人材の取得が全員一覧の可否判定に必要な範囲だけは継続。WRQ-20261019-WORK-HIRE-UI PARTIAL（scope=sort-only）。以前のchipを含む次P0をこの訂正で上書き。

## WORK-HIRE-SORT-ABI-BRIDGE-20261019
WRQ-20261019-WORK-HIRE-UI | Work | P0 | PARTIAL。586080 nativeABI(ESI雇用者/ECX対象/AL返却)確定、DLL専用bridge追加、x86試験32PASS。参照=固定handoff同checkpoint/_work/hire_ui_586080_abi_static.json。未完=所属人材取得/後段可否/全員一覧sort/UI接続。原作呼出/注入未実施。チップ除外維持。

## WORK-HIRE-SORT-EXISTING-RULES-20261019
WRQ-20261019-WORK-HIRE-UI | Work | P0 | PARTIAL。既存Claude can_lead_586080/can_join_586ab0とfindings §30を再利用。現DAT591件friend_ex/num/append字句0hit、RNG実測は未実施。参照=固定handoff同checkpoint/_work/hire_ui_friend_fields_scan.json。停止=所属人材列挙/GUIphase/後段条件/UI接続、chip除外。

## WORK-HIRE-SORT-ROSTER-ADAPTER-20261019
WRQ-20261019-WORK-HIRE-UI | Work | P0 | PARTIAL。ACTUALで固定681468の所属5人取得を確認、別instance仮説不要。DLL HkReadNativeEmployers追加、x86試験40PASS。参照=固定handoff同checkpoint/roster observation/verification JSON。残=UIthread接続/全候補可否/全員一覧sortと描画・選択整合。chip対象外。

## WORK-HIRE-SORT-UI-THREAD-PROBE-20261020
WRQ-20261019-WORK-HIRE-UI / Work / P0 / PARTIAL。DLL UIthread実機読取成功（5所属/17候補）、43checks+self/timeout成功、解除確認。並替え未接続。次=全員一覧の資金/領域込み判定・描画/選択整合。詳細は固定handoff同checkpoint、_work/hire_ui_dll_verification.json。chip対象外。Golden0/MATCH0。

## WORK-HIRE-SORT-ROW-AND-BITMAP-20261020
WRQ-20261019-WORK-HIRE-UI / Work / P0 / PARTIAL。ユーザー確定=原作586080雇用関係を全所属へOR、資金/領地は原作のまま。行metadata/画像copy permutation実装、72checks、実機HDC300x5632x32と所属5/候補17確認。並替え表示未接続。次=辞書read-only lookup→native relation評価→可逆commit。固定handoff同checkpoint参照。


## WORK-HIRE-LINK-SORT-READBACK-20261020

所属全員の原作586080雇用リンクをORする優先表示。資金/領地は今回の優先条件から除外。chip対象外。辞書read-only lookup・native predicate・行metadata/bitmap同一順序更新を接続。93合成checks成功。実機で所属5/候補17、78calls、優先6人。nonce44847500で即時4配列一致、44848696で後続読取一致。画面を開き直すと原順へ戻る。nonce44973156再適用後も表示未更新だったが、nonce45193105でデータ保持を確認。ユーザーがスクロールするとKBSトリオ先頭になったと確認し、再描画不足を特定。原作EXE/save未変更。Golden0/MATCH0。

## WORK-HIRE-NATIVE-REDRAW-20261020

Work / WRQ-20261019-WORK-HIRE-UI / P0 / PARTIAL。原作453C20の提示処理を接続し、スクロール不要で優先表示に変わることをユーザーが実機確認。根拠: 保存Ghidra疑似CとSHA一致コピーの限定x86読取、4D77B6..4D77C2 callerがECX=window/EBX=0/stack zero3引数、453C20 callee ret12。HkCallNativeHireRedraw追加。TDD: PID31360欠落exportでFAIL→PID25324/13940で97checks PASS。最初の実機試験nonce45864049はhover1000（リセット上）で無変更拒否。外へ移動後nonce45978065でsort0/immediate_rows_verified=true/redraw0、UIhook解除、ユーザー「すぐKBSトリオが先頭になった」。変更=src/hire_ui_extension.c/.h,src/hire_ui_observation.c,tests/hire_ui_dll_test.c。現行DLLビルド成功。元順復帰は原作リセットで確認済み。ただし自動再適用と優先/元順切替は未実装、表示とhover対象の全行照合/雇用操作試験は未実施。次=全員表示のライフサイクル判定と再適用、個別雇用者表示を維持、元順復帰。REAは接続ありだがGhidra providerはJAVA_HOME未設定/java.exe絶対path必須エラーでruntime_unavailable。設定変更せず記録し、既存資料と許可されたLocal解析を使用。全体Python未実施、旧2FAIL未解消。原作EXE/save未変更、Git変更操作なし。他担当ファイル変更なし。Golden0/MATCH0。


## WORK-V4-FOUR-GROUPS-20261021

ユーザーからV4引継ぎを受領し、data/recruit_sort_v4を改修正本として確認。新要件は安定順: 0雇用可能、1雇用リンクあり領地不足、2リンク/領地あり資金不足、3リンクなし。複数雇用者では完全成立を優先し、なければ領地成立の資金不足を採用、誰も領地成立しなければ領地不足。表示グループの順番と複数雇用者の成立度を混同しない。rect_sort_core.hに4分類/雇用者間集約/安定順列を追加。関連条件がunknownなら拒否。新規5組の条件assertと既存10000矩形ケース成功。native relation模擬17人/5雇用者/61calls成功。4段階分類のネイティブ領地/費用入力は未接続: 製品DLLは依然relation-onlyであり4段階完成とは扱わない。原作UI保存4D4A50 L1066-1084には5AC880等の領域集合と資金/価格比較がある。価格はL1012-1046の雇用者依存補正を含むため、全員表示の価格をそのまま各雇用者の価格と推測しない。今後native ABIを確認して入力アダプターへ接続。
V4の再描画を修正: 通常thiscallだけでは不足する453C20のEBX=0を、Workで実測済みのbridgeと同形式で設定。対象window最小確認サイズを1554→1558へ修正。build成功、dist DLL SHA ac840dc8d20243e0d941ba65b30987e72e2f0fc148797f25d19cb42e48e84b7f。ゲームフォルダの配置DLLは今回は未更新、原本/セーブ/他担当は未変更。最新保存V4実機ログはrenderer初回→priority skipped reason=-8 n=17。ユーザーは並び変化ありと報告しており、ログと同一回の観測とは未確認。-8はHkReadNativeEmployers拒否であり、ロード時フック成功と分離して調査する。V4全完成/実雇用/クリック整合は未検証。Work旧105checks版panel/restoreソースはdev_labに残るが実機パネル起動未実施、V4へ混在させない。次P0=roster mode/count/取得時点を診断、原作領地・雇用者別価格/資金の意味/ABI確認、4段階入力接続、V4描画・hover実機試験。上限100件は継続VERIFY。Golden0/MATCH0。
