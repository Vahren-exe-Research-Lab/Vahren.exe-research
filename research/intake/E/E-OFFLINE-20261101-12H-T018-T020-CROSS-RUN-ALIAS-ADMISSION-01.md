# E-OFFLINE-20261101-12H-T018-T020-CROSS-RUN-ALIAS-ADMISSION-01 — E sanitized intake (not curated)

research_id: `E-OFFLINE-20261101-12H-T018-T020-CROSS-RUN-ALIAS-ADMISSION-01`
owner: `E`
tasks: `T018; T020`
observed_at: `2026-11-01 12H JST`
source_snapshot: `2026-11-01 12H source Library, synthetic POSIX temp files`
source_relative_paths: `ChatGPT Library / T018_T020_CROSS_RUN_ALIAS_AUDIT_20261101_12h.md` (Library file, not confirmed in PC checkout)
source_bytes: `6377`
source_sha256: `638F53757F091144F1278DAFD41BB91E5FDA6AC59EAD76F783205332B321DBD2`
source_verification: 2026-11-02 01:49 JST; file bytes SHA-256 measured from materialized ChatGPT Library original Markdown, NOT from PC copy. PC `tests/` source presence checked and all five were absent. Current PC E MASTER/T018/T019 checked read-only; historical old source hash is not newly verified native/ZIP hash.
provenance: ChatGPT Library user E-owned Markdown; in-source author/owner E, PC owner file not synced. No source Markdown, DAT/EXE/SAVE/SQLite, or raw trace uploaded.
VA/function_range: `N/A` (function ranges not independently revalidated in this publication)
CALL_site: `N/A`
offsets: `file identity (POSIX inode in synthetic trial), not game runtime offsets`
evidence_kind: `SYNTHETIC_45 / VERIFY / ERRATUM_REQUIRED`
golden_status: `G0/G1/G2 NOT QUALIFIED; DYNAMIC OBSERVED 0; actual Golden PASS 0; strict MATCH 0`
ready_status: `NOT READY; no MASTER formal integration`
prior_ids_or_KB: E 09/10/11H synthetic gates, prior 11H byte-integrity comparator
supersedes_or_errata: IMPORTANT 2026-11-01 18H E-owned PC triage `tests/T020_E_OFFLINE_39_ADMISSION_TRIAGE_20261101_18H.md` (locally rehashed 2026-11-02; SHA256 D7A4498270737DC4E756638758BCAB1B9FD0E1EBF68592614D85F08FE66B7245): 12Hの『全runの全相対path/実体を例外なく一意』と読める結論はOVERSTRICT。original/replacementが同じ不変の再生INPUT SAVE/MAPを共有しても正当な場合がある。区別すべきは共有INPUTと独立取得された各runの観測OUTPUT/CAPTURE。共有byte/SHAは独立観測の証明ではない一方、ただちに不適格とも限らない。旧12Hの一律拒否規則を無批判に採用しない。

## Reusable E acceptance/correction delta
先行11H比較器の同run内`relative_path`重複検査では、別runが観測出力ファイルを共有していることやハードリンクaliasを独立原本/置換結果として誤受入し得る。実run所有権/role namespace/ファイル実体同一性・自己申告DYNAMICを別条件として扱う、という合成の検査漏れ。

## Historical tests (not rerun this intake)
元Library報告の45/45 synthetic PASS、legacy誤受入24/24、新gateで同じ24/24検出、初回期待値不一致3を分類訂正。今回テストなし。

## Source limits / unresolved
POSIX inode/hardlink検査はWindows File ID/再解析ポイント/TOCTOU検証に未適用。実ゲームの不具合ではない。

## Next permitted validation
Windowsでsource role/provenance/run captureの区別を検証し、入力fixture共有例外と独立観測出力一意性を別判定とする。原作Golden/DYNAMIC証拠なし。

**KB_CANDIDATE only.** Native/static source findings belong to their original B/REA owners; this E publication preserves only E-owned comparison rules and corrections. Do not upgrade SYNTHETIC/STATIC to real-game Golden or READY. Do not retry previously refused source operations or guarded VA 0x5710C0–0x571500. No user worktree/develop/REF/dictionary changes.
