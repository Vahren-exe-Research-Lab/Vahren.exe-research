# B-20261031-13H-T013-SORT-ANCHOR-TIE-CORRECTION-01 — B historic T013 source intake

- research_id: `B-20261031-13H-T013-SORT-ANCHOR-TIE-CORRECTION-01`
- owner: B
- tasks: T013 (Battle candidate targeting and ordering)
- observed_at: 2026-10-31 13H JST
- source_relative_path: `data/T013_DUAL_SCORE_SORT_ANCHOR_TIE_CORRECTION_NATIVE_20261031_13H.md`
- source_sha256: `6c09ea760deb4fdd6c6793648833d22c2b246a94a8aeb82bb8c9fb6fafa9cb18` (2026-11-02 JST actual PC report UTF-8 byte SHA256 and file-size verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (prior source target; executable not independently rehashed this intake)
- evidence_va_call_offsets: `0x448F73/0x448F84/0x44926E/0x449276→0x47BB50;0x47BBF6→0x44D6A0;0x47BB83→0x47BCC0;0x4492AF/B7/BB/BF;candidate+0xA0C/+0xA10`
- prior_ids_and_corrections: supersedes/errata: B-20261031-12H-T013-DUAL-SCORE-COMPARATORS-01 adjacent-tie or previous-score ranking description; older generic sort and comparator are linked, not counted again
- evidence_kind: historical source STATIC original ASM / V9-index CALL and INFERRED where described, VERIFY for final semantics; original game DYNAMIC=0
- golden_status: original gameplay PASS 0, strict MATCH 0
- ready_status: newly formal READY 0; E MASTER changes 0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback, not CURATED

## Reusable historical findings

Historical primary x86 verifies caller-clean comparator and range arguments to `0x47BB50`: mode==2 selects `0x447240` (`+0xA0C`), otherwise `0x447260` (`+0xA10`). In the **2–32 element** insertion-sort path `0x47BBF6→0x44D6A0`, comparator false on exact equal score is consistent with keeping those elements in input relative order; the **33+ element** partition branch `0x47BB83→0x47BCC0` has no proven global tie stability. Crucial ranking correction: `0x4492AF` compares the fixed anchor EDI to sentinel `0x80000008`, `0x4492B7` initializes it to the first non-sentinel value, and `0x4492BB/0x4492BF` compare each later raw score **against that unchanged anchor**, decrementing EBP=10000 each time they differ. Thus ordered example `[20,20,8,8]` yields `[10000,10000,9999,9998]` in the bounded model, not a single tied second rank; the example is synthetic and not legal-game Golden. Sentinel exceptions, comparator ABI, and actual action are still VERIFY.

## Provenance and next verification

Curator must replace 12H imprecise adjacency claim with fixed-anchor rule only for the verified native path; validate mode2 and other branch with permitted original byte windows, and distinguish <=32 from >32. This is a sanitized owner report summary with original relative source and measured SHA, not a new full disassembly or dynamic game validation. Dedicated KB curator alone may compare permitted V9 ASM/DAT, earlier contradictory findings, source ID and correction lineage before entering REF/typed dictionaries/develop. No game executable, DAT, SAVE, giant DB, personal data or refused material included.
