# Recovery native independent verification
Research: P0_TAKEOVER_20261024_01; run: 20261024T010904_4487298e.
Status: PASS_LIMITED_WORKER_EARLY_EXIT_TIMEOUT_NATIVE_CONTINUATION. Checks: 36/36.
EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187.
V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE.
Frozen 27-event prefix SHA256: 32dd57cdb39103200c0b8b93b9ad90f42e7bf5ce4b0d4bad7ffc933e86cbf712. Final log has29 events and exactly extends it.
Primary machine-readable receipt: RECOVERY_NATIVE_VERIFICATION.json; all source hashes, checks, positions and limitations retained.

The prewarmed worker PID36960 received the correct source/battle/digest envelope with synthetic_only=true.
Its log reports synthetic_crash/before_ack; receipt has zero ACKs and remains outcome_unknown, exit_code_at_receipt=null.
A separate saved OpenProcess/GetExitCodeProcess readback reports exit91 for PID36960.
That readback has path_query_ok=false and an empty executable path. PID matches prewarm, but path/creation-time identity was not independently completed. This limitation is preserved.
The unchanged worker code returns91 before ACK/OpenEvent/SetEvent; this is controlled early termination, not an OS crash or SEH exception.

C1 at originalVA004C2935 (rebased 0x982935) was eligible: pass6975, slot0, count399, tid38988, no first Unit yet.
Wait result258, reported interval504ms; entire gate through postcapture877ms. Reported interval includes emit overhead and is not a direct API-only timer or hard wall-time guarantee.
The pre digest d825c2ffcd5f839b3e100d321ec4606e721372ec3345a960a82a9525cfa77c4f was reconstructed from saved start roster and gate state/counter. The observer reports the same post digest; post raw object was not saved independently.
Observed Unit/tick counters stayed0 during hold. The original slot1 followed, then first Unit on the same pass and first tick on pass6976.
Natural finish at702 accumulated ticks returned through originalVA0049303F; active became0 and later mode1/active0 was observed.
Final log records application-requested detach and controller_exit with user_process_killed=false.

Scope: limited controlled worker early-exit -> native timeout -> original continuation -> natural battle finish.
Commit state NOT_STARTED_NOOP; reason enums WORKER_EXIT_BEFORE_ACK and NATIVE_WAIT_TIMEOUT.
No external result was applied. Full G6, OS crash recovery, partial/unknown commit recovery, and nonblocking UI remain unproven.
Original EFLAGS/SEH and full MAP/VM/RNG/all-thread state remain unproven. Unit hook records first update only; tick count702 is aggregate with only first3 ticks emitted.
Parent-owned recovery JS now guards pending-wait cleanup, existing event collision, and WAIT_FAILED error reporting; prior G6 notes describe earlier NOOP revision and are not silently rewritten.
This audit only reads existing evidence and writes ipc receipts: no native operations, shared edits, raw changes, or synthetic reruns.
Resume: retain this limited receipt; future failure variants and result commit phases need separate evidence.
