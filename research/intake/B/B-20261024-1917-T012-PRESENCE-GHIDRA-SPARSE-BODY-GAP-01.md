# B-20261024-1917-T012-PRESENCE-GHIDRA-SPARSE-BODY-GAP-01 — source-preserved B research

- research_id: `B-20261024-1917-T012-PRESENCE-GHIDRA-SPARSE-BODY-GAP-01`
- owner: B
- tasks: T012
- observed_at: 2026-10-24 19:17 JST
- source_relative_path: `data/T012_PRESENCE_FUNCTION_BODY_SPARSE_GAP_NATIVE_20261024_1917.md`
- source_sha256: `1f2e7076bbadc9bcd0a38c3e069ebc085dc704c29cab0b66a82c44f7a5cb836f` (actual authorized research-PC Markdown byte SHA-256 rechecked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no fresh PE hash in this intake)
- original_source_kind: saved original-PE ASM / V9 or historical index / normalized DAT, as attributed below; current independent runtime = VERIFY
- evidence_va_call_offsets: `0x464290..0x46444A, gap 0x46444B..0x46444F, 0x464450..0x4645B6, 0x4645B3, body_size 802, span 807`
- prior_ids_and_errata: B-OFFLINE-20261024-17H-T012-STR-RATIO-PRESENCE-RET50-01; B-OFFLINE-20261024-18H-T012-PRESENCE-TAIL-CFG-01 (earlier Ghidra size uncertainty)
- supersedes: only expressly mentioned source corrections; other older interpretations remain linked
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: newly READY 0 / formal E MASTER update 0
- intake_stage: OWNER_STAGED; only a successful exact GitHub readback establishes PUBLISHED_INTAKE; not CURATED

## Reusable research evidence

A **correction to Ghidra size interpretation**: the original Ghidra source for `0x464290` reported body_size=802 and address span=807 across TWO distinct ranges, `0x464290..0x46444A` (443 bytes) and `0x464450..0x4645B6` (359 bytes). The intervening five bytes `0x46444B..0x46444F` are a short JMP `EB 03` and a three-byte NOP-equivalent `8D 49 00` in the historical original-PE check. Therefore entry+body_size-1 is NOT a reliable final address and earlier 18H doubts about missing tail were overbroad; the success tail is already part of range2. This DOES NOT repair the `void` return-type error or prove real Skill effects. Reuse Ghidra body-ranges rather than a contiguous size assumption.

## Limits and next validation

Compare canonical V9 function-body ranges and disassembly of allowed 5-byte gap; retain distinct return/ABI correction. The old owner source and cited sites are the verification authority; this text is a sanitized reusable research note, NOT a new native experiment, complete game-engine contract, or G4 result transaction proof. Independent curator must check original SHA, permitted V9 ASM/DAT, earlier REF/dictionary confidence and correction lineage before adopting semantic facts. No raw executable, original game assets, absolute private paths, token/logs, denied-operation content or large database is published.
