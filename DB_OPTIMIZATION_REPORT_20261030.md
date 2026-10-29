# 全文研究検索DBの軽量化・更新検証（2026-10-30）

作業ID: KB-DB-03-20261030
結果: LIVE DEPLOYED / LEGACY BACKUP VERIFIED / 研究正本ソース維持
初期試験は独立したコピーで行った。2026-10-30の正式切替では元DBを完全なハッシュ検証付きでバックアップし、最適化版へ切り替えた（末尾に記録）。

## 結果

| 測定 | 元DB | 最適化コピー |
|---|---:|---:|
| SQLiteファイルサイズ | 506,351,616 bytes | 415,801,344 bytes |
| 削減率 | - | 17.88% |
| 研究文書 | 1,664 | 1,664 |
| 本文行 | 1,080,581 | 1,080,581 |
| VA引用 | 138,082 | 138,082 |
| SQLite quick_check | 原本未変更 | ok |
| 更新テスト | 旧スキーマ | 新外部コンテンツトリガーPASS |

FTS5の本文二重保管を削り、既存 doc_lines を参照する外部コンテンツモードを採用した。
外部FTS5: content=doc_lines, content_rowid=id, tokenize=trigram, columnsize=0。
doc_linesへのINSERT・DELETE・UPDATEで索引を自動追従するトリガーを作成した。
詳しい手順は tools/optimize_research_db.py。入力のSHA-256は処理前後で変化しなかった。

## 代表検索の件数・中央値（4回の計測、ms）

| 検索句 | ヒット | 元DB | 最適化コピー |
|---|---:|---:|---:|
| 経験値 | 143 | 0.732 | 0.418 |
| 0x54E7B0 | 111 | 4.156 | 1.965 |
| GUI | 584 | 0.685 | 0.337 |
| Battle | 5,055 | 6.304 | 5.908 |
| 召喚（2文字、FTS直接） | 0 | 0.317 | 0.289 |

注: FTS5 trigramは2文字の検索句を直接処理しない。kb.py research は短い語を従来どおりinstrフォールバックで検索する。追加資料の索引に成功し、外部索引の更新後 check は変更待ち0件となった。

## 安全な展開手順

- 変換コードは元DBを読み取り専用で扱い、--output に指定した別パスにだけ作成する。既存パスがあれば停止する。
- 新しい research_index.py は legacy FTS5 と external-content FTS5 の両方を検出し、DBの形式に合う更新方法を選ぶ。
- build_kb.py は新しい順位表の再生成も行う。未登録アドレス候補は手書き辞書に自動追加しない。
- 最適化された完全コピーは知識ベースの独立した検証用クローンの generated/research.sqlite に保管中。
- 初期検証時は他AIの作業ブランチを保護するため置換を行わなかった。後日の正式切替結果は末尾を参照。
- 正本へコードをff-only統合後、他AIの追加2件も別の統合ブランチで照合し、元のローカルブランチを保全したままdevelopを更新してから切り替えた。
- GitHubに500MB級DBやゲーム原作は登録しない。研究ROOTの文書があれば新形式DBを再生成できる。
- 競合・安全拒否は迂回せず、日時・作業ID・未完了範囲と再開位置を記録する。

## 検証コマンド

python -B tools/optimize_research_db.py --source GENERATED_LEGACY --output NEW_OPTIMIZED
python -B tools/research_index.py --check
python -B tools/test_kb_workflow.py
python -B tools/build_kb.py --check

履歴注記: ここまでの記録は初期コピー検証段階のもの。最終の正式切替結果は文末を参照。
## 2026-10-30追記：新形式DBの独立運用

- knowledge_validation_20261030 は非公開developからの独立Gitクローンで、外部コンテンツFTS5形式の generated/research.sqlite を利用している。
- 2026-10-30再生成後のDB容量は423,120,896 bytes（403.5MiB）。旧DBは506,351,616 bytes（482.9MiB）。更新後も約16.4%の容量削減。
- 最新の辞書は365件。候補順位と全文索引が新形式DB上で動作し、検索コマンドと回帰テストを通過した。
- 研究ROOTの dev_lab/docs を他のAIが更新しているため、索引 --check が変更待ちを返す場合は異常と決めつけず、変更された報告の差分を確認する。
- この追記時点では元の knowledge の旧DBは未置換だった。現在はバックアップ付きで本番のDBを切り替えている（末尾を参照）。
- 元DBを切り替える場合は、現在作業ブランチの調整、更新済み研究インデクサの反映、旧DBのバックアップとSHA照合、再生成後の整合性確認が前提。
- GitHubには約400～500MiBのDB本体や原作EXE・DAT・セーブを追加しない。
## 正式切替完了（2026-10-30 JST）

- 作業ID：KB-DB-PRODUCTION-20261030。最初の独立検証（約506MB→416MB）を本番のknowledgeへ導入した。
- GitHub private develop SHA adc59bfebb9adc2b61a8f8565f2de3865ab83bec へff-only更新後に実施。旧作業ブランチ work/kb-location-name-20261030 のcommit 4f74996e1bfe33947d851dde9fa3c1acf691e260 は削除せず保存。
- 辞書は365件。統合前363件の値は維持し、実機照合済み領地名2件のみ追加。辞書SHA256 C01924149029DC7AB062A3056E8C7DF00968B126ACE32059E67DE871F456A704。
- 旧DBのSHA256 C4D0CD162B9150EC46BC445D3774E287DB3C8AE73211D3B86C3B6DCF91A45518 と件数を事前確認。
- 新DBの初期値415,801,344 bytes（17.88%削減）、SHA256 DAC01F6E6FEBC9F16F2B73653C77C8EB3A97A56563F0302751E46ABA061374B3。
- SQLite quick_check、文書1664件・本文行1080581件・VA言及138082件の一致、代表検索のヒット件数一致、INSERT/DELETEの更新トリガーを検証。
- バックアップをgenerated/research_backup_legacy_20261030.sqlite にバイト単位で複製し、SHAを再検証してから本体のみを単一ファイル置換。
- 旧DBバックアップは506,351,616 bytes・SHA256 C4D0CD162B9150EC46BC445D3774E287DB3C8AE73211D3B86C3B6DCF91A45518。削除禁止。
- 切替処理の機械可読ログ: dev_lab/_work/kb_ghidra_validation_20261030/DB_MIGRATION_LOG_20261030.json。
- 切替直後の検証スナップショットは422,760,448 bytes（旧比約16.5%削減）、SHA256 209720F7C635B5C38AAAE40329E5B6EF14EC81BF138D299D25BDF9881F6A11BA。**以後の研究報告の増分更新で現行DBのSHAは変わる**。最新値はその都度 Get-FileHash generated/research.sqlite で取得する。
- 切替後の検証スナップショット：研究資料1675件、本文行1081290件、VA言及138324件。research_index.py --check はその時点で変更待ち0件・削除待ち0件。件数は継続的に増減する。
- x32dbg用単独インポートDBは980ラベル/562コメント、オフライン出力・読戻し・構文検査PASS。ゲーム実機への一括インポートは保留（ゲームの継続稼働を優先）。
- Gitのdevelopは生成ファイルを追跡しないので、ファイルの再生成はGit作業ツリーに影響しない。
- 他AIが同じ資料を更新し続ける場合は --check の変更待ちを自然な差分として扱う。安全拒否・衝突を迂回しない。

### 復旧方法

- 読取・更新プロセスを停止し、バックアップのSHAが C4D0CD16...A45518 と一致することを確認する。
- 復元する場合は旧DBを別の一時ファイルへコピーしてSHAを再検証し、作業停止状態でgenerated/research.sqliteへ単一ファイル置換。バックアップ原本は残す。
- 復元後に実行するresearch_index.pyは旧legacy FTSにも対応する。安全な状態なら新DBを再生成することも可能。
- GitHubには旧DB・新DBの実体はアップロードしない。記録とソースコードのみ同期する。

