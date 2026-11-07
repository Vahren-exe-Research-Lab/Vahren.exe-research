# 研究知識ベース同期状態

> **2026-11-07 正本切替:** [Vahren-exe-Research-Lab/Vahren.exe-research](https://github.com/Vahren-exe-Research-Lab/Vahren.exe-research) の `develop` が正本。旧リポジトリはPrivateバックアップ。以下の古いPR/URLは歴史的出典。
> GitHub公開は未承認。旧リポジトリへの新規push禁止。

- 作業ID: KB-SYNC-01-20261029
- 状態: **SYNCED / PRIVATE / DEVELOP CLEAN（最終のGitHub側とローカルのSHAを都度照合する）**
- 正本: https://github.com/Vahren-exe-Research-Lab/Vahren.exe-research （非公開）
- 正本ブランチ: `develop`。**現在の先端SHAは `git rev-parse HEAD` とGitHubの `git ls-remote origin refs/heads/develop` を必ず照合する。** 古いSHAを固定参照しない。
- **2026-10-29時点の履歴検証**: `work/kb-KB-SYNC-01-VERIFY` で `start` → `checkpoint` → `publish` 成功。private確認・GitHub側の同一SHA確認後、`git merge --ff-only` で正本に統合。現時点の最新GitHub先端と混同しない。
- Git管理対象: `tools/sync_knowledge.py` の許可リスト掲載原本＋生成SHA台帳。許可外はステージ/同期禁止。
- **2026-10-30当時の辞書履歴（最新値ではない）**: `symbols.tsv` は365件（旧363件＋領地名2件）、SHA-256 `C01924149029DC7AB062A3056E8C7DF00968B126ACE32059E67DE871F456A704`。旧363件のSHAは `6DE767D362CDAF354C30832E7CFAF82B17512661890C8F215FAF652CB627851F`。現在の辞書件数・SHAは現物から再計算する。
- Git管理から除外: 最新の全文索引DB（422.8MB）・旧DBバックアップ（506.4MB）、生成ラベル/目録、原作EXE・DAT・MAP・セーブ・ZIP、個人情報・トークン。
- 同期の形式: **必要なときに手動実行**。バックグラウンドで自動pushする仕組みではない。
- 作業ルール: `python -B tools/sync_knowledge.py status` → `start TASK_ID` → `checkpoint TASK_ID` → `publish`。担当別作業ブランチ、ff-only統合。force/reset/stash/rebase/amend禁止。
- 同期確認: `git status --short --branch`、`git rev-parse HEAD`、`git ls-remote --heads origin refs/heads/develop`、`gh repo view Vahren-exe-Research-Lab/Vahren.exe-research --json visibility`。
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

## 2026-11-02 KB curator: B/T013 historical comparator, mode setter and producer CURATED_STATIC

- Previously owner-published on [B PR #18](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/18), pinned head `4fdd9901b1413972d201716bcd44d77b031e7b6d`: 3 existing IDs `B-20261023-20H-T013-TROOP-SORT-1BC-NATIVE-01`, `B-20261023-22H-T013-TROOP-FORM-MODE-SETTER-01`, and `B-20261023-2317-T013-TROOP-MODE-SOURCE-CASE8-01`. The sanitized owner intake abstracts were copied byte-for-byte into private develop (3 **PUBLISHED_INTAKE** IDs, not new discoveries); 3/3 source report SHA matched original PC and original ver0.67 PE SHA matched, with independent pefile/Capstone native windows 26/113/221 bytes checked.
- **New CURATED_STATIC: 3 research IDs** for bounded native comparator `0x567EC0`, mode setter `0x569530`, and signed >2 producer gate `0x4B597E/81`. Full meaning, object type, 32/33 candidate ordering, mode inputs on other callers, dynamic movement and G4 are **VERIFY**. Two justified function names entered `symbols.tsv`; no speculative `structs.tsv` entries. Source/errata links in [REF_BATTLE_AI_MORALE.md](REF_BATTLE_AI_MORALE.md) and [intake README](research/intake/README.md). First curator commit [`602e1326bde46aaaef6f6b4f978bd185255e8012`](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/commit/602e1326bde46aaaef6f6b4f978bd185255e8012) reached PRIVATE develop via normal branch push and ff-only develop push and independent GitHub readback. No owner PR/checkout/branch was changed.
- Gate: SOURCE_MANIFEST **201** entries, `sync_knowledge.py audit` PASS; `check_symbols.py` 442 entries/error0/warn0; KB workflow 5/5 and sync security 9/9 tests PASS, `git diff --cached --check` PASS. `kb.py addr/find` for both new functions, `kb.py docs`, `kb.py files --task T013` smoke passed in the isolated worktree using a local ignored small DB patched from staged symbols only; generated DB not pushed. Original-game Golden PASS=0, strict MATCH=0, newly accepted READY=0. Indexed PC text sources 1941 with **12 update-pending, 0 removals**; these 12 are not 12 missing research IDs.
- **Next cursor:** B/T013 2026-10-23 next source-mode/sort follow-ups by research ID/source SHA/errata, plus B/T011–T028 unCURATED and E/REA owner backlog; preserve the distinct PUBLISHED_INTAKE/CURATED/DUPLICATE/VERIFY categories. Check fresh develop HEAD, worktree ownership/dirty/lock before writes. Excluded B rejected payloads, protected VA, REA 18H/Wave6 remain SAFETY_HOLD; no retry or alternative-route bypass. Remaining total semantic backlog denominator NOT yet proven.


## 2026-11-03 KB curator B/T012 flash source/callee semantic batch (08H JST)
- Work ID: `KB-CURATION-B-FLASH-20261103-08H`. Existing B owner IDs `B-20261013-1440-01` and `B-20261013-1614-01`; source owner private Draft PR #18 head `844e8088162420c56b3b6866e3633fa89e31e6f8`. Both authorized-PC original reports source SHA matched; original PE SHA `E8DAC301…767187` matched; three original caller windows and 81-byte/21-instruction gated wrapper independently decoded. Native bounded facts + correction links adopted in `REF_SKILL_POST_ACTION.md`, meaning crosswalk in `research/intake/README.md`, verified function-only symbol `0x576F10` added; `structs.tsv` unchanged. No newly discovered research ID or owner-source mirror.
- Local quality gates: `sync_knowledge.py audit` PASS (201 allowlisted source entries); `check_symbols.py` 449 entries/0 errors/0 warnings; KB tests 5/5, sync security 9/9; `git diff --check` PASS. `kb.py addr 0x576F10`, `find SkillFlash_PostDamage_GatedRingDispatch`, `docs 0x576F10` and `files --task T012` returned 0 using an **isolated ignored temporary copy** of the existing 2.44MB small KB database with only the new symbol patched for smoke testing; full `research.sqlite` reindex and source-game run NOT performed. Source-code/dictionary indexing is separate from the temporary smoke DB and must be regenerated through the normal toolchain before production use.
- **ENV_HOLD `KB-CURATION-B-FLASH-20261103-08H-TEMP-DB-UNLINK`:** deletion of isolated ignored `.worktrees/kb-curate-skillchance-20261103-07h/generated/kb.sqlite` after successful smoke checks failed `PermissionError [WinError 32]` (another process holds the file). No alternate tool/path/shell deletion retry, and no staging/push of this generated DB. It remains an ignored temporary artifact. Authorized next cleanup only when its file handle/ownership is independently verified free, without changing other-owner files. This is independent of the curated source evidence; it must not be mistaken for an original-game result.
- G4 result commit NOT PASSED; actual original-game Golden PASS=0, strict MATCH=0, newly approved READY=0. Next legal source cursor: `B-20261013-1356-01` (only if independently safe) or independent `B-20261013-1417-01`; E/REA/A/C/D owner backlog separate. Do not revisit refused content. Actual GitHub develop publication/commit must be verified separately; local checks alone are NOT publication.
