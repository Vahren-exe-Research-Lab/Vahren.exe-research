# ABI3 follow-up — original BGM call-boundary observation

Research ID: REA-T015-OGG-REUSE-20261105 / ABI3-20261105  
Status: OWNER_INTAKE / NOT_CURATED / DLL REUSE STILL UNVERIFIED

The user resumed normal game execution and changed BGM. This run used the installed game with explicit user permission, not an isolated-copy certification. Target EXE SHA256 remains e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187.

## New evidence

Raw log (local only) SHA256: 51c33e0de4c82c37262fc605fd7811e954a6e1b13e1cd5e645374c9323b63acf; 68,665 bytes, 1,559 lines. Earlier failed setup attempts are in the same file; analysis selects events after the last ARMED marker at line 37.

| Boundary | Matched pairs | Observed result |
| --- | ---: | --- |
| 0x5D16C0 open (CALL 0x502038 / return 0x50203D) | 3 | EAX=0 all |
| 0x5D0F70 info (0x502060 / 0x502065) | 3 | non-null all |
| 0x5D12E0 read (0x501F91 / 0x501F96) | 16 | positive partial/full bytes, no sampled EOF/error |
| 0x5CFE00 clear (0x501EC1 / 0x501EC6) | 3 | EAX=0 all; actual return now observed |

All 25 pairs preserved ESP, EBP, EBX, ESI, EDI across the call. Pairing uses function family, thread ID and ESP; stable arguments are checked separately. No unmatched/overwritten calls or returns were observed. Three format snapshots at 0x502085 show stereo, 44100 Hz, 16 bits. Read samples are on a BGM worker; open/info/clear are on the main thread. This supports the candidate cdecl boundary in the observed normal paths, not a universal ABI certification.

## Important argument-slot qualification

In all three clear pairs, caller stack [ESP] held the context pointer before the call and 1 after it. This is **not evidence of a corrupted ESP or a changed pointer in the caller's retained object**.

Fresh disassembly of the same-SHA EXE shows:
- 0x5CFE04: ESI = [EBP+8], retaining the original context.
- 0x5CFE42: [EBP+8] = EDI (zero), repurposing the incoming argument slot.
- 0x5CFE66 / 0x5CFE69 / 0x5CFE73: read, increment, write that slot as a loop counter.
- 0x5CFE76 compares against [ESI+0x34].
- 0x5CFEFB zeroes the outer 0x2D0 bytes; 0x5CFF04 sets EAX=0; 0x5CFF08 RET.

Thus a post-return stack dereference cannot be used to identify clear's original context. Use the saved call-side pointer or retained object register for correlation. The current diagnostic DLL keeps a static context backing and does not recover its pointer from this argument slot; no code change follows from this observation. This is a bounded tracing/ABI qualification, pending curator dedup review, not a formal dictionary correction.

## Capture limitations and next gate

The file contains no END marker. Prior user output showed LogRedirectStop before END; the exact cause in this run is not established. Returned pairs are usable but complete recording shutdown and leak-free cleanup are not certified.

The 16-hit read cap can expire before later BGM opens, so these samples do not demonstrate a complete open→read→clear lifecycle for every opened instance. Context addresses may be reused by allocation and are not stable lifetime IDs.

Not tested: new DLL-created context, independent-context concurrency with original BGM, failed-open ownership, malformed/chained inputs, PCM sample accuracy, leak/resource balance, DLL sink output, DAT path transfer. Next work is failed-open static ownership analysis and a controlled diagnostic adapter test after remaining ABI checks. Do not infer production readiness.

## Reproduction and scripts

Run `python analyze_abi3.py <closed-local-log> <new-output-directory>`. Summary and pairs contain no raw process pointers, filenames, or local absolute paths. Raw log is not uploaded.

The setup required two fixes: remove redundant bpe after bp, and omit the new breakpoint-name argument when reusing an already-set address. Official x64dbg BpGet searches by name when a name is supplied; cbDebugSetBPX then reaches IsBPXEnabled for an address occupied under an older name. Address-only bp reuses the existing entry. Sources: [command implementation](https://github.com/x64dbg/x64dbg/blob/development/src/dbg/commands/cmd-breakpoint-control.cpp), [BpGet](https://github.com/x64dbg/x64dbg/blob/development/src/dbg/breakpoint.cpp). Successful ARMED was user-observed after these fixes.

This follow-up augments [the design report](../REPORT.md); no original code/assets or shared dictionaries were changed.
