# B-20261023-1519-T013-GROUP-AGGREGATE-LIFECYCLE-01 — Group +0x34 aggregate update and five lifecycle callsites (legacy V3)

research_id: B-20261023-1519-T013-GROUP-AGGREGATE-LIFECYCLE-01
owner: B
research_tasks: T013,T028
original_observation: 2026-10-23 historical B owner report (not new native analysis)
source_relative_path: data/T013_GROUP_AGGREGATE_LIFECYCLE_V3_20261023_1519.md
source_report_sha256: 7AE51EA288724AEA67005A2E727E7E0DCF8A0776C431C8055C96A962AE240856
source_sha256_reverified: 2026-11-03 authorized PC read-only whole-file; exact match
isolated_original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (identity only)
current_composite_V9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE (identity only)
evidence_kind: HISTORICAL_V3_STATIC_REPORT / INFERRED / VERIFY (V9 semantic recheck NOT RUN)
intake_stage: PUBLISHED_INTAKE after exact GitHub readback; not newly CURATED
original_game_Golden_PASS_new: 0
strict_MATCH_new: 0
formal_READY_new: 0

## Bounded evidence; not a new discovery
Historical V3 owner report identifies 0x569280 writing a derived group-like +0x34 value, with five reported direct E8 callsites 0x5684B8, 0x56880A, 0x568F5E, 0x568F9C, 0x56902C across group member add/remove/clear/recalculation contexts. It skips members with Unit+0x1867C!=0 and conditionally considers Unit+0x228; Group+0x30/+0x38 and a 'breast_width' parse site were associated in historical pseudoC. Native numeric/FPU ABI, owner identity, the exact formula, whether +0x34 is morale, and actual battle effect are VERIFY, never declared proven. Historical V3 result is not the current V9 source.

## Address/offset lookup hints, not established ABI
- Owner historical address mentions: 0x569280, 0x5684B8, 0x56880A, 0x568F5E, 0x568F9C, 0x56902C.
- Historical untyped offsets: Group+0x34,Group+0x38,Group+0x30,Group+0x1D,Unit+0x1867C,Unit+0x228.
- Same original EXE SHA and V9 index SHA were checked, but NO native V9 function/call edge or original gameplay was newly independently validated. Do not promote V3 pseudoC to current canonical V9, original-machine-code proof, class names, READY or CURATED.

## Prior IDs / correction relationship
The 14:14 historical group prune/livecount report is a separate earlier study and was not re-read, reproduced or counted. Current REF_BATTLE_AI_MORALE.md contains later group/AI crosswalks; apparent semantic overlap must be curator-checked by source SHA, not assumed as a new discovery.

## Curator-only selective verification
Compare only permitted V9 0x569280 function-range/native callsites with this older source, review existing group/AI REF and source-ID corrections; obtain unmodified original game group membership transition Golden before proposing morale or formula.
- Original game Golden PASS0, strict MATCH0, new READY0; external G4 settlement/side-effect contract not proven. No banned ranges, prior refused native evidence/operations, raw game bytes, original DAT, saves, database, absolute local PC paths or other-owner dirty files are reproduced or retried. Curator selects independently corroborated evidence only; never whole-merge diverged owner PR.
