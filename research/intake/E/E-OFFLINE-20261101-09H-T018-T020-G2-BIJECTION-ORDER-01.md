# E-OFFLINE-20261101-09H-T018-T020-G2-BIJECTION-ORDER-01 — E sanitized intake (not curated)

research_id: `E-OFFLINE-20261101-09H-T018-T020-G2-BIJECTION-ORDER-01`
owner: `E`
tasks: `T018; T020`
observed_at: `2026-11-01 09H JST`
source_snapshot: `2026-11-01 09H source Library, synthetic fixture`
source_relative_paths: `ChatGPT Library / T018_T020_G2_BIJECTION_ORDER_AUDIT_20261101_09h.md` (Library file, not confirmed in PC checkout)
source_bytes: `9968`
source_sha256: `1F4E9A31904772FA5990F8F324EDA234A204FD5C0D317834DEA00EBFC26C07A1`
source_verification: 2026-11-02 01:49 JST; file bytes SHA-256 measured from materialized ChatGPT Library original Markdown, NOT from PC copy. PC `tests/` source presence checked and all five were absent. Current PC E MASTER/T018/T019 checked read-only; historical old source hash is not newly verified native/ZIP hash.
provenance: ChatGPT Library user E-owned Markdown; in-source author/owner E, PC owner file not synced. No source Markdown, DAT/EXE/SAVE/SQLite, or raw trace uploaded.
VA/function_range: `N/A; prior E/T018 battle container refs only` (function ranges not independently revalidated in this publication)
CALL_site: `N/A (prior caller references to 0x4E53B0 are not new analysis)`
offsets: `prior E+0x1E8630/34/38; Side Unit vector+0x48/4C/50; Troop vector+0x38/3C/40; Troop members+0x0C/10/14`
evidence_kind: `SYNTHETIC_117 / VERIFY`
golden_status: `G0/G1/G2 NOT QUALIFIED; DYNAMIC OBSERVED 0; actual Golden PASS 0; strict MATCH 0`
ready_status: `NOT READY; no MASTER formal integration`
prior_ids_or_KB: E 08H temporal ID; curated REF_BATTLE_TAKEOVER.md as prior STATIC (not new E discovery)
supersedes_or_errata: No original-native supersession claimed; do not double-count predecessor evidence.

## Reusable E acceptance/correction delta
G2を単一rowではなくattack/defend/reinforce三side×順序付きUnit/Troop別個の全単射で比較する合成条件。別Unitが同じ定義参照でも自動dedupeしない。同じmember並びを持つ別TroopでもTroop IDとordinalsを独立に見る。NULL/raw pointer alias/Unit generation/偽DYNAMIC_VERIFIED/不正MAP SHAはVERIFY。最初の105件中9不一致を是正後、同member-list Troop入替を検出するためTroop bijection追加。

## Historical tests (not rerun this intake)
過去の合成117/117 PASS (model-equal9, different24, verify84); 初期96/105 mismatch9、後105/105、その後117/117へ拡張。今回テスト/原作実行なし。

## Source limits / unresolved
合成Power, spawn witness, Unit/Troop identityは実ゲーム観測した値ではない。`MODEL_G2_SYNTHETIC_EQ`は旧ゲームのG2受入やstrict MATCHではない。

## Next permitted validation
同一合法runのG0/G1実バイト/SHAとG2実MAP/3 Powers/ordered Unit+Troopを入手後、証拠付きmappingでfixture適格性を判定。

**KB_CANDIDATE only.** Native/static source findings belong to their original B/REA owners; this E publication preserves only E-owned comparison rules and corrections. Do not upgrade SYNTHETIC/STATIC to real-game Golden or READY. Do not retry previously refused source operations or guarded VA 0x5710C0–0x571500. No user worktree/develop/REF/dictionary changes.
