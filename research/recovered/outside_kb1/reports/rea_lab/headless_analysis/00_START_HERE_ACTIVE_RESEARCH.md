# 【最初に読む】迫真戦記 ver0.67 Ghidra 解析（2026-10-29 更新 / Claude）

**現行版は統合 V9 です。** 以前の V3 を現行とする案内は、2026-10-29 の整理で古くなりました。

## 使うもの

| 用途 | 場所 |
|---|---|
| 関数の検索・疑似コード・呼び出し元（研究で分かった名前つき） | `..\..\knowledge\kb.py`（例: `python -B knowledge\kb.py func 0x55BC60`） |
| 関数の検索（V9 の元の CLI） | `search_index\search_unified_v9_20261023.py`（例: `... function 0x004A1250`） |
| 索引の本体 | `search_index\HAKUSHIN067_UNIFIED_V9_20261023.sqlite`（関数 11,950、参照 243,678、全関数の疑似コード） |
| V9 の再検証 | `search_index\build_unified_v9_20261023.py verify`（V8 の DB と V7 の jsonl 4 つを使う。消さない） |
| V9 の説明 | `search_index\00_START_HERE_UNIFIED_V9_20261023.md`（「PC の既定は V3」という記述は 10-23 時点のもの） |
| Ghidra で見る | `Hakushin067_ResidualCodeRepair_20261022`（V8 までの修復をすべて含む標準のプロジェクト。V9 で追加された atexit 関数 35 個は含まない） |
| 名前・構造体を Ghidra に付ける | `..\..\knowledge\tools\ApplyKnowledge.java`（使い方は `..\..\knowledge\README.md`） |

## 2026-10-29 の整理

- 古い Ghidra プロジェクト（Index、ABI_Fixed、FunctionRepair、EHRepair、InitAtexitRepair、PEGapRepair、TailTransferRepair、AtexitTailRepair）、V1〜V7 の索引 DB、古い配布パック、古い疑似コード（full_pseudoc_20261020）はごみ箱へ送った（ユーザーの許可による）。
- 小さな記録ファイル（ログ・スクリプト・古い案内）は `_history_20261029\` に移した。
- 記録: `CLEANUP_20261029.log`

**静的な確認 ≠ ゲームでの確認。** 疑似コードは元のソースではない。
