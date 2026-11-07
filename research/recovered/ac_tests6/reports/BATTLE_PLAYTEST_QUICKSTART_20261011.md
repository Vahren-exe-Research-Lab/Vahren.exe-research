# 迫真戦記 再開発 — 先行試遊EXE（2026-10-11）

## 目的と状態
- 既存の `HakushinBattle.exe`（151 MAP + F3原作宣言一覧）は変更しない。別起動 `HakushinPlaytest.exe` にて **原作MAP・原作PNGを使って選択・移動・攻撃ができる** 最初の遊べる vertical slice を作成。
- **オリジナルの戦闘を再現したエンジンではない。** 味方3体／敵4体の構成、座標、HP、攻撃、射程、移動速度、衝突未実装、敵AI、範囲技／回復、リロード、勝敗判定はこの先行体験のために新規作成した仮ルール。原作ベースラインや既存研究GOLDENへ適用しない。
- 元のヴァーレンEXEを起動／逆解析せず、原本DAT・MAP・PNG・セーブには一切書込しない。リソースは既存の完全解凍豪華版から **読取専用** で参照し、EXEの配布物へゲーム素材を複製して含めない。

## 今すぐ起動する
`[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab\dist\HakushinPlaytest\HakushinPlaytest.exe`

- ダブルクリックで試遊。Windows windowed版なので通常は端末表示なし。初回は原作画像マップから静的tile cacheを構築する。
- **同フォルダの `_internal` は必須。** EXEだけを別の場所へ移すと起動できない。原作完全解凍済み `a_default` の場所も維持する。
- デフォルト原本 `s1.map`。試作の3味方（TNOK, ICE, 槍兵）／4敵を中央近辺に配置する。原作シナリオでの勢力やunit参加条件・スポーン場所は模倣していない。
- 原作Map markerは実参加Unitではない。既存デバッグ画像とは別で、pygame上に実際の位置が更新されるユニットを描画する。

## 操作
| マウス/キー | 試作機能 |
|---|---|
| 左クリック | 味方1体を選択 |
| 右クリック（地面） | 選択中の味方に移動命令 |
| 右クリック（敵） | 敵を追撃・攻撃命令 |
| 1 または左下「範囲攻撃」 | 選択Unitの周囲の敵に試作AoE（クールダウン） |
| 2 または左下「回復」 | 選択Unitを試作量だけ回復 |
| Space または左下「停止」 | 一時停止／再開 |
| F5/F6/F7 または上部「普通/中速/高速」 | 速度1倍／2倍／4倍 |
| TAB | 生存中の次の味方を選択 |
| R または左下「やり直し」 | 戦闘を初期化・再挑戦 |
| WASD / 矢印 / 中ボタンドラッグ | カメラ移動 |
| マウスホイール、+／- | カメラ拡大縮小 |
| G | デバッググリッド切替 |
| F8 | 現在の試遊画面をdev_lab/reportsへPNG保存 |
| Esc / ウィンドウの× | 終了 |

## Wiki画像の参照状況
- ユーザー指定：新約迫真戦記Wiki「マリナーズ傭兵団 Ver.0.57 アナル地獄 レザマリ縛りプレイ」。ページは旧バージョン0.57で、再開発対象は同梱0.67。**参考は表示・操作UIに限定**、当時の技能・能力値を現行の一次仕様にはしない。
- 公開記事HTMLから画像タグ77件、画像ファイル参照60件を確認。代表画像4枚を閲覧。世界戦略地図には地域・拠点アイコン・接続線と編成一覧のダークUI。原作戦闘画像には多数の小チップ、HPバーとダメージ文字、右上のUnit能力欄、左下の命令パレット、上の停止／速度操作。
- 今回の試遊では、**右の能力情報・味方敵HPバー・左下の命令パレット・上部速度切替**を参考に配置。素材／ルール1対1再現やWikiのスクリーンショット画素一致はまだしていない。
- 公開Wiki写真はダウンロードしてGitに登録せず、画像鑑賞用途のみ。追加されたコードは元の原作アセットだけをローカル参照する。

## 独立実装ファイルと所有権
- 新：`playtest_launcher.py`（PyInstallerの新entry）。
- 新：`src/hakushin_compat/playtest_rules.py`（1/30秒固定更新、攻撃、追撃、再生速度とは分離した仮ルール）。
- 新：`src/hakushin_compat/playtest_game.py`（pygame窓、キャッシュ付きMAP描画、原作PNGの移動sprite、情報欄/クリック、画面保存）。
- 新：`tests/test_playtest_rules.py` と `tests/test_playtest_game.py`。既存 `battle_window.py` は**read-onlyで呼ぶだけ**、別AIの変更を上書きしない。
- `dist/HakushinPlaytest/` にPyInstaller onedir/windowedバイナリを独立build。既存 `dist/HakushinBattle` には一切上書きしない。
- 研究A〜E専属MASTER/REA/元EXE、Claudeのparser、他AIのF3/manifest/loaderなどは非編集。Git commit/push/公開は同時作業のため保留。

## 検証と完成判定
- 旧EXE Gameplay Golden actual **0**、新native strict MATCH **0** は維持。別モードでの **PLAYTEST動作**はゲーム互換テストには加算しない。
- 旧元データを書き換えず、smokeが原MAP110x110/試作7 actorを検査。GUI headlessで原画像合成／Unit draw／5tick／PNG出力を実施。
- さらに画面の左クリック選択・右クリック移動/追撃、テスト範囲/回復、ポーズ、速度UI、勝敗と更新の決定性をpytestではなく標準unittestで検査。
- **未実装**：地形衝突／川・壁の通行、原作のUnit/Skill実ステータス、原作mob roster、隊列複数選択、オリジナル戦闘CPU、元script event、MP、アニメーション、勝敗原規則、セーブ継続。BF-03/06/07の試作下地であり、原作BG2〜BG6のDONE認定には当たらない。

## 次の実装優先順
1. Playtestの移動選択を基に、当たり判定・経路探索・部隊複数選択・攻撃move命令を増やす。原作当たり判定が未確認なら trial モードとstrictモードで分離。
2. 原作 `unit/class/skill` の定義合成と保存実セーブUnit参照をしっかり接続し、原作選択Unitの能力表示・戦闘初期化へ移行。
3. 戦闘で正しいSkill/ダメージ/状態/RNGの検証済断片を段階統合し、旧EXEで目に見えるゴールデンと比較。1v1原作実機の戦闘が厳密再現できるまで完成とは呼ばない。
4. 地形の紫（stairN等）は原作画像のレンダリング仕様未解析による未解決であり、Wikiを見ただけで適当な画像へ置換しない。

## 完成EXEの最終確認結果
- Windows版 `dist/HakushinPlaytest/HakushinPlaytest.exe`：PyInstaller 6.22.3 onedir/windowed。最終 **FINAL_BUILD_EXIT=0**。
- 完成EXE size **5,400,312 bytes**、SHA256 **99854C1D93B6AB20B1739A27120F264FDE149599ABD3BEB4DC8F06A2850A9D76**（exe本体のみ。実行には同梱 _internal も必要）。
- Windowsアプリを `Start-Process -Wait -PassThru` で呼び、SDL dummy環境で `--stage s1.map --gui-smoke --screenshot reports/battle_playtest_final_exe.png` が **EXIT 0**。原作PNG・ステージを表示した1120ではなく**1200x780**の画面をPNG証拠として保存。
- 同じ完成EXEを `--stage sfight.map --smoke` で起動して **EXIT 0**。旧本体Vahren.exe呼出0。
- 新規独立test_playtest_rules 16件 + test_playtest_game 10件＝ **26/26 PASS**。最終結合 `Ran 26 tests in 5.446s / OK / FINAL_26_TESTS_EXIT=0`。
- GUIの普通/中速/高速と試作命令ボタンはWindows SDL dummyで描画・静的ボタンhit検証済。ただしユーザー自身の実Windowでマウス操作・ゲームplay終了の目視はまだNOT RUN。
- 全研究A〜E・原本・既存GUI・GitHub remote・automationに手を加えず、Git commit/stage/pushなし。Git main HEAD b49c678。原作互換パーセントやstrict MATCHを上げない。
