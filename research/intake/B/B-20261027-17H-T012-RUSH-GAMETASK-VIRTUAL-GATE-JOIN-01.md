# Historical B/T012 native RushMissile: conditional GameTask virtual update
- research_id: `B-20261027-17H-T012-RUSH-GAMETASK-VIRTUAL-GATE-JOIN-01`
- owner/tasks: B/T012 primary; T011,T013 linked
- historical_observed_at: 2026-10-27 17H JST; source+original PE SHA checked on authorized PC 2026-11-02 05H JST
- source_relative_path: `data/T012_RUSH_GAMETASK_VIRTUAL_STATUS_GATE_NATIVE_20261027_17H.md`
- source_sha256: `FBA05552A822FD52F337FD68B51E7241BB96A287E2E6A4D1244EE5DBF648EBAD` (5,017 B; current PC source)
- original_PE_SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (current read-only verified)
- V9_composite_SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (current read-only V9 tool-reported; full DB not rehashed)
- evidence_kind: historical STATIC_ASM, RTTI/vtable + E8, INFERRED runtime receiver binding; original gameplay VERIFY
- original_gameplay_golden_PASS: 0; strict_MATCH: 0; DYNAMIC: 0; new_READY: 0
- curation_status: PUBLISHED_INTAKE; current develop `REF_BATTLE_AI_MORALE.md` already summarizes Rush-vs-Heal **at a coarser level**, so this is evidence preservation not a claim of uncited discovery or a new CURATED promotion.

## Bounded evidence from the existing owner report
- Source §PREEXISTING: Rush primary vtable `0x63A6B4`, slot +4 `0x63A6B8 -> 0x5501A0`; slots +0xC/+0x10 both map to `0x54E0A0`. These slot targets and `Rush+0x210` existed in B 2026-10-21 16:08/17:14; NOT new here.
- Source §RTTI/CHECK: original PE RTTI from `0x63A6B0 -> 0x63F83C -> 0x68D3D4` identifies a RushMissile candidate. Source's 24-byte vtable-window historical SHA256 `56180FC8F1EB46CCDA28D8F83D1635B14930EA31F873C409CF44991C9EB42384` is retained as historical window metadata, not independently re-hashed here.
- Source §NATIVE WRITER: `0x54F773` initializes the Rush vptr; `0x54F7DD -> 0x54F990` reinitializes; `0x54F7EC -> 0x4C2240` is one task-pending registration. A separate array write at `0x54F803 -> 0x550410` must not be equated to active GameTask registration.
- Source §DISPATCH ASM: in Task loop `0x4C28D0`, `M+8` and `M+0x14` determine whether to call a virtual predicate in slots +0xC / +0x10; approved path reaches `0x4C2933 CALL EAX` via vtable slot +4. If EBX really refers to a Rush object, **one candidate** destination is `0x5501A0`.
- Source §RUSH GETTER ASM: `0x54E0A0 MOV AL,[ECX+0x210]; RET`. Conditional model for a valid live Rush in this manager: `(M+8==0 && M+0x14==0) || Rush+0x210!=0`. This is a local conditional claim, not all-Task lifecycle/actual frame rate. Heal's predicate is a distinct earlier report, not interchangeable.
- Source §CALL VALIDATION: original report counted five historical x86 E8 rel32 edges; its `0x4C2933` is indirect and NOT counted among them. Current V9 `--inspect 0x5501A0` recognizes the existing function and five outgoing E8, zero *direct* E8 callers (indirect vslot evidence is separate).

## Provenance, dependencies, limitations
- prior_ids: `B-OFFLINE-20261021-1608-01`, `B-20261021-1714-01`, `B-20261027-09H-T013-HEAL-DEFERRED-TICK-DISPATCH-01`. This ID links the previously independent gates and slot mapping; do not inflate discoveries.
- supersedes/errata: no supersession of these old IDs; correct only the possible misconception that all tasks or Heal/Rush update identically.
- limitations: identity of EBX at runtime, legality and writer of +0x210, tick scheduler, mutation of M flags, exact callback ABI, effect/RNG/EXP and external settlement all VERIFY. `0x4C2933` is an *instruction site inside Task dispatcher*, not a standalone safe G2 pause location.
- G4: timed effect may change the settlement input but neither this report nor V9 establishes a battle-end commit or safe external-result substitution.

## Next validation
Reconcile Task's actual M owner/flags with Rush identity and lawful unmodified original Skill/DAT state; verify +0x210 writer and measured first update against original gameplay Golden; keep protected/previously refused targets and other-owner P0 material off limits.
