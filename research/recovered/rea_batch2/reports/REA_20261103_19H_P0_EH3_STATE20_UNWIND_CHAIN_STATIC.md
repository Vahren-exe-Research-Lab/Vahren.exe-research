# REA 2026-11-03 19H | EH3 state-20 unwind chain and native helper split (STATIC / VERIFY)

- Work ID: REA-20261103-19H-P0-EH3-STATE20-CHAIN-STATIC; owner: REA; existing research ID: REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01. New independent research IDs: 0.
- Observed: 2026-11-03 19H JST, bounded read-only original PE32 and Ghidra unified V9 SQLite; no REA runner/game launch or memory edits. Publication classification is PUBLISHED_INTAKE only after GitHub exact-text readback, otherwise UNSYNCED; never CURATED.
- Original source: rea_lab/targets/hakushin067_Vahren.exe; SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (remeasured this run).
- V9 source: rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite; SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE (remeasured this run; read-only mode).
- Prior same-ID report: rea_lab/decomp_task/REA_20261103_18H_P0_LOAD_EH3_MAP_CATCH_UNWIND_STATIC.md; SHA256 8569DA6B56DF2601DD5431C3DBC8C7C45355CE84CE5036B194AD9DC5ABF10D03 (remeasured). The prior 18H analysis established a 30-entry EH3 unwind map at VA 0x654EF8 and normal-CFG state 20 at 0x45F5F9. This addendum examines the not-yet-described continuation from that map entry, not a new ID.

## New bounded original-x86 findings

- Unwind-map chain from indexed entries: state 20 -> state 3 -> state 0 -> -1. These are predecessor-state metadata, NOT proof of an actual exception traversing the chain.
- Entry 20: predecessor 3, action VA 0x5FD581. Native bytes decode as `lea ecx,[ebp+0x40]` followed by `jmp 0x4026B0`. This action was identified at 18H; it is included as the chain starting point, not double-counted.
- Entry 3: predecessor 0, action VA 0x5FD553. Native bytes decode as `lea ecx,[ebp-0xF8]` followed by `jmp 0x428680`. The action targets a different helper than state 20. The target's first 96 native bytes set an SEH frame using fs:[0], write vptr-like constants 0x6384CC and 0x63848C, and call 0x42A9A0 and 0x4296E0. It is not equivalent to a simple free and its full exceptional side effects/lifetime remain unverified.
- Entry 0: predecessor -1, action VA 0x5FD540. Native bytes decode as `lea ecx,[ebp]` followed by `jmp 0x4026B0`. It reuses state-20's helper with a *different* ECX object address.
- The bounded `0x4026B0` helper checks `[esi+0x14] >= 0x10` before `call 0x5B6BBB` (conditional release) and on ordinary return resets `[esi+0x14]=0xF`, `[esi+0x10]=0`, and byte `[esi]=0`. Runtime execution and complete owner-object cleanup are NOT proven.

## Native byte receipts (VA + exact length, SHA256)

- 0x5FD581 +8: E4C28633E81943A7EBE3F1D0E40C7CE46D0C7477636E234D176F8B2471A002D6
- 0x5FD553 +11: 2427C1291E1EEA5CF56AC4CD36832F4D4DFF72F3F5F11E9A9B51BF7E2C81DC26
- 0x5FD540 +8: 07484F350E3815AA1507A17169BABD1FE80ED2A1274BB83487F8D833DB8BC596
- 0x428680 +96: 3E49C2C5B6B78973E7188A6460B742AEE4BBDCDC61819CF32EB919E28CB1AD8F8
- 0x4026B0 +48: 9B21D63086C016CF4D15973EF398DFDD729BF85644CA92BABCB4E8A5034047FD

## Targeted V9 versus native callsite check

- 0x5FD543 E9 -> 0x4026B0; 0x5FD559 E9 -> 0x428680; 0x5FD584 E9 -> 0x4026B0: 3/3 matching instruction bytes and V9 target rows.
- 0x4286C8 E8 -> 0x42A9A0; 0x4286CF E8 -> 0x4296E0; 0x4026BC E8 -> 0x5B6BBB: 3/3 matching native bytes and V9 target rows.
- Total 6/6 original-x86/V9 direct edges concordant. Both V9 function entries 0x428680 and 0x4026B0 have verified_abi=0. These checks are NOT a complete formal five-method bundle and do not establish real exception dispatch.

## Meaning delta, evidence status and curator gate

- STATIC: the three-state predecessor chain, the action ECX bases and direct JMP targets, bounded helper entry/conditional release/normal-return stores, six native/V9 edges.
- INFERRED: likely cleanup intent for three different locals/objects. VERIFY: actual EH3 state selection, exceptional continuation/outer interception, success/failure effects of 0x428680, vptr+8 callback producer, object lifetimes, and whether exceptions escape/catch at all. Do not infer leak, crash, rollback, or gameplay behavior.
- Duplication: same existing original research ID; supersedes no separate ID. This adds the predecessor chain and distinct state-3 target to 18H; parent report remains the provenance anchor. A/T014 owner evidence is a read-only reference and was not modified.
- Formal REA five-method newly VERIFIED 0; previously archived 64/64 not rerun. Original-game Golden PASS 0, strict MATCH 0, READY 0. No refused/safety-held evidence, protected target, or prohibited operation was acquired or retried.
- Curator: independently rehash PE/V9/prior report and five byte windows; verify six `native_callsite` rows, EH3 chain 20/3/0, source/erratum links and A/T014 overlap. Only curator may adopt selected meaning into develop/REF/symbols; this report alone is NOT CURATED.
- Next lawful cursor: the outer exception propagation/handler boundary beyond state-0 metadata, bounded native effects of 0x428680's two callees, and independently authorized child vptr+8 producer. Avoid already covered EH map and all safety holds.
