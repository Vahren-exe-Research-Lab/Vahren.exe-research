# REA 2026-11-03 09H | three nullable player slots: mode dispatch, virtual calls, and later NULL guards (STATIC / VERIFY)
- research_id: `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` (existing owner study, same-ID continuation; **new IDs 0**).
- owner/tasks: REA / P0/T015; observed 2026-11-03 09H JST. Scope: original ver0.67 PE32 and read-only composite V9, bounded known functions, no REA rerun.
- source_relative_paths: `rea_lab/targets/hakushin067_Vahren.exe`, `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`, `rea_lab/decomp_task/REA_20261103_08H_P0_TRIPLE_PLAYER_ALLOC_NULL_SIGNAL_GATES_STATIC.md`.
- observed PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. Observed V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. Both rehashed locally in this run.
- evidence_kind: native original ASM and selected native E8/V9 matching **STATIC**, pointer lifetime/dominance and exact runtime failures **VERIFY**. Golden PASS=0, strict MATCH=0, READY=0; newly collected formal five-method VERIFIED=0.

## Bounded new facts after 08H
- `0x4B9930` initializes `[ESI+8]=0` at `0x4B9941`, calls a vtable callback at `0x4B995F`, then tests `[ESI+8]==2` at `0x4B9961/65`; this condition exits before the dispatch loop. Callback effects are unknown, so this is **not** a global invocation guarantee.
- When not exited, `0x4B9970/76/79/7B` reads outer mode `[ESI+0x1EF144]`, bounds it by unsigned 7, and indexes 8 native jump-table words at `0x4B99FC`: index 1 → `0x4B99B9` → `0x4B99C0 CALL 0x48C880`; index 2 → `0x4B99C7` → `0x4B99CD CALL 0x48D6A0`. These two *distinct* route targets share the engine base `ESI+0x504`; the dispatcher contains no direct validity check of the three engine slots before either direct CALL.
- **New route-2 window** in `0x48D6A0`: `0x48D8EC/8F9/906` loads each of `[EBX+0x1E8630]`, `+0x1E8634`, `+0x1E8638` and immediately dereferences its vptr slot `+4` for three consecutive indirect CALLs at `0x48D8F7/904/911`. The shown sequence has no interposed NULL test for the three slot pointers.
- **Important guard-order distinction:** later at `0x48D913..927`, `0x48DA05..19`, and `0x48DAF7..DB0B`, the respective same three slots *are* tested against zero before deriving `pointer+0x90` (or replacing that derived pointer with 0). These later guards **do not retroactively validate** the preceding virtual calls.
- Additional bounded `0x48DC08..52`, `0x48DC60..AC`, and `0x48DE60..AB` branches use the same trio for vptr `+8` indirect calls. Their branch conditions involve mode/other fields; no blanket no-check claim is made outside these windows. Runtime vptr value, callees and side effects are not established.
- **Interpretation:** 08H had proved the three allocation-failure NULL stores and unchecked mode-1 `0x48CA53` dereference. This addendum independently adds the mode-2 triple-call versus later-check ordering; it is **not** evidence that low memory is reachable in actual play, or that a crash occurs.

## Reproducible evidence receipts (original PE VA windows, SHA256)
- `0x4B9961+0x85` = `0910461CB5091D4EF1EC761589B5576C1D36035C2743AB617A13DCAC9DA5E3DB`.
- `0x4B99FC+0x20` jump table = `21CD59E18382D6780BC6B5AA494CD8D5F5C43943FB88AF272293464DF646A257`; words (index 0..7) `4B9982,4B99B9,4B99C7,4B99DF,4B998F,4B99AB,4B999D,4B99D4`.
- `0x48D8EC+0x42` = `34DA2A3D9121E1F05A5FBAC728AC2375939C79F5300FE06136EA390E7FBE8EC0`.
- `0x48DA05+0x1B` = `503591DEEFFF8BAC4F2268740B71BC35CFB7B61C0A2F56907BB0C05863525CE9`; `0x48DAF7+0x1B` = `D33AFDDD527238CE917538F258A7EA405C6CDCA8CAF1816B4DA38007DA1C72D0`.
- `0x48DC04+0x50` = `39C7088CEA4BBCB0B226777332C988E5A174CE362BB000A7AC572BBB2CF295D9`; `0x48DE57+0x55` = `87C09BFF68C2421F7FFAAD092115978CEBDDD5A32333E210C5D9F85199F7E5D4`.
- Native E8 rel32 independently decoded and matched V9 `native_callsite` **3/3**: `0x4B99C0→0x48C880` (`e8bb2efdff`), `0x4B99CD→0x48D6A0` (`e8ce3cfdff`), `0x48D8DA→0x501A40` (`e861410700`). This is not three newly VERIFIED formal REA bundles.

## Owner/cursor/curator boundary
- Dedup: preexisting develop `REF_BATTLE_TAKEOVER.md` §2 already knows the three side slots and §1 the `0x4B99CD→0x48D6A0` edge; 05H and 08H already describe case-1 setup/NULL behavior. **Only guard ordering on the selected case-2 triple-indirect-call path and selective comparison** are the new owner evidence; no new symbols or supersedes.
- Curator: recheck this file's actual SHA256, PE/V9 pinned hashes, ISA windows, B/E and current develop semantic overlap; select only novel safe STATIC facts in dedicated curator-owned develop worktree. Owner publication remains PUBLISHED_INTAKE, **not CURATED**.
- Unresolved: whether failure reaches this mode, indirect call exception/SEH, engine+slot lifetimes, all prior callers/virtual side effects, and true initialization-before-request dominance. No protected/refused VA, Wave6 or missing 18H evidence accessed.
- Next permitted cursor: `0x48D6A0` pre-triple-call reaching guards/earlier exits and downstream branch conditions for the three side slots; compare mode-2/1 activation with worker startup, without making dynamic claims.
