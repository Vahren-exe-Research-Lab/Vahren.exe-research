# E-OFFLINE-20261101-08H-T018-T020-CALLER-TEMPORAL-IDENTITY-01 — E sanitized intake (not curated)

research_id: `E-OFFLINE-20261101-08H-T018-T020-CALLER-TEMPORAL-IDENTITY-01`
owner: `E`
tasks: `T018; T020`
observed_at: `2026-11-01 08H JST`
source_snapshot: `2026-11-01 08H source Library, based on earlier 03/04/07H reports`
source_relative_paths: `ChatGPT Library / T018_T020_CALLER_TEMPORAL_IDENTITY_AUDIT_20261101_08h.md` (Library file, not confirmed in PC checkout)
source_bytes: `8227`
source_sha256: `1688171315BDB14A1487443E476E66E23A8A839983CEE405205AC1CF5F029451`
source_verification: 2026-11-02 01:49 JST; file bytes SHA-256 measured from materialized ChatGPT Library original Markdown, NOT from PC copy. PC `tests/` source presence checked and all five were absent. Current PC E MASTER/T018/T019 checked read-only; historical old source hash is not newly verified native/ZIP hash.
provenance: ChatGPT Library user E-owned Markdown; in-source author/owner E, PC owner file not synced. No source Markdown, DAT/EXE/SAVE/SQLite, or raw trace uploaded.
VA/function_range: `0x4E53B0 (prior only)` (function ranges not independently revalidated in this publication)
CALL_site: `prior 0x545A02; 0x57AD8C; 0x57D982, NOT new native discovery`
offsets: `Unit +0x1E570 (prior STORE32); synthetic spawn-event key is NOT known native field`
evidence_kind: `PRIOR_STATIC / SYNTHETIC_60 / INFERRED / VERIFY`
golden_status: `G0/G1/G2 NOT QUALIFIED; DYNAMIC OBSERVED 0; actual Golden PASS 0; strict MATCH 0`
ready_status: `NOT READY; no MASTER formal integration`
prior_ids_or_KB: E 03H,04H and E 07H candidate identity; preexisting E 2026-10-28 capture binding
supersedes_or_errata: No original-native supersession claimed; do not double-count predecessor evidence.

## Reusable E acceptance/correction delta
比較器の合成受入では、STORE32結果を単なる真偽へ縮退すると情報欠落する。同一生pointer値をrun/フレームを跨いだUnit同一性の証明に使わない。caller別STORE32とBOOLEAN_GATEを区別し、Unit lineage・生成イベント・battle/frameの外部一次witnessがない場合はMODEL_STALE_LATCH/VERIFYとする。これは再利用・再割当の原作観測結果ではない。

## Historical tests (not rerun this intake)
元Library報告の60 synthetic PASS/9 mutation PASSは過去履歴。本入庫回に再実行なし。

## Source limits / unresolved
spawn_event形式とsource Unit lineageは合成スキーマ。新しいnative/原作DYNAMIC根拠ではない。現在の実装との一対一照合未了。

## Next permitted validation
E/T018合法G0+G1+G2の同一戦闘観測後にのみ、可視/合法に取得可能なUnit identity witnessとの整合を設計する。

**KB_CANDIDATE only.** Native/static source findings belong to their original B/REA owners; this E publication preserves only E-owned comparison rules and corrections. Do not upgrade SYNTHETIC/STATIC to real-game Golden or READY. Do not retry previously refused source operations or guarded VA 0x5710C0–0x571500. No user worktree/develop/REF/dictionary changes.
