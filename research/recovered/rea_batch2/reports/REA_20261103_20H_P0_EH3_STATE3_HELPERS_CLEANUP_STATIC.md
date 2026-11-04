# REA 2026-11-03 20H | EH3 state-3 cleanup helpers (bounded native STATIC / VERIFY)

- Work ID: REA-20261103-20H-P0-EH3-STATE3-HELPERS-STATIC; owner REA; historical research ID `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01`; **new independent study IDs 0**. Observed 2026-11-03 20H JST.
- Original source `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; read-only V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`; both remeasured in this run, not game-executed.
- Predecessor same-ID `rea_lab/decomp_task/REA_20261103_19H_P0_EH3_STATE20_UNWIND_CHAIN_STATIC.md` SHA256 `5536F6383FC1A3BD11D625DA76A7218172323D52C1E9AD25A069B73FD6C4E62F` remeasured. This is a narrow continuation of its state-3 action `0x5FD553 -> 0x428680`; not a new discovery ID or a replacement for 19H.

## New bounded original x86 observations

- `0x428680` (139 bytes) saves an SEH frame, adjusts its incoming receiver to an `ESI = receiver+0x10` subobject, writes vptr-like constants, and calls `0x42A9A0` then `0x4296E0`. On their ordinary return it writes another vptr-like value, calls `0x5B5D79`, restores `fs:[0]`, and returns. This is static control flow only; exception-path completion is unproven.
- `0x42A9A0` uses **ESI**, not the caller's ECX, for field accesses: if `[esi+0x40] bit0` it calls `0x5B6BBB` on `[[esi+0x10]]`; it zeroes six pointed-to locations sourced from `[esi+0x10/+0x20/+0x30/+0x14/+0x24/+0x34]`, clears bit0 in `[esi+0x40]`, sets `[esi+0x3c]=0`, and returns. Non-null validity/heap ownership/runtime conditions are not proven.
- `0x4296E0` receives ECX=ESI, overwrites its own vptr-like word at `[ebp]` with `0x63843C`, and checks pointer `[ebp+0x38]`. When nonzero it accesses the nested first pointer, conditionally decreases a count field `[child+4]` (only if 0<count<0xFFFFFFFF), may invoke `call [child-vptr+0]` with stack argument 1, and frees the backing pointer via `0x5B6BBB`. It finishes with `jmp 0x5B61C9` after placing ECX at `[ebp+4]`; the tail helper's complete semantics were not examined.
- **Important ABI distinction:** `0x42A9A0` uses preserved ESI context; `0x4296E0` uses ECX as receiver. V9 reports `verified_abi=0` on all three entries; no native dynamic receiver identity, child vptr target, exact destructor semantics, or outer EH propagation is proven.

## Reproducible source receipts / native-V9 cross-check

- Exact byte windows: `0x428680+139` SHA256 `32F4AB9E0D087DC5E2CE8AB9DA4D2CD8A01388E9EB308BAB7713A1390FB8FB42`; `0x42A9A0+86` SHA256 `17B849809A9E02CA0420CE415AAAC96091800D6303A247E516CC5393856421EA`; `0x4296E0+110` SHA256 `999DE95DD29745E52821CAEC9A1C759355BACA07189DBCF771B86B86BEFEDC52`.
- Newly checked native x86 versus V9 `native_callsite` matches **6/6** (5 E8, 1 E9): `0x4286F1 -> 0x5B5D79`, `0x42A9AC -> 0x5B6BBB`, `0x429700 -> 0x5B6170`, `0x429723 -> 0x5B6198`, `0x429738 -> 0x5B6BBB`, `0x429749 -> 0x5B61C9`. Insn bytes/length/target matched. Prior 19H's two caller E8 edges were not recounted.
- Read-only method: SHA256 file hash, `pefile` PE VA-to-offset, Capstone 32-bit bounded disassembly, SQLite URI `mode=ro` `pragma query_only=ON`; no REA rerun, game execution, source patch, generated DB modification, or safety-held evidence access.

## Meaning, duplicate and curation gate

- **STATIC:** the above memory writes/branch and call structure; **INFERRED:** staged subobject cleanup; **VERIFY:** exceptional dispatch or completion, finalizer effect at `0x429734`, tail `0x5B61C9` semantics, dereference safety, ownership/lifetime, upper EH catch and game effects. Do not claim full rollback, exception recovery or leak/crash.
- Same original study ID, no superseded separate ID; A/T014 and prior 18H/19H are read-only overlap references. Original five-method new VERIFIED 0; previously archived 64/64 **not rerun**; actual original Golden PASS 0, strict MATCH 0, READY 0. Index historical 266 IDs (prior 258 intake + 8 safety hold), not a curated count.
- PUBLISHED_INTAKE **only if GitHub report exact-text readback succeeds**; NOT CURATED. The refused Wave6, older held 18H material and protected range remain metadata-only and were not accessed. No develop/REF/symbol/other-owner changes.
- Curator: rehash three windows and source files, verify six native/V9 target rows and ABI0, reconcile 19H state-3 chain and A/T014 ownership; adopt only distinct STATIC meaning in curator-owned isolated develop worktree.
- **Next lawful cursor:** bounded `0x429734` indirect finalizer target identification and `0x5B61C9` tail helper/caller ABI, then upper EH propagation beyond state 0. Keep dynamic semantics in VERIFY.
