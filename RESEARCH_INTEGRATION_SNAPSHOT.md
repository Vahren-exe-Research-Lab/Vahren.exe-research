# Research source integration snapshot

This is a metadata inventory, NOT a validation of all research findings.
GitHub does not contain original game files or the generated search database.

- Indexed research documents: 1823
- Indexed lines: 1,157,937
- Indexed VA mentions: 142,454
- Catalog source receipts: 1823; missing: 0; stale SHA/size: 0; redacted path entries: 0
- Exact-byte duplicate groups: 18, total referenced files: 38
- Shared-primary-ID candidate groups: 144 (NOT automatically duplicates)

## Automatic tentative classification

| Category | Indexed sources |
|---|---:|
| AI_TARGET | 289 |
| GOLDEN_QA | 282 |
| BATTLE_DAMAGE | 233 |
| SCRIPT_VM | 216 |
| UNIT_SKILL_EXP | 188 |
| GHIDRA_INDEX | 179 |
| MORALE_RETREAT | 98 |
| UNCLASSIFIED | 89 |
| STRATEGY | 62 |
| SAVE | 46 |
| RTS_UI | 34 |
| IMPLEMENTATION | 29 |
| COORDINATION | 24 |
| RNG | 20 |
| EVENT | 15 |
| OTHER_TASK | 13 |
| ENGINE | 6 |

## Review rules

1. Cross-check research IDs, original ASM/DAT and prior corrections before extracting conclusions.
2. Duplicate SHA means identical content only; duplicate ID can be an expected detail/HANDOFF mirror.
3. Never upgrade STATIC, INFERRED, VERIFY, DYNAMIC or Golden/READY based on metadata.
4. Do not import blocked/refused source payloads or analyze the prohibited address range.
5. The catalog is intentionally paths/SHA and task suggestions; it cannot replace local source files.
6. The search index excludes binaries and over-limit documents, so this is NOT full project backup.
7. Review domain guesses, especially multi-task files, before publication as verified facts.
