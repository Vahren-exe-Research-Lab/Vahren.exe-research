# 研究知識ベース同期状態

- 作業ID: KB-SYNC-01-20261029
- 状態: **SYNCED / PRIVATE / DEVELOP CLEAN（最終のGitHub側とローカルのSHAを都度照合する）**
- 正本: https://github.com/ButaMonky/Hakushin067-Research-Knowledge （非公開）
- 正本ブランチ: `develop`。**現在の先端SHAは `git rev-parse HEAD` とGitHubの `git ls-remote origin refs/heads/develop` を必ず照合する。** 古いSHAを固定参照しない。
- **2026-10-29時点の履歴検証**: `work/kb-KB-SYNC-01-VERIFY` で `start` → `checkpoint` → `publish` 成功。private確認・GitHub側の同一SHA確認後、`git merge --ff-only` で正本に統合。現時点の最新GitHub先端と混同しない。
- Git管理対象: `tools/sync_knowledge.py` の許可リスト掲載原本＋生成SHA台帳。許可外はステージ/同期禁止。
- **2026-10-30当時の辞書履歴（最新値ではない）**: `symbols.tsv` は365件（旧363件＋領地名2件）、SHA-256 `C01924149029DC7AB062A3056E8C7DF00968B126ACE32059E67DE871F456A704`。旧363件のSHAは `6DE767D362CDAF354C30832E7CFAF82B17512661890C8F215FAF652CB627851F`。現在の辞書件数・SHAは現物から再計算する。
- Git管理から除外: 最新の全文索引DB（422.8MB）・旧DBバックアップ（506.4MB）、生成ラベル/目録、原作EXE・DAT・MAP・セーブ・ZIP、個人情報・トークン。
- 同期の形式: **必要なときに手動実行**。バックグラウンドで自動pushする仕組みではない。
- 作業ルール: `python -B tools/sync_knowledge.py status` → `start TASK_ID` → `checkpoint TASK_ID` → `publish`。担当別作業ブランチ、ff-only統合。force/reset/stash/rebase/amend禁止。
- 同期確認: `git status --short --branch`、`git rev-parse HEAD`、`git ls-remote --heads origin refs/heads/develop`、`gh repo view ButaMonky/Hakushin067-Research-Knowledge --json visibility`。
- 失敗/再開: `KB_SYNC_BLOCKED_20261029.md`、`SYNC_PROTOCOL.md`、ローカル `.git/kb-sync-journal.jsonl`。
- 生成DBの復元: 原作を扱う許可済PC上の研究ROOTにて `python -B knowledge/tools/build_kb.py`。GitHubには原作・V9実DBのバックアップはない。

## 新規クローンからの復元確認（2026-10-29）

- 検証対象のprivate developコミット: `96c9fce5a0645e0ee6c15f6a8ff2d240a0a9f322`。
- 新規Git cloneのHEADがGitHub・作業PCと一致。
- `SOURCE_MANIFEST.tsv` 記載の原本24ファイルのSHA-256およびバイト数が**24/24一致**。
- クローン内 `tools/sync_knowledge.py audit` PASS。
- 同期ガード単体試験 **8/8 PASS**、研究辞書・索引の単体試験 **5/5 PASS**。
- クローンのGit作業ツリーはクリーン。検証に使った一時クローンは処理後に削除を試行。
- 本文研究検索DBや原作EXE/V9等はGitHubに無い。完全な解析環境の再現には認可済み研究PCの別途保存データが必要。

## 2026-10-30 本番切替検証済み

- 作業ID KB-DB-PRODUCTION-20261030。knowledgeのGit作業ツリーをdevelopへff-onlyで更新し、旧ブランチ work/kb-location-name-20261030 のコミットは保存した。
- `symbols.tsv` 365件、source SHA256 C01924149029DC7AB062A3056E8C7DF00968B126ACE32059E67DE871F456A704。
- 新形式DBを普段使う generated/research.sqlite に導入。**導入直後の検証スナップショット**は422,760,448 bytes、SHA256 209720F7C635B5C38AAAE40329E5B6EF14EC81BF138D299D25BDF9881F6A11BA。本文更新により現行DBのハッシュは変わるため、確認時に Get-FileHash で再計算する。
- 元の旧DBは generated/research_backup_legacy_20261030.sqlite に506,351,616 bytes・SHA256 C4D0CD162B9150EC46BC445D3774E287DB3C8AE73211D3B86C3B6DCF91A45518 として保存済み。
- 機械可読記録は dev_lab/_work/kb_ghidra_validation_20261030/DB_MIGRATION_LOG_20261030.json。復旧手順は DB_OPTIMIZATION_REPORT_20261030.md。
- 正式切替直後の全文索引は1675資料、1081290行、138324アドレス参照。変更待ち0の時点を検証済み。以降は資料更新に従って増分更新される。
- Ghidra複製で領地名2件、その他7関数、戦闘終端を検証。x32dbgは隔離Notepadで1ラベルと1コメントの保存成功。
- Vahren.exeのライブデバッグへの全件インポートは未実行。ユーザーのゲーム実行を保護し、自動dbloadしない。
- GitHubのprivate developが唯一のソース正本。DBとゲーム原作の実体はGitHubには無い。
