# REA/T015 | 2026-11-01 23H — CRT __getstream two-level lock ownership

**Research ID:** `REA-LOCAL-20261101-23H-P0-GETSTREAM-LOCK-OWNERSHIP-STATIC-01`.
**Stage:** PUBLISHED_INTAKE only / NATIVE-STATIC + conditional INFERRED / VERIFY / NOT READY. No original gameplay test.
**Original PE SHA256:** `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
**V9 composite SQLite SHA256:** `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (read-only quick_check=ok).

## Static crosswalk: what differs from 22H
- Previous `REA-LOCAL-20261101-22H-P0-FSOPEN-EMPTY-NAME-UNWIND-STATIC-01` established `__fsopen 0x005D1CB1` directly calling `__getstream 0x005D2165` at `0x005D1CFD`, with caller scope cleanup `0x005D1D63`. That CALL is **not** a new finding here.
- **New independent bounded native x86 evidence:** `__getstream` body `0x005D2165..0x005D228B` (295B); owner local original-PE window SHA256 `973BE2F2ADBB309B94ECB05282358E56E05445532EF36EFBDCD2EDF9632F2B46`. Its 9B global-unlock helper `0x005D228F..0x005D2297` has SHA256 `07DC33ADD7C561A7C3CF4B869E86CC7FC74442EF106CEE681CD4BA8A1D4141AC`.
- **Global table lock:** `0x005D2178/0x005D217A` push 1/call `0x005C1041`; common exit `0x005D227F -> 0x005D228F` calls `0x005C0F68` at `0x005D2291` with argument 1. Names `__lock/__unlock` come from V9 CRT labels, not DLL ABI proof.
- **Existing stream candidate:** flags at `FILE+0x0C` tested against `0x83` and `0x8000` (`0x005D21A5/0x005D21A9`); `0x005D21D3 -> 0x005BDB12 __lock_file2` followed by `0x005D21E2` recheck. When now occupied, `0x005D21EA -> 0x005BDB80 __unlock_file2` and scan continues. When free, FILE* is returned without an intervening **per-FILE** unlock.
- **Fresh stream candidate:** `malloc(0x38)` at `0x005D21FB/0x005D21FD`; null result returns null. `0x005D2221` indirect critical-section initialization (V9 labels `InitializeCriticalSectionAndSpinCount`, `spin=4000`); a zero result frees and clears the slot (`0x005D2233/0x005D223E`), then returns null. Successful initialization routes through `0x005D224A` indirect enter-critical-section call, stores returned FILE* and clears flags. **IAT API names were not independently re-proven**.
- **Return boundary:** `0x005D2262` masks flags, `0x005D2274` sets `_file=-1`, `0x005D2278` deactivates scope, `0x005D227F` releases **table-level** lock, `0x005D2284` puts FILE* into EAX and then epilog/RET. Thus a successful normal return **appears to transfer a locked FILE* to caller**; `__fsopen` 22H caller's `__unlock_file` cleanup is consistent. Real concurrency and exceptional unwind remain VERIFY.
- **Bounded failure nuance:** failed lock initialization `0x005D21C4`, malloc null `0x005D220E`, or critical-section init failure `0x005D2241` goes straight to common return rather than scanning later slots. This is a static branch description, **not** an observed fault.

## Provenance / tests / limits
- Source-owner report: `rea_lab/decomp_task/REA_20261101_23H_P0_GETSTREAM_LOCK_STATIC.md`, SHA256 `289B7D015CE3A6917946F26E2EF2C62EEE772B994CF242C55BBE1099342DE8A8`.
- Machine-verifiable receipt: `rea_lab/decomp_task/REA_20261101_23H_P0_GETSTREAM_LOCK_EVIDENCE.json`, SHA256 `35F8B4C164DDFEDB024FF92E00F2213E57FD65C39953EB7F6B42F77F72AD5273`. Owner audit: `REA_20261101_23H_P0_GETSTREAM_LOCK_AUDIT.py`, SHA256 `363DA5C1DA80183907BA55BE05A06B7264919A4D86D08FE888CF875710177621`.
- Independent static check: PE/V9 SHA, read-only SQLite check and PE32, two full x86 decode windows, 35 original opcode sites, nine E8 targets = **49/49 PASS**. Code and evidence remain on authorized source PC, not copied to GitHub.
- V9 info/pseudo index available; assembly is bounded native x86; callers is a single earlier `__fsopen` E8; callees are bounded nine E8. **New official five-evidence complete=0, new REA VERIFIED=0, official TODO/VERIFY/BLOCKED delta=0/0/0; original-game Golden PASS=0, strict MATCH=0, READY=0.** Previous 64 formally verified are historical, not incremented.
- **KB_CANDIDATE:** search `__getstream`, `__fsopen`, `0x5D2165`, `0x5D228F`, `0x5D21D3`, `0x5D21EA`, `0x5D2221`, `0x5D224A`, `0xB13A00` stream table, `0xB14A20` slot count. Curator destination CRT/FILE/IO reference and selected `symbols.tsv` only after independent review.
- **Next VERIFY:** native implementation of `0x005BDB12 __lock_file2` / `0x005BDB80 __unlock_file2`, unverified Windows import symbols, caller frame and exceptional lock ownership; no original game execution.
