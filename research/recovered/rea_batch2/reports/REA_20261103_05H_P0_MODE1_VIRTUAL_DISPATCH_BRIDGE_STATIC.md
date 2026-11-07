# REA 2026-11-03 05H | bounded mode-1 entry to virtual +4 setup (STATIC / VERIFY)
- **research_id:** `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` (existing ID, same-ID addendum; **new IDs 0**). **owner/task:** REA / P0 T015. **observed_at:** 2026-11-03 05H JST.
- **source_relative_paths:** `rea_lab/targets/hakushin067_Vahren.exe`, `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`, preceding `rea_lab/decomp_task/REA_20261103_04H_P0_VIRTUAL_SETUP_SWITCH_VPTR_DUALWRITE_STATIC.md`.
- **measured SHA256:** original PE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; read-only V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (2026-11-03 05H).
- **scope:** targeted original x86 + read-only V9; no REA rerun, game execution, protected/refused material, other-owner files or shared `develop` edits.

## Distinct new bounded native observations
- `0x4B9970 mov eax,[esi+0x1EF144]`, `0x4B9976 cmp eax,7`, `0x4B997B jmp [eax*4+0x4B99FC]`: native eight-entry jump table `[0x4B9982,0x4B99B9,0x4B99C7,0x4B99DF,0x4B998F,0x4B99AB,0x4B999D,0x4B99D4]`. Thus **index 1** selects `0x4B99B9`, not an unconditional caller.
- `0x4B99B9 lea eax,[esi+0x504]`; `0x4B99BF push eax`; `0x4B99C0 e8bb2efdff call 0x48C880`. The native E8/rel32 is separately present in V9 `native_callsite` with caller `0x4B9930` (**1/1** direct edge); caller's `[esi+8]==2` escape and other loop outcomes remain relevant.
- Within that callee, native `0x48C8BE c7853cec1e0001000000` writes value **1** to `[ebp+0x1EEC3C]` (where the caller supplies `ebp=esi+0x504` through the argument). This is `[esi+0x1EF140]`, **not** the outer dispatch `[esi+0x1EF144]`; the distinct four-byte fields must not be conflated.
- Later in the same `0x48C880` body, `0x48CA53 mov ecx,[ebp+0x1E8630]` / `0x48CA59 mov edx,[ecx]` / `0x48CA5B mov eax,[edx+4]` / `0x48CA5E call eax` exhibit a native **indirect vtable +4 invocation** after the mode-1 write on the shown linear path. The limited call window has **no local NULL check** for `ecx`; this is NOT evidence that NULL is reachable.
- Prior same-ID 04H report independently pins vtable `0x639B08+4 -> 0x51E6F0`, with ctor/cleanup vptr writers. **Conditional target:** only if the live object in `[ebp+0x1E8630]` retains that vptr, `0x48CA5E` can invoke `0x51E6F0`. Its selector reads `[[player+0x194]+0x1EEC3C]`. Despite native constructor `0x51E3A7 add eax,0x504` and `0x51E3B9 mov [edi+0x194],eax`, aliasing to the caller's `[esi+0x1EF140]` and lifetime must be proved; do not infer unconditional case-1 setup.

## Small-window native reproducibility receipts (SHA256)
- `0x4B9970 +0x76`: `B9E89CDF76EA0BEAE6FC7B58EE55135B1DF700BAA3747E72F4D5365BE6372859`.
- `0x4B99FC +0x20` (eight dispatch targets): `21CD59E18382D6780BC6B5AA494CD8D5F5C43943FB88AF272293464DF646A257`.
- `0x48C8B2 +0x50`: `56B46F24BEB74768E6B2C6913DAABD7131CC71450E20415A896D418490B44736`.
- `0x48CA53 +0x1B`: `8F316FFA98397DE50FE725B9C0EF8D7ACCC9CA2C6BC95F72033FA3DD22962BE4`.
- `0x51E3A4 +0x21`: `AF1B107FFAD0DF61D9F9AD53AFA50A513660428C53C99EA64A1FAB911FF9CDA2`.
- `0x51E98C +0x1C`: `07F99628EBCCC0A927DB1D1C8FBCA22C3751EBC724D595ABFF0E8E4C7AF75CA6`.

## Evidence state, dedup and handoff
- **STATIC:** bounded PE opcode, rel32, table, indexed native E8 and address arithmetic. **INFERRED:** virtual call target conditional on active vptr and pointer lineage. **VERIFY:** object pointer alias, runtime vptr changes, whether transition's path reaches virtual call, exception/NULL effects, setup-before-use relative to `0x491870/0x4922A0`, and actual exclusion-tree insertion.
- **Duplicate/correction:** no new research ID, no supersedes. Prior 00H–04H same-ID evidence already links ctor/vtable/guarded requests. The new distinct evidence is **outer mode index1 -> `0x48C880` -> inner mode1 write -> indirect slot+4 call**; `develop/REF_BATTLE_TAKEOVER.md` does not currently carry these exact sites. B/E semantic overlaps are not exhaustively certified.
- **Curator action:** pin exact owner report SHA + PR commit and current `develop`; independently review small native windows, same-ID correction history and B/E overlaps; admit only the conditional STATIC edge to `REF_*` from curator-owned clean latest-develop branch. Owner PR evidence is PUBLISHED_INTAKE, not CURATED.
- **Formal:** previously archived five-method static evidence 64/64 (historical `logs/progress_sync_20261011T153958076Z.json`); new 5-method VERIFIED **0**, original Golden PASS **0**, strict MATCH **0**, READY **0**. No new safety refusals or original game changes.
- **Next lawful cursor:** prove or refute `[player+0x194]` alias and vptr stability at `0x48CA5E`, and relate only the permitted `0x4B9930` mode-1 path to request ordering. Do not retry protected VA, Wave6 or 18H evidence.
