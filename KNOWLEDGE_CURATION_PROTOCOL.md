# Central research knowledge integration policy

Repository: private ButaMonky/Hakushin067-Research-Knowledge, protected workflow on develop.
Local research authority: authorized PC _REDEV_RESEARCH, including MASTER_LEDGER and A-E/REA source receipts.
Purpose: give AI a small, trustworthy map without destroying or blindly copying research history.

## Provenance and precedence
1. Verify repo is PRIVATE and compare GitHub develop SHA with local develop before starting a separate work branch.
2. Read the KB README/SYNC_STATUS, MASTER state, owner HANDOFF and source SHA. Never assume an old GitHub summary is current.
3. The original ASM/DAT, its own source SHA and corrected owner report outrank a search hit or a previous summary.
4. Source catalogs are leads, not authoritative conclusions; generated databases stay on the research PC.
5. Preserve research IDs and corrections. Treat same-ID cross-file references as links, not automatically independent findings.
6. Use evidence states STATIC, INFERRED, VERIFY, DYNAMIC, safety BLOCKED, GOLDEN and READY separately.

## Automatic source inventory
- Command from the PC research root: python -B knowledge/tools/audit_research.py --root . --out knowledge
- The script reads generated/research.sqlite (read-only) and each indexed text's first 2 KiB (read-only).
- Export RESEARCH_SOURCE_CATALOG.tsv: path, PC source SHA256, bytes, line count, VA mentions, heuristic owner/task/domain and candidate ID.
- Export RESEARCH_DUPLICATE_CANDIDATES.tsv: exact-byte SHA groups and shared-ID groups requiring review.
- Export RESEARCH_INTEGRATION_SNAPSHOT.md: corpus totals and classification coverage.
- Exports are intentionally metadata only. They contain no original game binaries, saves, large search DB or privileged local paths.

## Ongoing A-E/REA scheduled tasks
- Before new research, consult the most recent KB refs and read-only native V9/owner evidence, then search for duplicates.
- Each agent keeps modifications within its own task/HANDOFF. Report new evidence in KB_CANDIDATE with research ID, task/owner, VA, calls, offsets, proof path, SHA, confidence, error/correction, next validation and Golden/READY.
- Only the dedicated knowledge curator uses the shared KB Git repository, one isolated work branch at a time.
- Curator reads candidate deltas, verifies source ownership, metadata, content and conflicts; updates curated refs and catalogs; runs audits/tests; then publishes reviewed branch, ff-only after validation.
- If PC is offline, work from accessible private GitHub sources and label any unsynced work OFFLINE-UNSYNCED/VERIFY, never invent original source content.
- Never directly merge, overwrite or delete another agent's work and never attempt a blocked command by an alternative route.

## Known incompleteness
- The curated GitHub repo is not a mirror of the ~22k local files; it holds approved sources, their index and summarized evidence.
- Text index may skip files larger than its limit, binaries, images, Ghidra project databases and other formats.
- The old B Library 54-byte-difference set, safety holds and missing 10/25 text remain separate recovery issues; no automatic acceptance.
- New/edited source files require a fresh read-only index --check and an authorized incremental index run on the PC.
- A snapshot is not proof of the original game matching a replacement engine; original gameplay Golden remains independently measured.

## Ghidra V9 graph-first workflow (2026-10-31)
- A-E/REAは研究開始時に既存のsymbols.tsv、V9の関数range・E8 CALL site・Ghidra参照とowner HANDOFFを調査し、同関数の重複研究を避ける。
- 研究報告で直接触れていない関数も tools/v9_coverage.py で調査対象にする。read-only V9 SQLite・既存research.sqliteから再計算し、元Ghidraプロジェクトを再解析しない。
- --inspect VA は関数入口でなくても function_range から所有関数を返し、native E8 CALL siteと元命令バイトを8件以内で示す。これはABIの確定やGolden PASSを意味しない。
- GitHubのGHIDRA_V9_GAPS_TOP500.tsvと分野別TSVは軽量な候補キュー。完全版V9_FUNCTION_CROSSWALK.tsvは研究PCのgenerated/にのみ保存する。
- 検証を終えた新規関数だけ、元ASM/DATの出典・VA・研究ID・確度・ownerを揃え、symbols.tsvとREF_*へ正式に登録する。自動候補からの無確認昇格を禁止。
- 収録されない資料を調べる際はGHIDRA_V9_COVERAGE_REPORT.mdの検索対象外理由を確認する。サブディレクトリ、コード形式、3MB超過、バイナリは本文全文索引と別に扱う。
- 現行Ghidra V9はV8と後発関数を合成したSTATIC索引であり、同名の単一Ghidraプロジェクト全体が完全統合済みという意味ではない。
- 証拠・辞書・作業ブランチの衝突を優先して中断し、拒否済み範囲の別手段取得は行わない。
- Nested 799-file metadata audit (2026-10-31): archives 206, plugin work 321, takeover research 180, snapshots 52, runtime 31, manual review 9. Preserve shallow indexing by default; review the nine individually and eligible takeover summaries before opting into any recursive search. Never bulk-import original snapshots/runtime logs or overwrite owner data.

## Isolated-worktree V9 symbol source (2026-10-31)
- When a curator edits symbols.tsv in a dedicated worktree, invoke that worktree's tools/v9_coverage.py with `--root <research-root> --out <isolated-kb> --symbols <isolated-kb>/symbols.tsv --export`. This keeps the indexed original PE/V9 and research.sqlite under the authorized read-only research root while using the curated symbol dictionary from the isolated worktree.
- Without --symbols, the backward-compatible default reads <research-root>/knowledge/symbols.tsv, which may be an unrelated user checkout. Never equate that older dictionary with the isolated candidate version.
- The full V9 function crosswalk remains in the local research root's knowledge/generated directory; GitHub receives only lightweight report and priority TSVs. Candidate counts are descriptive STATIC metadata, not proof or READY.


## User-authorized B GitHub evidence staging (2026-11-01)
- User direction supersedes the earlier B prohibition on Git/GitHub **only** for independently sourced, safe B-owned T011/T012/T013/T024/T028 research evidence. Keep all safety refusals, data ownership, MASTER ownership by E, original PE/DAT/SAVE/ZIP read-only, and curator-only `develop`, `symbols.tsv`, `structs.tsv`, `REF_*` and `SOURCE_MANIFEST.tsv` editing.
- The B owner must check the most recent HANDOFF, conflict/recovery queue, source SHA, research ID and existing KB/V9 before new investigation. Each scheduled run should **publish** new B findings plus a small oldest-first batch of previously unintegrated findings, instead of letting candidates accumulate only on the PC.
- Before publishing verify PRIVATE, redact identities/paths/secrets, and exclude raw EXE/DAT/SAVE/ZIP, DBs, screenshots and generated indexes. **2026-11-02 superseding destination:** B's sole canonical owner path is `research/intake/B/`. `research/lane_b/` is historical read-only mirror. Reuse existing owner PRs rather than creating hourly PRs; never edit user checkout or `develop`.
- Each candidate's **actual reusable evidence** must include ID, owner/task, VA/CALL site/offset, exact operation/branch and competing interpretation, source-relative path and verified SHA/lines, native-window/PE SHA when available, status STATIC/INFERRED/VERIFY/DYNAMIC, prior/duplicate IDs, correction/erratum, Golden/READY, missing source, next validation and recovery. A TSV alone or a path-only catalog is insufficient; provide a readable explanation so a future AI can work from GitHub without inventing the missing PC report.
- GitHub branch+PR with fetched commit SHA/file readback is `GITHUB_STAGED/NOT_CURATED`, **not** a valid claim that `develop` is updated. The dedicated curator owns verification, audit and SAFE allowlist/manifest updates, integrates confirmed evidence into `REF_*` and only names/symbols justified by original sources, then performs approved ff-only publication to `develop`. Report `GITHUB_CURATED` only after verified `develop` SHA and source links.
- Curator's first priority is the existing B backlog, especially 2026-11-01 10–21H T013/T024 evidence and older unsynced 03H/07H/10-25 gaps. Triage as `source_verified`, `staged`, `curated`, `pending_source`, `blocked_safety`, `superseded`; never treat an unrecoverable file as available. No automatic promotion to Golden/READY or automated conclusion from V9 metadata.
- On connection/push refusal, stop that specific operation (never switch tools, paths or accounts to circumvent an existing safety denial); persist error, unsaved/pending IDs and permitted next action in the B HANDOFF. Continue independent safe work. Existing automation cadence/enabled states are unchanged.

## 2026-11-01 Private research intake publication
Current user directive and exceptions: [RESEARCH_INTAKE_PROTOCOL_20261101.md](RESEARCH_INTAKE_PROTOCOL_20261101.md). Owners A-E/REA may publish only their own sanitized, evidence-labeled research on private isolated `research/intake/<owner>/` branches; the KB curator remains sole editor of curated `develop`, `REF_*`, `symbols.tsv`, `structs.tsv`. Previous blanket Git restriction is superseded **only** for this owner-specific intake scope. Do not publish blocked evidence, sensitive material, raw game assets or databases; VERIFY and synthetic results are not Golden or READY. The [intake backlog index](research/intake/README.md) tracks incomplete recovery. Existing per-task schedules and owner boundaries remain intact.

## 2026-11-02 canonical intake and non-linear PR curation
- For A-E/REA, canonical owner source path is `research/intake/<owner>/`. Deduplicate `research_id` + actual source SHA + corrections across PR stacks and mirrors, preserving source PR/head SHA. An old duplicated historical ID is not a new finding.
- Different open owner PRs can share an older base. Curator may copy only reviewed, sanitized Git blobs into a private, isolated curation branch starting at the current `develop`; never rebase/force/merge other-owner branches. Advance `develop` ff-only only after lock, PRIVATE, allowlist, manifest, privacy, tests and remote SHA gates.
- Distinguish `PUBLISHED_INTAKE` (searchable owner source), `CURATED` (independently checked original evidence and semantic links), `DUPLICATE_LINKED`, `VERIFY`, `MISSING_SOURCE` and `SAFETY_HOLD`. Owner-stated original PE SHA and GitHub blob readback do not constitute curator's independent x86 or Golden proof.
- Maintain per-ID source PR/head, original owner source SHA, correction, target REF and unverified constraints in `research/intake/README.md`; do not promote dictionary confidence from file names, V9 static CALL graphs or unreviewed study. If PC is disconnected or lock/unit tests cannot be checked, preserve the isolated branch without advancing develop and record the exact pending gate.

## Current curator status categories and existing-PR reuse (2026-11-02)

Canonical owner path is research/intake/<owner>/ (B specifically research/intake/B/; research/lane_b/ is history-only). **Reuse existing owner PRs rather than create hourly branches or one PR per ID.** Curator alone uses a clean isolated branch from the most recent PRIVATE develop to copy audited sanitized blobs across non-linear old-owner PR histories; retain immutable owner SHA/source report hashes and corrections, never rebase/force/overwrite an owner. Only verified lock, privacy, allowlist, full SOURCE_MANIFEST, tests and remote SHA permit ff-only develop publication.

Count PUBLISHED_INTAKE separately from CURATED_POLICY, CURATED_SOURCE_PROVENANCE, CURATED_STATIC, DUPLICATE_LINKED, SOURCE_MISSING and SAFETY_HOLD. Owner study crosswalks are not automatic native evidence or Golden/READY. [E legacy 193-ID intake](research/intake/E/INDEX.md), [shared backlog](research/intake/README.md), [battle REF](REF_BATTLE_TAKEOVER.md) and [DAT REF](REF_DAT_BEHAVIOR.md) hold the precise reviewed scope.
