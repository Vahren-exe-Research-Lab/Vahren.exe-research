# ADR BT-01 — 戦闘専用の新エンジン・既存解凍素材の利用方針

**2026-10-11 / 初版。** 目的は原作ゲーム性・画面体験・スキル・CPUを再現する独立Windows EXE。原作EXEの内部構造・音声デコード方式は複製しない。

## 選定と理由

**採用する初期開発経路：Python 3.12 + pygame-ce（SDL2の2D描画）+ Pillow（画像メタ/変換用）。Windows配布はPyInstallerのonedir方式から始める。**

- 既存の93+ Python互換モジュール（DAT lexer/VM、map、画像メタ、数値・戦闘時計、AI限定モデル）がそのまま呼べる。C#/Godot移植を今開始すると既知コードの重複になり、戦闘画面の初回到達が遅れる。
- pygame-ceは画面・入力イベント・複数sprite・画像・将来の音声sinkを単一バックエンドで扱える。tile/atlasは1回デコードしてキャッシュ、描画は可視領域中心に更新。ゲームロジックの固定tickと画面FPS・音声を分離。
- **PCの現況:** Windows + Python 3.12、Pillow、tkinter、Gitは存在。pygame-ceとPyInstallerはまだ未導入。Windowsには.NET 8のruntimeはあるがSDKなし。新EXEビルドや実起動の証拠はまだ0件。
- **先行の代替案:** tkinter+Pillowは既存環境で簡易画面を作れるが、完成候補の多sprite描画・入力更新にはpygame-ceを優先。Godot4、C#/MonoGame、Rust/wgpuは大量Unitや可視領域描画の実測でPythonの限界が見えた場合のみ再評価。**早い段階で再評価するため、SimulationCore・AssetProvider・Renderer・InputAdapterを分離**。
- **日本語文字:** Windows OSのメイリオ/游ゴシック系フォントを `pygame.font.SysFont` で検索し、利用不可時は明示警告/代替選択にする。フォントファイルをGitや配布物へ無断コピーしない。
- **音声:** 戦闘完成初期ゲートは無音。将来のAudioSinkは `pygame.mixer` 等を検討し、描画・戦闘ロジックと分離。旧音声コーデック内部は移植しない。
- **Windowsビルド経路:** battle起動スクリプトができた後に `python -m pip install pygame-ce pyinstaller`、`python -m PyInstaller --onedir --windowed --name HakushinBattle <battle_launcher.py>` を実行する計画。現時点では依存ライブラリをインストールせず、新EXEが完成したとは言わない。
- この選定は**開発の最初の技術ADR（BT-01）の完了**を意味するだけであり、Windows EXEのビルド成功や戦闘再現性は意味しない。

## 実在する解凍済みゲームとデータ参照

ユーザー指定の既存解凍豪華版を読み取り専用の一次素材とする。

相対配置：

```text
迫真戦記/
  新約迫真戦記―ほのぼの神話ver0.67 豪華版/
    Vahren.exe                   ← 起動/変更/再配布しない
    a_default/
      stage/                     ← 151 MAP、16.4MiB
      script/                    ← 590 DAT、14.1MiB
      chip/                      ← 1,323 files、3.0MiB
      chip2/                     ← 1,147 files、2.4MiB
      image/                     ← 519 files、194.6MiB
      icon/                      ← 346 files、0.8MiB
      face/                      ← 2,458 files、37.2MiB
      picture/                   ← 1,265 files、240.9MiB
      bgm/                       ← 434 files、819.7MiB
      sound/                     ← 691 files、297.3MiB
      voice/                     ← 5,288 files、1,942.9MiB
  _REDEV_RESEARCH/
    dev_lab/
      .git/                      ← ソース履歴
      src/ ...                   ← 新エンジンコード
      docs/ ...                  ← 手順と研究handoff
```

ゲームを新設した開発用フォルダへ大量コピーしない。実ファイルの経路は `src/hakushin_compat/unpacked_game_assets.py` が探し、原作豪華版の `a_default/stage,script,chip,image,icon,face,picture,bgm,sound,voice` から**直接read-only**参照する。名称・資産key・chip atlas/PNG優先ルールは既存 `T007,T008,T015,T017` の証拠に基づき後で実装。

### 実装済みの素材参照境界

- `UnpackedGameAssets.discover()` は `_REDEV_RESEARCH` の親にある**完全解凍版**を探す。`HAKUSHIN_GAME_DIR` で明示パス指定可。研究用の画像/音声削除source_snapshotを誤認しない。
- `file("stage", "s1.map")` / `file("script","scenario1.dat")` / `file("chip", "13h.png")` などは**元フォルダの既存パスを返すだけ**。パス脱出・不正sectionを拒否する。`read_bytes()` は元データの純粋読み取り。
- `tests/test_unpacked_game_assets.py` の専用10件で解凍版の発見・map解読との接続・入力パス境界を確認する。音声/画像の描画はまだ行わない。
- 今後ゲームのパッケージだけ移動したい場合は環境変数・設定ファイルにゲーム素材の場所を指定させる。原本パスをWindows固有の絶対パスとしてソースコードに焼き込まない。

## Gitの安全な境界

- Git正本は `dev_lab/.git`（ゲーム本体・研究A〜Eの所有資料の外側）。履歴へは `README.md`, `src/`, `tests/`, `docs/`, `run_checks.ps1`, `recovered_source/` の**テキストのみ**を登録する。
- `.gitignore` は一時保存 `_work/`、生成分析結果 `reports/`、バックアップZIP、Pythonキャッシュ、配布EXE、コピーされた大量素材を履歴から除外する。**無視=削除ではない**。実際に使用する画像・音楽は全て元フォルダに残す。
- ユーザーは個人情報がないと明言。今回は個人情報の有無を理由とした任意のソース/文書削除はしない。ただし将来GitHubへ公開するときは権利・秘密情報の最終チェックを別途必須にする。
- GitHubリモート登録・push・releaseは実施しない。最初のローカルコミットはコードの復帰点。並列AIは各担当ファイルを自分のスコープで変更し、staging/commitを競合させない。

## 専用EXEに向けた次のマイルストーン

1. **BT-02 / BT-03:** pygame-ce / PyInstaller を導入し、新たな単体Windowsプロセスがウィンドウを開き、正常に閉じることを確認。OS側の設定や元ゲームEXEには触れない。
2. **BF-04 / BF-05:** 通常戦闘用 `s1.map` から原作 `.map` とfield/chip宣言を読んで、実際の地形・オブジェクト・背景画像を画面表示。ここで生成する画像は原作アセットを動的参照して表示し、偽物のチップ表示を原作再現完了と判定しない。
3. **BF-03 / BF-06 / BF-07:** scenario由来のUnit/Skill解決・HP/MP初期化・ユニットの可視選択・移動命令を接続。
4. **BF-08以降:** battle tickとCPU、ダメージ、Skill、イベント、勝敗を既存研究B/Claude成果で実装、原作実機Goldenで比較。
5. **性能検証:** 110×110 stage、カメラ移動、チップ描画、ユニット数別の描画FPS/論理tick遅延を計測。Pythonで足りないボトルネックだけキャッシュ、最適化、必要ならネイティブ化。

**注意:** 音声はユーザー体験上は残す選択肢だが、旧再生処理を復元する必要はない。通常戦闘が最初に動くまでは無音でもよい。原作メディアを第三者に配布する場合は、それぞれのライセンス・権利を確認する。

## 2026-10-11 BT-02実装結果（初版ADRの「未導入」状態を更新）

- `dev_lab/_work/.venv` に Python3.12の専用環境を作り、`pygame-ce==2.5.8` と `PyInstaller==6.22.3` を導入済み（元のWindows system Python環境を上書きしない）。
- `battle_launcher.py`、`src/hakushin_compat/battle_static_tiles.py`、`battle_window.py` が `s1.map` と原作atlas/chip画像を読み取り専用で描画する。field宣言の単純image名aliasだけ参照、nativeの描画順や物理衝突は未検証。
- `dist/HakushinBattle/HakushinBattle.exe` の PyInstaller onedirビルド exit0、exe `--smoke` exit0、SDL dummy GUI `--gui-smoke` exit0。スクリーンショット `reports/battle_s1_static_preview.png` も生成済み。
- **未完了:** 本物のWindowsデスクトップ上で表示した画面の実機目視・スクロール・原作との一致チェック。既知未解決 `stairN/stairoff` 2種の画像/ステップ表現。Unit/Skill/戦闘AI・結果計算は一切追加していない。
- 実機確認手順は `docs/BATTLE_FIRST_EXE_RUN_20261011.md`、公式状態は `DECOMP_TASK_LEDGER_20261011.md` v1.5を参照。
