# 共通プラグイン基盤 実装計画

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


Goal: 原版EXEを変更せず、設定で許可した機能DLLを追加・交換して拡張する。既存selectorの完成とは別に進捗を管理する。
Architecture: 起動入口とCoreを分離。dinput8 proxyを第一候補とし、原作DirectInput呼出をsystem DLLへ転送。CoreがAPI、依存、ライフサイクル、hook所有、ログを管理する。原作の保存済みPE表と現物解析でDirectInput8Create importを確認済み。実機proxy loadは未確認。
Tech stack: 既存Zig 0.14.1、C ABI、x86 Windows DLL。新しい外部依存を導入しない。
Spec: 利用者の共通DLLプラグイン基盤10要件とCHATGPT_CURRENT_HANDOFF.md WORK-COMMON-PLUGIN-FOUNDATION-REQUEST-20261023。

## 制約
- EXE/DAT/save不変。Git変更操作なし。既存他担当ファイルを触らない。
- 実装はdata/recruit_sort_v4/coreに集約し、既存配布ZIPを上書きしない。
- 未知DLLはLoadLibrary前に設定で除外する。ロード後API照合は未知DLL対策ではない。
- 32bit/C calling convention/構造体size/API versionを明示。プロセスポインタを将来64bit IPC形式として流用しない。
- DllMainでpluginロードや待機をしない。初期化はloader lock外で行う。
- DLLの失敗は障害隔離を保証しない。任意pluginクラッシュから原作を必ず守れると宣伝しない。
- 実行中hot reload不要。起動済pluginはshutdown順序を守り、callback/hookが残る状態でunloadしない。

## Task 1 ABIとCore試験（担当 core_abi）
- [x] version/size付きAPI header、HakushinCore.dll、許可済絶対pathを明示したplugin load関数。
- [x] 正常plugin、version不一致、init失敗をx86 hostから検証。
- [x] 実DLL build/runを行う。これは自動検出/原作統合の完成ではない。

## Task 2 設定と依存
- [x] 明示的enabled plugin ID/file、順序、required API、依存IDを設定で宣言。未宣言DLLは検出してもロードしない。
- [x] DLL実行前に重複ID、循環、依存欠損、無効依存、path traversal、x64、API宣言不一致を検査。依存順は安定的に決定。
- [x] メタデータに反する実APIは初期化前に拒否。依存init失敗なら従属を開始しない。
- [x] UTF-16 Windows pathとログ保存先をmodule基準で解決し、cwdに依存しない（startup fixture、下記追補参照）。

## Task 3 hook/event共通管理
- [ ] 同一targetの二重所有を拒否。まず予約/解除をfixtureで確認し、実patchは確認済hook契約ごとに実装。
- [ ] 原作hookのABI/期待bytes/EXE identity照合。失敗時rollback、開始順と逆順shutdown。
- [x] event購読・解除の寿命と再入を定義し、解除後callbackを呼ばない試験（standalone + Core extension fixture）。

## Task 4 proxyと原作検証
- [x] system directoryの本物dinput8を絶対pathで解決、DirectInput8Createを同じABIで転送。
- [x] Core無効/欠損/起動失敗時の原作継続をfixture検証。安全でない部分初期化はログに明示（実機全条件の証明ではない）。
- [ ] 原作を通常終了した後のみ配置。二重起動防止、原版SHA不変、実ロードmodule path、タイトル・入力・戦闘を確認。

## Task 5 BattleObserverと配布
- [ ] 現物所在の回答または台帳参照から回収。未発見を再実装成功としない。
- [ ] 既存観測機能をAPI経由へ移し、hook重複防止・イベント通知を試験。
- [ ] 追加/無効化/差替/異常plugin/API更新/ゲーム復帰の検証結果と既知制限を記録。

## Review focus
DllMain副作用はAPI確認以前に起きる／失敗initのpartial登録／依存先停止後callback／パスとworking directory／設定無効でも残るhookを重点確認する。

## 現在の範囲
設計の細部はWork判断。元のユーザー仕様は維持。Core ABI fixtureから段階的に実装し、未完工程を隠さない。BattleObserver所在は質問中。SELECTORの過去拒否修正は別件のまま維持する。

## WORK-CORE-BOOTSTRAP-20261025
Task 1とTask 2のmanifest/PE preflight/runtime接続はfixtureで検証。module基準の設定ファイル読取・ログ保存・起動統合は未完了。証拠 _work/work_core_bootstrap_20261025.json。


## WORK-PLAN-STATUS-20261025-RECRUIT
上記初期チェックリストの追補: module基準config/log、起動失敗時DirectInput継続はstartup12fixtureで確認済み。予約管理とCore extensionは実装検証済み（実patch共通管理とは区別）。原作proxy-only title到達済み、入力/戦闘未検証。雇用adapterを配置済み、利用者による実機確認待ち。BattleObserver現物未発見。


## WORK-EVENT-DISPATCH-PLAN-20261025
共通event実装を独立担当event_dispatcherへ委任。既存Core/原作を変更せずcore/hakushin_events.*とfixture/build/docsのみ所有。登録順の同期通知、ownerと世代付き解除、通知中の自己解除/他者解除、通知開始後の追加は次回から、再入emit拒否、実行中callbackが終わるまでownerをbusyとする。threadはcaller直列化、payloadは通知中のみ借用。
Ruling: 原作診断ログ待ちに独立した共通event要件を進める。戦闘eventを取得できたとは扱わず、Core接続はレビュー後に別段階。現行gameへは配置しない。誤った設計判断ならdispatcher部分のみ修正でき、雇用実機試験に影響しない。


## WORK-CORE-CALL-EXTENSION-PLAN-20261025
現在の最優先は雇用plugin修正版の実機確認。ゲーム操作は利用者、原作配置への追加変更なし。旧初期化thread待機の修正配置済み、実機成功は未確定。
Ruling: 確認を待つ間に、既に検証したCALL管理をCore extension3/version1へ接続する。ABI1を維持し、Coreが発行するinstanceで所有する。共通予約との重複を拒否し、管理patchの予約を通常releaseで解放させない。patch/復旧recordが残るinit失敗・shutdownではmoduleを保持。quiescenceは利用側の責任であり自動drainや安全unloadを保証しない。
担当core_call_extension、所有はcore/のCore実装・extensions・新fixture/docsとbuild linkage。原作/配布/queue/handoffは変更しない。rootが独立reviewとtargeted test後に記録する。元の10要件を縮小せず、BattleObserver現物未発見、戦闘hookとゲーム実機確認は未完のまま。
