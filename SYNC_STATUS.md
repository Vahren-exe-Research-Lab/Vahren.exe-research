# 研究知識ベース同期状態

- 作業ID: KB-SYNC-01-20261029
- 状態: **SYNCED / PRIVATE / DEVELOP CLEAN（最終のGitHub側とローカルのSHAを都度照合する）**
- 正本: https://github.com/ButaMonky/Hakushin067-Research-Knowledge （非公開）
- 正本ブランチ: `develop`。この状態更新の直前に確認したSHA: `abcc6a177b01c36d5be766e915a0d47854344c3f`。**この文書自体の更新でコミットSHAは変化するため、現在のSHAは下記コマンドで取得する。**
- 直近の検証: `work/kb-KB-SYNC-01-VERIFY` で `start` → `checkpoint` → `publish` 成功。private確認・GitHub側の同一SHA確認後、`git merge --ff-only` で正本に統合。
- Git管理対象: 原本24ファイル＋生成SHA台帳1ファイル。許可リスト以外はステージ/同期禁止。
- 辞書保護: `symbols.tsv` は363件、SHA-256 `6DE767D362CDAF354C30832E7CFAF82B17512661890C8F215FAF652CB627851F`。
- Git管理から除外: 約475MiBの全文索引DB、生成ラベル/目録、原作EXE・DAT・MAP・セーブ・ZIP、個人情報・トークン。
- 同期の形式: **必要なときに手動実行**。バックグラウンドで自動pushする仕組みではない。
- 作業ルール: `python -B tools/sync_knowledge.py status` → `start TASK_ID` → `checkpoint TASK_ID` → `publish`。担当別作業ブランチ、ff-only統合。force/reset/stash/rebase/amend禁止。
- 同期確認: `git status --short --branch`、`git rev-parse HEAD`、`git ls-remote --heads origin refs/heads/develop`、`gh repo view ButaMonky/Hakushin067-Research-Knowledge --json visibility`。
- 失敗/再開: `KB_SYNC_BLOCKED_20261029.md`、`SYNC_PROTOCOL.md`、ローカル `.git/kb-sync-journal.jsonl`。
- 生成DBの復元: 原作を扱う許可済PC上の研究ROOTにて `python -B knowledge/tools/build_kb.py`。GitHubには原作・V9実DBのバックアップはない。
