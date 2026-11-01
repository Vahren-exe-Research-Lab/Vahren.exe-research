# Historic B T012/T028: vslot+0x70 argument layout and distinct death sentinels
- research_id: `B-OFFLINE-20261024-1016-T012-T028-VSLOT70-ABI-SENTINEL-JOIN-01`
- owner/tasks: B / T012, T028
- historical_observed_at: 2026-10-24 10H JST; PC source+target SHA read-only measured 2026-11-02 05H JST
- source_relative_path: `data/B_T012_T028_VSLOT70_ABI_SENTINEL_20261024_1016.md`
- source_sha256: `ABB2F9059B4C33827E6ABD89A9C1D0CB22F9905B98D182BCB31FE5C0D6E93F48` (PC current source, 7,131 bytes)
- original_PE_SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (read-only verified at this intake)
- V9_composite_SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (V9 tool-reported digest, not rehashed)
- evidence_kind: historical STATIC_PE/old SQLite, INFERRED ABI; current V9 bounded metadata inspection; gameplay VERIFY
- original_gameplay_golden_PASS: 0; strict_MATCH: 0; DYNAMIC: 0; new_READY: 0; CURATED: false

## Reusable evidence and source anchors
1. In source §1, three historical indirect `CALL EDX` sites use a receiver's `vtable+0x70` with four stack arguments (push order is meaningful): `0x551154` in `0x550E70`, `0x578E1E` in `0x578B70`, and `0x57E04D` in `0x57DF90`. At `0x551154` the first stack argument is computed `ECX`; the other two sites push immediate `0xF4241` as their first stack argument. The actual native argument *meanings* and indirect target at runtime remain VERIFY.
2. In source §2, the `0x551117 MOV ECX,0xF4240` branch passes **1,000,000**, while the other two sites pass `0xF4241` (**1,000,001**). In the Unit-type historical native implementation `0x5783D7 CMP EAX,0xF4241`, equality zeros `Unit+0x1E568` at `0x5783E6`; inequality subtracts the amount from the auxiliary field at `0x5783DE`. Both later subtract HP. Do **not** generalize to SimpleUnit, StaticUnit or SimpleStaticUnit.
3. In source §2, a negative auxiliary amount at `0x5785A3..0x5785C0` is routed through `0x4E1950` before clearing. Whether this is reached and what effect it produces is unproven. Source §3 records lazy initialization `0x57E01F -> 0x599600` of a context object for one HP-negative route; not a proven generic dummy context.
4. Source §mechanical check describes vtable candidates: SimpleUnit `0x544790`, Unit `0x578370`, StaticUnit `0x55ABA0`, SimpleStaticUnit `0x55B060`; indirect dispatch requires matching live types. Source's synthetic 4-case arithmetic is not original execution. Current V9 `--inspect 0x578370` found the containing function and 50 *direct outgoing E8* edges but **zero direct E8 callers**, compatible with an indirect vtable candidate; V9 metadata does not itself prove a vtable binding.

## Prior/errata and limits
- prior_ids: T012_BATTLE_CALC §26/27/29, B-20261011-1411-01/-02 and preceding B/T012 vtable research. Prior four RTTI targets/3 callsites are linked, not newly discovered here.
- erratum: treating 0xF4240 and 0xF4241 as an interchangeable universal "instant death" marker loses the documented Unit-only auxiliary-field branch. No new correction to other class implementations is asserted.
- G4 relevance: deferred death/auxiliary-state side effects may matter for external settlement, but this report does **not** establish an external result, unique end-of-battle commit, stable identity or Golden comparison.
- limits: old offline evidence originally used a dated archive/SQLite; original-game reachability, runtime arguments, overflow, object lifecycle, effects and persistence are VERIFY. Do not include or re-run old safety-held evidence.

## Next validation (owner B)
Independently confirm safe native instruction windows and 3 indirect callsite push sets against current V9/original ASM; establish live dispatch and branch reachability with legal unchanged original fixtures; compare `0xF4240` vs `0xF4241`, HP below/equal/above zero, Unit class variants and side effects. Keep P0 takeover owner separate.
