# B-20261025-2117-T024-POSTUNLINK-ZERO-TAILJMP-01 — Historical original x86 owner-key unlink / count-zero reset / tail JMP boundary
research_id: `B-20261025-2117-T024-POSTUNLINK-ZERO-TAILJMP-01`
owner: `B` | tasks: `T024,T028` | stage: `PUBLISHED_INTAKE / NOT_CURATED / VERIFY`
original_report_relative_path: `data/T024_SELECTION_UNLINK_RESET_TAILJMP_NATIVE_20261025_21H.md`
original_report_SHA256_measured_PC_2026-11-02_JST: `2BBFED167FE9FF5F1B7D8232D10EA2CE392837AA31930D03B68A8FCFD8B3945C`
original_target_PE_SHA256_measured_PC: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (2910720 bytes)
unified_V9_SQLite_SHA256_measured_PC: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (141033472 bytes; index provenance only)
evidence_kind: `NATIVE_STATIC_PRIOR / INFERRED / VERIFY`
Original-game Golden PASS: `0` | strict MATCH: `0` | new formal READY: `0` | new DYNAMIC: `0`

## Original owner evidence (historical, not new independent decode)
Prior B report locates 0x527ED0 / 0x4EC680 pointer-keyed unlink and decrement before Unit+0x34C zero test / Unit+0x45D reset candidate, distinguishes 0x527EA0 RET and 0x527ED0 RET4, and describes 0x5685C5 as tail JMP to 0x527EA0 after stack restoration. Legacy caller index incorrectly called the JMP a CALL. The exact native windows and current V9 CALL/JMP classification were NOT independently inspected in this run; no full ABI or runtime unit-death/G4 result proven.

## Provenance and correction
Earlier T024 19H / 20H results covered other count reset and caller paths. This ID records later unlink-count and return-kind refinements, not a second discovery of prior call sites. Source is the exact owner report above; no DAT source or original dynamic capture was used.

## Next check and safety
Curator may independently re-decode safe windows 0x5685C5, 0x527ED0 and 0x4EC680 from original PE and compare V9 metadata before selective REF adoption. Original-game behavior, ownership, ABI and G4 contract stay VERIFY, Golden=0.
Only sanitized B-owned summary; no raw EXE/DAT/DB/ZIP/SAVE, personal identifiers, refused payload/address body or other-owner files. Curator alone changes shared REF/TSV/develop. No bulk owner PR merge.
