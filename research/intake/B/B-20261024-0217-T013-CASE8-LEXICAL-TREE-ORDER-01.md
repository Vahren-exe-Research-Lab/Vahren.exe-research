# B-20261024-0217-T013-CASE8-LEXICAL-TREE-ORDER-01 — TARGET_SELECTION (historical B owner source, NOT CURATED)
Research ID: `B-20261024-0217-T013-CASE8-LEXICAL-TREE-ORDER-01`
Owner / task: B / T013
Source: `_REDEV_RESEARCH/data/T013_CASE8_LEXICAL_TREE_COMPARATOR_NATIVE_V9_20261024_0217.md`
Source SHA-256 (2026-11-02 authorized PC independent Get-FileHash, source Markdown): `FB3D04EBCAFFA8D789C5BA99F070A62CDED17DF5DD29F04677BD67B545006C2A`
Target original static PE SHA-256 (2026-11-02 rechecked): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
Ghidra unified V9 SQLite SHA-256 (2026-11-02 rechecked): `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
Review: 2026-11-02 17H JST, source document original read only; this sanitized abstract is NOT an independent re-decompilation, gameplay capture or guarantee of all report native claims.
Evidence class: HISTORICAL_SOURCE_STATIC / PRIOR_NATIVE_STATIC_WHERE_NOTED / INFERRED / VERIFY.
Stage: owner GITHUB_STAGED; PUBLISHED_INTAKE only after exact GitHub readback; NOT_CURATED.
Original gameplay Golden PASS: 0; strict MATCH: 0; new formal READY: 0; current G4 result settlement: NOT PROVEN.

## Research meaning, limited to source evidence
Original B source reports a bounded case8 tree key bytewise comparator: length-limited compare with prefix/length fallback, SSO short/heap selection and three direct 0x402C40 calls. Locally inferred negative/zero/positive comparator result does NOT prove the complete target ordering.

## Evidence provenance and address links
Owner report NEW-KEY/NEW-NATIVE-CALLS/NEW-COMPARE-ABI/NEW-SSO/PE WINDOW SHA256; referenced original x86 window 0x402C40 len0x71 SHA 0B59C8A69F290BA8624117E2FAD0F33EF176F82CBE2CC3E4907502302BB6D77C; V9 original search provenance.
- VA (source-reported, not automatically verified function boundary): 0x49E8B0;0x49F410;0x49F484;0x49F4E0;0x49F569;0x402C40;0x49F45C;0x49F477
- Fields/offsets: key+0x10 length;node+0x1C length; cap >=0x10 branch
- Prior / correction / dedup: Earlier B case8 01:10 iterator/alive-filter observation, research ID requires curator reconciliation
- Unresolved evidence: Ghidra fastcall signature is not accepted as complete ABI. Input key encoding, item identity, higher-level target sorting and gameplay behavior VERIFY. No refused XREF/VA capture.

## Safe curator continuation
Curator validate source byte SHA/native E8 pair and dedup earlier T013 case8; admit only bounded comparator if confirmed.
Selectively compare this research ID, actual PC report SHA, original PE / V9 / DAT evidence and supersedes/errata against current private develop REF/symbols/structs. If independently validated, curator may admit only the bounded proven semantics; this owner PR must not be bulk merged. The old source document may discuss other preexisting refused work; this summary intentionally contains no refused content or protected native capture. No original EXE/DAT/MAP/SAVE/ZIP, other owners, develop, dictionaries or MASTER changed.
