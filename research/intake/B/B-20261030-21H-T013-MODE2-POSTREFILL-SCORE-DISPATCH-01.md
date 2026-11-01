# B-20261030-21H-T013-MODE2-POSTREFILL-SCORE-DISPATCH-01 — B historical targeting source intake

- research_id: `B-20261030-21H-T013-MODE2-POSTREFILL-SCORE-DISPATCH-01`
- owner: B
- tasks: T013 (T024 AI and T028 references, no ownership transfer)
- observed_at: 2026-10-30 21H JST
- source_relative_path: `data/T013_MODE2_POSTREFILL_SCORE_DISPATCH_NATIVE_20261030_21H.md`
- source_sha256: `5f55505a8bf61acbcf060c0d1d293a7007f680cebf17e762020efd36e73d1d6e` (authorized PC Markdown SHA256/byte size independently measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target, not a fresh EXE hash in this intake)
- evidence_va_call_offsets: `0x44C588/0x44C599,0x44C5A5/0x44C5AD,0x44C5D4/0x44C5FE→0x510850,0x44C624,0x44C633→0x591570,0x44C6BD/0x44C6C7→0x515060,0x44C6CE manager+0xB0,0x44C70F..0x44C7E8,0x44C856..0x44C975`
- prior_ids_and_corrections: B-20261030-19H key erase and 20H empty refill, earlier T013 +0xD0 comparator and Unit action dispatch do not re-count
- evidence_kind: historical STATIC native/callgraph / INFERRED, VERIFY for ABI/runtime/result; original DYNAMIC 0
- golden_status: original Gameplay PASS0, strict MATCH0
- ready_status: new READY0; E MASTER formal promotion0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; not CURATED

## Reusable source-grounded findings

After the 20H conditional refill, old original ASM continues candidate iteration around `0x44C588/0x44C599`. On exhaustion a scratch flag `[ESP+0xCC]` controls either cleanup of two temporary trees using `0x510850` and frees, or a continuing score/Unit-dispatch path. In the latter path `0x44C633→0x591570`, three property getter calls `0x46F4C0`, and two `0x515060` calls derive manager/group sums; `manager+0xB0` keeps a raw result before conditional zero-to-one normalization. Existing `manager+0xD0` score/threshold route is then applied. One branch may write manager `+0x20=3` and call `0x449500(3,manager)`, another branch writes 1 under a distinct x87 predicate. Later category jump table and Unit-vector iteration gate five Unit state fields before conditioned RNG/wait/label updates. This is **post-refill scoring and possible per-Unit routing**, not a proven attack selection. FPU condition bits, ownership and runtime effects remain VERIFY.

## Next verification and safety constraints

Use 22H manager/group sum and x87 comparison proof, 23H category table/Unit writer, and valid original DAT to verify branch semantics. Curator must independently check permitted original V9 ASM/DAT and prior B/other owner corrections before REF/typed dictionary/develop semantic adoption; no raw EXE/DAT/SAVE/ZIP, generated DB, private path or refused material is included. A B intake summary is not a gameplay Golden or G4 battle-result writeback proof.
