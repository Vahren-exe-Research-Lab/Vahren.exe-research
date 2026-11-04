# Historic B T012/T028: static-object death routing and low-AL ambiguity
- research_id: `B-OFFLINE-20261024-1111-T012-T028-STATIC-RETURN-DEATHBRANCH-01`
- owner/tasks: B / T012, T028
- historical_observed_at: 2026-10-24 11:11 JST; PC source+target SHA read-only measured 2026-11-02 05H JST
- source_relative_path: `data/B_T012_T028_STATIC_RETURN_DEATHBRANCH_OFFLINE_20261024_1111.md`
- source_sha256: `EFA7E2FAC7CC9FDF1CBA01FDDFCFA069230B4480E07F0E2A10A47EDCFCE3B616` (PC source, 9,103 bytes)
- original_PE_SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (read-only verified at this intake)
- V9_composite_SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (tool-reported, whole DB not rehashed)
- evidence_kind: historical STATIC_ASM/local PE saved-window hashes; INFERRED meanings, current source SHA verified; dynamic/golden VERIFY
- original_gameplay_golden_PASS: 0; strict_MATCH: 0; DYNAMIC: 0; new_READY: 0; CURATED: false

## Reusable evidence and source anchors
1. Source §1 reports StaticUnit-type vslot `0x55ABA0`: the HP/death path at `0x55ABBC/0x55ABC5` tests a string-like length at `this+0x1E808` (with neighboring `+0x1E7F8` and capacity `+0x1E80C`), selecting a copied-string callback `0x55AC54 -> 0x402710`, then `0x55AC5F -> 0x4678A0`, with returned `+0x74` selecting `0x580280` or `0x54F720`. Empty branch constructs a `BreakFire` string and follows `0x55AD05 -> 0x4E1550` and indirect dispatch. Exact skill/event interpretation is VERIFY.
2. Source §2 contrasts SimpleStaticUnit vslot `0x55B060`: HP subtraction `0x55B07D` then different Skill+0x1B0 / +0x1BC bit1 / +0x194 gates for calls to `0x547FC0`; the above StaticUnit string-length split is absent *from this function*, not globally.
3. Source §3 warns `AL=1` is not equivalent to "newly killed by this hit": existing `this+0x1867C !=0` can return AL=1 without another HP decrement at `0x55ABB0 -> 0x55AD72`; corresponding SimpleStaticUnit path is `0x55B06D -> 0x55B136`. Live/survival returns `AL=0`. The local `MOV AL`/`XOR AL` do **not** establish EAX upper 24 bits. Both functions end `RET 0x10`.
4. Source §4 compares Unit-only `0x5783D7 CMP EAX,0xF4241` with SimpleUnit/StaticUnit/SimpleStaticUnit, which lack that same compare in the examined bodies. Original byte-window digests are tabulated in source §原本PE局所バイト照合; **not newly re-hashed window-by-window in this intake**.

## Prior/errata and limits
- prior_ids: `B-OFFLINE-20261024-1016-T012-T028-VSLOT70-ABI-SENTINEL-JOIN-01`; `data/T012_BATTLE_CALC.md` §§17-18. Vtable class mapping and generic afterhit/afterdeath branch were old findings, not additional discoveries.
- erratum: do not treat a low-byte true return as a fresh death event or assume EAX fully zero-extended. Do not assume one class's death callback applies to all class types.
- G4 relevance: duplicate-death avoidance, event callback, surviving HP and object lifetime are candidate side effects, **not** proved battle-end native settlement contract.
- limits: original static source was obtained in an offline run; current PC source/target SHA were measured, but a live class dispatch, callback effect, event count and full x86 ABI remain VERIFY. Existing safety HOLD remains untouched.

## Next validation (owner B)
Bounded native-x86 reconfirmation at the permitted vslot functions; map actual indirect callers consuming AL and fields `+0x1E808/0x1E7F8`; lawful unchanged-original class/HP/dead-flag fixture. Keep scene/event/sound ownership distinct from B's limited branch study.
