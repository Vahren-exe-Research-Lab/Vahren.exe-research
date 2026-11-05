# REA T014 — save token reader caller scope and global scratch audit (2026-10-12 07:38 JST)
- Independent saved-evidence review only; REA/Ghidra new execution 0; new VERIFIED +0; original executable/game NOT RUN.
- Target: approved copy hash E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (current Get-FileHash MATCH).
- Scope: T014 0x4705F0 string-token helper; T014 0x470700 numeric helper; preserved Wave5 results.
## Observed caller scope
- Ghidra 0x4705F0 procedure_callers reports **13 distinct resolved calling functions**; evidence ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87.
- 0x598980 (Spot runtime reader) invokes 0x4705F0 for initial fields and repeated record keys; saved pseudo ev_0acff01a3a0b32c2efc27bc4c2c113a5990bee48a71916922824806d419968ad.
- 0x5964C0 (Power runtime reader) invokes 0x4705F0 for header/field tokens and repeated variable-length keys; saved pseudo ev_9608d350a99e5ba1453392474e951d01a83321124085c78de8ef29ffc8ea96d9.
- 0x435550 (Spot graph reader) invokes 0x4705F0 before constant-tag comparisons and within successive graph record loops; saved pseudo ev_7a9e58e9b0b538edf453aaf98e7755f5ebedda9102d81657c549716351eec905.
- 0x471AF0 (diplomacy runtime reader) invokes 0x4705F0 for record identifiers before resolution into known runtime entities; saved pseudo ev_1e776fb470e6e934d7fffa736600daa070a5e3e009552f7951f653edbc00f871.
- Remaining nine resolved caller functions are NOT assigned an assumed record family here. Indirect/unresolved calls are outside the 13 count.
## Native scratch contract
- 0x4705F0 assembly ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d: zeroes global 0xB060F8 length 0x400 at 0x4705F4..0x470608, reads bytes into this same global, then passes pointer+actual NUL-terminated length to 0x402800 at 0x470680..0x470686. Scratch is overwritten by the next call; do not expose it as a stable returned pointer.
- 0x470700 assembly ev_f7ed3af4df1cdf7b14d9208f3d4aa735267b9ab022ee7d6b3860c4521bbb95cf uses distinct global DWORD 0xB060F0 (eight bytes before string scratch) through 0x42E700 and copies DWORD into caller destination at 0x470754..0x47075D.
- The saved native code establishes shared global temporary storage, not thread safety nor a dynamic race. Reimplementation must use per-reader/per-call destination lifetime and preserve call ordering, while actual concurrency is NOT TESTED.
## Scope/VERIFY and golden separation
- The already observed signed-byte allowed 0x20..0x7F and max 255 non-NUL bytes apply to **this native token reader**, not to every save payload, language string, or script text. Prior audit: REA_T014_SAVE_TOKEN_SIGNED_BYTE_LENGTH_AUDIT_20261012_0637.md.
- Boundary fixtures for the T014 owner (not executed): 0x7F versus 0x80, lengths 254/255/256, NUL absent and subsequent-tag alignment, EOF/stream-state exception, multiple sequential reads. No T018 file changed.
- The 13 caller taxonomy is incomplete; additional caller-specific label semantics and downstream overlength behavior remain VERIFY. No static evidence promoted into gameplay golden.
## Latest static progress/safety
- Latest saved sync progress_sync_20261011T153958076Z: Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 12/12, Wave5 16/16 = 64/64 STATIC VERIFIED; P0=29/29, P1=35/35; new +0.
- Wave6 is not formally registered: candidate 0/16, candidate P0=5/P1=11, TODO16/VERIFY0. queueUpdate=STALE_RENAME_DENIED and humanReadableProgress=SKIPPED_QUEUE_STALE; no EPERM retry or alternate overwrite.
- Latest MASTER checkpoint83: DONE9/34 (IN_PROGRESS21/VERIFY4); old-EXE actual gameplay golden PASS0; game reimplementation percentage NOT MEASURED.
- Start preflight Local CPU 0%, free RAM 15.82GiB, Java/Ghidra none, active.lock false, approved-copy SHA MATCH. New REA execution 0s; read-only audit wall time not measured.
- REA 6.1.0/Ghidra 12.1.4 policy retained: single MCP session, max 4 functions/run, Ghidra 900000ms, request 960000ms. No safety-refused ranges or extraction retried.
- Next: review saved callers 0x428010/0x45E1E0/0x58E870 and streaming boundary without changing A-E owner files; Wave6 only after legitimate queue update.
- Original ZIP/EXE, A-E/MASTER/T018, dev, Git/push/publication, MCP settings, schedules all untouched.
