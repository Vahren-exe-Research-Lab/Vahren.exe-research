# Memory reader/writer relation review

Review scope: repository prose already published at the supplied 14b3cbc baseline, for the ver0.67 function/memory encyclopedia. This review does not inspect the original game, binaries, native instructions, SQLite, external report originals, or excluded/withheld paragraphs. No new runtime confirmation, Golden result, compatibility claim, or ownership/type discovery is made.

## Result

Appended **86** relationships to the existing 28: **67 reads, 19 writes**, for **114 total**. The original 28 lines are byte-preserved; their SHA256 is `3a272a1b24ebaced51274e38a63daaf2914419d841a06a86fdbfc4baa67ac4c0`.

| Canonical owner | Added relations |
|---|---:|
| UnitDef | 52 |
| Power | 17 |
| Spot | 10 |
| Ctx | 5 |
| GameTask | 2 |

## Accepted claims and evidence policy

Each new JSONL entry records an existing registered function and field endpoint, a source file SHA256, and one contiguous inclusive line interval. The interval contains the exact function VA, the field offset/owner context, and the stated operation. A save table row's interval begins at its section heading because the heading identifies the serializer and record owner; it ends at the relevant row. The format supports one interval, so these include intervening table rows instead of inventing a multiple-interval schema.

- **57 serializer reads**: 0x58EFD0 reads 32 registered UnitDef fields, 0x598CE0 reads 9 Spot fields, and 0x596AA0 reads 16 Power fields. REF_SAVE_FORMAT section 4 explicitly identifies its Unit record with UnitDef; sections 5 and 6 explicitly identify Spot and Power. A serializer writes the save stream by reading these in-memory fields. No write to the in-memory field, loader inverse, separate initialization, or save-format runtime success is inferred.
- **10 other reads**: UnitDef_GetField reads class and scenario name; friend generation reads tag/class, current collection and size; training count reads Power+0xD8; the frame loop reads GameTask+0x78; the personality path reads Ctx player-unit/player-power guards.
- **19 writes**: roaming assigns/clears/moves the destination, resets eight explicit fields, and adds/removes entries in Ctx+0x32C; definition creation explicitly sets tag/race/class; friend generation reconstructs its collection; Spot capacity initialization applies the documented fallback/upper bound; frame-period configuration sets GameTask+0x78.

The UnitDef+0x168 relation is a read of the existing aggregate stats field, whose table row enumerates its member offsets. No new field is invented for experience+0x16C, threshold+0x170, or money+0x174, and no interior-offset occurrence is treated as a separate canonical field. UnitDef+0x160 is read as the friend count, but is not claimed to be serialized as a separate scalar.

Confidence is historical static evidence only, including where the original report says CONFIRMED. Power+0x40 keeps an explicit inferred/unknown-meaning qualification. UnitDef+0x79, UnitDef+0x7C, UnitDef+0x130 and Power+0x60 receive only their documented operation; their unresolved game meaning is not promoted. The old findings section 26 description of +0x78 as a neutral leader is not propagated: the later canonical correction calls it the troop-leader flag. Its explicit reset-to-zero operation remains usable.

## Deferred or rejected claims

- **Eight Spot initializer candidates omitted**: +0x00, +0xB0, +0x80, +0x84, +0x2C, +0x48, +0x8C and +0x90. Findings section 58 names wrapper 0x467260, constructor 0x5971A0 and initializer 0x5972E0 before an aggregate assignment list. That paragraph does not unambiguously attribute every assignment to one function. Only capacity+0x88 is retained, corroborated by the existing 0x5972E0 function definition. No relation is added from the wrapper, which is not an available function endpoint.
- Per-field loader writes from the save tables: their detailed rows are explicitly in write-out order; serializer reads alone do not prove each loader store or its fallback/correction behavior. Existing TurnState relations are preserved without extending this inference.
- UnitData / UnitDef / runtime Unit identity: no new blanket alias or identity is asserted. Findings' explicit definition context and REF_SAVE_FORMAT's explicit UnitDef identification support only the accepted definition operations. EXP/summon ownership and lifetime claims remain deferred.
- Training's UnitData+0x16C/+0x170, skill+0x2B0, leader memo node+0x10: no exact canonical field endpoint exists, and a raw offset or nearby aggregate is insufficient to manufacture one.
- AI candidate/group/record fields and coordinate objects, including +0xA14, +0x28, +0x1BC and +0x50: owner/type uncertainty remains. No Unit/Troop identity is inferred merely from compatible offsets or callers.
- Header preparation field reads: REF_SAVE_FORMAT gives internal sites such as 0x45F9AC, but not the owning entry VA in the same concise paragraph. No per-function header relation is added by guessing containment.
- Power personality writes to +0x20, GameTask/app fps+0x74, and additional callback/constructor operations: concise prose is insufficiently explicit about the exact store or receiver identity for a new edge. Only the explicit reads/frame-period operation above are retained.
- Excluded VA ranges 0x5710C0..0x571500 and 0x58021E..0x580340, VA 0x5769B0, and downstream 0x5767B0 claims remain outside this review. No accepted source interval contains those VAs or a withheld paragraph.

## Source receipt

Only the following files supply new relationship evidence. The screened findings file is a partial recovered copy, not the original report; its SCREENING.json/README limits continue to apply. This review manually checks the cited snippets, not the whole recovered corpus.

| Published repository source | SHA256 |
|---|---|
| [REF_SAVE_FORMAT.md](../../REF_SAVE_FORMAT.md) | `ab8ad91a089936864ce06657fd35decb1a9fa2e65a437ffa1f88c85323026366` |
| [REF_UI_SYSTEM.md](../../REF_UI_SYSTEM.md) | `657781d377f4dc52c3d7c6a048258417e8baa97378eff891dde7ce59d932a11c` |
| [REF_UNIT_EXP_SUMMON.md](../../REF_UNIT_EXP_SUMMON.md) | `a7f4d4ca196ed68b59d57e51692cb51c966c62ff0fba78c37b35e4b3da30d797` |
| [research/recovered/findings/PEER_SCRIPT01_FINDINGS_20261011.md](../../research/recovered/findings/PEER_SCRIPT01_FINDINGS_20261011.md) | `6c61b104076363710e09535c6db62daedbe0f0ee159a6ce3240aceb4f417d2d8` |

## Validation

- reference.load succeeds: 482 symbol endpoints, 107 field endpoints, 114 relationships.
- All 86 appended entries have unique IDs and unique subject/predicate/object triples; their endpoints exist. Source checksums and inclusive line bounds pass the repository loader.
- All 86 source intervals contain the literal subject VA and pass the excluded-VA/withheld-paragraph scan. Representative field/operation checks include 0x58EFD0 -> UnitDef+0x1C (read), 0x596AA0 -> Power+0x40 (read, meaning inferred), 0x460E90 -> UnitDef+0xC0 (write 100), 0x460F10 -> Ctx+0x32C (remove), 0x586320 -> UnitDef+0x160 (read), 0x595320 -> Power+0xD8 (read), and 0x4C21F0 -> GameTask+0x78 (write).
- The original 28 relationship lines retain their original bytes and checksum. No generated reference pages, dictionary fields, or builds are produced by this task.
