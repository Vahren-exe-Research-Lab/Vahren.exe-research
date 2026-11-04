# UnitRuntime field review (proposal only)

Base requested: `a91676b`. Scope: already reviewed repository text only; no new native evidence, original research root, binary, linked native payload, or unscreened note was opened. Two additional reviewed report bodies were used (S09/S10), within the five-body limit. Source IDs below resolve to exact repository path, full SHA256 and line count in [source index](receipts/source_index.json); all cited ranges are inclusive. This directory retains the reviewed proposals as receipts; see Parent adoption below for the applied dictionary state.

## Proposed ownership boundary

`UnitRuntime` is a **descriptive research layout name**, not recovered RTTI or a proven original C++ class name. It names the live Unit-like pointer used locally by registered `Unit_PostHpTierRegister` (0x577100): EAX copied into ESI, followed by offset accesses (S03:L69-L72; S06:L4-L6). It does not alias an unqualified `Unit` globally and does not claim all Unit-named callees share one concrete base type.

The name is consistent with existing registered `vt_UnitRuntime` (S02:L240) and `Unit_ConstructSummonedRuntime` (S02:L234): constructor 0x56F880 writes 0x63A9E4 to [EBP], returns constructed EBP, and is described as normal Unit type (S09:L4; S10:L7-L11; S04:L53-L59). This is naming support, **not** proof that each 0x577100 input has this normal vtable. Neither the shared offset nor a common registration helper establishes class identity. Layout fields and proposed edges are qualified to this local pointer interpretation; downstream R/P/L owners stay separate (S03:L35-L39, L60; S06:L4).

`UnitDef` describes DAT/save records: notably +0x84 is a string whose length is +0x94, and +0x168 is the stored stat array (S01:L7, L11, L13). A live pointer also has a linked UnitData record at +0x1C8 in documented battle paths (S04:L93). No layout merge, `UnitDef` alias, or serialization meaning is proposed. Existing dictionary has no `Skill` layout row (S01 whole file); a nearby offset alone cannot supply it.

## Proposed fields and relations

Four fields in [proposed_fields.tsv](proposed_fields.tsv), with the same seven columns as structs.tsv: HP +0x90, HPmax +0xDC, HP tier +0x738, registration countdown +0x185F4. Five relations in [proposed_relations.jsonl](proposed_relations.jsonl), matching the existing JSONL schema. The only subject is **already registered function** 0x577100 (S02:L525). These are reads of HP/HPmax/timer and writes of tier/timer. Guard conditions and disabled/enabled behavior are retained. No field is made an absolute VA global.

The field confidence column is normalized to the dictionary schema value `静的確認` (accepted enum: 実機確認 / 静的確認 / テストのみ / 推定). The full qualifier "回収済み研究本文のみ。幅・具体的class同一性未確定" remains in every field summary. This is schema normalization, not a confidence promotion; detailed relation confidence remains unchanged.

All four types are `unknown`. FILD/FIDIV establish integer-memory use but this reviewed prose omits operand-size annotations; offsets do not prove widths (S06:L5; S03:L71). Signed clamp/comparison/decrement describes the operation on that path; it does not establish a declared signed type or width of the storage. No u32/i32 assumption is introduced for any field. Tier is an integerized clamped result, not a fractional HP store. Timer constructor initialization at 0x5707F9 is reported (S07:L4), but no constructor edge is emitted from address containment alone.

The countdown report gives a current correction/clarification: both enabled routes refresh 150, including timer nonzero which skips registration (S07:L4; S03:L72). The HP contract line6 already identifies the common 0x57720F write; its abbreviated skip wording must not be read as skipping refresh. Mode0 clears after unlink helper returns (S06:L4). Early guards can return without these effects.

## Deferred or rejected candidates

- **MP +0x94 and Skill +0x278:** S08:L4 records EDX = Skill+0x278 and Unit+0x94 -= EDX, supporting a local debit ordering observation. It does not establish the canonical Skill layout, operand identity provenance, or concrete normal Unit vtable at that handler. S08:L3 says it covers a normal handler region in 0x57EB40, while the registered symbol names an outer action dispatcher (S02:L137); no offset-containment-to-owner relation is proposed. These two fields and all MP relations are deferred, rather than treating UnitDef+0x94 as MP or inventing a Skill owner. EDX makes this reported operation 32-bit register based; a full declared field type, signed semantics and canonical owner still remain unproven.
- **Tick-consumer edges:** S07:L5-L6 supplies local paths at 0x57AB38 and 0x55AD80; no relation from the enclosing 0x57AA00 symbol or an invented 0x55AD80 function is emitted. The permitted source does not explicitly bind the former local range to that registered function owner; latter has no existing registered endpoint here. The differing death/inactive guards are retained in proof notes.
- **HP producer writes/HPmax producer:** the selected HP post body reads them; the caller references do not establish unconditional HP writes by 0x577100. No such relations are proposed.
- **Embedded registration record, guards, ring +0x185F8, context +0x1DC:** useful local observations, but outside the requested canonical field subset. R/P/L identity is not flattened into UnitRuntime (S03:L37; S07:L7).

## Confidence and holds

Confidence is recovered-report static description only; semantic identity of these offsets at 0x577100 is strong within that report, while concrete runtime class identity and widths remain unknown. The current work independently rehashes repository text, not the original EXE. Historical independent native receipts are provenance reported by S03/S04, not fresh validation by this task.

No ticking cadence, double decrement per tick, FPS/seconds conversion, 150-frame lifetime, visible HP bar, registration/Task success, downstream callee effect, or legal runtime reachability is established. HPmax=0, NaN/overflow, FPU rounding, every caller type, failure paths and same-seed original/new comparisons stay VERIFY. Original gameplay Golden PASS 0 / strict MATCH 0 / new READY 0 remain unchanged (S03:L74; S06:L10-L11; S07:L2, L6-L12). Existing source holds and refused-operation boundaries remain in force (S06:L11; S07:L11; S08:L13-L14; S09:L12). This proposal does not promote them.

The root dictionaries, existing 139/140 relations, generated outputs and Git state were not written by this subtask. See receipts for exact input hashes and validation results.

## Parent adoption — 2026-11-05

The coordinating task adopted the four fields and five relations after independent review. `structs.tsv` uses the existing confidence enum `静的確認`, with recovered-text-only / unknown-width / uncertain concrete-class qualifiers retained in every summary. Relations retain their per-claim explanatory confidence strings, as supported by `reference.py`; the four-value enum applies to the dictionary rows rather than the relation schema.

The old dictionary bytes are preserved as a prefix. Five existing dictionary citations (four correction records and one relation) were re-anchored only after exact original inclusive cited-line equality was proven. No existing field meaning or certainty was changed. The descriptive layout is queryable as `UnitRuntime+0x90` / `UnitRuntime+0x185F4`, without creating a global `Unit` alias.

The old Ghidra importer falls back to four-byte undefined storage for an unrecognized type. Unknown-width fields therefore must be excluded from the Ghidra structural export; they remain visible in the portable encyclopedia and machine-readable dictionary. Native execution, original-Golden validation and concrete class membership remain unproven.
