# E-AUDIT-20261030-18H-T020-T013-RANGE-UNIT-GATE-01
Status: STATIC / ORIGINAL PE BYTE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY (2026-10-30 18H JST)
Owner: E/T020. Source B ID: B-20261030-18H-T013-MODE2-RANGE-INSERT-UNIT-GATE-01 (B/T013/T024; VERIFY / NOT READY).
B detail: data/T013_MODE2_VECTOR_RANGE_INSERT_UNIT_GATE_NATIVE_20261030_18H.md; actual SHA256 93D24D9B087A7645CBF4EDA00EDE5FF26D8013DAD6902A648B6BFE3497D537E9.
Original research PE copy: rea_lab/targets/hakushin067_Vahren.exe; actual SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (2,910,720 bytes).
Current index is V9 by rea_lab/headless_analysis/CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json. Historic 2026-10-21 search.sqlite is not canonical since 2026-10-29; no Ghidra rerun, no search-index write.
## Independently reproduced native bytes (read-only PE)
- Window 0x44D730..0x44D875 exclusive: SHA256 65CFBA51FC736C8169F2730E586C6D255CCEB283453F255A67F5D84BE00877A9, B match.
- Window 0x5690C0..0x56913C exclusive: SHA256 9959940835B8511ED4AFC92FAB7861E95B27165FA636C87B9B84980E4E9FC219, B match.
- Direct E8 CALL displacement 6/6: 0x44D773->0x4634F0, 0x44D7E3->0x42AC20, 0x44C3C3/0x44C541->0x5690C0, 0x5691F9->0x5B6EAB, 0x569212->0x5D1B80.
- Native return bytes 0x44D8DA C2 10 00 (callee pops 16), 0x56927D C2 08 00 (callee pops 8): 2/2.
- Native evidence therefore disproves treating 0x44D730 as a simple 3-argument function; use an ABI-compatible 4-stack-argument model, but the exact higher-level types remain VERIFY.
## Newly executable E-owned T020 acceptance
- tests/t020_e_t013_mode2_range_unit_gate_20261030_18H.py and immutable-on-rerun JSON fixture tests/T020_E_T013_RANGE_UNIT_GATE_CASES_20261030_18H.json.
- Unit gate 32/32 synthetic: Unit+0x8C zero / +0x1F8 nonzero / +0x1F9 nonzero, candidate NULL or nonNULL, abstract byte flag 0/1. Early-return no +0x48 write vs early-return +0x48 write vs general path with write; do NOT pretend to know downstream full effects.
- Vector gate 20/20 synthetic: range lengths 0/1/2/4/32768 and manager+0xA7 flag, first and reached-second stage; empty vector suppresses shuffle call; actual second-stage reachability is UNKNOWN.
- Unsupported inference guards 12/12: +0x58 type, early-return stale value, vector alias, always-reached, final targeting, RNG count high-n, recipient identity and gameplay PASS are UNKNOWN/INELIGIBLE.
- New 64/64 PASS on initial run AND independent repeat; 17H previous synthetic 56/56 independently rerun; this run 120/120 synthetic, report cumulative 809+64=873 (NOT all 873 rerun). Script validates PE SHA, B source SHA, native windows, CALL E8 and return ABI bytes before checking synthetic fixtures.
## T018 / T019 / T020 / custody
- G0 lawful unmodified-original UI start; G1 SAME battle pre-start untouched SAVE bytes/SHA and timestamped input; G2 SAME battle actual MAP bytes/SHA, attacking/defending/support sides and ordered deployed Unit/Troop; G3 fight result and G4 returned World state delta, each with run/time/PID/asset provenance. No same-battle joined evidence currently: DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0. The 2026-10-22 karate x20 test-DAT history requires proof of restored unmodified DAT before accepting any Golden.
- T019: no newly established contradiction. GameClear DAT13 vs TXT2 source-scope RESOLVED; script2 winner/phase flag, TXT runtime load, gwrite resume, decide11 remain VERIFY. 64 tests only simulate native branch gates; original game NOT RUN, native Unit effect lifetime and real AI target UNKNOWN.
- MASTER: latest directly read/hashed E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3; final formal cp196, READY596 A115/B229/C136/D116. 34 TASK QUEUE rows directly counted DONE9 / IN_PROGRESS21 / VERIFY4. New READY integrated 0; B18 NOT READY; MASTER unchanged. A/C/D no new final handoffs beyond prior records in latest tails; no cross-owner write.
- Refusals: B-RC-20261030-1115-T028-T013-APPEND-SAFETY-01 (three B summaries) BLOCKED. Prior E T018 table boundary/session join/T019 XREF, C T026/T032, D T030 TSV, VA0x5710C0 and other refused payloads untouched; no alternate tool/path/shell/Remote/ZIP retries. Old OFFLINE-UNSYNCED reconciliation remains OPEN.
- Original PE/ZIP/DAT/SAVE and A-D/REA/dev_lab/Git/Work/settings/automation not modified. Only E-owned new T020 files were written; no official READY.
- Next: inspect B 0x5690C0 recipient ECX producer, 0x579AA0 and range iterator element identity using approved read-only evidence, design original observable 0/1/multi candidate transitions and same-run G0-G2 receipt, never infer implicit RNG or final selection.
