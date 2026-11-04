# 戦闘参加データの接続・実装記録（2026-10-11）

## 目的と既存設計
- CURRENT_HANDOFF_BATTLE の BF-03 / DA-03 / DA-04を継続する。通常戦闘を優先し、セーブの内部ABI再現や新しい別エンジンの作成へ戻らない。
- 開始時Git HEAD b49c678、main、status clean、remoteなし。既存 battle_window / tile renderer / Claude parserを利用。
- 原作590 DATは下位フォルダを含む。直下globだけでは19 DATとなるため必ず再帰読込し、元ファイルSHAと宣言位置を保持する。
- 原作Unit/Class/Skillの定義を索引化し、既存native parserで選択した宣言だけを解析する。親Unit/Class跨ぎを扱うが複数候補・循環・欠落は推測で補完しない。
- 表示するHP/MP等は宣言上の値。レベル補正・クラス合成・技能のレベル付き配列・原作実戦闘の現在HPを同一視しない。
- 既存GUIにF3の読取専用定義パネルを接続する。マップmarkerを実参加部隊と呼ばず、元DATを変更しない。

## 実装順
1. 新catalogのテストを先行実行して失敗を確認→最小実装→実590 DATで照合。
2. 元画像/名称/パラメータ/技能宣言の情報パネルを実装、F3開閉・検索・選択をテスト。
3. 関連回帰、SDL dummy、EXEビルドとスモーク、画像とJSON保存。
4. WBS/一枚handoff/履歴を更新。未確定の合成・成長・移動・戦闘CPUは未完のまま残す。

## 判定
- 本工程はBF-03/BF-06の一部。戦闘参加者の自動確定、命令/移動、勝敗、原作実機との同条件一致は完了条件に含めない。
- 追加逆解析は既存全関数疑似Cとnative資料に不足がある範囲のみ。既往の安全拒否操作は再試行・迂回しない。
- 専用worktree/新フォルダを増やさない既存方針を維持し、他AI所有コードには書込しない。

## 実装・確認結果
- 再帰で原作590 DATを読み取り、Unit4,586/Class4,080/Skill16,554/Skillset106の構文宣言を索引化した。元ファイルのSHA256を全590件、作業後に照合して不変を確認。件数は実際の戦闘参加Unit数ではない。
- battle_definitions.pyが選択宣言だけを既存Claude native-order parserへ渡す。値ごとに元DAT相対パス・行番号・SHA・親宣言を保持。親候補が一意な範囲のみ解決する。複数候補・循環・欠損・重複field・未対応構文は明示し、class=の合成や成長・実HP/MPは推定しない。
- 原作には unit:base と class:base が別ファイルに存在する。unit:tnok→unit:base2→unit:base1の次のbaseは曖昧。F3閲覧は「既知の親連鎖の部分表示」と警告し、未読親の値を補完しない。シナリオvariant指定を伴う部分解決は優先順位を確定できず拒否する。
- class:mag_defsは祖先class:defbaseのradius重複により未解決。黄色map markerをそのまま有効戦闘Unitへ変換しない。
- battle_definition_panel.pyを既存battle_window.pyに接続。F3で原作IDを検索、Ctrl+A消去、↑↓またはクリックで選択。右側ホイール/Shift+↑↓で宣言値と根拠をスクロール。Esc/F3で元MAPへ戻り、F8で宣言メタ付き画像を保存する。カメラ入力はモーダル中停止し、F2マップ閲覧と同時に開かない。
- 元chip PNGの単一候補だけを表示。TNOKはchip/tnok.png(48x32)。クラス画像への自動fallbackやchip/chip2優先の推定は行わない。表示HP28930はunit:tnokの宣言値であり原作レベル5戦闘中の現在HPではない。
- GUI表示に長い文字列があっても省略処理を二分探索にし、原作image/sourceへの書込はしない。
- TDDで新catalog、部分継承、variant安全性、UI、F8、detail scroll、クリック選択を先に失敗させた後で実装。新規28件＋既存関連48件＝76/76 PASS（16.704s）。ログ reports/battle_definition_regression.log。全プロジェクト一括試験は未実行。
- 既存PyInstaller onedirへ再build成功（28.84s）。完成EXEのs2 MAP smoke、tnok定義smoke、s2/tnok GUI smoke、sfight/m_wind_bad GUI smokeの4件がすべてexit0。GUI自動試験はSDL dummy2framesであり、今回のF3をユーザーが目視した証明ではない。
- reports/battle_s2_definition_tnok.png と battle_sfight_definition_wind.png(各1120x696)を生成し、親連鎖と項目ラベルの重なりを修正後に再描画確認。いずれも新EXE側の見た目であり原作EXE比較画像ではない。
- reports/BATTLE_DEFINITION_CATALOG_20261011.json、BATTLE_DEFINITION_NATIVE_DEPENDENCIES_20261011.json、BATTLE_DEFINITION_RELEASE_20261011.jsonに出典・検証・バイナリhashを保存。
- 保存済逆コンパイル4関数（0x504400、0x505210、0x507730、0x50D650）の呼出依存を再照合した。元10,257関数ZIPの再生成や新規decompilerプロセスは行っていない。未確定のUnit/Class優先順位とkeyword合成は次の限定解析対象。

## 既存作業との分離
- 開始時main b49c678はcleanだったが、途中で別AIのsaved_scene_state_api.py、native_saved_loader_bootstrap.py、関連test/docが更新された。この作業では触れていない。
- 同時Git index編集を避け、このターンのコミット・公開は行わない。build/source/testをPCへ保存し、次の担当がgit status/HEADを確認して担当pathだけをコミットする。
- BF-03は宣言読込部分ができたためPARTIAL。BF-06/07の実参加Unit描画・命令・移動やBG2完成とは判定しない。

## 次の限定タスク
1. 保存nativeのparent registryとフィールドconsumerからUnit/Classの優先順位、class=合成、level/skill2の配列解釈を確認し、曖昧な表示警告を根拠付きで解消。
2. BF-03: 手動で明示した参加者fixtureと原作由来参加データを区別して実BattleUnitを生成。最大HP/MPの初期化を原作式に接続。
3. BF-06/07: 原マップへ部隊チップを配置し、選択/停止/移動へ。MAP markerは参加部隊の代替にしない。

EXE SHA256: 853c28eaba515e540fea914cab0d38d935c7e4a44508dc2968352f9030f44660 / 5379938 bytes
