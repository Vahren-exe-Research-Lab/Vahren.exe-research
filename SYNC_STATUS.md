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

## 2026-11-01 KB-DATUI / KB-SAVE（Claude）

- develop 0225b2e を基準に隔離 worktree で作業。develop は統合用 worktree が使用中のため `sync_knowledge.py start/checkpoint/publish` は使えず、同じ検査（`.git/kb-sync.lock` の排他、PRIVATE 確認、origin/develop が基準と一致、作業ツリー clean、push 後の ls-remote 一致）を手作業で行った。
- `work/kb-KB-DATUI-20261101`（5ba36b7）: 汎用一覧 v4 の調査（R1101）と、未送信だった selector-cancel（68e0546）の取消契約節。
- `work/kb-KB-SAVE-20261101`: DATUI の上に重ねた。通常セーブ形式 `REF_SAVE_FORMAT.md` を新設し許可リストへ追加、symbols/structs の追加と既存の誤り修正。統合は DATUI → SAVE の順に ff-only。
- 確かさの引上げ（ユーザー承認 2026-11-01）: 0x8BCF00・0x521560 → 実機確認（R1101）、0x598CE0・0x596AA0・0x471AF0・0x471D20 → 静的確認（T014 監査15〜19 と実セーブ byte 一致）。生成時は `build_kb.py --accept-confidence-change` が要る。

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

## 2026-11-02 KB curator: B/T011–T013 historical semantic adoption (two verified ff-only batches)
- PRIVATE develop publication independently read back: `60288e7d429c76f0a56e56987bd72790615593dc` → [`d4ad5d475f70eaf22a09341337f9663c38141f4b`](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/commit/d4ad5d475f70eaf22a09341337f9663c38141f4b) → [`3f09a3b91ef1801e49bc4dcc30c9d868b83472b8`](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/commit/3f09a3b91ef1801e49bc4dcc30c9d868b83472b8). Normal private branch push and develop push, actual SHA and file readback succeeded; no force/rebase/reset. Source owner was existing B Draft PR #18 at pinned head `48821779f639013a4cc371ddc91e1b3064bc3647`; no new owner PR.
- **PUBLISHED_INTAKE owner originals mirrored to develop: 4 existing IDs**, `B-20261013-1110-01`, `B-20261013-1134-01`, `B-20261013-1141-01`, `B-20261013-1146-01` (owner blob bytes matched 4/4). **New independently reviewed CURATED_STATIC: 3 IDs** (1110 post-action `0x57BE30`; 1134 summon core `0x54E7B0`; 1146 runtime constructor `0x56F880`); **DUPLICATE_LINKED: 1** (1141 keyed record `0x577260`, pre-existing symbol/EXP ABI). These are historical study IDs, NOT four new discoveries or owner READY promotion. Source report SHA matched authorized PC 4/4 and original PE hash matched; three native windows independently decoded 224/871/1221 instructions, respectively.
- Meaning links: [post-action REF](REF_SKILL_POST_ACTION.md), [summon/EXP REF](REF_UNIT_EXP_SUMMON.md), updated [symbols](symbols.tsv) and SOURCE_MANIFEST. Curated scope is narrow original x86 CALL/field/branch/return only. All original-game Golden PASS=0, strict MATCH=0, newly authorized READY=0, G4 external-result commit NOT PASSED; inferred downstream child/ABI effects stay VERIFY.
- Gate: dedicated `work/kb-curate-b-skillpost-20261102` isolated worktree, other owners' dirty worktrees/branches untouched; PRIVATE checked, allowlist/secret audit pass, manifest pass, symbol check error0/warning0, KB tests 5/5 and sync tests 9/9, Git diff check. No original EXE/DAT/MAP/SAVE/ZIP or generated SQLite pushed. Isolated smoke-search `kb.py addr/find/docs` passed using a **local ignored copy** of the prebuilt small KB DB with newly verified symbol patched for lookup only; full research.sqlite reindex NOT run and this temporary DB is NOT Git source of truth.
- **Next cursor:** reconcile remaining existing B owner PR #18 T011/T012/T013/T024/T028 IDs by source SHA+semantic correction (including T013 2026-10-23 20H/22H), then REA #16 04H/06H/09H and legacy semantic backlog. Independently check current develop HEAD and curator dirty/lock before every next write; revisit `research/intake/README.md` and `REF_BATTLE_TAKEOVER.md` only after separate curator dirty ownership clears. B blocked payloads, protected native VA, REA 18H/Wave6 remain SAFETY_HOLD without alternative-route retry. **Unknown backlog denominator: not computed this run**; 1941 read-only indexed sources with 12 update-pending is metadata, not 12 new findings.
