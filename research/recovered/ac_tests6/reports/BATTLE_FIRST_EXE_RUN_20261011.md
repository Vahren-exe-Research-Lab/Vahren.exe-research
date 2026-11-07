# 初めての独立戦闘画面 — 新EXE起動と原作画像表示（2026-10-11）

**性質:** 初回のBattle-First GUI／STATIC STAGE VIEW。原作の戦場 `s1.map` と地形 `image.dat`、`chip/*.png`、static `field.image` aliasを直接使用する。スキル/HP/CPU/戦闘イベント/勝敗は**未実装**。原作EXEは実行しない。

## ユーザーの確認手順

PCで以下をダブルクリック：

`[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab\dist\HakushinBattle\HakushinBattle.exe`

- 新規Windowsウィンドウに原作の `s1.map` 地形・城壁・装飾などが出るはず。地形名由来で画像解決できない `stairN` と `stairoff` は検出用の紫で表示する（計10セル）。配置marker12件は仮の黄丸で示す。これは原作ユニット/戦闘中の陣営ではない。
- **カメラ移動:** WASDまたは矢印キー。
- **ズーム:** マウスホイール、+ / -。
- **右ドラッグ:** 戦場をスクロール。
- **左クリック:** そのマスの静的データ名を下欄に表示する。攻撃/移動命令にはならない。
- **G:** グリッド表示切替。**M:** 元マップ配置marker表示切替。**Esc:** 終了。
- 初期版はコンソールも表示される開発用ビルド（`--console`）。黒いコンソール画面はエラーログ観察用で、不要になれば次のUI検証後に非表示ビルドへ変更する。
- 正常終了・表示の確認、スクロール、マップの見た目、実際の画面が黒い/紫一色/落ちる等を報告してもらう。Windows本物画面の手動確認はまだ完了していない。
- EXE単体を別フォルダへ移さず、`dist\HakushinBattle\`の`_internal\`等と一緒に置く。原作豪華版も元の場所に残す。

## 既存解凍素材の読み込み

原作実データ（完全解凍豪華版）は、開発フォルダの外の同じ `迫真戦記` 配下に保存されたまま。exeはプロジェクト内から起動した時に自動発見する。別PC/別保存先では環境変数 `HAKUSHIN_GAME_DIR` に豪華版ゲームフォルダを指定する必要がある場合がある。画像・BGM・ボイスの数GBをEXEに同梱・Gitへ登録していない。

## ソース・起動確認

- `battle_launcher.py` — 一つだけの起動入口（旧EXEと無関係）。
- `src/hakushin_compat/battle_static_tiles.py` — original BMP atlas/image metadata/chip PNG/field.image alias読込。atlas画像のcolor-key一致を透明化。
- `src/hakushin_compat/battle_window.py` — 単純なterrain→scenery描画、仮marker、静的map閲覧GUI、Pillow screenshot、CLI smoke。
- `tests/test_battle_window.py` — 独立13件の表示/PNG/field alias/原ファイル不変更等の回帰。
- `reports/battle_s1_static_preview.png` — 元画像を使った静的スクリーンショット（Git管理しない）。
- Python3.12を使用。ライブラリ `pygame-ce 2.5.8` + `PyInstaller 6.22.3` を `dev_lab/_work/.venv` 内に導入し、システムPythonを上書きしない。

### 再実行可能なコマンド

```powershell
cd "$HOME\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab"
.\_work\.venv\Scripts\python.exe battle_launcher.py --smoke
.\_work\.venv\Scripts\python.exe battle_launcher.py --screenshot reports\battle_s1_static_preview.png
# Windows GUIは --gui-smoke で2フレームのみ自動終了可
.\_work\.venv\Scripts\python.exe -m unittest discover -s tests -p test_battle_window.py -v
```

### EXE作成の再現

```powershell
cd "$HOME\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab"
.\_work\.venv\Scripts\python.exe -m PyInstaller --noconfirm --onedir --console --name HakushinBattle --paths .\src --distpath .\dist --workpath .\_work\pyinstaller --specpath .\_work .\battle_launcher.py
```

## 観測済み検証（過剰な完成宣言を避ける）

- 原作 map `s1.map`: 110x110、terrain12100、scenery446、spawns markers12。原作の有効な地形宣言 `grass0` 等は `field_01.dat` で `image=grass` とされ、別名から原画像へ解決可能。特定できない `stairN/stairoff` の画像は現在未解明（型だけ検出）。
- 原作`image.dat`のatlasと`imagedata.dat`のmetadataを既存 `image_codec` で読み、PNGに依存せず実タイルを復元。atlas色キーのピクセル透過を適用。原作レンダラのlayer/anchor/アニメの厳密等価性は未検証。
- **実施済み:** 新GUI静的表示の独立テスト13/13 PASS、`--smoke` PASS、`--screenshot`でPNG生成、pygame-ce GUI dummy driverで2フレームとイベントループ正常終了、PyInstallerビルド exit0、パッケージEXEの `--smoke` exit0 と `--gui-smoke` exit0。元EXE稼働0。
- **未実施:** 実際のWindowsデスクトップの可視UI確認・ユーザーの操作確認・原作と同一画面/全sprite/全技能一致。原作Gameplay Golden PASS0、新実装のstrict behavior MATCH0。
- 新EXEの生成はBT-02の達成、GUIのSDL dummyによるウィンドウ閉鎖はBT-03のPARTIALまで。BF-04/05は原作静的画像描画ができたが実GUI・原作描画比較が未検証なのでPARTIAL。ユーザーが実機表示を確認したらgateを再評価する。

## 安全・並行作業

元ゲームファイル/EXE、各研究レーン(A〜E)/MASTER、Claude他AIの所有実装、GitHub、Remote、autotasksは触らない。`dev_lab`の新規ファイルだけを開発・Gitへ格納し、`dist/`と`_work/`及び報告PNGはローカルのGit除外に保持。他AIの最新branch/dirty所有を確認して競合せず、必要時だけタスク別に差分チェックする。


## 2026-10-11 第2版：新EXEを同じ場所のまま更新 — 151マップ比較

最初のEXEはユーザーのWindows実機でs1.mapを表示したスクリーンショットにより表示確認済み（タイトルバー「Hakushin Battle / Static Map Preview」）。原作スクリーンショットとの比較ではなく**新ゲームの初動表示成功**。

**再ビルド版GUIの新機能（再ビルド検証が済んでから利用）**

- **F2**：MAP選択一覧を開き、ファイル名の一部（例 \`s2\`, \`sfight\`, \`sdrama\`）を入力してフィルタ、↑↓で選択、Enterで切替。Escで一覧を閉じる。原作のstageファイル151件を直接列挙する。
- **PageDownまたはN**：次のMAP、**PageUpまたはP**：前のMAP。各ステージ読込のたびにアトラスBMP数MBを再解析しないよう共通画像カタログを再使用。
- **F8**：いま見ているMAP viewportを \`dev_lab/reports/battle_<stage>_<timestamp>.png\` に保存し、同名 \`.json\` に表示原点座標（カメラ位置）、ズーム、格子/marker/クリック座標を保存。**カメラとズームを旧ゲームスクショに合わせる時のための記録**である。
- 従来の移動(WASD/矢印、右ドラッグ)、ズーム(マウスホイール、+/-)、M(黄マーカー)、G(格子)、左クリック(静的map cell名)、Esc(アプリ終了)も継続する。

**手元のMAP比較画像（ユーザーの原作ファイルから生成した新エンジンの描画）：**

\`\`\`text
dev_lab\reports\battle_map_4stage_comparison.png
    s1.map / s2.map / s4.map / sfight.map の4分割。
dev_lab\reports\battle_map_special_comparison.png
    s1.map / s2.map / sdrama.map / tutorial.map の4分割。
\`\`\`

隣接する同名 .jsonには各mapの原本SHA、表示画素数と未知sprite名が入る。比較画像は**すべて新エンジン描画**であり、原作EXEの画面はまだ1枚も直接比較していない。原作EXEと数値で比較したい場合は、ユーザーが同じマップの旧ゲーム画面スクリーンショットを提供し、カメラ/座標/ズーム/クロップ領域を合わせてから \`battle_compare.py\`で3画面差分を作る。違う領域、ユニットのアニメーション、旧UIを含んだ差を原作描画バグとして断定しない。

コード／ツール:

\`\`\`powershell
$dev = "$HOME\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab"
Set-Location $dev
$env:PYTHONPATH=Join-Path $dev "src"
.\_work\.venv\Scripts\python.exe -m hakushin_compat.battle_compare --stages "s1.map,s2.map,s4.map,sfight.map" --sheet reports\battle_map_4stage_comparison.png

# ORIGINAL.pngは、旧原作EXEで撮影した同じstage・同じカメラ/拡大率のスクリーンショット。
# --crop X Y W H でゲーム画面領域だけ切り出し、--originでMAP座標を一致させる。
.\_work\.venv\Scripts\python.exe -m hakushin_compat.battle_compare --reference "ORIGINAL.png" --stage "s2.map" --crop 0 0 1024 704 --origin 37 38 --zoom 32 --output reports\compare_s2.png
\`\`\`

\`--crop\`や\`--origin\`の数値は単なる例であり、実際のスクリーンショットに合わせて定める。任意の画像でも生のpixel differenceは計算できるが、原作比較の適格性は自動保証されない。

**既存技術的未解決:** \`stairN/stairoff\`等のfieldは原シナリオで\`smooth=step\`、\`member\`、\`alt\`を指定する一方、直接の\`image\`指定がない。単純画像解決器はそれを紫の欠落セルとして表示する。\`tutorial.map\`は目的の異なる特殊MAPで、スクリーンショットの紫色が大きく現れる。この静的レンダリングは原作描画を完全コピーしている証拠ではない。原作のstep/smooth/色と地形chip合成規則を別途確認する。

**次の機能段階:** mapマーカーが実Unitという意味ではない。Unit/Skill/classの原scriptとbattle fixtureを結んでHP/MP、位置、方向、選択、移動/攻撃命令へ進む。原作CPU/skill/damage/士気/勝敗はまだ未実装。
