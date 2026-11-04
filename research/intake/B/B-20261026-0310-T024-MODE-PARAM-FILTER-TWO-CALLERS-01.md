# B historical research intake — 0x41EF50 mode-dependent owner filter, count cap and two-caller argument separation

- ID: `B-20261026-0310-T024-MODE-PARAM-FILTER-TWO-CALLERS-01`; owner B; tasks T024.
- Source report: `data/T024_MODE_PARAM_FILTER_TWO_CALLERS_NATIVE_20261026_03H.md`, source Markdown SHA256 `6C7BB704A31FED10D12914848E2980BDDA521DFFAED6155C801FAAE86BAB1F24` **independently measured on authorized PC 2026-11-02** (read-only). Historical study ID, not new discovery.
- Target original PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; unified V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (both rehashed read-only this intake). Use V9 as static index only; native proofs are scoped below.
- Stage: **PUBLISHED_INTAKE / NOT_CURATED** after exact GitHub readback. Original Gameplay Golden PASS=0, strict MATCH=0, new READY=0, DYNAMIC=0.

## Bounded research claims, source/errata and future check
- Native mode gate `0x41EFE9` compares global byte `0x65EB64` with zero. When nonzero, `0x41F020` checks the argument flag and only the nonzero-argument path can filter a candidate on owner `+0x1C` at `0x41F035`.
- Surviving candidate is evaluated through an inner vector at `+0x0C/+0x10` and Unit checks `+0x8C/+0x1F8`; the code increments a candidate count `0x65EB60` from the local 3 baseline. At `0x41F0E2`–`0x41F0F5`, owner native uses a *27-count cap* on this variable; that is **not** a proven physical Unit cap or visible UI count.
- `0x54F30A/0x54F311` gate a known caller before the prior first-Unit test; earlier reports `B-20261026-0115-T024-GLOBAL65EB64-MODE-WRITERS-01` and `B-20261026-0212-T024-TWO-CALLSITE-FIRST-UNIT-GATE-01` are prior evidence, not new additions.
- **Independent original-PE byte check this run:** `0x41EFD0` 270-byte window SHA256 `199463DBB4C9F1BEC4B91D1851F8A5727AC5C82A2C06D279BBE3EE9A3941C40E` matched the owner report. No new legal runtime observation.
- The report also notes potential inner-empty vector reachability; **no confirmed crash/bug** and no proof that caller arguments have equivalent gameplay outcomes. Next: legal producer invariants for inner vector, stack args and visible UI count.

## For selective KB admission
The curator must independently check cited source MD SHA and original bounded ASM sites, correlate prior IDs/errata, and admit only confirmed facts into REF/symbols. Address mentions are search leads, not automatically verified ABI or runtime. No raw EXE/DAT/MAP/SAVE or refused research content is stored here.
