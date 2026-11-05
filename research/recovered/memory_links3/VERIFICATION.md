# Final proposal verification

Checked 2026-11-05. Integrity, source association and schema checks only; no native behavior was revalidated.

- Current preparation baseline has 486 symbols, 120 fields, 155 relations and 1545 root recovery-ledger rows. All 14 recorded inputs still match snapshot bytes and SHA-256 after this task's writes.
- Four distinct missing relation triples/IDs use exact existing relation and source-object schemas. All objects are existing fields. No new field or width/enum/Unit owner alias is introduced.
- Three symbol proposal rows use the standard six-column schema: new code position 492960, new historical-source function 467E90, and explicit existing 467F40 correction. Baseline 467F40 still says inferred Spot_FindByName; the proposal does not silently modify it. New code stays code, existing wait stays code. All human-facing symbol/relation summaries are Japanese.
- Parent independently reviewed old F uncertainty and later F/T014 owner clauses before authorizing the resolver correction and new function proposal. Correction13 preserves old F49 history, distinguishes later Power versus Spot claims, and leaves full ABI/runtime unverified. Current REF_SAVE_FORMAT Ctx terminology prevents a ScriptEngine alias.
- All four primary source hashes match accepted root-ledger destination identities. Exact saved line bounds are valid. Every EVIDENCE.tsv literal excerpt was rebuilt and matches, including wait's secondary endpoint binding at T01097-104 and operation at 232. F correction citations use the published partial derivative SHA, explicitly distinguished from original-source SHA; omitted F content was not opened.
- All symbol proposal source cells contain original accepted ledger labels for SourceLinks routing. Proposed field table has only the standard seven-column comment header. No obsolete conditional-only relation artifact remains.
- Spot reservation/candidate/Unit flag types, prepass owner projection and unanchored 433900-family copy were skipped. Held/refused helpers/erase/E13/castle/rsc scopes were excluded. No original/native/script/linked JSON evidence/log/EXE/DB/archive/network source was read or executed.
- All outputs strict UTF-8 decode without replacement characters. No canonical/root/code/Git writes; only research/recovered/memory_links3/ changed. No new native/runtime/READY/VERIFIED/Golden/strict-MATCH claim.

Baseline60bffac is coordinator supplied, not independently Git-queried. Input receipts are proposal-preparation snapshots; parent later integration may change canonical files. Parent review/application remains separate.
