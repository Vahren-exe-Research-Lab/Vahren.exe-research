# 全文研究検索DBの軽量化・更新検証（2026-10-30）

作業ID: KB-DB-03-20261030
結果: OPTIMIZED COPY PASS / LEGACY ORIGINAL NOT REPLACED
変更したのは研究リポジトリの新しいPythonコードと隔離したコピーのみ。元の約506MB研究検索DBに対する破壊的処理は行っていない。

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
- 元の knowledge は別のAIが独立作業ブランチを使用していたため、生成DBの置換とソースの上書きは行わなかった。
- 今後、利用中の作業が終わり、正本にこのコードを統合してから、データ破損・別AIの稼働がないことを確認し、元DBの別途バックアップとSHA照合を行ったうえでコピーを切り替える。
- GitHubに500MB級DBやゲーム原作は登録しない。研究ROOTの文書があれば新形式DBを再生成できる。
- 競合・安全拒否は迂回せず、日時・作業ID・未完了範囲と再開位置を記録する。

## 検証コマンド

python -B tools/optimize_research_db.py --source GENERATED_LEGACY --output NEW_OPTIMIZED
python -B tools/research_index.py --check
python -B tools/test_kb_workflow.py
python -B tools/build_kb.py --check

CURRENT: この報告は元の研究PCの生成DBを勝手に差し替えたという意味ではない。
## 2026-10-30追記：新形式DBの独立運用

- knowledge_validation_20261030 は非公開developからの独立Gitクローンで、外部コンテンツFTS5形式の generated/research.sqlite を利用している。
- 2026-10-30再生成後のDB容量は423,120,896 bytes（403.5MiB）。旧DBは506,351,616 bytes（482.9MiB）。更新後も約16.4%の容量削減。
- 最新の辞書は365件。候補順位と全文索引が新形式DB上で動作し、検索コマンドと回帰テストを通過した。
- 研究ROOTの dev_lab/docs を他のAIが更新しているため、索引 --check が変更待ちを返す場合は異常と決めつけず、変更された報告の差分を確認する。
- 元の knowledge は別AIが独立作業ブランチを使っているため、そこにある旧DBは上書きしていない。
- 元DBを切り替える場合は、現在作業ブランチの調整、更新済み研究インデクサの反映、旧DBのバックアップとSHA照合、再生成後の整合性確認が前提。
- GitHubには約400～500MiBのDB本体や原作EXE・DAT・セーブを追加しない。
