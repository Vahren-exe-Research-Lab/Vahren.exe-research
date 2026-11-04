# Battle-limit global relationship review

Scope: append-only curation at base69de6a29 of already reviewed repository prose. No original-game, native dump, SQLite, payload read, runtime experiment, build, Git mutation, dictionary edit, correction edit, or root-ledger edit was performed. Historical STATIC evidence remains STATIC; no gameplay Golden PASS or strict MATCH is claimed.

## Accepted relationships

Exactly **5 direct global-memory relationships** were initially appended to `reference/relations.jsonl`. Both globals and both helper endpoints were already declared in `symbols.tsv`; no new symbol, width, layout, or function boundary is inferred. Global endpoints use the existing `va:` convention.

| Helper endpoint | Operation | Global endpoint | Source inclusive lines |
|---|---|---|---|
| `va:0x00565700` | reads | `va:0x0067B938` / g_BattleLimitMode | 109–110 |
| `va:0x00565700` | reads | `va:0x0067B93C` / g_BattleLimitRemaining | 109–110 |
| `va:0x00565700` | writes | `va:0x0067B93C` / g_BattleLimitRemaining | 109–110 |
| `va:0x00565730` | reads | `va:0x0067B938` / g_BattleLimitMode | 109 |
| `va:0x00565730` | reads | `va:0x0067B93C` / g_BattleLimitRemaining | 109 |

Each citation is to `research/recovered/script_topics/T010_EVENT_SCHEDULER.md`, SHA256 `1f07c79b4b9ff6a0b674548b77082b53ebf6e8bb9313ff5efa2127c72d96ef2b`. Line109 supplies the literal state `[0x67B938]`, current `[0x67B93C]`, helper0x565730 and its sentinel branch. Line110 supplies helper0x565700 and its current-value update; the bounded109–110 interval joins that explicitly named current/state vocabulary to the literal global addresses.

For helper0x565700, sentinel0x80000008 selects increment of current; the other state decrements only when current>0. For helper0x565730, sentinel state selects semantic return0x7FFFFFFF; current is the documented return in the other branch. That semantic result is not evidence that a speculative memory load, guard, or absence of a guard occurs on the sentinel branch. All links are ver0.67 historical static claims, not new execution evidence.

## Deferred proof

- Helper0x565750: line110 describes initial-current in timed mode and current in sentinel mode, but does not explicitly bind this helper's operands to literal memory addresses. No reads link to either global, and no invented initial-memory address, is added.
- Handler0x45190B calls0x565730 at line109. A transitive helper read is not promoted to a direct handler/global memory link. Handler0x451915 concerns isInterval and supplies no battle-limit-global read/write proof here.
- No writer of g_BattleLimitMode or setup assignment of either global is established by these bounds. No storage width follows from adjacency, sentinel constants, or arithmetic prose.
- Lines128–131 contain clock/cadence discussion, but no unconditional ticking, legal-scene reachability, concrete callsite VA, or new10-tick cadence link is asserted. The prior unknown absolute-clock width and suspicious T031 offsets remain deferred.
- No excluded address range, withheld owner, original body, downstream5767B0/5769B0, or unscreened finding is used.

## Preservation receipt

The original132 records are byte-preserved as the first82,238 bytes, SHA256 `065a434b82eb24d54f6d56e7a3943a41dec5f74a36b6b6f57f2314a85e2e3b08`. The file now has137 records. Immediate local checks confirmed exact prefix identity,5 unique new IDs/triples, valid JSON, and the cited source SHA. Only this review and the append to relations are authored here; the coordinating task owns repository-wide validation and publication.

## Parent integration: handler navigation

A sixth relationship records the explicit line109 statement `getLimit handler0x45190B calls0x565730`. This is a handler-to-helper calls edge, not a direct handler-to-global reads edge. The source declares no exact CALL instruction position or ABI, so none is added. The resulting path is handler → helper → existing global, preserving the direct/transitive distinction. Total138 relationships; original132-record prefix remains byte-identical.

## Indexing verification

At549 recovery rows, citation matching exceeded Python’s shared regular-expression cache and repeatedly rebuilt the same label patterns. The CLI now memoizes only compiled label patterns, with the exact original boundary expression. No compiled object enters source-link data or JSON. A local synthetic600-label×60-row check kept identical links and changed from4.076s to0.084s; this is indexing verification, not game evidence or a portable timing guarantee. All41 existing reference fixtures and1,575 independent boundary comparisons passed.
