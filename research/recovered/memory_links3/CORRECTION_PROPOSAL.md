# Proposed correction13: inferred467F40 Spot label versus later Power evidence

Proposal only. Parent independently reviewed F1308/F2873,T014142/571-572 and the current Ctx terminology and authorized preparing this explicit correction13 and the two resolver relationships. No canonical rename,confidence change or correction entry has been applied by this task.

## Existing dictionary statement

symbols.tsv line64 at preparation contains:

```tsv
0x467F40	func	Spot_FindByName	スポット（領地）を名前で引く（推定）	推定	F§49
```

Complete baseline symbols.tsv SHA256 is recorded in INPUT_RECEIPTS.tsv. Its cited F49 is not itself evidence that467F40 returns Spot.

## Exact old and later authored evidence

- Saved F49 lines1255-1271:467F40(def+A0)+128 provides a string vector; a chosen entry must subsequently resolve as a Spot. Line1266 separately names467E90 as the current-Spot resolver. This does not prove the467F40 object is Spot. F52 line1308 explicitly keeps the467F40 object type VERIFY.
- Later saved F79.3 lines2868-2873 explicitly maps faction=467F40,def=467DE0,spot=467E90. F79.8 lines3052-3056 separately attributes Spot addGain/castle/capacity to467E90 and faction training/base-level operations to467F40.
- Accepted T014 lines139-142 explicitly states467F40 looks up the Power map at owner+2DC/2E0,returnsPower and sets returnedPower+E0 to its owner. This is a direct authored identity/access claim,not an RTTI or matching-offset inference.
- Current REF_SAVE_FORMAT.md lines3-10 defines the old save-study term engine as Ctx=GM+1B8,distinct from ScriptEngine E=GM+504. Thus the E0 back-reference is Ctx,not ScriptEngine. Existing Power+E0 field is already ptr/ctx and cites this resolver/T014; no new field/type is requested.

The accepted saved F document is a SCREENED PARTIAL DERIVATIVE: published destination SHA2566c61b104076363710e09535c6db62daedbe0f0ee159a6ce3240aceb4f417d2d8. Its root ledger separately records original-source SHA2569e5ceec9635f2c0306c9417bef1648722f8c354c382a3049986507fc7bbb5c34. Exact cited line numbers and quotes here refer only to the published saved derivative. No original,F screening JSON,omitted paragraph,appendix or linked evidence was opened. Do not treat the derivative as complete/manual validation of the original.

T014 saved/full-source SHA256a07cc0081722b4370540a51ca7b8cded919ad1a4eb54cd4b69463a8ad2df586a matches its root-ledger source/destination pair. EVIDENCE.tsv pins all exact clauses and literal excerpts;INPUT_RECEIPTS.tsv pins each document and current curated terms.

## Proposed result after independent review

Suggested name: Power_FindByName. Suggested bounded summary: resolve a name through the Ctx Power map and set returnedPower+E0 toCtx,as described by accepted authored T014. Preserve func kind,leave full ABI/exception/runtime behavior unverified,and do not claim a new native inspection. Source reference should include original ledger label data/T014_GLOBAL_SAVE.md line142 and dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md F79.3/79.8,while retaining F49 as superseded/unsupported naming history rather than erasing it.

PROPOSED_SYMBOLS.tsv now includes the explicit existing467F40 correction to Power_FindByName and a separate new467E90 Spot_FindByName function proposal,both qualified as historical authored-source claims without a new native rerun. PROPOSED_RELATIONS.jsonl includes Power+E0 and Spot+B0 writes alongside the two VM relations. Parent must apply correction13 together with the467F40 rename/qualification before installing its relationship. The obsolete conditional-only artifact was removed from this owned proposal directory. No field width or function ABI is promoted.
