# E-OFFLINE-20261101-0453-T020-T013-THREE-CALLER-RETURN-USE-01 — E sanitized intake (not curated)

research_id: `E-OFFLINE-20261101-0453-T020-T013-THREE-CALLER-RETURN-USE-01`
owner: `E`
tasks: `T020; related T018/T019`
observed_at: `2026-11-01 04:53 JST`
source_snapshot: `2026-10-21 ZIP SQLite (historical)`
source_relative_paths: `ChatGPT Library / T020_T013_THREE_CALLER_RETURN_USE_AUDIT_20261101_0453.md` (Library file, not confirmed in PC checkout)
source_bytes: `8634`
source_sha256: `A14162DDC2CB73D9782638D19C1E4FFF87598972332658DA892934273215E70A`
source_verification: 2026-11-02 01:49 JST; file bytes SHA-256 measured from materialized ChatGPT Library original Markdown, NOT from PC copy. PC `tests/` source presence checked and all five were absent. Current PC E MASTER/T018/T019 checked read-only; historical old source hash is not newly verified native/ZIP hash.
provenance: ChatGPT Library user E-owned Markdown; in-source author/owner E, PC owner file not synced. No source Markdown, DAT/EXE/SAVE/SQLite, or raw trace uploaded.
VA/function_range: `callee 0x4E53B0; callers 0x545740, 0x57AA00, 0x57D8B0` (function ranges not independently revalidated in this publication)
CALL_site: `0x545A02 E8→0x4E53B0; 0x57AD8C E8→0x4E53B0; 0x57D982 E8→0x4E53B0`
offsets: `Unit +0x1867E, +0x1E570; vtable+0x5C candidate only`
evidence_kind: `STATIC_SNAPSHOT / SYNTHETIC_24 / VERIFY`
golden_status: `G0/G1/G2 NOT QUALIFIED; DYNAMIC OBSERVED 0; actual Golden PASS 0; strict MATCH 0`
ready_status: `NOT READY; no MASTER formal integration`
prior_ids_or_KB: E 03:51 scan/rect/vcall; existing B/T012 target latch interpretation
supersedes_or_errata: No original-native supersession claimed; do not double-count predecessor evidence.

## Reusable E acceptance/correction delta
同じcalleeを使う3 callerの局所文脈を比較。0x545A02と0x57AD8Cでは戻り値をUnit+0x1E570の32-bit slotへstoreする静的経路がある一方、0x57D982ではstoreせず0/nonzero gateとして用い、rect値もゼロでのみ後続間接virtual callが候補となる。Unit+0x1867Eは前2 callerで==0、第三で!=0の局所gate。すべて前提条件であり実行到達や意味・同一targetは未証明。

## Historical tests (not rerun this intake)
元Library本文は旧codeSHA4/4、直接CALL3/3、local guard3/3、mutation拒否4/4、24/24 syntheticと報告。128前回fixtureは再実行扱いで独立新発見と数えない。本入庫回の新テストは0。

## Source limits / unresolved
出典は旧snapshotとE owned reportの記録。現在のV9現物と元EXE E8 bytesはこの入庫回では未照合。old index codeSHAをPEの実バイトSHAと混同しない。

## Next permitted validation
現行B source/KBを先行確認し、2 STORE32 vs 1 BOOLEAN_GATEをcallerごとにfixture識別。ゲーム観測と同じUnitの世代照合が得られるまではstrict比較不可。

**KB_CANDIDATE only.** Native/static source findings belong to their original B/REA owners; this E publication preserves only E-owned comparison rules and corrections. Do not upgrade SYNTHETIC/STATIC to real-game Golden or READY. Do not retry previously refused source operations or guarded VA 0x5710C0–0x571500. No user worktree/develop/REF/dictionary changes.
