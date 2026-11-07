# T024｜0x528700 temporary selection adapter / 0x56BA80 conditional refresh（2026-10-25 22H JST）
ID: B-20261025-2213-T024-TEMP-SELECTION-UI-ADAPTER-01
Owner: B / T024. State: STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA-V3 / INFERRED / VERIFY / NOT READY. Gameplay Golden PASS=0; strict MATCH=0; new READY=0.
## Provenance / precheck
Local Compact PC connected. Read MASTER checkpoint 196 / READY 596 (last E checkpoint, not a new recount), LANES_PROTOCOL, B HANDOFF and T011/T012/T013/T024/T028 owner tails, old un-synced/denial records, search_index README+manifest.
Original targets/hakushin067_Vahren.exe SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (actually rehashed). Legacy search.sqlite is historical; active V3 guard PASS_ACTIVE_V3_STATIC, hashes 14/14, E8 44889, JMP 6324, errors[]; V3 SQLite actual SHA=0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25. Other Ghidra/Java heavy not observed; existing Vahren process PID22984 left untouched.
## New native evidence: adaptive read-list 0x528700
0x528727 MOV EAX,[EDI+368]; 0x52872D SUB EAX,[EDI+364]; 0x528733 TEST EAX,FFFFFFFC; 0x528738 JLE 0x52884D (no 4B entries => return address EDI+348).
If positive span: 0x528790..0x5287CA clears an existing static intrusive list rooted at 0xAFD0FC, setting count 0xAFD100=0 and freeing previously linked nodes via 0x5287B6 CALL 0x5B6BBB.
0x5287D6 ADD EDI,0x358; 0x5287DD stores EDI into key/value insertion local; 0x5287E1 CALL 0x4C52D0; 0x528829 INC [0xAFD100]; 0x528836 MOV EAX,0xAFD0FC. Under successful allocation, a 1-entry temporary wrapper/list refers to owner's +358 member; it is NOT proven to be a durable Unit roster.
0x528700 native 357B SHA256=0E9D05AD4A699D732DECD7AD3674D1C99DF8079DA84EFB7F6931928DE4871A3A.
## New native evidence: UI refresh gate 0x56BA80
0x56BA89 CMP BYTE [0x65E5CC],0; 0x56BA96 CMP BYTE [0x65E600],0; 0x56BA9D JE 0x56BE44: BOTH 0 => early return. Otherwise 0x56BAA9 E8 CALL 0x528700, followed by candidate-count and vector-span gates at 0x56BAB6/0x56BAD0.
0x56BBA6 and 0x56BBFA test [candidate Unit+0x1F9] and split two presentation paths; 0x56BC5D calls the 0x609264 imported rendering function (Ghidra labels DrawEdge); 0x56BC63 writes global selection sentinel 0x65ECE4=0x80000008.
0x56BC7C / 0x56BD54 / 0x56BE33 / 0x56BE3F call 0x56BE50, whose pseudo-C includes SelectObject, FillRect, DrawFrameControl, DrawTextA/W, and DrawEdge. Hence this branch is high-confidence UI/selection refresh (INFERRED), not evidence of an actual AI action or battle result commit.
0x56BA80 native 972B SHA256=CEE60695D1AD51DEAFB140DEFC299966833D8FD4F35273A94C4FE77248548D27.
## Crossjoin (V3 direct-E8 verified by original PE)
0x527EA7 (from 0x527EA0) -> 0x56BA80, bytes E8D43B0400; 0x527F2E (from 0x527ED0) -> 0x56BA80 E84D3B0400; 0x5280F5 -> 0x56BA80 E886390400; 0x568540 -> 0x56BA80 E83B350000. 0x56BA80 direct E8 callers=18; 0x528700 direct E8 callers=10 in V3, index totals not exhaustive.
ABI type/virtual slots and runtime pointer validity are VERIFY. The static 0xAFD0FC temp reset may matter to display state but must not be equated with persistent candidates (+348/+34C, +364/+368) or Unit target selection.
## Dedup/limits/Golden
Prior B-21H established 0x527EA0 vs 0x527ED0 cleanup, 0x56BA80 CALL and tail JMP; B-20H Troop branches were prior; both NOT recounted. New delta: 0x528700 empty-vector vs temporary-list routing, list reset+one wrapper, early UI gate, +1F9 split and render sentinel. Exact B T024/T028/HANDOFF search: 0x528700/0x56BBA6/0x5287D6/0x56BA89 = 0 before this study. Full all-owner/22+10/Library2 semantic dedup remains VERIFY, including 14H OFFLINE unsynced.
Golden DESIGNED_NOT_RUN: original untouched EXE + pre-x20 DAT + identical SAVE/MAP/input/RNG, compare empty/nonempty (+364/+368), +348 list/+34C, +1F9 flag, 0x65E5CC/0x65E600, UI redraw/selection and next tick; do not count Win32 render drawing as gameplay Golden PASS.
Next P0: discover producer for Troop+0x1D/+0x1C and Unit+0x45D=1, 0x528700 owner+358 alias/lifetime, 0x56BA80 virtual-slot effects, and source-level AI target selection; use strictly local bounded read-only static evidence. No old refusal VA 0x5710C0..0x571500 retried, no original execution, no Ghidra rebuild; no writes outside B own docs/HANDOFF.