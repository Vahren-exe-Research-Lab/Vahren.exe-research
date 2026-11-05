> **2026-11-01 P0 RECOVERY ARTIFACTS RETIRED:** The historical game_copy, recovery delta ZIP, and two restore helpers are now in Windows Recycle Bin, not runtime. Original distribution and current playable/diagnostic installations remain unchanged. The original ZIP alone cannot reproduce the seven P0-only saves and one research DAT. See runtime/GAME_COPY_RECOVERY_DISCARDED_20261101.md. The P0 experiment scripts cannot run before restoration.

> **2026-11-01 P0 STORAGE UPDATE:** The old runtime/game_copy is no longer at its original location; it is in the Windows Recycle Bin. The original full game distribution ZIP plus runtime/game_copy_delta_20261101.zip were SHA-256 checked to reconstruct all 14,370 files. **Do not run old P0 hook scripts until explicitly authorized to restore.** See runtime/GAME_COPY_CLEANUP_COMPLETED_20261101.md. G1-G6 research status is unchanged.

# P0 battle takeover handoff — 2026-10-24

Research ID: `P0_TAKEOVER_20261024_01`. Status: **IN PROGRESS; native bounded NOOP roundtrip observed; full replacement not established**.

## Identity and ownership

- EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
- V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. Explicit V9 verifier returned `V9_INDEPENDENT_READBACK_PASS`, 11,950 functions / 243,678 references / 51,214 native callsites. V9 is composite SQLite; not a unified Ghidra project. Do not use default V3 `search_current.py`.
- Primary existing index: `../BATTLE_BRIDGE_RESEARCH_INDEX.md`. Only root updates this index. No edits to original EXE/DAT/MAP/SAVE, existing Ghidra/SQLite, E-owned MASTER or other lanes. Original data copied physically into `runtime/game_copy`; current user-operated test PID39496 is this copy. PID is historical, revalidate path and SHA before every attachment.
- A/B/C/F/G: `entry/`; D/E: `scheduler/`; H/I/J: `exit/`; K/L: `ipc/` and `evidence_audit/`; M: root runtime; N: `review/`. Four concurrent slots used, with follow-up tasks covering the fourteen specialties. No duplicate whole-binary decompilation.

## Read these results first

1. `BRIDGE_CONTRACT_DRAFT.md`: candidate hook/ABI, data ownership, transaction design, unsupported cases.
2. `entry/ENTRY_FINDINGS.md`, `scheduler/DE_SCHEDULER_FINDINGS.md`, `exit/H_I_J_EXIT_RESULT_CONTRACT.md`: V9 and original instruction evidence.
3. `review/N_NATIVE_RECEIPT.md`, `review/N_NATIVE_RECEIPT_VERIFICATION.json`, `review/N_SHARED_POINTER_ALIASES.json`: independent first native run audit and instrumented caller limitation.
4. `runtime/runs/20261024T005426_10cf1dfb/NOOP_NATIVE_SUMMARY.json`: bounded external-worker roundtrip evidence. Independent review is a separate artifact, not implied by this summary.
5. `exit/EXTERNAL_NOOP_SETTLEMENT_FEASIBILITY.md`: why directly invoking finish at the candidate task slot is currently NO-GO for G4.
6. `ipc/G6_FAILURE_CONTRACT.json`: failure phases and recovery limitations; synthetic worker exits are not native OS crashes.

## Native evidence achieved

First observation: `runtime/runs/20261024T004450_4e1f3594/completed_battle_prefix.jsonl`, SHA256 `07323F3F4219E65A82E33635239AAD334CDB34E52264E9383F9B748AB719C755`, 21 events. Same game thread38988. Activation completed in task pass1349; C1 candidate at index0 before the first observed Unit update. A Unit then updated in the SAME pass, before the next battle tick. This proves that delaying interception until the next battle tick or Task pass is too late in this case. Start331 Units (144/187/0); finish533 (299/234/0), 498 unique shared records. Seven non-null shared-record alias groups cover42 Units. Never use shared record alone as a unique Unit ID.

NOOP: `runtime/runs/20261024T005426_10cf1dfb/completed_noop_prefix.jsonl`, SHA256 `4FEE362C97CAB46780CF5C695A9F375BD0ED4DB3DCDDA8308081C904EE634FB2`, 27 events. One request and matching external worker receipt, native Wait result0, elapsed98ms, sampled state digest unchanged, sampled tick/first-Unit indicators0→0. Packet206 Units (84/122/0). Original battle subsequently ran1400 observed ticks; native finish returned; task observer later recorded mode1/active0. This establishes a bounded NOOP transport roundtrip in one normal battle, not battle replacement, all-writer quiescence, new-result commit, or save/load correctness. Communication wait argument500ms excludes snapshot work and is not a hard total wall-time guarantee.

Source hashes: first observer's saved raw source contains CRCRLF; one CRLF→LF normalization matches the actual injected logical source hash. Preserve both identities (`review/N_NATIVE_RECEIPT_VERIFICATION.json`). NOOP source is saved with explicit LF and should hash byte-exactly to its injection receipt.

Independent NOOP audit: `review/N_NOOP_NATIVE_VERIFICATION.json`, 30/30 checks. Native recovery trial: `runtime/runs/20261024T010904_4487298e/completed_recovery_prefix.jsonl`, 27 events, SHA256 `32DD57CDB39103200C0B8B93B9AD90F42E7BF5CE4B0D4BAD7FFC933E86CBF712`. Worker exited before ACK; native wait returned258 (timeout), elapsed504ms measured from before emit, capture-inclusive interval877ms. Sampled pre/post digest equal, tick/first-Unit indicators0→0, same-pass continuation,702 observed battle ticks, natural finish, then mode1/active0. `ipc/RECOVERY_NATIVE_VERIFICATION.json` independently checks36/36 conditions. Separate read-only worker exit query returned91; image-path query failed and creation time was not cross-checked, retained in `WORKER_EXIT_READBACK.json`. Host receipt originally had null exit code; do not rewrite that record. Classify as limited controlled-worker-exit fallback, not OS exception/SEH or complete G6 recovery. Controller detached after world return; no target kill.

Post-recovery save/load sequence was user-operated: save unused slot4→load4→save unused slot5. Copies and initial comparison are in `runtime/save_roundtrip/`. Both files parse/repack completely (5468 Unit records,138 Spots,30 Powers); numeric records and Spot/Power group hashes match. Unit group grows66 bytes and one unknown header scalar changes15→16. Until record-level differences are explained, do not claim exact or semantic G5 equivalence. A post-load read-only sample shows mode1/active0 and Task counter2869→2873. This is a save/load test after native fallback, not after external result commit.

## Gate status as of the successful NOOP

| Gate | Status | Evidence / remaining requirement |
|---|---|---|
| G1 exact start information | PARTIAL | Same game-thread roster/selected state obtained. Runtime MAP, full required VM/RNG state, definition IDs/generation and other-writer exclusion incomplete. |
| G2 safe hold/resume | PARTIAL | One short sampled-state-preserving wait and continuation observed. Long battle hold, UI responsiveness, original SEH/EFLAGS and all writer/lifetime constraints unproven. |
| G3 external NOOP roundtrip | PASS, BOUNDED SCOPE | One identified request/echo/event/native return. Original battle still runs after return. |
| G4 external result exactly once | NOT PASSED | No new result written. ACK dedupe is not result commit. Finish caller/Task/VM and casualty writer contract unresolved. |
| G5 world + save/load | PARTIAL | Native world-mode return observed. No post-bridge save/load semantic Golden comparison. |
| G6 failure recovery | PARTIAL; limited native fallback observed | Controlled worker exit before ACK, timeout, unchanged sample, continuation and world return; independently36/36. OS crash/SEH, interruption, long hold and partial commit recovery remain unproven. |

## Safe resumption instructions

Do not start a second observer while `runtime/ACTIVE_RUN.json` identifies a live controller. Read that run's events and validate its PID/path first. The successful NOOP controller was stopped only after `world_return_task`; it detached without killing the user-restarted game. A later run may supersede it. Follow the latest gate JSON / run identity, not this historical PID alone.

Controlled worker-exit experiment is now completed in the run above. Do not repeat it just to reconfirm the same observation. Cleanup must defer while a wait is pending; closing the waited handle is not a recovery method. Latest active-run metadata can point to a stopped historical run; inspect final controller_exit/detached evidence and process status before interpreting it as active.

Next substantive replacement experiment: instrument Task active/pending membership and lifetime plus native finish→43360C→43361B/VM/world order. Identify a continuation that can commit without resuming stale Unit slots. Do not invoke493630 from4C2935 merely because its argument ABI is known. Independently establish casualty/EXP pre-settlement writers before any HP/EXP/death mutation.

Unknown/partial commit must never be replayed automatically. Preserve raw evidence, source hash, exact phase and restart point. No success is inferred from silence, user-visible return alone, a synthetic test, or a function's return value.
