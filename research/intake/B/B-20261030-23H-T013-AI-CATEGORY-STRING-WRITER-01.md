# B-20261030-23H-T013-AI-CATEGORY-STRING-WRITER-01 — B historical targeting source intake

- research_id: `B-20261030-23H-T013-AI-CATEGORY-STRING-WRITER-01`
- owner: B
- tasks: T013 (T024 AI and T028 references, no ownership transfer)
- observed_at: 2026-10-30 23H JST
- source_relative_path: `data/T013_MODE2_CATEGORY_LABEL_AND_UNIT_WRITER_NATIVE_20261030_23H.md`
- source_sha256: `4fdcf334197b1b61d8a867db0a92ed8618354472e5ff0a4d9f07094caef13fe0` (authorized PC Markdown SHA256/byte size independently measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target, not a fresh EXE hash in this intake)
- evidence_va_call_offsets: `0x44CD4C and 0x449704 nine-way category tables,0x44C9AA→0x449500(2),0x4495F7..0x44963B,0x44CAE8..0x44CB1C,0x44CBD9/0x44CBE1→0x402800,0x44CBFD/0x44CC01/0x44CC09,0x4496C4→0x577220,Unit+0x1E4FC/+0x1E4F8`
- prior_ids_and_corrections: B-20261030-22H-T013-SUM88-AH41-01 category argument=2, earlier 21H branches and known label candidates; 2026-10-31 00H coefficients and 04H fan-out refine
- evidence_kind: historical STATIC native/callgraph / INFERRED, VERIFY for ABI/runtime/result; original DYNAMIC 0
- golden_status: original Gameplay PASS0, strict MATCH0
- ready_status: new READY0; E MASTER formal promotion0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; not CURATED

## Reusable source-grounded findings

Old original-PE byte evidence independently decoded two category-label tables `0x44CD4C` and `0x449704` with labels 0 hold,1 even,2 even,3 push,4/5 hold,6 advance,7 even,8 back. A `0x449500` call with argument category2 may preserve 2 for `manager+0x98>10` (label "even"), or rewrite it to 6 ("advance") at <=10 and perhaps 6→7 when separate group/manager flags require. Other entry uses category6/7. Qualifying Unit is checked via five gates `+0x1867C/+0x1867E` zero and `+0xC0/+0xC8/+0xD0` nonnegative; on accepted path `0x44CBE1→0x402800` assigns text-like Unit `+0x1E4FC`, while `0x44CBFD..0x44CC09` writes signed max of a computed RNG-related value vs Unit `+0x1E518` into `+0x1E4F8`. A separate call `0x4496C4→0x577220` reaches related label/wait logic. The table shows **text choice and parameter propagation**, not proof of a Unit executing movement/attack or original-game event timing.

## Cross-study correction (2026-11-05; existing B evidence, no new ID)

The **category label is not a unique numeric score or a single Unit selection**. Existing [00H weight study](B-20261031-00H-T013-CATEGORY-WEIGHT-RNG-INLINE-HELPER-01.md) (source `data/T013_CATEGORY_WEIGHT_RNG_INLINE_HELPER_NATIVE_20261031_00H.md`, historical SHA256 `419771cb57f66152d8bd7af92e69f0a40cddfef59f473f6290032d9499102caa`) and [04H fan-out study](B-20261031-04H-T013-CATEGORY-LABEL-WEIGHT-FANOUT-01.md) (source `data/T013_CATEGORY_LABEL_WEIGHT_VECTOR_FANOUT_NATIVE_20261031_04H.md`, historical SHA256 `04fbcbb5eda02856fd7b9c7e711c141e53e40eed2897eddd560959f256fae31c`) distinguish the `0x449704` category-to-label map from the `0x44968E..0x4496A7` weight branch. Category 0 and categories 4/5 share the **"hold" label**, but category 0 has factor **0.6** (200→120) while 4/5 take the **0.8** fallback (200→160). Category 6 uses factor **0.3** (200→60); 1/2/3/7/8 use **0.8**. These are historical bounded STATIC arithmetic claims, **not** a demonstrated final AI command, reachable-category set, or runtime RNG count.

The same 04H note bounds `0x44963B..0x4496E5` as a **loop over a manager Unit-pointer vector** with independent per-Unit eligibility gates; label/wait writes may fan out to multiple eligible Units, rather than identify a single chosen target. Existing [02H threshold study](B-20261031-02H-T013-SPECIAL-LIMIT-CATEGORY-CLOCK-01.md) and [03H source-DAT/cache study](B-20261031-03H-T013-BTL-LIMIT-ACTUAL-CACHE-01.md) further delimit category 1/7→6 rewriting: the normalized `context.dat` source snapshot reports `btl_limit=1300`, `btl_limit_c=1500` (thresholds 260/300 for finite nonnegative values) rather than the getter's absent-property default 500 (threshold 100); present zero is not absent. Normalized source DAT is **not** an original unmodified runtime Golden fixture. Hence label identity, numeric score, key selection, category rewriting, Unit field writer and actual action must remain separate concepts.

Dedup/curation check at GitHub develop on 2026-11-05: the 00H/01H exact IDs are present in `REF_BATTLE_AI_MORALE.md`, 04H exact ID appears in `symbols.tsv`, and the exact 23H/02H/03H IDs were not found in the scoped REF/symbols/structs set. This is **not** proof that their entire semantics are absent from develop, nor a new CURATED claim. No authorized PC SHA/V9/DAT re-verification this run; historical original reports only. Original gameplay Golden PASS=0, strict MATCH=0, newly formal READY=0. Curator should verify the isolated native windows and source-DAT provenance before selective adoption.

## Next verification and safety constraints

Reconcile later 2026-10-31 00H weight and 04H label fan-out, verify actual original-game status before naming canonical AI tactics. Curator must independently check permitted original V9 ASM/DAT and prior B/other owner corrections before REF/typed dictionary/develop semantic adoption; no raw EXE/DAT/SAVE/ZIP, generated DB, private path or refused material is included. A B intake summary is not a gameplay Golden or G4 battle-result writeback proof.
