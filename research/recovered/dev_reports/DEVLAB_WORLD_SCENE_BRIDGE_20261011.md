# DEVLAB-007/008 — 実セーブのscene読取APIとnative loader分岐精査（2026-10-11）

## 対象と根拠
- 研究正本 `MASTER_LEDGER.md` checkpoint83／正式190 ID／DONE9/34 と `ANALYSIS_LANES_PROTOCOL.md` を先読。5レーン owner正本には書き込まず、独立dev_labの追加ソースのみを変更。
- 読取根拠: 保存済み `recovered_source/peer_script01_ghidra_named_decomp_20261011.zip` 中の `decomp_0045xxxx.c`（0x45E1E0）、`decomp_0047xxxx.c`（0x4705F0/0x470700）、`decomp_0043xxxx.c`（0x435550）。旧EXEの実行・Ghidra/REAの新規逆解析ではない。
- `0x45E1E0` のGhidra自動名 `Save_GlobalEnvelope` は通常.sav readerの名前として不正確。ソース本文から呼出順を確認し、擬似Cの型/ABI/実ポインタ意味を断定しない。

## 確定した静的訂正: numeric保存レコード
- normal reader 0x45E1E0 のnumeric loopは 0x4705F0 を呼んで名前/文字列を消費し、途中再度0x4705F0を呼んでから 0x470700 でDWORD値を取得する。
- 0x4705F0 の保存Ghidra本体は0x470980等から文字を読んで string を構築するのに対し、0x470700 は 0x42E700 等を経由して `*param_1 = DAT_00b060f0` と値を書き込む。
- 既存 `native_saved_loader_bootstrap.py` の READ_NUMERIC_GROUP に記した代表VA 0x4705F0 は名前readerであるため **0x470700** に修正。0x4705F0の存在は直前コメントに残した。代表11段階は原作の逐次全call列ではなく研究用の概要である。
- `normal_save_runtime_registry.py` では既に READ_NUMERIC_GROUP が0x470700で整合していた。この訂正は原セーブの復号・保存bytesの変更を伴わない。

## 0x435550 の通常save mode1 と別mode0の非同一性
- 0x45E1E0 が呼ぶ世界graph readerは `FUN_00435550(...,1)`。mode0（param_2==0）には0x36c SpotElm・0x240 SpotPath/EscapePathのheap allocation、既存map更新・挿入の処理が見える。
- mode1側の保存Ghidra疑似Cには静的初期化bit 1/2/4/8・atexit登録と、3 bucketの文字列キー読込ループがある。区分別calleeは `Spot__vf23(...,1)`、`SpotPath__vf23_shared2(...,1)`、同callee(...,1)の順。可視body内にmode0と同じheap-new/map insertを確認できない。
- **限界**: mode1の静的初期化、vf23内部効果、name→native pointer、C++ owner/lifetime、既存graphへの格納先は未確定。mode0の生成と互換だと仮定しない。実機pointer/read-after-loadまたは保存済native callee追跡が必要。

## 新エンジン用データAPI
- `src/hakushin_compat/saved_scene_state_api.py` を追加。既存 `CandidateBootstrappedWorld` の同一captureレジストリと保存ID graphを検証後、immutableなSpot/Unit/Power/Routeカードを作る。
- 138 Spot、29 Power、保存Unit 7355/8763、経路160+11の元順序、SpotElm bucket 121、Spotに載らないUnit 8/7の情報を落とさず扱う。
- WorldGraph routeのendpoint_1e8とendpoint_204、regular/escape、raw flagは保存順で残し、無向のendpoint接点だけを **候補** として利用できる。経路の向き・通行可否・移動時間・座標は不明。
- Spot→Unit tree登録とUnit+0x84の別Spot名、Power+0x68/0x24とUnit vector0を勝手に「駐屯・領有・指揮官・戦闘参加者」と断定しない。
- 生成物は原sav bytesを保持せず、元実ファイル書込なし、renderer・戦闘CPU・イベントVM・native constructor無し。元mode1以外、capture混入、不明経路端点に加え、native実行済stage・renderer/event scheduler接続済みフラグが紛れた場合もfail closed。

## テストとブロッカー
- 新 `tests/test_saved_scene_state_api.py` **11/11 PASS**。元private実saveのSHA256 gate、world counts、参照順序、未登録Unit、immutable構造、mode/capture混入拒否、VA訂正、JSON安全出力を検査。
- 既存4モジュール `test_native_saved_loader_bootstrap`、`test_native_saved_reference_graph`、`test_native_saved_scene_transition`、`test_native_saved_scene_inspector` はまとめて **37/37 PASS、SUITE_EXIT=0（77.409秒）**。今回の新規11件と合計48件の限定回帰成功。大型 `run_checks.ps1` は他AI peer surveyの長時間問題があるため未実行。限定試験をフル回帰PASSと混同しない。
- 旧原作 Gameplay Golden 0、新 strict MATCH 0。セーブBYTE一致・保存ID crosswalk・静的reader解釈は旧ゲームのUI/CPU/移動を実測再現したものではない。
- 同時に他AIが `battle_window.py`、battle_definitions系と `DEVLAB_NATIVE_LOADER_STAGE_20261011.md` を変更中のため、それらは触らない。研究A/E owner・MASTER、原本、REA、Git stage/commit/push、Remote、自動化変更なし。

## 次
1. A/T014担当が 0x58E870/0x598980/0x5964C0 および0x435550 mode1 callee内部のpointer関係を明らかにしたら、保存ID viewとのズレを限定確認。
2. 戦闘viewerへの接続は別AI作業中の原DAT Unit/Class/Skill catalog完了後、保存Spotの「候補Unit ID」が戦闘参加者であると別証拠が取れた範囲に限って設計。
3. 原作の合法UIロード後Golden（画面・入力・保存・再開）の採取と strict trace比較は未着手。天候/土砂崩れはbaselineフラグ分離方針を維持。

## 補足: 保存済みGhidraの各オブジェクトreader内部（今回の追加照合）
- `decomp_0058xxxx.c` の0x58E870ではUnit既存領域への文字列・DWORD読込に加え、4系列の既存ベクタ領域のclear/repopulate候補と、+0x130木構造のclear→保存名付きレコードinsertが見える。Ghidraが引数/ECXを欠落させているためnative Unit取得元・各element型・デストラクタ順はVERIFY。
- `decomp_0059xxxx.c` の0x598980 Spot readerでは既存+0x20木領域のclear後、文字列キーを逐次読み、条件付きで+0x88/+0x8C/+0x90/+0x48等へ保存値を反映する経路が見える。どの可視UIパラメータかは既存writer証拠と区別し、ロード後有効な効果はVERIFY。
- 同ファイルの0x5964C0 Power readerでは+0x68、+0xA4、+0xB4の既存木/list領域のclearと再構成候補、+0x24文字列reader、+0xDCの0x80000008デフォルト設定経路が見える。保存済みPowerのfieldsと整合するが実native pointer再接続は未証明。
- これらのreaderは単なる「セーブIDを辞書へ格納」より多いnative内存更新を含み得る。したがって今回のimmutable `saved_scene_state_api` は **scene表示に供給する安全な保存ID索引**であり、旧EXEロード後のworld objectそのものを再現したものではない。
- 参照は全て既存10,257関数ZIPの静的C疑似コード。real caller/register/vf23副作用・gameplay実行0。研究A/T014・E/T018の正本へ勝手なREADY/DONE認定はしない。
## 2026-10-11 続行: 保存Unit→原作DAT構文定義の名前照合と戦闘用デバッグ配置

### 背景と独立作業
- 継続時に研究MASTER checkpoint83・190正式ID・DONE9/34、5レーン所有権、Git main b49c678とdirty listを確認。別AIはbattle_window、battle_definition_panel、battle_definitions、native_script_file_providerとdocsを変更中であったため**編集しない**。このDEV独立モジュール以外へのGit操作・commit/pushは0。
- 別AIの新F3閲覧は、元590DATからunit4,586/class4,080/skill16,554/skillset106の構文定義を索引化する。今回はその既存BattleDefinitionCatalogを**read-only利用**して、保存されたUnit文字列が原DATに同名で存在するか照合。casefoldで比較しているため、native case/異種混在優先・重複名のruntime処理は未証明。
- 新src `saved_unit_definition_bridge.py`: Unitの保存keyと内部string+0x00一致を要求。+0x1C/+0x54をunit/classの原DAT宣言名候補へ照合し、宣言元ファイル/行/SHAを併記。Spot所属・+0x84別Spotを捨てず、immutableマッピングを生成。重複・異kind衝突はfail closed。原作原文やセーブを改変せず、runtime HP/MP・技能・native class取得済を主張しない。

### 実セーブ3件からの直接名前照合
- save1: 保存Unit7355、+0x1Cが唯一のunit宣言626・class宣言6725・未該当4 → **7351/7355**で定義名一致。+0x54はclass一意7254・空97・未該当4。
- save2/auto: 保存Unit8763、+0x1Cは唯一のunit宣言631・class宣言8128・未該当4 → **8759/8763**一致。+0x54はclass一意8659・空100・未該当4。autoとsave2は元暗号文SHAが異なるがデコード内容同一の既報を維持。
- 未該当は3保存共通で `bakushin+0`、`dammy_ru+0`、`dammy_sakerobo+0`、`knnnnk+0` の4 ID（格納名はsuffixなし）。生成されたruntime alias等の原因は**UNKNOWN**、勝手なDAT名へ修正しない。
- 具体例: saved `tnok` = +0x1C `unit:tnok`、+0x54 `class:c_tnok`；saved `0gnhkn+0` = 両欄 `class:0gnhkn`。+0x38は別の未型付け文字列（例r0_hm）として保持し、全ての継承・画像優先・native producerが確定したとは言わない。
- 直接結果レポート（ゲームID・出典のみ、sav生bytesなし）: `reports/SAVED_UNIT_SOURCE_CROSSWALK_20261011.json`。元sav3件の既知SHA256 gateを通過。

### BF-03/BF-06試験入口（本番戦闘は未実装）
- 新src `candidate_battle_placement_fixture.py`: 明示したsaved unit IDと**手動指定座標**を入力し、+0x1Cの一意な原DAT宣言を選択、既存catalog.preview(allow_partial=True)で既知の項目だけを閲覧。原MAP bytesを読取専用でデコードして座標範囲・元map SHAを検証。元chip/chip2 PNGがちょうど一つなら参照、0件/複数件なら未確定。存在しないUnit・曖昧定義・重複座標・source manifest不一致はfail closed。実HP/MP・戦闘CPU・原作spawn結果は作成しない。
- 新src `candidate_battle_debug_overlay.py`: 現有の独立static rendererへ原作PNGを合成する**PC上の試験用PNG描画関数**。現EXE GUIのBattle runtimeには未接続。画面に `MANUAL TEST OVERLAY - NOT ORIGINAL GAME` ラベルを必ず描く。static TileCatalogと元map画像は無改変で利用。
- s1.map 110x110の座標(52,54)=tnok / (57,54)=0gnhkn+0 / (62,54)=udk を固定fixtureとしてPNG出力。tnok=chip/tnok.png、0gnhkn=chip/gnhkn.PNG、udkは既知prefixにimageが無いためplaceholder。原作の参加者・隊列・移動AI・draw orderと同一と**判定しない**。
- 作成物: `reports/battle_s1_manual_unit_fixture.png`、`reports/BATTLE_MANUAL_UNIT_FIXTURE_PROOF_20261011.json`。スクリーンショットは独自試験の静止画で、旧ゲームのGoldenスクショでも新EXEのplayable状態でもない。

### 描画候補の網羅度・残件
- save1で+0x1Cが唯一の構文宣言に一致する7351保存Unit（831 distinct ref）を、既存catalogの既知継承prefixと元PNGで探索。**6872保存Unit（429 distinct ref）**は現時点で画像ファイルを一つに特定できた（全7355の約93.4%）。
- 他は既知prefix上のimage未取得391、宣言のpreview拒否88（11 distinct refs、同名key重複等）、原DAT名自体の未解決4。image未取得391は「原作に画像が存在しない」の証明ではない。親継承解決・native image consumer・chip/chip2優先順位はVERIFY。
- 監査レポート `reports/UNIT_VISUAL_CANDIDATE_COVERAGE_20261011.json`（元script bytes/保存bytes/画像のコピーなし）。

### 実行確認
- 新 `tests/test_saved_unit_definition_bridge.py` **13/13 PASS**、source名衝突・同名複数宣言・capture混入・ID破損を拒否。
- 新 `tests/test_candidate_battle_placement_fixture.py` **11/11 PASS**、手動座標・元MAP寸法・source SHA・絵未発見・未解決IDの境界を確認。
- 新 `tests/test_candidate_battle_debug_overlay.py` **5/5 PASS**、元PNG合成・改変無し・MAP照合を確認。3ファイル合計29/29専用PASS。PCでPNG生成・試験レポート生成 exit0。
- 旧EXE Gameplay Golden0、strict gameplay MATCH0。全 `run_checks.ps1` はpeer survey長時間既往があるため今回未実行。既存コード・他レーンのDONE数には自動加算しない。

### 次工程
1. 本番の戦闘選択/参戦部隊決定・原作クラス合成・レベル/skill2効果を研究B/T011・A/T005の保存nativeで根拠付き確定し、戦闘用runtime Unitへ接続。保存Spotにいるだけで戦闘開始時の参加者と推定しない。
2. 安定した現F3定義閲覧GUIに、独立fixture adapterの視覚試験を安全に受け渡す。GUI担当のdirtyコードを横取りしない。見た目・選択・移動・当たり判定はBF-06/07として別途試験。
3. 研究E/T018による合法な旧ゲーム実機golden取得までは、screenshot比較・HP/MP/skill/CPU動作のstrict互換PASSを増やさない。天候/土砂崩れは後の拡張モードに分離。


### 同一プロセスでの結合回帰（最終追記）
- `python -m unittest -q test_saved_scene_state_api test_saved_unit_definition_bridge test_candidate_battle_placement_fixture test_candidate_battle_debug_overlay` をDesktop Commander Local上のdev_lab環境で実行。**Ran 40 tests in 70.923s / OK / BRIDGE_REGRESSION_EXIT=0** を確認。
- 対象は前回保存世界scene API 11件＋今回新13/11/5件。別AIのF3/EXE既存76件の再実行や全 `run_checks.ps1` 合格を意味しない。旧EXE actual gameplay Golden0、strict MATCH0維持。
- 新しいGUI本体 `battle_window.py` は参照のみ。Git index操作とコミット・公開なし。他AIのdirty編集を保護。次回はこのdocの最後の節を読めば、今回のコード/出典/レポート/未検証事項から再開可能。

## 2026-10-11 先行試遊モードの引継ぎ入口
- ユーザーはWikiマリナーズ傭兵団Ver.0.57の実画面を提示し、「早く形にして遊びたい」と試遊を優先。公開Wiki画像から確認できた戦闘画面はHPバー、選択状態、右の能力欄、左下命令列、上部一時停止・速度操作。素材は同梱Ver0.67を使用し、旧Ver0.57の数値は輸入しない。
- **いま実際に起動できる別EXE**：`dev_lab/dist/HakushinPlaytest/HakushinPlaytest.exe`（windowed、原ゲーム完全解凍版を外部読取）。これまでの静的/F3 `HakushinBattle.exe` を維持。
- 新ソース `playtest_launcher.py`、`src/hakushin_compat/playtest_rules.py`、`playtest_game.py`。**7体の明示仮Roster・戦闘試作ロジック**を使用し、選択・右クリック移動／攻撃・範囲技・回復・簡易AI・勝敗・ポーズ・可変速度が可能。元のゲーム機構に勝手に接続しない。
- 専用 `tests/test_playtest_rules.py` 16 + `test_playtest_game.py` 10＝**26/26 PASS**、同名GUI exeビルド・SDL dummy GUI起動・PNG・sfight.map startup各exit0。具体的操作とEXE SHAは `docs/BATTLE_PLAYTEST_QUICKSTART_20261011.md` に記録。
- GUI画面参照 `reports/battle_playtest_final_exe.png`、出力はGit ignore。元の公開Wiki画像は保存・コミットしていない。原作Gameplay Golden0、新strict MATCH0、研究DONE9/34据え置き。
- 次回：試遊実機で移動/攻撃/一時停止/速度/勝敗をユーザー確認してもらう。壁と川の衝突・Unit能力/skill実装・同条件原作AIの比較・戦闘開始ロスターは今後厳密に実装。新しいAIはまず本節とquickstart、既存のCURRENT_HANDOFF_BATTLEを読み、別AIのdirty GUI/WBS/MASTERに干渉しない。


## 2026-10-11 追加ハンドオフ：正規ゲーム仕様の「推測禁止」分岐（制作DEV）
- ユーザーは本来のゲーム性をチャットで答えず、元EXEの保存済み逆コンパイル／逆アセンブルと原DAT・原セーブから確認できた仕様だけ実装する方針に明示変更。以前作った別HakushinPlaytest.exeの仮HP/AI/範囲技は原作仕様ではなく隔離のまま。
- 新しくDEVLAB_NATIVE_PARENT_PRIORITY_RESEARCH_20261011.md、src/hakushin_compat/native_parent_candidate_audit.py、tests/test_native_parent_candidate_audit.py/test_native_single_kind_parent_audit.py、reports/PARENT_CANDIDATE_CONFLICT_AUDIT_20261011.jsonを作成。Unit/Classのbase二重候補への影響を全590 DATと3実保存のSHA付source名で定量化。親lookupが未確定なので、元能力値の生成を明示拒否する。
- 新しくDEVLAB_NATIVE_SKILL_CAPABILITY_20261011.md、src/hakushin_compat/native_skill_capability_subset.py、tests/test_native_skill_capability_subset.py、reports/NATIVE_SKILL_CAPABILITY_SUBSET_20261011.jsonを作成。保存x86のVA0x5739E4..A48と0x577843..997の限定成功分岐だけTyped Pythonへ移した。kind5/6、unknown action/failed gateはNativeSkillContractUnknown。原戦闘CPU/skill発動を創作しない。
- このチャットによる作業はdev_lab固有の新規source/test/doc/reportsだけ。ユーザー/別AIが編集するbattle_window.py・battle_definitions.py、原本、E MASTER、B T011/T013の正本、REA/Ghidra保存源へ書込みなし。Git stage/commit/pushなし。
- Native source局所試験、既存F3関連・DAT providerとの限定統合回帰結果を本chatで検査し、原作同条件Golden0/new strict0を増やさない。次の研究焦点はA/T005/B/T011の同名親base優先とEffectiveSkill組立、BF-19 comparator=0x50BF00の保存native未回収、B/T013の特殊kind5/6、E/T018可視動作観測。


## 2026-10-11 追加：native種類付きparent lookupと限定統合回帰
- 保存Ghidra 0x465060の親chain検索は構造種類文字列を受ける処理を含み、保存x86 callerの0x4A18D1..E2／0x432FA6..B5はeventとblockの別引数を渡している。
- 保存Ghidra 0x588470／0x58A650の一部Unit関連helperではUnit相当+0x1C名をunit型、+0x54名をclass型で別照会する。前者の保存native VA0x5885CA..0x588605はunit literal0x627784（既存文字列対応表で確認）から0x465060を呼ぶ。親base一般優先順位は未解明のままで、baseを参照する全宣言に実行時の競合があるという意味にはならない。
- 詳細な根拠と未確認事項はDEVLAB_NATIVE_PARENT_PRIORITY_RESEARCH_20261011.mdとreports/PARENT_CANDIDATE_CONFLICT_AUDIT_20261011.json内のsaved_original_native_typed_lookup_evidenceへ。
- 保存B所有nativeのSkill局所x86契約はDEVLAB_NATIVE_SKILL_CAPABILITY_20261011.md、src/hakushin_compat/native_skill_capability_subset.py、tests/test_native_skill_capability_subset.py、reports/NATIVE_SKILL_CAPABILITY_SUBSET_20261011.jsonへ。
- 親候補・技能局所契約・既存F3 source解析・DAT providerをまとめた限定Python回帰58/58 PASS、NATIVE_SOURCE_FOCUSED_EXIT=0（39.261秒）。旧EXE実機同条件GAMEPLAY Golden0／新native strict MATCH0。試遊EXEの仮ルールを本物の互換ソースへ移さない。
