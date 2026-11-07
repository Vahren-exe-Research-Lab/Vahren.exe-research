<!-- CURRENT-RESUME-20261026-HOVER -->
## 最初に読む：現在の再開位置（2026-10-26）
目的は教育・アイテム等の人材選択UIと共通DLL基盤の完成。完全エンジン再開発は現在の優先作業ではない。

1. [最新配置・試験記録](../_work/work_selector_hover_deployment_20261026.json)：元フォルダは旧DLLへ復元、研究版は診断用コピーに配置。PID20976は参考値なので操作前に再確認。
2. [共有依頼キュー](WORK_REQUEST_QUEUE.md)と[固定handoff](CHATGPT_CURRENT_HANDOFF.md)の「主HWNDガード後」を読む。状態PARTIAL。新パネルとAKYS詳細は実画面確認済み、技能ホバー説明は未成功。
3. [呼出所有権の根拠](../../data/recruit_sort_v4/tests/work_hover_ownership_20261026.json)と既存ソースを参照。次はdispatch/判定拒否の限定診断。広い再解析を繰り返さない。

記録は「静的根拠」「単体試験」「実機観測」「利用者確認」を区別し、対象版・SHA・再現手順・未検証範囲を残す。古い配置やPIDは履歴。キュー編集はWorkのみ。原作EXE/DAT/セーブを保持し、確定操作は現在無効。既知の修正拒否を別経路で迂回しない。

# 教育・アイテム選択UI／共通ローダー：研究・再開索引

## 他チャット・AI向け：最短の再開手順
1. 本書冒頭の最新状態を読み、共有依頼キューで担当・状態を確認する。
2. 固定引継ぎの末尾を読み、対象機能の根拠JSONだけを開く。過去のPID・SHA・配置成功を現在値とみなさない。
3. ホバーの最新証拠は [所有権と採否](../../data/recruit_sort_v4/tests/work_hover_ownership_20261026.json) と [REA呼出規約](../../data/recruit_sort_v4/tests/work_hover_call_abi_rea_20261026.json)。後者SHA: 3c412230ce9db6a0b37d0873ab50f0de182d7b4b211a7be96046ed468b43b031。所有権JSONの最新SHA: ed3a901d5a202097bacea041e2d8996874cc361cea402d68a0b268746370954a。同期接続部品の現状は [実装・試験記録](../../data/recruit_sort_v4/tests/work_hover_context_receipt_20261026.json) と末尾の最新追補を参照。
4. 原証拠・実装・単体試験・実機確認・未解決を別々に扱う。採用しなかった案の理由も参照して重複調査を避ける。
5. 担当成果は担当所有ファイルへ保存し、Workが共有キューを更新する。根拠のないCLOSED化や未検証の成功扱いはしない。


## 引継ぎ用の記録形式
各成果には次を残す。会話の要約だけでなく、再確認に必要なファイルを参照する。
- 依頼ID／担当／対象バージョン・SHA／変更したファイル・関数
- 確認段階：静的解析、隔離テスト、実機観測、利用者確認を分離
- 判明した仕様、採用・不採用の判断と理由、失敗した試験
- 再実行コマンドまたは操作手順、結果JSON・ログの保存先
- 未確認範囲、現在の配置版との差、次の一手、復旧方法
過去の追補は履歴として保持する。現在状態はこの冒頭と最新の根拠JSONを更新し、古いPIDや成功記録を現在の保証として扱わない。

## 現在のホバー実装（2026-10-26、研究ビルドまで）
- 状態：PARTIAL。同期ホバーをpreviewとCore adapterへ組込み、研究DLLのビルド・関連テストは完了。**この研究DLLはゲームへ未配置、実機ホバーは未確認。**
- 最新の実装・試験・ソースSHA：[統合記録](../../data/recruit_sort_v4/tests/work_selector_hover_integration_receipt_20261026.json)。
- 再実行：data/recruit_sort_v4/tests/run_work_selector_hover_host.ps1、core/test_selector_hover_adapter.ps1、core/build_selector_hover_research.ps1。
- 実装説明：[SELECTOR_PLUGIN.md](../../data/recruit_sort_v4/core/SELECTOR_PLUGIN.md)。通常ビルドと機能有効な研究ビルドを区別する。
- 残条件：0x521AF0のCALLを書き換える際の実行安全性。UIメッセージ境界だけで他スレッドの不在を証明した扱いにしない。所有権担当が既存資料を限定照合中。
- この確認が済むまでは配置版を交換しない。顔・能力・移動型のホバーは別の未完了範囲。

## 最初に読む：最新状態（2026-10-26、PID4972の試験まで）

目標は教育・アイテム選択UIと共通DLLローダーの完成。現在は **PARTIAL／表示試験版** です。下の時系列記録には旧状態も含むため、この要約と最新receiptを優先してください。

| 読みたい内容 | 参照先 |
|---|---|
| 作業分担・優先度・未完了範囲 | [共有依頼キュー](WORK_REQUEST_QUEUE.md)（Workのみ編集） |
| 次の担当が再開する位置 | [固定引継ぎ](CHATGPT_CURRENT_HANDOFF.md)の最新追補 |
| 地名再利用版・最新実機確認 | [最新記録](../_work/work_selector_spot_projection_actual_20261026.json)・[速度比較](../_work/work_selector_spot_projection_benchmark_20261026.json) |
| ホバー接続の残条件とソース照合 | [独立レビュー](../../data/recruit_sort_v4/tests/work_skill_hover_host_review_20261026.json) |
| 講師7人・生徒6人の前版実機確認、測定、配置SHA | [実機記録JSON](../_work/work_selector_snapshot_actual_20261026.json) |
| DAT重複読取削減の実装・関連40テスト | [統合記録](../_work/work_selector_snapshot_integration_20261026.json) |
| 再実行できる速度比較 | [ベンチマーク](../_work/benchmark_selector_snapshot.py)・[結果](../_work/work_selector_snapshot_benchmark_20261026.json) |
| 元一覧の非表示を行う研究DLLの配置・退避先 | [配置記録](../_work/work_selector_render_deployment_20261026.json) |

- 実機確認済み：自動パネル、元一覧の非表示、所在地・予想結果表示、講師の原作詳細、右クリック復帰。
- 速度：最新の地名再利用版で講師7人の表示受付2.103秒、後処理2.409秒。生徒6人の前版は受付2.474秒。別条件を混ぜず、受付と最初の描画フレームを区別する。瞬時表示は未達。
- 未完：確定操作（現版は無効）、実教育結果との照合、ホバー説明、準備中も含む完全置換、必須イベント、配布用依存分離。
- 再開：原作PID4972（06:55:34開始）の存在と画面を確認。水泳の原作講師一覧で未確定。パネルは閉じた。セーブ上書きなし。起動中のimport元Pythonを変更しない。
- 記録基準：静的解析／単体試験／実機観測／利用者確認を分け、失敗・未検証も残す。生ログだけで成功扱いせず、他担当は根拠と対象SHAを照合する。


更新: 2026-10-26。作業の入口は WORK_REQUEST_QUEUE.md と CHATGPT_CURRENT_HANDOFF.md。本書は成果を探す索引で、キューの状態管理を置き換えない。

## 現在の目的
教育・アイテム等の人材選択をチップ、検索、能力値、所在地、並替え、原作詳細表示で改善し、共通DLLローダー経由で使用可能にする。原作の候補・イベント進行・必須選択を維持する。旧新エンジン目標からこの作業へ優先変更済み。

## 確認段階
| 項目 | 根拠と現在の状態 |
|---|---|
| 原版直接起動→Core→雇用並替え | 利用者実機確認済み。biim兄貴の雇用後も正常。_work/work_loader_recovery_actual_20261025.json |
| selector自動起動 | PID10996でhelper起動、prewarm_ready7.96秒、epoch2の66候補、display_returned3.988秒。Computer Useで白いパネル、チップ、能力列、教育補正列、所在地を実際に確認。瞬時表示は未達 |
| UIからの教育・アイテム確定 | 現在のDLLは無効。過去の外部UI成功を今回の確定成功と混同しない |
| 元の名前ボタン一覧の非表示 | 研究DLLに機能フラグ付き統合。通常ビルドは無効。研究版で7候補の非表示・取消復帰を実機確認（末尾参照） |
| 詳細の技能ホバー説明 | 独立header/fixtureと独立review済み。本番未接続 |
| 顔・能力・移動型等の全ホバー | owner側定義とpreview対象の不一致あり。未対応 |

## 現在の起動構成
ゲーム内: Vahren.exe（原版）、dinput8.dll、HakushinCore.dll、plugins/HakushinRecruitPlugin.dll、plugins/HakushinSelectorPlugin.dll。
HakushinSelectorHelper.iniはUTF-16 LE BOM。明示有効化、Python/entrypointのSHA256を設定。
起動用entrypointはゲーム側HakushinSelectorHelper.py。研究core/selector_helper_entry.pyを直接参照しない。
Pythonはdev_lab/_work/toolchains/selector_runtime/Scripts/python.exe。-IでPillowが必要。通常Pythonのuser-siteは-Iでは見えない。
source_rootはまだdev_lab/src。確認中はこのimport対象も固定する。配布時には依存一式を分離して固定する必要がある。
helperは対象プロセス終了まで監視。一度失敗した画面への自動再送や履歴の消去による再試行はしない。
ログ: ゲーム側HakushinSelectorPlugin.log / HakushinSelectorHelper.log。helper_startedだけで成功としない。prewarm_ready→display_returned→画面確認を区別。

## 解析成果（data/recruit_sort_v4以下）
- tests/hover_abi_20261026.json: 原版SHA一致・機械語・hover/clear/座標ABI。0x561120はECX=self、stack x,y、ret8。0x562140はclear、正常EAX=0なのでbool扱い禁止。
- src/work_selector_skill_hover.h: 技能限定、先行7RECT除外、最大100、UIthread/epoch/target照合、cleanup debt。tests/test_work_selector_skill_hover.c / skill_hover_validation_20261026.json。
- tests/work_choice_render_research_20261026.json: 0x41E910は生成・レイアウト・描画面構築。省略禁止。描画getter slot0x638238、呼出戻り先0x4C4D78を対象限定する方式。
- tests/work_choice_render_source_integration_evidence_20261026.json: 機能フラグ付き研究DLL/試験。tests/HakushinSelectorPlugin-render-research.dllを配置済み。起動状態は末尾の追補参照。
- core/SELECTOR_HELPER.md: 明示起動・信頼対象・設定・試験仕様。
- core/SELECTOR_HELPER_REVIEW_FIX_RECEIPT.txt: Unicode設定、遅延installer起動抜けの修正。
- core/SELECTOR_HELPER_LIFETIME_RECEIPT.txt: 1時間制限除去とprocess寿命監視。

## 失敗から得た運用規則
1. 実機確認依頼後に研究entrypointを変更し、配置pin不一致になった。配置物と研究物を分離し、試験中の版を固定する。
2. PILを通常Pythonでしか確認せず、-I起動で失敗した。必ず配置されたexeと同じ引数・依存環境で確認する。
3. DLLがACTIVEでもhelperが起動しなければ自動表示しない。各段階のlogを確認する。
4. 原作起動障害の原因は未特定。ZIP上書きで復旧したことだけが事実。DLLや多重起動が原因と断定しない。
5. 広範テストに途中エラーがあったが最終報告未取得。全件PASSという記録にしない。狙った関連試験だけの結果を明記する。

## 次の作業
1. PID/作成時刻/配置SHA/ログ/画面を照合し、現在の自動表示を確定する。
2. 元一覧非表示の研究統合を別担当レビュー。Core予約、元ポインター照合、復帰、FP/SSE保持、世代・可視性・所有権を確認。
3. 研究版へ切替時は原作終了とプロセス消滅を確認。原版EXE/DAT/saveを変えない。通常セーブを上書きしない。
4. 取消・開き直し・最小化・ウィンドウ移動・必須イベント・確定処理を段階的に実機検証する。
5. 4秒の表示時間を実測で短縮。事前読込7.96秒と一覧表示3.988秒を足し引きして別場面の速度と比較しない。

## 他担当のルール
共有キューはWorkのみ編集。他担当は自分の成果/根拠/未解決/テスト/再開位置を保存しWorkへ返す。Git操作禁止。既存Ghidra V3 canonicalを先に検索して重複解析を避ける。REA MCP復旧済み、設定変更不要。
保護された確定guardのLocal拒否は残件。経路変更で同じ拒否操作を迂回しない。protected bridge/live/selector本体の変更前には既存記録を読む。

## 追加実機確認（2026-10-26）
PID10996: WorkがLv見出し昇順、行選択と原作詳細、右クリック取消を画面で確認。教育未実行・セーブ未保存。_work/work_selector_autostart_actual_20261026.jsonを参照。


## 2026-10-26 記録共有・研究版配置の追補
- 利用者要求: 有用な調査結果をPCに保存し、他チャット・AIが利用できる形式にする。入口は docs/SELECTOR_LOADER_RESEARCH_INDEX.md。主張ごとに根拠ファイル、検証段階、未解決事項を分ける。
- WORK-SELECTOR-NATIVE-REPLACEMENT-20261025: Work / P0 / PARTIAL。研究DLL 33b0cca79b1627e9d74f35fd32b7c198f2374debe7ec1f13935c787f5a051e04 を配置済み。以前の「未配置」はこの追補で更新する。バックアップ _work/HakushinSelectorPlugin_before_render_20261026.dll（faf39b3df2da93b48fb09b4b82407c6dbff8945182f2fa537e7853f9dfd7d933）。配置receipt: _work/work_selector_render_deployment_20261026.json。
- 起動確認: PID23724、開始2026-10-26 02:48:58+09:00、原版のパスを照合。再確認でもMainWindowHandle=0、タイトル空欄、Responding=true。画面未表示。停止・クラッシュ・DLL原因とは未確定。二重起動はしない。
- 再開位置: 現PIDの存在・作成時刻・モジュール・起動ログを再確認し、必要ならこの試験プロセスの終了確認後にバックアップDLLへ戻して比較。原作EXE/DAT/セーブは変更しない。この時点では元一覧の描画抑止は実機未確認。後続の実機確認を参照。確定操作は無効のまま。
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

### 他チャット・AIへの渡し方
この索引→共有依頼キューの現行目標→固定引継ぎの最新追補→担当する機能の根拠JSON/ソースの順に読む。履歴中の旧目標・旧配置・旧PIDを現在状態と混同しない。実機へ接続する前にプロセスと配置版を取り直す。
再現用の最小記録様式：結論／対象版・SHA／根拠ファイルと行・VA／試験手順／実測結果／未検証・制約／次の一手。機械可読JSONには同じ根拠と結果を保存する。


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


## 最新訂正 2026-10-26：ホバー診断・ゲーム終了済み
共有キューの「ホバー診断の続報：操作ツールによる遮蔽」を優先する。診断ではcodex-computer-use.exeの全画面ウィンドウがカーソル非遮蔽条件を止めていた。根拠は ../_work/work_hover_diagnostics_akys_skill1.json と work_hover_occlusion_akys_skill1.json。安全判定は緩めていない。右クリック復帰は確認済み、技能説明切替えの安定確認は未完。
試験PID24116は通常終了し、Vahren不在確認後に診断用コピーのselectorを研究版0fa2145d…へ復元した。元フォルダの旧DLLは変更なし。PID20976/24116が開いたままという過去記録は失効。最新診断artifact4d0926d1…は単体12構成PASS・未配置。read_hover_diagnostics.pyは旧診断SHA/PID固定なので再利用前にidentityを更新する。機械可読deployment記録の更新はLocal timeoutで未確認、古いstageを優先しない。


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

## 2026-10-26 DAT汎用UIの最小実証（承認済み・作業中）
入口は DAT_GENERIC_UI_SPIKE_PLAN_20261026.md。評価は DAT_GENERIC_UI_DESIGN_REVIEW_20261026.md。静的根拠は ../../data/recruit_sort_v4/tests/work_dat_ui_dispatch_evidence_20261026.json と work_dat_ui_result_evidence_20261026.json。未配置DAT fixture work_dat_ui_spike_v1.datは静的parseのみ確認、DLL往復未完成。新経路の補正値はDATから渡し、DLLが教育DATを再解析する方式に戻さない。
- 汎用数値列・要求結合の再現入口：../../data/recruit_sort_v4/tests/run_custom_column.ps1、run_work_dat_ui_request.ps1、run_work_dat_ui_panel.ps1。Win32部品とrequest契約までの試験で、原作DAT往復は未完。明示命令の型/配置根拠：同tests/work_dat_ui_literal_evidence_20261026.json。
- DAT明示呼出の入口部品：tests/work_dat_ui_dispatch_receipt_20261026.json（schema2、旧Cwrapperの例外問題とtailjump修正）、work_dat_ui_snapshot_evidence_20261026.json（読取専用変数抽出）。どちらも隔離試験のみ。ゲーム側の待機・結果書込み・再開は未接続。

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

## 2026-10-29 記録整理
- 原文2件をarchiveへ保存し、内容とハッシュの一致を確認。引継ぎは現行目標に整理。
- 回帰結果は12組成功・2組未完了。拒否の迂回なし。エージェント結果は回収済み。
- 10:52のゲーム終了は手動操作と訂正。音声クラッシュは再発時だけ調査。
- 統合版はテストのみ。次は独自数値列と所在地列をまとめて実機確認。
- 混在変更のため今回コミットなし。以下は整理時点の未コミット一覧。

 M docs/BATTLE_MODE_FIRST_WBS_20261011.md
 M docs/CHATGPT_CURRENT_HANDOFF.md
 M docs/PEER_SCRIPT01_FINDINGS_20261011.md
 M docs/WORK_REQUEST_QUEUE.md
 M recovered_source/INDEX.md
 M recovered_source/manifest.json
 M recovered_source/verified_call_graph.mmd
 M src/hakushin_compat/battle_definitions.py
 M src/hakushin_compat/battle_static_tiles.py
 M src/hakushin_compat/hit_linked_award_subset.py
 M src/hakushin_compat/native_battle_outcome.py
 M src/hakushin_compat/native_battle_runner.py
 M src/hakushin_compat/native_battle_session.py
 M src/hakushin_compat/native_battle_view.py
 M src/hakushin_compat/native_dat_damage_adapter.py
 M src/hakushin_compat/native_dat_heal_adapter.py
 M src/hakushin_compat/native_heal_mutation_subset.py
 M src/hakushin_compat/native_heal_numeric_profile.py
 M src/hakushin_compat/native_unit_ai.py
 M src/hakushin_compat/native_unit_hit_prefix.py
 M src/hakushin_compat/native_unit_motion.py
 M src/hakushin_compat/native_unit_movement.py
 M src/hakushin_compat/peer_script01_battle_end.py
 M src/hakushin_compat/peer_script01_native_definitions.py
 M src/hakushin_compat/peer_script01_power_diplomacy.py
 M src/hakushin_compat/peer_script01_power_hire.py
 M src/hakushin_compat/peer_script01_strategy_events.py
 M src/hakushin_compat/peer_script01_strategy_world.py
 M src/hakushin_compat/peer_script01_turn_frame.py
 M src/hakushin_compat/peer_script01_war_start.py
 M tests/test_battle_window.py
 M tests/test_hit_linked_award_subset.py
 M tests/test_native_battle_runner.py
 M tests/test_native_battle_session.py
 M tests/test_native_dat_damage_adapter.py
 M tests/test_native_unit_hit_prefix.py
 M tests/test_native_unit_motion.py
 M tests/test_native_unit_movement.py
 M tests/test_native_unit_tick.py
 M tests/test_peer_script01_battle_end.py
 M tests/test_peer_script01_power_diplomacy.py
 M tests/test_peer_script01_power_hire.py
 M tests/test_peer_script01_strategy_events.py
 M tests/test_peer_script01_strategy_world.py
 M tests/test_peer_script01_turn_frame.py
 M tests/test_peer_script01_war_start.py
?? build_hire_ui.ps1
?? build_runtime_battle.ps1
?? docs/DAT_GENERIC_UI_DESIGN_REVIEW_20261026.md
?? docs/DAT_GENERIC_UI_SPIKE_PLAN_20261026.md
?? docs/SELECTOR_LOADER_RESEARCH_INDEX.md
?? docs/WORK_PLUGIN_FOUNDATION_PLAN.md
?? docs/WORK_RECRUIT_PLUGIN_MIGRATION.md
?? docs/archive/
?? recovered_source/ghidra_c_pseudocode/FUN_0040B200.c
?? recovered_source/ghidra_c_pseudocode/FUN_00427040.c
?? recovered_source/ghidra_c_pseudocode/FUN_004270F0.c
?? recovered_source/ghidra_c_pseudocode/FUN_00428010.c
?? recovered_source/ghidra_c_pseudocode/FUN_00428710.c
?? recovered_source/ghidra_c_pseudocode/FUN_00429C60.c
?? recovered_source/ghidra_c_pseudocode/FUN_00432EE0.c
?? recovered_source/ghidra_c_pseudocode/FUN_00435550.c
?? recovered_source/ghidra_c_pseudocode/FUN_0045E5F0.c
?? recovered_source/ghidra_c_pseudocode/FUN_004705F0.c
?? recovered_source/ghidra_c_pseudocode/FUN_00470700.c
?? recovered_source/ghidra_c_pseudocode/FUN_00471AF0.c
?? recovered_source/ghidra_c_pseudocode/FUN_00471D20.c
?? recovered_source/ghidra_c_pseudocode/FUN_004930C0.c
?? recovered_source/ghidra_c_pseudocode/FUN_004A6700.c
?? recovered_source/ghidra_c_pseudocode/FUN_00514D60.c
?? recovered_source/ghidra_c_pseudocode/FUN_00514F10.c
?? recovered_source/ghidra_c_pseudocode/FUN_005154F0.c
?? recovered_source/ghidra_c_pseudocode/FUN_005155C0.c
?? recovered_source/ghidra_c_pseudocode/FUN_005158A0.c
?? recovered_source/ghidra_c_pseudocode/FUN_00565700.c
?? recovered_source/ghidra_c_pseudocode/FUN_0057CFA0.c
?? recovered_source/ghidra_c_pseudocode/FUN_0057CFD0.c
?? recovered_source/ghidra_c_pseudocode/FUN_005964C0.c
?? recovered_source/ghidra_c_pseudocode/FUN_00598980.c
?? runtime_battle_launcher.py
?? src/hakushin_compat/battle_runtime.py
?? src/hakushin_compat/battle_runtime_actions.py
?? src/hakushin_compat/battle_runtime_audio.py
?? src/hakushin_compat/battle_runtime_geometry.py
?? src/hakushin_compat/battle_runtime_movement.py
?? src/hakushin_compat/battle_runtime_skills.py
?? src/hakushin_compat/battle_runtime_terrain.py
?? src/hakushin_compat/battle_runtime_view.py
?? src/hakushin_compat/native_skill_bookkeeping.py
?? src/hakushin_compat/peer_script01_live_observer.py
?? src/hakushin_compat/script_declaration_cache.py
?? src/hakushin_compat/work_choice_observer.py
?? src/hakushin_compat/work_education_contract.py
?? src/hakushin_compat/work_education_outcome.py
?? src/hakushin_compat/work_education_prediction.py
?? src/hakushin_compat/work_exp_observer.py
?? src/hakushin_compat/work_numeric_variables.py
?? src/hakushin_compat/work_power_spots.py
?? src/hakushin_compat/work_runtime_stats.py
?? src/hakushin_compat/work_selector_auto.py
?? src/hakushin_compat/work_selector_auto_history.py
?? src/hakushin_compat/work_selector_auto_policy.py
?? src/hakushin_compat/work_selector_display_metadata.py
?? src/hakushin_compat/work_selector_education_context.py
?? src/hakushin_compat/work_selector_education_outcomes.py
?? src/hakushin_compat/work_selector_education_student.py
?? src/hakushin_compat/work_selector_icons.py
?? src/hakushin_compat/work_selector_ingame_preview.py
?? src/hakushin_compat/work_selector_live.py
?? src/hakushin_compat/work_selector_outcome_packet.py
?? src/hakushin_compat/work_selector_presentation.py
?? src/hakushin_compat/work_selector_prewarm.py
?? src/hakushin_compat/work_selector_runtime_metadata.py
?? src/hakushin_compat/work_selector_spot_names.py
?? src/hakushin_compat/work_selector_student_context.py
?? src/hakushin_compat/work_selector_swim_outcomes.py
?? src/hakushin_compat/work_selector_vm_commands.py
?? src/hakushin_compat/work_selector_vm_context.py
?? src/hakushin_compat/work_swim_prediction.py
?? src/hakushin_compat/work_unit_selector.py
?? src/hire_ui_extension.c
?? src/hire_ui_extension.h
?? src/hire_ui_observation.c
?? src/hire_ui_probe_host.c
?? tests/hire_ui_dll_test.c
?? tests/test_battle_runtime.py
?? tests/test_battle_runtime_actions.py
?? tests/test_battle_runtime_audio.py
?? tests/test_battle_runtime_geometry.py
?? tests/test_battle_runtime_movement.py
?? tests/test_battle_runtime_skills.py
?? tests/test_battle_runtime_terrain.py
?? tests/test_battle_runtime_timeline.py
?? tests/test_battle_runtime_view.py
?? tests/test_peer_script01_live_observer.py
?? tests/test_script_declaration_cache.py
?? tests/test_script_snapshot_scope.py
?? tests/test_work_choice_observer.py
?? tests/test_work_education_contract.py
?? tests/test_work_education_five_predictions.py
?? tests/test_work_education_outcome.py
?? tests/test_work_education_prediction.py
?? tests/test_work_education_tea_prediction.py
?? tests/test_work_exp_observer.py
?? tests/test_work_numeric_variables.py
?? tests/test_work_power_spots.py
?? tests/test_work_runtime_stats.py
?? tests/test_work_selector_auto.py
?? tests/test_work_selector_auto_history.py
?? tests/test_work_selector_auto_lifetime.py
?? tests/test_work_selector_auto_persist.py
?? tests/test_work_selector_auto_policy.py
?? tests/test_work_selector_commit_ui.py
?? tests/test_work_selector_display_metadata.py
?? tests/test_work_selector_display_timing.py
?? tests/test_work_selector_education_context.py
?? tests/test_work_selector_education_outcomes.py
?? tests/test_work_selector_education_student.py
?? tests/test_work_selector_icons.py
?? tests/test_work_selector_live.py
?? tests/test_work_selector_metadata_cache.py
?? tests/test_work_selector_outcome_packet.py
?? tests/test_work_selector_presentation.py
?? tests/test_work_selector_prewarm.py
?? tests/test_work_selector_runtime_metadata.py
?? tests/test_work_selector_sender_sequence.py
?? tests/test_work_selector_spot_cache.py
?? tests/test_work_selector_spot_names.py
?? tests/test_work_selector_student_context.py
?? tests/test_work_selector_swim_outcomes.py
?? tests/test_work_selector_teacher_subjects.py
?? tests/test_work_selector_vm_commands.py
?? tests/test_work_selector_vm_context.py
?? tests/test_work_swim_prediction.py
?? tests/test_work_unit_selector.py

## 2026-10-29 独自列統合版の配置
- 統合DLL・試験DAT・設定を診断コピーに配置、変更前バックアップと前後照合済み。原作は変更なし。
- 実機確認：タイトル起動とユーザー報告の3人表示。写真はCount=3、Index=-1、Result空、Status=2、Before/After=1、Backend=0、Anchor=1の取消結果。
- テストのみ：独自列と所在地IDの内容・並替え・選択返却は実機確認中。取消写真を独自列成功の証拠にしない。
- 接続の一時タイムアウト後、ファイル接続は復帰。次は表示内容の回答と実行ログを照合。


### 2026-10-29 独自列の実機確認
- 実機確認：ユーザー画像で帝国歩兵3人のBonus=-5/30/55昇順表示。選択a000+1のResult=a000+1、Status=1、Backend=1をユーザー確認。
- 実機確認：場面Bの所在地ID列はID: sp_mtなどを表示。人向け地名の解決は未実装。
- 次：ボタンなし版の実機確認。原作フォルダは変更なし。

## 2026-10-30 並行レビューの回収
- したこと：2担当の読取レビューを回収し、共通選択ラッパーと一括雇用の該当コードを親でも照合した。コード・ゲーム配置は変更なし。
- 結果（静的確認）：教育24入口・人材アイテム・解雇・一部ランダムイベントはchoiceUnitFromListに集約。一括雇用は全隊長自動対象であり、選択一覧の単純差替えではない。
- 要修正：診断claude_lecture_v4.datは全用途へ補正=magdefと取消可能を固定。非教育の列設定、専門学校送り等の強制選択条件を呼出側の規則と照合してから対応する。
- 配布レビュー：現在confは選択DLL単独。現行v4と雇用DLLの同居・無効化・差替え・不一致拒否の受入が必要。旧READMEの直接起動で無効という説明は新ローダーに適用不可。
- 次：教育12科目の講師/生徒/取消/実行、通常・制限付きアイテム、選択イベント、配下管理を受入表にまとめ、配布候補で通し確認する。大規模な将来目標はGITHUB_DEVELOPMENT_PLAN.mdに分離した。
