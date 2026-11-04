# B-20261027-2315-T028-COUNT-QUEUE-MODE-BRANCH-01 — MORALE_RETREAT_RESULT (historical B owner source, NOT CURATED)
Research ID: `B-20261027-2315-T028-COUNT-QUEUE-MODE-BRANCH-01`
Owner / task: B / T028,T013,T024
Source: `_REDEV_RESEARCH/data/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md`
Source SHA-256 (2026-11-02 authorized PC independent Get-FileHash, source Markdown): `8C7354AB542866963C555805C04BDDB2790F2B1E88D3570EB702F2C36FF7FB17`
Target original static PE SHA-256 (2026-11-02 rechecked): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
Ghidra unified V9 SQLite SHA-256 (2026-11-02 rechecked): `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
Review: 2026-11-02 17H JST, source document original read only; this sanitized abstract is NOT an independent re-decompilation, gameplay capture or guarantee of all report native claims.
Evidence class: HISTORICAL_SOURCE_STATIC / PRIOR_NATIVE_STATIC_WHERE_NOTED / INFERRED / VERIFY.
Stage: owner GITHUB_STAGED; PUBLISHED_INTAKE only after exact GitHub readback; NOT_CURATED.
Original gameplay Golden PASS: 0; strict MATCH: 0; new formal READY: 0; current G4 result settlement: NOT PROVEN.

## Research meaning, limited to source evidence
Pre-battle count queue initialization precedes branch on manager+0x1EED43 mode byte in bounded original PE CFG. Two 0x521D90 paths pass common manager with mode 0/1, while 0x491870 passes already stored mode. Neither branch demonstrates actual death/morale changes.

## Evidence provenance and address links
Owner report NEW CALLERS/INIT BEFORE BRANCH and native byte checks 5/5: 0x4921CD→0x4922A0, 0x522297→0x4922A0, 0x5222AA→0x4922A0, 0x4923F5→0x5B6C2B, 0x49244E→0x432EE0. Prior PE slice 0x4923BA..0x4923F2 len56 SHA 59A4E51FCD5412A653B872A4B0E1B705614B755682DD8A0BC83833E2ABC2A6C8.
- VA (source-reported, not automatically verified function boundary): 0x4921C4;0x4921CD;0x522286;0x522297;0x5222AA;0x4922A0;0x4922E3;0x4923BA;0x4923F1
- Fields/offsets: manager+0x1EED43;manager+0x1EEFA0;manager+0x1EEFA4
- Prior / correction / dedup: B 20261027 21H and 22H prior queue/clear observations, IDs to reconcile (not new facts)
- Unresolved evidence: Queue consumer/clear lifetime, manager identity, mode meaning, game original deaths or morale and G4 external result settlement VERIFY. No dynamic result.

## Safe curator continuation
Curator verify original PE windows/V9 native calls and queue-clear-before-mode branch; only narrow order semantics eligible for STATIC.
Selectively compare this research ID, actual PC report SHA, original PE / V9 / DAT evidence and supersedes/errata against current private develop REF/symbols/structs. If independently validated, curator may admit only the bounded proven semantics; this owner PR must not be bulk merged. The old source document may discuss other preexisting refused work; this summary intentionally contains no refused content or protected native capture. No original EXE/DAT/MAP/SAVE/ZIP, other owners, develop, dictionaries or MASTER changed.
