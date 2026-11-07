配布用ZIP: dist/HakushinRecruitSort-0.1.0-preview.zip。導入説明は同梱README.txtを参照。雇用後自動並替えも実機確認済み。

# 現在版：4分類並替え（2026-10-22）

現行DLL: dist/HakushinRecruitSortV4.dll
SHA256: ffdc73d2f416ab29d89089bdafee487b712b85d693426c31db4539bac3e0c981

全所属人材について判定し、誰か1人で成立すれば雇用可能を優先。
表示順は雇用可能→リンクあり領地不足→リンク/領地あり資金不足→リンクなし。同群は元順。
原版EXEにDLLを接続し、画像とクリック矩形だけを並替えます。

実機確認: 開いた時点の自動並替え、リセット1回での再適用。資金495で資金不足6人・リンクなし11人をログ確認。
関連描画テスト10PASS。未解決: 一瞬原順が見える、領地不足の実機照合、実雇用後更新。

起動: ゲーム終了状態で tools/launch_original.ps1 をPowerShellから実行。
既存ゲームがあれば新規起動しません。原版ハッシュを確認し、1つ起動して研究distのDLLを接続します。
起動待ち・接続失敗でもゲームは強制終了しないため、残っている状態で別のゲームを起動しないでください。
今回追加したロード待ちは構文/CheckOnlyのみ検証、起動全体の再試験は未実施。
拡張なしで使用するときは一度終了し、原版Vahren.exeを直接起動してください。
原版EXE・DAT・セーブは変更しません。ゲームフォルダの旧V4 DLLは現在の接続先ではありません。

以下は履歴です。旧「relation-only」「未実機検証」等は現在の状態を表しません。最新証拠はreports/staged_on_pc.json。

---

# 人材雇用画面・雇用関係優先表示 V4（2026-10-21）

状態： BUILD=PASS / x86_WIN_NATIVE_RELATION_SYNTHETIC=PASS / V4_INSTALL_STAGE_8_CALLS=PASS / GAMEPLAY=NOT_RUN / VISUAL_SORT=UNVERIFIED

V3では人材17人のうち押下フラグが全員0だったため並び替えなし。
V4ではWorkが実ゲームUIスレッドで検証した0x586080を採用：
ECX=候補定義、ESI=雇用者定義、AL=関係判定。
雇用者の一覧にある雇用者をOR判定し、関係ありの候補を先頭表示する。
資金不足・人数上限などの最終雇用条件は変更しない。

## V3からの改修
- +0x1480（押下可能フラグ）を雇用関係の判断に使用しない。
- Work所有のネイティブ定義マップ解決とABI橋渡しを、独立コピーで再利用。
- 28byte C++ std::stringの候補ID・費用・セーブは不変。画像とRECTの対応だけ動かす。
- 0x004D4A50直接CALLを8箇所フック。追加2箇所：0x004A5B28 / 0x004A5B54（reloadMenu）。
- 画面描画時に優先候補数、判定失敗理由、並び替え回数をログへ記録。
- DLLもEXEもV4専用名。V3と原本は上書き禁止。

## 実施済みテスト
- Windows32bit DLLの公開関数名、PE構造を確認。
- Windowsネイティブで両EXEの起動前DLLフック設置が終了コード0：8箇所成功。
- tests/test_priority_win32.c：4MB模擬メモリ、候補17・雇用者5・優先6、61 native ABI呼出に成功。
- 破損状態、ロスターのモード不一致、未生成キャッシュでは、元配列を変更せず失敗する。
- Workの実機記録：5雇用者、17候補、6人優先、78 native呼出。実機側はまだV4で未再観測。

## 実機確認時の注意
1. 原本とセーブデータをバックアップ。V4は別名EXEなので、高DPI設定もV4名ごとに必要。
2. V4実験EXEを起動、まず人材雇用の表示だけを確認。初回は実際に雇用を確定しないこと。
3. ゲームフォルダの HakushinRecruitSortV4.log を読み、relation ready や priority skipped を確認。
4. マウス座標、ホバーした候補と表示テキスト、並び順とスクロールの整合を優先確認。
5. 不具合があればV4を閉じ、原本EXEを使用。スクリーンショットとログを研究記録に保管。

## 未解決事項
- 描画バッファの並び替えと最終画面表示の関係。Work以前の試験で再描画消失現象があった。
- ネイティブ関係判定は雇用費用・所属条件まで完全評価したものではない。
- 原作一覧に存在する100件上限の外側はソート不可。
- Windowsの実ゲーム画面で並び順・クリック・セーブをまだ検証していない。
- Work所有のdev_lab/src、MASTER、他レーン、製品DAT、原本EXEは未変更。


## WORK-V4-FOUR-GROUPS-20261021

ユーザーからV4引継ぎを受領し、data/recruit_sort_v4を改修正本として確認。新要件は安定順: 0雇用可能、1雇用リンクあり領地不足、2リンク/領地あり資金不足、3リンクなし。複数雇用者では完全成立を優先し、なければ領地成立の資金不足を採用、誰も領地成立しなければ領地不足。表示グループの順番と複数雇用者の成立度を混同しない。rect_sort_core.hに4分類/雇用者間集約/安定順列を追加。関連条件がunknownなら拒否。新規5組の条件assertと既存10000矩形ケース成功。native relation模擬17人/5雇用者/61calls成功。4段階分類のネイティブ領地/費用入力は未接続: 製品DLLは依然relation-onlyであり4段階完成とは扱わない。原作UI保存4D4A50 L1066-1084には5AC880等の領域集合と資金/価格比較がある。価格はL1012-1046の雇用者依存補正を含むため、全員表示の価格をそのまま各雇用者の価格と推測しない。今後native ABIを確認して入力アダプターへ接続。
V4の再描画を修正: 通常thiscallだけでは不足する453C20のEBX=0を、Workで実測済みのbridgeと同形式で設定。対象window最小確認サイズを1554→1558へ修正。build成功、dist DLL SHA ac840dc8d20243e0d941ba65b30987e72e2f0fc148797f25d19cb42e48e84b7f。ゲームフォルダの配置DLLは今回は未更新、原本/セーブ/他担当は未変更。最新保存V4実機ログはrenderer初回→priority skipped reason=-8 n=17。ユーザーは並び変化ありと報告しており、ログと同一回の観測とは未確認。-8はHkReadNativeEmployers拒否であり、ロード時フック成功と分離して調査する。V4全完成/実雇用/クリック整合は未検証。Work旧105checks版panel/restoreソースはdev_labに残るが実機パネル起動未実施、V4へ混在させない。次P0=roster mode/count/取得時点を診断、原作領地・雇用者別価格/資金の意味/ABI確認、4段階入力接続、V4描画・hover実機試験。上限100件は継続VERIFY。Golden0/MATCH0。


## WORK-V4-DIAGNOSTIC-20261022

段階試験用の診断モードを追加。起動する試験プロセスの環境変数HAKUSHIN_SORT_V4_DIAGNOSTICを正確に1とすると、四分類判定をHakushinRecruitSortV4.logへ記録する。未指定時は従来のrelation-only表示。診断時は表示順・hitboxを変更しない。rowは0始まり原作候補順、rank0雇用可/1領地不足/2資金不足/3リンクなし。1成功snapshotまで、失敗最大8試行。雇用者絞込・hover絞込はスキップ。再記録には試験プロセス再起動が必要。native queryがscratchを使うため完全read-onlyとは表記しない。実機分類は未検証。配備前にゲーム終了と旧DLLのhash/所有を確認する。既存stage_v4.pyは異なる既存DLLの上書きを拒否する仕様のため、無理に実行して回避しない。
検証: test_diagnostic_win32.c、test_priority_win32.c、test_rect_v4.c。診断テストは本番rendererとfake classifierで、実ゲーム判定の一致証明ではない。


## WORK-V4-ACTUAL-SORT-20261022

現在の通常起動は4分類並替えです（以前のrelation-onlyという記述は旧版）。表示順0雇用可→1領地不足→2資金不足→3リンクなし、同群は元順を維持。診断環境変数=1のときだけ表示変更を停止。新版DLLはゲーム側へ配置済み、SHA45540b5f10352135e97d96d7bcd6a94620a7280e30770a93542767705aa96b0c。旧版バックアップdist/HakushinRecruitSortV4.pre_diagnostic.dll。復元はゲーム終了後・対象hash確認後に行う。
実機確認済み: 17候補中6人先頭、リセット後再適用（ユーザー報告＋描画ログ）。未確認: 領地不足/資金不足混在、実雇用後更新。研究成果はreports/staged_on_pc.jsonに条件/ログ/候補ID付き。原作EXE/saveは変更していない。


## WORK-ORIGINAL-EXE-ATTACH-20261022

原版Vahren.exeを使える。tools/launch_original.ps1をPowerShellから起動すると原版SHA確認→ゲームを可視起動→UI-thread bootstrapでDLLを接続する。-CheckOnlyは起動せずパス/原版hashを検査。既存ゲーム起動中は拒否。DLLはdistの絶対パスから読む。原版EXEやd3dx DLLを置き換えない。単にVahren.exeを直接起動した場合はこの拡張は自動接続されない。通常の起動用入口としてlauncherを使う。一括scriptの全体試験は未実施、同等の分割起動で実動作を確認済み。
重要: EXEファイルが原版でもDLL接続後のメモリは拡張状態である。解析の原作baselineは拡張なしの別セッション/原版静的証拠と区別する。DLLをpinしているためアンロードせず、拡張を外すにはゲームを終了する。境界4分類・雇用後更新はまだ全ケース未検証。
