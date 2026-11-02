# B-20261024-07H-T028-DEAD-EVENT-CONTEXT-REPLACE-01 — two death callbacks set dead_event_a/d then invoke event handler

**Owner/task:** B / T028,T013. **State:** safe historical owner report PUBLISHED_INTAKE, **NOT CURATED**; original-game Golden PASS 0, strict MATCH 0, new E-formal READY 0. Prior static/source confidence must remain bounded.

**Source:** `data/T028_DEAD_EVENT_CONTEXT_MAP_RANGE_REPLACE_NATIVE_20261024_07H.md`; actual authorized research-PC report SHA-256 `55221E3C283164072A32166B57EA6505F90B8A8A983BF8D1B4629906C82A1634` remeasured read-only 2026-11-02 (21H JST); line-level provenance: report lines 5–19 (original PE native CALL sites, prior V3 references, bounded writer/iterator relation). Original ver0.67 isolated PE SHA-256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; unified Ghidra V9 SQLite SHA-256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` independently remeasured as **identity only** (no new decompilation, ABI proof, original DAT byte-hash or game run).

**Previously reported allowed VA:** `0x544C5E`, `0x544CA0`, `0x578A91`, `0x578AD3`, `0x49CD60`, `0x49F1F0`, `0x49EE60`, `0x4321B0`. **Untyped related fields:** script context+0x1E0;candidate source+0x1C8;writer stack cleanup ret0x38. Addresses are references for source navigation, not independently reviewed claims this run.

## Narrowly reusable source statement

Owner-reported local x86 windows show two death callback routes storing `dead_event_a` and `dead_event_d` context values before a common event callback. The dictionary writer evidence includes range lookup/erase-before-insert behavior in its bounded path. Game semantics of attacker/victim identity, callback effects and persistence are unproven.

## Limits / correction / next independent validation

- **Prior evidence / dedup:** B-20261024-0616-T013-MAP-VECTOR-STRIDE-WRITER-01. This is one existing historical study ID, not a new discovery or an extra re-count of earlier CALL/refs.
- **VERIFY:** Source pointer type, key context ownership, callback reentry, stale-entry lifecycle and G4 external result semantics. No denied native content included.
- **Safe next step:** Curator selectively verify these pre-existing allowed callsite byte windows and script-key producer; G4 settlement boundary remains VERIFY.
- **Curator:** use `B_KNOWLEDGE_CATALOG.tsv` for study/source SHA/prior IDs and `B_VA_LOOKUP.tsv` for nonauthoritative allowed address mentions; compare against latest `develop` REF/symbols/structs, verify only safe native/source proof, select narrowly supported facts into the curator-owned isolation. No automatic meaning/ABI/DYNAMIC/READY/Golden promotion.
- **Safety:** No previously refused operation, native payload, protected-address bytes or alternate-route retrieval. Other owners, original game/source archives, MASTER, develop, shared dictionaries, Work and scheduled settings untouched.
