# B-20261029-0113-T028-RESULT-18CALLER-INDEX3-NULL-SINK-01 — B historic T028 result/queue research

- research_id: `B-20261029-0113-T028-RESULT-18CALLER-INDEX3-NULL-SINK-01`
- owner: B
- tasks: T028 (result/notification candidates; T012/T013 crossreference only)
- observed_at: 2026-10-29 original owner study
- source_relative_path: `data/T028_RESULT_TUPLE_18CALLERS_INDEX3_NULL_SINK_NATIVE_20261029_01H.md`
- source_sha256: `618cfa867ac3982893ead0e1dff4f9cb8e237411d66b5a10ec52c6209e2a0926` (authorized PC Markdown real SHA256+bytes measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (previous measured original target, no fresh PE rehash)
- native_evidence_va_call_offsets: `0x434B10: 18 E8 sites / six callers,0x434EB0/0x45B850/0x493630/0x4962B0/0x4973E0/0x497BB0,tuple index3 at 0x48CD0D/0x48CD13/0x48CD1B,0x48CD61/0x48CE5C/0x48CF0B`
- prior_ids_and_errata: B-20261029-0015-T028-FIVE-ELEMENT-RECORD-PRODUCER-CORRECTION-01; B 10/28 23H tuple consumer and two sinks recognized before
- evidence_kind: historical original ASM STATIC / old V3 index supplement / INFERRED and VERIFY for ABI, gameplay
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0 / E MASTER unchanged
- intake_status: owner PUBLISHED_INTAKE upon matching GitHub fetch; NOT_CURATED

## Reusable owner research facts

A historical original-PE E8 survey found **18 direct callsites** targeting five-element record producer `0x434B10`, classified into 6 enclosing functions: 1 site each from `0x434EB0/0x45B850`, five from `0x493630`, four from `0x4962B0`, two from `0x4973E0`, five from `0x497BB0`. The actual ECX integer/string argument producer differs by caller; cannot claim uniform event type or identical AI side effect. Consumer `0x48C880` reads index3's string as a normalized pointer, with nullness choosing different sinks; a non-null pointer is NOT guaranteed live text, and the five-element tuple arity must be guarded. This is a static reuse map, not an 18-event runtime count, and does not mean each input creates a logged or user-visible message.

## Next verification

Check 02H per-element boundary/sink convergence and actual owner game semantics; no expansion of historical unsafe caller evidence. Curator must validate permitted current V9 original ASM/DAT and existing corrections before any REF/symbols/develop acceptance. No original game files, large DB, private addresses, or previously refused operation content was uploaded. Static event/queue control is not proof of original game action or G4 external battle settlement.
