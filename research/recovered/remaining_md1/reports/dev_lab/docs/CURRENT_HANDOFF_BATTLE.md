# 最優先・迫真戦記再開発 引継ぎ（常にこのファイルを先に読む）

> **最新版（2026-10-11・WBS v1.7）:** 新EXEは151 MAP閲覧に加え **F3原作Unit/Class/Skill定義パネル** を実装・再build済み。BF-03の宣言読込部まで進捗。新28件＋既存48件＝76/76関連試験PASS、完成EXE4スモークexit0。詳細は本書末尾および BATTLE_DEFINITION_STAGE_20261011.md。実参加部隊、成長反映HP/MP、戦闘行動は未実装。下のv1.6記録は過去のチェックポイント。


更新日: 2026-10-11 JST / 対象: ユーザー向け **通常戦闘モード単独完成**。このファイルは同名で更新し、新たなフォルダやhandoffのコピーを無暗に増やさない。

## 新しいチャットで最初に実行するための指示文（そのまま転送可能）

「迫真戦記再開発を継続。PCのDesktop Commander **Local** のみ利用。原作本体はread-only、Remoteや安全拒否の迂回禁止。最初に
 \`[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\MASTER_LEDGER.md\` の最新checkpoint/TASK QUEUE、
 \`evidence\ANALYSIS_LANES_PROTOCOL.md\`、
 \`dev_lab\docs\CURRENT_HANDOFF_BATTLE.md\`、
 \`dev_lab\docs\DECOMP_TASK_LEDGER_20261011.md\`、
 \`dev_lab\docs\PROJECT_HANDOFF_MASTER_20261011.md\`
およびdev_lab Git status、他AIのファイル所有/作業中状態を確認する。原作の操作、戦闘、CPU、スキルの結果と見える体験を再現するが内部ABI/旧音声APIは一致不要。story/character/skillの原DATは改変せず読み込める互換層にする。戦闘画面の新EXEは既に完成した*静的マップビューア*の段階なので、ふたたびゼロから環境を作らず、そのソース/テストを拡張する。複数既存MAPを並べた参考スクリーンショット、F2選択、F8キャプチャ、任意の原作スクリーンショットとの比較機能を使い、表示差と未解明画像を特定する。次に実Unitの参加部隊/HP/MP/Skillの原script根拠あるロードと選択/移動を進める。**実Unit/戦闘AI/勝敗が完成済みとは宣言しない**。新しい成果・残件・テスト・Git変更を本handoff末尾とMASTER§次へ追記し、新チャットでも再開できるようにする。」

## 直近のユーザー確認・価値基準

- ユーザーは実PCで\`HakushinBattle.exe\` を起動し、**s1.map の草地・城・城壁・船・UI/黄マーカー・紫の未解決マス**が描画されたスクリーンショットを会話で送った。**初回のWindows実機GUI表示は成功と認定可能**（ただし WASD・ズーム等の個別操作結果はこの画像だけでは未確認）。
- 今回の新要望：「次も同じ/類似するチェックなら、既に存在する別マップを表示してどれくらい違うか見たい。次へ進みたい。チャット会話上限が近いので、いつでも引継げる詳細文書を作る」。
- ユーザーの「違い」には2種類ある。(1) **元データs1/s2/s4/sfight等の違うマップを新EXEで並べて表示**＝今回実装・生成。(2) **旧原作EXEの同じ戦闘画面との一致率**＝旧原作の同MAP・同領域・同拡大率の撮影画像が必要。今回送られたのは**新EXE**のスクリーンショットであり、旧原作画面との一致・原作実機golden証拠には加えない。
- 最優先は、原作と見える/感じる挙動が一致すること。旧DirectXやC++ ABI/旧音声再生経路まで同一にしなくてよい。ストーリー/キャラクター/スキルDATは手を加えず再利用。

## PC実際の構成と安全境界

\`\`\`text
[USER_HOME]\Documents\迫真戦記\
  新約迫真戦記―ほのぼの神話ver0.67 豪華版\
    Vahren.exe            (原作・実行/変更しない)
    a_default\stage\      (151個のMAP、直接READ ONLY参照)
    a_default\script\     (590 DAT、直接READ ONLY参照)
    a_default\chip\       (PNG)
    a_default\chip2\      (PNG)
    a_default\image\      (BMP atlas *.dat とメタデータ)
    a_default\bgm\sound\voice\  (保存したまま、今は読み込まない)
  _REDEV_RESEARCH\
    MASTER_LEDGER.md      (Eのみ所有・他のAIは読取のみ)
    evidence\ANALYSIS_LANES_PROTOCOL.md
    evidence\LANE_A_HANDOFF.md  (A script/VM/save 担当)
    evidence\LANE_B_HANDOFF.md  (B battle/skill/AI 担当)
    evidence\LANE_C_HANDOFF.md  (C strategy/economy 担当)
    evidence\LANE_D_HANDOFF.md  (D RTS/graphics/native input 担当)
    dev_lab\
      .git\                (ローカルのみ、branch main)
      battle_launcher.py
      src\hakushin_compat\battle_window.py
      src\hakushin_compat\battle_static_tiles.py
      src\hakushin_compat\battle_compare.py
      src\hakushin_compat\unpacked_game_assets.py
      tests\test_battle_window.py
      tests\test_battle_compare.py
      docs\CURRENT_HANDOFF_BATTLE.md
      docs\DECOMP_TASK_LEDGER_20261011.md
      docs\PROJECT_HANDOFF_MASTER_20261011.md
      docs\BATTLE_FIRST_EXE_RUN_20261011.md
      _work\.venv\        (pygame-ce 2.5.8, PyInstaller 6.22.3, Python3.12)
      dist\HakushinBattle\HakushinBattle.exe
      reports\             (検証PNG/JSON。Gitで除外)
\`\`\`

- \`dev_lab/src\`の既存Claude製 \`peer_script01_*\` やA〜E/REAの専用資料を**横取り編集しない**。DEVのGUIソース/docs/testsのみに変更を限定。
- GitHub remote = 0、push/公開なし。画像・BGM/SE/voice/zip/実savはGitに追加しない。コピーを作らず外部参照する。個人情報が無いというユーザー説明と外部公開の権利審査は別。
- Git mainベースコミット：初版 \`9218a02\` →引継ぎ等 \`6ddbc6c\`→独立新EXE静的ビュー \`de761bd\`。以後は必ず **現在の git log -1 と git status を読んでから**作業する。別AIのdirty/予約コードには触れず、Git indexを同時に編集しない。Python unittestを新規小分けで実行し、長い全件テストの反復は避ける。
- 元EXEの保存Ghidra pseudoが10,257関数あるが元のコンパイルできるC++ではない。正式E MASTER checkpoint83＝研究34件のDONE9/IN_PROGRESS21/VERIFY4、公式研究ID190（この件数は進捗率ではない）。REA重点対象39/48静的確認、ゲーム全体再現率ではない。元ゲーム合法UI gameplay golden 0、新engine厳密ゲーム動作 match 0を保持。

## 最新GUI・比較システムの実装

### 直前の安定版（実機確認済）

- \`dist\HakushinBattle\HakushinBattle.exe\`をWindowsで起動、\`s1.map\` 110×110／原MAP地形12100、装飾446、配置marker12を表示。
- 原作の \`image.dat/imagedata.dat\`から32x32地形、\`chip/*.png\`から城壁/船、\`field_01.dat\`の \`image=\`継承等から地形aliasを解決。原作sourceを無改変のまま読む。先行のGUI依存、map/atlas読取/画面dummy smoke・PyInstaller build PASS。
- 実機スクリーンショットで黄丸のMAP markerと未解決紫のマスが確認できる。ただし黄丸は軍勢の実Unitではない。戦闘演算0。
- 現在のrendererはterrain→sceneryを単純描画し、ゲーム内本来のdepth/色/高低差/スムージング/透過の完全性は未実証。紫は \`stairN/stairoff\` などソースに \`image\`が無いfieldで起き、原作の姿を予想して塗替えない。

### 今回新しく作成・試験中の拡張

- 既存 \`battle_window.py\` に \`available_stage_names\` で**実stageの151件**をnatural sort、\`filter_stage_names\`で検索を追加。\`StaticBattleScene.load(name,assets,catalog=shared)\`で毎回巨大atlas/field全部をdecodeし直さず舞台を変更可能。
- GUI：**F2**＝MAP一覧・検索（入力して絞込み、↑↓移動、Enter決定、Esc閉じる）。**PageUp/PageDownまたはP/N**＝前後のMAP、**F8**＝表示中の領域をPNGと撮影設定JSONへ保存（\`dev_lab/reports\`）。WASD/矢印＝カメラ、ホイールと+/-＝zoom、右ドラッグ＝スクロール、G＝格子、M＝黄マーカー、左クリック＝cell名、Esc＝終了。
- \`battle_compare.py\` は複数の元MAPを同一新レンダラーで表示するコンタクトシートと証拠JSONを作る。既存原作画像を直接使用、**異なるMAPどうしの外見の差**であり、元EXEの描画忠実度を示さない。
- 生成物 \`reports/battle_map_4stage_comparison.png\`（s1/s2/s4/sfight）と \`reports/battle_map_special_comparison.png\`（s1/s2/sdrama/tutorial）。それぞれのJSONには原MAP SHA、解像度、未解決ラベル、原作EXEと比較していない旨を記載。Gitでは無視。
- 将来**原作側のスクリーンショットが届いたら** \`python -m hakushin_compat.battle_compare --reference ORIGINAL_SCREEN.png --stage s1.map --crop X Y W H --origin ORIGIN_X ORIGIN_Y --zoom 32 --output reports/compare_s1.png\` で「提供画像/新静的renderer/pixel difference」の3枚とJSONを作れる。原本スクショか/画面範囲が一致したかはフラグfalseにしており、**数値を原作一致率だと言い換えない**。ユニット・アニメ・高低差の揺れに注意。
- CLI個別MAPスモークは \`battle_launcher.py --stage s2.map --smoke\`、GUIは \`battle_launcher.py --stage s2.map\`。Windows版はdist/HakushinBattle/HakushinBattle.exe。

## 実装・ビルド・検証（必ずexit codeを確認）

PowerShell：
\`\`\`powershell
$dev = "$HOME\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab"
Set-Location $dev
git status --short
$env:PYTHONPATH = Join-Path $dev "src"
$env:PYTHONDONTWRITEBYTECODE = "1"
.\_work\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_battle_compare.py" -v
.\_work\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_battle_window.py" -v
.\_work\.venv\Scripts\python.exe -m hakushin_compat.battle_compare --stages "s1.map,s2.map,s4.map,sfight.map" --sheet reports\battle_map_4stage_comparison.png
.\_work\.venv\Scripts\python.exe -m hakushin_compat.battle_compare --stages "s1.map,s2.map,sdrama.map,tutorial.map" --sheet reports\battle_map_special_comparison.png
.\_work\.venv\Scripts\python.exe battle_launcher.py --stage s2.map --smoke
$env:SDL_VIDEODRIVER = "dummy"
$env:SDL_AUDIODRIVER = "dummy"
.\_work\.venv\Scripts\python.exe battle_launcher.py --stage s2.map --gui-smoke
Remove-Item Env:\SDL_VIDEODRIVER
Remove-Item Env:\SDL_AUDIODRIVER
# 再ビルド（status/並列AI予約確認後）
.\_work\.venv\Scripts\python.exe -m PyInstaller --noconfirm --onedir --console --name HakushinBattle --paths .\src --distpath .\dist --workpath .\_work\pyinstaller --specpath .\_work .\battle_launcher.py
.\dist\HakushinBattle\HakushinBattle.exe --smoke
# GUI自動終了時だけSDL_VIDEODRIVER=dummy。通常実機では設定しない！
\`\`\`

**注意:** Python環境内 \`PYTHONPATH\`はテスト時に必要。画像プレビューと新EXEは元ゲーム完全解凍版を参照する。既存original exeには触らない。GUIのボタン/ショートカットはユーザーの実機確認まで未検証として残す。

## 優先順位・未完了

1. **表示比較/ユーザー実機チェック:** 再ビルド済EXEを配布せずPCローカルで起動し、F2で \`s2.map/sfight.map/sdrama.map\`を開けるか、ズーム/スクロール、画像名や紫未解決部分を記録。ユーザーに旧原作 \`s1.map\`または\`s2.map\` の同位置のスクリーンショットを別途お願いする。モードやカメラが違う場合は厳密画素比較をしない。
2. **原本フィールド描画差分:** \`stairN/stairoff\`は \`field_01.dat\`で \`smooth=step\`, \`member=stair18/stairxx\`, \`alt=24\` を持ち直接 \`image\`なし。単なる半透明/地形色か暗黙チップかは未確定で紫を正常完成扱いしない。底面位置/透過/スタック順・edge/jointの原作表示との差を原作実機画面でチェック。任意仮実装を事実にしない。
3. **BF03/06/07: 本物の戦闘Unit解決:** map marker(例\`mag_defs/can_defs\`)と scenario/unit/class/skill継承・原作参加軍実体/HP/MPを区別。原script元ファイルは変更せず、既存Claude parser/VM＋B研究T011/012/013の成果に接続。原本側スクリーンショットが揃うまではFixtureの仮部隊が本物であると宣言しない。
4. **BF08以降:** 固定tick、移動、スキル処理、damage、CPU target、士気、勝敗/イベント。元ゲームの同条件golden(現時点0)に合格して初めて忠実再現と判断。従来の全10,257疑似Cを再逆解析すること自体が目標ではない。
5. **品質/安全:** 古い \`typed_damage_fragments\` に古い \`1-R\`誤式があり、新しい \`main_decomp_attack_expression\`の\`2-R\`を優先。初回Git \`.gitignore\`は数GBのimage/music/voice/game source/savなどを追跡除外。たとえユーザーが「個人情報無し」と言っていても外部GitHub公開は別途承認が要る。Codex追加消費はユーザーが節約希望、通常Local toolで進行。

## 本書の更新手順

- 既存の \`docs/CURRENT_HANDOFF_BATTLE.md\` を上書き更新（本書は最新版として維持）。
- 正式な過去経緯は \`docs/PROJECT_HANDOFF_MASTER_20261011.md\` へ**新節を追記**（既存履歴消去しない）。
- 現在のWBSは \`docs/DECOMP_TASK_LEDGER_20261011.md\` が唯一の状態正本。validatorを実行して根拠付きでDONE/PARTIAL変更。Game completion率と呼ばない。
- Gitのコミットを行ったらそのSHA、変更ファイル、実機確認範囲・元executableとの差分不明点を本書へ追記する。ユーザーが次の会話で「続けて」と言えば、本書を最初に読んで再開。

## 最新テスト・ビルド確定（2026-10-11／本節より上の暫定表現を更新）

- **WBS正本 v1.6**：82件= DONE9/PARTIAL39/READY2/WAIT32、validator exit0。ユーザーの実Windowsで旧バージョンs1 GUIが表示された証拠により BT-03/BF-04 DONE、BT-05/BF-05はPARTIAL。G0 PASS3/3。**新GUI F2切替・PageUp/Down・F8のユーザー目視はまだ未実施**。
- **新比較版のPyInstaller build exit0**。同一パス dist/HakushinBattle/HakushinBattle.exe に更新（約5.3MBのexe本体と同フォルダ _internal 等が必要）。exe --stage s2.map --smoke exit0、--stage sfight.map --smoke exit0、SDL dummy EXE --stage s2.map --gui-smoke exit0。実行時MAPを別フォルダへコピーしない。原作exe起動0。
- **試験実績:** test_battle_compare.py 10、test_battle_window.py 13、test_battle_stage_view_manifest.py 10、test_unpacked_game_assets.py 10、test_map_codec.py 3、test_image_codec.py 2＝計**48/48 PASS**。F2マップ検索から「s2」→Enterのイベント注入も成功。Python SDL dummyでs2/sfight両方 GUI smoke終了0。
- **見比べ画像:** dev_lab/reports/battle_map_4stage_comparison.png と battle_map_special_comparison.png、および同名 JSON を生成済。実原本MAPの新エンジン表示4分割で、原作EXEそのものの画面差分ではない。旧EXEの同マップ同位置画像は今後ユーザーから受け取る必要がある。3画面reference diffの関数はsynthetic equal-inputテストで差分ゼロを確認（これを元ゲーム互換goldenへ加算しない）。
- **将来の最短タスク:** まずユーザーによるF2/s2/sfightの新GUI操作結果の確認。次は元scriptの Unit/Class/Skill参照・構造体継承（A/Claude）とB戦闘計算を新Coreにつなぎ、BF03/06/07へ。空のmap marker12を即場面内の実ユニット12体と判断しない。原作ダメージCPU一致の実機証拠は0のまま。
- **Git:** 開始時HEADは de761bd (main)、新GUI比較ブランチは既存branch main上で作業。**必ず最初に git log -1/git status を再読して最新コミットを確認する**。A〜E/REA/他AI所有ソースは触らない。GitHub remote0。今後もこの同一ファイル CURRENT_HANDOFF_BATTLE.md を更新し、MASTERの新追記は§26で保存済み。

## Gitチェックポイント：新151マップ比較機能のコミット

- GUIのF2/PgUp/PgDn/F8、画面比較モジュール、テスト10件、引継ぎ更新は **feature commit 37f9ee1**（branch main）へローカル保存した。対象8ファイル、stage/compare/test/doc限定、GitHub remote0。前回旧版は de761bd。現在の最新HEADは引継ぎ開始時に必ず git log -1 で確認すること。
- 上記feature commit後の git status はクリーン。Python48/48と新EXE再build/smokeの成功証拠は本書前節およびMASTER§26。ユーザーが次に行うのは既存dist/HakushinBattle/HakushinBattle.exeのF2切替・PageUp/PageDownとF8保存の目視確認。


## 最新：F3原作定義パネルを独立EXEへ接続（WBS v1.7）

- **現EXE:** dist/HakushinBattle/HakushinBattle.exe（同名更新、同フォルダ _internal は必須）。F2の151 MAP選択は維持。F3で原作の宣言を読む独立パネルを開く。初回のみ元590 DATを再帰索引化、以後catalogを再利用する。
- **操作:** F3開く→Ctrl+Aで検索欄消去→unit:tnok / class:a001 / skill:m_wind_bad 等を入力→↑↓/クリックで選択。右欄ホイールまたはShift+↑↓で全項目、F8でPNG+宣言出典JSON、Esc/F3でマップに戻る。F3中はカメラ移動やF2マップ入力と競合しない。
- **宣言閲覧:** Unit4586、Class4080、Skill16554、Skillset106を構文索引化。選択対象のみ既存Claude native-order parserで解析。表示はname/image/宣言HP等と元DATのパス/行/親/ハッシュ。原作の実キャラクター画像をそのままread-only参照する。
- **未確定部分:** 同名unit:base/class:baseへの親参照が曖昧な場合は先へ進まず、既知の親連鎖だけを警告付きで表示。class=参照は表示するが能力合成はしない。skill/skill2のレベル付き配列も元tokensのまま。class:mag_defsはradius重複の扱い未確定でエラー表示。現在HP/MP・戦闘Unit数を捏造しない。
- **ファイル:** 新 src/hakushin_compat/battle_definitions.py と battle_definition_panel.py、変更 battle_window.py、新 tests/test_battle_definitions.py(16件)、test_battle_definition_panel.py(12件)。peer_script01_*には変更なし。
- **検証:** 新28＋既存48＝76/76 PASS（battle_definition_regression.log）。Windows PyInstaller再build exit0、完成EXEのs2 MAP smoke、unit:tnok定義smoke、s2/tnok GUI smoke、sfight/m_wind_bad GUI smokeの4件exit0。GUIはSDL dummy2frame検査で、ユーザー実WindowsのF3目視は未確認。
- **画像:** reports/battle_s2_definition_tnok.png と battle_sfight_definition_wind.png、元DAT出典レポートBATTLE_DEFINITION_CATALOG_20261011.json、逆コンパイル参照4関数レポートBATTLE_DEFINITION_NATIVE_DEPENDENCIES_20261011.json、build/hash/4スモークBATTLE_DEFINITION_RELEASE_20261011.json。
- **継続の最短手順:** parent優先順位・class=合成・levelとskill2の解釈を保存nativeのconsumerから確証→BF-03参加者fixtureでBattleUnit生成→BF-06マップ上の実部隊表示→BF-07選択・移動へ。F3は基礎データ確認画面であってBG2完成ではない。
- **WBS:** v1.7、82件 DONE9/PARTIAL40/READY2/WAIT31、BF-03 WAIT→PARTIAL、validatorエラー/警告0。G0だけ継続PASS、BG2未達。
- **並列注意:** 開始時main b49c678 clean→作業中に別AIがsaved_scene_state_api.py、native_saved_loader_bootstrap.py、関連test/docを変更。本GUI作業はそれらへ触れず、同時index編集を避けてコミットを保留。次のrunは必ずgit status/log/stagedを確認し、担当ファイルを明示して扱う。git add . は禁止。

現EXE SHA256: 853c28eaba515e540fea914cab0d38d935c7e4a44508dc2968352f9030f44660 / 5379938 bytes
