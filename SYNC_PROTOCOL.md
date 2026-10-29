# 研究知識ベースの正本・競合防止（KB-SYNC-01）

対象は `_REDEV_RESEARCH/knowledge` のみ。研究ROOT全体、原作EXE・DAT・MAP・SAVE・ZIPはGit管理しない。
予定正本: 非公開 `ButaMonky/Hakushin067-Research-Knowledge` の `develop`。存在とPRIVATE設定を確認してから同期する。
過去の拒否・復旧履歴は `KB_SYNC_BLOCKED_20261029.md` を参照。現在の実行状態は `SYNC_STATUS.md` を参照。安全拒否された操作は迂回しない。

## Gitに含める内容

- 人が編集する `symbols.tsv` / `structs.tsv` / 手書き事典 / README / `kb.py`。
- 再生成用Python・Java・バッチと旧ラベルTSV、研究内容を要約した非機密の報告書。
- `SOURCE_MANIFEST.tsv` で各ファイルのバイト数・SHA-256を記録。コミット履歴が保存地点になる。
- 追跡対象は厳格な許可リスト。登録前に機密情報・拡張子・サイズ・辞書品質・ハッシュの変化を確認。

## Gitに含めない内容

- `generated/` の `research.sqlite`（約475MiB）と `kb.sqlite`、`CATALOG.md`、自動生成したREF・ラベル。
- Ghidraプロジェクト、Ghidraの統合V9 DB、ゲームの原作ファイルや実行/保存データ。
- Cookie、APIキー、トークン、個人名・メール・OSユーザー名、ローカルアクセスログ。
- 生成物の復元は認可済PCで `python -B tools/build_kb.py` を使う（研究ROOTの関連証拠が必要）。

## 作業ごとの安全フロー

1. `python -B tools/sync_knowledge.py audit` で機密検査・許可対象検査。失敗したら変更しない。
2. `python -B tools/sync_knowledge.py status` でGitの分岐・dirty状態・SHAを確認。
3. developがクリーンでリモート一致のときだけ `start TASK_ID` で `work/kb-TASK_ID` ブランチを作る。
4. 作業中に他のAIが同じフォルダを操作しない。別PC・別クローン・別担当ブランチを使用する。
5. 根拠を記した変更後、既存テストと `build_kb.py --check` を実行する。
6. `checkpoint TASK_ID` は許可対象だけステージし、変更前後のSHAが不一致なら停止する。
7. `publish` はPRIVATEを検証し、developの先行変更がない場合に限り通常のpushをする。
8. 作業ブランチはレビュー用。developへ無断統合しない。ff-only統合の条件を維持する。

## 禁止と復旧

- `reset`・`stash`・`rebase`・`amend`・`force` を行わず、作業外のファイルを触らない。
- 先行コミット・同時編集・権限拒否・認証拒否・安全拒否はすべて停止し、作業ID・日時・ログ要点・未完了範囲・再開位置を記録。
- Gitに残るコミットと `SOURCE_MANIFEST.tsv` を照合する。未pushなら LOCAL_ONLY と明示する。
- 遠隔の正本が変わった場合は `git fetch origin develop` と差分確認のみ。強制同期は行わない。
- Gitが壊れたときは `git status` と記録を確認し、正規のクローンに差分を手動再適用する。
- `.git/kb-sync.lock` が残っている場合は別AIが作業中の可能性があるので無断削除しない。
- 認証情報が疑われる時はpushを実施せず、対象ファイルをローカルに隔離する。

## 注意

過去の安全拒否は `KB_SYNC_BLOCKED_20261029.md` に保存済み。再開時に新たな許可された作業として設定・同期ツールを実装し、監査と回帰テストを通過した。
実際の同期成否はGitHubのprivate・ブランチ先端SHAの照合と `SYNC_STATUS.md` で確認する。
