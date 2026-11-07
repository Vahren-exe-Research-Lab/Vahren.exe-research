# Memory links3: VM accesses and resolver correction proposal

Prepared 2026-11-05 against coordinator-supplied baseline `60bffac`, branch `work/kb-memory-scope`. The preparation baseline contains 486 symbols, 120 fields and 155 relations. No canonical dictionary, root, code or Git file was edited. The explicitly authorized built-in local fallback continued after previously observed connector HTTP429. Remote and network use: zero.

The final proposal contains **four missing field-access relations, one new reported code position, one new authored-source function entry, and one explicit correction to an existing symbol**. No fields or widths are added.

| Subject | Access | Existing field | Primary source |
|---|---|---|---|
| Reported code position 0x492960 | writes 2 | ScriptEngine+0x1EEC3C | T010 line 232 |
| Existing wait code position 0x4A17D8 | reads mode==2 | ScriptEngine+0x1EEC3C | T010 line 232; endpoint binding lines 97-104 |
| Existing resolver 0x467F40, with proposed name correction | writes Ctx reference | Power+0xE0 | T014 line 142 |
| Newly proposed resolver 0x467E90 | writes Ctx reference | Spot+0xB0 | T014 lines 571-572 |

All proposed summaries are Japanese. Position 0x492960 remains `code`: no function entry, boundary or exact instruction encoding was revalidated. The new 0x467E90 `func` proposal follows the authored report's explicit resolver/callee description and separate-function statement, after parent independent review. This is no new native inspection. Existing wait remains `code`. Existing field types, including unknown currentExecutionMode and all four UnitRuntime HP fields, are untouched.

## Existing symbol conflict

Baseline 0x467F40 is `Spot_FindByName`, inferred from F49. F49 does not prove that Spot identity, and F52 still keeps its object type VERIFY. Later F79.3/F79.8 explicitly distinguish faction 0x467F40 from spot 0x467E90. Accepted T014 line 142 identifies a Power-map lookup and a returned Power+0xE0 write. Current REF_SAVE_FORMAT line 10 defines the old save-study term “engine” as Ctx, distinct from ScriptEngine. Both resolver relationship summaries therefore say Ctx.

CORRECTION_PROPOSAL.md preserves the exact old row, F49/F52 uncertainty, later F/T014 evidence and both saved/original F hash identities. Parent independently reviewed those clauses and authorized preparing explicit correction 13. PROPOSED_SYMBOLS.tsv proposes `Power_FindByName` with historical-source confidence, keeps F49 as history and appends original ledger labels for the later F/T014 evidence. Parent should apply the correction/name qualification together with the Power edge. This task has not renamed any canonical symbol. The former conditional-only artifact was removed from this owned directory after review; all four final edges are in PROPOSED_RELATIONS.jsonl.

## Owners and excluded alternatives

Current REF_BATTLE_AI_MORALE and REF_SCRIPT_VM_CONTEXT supply explicit ver0.67/STATIC scope; REF_SAVE_FORMAT supplies the Ctx terminology correction. Their original PE hash is E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187. The PE itself was not opened. Historical authored access clauses add no new native, runtime, ABI, READY, VERIFIED, Golden or strict-MATCH evidence.

Spot+0xB8 reservation INC/DEC and resolved candidate+0x78 were excluded because the accepted 22H/23H reports keep object identity/type provisional. Unit+0x75/+0x77 gates do not justify a UnitDef/UnitRuntime alias. Prepass 18H proves ESI=[EBX+4]+0x504 for one caller, but does not establish that [EBX+4] is GameManager. No ScriptEngine pointer fields or prepass mode edge was inferred from the offset pattern. T010 line 230 names the 0x433900 family without independent entry/range proof for 0x4338D0, so that copy edge was also omitted. Existing clock/frame-vector relationships were not duplicated. Fewer than five accepted relations is intentional.

All previously held/refused helper, erase, E13, castle/CSCI/rsc3/rsc4 and other excluded scopes remained outside proposal endpoints and evidence. No original, native, script, linked JSON evidence, log, EXE, DB, archive, media or network source was read or executed. Existing relations.jsonl was read as required dictionary metadata only. The accepted F text is a partial screened published derivative: only its saved authored clauses were used. No omitted F body, screening JSON or original was opened.

## Artifacts

- PROPOSED_RELATIONS.jsonl: four rows with the exact standard relation/source-object schema.
- PROPOSED_SYMBOLS.tsv: standard six-column rows for new code 0x492960, new function 0x467E90 and the existing 0x467F40 correction. Original accepted root-ledger labels support SourceLinks resolution.
- PROPOSED_FIELDS.tsv: only the standard seven-column comment header, with no field rows.
- EVIDENCE.tsv: literal saved line excerpts, hashes, roles and limits, including the secondary wait address binding.
- INPUT_RECEIPTS.tsv: 14 preparation snapshots. SKIPPED.tsv records exclusions and review resolutions.
- CORRECTION_PROPOSAL.md and VERIFICATION.md: correction rationale and completed integrity checks.

Only research/recovered/memory_links3/ was written. Parent reviews and applies independently. Preparation snapshots are not a guarantee that later parent integration leaves canonical files unchanged.

## 親による採録

独立レビュー後、467F40の訂正、別のSpot関数467E90、報告位置492960と4読書き関係を採録した。新しい型・幅・RTTI・ABIや実機確認は加えない。既存4辞書引用は引用バイトを保って全体SHAだけ更新した。APPLIED_MEMORYとDICTIONARY_REANCHORSに変更行・件数・SHA・保持範囲を記録する。
