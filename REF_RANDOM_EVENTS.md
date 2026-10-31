# World random events and tea subgame — curated C/T031–T034

Scope: normalized original ver0.67 DAT command order STATIC-SCRIPT; native phase reader STATIC; gameplay outcomes and exact RNG stream VERIFY. Original-game Golden PASS=0, strict MATCH=0.
Owners: C/T031 and T032, C/T034. Source reports data/T031_RANDOM_EVENT_SCHEDULER.md, data/T032_RANDOM_EVENT_EFFECTS.md, data/T034_SHIMOKITANO_TEA_SUBGAME.md. Related World crosswalk in REF_DAT_BEHAVIOR.md.

## 1. Scheduler, pool and persistence
- World event calls randomset BEFORE checkturn/checktiming guard. Eligible player-end or new-turn nonmaster World entries, tutorial off, randomevon=1, turn<=60 increment randomevturn. Every fourth eligible World entry triggers selection; background-event same-turn reentry may increment it again. NOT strictly four calendar turns.
- Turn1 persists shuffled numeric ordinal fields randomevN and a monotonically growing cursor randomevnum, not the transient string array. A skipped/failed wrapper can advance the cursor again within the same trigger.
- Largest conditional pool has 51 slots/50 unique names. randomev10 appears twice (only final ordinal retained), randomev20 has no dispatch assignment, yielding two unselectable holes. Do not deduplicate or auto-fix these in strict compatibility.
- Independent randomev13 turn10 branch sits outside this pool. OFF choice does not prevent recorded pre-draw RNG work outside the ON/OFF selection. The rpo1=N/rpo2=4N source typo survives in strict behavior.
- A depleted cursor loop under edited/malformed state may not exit; no claim that normal original gameplay reaches the hang.
- Original normalized randomset.dat SHA256 12276C86F1E09733BA97122CCA524BD30C72B06131A7EE7FC81385D9B55017D1 and event_world.dat SHA256 523B389E2E985D3924D83246E076343F8AA1EA2C610044B1739E6792EB7E7D9A (current read-only source receipts).

## 2. Event effect catalog is a different layer
- T032 traces 49 schedulable active roots and independent randomev13: 50 root closures, not 50 original-game verified outcomes. Event/child conditions and randomevhappened determine whether the same trigger skips forward.
- Corrected inventory excludes block-comment drafts. Actual randomev31 is in randomev31-40.dat; a randomev71-80.dat copy is commented out. Cross-check source closure rather than Wiki counts.

## 3. Tea competition is an independent, source-complete special branch (T034)
- T034 source-level subgame is DONE, but native RNG/index/choice semantics and gameplay acceptance are not. randomev13 draws six contestants, with 3 competition rounds; scoring reuses the T026 tea-lesson evaluator, not a new arbitrary tea-scoring formula.
- Each guest round score includes base 50, teacher/student modifiers and dext difference. Comparison boundaries produce different dext gains at <150 / <200 / <300 / >=300; later rounds see updated dext, so scoring is stateful.
- Strict quirks: contestant 5 skips the Round3 1.5x score; a forced player bonus can be omitted from the accumulated ranking while CPU bonuses are added; first-place ties prioritize lower contestant numbers; winner1's second-place check for contestant3 repeats te4 and omits te5.
- Cancelling the representative AFTER accepting participation skips the main contest but still leaves net polip -45 and a three-turn action-lock route. This is source-code consequence, NOT a measured game bug.
- Original normalized randomev_tyakai.dat SHA256 1295BFDFDE47D295F7F722474103ACE47BF7F941A2AE3D5C87EAA9768DD73514. Source: data/T034_SHIMOKITANO_TEA_SUBGAME.md §§9-14; T026 scorer cross-reference.

## 4. Scope and next validation
- T031 scheduler, T032 per-root effects and T034 tea share state but have different acceptance gates. No increase of owner READY or Golden based only on this concise summary.
- P0: exact RNG/reseeding and shuffle stream, World reentry phase-byte writer and timing, normal-game cursor exhaustion, eligible tea-score/rank fixtures, VM event()/routine() Yield and original-game observed state.
- Never silently fix duplicate randomev10, absent randomev20, script typos, source-defined tie handling or instruction-order anomalies in a strict compatibility mode.
