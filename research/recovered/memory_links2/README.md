# Missing VM memory relationships: reviewable dictionary proposal

Prepared2026-11-05 against coordinator-supplied baseline9e7cb388...; no Git query was run. Proposal only: **9 missing relations and3 unrepresented ScriptEngine fields**. Existing dictionaries,root files and code were not edited. Baseline has117 fields and146 relations. Local connectorHTTP429 had already been observed; expressly authorized built-in local fallback was used. Remote operations0.

The proposed relationships use six already registered endpoints: functions0x492710,0x492890,0x492D80,0x4335E0 and existing code/handler positions0x451915,0x4A17D8. Code positions remain code positions,not newly identified whole functions. Eight relations point at proposed fields and one points at the existing elapsed field: specifically absolute-clock reads2/writes3,wait reads1/writes1,mode reads1,and existing elapsed write1. No endpoint or layout-owner alias was invented.

## Proposed coverage

| Field | Declared type | Missing relationships |
|---|---|---|
| ScriptEngine+0x1EED64 absoluteSchedulerCounter | unknown | isInterval read; battle setup and battleEvent setup zero writes; main battle-tick family read and increment write |
| ScriptEngine+0x1EED58 waitCounter | unknown | existing wait handler reads retained counter while decrementing and writes argument/decrement/sentinel state |
| ScriptEngine+0x1EEC3C currentExecutionMode | unknown | existing execution loop reads/switches mode1/2/6 |
| Existing ScriptEngine+0x1EED60 resettableElapsed | existing i32 retained | main battle-tick family increments this separate elapsed counter |

No width or declared signed/enum type is inferred for the3 new fields. Integer arithmetic,32-bit-looking sentinels and an x86 target do not alone set a field's width. The absolute counter and resettable elapsed counter remain distinct; no resetTime-write edge is proposed for the absolute counter. Current mode remains distinct from phase identity/frame-install mode.

All primary access claims come from already accepted authored report research/recovered/script_topics/T010_EVENT_SCHEDULER.md,complete SHA2561f07c79b4b9ff6a0b674548b77082b53ebf6e8bb9313ff5efa2127c72d96ef2b. The root RECOVERY_LEDGER row matches both source and destination SHA and marks LOCAL_EXACT_BYTES_VERIFIED. Only this published Markdown was consulted,not the original or its linked native/script/JSON evidence. Exact1-based source spans and literal line excerpts are in EVIDENCE.tsv and each relation's source object.

The compatible target scope is explicit in current REF_SCRIPT_VM_CONTEXT.md lines1-4: Hakushin ver0.67 original PE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; line4 names T010_EVENT_SCHEDULER as authoritative owner. Lines15/17 independently retain wait+1EED58 and the resettable/absolute clock distinction. This curated scope takes priority over old report line6's provisional7.0-era documentation wording. No V701/version-comparison behavior is imported. INPUT_RECEIPTS.tsv pins both texts,root acceptance metadata and all dictionaries by hash.

## Limits that must survive integration

Relations say what the historical authored report states; they add no independent native/runtime evidence,formal VERIFIED increment,READY,Golden PASS or strict MATCH. The main-tick author clause says0x492D80 family rather than an exact internal instruction address; that family-level qualification is kept in summaries. Existing0x492D80 symbol confidence remains inferred. The three tick relations are explicitly marked inferred because the report names a family and the proposal maps that family to the existing entry without an exact internal instruction site. Other relation confidence describes the cited STATIC claim,not a promotion of any symbol or its full semantics. EVIDENCE.tsv separately records each existing endpoint kind/confidence. Real per-scene ticks,legal transitions and native runtime reachability remain unvalidated here.

Current REF_SKILL_POST_ACTION.md lines65-76 and the existing UnitRuntime dictionary were checked for scope. HP+0x90,max+0xDC,tier+0x738,countdown+0x185F4 retain unknown widths and current Unit-like qualification; their five577100 access edges already exist. No blanket Unit/UnitDef alias or5769B0 HP-crosscall/tick addition is proposed. R/P/L identity corrections are not expanded into new inferred classes.

Known held/refused scopes,including5710C0..571500,58021E..580340,5769B0/5767B0,whole580280,4C28D0,4BC9C0,429620,5BC860,547FC0,579290,Rush5503E7..55040C/two-dash2010,castleSCI/CSCI/rsc3/rsc4 and heldE payloads,were excluded as proposal endpoints/evidence. Authored source references do not authorize linked payload reads. No original,native,script,JSON evidence,log,EXE,DB or archive was read or executed. The existing reference/relations.jsonl is dictionary metadata expressly required for comparison,not a linked evidence payload.

## Files and review contract

PROPOSED_RELATIONS.jsonl uses the exact existing relation keys and source-object schema. PROPOSED_FIELDS.tsv uses the standard seven-column structs.tsv schema with its comment header. EVIDENCE.tsv preserves literal saved lines,target scope,endpoint kind/current confidence and limitations. SKIPPED.tsv records duplicates,unregistered/ambiguous sites,held scopes and unknown types. No additions were manufactured to meet a count. Parent coordinator can inspect and apply a compatible subset; nothing has been applied by this task.

Only research/recovered/memory_links2/ was written. Input hashes and source-line excerpts were verified at initial proposal preparation; they are historical snapshot receipts, not an assertion that every shared file remains unchanged after subsequent parent integration. Parent later appended three source-only symbol locators and reanchored four correction checksums; it reports that the first five semantic symbol columns were unchanged. These parent edits were not performed by this task. Refer to VERIFICATION.md for the final proposal checks. No Git,REA,Ghidra,game,linked script,audit or native byte inspection ran.

Field source cells use the original accepted ledger label data/T010_EVENT_SCHEDULER.md so source-link attachment can resolve them. The saved destination and full content SHA remain in relation source objects,EVIDENCE.tsv and INPUT_RECEIPTS.tsv; changing this label does not change source lines or proposed semantics.

## 親による採録

3フィールド・9関係を採録し、全3項目の本文リンクが解決することを確認した。新規3項目はすべて型unknown。既存113既知型行は不変。元の構造体辞書の全バイト列を先頭に保持した。辞書を引用していた既存5件は引用範囲のバイト一致を証明して全体SHAだけ更新し、DICTIONARY_REANCHORSに記録する。意味・関係・訂正の変更ではない。APPLIED_MEMORYに採録後件数・SHA・範囲を記録する。
