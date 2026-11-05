# B-20261030-20H-T013-MODE2-EMPTY-RANGE-REPOPULATE-01 — B historical targeting source intake

- research_id: `B-20261030-20H-T013-MODE2-EMPTY-RANGE-REPOPULATE-01`
- owner: B
- tasks: T013 (T024 AI and T028 references, no ownership transfer)
- observed_at: 2026-10-30 20H JST
- source_relative_path: `data/T013_MODE2_EMPTY_RANGE_REPOPULATE_NATIVE_20261030_20H.md`
- source_sha256: `cef83db32b3f4812cb6e8f195d35e9f33de4342bcdf211078c37e865db08539f` (authorized PC Markdown SHA256/byte size independently measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target, not a fresh EXE hash in this intake)
- evidence_va_call_offsets: `0x44C570..0x44C588,0x44C577/0x44C57B/0x44C57D/0x44C57E/0x44C57F/0x44C583→0x56F130;0x56F135/0x56F14E→0x44D2A0;0x56F153..0x56F1A6,0x44D2A0`
- prior_ids_and_corrections: B-20261030-19H-T013-EQUAL-RANGE-ERASE-01 (candidate delete), later 21H continues dispatch after refill
- evidence_kind: historical STATIC native/callgraph / INFERRED, VERIFY for ABI/runtime/result; original DYNAMIC 0
- golden_status: original Gameplay PASS0, strict MATCH0
- ready_status: new READY0; E MASTER formal promotion0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; not CURATED

## Reusable source-grounded findings

Historic original ASM demonstrates an **empty-tree fallback** after the selected equal-range deletion: when the working tree count becomes zero, `0x44C577..0x44C583` passes another source tree's begin/end into `0x56F130`, and nonempty cases skip directly to `0x44C588`. Callee `0x56F130` returns immediately for an empty source range; otherwise it visits successive source nodes, passing key/payload to `0x44D2A0` insertion candidate. Thus a depleted working candidate tree can be repopulated from a retained source range. This neither proves the source and destination represent distinct runtime objects nor that a unique final target is chosen. Original source contains a decompiler hidden-register warning and a `RET8` calling boundary; do not trust a guessed three-argument C signature.

## Next verification and safety constraints

Validate 19H key-range result and 21H post-refill cleanup/dispatch against V9, determine whether actual source records can be recycled without double-ownership. Curator must independently check permitted original V9 ASM/DAT and prior B/other owner corrections before REF/typed dictionary/develop semantic adoption; no raw EXE/DAT/SAVE/ZIP, generated DB, private path or refused material is included. A B intake summary is not a gameplay Golden or G4 battle-result writeback proof.

## 2026-11-06 bounded 19H → 20H → 21H source-role crosswalk (existing IDs only)

The preceding [19H B/T013 study](B-20261030-19H-T013-EQUAL-RANGE-ERASE-01.md), owner source `data/T013_MODE2_EQUAL_RANGE_ERASE_NATIVE_20261030_19H.md`, historical report SHA256 `034eebc1521c16f9eb77f500e9579ccf4c7db3744f82bf478a1f858e41b705e8`, **corrects** the source-role distinction: `0x579AA0` is an equal-key **range reader** (returns boundaries; `RET 8`), whereas later `0x510850` performs the **range erase**. The separate [20H owner report](./B-20261030-20H-T013-MODE2-EMPTY-RANGE-REPOPULATE-01.md) (historical source SHA256 `cef83db32b3f4812cb6e8f195d35e9f33de4342bcdf211078c37e865db08539f`) describes the **count-zero conditional refill** `0x44C577..0x44C583 -> 0x56F130` from a retained range into an insertion helper `0x44D2A0`. Its branch does **not** guarantee that the range is nonempty or that repopulation inserts anything. A nonzero working-tree count bypasses that refill.

The following [21H B/T013 study](B-20261030-21H-T013-MODE2-POSTREFILL-SCORE-DISPATCH-01.md), owner source `data/T013_MODE2_POSTREFILL_SCORE_DISPATCH_NATIVE_20261030_21H.md`, historical report SHA256 `5f55505a8bf61acbcf060c0d1d293a7007f680cebf17e762020efd36e73d1d6e`, locates post-refill iteration at `0x44C588/0x44C599`, then separate cleanup-or-score/Unit routing. A 20H refill call is therefore **not** itself final target selection, manager score normalization, or a proof that any Unit executes an action. The 21H score interpretations are further narrowed by existing 22H manager/group raw-sum and 23H category-argument-vs-mode corrections. Do not import the T028 postretreat caller's independent `0x510850` **full-range** proof into this T013 caller; it only shares the generic helper.

Scoped read-only comparison with private `develop` at `b0be48dd5316f0dba8cc560456e64a6a9f3c7d08` found T028 references to `0x510850` in `REF_BATTLE_AI_MORALE.md` but no exact `0x56F130`/`0x579AA0` mention in that REF. Absence of a literal address **does not prove absence of semantic adoption** elsewhere in the KB. This is a **DUPLICATE_LINKED correction chain** among three previously published B-owner studies, not three fresh source reports, new DYNAMIC evidence, or an automatic `CURATED` promotion. The local research PC normal connection returned transient 429; original source SHA/PE/V9/DAT/MASTER were **not** rehashed or re-run here. Curator's next independent check: permitted native branch/argument windows for 19H reader and `0x510850`, 20H zero-count and empty-range guards, and 21H `0x44C588` continuation; retain separate source ownership/lifetime and final-target `VERIFY`. New ID, PUBLISHED_INTAKE, CURATED, READY, original Golden PASS, strict MATCH: **0**. Previously refused index/B_AI_ENTRY writes and protected evidence remain BLOCKED.
