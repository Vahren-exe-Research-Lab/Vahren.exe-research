# 迫真戦記再開発｜Work→研究チャット共有依頼キュー

## 現行目標 — WORK-GOAL-SELECTOR-LOADER-20261025（最優先）

ユーザー明示変更：「目標を現在の教育やアイテム使用を分かりやすくする作業と、プラグインローダーの作業に定めてください。つまるところ、今やってる作業の完成を目標にして」。本節が過去の新Windowsエンジン全体・戦闘再現・別戦闘EXEの目標より優先する。過去成果は保存し、当面の完成条件に全戦闘/ストーリー互換を含めない。

**今回の目標：迫真戦記ver0.67で、教育・アイテム等のユニット選択をゲーム内で分かりやすく操作できる機能と、それを継続的に追加・更新できる共通プラグインローダーを、実用・配布可能な状態まで完成させる。**

### A. ユニット選択画面の完成
- 教育の講師/生徒、アイテム使用対象、同型の自勢力ユニット選択を行うランダムイベントに対応する。勢力全体/領地内の元の候補条件を守る。
- ゲーム内にチップ・名前・能力値・所在地を表示し、名前検索、列見出しの昇降順、元の順への復帰を使えるようにする。選択行と原作右上詳細を一致させる。
- 教育補正順と「失敗・通常・成功・大成功」の予想を、実際の教育処理の根拠と一致させる。技能・連続講師等の補正を含め、DAT更新の未対応を検出し、未確認値を確定表示しない。HP増加量の予測表示は不要。
- 講師→生徒→実行、アイテム対象→使用を正しいユニットへ一度だけ反映する。候補の更新/画面遷移/再表示時の古い選択を拒否し、検索・並替えでIDを取り違えない。
- 右クリックで一段戻る/閉じる。強制選択イベントではイベントを飛ばさず、必要なら補助UIだけ閉じて原作の必須選択へ戻す。非表示のままゲーム操作を奪う不具合をなくす。
- 代表的な教育/アイテム/強制選択イベントを実機確認し、開き直し・取消・連続使用・画面状態変化を検証。試験専用確認UIのままを完成扱いしない。

### B. 共通プラグインローダーの完成
- 原作Vahren.exeを変更せず起動できる32bitローダー/Core/機能別DLLを完成させる。dinput8方式の実ロード、入力、通常起動/終了を確認する。
- plugins/内の明示的に許可されたDLLを設定に従って読込み、ON/OFF・順序・依存・API版照合・エラーログを管理する。未知DLLを無条件実行しない。
- フックの重複所有、途中失敗、残存callback/patchのあるDLL解放を適切に扱う。ゲーム再起動で機能DLLのみを交換できる。hot reloadは対象外。
- 現在の雇用並替えと新しいユニット選択を基盤上で実用確認する。雇用プラグインは基盤の既存機能との互換確認対象であり、新しい別機能へ範囲を広げない。
- 既依頼のBattleObserver再利用/統合は現物未発見の依存事項として明記する。所在未確認を統合済みとしない。これを理由に戦闘エンジン再実装へ進まない。
- ビルド可能なソース、配置/更新/無効化/原作起動へ戻す手順、配布物と検証結果を揃える。実機で機能追加・無効化・差替え・失敗時挙動を確認し、ユーザーの最終確認へ渡す。

### 優先順位・完了判定
1. Aの既存実装と未完箇所を照合し、実行まで通る選択UIを最優先で完成へ進める。
2. BはAおよび既存雇用機能を実際に載せて運用するのに必要な範囲を完成させる。抽象基盤や合成試験の追加を自己目的化しない。
3. 両方を実機で通し、配布物・手順・既知制限を揃えてユーザー確認。試験件数やbuild成功だけでは完了としない。
当面の対象外：新エンジン全体の再現、戦闘乗っ取り、地形/召喚EXP拡張、他MOD全面対応、新しい無関係な機能。既存研究は消さず保留する。
原作EXE/DAT/save保護、他担当の所有権、Git操作禁止、安全拒否の迂回禁止は継続。原作操作は最新の「利用者が確認する」方針を維持する。
アプリ内自動継続goalは旧本文が残っている（現ツールに本文編集機能なし）。旧目標を達成扱いにして置換しない。自動継続に旧本文が現れても、このユーザー明示の新目標を作業方針とする。






## 現在の優先方針 — WORK-HIRE-UI-DLL-PROTOTYPE-20261019


最新ユーザー指示は「原作EXEを最大限利用し、DATで可能な機能はDAT、必要箇所だけDLL等で拡張」。戦闘別EXEは実証後に選ぶ選択肢であり、必須の直近主線ではない。直前WORK-EXTERNAL-BATTLE-POLICYの別EXE最優先記述より本節を優先。


最初の実装対象: save1ロード→人材雇用。左は所属人材、hoverで右の雇用対象を絞る（ユーザー確認）。右は雇用可能優先/原作順切替、同区分内元順保持。左は名前横に静止チップ。既存hover/雇用条件/費用/対象対応を保つ。今回DLL作成・ビルドまで明示依頼あり。戦略全再実装や全EXE逆コンパイルは行わず、既存研究と部品を再利用する。





## 現在の依頼運用 — WORK-EXTERNAL-BATTLE-POLICY-20261019


Work / P0 / OPEN: 原作→別戦闘EXE→原作の開始/結果受渡し実証を最優先。参照=固定handoff冒頭の新方針。停止VAは未選定、開始/終了の既存成果を照合して決める。未完=入出力契約・戦闘中イベント・安全な復帰・異常終了時の扱い。既存依頼は履歴/状態を保持し、方針転換だけでCLOSEDにしない。広範な全EXE解析/戦略再実装依頼は優先解除。召喚EXP還元・動的地形は必須拡張。今回は他担当への送信/起動なし。下記旧運用と競合する場合は本節を優先。





## 現在の依頼運用 — WORK-PLAYABLE-ENGINE-POLICY-20261013


広範囲の内部復元依頼は優先解除し既存成果の統合を先行する。他チャット/automationを実際に停止・送信した記録ではない。旧P0 VA一覧は履歴で新規一括解析指示にしない。PARTIAL/OPEN/BLOCKEDは維持し、方針変更でCLOSEDにしない。


次のWork主線: 意味ベースBattleRuntime→DAT/Unit/数式/移動/技能→live素材表示→一戦完走。57FC19内部free/cookieを主線から外す。


追加依頼は「止まっているゲーム機能・不足証拠・接続先・終了条件」を必須にする。B=技能/AI/間隔、D=弾/アニメ/時間、C=出撃/イベント、Claude=戦略IF、E=比較、REA/A=結果に効く不足だけ。現時点で新しい解析依頼は出さない。拒否代理取得は禁止。





仕様: WORK-REQUEST-QUEUE-V1 / 作成日: 2026-10-13 / 宛先: A・B・C・D・E・REA・Claude Code


管理者: Workのみ。初版はユーザー依頼に基づき通常チャットがbootstrapした。以降、Workが本ファイルを更新する。


目的: Workが利用制限・中断中でも解析依頼と停止点を保持し、各担当が実行開始時に自動で読む。新フォルダは作らない。





## 運用契約（最初に読む）


1. 各担当は毎run開始時にこのファイルと自身の最新handoff、`../../MASTER_LEDGER.md`、`../../evidence/ANALYSIS_LANES_PROTOCOL.md`、担当の予約・既存証拠を照合する。本ファイルは依頼であり、原作仕様の一次証拠でもMASTERの代用品でもない。


2. **本ファイルの書込・依頼状態更新はWork単独**。A〜E、REA、Claudeはread-only。成果は自身が所有する既存の正式資料とHANDOFFへ依頼IDを付して保存・readbackする。保存済みREADY/VERIFY/NOT RUN、検証数、原作実機0件を区別する。


3. Workは再開時に担当HANDOFFの依頼ID・成果ID・最新日時を読取り、依頼を OPEN/PARTIAL/READY-FOR-INTEGRATION/BLOCKED/CLOSED へ更新する。Work自身のコード・試験・EXEと照合せずにCLOSEDにしない。新ID乱発や同じ関数の重複調査を避ける。


4. 進捗の引継ぎは Work正本 `CHATGPT_CURRENT_HANDOFF.md` と製品ログ `../reports/CHATGPT_HEAL_MUTATION_20261012.log` を併せて参照する。598→916の未反映履歴はWorkが回収済み。旧内部復元の広域履歴は2026-10-13の1109PASS checkpoint（特殊技能登録・phase0更新・後処理帰還→57FC19、新EXE2ケース自己照合）。履歴とは違う時点・検証範囲。実EXE Gameplay Golden=0、strict MATCH=0。既知sourcebook全体2FAILの解消は未証明。


5. 読取不能ならBLOCKED/CONNECTIONとして担当HANDOFFまたは応答に、対象・最終成功・次回再開を残す。読めたと偽らず、Remoteや他経路に無断切替しない。安全拒否は別tool/shell/pathによって迂回しない。許可範囲の独立調査は続行してよい。


6. 原本ゲーム、原作ZIP/EXE/DAT/MAP/saveは完全read-only。MASTERはE単独、製品コードと本依頼ファイルはWork単独、各レーンの担当境界を守る。Git stage/commit/push/reset等は別途明示許可なしに実施しない。


7. タスクの“自動読取”は各チャットの開始・定期実行時にそのチャットの指示で行う。ファイル変更自体で他チャットを起動するpush通知はない。Localアクセス不能時はその回に読めない。


8. Wikiの976ページ分の探索・要約は通常チャット担当。Workの利用枠をWeb調査だけに使わない。





## P0｜依頼一覧





### WRQ-20261013-B-SKILL｜研究B｜P0｜PARTIAL／限定HP・EXP接続済／追加効果・帰還未完


- 目的: 通常AIが技能発動まで正常帰還する契約。57EB40(kind2)、57F570(kind3)、57F190(kind4)とUnit virtual+7C/+80、57FFD0/57FC90等を、入口→対象→効果→MP/cooldown→returnで閉じる。


- 既存のB-20261013-0151-01/02/03、B-20261013-0323-01、B-20261013-0718-01/02と `../../data/T013_WORK_SKILL_HANDLERS_BOUNDARY_20261013.md`、B native/T012・T013を先読し、確定済み入口/RET/405440/owner検索を再解析しない。


- 尚VERIFY: 子callee、発射/召喚の実効果・RNG総順序、virtual実体、Unit単位のreturn、未保存/安全拒否追加検査。未知はREADYに偽装しない。


- 納品: 担当T012/T013正本＋LANE_B_HANDOFFに新規差分ID、Workが接続できる次VA、入力/型/offset、AL・副作用・RNG、未完calleeと最小試験。





### WRQ-20261013-REA-DEATH｜REA（既存証拠）/Work（統合）｜P0｜PARTIAL


- 目的: 実DATの致死hitからゲーム結果・演出・戦略状態・勝敗までを接続。2026-10-19更新: 旧embedded window/二度目選択/2Troop/親returnの限定枝はWork接続済み。既存部品を最初から解析し直さない。


- 現在の停止: 5785A3致死前段、5789F0 disable呼出の成立条件、5789F2後のevent/return。575A60単体完了を致死hit完了として使わない。


- Work実装順: ①4E1950/功績/death-break/corpse/afterdeathのゲーム上の意味と必要入力を保存証拠から確定 ②Claude unit_defeated_588470をshared world/def/RNGへ一回だけ接続（個人資金・payer不明を0で代用せず、途中Gap再実行によるEXP二重処理を防ぐ）③既存disable限定経路再利用 ④1862Cを解除後再読してevent/skip→handler return ⑤damage tail/EXP→side判定→戦闘終了。


- 原作内部コンテナ/Window allocatorの一致は不要。新host表示・登録へ置換してよいが、death演出・功績・資金・EXP・event・RNGは保持する。GUIの操作権限用private projectionを完全な戦略worldとして使わない。


- 受入条件: 実DAT由来の致死攻撃を入口に、HP・功績・def1B0/1B1・部隊・Task・EXP・資金・event・RNG・勝敗への反映順と一回性を確認。途中で未解決ならVERIFYを保持し、無条件kill/勝利や手動disableで代用しない。


- 参照: ../../rea_lab/decomp_task/SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md ND-LETHAL/DEATH21-22、REA_20261015_1640_LETHAL_POST_DISABLE_BRANCH.md、REA_20261019_0335_DEATH_TROOP_SEMANTIC_RESUME_DRIFT_QC.md、既存native_battle_session/outcome、Claude peer_script01_strategy_world.unit_defeated_588470（read-only）。


- 状態: 既存解除契約READY-FOR-INTEGRATION（限定枝は接続済み）、致死前後全体PARTIAL。死亡観測準備OPEN、現在ユーザー操作不要。REA QUEUE/PROGRESS EPERM・旧拒否は別BLOCKED、迂回/広範再取得は依頼しない。キューはWorkのみ編集。





### WRQ-20261013-A-HOST｜研究A｜P0｜PARTIAL／未完caller


- 目的: host周回、GameEvent Task、battle clock、pause/速度、描画、終了前段493630の順序を、Work接続済みA72/A73後の未知callに限定して閉じる。


- 対象候補: 49B280/520800/52BFF0/5656A0/49D5B0、roster実初期化callback順、enter/leave、同一frame内VM再開・raw outcome→493630直前。


- 既存 `../../exe/T010_BATTLE_FRAME_ORDER.md` と最新 `../../evidence/LANE_A_HANDOFF.md` を先読し、拒否済みA80/A81など担当資料にのみ残るNOT READYを勝手に統合しない。


- 納品: A所有T006/T010資料＋HANDOFFにcall順・時計カウンタの区別・中断PCと未確定点。原本実機Goldenは未観測。





### WRQ-20261013-C-BATTLES｜研究C｜P0｜PARTIAL／実出撃NOT READY


- 目的: 通常戦闘の同条件比較ができる原作の合法2〜3実例（C-NB01/02/03）。


- 既存 `../../data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md`、`../../evidence/T025_NORMAL_BATTLE_SAVED_ROSTERS_20261013.json`、原作sci1のspot/MAP/script、EのT018比較設計を再利用。


- 尚VERIFY: 実MAPの選択、参加3side、Unit/Troop階層、配置、開始操作列・勝敗。保存名簿数を出撃数と混同しない。原作EXE未実行の値はDESIGNED/NOT RUN。


- 納品: C所有T025/T016とLANE_C_HANDOFFに入力packet候補＋出所/hash/不足証拠。戦略APIはClaude所有、重複実装しない。





### WRQ-20261013-D-COMMAND｜研究D｜P0｜PARTIAL／GUI最終consumer未確定


- 目的: 原作「通常戦闘」の選択、移動、攻撃、手動技能、停止・速度・カメラ・隊列の操作から、座標変換、実callee、Unit/Troop/engine writerまでをtrace。


- 既存 `../../data/T015_UI_RENDER_INPUT_AUDIO.md`、A73 pause、T015既知入力、57C600/57C9B0を再取得しない。RTS/T030の経路を通常戦闘へ混ぜない。


- 納品: D所有T015とLANE_D_HANDOFFに操作1件ごとの最後の確認済みconsumer、未回収VA、ゲーム状態と表示専用stateの別、原作合法UI観測案。





## P1｜重要な継続依頼





### WRQ-20261013-B-NUMERIC｜研究B｜P1｜PARTIAL


- 技能の接続で必要となった不足だけを調査。514F10 owner共有scratch・support cacheの差、非平方5E3B70/5D1B80、毒5B6ED0、owner virtual+18/5767B0の差分。


- B0031/405440や既存callerは再解析しない。計算式のnative命令、FP環境仮定、実機未実測を別記。根拠不足ではVERIFY停止。成果はB所有へ保存。





### WRQ-20261013-E-GOLDEN｜研究E｜P1｜OPEN（比較設計済・実機未実施）


- MASTER checkpoint94=公式225 ID（当時）。各レーンHANDOFFで新READY/未保存/拒否を区別し、意味重複を除き、E所有MASTER/T018へ合法な分だけ統合。


- 代表通常戦闘 C-NB01/02/03 の原作vs新EXE同条件比較（開始条件、実MAP、Unit/Troop、frame、HP/MP、対象、死亡、勝敗、EXP/scene）をDESIGNED/NOT RUNのまま更新。合法観測がないならGolden/MATCHを増やさない。


- 旧E所有T018表境界・拒否済み統合をWork/他レーンが代行しない。





### WRQ-20261013-CLAUDE-BRIDGE｜Claude Code｜P1｜PARTIAL


- 現状§68.7のcontext/cache失敗時保護、§68.8の434EB0/5AC1A0範囲整合、§72のstrategy turn→battle dispatchは既に回答済み。再解析不要。


- 未完: Workから使える原作WarState/出陣選択/3side、戦略結果API引数、死亡/退却/EXP/LvUpの重複適用禁止、復帰scene/プレイヤーダイアログ再開の入力とreturn境界を固定。未確定MAP link順・pointer順はCOMPAT/VERIFYのまま。


- 納品: 既存 `PEER_SCRIPT01_FINDINGS_20261011.md`、自身所有source/testに依頼IDとIF型・責務・中断条件・差分試験。Workソースは触らない。





## Work再開時の優先事項


1. 実装先 `../src/hakushin_compat` と固定handoff末尾 WORK-CORE-HP-REFRESH-20261013-1023、製品ログ support_core_hp_refresh_broad/exe を照合。598→916回収と997/1004/1023実装は既済として再解析・再実装せず、551C6Aから継続する。


2. 担当別HANDOFFで上記依頼IDの回答を確認し、本キューだけをWorkが状態更新。既存B/REA/Aの部分契約で早期branchを実装できるなら依頼未完を理由に全体停止しない。


3. 通常技能実作用→通常致死・消去→自動勝敗→493630戦略API→strict戦闘GUI/場面復帰の順にゲート検証。試作GUIの便宜仕様をstrict coreへ混入させない。


4. 最終ログと固定handoffと本キューをセットで保存・readback。Work利用制限前・ネットワーク切断前でも途中checkpointを残す。








## Work受領・統合判定 checkpoint 2026-10-13（WORK-WRQ-RECONCILE-20261013-01）


- Workが開始時に本キュー全67行、固定handoff最新checkpoint、A/B/C/D HANDOFF、E MASTER cp120、REA DAMAGE_STATUS末尾DEATH59、Claude findings §74.7/§79をread-only照合。ユーザーが新F停止済み・Work引継ぎを明示。新F/Claudeの既存dirtyを保全し、製品の継続書込はWorkが引き継ぐ。Git HEAD=be45dc2d563dcc1885a3caf4e3c8af43f6b8619b、Git変更操作なし。


- 598→916は製品ログ9131～9343行の履歴。支援cache/候補/選択/発動、技能後段、部隊・描画解除、射撃・Rush、選択解除、window期限とpending保護を含む。最終 `window_guard_broad`=916/FAIL0/ERROR0を実ファイル確認。直前9341行の `broad_after_fix=NOT_RUN` は後続9343行で更新済み。E cp120の未実施記載は古い中間状態なので、Eは自身の次回更新時に末尾を再確認すること。WorkはE MASTERを書き換えない。


- 新Fはその後m_healの正規AI→単回MP減算→550980再利用→54E123のrecord writerを追加。固定handoff最終記載PC54E1CCより現sourceが先行し、effect_random/core_gate/core_chance/core_scratchも存在。これらは今回受領時点で検証中。履歴916と新F scoped587/後続17件を加算しない。現EXE SHA256=92c811d50298d2c1668b5fed2b2005fbebb273b0f4d8f531092b3783b2ac3d32、6ケースsource一致の保存JSONあり。ただし最新source全体に対応するEXEとは未確認。


- 原作Gameplay Golden0 / strict MATCH0、通常戦闘完走未達。原DAT＋明示runtime fixtureと原作実機を区別。既知sourcebook全体2FAILは未検証。





| 既存依頼ID | 担当・優先度 | 状態 | 受領済み差分／次の停止VAと未完了範囲 | 参照・次の担当動作 |


|---|---|---|---|---|


| WRQ-20261013-B-SKILL | B / P0 | PARTIAL | B1122/1126の54E0B0・550980は新Fが限定再利用枝へ接続。B1614の576F10 wrapperとB1356の4DFBB0はREADY-FOR-INTEGRATION（局所契約のみ）。主線551574以降と54E31C後の正常帰還、実HP更新・次Unitは未完。 | B HANDOFF、T013_SUPPORT_EFFECT_54E0B0_CONTRACT、T012_FLASH_DAMAGE_WRAPPER_576F10_CONTRACT、T012_HEAL_EFFECT_RECORD_4DFBB0_CONTRACT。B-MT-01..10を再採番せず利用。WorkはR/P/L訂正B1415を優先し、支援pool0xA8とUnit内0x264効果slotを混同しない。 |


| WRQ-20261013-REA-DEATH | REA / P0 | PARTIAL | DEATH52～59受領。UIの41F850→56BA80→virtual+C→401BE0正常return位置、+54の描画/空間両writerが追加。575AEF child、575C52 embedded解除、実vptr未確定と拒否範囲は継続。 | SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md DEATH59、DEATH41/46/50。26静的assert PASSは製品テストに加算しない。QUEUE/PROGRESS EPERMは独立BLOCKED。 |


| WRQ-20261013-A-HOST | A / P0 | PARTIAL | A1401-01/02/03はREADY-FOR-INTEGRATION（VM global frame限定）。自然終端count==PCは正常pop、count<PCのみ失敗という訂正を受領。通常戦闘host全体/493630前段は未完。 | A HANDOFF・T006_TARGET_DISPATCH、4339B1～433E03。A1458-01/02のowner保存拒否はNOT READYのまま採用しない。 |


| WRQ-20261013-C-BATTLES | C / P0 | PARTIAL | C-NB01/02/03実出撃G0/G1/G2はNOT READY。後続の商人・戦略script増分を合法通常戦闘packet完成と扱わない。 | C HANDOFF、T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT、保存roster。合法開始SAVE・MAP・3side・配置の不足をC/Claude境界で確定。 |


| WRQ-20261013-D-COMMAND | D / P0 | PARTIAL | D1633-02の4EE110 input再設定順はREADY-FOR-INTEGRATION（限定）。通常戦闘命令の最終consumerは未完、RTS T030は流用しない。 | D HANDOFF、T015_UI_RENDER_INPUT_AUDIO。focus flushとAcquire/中心再設定/キーclearを分離。 |


| WRQ-20261013-B-NUMERIC | B / P1 | PARTIAL | B1247の5D1BB6 alternate、B1417毒CRT差分あり。B-MT-05のstealth有限式は既Work一致・再実装不要。実FPU profileと非軸/非平方はVERIFY。 | B HANDOFFとT012_T013_B_RESEARCH_TASKBOARD B-MT-07。新F数値はASSUMEDとして検証、strict既定を無断変更しない。 |


| WRQ-20261013-E-GOLDEN | E / P1 | OPEN | cp120公式422、旧実機0件。未統合見出し101はREADY101件ではない。Work916の末尾訂正参照。 | MASTER cp120/T018。原作同条件観測がない限りGolden/MATCHを増やさない。 |


| WRQ-20261013-CLAUDE-BRIDGE | Claude / P1 | PARTIAL | §74.7公開API（出撃回答/確定/FrameGates/再開）はREADY-FOR-INTEGRATION（IF部分）。§79イベント橋追加。戦闘側が必要な終了receipt・scene cleanupをまだ生成しない。 | PEER_SCRIPT01_FINDINGS §74.6/74.7/79、peer_script01_*はread-only。未回答dialog/未適用battle_id/scene未復帰のまま戦略tickへ戻さない。 |





### 次のWork実行順・受領条件


1. 新Fの未記録source/testとfixtureを照合し局所試験。その後、回復coreの正規入口・実効果・正常returnを既存契約から延長。未完calleeのno-op禁止。


2. 依頼全体PARTIALと受領した局所READY-FOR-INTEGRATIONを区別する。CLOSEDは製品接続・関連検証・未完範囲なしを確認した依頼だけ（今回CLOSED追加0）。


3. 終了前は本キューを再読し、固定handoff/製品ログの最新状態と照合。過去の固定資料更新拒否は成功扱いしない。保存の再審査が必要なら同Local経路と対象を限定し、拒否payloadの別資料への代理転記をしない。


4. USER-DIRECTIVE-NO-ABANDON-20261013 をWork受領。拒否・未保存・競合はownerと正規再開条件を明記し、原本/Git/他ownerを変更しない。Wikiは通常チャット、Workは通常戦闘実行接続を優先。








### WRQ受領後の具体的な残依存（2026-10-13 Work・局所9PASS後）


- WRQ-20261013-B-SKILL / B-MT-06 / P0 / PARTIAL: Workは551574～55164CをSession/Taskへ接続した。m_healの現在停止は55159E→415530、戻先5515A3。add2全件は5515C4→4ACE30（ret5515C9）、単要素を含む抽選は55164C→415530（ret551651）。先行chanceとMP・RNGを再実行しない。次の担当は415530/4ACE30/402710の既存保存証拠と文字列28-byte vectorの確保/所有権/正常return契約を確認し、既知原作属性選択モデルを本体の実状態へ接続可能にする。0x415460の拒否とは別関数だが、その範囲を再試行しない。


- Work read-only確認: 保存Ghidra decomp_0041xxxx.c の415530はvector+4==+8で415AA0、出力要素をSSO初期化し402710コピー後end+=28。これはPSEUDOであり新native確定/正常全returnの証明ではない。現段階ではコピー/allocatorをskipしない。


- WRQ-20261013-B-NUMERIC / P1 / PARTIAL: 新Fの54E1CC drawと551490 chance・551511 scratchは今回局所試験31PASSで受領。FPU実測未確認は維持。非軸角度・非平方距離・CRT alternateを高思考で扱う場合も、まず保存済み根拠と入力を揃える。新しい解析依頼IDを増やさず既存B-MT-07へ集約。


- 広域回帰/ビルド後の最終件数は製品ログ `work_resume_newF_attribute_broad` / `work_resume_newF_attribute_exe` の確定結果で更新する。まだ進行中の処理をPASSと数えない。








### Work終了前照合 WORK-RESUME-20261013-997


- 確定結果: 新F受領局所31PASS、今回追加9PASS、20module広域997PASS/FAIL0/ERROR0（415秒、対象source/test5件の前後SHA一致）。新EXE build exit0、2ケースfresh source全JSON一致/期待exit3。原作Gameplay Golden0/strict MATCH0、全suite既知2FAIL未検証。件数は合算しない。


- 固定handoff冒頭と末尾WORK-RESUME-20261013-997、既存監査JSON、製品ログ、既存WBSを現時点の実測に更新。旧598以降の未反映履歴はログ9131～9343を参照して回収した。過去拒否された610更新そのものの成功を主張しない。


- 最優先依頼はB-SKILLの55159E→415530正常returnと551653以後の実HP/状態/EXPへの接続。A/REA/Claude/Dの局所READYは上表どおり、依頼全体PARTIAL、CLOSED追加0。新F停止済みでWorkが通常戦闘コードを引継ぐ。


- 依頼閲覧先はこの既存ファイル。各担当へのチャット自動送信は未実施。次回開始時は各HANDOFFの新しい差分を再照合し、原作通常戦闘の実行範囲を優先して進める。





- [E cp121受領] 終了前再照合でE MASTER cp121（正式430=A102/B149/C97/D82、保存後監査済）を受領。B1614/1622、D1633-02等はE正式統合済みに更新されたが、Work製品接続済みとは別。依頼全体PARTIAL/原作Golden0/MATCH0を維持。








### Work終了前照合 WORK-ATTRIBUTE-COPY-20261013-1004


- 2026-10-13T17:44:53.439619+09:00: 新規7PASS、20module広域1004PASS/FAIL0/ERROR0、source/test5SHA不変。新EXE build0・copy成功/容量不足2ケースがfresh sourceと全JSON一致、期待exit3。原作Golden0/MATCH0、既知全体2FAIL未検証。固定handoff・既存監査/WBS/製品ログへ同期。


- WRQ-20261013-B-SKILL / B-MT06 / P0 / PARTIAL: Work接続済=415530→402710→短い非重複整列5B8730→4155FB→551653（空vector既確保SSO領域限定）。再解析不要。次停止551653、未完=5516B8局所copy/551738属性/550D80効果量/551924HP・状態→追加効果→54E31C/57FA9E正常帰還。context+D/E=1/1を+D1/E0で代用しない。B1614/B1356のflash576F10/4DFBB0契約を使い、未解決caller/flags/returnだけ確認する。容量不足415AA0、全add2列4ACE30、heap文字列は未接続、未知allocator成功を合成しない。参照=固定handoff同checkpoint、製品ログsupport_attribute_string_native/copy_crt_native/copy_aligned_tables、既存exe/T012_HEAL_ATTR_PROBE.txt。拒否済範囲への再試行は依頼しない。


- B-MT-AUDIT1717はINDEX ONLY/NOT READYで受領。non-grid4E7ED0/owner距離sentinel等は後続独立候補、既存索敵の全再解析は不要。WRQ-B-SKILL全体CLOSEDにしない。


- A1700 READYはDAT重複33件のcallback族対応。key-specific規則はVERIFY、A-HOST完了とは別。Claude findings付録Aのx87/ftolは未統合ドラフト。E cp121/430、REA DEATH59、C/D既受領状態を維持。依頼全体PARTIAL、E-GOLDEN OPEN、CLOSED追加0。各チャットへの自動送信は未実施。








### Work終了前照合 WORK-CORE-HP-REFRESH-20261013-1023


- 2026-10-13T18:22:51.511745+09:00: 新規19PASS、共通回復/新helper関連99PASS、広域1023PASS/FAIL0/ERROR0、6source/test SHA不変、新EXE2ケースfresh source全JSON一致。実DAT m_heal魔力542×200%=1084、kmr HP1→1085、MP20/RNG2/EXP0、Task未帰還。Golden0/MATCH0、全suite既知2FAIL未検証。


- WRQ-20261013-B-SKILL / B-MT06 / P0 / PARTIAL: Workは551653→属性index/550D80→551924→実HP writer→578EF0空entry正常return→551C6Aを接続済、同区間の再解析不要。最優先停止551C6A/callee551E50/ret551C6F。既存EXPコードへ同effect contextのC once flagとD/E=1/1を維持して接続、次にD8補正→551C7F E効果→54E31C/57FA9E/Unit return。B1614/B1356 flash契約を再利用。未完=Skill+74出所、special未指定getter、数値変換環境、m_heal flash5/577100/1E568、非空refresh4E02A0。元E=1を0へ初期化して旧D1/E0 adapterを通す代用品は禁止。


- B1734（4ACE30→479B50 wrapper/ret8）は局所READY-FOR-INTEGRATIONとして受領、全件vector/確保・cleanupはVERIFY。B1740（raw special→Skill4C）は受領、m_heal raw54～79にはspecialが無いためfixture既存4C=3はSYNTHETICのまま。A/T005のmissing/parent/off最終getter根拠を先に参照し、推測0やbool化しない。B1730-415530保存拒否はB所有BLOCKED/NOT READY維持。Work以前の成功保存と別操作であり、拒否範囲の再試行・代理転記を依頼しない。


- WRQ-C-BATTLES / P0 / PARTIAL: C1724-01/02のSpot scenario条件とsource追加link受領。原作合法G0/G1/G2・実MAP/3side/Unit/Troop未取得のため実戦packetREADYとはしない。WRQ-D-COMMAND / P0 / PARTIAL: D1732-01 window/input寸法crosswalk受領、通常コマンド最終consumerは未完。D1732-02 RTS、03 audioは別領域の限定READYとして参照、通常操作へ流用しない。


- E cp121/430、A1700、REA DEATH59、Claude付録A未統合draftを維持。依頼全体CLOSED追加0、E-GOLDEN OPEN。ユーザーへの追加操作要請は現時点なし。各研究チャットへの自動送信なし。固定handoff/監査/製品ログへ同checkpointを保存して再読する。








### Work開始時照合 2026-10-13 EXP接続


- 前1023 checkpointと6source/testのSHA一致・HEAD/所有権を確認。Workは551C6A→551E50 normal Unit→D8補正→E1追加効果を実装中。B1814は受領、非空1属性の厳密19名照合/未知名551D40はWork1023ですでに接続済。空vector551DEB/全add2は未接続のまま。B側の旧Work prefix-only記載と現実装を混同しない。Skill+74のraw producerとspecial未指定はVERIFY、入力無しを0にしない。








### Work終了前照合 WORK-AWARD-FLASH-20261013-1041


- 2026-10-13T19:12:32.462458+09:00: 新規18/関連114/広域1041PASS、FAIL0/ERROR0、新EXE build0・2ケース自己照合。HP1→1085、EXP0→10、D8 32402→31318、MP20/RNG2。Unit未帰還、Golden0/MATCH0。既知全体2FAIL未検証。


- WRQ-20261013-B-SKILL / B-MT06 / P0 / PARTIAL: 551C6A→551E50普通Unit帰還→D8→551C7F→DAT flash5→551CA1はWork接続済、再解析不要。停止551CA1/Skill6F0欠落。未完=6F0/6F4 producer、4DFBB0実効果、577100/551D40/551E4A/54E31C上位帰還、74出所/special未指定/数値環境。参照=固定handoff1041/製品log support_award_flash_*。6F0拒否literalの再取得は依頼しない。


- B1825/1831-01/1833-01/1850/1858/1901は局所READY-FOR-INTEGRATION。1841 D/Eと1831-02属性順は実装照合済。1856-02はSOURCE宣言のみ、@/learn/実MPはVERIFY。B-INDEX1850は新規READYに数えない。


- WRQ-C-BATTLES P0/PARTIAL: C1825/1847受領、SOURCE/合成のみで合法G0/G1/G2未達。WRQ-D-COMMAND P0/PARTIAL: D1834-01/02受領、VT/ヘルプ文言限定READY、操作consumer未達。A1700/Ecp121(430)維持、REA/Claude所有source非編集。


- 次依頼B: 保存証拠を起点に551D40候補loop/cleanup→551E4A→54E31Cのcaller状態・戻先を整理。74/missing specialはA/T005既存getter契約と照合、未知を明示。拒否済calleeの再試行/代理抽出は依頼しない。Workは既存577100の接続と通常死亡の独立経路を選ぶ。依頼全体PARTIAL、E-GOLDEN OPEN、CLOSED追加0。チャット自動送信なし。








### Work開始時照合 1041後 HP表示帰還


- 前turnはPROGRESS。1041 source/test SHA一致・HEAD/dirty確認。A1901 T005 caller、B1905 HP timer subtype VT、C1854固定event loopを受領。Workは既存refresh_hit_lifebarを再利用し551CF2→577100→551D03/551D40を接続、未知描画登録や4DFBB0は成功扱いしない。研究/Claudeソース非編集。








### Work終了前照合 WORK-CORE-RETURN-20261013-1056


- 2026-10-13T19:39:47.214845+09:00: 新規15/関連45/広域1056PASS、FAIL0/ERROR0、新EXE build0・2ケース自己照合。元通常flash5/8D0枝は551CA1依存維持。明示SYNTHETIC 8D1/count2/既存HPbar/stackを使うDAT試験ではcore551E4A→54E31Cに帰還、Unit未帰還。Golden0/MATCH0、全体既知2FAIL未検証。


- WRQ-20261013-B-SKILL / B-MT06 / P0 / PARTIAL: Work接続済=551CF2 HPpost→実577100限定return→1E568→551D40単一inlinecleanup/cookie→54E31C。同範囲再解析不要。最優先停止54E31C。未完=Skill30/34実DAT source・4B9F70 receiver/virtual24・268/global609268/4C3140→54E3E1/57FA9E/UnitRET。B1825/1831-01/1833-01は局所READY-FOR-INTEGRATIONとして利用。参照=固定handoff1056、製品log support_hp_post_return_*。


- B1918-99 scratch tail受領・単一最終属性を実装照合済。複数属性の二段fresh count/heap/5B5BBAはPARTIAL。旧1918-01を重複登録しない。B1920-02で74 writer59C747が判明、raw key624EE8/既定/@はVERIFY。原作取得拒否の6F0/6F4、4E13F0等を再試行/代理抽出する依頼ではない。既存証拠からのreceiver/input/return契約整理を継続希望。


- WRQ-20261013-REA-DEATH / P0 / PARTIAL: DEATH60 AllLifeWnd(vptr637E64/453A50/+84)と61/62 FlashObj、63Task型bind差分、65/66pool/header/node本体分離を受領。局所READY-FOR-INTEGRATION、全通常死亡CLOSEDではない。Work Task種別・実getter接続は独立候補。DEATH64拒否/QUEUE PROGRESS EPERMは別BLOCKED、迂回不要。参照=REA所有SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md DEATH60～66。


- WRQ-A-HOST PARTIAL:A1901 parser実caller受領、host完了とは別。WRQ-C-BATTLES PARTIAL:C1854 source固定loop受領、合法G0/G1/G2未達。D938行、Ecp121/430・E-GOLDEN OPEN、Claude付録A未統合を保持。CLOSED追加0、各チャットへの自動送信なし。








### Work開始時照合 1056後 postcore


- 前turn PROGRESS、1056 source/test SHA・HEAD/dirty一致確認。B1930-01 rush→74/+78/+7C/+80、1926-03 268二writer、1930-07 2A0/2B4 typed producerを受領。rushキー判明で以前のUNKNOWN名を訂正、missing/@/親getterはVERIFY維持。Workは54E31C postcore list/追加処理/正常returnを保存契約から接続中。C1918/1927/1921/1931はSOURCE/条件付き差分として受領、合法戦闘packet未達。








### Work追加成果受領・postcore統合中（2026-10-13）


- WRQ-20261013-B-SKILL / B / P0 / PARTIAL: B1825/1831-01/1833-01の既存保存nativeから54E31C list選択、4C3250矩形、4C3140非zero phaseをWorkへ接続。保存Ghidra54E0B0により609268=USER32.PtInRectを照合し、実Windows APIを実行（HOST_API、原作ACTUALではない）。限定branchで54E3E1→57FA9E。新規helper11/DAT8 PASS、広域/EXEはこの追記時点RUNNING。停止は非空list4BA009/zero phase4C314C/帰還後57FA9E。Skill30/34/268・stack/viewport/phaseは明示合成入力、原作getter/defaultの証明ではない。


- B1946-87 Skill254 scalar writer、B1945-01 table19 parity、B1951-01 next_order/next_interval、B1953-01 vector異常入口、B2004-01 fallback自己除外訂正を受領。局所READY-FOR-INTEGRATIONと依頼全体PARTIALを区別。table parityはB1831-02と意味重複あり。B2004は現targeting_subsetのself除外と整合、除去しない。B1939-01 three-vectorはowner保存拒否/NOT READYであり採用・代理転記しない。


- WRQ-20261013-REA-DEATH / REA / P0 / PARTIAL: DEATH67～71、MOVEANCHOR/MOVECENTER、RETREATVOICE/RETREATMSGの追加見出し・境界を確認。参照=rea_lab/decomp_task/SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md（1080行時点）。67～71の詳細適用監査は次工程。Task型の合法bindingを行うまではUnit+800等へ推定割当しない。QUEUE/PROGRESS EPERMと旧拒否は独立BLOCKEDを維持。


- WRQ-20261013-D-COMMAND / D / P0 / PARTIAL: D1939-01の派生poll clear順、D1952-01 owner-side条件付き参照、D1952-02音量gateを受領。通常命令consumerは未完。WRQ-C-BATTLES / C / P0 / PARTIAL: C1931等SOURCE局所のみ、合法packet未達。C1941-01はC1942 recovery記録によりNOT READY/BLOCKEDであり統合しない。


- WRQ-20261013-E-GOLDEN / E / P1 / OPEN: MASTER cp123/445を確認。原作Gameplay Golden0/strict MATCH0、既存拒否cp122別8件は未解消。A1901/Claude3463行は既受領状態。CLOSED追加0。


- 次のWork P0: 57FA9EのSkill100/104 vector→57FBAC SkillF4→57FC14 callee57BE30→候補list cleanup/正常RET。参照は既存exe/T013_SUPPORT_EVAL_FOCUS.txt:959以降。580280拒否範囲へ踏み込まず、未接続calleeは停止を維持。別優先=通常flash6F0/6F4 producer、HPbar新規登録、全Unit/Task継続。追加研究依頼は既存ID内で不足した合法producer/identity/正常return証拠のみ、同関数再解析や拒否再試行は依頼しない。








### WORK-POSTCORE-RETURN-20261013-1075｜終了前照合


- WRQ-20261013-B-SKILL / Work統合 / P0 / PARTIAL: 上記WIPを1075PASS/FAIL0/ERROR0、source/EXE2ケース一致で検証済へ更新。list抽選・矩形・非zero phase・54E3E1帰還の局所契約は製品接続済。停止VA57FA9E（空list/条件付きpostcore）、4BA009（非空listvirtual）、4C314C（zero phase）。参照=固定handoff同checkpoint、製品log support_postcore_broad/exe。残範囲=Skill100/104/F4、57BE30、list解放・親/UnitRETURN、通常flashと実DAT既定値。依頼全体CLOSEDにはしない。


- E cp123/445、REA追加資料/各owner拒否の状態は直前受領節どおり。WRQ E OPEN、他依頼PARTIAL、各拒否/EPERM BLOCKEDを維持。ユーザーの追加承認・研究の重複再解析は不要。保存後読み戻し/ハッシュ確認、原作Golden0/strictMATCH0。








### Work開始時照合1075後｜支援追加技能/共通後処理


- 前turnはPROGRESS。source/test6SHA一致、HEAD/statusと固定handoff1075を確認。Work担当native_unit_ai/session/runnerと専用testのみ編集。WRQ-B-SKILL/P0/PARTIAL、停止57FA9Eから既存T013_SUPPORT_EVAL_FOCUSとT012_SKILL_POST_57BE30を利用。射撃側57BE30 prefixを共有し、追加技能/未知callee/正常returnを混同しない。研究B1939の拒否payloadは採用せず、独立した従来保存nativeのみ参照。








### Work支援後処理の局所checkpoint（広域試験中）


- WRQ-20261013-B-SKILL / P0 / PARTIAL: 57FA9Eの追加技能列/optional文字列gate→57FC14の57BE30、優先度/待機writer、57BF3Dの後段gateをWorkへ接続。新規15件・関連27PASS。広域/新EXE2ケースはRUNNINGで、完了件数は終了checkpointを参照。実DAT既定値未証明のSkill100/104/F4/208/200/20Cは明示合成入力のまま。


- 最優先停止57BF54→565780/ret57BF59。既存T010の部分証拠では不足した565780成功枝のみ、許可されたLocal原作隔離copyをread-only限定読取し確認。20B確保→owner+4を3linkへ、WORD10=0、node+C=Skill*、5657BA RET4。allocation fail枝/フック/アドレスはVERIFY。製品log support_special_node_staticへSHA/native命令保存。新規原本実行なし、既拒否再試行なし。


- 保存Ghidra5469B0（製品log support_special_insert_saved）はunsigned node+C比較・等値右下行→40EBE0挿入へ。次の依存=565780正規確保adapter、5469B0/40EBE0 native ABIと木更新、57BE30 stack/SEH/cookie、57FC19候補list free→57FC42 AL1。同じ索敵/回復/MP/EXPを再解析/再実行しない。非空追加技能の402710/4678A0/580280側は別VERIFY、580280拒否範囲の再取得は禁止。


- REA TASKTYPE-MATRIX/STATICUNIT-TASK/DISABLEを詳細受領。Task7型28slot＋StaticUnit4slotのSTATIC確認は製品混合Task試験ではない。合法vptr保持で型別callbackとpause/busy gateを結合する独立工程を次候補にする。SimpleStaticUnit+34 LifeBar-only、+58専用disableを通常Unit死亡へ代用しない。QUEUE/PROGRESS EPERM等は別BLOCKED。








### WORK-SUPPORT-FINALIZE-20261013-1090｜終了前照合


- WRQ-20261013-B-SKILL / Work / P0 / PARTIAL: 上記RUNNINGを広域1090PASS/FAIL0/ERROR0・EXE2ケース全JSON一致で確定。主停止57BF54、追加技能ありは57FB02/57FBDA、cooldownありは57BEC3。参照=固定handoff同checkpoint、log support_finalize_broad/exe・support_special_node_static/insert_saved。次=565780確保/5469B0/40EBE0木挿入、57BE30 stack/epilogueと候補list free。原作special未指定getter・Skill20Cキー/既定値を不足として明記し、m_healの合成4C3を原作確定値にしない。


- WRQ-REA-DEATH/P0/PARTIAL: TASKTYPE-MATRIX/STATICUNIT-TASK/DISABLEを限定READY-FOR-INTEGRATIONとして受領、通常死亡全体CLOSEDではない。通常Unit/StaticUnitの別vptr・別disableを守る。旧拒否/EPERM BLOCKED維持。E-GOLDEN OPEN、MASTER cp126/467、Golden0/MATCH0。B2018-71 SOURCE-only受領、D後続詳細未読は未統合。ユーザーへの追加承認要請なし、各研究チャットへ新規送信なし。








### Work開始時1090後｜特殊技能登録と帰還


- source/test6SHA・HEAD・最新handoff1090を照合。B2023-77定数、2034-62 refresh除去を局所受領（PARTIAL、未統合）。主線565780→5469B0→40EBE0/回転を保存Ghidraで特定後、未拒否の4関数計656BをLocal限定read-onlyでnative照合し既存製品logへ保存。Work所有のnative_skill_bookkeeping.pyを独立実装予定、研究/Claude資料は無編集。原作Golden0/MATCH0。








### WORK-SUPPORT-SPECIAL-PHASE-20261013-1109｜終了前照合


- WRQ-20261013-B-SKILL / Work統合 / P0 / PARTIAL: 565780→5469B0/40EBE0木挿入・57BE30 stack/SEH/cookie→57FC19を製品接続。B2023-77初期phase定数も接続済（局所契約統合済、依頼全体未完）。新規19/広域1109PASS・EXE2case JSON一致、元Golden0/MATCH0。参照=固定handoff同checkpoint・製品log support_special_phase_broad/exe。


- 最優先停止57FC19。次のWork: 既存T013_SUPPORT_EVAL_FOCUS:1072とT013_SKILL_HANDLERS_BOUNDED_NATIVE:813を使い、親57F570 entryのalignment/SEHとlist解放所有権を捕捉→57FC59 RET4→57E5E2/57AEC1。node/headの解放順、既filter解放nodeとの重複、AL1・UnitRETURNを別判定。新規再解析依頼ではない。


- Bへの既存ID内要望: 未指定special/74/6F0等の合法producer/identity・原作初期値を既存保存証拠から整理。拒否literalや49ED30新取得を再試行しない。B2042-68/2048-69/2055-70は局所READY-FOR-INTEGRATION受領、4E02A0全経路は子callee未完のPARTIAL。新しい49ED30取得拒否はBLOCKED/NOT READYを維持。


- WRQ-REA-DEATH / P0 / PARTIAL: VECTOR-GROW限定STATIC受領、次callee501A40取得拒否はBLOCKED/NOT READY、EPERMも未解消。型別Task継続・通常死亡の独立接続をWorkの次候補とする。拒否再取得/代理抽出を依頼しない。


- WRQ-D-COMMAND / P0 / PARTIAL: D2038-01 producer局所READY-FOR-INTEGRATION、最終Unit命令consumerは未完。D1952-05/06の限定RTS/音声と通常戦闘を混同しない。WRQ-C-BATTLES/P0/PARTIAL: C2026-01 SOURCE受領、合法G0/G1/G2未達。E-GOLDEN/P1/OPEN、E cp128正式472を確認。各拒否状態維持、依頼全体CLOSED追加0。ユーザー追加承認不要・各チャットへの新規送信なし。








## WORK-PLAYABLE-ENGINE-POLICY-20261013｜保存と現行監査


- 2026-10-13T22:01:44.769751+09:00。直前相談はPC変更なし。今回は新方針/実装計画を保存。code変更0/test未実施、前1109PASS/EXE2case/Golden0/MATCH0は履歴。


- Git/dirtyと表示/仮試遊/数式/Unit生成/戦略IFを照合。Claude source非編集、新F停止Work引継ぎ維持。


- 次はWBS新計画Task1、意味ベースDAT rosterから着手。旧57FC19継続解析へ戻らない。追加録画依頼/研究チャット送信なし。








### WORK-SEMANTIC-ROSTER-20261013 終了前照合


Workは新方針の意味ベースDAT Unit生成を実装、新規5/関連113PASS。追加研究依頼なし。旧VA帰還研究を再優先せず、既存意味/数式を表示と実行へつなぐ。B/REA/A/C/D/Claudeの依頼全体はPARTIAL、E-GOLDEN OPEN、拒否BLOCKED維持。参照=固定handoff/WBS同checkpoint、製品log semantic_roster_related。








### WORK-SEMANTIC-VIEW-20261013 終了前照合


Workは意味ベースDAT配置→原作MAP/3Unit画像表示を新EXEへ接続、JSON/PNGソース一致。解析依頼新規0、旧内部帰還研究へ戻らない。次は移動/Stop/時間、必要根拠は既存速度・地形・host時計。D関連未解決表示stairN/stairoffはWorkが既存素材/定義でまず照合する（新規チャット依頼ではない）。全依頼PARTIAL/E-GOLDEN OPEN/拒否BLOCKEDを維持。





### WORK-SEMANTIC-TERRAIN-20261013 終了前照合


Work所有の地形接続を追加、新規5/関連46PASS、s1全12100セル属性/33movetype取得、Windows source起動成功。次はMove/Stop/時間と衝突。研究A保存T010_FRAME_ORDERを再利用。65BD50は初期1の後5709B2設定writerあり、設定キー627EC0・適用順を既存資料からWorkが先に確認（新規解析依頼なし、拒否範囲再取得不可）。WRQ-E-GOLDEN OPENの小範囲観測として録画1本+可能なら開始saveコピー/設定をユーザーへ依頼済。提供待ちで独立工程を止めない。各研究依頼PARTIAL、旧拒否BLOCKED維持。





### WORK-SEMANTIC-CLOCK-GEOMETRY-20261013 終了前照合


Workでradius/radius_press初期化の限定nativeを照合して実DAT Unitへ接続、時計/停止/速度を新EXEへ追加。新規10/関連69PASS、原作Golden0。次は通常移動。WRQ-B-SKILL/REA/D/A等PARTIAL、E-GOLDEN OPEN/旧拒否BLOCKED維持。新規チャット依頼なし。Workが先に既存scenery/field衝突登録・Unit移動条件/描画矩形producerを照合する。627EC0=move_speedと普通枝global倍率1は解消済みで再調査不要、特殊dungeonは別。録画待ちで独立工程を止めない。








### WORK-SEMANTIC-MOVEMENT-20261013 終了前照合


Work限定移動/Stop/時計を新EXEへ接続、関連77PASS。追加研究依頼0。初期対象はユーザー指定の迫真空手道場po2（別poo2と区別）。WRQ-B-SKILL/REA/A/C/D/ClaudeはPARTIAL、E-GOLDEN OPEN、既存拒否BLOCKEDを維持。REA保存成果末尾と旧PROGRESSを再読、解析実行機能/EPERM解消は未確認。次は既存技能条件/間隔/効果の意味ベースruntime接続とpo2開始イベント/戦略IF確認。研究へ内部container復元を一括依頼しない。普通戦闘録画1本＋可能なら開始saveコピーを依頼済、提供待ちで独立工程を止めない。








### WORK-SEMANTIC-SKILL-INPUTS-20261014 終了前照合


WRQ-B-SKILL/P0/PARTIAL: Workで実Unitの技能参照グラフと説明表示を接続。次はpo2のsw_karate0 next/joint_skill/next3の時刻・連撃・子発射。既存B1930-01/1951-01とnative_rush_missileを先に利用、新規チャット送信0。B2113 510C20取得/B2218HANDOFF/B2310owner保存拒否はNOT READY/BLOCKED、代理保存/取得しない。各依頼PARTIAL、E-GOLDEN OPEN、その他拒否維持。REA新スキルは読了、native MCPツール無し/rea PATH未検出、登録変更やインストールは未実施。保存済成果は利用可能。詳細=固定handoff同checkpoint。








### WORK-SEMANTIC-RUSH-TIMING-20261014 終了前照合


WRQ-B-SKILL/P0/PARTIAL: B1218caller count/lifetimeとB1930interval変換を新RuntimeActionsへ利用。既存コードのRush timing再解析不要。次に必要=sw_karate0のjoint_skill/next/next3/next_first/next_last/pair_nextの実発火時点、wait_timeと子弾/命中への接続。まずWorkが保存済証拠を利用、追加解析チャットへの送信0。拒否580280本体等の新取得や代理取得を依頼しない。各依頼PARTIAL/E-GOLDEN OPEN/既存拒否BLOCKED維持。固定handoff同checkpointと実結果JSONを参照。








### WRQ-20261014-CLAUDE-YAJU-ATTACK｜Claude Code｜P0｜PARTIAL


- 対象: 勢力「迫真空手道場」に初期所属する田所(yaju)の技能「迫真空手・正の裏技」sw_karate0。勢力名は技能名ではない。MUR/KMR等の技能とは区別する。ユーザー要望により会話で依頼文を提示済み。実送信・着手・成果保存は未確認。


- 目的: 通常戦闘の一回の攻撃を実効果へ接続するため、既存保存証拠・DAT・文書からゲーム上の意味を整理。内部ABI/allocatorの復元、戦略機能追加は今回の依頼対象外。


- 停止箇所: sw_karate0(next_first on, next sw_karate_js_joi, pair_next karate_pr0) → joint_skill/wait_time6/rush2/interval4 → sw_karate_js_joi2 → sw_karate_js/sw_karate_jsb/sw_karate_js2。これは参照関係であり実行順の確定ではない。


- P0未完: next/next_first/pair_next/joint_skill/next3の発火時点、wait_time起点と連撃の関係、親子の発動者/標的/座標/方向、start_random_degree/rush_random_degreeの乱数順、子の生成/命中/終了条件。


- P0命中: damage=0/-3、collision=none、range/speed/寸法と当たり判定、一弾の同一/複数対象への命中回数、消滅/貫通/next=punch_hit、既存数式へ渡す属性/能力/耐性。


- P1: 射程/発動条件/攻撃間隔、MP/EXP単回処理、slide/slow_per、画像アニメ/音の開始終了。通常死亡全体・戦略復帰・他勢力特殊技能へ広げない。


- 参照: _work/karate_attack_inputs.json、最新固定handoff、B/D/REAの許可された保存成果、battle_runtime_actions.py/skills.py、native_rush_missile.py、native_dat_damage_adapter.py、native_damage_compute.py、native_unit_hit_prefix.py。連撃タイマーと既存数式の再解析・再実装は不要。


- 納品: Claude所有の既存findings/handoffに時系列表、条件/入力/副作用/RNG/出力、証拠path+行/節またはVA、接続可否、最小試験、残るVERIFY。STATIC/DAT_DERIVED/文書/ACTUALを区別。原作未比較ならGolden/MATCHを増やさない。


- 分担: Workが戦闘コード/テスト/統合を所有。Claudeは本件調査のみ、Work source/tests/固定handoff/本キューおよび研究資料へ書込禁止。原本read-only、Git禁止操作維持。拒否済580280等の新取得/別経路/代理取得は禁止。この依頼は再審査承認ではない。


- 完了条件: 田所の当該技能一回についてWorkが実行順/命中/数式/演出を接続できる契約を保存。未確定点は具体的な不足として保持。Workによる接続検証までCLOSEDにしない。








### WORK-RESOLVED-CHILD-IMPACT-20261014 終了前照合


WRQ-20261014-CLAUDE-YAJU-ATTACKはOPEN（会話指示文/本キュー保存済、受領/実行未確認）。対象は勢力ではなく田所の技能。Workで命中済みchildの出所検証から既存HP/EXPまで接続、120PASS。各旧依頼PARTIAL/E-GOLDEN OPEN/安全拒否BLOCKED維持。








### WORK-LIVE-EFFECT-BRIDGE-20261014 終了前照合


CLAUDE-YAJU-ATTACK OPEN継続（成果未確認）。Workは共有状態bridgeを実装/149PASS。E-GOLDEN OPEN: ユーザーからマップテストの選択/戦闘画像・起動手順を受領。sci_mt/po_mt/po_mt2、試験unit_mt、fight be_stを保存DATで確認。テスト専用条件を控えて比較入口に使う。実選択難易度等は未確認、Golden/MATCH0。原本DAT編集せず、必要な検証copyの設計は別。追加チャット送信なし、旧拒否BLOCKED維持。








### WORK-YAJU-ROOT-CONTRACT-20261014｜成果受領・追加観測依頼


- WRQ-20261014-CLAUDE-YAJU-ATTACK / Claude Code / P0 / PARTIAL。旧OPEN/未受領は履歴。参照=docs/PEER_SCRIPT01_FINDINGS_20261011.md §80、固定handoff同checkpoint。root倍率0の計算/RNG/handlerはWork回帰3PASS。next3/待機/命中分類は接続候補で、依頼全体CLOSEDではない。


- 停止=580280生成入力（コード新取得拒否維持）、生成同tickの更新。未完=初期位置/角度/速度/乱数順/slow_per、演出と実命中の実行接続。


- Claude追加依頼を会話で提示（実送信・着手未確認）: 既存ローカル観測ツール/offset/プロセス識別を確認し、ユーザーの原作操作中に田所の一回の攻撃を自動記録する準備。原本read-only。コード注入/書換え/乱数固定なし。拒否済みコードをメモリ経由で取得せず、今回拒否されても迂回しない。


- 記録候補: yaju/標的のID・XY・向き・HP/MP/EXP、joi/joi2/js/jsb/js2/karate_pr0/punch_hitの技能ID・親/標的・XY/角度/速度・wait counter・出現/命中/消滅。既知フィールドだけ読み、不明を推測しない。短命弾取りこぼし/複数時点混在を評価し、最初の観測時刻を生成時刻と断定しない。原作更新/描画frame/録画frame/実時間を区別。


- ユーザー手順を固定難易度・出撃条件で開始→記録開始→田所が一回技能使用→記録終了へ絞る。unit_mtをyajuと同一視しない。標準マップテストで不可能なら原本を変更せず別試験copy案を提示。ユーザーにリアルタイム数値転記を要求しない。


- 優先観測=子初期位置、jsb/js2移動量、生成から初回更新、wait6、Rush2発と子命中対応、突進往復。必要な距離/向き差分だけ比較。停止観測と連続実行を区別する。ツール存在のみで観測可能と判断せず、小さく取得成功を確認する。


- Claudeは既存の自身findingsへ再現操作・取得根拠・ログ場所・実測/静的推定/未取得を保存。Work source/queueは編集禁止。§79.9関連370PASSは担当報告でWork未再実行。Workによるツール導入/attach/原作起動/観測は未実施。Golden/MATCH0。








### WORK-MISSILE-WAIT-20261014 終了前照合


WRQ-20261014-CLAUDE-YAJU-ATTACK / Claude+Work / P0 / PARTIAL。§80 wait意味を保存54BA00で照合してWork runtimeへ統合、160PASS。停止=580280生成入力/生成同tick更新、未完=joint寿命・next3発火の実接続/飛翔/命中。次はWorkが保存54BA00/54DCA0とSkillBookを利用、Claudeは既存の観測準備依頼。新規チャット送信なし。原作Golden0/MATCH0、拒否範囲維持。








### WORK-JOINT-NEXT3-20261014 終了前照合


WRQ-20261014-CLAUDE-YAJU-ATTACK / P0 / PARTIAL。Workで静止joint寿命・next3生成順・親target継承を保存54BA00/54DCA0から統合、実DAT29PASS。次の不足は葉の生成入力と実飛翔/命中、弾ごとのhit context。Claude観測準備の既存依頼を継続し新規同内容依頼なし。新EXE更新済だが原作観測なし、Golden/MATCH0。拒否580280等は維持、CLOSEDにはしない。








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


CLAUDE-YAJU-ATTACK / P0 / PARTIAL。Workで解決済み通常弾body→実DAT子ダメージを接続、155PASS、新EXE更新。初期化/角度RNG/候補選択/next命中演出のadapterが未完でCLOSED不可。制御ログの変位校正後210状態一致はGameplay MATCHでない。参照=固定handoff同checkpoint、_work/linear_missile_observed_replay.json。追加ツール導入/ユーザー操作は不要、Claudeソース未編集、新規チャット送信なし。DAT-DELIMITERはOPEN、旧拒否BLOCKED維持。








### WORK-LINEAR-LAUNCH-UNIT-HIT-20261014


CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。実DAT飛翔compilerと4E5860限定Unit判定を実装、166PASS。保存原作ログの初期角から262/262状態再生（同一logで数値profile選択、独立MATCHでない）。停止=実Unit矩形/陣営/候補順供給、生成位置/角度RNG、next命中演出。参照=固定handoff同checkpoint、linear_launch_replay_result.json。Claude末尾の付録Aは未統合FPUドラフト、実測確定とは扱わない。追加ツール/ユーザー操作要求・新チャット送信なし。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。





### WORK-LIVE-ROSTER-PROJECTILE-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。live実Unit矩形/共有HP・EXPへの普通弾adapterを接続、177PASS、新EXEbuild/CLI確認。停止=発射pose/角度RNG・native候補順provider・next命中演出/操作接続、参照=固定handoff同checkpointと_work/live_projectile_verification.json。CLOSED不可。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。ユーザー長時間記録案は受領、容量/負荷/画面切替/場面識別の設計確認前に無人運転しない。新規解析依頼送信・追加ユーザー操作要求なし。





### WORK-LIVE-PROJECTILE-DISPLAY-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。通常弾snapshot→原作画像→既存WindowsGUIへ接続、185PASS、新EXEbuild/CLI成功。source画面で実DAT拳1体を確認（解決済fixture、命令発射ではない）。保存ACTUAL52組でpunch_hit生成中心/表示角を親jsb移動前状態と照合。停止=命中静止animation factory/音RNG・発射pose・GUI命令。参照=固定handoff同checkpoint、punch_hit_observed_display.json、projectile_display_verification.json。追加ユーザー操作/新解析依頼送信なし、DAT-DELIMITER OPEN、拒否BLOCKED維持。





### WORK-HIT-ANIMATION-LIFECYCLE-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。命中後の移動前rect→実DAT静止演出tick/4コマ/消滅を接続、関連174PASS＋ガード変更後局所37PASS。source Windowsで原作命中画像確認、新EXEbuild/CLI成功。停止=親表示角/汎用factory・sound RNG4B9F70・GUI命令。参照=固定handoff同checkpoint、hit_animation_verification.json。音は要求のみ/再生未実装。追加依頼送信なし、DAT-DELIMITER OPEN、旧拒否BLOCKED維持。





### WORK-RUNTIME-SOUND-AND-CHILD-ANGLE-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。既存B1825-01/x86を再利用し音候補の共有RNG選択→GUI再生queueを接続、親表示角もchildへ供給。177PASS、新EXEbuild/CLI、source Windowsで原作WAV再生Channel1件。native音量/定位/priorityはVERIFY。停止=汎用factory・root-chain pose/発動・GUI攻撃。参照=固定handoff同checkpoint、runtime_audio_verification.json。追加依頼送信なし、DAT-DELIMITER OPEN、旧拒否BLOCKED維持。











### WORK-RESOLVED-HIT-FACTORY-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。通常next命中演出の実DAT組立をRuntimeRoster本体へ移動、関連178PASS、新EXEbuild/CLI確認。source Windowsでdamage/EXP→factory→画像/音queue接続を検証。停止=通常攻撃受付/root-chain pose/角度RNG/GUI発動、参照=固定handoff同checkpoint・_work/hit_factory_verification.json。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。追加チャット送信/ユーザー操作要求なし。








### WORK-RUNTIME-RANDOM-RUSH-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。既存55029B方向計算を実DAT Rushへ接続、各弾emit時に共有RNG1回。関連187PASS＋召喚guard後35PASS、EXEbuild/CLI成功。停止=通常sword受付/root効果順/子生成pose・start_random_degree/操作発動。参照=固定handoff同checkpoint・_work/random_rush_verification.json。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。追加依頼送信なし。








### WORK-SWORD-ROOT-PREFIX-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。通常swordの非混乱R0..R3を共有Unitへ接続、184PASS。停止=VERIFY_SWORD_AFTER_ROOT_DAMAGE（57E89F sound/next/slide/pair/57BE30後処理は未接続）。source battle_runtime.py::_sword_prefixesを保持しMP/root二重実行を禁止。参照=固定handoff同checkpoint・_work/sword_prefix_verification.json・Claude§80.3。EXEは前版、今回GUI発動なし。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。追加依頼送信なし。








### WORK-SWORD-NEXT-AND-LUNGE-EVIDENCE-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。root処理済→sound→next_first Rush登録を接続、関連50PASS。停止=VERIFY_SWORD_SLIDE。保存ACTUAL3503active sampleで特殊flag1/地上座標固定/矩形移動を確認、native_unit_motionの通常flag0消費を代用しない。参照=固定handoff・sword_lunge_path_analysis.json・保存5795E0:6329..6426。残り4C60F0特殊位置参照/579290生成/midpoint/pair/post。DAT-DELIMITER OPEN、既存拒否BLOCKED、新規依頼送信なし。








### WORK-SPECIAL-TRAJECTORY-CONSUMER-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。特殊5795E0 path消費をUnit motion phaseへ接続し地上固定/矩形索引更新を実装。関連480PASS＋共有実Unit追加後58PASS、新EXEbuild/CLI成功。停止=root VERIFY_SWORD_SLIDE、未完=生成式/新GUI表示pose/pair/post。参照=固定handoff・special_motion_verification.json・native_unit_motion.advance_special_trajectory_frame。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。新規依頼送信なし。





### WORK-LIVE-UNIT-DISPLAY-POSE-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。特殊motionのlive矩形→新GUI表示poseを接続、ground維持。関連69PASS、source Windows画像2Unit/20frame確認、EXEbuild/CLI成功。停止=VERIFY_SWORD_SLIDE、未完=579290生成式/子pose/pair/post/GUI攻撃。参照=固定handoff同checkpoint・_work/unit_pose_verification.json・保存B1253-01契約。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。追加依頼送信なし。





### WORK-SWORD-SLIDE-BUFFER-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。実DAT slide_speed→解決済み幾何入力から往復buffer生成→共有Unitへ接続。関連104PASS、生成/消費統合後527PASS、EXEbuild/CLI成功。停止=VERIFY_SWORD_PAIR。未完=距離/角度/trig前段・pair_next factory・57BE30・GUI攻撃。参照=固定handoff同checkpoint・_work/sword_slide_verification.json/evidence.json・保存B1253-01。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。新規依頼送信なし。





### WORK-SWORD-PAIR-JOINT-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。初期化済み不可視jointのlive caster追従→next3順序/子pose/来歴を本体接続。R7は明示生成RNG receiptを照合しVERIFY_SWORD_POSTへ、関連146PASS/EXEbuild・CLI成功。元initializer入力/乱数は未解明、合成receiptを原作実測としない。停止=57BE30、未完=R6幾何前段/R7初期化/子のcenter=end・swing描画/GUI発動。参照=固定handoff・_work/sword_pair_verification.json/observed_pose.json。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。新規依頼送信なし。








### WORK-SWORD-POST-VALUES-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。通常swordのR8前段を実DAT slow_per/slow_time→共有Unitへ接続。関連150PASS/FAIL0/ERROR0、新EXE build/CLI成功。待機・cooldownは未解明slotの明示入力を必須とし、後段未処理で停止を維持。 停止=57BEC3/57BF3D、未完=20C/210/214実入力・post後段・R6/R7入力・GUI攻撃。参照=固定handoff同checkpoint、_work/sword_post_verification.json、B T012§86/保存57BE30契約。624DD0/624DE4の拒否を迂回しない。DAT-DELIMITER OPEN、旧拒否BLOCKED維持。新規依頼送信なし。





- 後段依存の追加照合: Claude peer_script01_native_definitions.py:461/1057/1104のdef.talent_on=+75、special_77=+77をread-only確認。linked判定はこの既存意味を使える。Skill4CはB-20261013-1740-01（data/T011_SPECIAL_PROPERTY_SKILL4C_20261013.md）でspecial=on→1/整数→その値が確定済み。ただしoff/欠落のnative numeric値は同契約でもVERIFY。rootで省略されるから0と推測しない。Unit238/1F8/1F9の生成writerは今回ソース検索で未接続、次回この入力を解く。新しい仮defaultや後段skip実装は追加しなかった。








### WORK-SWORD-POST-TAIL-20261014


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。実DAT special・実defのtalent_on/special_77を発動後分岐へ接続。追加処理不要の枝は技能本体return AL1まで進み、VERIFY_SWORD_OUTER_ACTIONへ。関連155PASS/FAIL0/ERROR0、新EXE build/CLI成功。 停止=外側577600/571A40またはpost追加callee。未完=Unitflag生成/26C/wait/cooldown/R6/R7入力/同一tick/GUI。参照=固定handoff同checkpoint、_work/sword_post_tail_verification.json。DAT-DELIMITER OPEN、既存拒否BLOCKED維持。





WRQ-20261014-A-GENERIC-SCALAR-AUDIT / A / P1 / OPEN。停止VA=50536A/505381..5053C3/464B7C。依頼: T005_FORMAL_GRAMMAR.mdの『ordinary string scalar=80000008』と保存T005_EXPLICIT_NULL_PROBE.txtを照合してA所有資料を訂正または反証する。Work照合では非数値枝はnumeric storeを飛ばし初期0を保持、Claude現行codeと一致。@のtext保持は別争点で今回未確定。参照=_work/sword_post_tail_evidence.json、固定handoff最新checkpoint。新規原本取得・拒否迂回・Work/Claude source編集不要。キュー記載のみ、別チャットへの送信なし。








## WORK-LIVE-MOTION-BINDING-RECOVERY-20261016


実UnitのHP/MP/能力値共有mappingを通常移動・吹き飛ばし継続処理がclearして例外になる不具合を修正。native_unit_motion.pyの段階state反映をupdateに変更。RuntimeRoster.advance_resolved_unit_motionで移動後の命中/描画位置publicationも更新し、stale geometryを検出する。未完cast中は進めず、57AD3C到達をAI完了にしない。


- 前回保存済みの製品2fileとtest1fileを検証JSONのSHAと照合し一致。関連8module581PASS/FAIL0/ERROR0、63.625秒（記録値）。今回再実行ではなく既存terminal結果の回収。参照=_work/live_motion_binding_verification.json。実DAT Unitと合成2点経路/knock fixtureを使用、原作実機比較ではない。全suite未実施、既知sourcebook2FAIL未解消。


- 前回GUI起動は自動承認サービスの利用制限で未実行。今回は同じLocal経路の読取/プロセスが成功し記録回収。今回修正を含むEXE build/GUI検証はこのcheckpoint時点で未実施。従来EXEはPOST-TAIL版。


- G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Gameplay Golden0/strict MATCH0。原本/Claude source非編集。HEAD be45dc2d563dcc1885a3caf4e3c8af43f6b8619b。


- 次: 現行sourceのbuild/GUI確認、外側行動returnとmotion/弾更新の統合。Unitflag producer・R6幾何・R7初期化RNG・wait/cooldown・26Cを未知のまま既定値化しない。追加EXE解析は保存成果を先に照合しREA MCP/Ghidraを優先検討、拒否範囲は再取得しない。


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。停止=VERIFY_SWORD_OUTER_ACTION(577600/571A40)、上記未完範囲維持。A-GENERIC-SCALAR-AUDIT OPEN、DAT-DELIMITER OPEN、旧拒否BLOCKED。新規依頼送信なし。





- 同checkpoint追記: 現行EXE build exit0/CLI --help exit0、SHA d2db89ad54eb8d22e0b26852a6b6d7f0df4d54322ec5f376e2384ec1cb6bb91a。_work/live_motion_build_verification.json。source Windows GUIもexit0、実DAT2Unitを合成2点経路で更新後20frame一時停止表示、描画位置(272,260)→(288,264)、sprite欠落0/pose gap0。PNG読み戻し確認。_work/live_motion_view_result.json/live_motion_view.png。GUIはsource、EXE内戦闘の試験ではない。海上は合成配置、地形一致を主張しない。stairN/stairoff静的素材解決は残存。初回GUIはPowerShell日本語encoding未指定で素材path読取失敗1回、UTF-8明示後成功。製品source変更なし。次は外側行動returnと同一tick統合。Golden0/MATCH0。








## WORK-SWORD-OUTER-RETURN-20261016


- 前turnはREA紹介への回答のみで開発state変更なし(NO_PROGRESS)。今回は最新handoff/WRQ/Git dirtyを確認しWork本体battle_runtime.py/testsのみ変更。原本/Claude所有ファイル非編集、新規EXE解析なし。


- RuntimeRoster.resume_resolved_sword_outer_actionを追加。既存native_unit_ai.resume_selected_skill_post（57E610/577600/571A40/57B375）を再利用し、技能本体AL1済みかつ追加操作処理不要の枝だけ_sword_prefixesを解除。実HP/MP/EXP/RNG/弾登録を再実行しない。local frameは制御値で、元stack/allocation再現を要求しない。


- 操作側577600が必要ならVERIFY_SWORD_OUTER_CONTROLLEDで停止、未実行の副作用をreturnと偽らない。Unit1863C/8C/1F8は既存live値を要求し欠落を0としない。重複resume拒否。


- 実DAT root→Rush→slide→pair→post→outer return→次tickのRush1発目まで既存統合testを延長。R6幾何/R7生成RNG/flag/wait/cooldownは明示SYNTHETIC条件、GUIから発動可能になったとはしない。特殊motionと弾の同一tick接続は次工程。


- TEST: 新規3件missing API ERROR3を確認→実装。初段Roster37PASSだが存在しないtest_native_unit_ai指定でloader ERROR1、指定修正後4module496PASS/FAIL0/ERROR0、61.141秒、PID10728 exit0。_work/sword_outer_verification.json。全suite未実施、既知sourcebook2FAIL未解消。以前581と合算しない。


- EXE build/CLI --help exit0、SHA 9a0507a003419b1e0afd0f6c1e147d8c69b86c4ab02a96f3c099e90017419a7b。_work/sword_outer_build.log。今回GUI/原作実機比較未実施、Gameplay Golden0/strict MATCH0。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。


- 次P0: 保存577600操作側契約とUnitflag生成を照合し、プレイヤー発動に必要な副作用を接続。特殊motionと既存弾queueの順序/初回更新を統合する。R6幾何・R7初期化/RNG・wait/cooldown/26C未知を黙って既定値化しない。拒否範囲維持。REA/Ghidraは新規不足仕様の調査時に優先検討、既存証拠の再取得不要。


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。停止VA=577623/577600操作枝、未完=Unitflag生成/同一tick/R6/R7/wait/cooldown/26C。参照=固定handoff同checkpoint・_work/sword_outer_verification.json。A-GENERIC-SCALAR-AUDIT OPEN、DAT-DELIMITER OPEN、旧拒否BLOCKED維持。追加チャット送信なし。








## WORK-CONTROLLED-POST-DEPENDENCIES-20261016


- 前goal turn=outer return実装/496PASS/build/checkpointでPROGRESS。今回保存B契約とGhidra疑似codeを照合。製品source変更/テスト再実行/EXE buildなし。最新検証は前checkpoint496PASS/FAIL0/ERROR0、Golden0/MATCH0。


- 保存T013_POST_ACTION_SKILL_577600_CONTRACT_20261013.mdとexe/T013_POST_ACTION_SKILL_577600_20261013.txt、T012_ACTION_FRAME_RESET_SPATIAL_POSTSELECT_ORDER_20261014.mdを再利用。577600の返ALをcaller成功値へコピーしてはならず、後続571A40/条件56BA80は別処理。通常枝は44D070照合→special使用回数5799D0→候補再構築576450→必要なら579BA0属性filter→候補count→選択/rearm。これを省略して操作枝を解除しない。


- 保存zipのdecomp_0044xxxx.c 44D070はunsigned整数keyのtree完全一致検索で、見つからなければsentinelを返す。577600のcaller key/map入力は疑似Cで失われており未確定。decomp_0057xxxx.c 576450は候補listをclearしてsource範囲から再構築、577600中の呼出後の18654が技能切替可否に影響する。内部list形状は新設計可能だが候補順/内容は保持が必要。


- REA MCP binary_sessionは成功、server rea-agents6.5.0。open=false、Ghidra provider not_configured: GHIDRA_INSTALL_DIR未設定、analyzeHeadless/native decompiler未検出。これは接続不能や安全拒否ではなくprovider設定不足。現在のREAによる新規native解析はBLOCKED、保存Ghidra資料は使用可能。設定変更/新規install/原本読取/拒否範囲再試行は実施していない。


- 次P0: 577697の44D070 callerについてkey/mapの保存assemblyを限定検索、なければ既存Ghidraの場所と版を確認しREA provider接続を修復する。576450/579BA0は既存B2356-02/B0718-02契約を再利用してsemantic candidate listへ接続。新規原本解析はこの不足だけ。現在G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。戦闘完走/GUI攻撃未達。


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。停止VA577697: caller key/map、576450/579BA0候補再構築・filter、後続571A40/56BA80未完。REA provider設定不足は独立BLOCKED。既存A依頼OPEN/安全拒否BLOCKED維持。別チャット送信なし。








## WORK-REA-GHIDRA-CONFIG-20261016


- ユーザーがREA専用設定追加を明示承認。既存 C:/Tools/ghidra_12.1.4_PUBLIC のapplication.properties(version12.1.4/java.min21)とanalyzeHeadless.bat存在を確認。


- [USER_HOME]/.codex/config.tomlのmcp_servers.rea.envへGHIDRA_INSTALL_DIRのみ追加。TOML解析で他設定の意味が不変と照合、読戻しSHA256=96cc198cefe6358e2c90dc319002423ed2e2d088bf0e309eb445ffa0846c8094。旧設定バックアップ=_work/rea_config_before_ghidra_20261016.toml（設定情報を含むためチャットへ全文出力しない）。新規install/原本変更/他AI source変更なし。


- 変更後REA binary_sessionでサーバー起動時刻2026-10-15T18:02:08.492Zのまま、Ghidra not_configuredを再確認。設定保存成功と稼働反映を区別。REA接続またはCodexアプリ再起動が必要。再起動/プロセスkillは未実施。


- 次回: binary_sessionでGhidra availableを確認してから、既存保存資料にない577697 callerの検索key/map入力だけをREA/Ghidraで確認。577600/576450/579BA0既存契約を再利用して操作側技能後処理へ接続。安全拒否範囲の再取得はしない。


- 製品変更/テスト/buildなし。最新製品はouter-return版496PASS、EXE SHA9a0507a003419b1e0afd0f6c1e147d8c69b86c4ab02a96f3c099e90017419a7b。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。REA provider修復=設定保存済、再接続待ちBLOCKED。停止577697/後続候補再構築。追加チャット送信なし。








## WORK-SWORD-SYMBOLIC-SLOW-20261016


- 前turnはREA設定保存でPROGRESS。REA binary_session再確認では同じ旧サーバー起動時刻/未設定状態、再接続はまだ。設定待ちだけで止めず保存証拠で独立DAT処理を接続。


- battle_runtime.pyのresume_resolved_sword_postでslow_per=on/offを受入。保存generic parser50536A/505381..5053C3の非数値cache0、Ghidra decomp_0059xxxx.c:9201の初期zero判定と9555..9565(sword59CC3B)の最終補正を結合。最終倍率は両者1.0、前段のon=-1/off=1をそのまま使わない。slow_time symbolic/式/@/listは未解明のまま拒否維持。元DATやClaude source非編集、FPU全体profile変更なし。


- TEST: 既存境界testを拡張、変更前ERROR1（未対応拒否）→変更後runtime/skills44PASS/FAIL0/ERROR0、56.995秒、PID11104 exit0。HP/MP/EXP/RNG不変と既存数字80/0/待機overflowも確認。_work/sword_symbolic_slow_verification.json。DAT_DERIVED+SYNTHETICで原作実機比較なし。全suite/新EXE build/GUIは今回未実施、EXEは前outer-return版のまま。以前496/581と合算しない。


- G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。次P0はREA再接続確認→577697の検索key/map不足確認→操作側候補再構築/切替、続いてmotion/弾更新の同一tick統合。再接続前は保存資料を利用し拒否範囲を迂回しない。


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。停止577697、候補list/切替/同一tick未完。REA再接続待ちBLOCKED、既存A依頼OPEN維持。参照=固定handoff同checkpoint/_work/sword_symbolic_slow_verification.json。








## WORK-REA-577600-RUNNING-20261016


- 前turnはslow_per接続44PASSでPROGRESS。今回はREA MCP再接続に依存しない同じ既存REA CLIのスキーマを確認し、実行プロセスだけGHIDRA_INSTALL_DIRを渡してGhidra解析を開始。安全拒否の再試行/別ツール迂回ではなくprovider未設定の解消。永続設定追加変更/新規install/原本変更なし。


- 実行中Desktop Commander Local handle PID9076。node rea.mjs function [USER_HOME]/Documents/迫真戦記/_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe 0x577600 --provider ghidra --format json。出力=_work/rea_577600_function_20261016.json（PowerShellリダイレクトのためUTF16の可能性あり）。スキーマ照会8476/17496はterminal終了。


- 最終poll時PID9076は未終了、出力なし。Java4504のCPU178.53→229.91秒増加を確認。結果未取得であり関数解析成功とは扱わない。自動解析の進行待ち。原作EXEを起動しているのではない。


- 次回最初にread_process_output(pid=9076)をpollする。観測timeoutで再起動しない。handle消失ならprocess/output状態を確認してから判断。途中ファイルを完成証拠として読まない。terminal時のみJSONのidentity/limitations/577697の検索keyとmap入力を確認して、既存577600/576450/579BA0契約から操作側実装へ戻る。


- 保存契約579BA0ではsword/bow/magic/summonは分類可能だがcare/powerupの415460照合は旧拒否境界を保持。元list順をset/sortに変えない。新規製品変更/test/buildなし。最新44PASS、EXEは前outer-return版。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。目標ACTIVE、今回末尾はverified wait。


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。停止577697のREA取得実行中PID9076、再起動禁止、terminal確認後統合。








## WORK-REA-RECOVERY-CONTROLLED-KEY-20261018


- Local直結MCPで固定handoff/WRQを読取成功。以前Compact tunnelのtimeoutは現在のLocal読取には再現せず。旧PID9076 session消失、Java processなし。保存REA JSONは完成したエラー応答でprovider_timeout/330000ms/Ghidra startup deadline elapsed。SHA256=30c3336bf696fd9545b76c3567e435d4d234f041a152ac7abfb88b663caed5fa。解析成功/実行継続中とは扱わない。同じ全体解析再実行0。


- 現REA MCP6.5.0起動2026-10-18T04:41:15.052Z、Ghidra12.1.4/Java21 availableをbinary_sessionで確認。旧not_configuredは解消。新target未open、新しい全体Ghidra解析なし。


- STATIC限定read-only: 原本と同SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187の既存rea_lab/targets/hakushin067_Vahren.exeをpefile/Capstoneで577600..577686および577680..5776B8のみ確認。timeout後の限定調査であり安全拒否範囲の再試行なし。範囲SHAは824f62d6bb9fd7635f6b43f520991012d013b2b08cbb8bf2654278b105c3aaa2と34b3a3984f324663e1d6184386c5b46c9c7e05d563185428ce8cad1496d67eaa。


- 確定: prolog push ecx/ebx/ebp/esi/edi後の[esp+1C]は第2引数Skill pointer。577623 mov ebx,[esp+1C]、577686 mov esi,[ebx+40]。577697 lea ecx,[ebp+1865C]、57769D lea ebx,[esp+1C]、5776A1 lea eax,[esp+18]、5776A5 call44D070、5776AA mov eax,[eax]、5776AC cmp eax,[ebp+18660]、5776B2 je577706。従って既保存44D070 unsigned pointer-key完全一致契約への入力はUnit+1865C mapとSkill引数pointer。旧B要約の『577697 call』は準備位置で実callは5776A5。map producer/技能所有集合の生成は未接続、意味上の集合lookupへ実装可能だが未確認集合を捏造しない。


- 最新B HANDOFF末尾を参照: B-20261018-1328-01 a0054直接2技能宣言等はSOURCE限定READY、合法取得/共有cooldownはVERIFY。この成果を577600 map producer確定とは扱わない。B安全拒否0911/1110等は維持、他所有資料非編集。HEAD be45dc2d563dcc1885a3caf4e3c8af43f6b8619b、既存dirty維持。


- 今回製品変更/テスト/build/実機なし。最新製品検証44PASS、EXEはouter-return版のまま。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Gameplay Golden0/strict MATCH0。


- 次P0: battle_runtime.py resume_resolved_sword_outer_actionのcontrolled枝へ、実効技能所有集合lookup・候補再構築576450・必要579BA0 filterを接続。後続571A40/条件56BA80を飛ばさない。保存済native_unit_aiとB契約を再利用し、map producer/候補入力の未確定だけ照合する。motion/弾同一tick統合へ続く。


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。検索入力STATIC確定、実効所有集合producer/候補再構築/後続未接続。REA設定BLOCKED解消、旧解析TIMEOUT終了。研究B新SOURCE成果は接続仕様と区別。








## WORK-SKILL-LIFECYCLE-POST-UI-20261018


- 577600統合前に検索集合と候補sourceの生成/削除を照合。既保存Ghidra decomp_0057xxxx.c FUN_574E30はsource vector18640..18644から最初の一致を除去、候補list18650/654から一致全件除去、579AA0/510850で1865C集合から除去。static疑似Cのみ、原作実機ではない。


- 限定STATIC x86 574D70..574E30（同原本SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187、範囲SHA174ee756b101bb9349d1095bea29caebfed74d66d40ad10d97885c4943706f02）。574D7F lea ebx,[Unit+1865C]→565780 node payload=Skill引数→5158E0登録が両順序枝に先行。第3引数非0は18640 vector先頭側insertとcandidate先頭insert、0は末尾側append。node生成565780保存疑似Cはpayload+0C=Skill。集合と順序付き候補を区別し、重複を集合で消さない。DAT生成での574D70呼出順/第3引数は未照合、definition.skillsだけを無条件同一視しない。


- 保存Ghidra FUN_576450/5764A0は候補clear後source rangeを先頭から順にcopy。乱数/MP callはその保存局所にはない。既B契約再利用で新解析件数に重複加算しない。


- 保存Ghidra FUN_56BA80は表示有効global gate、選択Troop/Unitの1F9走査、DrawEdgeと操作panel virtual calls/56BE50/453C20等。新設計ではpanel refresh通知に置換する候補。全calleeの作用を今回確定したとはしないため『ゲーム副作用なし』やcontrolled return完成とはまだしない。元GUIコンテナ/Win32 GDIの逐語復元を完成条件に戻さない。


- 製品ソース/テスト/build変更なし。意図したcontrolled統合は入力生成の不足が判明したため未実装。既存44PASSは過去結果で今回再実行0。G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達、Golden0/MATCH0。


- 次は既存保存コードの574D70 callerでDAT実効Skill列→順序付きsource/検索集合の対応を限定照合し、battle_runtime.pyのcontrolled continuationへ直接つなぐ。元heap/list ABIを新実装の入力要件にしない。56BA80は新GUI更新境界として切り分け、callee未知を記録する。


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。停止は577600 caller lookup入力から、574D70 callerのSkill生成順とcontrolled postの候補選択へ前進。56BA80表示層境界を候補化、未完をCLOSEDにしない。参照=同checkpoint。





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


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。停止=571B70前段の解決済みUnit技能列供給/577600 controlled切替。初期化APIと所有判定は実装済、関連48PASS。参照=固定handoff同checkpoint/監査JSON。CLOSEDへ変更しない。








## WORK-AUTO-LEADER-SKILL-CHOICES-20261018


- RuntimeRoster.bind_effect_sessionで通常self-leading Unitの実DAT def技能列を自動でinitialize_skill_choicesへ接続。明示的なinitialize_unit_skills=Falseはcaller解決待ちとしてunit_skill_gapsへ。neutral_78/roam_spot/別leaderは既定の自己def列で代用せずleader/member augmentation VERIFY。gapがあるUnitのroot sword開始は効果/MP/RNG commit前に拒否。解決済み列を明示初期化すればgapを解除する。


- 保存Ghidra571B70 L1963..1967: DWORD+134とWORD+138を0化するため、既存初期化APIも134..139の全6bitを生成結果へ設定。正bitのみだった前checkpointの制限をここで解消。130chargeはsemantic tag保存、旧pointerを要求しない。未解決1A4/+26D、操作flag1F8等は補完しない。


- 限定x86 read-only 5734BE..573527、同原本SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187、範囲SHA9e6339835c8a07c3b1dcdc10de04b2b1ec46c3beca56394ff530d42be6bd9fa4。5734BE ECX=Unit1C8→+EC→42E8E0でdef列copy、5734E5/EF def78/94 gate、573507..517別leader比較。保存疑似Cの5736AB以降はneutral/roam時member補正、それ以外の通常selfleaderは両augmentationをskip。配下/中立の未実装範囲をselfleaderで成功扱いしない。


- 追加read-only既存Ghidra: constructorはUnit18638/1863CにAAFBB8を設定。56B650保存疑似CはAAFBB8+40(AAFBF8)=8。選択なしは通常DAT技能/nullではなく組込みkind8。attr/+120/+4C等は未確定、577600の普通技能集合lookupを一律適用しない。新規原本取得なし（このkind8照合は保存zipのみ）。


- TEST: 新規2件RED=未実装keyword TypeError2→実装。runtime/skills/actions関連3module79PASS/FAIL0/ERROR0、189.000秒、PID42540 exit0(runtime193.06秒)。実DAT yaju/kmr通常leader初期化、charge/6capabilitybits、配下gapと攻撃前拒否、既存発動・回復・効果・action schedulerを回帰。DAT_DERIVED+SYNTHETIC、旧EXE比較ではない。全suite/広域は未実施、既知sourcebook2FAIL未解消。


- BUILD: PyInstaller exit0/108.0秒、CLI --help exit0、EXE SHA33d1fceacc4203b5373230420f23d15166e23800ab22df06a1ffe4a0d01ac2d6。_work/unit_skill_choices_build.log/verification.json（実名unit_skill_choices_build_verification.json）。source/test4file SHA前後一致。GUI/EXE内の戦闘実行は未実施。GUI mainはまだeffect_sessionを自動bindしないので、これはコアAPI初期化の接続でありGUI攻撃完成ではない。


- G1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。Golden0/MATCH0。原本/Claude/A-Eソース非編集。今回Work変更=src/hakushin_compat/battle_runtime.py、tests/test_battle_runtime.py。前checkpointのruntime_skills/helperもbuildへ収録。


- 次P0: 組込みkind8選択の意味(+120/+4C/属性)を保存証拠から限定照合→semantic selected/previous state→577600候補再構築/切替→UI更新通知。部隊配下の技能付与は既存583F40/5842F0/5882F0成果を確認して実装。kind8をnullや通常root技能に置換しない。motion/弾同一tick、GUI入力、戦闘完走は引続き未接続。


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。通常leader技能初期化接続済。停止=組込みkind8選択状態/577600 controlled切替、配下技能付与、同一tick/GUI。79PASSとbuildは限定成果、CLOSEDにしない。








## WORK-REA-BUILTIN-SELECTION-XREF-WAIT-20261018


- Local接続復旧をread_file/start_processで実確認。HEAD be45dc2d563dcc1885a3caf4e3c8af43f6b8619b、status54件。既存dirty/他担当source非編集。


- 保存GhidraのAAFBB8参照を再利用。577600のcontrolled切替はkind8属性長/+4Cの確定待ちで維持。通常選択の初期値を推測してreturn扱いにしない。


- REA open_binary(ghidra)成功、対象rea_lab/targets/hakushin067_Vahren.exe SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。xrefs(0x00AAFBB8)はMCP300秒応答timeout。安全拒否ではない。Java PID22424 StartTime2026-10-18 14:12:23、14:17:25確認時CPU349.109375/Responding=True。再起動・重複要求なし。binary_sessionはbinding Ghidra12.1.4、analysis_activity=not_observed/providers=[]で終了証拠にならない。次回まずPID22424とprovider状態を確認し、timeoutのみで再解析開始しない。


- source追加修正/新テスト/buildなし。前回79PASSとEXE build記録を再実行成功とは扱わない。Golden0/MATCH0、G5/G7/G8未達のまま。


- 独立確認: battle_runtime.py子技能provenanceの複数箇所がdefinition.skills.skillsを使用。前回追加した解決済みUnit技能集合との接続に注意。発射済み子が技能変更後も継続するかを無視した単純置換は禁止。後続実装時にcast時の根技能認可を保持する設計を検討（仕様未確定、今回コード変更なし）。


- WRQ-20261014-CLAUDE-YAJU-ATTACKはPARTIAL維持。次P0=通常選択オブジェクトの初期化元確認→577600 controlled continuation、UI通知。新しい依頼の他チャット送信なし。





- 同checkpoint終了確認追記: LocalPID43572 exit0がPID22424=MISSINGを返した。Java解析プロセスは終了済み、xref結果未取得。WAIT_UNCONFIRMED_TERMINALをTERMINAL_NO_RESULTへ訂正。自動再起動なし。次回は既存保存証拠・独立工程を優先する。








## WORK-STANDARD-SELECTION-RESTORE-20261018


- 前turnのREA xrefsは300秒MCP timeout後JavaPID22424終了確認済。同要求の再起動なし。Localで同SHA原本解析copyのAAFBB8 literal参照位置だけ検索し、未拒否startup 603A70/608630各32byteを限定読取。603A70 pushAAFBB8→599600 ctor、608630→467A40 destructor。603A70範囲SHA6f0cc09a81e08c9082e480a0795fcfa15c2e9c16df8354ec78709c7b6a6abf1e、608630範囲SHA6ae666637e9b677f8ebe06ac6d3af78abd2061f3ac2a0bf20da6214ca068b505。対象SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。


- 保存Ghidra599600でattr110空/120=0、末尾599900でspecial4C=0。56B650の限定命令照合で56B83CがAAFBB8+40=8を設定、402800の属性書込先はAB1138/AADE38/AB1B68/AB2598/AAF288/AB2FB8/AAE868/AB0718でありAAFCC8ではない。56B650..56BA80範囲SHA4a8be4b0a8453aa78c7ec941e4dd0b6a9b79b3395e5b12082d1c6db422917290。通常選択はkind8/空属性/special0として確定（STATIC、実機観測なし）。


- 実装src/hakushin_compat/battle_runtime.py: bind_effect_sessionが既存の明示値を保存しつつ18638/1863Cを通常選択tokenで初期化。旧pointer literalは互換adapter内tokenであり新heapのaddress入力要件ではない。resume_resolved_sword_standard_selectionをcontrolled continuationへ追加。通常→通常のみ、所有技能source全順序をcandidateへ復元。emptyは577600 AL0、それ以外AL1。どちらもcallerがALを無視し571A40→56BA80へ進むためVERIFY_SWORD_OUTER_UIで保持。HP/MP/EXP/RNG/timer再実行なし、二重再開拒否、未完castのtick停止維持。他の選択/過去選択値・配下skillgapは拒否。


- TEST tests/test_battle_runtime.py新規2件: 未実装でERROR2（18638/1863Cなし、45.817秒PID42424 exit1）→runtime/skills/actions 3module81PASS/FAIL0/ERROR0、178.399秒、PID42080 exit0(runtime182.55秒)。DAT_DERIVED+SYNTHETIC。全suite/広域/EXE再build/GUI実行は今回未実施。前EXEはこの差分未収録。既知sourcebook2FAIL未解消、Golden0/MATCH0。


- 次P0: 56BA80/56BE50の表示用技能一覧再構築を新UI状態通知へ置換し、操作側の行動returnへ接続。保存56BA80は選択部隊・Unit1F9に応じpanel表示/DrawEdge、56BE50は577EE0を呼び表示可能技能を収集・描画。577EE0はsource18640からspecial使用回数/現在選択/summon容量で返却vectorを構成。56F130は一時tree処理。表示更新を無条件no-opと断言せず必要なUI状態契約を作る。原GDI/container/heap一致は目標でない。


- 完成ゲートG1/G2/G3/G4/G6 PARTIAL、G5/G7/G8未達。WRQ-20261014-CLAUDE-YAJU-ATTACK PARTIAL、停止VA56BA80（通常→通常限定577600復元接続）。他ownerソース/原本非編集、禁止Git操作なし。








## WORK-CONTROLLED-RETURN-UI-20261018


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。通常→通常post復帰と新UI更新通知を接続、93PASS、新EXEと停止GUI2frames確認。残るGUI攻撃受付/初期化・特殊選択・AI・戦闘完走は未達。詳細は固定handoff同checkpoint。拒否範囲維持、CLOSEDにしない。








## WORK-RUNTIME-DAMAGE-BINDINGS-20261018


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。実contextと通常Unit命中handler/実耐性を自動接続、103PASS・新EXE build/help成功。残る技能受付/初期context/方向/弾初期化/AIは未完。詳細は固定handoff同checkpoint。B1418-01 SOURCE成果確認、今回経路と別範囲、CLOSED化なし。








## WORK-RUNTIME-ROOT-DAT-20261018


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。root rush/damageを実DATから取得、呼出側不一致をcommit前拒否。関連105PASS、新EXE build/help成功。GUI攻撃/初期context/AI/戦闘完走は未達。固定handoff同checkpoint参照。Golden0/MATCH0、依頼CLOSED化なし。








## WORK-OBSERVED-MISSILE-CONTEXT-20261018


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。保存ACTUAL弾記録でD/E=1/1とother=selfを確認。命中contextから参照有無を導出し発射前に矛盾拒否、関連88PASS。root初期context/GUI攻撃等は未完、今回EXE未build。固定handoff同checkpoint参照。Golden0/MATCH0。








## WORK-SEMANTIC-SWORD-AIM-20261018


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。公開Unit位置→semantic方向/角度→root/連撃への捕捉角継承を接続。関連93PASS＋拡張1件PASS（重複あり）、原作保存27例のdirection不一致0。新EXE build/help成功、GUI実行なし。厳密数値一致/戦闘完走未達。詳細は固定handoff。





### 同依頼の追加観測要望（Claude／P0／OPEN）


- 親ID WRQ-20261014-CLAUDE-YAJU-ATTACK、停止点=通常攻撃R3直前のUnit+0x7C context初期値（57E7A5..57E7BAの意味）。拒否済57E650/580280本体の再取得・代理解析依頼ではない。


- 既存許可のread-only観測で、Claude所有peer_script01_live_observer.unit_recordが既に読んだblob[0x7C:0x8C]をhexとして記録に残せるようにする。読取範囲を増やす必要はない。WorkはClaude所有ソースを変更しない。新たな安全拒否があれば迂回せずBLOCKEDとする。


- 次回原作マップテストで一回以上の攻撃直前〜直後を記録。Unit ptr/tag、skill130/1E4A0、target1E570、stamp前後/torn、HP/MP、16byte contextを対応づける。C/D/E各flagとsource/other/skill参照を弾の値と区別する。可能なら発動前/初回/二回目の変化を報告。観測後の値を命令実行直前の初期値と断定しない。


- 参照=固定handoff WORK-OBSERVED-MISSILE-CONTEXT-20261018 と WORK-SEMANTIC-SWORD-AIM-20261018、Claude findings§80/81、既存capture02。納品はClaude所有findingsと既存観測summaryへ。Workが統合するまで親依頼PARTIAL、Golden/MATCHは比較未完のまま。








## WORK-SEMANTIC-SWORD-SLIDE-20261019


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。発動時位置・解決済み半径・実DATからR6往復経路へ接続。131PASS、build/help成功、GUI未実行、Golden0/MATCH0。未解決半径と初期context/pair/GUI/AIは残存。固定handoff同checkpoint参照。





### 思考レベル運用・難解析の集約（ユーザー指定2026-10-19）


- 通常の実装・統合・関連テスト・既存証拠照合はAstra mediumで継続。モデル変更は未実施。Sol highとの同一課題利用量比較は未測定で、節約できるとは断定しない。


- 既存親ID WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P1 / OPEN（high候補・今は後回し）: 停止範囲=579290幾何→既存57948A..5795CE補間の数値境界。不足=元runtime FPU条件と同じ初期半径・標的位置の観測。影響=整数点が変わる場合の命中/移動/RNG分岐。参照=Claude80.3/81.7、battle_runtime_geometry.py、native_unit_movement.py、既存sword_lunge_path_analysis.json。終了条件=ゲーム結果に影響する境界の比較と採用数値profileの根拠。旧logのcap fitだけを仕様化しない。


- highへ切替を提案する時点: 既存証拠と反例を揃えても演算順/丸め/処理順の矛盾が残り、直近の一戦完走の統合を止めた時。対象・入力・候補・判定テストをまとめてから知らせる。現段階ではmediumで独立接続可能なため切替不要。


- root Unit+7C未記録はClaude追加観測OPEN、580280等安全拒否は既存BLOCKED。これらは思考レベルを上げても解消しない証拠/権限制約でありhigh解析バッチへ代理取得として混ぜない。半径未解決もまず既存初期化契約の接続で扱う。








## WORK-INITIAL-UNIT-GEOMETRY-20261019


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。解決済み初期矩形から実DAT半径とlive命中矩形を生成時に接続。88PASS＋既存拡張1PASS、EXE再buildなし。停止=初期矩形の素材由来生成/root context/pair/GUI。新着研究の横断照合を次に実施。詳細は固定handoff。








## WORK-RESEARCH-INTAKE-20261019





- ユーザーの研究資料活用確認を受け、A/B/C/D HANDOFF末尾、E cp187、Claude findings末尾、REA古いPROGRESSだけでなく新しいQC/復旧監査を横断読取。A末尾20261014-0302、C20261016-0122、D20261016-0137、B新着20261019-0117、REA2340/0034を確認。最新成果すべての統合完了とは主張しない。


- 重要な未統合証拠: B0117のcaller分類から既存exe/T012_DAMAGE_CALLER_CONTEXTS.txtを直接照合。UTF16 BOMの保存テキスト。VA57E7A5 lea context=Unit+7C、57E7A8 source=Unit、57E7AA context+8=Skill、57E7AD other=0、57E7B4 WORD+C=0x100(C0/D1)、57E7BA BYTE+E=1。context+Fの書込はこの窓にない。これまでroot context全体を観測待ちとしていたのは拾い上げ不足。次はこの15byteの既存確定書込をroot adapterへ接続し、+Fのconsumer有無を既存モデルで確認。新規拒否済57E650本体取得はしていない。


- B0117の正式READYマーカー保存は安全拒否でBLOCKED/NOT READY。Workはその正式状態を昇格・代理保存しない。今回の実装判断の出所はWorkが直接読んだ既存caller命令であり、B正式台帳を修正しない。


- REA 20261018-21H/2340 QC: 527ED0選択解除prefixはWorkと整合。527F27以後UI帰還、5685FD mode2判定→4C22B0(delete0)→56861A→死亡側575F71/575F91復帰が未接続候補。PROGRESS/QUEUEのEPERMによる古い表示だけを最新状態とみなさない。REA0034 preflight拒否は維持し、代理再実行しない。


- Aはイベントclock/区切り文法、CはWorld入口変数と子event、Dは旧DirectMusic初期化/終了ABIが最新末尾。現在の攻撃入口を直接解除する資料ではなく、物語接続/音声参照として保持。新エンジンの内部実装を旧COM ABIへ戻さない。


- 次の優先度を変更: root contextの既存確定書込の実装接続→死亡/選択解除の復帰不足→初期描画矩形の素材由来接続。新規広範解析より保存済み未統合契約を優先。追加観測要望はparent PARTIAL維持、root書込15byteはSTATICで解決し、観測はruntime比較用途へ縮小。今回の横断照合による新テスト/buildなし、直前88PASS+既存拡張1PASSを流用計数しない。Golden0/MATCH0。








## WORK-ROOT-CONTEXT-INITIALIZER-20261019


WRQ-20261014-CLAUDE-YAJU-ATTACK / Work / P0 / PARTIAL。root初期命中情報先頭15byteの構築を接続、95PASS＋同一拡張1PASS、build/help成功。Claude追加観測は比較用途OPENで実装待ち理由から外す。B正式拒否状態は変更なし。次WRQ-20261013-REA-DEATHはPARTIAL、527F27 UI後→5685FD→親死亡returnの接続へ。詳細=固定handoff同checkpoint。








## WORK-TROOP-SELECTION-RETURN-20261019


WRQ-20261013-REA-DEATH / Work / P0 / PARTIAL。527F27表示tailを新UI revisionへ置換し568538/56861Aへ復帰、mode2 Task解除接続。停止=親575F71/575F91と前段graph、残UI枝/複数binding。24PASS＋実DAT4PASS、関連3module340PASS/FAIL0/ERROR0（最終runner差分は別4件、重複あり）、新EXE build/help成功。詳細=固定handoff同checkpoint。REA Java環境障害は記録、追加の広範解析依頼なし。








## WORK-TROOP-LIVE-UI-RETURN-20261019


WRQ-20261013-REA-DEATH / Work / P0 / PARTIAL。56853B/527EA0のUI帰還と完了後selection再呼出しを接続。関連35PASS＋最終周辺27PASS（重複）、EXE build/help成功。次停止=575DF0前段graphと575F71/575F91の2call識別/1867D再読。独立部隊更新を死亡完了としない。固定handoff同checkpoint参照。





## WORK-DEATH-EMBEDDED-WINDOWS-20261019


WRQ-20261013-REA-DEATH / Work / P0 / PARTIAL。埋込window3個の解除を接続、98PASS、新EXE build/help成功。停止575F15、残=子効果detach→2Troop call/1867D再読→親死亡/結果判定。参照=固定handoff同checkpoint・既存REA ND-GRAPH。


ユーザー協力（同依頼の観測準備）: OPEN / 担当Work / 優先P1。1体の死亡前後の短時間記録について試験条件と手順を準備する。今はユーザーへ実行を依頼していない。追加導入・大量記録不要。ACTUAL未収集。





## WORK-DEATH-GRAPH-RETURN-20261019


WRQ-20261013-REA-DEATH / Work / P0 / PARTIAL。停止575F15から子解除/2Troop call/選択再読/本体解除を575D0Dまで接続、最終353PASS、新EXE build/help成功。未完=致死5785A3前段と5789F2以後caller、active子/marker/sparse、GUI/host生成/勝敗接続。参照=固定handoff同checkpoint、REA ND-LETHAL/ND-DETACH/ND-GRAPH-TAIL/ND-PARENT-RETURN。CLOSEDにしない。次はGUI load_runtime_deployment→既存bind_effect_sessionと実攻撃/致死入口を優先し、新たな広範解析依頼なし。ユーザー死亡観測準備OPEN（今は操作不要）、high候補既存のみ。





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





## WRQ-20261019-CLAUDE-JOINT-INIT


- 担当: Claude（既存観測/所有findings）、Work（統合・必要な試験条件準備）。優先P0、状態OPEN。親WRQ-20261014-CLAUDE-YAJU-ATTACKはPARTIAL。


- 停止: Rush 0x55037F後→joi生成→初回54BA00。580280本体の新取得は依頼しない。生成済みjoi→joi2→3弾→HP/EXP更新はWorkで接続済み、再解析不要。


- 必要な結論: (1) Rush出力角度とjoi初期角度との差、start_random_degree=8がこの経路で適用されるか (2) 生成1回の追加乱数消費を証明できるか (3) joi/joi2/js系の初期counter・速度・サイズ・位置・子の角度継承 (4) sound=defenseの開始時刻と乱数消費。角度一致だけで乱数0回と断定しない。


- 参照: docs/PEER_SCRIPT01_FINDINGS_20261011.md §80/81.7、_work/claude_live_obs_karate_02.jsonl とsummary、data/T011_KARATE_JOINT_ANGLE_TIMING_20261014.md、Work固定handoff WORK-STATIONARY-JOINT-CHAIN/WORK-LINEAR-DAT-IMPACT、src/hakushin_compat/native_rush_missile.py。既存観測unit_mtを田所のdamage/EXPとして扱わない。


- 手順: まず既存ログ/保存証拠の不足列だけ照合。分からない場合は不足列を列挙し、既に許可されたread-only観測で取得可能か確認。拒否操作の代替取得・注入・ゲーム内値書換えはしない。新観測が必要ならWorkが実行条件/記録時間を準備してユーザーへ依頼する。既存量で決まらないことを大量記録で解消したとしない。


- 比較候補: 許可された試験用DATコピーで同じ攻撃者/標的/距離を用い、start_random_degreeだけ8と0に分けた短い観測。これは未実施の設計候補、原本書換え/観測成功/同seed保証を意味しない。RNG内部状態を読めない場合は分布/角度だけのACTUALとして限定する。


- 納品: Claude所有の既存findingsへ値/根拠/未確定/観測条件/ログhashを記録。Work-owned queueは編集しない。STATIC/ACTUAL/SYNTHETICを分離、Golden/MATCH0維持。依頼はPC保存のみ、別チャットへ未送信。





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


ID WRQ-20261019-WORK-FACTION-CONTROL / Work / P0 / PARTIAL。停止57F620/57F7BBのUnit1F8入力。未完=player faction/leader/troop controlとbeast gateのbinding。保存btl_semiauto/@mode_auto同定済み、放浪枝は分離。参照=固定handoff同checkpoint、exe/T013_UNIT_1C8_1D4_PROBE.txt、T013_UNIT_STRING_BAND.txt、保存Ghidra571B70/49D030、Claude NativeDefinition.byte_74。既存観測にUnitflagsなし。現時点ユーザー操作不要、必要時に短時間観測を準備。Claude observerは未編集。624DD0/624DE4承認待ち、JOINT-INIT OPEN/REA-DEATH PARTIAL維持。





## WORK-FACTION-CONTROL-BINDING-20261019


WRQ-20261019-WORK-FACTION-CONTROL / Work / P0 / PARTIAL。共有StrategyWorld→live Unit操作flags→normal回復MP gateまで実装、127PASS。未完=通常初期化からworld/actor_powers/troop_controlled/autonomous_units/攻撃spot供給、GUI入力切替。現GUIは自動呼出なし。固定handoff同checkpoint参照。624DD0/624DE4承認待ち・未再試行、JOINT-INIT OPEN/REA-DEATH PARTIAL維持。





## WORK-DEPLOYMENT-CONTROL-STARTUP-20261019


WRQ-20261019-WORK-FACTION-CONTROL / Work / P0 / PARTIAL。明示配置→実DAT勢力tag検証→live flagsをGUI初期化から接続、128PASS、新EXE画面/3Unit状態確認。未完=campaign world引渡し/部隊状態自動生成/UIモード変更。独自試験配置を原作初期編成と混同しない。624DD0/624DE4承認待ち、JOINT-INIT OPEN、REA-DEATH PARTIAL維持。





## WORK-SKILL-ADMISSION-DEPENDENCY-20261019


Work / P0 / BLOCKED（Skill210/214 DAT名取得のみ、goal全体ではない）。624DD0/624DE4各最大32bytes/NUL終端、同Local限定再審査の承認質問を再提示、USER RESPONSE PENDING。未再試行。既存normal admissionと共有cooldownへのbindingが次の具体的実装。B最新0408の座標契約はこの不足を解消せず、旧拒否の解除でもない。製品変更/テストなし、最新128PASSは前turn結果。





## WORK-TUTORIAL-FIELD-IMAGES-20261019


WRQ-20261019-WORK-TUTORIAL-FIELD / Work / P1 / CLOSED（サブフォルダfield画像alias読込漏れの限定修正）。37PASS、新EXE tutorial.map/3Unit表示、未解決画像0、対象622マス。階段smooth/member/altは別VERIFY、ゲーム完走とは別。実Skill210/214限定再審査回答待ち・未再試行を維持。





## WORK-LIVE-PLAYER-MOVEMENT-CONTROL-20261019


WRQ-20261019-WORK-FACTION-CONTROL / Work / P0 / PARTIAL。初期化flagsを実移動/停止命令へ接続、side固定を除去、専用9/関連109PASS。新EXE side反転配置の移動到着確認。未完=UIモードwriter/campaign入力/通常発動。JOINT-INIT OPEN、REA-DEATH PARTIAL、2文字列限定再審査回答待ち・未再試行。追加ユーザー操作不要。固定handoff末尾参照。





## WORK-SWORD-C4-ADMISSION-20261019


Work / P0 / PARTIAL。保存57E650入口のC4 gateをroot発動へ接続、関連112PASS。JOINT-INIT OPEN（成果未追加）、Skill210/214限定再審査未回答・未再試行、REA-DEATH PARTIAL維持。新規追加解析依頼なし。次は既存生成契約の成果確認。





## WORK-LETHAL-INTEGRATION-PLAN-20261019


REA-DEATH既存項目を最新ソースと照合して更新。B0520-01は限定STATIC報告受領、raw/実効mappingは未統合。C4修正EXE build/help成功、新規test/GUIなし。2文字列承認待ち、JOINT-INIT OPEN維持。





## WORK-LETHAL-DISPLAY-MERIT-20261019


WRQ-20261013-REA-DEATH / Work / P0 / PARTIAL。4E1950は保存資料でNumberTextと確認、致死表示要求→功績resumeを実装。関連283PASS、新EXE build/help成功。停止57860C dead/breakが次工程。GUI表示consumer/通常死亡完走は未達。新たな広範解析依頼なし。JOINT-INIT OPEN/Skill210・214承認待ち維持。固定handoff末尾参照。





## WORK-LETHAL-DAT-PRESENTATION-20261019


WRQ-20261013-REA-DEATH / Work / P0 / PARTIAL。dead Unit-only/break Class fallbackを接続、285PASS。空breakの次は578929 corpse。保存4E0610/588FF0でlost_corpse/scream/GM+1EF26Cを確認、次はv24音声とcorpse寿命/カウンタ消去の既存証拠確認。GUI表示/音声consumerは未接続。固定handoff参照。新規広範解析依頼なし、既存拒否/未回答維持。





## WORK-CORPSE-EXISTING-CONTRACT-20261019


WRQ-20261013-REA-DEATH / Work / P0 / PARTIAL。次に求めていたcorpse寿命/カウンタ減算とscream fallback/engine音声gateは既存DEATH-23/26/29/34に保存済み。再解析依頼不要。実装は未着手、非0 lost_corpse数式/通知副作用/実音声設定bindingはVERIFY。前回の次工程メモをこの参照で精密化。





## WORK-CORPSE-LIFETIME-GUN-DELAY-BINDING-20261019


- WRQ-20261013-REA-DEATH / Work / P0 / PARTIAL。空break→corpse登録/寿命更新を接続、295PASS。停止4E081F死亡音。未完=scream/runtime設定/audio gate、588470共有world、afterdeath/disable後event/EXP/outcome、corpse描画/通知consumer。固定handoff同checkpointと既存DEATH-23/26/29/34参照。


- WRQ-20261013-B-SKILL / Work / P0 / PARTIAL。624DD0/624DE4文字列読取はユーザー承認後同Local再審査成功、両方gun_delay。文字列取得サブ課題CLOSED、従来『承認待ち』はこの追記で更新。Skill210/214→DAT adapter→共有gate/postwriterまで統合、122PASS。停止=通常caller/20C wait/外側帰還。解析の再依頼不要、所有者資料は変更0。参照=固定handoff/監査JSON/log同checkpoint・B保存59C1BA..59C253。


- JOINT-INIT OPEN。その他の拒否範囲は維持し『全て許可』を包括的解除に使わない。追加ユーザー操作/他チャット送信/high要求なし。





## WORK-NORMAL-SUPPORT-DAT-GATE-20261019


WRQ-20261013-B-SKILL / Work / P0 / PARTIAL。実DAT gun_delay→通常Unit57F570入口→共有待機値判定をTask継続経路へ接続。正値は57E5F0 recovery、欠落/非正は57F685候補生成前で停止。関連236PASS、新EXE build/help成功。未完=GUI RuntimeRoster共有辞書の自動供給、通常selection/core後段/20C wait/outer帰還。固定handoff同checkpoint参照。REA-DEATH PARTIAL/JOINT-INIT OPEN、旧拒否維持、2文字列取得サブ課題CLOSED。追加ユーザー操作・high依頼なし。








## WRQ-20261019-WORK-HIRE-UI | Work | P0 | PARTIAL


停止VA: 4D4A50/4D79C0/4D8E40（保存候補、hook未確定）。未完=原作eligibility/filter/render/click対応・左chip実描画・UI切替・実機確認。参照=固定handoff WORK-HIRE-UI-DLL-PROTOTYPE-20261019、_work/hire_ui_dll_verification.json。DLL32bitビルド/25checks成功、原作UI未接続。戦闘別EXE往復は直近主線から外し選択肢として保留、旧依頼を完了扱いしない。





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





## Hire sort UI-thread probe plan (Work, 2026-10-19)


Goal: 原作UIthread上でDLLから既存roster/right metadataをread-only取得し、sort接続位置を検証。通常戦闘/並替え完成の代用品ではない。


Files: src/hire_ui_observation.c（hash-gated probe/WH_GETMESSAGE callback）, src/hire_ui_probe_host.c（有限timeout・解除）, existing header/test/build。


- [x] test missing export then wrong-target rejection.


- [x] implement SHA256 identity check, request-only callback, DLL隣の専用log、source/source-save変更なし。


- [x] host posts registered message, verifies reply nonce, always unhooks before unloading; test own process then ACTUAL if available。


- [x] read output log / verify thread identity / save checkpoint。


Review: wrong EXE→reject; stale PID→reject; timeout→unhook; no game rules calls/writes; no DllMain work。Git操作禁止/他担当変更禁止。





## WORK-HIRE-SORT-UI-THREAD-PROBE-20261020


WRQ-20261019-WORK-HIRE-UI / Work / P0 / PARTIAL。DLL UIthread実機読取成功（5所属/17候補）、43checks+self/timeout成功、解除確認。並替え未接続。次=全員一覧の資金/領域込み判定・描画/選択整合。詳細は固定handoff同checkpoint、_work/hire_ui_dll_verification.json。chip対象外。Golden0/MATCH0。





## WORK-HIRE-SORT-ROW-AND-BITMAP-20261020


WRQ-20261019-WORK-HIRE-UI / Work / P0 / PARTIAL。ユーザー確定=原作586080雇用関係を全所属へOR、資金/領地は原作のまま。行metadata/画像copy permutation実装、72checks、実機HDC300x5632x32と所属5/候補17確認。並替え表示未接続。次=辞書read-only lookup→native relation評価→可逆commit。固定handoff同checkpoint参照。





## WORK-HIRE-PRIORITY-CORRECTION-20261020


ユーザー最新訂正: 雇用関係だけではなく、現在実際に雇用可能な人物を先頭にする。資金/領地等を含む原作の可否を使用。直前の関係のみ優先案は採用しない。--sort試験は適用成功応答したがユーザー表示は変化なし。表示成功とは扱わず原因調査。再適用はしない。




## WORK-HIRE-LINK-FIRST-20261020

ユーザー最終指示: まず資金/領地を除外し、ユニットごとの雇用リンクがつながって雇用可能な人物を先頭へ。上の資金/領地込み訂正を当面上書き。現状=relation判定取得済、表示反映不具合を優先修正。sort成功応答のみを機能完成と扱わない。



## WORK-HIRE-LINK-SORT-READBACK-20261020

所属全員の原作586080雇用リンクをORする優先表示。資金/領地は今回の優先条件から除外。chip対象外。辞書read-only lookup・native predicate・行metadata/bitmap同一順序更新を接続。93合成checks成功。実機で所属5/候補17、78calls、優先6人。nonce44847500で即時4配列一致、44848696で後続読取一致。画面を開き直すと原順へ戻る。nonce44973156再適用後も表示未更新だったが、nonce45193105でデータ保持を確認。ユーザーがスクロールするとKBSトリオ先頭になったと確認し、再描画不足を特定。原作EXE/save未変更。Golden0/MATCH0。

## WORK-HIRE-NATIVE-REDRAW-20261020

Work / WRQ-20261019-WORK-HIRE-UI / P0 / PARTIAL。原作453C20の提示処理を接続し、スクロール不要で優先表示に変わることをユーザーが実機確認。根拠: 保存Ghidra疑似CとSHA一致コピーの限定x86読取、4D77B6..4D77C2 callerがECX=window/EBX=0/stack zero3引数、453C20 callee ret12。HkCallNativeHireRedraw追加。TDD: PID31360欠落exportでFAIL→PID25324/13940で97checks PASS。最初の実機試験nonce45864049はhover1000（リセット上）で無変更拒否。外へ移動後nonce45978065でsort0/immediate_rows_verified=true/redraw0、UIhook解除、ユーザー「すぐKBSトリオが先頭になった」。変更=src/hire_ui_extension.c/.h,src/hire_ui_observation.c,tests/hire_ui_dll_test.c。現行DLLビルド成功。元順復帰は原作リセットで確認済み。ただし自動再適用と優先/元順切替は未実装、表示とhover対象の全行照合/雇用操作試験は未実施。次=全員表示のライフサイクル判定と再適用、個別雇用者表示を維持、元順復帰。REAは接続ありだがGhidra providerはJAVA_HOME未設定/java.exe絶対path必須エラーでruntime_unavailable。設定変更せず記録し、既存資料と許可されたLocal解析を使用。全体Python未実施、旧2FAIL未解消。原作EXE/save未変更、Git変更操作なし。他担当ファイル変更なし。Golden0/MATCH0。


## WORK-V4-FOUR-GROUPS-20261021

ユーザーからV4引継ぎを受領し、data/recruit_sort_v4を改修正本として確認。新要件は安定順: 0雇用可能、1雇用リンクあり領地不足、2リンク/領地あり資金不足、3リンクなし。複数雇用者では完全成立を優先し、なければ領地成立の資金不足を採用、誰も領地成立しなければ領地不足。表示グループの順番と複数雇用者の成立度を混同しない。rect_sort_core.hに4分類/雇用者間集約/安定順列を追加。関連条件がunknownなら拒否。新規5組の条件assertと既存10000矩形ケース成功。native relation模擬17人/5雇用者/61calls成功。4段階分類のネイティブ領地/費用入力は未接続: 製品DLLは依然relation-onlyであり4段階完成とは扱わない。原作UI保存4D4A50 L1066-1084には5AC880等の領域集合と資金/価格比較がある。価格はL1012-1046の雇用者依存補正を含むため、全員表示の価格をそのまま各雇用者の価格と推測しない。今後native ABIを確認して入力アダプターへ接続。
V4の再描画を修正: 通常thiscallだけでは不足する453C20のEBX=0を、Workで実測済みのbridgeと同形式で設定。対象window最小確認サイズを1554→1558へ修正。build成功、dist DLL SHA ac840dc8d20243e0d941ba65b30987e72e2f0fc148797f25d19cb42e48e84b7f。ゲームフォルダの配置DLLは今回は未更新、原本/セーブ/他担当は未変更。最新保存V4実機ログはrenderer初回→priority skipped reason=-8 n=17。ユーザーは並び変化ありと報告しており、ログと同一回の観測とは未確認。-8はHkReadNativeEmployers拒否であり、ロード時フック成功と分離して調査する。V4全完成/実雇用/クリック整合は未検証。Work旧105checks版panel/restoreソースはdev_labに残るが実機パネル起動未実施、V4へ混在させない。次P0=roster mode/count/取得時点を診断、原作領地・雇用者別価格/資金の意味/ABI確認、4段階入力接続、V4描画・hover実機試験。上限100件は継続VERIFY。Golden0/MATCH0。


## WORK-V4-NATIVE-CONTRACT-20261021

Progress: STATIC入力契約をreports/native_four_group_contract.jsonに保存（SHA一致原作解析コピーの限定x86、原本未変更）。4D6B3E..6B98: 5AC880(element,1,0) cdecl、始点Spotを集合へ追加しtargetの583CF0結果が集合にあるか確認。領地不足は資金判定より先。4D6BC0..6BE6: signed資金>=price、またはprice<=0で資金通過。4D6781..68B3: 585960 priceに相性/係数/x87丸めを適用、候補+75/+77と雇用者/候補の583A80で追加係数分岐。勢力表示の相性は5878A0(target EDI,power EBX)、人材プレイは5878F0。従って「雇用者別価格」は主に傭兵等の追加条件による差で、勢力モード基本相性は候補対勢力。4D4A50開始保存C: wnd+98→+4 manager、manager+20C powerの+5C資金（人材プレイ条件成立時はmanager+208 def+174）。いずれもnative関数の新実行は行っていない。597BA0は要素不在時にdummyを生成する枝を持つので、単純なread-only関数として無検証呼出ししない。新規REA MCPは現行ツールから削除されており、既存GhidraとLocal限定読取を使用。
実装: native_priority_v4.cにロスターmode/count/decoder_status診断、hakushin_recruit_sort_v4.cの拒否logへ追加。tests/test_priority_win32.cで不正mode0/count5/decoder1と出力無変更を検証。PID24720 exit0: 模擬native判定PASS、DLL build/PE check PASS。DLL SHA bd9d773b7535297928b70897057ae8feb1861722ba0d6452843653c3f5cdcd14。ゲームフォルダ未配置、最新4分類の実機実行なし。四分類コアは前checkpointのテスト済みだがnative領地/費用アダプター未接続。原作保存済ログ-8の具体原因は未確定、タイミング説は仮説であり追加観測/呼出経路確認が必要。次: 取得タイミングの診断、領地/価格の残るABI・副作用を確認して4分類へ接続、実機表示とhover/click整合。ユーザー承認待ちで作業を止めたわけではない。元EXE/DAT/save・他担当は変更なし、Git stage/commit等なし。Golden/MATCH 0。


## WORK-V4-USER-STATUS-20261021

ユーザー補足: V4は未完成だが、並び方が変わる段階まで到達。これをV4の表示変化の報告として保持し、四分類や全行クリック整合の成功とは扱わない。最新ソースは依然relation-only。追加STATIC確認: 597BA0はEDI=Spotを受け、Spot文字列/ctx経由のmanager+504辞書を49E490へ渡す。結果なしの場合AC0990の共有dummyを再利用または生成、597C89はplain ret。native_four_group_contract.jsonへ限定命令と副作用を保存。新しい原作実行・配備・テストは今回なし。既存DLLビルド/模擬試験結果を新規実機結果へ読み替えない。次P0は副作用を避ける既存element取得契約、領地・価格入力アダプター、四分類の本番接続。表示の変化がすでに得られた箇所を初めから作り直さない。


## WORK-V4-EXISTING-ELEMENT-20261021

P0 PARTIAL / 所有V4のみ。native_priority_v4.cにrs4_lookup_existing_elementを実装。SHA一致コピー49E490限定x86と既存4C1200/4682B0によりmanager+1EF0D4のstring->SpotElm辞書を確認。597BA0のdummy生成枝を呼ばず、既存Spotからcontext/manager対応、辞書key、element+ A0のSpot逆参照を検証して取得。欠損は1=VERIFY、破損は-1として出力を変更しない。領地不可とは混同しない。tests/test_priority_win32.cに存在/無変更/欠損/逆参照不正/循環/owner不一致を追加。RED PID17992欠落関数link error→GREEN PID6456 exit0。既存17候補/5雇用者/6優先/61呼出試験もPASS。PID10168: 10000矩形ケースPASS、DLL build/PE check PASS。新DLL SHA da7291b53b51a03b8d2e1ef17fdae18420e30e05241274b5c3df76f0e6b914f6。ゲームフォルダへの配置・実機呼出しなし。新getterは4分類アダプター用で本番分類からはまだ未使用、V4現行分類はrelation-only。原作EXE/DAT/save・他担当は未変更、Git書込操作なし。
次具体位置: native_priority_v4.cのrs4_lookup_existing_elementを使用し、583CF0で対象/雇用者Spotを取得するABI bridgeと5AC880(element,1,0)領地集合取得を接続。5AC880の返却集合はshared scratchで初回alloc/毎回clearがあるため純read-onlyとは呼ばない。saved44D070は集合head+4,node key+0C,nil+11のunsigned pointer比較を確認済み。始点Spotを含める原作呼出側の意味を維持。価格585960/46F4C0/583A80のABI・所有権を確定後4段階へ接続する。全体Python未実施、旧2FAILは未解消、Golden/MATCH0。全完成とは扱わない。


## WORK-V4-TERRITORY-CURRENT-GHIDRA-20261021

ユーザーのGhidra機械解析について確認。これまで旧10/11保存ZIP中心だったが、新しいrea_lab/headless_analysis/search_index/00_START_HERE_ACTIVE_RESEARCH.mdとCURRENT_ACTIVE_RESEARCH_STATE_20261021.jsonを読み、正本をHakushin067_FunctionRepair_20261021.gpr + HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite + search_current.pyに更新。DB SHA282924553309c4778ff6c5d5346ccf5c2bcb1b6fd17e46dbbae9031547453f8d、CLI SHA372fafd6751ef9593a12df7b503723df082deacfb53659f3d6272766d9d16baaをマニフェスト照合済み。新CLI read-onlyで4D4A50呼出8箇所と585960/583CF0を照合。reloadMenuの4A5B28/54は4A1250所属へ修復済み、V4既存8フックと一致。修復擬似C10件/verified ABI3件に限り、全関数のABI確定ではない。以後新規調査は現行DB/CLIを先に参照。旧ZIPは履歴比較用に保持、他担当正本は変更しない。
実装: native_priority_v4.cにrs4_native_territory/583CF0 EAX bridge/44D070相当pointer集合読取を追加。existing element取得→5AC880(element,1,0)→target Spot→集合membershipと始点Spotの和集合という入力経路を接続。5AC880はnative scratch変更/一時allocationあり、純read-onlyとは記載しない。unknown/欠損は出力不変でVERIFY。これはまだ実行adapterでありrs4_priorities本番から未使用。価格接続前に雇用可能として出力しない。
テスト: RED PID464欠落symbol→GREEN PID4424 exit0、呼出順整理後PID7568でもnative模擬試験全PASS、DLLbuild/PEcheckPASS。領地包含/不包含/同地点/集合破損/element欠損/Spot欠損とcdecl引数/EAX引数を模擬確認。DLL SHA3337a7ef85f066470c6c20cd2e19b16d60bf9c12df69f946f3eb890decb3d82b。実原作呼出・ゲームへの配置なし。4段階並替えPARTIAL。次: 現行検索DBから585960/46F4C0/583A80の価格ABI/出力所有権を確認し、本番4分類と価格/資金へ接続、ロスター取得時点診断と実機画面整合。原作/save変更なし、全体Python未実施、Golden/MATCH0。


## WORK-V4-BASE-PRICE-20261021

native_priority_v4.cにrs4_native_base_price/585960 bridgeを追加。現行search_current.pyで585960/4647D0/46F4C0/583A80を先に確認。585960はEDI=def、stack(output,key)、585AC6 ret8。価格返却は36byte ScriptData（vptr+0,string+4,size+14,capacity+18,int+20）。注意: callerのpush後leaを補正するとbufferは旧ESP+1C8であり、capacityをoutput+14と扱ってはいけない。容量16以上のheap文字列を原作delete5B6BBBで一度解放。原作関数のnew/delete所有権をDLL CRTへ渡さない。STATIC契約はnative_four_group_contract.jsonに保存。
TDD RED PID18556欠落symbol→GREEN PID29020 exit0。新3ケース（inline価格、heap価格/native解放、無効引数で出力不変）と既存relation/element/territory模擬ケースすべてPASS。PID17752 DLLbuild/PEcheck成功、SHA7c66776eca9712609fe9c783b0c95b6d84736ddbc213031b6417ab5754a5b952。新たな実機呼出・配置はなし。getterは本番分類にはまだ未使用、V4はrelation-onlyのまま。
残るP0: 5878A0(E DI target/EBX power)相性と46F4C0(ECXkey,stack ctx/default,ret8)係数、583A80(EDI,AL)傭兵判定を呼び、4D67EA..68B1と同じx87順序/64bit一時値/ftol2丸め/32bit積で最終価格を得る。基本価格だけで資金条件を満たすと扱わない。その後領地/資金/複数雇用者の成立度を集約し、本番rs4_prioritiesとhrs_ranked_firstへ接続。所属ロスターmode/取得時点と100件上限は継続VERIFY。原作/DAT/save、他レーン所有は未変更。新全体回帰なし、既知2FAIL未解消、Golden/MATCH0。


## WORK-V4-FINAL-PRICE-20261021

V4 native_priority_v4.cへrs4_price_arithmeticとrs4_native_faction_priceを実装。保存x86 4D67EA..6837/686C..68B1に基づき(100-affinity)*percentを64bit一時保存、係数*percent→base*一時値→fmulp→half加算→元ftol2入口、ADD32bit wrap、追加補正はIMUL32bit後x87という順を使用。FPU制御をDLL独自値に変更しない。最終価格adapterは585960の基本価格と解放→5878A0(EDI target/EBX power)→46F4C0(ECX key/stack ctx,default/ret8)→通常補正→target+75/+77時だけ583A80(EDI,AL)をemployer優先/target次の順に評価→倍率1000/33系の条件補正。元EXE内constant/ftol2をbase相対で利用する構成。勢力プレイ・def行用のみ。人材プレイ/非def行を勝手に同じ扱いにはしない。
TDD: arithmetic RED PID21396→GREEN PID14284、最終価格RED PID28088→GREEN PID26872 exit0。新7計算例（通常/ゼロ差/係数/二段補正/負値丸め/IMUL32bitoverflow/ADD32bitoverflow）、FPUcontrol/TOP維持、無効引数、4本のnative呼出模擬連結（通常、employer特殊、target特殊、両方false）PASS。既存relation/element/territory/property試験もPASS。整数変換はテスト用x87切捨てstubであり元5D1B80実行ではない。原作MATCHとは扱わない。PID13220 DLL build/PEcheck成功、SHA29d8c854f09caab3439876dfbbbe40c0f93a7a613b8c80bdde0c8976a060506e。未配置・実機未実行。
次P0: rs4_prioritiesの共通入力読取を使い、wnd+98→controller+4のmanagerとmanager+20C power+5C資金を検証、個々の雇用者の関係/領地/最終価格を4分類に集約。表示order0,1,2,3と集約優先0>2>1>3を区別。hakushin_recruit_sort_v4.cからhrs_ranked_firstに接続し、1候補でも4条件/複数雇用者/unknownを模擬統合試験。その後ロスター取得時点診断・原作実機。現行描画本番はrelation-onlyのまま、完成ではない。元EXE/save/DAT変更なし。全体Python未実施、旧2FAIL残存、Golden/MATCH0。


## WORK-V4-FOUR-GROUP-STAGED-20261022

ユーザー方針: 一度に複雑な機能を実機へ投入せず、小さな試験を繰り返す。今回V4 native_priority_v4.cの共通入力読取へ四分類モードrs4_four_group_prioritiesを接続。manager/power/fundsを検証し、各候補のリンク→領地→原作最終価格→signed資金比較で分類、複数雇用者は0>2>1>3で集約。非def行/勢力なし/領地unknownは明示拒否で出力不変。既存relation-only入口rs4_prioritiesと描画側は保持し、ゲームへの適用はまだ切替しない。
段階1 RED PID15948 missing symbol→GREEN PID29836 exit0。1候補/1雇用者で4分類、資金同額と1不足、欠損情報/unsupported modeを確認。段階2 PID29188: 2雇用者で最初のリンクあり候補が高額でも次の安価なofferを採用、全員資金不足ならrank2を確認。新8シナリオと既存全native模擬試験PASS。rect_sort_core.hは共有headerの未使用警告をinline化で解消、再コンパイルの10000矩形ケースPASS。DLLbuild/PEcheck PASS、SHA67365f3ae8b15d22ff43f6864f1362f7dccfdc08517b04a0d5dbe25b3abd815f。原作実行/ゲームフォルダ配備なし、Golden/MATCH0。原作/save/DAT・他担当未変更、Git書込操作なし。
次: 段階3として複数候補の4群表示順と矩形/hover対応を検証する。さらに実機はまず判定結果の記録だけを行い、原作画面の各候補と照合してから表示順変更へ進む。最新Ghidra正本/検索CLIは10/21 FunctionRepair/current canonicalを継続。現行rendererはrelation-onlyであるため四分類画面完成とは報告しない。ロスター全所属/hover絞込との区別、表示更新タイミング、100行上限、個人プレイは残るVERIFY。旧全体Python2FAILは未解消。


## WORK-V4-STAGE3-20261022

Work所有V4四分類: PARTIAL。段階3（7候補/安定順序/候補IDと矩形対応/復元）SYNTHETIC_PASS。次P0: 表示変更なしの分類診断→原作画面との照合→表示変更の順で小分けに試験する。診断未実装、他担当への追加解析依頼なし。


## WORK-V4-DIAGNOSTIC-20261022

V4四分類: PARTIAL。Workが診断モードを実装し合成4項目・既存分類・10000矩形試験PASS、loader-only2ケースPASS。次P0は表示を変更しない原作分類の実機照合。ゲームへのDLL配備未実施。成果参照: data/recruit_sort_v4/src/hakushin_recruit_sort_v4.c、tests/test_diagnostic_win32.c、README_V4.md、reports/stage_probe_results.json。原作新規解析・他担当への依頼なし。


## WORK-V4-ACTUAL-SORT-20261022

V4雇用可能順: PARTIAL（実機表示まで前進）。4分類描画接続、ユーザーが並替えとリセット後再適用を確認。次はrank1領地不足/rank2資金不足の各1例と雇用後の再判定。既知リンク/再描画の反復確認を避ける。成果: data/recruit_sort_v4/reports/staged_on_pc.jsonのdiagnostic_session/four_group_session、src/hakushin_recruit_sort_v4.c、tests/test_diagnostic_win32.c。Work所有。


## WORK-ORIGINAL-EXE-ATTACH-20261022

原版EXE+拡張DLL起動: READY-FOR-INTEGRATION（手動分割起動で実機並替え確認、一括launcherはCheckOnlyのみ）。Work所有src/original_exe_attach*.c/tools/launch_original.ps1。4分類改修はPARTIAL、領地不足/資金不足/雇用後は未確認。原作解析証拠と拡張版runtimeを明確に区別。


## WORK-STARTUP-RECOVERY-20261022

P0 起動復旧（Work:調査、ユーザー:ZIP展開）。原版DLLなしもscript loading中exit0、原因未確定。原版SHA一致、ZIP比較612ファイル一致、追加work_observation.datのみ（原因断定不可）。ユーザー展開先確認待ち。Workは展開/上書きしない。資金不足試験はPARTIAL（資金495、原作gate0/拡張hireable0、全所属roster未確定）。領地試験/雇用後試験は復旧後。


## WORK-RECOVERY-ROSTER-CHECK-20261022

起動復旧はユーザー確認済み。既存フォルダへZIP上書き後に起動できたと報告、多重起動が原因との推測は未立証。Work保存済みセーブバックアップはdev_lab/_work/hire_startup_saves_20261022.zip、SHA95fe9f0b0ee864f8c1dfcd8f9d3ae09188ffad8a64b032009c0da155515e76b9、5ファイルの読戻し/CRC/内容一致検証済み（前checkpointの未作成記述を訂正）。
再確認PID32468は原版Vahren.exe単独、拡張DLLはmodule一覧に未検出。read-only snapshot: 資金64980、候補0、roster mode0/count0、selected/hover0。資金不足状態ではない。起動・接続・雇用操作は今回行わず、ユーザーに人材雇用→リセット→一覧外マウスを依頼。記録=data/recruit_sort_v4/reports/staged_on_pc.json recovery_retest_session。
ユーザー要件再確認: 領地条件は特定雇用者だけで決めず、全所属人材の誰かで成立すれば成立。実装の集約0>2>1>3を維持（表示順0,1,2,3）。現段階のP0は全所属ロスターが判定入力へ渡る実機確認。資金不足/領地不足の実機試験はPARTIAL、未成功扱い。新テスト/ビルドなし、原作・セーブ変更なし。


## WORK-V4-DEFERRED-ROSTER-20261022

実機PID28584/base270000: 原版SHA確認・旧DLL b050...接続installed1。資金495、所属5、候補17。ログhireable0/calls85/First four-group rendered後、resetでroster0によるreason-9、後の読取ではroster5かつRECT原順。資金不足分類そのものが原因とは未確定、リセット途中の所属一覧準備待ちから再適用されない経路を修正。途中snapshot保存照合のAssertionErrorはtuple/list JSON変換の観測側ミスであり、ゲームの不安定状態の証拠ではない（会話説明を訂正）。
変更: src/hakushin_recruit_sort_v4.cにUI thread SetTimerによる16ms/最大8回の限定再試行を追加。分類reason-8/-9のみ対象、別renderer呼出でpendingを取消。candidate tags/sourceDC/count/選択雇用者/hover/modeが変われば中止。native rendererや候補構築・資金処理は再実行せず、既存分類→GDI/RECT→presentのみ。成功snapshotのログに4群件数を追加。tests/test_diagnostic_win32.cに準備完了後の再試行、上限8、選択変更時取消、雇用可0でもrank2をrank3より前へ出すケースを追加。RED PID32036→GREEN PID12276(9PASS)→最終PID27856(10PASS)。timer callbackは合成試験で明示呼出し、原作message pumpでの成功は未確認。
修正版DLL build/PEcheck成功: SHA533054961ce3b37450fb5caf40e2f5eb99c2d7ad36a77734df01748ddd5e0c65、231424bytes。ユーザー終了承認後、旧DLLhashを照合し研究dist正規DLLへ差替・読戻一致（.next.dll同内容も保持）。原版EXE/DAT/saveは変更なし。tools/launch_original.ps1でPID13368を1つだけ起動したが、起動直後の接続はreply0 timeout。process生存/応答/拡張未loadを確認し、同一PIDへattachのみ再試行→UI31040/reply1/installed1。二重起動なし。launcher早期接続のtimeoutは別VERIFY。ユーザーへ低資金save→人材雇用→Reset→一覧外マウスを依頼、結果待ち。全体Python未実施・旧2FAIL残存、Golden/MATCH増加なし。
次: 修正版の実機groupsログ/Deferred roster-ready/RECT順を確認し、資金不足がrank2として残ることを照合。領地が別雇用者で成立する場合はそのofferを優先する既存0>2>1>3集約を維持。全完成とは扱わない。


## WORK-V4-RESET-ONCE-20261022
ユーザー実機報告: 前版533054...はリセット2回目で変態糞娘先頭の並替え成功。資金495、原作ログgroups=0,0,6,11（資金不足6/リンクなし11）とDeferred roster-ready確認。分類の資金不足分離は動作しており、1回目の不完全表示は残る。
修正: 即時分類をやめ、全員表示の分類/並替えをnative rendererの呼出元が戻った後のUI timerに統一。空でない未完成ロスターでも早期判定しない。deferred完了後は元repaint引数が0でも必ずpresent（呼出元は既にreturn済みのため）。古いpending取消・candidate/画面state検査・最大8回は維持。分類ルールは変更しない。
tests/test_diagnostic_win32.c: native renderer直後はclassifier0回、timer後に分類/RECT/pixels/present1回を確認。RED PID31968→GREEN PID30828→最終PID14852、関連10PASS/FAIL0。src/hakushin_recruit_sort_v4.cと当該testのみ変更。DLL build成功、SHA420baf22e0d89224b379c7c370549fafe09198c5d8700dab79844489779c5f0d。原版SHA確認、ユーザー終了/差替許可後distの正規DLLへ配置・hash照合済み。原版PID33044を単独起動、次は同一PIDへDLL接続→低資金save→Reset1回の実機検証。現段階で1回での成功は未確認。原作/セーブ未変更。

追記: PID33044/UI24852へのDLL接続reply1/installed1成功。ユーザーへReset1回での表示確認を依頼中。


## WORK-V4-RESET-ONCE-ACTUAL-20261022
ユーザー実機確認（PID33044、DLL420baf22...）: 人材雇用を開いた時点で既に並替え済み。Reset1回で一瞬原順が表示され、その後自動で並替えされる。旧「2回押す必要あり」はこの操作で解消。game logのDeferred roster-ready view renderedも確認。起動時/Reset1回の再適用はACTUAL_USER_CONFIRMED。全4条件/全セーブ/雇用後の完全検証ではない。残る問題は原順の一瞬表示（deferred適用前の描画が原因候補）、領地不足rank1の実機照合、実雇用後の更新、launcher初回接続timing。関連10PASS/FAIL0、原作EXE/DAT/save変更なし。追加の再起動依頼はせず、この動作版を維持。


## WORK-V4-LAUNCHER-WAIT-20261022
起動補助tools/launch_original.ps1へWaitForInputIdle(30000)を追加。splash表示だけでDLL接続を始めない。timeout時は同一ゲームを残して停止し、再起動/二重起動はしない。構文parseと-CheckOnly PASS（PID31332）、ゲーム起動全体は未再検証。README_V4.md冒頭に現在の4分類/DLLhash/実機確認/残課題/起動方法を整理し、旧履歴を明示。初回編集はCRLF一致assertで中断し無変更、改行を正規化して再適用・読戻済み。既存稼働ゲームとDLL本体は今回未変更。次は一瞬の原順表示と実雇用後更新/領地不足検証。


## WORK-V4-POST-HIRE-GUARDS-20261022
実雇用後確認に向けtests/test_diagnostic_win32.cへ候補削除、同数候補差替え、取消済timer callbackの3ケース追加。古いpendingが分類に入らないことを検証、PID31488:関連13PASS/FAIL0。DLL本体420baf22...は変更/再起動なし。実雇用試験はユーザーが資金十分のセーブへ切替え、任意1人を雇用して名前と一覧からの除去を報告する予定（返答「これから1人雇用して確認する」）。現在まだ雇用成功/候補除去を実証したとは扱わない。原作save上書きは依頼していない。


## WORK-V4-DISTRIBUTION-PREVIEW-20261022
雇用後の問題を実機で特定: reason-11、所属6/候補16。新規雇用者のdef+160 friend-cache件数0をDLLが全体拒否していた。保存current Ghidra 586080→586AB0→586320を再利用し、原作が必要時にfriend情報を生成する枝を確認。native_priority_v4.cの4分類製品経路だけは件数0でも原作判定へ渡す。旧relation観測入口のwarm-only制限は保持。friend_num/friend_ex生成はRNGを使用しうるため、RNG完全中立とは扱わない。元の定義/セーブを書き換えて埋める実装はしていない。tests/test_priority_win32.cへcold employerの原作側初期化stubを追加、RED PID28924 exit80→GREEN PID2292。native suite11 PASS表示（複数ケース内包）＋renderer13PASS、失敗0。
DLL SHAffdc73d2f416ab29d89089bdafee487b712b85d693426c31db4539bac3e0c981をユーザー許可後配置・hash検証。原版PID27644/UI21416への接続成功。WaitForInputIdleだけでは初期接続reply0を防げず、同一PIDへの再接続でinstalled1。ユーザー実機:「雇用後も自動で並替わった」。KBSトリオ雇用自体も成功しており、左欄を見る手動操作が必要な問題は今回解消。領地不足の実機試験・ちらつきは残存。
配布依頼を受けdata/recruit_sort_v4/dist/HakushinRecruitSort-0.1.0-preview.zipを作成。原作EXE/DAT/MAP/素材/saveは同梱しない。6 entries: DLL、attach host、portable launch_original.ps1、START.cmd、README.txt、SHA/size manifest。配置はゲームのVahren.exeと同じ階層にHakushinRecruitSortフォルダを置きSTART.cmd実行。元EXEhash限定・既存ゲーム起動中拒否。
launcherはreply0/installed999時のみ同一PIDへ最大3回再試行、拒否応答/ゲーム終了では中止。tests/test_launcher_retry.ps1 4PASS（成功、拒否、3回上限、終了済み）。CheckOnly PASS。起動全体の配布版実機試験は未実施とREADMEに記載。
ZIP SHA: 27040aa51b02c497ce2824986f7f44130dc7ebee3f7748c3be97ad934a4fb9f0
ZIP CRC/全entry byte一致/原作データ非同梱を検証。tools/package_preview.pyで再作成可能。README_DISTRIBUTION.txtに確認済み範囲・ちらつき・領地不足未検証・100件上限・RNG副作用を明示。配布はユーザーが行うため、外部公開/アップロード/Git release等は未実施。


## WORK-V4-PACKAGE-EXTRACT-CHECK-20261022
配布ZIPを一時フォルダへ展開し、manifestの全ファイルSHA/サイズ、相対配置、START.cmdのCRLF、展開したlauncherのCheckOnly、展開したhostとDLLの自己試験を検証。PID31552 exit0。自己試験 reply1/installed0/self_test1 は非ゲームへの接続拒否が期待どおりという意味。配布START.cmdによる原作起動全体は引き続き未実施。現行ゲームには操作せず、ZIPの内容も変更なし。ZIP 224618 bytes / SHA256 27040aa51b02c497ce2824986f7f44130dc7ebee3f7748c3be97ad934a4fb9f0。


### 配布版起動確認の引継ぎ（2026-10-22）
現在の原作PIDは16764（Hell表示）で、前回DLL確認の27644とは別。Workは追加起動・接続・終了を行っていない。配布版START.cmdの通し確認は利用者の都合のよい終了・再起動待ち。DLLの既存実機確認と配布launcherの通し確認を混同しない。配布ZIPは変更なし。


### 配布版START.cmd起動成功（利用者実機確認）
利用者が配布ZIPの起動確認依頼に「起動できました」と回答。配布版から原作の起動成功をACTUAL_USER_CONFIRMEDとして記録。今回セッションのDLL接続・雇用一覧並替えはこの回答だけでは未確認。過去のDLL実機並替え・雇用後自動更新とは区別する。配布ZIPは変更なし。


### 配布版0.1.0-preview：起動から自動並替えまで実機確認済み
利用者がSTART.cmdから起動成功に続き「はい、問題なく自動で変わりました」と回答。配布ZIPによる起動→人材雇用→自動並替えをACTUAL_USER_CONFIRMEDとして記録。配布ZIPは変更せず、SHA256 27040aa51b02c497ce2824986f7f44130dc7ebee3f7748c3be97ad934a4fb9f0を維持。残る制限は領地不足分類の実機ケース未確認、リセット時の一瞬の旧順表示、広範な長時間互換性未検証。通常戦闘エンジン全体の完成やGolden/MATCH達成を意味しない。


## WRQ-20261022-WORK-SUMMON-EXP｜Work｜P1｜PARTIAL（読取専用EXPサンプラー実装・合成試験済／親子対応未確定）
- 目的: 召喚子の戦果を召喚者の成長へ反映する拡張。配布済み雇用DLL0.1.0-previewは固定し、混入させない。
- 既存成果: exp_research_20261021/EXP_COLLAB_HANDOFF_20261021.md、EXP_SUMMON_OWNER_RESEARCH.md CP01、rea_lab/headless_analysis/search_index/P0_SUMMON_EXP_OWNER_REPORT_20261021.md をWorkが読取照合。研究はSTATIC/NOT READY、実機未観測。既存研究所有資料は編集しない。
- 再解析不要: 54E7B0→577260/577310のR検索/生成→56F880+1C8→551E50のR+16C加算。57F4E9の召喚発動EXPは別イベント。+1CCは部隊代表候補であり召喚者IDとして使わない。R共有の可能性があるためR差分を子ごとに複製加算しない。
- 現行観測器の再利用: dev_lab/src/hakushin_compat/peer_script01_live_observer.py は既にdef_1c8とexp_16c/exp_next_170を読む。UNIT_FIELDSに+1CC/+1D0や生成時source→childの対応記録はない。単なる親子EXPポーリングだけで因果や還元先が確定したとは扱わない。Claude所有かつdirtyなので直接変更しない。
- 次の最小工程: 所有分離した読み取り専用アダプターで既存Reader/Observerを利用し、actor・R・部隊・フレーム・EXPを欠損明示で記録する。生成時source→child契約を得るまでは親を推定しない。初段は記録のみでEXP書込みなし。
- 未完: 生成時sourceの安定ID、R共有/寿命・親死亡/戦闘終了での確定先、drain別経路、還元率・多段召喚・変身の方針。新しいフックを実機へ入れる前にABIと寿命を確認する。割合など未合意値を固定しない。
- 停止VA: EXP配分先の寿命/同一性（54E7B0/577310/551E50周辺の既存証拠から接続）。既拒否Wiki追記/VA/SQLは再提出しない。研究チャットへの送信・起動は今回なし。


## WORK-SUMMON-EXP-SAMPLER-20261022
新規Work所有 src/hakushin_compat/work_exp_observer.py と tests/test_work_exp_observer.py を追加。Claude所有peer_script01_live_observer.pyをimportしてReader/Observer/ASLRアンカーとEXE hash/probeを再利用し、元ファイルは編集しない。
Unitの+1C8 record / +1CC group representative / +1D0 troop、record+168 level/+16C EXP/+170 thresholdをraw unsigned値として2回読取。Task stamp前後と両pass不一致をUNSTABLE、欠損をINCOMPLETE、null recordをNO_RECORDとして扱う。親IDはUNRESOLVEDで、+1CCを召喚者として推定しない。同一recordを共有するactor集合を1項目で列挙し、子ごとに加算する計算はしない。CONSISTENT_READは原子的読取やポインタ世代の証明ではなく、ABA再利用・ポーリング間の変化は検出保証しない。
CLIは --pid --out を必須とし、既存ファイルを上書きしないexclusive作成、秒数最大300、最小poll10ms。既存原作SHAとGMアンカーを確認し、active/pending Task内Unitを記録、Task集合変化もUNSTABLE。EXEへの書込・中断・注入なし。実戦を今回は実行/観測していない。
検証: RED PID31200（未実装8FAIL）→GREEN PID5888 新規8PASS＋既存観測9PASS、FAIL0。CLI --help PASS。全体回帰は未実施、過去全体2FAILは未解決のまま。合成memory試験でありACTUAL/GOLDEN/MATCHを増やさない。配布済み雇用DLL/ZIPは変更なし。
実行例（dev_labでPYTHONPATH=src）: python -m hakushin_compat.work_exp_observer --pid <確認したPID> --out <未使用JSONLパス> --seconds 20
次: 最小召喚条件の記録に用いる前に生成時source→childの既存契約と観測接続を整理。現在のサンプラーだけで真の親子対応や親死亡後の配分先は確定できない。還元率・多段召喚・変身の仕様未合意なのでEXP書込を実装しない。ユーザーのプレイ中ゲームを変更しない。


### 召喚EXP還元の利用者指定（2026-10-22）
利用者回答: 「還元率を設定できるようにし、値は後で決める」。固定100%などの値を採用しない。率未設定時は還元無効で原作挙動を維持する。子のEXPを残して追加するか、親へ移すかは今回回答で決まっていないので未確定のまま。丸め・多段召喚・親死亡・戦闘後LvUpの扱いも未確定。現段階は読取・観測・集計までを進め、率や移転方式を黙って補完してEXP書込を開始しない。配布済み雇用拡張へは混入しない。


## WORK-EDUCATION-ITEM-SELECTOR-20261022｜Work｜P0｜PARTIAL
最新利用者要望により次の主作業を教育（講師/生徒）とアイテム使用対象の選択UI改善へ変更。召喚EXPは成果を保持し優先を下げる。困り事は大量人材の探索、名前順不足、チップなし、アイテム画面のソート不足。原作の候補条件・教育効果・アイテム消費・対象IDは維持する。最初は名前順とキャラチップの実現方式を確認し、小さい実機試験から進める。配布済み雇用0.1.0-previewは変更しない。
PCで確認: script/43_内政_教育/lecture.dat の共通choice処理は8人/ページ。1030/1043/1055行choice、1061以降は8=次、9=戻る、10=やめる、11=能力切替。1074〜1079はpage*8+選択indexから@chara_listの対象を取得。表示だけの並替えは対象誤選択を起こすため不可。生徒側は同ファイル870〜929に別ループがある。1423 getCharaListはstoreUnitOfPower/Spot→getCharaFromList→除外。原作順が所在地登録番号順という利用者推測は未確定。
水泳ev01_swim.dat 250〜269: 講師候補を取得後、magdefへ講師補正を書いている既存処理がある。画面のmagdefを単なる通常能力値として扱わず、教育の既存ソートと補正/復旧処理を維持する。
アイテム ev_item_use_000_status2.dat 10〜12/44〜46 はitem_chara_choiceを呼び、返却@erandacharaへ後段効果を適用。呼出側は@sort_status=mp/hpを設定しているが、これだけで現行UIにソート切替があるとは断定しない。
次: item_chara_choice本体・教育共通choice caller・画像付き選択肢の既存DAT/エンジン契約を照合。DATのみで可能な改修を先に選び、必要部分だけDLLを検討する。ゲームDAT/EXE/セーブの変更、クリック/教育/アイテム消費はまだ行っていない。
item_chara_choice検索結果: ['41_内政_アイテム\\ev_chara_choice.dat:1', '41_内政_アイテム\\ev_chara_choice.dat:433', '41_内政_アイテム\\ev_chara_choice.dat:535']


## WORK-UNIT-SELECTOR-INVENTORY-20261022
利用者追加要望: 教育/アイテムだけでなく所属Unitから選ぶランダムイベントも対象。共通selectorと独自selectorを分け、会話選択肢・次へ戻る・全軍効果は並替え対象外。
既存script_sourceのコメント分類を再利用して3235 eventの候補索引を作成。choiceUnitFromList/getCharaList/item_chara_choiceからliteral routine逆参照71名、独立候補35件、CP932読取gap0。これは画面数や対応完了数ではなく字句検索候補。動的呼出/event()は網羅保証なし。reports/WORK_UNIT_SELECTOR_INVENTORY_20261022.jsonに出所hash・event・行位置・call・choiceを保存し読戻し。
確認済み: ev_chara_choice.dat冒頭item_chara_choice→sortStatus→choiceUnitFromList。433/535行の同名定義はblock comment内で非実行。ランダムrandomev55もitem_chara_choiceを呼ぶ。randomev31_1/31_2は単なる物語の選択＋全軍LvUpなので対象から除外。教育choiceUnitFromListは名前/能力表示の8枠＋操作枠、選択結果は元リストindexへ戻す。group全体を名前順にするには全ページの候補ID列を保持しなければならず、画面の現ページだけのsortでは不足。
次の実装設計: 教育/アイテム共通選択を初段、独立ランダム選択は対象ID取得/返却契約の確認後に追加。チップ表示のchoice対応は未確定。既存select命令は決定取消のダイアログでありUnit画像選択器の代用ではない（Claude findings旧§参照）。DATのみの名前取得/比較と画像表示の可否を確認し、必要なら限定DLLで共通のUnit選択を補う。原作の教育補正/能力順と絞込を保持する。今回原本DAT/EXE/保存データ・配布DLLは未変更、実機選択試験未実施。


## WORK-UNIT-SELECTOR-SCOPE-SWITCH-20261022
利用者の追加スクリーンショットを原作DATと照合。50_その他新システム/siki_item_switch.dat:1-20はunit 005_switch（politics=fix、image=kozinomi、merce=cmd_000_allchara,cmd_001_spotchara）と各コマンドUnitの画像を定義。68-78行でptestに応じitem_choice_kirikaeを0/1に設定しreloadMenu(on)。これはDATで定義された内政コマンドの画像付き一覧であり、汎用choice命令で画像を表示できる証拠とは区別する。
lecture.dat:303-306 teacher_chara_choice、1386-1387 choiceChara、1423以降getCharaList、1442以降getLeaderListが当該設定を読む。既存の勢力全体/指定領地という候補範囲切替を保持し、その後の候補リストに名前順/チップ表示を適用する方針。独自ランダムイベントがこの設定を参照しない場合、勝手に候補範囲を変更しない。教育補正・除外・返却UnitIDも保持する。画像付き内政コマンドとイベント選択肢は別描画系の可能性があるため、見た目だけで同一と判断しない。
今回は原作DATのread-only照合と記録のみ。製品実装/実機選択/新規テストは未実施。配布雇用DLL/原作DAT/EXE/save変更なし。次は共通choiceで候補IDと表示を対応させる最小試験を作る。


## WORK-CHOICE-READONLY-ACTUAL-20261022
追加実装: Work所有src/hakushin_compat/work_choice_observer.py、tests/test_work_choice_observer.py。既存Claude Readerを変更せず再利用。原作SHA限定、ASLR対応、ChoiceWnd vtable照合、最大50件、2回照合、不足/不一致を明示、出力上書き禁止・読戻し。ゲームへ書込/注入/native呼出しなし。閉じた画面の値が残る可能性があるためvisibility=UNVERIFIED、selector_kind=UNRESOLVEDを維持。text_templateは表示名でなく未展開参照式の場合がある。同名をUnitIDへ推測変換しない。
根拠は既存exe/T006_CHOICE_VMETHODS.txt、T006_UI_RTTI_PROBE.txt、保存current Ghidra41E710/41E910。ChoiceWnd VA8BB6D8、vtable638234、count+170、result name+190、RECT+1AC stride16、strings+4CC stride1C。41EBE0は選択indexを返却先numeric entry+1Cに書く。GhidraのABI未確認警告は維持しhook prototypeには使用していない。
試験: RED PID17724で未実装6FAIL→GREEN PID23596 新規6PASS＋既存Reader9PASS/FAIL0。最終text_template命名修正後も同じ関連試験を実行。全体回帰未実施、既知過去2FAIL未修正。これはSYNTHETIC試験。
実機読取: PID18704/base270000、原作SHA一致。_work/choice_observation_20261022_01.jsonはcount11、result_variable=use_spot_sentaku、_02.jsonは利用者が領地選択後に開いたUnit一覧でusechara_sentaku。両者とも8個の&@choiceN&と次へ/戻る/やめる、RECT一致、2回読取一致。raw JSONのlabelキーは未展開テンプレートを示す（後のコードではtext_templateへ明確化）。この観測は実際のUI遷移に対応したACTUAL_READ_ONLYであり、並替え/チップ/効果対象一致は未実装・未実証。Golden/MATCH増加なし。
次: @chara_listと@choiceNの文字変数から全候補IDと表示名・画像を安全に対応させる。既存peer_script01_native_expression.pyはevalString44DBF0を記録、保存Ghidra49C450/49ECA0に文字変数検索とvector先頭読取があるがpseudocode引数はABI未確認。ctx+504という呼出情報だけでruntime mapを推測書換えしない。全ページ候補IDを並べ替え、戻り値を正しく元候補へ対応させる必要がある。領地候補・会話選択肢をUnitとして扱わない。
配布雇用DLL、原作EXE/DAT/saveは無変更。利用者はUnit一覧まで準備済み。次の確認までアイテム使用等は依頼していない。


## WORK-CHOICE-CANDIDATE-IDS-20261022
Work所有work_choice_observer.pyへbounded文字変数map読取を追加。保存Ghidra4303E0はChoiceWnd+98 owner→owner+4 context、context+504を文字展開へ渡す。49C450/49C5C0/49ECA0/49F390の保存解析からscope+1E8640=head、tree node key+C/left0/right8/isnil39、values vector+28/+2C/+30を照合。実機context+1E8B40のmap(header+4head/+8count)、44node、std::string stride1Cをread-onlyで確認。native関数を呼んでいないため未確認ABIをhookに流用していない。
実装capture_variablesは最大4096node/vector4096要素、循環/同名key/不正nil/欠損/不正vector/ヘッダ変化/2回不一致を拒否。missing key=Noneと空vector=[]を区別。CLI --variablesでChoiceWnd+owner/context+候補mapを2回照合しexclusive保存・読戻し。二重snapshotは原子性/ABA安全性を証明しない。ゲームへの書込み・停止・注入なし。
テスト: PID31044で新規5件未実装FAIL→PID27860 11PASS→PID4424専用11＋既存Reader9PASS/FAIL0、CLIhelp PASS。広域/全体未実施（過去2FAIL未解決）。実機CLI PID32260 exit0、_work/choice_observation_20261022_03.json SHAe08732721b999acce8ed7fb0ac79db4068b60107ac7c122117253abac71ff912。PID18704/base270000原作SHA一致、usechara_sentaku、sp10候補ID[kusomusume,ice,tknuc]、2回一致。
先の探索読取_work/choice_variables_20261022_01.jsonでは[ice,kusomusume,tknuc]と一部古いchoiceN値を観測。後の_02とCLI03は[kusomusume,ice,tknuc]かつ先頭3つのchoiceN対応を観測。Workは並べ替えていない。観測間の順序変化の原因は未確定で、live状態を各回取り直す必要がある。利用者は3人が表示されていると回答。候補数を超えるchoice4..8には末尾tknucが残るため、choiceN値だけで全候補数を判断しない。
既存BattleDefinitionCatalog再利用でDAT名前/画像を確認。完全chain previewはbase同名2候補で拒否（_work/choice_unit_definitions_20261022_01.json）。allow_partial=Trueの既存機能で既知prefixのみ参照し、3人ともunit自身にname/imageの直接定義があることを確認（_02.json SHA9cbb14e9590eae5466b03228122db822a3a7302c344ee1fe21ce0a21d0589dd7）。ice=ＩＣＥ姉貴/icecream、kusomusume=変態糞娘/kusomusume、tknuc=ＴＫＮＵＣ/tknuc。これはDAT_DERIVEDの直接定義で、live rename/image overrideや不明な継承の解決ではない。parserを改変せず曖昧なbaseを選ばなかった。
次の製品接続: 候補ID列を正本に名前順とチップを表示し、選択globalindexを原作のページ/戻りindexへ正しく渡す。汎用ChoiceWndを無差別に並べ替えず、教育/アイテム/関連ランダムの候補契約を明示。現在はread-only基盤まで、並替え・チップ・クリック結果反映は未実装。native41E710/41E910 hook ABI、文字列所有権、原作VM再開を確認してから変更する。配布済み雇用DLL/原作DAT/EXE/save無変更、Golden/MATCH増加なし。


## WORK-UNIT-SELECTOR-UI-PREVIEW-20261022
Work所有src/hakushin_compat/work_unit_selector.py、tests/test_work_unit_selector.pyを追加。保存した原作候補snapshot→既存BattleDefinitionCatalog→既存load_declared_spriteを利用し、別ウィンドウの名前/チップ/名前順（NFKC casefoldの表記順、読み仮名五十音順ではない）/元の順/検索/選択ID確認を実装。元のsource_indexを保持し、同名・同ID・ページ越し候補も区別する。候補列が変わる場合のchoose拒否、領地result拒否を実装。元DAT候補の効果・領地条件・教育補正は変更しない。
UIは明確に「試作・ゲーム反映なし」。独立Tk画面でありゲーム内DLL接続ではない。保存snapshotを表示しており自動live更新はまだない。name/imageはDATの既知prefixなのでruntime変更名/画像は未反映、欠損はID/画像なしへ明示。原作対象を実行せず選択IDを表示するだけ。
試験: PID33060 未実装6FAIL→PID21712 6PASS。Windows実データGUI self-test PID32860 PASS、候補3/チップ3枚、並替え・検索・選択ID保持を操作検証。pythonw PID29896で利用者向け試作を起動し、プロセス応答を確認。利用者が「表示され、並べ替え・検索できた」と回答（ACTUAL_USER_CONFIRMED、あくまで別ウィンドウUI）。原作プロセスの起動/終了/変更はなし。
返却契約を元lecture.dat967-1080で照合。choicepage*8+usechara_sentakuから@chara_listをindexし@eranda_charaへ返す。return_planは元globalindex//8をchoicepage、%8をusechara_sentakuとして計算するpure adapter。8/9/10/11の次頁/前頁/取消/能力切替をUnit indexとして生成しない。領地use_spot_sentakuは拒否。PID5436新規2FAIL→最終専用8PASS・observer11PASS・既存Reader9PASS/FAIL0。全体回帰は未実施、旧2FAIL未解決。原作返却/アイテム消費/教育適用はまだ実装していない。
次: native UI threadでの返却接続を最小1例で実装。候補ID全列・現在のChoiceWnd/VMcontext・result変数・世代の再検証が必要。原作のstd::stringやvectorを外部から並べ替えず、view順と元indexを分離。native完了callback/VMresumeは41EBE0保存ASM参照、数値map463CA0はfind-or-createなので無検証呼出をしない。原作関数ABI確定前に注入/実行しない。
Localのsaved query一回がnetwork timeout、別経路へ迂回せず同Local read_file成功で回復確認。原作/試作の再起動はしていない。配布済み雇用DLL/ZIP/EXE/DAT/save無変更。利用者は試作ウィンドウを閉じても問題ない。固定handoff・キュー・ログに保存し読み戻す。


## WORK-CHOICE-RETURN-BOUNDARY-20261022
保存証拠再利用で原作返却の不足箇所を確認。exe/T006_SELECT_CHOICE_CALLBACKS2.txtの41E6D0..41E70D: ECX=this、push1→453AC0、owner+98→+4からcontext、context+28へ文字列choiceを登録、ret（追加stack引数なし）。41EBE0の成功commitはnumeric result+1C書込→vtable+54=41E6D0。従ってclose処理には単なる非表示だけでなくVM側へのchoice通知が含まれる。保存Ghidra453A50はFrameWnd+84が可視flag、453AC0はその解除/描画更新。pseudocodeだけから引数を推定せず、close thiscallの呼出根拠は既存ASMを採用。
数値変数: 保存463CA0/4C1200/436680/4682B0でcontext+1B8のscopeから+30C map、+310 headを参照。tree node key+C、value record pointer+28、isnil+2D、record+1Cが数値。read-only実機でcontext+4C4 map3979nodeを全走査し、choicepage/page/n_page/usechara_sentakuを確認。_work/choice_numeric_return_20261022_01.json SHA3db3700e551c28232bd7423e46c4945dda7acf4dd9f7db206469555d3b05d45d。PID18704原作SHA一致、ChoiceWnd+84=1、返却usechara_sentaku。choicepage0、n_page1、page1、usechara_sentaku3（前回値として残り得るので未決定の現在選択と解釈しない）。ゲーム書込みゼロ。
次の実装を具体化: 既存recruit_sort_v4のUI-thread WH_GETMESSAGE bootstrapとx86 Zig環境を再利用し、別名WorkUnitSelectorBridge.dllを作る（配布済DLL/ZIPは触らない）。原作全候補文字列/vectorを変更せず、bridgeがcurrent candidate列と要求source_indexを照合→choicepage=index/8、result=index%8→確認済native close通知。最初はdry-run検証を実装してからcommitを有効化する。
古い別画面への誤適用防止にはPID/context/候補列/可視flag/result変数だけでなくinteraction世代が必要。同じ画面を閉じ再表示するABAを考慮し、choice setupの既存直接CALL 41E7E3→41E910（保存E8 28 01 00 00）へレジスタ/flagsを保持する世代カウンタgateを検討。元rendererのnative prototypeを推定せず、元呼出へtail jumpして引数/戻りをそのまま保つ。commitは原作UI thread内で再検証し、世代不一致なら拒否。外部UI確認時に任意のプロセス値を書くだけの方式は採用しない。クリア/次/戻る/能力順は引き続き原作へ委譲する。
現在まだbridge DLLは未作成・未接続、原作の効果実行も未試験。このturnは保存nativeと実機read-only照合のみ、新規テストなし。既存UI専用8＋observer11＋Reader9PASSの記録は維持。全体回帰未実施、Golden/MATCH増加なし。資料保存後読戻し確認。


## WORK-CHOICE-BRIDGE-VALIDATION-20261022
利用者がUI試作のチップ表示・名前順・検索を確認済み。今回、Work専用の検証DLLを実装・ビルドし、原版PID18704へ接続して現在の候補3人を実機照合した。配布済み雇用DLL/ZIPは変更なし。
追加: data/recruit_sort_v4/src/work_selector_packet.h、work_unit_selector_bridge.c/.def、tests/test_work_selector_packet.c、test_work_selector_native.c、tools/work_selector_validate.py、build_work_selector.py、dist/WorkUnitSelectorBridge.dll。
DLLは原作SHA256限定、既存UI-thread bootstrapを再利用。message-only window WorkUnitSelector.Validate.v1 / WM_COPYDATAで検証専用要求を受ける。ChoiceWnd vtable/可視flag/VMcontext/result名usechara_sentaku/候補数/全候補ID列/選択indexを照合。候補文字列・vectorは変更しない。action1のみ許可しcommitのaction2は必ず拒否。現時点でコードpatch/変数書込/選択確定/VM再開は一切なし。DLLをプロセス内へロードしてendpointを追加しているため、完全に非侵襲な外部読取と区別する。
試験: packet未実装RED→assert有効の8ケースPASS、native fixture10ケースPASS（fixture全メモリ不変も照合）。最初のO2ビルドでNDEBUGによりassertが無効だったため、その結果は採用せず、明示#undef NDEBUGと-Werrorで再ビルド・再実行済み。非ゲームhost自己試験は接続拒否が期待どおり成功。Python関連 UI8+choice observer11+既存Reader9=28PASS、FAIL0。広域/全体回帰未実施、既知過去2FAILは未修正。
実機: _work/choice_bridge_validation_20261022_01.json、ACTUAL_VALIDATION_ONLY。原版SHA確認、context7529200、候補[kusomusume,ice,tknuc]一致。正常候補一致、commit拒否、別context拒否、範囲外index拒否、変更ID拒否、choice/candidates前後不変の6項目PASS。教育/アイテム効果はまだ実行していない。Golden/MATCH増加なし。
DLL SHA256 1bd08fb7cc74f218311ed2b0a500b017572d8c907c28a5ac28d977aa3f2e7744。現行PIDには検証DLLがpin済みなので、同名DLL差替え前は通常終了が必要。今回はゲーム終了/再起動を要求していない。
次: 同じ候補で開き直した場合も識別するinteraction世代のguardを実装・fixture検証。保存済41E7E3 direct CALLとレジスタ/flags保持gate案を再利用。世代・context・全候補をUI threadで再検証してからchoicepage=index//8とusechara_sentaku=index%8、41E6D0 close/VM通知へつなぐ。現validatorの成功だけを将来のcommit許可に流用しない。close ABIは既存境界checkpoint参照。まず非消費dry-run、実選択は利用者が明示的に確認する1件で行う。独立生徒selector/未接続ランダムイベント/能力順連携/runtime変更名は残課題。


## WORK-CHOICE-GENERATION-GUARD-20261022
前turnは実装・実機証拠を伴うprogress。今回も現行handoff/queue/source/Git dirty76件/原作PID18704 Respondingを再確認し、選択UI接続を継続。Work所有work_choice_generation.hを追加。原作choice setupの既知CALL 41E7E3→41E910を、完全一致E8 28 01 00 00の場合だけhookする処理をbridgeへ追加した。原本EXEファイルは変更しない。gateはpushfl/incl(epoch)/overflow時exhausted=1/popfl/tailjmpだけ。C関数呼出やFPU/SSE操作なし、全引数と元return先を保持。世代0/不一致/uint32一周後は永久拒否。
WM_APP+71で可視usechara_sentaku画面のepochを取得。WM_COPYDATA tag0x32535557はuint32 epoch+従来検証packetを受け、世代一致後に全候補/context/可視等を再照合。旧v1は検証専用のまま。両方action2 commitは無効。原作選択/変数/VMはまだ変更しない。
TDD: test_work_choice_generation.c header欠落RED→GREEN。x86 naked harnessでEAX/ECX/EDX/EBX/EBP/ESI/EDI、carry flag、tail return保持、stale/reopen、世代overflow後fail-closedを実行確認。test_work_selector_native.cはv2同一候補でも世代変更後拒否、非表示時token0、CALL前bytes不一致拒否/rel32先一致/二重patch拒否を追加。最終build_work_selector.pyでpacket8ケース＋native suite＋generation suite全PASS、-O2 -Wall -Wextra -Werror、assert明示有効、非ゲームhost自己試験PASS。build scriptへ--output追加。Python live probeへ--guarded/--dll追加、compile/help成功。今回広域/全体回帰なし。
現在ロード中の旧DLLを上書きせず、dist/WorkUnitSelectorBridge-generation-preview.dllへビルド。SHA256 45986abb38db2a3039c9fa7c5586c6d6b0f4d9532338adf7ad523328b797532c。この新版はまだ原作へ接続していない。既存UI endpointクラスと競合するため、ゲーム通常終了後に新規起動したPIDを確認して新版を接続する。二重起動や勝手な終了をしない。
次の実機試験: 共通人材選択を開いて --guarded --dll <generation-preview.dll> でdry-run。一度画面を戻り同じ候補を開き直し、epoch増加と旧token拒否を確認。単にepoch-1を送る試験と、実際の再表示を区別。通過後にのみ選択確定経路を実装。close native契約は前checkpoint参照。利用者のアイテム消費は今回求めない。原作Golden/MATCH増加0、雇用配布ZIP無変更。


### WORK-CHOICE-GENERATION-LIVE-ATTACH-20261022
利用者がゲーム終了を報告。Get-ProcessでVahren不在を確認し、原版EXE SHAおよびgeneration-preview DLL SHAを照合後、原版を1プロセスだけ起動（PID32416）。既存attach hostで新版を接続し exit0 / ui_thread27520 / reply1 installed1 self_test0 を確認。原本EXEファイルは変更なし。今回のDLLは世代計測CALL hookを含む検証専用で、選択確定は無効。
利用者へ同じ3人の共通Unit選択を開くよう依頼中。実際の再表示によるepoch増加・旧token拒否の実機試験はまだ未実施。起動成功・DLL接続成功と選択UI実動作を区別する。次はtools/work_selector_validate.py --pid 32416 --guarded --dll <dist/WorkUnitSelectorBridge-generation-preview.dll> --out <新JSON> を使う。PID再利用を避け、実行時に原作SHA確認を維持。ユーザーの人材決定/アイテム使用は依頼していない。


## WORK-SELECTOR-LIVE-UI-20261022
前turnは新版DLL実機接続を行ったprogress。今回PID32416のendpointに--guarded probeを行い応答を得たがepoch0/No active guarded selector。これは原作終了・DLL故障と判断せず、利用者の一覧準備待ちとする。自動再起動なし、アイテム消費なし。
独立工程としてsrc/hakushin_compat/work_selector_live.pyを追加。WindowsBridgeは原作SHA/PIDに属するendpoint照合、epoch前後一致、候補snapshot2回一致、原作UI threadの全候補照合を経て試作を表示。LiveSelectionは元indexを保持し、拒否/通信失敗時にはセッションを永久invalidにする。commit要求は送らない。既存work_unit_selector.pyのload_snapshotをload_stateへ分離、任意live_check callbackを追加し、並替え/検索後に「原作の候補と照合」ボタンで確認可能にした。UIは引き続き試作・ゲームへ反映しない旨を表示。古いファイルsnapshotの確認経路も保持。
試験:新規4件RED→PASS（元index保持、候補拒否後再使用拒否、不正index未送信、通信失敗後再使用拒否）。UI8＋observer11＋Reader9を再実行し合計32PASS/FAIL0。WindowsBridgeの実機captureと新live GUIは利用者が一覧を開いた後に検証するので未実施。新規4件はfake transport試験であり実機一致と混同しない。全体/広域未実施。
次:python -m hakushin_compat.work_selector_live --pid <SHA確認された現PID> --game-dir <原作展開先> でlive試作を起動。先にtools/work_selector_validate.pyの--guardedで8項目確認、一覧を実際に開き直したepoch増加/旧token拒否も確認する。効果決定接続はまだ未実装。固定handoff/queue/log保存、読戻しhash照合。配布雇用DLL/ZIP原本は変更なし。


## WORK-CHOICE-RETURN-STAGED-20261022
前turnはlive UI接続実装のprogress。今回current source/handoff/queueを再読し、原作選択を確定する内部経路を実装。ただしlive dispatcherに公開しておらず、現在起動中generation-preview DLLにはこの変更を適用していない。
追加src/work_choice_return.hとtests/test_work_choice_return.c（data/recruit_sort_v4以下）。元globalindexをpage=index/8、result=index%8へ変換。両書込先をVirtualQueryで事前確認し、null/alias/readonly/不正index/世代不一致/overflow後は拒否。callback前にepochを無効化し二重送信・再入を防止。全候補/context検証と同じUI thread内で呼ぶ前提。
work_unit_selector_bridge.c: prepare_returnがcontext+4C4 numeric treeをbounded走査し既存choicepage/usechara_sentaku record+1Cを解決。find-or-createを呼ばず欠落/alias/cycleを拒否。close vtable+54がbase+1E6D0と一致することも確認。unexported commit_validated_choiceはvalidate→prepare→stores→thiscall41E6D0の契約へ接続。現在WM_COPYDATA action2は従来どおり拒否するので、実機確定は未実施。決定音は未接続。
試験: return header未実装RED→GREEN。index19→page2/result3、close呼出前の値、同token二重適用拒否、範囲外、書込先alias/readonly、epoch overflowをnative fixtureで検証。既存native suiteに数値map解決/値不変/missing/cycle/alias/staleを追加。packet8、native、generation、returnの4実行体全PASS（assert有効、-O2 -Wall -Wextra -Werror）。host自己試験もPASS。テストcallbackは原作41E6D0を実行していないので、原作VM再開成功とは扱わない。
未ロード別DLL dist/WorkUnitSelectorBridge-return-staged.dll SHA256 96bdace61a5e14ada088407ab1e81fc82ad9ffe5e0d054f73d254b64c025fd90。原作EXE/DAT/save・公開雇用ZIPに変更なし。次は利用者が人材選択を開いた後、現generation-previewで実際の再表示によるepoch増加/旧token拒否を確認。それから明示的な選択確認UIとcommit dispatcherを接続し、1人の対象と実効果を照合する。全体/広域未実施、Golden/MATCH増加なし。


## WORK-CHOICE-COMMIT-PREVIEW-20261022
現PID32416のguarded endpointを再照合したがepoch0/No active guarded selector。原作とDLLは応答、一覧準備待ち。前turnは返却core実装のprogressであり、待機だけを進捗に数えない。
待機中に実際の選択要求経路を実装。bridgeのv2 WM_COPYDATA action2をWORK_SELECTOR_ENABLE_COMMITビルド時だけ受付。copyしたpacketのactionを検証用1に変換して既存全候補/世代/context検証・prepare・返却へ接続。v1および既定ビルドは引き続き確定不可。WM_APP+72で確定対応capabilityを問い合わせる。ゲームにロード中のgeneration-previewは変更なし。
Python LiveSelection.commitは送信前にセッション無効化。成功・拒否・timeoutいずれも同じtokenを再送しない。WindowsBridgeのcommitメッセージ追加。work_selector_live CLI --allow-commitとDLL capabilityが揃うときだけUIの「この人材で進める」を表示。対象名と教育/アイテム使用の可能性を示す確認ダイアログ後に送信。通常起動は検証のみ。成功時UIを閉じる。GUI確定動作は実機未確認。
試験: Python新規3件RED→GREEN、live7+UI8=15PASS。nativeはpacket/generation/return/既定validatorに加え、commit macro有効の同一native fixtureを別exeで実行。UI-message→候補検証→numeric record→page/result書込→fake close1回→epoch増加→重複拒否までPASS。fake closeであり原作41E6D0/実効果を実行したとは扱わない。5テスト実行体＋host自己試験PASS、-Werror/assert有効。
未ロードdist/WorkUnitSelectorBridge-commit-preview.dll SHA256 bc4f27f7c128b00e31e703e724e63e14c79b2ca9c2df382aee5c5d240bc17b4d。ビルド再現: tools/build_work_selector.py --enable-commit --output <別DLLパス>。既定ではcommit無効。原版への新版差替えはまだ行わない。現generation-previewで利用者が一覧を開いた後、実際の再表示世代を確認してから通常終了/差替え/明示的な1件選択へ進む。
全体/広域未実施、Golden/MATCH増加なし。原作ファイル/セーブ/雇用配布物無変更。固定handoff/queue/log読戻し検証済み。


## WORK-CHOICE-REOPEN-ACTUAL-20261022
利用者が3人の一覧を準備。原版PID32416/generation-previewにguarded probeを実行し、epoch4、候補[ice,kusomusume,tknuc]、8項目すべてPASS。_work/choice_bridge_generation_20261022_01.jsonへ保存。commit_disabledも実機確認、選択や消費なし。
利用者が「やめる」から同じアイテム/領地の3人一覧を開き直した後、WindowsBridge.captureを実行。epoch4→6、同一候補列、旧epoch4の要求拒否・現epoch6の要求受理を確認。_work/choice_bridge_reopen_20261022_01.json SHA d01777f2896c0af736dbd6b76d05d4c280eba32d62e39c8ee778ef8b9ad2035f。これは実際の再表示によるACTUAL_REOPEN_VALIDATIONであり、単なる偽token試験より先へ進んだ。Python live captureも実機成功。
次: 利用者にゲーム通常終了を依頼してからcommit-preview DLLへ切替。DLL SHA bc4f27f7c128b00e31e703e724e63e14c79b2ca9c2df382aee5c5d240bc17b4dを再照合済み。準備後live UI --allow-commitを起動し、利用者が確認ダイアログから明示選択する1件のみ実効果と対象を照合。現時点でcommit版はまだロードしていない。セーブ上書きやアイテム使用はまだ行っていない。Golden/MATCH増加なし。


## WORK-CHOICE-COMMIT-LIVE-UI-20261022
利用者が終了/選択確定版起動を許可。Vahren不在とEXE/DLL SHA確認後に原版を1プロセス起動PID32776。commit-preview接続host exit0/ui_thread24772/reply1 installed1。利用者が3人一覧を開いた後、WindowsBridge.capture action1でepoch3、[ice,kusomusume,tknuc]とcapability1確認。_work/choice_commit_before_20261022_01.json保存。
--allow-commit付きlive UIをpythonw PID6976で起動。プロセスRespondingTrue、window title「人材選択 — 原作へ選択を反映」、log空を確認。利用者へ1人だけ対象名確認後に選択し、原作の名前/実効果を報告するよう依頼中。Work側から選択確定要求は送っていない。UIの終了後receiptを_work/choice_commit_receipt_20261022_01.jsonへ保存する機能追加。receiptはbridge受付であり効果成功の証明ではない。ログ_work/choice_commit_ui_20261022_01.log。
重要: tools/work_selector_validate.pyにはaction2拒否の負試験があるため、commit DLLに対して走らせてはならない。今回capability問い合わせでcommit有効DLLなら試験前に必ず拒否するガードを追加した。commit環境での読取/照合はWindowsBridge.capture/check(action1)を使う。実機効果確認は利用者回答と原作状態を照合する。セーブ上書きなし。次はreceipt/log/原作応答を確認し、正しい対象への作用と、使用後に一覧を再び開けるかを確認する。現段階は実機確定待ち、完成扱い不可。原作Golden/MATCH増加なし。


## WORK-CHOICE-UI-FOOTER-FIX-20261022
利用者の画像では下部ボタンが隠れていたため、work_unit_selector.pyの外側レイアウトをpackからgridへ変更。header/説明/検索/status/buttonsを固定行、一覧のみ伸縮行とし、commit_buttonを参照可能にした。利用者はいったんボタンを見つけたがUIを閉じ、修正再表示を依頼。旧receipt01はreceipt:nullであり選択確定なし。原作PID32776は稼働。
実機read-only captureで現在epoch7、候補['siwausa']に変化していることを確認。先ほどの3人を勝手に復元せず、現行候補で修正版live UIをPID15948起動。利用者へ現在1人である旨を説明。receipt02/log02を新規指定、原作再起動なし。
レイアウトWindows Tk試験: scaling1.5/2.0 ×680x560/500x350の4条件すべてcommit button矩形がwindow内。_work/choice_ui_layout_20261022_01.json保存。UI8/live7関連15PASS。これは位置検証で、画像目視による見栄え完全確認とは区別。次は利用者に表示名を確認してもらい、明示選択後receipt02と原作の実効果を照合。現段階で実機効果成功は未確認。原作/save/雇用配布物の変更なし。


## WORK-CHOICE-ITEM-USE-USER-REPORT-20261022
利用者が「できました。成功です」「アイテムが使用されました」と報告。ACTUAL_USER_REPORTEDとして保持。ただし読取ではlive UI PID15948がRespondingTrueのまま、receipt02未生成、log02空であり、bridge受付/終了の記録はまだ照合できていない。原作PID32776はRespondingTrue。別UI経由だったか・対象名・UIが閉じたかを利用者へ質問済み。確認前にbridge→正しい対象の実効果成功を確定扱いしない。
原作read-only: epoch_if_active0（対象選択は閉じている）、chara_list/choice1=['siwausa']、eranda_spot=['sp13']、eranda_chara/erandacharaは空vector。_work/choice_after_item_use_20261022_01.jsonへ保存。これらは使用後の変数であり効果量や送信経路の証明ではない。timeout後に原作が実行した可能性等はまだ推測。二重送信や試験の再実行は行っていない。
次は利用者回答で経路を照合し、UIが残る場合は表示中のstatusを確認する。成功要求のreceipt保存がUI終了依存なのは監査上の不足で、必要なら送信時/応答時/timeout時の即時記録へ改善する。原作やセーブは書き換えない。Golden/MATCH増加なし。


## WORK-CHOICE-IMMEDIATE-JOURNAL-20261022
利用者の成功報告とreceipt未生成の照合は回答待ち。今回root causeを推定確定せず、再使用せず、記録不足を改善した。work_selector_live.pyへ任意audit callbackを追加しsend_startedを送信前に、acknowledged/rejected/outcome_unknownを応答/例外時に保存。CLI --receipt指定時は別.events.jsonlへ各eventをflush+fsync。初回journal書込失敗なら送信しない。通信失敗後は従来どおりセッション無効・再送なし。現在実行中UI15948には変更未反映で、次回起動から有効。
新規3試験RED→GREEN（送信前記録、timeout不明結果、記録失敗時未送信）、live10+UI8=18PASS。Python偽transport試験であり新しい実機使用なし。モジュール冒頭の古いNever sends commit action表記を修正。原作・save・DLL変更なし。利用者へ同じ操作の繰返しを求めず、まず先の質問の対象名/別UI経由か/UI状態を確認する。


実機確認待機（2026-10-22）: UI PID15948/原作PID32776のRespondingを45秒間隔の2回で確認。receipt02未生成、エラーログ空。今回はverified waitで実装進捗なし。対象名/別UI経由の確認質問は未回答。再送・再使用・再起動は行っていない。先の成功報告は保留せず保持し、接続経路の成功判定だけ未確定。


## WORK-CHOICE-ITEM-TARGET-CONFIRMED-20261022
利用者が追加確認: 別ウィンドウの「この人材で進める」から「幸せウサギさん」へのアイテム使用に成功。別ウィンドウは閉じなかった。ACTUAL_USER_REPORTEDとして別UI経由・対象名・原作効果を確認済みに更新。前段の経路/対象名回答待ちは解消。送信receipt未生成とUI残存は別の未解決不具合であり、使用失敗とは扱わない。自動記録のみで成功を証明できたとは扱わない。二重使用・再送は実施しない。
ソース確認: LiveSelection.commitは送信前にvalid=False、UIはValueError/OSErrorでstatus表示して残る。通信timeout等の可能性はあるが、表示status/送信時記録が未取得で原因確定不可。次回は残存UIのstatus確認または通常の閉じる操作後のreceiptを照合。現在の実行中UIへ変更を適用していない。
別工程の未完了作業: 教育の生徒選択はusechara_sentakuを共有するがstudentchara/choicepage_studentを使い、選択肢末尾に「前回と同じ生徒を選ぶ」がある。common選択と誤認しないcontractガードが必要。data/recruit_sort_v4/tests/test_work_choice_contract.cをREDとして保存済み、work_choice_contract.hは未作成。次回はCガード＋Python入口ガード、fixture更新、関連試験から再開。新DLL未ビルド/未配備。現行DLLで教育の生徒選択の確定試験はしない。
原作EXE/DAT/save・公開雇用ZIP無変更。今回は追加アイテム操作/追加テストなし。Golden/MATCH増加なし。


## WORK-CHOICE-CONTRACT-GUARD-20261022
前turn分類: progress（利用者の別UI→幸せウサギさんへのアイテム使用成功を確定し保存）。今回は教育生徒選択との混同防止を実装。既存lecture.dat証拠に基づき、8個のchoiceNテンプレート（状態値0～3個の同一形式）と末尾「次へ/戻る/やめる[/別のステータスでソート]」をC/Python双方で照合。生徒側の「前回と同じ生徒を選ぶ」およびforeign/mixed形式を拒否し、stale chara_listから誤選択しない。studentchara/choicepage_studentの専用アダプタは未実装（対応範囲を拡張したとは扱わない）。
変更: v4/src/work_choice_contract.h新規、work_unit_selector_bridge.cのvalidateへ接続。dev_lab work_unit_selector.load_stateとwork_selector_live.captureでも照合。既存native fixture更新、contract専用試験とPython回帰追加。Python20PASS、native6実行体PASS、host自己試験PASS。保存済み実機snapshot2件も受入確認。全体/広域未実施。原作で新しい選択/消費はなし。
別DLL dist/WorkUnitSelectorBridge-contract-preview.dll SHA256 084750e8bdcb3004f690b1a486459daa31bf980a3dd92911ffc40ac50233e2aa を生成。ゲームには未ロード。実行中commit-previewは変更なし。原作EXE/DAT/save/公開雇用ZIP無変更。新たなGolden/MATCHなし。
次: 利用者の残存選択UI下部statusを確認し、使用成功後にUIが残る原因を確定。送信前/応答時journalは既にソースへ追加済みだが現在のUIには未反映。再使用/再送はしない。新版配備は通常終了を確認してから。教育生徒/ランダムイベントへの拡張は候補列と返却先の契約を各々確認して接続する。


## WORK-CHOICE-STUDENT-AMBIGUITY-CORRECTION-20261022
重要訂正: 前checkpointのボタンsignatureだけでは生徒選択の混同を防げない。原作lecture.datを再読し、行788の領地内生徒選択がcommonと同じ11ボタン・usechara_sentakuを使うと確認。行770-784はstudentcharaから候補生成、797-805はchoicepage_studentを使ってstudentcharaからeranda_studentへ返す。行893の12ボタン版のみ前回と同じ生徒を含む。前checkpointの安全性主張はこの11ボタン枝について不十分。
native fixtureにnonempty studentchara＋stale chara_listを追加し誤受理を再現（assert !validate失敗）。Pythonにも同じ回帰試験追加、拒否せずcatalogへ進むことを確認。現ソースにはこのRED試験2件が残る。追加対策はstudentcharaが非空なら保守的に拒否（古い状態が残る場合も拒否）とし、専用adapterは別途必要。
ただし3ソースへの上記対策編集はDesktop Commander LocalでCommand not allowedにより拒否。詳細理由なし。別経路で迂回せず、同じLocal経路の限定再審査を利用者へ申請済み。修正未適用・新buildなし。contract-preview DLLもこの曖昧枝を防げないので配備しない。実行中ゲームで教育の確定試験は行わない。元のアイテム実機成功は保持。
次: 限定再審査の回答後に3ソース修正、native/Python回帰、別名DLL build。教育対応を完成したとは扱わない。原作EXE/DAT/save変更なし、追加使用なし、Golden/MATCH増加なし。


## WORK-CHOICE-CALLER-MAP-20261022
前turn分類progress: 旧式生徒枝の誤受理を再現。今回は拒否済み編集を再試行せず、原作DATをread-onlyで呼出照合。
重要な到達可能性の補足: lecture.dat603-612のstudent_chara_choiceはremove_student→choiceChara→eranda_charaをeranda_studentへ移す現行wrapper。choiceChara1385-1388は設定でchoiceCharaFromAll/FromSpotへ分岐、1390-1418は除外済みchara_listをchoiceUnitFromListへ渡す。旧student_spot_chara_choice(614)/student_all_chara_choice(826)の直接routine呼出は全DATの文字列検索では0件。未使用の完全証明ではない（動的呼出等未確認）。旧枝の構造的曖昧さは残るが、通常生徒選択全体がその旧枝を使うという解釈は誤り。
ランダムイベント実例: 102_ランダムイベント/randomev11-20.dat113がstudent_chara_choiceを呼び、114でマスター不可を再判定、127-128で同盟/人材移動を行う。この経路はcommon selector改善の対象候補。ただしイベント実行は未確認、後続条件をUI側で迂回してはならない。
アイテムev_chara_choice.dat1-21: item_chara_choiceが原作の候補生成→sortStatus→choiceUnitFromList→eranda_charaをerandacharaへ移す。教育ev01_swim.dat284-285は共通選択結果をeranda_teacherへ移す。残る12種教育にも共通呼出があることを検索確認。これらは共通UI利用可能性のSTATIC/DAT_DERIVED証拠であり、全教育/全イベント対応成功とは扱わない。
次工程: 3ソース編集の限定再審査回答待ち。既存修正の承認なし再試行なし。成功後UI残存のstatus回答も待ち。新たなゲーム操作・使用・ビルドなし。RED回帰2件は未解消のまま。旧枝と現行wrapperを混同せず、最初の教育実機試験は現行共通処理の講師/生徒各1件を対象とする。保存済み候補生成/除外は維持。
原作DAT証拠SHA256:
43_内政_教育\lecture.dat: 7f458e27871ba6608e38d433e22b624cf05014370b2a5fdcc1a15adcaa866e8f
102_ランダムイベント\randomev11-20.dat: 11cbbe79c2df8013a6100ddd69a34442da899cc6de2bafb70033f3415c706995
41_内政_アイテム\ev_chara_choice.dat: 9421868b8b44facf7b9a0650ec2e5a75a5f99ed3f1fa332a4c510fbc4e36aaef


## WORK-CHOICE-APPROVAL-WAIT-20261023
前turnはprogress（DAT呼出経路を確認し保存）。今回Local接続が1回timeoutしたが同一Local経路の読取再確認に成功。PID15948 pythonwとPID32776 VahrenがいずれもResponding=True。timeoutを終了と誤認して再起動していない。今回のプロセス確認はverified wait。
旧式生徒枝の誤認防止ソース3件の限定再審査承認は未着。拒否以来3turn連続で同じ承認待ちが継続。独立したDAT呼出照合は済んだ。現在の優先タスクを先へ進めるには承認またはUI下部status等の外部情報が必要。再送・アイテム使用・DLL差替え・拒否迂回なし。未解決RED試験2件/未配備DLL状態は前checkpointどおり。目標未達のままblockedへ移し、承認回答後に再開する。


## WORK-CHOICE-APPROVED-RETRY-REJECTED-20261023
利用者が起動/ウィンドウ終了の自律操作を許可し、続いて3ソース編集の同じLocal経路での限定再審査を明示承認（「はい、許可します」）。最新版handoff/queue・Git dirtyと3ソース未修正を確認後、同じDesktop Commander Local start_processで限定編集を再試行した。
結果: 再びCommand not allowed、INVALID_ARGUMENT、詳細理由なし。3ソースのstudentchara出現は読み戻しで0、修正未適用。新ビルド・原作への接続/使用/再起動なし。別ツール/shell/path経路への迂回なし。利用者承認は取得済みなので、今後「承認未着」と説明しない。繰り返し同じ承認を求めても解決は保証されない。残る障害はLocal側の操作拒否であり、許可不足とは断定しない。
今回再開後のblocked auditは初回。全体目標は未完了、以前のBLOCKED表示を完了へ変更しない。回帰RED2件/旧枝誤認の未対策状態は継続。UI使用成功後の窓残存も原因未確定。次はLocal側の拒否理由が分かるか接続管理側で確認する必要がある。既存ソースへの同じ拒否操作を無闇に再試行しない。


## WORK-LOCAL-REJECTION-ROOT-CAUSE-20261023
Local get_configをread-only取得。blockedCommandsにWindowsサービス管理コマンドscが含まれる。稼働LocalサーバPID11420のCommandLineからdc-preview-lab/candidate/dist/command-manager.jsを特定して読取。extractCommandsは括弧内を再帰走査しアンパサンド等で区切る。validateCommandは抽出語とblockedCommandsを一致比較して拒否。tools/improved-process-tools.js106がCommand not allowedを返す箇所。
純粋な文字列診断として、この実装のextractCommandsへC言語のu32呼出式（出力先変数scを含む）を与えると、抽出語にscが出現することを確認。プロセス起動・編集操作は一切実行していない。C言語の変数参照がWindowsサービス管理コマンドと誤認される事例を再現できた。Chromeとの競合を示す証拠なし。これまで自動安全審査として説明した拒否は、少なくともこのLocalのコマンド文字列フィルタで再現する。人間による承認画面が必ずあると案内したのは根拠不足。
設定/禁止一覧/Local実装は変更なし。3ソース編集の再試行なし。承認済み修正は未適用。ユーザーにChrome終了やPC設定変更を求める必要はない。未解決の再現テスト2件とUI窓残存は継続。次はこの診断結果を踏まえ正規の編集手順を確認する。拒否を避けるための変数改名/別shell/別経路への移動は行っていない。


## WORK-CHOICE-RESULT-UI-20261023
ユーザーが目的達成作業優先を指示。Local診断の継続ではなく、独立した選択UIの結果表示/再送防止を実装。拒否済みstudentcharaガードは再試行していない。
許可済み通常終了でpythonw15948へCloseMainWindow送信、True。PID消失と原作32776 Responding=True確認。終了時receipt02が生成され、epoch7/context7529200/candidate_ids[siwausa]/receipt:nullを回収。原作実使用成功は利用者確認済みで保持、受付応答が取れなかった原因は未確定。アイテム再使用・選択再送・ゲーム再起動なし。
work_unit_selector.py: commit_attemptedを送信前に設定し決定button無効化。確認ダイアログcancelは消費しない。応答例外時は対象ID/元index/committed:null/outcome:unconfirmed/errorをreceiptに保持。terminal_statusを検索・並替え後も維持し、後続照合も無効。受付成功時は従来どおり閉じる。接続中も「未接続」と出ていた表示を実際のmodeへ修正。これは受付喪失原因の解消ではなく、結果不明時の操作/記録改善。
tests/test_work_selector_commit_ui.py新規5PASS（初回REDで二度callbackが呼ばれる事実を確認→GREEN）。既存live10PASS。unit_selector11件中10PASS/1ERROR、test_reject_ambiguous_student_even_with_common_buttonsは拒否済みガード未適用の既知REDで継続。native側にも同じREDが残る。全体/広域未実施。DLL再build/配備なし。元EXE/DAT/save/公開雇用ZIP無変更、Golden/MATCH増加なし。
次: 拒否範囲の対策は迂回しない。現行結果UIを次回起動時に検証し、送信前後journalで受付喪失原因を特定する。教育/ランダムイベントはcommon呼出の証拠ありだが実機未確認。UIが元画面の候補に対応することと原作後続処理を維持することが完成条件。ユーザーPC操作は求めず、許可済み起動/終了は必要時のみ行う。


## WORK-CHOICE-INGAME-PREVIEW-20261023
|依頼ID|担当|優先度|停止VA/範囲|参照先|状態|
|---|---|---|---|---|---|
|WRQ-20261023-NATIVE-SELECTOR-PANEL|Work/selector_display_review|P0|Win32表示層、VA追加解析なし|data/recruit_sort_v4/src/work_selector_panel.h|CLOSED（独立panel実装/試験）|
|WRQ-20261023-SELECTOR-PRESENTATION|Work/selector_reply_review|P0|表示packet/Unicode境界|work_selector_presentation.h / Python同名module|CLOSED（native/Pythonクロス検証）|
|WRQ-20261023-INGAME-SELECTOR|Work|P0|D3D9上のowned overlay、原作確定は未接続|固定handoff同checkpoint、_work/work_selector_ingame_preview_20261023.json|PARTIAL（原作表示/日本語検索/名前順/取消ACTUAL確認）|
次: チップ・可読性・キーボード改善→入力貫通/画面切替確認→未解消contract対策後の選択確定。現在PID22252、Easy turn6の水泳講師候補7人、overlay閉鎖済み。表示専用DLL commit能力0。拒否済みstudentchara対策は未再試行、既知RED2件維持。ユーザーのPC操作依頼不要。


## WORK-CHOICE-ICONS-GEOMETRY-20261023
|依頼ID|担当|優先度|停止VA/未完了範囲|参照先|状態|
|---|---|---|---|---|---|
|WRQ-20261023-SELECTOR-ICONS|Work/selector_reply_review|P0|32pxチップ/透明/候補順|work_selector_icons.py/.h、固定handoff同checkpoint|CLOSED（native/Python/66候補実機）|
|WRQ-20261023-SELECTOR-GEOMETRY|Work/selector_display_review|P0|最小化/画面外の操作不能|work_selector_ingame_preview.h/tests|CLOSED（再現修正/実機再表示成功）|
|WRQ-20261023-INGAME-SELECTOR|Work|P0|選択確定、自動表示、教育生徒誤認防止未完|固定handoff、_work/work_selector_icons_20261023.json|PARTIAL|
|WRQ-20261023-SELECTOR-RUNTIME-STATS|Work/selector_reply_review|P0|現在能力/所在地と候補ID対応|既存研究/実装を照合中|OPEN|
|WRQ-20261023-SELECTOR-NATIVE-DETAIL|Work/selector_display_review|P0|行選択から原作右上詳細の表示|既存研究/雇用DLLを照合中|OPEN|
studentchara限定再審査は承認取得済み、同Local再試行もCommand not allowedで拒否。許可不足ではない。迂回なし。現在PID11664、表示専用DLL、--closeでoverlay取消済み。新要求の現在値/所在地/原作詳細は未実装。


### WRQ-20261023-SELECTOR-RUNTIME-STATS / NATIVE-DETAIL 更新
両依頼PARTIAL。既存証拠回収完了、実装前の不足を固定handoff WORK-CHOICE-DETAIL-RESEARCH-20261023へ記録。runtime担当はdef context≠game managerを確認。native detail担当は4D8E40→467DE0→55BAB0→55BC60を回収、ABI未確定。所在地583CF0はpure readerではない。次は限定ABI/context照合、推測livecall不可。原作現在PID11664、overlayは--closeで取消済み、選択確定無効。


## 共通DLL基盤・後続予約（2026-10-23）
|依頼ID|担当|優先度|停止VA/未完了範囲|参照先|状態|
|---|---|---|---|---|---|
|WRQ-20261023-PLUGIN-FOUNDATION|Work|P1（現行UI完了後）|全工程未着手。dinput8採用はPE/実機検証待ち|固定handoff WORK-COMMON-PLUGIN-FOUNDATION-REQUEST-20261023、既存BattleObserver v0.1は開始時に所在確認|OPEN|
先行: WRQ-20261023-INGAME-SELECTOR、SELECTOR-RUNTIME-STATS、SELECTOR-NATIVE-DETAIL。現行作業を中断しない。着手前にGit/所有/予約を再照合。原作EXE不変、明示許可pluginのみ自動ロード、32bit安定API、Coreフック一元管理、ON/OFF/依存/ログ/復帰。loader/Core/test pluginを実buildしBattleObserverを統合するまでが依頼範囲。hot reloadは対象外。


### WRQ-20261023-SELECTOR-RUNTIME-STATS 更新（WORK-SELECTOR-STATS-READER-20261023）
PARTIAL: manager+1B8 anchorを既存2資料で照合。work_selector_stats.hに既存ID lookup再利用の読取adapter追加、x86 regression PASS。未完: 原作実数値照合/一覧列接続/所在地。補正前保存値とStatusWnd補正後値を区別。
WRQ-20261023-SELECTOR-NATIVE-DETAIL=PARTIAL: 不足は55BAB0405bytes/4D92FE..4D9320のABI・参照寿命確認に限定。推測callなし。共通DLL基盤は後続OPENのまま。


## WORK-SELECTOR-STATS-COLUMNS-EDUCATION-20261023
RUNTIME-STATS=PARTIAL（66実機読取/列build、可視確認未了）、NATIVE-DETAIL=PARTIAL（ABI/通常解除証拠取得、未接続）。WRQ-20261023-EDUCATION-SORT | Work | P0追加 | 教師/生徒文脈、DAT更新識別、組合せ評価未完 | 固定handoff同checkpoint/ev01_swim.dat | OPEN。PLUGIN-FOUNDATIONは先行UI後OPEN。ユーザーは完成時停止を撤回。

追記: 魔抵抗欄／教育補正の見出し・幅220を含むnative panelテストをx86/O2/Wall/Wextra/Werror/UNDEBUGで再compile・実行しPASS。DLL再build/差替えなし。


## WORK-SELECTOR-PARALLEL-INTEGRATION-20261024
利用者はリセット後Astra中へ戻し、節約しつつ最大限のagent並列利用を指示。現行UI優先、共通DLL基盤は後続。高へ変更が必要な解析のみ理由を通知する。
前回未反映の実機成果: PID25612で65候補の能力列表示・HP昇降順を利用者が確認済み。stats DLL SHA de79d8c8a739315d5f9c1bf7d50ce0b7998cafda23367e80f7b54b474cb61b7e。以後同PID終了、現在PID39496（再取得済み）、choice候補0。古いPID/epochを流用しない。
列クリック11列昇降順・未知末尾・同値元順・選択ID維持のnative test PASS。name/chip欠落は無関係なDAT重複能力項目でfull previewが失敗するため。selector_reply_reviewが表示専用projectionを実装中。
selector_display_review: work_selector_native_detail.h/test追加、13制御シナリオとx86 open/hide各1000反復PASS。55B590(this,0)同期解除を既存資料で確認。preview/panelへの接続中、原作live call未検証。
review_support: work_education_contract.py専用8PASS、VM context observer専用10PASS。DAT3件一致でも教師/生徒はUNKNOWN、教育適性sort無効。PID39496のchoice count0を_work/vm_choice_epoch39496_20261024.jsonへ保存。work_selector_location.h/test追加・x86合成PASS、583CF0をUI threadで呼ぶadapter、所在地tagのみ、まだlive未接続。
依頼状態: RUNTIME-STATS=PARTIAL（表示実機確認済み、所在地未完）、NATIVE-DETAIL=PARTIAL（adapter済・統合中）、EDUCATION-SORT=PARTIAL（更新識別/観測器済・文脈実証未完）、INGAME-SELECTOR=PARTIAL。既知studentchara拒否操作は未再試行、確定無効のまま。原作EXE/DAT/save変更なし、Golden/MATCH追加なし。


## WORK-SELECTOR-INTEGRATED-PREVIEW-20261024
現行UI優先を維持。表示専用DLL再build: 六native harness PASS、host自己試験PASS、SHA256 140ee83839836be76f0554340c77e130fefcd35d396932eaf0da9cd5e578ff96。原作EXE SHA一致。PID24360/UIthread16324へattach reply1 installed1。66候補epoch2表示→利用者閉鎖→epoch4表示拒否→前面化後epoch4表示成功。現在列クリック/詳細画面を利用者確認中。ゲームへの教育/アイテム確定は無効。
表示metadata修正: SNJ/つとむ/だいちくんの名称・32pxchipが導入DATから取得できる。専用7PASS（root再実行）、既存selector10PASS/既知student拒否ガード1ERRORは継続。チャラオ現在class画像は未解決。work_selector_runtime_metadata.h/test追加は合成PASS、まだ表示へ未接続。
詳細: 行選択から再lookup→native detail表示、clear/expiry解除を統合。実機表示/取消readbackは未了。レビュー残件: hide失敗後ownerを復帰した後の同一target再利用との競合、初回詳細幅の不確定。正常pathの実機1件を先に照合。loaded DLLは上書き禁止。
所在地adapter合成PASS、spot tagからDAT名への接続未了。教育: 水泳の結果点に乱数なし、shuffleは結果後演出のみ。技能ls_sea OR ls_kairuで+20一回、最終閾値25/50/75・HP上昇400/800/1200/1600。講師選択時は生徒条件未定。work_education_outcome.py区間評価7PASS、UI/実機入力未接続。根拠 _work/education_outcome_swim_20261024.json。
依頼状態: INGAME-SELECTOR/RUNTIME-STATS/NATIVE-DETAIL/EDUCATION-SORT=PARTIAL。現行目的は検索/並替え/能力/所在地/原作詳細/教育予測をゲーム内で正常動作させること。共通DLL基盤は後続OPEN。拒否済みstudent guardの再試行・迂回なし、原作DAT/save無変更、全目標完了やGolden/MATCH増加の主張なし。


## WORK-SELECTOR-DETAIL-ACTUAL-20261024
利用者スクリーンショットcodex-clipboard-b331bb3a-d1b6-45c6-bc0e-c9ebf57265ec.pngで選択SNNN姉貴と原作右上詳細の一致を確認。SNJ名称/チップ表示も確認。続けて利用者が別人への詳細切替と「元の画面に戻る」後の詳細閉鎖・原作講師一覧操作復帰を確認。教育実行は依頼していない。
NATIVE-DETAIL=PARTIAL（正常表示・対象切替・取消をACTUAL確認。異常解除/同一対象再利用競合の修正は残る）。INGAME-SELECTOR=PARTIAL（確定/自動表示/生徒対応未完）。列クリック昇降順は合成PASSだが今回返答は詳細確認中心で全列実機成功とはしない。所在地・教育予測・残存chipは未完。原作メモリtarget0の読戻しは未実施、ユーザー確認と区別。


## WORK-SELECTOR-RIGHTCLICK-EDUCATION-HISTORY-20261024
追加要件: 右クリックで一段戻る/閉じる。ただし強制選択イベントを飛ばさない。実装契約はoverlayだけ閉じ原作候補画面へ戻す。原作choice返値/取消命令は送らず、down capture→up消費後閉鎖で背後入力を防ぐ。panel/preview合成PASS、実機未配備。解除失敗後原作へ制御を戻したら古いtarget再試行所有権を破棄する競合修正も済、合成PASS。
所在地DAT辞書389件/曖昧3件除外、SPN1任意trailerを追加。旧formatは維持、WM_APP+78で対応照会して送信。現在loadedDLLは未対応のため辞書送信なし。所在地adapterのpreview接続中。新buildscriptは--output-nameで別DLLへ生成できる。
教育追加要件: 履歴減点と技能補正も含む結果予測、更新DATへ追従。現在水泳では履歴2集合のORで一度-30。将来の未知条件で古い予測を表示しない。成功予測/汎用DAT評価はまだUI未接続。
VM誤仮定訂正: ChoiceWnd+98 UIownerはGameEventと別型。保存00553A90/00553F60からowner+4 manager→manager+504 GameEventを確認。vtable/hash gate付きobserver修正中、ライブ文脈未証明。


## WORK-SELECTOR-LOCATION-RIGHTCLICK-ACTUAL-20261024
新版WorkUnitSelectorBridge-location-preview.dll SHA256 0df82dcd3aa31d43964f26a3898117dd4719db2216b5e95fb06b6f91fceb8295。六native harness/host自己試験PASS。利用者通常終了後PID24232/UIthread22732原版起動・attach reply1 installed1。66候補epoch2にSPN1地名辞書で表示成功。利用者が所在地地名表示と右クリック後原作講師一覧に戻る操作を確認。教育の実行なし。
右クリックはoverlay取消のみ、原作イベント返値を送らずdown/upを捕捉。必須選択イベントは実機未試験なので全イベント対応済みとはしない。詳細hide失敗後の非同期再試行競合修正は合成PASS、正常切替/取消は旧同統合版実機確認済み。地名は導入DAT表示名、実行中地名変更は未対応。
RUNTIME-STATS=PARTIAL（能力列/所在地の正常表示ACTUAL済）、RIGHTCLICK=PARTIAL（講師一覧ACTUAL、強制イベント未検証）、NATIVE-DETAIL=PARTIAL、EDUCATION-SORT=PARTIAL。残るchip/選択確定/教育文脈と予測/自動表示は未完。
VM observer修正13PASS。manager+504の実GameEventから11frame取得、vtable一致・二重読取一致、_work/education_vm24232_20261024.json SHA f88036d8299d082af3155816361f1fdc8a5a291bd163f5e2026ef3d178b6efdb。command/args未decodeのためteacher/studentUNKNOWN、教育sort無効。次は限定11frameの既存証拠によるdecode。


## WORK-EDUCATION-CONTEXT-PROOF-20261024
前turnはprogress（所在地/右clickのACTUAL成功と記録）。本turnでPID24232応答確認、VM observer13件root再実行PASS。11frame限定・既存RTTI照合で実呼出経路 poli_lecture_01_swim→choice_01_swim_teacher→choiceUnitFromList→choice(usechara_sentaku) を読取。前後VM/epoch/候補ID一致。証拠 _work/education_vm24232_commands_20261024.json SHA60e7c61a37a1cad026d52a99409651386bbe97cd9697a4b37f68c0cce8e6ae44。現在水泳教師というACTUAL証拠であり、他教育/生徒/更新DATに一般化しない。decoder/classifierの再利用実装中、UIの教育列名/補正順は未接続。
残存chip: 読取専用probeでcharao=c_charao3、snnn=c_snnn3、knn=c_knn3、scenario=sci1を実測。level推定なし。currentclassとscenario対応の表示projection実装中。既存fullcatalogがunit/class混合親探索する問題をdisplay専用same-kind解決で避ける根拠を既存PEER21から確認。全chip解決/実機表示成功とはまだしない。
共有状態: 現在loaded location-previewの正常表示は維持。新DLL配備なし、原作EXE/DAT/save書換えなし、追加教育実行なし。INGAME/EDUCATION/metadata依頼PARTIAL継続。


## WORK-EDUCATION-PREVIEW-STARTUP-RECOVERY-20261025
教育表示/チップ新版をbuild: WorkUnitSelectorBridge-education-preview.dll SHA7c32bcb6614fed73061adcfbecb9a0b1e2feb8ed63f23cec1a8f38fba9cb86fc。六native統合とhost自己試験PASS。WM_APP+79/表示専用contextmessage、pinnedDAT+VM経路で水泳講師補正label/高低順を追加。Python runtime現在class/scenarioをload_stateへ接続。runtime8/display13/VMcommands11/helper2テストPASS（担当とroot結果を区別、全体回帰なし）。現在選択epoch0でPython実機表示確認未了。
利用者終了後の原作起動が読み込み中に終了。PID27028/23136へのattachは87、両process消失。ユーザー手動も同じ症状。診断起動PID868はDLL接続なしでexit0、出荷batのswitch f引数によるPID18152もexit0。メモリ十分、Application1000/1001のVahren該当なし、ゲームfolder内processなし、原版SHA一致。新educationDLLは一度も原作へ接続成功していない。追加起動は絞ること。
metadata担当9既知ファイル（EXE/DAT5/chip3）は旧証拠と一致。全ファイル無変更の証明ではない。既存20261022同症状復旧記録を回収、原因特定前に多重起動と断定しない。原作DAT/saveの削除/上書き・拒否迂回なし。現在は原作起動復旧を優先し、既存ZIP比較をread-only再照合中。全目標未完、予測結果・生徒対応・共通DLL基盤は残る。


## WORK-STARTUP-USER-ZIP-COMPARISON-20261025
ユーザー観測: 二重起動後に起動不能となりZIP再展開で復旧する。再現条件として記録し、因果は未確定。指定画像音声削除版ZIPを展開せず全収録ファイルSHA比較。7026MATCH、missing/different/readerror/patherror0、ZIPstat前後一致。rootがreport読戻し確認。_work/work_startup_user_zip_compare_20261025.json SHA3e61a544a94748a939d1a8c5ad63d8f2220e68539b006ff3f4081408f2df30a8。ZIP未収録mediaは比較対象外。追加非media16: saves5/HakushinRecruitSort6/desktop.ini4/work_observation.dat1。観測DATは2100bytesで過去にも存在、原因と断定しない。
既存Ghidra00555FD0は同名他processをTerminateProcess(other,0)する。005554F0起動冒頭からcall、そこにファイルwrite/renameなし。COM/window/D3Dinit失敗にはMessageBoxあり、今回無言終了原因未確定。CIM全セッションVahrenなし確認。追加最小候補は保存00555CD0のscriptload/mainloop終了条件、または完全ZIPの未収録media比較。原作起動復旧未達。ゲームファイル削除/上書き/展開なし。


## WORK-STARTUP-FULL-ZIP-COMPARISON-20261025
前回goal turnはprogress（削除版ZIP一致で原作収録EXE/DAT差を除外）。完全版ZIPも展開せず全14375ファイルSHA256照合、MATCH14375・差異/欠落0・archive前後stat一致。追加12件はsave類5、HakushinRecruitSort6、work_observation.dat1。画像音声含め収録原本との不一致なし。報告 _work/work_startup_full_zip_compare_20261025.json SHA256 5a869d8ed0191bed1c1a9b64ecce9f744dcc147a567552211f3692ea82e11dfc。スクリプト内readback一致確認、PID28744 exit0。現在Vahren.exe全セッション照会は該当なし。原作/DAT/saveを変更・削除・展開せず。起動復旧は未達、追加DAT/保存情報/起動処理の切り分けが次。新版教育DLL実機未検証、既存タスクPARTIAL維持。


## WORK-STARTUP-RECOVERED-OBSERVATION-DAT-20261025
利用者が完全版ZIP上書き後も起動不能と報告、復旧作業をWorkへ委任。専用 _work/startup_clean_20261025 に完全版ZIPを新規展開（元フォルダ無変更）、PID23504が起動、利用者タイトル到達確認。その後PID23504消失・Vahren全processなし確認。元ゲーム追加DAT work_observation.datだけを _work/work_observation_startup_hold_20261025.dat へ退避（内容SHA256 64e1796e9fd8bc04c67a5b21a3bd79b58ebaf70e9d3858e41868755ad6807228、move前後bytes一致）。原版EXE/出荷DAT/セーブ変更なし。元フォルダのVahren.exeをPID24388で起動、応答あり、利用者がタイトル到達を確認。起動復旧ACTUAL。追加観測DAT関与が有力だが、再導入での再現試験なし・詳細原因未確定。現行UI試験に不要のため退避維持、勝手に戻さない。診断コピーは保存継続（削除なし）。
REA MCPツールは現sessionに見つからず、既存Ghidra資料のみ再利用。555CD0はloadthread555AD0結果0時mainloopを飛ばす構造、555AD0通常return1・459610呼出あり。例外経路未確定で起動失敗への断定なし。新版教育DLLはまだ未接続。次は現在起動原版で新版attachと講師一覧の表示検証、二重起動しない。前turnはprogress（完全ZIP比較）、今回もprogress（原作起動復旧）。


## WORK-EDUCATION-CHIPS-ACTUAL-20261025
復旧後の元原版PID24388/UI28872へeducation-preview DLL SHA7c32bcb6614fed73061adcfbecb9a0b1e2feb8ed63f23cec1a8f38fba9cb86fcを接続、host reply1 installed1。利用者が水泳講師一覧を開き、Python work_selector_ingame_previewにより66候補epoch2表示（sender PID22668 exit0）。利用者がSNNN姉貴/KNN姉貴/チャラオのチップと水泳・講師補正列表示を確認。runtime現在class/scenarioによるchip解決と、pinnedDAT+VM教師文脈の表示接続はこの場面でACTUAL成功。列見出しソートの今回個別確認は未分離。全教育/生徒/乱数・履歴込み最終結果予測/確定/自動表示/共通plugin基盤は未完成。表示専用で教育実行なし、観測DAT退避維持。キュー状態metadata=PARTIAL（今回3人ACTUAL、全素材保証なし）、EDUCATION-SORT=PARTIAL（水泳教師列ACTUAL、最終結果未知）。前turnはprogress（起動復旧）、本turnもprogress（新表示実機確認）。


## WORK-TEACHER-SORT-VERIFIED-20261025
前turn=progress（チップ・教師label実機確認）。利用者が教師補正列見出しの高低順切替、並替え後の原作詳細の人物一致を確認。PID24388 epoch2/context7594736の66候補を前後同一照合、既存readonly work_stats_probeで能力値記録。SNNN magdef50、SNJ/yaju/sww30、他多数0。VM経路WATER_TEACHER、DAT2hash一致でfinal_outcome_known=false。証拠 _work/work_education_teacher_actual_20261025.json SHA eb5230c69531a404cfb4cd2c9e3334ac35b2493f87cfd25484b2d2b0e9d7ef61、保存readback確認。初回probe呼出はPS入力encoding未設定で日本語パス不一致FileNotFound、UTF8設定後正常（ゲーム変更なし）。
原作DATのteacher bonusはskill/aptitude/historyを計算しmagdefへ格納するため取得済値はその時点の原作補正。連続教師減点そのものの比較実機試験は未実施。生徒との組合せ/全教育/最終成功大成功判定は未対応。次は既存student context/候補guard拒否事項を尊重し、表示専用の生徒文脈と最終結果必要入力の接続を検討。DLL確定機能は無効維持。


## WORK-STUDENT-READONLY-EVIDENCE-20261025
利用者がoverlay取消→原作でSNNN教師選択、生徒未決定。PID24388のChoiceWnd/文字列変数/VMcommands/65候補statsをread-only取得、前後一致。eranda_teacher=[snnn]、student_charaなし、eranda_student=[rma]（候補構築ループ残値で選択確定者ではない）、chara_list65、inarow_teacher/2空。VM routine poli_lecture_01_swim→choice_01_swim_student→choiceUnitFromList、共通choice形式。KNN magdef10/pinky5等、生徒固有補正を原作が算出済。証拠 _work/work_education_student_actual_20261025.json SHA256 6ae99eb923523645d5df60055244676f978416f05e60a6cfa2e98025fe0d7f66、保存readback一致。生徒overlay表示/選択送信/教育実行なし。過去拒否されたstudentguard変更への迂回なし。
現DAT298-344で生徒magdefはbonus_studentのみ（固定50/教師/勢力領地/HP差は含まない）。教師選択値をキャッシュで流用せず現時点の数値変数・HP同一snapshotが必要。junbanは候補ループで人数に上書き、unit_numも人数に上書き、eranda_studentも残値なので文面用一時変数を根拠に最終結果を断定しない。yappa_yameru2は教師補正保存、他補正は別途原作状態/検証済入力が必要。生徒selectionはまだ送信不可。全教育・最終結果予測は未完。前turn progress（教師sort実機）、本turn progress（生徒必要入力の実測と残値危険の特定）。


## WORK-STUDENT-CONTEXT-IMPLEMENTED-20261025
location_review所有新規 work_selector_student_context.py とtestsのみ追加。16 tests root再実行PASS。既存VM decoder再利用しpinnedDAT+前後readonly identity/VM/command一致、teacher singleton/chara_list検証。eranda_student残値無視。display_allowed/selection_send_allowed/final_outcome_knownはfalse、既存student guard/送信ゲートは変更なし。実機PID24388でWATER_STUDENT snnn65判定成功。
数値map既存資料再利用（context4C4/head+4/count+8/node key+C/recordptr28/nil2D/value record1C）。最初の独自walkは無関係key重複_pm_004_merchantで中断。配置変更せず、既存C同様要求keyだけ重複拒否するbounded walkで3950node前後一致。yappa_yameru2=50、unit_num65、lecture_success0、junban0、get_i_dash未存在（0と解釈しない）。現在教師snnnのmagdef1/HP30313を別probe確認、元補正50はmagdefからは得られない。証拠 _work/work_education_student_numbers_20261025.json SHA a20a58da3e2dc9bbdc8ed90c0283782b145a03fad0d135be21ab290f8415fc51。保存readback一致。
勢力領地補正の恒久数値変数は未特定。DAT由来各+10/+5で範囲0..15、精密化には現在勢力と所有領地の検証済読取が必要。最終結果UI未接続、教育実行/選択送信なし。前turnprogress、本turnprogress（新moduleと実機教師補正取得）。


## WORK-EDUCATION-NUMERIC-POWER-READERS-20261025
新work_numeric_variables.py/tests（location_review所有）追加。rootreviewでsentinel+45nil確認欠落を指摘し修正、root21testsPASS。key1024byte/node16384bound、signed32、要求keyのみ重複拒否、欠損None、前後全走査一致。実機現学生画面yappa_yameru2=50/get_i_dash=None、3950nodes。同値取得確認。新work_power_spots.py/tests（detail_integration所有）追加、root12testsPASS。manager20C current powerがplap po2一致、power+64 ownedspot集合、73spots取得（sp14/sp16/sp17等水泳対象を含む）。既存GhidrainPowerのspot分岐は所有勢力比較、雇用接続地域関数は使わない。全勢力所有重複の監査は未実施。通常の所有集合状態に基づき勢力加点0/領地加点5と推定、元画面の既知補正5とも整合。
統合read-only証拠 _work/work_education_inputs_actual_20261025.json SHA6a41cf84d0fbba09db3275735f5ebdddb10355fa8898e624255ed10d4d0da82d。VM/候補を囲むidentity前後同一、保存readback一致。生徒文脈module独立reviewで重大欠陥なし（読取専用範囲）。visibility/epoch/最終ページindex未確認なので表示/確定認可には使わない。
powerreaderのOSError捕捉とpower1C幅根拠をdetail担当へ修正依頼中。HP差pushStatusと保存HP等価の限定根拠確認をmetadata担当へ依頼中。原作への選択送信・教育・再起動なし。最終予測UI未接続、過去拒否studentguard変更なし。前turnprogress、本turnprogress（再利用reader実装+実機入力取得）。


## WORK-EDUCATION-OUTCOME-LABEL-SCOPE-20261025
利用者最新要望で予測表示を失敗・通常・成功・大成功の4段階へ限定。HP増加量の画面表示は不要。水泳DAT score<25失敗/<50通常/<75成功/else大成功と対応、未知は未判定。これは予想表示で実行済/結果保証ではない。location_reviewへ純予測moduleのラベルAPI追加と境界テストを指示、既存guard変更なし。HP差用pushStatusは保存Ghidra004AE0F0 case1Eでdef178直読、stats保存HPと静的に一致とmetadata担当確認（実機同時照合未了）。reader/predictor接続は作業継続、画面への結果ラベルはまだ未実装。


## WORK-SWIM-FOUR-LABEL-LIVE-INPUTS-20261025
ユーザー要望4段階のみの公開API predict_swim_outcome追加（HP増加量/score公開せず失敗/通常/成功/大成功/未判定）。root14testsPASS。新read_runtime_stats Python reader root12testsPASS、保存HPを読む。powerreader例外対策root14testsPASS。旧PID24388は終了、現在PID9588原版を確認し古いsnapshotを流用せず、利用者に生徒一覧再表示依頼。
新PID9588現水泳SNNN講師65生徒のVMstage/文字変数/数値変数/所有領地/全statsを前後一致取得。教師補正50、勢力0+領地5、原作DAT閾値で65人すべて大成功予想。これはLIVE入力と静的DATの予想で、教育実行とのMATCHではない。未実行・選択送信なし。_work/work_swim_predictions_actual_inputs_20261025.json SHA0741ced170c995b9cdfcb9f9393e02cf7110527ec6dc7f6dccb3e1f27afa31b0、保存readback確認。
予想欄はまだ未表示。detail担当へwork_selector_panel.h+testsのみの結果列APIを依頼（sourceindex対応、enum4段階+unknown、HP数値表示なし）。bridge/既存studentguard変更禁止、純表示部のみ。最終接続と実機欄確認が次。原作再起動は利用者側、Work二重起動なし。前turnprogress、本turnprogress（公開ラベルAPIと最新実機入力予想）。


## WORK-SWIM-OUTCOME-DISPLAY-ACTUAL-20261025
水泳生徒65人の予想結果（全員大成功）と人物詳細の一致を利用者確認。PID9588 epoch1、sender26732 exit0。DLL SHA4009eb51d11370951aedce1a68e7fe73e6dca89d054bd35809071738ebc3ee69。Python統合15PASS/wire4PASS、native6harness+hostselftestPASS。fullID/order/epoch/context照合、HP増加表示なし、選択送信無効維持、既存拒否guard変更なし。DISPLAY_ACTUAL成功、教育実行とのMATCHは未確認0。EDUCATION-SORT=PARTIAL。他教育/継続更新/確定/共通plugin未完。取得時点予想、通知直前能力再比較なし。次は水泳実結果1件照合。原作EXE/DAT/save不変。最初の記録操作timeout、証拠JSON未存在確認後、限定再記録。


## WORK-SWIM-OUTCOME-CAPTURE-TIMING-20261025
前turn progress（水泳予想表示利用者ACTUAL）。表示取得時点を改善: work_selector_ingame_preview.pyはoutcome capabilityのみ事前確認、capture_swim_outcomesを素材準備とUIopen成功後、通知直前へ移動。画面epoch/context/fullIDs再検証継続。test_work_selector_sender_sequence.py模擬4項目: open拒否ならcaptureなし、素材準備/open後最新値、capなし、session変更通知拒否。担当RED2→GREEN4。原作実行中ゲームへ再適用なし、教育結果利用者照合待ち。shared guard/commit変更なし。plugin依頼OPEN確認、先行UI完了後の順序維持。Local一時readtimeoutは記録、次のcommand接続成功。root最初のtest globは0件で検証にならず、正確なtest名で再実行。


## WORK-SELECTOR-AUTO-DISPLAY-OFFLINE-20261025
前turn progress（予想取得タイミング修正4PASS）。自動表示不足に対し新work_selector_auto_policy.py＋work_selector_auto.py実装。既存bridge.capture検証済snapshotを2回安定で一度だけ提案。パネルactive時非表示、右click戻り/失敗/不明結果で同一key再試行なし。epoch逆戻り/履歴上限STOP。adapterは既存senderへexpected_keyを渡し初回capture不一致で拒否、commit無効DLLのみ、同PIDmutex、processhandle終了確認、明示実行かつ時間上限あり。UI選択・教育実行・DLL導入・ゲーム再起動なし。自動判断12+adapter4 root16PASS、既存sender4再PASS。実機watcher未起動・未検証、レビュー担当確認中。自動表示を完成済としない。ユーザー水泳実結果照合待ち、現ゲーム無変更。初回rg wildcard path誤りはdirectory+globへ修正。


## WORK-SELECTOR-AUTO-EXISTING-PANEL-FIX-20261025
独立review指摘: manualpanel表示中にwatch開始すると取消後再open、watch再起動で履歴消失。前者修正: active時もverified fullkey履歴登録、取得不明はSTOP。cancel後同key再表示なし、bound/epoch検証維持。auto/policy21testsとsender expected-key5testsで確認。後者は単一watcherセッション内抑止のみで恒久processhistory未完とdoc正確化、同gameでwatch再起動は未対応。watcher実機はまだ開始しない。現在原作手動検証に変更なし。水泳結果比較待ち。


## WORK-SELECTOR-AUTO-PROCESS-HISTORY-20261025
前turnprogress（自動表示判断/既存panel取消対応）。watcher再起動で履歴が消える制約を実装で解消するためnew work_selector_auto_history.py/tests追加。PID+GetProcessTimes作成時刻+EXEshaで履歴を束縛、既存_work下にゲーム起動単位JSON、schema厳密/64MiB上限/256attempts、pending非保存。破損/identity不一致/履歴縮小/stop解除拒否。tempflush/fsync/replace、失敗時原履歴維持。controllerはOPEN前・activepanel記録時にpersistし失敗STOP、選択送信なし。mainにload/save接続、mutex維持。原本ファイルへの書込みなし。
root auto関連37testsPASS（policy+adapter+persist+history）。途中の広いtestdiscoverはagentRED段階のmodule未保存を拾いImportError、完成後37再実行PASS。UI運転は未実施、DLL変更なし。現game操作/再起動なし、ユーザー教育結果回答はまだ未受領。次は結果照合後、短時間watcher実機で新一覧自動表示・右click戻り・監視再開時再表示抑止確認。


## WORK-SELECTOR-AUTO-RESUME-ACTUAL-20261025
前turnprogress（履歴永続化）。PID9588でactivepanel epoch1/65人/commit0を実機read-only確認。watcherをseconds3で開始し終了、既存手動panelを履歴1件へ登録。履歴work_selector_auto_9588_134373408250188525.json SHA562ecb135fc821e42f2ffa87697c661ebadfa7eaf085c7ba3d2d341a7af977f5。同じゲームでwatcher seconds3再起動し表示attemptなし、正常終了、履歴SHA不変を確認。現在panel/epoch/候補数不変、選択・教育・再起動なし。監視再開と実processidentity取得はACTUAL、次の新一覧自動表示/取消後原作操作/教育実結果一致は未確認。watcher終了済みで常駐なし。


## WORK-EDUCATION-SING-KARATE-PREDICTOR-20261025
前turnprogress（watcher実機resume確認）。原DAT ev02_sing/ev03_karateを限定読取、location_review_education_next_20261025.json保存readback（SHAb7ac3fcf598c808bea94a0c34e3c20dbd6457e960de131769f2bcfeffcc8fbc6）。両方base50+教師/生徒/other+能力差、結果25/50/75。歌唱MP差<-100:-20,<50:-5,<100:+10,else+15。空手attack差<1:-10,<25:-5,<50:+10,else+15。教師yappa_yameru2/生徒magdef利用方針。空手96行に教師kmr条件混在があり原作算出値を優先して補正再実装しない。歌唱大成功後技能shuffleはあるが4段階判定は乱数なし。
new work_education_prediction.py/tests: swim/sing/karateのpinnedDAT純判定API、未知は未判定、増加量/技能/成功率非公開。root7testsPASS（境界162subcases含む）。現水泳runtime未置換、歌唱空手UI/VM実機は未接続・未検証。保存Ghidra functions/004A/004AE0F0.c case1eでdef178/17C/180 raw参照を再確認（最初のpathに004A不足とrg構文不一致で未取得後、該当行read成功）。新EXE広範解析なし。原作game操作なし。次は歌唱/空手VM文脈と科目別otherbonusの限定接続、元水泳結果照合未受領。


## WORK-EDUCATION3-INTEGRATED-20261025
前turnprogress（3科目純判定）。new work_selector_education_student.pyはexact科目VMchain+selectedDAT/lecturepin+前後全identity、24testsと保存水泳証拠65人replay。new work_selector_education_outcomes.pyは3科目field/other統合21tests。rooteducation群47testsPASS（既存2含む）、senderlegacyfallback+generic科目限定7testsPASS（RED1→GREEN）。新版DLL教育・予想結果列、+81capで3科目capture、旧DLLはwaterfallback。native6harness+selftestPASS。DLL WorkUnitSelectorBridge-education3-preview.dll SHAbc0069b09457a4e977f6ffee29525870c37399534786bbc9993e4cf946303b89。元guard/commit不変。
旧PID9588 read-only OpenProcess87で取得不能、processinventoryで新PID14284起動確認。既存SelectorDLLなし→host接続reply1 installed1、genericcap1/commit0、65候補epoch1。sender12800で65件kind4予想通知受理exit0。初回pollLocaltimeout後同handle再pollで成功確認、再送していない。可視表示の今回user確認と歌唱/空手実機文脈/教育実結果MATCHは未確認。game実行/教育選択なし、既存生徒一覧へ表示のみ。教育全科目・教師全科目label・自動表示新一覧・確定・plugin基盤未完。次は利用者の実結果照合、歌唱/空手1場面ずつ実機確認。


## WORK-SWIM-ORIGINAL-OUTCOME-MATCH-20261025
前turnprogress（3科目接続）。利用者の既存game起動操作終了包括許可に基づきComputerUse skyで原作UIを操作。元panel戻る→原作先頭ピンキー姉貴選択、教育会話を進めた。teacherSNNN/studentpinky、水泳。事前new3subjectcapture: kind4大成功、HP81400、teacher補正50/student5/other5/HP差-10、score100。原作UI後readonly2回一致: pinkyHP83000、lecture_success100、処理後hp_up0/eranda_teacher/student空（実行後クリア済）。差1600で原DAT大成功帯と一致。原作内政/教育メニュー復帰を画面確認。セーブ上書きなし、原作の教育ポイント等実行中状態は通常操作により消費/更新。
証拠before _work/work_swim_ui_trial_before_20261025.json SHAb6655947f8fbcf786082c60b6faaae20a37c0235a485c3dc57caca2421b2be4d、result SHAe6eac81bef17e82021dd22222cf38db8b95550133f01f17a70cb71ca9f9d4d66、match receipt保存readback。水泳この1組OUTCOME_MATCH=1。全科目/全境界の実機MATCHではない。UIにHP増分を追加する要件変更なし、増加量は証拠のみ。native選択送信gate未変更、原作の通常マウス操作のみ。


## WORK-SING-ORIGINAL-OUTCOME-MATCH-20261025
歌唱を原作の通常UI操作で1件実行。教師kusomusume（変態糞娘）、生徒majimekun（マジメ君）。実行前のVM科目sing/65候補/原作教師補正30・生徒補正0・勢力補正0・MP差補正-20からkind3成功を予想。実行後2回一致読取でlecture_success60、MP1150→1180を確認し予想成功と一致。元教育メニュー復帰を画面確認。生徒確定は原作UIのみ、bridge commit無効・拒否済guard不変、セーブ上書きなし。実行中ゲームの教育ポイント等は通常消費。
証拠_work/work_sing_ui_trial_before_20261025.json SHA712f837e9c3af46857992af6263d3ec9d58b2d25e038a3e516b1e49b73e504cc、result SHA72e3b81140fc183f14ea3364cd1bfc34abd1e6dd5d46ba912bd226d88adb20cc、work_sing_outcome_match_20261025.json。すべて保存読戻一致。水泳大成功1＋歌唱成功1の合計2組のみOUTCOME_MATCH。空手実機、他結果境界、全教育、選択確定、共通plugin未完。EDUCATION-SORT=PARTIAL維持。次は空手1組または自動表示新一覧の検証。今回コード変更なし。


## WORK-KARATE-ORIGINAL-OUTCOME-MATCH-20261025
前turn progress（歌唱成功実結果一致）。原作通常UIで空手AKYS→ビリー・ヘリントン(aniki)を1件実行。実行前subject karate/65候補/教師補正55、生徒5、other10、攻撃力差118による+15、基本50で135＝大成功予想。実行後2回一致読取でlecture_success135、attack1882→1932を確認。予想大成功と原作結果が一致。元教育メニューへ復帰、セーブ上書きなし。教育の実行中ポイント等は通常消費。
証拠_work/work_karate_ui_trial_before_20261025.json SHA2a651f31b3421016a56a8f33ae1fcf91557678510d20f3d0b7f03d908b74ff37、result SHA5c880e5e7c580e5733ef6bdbc09f9c6222ba7128b7b35bc07113da25490c3391、work_karate_outcome_match_20261025.json保存読戻一致。水泳大成功・歌唱成功・空手大成功の各1組、合計OUTCOME_MATCH=3。失敗/通常境界、連続教師ペナルティの実機比較、他教育は未検証。UIには増加量表示を追加しない。native commit無効/拒否済guard不変。EDUCATION-SORT=PARTIAL、共通plugin依頼OPEN維持。次は自動表示新一覧と取消抑止の実機検証、選択確定の未解決事項整理。


## WORK-SELECTOR-AUTO-ITEM-ACTUAL-20261025
前turnprogress（空手実結果一致）。現ターン教育制限のためアイテム・オレンジジュース対象選択で自動表示を検証。watcher28620は90秒正常終了、候補未表示でattemptなし。次のwatcher25628はepoch6/66人を1回自動open、実画面でチップ一覧を確認、exit0。watcher23020再開後、一覧内右クリックでpanelのみ閉じ原作選択維持、再表示attemptなしexit0。さらにwatcher15120を3秒再開してattemptなしexit0。最終reader epoch6/count66/active0/commit0、履歴SHA不変ce8c7312b1584b38f4832b7fe2d01379a5232e669e99e2e15fa5d68fd722a376。
証拠_work/work_selector_auto_item_actual_20261025.json保存読戻一致。アイテム未使用、セーブ未書込、ゲームは原作の対象一覧に残る。全watcher終了済み。新一覧自動表示・右クリック取消・監視再開後同一覧再表示抑止がこの1画面でACTUAL。全イベント互換/選択確定/配布用起動統合は未完。SELECTOR=PARTIAL、plugin=OPEN。次は表示専用から選択確定までの未解決点を現ソースと拒否記録で整理し、許可範囲内の実装方針を決める。


## WORK-SELECTOR-COMMIT-READINESS-20261025
前turnprogress（自動表示と取消実機）。現ソースを再照合: commit_validated_choice/WORK_SELECTOR_ENABLE_COMMIT経路は既存だが、現previewビルドはmacroなし、releaseではないとbuilder明記。test_work_unit_selector.py再実行11件中10PASS/1ERROR。studentchara併存時の早期拒否がなくasset NoneのAttributeErrorになる既知不具合を再現。既存アイテム成功を否定しないが、教育へ安全に一般化できた証拠ではない。過去Local Command not allowedは承認済再試行も拒否、変数sc誤認の保存証拠あり。今回は拒否操作の再試行/別経路迂回/確定有効化なし。
証拠_work/work_selector_commit_readiness_20261025.jsonはソースSHA付き保存読戻確認。現在SELECTOR=PARTIALの安全な区切り。共通plugin基盤は独立に着手可能、ただしselector完成とはしない。ゲーム配下ファイル名探索でBattleObserver/HakushinCoreソースは未発見（全PC不存在とはしない）。次は既存台帳のBattleObserver参照回収、既存ビルド基盤を再利用する共通ローダー設計・実装。原作ゲーム/EXE/DAT/saveは本turn無変更。


## WORK-PLUGIN-FOUNDATION-IMPORTS-20261025
前turnprogress（確定未解決点の現物監査）。共通基盤の第1段階。REA MCP候補は現セッション0件、接続回復資料を確認、設定変更なし。保存T015_IMPORT_MAP_608F_6099.txtを先に参照し、現原作EXEをpefileでread-only解析（REA出力ではない）。SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187、machine014C、直接import DINPUT8.dll!DirectInput8Create確認、delay importsなし。保存証拠と一致。dinput8起動候補を静的に支持するが実機読込/入力互換は未確認。_work/work_plugin_loader_imports_20261025.json SHA5b48290f84f4a610c1d511ad013cb62fa61027d98438700e45f48e18f04eaef9保存読戻一致。
方針: 指定構成dinput8 proxy→HakushinCore→明示許可pluginsを第一候補、既存attach hostを予備起動経路としAPIは起動経路から独立。元system DirectInput転送を維持し、DllMain内のCore/plugin初期化は避ける。Coreは32bit C ABI/version/size照合、設定で許可したDLLのみ、ロード前manifestによる依存・順序検証、重複hook所有権管理とログを担当。未知DLLはLoadLibrary前に除外、API照合をロード前安全性の代用にしない。hot reloadなし。失敗時の原作継続はCore/plugin未開始時と開始後で分け、部分patchの復旧をテストする。
BattleObserver v0.1はゲーム配下およびDocumentsファイル名検索で未発見、台帳に依頼参照のみ。利用者へ保存先をasync質問済み、返答待ちでもloader/Core調査は独立継続可能。WRQ-20261023-PLUGIN-FOUNDATION=PARTIAL（調査開始、未実装）。次は所有/Git読取確認、専用既存研究下でAPI仕様・ビルド/fixture計画を具体化し、実DLLビルド。原作起動/配備/EXE変更なし。


## WORK-CORE-ABI-BUILD-20261025
前turnprogress（PE import確認）。Git status read-only照合し多数既存変更を保持。data/recruit_sort_v4/coreのみ担当core_abiへ新規実装委任、rootはdev_lab/docs/WORK_PLUGIN_FOUNDATION_PLAN.md作成。C ABI/version/size/ID確認、明示許可absolute pathの単一plugin load、shutdown成功までmodule保持、失敗shutdown再試行を備えたHakushinCore.dllとhost/fixture DLLを実装。未知DLLの検出/設定認可は未実装でcaller責任、production自動loaderとはしない。
root reviewでlog callback再入が二重Load/Shutdownを通せる問題を発見、担当RED再現→lifecycle in_progress guardでHK_BUSY返却へ修正。x86 compile guard追加。rootがbuild_test.ps1を独立再実行PID23692、7ケース全PASS/exit0。全DLL/host PE machine014Cをroot確認。証拠_work/work_core_abi_build_20261025.jsonにartifactSHAを保存読戻。原作ゲームへの配置/接続/再起動なし、selector/他担当既存ファイル変更なし、Git変更操作なし。
PLUGIN-FOUNDATION=PARTIAL。残り: 複数plugin設定allowlist/依存順、共通hook/event、dinput8 proxy、BattleObserver現物統合、原作起動入力戦闘検証、配布。単一fixtureを基盤完成と呼ばない。次は設定依存のロード前検証とCoreの複数instance化。


## WORK-CORE-MULTI-MANIFEST-20261025
状態: PARTIAL / 担当: Work / 優先度: 継続 / 停止VA: 該当なし（共通DLL基盤）
ユーザー確認: 生徒一覧の予想結果表示と選択人材の原作詳細との一致を確認。教育実行結果の確認とは区別する。
Core: 32固定スロット、複数DLL、重複ID/module拒否、逆順終了、終了失敗時の保持と再試行。2DLL実機fixtureと従来7fixtureをWorkが再実行、PID14456 exit0。Manifest parserもPID29576 exit0。
未完了: manifestとCoreロードの接続、32枠境界、dinput8 proxyの原作実機検証、共通hook/event、BattleObserver統合。原作ゲームへCoreは未導入。selector確定は無効を維持。
参照: _work/work_core_multi_manifest_20261025.json; ../data/recruit_sort_v4/core; docs/WORK_PLUGIN_FOUNDATION_PLAN.md
再開位置: 設定を全件検証してから許可DLLだけを依存順で読み込む統合fixtureを追加する。


## WORK-CORE-BOOTSTRAP-20261025
前turn: progress。状態PARTIAL / 担当Work / 優先度 継続 / 停止VA 該当なし。
manifest→Coreのbootstrap実装。設定全件・enabled DLL全件の存在/PE32/i386/DLL flagをロード前検証。無効DLL除外、依存順起動、他者使用中Core拒否、失敗時逆順rollback、終了失敗時所有とmodule保持。Core追加はIsIdleとtypedef。rootレビュー後build_bootstrap_test.ps1を独立実行PID19280 exit0、ALL BOOTSTRAP TESTS PASSED。元EXE/DAT/save変更なし。
証拠: _work/work_core_bootstrap_20261025.json（保存読戻一致、ソース/成果物SHA付き）。実装: data/recruit_sort_v4/core/hakushin_bootstrap.c等。
未完了: 設定ファイル読込・起動統合、自動検出、proxy、hook/event、BattleObserver統合、原作起動入力戦闘検証。信頼済ディレクトリ・直列呼出必須、IsIdleはatomic所有権ではない。native依存DLL/ファイル差替競合を隔離する機構ではない。
次の再開位置: dinput8 proxyでsystem DirectInputを転送するfixtureを実装し、その後明示設定のCore起動を接続。原作へ配置する前にfixtureで検証。selector commit拒否事項は未変更。


## WORK-DINPUT-PROXY-FIXTURE-20261025
前turn progress。状態PARTIAL / 担当Work / 優先度継続 / 停止VA該当なし。32bit dinput8 proxy実装、system絶対pathへDirectInput8Createを同ABI転送、DllMain空、初回呼出InitOnce。root production/diagnostic再実行PID22588 exit0、W/A作成解放・invalid HRESULT一致・system file identity確認。追加startup import hostを独立再実行PID3208 exit0、別cwd Tempからexe隣のproxy自動ロードを確認。root PE importもdinput8.dll!DirectInput8Createを照合。
証拠: _work/work_dinput_proxy_fixture_20261025.json、data/recruit_sort_v4/core/PROXY.md。保存読戻とSHA確認。原作PID14284起動中をread-only確認、原作への配置/終了/起動なし。
未完了: proxyから設定/Core/plugin起動接続、無効時と起動失敗時のDirectInput継続、原作実機の起動入力戦闘、hook/event、BattleObserver。外部callerがDllMainから呼ぶケースは保証しない。他dinput8 exports非対応。system DLLはCOM寿命のためprocess終了まで保持。
再開位置: module基準の設定ファイル読取とCore初期化をproxy初回呼出へ接続し、無効/欠損/異常/正常プラグインのfixtureを検証。その後のみ原作へ段階導入。


## WORK-PLUGIN-STARTUP-20261025
前turn progress。状態PARTIAL / 担当Work / 優先度継続 / 停止VA該当なし。proxy初回DirectInput呼出→module基準config読込→Core→依存順plugin起動を実装。明示設定なし/空/無効ならCore未ロード、設定不正/欠損Core/API不一致/init失敗でもDirectInputを継続。起動CAS gateは同thread再入と他threadの入力を待たせない。初回caller自体はplugin init待ち得る。callback寿命のためCore/proxy pin、productionはprocess終了まで保持。
root sourceレビュー後build_startup_test.ps1独立実行PID26052 exit0、12ケースPASS。production(診断exportなし)もinit1回、同/他thread入力、未宣言DLL非実行を確認。rollback失敗時保持→診断shutdown再試行を確認。エラーindex/ID/statusログ追加、runtime failed_indexを補完しRED/GREEN試験。
証拠: _work/work_plugin_startup_20261025.json、core/STARTUP.md、startup_fixture/run_d42b9ffd123f495fb8e0fbf60c45d6e3。root PE014C/export DirectInput8Createのみ確認、ログ/SHA保存読戻一致。原作ディレクトリdinput8/Core/config/plugins不存在をread-only確認、原作への配置/操作なし。
未完了: 原作起動・入力・戦闘実機、共通hook/event、BattleObserver、既存selector移植・確定、配布。native crash/hang隔離やhotreloadは保証なし。次: 原作を通常終了してからloaderを段階配置し、EXE/DAT/save不変・実moduleとタイトル/入力を確認。BattleObserver現物所在は未回答。


## WORK-ORIGINAL-PROXY-AND-ARCHIVE-20261025
前turn progress（原作title実機、物理EscでUI停止）。状態PARTIAL / 担当Work / 優先度継続 / 停止VA該当なし。UI操作は再開せず。元EXE/DAT/save計601ファイルbaselineから照合、変更件数=0。
原作proxy-only配置済、config/Core/pluginsなし。sky.launch_appはproxy有無両方でwindowなし（PID10880/29528、試験processのみ終了）。Explorer通常起動ではproxy有無両方title到達、proxyありPID29460とplugins disabled:no configログ確認。起動方法差は確認、cwd原因までは未確定。Continue押下後の確認中に利用者Esc停止、入力/戦闘検証未完。UI再開は利用者指示待ち、独立開発は継続。追加proxyはゲーム直下に残る。
利用者からBattleObserver所在として渡されたdist/HakushinRecruitSort-0.1.0-preview.zipを展開/実行せず確認。ZIP SHA27040aa51b02c497ce2824986f7f44130dc7ebee3f7748c3be97ad934a4fb9f0。6項目、内容は雇用4分類DLL/attach host/launcher/README/START/manifest。manifest5ファイルSHA一致。BattleObserverとソースは含まれず、所在未確認を維持。雇用plugin移植の資料として参照。
独立hook予約管理64枠/32bit範囲/所有者と世代を実装、rootソースレビューとbuild_hooks_test.ps1 PID26804 PASS。実patch/Core組込ではない。記録 _work/work_plugin_original_and_archive_20261025.json、core/HOOKS.md。次: 予約管理のversioned Core API組込とイベント寿命管理。原作UIは操作しない。


## WORK-CORE-EXTENSIONS-20261025
状態 PARTIAL / 担当 Work / 優先度 継続 / 停止VA 該当なし。ABI1を維持した予約管理extensionをCoreへ統合。init時のAPI identity確認、Core発行instance token、他所有者release拒否・古いtoken拒否、未解除予約を持つDLLの保持を実装。rootがfixtureを読み、build_core_extensions_test.ps1を独立再実行 PID1348 exit0 / ALL CORE EXTENSION TESTS PASSED。
参照: _work/work_core_extensions_20261025.json、core/HOOK_EXTENSION.md、docs/WORK_RECRUIT_PLUGIN_MIGRATION.md。提供ZIPは雇用並替え配布物でBattleObserverではない。
未完了: 実hook設置とイベント寿命管理、雇用DLLのadapter、BattleObserver所在/統合、原作入力・戦闘実機確認。原作UIは利用者Esc停止後のまま操作せず。原作直下のproxyは前回配置のまま、今回新規配置なし。次は雇用DLLの8箇所の予約とUI thread上の導入を共通基盤へ接続する。process lifetime方式を優先し、安全な解除未実装を完了扱いしない。


## WORK-RECRUIT-PLUGIN-TRIAL-20261025
状態 PARTIAL / 担当 Work / 優先度 実機確認 / 停止VA 該当なし。雇用plugin adapterを新規実装し既存sorterソースは変更せず別DLLへリンク。8範囲予約→永久pin→同一threadの一意な可視host top-level window messageで一度だけ導入。hidden/message-only/複数windowは待機。Core ABI1維持。失敗時やshutdown時はmodule/予約保持、hotreloadなし。レビューでhidden補助window問題を検出し可視・caption・process全体の一意性条件を追加。semantic mainwindowの実機証明はまだない。
root build_recruit_plugin.ps1 -Test PID23680 exit0、success/overlap/failure retentionの3fixture PASS。実装 core/recruit_plugin_adapter.c、core/RECRUIT_PLUGIN.md。
利用者がゲーム終了を報告、プロセス不在確認後に原作直下HakushinCore.dll・plugins/HakushinRecruitPlugin.dll・hakushin_plugins.confを新規配置。既存proxy SHA確認。起動は行わず利用者が直接Vahren.exeで確認する。配置前後601原作ファイル不変。以前baselineとの差はauto.savのみで配置前から存在、復元せず現物を保持。証拠 _work/work_recruit_plugin_trial_20261025.json（読戻一致）。
未完了: 実機起動/並替え/reset/雇用後、共通event/実patch管理、BattleObserver統合、selector完成。次: 利用者起動後core logとplugins側legacy sorter logの新規分を読んで実ロード/導入/表示を照合する。利用者が操作するためWorkはUIを操作しない。


## WORK-RECRUIT-DIAGNOSTIC-TRIAL-20261025
状態 PARTIAL / 担当 Work / 優先度 実機不具合切分 / 停止VA 該当なし。利用者は原作起動成功・並替えなしと報告。Core logはplugins started、legacy installer logなし。PID13152/HWND723604応答ありを確認した後、read-only状態読取時にはOpenProcess87、再照会でVahren不在。対象終了後の読取を成功扱いしない。
接続adapterにboundedログのみ追加、挙動は未変更。初期thread/eligible画面数/最初8callbackの判定理由/installer結果を原作隣HakushinRecruitPlugin.logへ保存。root build_recruit_plugin.ps1 -Test PID16284 exit0。プロセス不在時のみ既知SHAのpluginを診断版へ差替え、旧DLLはresearch core/recruit_adapter_fixture/HakushinRecruitPlugin.before_diagnostics.dllへ保持。原作EXE/DAT/saveは触らず。
証拠 _work/work_recruit_plugin_diagnostic_trial_20261025.json。次: 利用者がVahren.exe直接起動し雇用一覧を開いたまま診断ログとprocess/threadを照合。UIは利用者操作。未完了: 実機で動作しない原因特定・修正、共通基盤残件、BattleObserver/selector。


## WORK-RECRUIT-PRODUCTION-REFUSAL-20261025
状態 PARTIAL / 担当 Work / 優先度 実機診断待ち / 停止VA 該当なし。前turnは診断版実装・配置のprogress。今回実production DLL（stubでない）を対象外の拡張サイズhostへロードし、hidden待機→visible unique message→FAILED_RETAINED、native IsInstalled=0、8箇所各5byte不変、shutdown後module/8予約保持をfixtureで確認。root production_host.exe PID28368 exit0。新規fixtureとbuild testに組込、記録 _work/work_recruit_production_refusal_20261025.json 保存読戻済。
原作の診断版logはまだ不存在。実機並替え原因は未確定、推測修正なし・今回game配置変更なし。利用者のVahren.exe直接起動→人材雇用を開いた状態を待つ。画面操作は利用者。次はHakushinRecruitPlugin.logのinit/thread/候補window理由を読む。


## WORK-EVENT-DISPATCHER-20261025
状態 PARTIAL / 担当 Work / 優先度 Core接続 / 停止VA 該当なし。前turnは実production拒否fixture追加のprogress。共通event standalone dispatcher実装: owner/世代handle、64購読、登録順snapshot同期通知、通知中追加は次回、通知前解除skip、自己解除後callback終了までOwnerBusy、再入emit拒否、borrowed payload上限65536、counter wrap拒否。thread直列化はcaller責任。
root source reviewと独立review、sole自己解除busyと最終generationの2試験不足を追加し再review承認。root build_events_test.ps1 PID28328 release PASS130/exit0（debugは担当報告）。証拠 _work/work_event_dispatcher_20261025.json、core/EVENTS.md 保存読戻一致。戦闘観測/実hook/安全unloadの証明ではなくCore ABI未接続。
原作診断logまだ未取得、原因未確定。ゲーム配置変更/UI操作なし。次: 原作log到着時は雇用問題優先、独立作業はCore event extensionのtoken/lifecycle連携と実DLL fixture。


## WORK-CORE-EVENTS-20261025
状態 PARTIAL / 担当 Work / 優先度 共通基盤 / 停止VA 該当なし。前turn standalone event実装progress。Coreへoptional event extension2/version1を統合、ABI1維持。init API identity限定query、Core instance token所有、stale拒否。emit全体lifecycle guardでcallback内Load/Shutdown/再入emit拒否。dirty init/dirty shutdownで購読が残ればDLL/依存保持、cleanup/retry可能。
root source review+独立reviewで具体的欠陥なし。root build_core_events_test.ps1 PID28272 exit0 ALL CORE EVENTS TESTS PASSED。担当回帰: reservation/original7/multi/bootstrap/startup12 PASS、startup_fixture/run_855d36a4d71147c5840858a576917d10。記録 _work/work_core_events_20261025.json保存読戻/ソース成果物SHA。minor試験gap3項目はreceiptへ明記、完了ゲートに拡張しない。
原作配置のCoreと診断RecruitDLL SHA不変を確認。ゲームへ新Core配置なし、画面操作なし。原作診断log未取得、雇用並替え不具合は未解決。未完: 実hook共通化/戦闘event/BattleObserver/selector/原作動作検証/配布。次: 利用者原作ログを優先確認、共通基盤の実hook所有・解除と既存プラグイン連携を進める。


## WORK-CALL-PATCH-MANAGER-20261025
状態 PARTIAL / 担当 Work / 優先度 Core接続 / 停止VA 該当なし。前turn Core event接続progress。共通HKH予約に接続したstandalone E8 CALL5byte管理実装。expected bytes/可読実行commit memory/guardなし/同pageを検証。所有者・世代handle、部分失敗時recordと予約保持、ownedまたはoriginal exact bytes時だけ復元、write/flush/protection/予約解放成功後のみ終了。callerのquiescence/ABI/lifetime確認が必須。
実private VirtualAlloc callable関数7→9→7と合成故障fixture。root review+独立reviewでP2保護rollback失敗status隠蔽を検出修正、再review承認。root build_call_patch_test.ps1 PID3000 exit0 ALL CALL PATCH TESTS PASSED。証拠 _work/work_call_patch_manager_20261025.json、core/CALL_PATCH.md 保存読戻/ハッシュ付き。初回REDのWindows filename elevation heuristic問題と遅れた有効RED観測はdocsに正直に記録。
Core ABI/原作/配置DLLは変更なし。原作診断log未取得で雇用不具合は未解決。次: 原作ログ優先、独立作業としてCore optional patch APIとmodule保持を接続。BattleObserver/実戦闘hook/selectorなど未完。


## WORK-RECRUIT-UI-ROUTING-20261025
状態 PARTIAL / 担当 Work / 優先度 最優先実機確認 / 停止VA 該当なし。原作PID18208の診断はinit_pending eligible_count=0のみでcallbackなし。初期化thread固定を廃止し、非同期で唯一の原作UI画面/threadを発見して一度だけ接続する修正。negative hook code即forward修正も含む。root build_recruit_plugin.ps1 -Test PID29244 exit0、配置済Coreとのproduction拒否fixture PID18920 exit0。ゲーム不在を確認してRecruitPluginだけ差替え、旧版をresearch fixtureに保持。原作EXE/Core/proxy/configのSHA不変。原作DAT/save操作なし。実ゲーム並替えは未検証。参照 _work/work_recruit_ui_routing_20261025.json。次: 利用者がVahren.exe直接起動→人材雇用を開き保持、診断logと並替えを照合。ゲーム操作は利用者。


## WORK-CORE-CALL-EXTENSION-20261025
状態 PARTIAL / 担当 Work / 優先度 共通基盤 / 停止VA 該当なし。前turnは雇用UI thread修正と配置のprogress。今回はCore optional extension3/version1にCALL管理を接続。ABI1維持、Core instance所有、共通予約とのoverlap拒否、管理予約の通常release拒否、patch/recovery残留時のmodule保持、cleanup retryを実装。caller quiescence必須で安全detach保証ではない。
root独立test build_core_call_test.ps1 PID23676 exit0 ALL CORE CALL TESTS PASSED、独立review具体的指摘なし。担当回帰reservation/events/original7/multi/bootstrap/recruit/startup12 PASS、startup_fixture/run_40b8a6ce95024413a9016736ddd222df。minor試験gap3項目はreceiptへ保存。参照 _work/work_core_call_extension_20261025.json、core/CORE_CALL_PATCH.md。
原作Core/RecruitPlugin/EXEの既知SHA不変、新Core配置なし。雇用修正版の新実機logはまだなく、並替え成功未確認。次は利用者の直接起動→人材雇用の結果と新logを最優先確認。基盤残件は実pluginへのmanaged CALL移行、BattleObserver現物・戦闘events、配布/原作入力戦闘検証。ゲーム操作は利用者。


## WORK-STARTUP-LOGGER-20261025
状態 PARTIAL / 担当 Work / 優先度 共通基盤 / 停止VA 該当なし。前turn Core CALL接続はprogress。今回は共通logがplugin messageを捨てる問題を修正。levelと最大256byteの内容を保存、改行/control/backslashをescape、truncation明示、最大1100byte出力。root logger fixture PID28152 LOGGER failures=0、独立review具体的指摘なし。担当startup12回帰PASS run_5f486b22c49a4b39b33043a647fb3c39。参照 _work/work_startup_logger_20261025.json、core/STARTUP_LOGGING.md。
雇用managed CALL移行の前提としてCore caller直列化とUI callback/startup並行性の解決が必要と確認、WORK_RECRUIT_PLUGIN_MIGRATION.mdへ記録。ゲーム配置変更なし。新実機logなし、並替え成功未確認。次は利用者結果/log優先、Core thread契約と実plugin移行を進める。


## WORK-CORE-THREAD-GATE-20261025
状態 PARTIAL / 担当 Work / 優先度 共通基盤 / 停止VA 該当なし。前turnログ改善はprogress。Core公開4関数とbound8関数へnonblocking atomic thread gateを追加。同一thread再入は許可し従来lifecycle制限を維持、他threadはmutable stateアクセス前にBUSY/出力不変。ABI layout不変。
root build_core_threads_test.ps1+recruit -Test PID27468 exit0、独立review具体的指摘なし。担当reservation/events/CALL/original7/multi/bootstrap回帰PASS。参照 _work/work_core_thread_gate_20261025.json、core/CORE_THREADS.md。原作配置Core/RecruitDLLの既知SHA不変。新実機logなし、並替え成功未確認。
次: 雇用UI callbackのmanaged CALL移行はCoreのBUSYで次回UI messageへ延期する契約が必要。metadata8予約との重複を解消し、途中失敗の復旧handleを保持する。Core gateは原作patch実行停止や安全unloadを保証しない。実機結果が届けば最優先で照合。


## WORK-RECRUIT-MANAGED-RESEARCH-20261025
状態 PARTIAL / 担当 Work / 優先度 共通基盤 / 停止VA 該当なし。前turn Core thread gateはprogress。研究用HRA_MANAGED_CALLSで雇用8CALLをCore extension3へ接続、metadata重複予約なし、従来default build保持。成果物core/recruit_managed_fixture/HakushinRecruitManagedResearch.dll、ゲーム未配置。host照合/GDI/renderer維持、RECOVER含む逆順復旧、未復旧handle保持、pristine BUSYのみ延期。
root reviewでINSTALLING中worker終了→DEFER取り残し競合を発見、独立reviewでexpiry/start gapも発見。worker寿命/expiry flag/claim直後確認を修正、deterministic fixture追加、再review承認。root最終build_recruit_managed_test.ps1 -Test PID14780 exit0。fake batch/actualCore private8CALL/production拒否/route競合試験PASS。担当legacy adapter回帰PASS。参照 _work/work_recruit_managed_research_20261025.json、core/RECRUIT_MANAGED_RESEARCH.md。
原作Core/RecruitDLL/EXEの既知SHA不変、新実機logなし。実ゲーム並替え未確認、全game threadのpatch quiescence未証明、実機配布の完成扱い不可。次は利用者の現試験版結果を優先し、管理版へ切替前のthread/導入時点の根拠を既存資料で確認する。BattleObserver/戦闘events/selector/配布は未完。


## WORK-GOAL-SELECTOR-LOADER-20261025 依頼管理
| 依頼ID | 担当 | 優先度 | 停止VA | 未完了範囲 | 参照先 | 状態 |
|---|---|---|---|---|---|---|
| WORK-SELECTOR-FINISH-20261025 | Work | P0 | 該当なし（過去拒否は既存台帳参照） | 選択確定・教育/アイテム/イベント接続・更新対応・実機回帰・配布 | 本節A、固定handoff、既存selector成果 | PARTIAL |
| WORK-LOADER-FINISH-20261025 | Work | P1 | 未確定（既存host契約参照） | 実機雇用/selector統合・起動互換・無効化/差替・BattleObserver依存・配布 | 本節B、WORK_PLUGIN_FOUNDATION_PLAN.md | PARTIAL |
旧戦闘/エンジン依頼は成果を保持して当面の作業対象外。CLOSEDへの偽装変更はしない。


## WORK-SELECTOR-UPDATE-REASONS-20261025
状態 PARTIAL / 担当 Work / 優先度 P0 selector / 停止VA 該当なし。前turn新目標明文化はprogress。selector現物監査で既存表示/検索/並替えを再利用し、DAT更新理由がearly UNKNOWNで失われる箇所を修正。既存教育captureにDAT_CHANGED/DAT_UNAVAILABLE/CONTEXT_UNVERIFIEDと確認済文脈metadataを付与、sender診断へ伝播。UNKNOWNはzero kinds/予想packetなし、認可条件は緩和しない。教師wrapperの欠落subject経路をreview後修正、共通lecture欠落は従来のruntime読取前拒否を維持し画面警告なし。console診断でありpanel banner実装ではない。
root初回PID6628 50+25+9PASS、followup PID10736 52+10PASS、未変更VM25を合わせ関連87PASS。独立review再確認承認。全suiteは担当が無関係corpus中に中断、pygame未導入3error確認、全体PASS扱いなし。参照 _work/work_selector_update_reasons_20261025.json。ゲーム/配布DLL変更なし。過去拒否bridge/unit_selectorの既知SHA不変確認、native commit無効維持。
最重要残件: 教育生徒の誤認拒否guardと選択確定の復旧。Local自動審査Command not allowedは利用者承認後も拒否された記録あり、別経路回避しない。単なる再承認を繰り返さず、当該拒否の解消が必要。表示改善で選択確定の未完了を隠さない。新目標A/Bの実機・配布完了は未達。


## WORK-SELECTOR-TEACHER-THREE-SUBJECTS-20261025
状態 PARTIAL / 担当 Work / 優先度 P0 selector / 停止VA 該当なし。前turn DAT更新理由改善はprogress。保存済DAT hashとteacher magdef代入を確認し、水泳/歌唱/空手の講師文脈認識を共通化。selected subject+lecture pin、exact routine/leaf、identity/VM安定を維持。旧water APIはwater限定。表示packet 0none/1swim/2sing/3karate、native列名/補正sort/custom見出し名を科目へ対応。旧DLL拒否時waterへ再送しない。
root PID29804 teacher6+sender12、native6harnessとisolatedselftest PASS exit0 installed0。独立review具体的blockerなし。研究DLL dist/WorkUnitSelectorBridge-teacher-three-subject-research.dll SHA91c3c2de19eb54a2b0dee0b8618d7d6d75b535c729677239e34583d248d931b2。commit無効、原作未接続/未配置。拒否対象bridge/unit_selector SHA不変。参照 _work/work_selector_teacher_three_subjects_20261025.json。
担当の無関係fullsuite PID30136はroot観測でsessionなし、完了結果未取得、全体PASSとしない。次: 講師3科目の実機表示確認、残り教育/強制イベントの候補文脈照合、選択確定guardの過去Local拒否解消が必要。A/B完成・配布は未達。


## WORK-SELECTOR-TEACHER-ALL-SUBJECTS-20261025
状態 PARTIAL / 担当 Work / 優先度 P0 selector / 停止VA 該当なし。前turn講師3科目表示はprogress。残6DATのhash/teacher bonus→magdef→選択→resetをread-only照合し、全9科目の講師補正列・sort表示へ拡張。teacher専用pinを分離し、結果予想3科目は増やさない。値4..9は糞遊び/声劇/茶道/調教/インタビュー/アメフト、10拒否・旧DLL拒否時誤label再送なし。
root PID3192 teacher8+sender13、native6harness+isolated selftest PASS exit0 installed0。独立review確認。研究DLL dist/WorkUnitSelectorBridge-teacher-all-subject-research.dll SHA7e07981debbc3c66936e0ef94442b1d390cbcffe2f1cf8435c80b4dbfc43b252。参照 _work/work_selector_teacher_all_subjects_20261025.jsonに残6のsource行/field/bonus caveatを保存。茶道結果は複数生徒/履歴/score特殊状態があり未検証予想を追加しない。
commit無効、拒否対象bridge/unit_selector既知SHA不変。原作起動/接続/配置/セーブ変更なし。全9teacher実機は未確認。最重要残件は選択確定guardのLocal拒否解消、全体実機操作/配布。A/Bは未完成、基盤の抽象追加を優先しない。


## WORK-SELECTOR-FIVE-PREDICTIONS-20261025
- 担当: Work / 優先度: P0 / 状態: PARTIAL / 停止VA: なし（既存DAT・読取経路）。
- 成果: 糞遊び・声劇・調教・インタビュー・アメフトの結果予想を追加。実DAT固定値・原作算出の生徒magdef・保存された講師補正を使用。茶道は特殊な複数人/途中経過処理のため未判定。
- 検証: root PID24424と21532、関連138テスト実行PASS、exit0。重複継承テストを含み、138独立仕様を意味しない。独立レビュー重大指摘なし。教師kusoasobi/生徒kusoは別経路で整合、現時点の機能不良なし。
- 未完了範囲: 新5科目の実機照合、茶道、選択確定の既存拒否解消、共通ローダー上での最終統合と配布確認。ゲーム差替え・起動・操作なし。既存の確定無効化と保護対象は変更していない。
- 参照先: _work/work_selector_five_predictions_20261025.json、tests/test_work_education_five_predictions.py。次は実用化を妨げる選択確定/ローダー接続を優先し、表示専用試験だけで完成扱いしない。


## WORK-SELECTOR-LOADER-GAP-20261025
- 担当 Work / 優先度 P0 / 状態 PARTIAL / 停止VA: bridge既存拒否範囲を維持。
- 現物監査: PID12244でVahrenなし、配置済み雇用修正版SHA一致、logは旧PID18208のinit_pendingだけ。修正後実機成功は未確認。利用者へVahren.exe直接起動→人材雇用を依頼済み。追加起動/配置なし。
- selector_loader_gap独立監査: UI/search/sortとPython watcherは既存。selector DLLはCore必須Query/init/shutdownをexportせず、そのままmanifest追加では不可。表示データはPython sender依存。必要なのはCore lifecycle/UI-thread・CALL所有権接続とデータ供給自動起動の接続であり、UI再実装ではない。
- 確定は既存コードあり・現build無効。student誤認guard修正のLocal拒否が残る。固定handoff2960–2967/2995を再確認し、承認取得済み、再試行拒否、C変数scの禁止コマンド誤検出の再現記録あり。許可不足と再説明せず、別wrapper/pathで迂回しない。
- 未完了: 上記接続・拒否解消・実機結果・配布。参照 _work/work_selector_loader_gap_20261025.json。前turnは教育5科目追加/検証保存のprogress。本turnは実装欠落経路と拒否原因記録を特定し次工程を絞ったprogress。


## WORK-SELECTOR-ORDINARY-TEA-20261025
- Work / P0 / PARTIAL / 停止VA:なし（既存拒否は継続）。通常教育9科目の予想処理が揃った。茶会は未対応。
- 原作DATで通常茶道と3人茶会の共有selectorを区別。通常親poli_lecture_06_sadouのexact chainのみ認識。教師最大113、生徒条件判定前最大93、実行時最大256で500条件が一覧と実行で反転しないことをsource/testで検証。茶会後もnative生徒magdefと保存講師補正を利用できる。
- tyakai_count/eranda_students/syukaku_raceを反復読取、欠落/変化は未判定。dext差・25/50/75判定を追加。茶会は将来選択で変わるため表示しない。
- root PID23248 関連149テストPASS exit0、独立review重大指摘なし。過去拒否bridge/unit_selectorのSHA不変確認。commit無効・ゲーム/配布物の変更なし。
- 参照: _work/work_selector_ordinary_tea_20261025.json、tests/test_work_education_tea_prediction.py。未完了: 新科目実機照合、選択確定拒否解消、ローダー統合と配布。起動状況PID23052ではゲームなし・旧logのまま。利用者への雇用起動確認は既存質問を維持し重複送信なし。


## WORK-SELECTOR-LOADER-BLOCKED-AUDIT-20261025
- Work / P0 / BLOCKED（未完成）。前turnは通常茶道追加・149試験・review保存のprogress。
- 同じ外部依存は直近3goal turn（loader-gap、ordinary-tea、本audit）連続で継続。並行して可能な通常9科目予想は実装/検証を済ませた。今回はPID12220でVahrenなし、logは旧PID18208のみ、質問への実機回答未着。現在走っているゲーム/検証jobを待つverified waitではない。
- 完成条件A: 表示・検索・ソート・詳細・右clickは既存実機証拠あり。通常9科目の予想は静的根拠/テストまで（新科目live未達）。選択確定のstudent誤認guardはLocal拒否未解決、commit無効。講師→生徒→実行/強制イベント/連続使用の最終回帰未達。
- 完成条件B: Core/設定/API/所有権管理はresearch fixture、原作proxy titleは既存証拠あり。配置済み雇用UI-thread修正版のlive未達。selector Core接続/データ供給起動/最終配置・配布未達。BattleObserver現物なし。
- 再開条件1: 利用者がVahren.exe直接起動→人材雇用を開いて報告。既存の質問を再送しない。再開条件2: Local管理側でC変数scを禁止コマンドと誤認する拒否を解消し、承認済み3ファイル修正を同じ正規経路で扱えること。許可不足ではなく、承認済み再試行も拒否のため別経路/複製wrapperで迂回しない。
- 未保存成果なし。現ソース・試験receipt・再開位置は既存queue/handoffと_work/work_selector_ordinary_tea_20261025.json、work_selector_loader_gap_20261025.jsonに保存済み。次は新たな周辺機能ではなく上記2依存の解消から開始。完成扱いにしない。


## WORK-STARTUP-RECOVERY-FOLLOWUP-20261025
- Work / P0 / PARTIAL。起動失敗報告で調査再開。元配置はloader無効/全追加拡張退避でも読込中終了。ZIP全14375原作ファイルsize/CRC一致、missing/diffなし。診断copyと元の全tree名/種類/size一致。
- 診断copyはtitle成功。元global→auto→save1/2/3を段階複製しても各title成功を利用者確認。元セーブ不変・複製SHA照合。利用者のEXE上書きも改善なし。原因未特定、セーブ破損やDLL原因を断定しない。
- 互換設定HIGHDPIAWARE→~ HIGHDPIAWARE試験も不成功。復旧時に予期しない現在値を検出、外部変更保護で上書きせず。現在値はreceipt記録。拡張7項目は_work/plugin_startup_hold_20261025へ可逆退避済み。元フォルダでは拡張無効。
- 再開先: _work/startup_clean_20261025/新約迫真戦記―ほのぼの神話ver0.67 豪華版（全セーブ複製済み、titleのみ確認）。saveロードでプレイ復旧を先行、その後拡張を段階確認。元フォルダ削除/全面上書き/自動起動なし。
- 参照 _work/work_startup_recovery_followup_20261025.json、work_startup_compat_trial_20261025.json。選択UI/loader完成は未達。


## WORK-LOADER-RECOVERY-STAGES-20261025
- Work / P0 / PARTIAL。前turnは起動失敗の比較・退避・互換値保護を記録したprogress。今回PID27160でゲームなし、退避loader/Core/configのhashと実体を確認。
- 作業先は起動成功済み診断copy。save1読込の利用者確認待ち（重複質問なし）。復帰用3ファイルの既知SHAを照合し、3段階配置manifestを_work/work_loader_recovery_stages_20261025.jsonへ保存・読戻。
- 順序: proxy単体configなし→Core/雇用plugin配置かつdisabled→明示enabled。各段階で通常起動/入力/読込/終了とlog、最後に並替え/リセット/雇用を検証。研究版Core/managed-CALL/selector確定を同時投入しない。
- 現在はPREPARED_NOT_DEPLOYED。ゲーム/配置変更なし。元フォルダの起動原因は未解決、追加拡張は退避のまま。userによるWindows7互換設定は保持。選択確定の既存Local拒否も継続。


## WORK-RECOVERY-EXTERNAL-WAIT-20261025
- Work / P0 / BLOCKED（完成ではない）。復旧調査turn→復帰段階準備turn→今回と、利用者の実機確認が必要な条件は継続。直前turnは復帰manifest/版照合を保存したprogress、今回は外部状態再確認。
- PID18748の確認でVahrenなし、診断copyにdinput8.dllなし。生きているgame/jobのverified waitではない。save1読込結果は未着。新しい自動起動/配置/迂回作業なし。
- 許可済みで独立に可能な9科目予想と復帰準備は済み。次の有用な実機作業には利用者の診断copyセーブ読込結果、選択確定には従前Local誤検出拒否の解消が必要。追加の周辺実装で待機を水増ししない。
- 再開: 診断copyでsave1読込を確認→ゲーム終了確認→work_loader_recovery_stages_20261025.jsonのstage1。元フォルダ/セーブ/退避物保持。未保存成果なし。


## WORK-ORIGINAL-RESTORED-PROXY-STAGE1-20261025
- Work / P0 / PARTIAL。利用者がZIP全面上書き後、元フォルダの起動・save1読込・通常操作成功を確認。原因未特定のまま。PID19768の元Vahrenパス、EXE既知SHA一致、拡張5項目不存在をread-only確認（PID8752）。診断copyを主作業先にする前方針は撤回し元フォルダへ戻る。
- 利用者終了回答後、processなし再確認。退避dinput8のSHA f36cc892b7565bd957e5851bab60f0ef47d0e69d5cbd0b1d136c3a5d06c3325bを照合し、元フォルダへ単独複製、読戻hash一致（PID3332 exit0）。Core/config/pluginsは未配置、原作EXE/DAT/save変更なし。
- stage1は配置済み・実機確認待ち。利用者へ直接Vahren起動→save1→通常操作を依頼。雇用並替え無効の段階。確認後logとmodule pathを読む。次stageはCore/plugin配置disabled、その後enabled。自動起動なし、同時に研究版へ更新しない。


## WORK-LOADER-RECOVERY-ACTUAL-20261025
- Work / P0 / PARTIAL。元フォルダでstage1(proxy単体)起動/save1/操作を利用者確認。PID9608とno config log確認。module一覧は取得結果なし、module path確認済みとはしない。
- 終了後Core/雇用DLLを既知SHAで配置、enabled0（PID15288 exit0）。Local poll1回timeoutは同じhandle再pollで終了確認、再実行なし。利用者起動/save1/操作成功。PID5232、empty plan log、plugin logなし（PID10636）。無効設定動作ACTUAL。
- 終了回答後processなし確認、設定だけenabled1へ変更・読戻（PID23728 exit0）。利用者へ起動→save1→人材雇用の並替え確認を依頼済み。stage3実機結果待ち。自動起動/EXE/DAT/save変更なし。
- 参照 _work/work_loader_recovery_actual_20261025.json。起動障害原因は依然未特定。選択UI統合/確定guardのLocal拒否は別残件。


## WORK-RECRUIT-LOADER-LIVE-PASS-20261025
- Work / P0 / 雇用接続 READY-FOR-INTEGRATION、全体目標 PARTIAL。元原版の直接起動→proxy/Core/雇用plugin enabled1で並替えを利用者確認。リセット1回と画面閉じ開きでも維持。biim兄貴を雇用し、所属移動・候補除外・残り並替えに問題なしと利用者確認。
- PID6776 init30452→worker30508→正しいUI3784、route_selected attempt3→installer_active→route_acknowledged。native EIGHT callsites hooked/renderer first/four-group n100 groups50,0,0,50。fixtureだけでなく実機導線成功。
- 証拠 _work/work_loader_recovery_actual_20261025.json更新、3logと配置SHA保存・読み戻し一致。原作EXE既知SHA保持。ユーザーの雇用操作は実行済み、セーブ上書きを依頼していない。元起動障害原因は未確定。
- 未完: 今回runの領地/資金各分岐、研究Core managed CALL移行、教育/アイテムselectorのCore接続・データ供給・確定guardと配布。今回雇用の成功を全基盤/selector完成とはしない。選択確定のLocal拒否は別件で残る。


## WORK-SELECTOR-CORE-ADAPTER-20261025
- Work / P0 / PARTIAL。停止VA=base+0x1E7E3 length5（既存generation CALL）。新規selector_plugin_adapterと専用build/fixture/docをcore内に追加。既存bridge/helperは変更せず、preview/stats/locationのみ、commit無効。
- Rootがbuild_selector_plugin.ps1 -Testを再実行、exit0。API/negative hook、非対応host無変更拒否、UI routing、重複予約拒否、worker生成失敗/installer失敗の保持を確認。独立review待ち。fixture結果を原作成功扱いしない。
- 原作への配置・起動・接続は今回なし。未完=review、実機loader接続、Pythonデータ供給の自動接続、既存確定guard拒否、配布検証。参照 core/SELECTOR_PLUGIN.md、_work/work_selector_core_adapter_20261025.json。

- 追記: 独立reviewはblockingなし。指摘された版照合不足を補い、現在ゲームに配置中の旧Core DLLそのものを指定してsynthetic host/production拒否fixtureを再実行、両方exit0。ゲーム接続なし。次は利用者終了確認後、既存雇用を維持してselector表示pluginを追加し実機確認。

- 配置追記: 利用者終了回答とVahrenなし確認後、HakushinSelectorPlugin.dll SHA 4a42badb34c04ebdeecbda6fcc0f83e40c4942f0e56e8fcd6e34747b936e7550をpluginsへ追加、manifestへhakushin.selector.preview enabled1/order20を追加し読戻一致。既存雇用/Core/proxyを交換せず、EXE/DAT/save変更なし。実機起動待ち、helper未起動、commit無効。

- 実機追記: PID22984の直接起動でselector installer_active/route_acknowledged（UI23168）を確認。利用者の講師一覧準備後、既存display-only senderを実行しexit0、66候補/epoch2のpanel opened。目視/検索/詳細/取消は利用者確認待ち。確定無効、watcher自動接続は未実装。証拠JSONへlog保存、文書読戻一致。

- 利用者実機確認: Core経由の66人一覧でチップ/検索/Lvソート/原作詳細/右クリック復帰すべて正常。表示接続はACTUAL。次は既存display-only watcherをPID22984に300秒限定で明示起動（exec session28836）し自動表示確認中。これは起動時helper自動連携の完成ではない。確定無効は維持。

- 自動表示試験は利用者「表示されない」。session28836はexit0/watcher_stoppedのみ、display_attemptなし。PID22984読取でpreview1/commit0/active0、epoch0、native visibility byte(base+0x4bb6d8+0x84)=00。候補12/result usechara_sentakuは残存。画面状態とvisibilityの対応未確定。自動表示成功とはしない。再起動/保護条件緩和なし、現画面の利用者確認待ち。

- 自動表示再試験: 利用者の名前一覧準備後、PID22984/epoch5/66候補をcaptureで確認。前watcher終了済みのため既存履歴を保持して300秒watcher開始(session76205)。display_attempt→panel opened→display_returnedを確認、目視回答待ち。原作起動時helper自動連携とは別試験。

- 利用者確認: epoch5自動表示が見え、右クリック後に再表示されない。session76205は時間上限でexit0/watcher_stopped確認。開き直し試験用に同一PID/履歴保持で3600秒watcher起動(session32998)、結果待ち。自動表示/取消維持ACTUAL、開き直しと起動時helper連携は未確認。

- 開き直し自動表示: 利用者が少し待つと出たと確認。watcher log epoch6/65候補はsnapshot changedで拒否、epoch7/66候補はdisplay_returned。遅延計測は別の現在epoch10/66候補でread-only実施: load_state26.036s、spot_names8.626s、education0.4621s、icons0.4486s、capture0.052s、assets constructor0.0018s。_work/work_selector_latency_20261025.json。reviewによりcatalogとspotnamesが各々全DATを解析する重複を特定。次は更新検知を保ちつつ共有解析/キャッシュ設計・計測、実行確定guardを迂回しない。

## WORK-SELECTOR-LATENCY-20261025
- Work / P0 / PARTIAL。停止VAなし（Python表示データ準備）。実測load_state26.036s/地名8.626sから、全DAT重複解析と表示用継承宣言の反復parseを改善対象とする。
- 担当selector_latency_review: catalog/assets/spot namesと専用testsのみ。担当selector_metadata_cache: display_metadataと専用testsのみ。root:統合計測/台帳。protected bridge/live/selector本体、ゲーム、DAT、save、Gitは変更しない。
- 設計:全DATのpath+内容hashで変更/追加/削除を検出しcaptured bytesを解析、有限キャッシュ。表示用宣言は正確なtextをキーに有限キャッシュ。実行時能力値/候補/epoch/contextはキャッシュしない。重複定義/警告/順序/シナリオ意味を維持。
- 完了条件:変更検出回帰試験、既存関連試験、cold/warm実測比較、独立review、実機開き直し比較。確定操作/起動時helper接続は別残件。参照 _work/work_selector_latency_20261025.json。

- 高速化実装: 全DATのcontent hash付き単一snapshot parse共有、表示宣言exact textの有限cacheを実装。root関連55tests PASS、担当間reviewでblockingなし。offline catalog cold4.646s+spot1.256s/warm1.236s+1.237s。実機after計測はPID22984終了/OpenProcess87、Vahrenなし確認で未実施。watcher32998 exit0。ゲーム再起動待ち、勝手に起動しない。_work/work_selector_latency_fix_20261025.jsonへ6変更filehashと検証結果保存。多ファイル読取は外部同時編集に対してatomicではない。

## WORK-SELECTOR-NATIVE-REPLACEMENT-20261025
- Work / P0 / OPEN。利用者追加要望: 教育/アイテム等の原作名前ボタン一覧を表示せず、新パネルだけ表示。即時に近い表示へ高速化。原作詳細の顔/技能/移動型へのhoverで説明を出す機能も新パネル利用中に動作させる（添付3画像根拠）。
- 方針: 原作選択の候補/イベント状態/確定/取消の意味を維持して描画・入力のみ差替える。必須イベントを閉じて飛ばさない。新パネル初期化失敗時は原作入力へ復帰。原作表示を無条件に消すだけの実装はしない。確定guard既存拒否は別途解消必要、迂回禁止。
- 低遅延: 起動/セーブ読込中の静的表示データ準備と再利用、候補/実能力値の都度取得。DAT更新検出を維持。現在の内容hash毎回全読取cacheだけでは即時表示の完成ではない。時間目標の達成は実測で判定する。
- 未完: 起動時helper連携、prewarm/低遅延更新検知、元一覧描画の抑止と復帰、詳細hoverの入力経路、確定/取消/強制選択の実機検証。停止VA未選定、既存generation base+0x1E7E3とnative detail成果から照合。

## WORK-REA-SESSION-20261025
- Work / P1 / PARTIAL。REAスキル42確認、active toolsにREA解析ツールなし。installed rea doctor --client codex --json exit0: Codex登録aligned/Node24.19/Ghidra12.1.4/Java21正常、live_server unknown。設定変更・再インストール不要。Codex再接続/再起動後tool公開確認、未解決なら起動logを読む。他engineのmissingは今回Ghidra利用の阻害としない。参照 _work/work_rea_session_diagnosis_20261025.json。
- hover: 原作ownerをEnableWindow(FALSE)にしているsource確認。既存native_detail所有条件上、単純enable禁止。安全なhover専用dispatchは未確定、保存済みGhidra vtable/ABI資料を確認開始。ゲーム操作/EXE新規解析なし。
- prewarm担当成果: work_selector_auto.py/new work_selector_prewarm.py/new test_work_selector_prewarm.py追加。最大256親宣言/2MiB先読み、display elapsed log、失敗時watcher開始なし。担当4新規+37既存tests PASS。root review/testは次回、まだ完成/実機反映扱いしない。現在helper session83619 PID5988は旧import版、再起動時はprocess状態を確認してから。

- prewarm root確認: static先読みをcontroller/session取得前に実行、失敗時watcher開始なし、候補/能力値/epochをcacheしない。rootでprewarm4+auto37 tests PASS。_work/work_selector_prewarm_20261025.jsonへhash/結果保存読戻。実機未確認、helper起動連携未完成。REA再接続待ちの間の独立作業として完了、原作の起動/操作/配置変更なし。

- 追加照合: prewarm独立reviewもblockingなし。prewarm_failedはexit0でもあり得るため起動連携はprewarm_readyを準備完了根拠にする。保存RTTIでTempStatusWndはStatusWnd/FadeWnd/FrameWnd/FrontView/Actionable継承を確認、hover呼出先は未確定。REA CLI6.7.0自体は利用可、function help確認済み（native provider指定可能）、MCP未公開とCLI不能を混同しない。既存Ghidraプロジェクト重複解析回避のため新たなfunction解析はまだ実行していない。

## WORK-SELECTOR-AUTOSTART-HOVER-20261026
- Work / P0 / PARTIAL。担当selector_latency_reviewはcore selector adapter/buildと新helper launcher/config/fixtureを所有。明示opt-in設定、直接CreateProcessW、固定引数、対象PIDのみ、単一起動、非表示console、成功installer後起動。失敗をlog、原作/commit不変更。配置前にroot review/fixture、まだ未実機。
- 担当selector_metadata_cacheはhover静的根拠のみ。現行V3verifyが14hash PASS、保存vtable/RTTIと関数照合。0x5214E0→0x51D140はdestructorのためhoverから除外。残りslot/inputは未確定。必要時は既存Ghidra project noanalysis/readOnly、広範再解析/原本書換え/原作実行はしない。
- 原作EXE/DAT/save/Git変更禁止、protected確定guard拒否の迂回禁止は維持。rootのみqueue/handoff更新。REA再起動確認待ちはこれら独立作業を妨げない。

- 自動helper起動実装root試験: native helper fixture/entrypoint3/adapter全fixture PASS exit0。明示opt-in/exe・entrypointhash/固定引数/hidden direct CreateProcess/ACTIVE一度だけ/非UI worker保持。_work/work_selector_helper_autostart_20261026.jsonへhash保存。独立review待ち、ゲーム未配置。hover調査では一時詳細TempStatusWndのhover slot+0x44がreturn0、隣接通常詳細の0x561120が候補。単純owner enableで解決とはしない。0x560650/0x560CA0は技能変更/解雇等を含むためhover転送に使わない。ABI未確定。


## WORK-SELECTOR-RESTART-REVIEW-20261026
- Work / P0 / PARTIAL。利用者のCodex再起動後、rootからREA binary_session応答を実際に取得。REA6.7.0/Ghidra12.1.4 available、target未open。設定変更/新規解析なし。参照 _work/work_rea_reconnected_20261026.json。REA接続不在の阻害は解消。
- 再起動後live agentなし、Vahren processなしを確認。既存hover証拠 tests/work_detail_hover_canonical_20261026.jsonの存在確認。
- 自動helper独立reviewでUTF-16設定の未指定と、installer遅延時に起動workerが先に終了する2点を特定。担当helper_reviewがcore launcher/adapter/fixture/docのみ修正中。ゲーム配置なし、確定guard変更なし。

- 続報: helper独立reviewの2不具合を修正。UTF-16LE BOM必須/非ACP文字fixture、遅延INSTALLING完了監視fixtureを追加。担当adapter全suite/entrypoint3PASS、root helper fixture再実行PASS。core/SELECTOR_HELPER_REVIEW_FIX_RECEIPT.txt参照。
- Vahrenなし/原版EXE既知SHAを確認後、selector DLLのみ38d13dfb7a68eac8e9b037fdc04e6955dae213e6242f864bed5a1bbac677084dへ交換。前版は_work/HakushinSelectorPlugin_before_autostart_20261026.dllへ保存。UTF-16LE設定を新規作成しPython/entrypoint hash固定。Core/proxy/recruit/EXEのSHA不変。ゲーム起動なし。
- _work/work_selector_autostart_deployment_20261026.json保存/読戻一致。利用者へ原版直接起動→水泳講師一覧で自動表示確認を依頼。未実機成功、commit無効、1時間watcher上限残存。元選択画面非表示/hover説明/即時表示は未完、成功扱いしない。

- 実機PID22320でhelper_hash_mismatch。確認依頼後に研究entrypointを更新したため配置pinと不一致になったroot運用ミス。ゲーム側専用HakushinSelectorHelper.pyへ複製しpin一致設定保存/読戻。起動worker一度のみのため再起動必要、現在DLL未交換。_work/work_selector_helper_pin_repair_20261026.json。以後確認中の配置物を研究ファイルへの直接参照にしない。
- hover ABI静的成果はtests/hover_abi_20261026.json。0x561120 ECX=self/stack x,y/ret8、clear0x562140 ret0。全領域転送はowner定義とpreview定義の相違が阻害。技能限定案の条件保存、まだ実装/実機なし。

- 利用者終了後Vahrenなし再確認、lifetime修正版DLLを配置・SHA読戻一致。game専用entrypointとPythonのpin一致。固定1時間制限を除きprocess終了まで監視、確定無効。_work/work_selector_helper_lifetime_deployment_20261026.json。実機起動成功は未確認。

- PID4724実機: helper_started26492/prewarm_ready16.86s/66候補epoch2検出後、No module named PILで表示停止。通常Pythonのuser-siteだけにPillowがあり-Iから不可視。手動試験と自動起動条件の不一致が原因。
- 原作終了済み確認後、既存_work/toolchains/selector_runtimeへ専用venv（pipなし）作成、既存PIL/pillow.libsを複製。-IでPillow12.3.0のRGBA32x32生成/4096bytes検証PASS、game側entrypointの同条件--help PASS。設定を専用exe+SHAへ更新/読戻。ゲーム起動なし。_work/work_selector_runtime_repair_20261026.json。次回実機表示未検証。
- 独立成果: skill hover新header/fixture x86,x64/既存detail回帰PASS報告、root未review・未統合。tests/skill_hover_validation_20261026.json。元一覧非表示は生成0x41E910の省略不可、描画getter chooser専用slot638238/return4C4D78での限定NULL返却が候補。tests/work_choice_render_research_20261026.json。静的のみ、原作変更なし。

- 独立skill hoverレビューblockingなし。rootもx86 fixture再ビルド実行PASS。原作の所有権/座標/target寿命/取消前clearの実機条件は未証明、production未接続。広範unittestは担当が不要に実施して終了済み、途中E3件のみ最終詳細未取得のため全件PASSとはしない。
- 元一覧描画抑止の独立部品をtests/work_choice_render_gate_isolated.hとfixtureへ追加。担当x86 PASS報告、exact self/returnsite/UIthread/epoch/visible overlayでのみNULL返却、それ以外原作getterへ戻る。root未review/未統合。Core所有/復元管理が必要。
- この区切りでもVahren processなし。実機自動表示確認は利用者再起動待ち。確認中の配置DLL/entrypoint/Python moduleは変更せず。研究成果は別header/fixtureに限定。

- PID10996自動表示をログ+Computer Use実画面で確認。66候補epoch2、prewarm7.96秒/display3.988秒。原作一覧はまだ背後に表示。_work/work_selector_autostart_actual_20261026.json。新規docs/SELECTOR_LOADER_RESEARCH_INDEX.mdへ配置構成/根拠索引/未対応/失敗教訓/再開手順を整理、読戻一致。利用者がゲーム起動終了含むPC操作を再承認、以後操作可能。セーブ上書きしない。

- root実機PID10996: Computer UseでLv見出しクリック→Lv昇順（先頭Lv5）、先頭行クリック→原作詳細、右クリック→panel/detail閉じ原作講師一覧が残ることを確認。教育実行/セーブ保存なし。_work/work_selector_autostart_actual_20261026.jsonへ追記。
- render独立reviewでchild panel幾何未検査を指摘→修正。surface clientにchild全域一致/positive size、零寸法・画面外・縮小で原作fallback。FP環境を保存後初期化してからAPI呼出、full x87/unmasked exception状態の復元fixture PASS報告。研究DLLのみ再ビルド、配置未変更。


## 2026-10-26 記録共有・研究版配置の追補
- 利用者要求: 有用な調査結果をPCに保存し、他チャット・AIが利用できる形式にする。入口は docs/SELECTOR_LOADER_RESEARCH_INDEX.md。主張ごとに根拠ファイル、検証段階、未解決事項を分ける。
- WORK-SELECTOR-NATIVE-REPLACEMENT-20261025: Work / P0 / PARTIAL。研究DLL 33b0cca79b1627e9d74f35fd32b7c198f2374debe7ec1f13935c787f5a051e04 を配置済み。以前の「未配置」はこの追補で更新する。バックアップ _work/HakushinSelectorPlugin_before_render_20261026.dll（faf39b3df2da93b48fb09b4b82407c6dbff8945182f2fa537e7853f9dfd7d933）。配置receipt: _work/work_selector_render_deployment_20261026.json。
- 起動確認: PID23724、開始2026-10-26 02:48:58+09:00、原版のパスを照合。再確認でもMainWindowHandle=0、タイトル空欄、Responding=true。画面未表示。停止・クラッシュ・DLL原因とは未確定。二重起動はしない。
- 再開位置: 現PIDの存在・作成時刻・モジュール・起動ログを再確認し、必要ならこの試験プロセスの終了確認後にバックアップDLLへ戻して比較。原作EXE/DAT/セーブは変更しない。元一覧の描画抑止は実機未確認、確定操作は無効のまま。
- 停止VA/対象: 描画getter slot 0x638238、呼出戻り先0x4C4D78。生成0x41E910は省略禁止。参照 data/recruit_sort_v4/tests/work_choice_render_source_integration_evidence_20261026.json。
- 記録運用: 他担当は索引→キュー→固定handoff→個別receiptの順に確認。過去の追記より最新の追補を優先し、推測を確認済みに昇格しない。キュー編集はWorkのみ。


## 2026-10-26 元一覧描画抑止：最初の実機確認
- WORK-SELECTOR-NATIVE-REPLACEMENT-20261025 / Work / P0 / PARTIAL。参照 _work/work_selector_render_actual_20261026.json。
- 画面なしPID23724はidentity/starttime/handleを再確認後終了。x86列挙ではlocal DINPUT8まで、Core/selector未ロード。CoreはDirectInput8Create経由で起動する（core/dinput8_proxy.c:29,48,56、hakushin_startup.c:95,98）。DLL原因とは断定不可。
- 同じ配置ファイルのままExplorerから原版起動→PID22200、タイトル/セーブ読込/操作成功。起動経路差は確認、cwd等の根本原因は未確定。
- save1 Easy turn6、水泳講師7候補。prewarm7.468s、display_returned15.343s。画面で新パネルと元名前ボタン一覧の非表示を確認。右クリックすると新パネルが閉じ、元一覧が復帰。教育未実行・セーブ上書きなし。
- 残件: 準備中には元一覧が見えるため完全即時置換は未達、15秒遅延要計測、hover未統合、確定無効、他文脈/必須選択/ウィンドウ移動等未検証。現在PID22200は原作講師一覧で開いたまま。追加起動前にプロセス確認。


## 2026-10-26 DAT重複読取削減・計測境界の修正
- WORK-SELECTOR-LATENCY-20261025 / Work / P0 / PARTIAL。元プロセスPID22200とhelper17352の終了を確認してからPython sourceを変更。次の起動がこの版をimportする。新実機試験はまだ。
- 調査: _work/work_selector_prepare_profile_20261026.json。7候補でcapture約0.05s、icons約0.05s、load_state約2s/spot約2s（cProfile付き）。15.343sのdisplay_returnedはshow全体であり、画面表示までの時間そのものではない。従前の「表示に15秒」はこの区別で訂正。
- script_snapshot_scope(assets)を追加し、1回の表示準備/prewarmでcatalogとspotsのDATを共有。次の処理で必ず再列挙・内容hash照合。runtime候補/能力/教育結果はcacheしない。同期scope終了で解除、別assetには使わない。同時ファイル編集に対してatomicではない。
- 実DATベンチ: 590DAT/387地名、別読込2.073/2.0953s→共有1.1596/1.2906s、読込1180→590。定義/名前/地名/警告一致。UI全体の時間ではない。再実行可能 _work/benchmark_selector_snapshot.py と結果 _work/work_selector_snapshot_benchmark_20261026.json。
- 計測: dat_snapshot_captureほかstage時間、panel_accepted（rendered_verified=false）、display_completedを分離。拒否/timeoutで再送しない。ログ失敗はゲーム要求の挙動を変えない。
- root関連25+15=40 tests PASS。独立scope review blockingなし。全体suite PASSや実機速度達成とはしない。protected3file hash一致確認、確定無効維持。
- 参照 _work/work_selector_snapshot_integration_20261026.json、work_selector_snapshot_scope_20261026.json、work_selector_display_timing_20261026.json。次は原版をExplorerから1回起動→水泳講師一覧、panel_acceptedと画面を照合→取消復帰。開く前にVahren存在確認。


## 2026-10-26 最新実機確認：講師・生徒の自動表示と記録共有
- 依頼ID: WORK-SELECTOR-LATENCY-20261025 / WORK-SELECTOR-NATIVE-REPLACEMENT-20261025。担当 Work、優先度 P0、状態 PARTIAL。停止VA: 描画 getter slot 0x638238 / return 0x4C4D78。生成 0x41E910 は省略禁止。
- 根拠: ../_work/work_selector_snapshot_actual_20261026.json（原ログ抜粋・各段階の時間・配置SHA・画面確認・未確認項目を同梱）。保存後JSON読戻一致、SHA256 9349eef058732ab07050760bd433a6ea13c268c362cb6c0528a5eddf4f71f563。
- PID13228、save1 Easy turn6。講師7人: DLL表示受付2.591秒、後処理完了3.072秒。生徒6人: 受付2.474秒、後処理完了3.144秒。起動時先読み6.495秒は別計測。受付時刻は描画開始時刻ではない。
- 実画面確認: 講師・生徒のパネル自動表示、パネル中の元ボタン一覧非表示、講師AKYSの原作詳細一致、右クリックで元一覧へ復帰。生徒の所在地「岡山県南」と予想結果「成功／大成功」を確認。生徒選択・教育実行・セーブ上書きなし。予想と実結果の一致は未検証。
- 現在地: 原作PID13228はAKYSを講師に選んだ後の原作生徒一覧で開いたまま。新パネルは右クリックで閉じた。再開時はPID/作成時刻/画面を確認し二重起動しない。
- 未完了: 準備中は元一覧が一時表示される。瞬時表示、ホバー説明統合、現在のパネルからの確定、必須ランダムイベント、配布用依存分離は未達。既存の確定guard拒否を別経路で迂回しない。
- 他担当の入口: SELECTOR_LOADER_RESEARCH_INDEX.md → 本キュー → CHATGPT_CURRENT_HANDOFF.md → 根拠JSON。古い「未実機」「15秒で表示」よりこの測定境界と新実機記録を優先。共有キューはWorkのみ編集する。


## 2026-10-26 継続作業：地名準備とホバー統合条件
- WORK-SELECTOR-LATENCY-20261025 / Work（spot_projection_cache担当）/ P0 / PARTIAL。原作PID13228を通常終了し、Vahren・Python helper不在を確認後に着手。対象はwork_selector_spot_names.pyと関連テストのみ。DATを毎回検証した後、同じ内容の地名変換結果だけを上限付きで再利用する。ゲーム未起動・確定処理変更なし。
- WORK-SELECTOR-AUTOSTART-HOVER-20261026 / Work / P1 / PARTIAL。停止VA 0x561120・0x562140・0x455D90。読取レビュー成果: ../../data/recruit_sort_v4/tests/work_skill_hover_host_review_20261026.json。ゲーム座標変換、排他所有、描画済み確認、取消失敗の後始末、他ウィンドウ上のカーソル除外が未完。本番接続前にこれらを満たす。既存100msタイマーを利用でき、新しい入力フックは不要。

## 2026-10-26 地名変換再利用：実機確認まで完了
- WORK-SELECTOR-LATENCY-20261025 / Work / P0 / PARTIAL。地名準備の局所修正は実装・試験済みだが、瞬時表示の要求は未達。停止VA: 該当なし（Python静的DAT表示準備）。
- 変更: work_selector_spot_names.py。最大2件、全ソースの順序付き(path,内容SHA256)をキーに地名・警告の変換結果を再利用。毎回の読取・内容照合は維持し、返却dictは独立。実行時の所属/能力/候補/予想はcacheしない。
- root関連33 tests PASS。実DAT590件・地名387件の比較3回すべて地名/警告一致。変換約0.16〜0.18s→約0.00035s（部分処理、全UI速度ではない）。参照 ../_work/benchmark_selector_spot_projection.py、work_selector_spot_projection_benchmark_20261026.json。
- 原作PID4972（開始06:55:34）、save1 Easy turn6、水泳講師7人。表示受付2.103秒、後処理2.409秒、外側呼出2.478秒。地名準備stage0.014秒。自動表示・元一覧非表示・チップ/能力・岡山県南/迫真空手道場・右クリック復帰を実画面で確認。教育実行/セーブ上書きなし。受付は最初の描画フレームではない。
- 根拠 ../_work/work_selector_spot_projection_actual_20261026.json（SHA c8aa7ccd07727f9e03bd95f6d12ae6463509981d7b8b9a1b24bb46a2b0725217）。ログ抜粋/変更ソースSHA/実機制約を同梱、読戻一致。
- 再開位置: PID4972は原作の講師一覧で開いたまま。パネルは右クリックで閉じた。次回はプロセス・作成時刻・画面を確認。起動中のPython import元は変更しない。
- ホバー統合条件レビューは ../../data/recruit_sort_v4/tests/work_skill_hover_host_review_20261026.json。実装接続は未完。座標、所有権、描画済み保証、取消失敗、別ウィンドウ上の除外の5点を満たしてから接続。通常hover全体を直接呼ばない。
- 未完了範囲は維持: 確定操作、瞬時表示、準備中の元一覧抑止、ホバー、必須イベント、配布用依存分離。目標完了とはしない。


## 2026-10-26 共有記録の運用補足（利用者の追加指示）
- 有用な成果は会話だけに残さず、SELECTOR_LOADER_RESEARCH_INDEX.mdを入口として既存資料へ整理する。新しい引継ぎファイルを重複作成しない。
- 各成果には対象版・ファイル/関数・根拠への参照・確認方法・結果・未確認範囲・再開手順を記す。STATIC、単体試験、実機観測、利用者確認を分ける。
- 成功だけでなく失敗、採用しなかった案と理由、接続/自動審査拒否も記録する。過去の成功を現在の配置版の成功として流用しない。
- 共有依頼キューはWorkのみ編集。他担当は所有する成果ファイルへ保存し、Workが照合して依頼ID・担当・優先度・停止VA・未完了範囲・参照先・状態を更新する。
- 最新の利用者許可：不在中もPC操作およびゲームの起動・操作・終了を許可済み。過去の「利用者が操作する」記述より本指示を優先する。セーブ上書きは行わない。
- 最新再確認：test_work_unit_selectorは11件中10PASS/1ERROR。test_reject_ambiguous_student_even_with_common_buttonsで生徒候補の拒否に至らずcatalogfrom_assets(None)相当の経路へ進む既知の未修正。全件成功とは扱わない。
- 当該3ファイルのLocal修正拒否は以前の限定承認後にも継続した記録がある。現行get_configはversion0.3.1でblockedCommandsにscを含む。過去のC変数名誤認の再現記録と、現行設定確認を区別する。今回、新たな書換え再試行・設定変更・迂回は実施していない。現行UIの確定は無効のまま。


## 2026-10-26 ホバー説明：原作側競合経路の特定
- 依頼ID: WORK-SELECTOR-HOVER-20261026 / 担当: Work（証拠担当 hover_coordinate_evidence・hover_ownership_evidence）/ 優先度:P1 / 状態:PARTIAL。
- 停止VA:0x521A00の上流仮想呼出と0x521560通常hover dispatcher。未完了範囲:排他接続、取消時clear、実機ホバー、顔/能力/移動型説明。まだ本番接続しない。
- 静的根拠: ../../data/recruit_sort_v4/tests/work_hover_coordinates_20261026.json（SHA902b33eecb5a7a431092e1ba270e7059e1c7f6ab838ce922f5c70e1bad4017a3）、work_hover_ownership_20261026.json（追補SHA c78bac0c604ef8d1de2efdd25b7123716fd03bc0962700366ae8b77f46c36845）。後者は初版764bad…を更新済み。
- 原作GetCursorPos→ScreenToClient取得箇所には倍率変換なし。幅0x65BEEC/高さ0x65BEF0との一致を要求する案。DPI/全画面での完全検証は未実施。55BAB0→55BC60→55DA70の通常openは同期描画、hide-only早期returnは別扱い。
- 重要:521A00→521560→window+0x30→455CF0→StatusWnd+0x44(561120)、clearは+0x34→455D20→+0x48(562140)。521560は879823を検査せず、5233A0より先に実行。したがってEnableWindow(FALSE)や879823=0で説明表示の排他を保証できない。両フラグ0も保持済み座標経路の排他証明にはならない。
- 実機read-only: ../_work/work_hover_runtime_baseline_20261026.json、../_work/work_hover_runtime_panel_20261026.json。原作PID4972/base0xC10000/SHA一致。原作一覧時822/823=1/1、パネルのAKYS詳細表示時=1/0、幅高さ1320x990、detail visible1・skill_count17。逐次読取なので原子的snapshotではない。既存WinProcessReaderを使用、フラグ書換え・hover呼出なし。
- Computer Useで7人パネル、AKYS行と詳細一致、元選択肢非表示を確認。最後に右クリックしてパネル/詳細が閉じ、原作講師一覧が復帰した。教育実行・アイテム使用・セーブ上書きなし。ゲームPID4972は原作講師一覧で開いたまま。
- 次:通常hover dispatcherの所有権と呼出条件を既存Core管理で扱える最小接続を検討。単にタイマーから561120を追加呼出する案は採用しない。今回ソース/DLLの変更なし。座標/排他の新しい根拠が次の実装方針を変更したため進捗として記録する。


## 2026-10-26 ホバー接続案の採否・再開位置
- WORK-SELECTOR-HOVER-20261026 / Work / P1 / PARTIALを維持。根拠JSON ../../data/recruit_sort_v4/tests/work_hover_ownership_20261026.json の最新版SHAは e3c45e55d70aae2272f0ede24c6fdbcd1d54059877b2b9d2b9e6a6255ded0611。過去SHAは履歴。
- 不採用1:TempStatusWnd+44だけの転送。+50および+1Cは43B5A0(return0)で原作dispatchから除外される。両方を有効化するとmouse-down/up560650/560CA0も通り得るので単純有効化しない。新規route prototype担当はこの証拠で中断、ファイル未作成をrootが確認。
- 条件付き候補:521AF0のCALL521560。保存命令は521AEE mov ecx,ebp／521AF0 E8 6B FA FF FF／521AF5 test al,al。ECX入力とALの消費は確認、完全ABIと直後分岐bytesは不足。AL=1でもmode2などでは526A40の入力処理へ進むため万能停止ではない。
- 先行520980/5203A0や会話521D90経路はこのCALL置換で抑止できない。Player+42Cの既存hover解除も飛ばすので開始終了の解除設計が必要。入力全体の停止・推測の戻り値で接続しない。
- 次の実装判断に必要な最小条件:戦略限定modeの検証、Playerコンテキストと前回hover所有者、先行経路のtooltip更新、cleanupの順序、完全ABI。上流を無制限に解析せず、この接続案の採否に限定する。既存Core managed CALLは研究版で実機未配置、現在のCore予約APIと混同しない。
- この回は調査で危険な2案を除外し停止VA/条件を具体化した。製品コード・DLL・原作EXE/DAT/save変更なし、テスト追加なし、ホバー実装済みとはしない。PID4972の存在を再確認。ゲーム状態は前回の原作講師一覧から操作していない。


## 2026-10-26 呼出規約確認・先行処理の条件（最新追補）
- WORK-SELECTOR-HOVER-20261026 / Work / P1 / PARTIAL。停止VA: 0x521AF0→0x521560。本番への接続・実機ホバーは未完。
- REA/Ghidraによる原版SHA e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187 の静的確認。521560はECX=Player、明示stack引数なし、通常RET、戻り値はAL。521AF5のTEST AL,ALと後続分岐を確認。AL非zeroでも戦闘mode2では526A40へ進み得るため万能停止ではない。
- 原証拠: ../../data/recruit_sort_v4/tests/work_hover_call_abi_rea_20261026.json（SHA256 3c412230ce9db6a0b37d0873ab50f0de182d7b4b211a7be96046ed468b43b031）。旧追補の「完全ABIと直後分岐不足」はこの範囲で更新する。
- 先行処理の静的条件: 520980はPlayer+468==Player+46Cで副作用前return、5203A0はPlayer+438==0x80000008で本文前return。呼出後の521AF0で検査するだけでは、その回の先行副作用がなかった証明にはならない。状態を強制変更しない。
- 追補根拠: ../../data/recruit_sort_v4/tests/work_hover_ownership_20261026.json（最新版SHA256 fc5ee5d8143671ca9515647c78db91a43a33d14f26030917174fa90a21242a15、過去SHAは履歴）。担当成果の読戻とroot側hash照合済み。
- 次の一手: 正しいPlayerの同定と上記フィールドの読取観測、戦略限定条件、以前のhover所有者の解除順を確認し、接続可否を決める。既存の座標・所有権JSONを先に読む。関数全体の重複解析は不要。
- 今回は記録整理と静的根拠の回収。新規DLL配置・ゲーム操作・教育実行・セーブ変更なし。PID4972は前回確認値であり、再開時に再確認する。


## 2026-10-26 同期ホバー接続部品：実装・単体検証
- WORK-SELECTOR-HOVER-20261026 / Work（hover_dispatch_thunk実装、hover_ownership_evidence独立レビュー）/ P1 / PARTIAL。停止VA:521AF0。本番接続・画面確認・取消時cleanup統合は未完。
- 実測: ../_work/work_hover_precall_runtime_20261026.json。PID4972/baseC10000、mode1、既存hover/captureゼロ、移動/拡縮idle。Player+4と+194を直接等値比較したcontext_matches=falseは異常ではない。保存資料51E100および実測で+194=*(+4)+504を確認した。原記録は保持。
- 訂正:同期CALL境界の後で更新する設計では、完了済みの先行処理に副作用がないことは必須条件ではない。idleは診断値。callsite迂回・以前のhover解除・mode2後段・再入は別途対応が必要。
- 新実装: ../../data/recruit_sort_v4/src/work_selector_hover_context.h（対象/コンテキスト/戦略mode/旧hover照合、二重読取、失敗時出力不変）とwork_selector_hover_dispatch.h（x86同期callback、原作へのfallback、GPR/flags/x87/SSE/stack保全）。まだ隔離部品であり配置DLLは交換していない。
- 試験: contextは初期stubでRED→実装後x86通常/O2 PASS。thunkは通常/O2各10004呼出PASSをrootも再実行。既存skill_hover回帰PASS。独立contextレビューにblockingなし。全体suite成功や実機ホバー成功を意味しない。
- 再実行: ../../data/recruit_sort_v4/tests/run_work_selector_hover_context.ps1 とrun_work_selector_hover_dispatch.ps1。証拠/SHA/未検証範囲はwork_hover_context_receipt_20261026.json（SHA6b07d06d648a8cc43331f2b0380178cca03732af52dc48b1da70d1016404e974）およびwork_selector_hover_dispatch_receipt_20261026.json。
- ownership根拠最新SHA:ed3a901d5a202097bacea041e2d8996874cc361cea402d68a0b268746370954a。過去fc5ee…は前版。REA原証拠を保存済みのため対象をcloseした。
- 次:既存previewのopen/row変更/closeにcleanupを接続し、同時に同期dispatchから技能hoverするhost callbackを実装・試験。その後Core管理下で限定配置する。preflight単体を所有権保証と誤認しない。確定guard拒否を迂回しない。ゲーム/セーブ操作なし。


## 2026-10-26 同期ホバー：preview・Core adapterへの組込みと研究DLLビルド
- WORK-SELECTOR-HOVER-20261026 / Work（host: hover_host_integration、review: hover_dispatch_thunk）/ P1 / PARTIAL。停止VA:521AF0。今回は実装が進んだが、実機接続はまだ。
- work_selector_ingame_preview.hに行変更/取消/破棄前の説明cleanupを接続。work_selector_hover_integration.hで同期技能hover、画面座標/遮蔽/対象/世代/UI thread判定、失効時の所有権放棄を実装。タイマーは取消専用。顔・能力・移動型の説明は未対応。
- selector_plugin_adapter.cは機能有効ビルドだけCore拡張3をinit中に取得し、既存bridge/render成功後にUI threadでインストーラへ渡す。通常ビルドは無効。Core管理CALLに別の予約を重ねない。原作EXE/DAT/save変更なし。
- レビュー指摘「hover非active時のunsafe fallbackで詳細所有権を残す」をREDで再現して修正、再レビュー済み。root再実行: host8構成PASS、adapter成功/bridge失敗時skip PASS、既存adapter回帰 -Test exit0。最適化試験は-UNDEBUG。全suite成功とはしない。
- 研究成果物: ../../data/recruit_sort_v4/tests/HakushinSelectorPlugin-hover-research.dll（SHA6318a75fe9fdedbea5c1da2a4556ac3c01101dde659e2f6ed9d5b791c9e0fdc1）。-Wall -Wextra -Werrorでビルド成功。配置中DLLは33b0cca…のまま、Coreも961712…のまま。3つの拒否対象ファイルSHAは既知値と一致。
- 根拠: ../../data/recruit_sort_v4/tests/work_selector_hover_integration_receipt_20261026.json（SHAe04ed5700a2e78dd9a3cb4af89e1aeb8ab0dc4bbef9c943b3f78ceddc784af3b）とwork_selector_hover_host_receipt_20261026.json。再実行: tests/run_work_selector_hover_host.ps1、core/test_selector_hover_adapter.ps1、core/build_selector_hover_research.ps1。
- 残条件: UI message境界だけでは他threadが5byte書換対象を実行していない証明にならない。インストール時の実行安全性を確認後、バックアップを保持してCore/selectorを限定配置し、原作でhover→行変更→右クリック→元一覧復帰を確認する。現状を実機対応済みと呼ばない。


## 2026-10-26 他AI向け再利用記録の整理
- 入口：SELECTOR_LOADER_RESEARCH_INDEX.md冒頭へ、記録形式と最新ホバー統合記録への直接参照を追加した。既存記録を利用し、重複した引継ぎファイルは増やしていない。
- WORK-SELECTOR-HOVER-20261026 / Work / P1 / PARTIAL。停止VA:0x521AF0。研究DLLはビルド・隔離試験済み、未配置・実機未確認の区別を冒頭に明記。
- 既存資料からPlayer+90登録→4C28D0 virtual+4→521A00、4C24B0のメッセージ処理loopという限定経路を担当が確認中。WH_GETMESSAGE対象threadとの一致は未確定であり、書換えの安全性確認済みとはしない。正式根拠は担当所有JSONへ保存してから照合する。
- core/SELECTOR_PLUGIN.mdは旧版配置済みと新ホバー研究版未配置を区別する説明に更新済み。次は所有権根拠を回収し、接続可否を判断する。ゲーム・原作・セーブへの追加変更なし。


## 2026-10-26 最新配置・実機試験の引継ぎ（主HWNDガード後）
- 依頼ID WORK-SELECTOR-HOVER-20261026 / 担当 Work / 優先度 P1 / 状態 PARTIAL / 停止VA 0x521AF0→0x521560。未完了: 技能説明の実画面表示、顔/能力/移動型の説明、取消回帰。確定は無効のまま。
- 主ウィンドウ実値 image_base+0x4797FC と親HWND・UI thread・processを照合するガードを追加。別HWNDへ変化した場合は所有権を放棄。tests/run_work_selector_hover_host_main_guard.ps1はO0/O2と既存8構成PASS、研究DLLビルド/Core CALL試験もexit0。単体成功は実機hover成功を意味しない。
- 根拠・現在SHA・起動比較・ログ抜粋: ../_work/work_selector_hover_deployment_20261026.json。このJSONは初回配置記録を保持して現在状態を追補。関連: work_hover_main_thread_actual_20261026.json、work_hover_launch_diagnostic_20261026.json、../../data/recruit_sort_v4/tests/work_hover_ownership_20261026.json。
- 配置: 元ゲームは旧Core 9617124c…/selector 33b0cca7…へ復元済み。診断用 startup_clean_20261025 以下に研究Core abffd3e3…/selector 0fa2145d…と拡張ファイルを配置。診断用コピーも現在は拡張入りであり「無拡張比較対象」ではない。両EXEは未改変SHA e8dac301…。
- 起動比較: 元フォルダは旧DLL復元後も、ローダーを一時除外しても起動中にexit0。原因は未確定。診断用はタイトルまで成功し、研究版でもsave1→水泳講師7人パネル/AKYS詳細を確認。二重起動が原因と断定しない。
- 表示受付2.019秒、後処理2.614秒。受付は最初の描画時刻ではない。技能アイコン上へ移動しても説明は見えなかったため、hover成功とは記録しない。CALL置換bytesは確認、会話flags2個は0。次はdispatch到達/ガード拒否/所有権失効を最小診断で切り分ける。
- 最新プロセス確認 PID20976 / HWND5638618 / 診断用コピー。ゲームを開いたまま。実操作前にidentityを再確認する。教育実行・セーブ上書きなし。
- 通常UI thread呼出鎖は保存資料で確認。任意の間接呼出を全排除した証明ではない。REAの追加Ghidra解析は330秒timeoutで終了しtarget close、設定変更なし。保存済み静的資料で限定継続。


## 2026-10-26 ホバー診断の続報：操作ツールによる遮蔽
- WORK-SELECTOR-HOVER-20261026 / Work / P1 / PARTIAL / 停止VA 0x521AF0。新診断機構で原因条件を特定。安定した実機hover完成ではない。
- 診断版EF958…を診断用コピーPID24116で試験。AKYS選択後flags239：所有権・対象・座標は成立、cursor_uncoveredのみ不成立、native_hover0。根拠 ../_work/work_hover_diagnostics_akys_skill1.json。
- ../_work/work_hover_occlusion_akys_skill1.json：上位2ウィンドウはPID22116の全画面領域。プロセス確認でcodex-computer-use.exeと一致。surface範囲外・UIthread captureなし・子判定=mainは成立。自動操作ツールに影響された試験。安全判定やプロセス名例外は変更しない。
- 研究版で説明が一度表示されたが切替えは未安定。右クリックでパネル/詳細を閉じ原作一覧へ復帰する実画面確認は両版で成功。教育実行・セーブ上書きなし。
- 診断コードのwrong-thread時UI参照を独立レビューで修正。worker RED/GREEN、root12構成PASS（PID16640 exit0）。最新診断artifact SHA4d0926d1546b66aece8f68ebf54e10c97d97bdd20add72724cadb1a0227f1d54は未配置。
- ゲームは通常終了済み。Vahren不在確認後、診断用コピーselectorを研究版0fa2145d…へ復元（PID3004 exit0）。元フォルダの旧DLLは変更なし。古いPID20976/24116を現在のプロセスとして使わない。
- 再利用：tests/work_selector_hover_host_receipt_20261026.json、tests/run_work_selector_hover_host_diagnostics.ps1、../_work/read_hover_diagnostics.py。readerは旧診断SHA/PID固定のため再利用前にidentity更新が必要。外部occlusionとゲーム内座標はDPI差があり数値を直接比較しない。
- 次：自動操作overlayがない条件で技能説明切替え/消去を確認。それまで独立したselector/loader残件を進める。顔・能力・移動型説明、確定、完全即時表示は未完。Local接続timeoutにより他の固定記録への反映成否は再確認する。


## 2026-10-26 helper相対配置・互換性の検証確定
- WORK-SELECTOR-HELPER-RELOCATION-20261026 / Work（実装adapter_review、独立review hover_dispatch_thunk）/ P2 / READY-FOR-INTEGRATION / 停止VA:該当なし。配布版統合・別PC実機は未完。
- 設定の .\ および ./ から始まるパスを、検証済みゲームディレクトリ基準で解決する。作業ディレクトリに依存しない。相対パスの親移動・曖昧な区切り・長すぎる値は拒否。既存絶対パスは従来validatorを保持。
- 独立レビューP2で絶対source_root末尾区切りと . / .. 正規化の互換性欠落を発見。実child回帰RED→修正GREEN、再レビュー解決済み。root再実行PID25988: test_selector_helper.ps1 + build_selector_plugin.ps1 -Test exit0。Python test_selector_helper_entry.pyは5件PASS/PID16164 exit0。全プロジェクトsuite成功とはしない。
- 根拠・再現手順・SHA: ../../data/recruit_sort_v4/core/SELECTOR_HELPER_RELOCATION_RECEIPT.txt と SELECTOR_HELPER.md。launcher SHA b83fdbc9efc56afe2deecf17657677a4f06b9f3dcdc1b57eb7ae6086fc376d1c、fixture SHA 28d5dc5c3020a7939920824ab87436d0bef084ccd0ebbfd01b99237321a3c985。
- 未完: Pythonはインストール済みPython312依存venvであり可搬runtimeではない。Pillow/Tclと36モジュールの依存閉包、書込み可能state配置、配布一式を別途統合する。exe/entrypoint hashだけで全importの保証とはしない。新helperは未配置、原作EXE/DAT/save変更なし。
- 配置記録訂正: ../_work/work_selector_hover_deployment_20261026.json更新・読戻済み、SHA FE3DE03B286895E660B13A3458106B2798FFA22B3B22E14436CA89CF917C4576。stage=game_closed_diagnostic_removed_research_restored_in_clean_copy。過去の更新未確認記述を訂正。
- ユーザー復帰。次は自動操作ツールを使わず、診断用コピーの研究版0fa2145d…で技能説明の切替・消去を人手確認する。確定機能は無効のまま。元フォルダ起動不安定の原因は未確定。


## 2026-10-26 人手再試験：行選択の切替えを再確認
- WORK-SELECTOR-HOVER-20261026 / Work / P1 / PARTIAL / 停止VA 0x521AF0。ユーザー初回報告は『一度選ぶとパネルが切り替わらない』。終了・再起動後は『今回は切り替わり、詳細も表示』。両方保持し安定完了とはしない。
- 読取照合時の現在プロセスは診断用コピー PID9640、CreationDate Unix ms1793000655049。selector logはinstaller_active/UI thread20512/helper PID17920。helper末尾はepoch2/66人、panel_accepted 2.271秒、display_returned 3.248秒。描画時刻や技能hoverの成功を意味しない。
- 先行試行PID25740のhelper末尾transport_stoppedはゲーム終了後に取得したため、切替不能の原因と断定しない。自動操作ツールの遮蔽だけで今回の症状すべてを説明できるとはしない。
- 次は人手で2つの技能アイコン間の説明切替と右クリック復帰を確認中。確定・教育実行なし。今回こちらはUI操作/配置交換なし。過去『全ゲーム終了済み』はPID9640確認時点で失効。使用前は再確認。


## 2026-10-26 設計再評価（正式変更前）
- WORK-DAT-GENERIC-UI-REVIEW-20261026 / Work / P1 / READY-FOR-INTEGRATION（評価案のみ、実装未承認）/ 停止VA 0x4A1250（ABI未検証）。参照 DAT_GENERIC_UI_DESIGN_REVIEW_20261026.md。
- DATが候補/独自列/結果予想を渡す汎用UIを条件付き推奨。最大未確定はVM待機・1回だけ結果返却・runtime unit識別。現行検出は互換adapterとして保持。正式目標変更なし。
- 最新Ghidra V3検証PASS、14入力照合。新規REA解析は既存資料で判断材料が揃うため実施せず重複解析回避。静的証拠と実機成功を区別。
- ホバー診断担当は安全な区切りで停止。tests/test_work_selector_hover_host_row_diagnostics.cのみ31行のRED scaffold、strict build成功/期待exit1、runner未登録。production/DLL/配置変更なし。レビュー根拠 tests/work_selector_hover_row_stall_review_20261026.json。未完コードを完成扱いしない。

## 2026-10-26 DAT明示呼出の最小実証：承認・着手
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL。停止VA 0x433B62→0x4A1250、choice完了0x41E6D0。未完：実機待機/一度だけ返却/取消/無効時fallback、3候補の往復。正式な全面移行は未実施。
- ユーザーは最小実証を承認。DATが補正値を渡し、DLLは教育式や種別推測を持たない方針を再確認。計画：DAT_GENERIC_UI_SPIKE_PLAN_20261026.md。
- 保存証拠：../../data/recruit_sort_v4/tests/work_dat_ui_dispatch_evidence_20261026.json と work_dat_ui_result_evidence_20261026.json。静的ABI根拠あり、実機接続成功とはしない。
- 未配置fixture tests/work_dat_ui_spike_v1.datは数値変数名参照と取消index3限定へレビュー修正。静的parse/構造検査exit0、SHA57cf3d5aebea79cfa8a22b9e70c0bfae7fbda9eecffd9dbc000045ec9d7efe20。原作fallbackもまだ実機未確認。
- 汎用数値列とnative非依存の3候補要求契約を別担当が実装中。原作EXE/DAT/save、配置DLL、拒否対象3ファイルに変更なし。入口ABI根拠だけで待機/返却可能と断定しない。

### 2026-10-26 最小実証の要求契約を追加
- 新規 src/work_dat_ui_request.h と tests/test_work_dat_ui_request.c / run_work_dat_ui_request.ps1（data/recruit_sort_v4以下）。3候補の所有コピー、独自signed数値、古い要求拒否、一度だけ確定/取消を実装。native読書きやゲーム接続なし。
- 独立レビューで現契約内の不具合なし。panelのsource_indexと要求ordinalは別物のため、明示変換 wdui_ordinal_for_source を追加。並替え後の別人誤選択を防ぐ。
- strict x86 RED→GREEN。root再実行PID9692 exit0。変換追加後の再実行PID18940はPASS出力、終了確認は後続記録を参照。
- header SHA e291502145c80f559ded49c33f9458ae2aae8b5a4569b29b3290bd1d4a3b3ebe、fixture SHA954d07108218d113f849a4fabe383da284b67b08604a7a16ff87eea58e93c642。
- 制限：3候補固有IDのみ・caller直列化。generationの真正性、DAT数値変数の解決、UI接続、VM待機/完了はadapter側の未完事項。試験成功をDAT往復成功と扱わない。
- 追記：root PID18940も終了コード0を確認。要求契約の検証完了、ゲーム側への接続と往復は未完。汎用数値列担当の成果回収・独立レビューを次に行う。

### 2026-10-26 汎用数値列と要求契約の結合試験
- src/work_selector_panel.hにrequest所有の独自数値列APIを追加。教育のmagdefや式には依存しない。欠損は末尾、同値は元順、signed端値、列追加/削除との共存、検索後のsource_indexを確認。
- root実行：run_custom_column.ps1 PID3264 exit0。既存test_work_selector_panel.c strict x86再ビルド/実行PID4372 exit0。独立read-onlyレビューで本変更の不具合なし。ゲーム配置なし。
- tests/test_work_dat_ui_panel.c + run_work_dat_ui_panel.ps1：hidden Win32表→列ソート→検索→選択→source_indexからordinal変換→kmr/value55返却を結合。root PID12200 exit0。取消は結果を送らず、古いgenerationは拒否。取消からDAT再開する処理はまだ未実装。
- 意図的なsource=ordinal取り違えでは結合試験が失敗することを担当確認。fixture SHA dfbb49bfa17272ab68655531897d8bea4e3df1d4f6cc3c04a6bdab9631ba8786、panel header SHA b45780c375affd37c7026d5a9a918e8c5a71f6b22bd176e70195df9192823ce1。
- 次：明示routineの引数decoder。tests/work_dat_ui_literal_evidence_20261026.json（SHA e50107900d5d889a73bab0e19bb3d8714ad561a9e2c061df8a673329f4edfa62）に既存raw/RTTI根拠保存。任意式評価せずliteralだけ認識するchecked-read実装を担当中。実機hook/待機/返却の成功ではない。
- 明示命令decoder追加：src/work_dat_ui_literal.h。checked-read経由でexact routine(hk_ui_select_v1)だけ認識、任意式評価なし。strict x86 root PID28976 PASS出力。根拠/担当RED→GREENはtests/work_dat_ui_literal_receipt_20261026.json。header SHA AF2B1D59FBCDF8BA6D5CD9DCB335C5A48AB617068BC5E2CA0AB038486659AC87。認識は待機・結果返却の許可ではない。原作へのhook/配置は未実施。

### 2026-10-26 DAT変数の読取と命令接続のレビュー
- src/work_dat_ui_snapshot.h追加。固定3候補/1列/3数値参照、既存5結果セルをchecked-readで照合する。新規変数作成/評価/native呼出/書込みはしない。二重読取はatomic/ABA保証ではなく、UI-thread/generationの検証は接続側に残る。
- root run_work_dat_ui_snapshot.ps1 PID26920 PASS出力（142読取失敗位置・不正構造等）。詳細はtests/work_dat_ui_snapshot_evidence_20261026.json。header SHA3a1980bd21d6d6e58ca8b1d1023adfef65467ba309a08e70c265d4af591be237。
- 重要：最初のwork_dat_ui_dispatch.hの通常Cwrapperは合成ABI試験PASSでも配置不可。原作4A1250にはCxxThrowExceptionへの経路があり、例外でTLS depth解放が飛ぶ。独立レビューで発見。原作呼出後に処理を残さず、observer限定guard解除→stack復元→original tailjumpへ修正中。
- 原作駆動の再帰は別観測、observer中の再帰だけ抑制する。原作return address/ESP一致を追加検証。native例外の実機検証・待機/返却は未完。配置DLL/EXE/DAT/save変更なし。
- 追記：snapshot root PID26920 exit0確認。dispatcherはobserver限定guardとtailjumpへ修正済み、header SHA A7D5265F589A696CFEED0B43D9558D7716D60A60C7F9C7BD43CD50A83659DD1F。旧Cwrapperで新ESP検査RED→修正版default/O2 GREEN。root PID26720も1005呼出PASS。原作例外の実機試験は未実施、observerはno-throw/no-gamecallを必須とする。次はread-only観測pluginへ組込み、実機の要求/待機状態を照合してから結果返却を接続する。

### 2026-10-26 読取専用probe DLLをビルド（未配置）
- 新規core/dat_ui_probe_plugin.c/.def/build_dat_ui_probe.ps1。出力core/dat_ui_probe_fixture/HakushinDatUiProbe.dll、SHA df42a6fd3d660e4137187c5cfdf9a0ef6d37020357ee5665f51efe05e4dd0bc8。exact EXE SHA・mainHWND base+4797FC・UI thread・Core管理CALLを検証し、明示routineのみbounded log。VM書込み/新UI/教育効果なし。
- root build_dat_ui_probe.ps1 -Test PID30560 PASS出力。合成privateメモリのownership/ABI/unsupportedhost/retainedshutdown確認のみ、実ゲーム起動やインストールではない。session pinにより更新/無効化はゲーム再起動が必要。
- 独立レビュー未解決：UI-thread上のinstallだけでは、他threadが433B62を実行中でない保証にならない。5byte patchのquiescence根拠を既存call経路から限定確認中。これが解決するまで未配置。
- 試験入口tests/work_dat_ui_spike_entry_v1.dat（SHA8ef0b9ea5665f4fb572ad997aa529118b3f7a99faeeb1eb2dddbd57992df4f05）は既存sci_mt blockを別名で複製し専用worldへ。we_stはlevel/skill変更を含むため連鎖しない。spikeと入口の静的parse/CP932変換可能性はroot PID18920 exit0、原作起動未確認。
- process確認で原作PID28800と別研究P0_TAKEOVER/runtime/game_copy PID28864が稼働。今回どちらも操作なし。startup_cleanへの配置/起動なし、他担当のゲームを終了しない。現在状態は次回操作前に再照合。
- 配置条件の追加根拠：tests/work_dat_ui_quiescence_evidence_20261026.json（SHA2e8cdf57b29968e54e804361b2c8daa045166197bbe7d19c490331aa19f1de2e）。loader実行中にもmainwindow message pumpあり、window visibleだけでは早すぎる。自動install版の配置は禁止し、初期タイトルでidleを確認後の明示arm＋loadingflag base+47983C==0へ修正中。flagだけで全thread安全を証明したとはしない。独立レビューでdirect worker interpreter callerは見つからず、間接呼出を全排除した証拠ではない。

### 2026-10-26 DAT UI probe: copy deployed, manual arm pending
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL / 停止VA 0x433B62 -> 0x4A1250。未完了: 実機要求読取、待機・確定・取消の往復、汎用UI接続。
- 手動arm版DLL SHA22101469f3e8d3cb07b0f2481ad313cb43f29b52866c5cb04593c277f5f9c4c5をstartup_clean_20261025の作業用コピーだけへ配置。以前の自動install版は使用しない。既存2プラグインを無効化しprobeのみ有効。原本変更なし。
- 配置・元設定バックアップ: ../_work/dat_ui_probe_deployment_20261026.json。実行ログは同コピーのHakushinDatUiProbe.15052.log。2026-10-26再照合でPID15052 / HWND23202194が存続、ログはmanual_arm_wait。まだCALL置換未実施、実機DAT往復成功ではない。
- 初期タイトル表示を前段で目視済み。ユーザーが操作可能になったため、現在も初期タイトルか確認待ち。難易度/ロード前にhelperでPID・path・creation FILETIME・HWND・cookieを再照合してarmし、patch_activeを確認する。古いidentityを再起動後に使い回さない。
- 起動試行PID29616は画面/ログ未出力、原因未確定。PID19300はHidden指定で画面なし。どちらも所有する作業用コピーと照合して終了済み。作業場所をゲームフォルダ、表示をNormalとしたPID15052でタイトル表示。二重起動原因と断定しない。
- 次: DAT UI Spike v1の専用イベントで3候補/値30,55,10を読取確認。現段階は原作choiceへのfallbackでbackend=0。新UIからの返却は別の未実装段階。ユーザー導入のx32dbgは必要時に利用可能、今回はまだ使用しない。
### 2026-10-26 manual arm preflight rejected (no patch posted)
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL。ユーザーと画面取得で初期タイトルを確認。arm helper実行PID10208はExact main window identity mismatchで送信前停止。
- 読取診断PID9096: target15052、HWND23202194、base8519680、UIthread29112、owner15052、visible=true、root一致、owner window=0。GetWindowLongW(GWLP_HINSTANCE=-6)のみ0。API失敗か仮定の誤りか未確定。ガードを削除せずadapter_reviewへ限定調査を依頼。原作操作/追加起動/arm再送なし。
- 次: helperのidentity取得を修正・検証後、現在processと初期タイトルを再確認して接続。ユーザーにはタイトルのまま待機を案内済み。DAT往復は未検証。
### 2026-10-26 manual arm succeeded in working copy
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL。helperの64bit呼出からGetWindowLongW(-6)はerror1413、GetWindowLongPtrW(-6)は0x820000でbase一致。bitness分岐・error検出を修正しexact比較を維持。helper SHA d65f78c76c76df49bf888c6182597eed8589a5d1051fbbbc469c21d4de641101。native x86 DLLは変更不要。
- 新PowerShell PID11836で1回arm送信。HakushinDatUiProbe.15052.log: UIthread29112 manual_arm_accepted, loading=0; patch_active code=0 site=00853b62 original=008c1250。初期タイトル確認後の限定試験であり全thread安全の形式的証明ではない。
- 次: Easy -> DAT UI Spike v1 -> maptest勢力から3候補の原作fallback要求を観測。DLL接続成功のみで、DAT値読取/新UI/返却は未検証。再起動時には新identityで再接続が必要。
- 2026-10-26再起動追記 / WORK-DAT-GENERIC-UI-SPIKE-20261026 / PARTIAL: 旧PID15052消滅を確認。ユーザーが作業用コピーを再起動しPID28336/HWND13699526/creation134374936849360560。初期タイトルを再度目視し修正版helperでarm、同PIDログにpatch_active code0/UIthread25948/site00853b62を確認。DAT往復未確認。次はEasy→DAT UI Spike v1。

### 2026-10-26 native fallback KMR round trip observed
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL。ユーザーが3候補画面→KMR→結果文を閉じた後、exact PID28336/path/start/HWND/hash再照合して読み取り。selected=[kmr], index1,status1,before1,after1,backend0。原作fallback成功であり新表UI返却成功ではない。
- 証拠 ../../data/recruit_sort_v4/tests/work_dat_ui_context_live_20261026.json SHA99f16a450d104a9ec0e7359d7ce3528b6cf75423706f7673d8acda793e143aca。root読み戻し済み。時刻22:50:28–29 JST。非atomic読取。先行画面はユーザーが再度開いておりentry1と同一要求とは断定しない。
- snapshot rejected原因: dispatcher ECXはevaluator、VM ownerは[evaluator+4]かつevaluator==VM+0x504。正しいVMから候補akys/kmr/tnok・値30/55/10・Bonusを読取。結果statusレコードは実行後に移動、古いアドレス保持での書込は禁止。
- adapter_reviewがchecked resolverと回帰試験を追加、probe修正ビルド済み未配置。DLL SHA771e91321d76886207edd432f5fa9b41746bce4ec0422f8f1732eee5e7f83633。rootソース/試験確認後にゲーム終了して差替える。
- 継続設計: requestコピー→次のchoice世代で対応確認→表→source_indexをordinal変換→結果セル再解決→token消費→原作close。既存世代フックはCore予約+直接patch、汎用accessor未公開。旧selector無効のコピー限定で競合を拒否する。教育専用choicepage/usechara_sentakuは流用しない。
- ユーザー希望: 操作依頼はrequest_user_input_asyncの質問通知で送る。音はアプリ側設定依存。
- 2026-10-26 WORK-DAT-GENERIC-UI-SPIKE-20261026 / PARTIAL: root context/probe tests PID5624 exit0。root再ビルド成果物SHA 99623632298AB3B5CA583284793F1E468345F24DC1FAD3761E5453E8624B815F はagentビルド771e…と異なり最初の配置照合で停止、配置なし。rootソース再確認後root成果物として配置。Vahren不在確認済み、startup_cleanコピーのみDLL差替・読戻一致。配置receipt更新。次回新PID/title確認後armし修正probeの実機読取を検証する。

### 2026-10-26 corrected probe runtime capture verified
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL。PID26632/start134374975724913237/HWND3287682の作業コピー。修正版DLL 99623632…を手動arm、UIthread10516でpatch_active code0。
- HakushinDatUiProbe.26632.log entry1: evaluator00cde7f4 -> vm_context00cde2f0, snapshot=ok。ids akys/kmr/tnok, refs hk_ui_value0/1/2, values30/55/10,column Bonus,index-1,status0,backend0,before1,after0。要求入口でchoice_ready_observed=0はchoice生成前。後続のUI同定の代用にしない。
- ユーザーが4選択肢表示確認。Cancel試験の案内後「タイトルに戻りますか」の確認を押したと報告、現在画面も初期タイトルと確認。取消の結果status2/after1は未検証、成功扱いしない。同じPIDは存続し接続済み、再armは不要。再度専用シナリオで明示Cancelボタンを試す。
- 先行KMR往復の成功と今回の修正probe読取成功を区別。新表UIの返却はまだ未実装。
### 2026-10-26 explicit native Cancel verified
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL。PID26632の新しいシナリオでユーザーが明示Cancelを左クリック。23:35:59–23:36:00 JSTのidentity再照合後読取でindex3/status2/before1/after1/backend0。文字列map全3ノード内にhk_ui_selectedレコードなし（空vectorを読んだという意味ではない）。先のタイトル戻り操作とは別の試験。
- tests/work_dat_ui_context_live_20261026.json after_cancel_observationsへ保存、root読戻済み。SHA7e630e19fb8b8b29415a87430db6e58b27806467d15b3b731e9f2188707a8e16。KMR往復と取消は異なるprocess/要求の観測。非atomic、ゲーム書込・nativecallなし。
- 確認済み: 修正probeのDAT候補/独自値読取、原作fallback確定KMR、明示Cancelと各after1。未完: 汎用表への接続、generationによる再表示/古い要求拒否、native返却、plugin無効・不正入力の実機。教育対応完成ではない。
### 2026-10-27 generic session and choice binding components
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL。generic_session_guard: src/work_dat_ui_session.hと専用fixture/runner。次のchoice世代限定、serial、supersession、一度だけ消費、枯渇拒否。generic_choice_binding: src/work_dat_ui_choice.hと専用fixture/runner。native4ラベル/owner/result名/既存結果セル/close先をchecked-readで照合。未配置・native書込なし。
- 独立レビューadapter_reviewでP1発見: active proof mismatch後、古いproof復元で再有効化可能。serial-aware revokeとRETIREDを追加、native不一致で失効。RED→GREEN、再レビューで解消。baseline待機時のnative消失/read失敗はadapterが明示revokeする責務。
- root両runner再実行PID28184 exit0確認。session NO REVIVAL等、choice52読取失敗位置を検証。fixture通過はnative実機返却成功ではない。choice offsetラベルstrideはdecimal28（0x28ではない）。
- 次: generic_choice_binding担当が新規test_work_dat_ui_composed.c/runnerのみでsnapshot→binding→session→hiddenWin32表→模擬store/closeの結合試験。rootがnative adapter統合を管理。既存教育bridgeの拒否対象は変更しない。
### 2026-10-27 composed fixture confirmed; native adapter pending
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL。composed fixture PID32040 exit0確認。snapshot→binding→session→hidden表→KMR ordinal1→模擬store/close一度を検証。実機返却成功ではない。
- tests/test_work_dat_ui_composed.c SHA023e5e22d079d9b8de0546a36bb592b4c569fb804e697579ec203972b6d3eb6b、runner SHA21ff596a8e86a4b716fa92fd75e470bdf9331eb4cc70672965c9417eb589ad1b。
- 既存資料再照合: RVA1E7E3 E8 28 01 00 00→1E910は通常choice setupの世代を数えるがclose/loadの失効保証ではない。close41E6D0は非表示とVM+28完了通知。新adapterのnative返却はlifecycle根拠確認まで無効。旧selectorとのhook競合は拒否。
- adapter_reviewへ新規core/dat_ui_selector_plugin.c等の隔離実装を依頼したがmodel capacityで中断。成果ファイルの有無・内容は次回照合必須、ビルド/配置成功扱いしない。原作や現在ゲームの操作なし。ユーザーの追加操作は現時点不要。

### 2026-10-27 staged selector build and finite lifecycle evidence
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL。前turnは結合fixture確認と記録の進展。今回capacity中断成果を回収し、core/dat_ui_selector_plugin.c/.def/build_dat_ui_selector.ps1を確認、root -Test PID32232 exit0。owned requestコピー、phase拒否/失効を実装。init常時拒否の準備部品であり、動作するselectorではない。配置なし。
- 停止VA: choice setup0041E7E3 / close0041E6D0 / task reset004C1FC0。未完: native寿命失効の接続、表の自動表示、結果返却実機。
- 新根拠 ../../data/recruit_sort_v4/tests/work_dat_ui_lifetime_evidence_20261027.json SHA46ee6a7540135116844bed5114d3e4c4b2b297b8b35ebd6237f778a3a9354c72。保存済みV9とrawから7 scene reset CALL、通常load、title確認、close/hideを列挙。close wrapperだけではtask queue resetを捕捉できない。既存資料の活用で調査範囲を有限化、網羅性/実機成功は未主張。
- 次: Core管理の複数hookを部分成功時も保持して無効化する契約と、direct hide/teardown経路を限定確認し、別lifetime epochとUIthread返却を接続。DAT_GENERIC_UI_SPIKE_PLAN_20261026.mdへ現在の実態を追記。原本・稼働ゲーム操作なし、ユーザー操作依頼なし。

### 2026-10-27 Claude loader integration and unattended operation checkpoint
- WORK-CLAUDE-LOADER-PATCH-20261027 / Work / P1 / PARTIAL. Base 32 SHA matched; 12 diffs passed git apply --check then applied; 14 new core files copied. Source backup and evidence: ../_work/claude_loader_patches_20261026/WORK_BASE_AUDIT_20261027.json and work_preapply_20261027/.
- Windows verification: build_claude_loader_patch_test.ps1 PID32468 exit0: ptr82/82, ptrhost17/17, manifest16/16, hash41/41, loader_wait9/9. Cancellation regression RED then GREEN; hash early-close/leaked-handle mutants RED(exit1), actual implementation GREEN(exit0). Core nine suites exit0; separate managed-render10/10 exit0. See WORK_CORE_REGRESSION_20261027_015727.log, WORK_MANAGED_RENDER_20261027_015931.log and core/hash_review_fixture_20261027/.
- Core retained-failure policy preserved: block new Load until successful complete cleanup or process exit. Log wording corrected; no behavior change. Managed pointer runtime option remains disabled. Golden/MATCH remain0.
- Diagnostic PID16992: both plugins logged route_wait_init_thread -> route_init_thread_exited -> installer_begin; user confirmed recruit sorting and basic selector. Missing skill hover traced to deployed basic build lacking NATIVE_HOVER; not a successful hover test.
- Replaced diagnostic selector with existing hover-research variant SHA f23e81f25d8731edc98f595f9310633375fcaee9e0d315854a679425930dff85; manifest v2 updated. Current diagnostic PID20340, HWND9177686 title observed. Both startup wait and selector installer_active logged; hover acceptance remains pending.
- Direct automation launch previously left PID16420 without a window; exact owned process was ended, zero Vahren processes confirmed, then Explorer launch succeeded. Cause unknown; do not attribute startup failure to double launch as established fact.
- User authorizes autonomous game launch/operation/close/save while away. Always verify existing game and close before another launch. Deletions must go to Recycle Bin. No files deleted or saves written in this checkpoint.
- Generic DAT UI: native adapter and separate lifecycle components now implemented and synthetic Windows fixtures passed, superseding earlier always-refuse staging note. Not deployed or game-validated; current focus is loader/hover acceptance. Unfinished: native generic return, stale-session rejection on actual game, disabled-plugin/bad-input game tests.
- Runtime checkpoint PID20340: title visible, Responding=True, manifest bootstrap/core/rollback/preflight all0, recruit and selector active. Two Continue clicks and Return through computer-use did not change the visible title screen. No repeated launch attempted. Cause unconfirmed; next step is distinguish automation input delivery from game/plugin input handling before claiming load/hover success. No save action occurred.

### 2026-10-27 active-epoch correction and input comparison
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL / stop VA choice0041E7E3. Independent review found ACTIVE overlay survived new opening with identical native binding bytes; completion already rejected stale writes, but UI remained stale. Fixed active-only epoch eligibility in core/dat_ui_selector_runtime.h; test in core/test_dat_ui_selector_native.c.
- RED actual adapter/private-native-memory fixture test exit1; GREEN O0/O2 and existing guard each exit0. Root build_dat_ui_selector.ps1 -Test session96338 exit0 rebuilt DLL including correction. No game/DAT resumption tested, no deployment of generic DLL. Logs ../_work/claude_loader_patches_20261026/WORK_ACTIVE_EPOCH_RED_20261027.log and WORK_ACTIVE_EPOCH_GREEN_20261027.log.
- Runtime SHA D7E0C2FC0E20CD0D24EE789D1068661B36430F38D54F5F1E612CF023C6D2173D; native test SHA C406E7F73BEF5B59AA5643B7735FB7C58170C148EF55AF92F60BE4F57A59F28A. Prior generic DLL build receipt is superseded by this rebuild; do not deploy using old hash.
- Input comparison: PID20340 normal-close succeeded. Zero Vahren processes verified before next launch. Diagnostic selector disabled only in manifest, recruit kept enabled; new HWND9243222 title reached, latest bootstrap plan contained only recruit. Same computer-use Continue click still did not advance. Selector hover variant alone therefore not established cause; original/no-plugin comparison and input delivery remain unresolved.
- Comparison game closed using Alt+F4; zero Vahren processes verified; manifest restored selector enabled=1 with f23e81... hash. Game currently stopped. No save changed or file deleted. Native hover acceptance remains pending; no user action required while away.

### 2026-10-27 automated input comparison without extensions
- WORK-CLAUDE-LOADER-PATCH-20261027 / Work / P1 / PARTIAL; runtime hover acceptance pending. PID30912 with both feature plugins disabled (latest log: plugins disabled: empty plan) still did not leave title after computer-use Continue double-click.
- Next controlled comparison: closed game, verified zero processes, renamed diagnostic dinput8.dll to .input-comparison-disabled (recoverable, no deletion), launched diagnostic PID29056/HWND3147908. Module list contained Windows SYSTEM32 DINPUT8.dll and no Hakushin module. Same computer-use Continue click did not advance. Thus symptom reproduces without extension loading; not evidence requiring a selector/loader source fix. Human-input comparison requested asynchronously for when user returns. No original files/saves altered.
- Normal Alt+F4 closure verified zero processes. Restored diagnostic dinput8.dll and enabled=1 for recruit/selector. Deployment source/destination hashes all matched; WORK_DIAGNOSTIC_DEPLOY_20261027.json now correctly records hover-research selector SHA f23e81... (receipt SHA8C9E2E68F883BFFCAE81C2E8096B63949F25A4C2F876ADFE9792B2EDDC65E0D3). Current game stopped.
- Generic build receipt core/dat_ui_selector_build_receipt_20261027.json refreshed to reviewed ACTIVE-epoch fix and rebuilt DLL SHAab6ac8cfe9c02fe63c4cd97548ad3e5e60ee199900b01530070c18cce6930f28. Not deployed; all actual DAT/native resumption claims remain false. Next: human input comparison or supported reliable GUI input, then hover acceptance and isolated generic native trial. Do not redo prior source tests without a new change.

### 2026-10-27 native trial blocked audit
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / BLOCKED (runtime gate only). Stop VA choice0041E7E3/close0041E6D0. Latest implementation/receipt reconciled into DAT_GENERIC_UI_SPIKE_PLAN_20261026.md; earlier always-refuse status is stale. Fixed3-row adapter source and Windows fixtures done, actual DAT resumption remains unverified.
- Same automation-input blocker recurred across consecutive continuations: selector enabled, selector disabled, both plugins disabled, loader removed (SYSTEM32 DINPUT8 only) all leave Continue at title. User unavailable; asynchronous human comparison pending. No Vahren process currently present. No live worker/job being waited on; no duplicate launch and no useful further source mutation justified before native gate. Mark thread goal blocked rather than repeating checks; not complete and not user-requested pause.
- Resume from hand-input result, then test plan native checklist. Loader+both plugins restored in diagnostic config. Do not redo completed source tests or claim generic native success from fixtures.

### 2026-10-27 autonomous GUI resumed; isolated generic deployment
- WORK-CLAUDE-LOADER-PATCH-20261027 / Work / P1 / PARTIAL. Supersedes runtime-only BLOCKED checkpoint: human Continue succeeded; user reauthorized after physical-Esc stop. Root subsequently navigated title -> Continue -> Hell turn19 save -> education -> swimming -> instructor list through computer-use on PID11468. No second launch while running, no save writes.
- 66-row chip panel automatically appeared; SNNN row displayed matching native detail; right-click restored native instructor choice. Hover skill icon highlighted but tooltip not visibly confirmed. Do not mark hover PASS: prior diagnostics show computer-use overlay can fail cursor_uncovered; current build has hover diagnostics disabled. Agent read-only review confirms helper PID21220 -> child19996 normal, log includes PID11468 prewarm6.586s/panel accepted, no suspended-thread evidence. Live log readers must allow shared writes; metadata alone is not current-content proof.
- Root closed PID11468 normally, confirmed zero Vahren processes. Diagnostic-only config backed up to ../_work/claude_loader_patches_20261026/WORK_PRE_GENERIC_MANIFEST_20261027.conf (SHA9b063c95ed9d36b8d8c2b6e57216f1c0ca5ab6563f62dac4fe5b12d227ea5f10). Current manifest enables only hakushin.dat.ui.selector. Copied reviewed DLL SHAab6ac8cfe9c02fe63c4cd97548ad3e5e60ee199900b01530070c18cce6930f28 and read-back matched. Legacy recruit/selector/probe not enabled concurrently. Original EXE/DAT/saves unchanged.
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL; stop VA0041E7E3/0041E6D0. First generic deployment now staged, launch requested via diagnostic Explorer. Not armed or native-return verified yet. Next: observe initial title, exact PID/path/start/HWND/cookie, manual arm and patch_active, then fixed-three DAT UI Spike. Restore backed-up manifest after isolated trial when needed.

### 2026-10-27 generic native lifecycle and display checkpoint
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Stop VA 0041E7E3/0041E6D0; next native visible panel and DAT result verification. User renewed all game operations; no duplicate launches.
- PID28480 first native trial copied values but title input polling advanced lifecycle on every poll (lifetime53525). Fixed title gate to preserve native post-refresh predicate, invalidate only real title/exit request. Full native prefix/epilogue and reservation checked. O0/O2 lifecycle RED then GREEN, 1000 idle polls, independent review no blocking findings. Added bounded once-per-serial invalidation diagnostics.
- Full build_dat_ui_selector.ps1 -Test exit0. DLL SHA912f1141009e0c4e133c1f54f61eafb40e3d80bf9e959b5284db3e6114d96d4d copied/hash-matched to diagnostic-only plugins. Only generic selector enabled. Legacy manifest backup WORK_PRE_GENERIC_MANIFEST_20261027.conf remains available.
- Native PID23992 HWND15599450 manually armed once at observed initial title (start134375392050132559); patch_active code0. Easy -> DAT UI Spike -> operation faction reached. request_copied serial1 lifetime6 values30,55,10 and panel_active. Accessibility confirms Names/Bonus and AKYS30,KMR55,TNOK10 controls, but screenshot shows only native four choices. panel_active is NOT visible-render acceptance. Native result/DAT resumption not tested; Golden/MATCH remain0.
- Display difference: new panel is direct GDI child of main game; existing working preview uses owned popup surface. Likely drawing conflict, not established solely from log. Agent generic_choice_binding implementing minimal owned-surface change with regression tests in core/dat_ui_selector_runtime.h and core/test_dat_ui_selector_native.c only; no protected src edits.
- Root closed diagnostic PID23992 with normal Alt+F4; process enumeration confirms zero Vahren. Original EXE/DAT/saves unchanged, no deletion. Source/test success distinct from runtime result. Next build/review/deploy new display fix, then observable selection and actual DAT return.

### 2026-10-27 generic native selection SUCCESS; cancellation test pending
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Minimum fixed-three selection path now native verified, not full generic production API. Stop VA0041E7E3/0041E6D0. Owned popup fix and actual WM_ENABLE(TRUE/FALSE) successor-request regression passed RED/GREEN; independent rereview no blocker. Full build_dat_ui_selector.ps1 -Test session23520 exit0 (O0/O2).
- Current diagnostic DLL SHA3d2779cffde4ccd9d9c0ab7b1f8d04327a50d9393e86d1428c96158ad224c43c; only generic enabled. Source runtime bb2415ed95a1d9d7e02c297aef666db1e415c52b2d3fcbb4fd89655f7120466e, nativefixture c3f75331ca39a16bf52bdd2c4a909cbe4ba29fba062986530938cfe700c26db0.
- sky.launch_app produced PID33708 with no HWND/no plugin log; bounded checks unchanged. After exact-path/no-window identity confirmation, stopped that process and verified zero Vahren; Explorer launch succeeded. Prefer Explorer launch for this game; no duplicate processes.
- Native PID23792 HWND18679496 start134375447920166696, manual initial-title arm cookie4b70853d2d32587f -> patch_active0. Easy/DAT UI Spike/operation faction: visible generic popup AKYS30/KMR55/TNOK10. Bonus header click sorted ascending TNOK10/AKYS30/KMR55. Selected third visible row KMR; confirm closed popup and native choice. Screenshot of original DAT message: Result=kmr; Status=1; Before=1 After=1; Backend=1. Native_result log one entry. This proves fixed-three sorted identity return and one DAT resumption in this trial; no general lifecycle/fullscreen coverage or Golden/MATCH claim.
- Minor usability issue: confirmation returned foreground to Explorer; activating original game revealed result. Owner foreground restoration should be reviewed later.
- Advanced result to strategy turn1, sent Escape to return title for cancellation trial. Next capture reported physical Escape user stop. No further Computer Use calls made. Game may remain running PID23792; enumerate and inspect before any input/restart. Need explicit renewed automatic-input permission under tool stop rule. Cancel/native fallback, repeated requests, title/load stale validation remain pending.
- Copied native log to _work/claude_loader_patches_20261026/WORK_GENERIC_NATIVE_23792.log. Original EXE/DAT/saves unchanged by agent; no save operation/deletion. Diagnostic scenario may perform its own normal runtime behavior.

### 2026-10-27 resumed native cancellation verification
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL; stop VA0041E7E3/0041E6D0. User renewed autonomous PC permission after pause. No duplicate launch; diagnostic PID31876 HWND4392170 start134375491753844200 armed once at observed initial title, cookie f88ec6c091250894. Current DLL SHA3d2779cffde4ccd9d9c0ab7b1f8d04327a50d9393e86d1428c96158ad224c43c; generic plugin only.
- Easy -> DAT UI Spike -> operation faction displayed AKYS30/KMR55/TNOK10. Right-click within popup closed overlay; after reactivating game, original four choices remained waiting. Native Cancel left-click produced actual DAT screen Result=(empty), Status=2, Before=1 After=1, Backend=0. No plugin native_result entry in this run. This verifies fallback cancellation without plugin selection commit and single DAT resumption; not a direct plugin-returned cancellation API.
- Foreground-to-Explorer issue reproduced on popup cancellation, matching prior confirmation run. generic_choice_binding owns runtime/header + native fixture for bounded cleanup-order investigation/fix; root owns deployment/records/game. No protected src edits, original EXE/DAT/save modifications or file deletion.
- Native evidence copied to ../_work/claude_loader_patches_20261026/WORK_GENERIC_NATIVE_31876.log. Remaining: foreground cleanup repair acceptance, repeated requests/stale actual-game validation, disabled/malformed request behavior, full generic candidate API and education/item integration. Do not claim full completion or Golden/MATCH.

### 2026-10-27 generic selector native acceptance and foreground repair
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Stop VA0041E7E3/0041E6D0. Fixed-three minimum path accepted; full general API and education/item integration remain unfinished. This supersedes earlier native-only BLOCKED/pending entries.
- Cleanup repair: re-enable originally-enabled owner BEFORE destroying popup; detach globals first for reentry. No forced foreground call. Agent RED exit1 then GREEN O0/O2 actual WM_ENABLE/WM_DESTROY assertions; root build_dat_ui_selector.ps1 -Test session23538 exit0; independent exact-source review found no blocker.
- Current DLL SHA cdc4554cf9ab4f542c0360a52b92b4d975a415418eb5bbb3d286322ab0a67438. Runtime SHA4140d098c43d0dc7d4d44b4888340568a8a67c7e68523c1b6c3731e7238354d4; native fixture SHAf814179425e2561af6bb5010d41aed7896ac94f38996414ba5e49c8cb46b6e38.
- PID20596: right-click closed only custom panel, kept game foreground and native choice waiting. Native TNOK gave Result=tnok Status1 Before1 After1 Backend0. Same process title-return/reopen reused evaluator/VM addresses but created serial2/lifetime13 (prior serial1/lifetime6). Bonus ascending sort then first visible TNOK returned Result=tnok Status1 Before1 After1 Backend1; exactly one native_result entry; foreground retained.
- PID34556 plugin-disabled control: no Hakushin module, empty-plan log; native AKYS returned Result=akys Status1 Before1 After1 Backend0. No custom table, normal event continued.
- PID32404 malformed-input control: diagnostic DAT referenced missing numeric variable instead of value1. Plugin armed/patch_active but rejected request, native four choices remained. Native Cancel produced empty Result, Status2 Before1 After1 Backend0. Log reason is generic request_rejected, not a dedicated missing-variable diagnosis.
- Original diagnostic DAT restored byte-for-byte SHA c9a96d9c6f83d21ef674b87f893219d4f58945bf174b24ecbdf000027cf4aef2 after normal game closure. Zero Vahren processes verified. Generic-only diagnostic manifest enabled; manual initial-title arming still required. Original game EXE/DAT/save not edited; no file deletion or explicit save operation.
- Evidence: ../_work/claude_loader_patches_20261026/WORK_GENERIC_ACCEPTANCE_20261027.json; WORK_GENERIC_NATIVE_20596.log, WORK_GENERIC_NATIVE_32404.log, earlier WORK_GENERIC_NATIVE_31876.log. Updated ../../data/recruit_sort_v4/core/dat_ui_selector_build_receipt_20261027.json reconciles current hashes and native evidence.
- Recommendation: DAT owns candidates/calculations, DLL owns table and selection. Next bounded proof: opt-in 2/4 candidate cases with one custom numeric column; preserve fixed-three baseline/native fallback. Do not assume choice(v,@labels) expands dynamically without evidence. Full-screen, live stale-load coverage, production automatic install, education integration and native skill hover remain pending; Golden/MATCH unchanged0. No formal broad goal rewrite performed.

### 2026-10-27 bounded v2 feasibility in progress
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL / stop VA0041E7E3/0041E6D0. Previous turn was progress: native fixed3 return/fallback and foreground cleanup accepted.
- Candidate v2 supports exactly2/4, while v1 retains exact3. Agent bounded_count_adapter owns source changes; adapter_review completed read-only exact-hash review with no code blocker. Root owns DAT fixtures/deployment/native acceptance. No concurrent edits now.
- Reference: ../_work/claude_loader_patches_20261026/WORK_GENERIC_V2_IMPLEMENTATION_20261027.md and DAT_GENERIC_UI_SPIKE_PLAN_20261026.md final section. Candidate DLL3a17cd64... isolated in bounded_v2; existing deployed cdc4554c... unchanged at this checkpoint.
- Actual adapter RED/GREEN, O0/O2 and16 legacy-suite runs passed. Standalone dispatch executable launch was canceled by Windows without test result; no bypass/retry. Do not label all regression suites passed. Root verification PID29904 live.
- Unfinished: root build confirmation, candidate diagnostic deployment and actual2/4 DAT result observation. Formal broad redesign/production migration not performed; no original EXE/DAT/save changes, no Git/deletion.

### 2026-10-27 bounded v2 candidate built, native gate pending
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL / stop VA0041E7E3/0041E6D0. Progress this turn: isolated opt-in2/4 candidate implementation, tests/review, diagnostic fixture preparation. This is still feasibility work, not formal broad migration.
- v1 remains fixed3; v2 exact2/4 profiles akys/kmr[/tnok/rma], one signed numeric column; source ordinal3 is valid for4 and native Cancel=N. Separate bounded numeric lookups preserve alias rejection across values/output cells; owner cleanup and lifetime/consume-before-store guards retained.
- Independent agent review matched all9 reported source hashes with no code blocker. Actual adapter RED then GREEN O0/O2; 16 legacy suite runs passed. Root build_dat_ui_selector.ps1 -Test -OutputDirectory bounded_v2 PID29904 exit0, log bounded_v2/ROOT_GREEN.log. Standalone dispatch test was canceled by Windows before a test result; NOT PASS, no bypass.
- Candidate DLL SHA3a17cd64a07a8e1b2c19ed107776702aaf21762c353a211d1c32e09a3dd57ead copied/hash-matched to diagnostic plugins with manifest update. Default fixed3 artifact cdc4554c... remains unchanged. Prior diagnostic manifest: WORK_PRE_V2_MANIFEST_20261027.conf.
- Root source fixtures: tests/work_dat_ui_spike_v2.dat and work_dat_ui_spike_entry_v2.dat. One event sequentially requests2 then4, negative/tied values30,-5,-5,55. Native literal choice branches preserve fallback; no assumed list expansion.
- First startup reported entry_v2.dat line18 numeric newline syntax error before DLL arm. Working v1 has CRLF; new v2 had LF only. Normalized both source and diagnostic v2 files to CRLF and verified text equality after CP932 encoding. Source DAT SHAa86c9c2f97b3a145222055b83fd2a1414c44f68e90a6921ffd0419c7eaf9bbd3; source entry SHAbadd555c511ea59cec1628e7a4801b49acc02f7c45da0f96ba6834be6bd76355; deployed entry SHA0ba81323cf019f4d55ea0edf30a6b1a11fe43e76f424386bf115008f904fce5a. Corrected startup NOT yet accepted.
- GUI recovery: Explorer element activation reported geometry unavailable. A coordinate attempt opened readme_4 in Notepad (no editing); subsequent input calls repeatedly reported user input, then minimized window. No further UI input pending user availability question. No new Vahren process exists; do not infer an in-flight test or start duplicate game. No original files/saves modified, no deletion, no Git.
- Resume: user availability -> exact diagnostic Explorer launch once -> title/identity/log/manual arm -> DAT UI Spike v2 -> N2 sorted KMR(-5) return -> N4 sorted RMA(original ordinal3) return; inspect Result/Status/Before/After/Backend and native logs. Then cancellation and v1 regression as needed. Do not label native2/4 successful before observed.
- References: ../_work/claude_loader_patches_20261026/WORK_GENERIC_V2_IMPLEMENTATION_20261027.md; bounded_v2/{RED,GREEN,REGRESSION_FINAL,ROOT_GREEN}.log; core/dat_ui_selector_build_receipt_20261027.json bounded_v2_candidate. Full education integration, arbitrary IDs/instances/counts, full-screen, native skill-hover and production automatic arming remain unfinished.

### 2026-10-27 human-assisted bounded v2 verification resumed
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL / stop VA0041E7E3/0041E6D0. Human resumed PC permission and offered hands-on testing; use question popup for action requests.
- Queue/handoff reconciled before work. Read-only process check found zero Vahren processes. Diagnostic DLL SHA3a17cd64a07a8e1b2c19ed107776702aaf21762c353a211d1c32e09a3dd57ead, v2 DAT SHAa86c9c2f97b3a145222055b83fd2a1414c44f68e90a6921ffd0419c7eaf9bbd3, CP932 entry SHA0ba81323cf019f4d55ea0edf30a6b1a11fe43e76f424386bf115008f904fce5a match prior checkpoint.
- Requested one diagnostic EXE launch, stop at initial title before Easy/Continue. Waiting for human startup result; corrected CRLF startup and native2/4 acceptance remain unverified. No source/deployment changes this checkpoint.
- Next: exact current identity/log/manual arm, then N2 KMR and N4 RMA sorted result with single DAT resumption. References: WORK_GENERIC_V2_IMPLEMENTATION_20261027.md and core/dat_ui_selector_build_receipt_20261027.json. No duplicate launch, original-file change, deletion or Git operation.

### 2026-10-27 bounded v2 native returns accepted; crash remains unresolved
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL / stop VA0041E7E3/0041E6D0; crash investigation VA005DA9F8. Not full generic/education completion.
- Human-assisted native PID9080: serial2 v2/count2 values30,-5, sorted KMR -> Count2 Resultkmr Status1 Before1 After1 Backend1; serial3 count4 values30,-5,-5,55, descending RMA(original ordinal3) -> Count4 Resultrma Status1 Before1 After1 Backend1. Human read visible DAT results; native log has exactly two native_result entries. Serial4 count2 right-click -> native Cancel -> empty Result Status2 Before1 After1 Backend0. No result screenshot retained; evidence is human result confirmation plus log.
- Earlier PID15964 crashed on foreground switch: Windows APPCRASH c0000005 Vahren.exe offset001da9f8 at21:23:01; actual log v1/count3 despite initial human report2. WER/log preserved; listed temporary dump unavailable. Native return not attempted in that run. Saved Ghidra005DA930 contains fault VA but no stack/register evidence; root cause UNKNOWN.
- Disabled control PID24008: no Hakushin modules, empty plan; same switch survived. Enabled PID9080 v1 switch also survived, so intermittent issue not proven fixed or reliably reproducible. Its v1 result text disappeared; game remained, no native_result entry; v1 return NOT accepted. Later genuine v2 success above is separate.
- Read-only agent focus_loss_review: current owner disabled/owned popup has no explicit foreground-loss lifecycle path; native fixture uses WS_EX_NOACTIVATE/STATIC owner, so lacks real activation/render coverage. No speculative code edits. Existing REA doctor6.7.0 exit0 confirms Codex registration and Ghidra12.1.4 healthy, but REA MCP tools absent; no config repair attempted.
- Diagnostic manifest restored enabled=1 from WORK_PRE_FOCUS_CONTROL_20261027.conf SHAa0d66296578a6b4d98697de3b40cb8b3b1781673e00ee1687aecf946f6d8cb84. DLL remains3a17cd64...; original EXE/DAT/saves unchanged. Last check one Vahren process; no new launch until stopped. Latest human state: count2 cancellation result.
- Evidence: ../_work/claude_loader_patches_20261026/WORK_GENERIC_V2_ACCEPTANCE_20261027.json; WORK_GENERIC_NATIVE_9080.log SHA120ddece1024afecf150dcdf6fc4b02e8aa496743b4209c3b5be557ee1156d8d; WORK_GENERIC_NATIVE_15964.log; WORK_GENERIC_CRASH_15964.wer. This supersedes prior corrected-startup/native2/4 pending checkpoint.
- Next: intermittent crash investigation with captured stack/activation evidence, then approved broader arbitrary-candidate integration. Keep direct cancellation API, full-screen, hover, education/item migration and production auto-arming explicitly unfinished. No Git/deletion; no Golden/MATCH change.

### 2026-10-27 debugger attachment and fault-subsystem checkpoint
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL / stop VA0041E7E3/0041E6D0; unresolved crash VA005DA9F8. Native2/4 acceptance remains as recorded above; no additional runtime PASS this checkpoint.
- Existing Ghidra evidence: rea_lab/headless_analysis/full_pseudoc_20261020/functions/005D/005DA930.c (291-byte function containing fault VA) performs codebook-style bit lookup/binary search; 005DA8D0.c reverses32 bits. STRING_INDEX.jsonl has libVorbis strings at0065B5F0 and0065B624. This supports an audio/Vorbis decoding classification, NOT a proven root cause or proof that the selector is innocent. Exact fault instruction, invalid address and crash stack remain missing.
- Agent fault_path_classify also identified bit-reader005E6CF0/005E6DB0 and callers005DAA60/005DAD60; inferred library names must not be treated as original symbols. No new binary parsing or source edits in this checkpoint.
- Human launched x32dbg at [USER_HOME]/Documents/x64dbg/release/x32/x32dbg.exe and attached existing diagnostic Vahren PID9080 with attach2378. Human reported setting SetExceptionBPX c0000005, first. No duplicate game launch or additional arming.
- Human screenshots confirm PID9080/thread20916 stops at selector TLS callback1 VA65438640 then callback2 VA654386C0 (DLL base65430000); both shown as INT3 breakpoints, NOT c0000005 evidence.
- After another single F9, human reported a further stop; reason UNKNOWN. Do not repeatedly resume until that reason is read. User currently performs debugger input.
- Computer Use read attempt was rejected as physical-Esc stop. No further Computer Use calls made. Await human stop-reason text/screenshot or explicit resumption before UI automation. File/document work remains available.
- Next: distinguish debugger startup/TLS stop from access violation; if actualc0000005, preserve exception address/access type, registers, stack and target dump locally before continuing. Do not infer a new crash from a debugger breakpoint.
- Original EXE/DAT/saves and deployed DLL/manifest unchanged; no deletion/Git. Prior turn yielded attachment/stop evidence; this checkpoint reconciles it into durable records. Full genericAPI, production automatic arming, education/item integration, fullscreen and hover remain unfinished.

### 2026-10-28 debugger wait revalidated
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Read-only process inspection confirms Vahren PID9080 (started2026-10-27 21:52:45) and x32dbg PID26416 (23:02:31) still exist; this does not establish the current stop reason. No UI actions or new launches.
- Existing research entry points and active V3 manifest were inspected. The reviewed saved pseudocode does not map the precise instruction at005DA9F8; do not derive a register/invalid-pointer diagnosis from it. Avoid repeating broad decompilation while waiting for the current debugger stop reason.
- Human stop-reason request remains pending. Next input is the x32dbg status text/screenshot; do not resume execution blindly. All production changes remain deferred; no additional runtime PASS, source changes or deletion.

### 2026-10-28 explicit runtime evidence blocker
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / BLOCKED (native crash investigation only; implementation remains PARTIAL). Stop VA005DA9F8. Same unresolved condition spans the stop-report turn and three automatic continuations: next debugger stop reason unknown; Computer Use physically stopped; user is handling debugger input.
- Independent saved-source review and evidence preservation are complete for this checkpoint. Further blind F9, process restart, speculative fix or broad migration would not resolve the evidence gap. No such action taken.
- Resume on human x32dbg status text/screenshot, or explicit permission to resume Computer Use inspection. Preserve the current diagnostic process if still present; do not double-launch. Native2/4 selection and fallback cancellation evidence remain accepted; crash not fixed.
- App goal is being marked blocked to stop repetitive automatic continuation, not complete or user-paused. Durable scope remains current selector/plugin-loader work; no return to full-engine implementation performed.

### 2026-10-28 implementation resumed; bounded generic5 preparation
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Supersedes prior debugger-stop BLOCKED entry. User reports PID9080 attached to x32dbg; execution resumed, logging breakpoints removed, C0000005 capture retained. No debugger/game action by Work this checkpoint.
- FINDINGS §84.5: 581 MAIN_STOP, 598 main decode, 299 worker starts, observed overlap0 and exception0. Later panel foreground-switch test also did not reproduce (human report). Crash VA005DA9F8 remains unresolved/reproduction pending; no speculative BGM CALL patch. Breakpoint timing and same-decoder identity limit inference.
- FINDINGS §85 and claude_gen_choice_wrapper.py read. STATIC: one native choice label per token, stack capacity50 without guard; bounded native fallback requires N+1 labels. Runtime label expansion/yield still unverified. Do not advertise capacity49 as tested.
- Next bounded spike: opt-in hk_ui_select_g, N1..5, DAT candidates/display labels/numeric values, strict native count and Cancel validation; preserve v1/v2. Root owns DAT/runtime/docs, generic5_adapter owns adapter headers/tests, generic_wrapper_review read-only reviews generator. No overlapping file edits.
- Stop VA0041E7E3/0041E6D0; pending generic5 synthetic/native acceptance, UI label expansion, cancellation, production automatic arming, education/item integration/fullscreen/hover. References: PEER_SCRIPT01_FINDINGS §84.5/§85, _work/claude_gen_choice_wrapper.py, DAT_GENERIC_UI_SPIKE_PLAN_20261026.md. Original EXE/DAT/saves and current deployed DLL untouched. No Git/deletion.

### 2026-10-28 Claude v3 runtime integration checkpoint
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. §89 / README_APPLY §7 replaces §6 runtime steps1-3 and the preceding generic5 plan. No duplicate implementation: generic5 header edits restored; preliminary evidence retained, not deployed.
- Claude runtime/reader/grid/test sources copied with exact base checks and CRLF-preserving patches. Receipt: _work/claude_loader_patches_20261026/v3integration/applied_sources.json. Runtime integration header SHA a3ddea32e4c3cc35de9697cb7be2f99c721d629db432a2a76347fba946511627. Literal SHA ce0175edb30b9084f901d30040eba62239730871b02dfd3488168070f3b854e3.
- Package synthetic build_dat_ui_v3_test.ps1 on Windows: PID1892 exit0, O0 85/85 and O2 85/85. This tests delivered package headers; installed-header and runtime/regression suites still pending. Native ACTUAL remains0; Golden/MATCH0.
- Independent review found partial list insertion could corrupt displayed-row mapping, and failed predecessor v3_show could revoke a successor request. Assigned separate files/tests to agents for narrow RED/GREEN fixes; do not deploy until verified.
- Optional AUTO arm patch applied with exact expected SHA432f033a...; existing build default remains off. Native diagnostic logs now use CREATE_NEW unique names, preserving previous logs. Narrow tests recorded in auto_arm/WORK_AUTO_ARM_INTEGRATION_20261028.md; full default/AUTO suites pending.
- §87 lifetime audit is STATIC only; no new gate or BGM patch. Stop VA0041E7E3/0041E6D0, crash VA005DA9F8 still reproduction pending. Current game/debugger and deployed DLL/manifest unchanged.
- Next: freeze reviewed sources, run Windows v3 runtime default/AUTO and legacy suites, then diagnostic-copy label expansion/return/cancel/fullscreen/IME. V3 grid currently names/numeric columns only; chip/detail/hover reuse and education/item migration remain unfinished.

### 2026-10-29 Work v4 integration resumed
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Current scope: DAT-driven generic unit selector and common plugin loader. README_APPLY sections8/9, v4/DAT_UI_V4_SPEC and FINDINGS sections90-92 supersede the preceding generic5/v3-only checkpoint.
- Claude/human ACTUAL evidence reports v4 chips, native details, 17/234 candidate selection and one education flow; latest V5 fixes remain synthetic-only until Work verification. Do not count the 12 education types as completed. Golden/MATCH remain0.
- Windows Work regression: lifetime O0/O2 PASS; v3 runtime default 55/55 twice; AUTO 55/55 twice; successor 12/12 twice. All four build processes exit0. Evidence: _work/claude_loader_patches_20261026/v4/WORK_RUNTIME_REGRESSION.json and WORK_*.stdout.log. These are synthetic tests, not game execution.
- After interruption, agent states were checked: two interrupted and one pending. Build owner and readonly review owner explicitly resumed. Root owns records and diagnostic-copy preparation; auto_arm_integration owns build/fixture files; generic5_adapter owns readonly v4/location/custom-column review; generic_wrapper_review owns readonly DirectInput design. No concurrent grid edits authorized.
- Build pending: v4 O0/O2/AUTO, edge, updated87-check v3 component fixture, full default/AUTO selector suites and formal Zig0.14.1 DLL SHA. Preserve diagnostic test logs using unique CREATE_NEW paths; expected values unchanged.
- Remaining: education12 teacher/student/cancel/execution on full diagnostic copy; location display-name resolver; explicit DAT numeric columns; DirectInput overlap/fullscreen/IME; old diagnostic additions cleanup. Native right-click result remains unverified. Crash VA005DA9F8 remains reproduction pending; no speculative BGM patch.
- Location review: existing adapter returns spot tag, old human-readable names came from DAT dictionary/SPN1. Direct inclusion is insufficient. Manifest documentation correction needed: enabled is field3, immediately after DLL name, not field4.
- Original EXE/DAT/MAP/saves/ZIP remain readonly. No Git mutation or game deployment this checkpoint. Stop VAs0041E7E3/0041E6D0 are evidence references, not permission to expand analysis.
### 2026-10-29 v4 build and StatusWnd evidence update
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. Windows Zig0.14.1 final default and AUTO build exit0; O0/O2 v4 68/68, edge10/10, v3 parts87/87 plus guard/native PASS. Build evidence: _work/claude_loader_patches_20261026/v4/WORK_BUILD_INTEGRATION_20261029.md. AUTO initially RED due PowerShell single-string splat, fixed with explicit string[] and rerun GREEN; logs preserved. Full Core/loader/legacy suite coverage is still pending, not claimed complete.
- Formal default DLL SHA4aa79e15dc8e7456f20f3de907668f7a75b42c6db0c3b533031c902ee950f5b5; AUTO SHA196d0544d3e1d4ba97d4545d7700b74e80914621ca33077fdd7b5e038df00645. Both retained in v4 WORK_BUILD_*_artifacts, not deployed by Work. No education12 ACTUAL yet.
- Existing full diagnostic copy inventory: original a_default non-save files have no missing/size-different counterpart. This is inventory/size evidence, not full byte identity. lecture.dat original and copy both SHA7F458E27871BA6608E38D433E22B624CF05014370B2A5FDCC1A15ADCAA866E8F. Existing copy reused, no new game folder.
- WORK-DAT-STATUS-HOVER-20261029 / Work / P1 / OPEN. User authorizes hk_ui_detail 0=none,1=buttonless default,2=explicit game actions. Design/review first; no implemented support claimed. Normal StatusWnd0x67E978 differs from TempStatusWnd0x8BCD48; opening55B5B0 has other-window/scene side effects. vtable/global faction/war flag modification prohibited.
- Human ACTUAL 2026-10-29:55BC60 argument0 for own/other;55D8F6 route:583CF0 result differs by unit (location hypothesis),597B00 result constant per faction,+1D own1/other two factions/allied0 (player-faction hypothesis). war window8BA538 +84=8BA5BC shown during sortie unit selection; +A4=8BA5DC is80000008 even normally. Setting this flag globally prohibited.55D8F6 rebuilt about10 times per open. Flags1C4 hire/1C5 extract/1C6 dismiss/1C7 item.55D712 group not observed. These are supplied observations; no broad semantic claim beyond sampled states.
- STATIC review:560650 sets pressed index+1BC using flags;560CA0 mouseup index1 can dismiss without rechecking1C6, index0 may extract without1C5 recheck. Merely clearing four flags after drawing is unsafe. Must inspect construction/drawing/hit-test/mouseup/clear and ownership together before implementation. No button suppression patch applied.
- User attached x32dbg to diagnostic game. Current OS evidence VahrenPID30228 and x32dbgPID30984; human last stop INT3 at vahren00B8D9FC, not C0000005 report. No F9 or added breakpoint issued by Work. Preserve active debugging; no duplicate game launch or file deployment.
- DAT_UI_V4_SPEC section6 enabled-field typo corrected to field3 and readback checked. Location/custom-column design saved in v4/WORK_V4_REVIEW_LOCATION_CUSTOM_COLUMNS_20261029.md. Pending numeric-column design, location names, mouse isolation/fullscreen, native hover/clear, explicit mode2 action tests and copy cleanup. Golden/MATCH unchanged0.

### 2026-10-29 v4 generic UI integration and native verification checkpoint
- WORK-DAT-GENERIC-UI-SPIKE-20261026 / Work / P1 / PARTIAL. This supersedes the earlier not-deployed / PID30228 debugger checkpoint. Scope remains generic DAT UI and plugin loader.
- Windows Core/loader regression 16/16 plus separate render-pointer PASS. Nine DAT suites (choice,composed,context,dispatch,literal,panel,request,session,snapshot) exit0. Evidence: ../_work/claude_loader_patches_20261026/v4/WORK_CORE_REGRESSION_20261029.md and WORK_DAT_REGRESSION_20261029_035358.json. Not all unrelated legacy suites have run.
- Formal AUTO DLL 196d0544d3e1d4ba97d4545d7700b74e80914621ca33077fdd7b5e038df00645 deployed only to startup_clean_20261025 diagnostic copy. Deployment receipt WORK_DIAGNOSTIC_DEPLOY_20261029_051417.json. Original game unchanged.
- Diagnostic conf current E576170E26F7B9BE3A1D2FE787E310FD3C0A30DF271050452E12E273CEE676AC, lecture current 62D9FEF1C12AC0BB69E9187F68F0C9F7BC3BB0B90FE08434E4C4520D09D4EE4D. Recoverable baselines in existing v4/WORK_DIAGNOSTIC_ORIGINAL_hakushin_plugins.conf and WORK_DIAGNOSTIC_ORIGINAL_lecture.dat. Restore after tests, with game closed. Baselines A0D66296... and 7F458E27... remain preserved.
- Launch with unspecified working directory produced windowless PID33772; exact-path process was recorded then stopped before launching again with diagnostic game working directory. PID28812 reached title. This comparison does not establish a unique startup root cause.
- ACTUAL PID28812: auto_arm_wait -> auto_arm_accepted (30 stable observations,594ms) -> patch_active. Test scenario case A copied217 candidates/4 columns, displayed chips/stats/native detail automatically. Search for test unit worked. Popup Cancel removed overlay and native detail, leaving original anchor choice waiting. No education executed or save written by Work. Current live process is diagnostic PID28812; check before any launch.
- Custom DAT numeric columns heading=@reference_list implemented; candidate-order numeric variable names/values captured, aliases/missing/count errors rejected, fresh revalidation before commit. Reader O0/O2 123/123 PASS; no game rules duplicated. Source work_dat_ui_v4.h SHA15090BAC63A3D88193C5697343760D174A36A9958E469229216AA20F6EB85A57.
- Location grid independent tests O0/O2 40/40; prior failure73/73 and v3/mapping87/87 PASS. Preserves eight numeric columns. Native resolver proves spot tag only; title explicitly states location ID/display name unverified. No inference that unknown means roamer.
- Core/location HK_OK header collision reproduced then fixed by extracting bounded native tag reader; real production TU and DLL compile/link pass. Existing metadata/stats/location tests pass O0/O2.
- Root runtime now connects location text with request/lifetime guards. Integration fixture adds custom sorted original-row return, mutated-value rejection, location unknown presentation. RED before connection failed only two location assertions. GREEN/full formal rebuild pending at this checkpoint; do not deploy changed sources yet.
- WORK-DAT-STATUS-HOVER-20261029 / Work / P1 / PARTIAL / VA00561120,00521650,00560CA0. Isolated hover helper synthetic196/196 passed but not integrated/deployed. Cleanup authority must survive focus/geometry loss, and clear must precede native detail hide and UI ownership release. Full StatusWnd button suppression and explicit mode2 actions remain unimplemented; flags-only suppression unsafe.
- Remaining: formal combined DLL verification, custom/location ACTUAL, full12 education flows, buttonless pinned native tooltip support, explicit button-mode semantics, DirectInput overlap/fullscreen/IME and diagnostic cleanup. Crash005DA9F8 remains reproduction pending; no speculative BGM patch. Golden/MATCH unchanged0. No Git mutations/deletion/original DAT or save modification.


### 2026-10-29 USER PAUSE - resume here
- User explicitly requested temporary pause. Root stopped PC/game input and interrupted active agents. App goal status paused. No automatic continuation until user resumes.
- Current objective is DAT generic display/selection functions and plugin loader; the app goal's older full-engine objective text is stale and is NOT the current implementation scope.
- Combined DLL full default/AUTO builds completed before pause, exit0, no stderr, source hashes stable. O0/O2: v4 runtime76/76, edge10/10, v3 components87/87, custom reader123/123, location grid40/40; guard/native/reentry PASS. Evidence: ../_work/claude_loader_patches_20261026/v4/WORK_CUSTOM_INTEGRATION_20261029_120721_859/evidence.json (SHA06EA552B73CFE929CF525AAAB508B4D7FC409C29B01F2ECD3BE573682216E3F2).
- New DLLs NOT deployed: default698892D6BA305032C2A548E3DA65EF90DC8784258D2BA00AE52625B9CDF259B2; AUTO4C451F10BE13364503373D524A28C3F68DD945DCAEBAAE3A1D20D9E546A1FB05.
- Prior live PID28812 disappeared after native Cancel; no Vahren Application1000/1001 event found in queried25-minute interval. No cause proven. DAT review finds no exit instruction; expected result is status2/backend0 then report. See WORK_V4_CANCEL_PATH_REVIEW_20261029.md.
- Diagnostic manifest currently selector DISABLED for native-Cancel control. Patched lecture/test DAT still present. Original game untouched. Baseline conf/lecture backups remain as recorded above; do not confuse disabled control with a broken auto-arm.
- Control game PID18664 reached title, currently left open at title after Easy clicks/Return did not advance. Root performed NO additional input after pause. Launch-monitor shell22232 may remain passively waiting for game exit (writes exit receipt only); it does not send input. Receipt WORK_NATIVE_CANCEL_CONTROL_20261029_120633.json. Verify current PID/window before any future launch; no double-launch.
- Additional old selector/hover regression agent was interrupted. Its process14264 no longer running when checked. Results not yet collected: do not claim these suites PASS.
- Resume: collect unfinished regression evidence; finish native-Cancel disabled control and capture exit/exception if repeated; then deploy new combined DLL only after game closes and hashes checked. Custom test proposal claude_dat_ui_v4_test_custom_proposal.dat remains unplaced. Tooltip/buttonless StatusWnd and input isolation still unfinished.
