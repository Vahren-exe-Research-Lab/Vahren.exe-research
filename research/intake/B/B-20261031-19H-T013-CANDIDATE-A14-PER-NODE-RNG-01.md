# B-20261031-19H-T013-CANDIDATE-A14-PER-NODE-RNG-01 — B historic T013 source intake

- research_id: `B-20261031-19H-T013-CANDIDATE-A14-PER-NODE-RNG-01`
- owner: B
- tasks: T013 (Unit candidate lists / target-selection prerequisites)
- observed_at: 2026-10-31 19H JST
- source_relative_path: `data/T013_CANDIDATE_A14_PER_NODE_RANDOM_SCORE_NATIVE_20261031_19H.md`
- source_sha256: `01af13e11c52a77b5d32ecef86fe5c40fe6b019e07d853b822b04d2349168a84` (2026-11-02 JST authorized PC original Markdown SHA256/byte-length verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no new executable hash during intake)
- evidence_va_call_offsets: `0x577AA7/0x577D47→0x57A7D0,0x57A7D9,0x57A7E0,0x57A7E3→0x5B6EAB,0x57A7F0/0x57A7F6,0x57A7FC→0x5D1B80,0x57A808 candidate+0xA14,0x5A3EDA/0x5A3EEC`
- prior_ids_and_corrections: 15H and 18H source use a DISTINCT random field record+0x28; 16H native comparator may use candidate+0xA14. Do not count known 0x5B6EAB or ftol as new.
- evidence_kind: historical source STATIC original ASM / V9 CALL and INFERRED, VERIFY for interpretation; original game DYNAMIC=0
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / no E MASTER formal update
- intake_status: PUBLISHED_INTAKE on exact GitHub readback; NOT_CURATED until independent KB review

## Reusable historical evidence

Historical original PE shows two direct `0x577AA7` and `0x577D47` calls into `0x57A7D0`. This helper iterates a candidate linked list and, **for each node if list nonempty**, calls `0x5B6EAB` RNG, multiplies via x87 constants 1/32768 and -8, converts through `0x5D1B80`, and writes candidate `+0xA14` around `0x57A808`. The local arithmetic is a candidate `-4 - ftol(raw_rng * (-8/32768))`; exact FPU rounding/seed and legal range remain VERIFY. The separately researched `0x5A3EA0` comparator can add `+0xA14` for eligible base scores `+0xA0C/+0xA10` above signed threshold `0x80000065`. This is an evidence link from a per-node RNG-derived field to a conditional sort score; it does not prove it always changes ordering or that final attacking target matches the list's first element. Distinguish from context `record+0x28`.

## Provenance and next verification

Check permitted V9 callsites and exact PE constant bytes, count eligible nodes and consumption order in legal original game before claiming Golden. This owner-created sanitized summary references the real B source by relative path and measured SHA. It does not constitute new full decompilation, original-game execution, G4 external battle-result settlement or verified final target. Dedicated curator alone may interpret REF/typed dictionary/develop based on independent native/DAT and errata audit; original game files, large index, private paths and refused payloads are excluded.
