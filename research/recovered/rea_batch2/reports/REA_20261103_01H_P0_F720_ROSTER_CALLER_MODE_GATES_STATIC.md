# REA 2026-11-03 01H | Five BattleStatusWnd caller modes and bounded branch gates (native x86 STATIC/VERIFY)
- **research_id:** `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` (existing owner ID; addendum, NOT a new discovery ID). Owner REA / P0 T015. Observed 2026-11-03 01H JST.
- **source_relative_paths:** `rea_lab/targets/hakushin067_Vahren.exe`; `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`; `rea_lab/decomp_task/REA_20261103_01H_P0_F720_ROSTER_CALLER_MODE_GATES_STATIC.md`.
- **actual SHA256 this run (read-only):** original PE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (2,910,720 B); V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (141,033,472 B).
- **prior/duplicate/correction:** Extends the same-ID REA 2026-11-02 21H–23H and 2026-11-03 00H addenda; `develop/REF_BATTLE_TAKEOVER.md` already CURATED_STATIC-links the *five direct E8 sites*. Do NOT count those five already-known edges again. E's DemoPerson lifecycle and B/T013–T028 `0x447810` remain separate owner sources. No supersession of B/E facts.

## Native five-site caller matrix (bounded Capstone from permitted PE + V9 mode=ro/immutable)
| E8 site -> `0x40D0A0` | V9 source function | Immediately prior native DL | Common bounded callframe |
| --- | --- | --- | --- |
| `0x491FFB` `E8 A0 B0 F7 FF` | `0x491870` | `mov dl,1` at `0x491FF9` | `push edi`, `lea ecx,[ebp+0x1EED30]`, `lea eax,[ebp+0x1EED20]` |
| `0x49204F` `E8 4C B0 F7 FF` | `0x491870` | `xor dl,dl` at `0x49204D` | same three inputs |
| `0x492143` `E8 58 AF F7 FF` | `0x491870` | `xor dl,dl` at `0x492141` | same three inputs |
| `0x4921F7` `E8 A4 AE F7 FF` | `0x491870` | `xor dl,dl` at `0x4921F5` | same three inputs |
| `0x492473` `E8 28 AC F7 FF` | `0x4922A0` | `mov dl,1` at `0x492471` | same three inputs |
- All **5/5** original opcode/rel32 targets and V9 `native_callsite` rows match, each `independently_verified_target=1`. At each entry the stack dword is read from caller `[ebp+0x1EED1C]` into EDI and pushed; `0x52AD90` is called before the bounded preparation. Function-wide ABI / callee effects are NOT VERIFIED.

## Native bounded condition and receiver-side effects
- `0x492005..0x49204F`: the `0x49204F` DL=0 route requires `[ebp+0x1EED56]!=0`, result of `0x469170` nonzero, and global `[0x683748]!=0` within this branch; failed tests branch to `0x4920FD`. Effects of `0x469170` itself are not derived.
- `0x4920FD..0x492143`: the `0x492143` DL=0 route is reached after `[ebp+0x1EED54]==0`, `[ebp+0x1EED55]==0` and `[0x683749]!=0` in this local branch. These are *site-specific*, not a global scene precondition.
- `0x4921B2..0x4921F7`: if `[0x683748]!=0` and `byte ptr [[ebp+0x10]+0x0B]==0`, the bounded route calls `0x4922A0` at `0x4921CD` instead of immediately calling the DL=0 site at `0x4921F7`; alternative entrances remain possible.
- `0x4923EB..0x492473`: the `0x492473` DL=1 site is in the `0x492441` arm of `cmp byte ptr [ebp+0x1EED43],bl / jne 0x492441`. Full conditions on arrival and prior call side effects are not exhausted. The upstream guard for DL=1 `0x491FFB` likewise remains VERIFY.
- `0x40D0AB` copies incoming EDX to EBX; `0x40D0BF` clears global byte `0x8B8E54`, then `0x40D0C6` directly calls `0x40F320`. Later `0x40D1B6 test bl,bl / je 0x40D1CB` and `0x40D1BA mov [0x8B8E54],1` create a conditional selector update; another separate `0x40D200` writes 1. Therefore DL=0 at entry does **not** prove the selector always stays zero; indirect callback EBX preservation and full route reachability remain VERIFY.

## Reproducibility, non-claims, curator handoff
- Original bounded windows SHA256: `0x492005..0x492054` `A56974B09FE60590518EBE059E262A924C9C544AA1C2C7A77711B5314D7F2946`; `0x4920FD..0x492148` `53D9AA64C5B559E72BEADB0928790A2B9E176A0733B800469F0EA73CFAB59EFE`; `0x4921B2..0x4921FC` `B1EE1A00EE8D5A3A889656DF20E919C1E437D5139BA289699969693089723852`; `0x4923D0..0x492478` `10F02E1C40D608FC4B70E2D557964C9017CFCBA73B2B621237CA4626359A6A15`; `0x40D1AC..0x40D1CC` `BCC2BDA20E1FBECA700DA46BF61E459914D76C205B6DE17522B79DE07E8CD832`.
- The two caller owner functions `0x491870`/`0x4922A0` have **no V9 direct E8 edge to `0x40CCF0`**; this is an indexed-direct-edge observation, not proof that successful `0x51E6F0` setup never precedes them through outer/indirect paths. It does NOT establish global non-NULL lifetime, a reachable crash, runtime branch identity, or exclusion-tree insertion.
- **Evidence:** native x86 per-site STATIC, conditional interpretation limited STATIC/INFERRED; transitive/ABI/runtime VERIFY. New formal REA five-method bundles=0, new formal VERIFIED=0, unmodified-game Golden PASS=0, strict MATCH=0, READY=0. No REA rerun, user-game execution, denied evidence, original asset changes or cross-owner edits.
- **Curator action:** compare pre-existing `develop/REF_BATTLE_TAKEOVER.md` five E8 edges and symbols first; selectively adopt only the distinct DL=1/0 site modes and narrowed native guards if needed, preserving the same research ID, source SHA and branch HEAD. Do not auto-promote indirect effects, NULL reachability or B/E-owned facts.
- **Next lawful cursor:** bounded pre-call guards of `0x491FFB` and caller-chain ordering between `0x51E6F0` and these five sites, without crossing refused ranges; other-owner `0x447810` side effects remain cross-link/VERIFY.
