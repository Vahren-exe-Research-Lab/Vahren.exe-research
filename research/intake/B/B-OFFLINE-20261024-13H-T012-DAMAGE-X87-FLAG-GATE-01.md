# Historic B/T012: x87 AH&0x44 parity gate in bounded damage path
- research_id: `B-OFFLINE-20261024-13H-T012-DAMAGE-X87-FLAG-GATE-01`
- owner/tasks: B / T012 (T028 downstream candidate)
- historical_observed_at: 2026-10-24 13H JST; current PC source+target SHA read-only measured 2026-11-02 05H JST
- source_relative_path: `data/B_T012_DAMAGE_X87_AH44_GATE_OFFLINE_20261024_13H.md`
- source_sha256: `DC5BCEC81279BCFF568F1FA51108CF2CDDFD665BA51A2D97EA3E4D2C2601AC6B` (PC current source, 7,187 bytes)
- original_PE_SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (read-only measured at intake)
- V9_composite_SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (tool-reported digest; full DB not rehashed)
- evidence_kind: historical STATIC_SAVED_PE_HEX + ISA_DERIVED; current V9 function/CALL metadata checked; gameplay reachability VERIFY
- original_gameplay_golden_PASS: 0; strict_MATCH: 0; DYNAMIC: 0; new_READY: 0; CURATED: false

## Reusable evidence and source anchors
1. Historical source §新たに詳細化した局所的制御条件 stores a previously captured PE window `[0x5510E1,0x551156)` (117 bytes), historical SHA256 `BDB6A82E2E265E72DC8323CC2855694F456532DB208C6DD82507A9010D9458DB`; this run **did not independently re-hash the window**. Within containing `0x550E70`, recorded `0x5510F1 FLD [ESI+0x280]`, `0x5510F9 FLDZ`, `0x5510FB FUCOMPP`, `0x5510FD FNSTSW AX`, `0x5510FF TEST AH,0x44`, `0x551102 JP 0x551108`.
2. Conditional x87 status interpretation: AH mask 0x44 selects C3 and C2; `JP` tests *even parity of the masked bits*. Finite nonzero comparisons generally produce mask `0` (branch taken); ordered zero produces `0x40` (not taken); unordered/NaN produces `0x44` (branch taken, *if reached without traps*). This is ISA-level inference, **not** an observed NaN attack.
3. Historical source also records `0x5510E5` resistance=10 bypass, zero-result ECX branch, mode=6/test-EDX branches, and signed clamp `0x551138..0x55113F` for **some**, not all, paths. These adjacent branches are older T012 evidence and are linked, not counted as new additions.
4. Current read-only V9 `--inspect 0x550E70` resolves existing function, 6 verified direct E8 callers and 29 direct E8 outgoing sites; the sample list confirms `0x550F38 -> 0x550D80`. This graph is **not an independent validation** of the x87 byte sequence or actual parameter meaning.

## Prior/errata and limits
- prior_ids: `data/T012_BATTLE_CALC.md` damage core, `B-OFFLINE-20261024-1016-T012-T028-VSLOT70-ABI-SENTINEL-JOIN-01`, prior unrelated x87-distance `B-20261015-1817-01`. No duplicate count for those.
- erratum: simplistic “damage nonzero => JP” is not equivalent to the tested AH parity condition, especially for unordered operands; do not infer NaN is legal DAT or causes an in-game hit.
- G4 relevance: linked to damage-to-death effect route, not proof of battle-end EXP/death/settlement or external result application.
- limitations: original report relied on saved PE bytes and old offline runtime; later report/source SHA is now verified on PC, but opcode-by-opcode current native validation and game reachability are still VERIFY. Prior holds and protected addresses not accessed.

## Next validation (owner B)
Scoped native x86 check at safe `0x550E70` / `0x551154`; correlate Skill+0x280 parser and resistance context with legal original DAT and gameplay; compare positive/zero/negative damage, resistance 10, mode6 and lethal HP while preserving unchanged EXE/DAT/SAVE/MAP/input/RNG. Never upgrade hypothetical NaN or external settlement to Golden.
