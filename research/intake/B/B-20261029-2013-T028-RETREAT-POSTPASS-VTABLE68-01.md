# B-20261029-2013-T028-RETREAT-POSTPASS-VTABLE68-01 — Retreat postpass call/return chain
- owner: B; tasks: T028 (T013/T024 reference); source_relative_path: `data/T028_RETREAT_OK_POSTPASS_VTABLE68_NATIVE_20261029_20H.md`.
- source_sha256: `7AA4478339B0FEF283EC9846A867A8E963A7E34E9D4B3030FDDE015C53FFE316`; source_size_bytes: 5776; PC source hash independently checked 2026-11-02.
- evidence_status: **OWNER_PRIOR_ORIGINAL_PE_ASM / STATIC_REPORTED / INFERRED / VERIFY**. Existing V9 `--inspect 0x5681C0` returned a defined function, 2 verified direct E8 callers and an unregistered symbol. This V9 coverage count does not replace a fresh byte-window/hash check; this run did not redump ASM.
- stage: B private intake; **PUBLISHED_INTAKE after GitHub readback; NOT_CURATED**.
- Target original PE SHA256 (PC read-only rehashed 2026-11-02): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (2,910,720 bytes). Original game was not executed or modified. Bounded V9 coverage lookup uses existing index; not a fresh full ASM reconstruction. Original gameplay Golden PASS=0; strict MATCH=0; newly E-formal READY=0; this intake is NOT_CURATED. All native game semantics not stated as direct saved-source facts remain VERIFY. No G4 external battle result commit or rollback has been proven.

## Prior original-native source facts and bounded interpretation
- Reported `retreat_ok` tail logic joins earlier condition branches at `0x52216E`; an independent branch skips this block. Not writing `[EBP+0x20]=4` does **not** alone prove battle/AI event suspension.
- Direct E8 sites recorded by owner: `0x522170 -> 0x528700`, `0x52217B -> 0x525C90`, `0x5221B7 -> 0x5681C0`; candidate list copy via `0x525C90` (inferred) is followed by list traversal and cleanup. Do not assume full Unit roster coverage.
- Prior owner byte and CFG reading at `0x5681C0`: caller `0x5221BC` **uses EAX** after the call, contrary to its Ghidra `void __fastcall` guess. A zero-vs-nonzero result from separate branches is reported; the nonzero value's meaning and ABI are **VERIFY**. Never implement a hook from the pseudocode's void signature alone.
- After a `Unit+0x1867C` byte gate on a candidate vector, prior native shows indirect **vtable+0x68** call with literal stack argument 1. Actual Unit-derived vtable, side effects and original-game retreat behavior are unverified.
- Reported possible nonzero-result notification passes to `0x52CCF0`; no proven visible UI effect, death resolution, EXP side effect or G4 settlement contract.

## Supersedes, duplication boundaries, acceptance
- Prior T028 19H state4 condition, T024 `0x528700` list adapter and earlier vtable+0x68 implementation mapping are reused, not new B discoveries.
- G4 boundary remains **NO-GO**: cannot infer external death/retreat application, transaction idempotence, result commit or save persistence from this normal native control-flow.
- Next: independently verify only permitted PE windows and actual EAX return flow, the `0x528700` list/order conditions, real vtable dispatch, and postpass effects under a legal no-modification original gameplay Golden. Report source headings `今回の独立増分`, `calleeの実ASM`, `既存成果重複`. Do not inspect denied VA/content.