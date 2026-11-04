# B-20261029-02H-T028-QUEUE-SINK-DIALOG-ARITY-GUARDS-01 — B historic T028 result/queue research

- research_id: `B-20261029-02H-T028-QUEUE-SINK-DIALOG-ARITY-GUARDS-01`
- owner: B
- tasks: T028 (result/notification candidates; T012/T013 crossreference only)
- observed_at: 2026-10-29 original owner study
- source_relative_path: `data/T028_QUEUE_SINK_SHARED_DIALOG_ARITY_GUARDS_NATIVE_20261029_02H.md`
- source_sha256: `0af1b368b49bbba862b23c4378c415bb61ff77a41327024186b9b6b3b7aefdd5` (authorized PC Markdown real SHA256+bytes measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (previous measured original target, no fresh PE rehash)
- native_evidence_va_call_offsets: `0x48CBF8,0x48CC36/7D/C4/FE/0x48CD45 per-index bounds,0x48CD0D index3,0x48CD54 index4,0x48CD61 nullness,0x48CE5C→0x52CF50,0x48CF0B→0x52CCF0;0x52CDDE/0x52D047→0x43F470`
- prior_ids_and_errata: B 10/28 23H five-slot tuple and sinks, B 10/29 00H producer five entries, 01H index3 split; this source verifies all index boundaries and shared sink
- evidence_kind: historical original ASM STATIC / old V3 index supplement / INFERRED and VERIFY for ABI, gameplay
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0 / E MASTER unchanged
- intake_status: owner PUBLISHED_INTAKE upon matching GitHub fetch; NOT_CURATED

## Reusable owner research facts

Original static consumer `0x48C880` iterates 0x1C-byte string records in tuples of five. Before each element index 0,1,2,3,4, it separately guards that vector count exceeds that index, otherwise takes the out-of-range path; first group starts at index0 and advances base by5 per next tuple. Index3 pointer is selected as heap or inline buffer, and **nullness** decides between `0x48CE5C→0x52CF50` and `0x48CF0B→0x52CCF0`. Contrary to earlier "two unrelated UI sinks" intuition, both callee paths converge to the **same `0x43F470` dialog core** with different string-preparation call counts; exact layout and live display are VERIFY. A static five-item guard does not guarantee corrupted/out-of-range tuples safely resume, and no successful original game event/G4 side effect has been observed.

## Next verification

Verify allowed native consumer/sink prep and legal five-record source from 00H, preserve original-game Golden and error path UNKNOWN. Curator must validate permitted current V9 original ASM/DAT and existing corrections before any REF/symbols/develop acceptance. No original game files, large DB, private addresses, or previously refused operation content was uploaded. Static event/queue control is not proof of original game action or G4 external battle settlement.
