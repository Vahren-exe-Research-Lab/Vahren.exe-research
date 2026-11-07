# VM/time memory curation review

Scope: append-only curation of already reviewed repository prose at base43233091. No original game, binary/native dump, SQLite, linked payload, code/build, Git mutation, or new runtime experiment is part of this review. Historical STATIC claims remain STATIC; original gameplay Golden PASS=0 and strict MATCH=0 remain unchanged. Existing screened findings exclusions and unknowns remain in force.

## Accepted entries

Appended **6 fields**, **4 code-position symbols**, and **18 relationships** (6 reads, 11 writes, 1 uses_layout). Existing dictionary lines, order, names and confidence values are byte-preserved; parent integration refreshes only the evidence SHA of the existing dictionary-backed relation after proving its cited line unchanged. No existing function or field is renamed or retyped.

`ScriptEngine` is a dictionary layout label for the documented embedded object **E**, not a recovered native C++ class or RTTI name. The corrected findings §82.1 explicitly identifies **E = engine = G+0x504**, distinct from G=GameManager, and describes its initialization and use as ECX. Accordingly, `field:GameManager:0x504 uses_layout struct:ScriptEngine` connects the existing embedded engine field to the new layout. No generic E/engine alias or new global address symbol is added.

| E-relative offset | Type | Dictionary field | Accepted evidence boundary |
|---|---|---|---|
| 0x1EED60 | i32 | resettableElapsed | T010 line108 explicitly calls this an `int32` returned by getTime at0x4518FA; lines127–130 identify setup/reset writes. |
| 0x1EED78 | vec | executionBlocks | T010 lines229–259 establish four parallel vectors, their base offsets, current-frame fetch and install transform; line344 identifies the four end-pointer pops. |
| 0x1EED88 | vec | executionPCs | Same vector proof. PC zeros inserted at begin in frameInstallMode0; ordinary mode1 appends. |
| 0x1EED98 | vec | executionModes | Same vector proof. Execution mode is independent of scenario phase identity. |
| 0x1EEDA8 | vec | executionFrameKinds | Same vector proof. Frame-kind zeros inserted at begin in frameInstallMode0. |
| 0x1EEC44 | u8 | battleActive | T010 line375 explicitly tests `byte[engine+0x1EEC44]` in mode2 at0x4335FA, then retests after the tick. |

The four aggregate vec fields do not assert element signedness, a complete STL ABI, vector object extent, or native template/class identity. Their documented last-element accesses and four-byte end-pointer decrements remain operation-specific evidence, not a guessed full Engine layout.

## Relationship proof boundaries

All new relationships have repository-relative source path, exact source SHA256 and inclusive line bounds. Source intervals contain the operation, registered endpoint and typed field/aggregate evidence. Owner identity is additionally anchored by the separate embedding relationship.

- **Elapsed counter:** read at0x4518FA uses T010 line108. Writes at0x492710 and0x492890 use lines108–127; reset at0x4B47FC uses lines108–130. The larger contiguous ranges retain the explicit int32 proof together with the writer codepoint. No unconditional per-frame increment relation is added.
- **Four frame reads:** code0x4339B1 uses T010 lines229–256, which include base offsets and last-element fetches.
- **Four frame installations:** code0x433203 uses T010 lines229–259, preserving the asymmetric frameInstallMode0 transform. Neither replaceRoot nor empty-stack preconditions are inferred.
- **Four frame pops:** code0x433A2A uses T010 lines229–344. This intentionally broad contiguous range joins the named aggregate/base-offset proof to the explicit0x433A2A..0x433A80 four-vector pop operation. It does not claim that all intervening prose is newly verified.
- **Active-byte gate:** code0x4335FA uses T010 lines375–376, a local mode2 gate with tick-before-retest ordering. No global scheduler exclusion or legal-scene reachability is inferred.
- **Embedding:** findings lines3538–3545 contain the corrected two-origin table, E=G+0x504 and the G/E distinction.

All four added symbol endpoints are **kind code**, not func: phase install0x433203, current-frame fetch0x4339B1, completed-frame pop0x433A2A, active-byte gate0x4335FA. No function-entry claim is manufactured from a branch/handler position.

## Deferred rather than guessed

- **wait E+0x1EED58:** REF and T010 identify the slot and operation, while findings §1.4 give signed sentinel/overflow examples. This review does not promote those examples into a new literal int32 width declaration; no typed field or reader/writer endpoint is added for wait.
- **absolute clock E+0x1EED64:** timing separation and modulo operation are explicit, but the reviewed prose does not independently label this slot int32/u32/dword. It is not assigned the adjacent getTime field's type by proximity. No typed field or link is added.
- **T031 phase predicates:** its engine+0x1EF140 / +0x1EF4C1..C4 wording conflicts with the corrected G/E origin distinction in findings §82.1. No offset subtraction or owner reassignment is silently applied. Existing historical statements remain intact.
- **T031 persistent map wording:** engine+0x30C/+0x310 is not converted into a new owner identity or linked to Ctx+0x30C solely because the numeric offsets match.
- **T005 grammar/scalar slots and ScriptIF fields:** names/offsets alone do not establish all requested storage widths or owner identity. No speculative typed AST layout is added.
- **Tick scope:** T010 early prose says per-tick increments; later lines384–400 describe early returns and separate argument/UI/body gates. The present links do not assert an unconditional tick, first-visible-tick, or runtime cadence. The two clock meanings remain distinct.
- Excluded VA ranges, withheld studies, serializer inverse writes and unresolved runtime effects are not used as new evidence.

## Source receipts

| Source | SHA256 |
|---|---|
| research/recovered/script_topics/T010_EVENT_SCHEDULER.md | `1f07c79b4b9ff6a0b674548b77082b53ebf6e8bb9313ff5efa2127c72d96ef2b` |
| research/recovered/findings/PEER_SCRIPT01_FINDINGS_20261011.md | `6c61b104076363710e09535c6db62daedbe0f0ee159a6ce3240aceb4f417d2d8` |

The screened findings copy is only partial recovered evidence. Source labels and historical confirmations do not override screening or create new ACTUAL evidence.

## Preservation and verification

Before append, original byte-prefix receipts were: structs.tsv13176 bytes SHA256`d6228f5b4ab5e85f5cfe4aac5b2eebced7b7ccf0508bc412a2600c8f8c1fa6bd`; symbols.tsv108785 bytes SHA256`8e24e13d46b525559479acfd06cd2eaafb46f3e7607650d18263b888da178612`; relations.jsonl70771 bytes SHA256`dba5a388d4d5d6a3d2439afe17a836b78a59f57e1e366a4a735e35e4157207b7`.

Local read-only checks confirm the two dictionary prefixes byte-identical, exactly6/4/18 appended rows, unique relationship IDs and triples, matching source hashes, valid inclusive line bounds, and every new read/write source interval containing its literal endpoint VA. Repository loader/encyclopedia integration and dictionary-backed correction receipts are left to the coordinating task; this review does not edit correction ledgers or claim those checks have run.

Parent integration: all18 new relationship summaries are Japanese; frameInstallMode is explicitly distinguished from executionMode. Eight dictionary-backed correction citations and the existing PANEL-SHARED-LAYOUT relation were re-anchored only after exact cited-line preservation checks. No old interpretation was changed.

Integration note: the relation file initially preserved the old prefix; after the necessary PANEL dictionary-source SHA refresh, old relationship meanings and cited lines remain unchanged. File byte identity is claimed only for the existing dictionary prefixes, not for the refreshed relation receipt.
