# B historical source intake — effect pool vtable +0x04/+0x24 maps to delayed tick and helper paths

- Research ID: `B-20261027-08H-T013-EFFECT-VTABLE-TICK-JOIN-01`; tasks: T013/T012.
- Authorized PC source report: `data/T013_EFFECT_VTABLE_TICK_JOIN_NATIVE_20261027_08H.md`, independent source Markdown SHA256 `BC7C1A54F77F2C345A73C7DFFF6B05472B000EA0B7F43886BA8C9CCE2CADD1AF` measured read-only 2026-11-02.
- Owner B; original 迫真戦記 ver0.67 original isolated PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`, unified V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (both independently rehashed on authorized PC 2026-11-02, read-only).
- Evidence stage upon GitHub readback: **PUBLISHED_INTAKE / NOT_CURATED**. Historical ID, no new discovery or new formal READY; original-game Golden PASS=0 / strict MATCH=0 / DYNAMIC=0. Source report bytes verified, but not all reported native facts independently decoded.

## Bounded evidence / corrections / limitations
- **Independent original PE .rdata window this run:** `0x63A604` 80-byte SHA256 `DB55B9F0991DA21C7914F4E196FAC413BB9929FC7F7A3AE736A75D4DE6484C2B` matches historical owner source. The vtable DWORD at `0x63A608` (table+0x04) points to `0x54E420`, and DWORD at `0x63A628` (+0x24) points to `0x54E3F0`.
- Owner report identifies two effect-pool record constructors `0x550B3B` and `0x550C29` storing vtable base `0x63A604`. Previous B research already covered the pool, `0x54E420` body and `0x54E3F0` item-choice helper; do **not** count these as new native functions. This ID contributes the static **vtable slot-to-function relationship** and owner constructor crosslink.
- Prior native report sites `0x54E4A3` and `0x54E595` E8→`0x551490` are source-owner evidence not re-disassembled in this intake. `0x54E0B0` direct core and `0x54E420` delayed path are distinct and should not be collapsed.
- **Critical VERIFY:** the existence of vtable slots does not prove the engine calls slot+0x04 in battle, nor that any delayed effect reaches real HP/MP/EXP/target state or G4. Return ABI, effect lifetime and dynamic tick callback remain unresolved.
- **Next:** a lawful bounded V9/callsite analysis for virtual slot dispatch and actual old/new gameplay Golden before advancing formal READY.

## Curator selective-adoption gate
Check source report SHA and original limited ASM/DAT, existing research IDs and supersedes/errata, and the current develop REF/symbols; only independently validated STATIC facts can be curated. Do not treat a search match or owner report as gameplay or full ABI proof. No original EXE, DAT, MAP, SAVE, ZIP, private logs, refused source or prohibited region included.
