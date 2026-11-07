> **2026-11-01?P0???????????** ?game_copy??????ZIP??????????Windows??????????????????????ZIP???DLL???????????ZIP????P0??????7?????DAT1????????????rea_lab/headless_analysis/search_index/P0_TAKEOVER_20261024_01/runtime/GAME_COPY_RECOVERY_DISCARDED_20261101.md?

> **2026-11-01 storage note:** Historical P0 takeover test runtime/game_copy is not currently installed. Its unique saves/script are in a small local ZIP. Full file-content recovery from the original distribution ZIP is verified. Do not run historical P0 hook scripts before reconstructing. See rea_lab/headless_analysis/search_index/P0_TAKEOVER_20261024_01/runtime/GAME_COPY_CLEANUP_COMPLETED_20261101.md. Regular player installation and startup_clean_20261025 were not changed.

# 迫真戦記 再開発 研究資料の地図（最初に読む）

2026-10-29 Claude 作成。研究資料がどこにあり、何から読めばよいかをまとめたもの。人と AI の両方向け。

## 今の目標

迫真戦記 ver0.67 で、教育・アイテム使用などのユニット選択をゲーム内で分かりやすくする機能と、それを載せる共通プラグインローダーを完成させる。新エンジン全体（戦闘の再実装など）は保留中。現在の作業状況は `dev_lab\docs\CHATGPT_CURRENT_HANDOFF.md` の冒頭を見る。

## 目的別の入口

| 知りたいこと | 見る場所 |
|---|---|
| **アドレス・構造体・DAT の挙動・UI の仕組み**（今わかっていること） | `knowledge\`（README.md から）。検索は `python -B knowledge\kb.py` |
| 関数の疑似コード、呼び出し元 | `python -B knowledge\kb.py func <アドレスか名前>`（統合 V9 に名前を重ねて表示） |
| Ghidra で見る | `rea_lab\headless_analysis\Hakushin067_ResidualCodeRepair_20261022`（標準のプロジェクト）。名前は `knowledge\tools\ApplyKnowledge.java` で付ける |
| x32dbg で見る | `knowledge\generated\x32dbg_labels.txt` をスクリプトタブで実行 |
| DAT から呼べる一覧選択（v4）の仕様 | `dev_lab\_work\claude_loader_patches_20261026\v4\DAT_UI_V4_SPEC.md` |
| 作業の現在地（Codex） | `dev_lab\docs\CHATGPT_CURRENT_HANDOFF.md` の冒頭、`dev_lab\docs\WORK_REQUEST_QUEUE.md` |
| **あるファイルが何か**、作業番号（T0xx）ごとの資料 | `knowledge\CATALOG.md`（目録）、`python -B knowledge\kb.py files <語>` |
| **研究報告の本文、アドレスの全出典、新規VA候補** | `python -B knowledge\kb.py research <語>`、`docs <VA>`、`pending`（詳細は `knowledge\README.md`） |
| **研究知識ベースのGitHub非公開正本・競合防止** | `knowledge\SYNC_PROTOCOL.md`、`knowledge\SYNC_STATUS.md`（GitHub: `ButaMonky/Hakushin067-Research-Knowledge`） |
| 調査の経緯・根拠（作業日誌） | `dev_lab\docs\PEER_SCRIPT01_FINDINGS_20261011.md`（Claude、§番号で参照）、`evidence\LANE_*_HANDOFF.md`、`MASTER_LEDGER.md` |

## フォルダの役割

| フォルダ | 中身 |
|---|---|
| `knowledge\` | **研究知識ベース**（事典、検索、Ghidra・x32dbg への反映） |
| `dev_lab\docs\` | 作業の記録（引継ぎ、依頼キュー、調査の日誌） |
| `dev_lab\_work\` | 作業用のビルド・ログ・試験用ファイル。診断用のゲームのコピー `startup_clean_20261025` もここ |
| `dev_lab\src\`、`dev_lab\tests\` | 新エンジン（Python）の再実装コードとテスト（保留中） |
| `data\recruit_sort_v4\` | DLL（プラグインローダー、雇用並べ替え、DAT 一覧選択）のソース |
| `rea_lab\headless_analysis\` | Ghidra の解析。`search_index\` に統合 V9 の索引（全関数の疑似コード・参照） |
| `rea_lab\targets\` | 解析用の原作 EXE のコピー（SHA-256 E8DAC301…767187） |
| `evidence\` | 初期の 5 レーン研究の引継ぎと、作業番号（T005〜T033）ごとの証拠 |
| `wiki\`、`exp_research_20261021\`、`exe\` | 戦闘・経験値・DAT の個別調査（2026-10-11〜22、戦闘の作業は保留中） |
| `MASTER_LEDGER.md` | 初期の研究台帳（作業日誌） |

## 守ること

- 原作の EXE・DAT・MAP・ZIP・セーブは読み取り専用。試験は診断用コピーで行う。
- 新しく分かったことは、作業日誌に加えて `knowledge\` の事典も書き直す（README.md の手順）。
- 古い解析版（Ghidra の中間プロジェクト、V1〜V7 の索引など）は 2026-10-29 に整理した。記録は `rea_lab\headless_analysis\CLEANUP_20261029.log`。
