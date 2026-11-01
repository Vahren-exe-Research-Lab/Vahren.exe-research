# E/T020 — Unit latch clearing: two native callers (offline research intake)

- research_id: E-OFFLINE-20261101-0549-T020-T013-DUAL-CALLER-LATCH-CLEAR-01
- owner: E; tasks: T020 (T018 Golden acceptance), T019 contradiction screen; T013 is B-owned, read-only reference only.
- observed_at: 2026-11-01 05:49 JST; source_snapshot: 2026-10-21 original-index ZIP, not current PE reanalysis.
- source_relative_path: Library/T020_T013_DUAL_CALLER_LATCH_CLEAR_AUDIT_20261101_0549.md
- source_sha256: 77D745B48233A4C4C10C7CE12B4192E4622C68FA7ED66DC42E742930F55FBCC1 (2026-11-01, source bytes freshly measured on materialized Library file).
- source_exe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (historic index manifest; **not** freshly measured original EXE).
- evidence_kind: STATIC_SNAPSHOT + SYNTHETIC + VERIFY; DYNAMIC: 0; golden_status: original actual PASS 0 / strict MATCH 0; ready_status: NOT READY / intake only.
- prior_ids: E-OFFLINE-20261101-0351-T020-T013-SCAN-RECT-VCALL-GATE-01; E-OFFLINE-20261101-0453-T020-T013-THREE-CALLER-RETURN-USE-01.
- kb_candidate: Update existing Unit_RefreshTargetLatch references with caller-conditional clear/side-effect caveats, curator review only.

## Reusable bounded observations
A previously extracted pseudocode snapshot shows caller function 0x00545740, direct CALL site 0x00545A02 -> 0x004E53B0. After preceding return gates, if Unit byte +0x1867E == 0 and param_1[0x35] >= 0, its return value is stored to Unit +0x1E570; otherwise the examined local else sets that latch to zero. Caller 0x0057AA00 uses 0x0057AD8C -> 0x004E53B0, with an additional param_1[0x61AB]==0 condition. Its local success branch stores the return; when it is nonzero, a later inspected block increments param_1[0x14F] and clears param_1[24999]. These refer to offsets 0x1E570, 0x53C and 0x1869C if the pseudocode addresses an int32 array. Semantic field names, caller preconditions and indirect targets remain VERIFY.

Source pseudocode provenance:
- functions/0054/00545740.c, code SHA256 4BD1B725B04BA8B7EE47829A7026AE9B23D8840EF747B3BDB24CE4CC4D4890D1 (lines 122-153).
- functions/0057/0057AA00.c, code SHA256 5827D0DF895C261CB6CFB81ABCCC730BC7F31EC977FFA0411BDF466C51E978B7 (lines 163-231).
- functions/004E/004E53B0.c, code SHA256 1B74D266BE034E2984E3C4456EBE5CF5DAEBDCA07C8674A934EB34EF3F5CE1E1.
- Native E8 machine-byte identity was **not** rechecked in this offline study. Call edges are old Ghidra index records.

T020 synthetic local-block model: 128/128 expected cases PASS, 104 local clear / 24 local scan / 4 conditional counter-and-wipe cases; mutation checks 8/8. It models conditional branch blocks, not guaranteed function-entry reachability, Unit behavior or original gameplay. All real original G0/G1/G2 and strict comparison remain NOT RUN.

## Contradiction / curation / next
No newly confirmed Wiki/DAT/EXE contradiction. T019 GameClear DAT13/TXT2 scope difference RESOLVED; runtime script2 precedence and TXT load VERIFY. C-NB02 acceptance requires one lawful UI battle, same-run prebattle SAVE bytes and ordered inputs, actual MAP and three-sided Unit/Troop deployment. This static latch evidence is not a Golden receipt.

Source is Library materialization, not an owned original PC file; the authorized PC MASTER was online and read independently on 2026-11-01, with last official checkpoint196 / READY596 (A115/B229/C136/D116), 34 tasks 9 DONE /21 IN_PROGRESS /4 VERIFY as **old last-confirmed values**, not newly recounted. New official READY 0. Historical safety denials remain blocked; no denied operation/content is published or reproduced. Next: curator checks prior IDs and owner B/T013 overlap, then safely updates REF notes if justified; do not auto-create new symbols.