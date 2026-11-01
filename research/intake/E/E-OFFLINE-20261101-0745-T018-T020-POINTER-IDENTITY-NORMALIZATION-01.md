# E-owned intake: preserve native-return DWORD versus cross-run semantic ID

research_id: E-OFFLINE-20261101-0745-T018-T020-POINTER-IDENTITY-NORMALIZATION-01
owner: E
tasks: T018, T020 (T019 contradiction status inherited)
snapshot_at: 2026-11-01 07:45 JST
source: ChatGPT Library /迫真戦記/E_OFFLINE_UNSYNCED/T020_CANDIDATE_IDENTITY_AUDIT_20261101_0745.md
source_sha256: 4BAF63C7636D17145CC3D2B2A3F3FCDB3EB75D52732FF9FC94CAF70653060227
source_bytes: 9684
source_verification: original Library file materialized and byte SHA-256 independently verified 2026-11-02 JST; digest matches Library readback receipt. The 07H report's bounded original-PE tests are *historic* and were not rerun today; current-PC V9 and game execution NOT RUN.
classification: bounded historic STATIC / INFERRED / SYNTHETIC / VERIFY / NOT READY
original_game_dynamic_observed: 0
actual_golden_pass: 0
strict_match: 0
new_ready: 0

## Evidence and correction
Prior offline 07H research distinguishes a DWORD-like return from the common boolean interpretation: source PE SHA256 (at prior 07H measurement) E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187. Function 0x004E53B0 showed nonzero return via EAX candidate-reference-like value at two branches, and zero on exhaustion; it was NOT proved to be the actual gameplay target. Call sites:
- 0x00545A02 (caller 0x00545740) stores return DWORD at +0x1E570.
- 0x0057AD8C (caller 0x0057AA00) preserves return DWORD at +0x1E570.
- 0x0057D982 (caller 0x0057D8B0) branches on zero versus nonzero; 0x0057D9A9 is indirect and remains unproven.

Prior Ghidra source-relative files and code SHA256:
- full_pseudoc_20261020/functions/004E/004E53B0.c — 1B74D266BE034E2984E3C4456EBE5CF5DAEBDCA07C8674A934EB34EF3F5CE1E1
- full_pseudoc_20261020/functions/0054/00545740.c — 4BD1B725B04BA8B7EE47829A7026AE9B23D8840EF747B3BDB24CE4CC4D4890D1
- full_pseudoc_20261020/functions/0057/0057AA00.c — 5827D0DF895C261CB6CFB81ABCCC730BC7F31EC977FFA0411BDF466C51E978B7
- full_pseudoc_20261020/functions/0057/0057D8B0.c — 2E0612C1CFC8295826E75095FCF6D2C37763EA867434D9E10E5667CFD0970A89

The archived 07H report documents 14/14 bounded instruction windows, 3/3 native E8 decodes, 96/96 conditional caller-value fixtures, 18/18 cross-process identity fixtures and 5/5 mutation detections. Do not treat historic synthetic PASS as this run's execution. In particular, conversion of a reference-like returned DWORD to bool loses information in A/B stores, while comparing raw old/new process pointers as strict identity gives false mismatches. A *verified* stable Unit ID at the same stage is required; no name-only or unresolved lookup can be upgraded.

## Dedup / correction / next
The existing KB symbol Unit_RefreshTargetLatch describes only a shorthand; this item offers caller-specific KB_CANDIDATE nuance, **not** a replacement symbol or newly discovered B-owned core behavior. The previously published 04H E caller-use item is an antecedent, not a duplicate of the 07H original-byte-and-identity correction. Other B-owner source claims remain attributed to B. Reproduce with archived report, receipt and source digest; compare native E8/V9 only by a separately authorized read-only inspection, not a repeat Ghidra project analysis.

G0 lawful original UI, G1 immediate SAVE+input, G2 one-run MAP/three powers/ordered deployed Unit and Troop are NOT RUN. Unresolved: indirect call, semantic target, cross-run stable ID and original gameplay. PUBLISHED_INTAKE / NOT CURATED pending GitHub readback and curator selection.
