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

## Next verification and safety constraints

Reconcile later 2026-10-31 00H weight and 04H label fan-out, verify actual original-game status before naming canonical AI tactics. Curator must independently check permitted original V9 ASM/DAT and prior B/other owner corrections before REF/typed dictionary/develop semantic adoption; no raw EXE/DAT/SAVE/ZIP, generated DB, private path or refused material is included. A B intake summary is not a gameplay Golden or G4 battle-result writeback proof.
