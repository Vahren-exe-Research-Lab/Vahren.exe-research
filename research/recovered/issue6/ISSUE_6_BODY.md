# REA-20261101-17H-21H-P0-CANDIDATE-QUEUE
**Scope:** private GitHub curation handoff (not curated `develop` or a gameplay proof). **Owner:** REA/P0-T015 as source; KB curator as meaning/REF/symbols integration owner. **State:** `PC-SAVED / NATIVE-STATIC / INFERRED-EH / VERIFY / NOT READY` except the 18H partial safety-held artifact. Original ver0.67 PE **previously validated** SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; composite V9 previously validated SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. Do not treat this issue as independent original-game Golden evidence.

## Source IDs to cross-link and curate (not five independent newly VERIFIED functions)

| REA source ID/time | Owner source relative path / new bounded meaning | Curator action |
|---|---|---|
| `REA-LOCAL-20261101-17H-P0-CRT-FTELL-FRAME-CROSSWALK-STATIC-01` (17H) | `rea_lab/decomp_task/REA_20261101_17H_P0_FTELL_FRAME_STATIC.md` + `...FTELL_FRAME_EVIDENCE.json`. Current V9 already recognizes 91-byte `0x005B797C` function; `0x005B79D7` is parent-EBP-dependent unlock helper; invalid-parameter handler may terminate. | Correct old V3 gap claim from 13H/16H; **do not promote as a new V9 discovery**. |
| `REA-LOCAL-20261101-18H-P0-CRT-INVALID-PARAMETER-TAILJUMP-STATIC-01` (18H) | `REA_20261101_18H_P0_INVALID_PARAMETER_TAILJUMP_AUDIT.py` completed; `...EVIDENCE.json` **partial after SAFETY_REFUSAL**. Handler dispatcher `0x005BCB38`, ptr `0x0068E018`; `0x005BCB4E` indirect JMP; hypotheses only. | **SAFETY-HOLD / EVIDENCE-INCOMPLETE**. Refused append must NOT be retried, substituted or represented as a valid evidence set. Only recovery metadata. |
| `REA-LOCAL-20261101-19H-P0-FTELL-SEH4-SCOPE-STATIC-01` (19H) | `rea_lab/decomp_task/REA_20261101_19H_P0_FTELL_SEH4_SCOPE_STATIC.md` + `...SCOPE_EVIDENCE.json`. `0x005B797C -> __SEH_prolog4`; `0x00641260` EH4 scope record parent=-2/filter=0/cleanup=`0x005B79D7`. Normal `0x005B79C9` calls same unlock. | Add a bounded scope record to the Vorbis tell callback source map; **exception delivery/lock release success unmeasured**. |
| `REA-LOCAL-20261101-20H-P0-EH4-DISPATCH-PHASE-STATIC-01` (20H) | `rea_lab/decomp_task/REA_20261101_20H_P0_EH4_DISPATCH_PHASE_STATIC.md` + `...EH4_PHASE_EVIDENCE.json`; `0x005BB6E0` search vs unwind branches; `0x005C363B -> 0x005C3500 -> 0x005CC2D4` conditional scope cleanup. Prior owner bounded native audit 32/32. | Link conditional unwind to 19H without double counting native addresses. No unconditional runtime claim. |
| `REA-LOCAL-20261101-21H-P0-UNWIND-FOUR-CALLERS-NLG-STATIC-01` (21H) | `rea_lab/decomp_task/REA_20261101_21H_P0_UNWIND_CALLERS_STATIC.md`, `...UNWIND_CALLERS_EVIDENCE.json`, `...UNWIND_CALLERS_AUDIT.py`. Fresh **7/7 bounded original PE check** (six E8 sites + `0x005CC2D4` `FF D0 C3`), source PC readback completed. | Add a four-caller crosswalk; distinct from 20H phase analysis. Flag fsopen error branch semantics as V9 pseudocode inference until raw branch ASM checked. |

## New native 21H lookup map (bounded evidence, not an ABI prototype)
- `0x005C35BD -> 0x005C3500 __local_unwind4` (caller `0x005C3590`, PE code fragment, ABI unverified); bytes `e83effffff`.
- `0x005C35E6 -> 0x005C3500` (caller `0x005C35D6`); `e815ffffff`.
- `0x005C3646 -> 0x005C3500` (caller `0x005C363B`); `e8b5feffff` (prior 20H known, not a new semantic finding).
- `0x005D1D33 -> 0x005C3500` (caller `0x005D1CB1 __fsopen`); `e8c817ffff`. V9 pseudocode associates this with an invalid/empty filename route but native branch condition remains **VERIFY**.
- `0x005C356E -> 0x005CC2B5 __NLG_Notify` bytes `e8428d0000`, `0x005C357B -> 0x005CC2D4` bytes `e8548d0000`; trampoline `FF D0 C3` = `CALL EAX; RET`.
- V9 pseudo shows `__local_unwind4` advancing the scope cursor before cleanup dispatch and calling `__NLG_Notify(0x101)`. **Cursor write instruction and NLG side effects not independently confirmed by this 7-site audit**. Never infer callability for DLL hooks.

## Non-duplication and pending backlog
- `REF_AUDIO_VORBIS.md` and `symbols.tsv` in private `develop` were read and do not yet reflect the above 11/1 EH4 17–21H chain. 10/31 21H and earlier Vorbis findings are already curated; do not import twice.
- **Already tracked:** [#3](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/issues/3) for 11/1 03–16H (14 research IDs/67 Library assets); [#4](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/issues/4) for broader source-linkage. Their issue-only stage is not formal KB integration.
- **Other PC backlog to review:** 10/31 22–23H and 11/1 00–02H source reports; assess local author source/path/hash and duplicates before adding any new symbol. Do not process entire binaries or exported pseudoc ZIP into Git.
- New formal REA five-evidence sets **0**, new VERIFIED **0**, official TODO/VERIFY/BLOCKED changes **0/0/0**; original gameplay Golden PASS **0**, strict MATCH **0**, READY **0**, replication percent unknown. Previously reported 64/64 remains history and is **not** incremented.

## Minimum GitHub reusable-output acceptance
Curator should make this research findable by VA, by research ID and by functional query in `REF_AUDIO_VORBIS.md` (or an appropriately named CRT/EH REF), selected `symbols.tsv` only when semantically supported, and lightweight backlog/curation metadata. Preserve corrected/superseded status, owner + evidence relative path, source SHA receipts, STATIC/INFERRED/VERIFY/Golden boundaries. Use *isolated curator worktree* with allowlist, redaction and ff-only verified publish; no REA direct shared-knowledge edit, Git branch switching, prohibited VA, source binary/large database, or blocked evidence recovery.

**Next REA P0:** original-x86 `0x005D1D33` __fsopen error branch, `0x005C3500` scope cursor ASM, `__NLG_Notify` side effects, FILE* state and normal/exceptional return boundaries.