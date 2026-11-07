# 迫真戦記研究知識ベース ①②⑤ 実装記録（2026-10-29）

作業ID: KB-WORKFLOW-125-20261029
状態: IMPLEMENTED / LOCAL VALIDATION / NO ORIGINAL GAME EDITS
範囲: ①研究報告の全文検索、②symbols.tsv品質検査、⑤未登録アドレス候補の自動生成。
全て通常チャットと認可済みのローカルPC作業で実装。GitHubへのpushは実施していない。

## 新機能と担当ファイル

- `knowledge/tools/research_index.py`：研究報告書の本文をSQLite/FTS5で索引する。指定の研究フォルダと手書きknowledge文書のテキストのみを走査する。SHA-256で新規・変更・削除を認識し、再実行しても同じファイルは再解析しない。
- `knowledge/generated/research.sqlite`：本文の出典ファイル・行番号・節、VAの言及、統合V9の関数先頭への正規化結果。`knowledge/generated/kb.sqlite` とは独立。
- `knowledge/kb.py`：`research`（本文全文）、`docs <VA>`・`addr <VA>`（全研究索引の参照行を併記）、`pending`（VA候補上位）を追加。
- `knowledge/tools/check_symbols.py`：6列、VA・名前の重複、許可kind/confidence、summary/source非空、コードとデータの範囲、V9関数先頭/所有範囲などを検査。`--compare` で過去辞書と比較して確度の引上げを警告。
- `knowledge/tools/build_kb.py`：従来の `--check` とビルドに辞書品質検査を組込み。通常ビルドに研究本文索引の増分更新・候補更新を接続。正常ビルド時には `generated/symbols_last_validated.tsv` を機械的に保存する。
- `knowledge/generated/address_candidates.tsv`：未登録の正規化アドレスを言及数と資料数で並べた提案（上位2,500行）。**自動登録・機能断定・確度引上げはしない**。
- `knowledge/generated/address_candidates_recent.tsv`：今回新規・更新された資料内の未登録VAを**出現回数が1件でも**別途全件抽出する。`kb.py pending --recent` で確認。更新資料なしなら前回の増分候補を維持する。
- `knowledge/tools/test_kb_workflow.py`：正常・不正・変更検知・削除検知・未検証VA保護等を一時フォルダだけで試す回帰テスト。
- `00_START_HERE.md`、`knowledge/README.md`：今後のAI向け入口・利用手順を追記。

## 完成時点の取得範囲

- 本文索引: 1,650資料、約108万行、約13.8万件のVA参照を索引化。
- メタデータ目録: 約2,524ファイル。これは全文索引より大きいが、全文索引はMD/TXT/JSON/JSONL/CSV/TSV等3MB以下のみ。バイナリ、ゲーム原作ファイルと旧履歴を除外している。
- `symbols.tsv`：363件（既存124+前回追加239）。今回、辞書の値・名前・確度は一切編集していない。
- 新規候補: 上位2,500行を生成。元VA・関数先頭正規化先・代表資料・行番号を保持。報告に単なる言及があることは、その関数の役割の確定を意味しない。

## 再現コマンド（研究ROOTで実行）

```powershell
python -B knowledge\kb.py research 経験値 --task T011 --limit 15
python -B knowledge\kb.py research 0x54E7B0 --folder data
python -B knowledge\kb.py docs 0x54E7B0 --limit 20
python -B knowledge\kb.py pending --limit 50
python -B knowledge\kb.py pending --recent --limit 50
python -B knowledge\tools\check_symbols.py
python -B knowledge\tools\check_symbols.py --compare knowledge\generated\symbols_last_validated.tsv
python -B knowledge\tools\research_index.py --check
python -B knowledge\tools\research_index.py
python -B knowledge\tools\test_kb_workflow.py
python -B knowledge\tools\build_kb.py --check
python -B knowledge\tools\build_kb.py
```

辞書の確度を過去承認版から上げた場合、自動ビルドは停止して人間に根拠確認を求める。確実に証拠を確認した場合のみ明示的に `--accept-confidence-change` を指定してスナップショットを更新できる。

## 安全境界と未検証項目

- 原作EXE・DAT・MAP・ZIP・セーブ、既存Ghidra解析DB/プロジェクト、MASTER_LEDGERは編集しない。
- 旧安全拒否範囲 `0x5710C0〜0x571500` の解析は実施しない。研究本文の既存記述は検索対象となるが候補への登録は除外する。
- 研究索引はテキストの出典・言及検出であり、機械語の新規解釈、実ゲームでの動作確認、Ghidra・x32dbg実機ラベル適用の成功を意味しない。
- 長い報告書や除外形式は検索対象外。FTS5の3文字未満の日本語検索は通常の文字列検索へフォールバックする。
- 複数AIによる同時編集や大規模なDB更新が発生した場合はファイル競合を再確認すること。保留/安全拒否を別経路から迂回しない。
- 初回本文索引生成ではDB約475MiBを使用した。容量を軽量化する最適化は今回の要件外であり、インデックスは生成スクリプトから再構築可能。
- 復旧記録（KB-WORKFLOW-125-RC01）：更新資料限定の候補一覧を追加した初回テストでSQLの列別名不足によるエラーが発生。作業対象は一時DBのみ。SQLの別名追加とSQLite接続の例外時クローズを修正し、回帰テスト5件が再実行で全件成功。元の辞書に変更なし。

## 検証

- 辞書：363件、エラー0、警告0。重複・欠落・確度変化の異常例は隔離テストで検出。
- 仮データでの全文索引：初回作成→変更検出→差分更新→削除反映を一時フォルダで試験。
- CLI：報告本文から日本語とVAの検索、docsとpendingの取得を確認。
- `build_kb.py --check` は書込なし。フルビルド後に元の辞書を再読してハッシュ不変、生成物と研究全文索引の連動を確認する。

