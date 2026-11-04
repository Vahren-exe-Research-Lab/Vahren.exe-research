# B-20261024-0317-T013-CASE8-KEY-PRODUCER-ORDER-01 — case8 key source selection precedes mode rejection

**Owner/task:** B / T013,T024. **State:** safe historical owner report PUBLISHED_INTAKE, **NOT CURATED**; original-game Golden PASS 0, strict MATCH 0, new E-formal READY 0. Prior static/source confidence must remain bounded.

**Source:** `data/T013_CASE8_KEY_PRODUCER_EVAL_ORDER_NATIVE_20261024_0317.md`; actual authorized research-PC report SHA-256 `0421E8D1C4E76675220A68706E6ED5CC3CF9688D4FBF2C7EF59194763452B338` remeasured read-only 2026-11-02 (21H JST); line-level provenance: report lines 5–14 (historical original-PE native window + V3/Ghidra corroboration). Original ver0.67 isolated PE SHA-256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; unified Ghidra V9 SQLite SHA-256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` independently remeasured as **identity only** (no new decompilation, ABI proof, original DAT byte-hash or game run).

**Previously reported allowed VA:** `0x4B595E`, `0x49C450`, `0x49C52E`, `0x49ECA0`, `0x4B5976`, `0x4B597E`, `0x49E8B0`. **Untyped related fields:** local output string [EBP-0x34];context+0x1EEBEC;candidate +0x14 source gate. Addresses are references for source navigation, not independently reviewed claims this run.

## Narrowly reusable source statement

Previously saved case8 code constructs a lookup key before evaluating the subsequent mode gate, with alternate direct-string and expression-reference paths. A zero/empty result candidate and inline/heap string treatment are observed only at these owner-reported sites; complete ABI/exception behavior and final Troop ordering remain VERIFY.

## Limits / correction / next independent validation

- **Prior evidence / dedup:** B-20261023-2317-T013-TROOP-MODE-SOURCE-CASE8-01;B-20261024-0015-T013-TROOP-MODE-EXPR-DEDUP-01. This is one existing historical study ID, not a new discovery or an extra re-count of earlier CALL/refs.
- **VERIFY:** Current V9 function and original input form, expression object type, empty-key branch side effects, case8 legal trigger.
- **Safe next step:** Check V9 only around preexisting caller sites, reconcile prior case8 sorted/variable-lookup errata and preserve exceptions as unknown.
- **Curator:** use `B_KNOWLEDGE_CATALOG.tsv` for study/source SHA/prior IDs and `B_VA_LOOKUP.tsv` for nonauthoritative allowed address mentions; compare against latest `develop` REF/symbols/structs, verify only safe native/source proof, select narrowly supported facts into the curator-owned isolation. No automatic meaning/ABI/DYNAMIC/READY/Golden promotion.
- **Safety:** No previously refused operation, native payload, protected-address bytes or alternate-route retrieval. Other owners, original game/source archives, MASTER, develop, shared dictionaries, Work and scheduled settings untouched.
