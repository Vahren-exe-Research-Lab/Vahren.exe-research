# E-OFFLINE-20261101-0351-T020-T013-SCAN-RECT-VCALL-GATE-01 — E sanitized intake (not curated)

research_id: `E-OFFLINE-20261101-0351-T020-T013-SCAN-RECT-VCALL-GATE-01`
owner: `E`
tasks: `T020; related T018/T019`
observed_at: `2026-11-01 03:51 JST`
source_snapshot: `2026-10-21 ZIP SQLite (historical)`
source_relative_paths: `ChatGPT Library / T020_T013_SCAN_RECT_VCALL_AUDIT_20261101_0351.md` (Library file, not confirmed in PC checkout)
source_bytes: `7773`
source_sha256: `5C399A9CCF30EB439E8DD29DA9A3DED4D99C06173CB35567FFD354C5B7163DD0`
source_verification: 2026-11-02 01:49 JST; file bytes SHA-256 measured from materialized ChatGPT Library original Markdown, NOT from PC copy. PC `tests/` source presence checked and all five were absent. Current PC E MASTER/T018/T019 checked read-only; historical old source hash is not newly verified native/ZIP hash.
provenance: ChatGPT Library user E-owned Markdown; in-source author/owner E, PC owner file not synced. No source Markdown, DAT/EXE/SAVE/SQLite, or raw trace uploaded.
VA/function_range: `0x57D8B0; 0x4E53B0; 0x4C1860` (function ranges not independently revalidated in this publication)
CALL_site: `0x57D982 E8→0x4E53B0; 0x57D994 E8→0x4C1860; 0x57D9A9 CALL EAX (unresolved virtual, guessed vtable+0x5C)`
offsets: `Unit +0x1867E; Unit +0x1E570 (prior caller-specific)`
evidence_kind: `STATIC_SNAPSHOT / SYNTHETIC_128 / VERIFY`
golden_status: `G0/G1/G2 NOT QUALIFIED; DYNAMIC OBSERVED 0; actual Golden PASS 0; strict MATCH 0`
ready_status: `NOT READY; no MASTER formal integration`
prior_ids_or_KB: B/T013 existing `Ai_AdjustSearchTargetCoordinates`; B/T012 `Unit_RefreshTargetLatch` name; later E 04H cross-caller comparison
supersedes_or_errata: No original-native supersession claimed; do not double-count predecessor evidence.

## Reusable E acceptance/correction delta
2026-10-21保存済みの旧Ghidra疑似Cでは、条件を満たすと0x57D982の0x4E53B0戻り値をアドレスとして使用せず0/nonzero gateにする。このcallerで0x4C1860矩形判定を評価し、双方ゼロのときだけ間接CALLへ到達し得る。`0x4E53B0`の全callerを一律『target保存』と解釈しない。`CALL EAX`の実体・ABI・副作用は未同定。

## Historical tests (not rerun this intake)
元Library本文に128/128 synthetic PASSと記載（64 invalid coordinate,32 inactive Unit,8 prior branch,9 virtual-eligible,15 suppressed）。今回モデル/原作は実行せず、元レポートの存在と実バイトSHAのみ検証。

## Source limits / unresolved
コードSHA・E8 bytes/実原本EXE SHAは過去スナップショットの記録で、本入庫回に再測定していない。旧README/V3を現行V9とみなさない。

## Next permitted validation
現行V9/既存B owner sourceと直接CALL siteを読取専用で突合し、旧codeSHAとの差異・間接先不明を保持。

**KB_CANDIDATE only.** Native/static source findings belong to their original B/REA owners; this E publication preserves only E-owned comparison rules and corrections. Do not upgrade SYNTHETIC/STATIC to real-game Golden or READY. Do not retry previously refused source operations or guarded VA 0x5710C0–0x571500. No user worktree/develop/REF/dictionary changes.
