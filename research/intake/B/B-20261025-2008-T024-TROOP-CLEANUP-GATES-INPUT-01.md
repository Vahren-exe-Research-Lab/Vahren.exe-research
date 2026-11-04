# B historical research intake — Troop+0x1D-specific candidate cleanup and guarded input coordinate continuation

- ID: `B-20261025-2008-T024-TROOP-CLEANUP-GATES-INPUT-01`; owner B; tasks T024 (T028 reference).
- Source report: `data/T024_TROOP_CLEANUP_GATES_INPUT_NATIVE_20261025_20H.md`, source Markdown SHA256 `5E7FFE1EAA4B241D8559342076D5C8E707CD32334410239ACDFA0391A6E1C92D` **independently measured on authorized PC 2026-11-02** (read-only). Historical study ID, not new discovery.
- Target original PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; unified V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (both rehashed read-only this intake). Use V9 as static index only; native proofs are scoped below.
- Stage: **PUBLISHED_INTAKE / NOT_CURATED** after exact GitHub readback. Original Gameplay Golden PASS=0, strict MATCH=0, new READY=0, DYNAMIC=0.

## Bounded research claims, source/errata and future check
- Owner's limited static `0x5684B0` report: branch on Troop-like owner `+0x1D`. Nonzero branch removes candidate Unit references with `+0x1867C!=0` and may call `0x527ED0`; zero branch counts living `+0x1867C==0` entries and gates `0x527EA0` or `0x527ED0` based on front Unit `+0x8C/+0x1F8`. Flag `owner+0x1C` and global state `+0x1EF140` affect a later branch.
- Separate owner static `0x4DE410` input path requires manager `+0x1EF148` and a bounded rectangle condition; `0x4DE64D→0x528870` calls candidate update, and AL nonzero branch writes owner `+0x1A8/+0x1AC/+0x1B0`.
- Previous owner 19H already knew `0x527ED0` and `0x528870` calls; this historical ID contributes their **input gates and Troop cleanup branching**, not proof of new function existence.
- **Current intake scope:** source-report SHA and target PE/V9 hashes independently checked, cited `0x5684B0/0x4DE410` native windows *not* independently rehashed this run. STATIC_PRIOR/INFERRED/VERIFY, not gameplay.
- Owner type assumptions, empty-front dereference reachability, caller ABI, actual user-input semantics, movement and G4 post-battle effects are VERIFY. Next: legal low-impact caller source and original-game same-run test; no certainty of a crash or behavior in a real run.

## For selective KB admission
The curator must independently check cited source MD SHA and original bounded ASM sites, correlate prior IDs/errata, and admit only confirmed facts into REF/symbols. Address mentions are search leads, not automatically verified ABI or runtime. No raw EXE/DAT/MAP/SAVE or refused research content is stored here.
