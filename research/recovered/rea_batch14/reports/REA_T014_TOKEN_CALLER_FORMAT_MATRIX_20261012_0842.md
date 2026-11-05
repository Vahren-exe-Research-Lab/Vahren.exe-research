# REA T014 — 0x4705F0 caller format matrix / 2026-10-12 08:42 JST
- Scope: approved-copy saved Ghidra evidence **read-only**, new REA/Ghidra calls 0, new static VERIFIED +0, original game NOT RUN. Current approved-copy SHA256 matched `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
- Master checkpoint83: DONE9/IN_PROGRESS21/VERIFY4 of 34. Original EXE gameplay golden PASS0. Game reimplementation percentage **not measured**.
- Source for resolved caller set (13): `runs/20261011T144115307Z/4705F0_procedure_callers.json` / `ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87`.
## Caller taxonomy — newly assigned 3 of 9 previously unclassified (7/13 classified overall)
- `0x428010` (T014, global.sav): saved pseudo `ev_7d8bf27f8f623acdc9c301d57fa247cf6372db3a769910b9ed7ad2099114e881`, ASM `ev_8f357dc6b9e49591c6a5cec5ac76b4bd2c9019e4bc9cd61f15e5b3ba1bd55118`.
  - At `0x4280A4..0x4280C2`, literal `"----------"` (10 chars) is installed as the global sentinel string. At `0x42839B..0x428412`, an input token from `0x4705F0` is compared against it with `0x402C40` **and a separate length check**; exact match branches to `0x4284C4` without consuming an entry payload.
  - Non-sentinel path `0x42843B..0x428494`: second string token read with `0x4705F0`, then numeric field with `0x470700`, then `0x4A69B0` insert wrapper. The resulting temporary tree feeds `0x4C1200`; found value is assigned to global `0xB06D78` at `0x42850F`. Exact lookup semantics and duplicate-key behavior remain VERIFY.
  - The function probes `global.sav` via FindFirstFileA, opens for reading, reads bytes, invokes decode `0x4270F0`, creates an input stream via `0x429C60`; failure/short read and extra data after sentinel are NOT established as permissible.
- `0x45E1E0` (T014, normal save root): saved pseudo `ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e`, ASM `ev_69ab9492fa443fe12c5fb3e0d6230b5c7bb67fcca9fbc5c2915973a18d18e124`.
  - Four successive root groups use the shared marker string at `0x65CD28` (length field `0x65CD38`) with content and length equality: first string+int payload, second `0x58E870` Unit reader, third `0x598980` Spot reader, fourth `0x5964C0` Power reader. After these groups the function calls `0x471AF0` diplomacy and `0x435550` graph readers.
- `0x58E870` (T014, Unit save state): saved pseudo `ev_992508cdab86c44fc73e0f72aa80b7ab30679a2b84144a444f5afe7a7d80760d`, ASM `ev_dd3a4fa049e9751b44ab874ad4dce5fdfbe23f8fc364274bf923e7a9cbebb839`.
  - Four repeated variable-field loops break on a zero-length token, then a subsequent map loop handles **empty token separately** from equality with the Unit-specific marker string at `0x68B9D0` (length field `0x68B9E0`), which calls `0x58E480` before fixed tail. This is not the same group delimiter as normal-save's `0x65CD38` nor the 10-hyphen global.sav sentinel.
- Previously classified: `0x598980` Spot, `0x5964C0` Power, `0x435550` graph, `0x471AF0` diplomacy (see `REA_T014_CALLERS_GLOBAL_SCRATCH_SCOPE_20261012_0738.md`).
- Remaining 6 resolved callers **not** independently assigned: `0x428710`, `0x45EAC0`, `0x470550`, `0x58E480`, `0x5A90E0`, `0x5B0400`. Indirect calls are outside the 13 resolved set.
## Reimplementation / VERIFY
- `0x4705F0` byte limit 255 and signed allowed `0x20..0x7F` are **token-local**. Do not collapse global.sav, normal save root, Unit fields into one generic terminator or infer all saved game text uses this reader.
- Open tasks: six caller uses, byte values of the normal-save marker at `0x65CD28` and Unit marker at `0x68B9D0`, `0x58E480` body, malformed/EOF/trailing bytes and duplicate key handling. This is static-only; no gameplay compatibility PASS.
- Saved waves 1-5: 16/16,10/10,10/10,12/12,16/16 = **64/64 STATIC VERIFIED**. P0 29/29, P1 35/35; Wave6 provisional 0/16, P0 5/P1 11, TODO16, function VERIFY0. Latest `logs/progress_sync_20261011T153958076Z.json` confirms `STALE_RENAME_DENIED` and `SKIPPED_QUEUE_STALE`; avoid previous EPERM rename retry or alternate overwrite.
- Preflight Local CPU9%, free RAM15.13GiB, no java/javaw/Ghidra/REA process observed, active.lock absent, SHA MATCH. New heavy processing **0 sec**, lightweight read-only inspection wall-time not rigorously measured.
- Next: caller `0x428710` (possible global-save companion; unverified) and `0x45EAC0` saved evidence, then `0x58E480` existing evidence only. Wave6 heavy run deferred until legitimate queue reconciliation.
- Limits unchanged: REA6.1.0/Ghidra12.1.4, one MCP session, 4 functions/run, 900000ms Ghidra, 960000ms request. No blocked `0x5710C0..0x571500` or refused extractor rerun, no original executable execution, no other-lane/MASTER/T018/Git/MCP/automation changes.

## Read-only EPERM triage
- Local Get-Item/Get-Acl inspection (no mutation): both QUEUE.json and PROGRESS.md have Attributes=Archive (not ReadOnly), inherited ACL, and 0 explicit Deny ACE. QUEUE last write 2026-10-11 21:39:42 JST; PROGRESS last write 2026-10-10 06:35:27 JST. These observations **do not** identify the underlying Windows rename EPERM cause or authorize retry/bypass.
- No sync run, rename, permission change, lock cleanup, or heavy process launch performed.
