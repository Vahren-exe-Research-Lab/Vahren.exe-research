#!/usr/bin/env python3
"""Guarded Git synchronization of curated Hakushin research knowledge only.
Commands: audit, status, start TASK, checkpoint TASK, publish.
Never uses reset, rebase, stash, amend, force, or writes to original game files.
"""
import argparse
import contextlib
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

import reference

KB = Path(__file__).resolve().parent.parent
REPO = "ButaMonky/Hakushin067-Research-Knowledge"
MAIN = "develop"
MANIFEST = "SOURCE_MANIFEST.tsv"
FILES = (
    ".gitignore", ".gitattributes", "README.md", "kb.py",
    "symbols.tsv", "structs.tsv", "REF_DAT_BEHAVIOR.md", "REF_UI_SYSTEM.md",
    "SYNC_PROTOCOL.md", "SYNC_STATUS.md", "KB_SYNC_BLOCKED_20261029.md",
    "KNOWLEDGE_CURATION_PROTOCOL.md", "RESEARCH_INTAKE_PROTOCOL_20261101.md", "REF_UNIT_EXP_SUMMON.md", "REF_SKILL_POST_ACTION.md", "REF_BATTLE_AI_MORALE.md", "REF_AUDIO_VORBIS.md", "REF_BATTLE_TAKEOVER.md",
    "REF_SAVE_PERSISTENCE.md", "REF_SAVE_FORMAT.md", "REF_RANDOM_EVENTS.md", "REF_RTS_SCENARIO.md",
    "REF_SCRIPT_VM_CONTEXT.md", "REF_SCENARIO_COMPAT.md", "REF_STRATEGY_ECONOMY.md",
    "RESEARCH_SOURCE_CATALOG.tsv", "RESEARCH_DUPLICATE_CANDIDATES.tsv", "RESEARCH_DUPLICATE_TRIAGE.md",
    "RESEARCH_INTEGRATION_SNAPSHOT.md",
    "GHIDRA_V9_COVERAGE_REPORT.md", "GHIDRA_V9_AUDIT_RUN_20261031.md",
    "GHIDRA_V9_GAPS_TOP500.tsv",
    "GHIDRA_V9_UNSTUDIED_CALLED_TOP200.tsv", "GHIDRA_V9_B_REVIEW_TOP150.tsv",
    "CANDIDATE_RANKING_20261030.md", "DB_OPTIMIZATION_REPORT_20261030.md",
    "GHIDRA_X32DBG_VERIFICATION_20261030.md",
    "KB_WORKFLOW_125_REPORT_20261029.md", "SYMBOLS_EXPANSION_REPORT_20261029.md",
    "tools/ApplyKnowledge.java", "tools/VerifyKnowledge.java", "tools/build_catalog.bat",
    "tools/build_catalog.py", "tools/build_kb.py", "tools/audit_research.py", "tools/test_research_inventory.py",
    "tools/v9_coverage.py", "tools/test_v9_coverage.py", "tools/check_symbols.py",
    "tools/research_index.py", "tools/optimize_research_db.py",
    "tools/rank_candidates.py", "tools/test_rank_candidates.py",
    "tools/verify_debugger_exports.py", "tools/test_debugger_exports.py",
    "tools/export_x32dbg_database.py", "tools/test_x32dbg_database.py",
    "tools/test_kb_workflow.py",
    "tools/sync_knowledge.py", "tools/test_sync_knowledge.py",
    "research/DAT_UI_V4_RESEARCH_20261101.md",
    "research/rea/INDEX.md",
    "research/rea/REA_20261101_17H_P0_FTELL_FRAME_STATIC.md",
    "research/rea/REA_20261101_19H_P0_FTELL_SEH4_SCOPE_STATIC.md",
    "research/rea/REA_20261101_20H_P0_EH4_DISPATCH_PHASE_STATIC.md",
    "research/intake/README.md",
    "research/intake/B/B-20261013-1110-01.md", "research/intake/B/B-20261013-1134-01.md", "research/intake/B/B-20261013-1141-01.md", "research/intake/B/B-20261013-1146-01.md",
    "research/intake/B/B-20261023-20H-T013-TROOP-SORT-1BC-NATIVE-01.md",
    "research/intake/B/B-20261023-22H-T013-TROOP-FORM-MODE-SETTER-01.md",
    "research/intake/B/B-20261023-2317-T013-TROOP-MODE-SOURCE-CASE8-01.md",
    "research/intake/B/B-20261101-17H-T024-52AD00-MERGE-TIE-LOCAL-STABILITY-01.md",
    "research/intake/B/B-20261101-18H-T024-DUAL-REFERENCE-COORD-AND-PC-RESTORE-01.md",
    "research/intake/B/B-20261102-00H-T024-542280-NATIVE-ATAN2-SENTINEL-ERRATUM-01.md",
    "research/intake/B/B-20261102-01H-T024-5421D0-8DIST-SENTINEL-WRITER-01.md",
    "research/intake/B/B-OFFLINE-20261101-08H-T011-T013-GROUP1E-CALLSITES-AL-POSTCALL-01.md",
    "research/intake/B/B-OFFLINE-20261101-09H-T011-T013-GROUP34-WEIGHTED-SQRT-01.md",
    "research/intake/B/B-OFFLINE-20261101-16H-T011-T024-MIDPOINT-SAR-ROUNDING-OVERFLOW-01.md",
    "research/intake/REA/INDEX.md",
    "research/intake/REA/REA_20261031_22H_23H_20261101_00H_GROW_CALLBACKS.md",
    "research/intake/REA/REA_20261101_01H_02H_RESIDUE_TYPE2_AND_DIVISORS_STATIC.md",
    "research/intake/REA/REA_20261101_03H_05H_OFFLINE_RESIDUE_CORRECTED_STATIC.md",
    "research/intake/REA/REA_20261101_06H_08H_MODE_CACHE_RECOVERY_STATIC.md",
    "research/intake/REA/REA_20261101_21H_22H_FSOPEN_UNWIND_STATIC.md",
    "research/intake/REA/REA_20261101_23H_GETSTREAM_LOCK_OWNERSHIP_STATIC.md",
    "research/intake/REA/REA_20261102_00H_CRT_FILE2_LOCK_INDEX_POINTER_STATIC.md",
    "research/intake/REA/REA_20261102_01H_DUAL_ENTRY_ESI_ABI_STATIC.md",
    "research/intake/E/E-PC-20261101-GOLDEN-G012-AND-KB-BACKLOG.md",
    "research/intake/B/B-20261101-23H-T024-542280-OPTIONAL-DOUBLE-FALLBACK-01.md",
    "research/intake/B/B-OFFLINE-20261028-21H-T028-WANDER-MERCENARY-DUAL-RESULT-SINK-01.md",
    "research/intake/B/B-OFFLINE-20261028-22H-T028-ALTERNATE-RESULT-VECTOR-PAIR-01.md",
    "research/intake/B/B-OFFLINE-20261101-13H-T011-T024-DISTANCE-SORT-MODE-GATE-01.md",
    "research/intake/B/B-OFFLINE-20261101-14H-T011-T024-DISTANCE-COMPARE-BOUNDARY-01.md",
    "research/intake/B/B-OFFLINE-20261101-15H-T011-T024-NAN-COMPARATOR-TRANSITIVITY-01.md",
    "research/intake/B/B_T028_20261028_21H22H_BACKFILL_MANIFEST.tsv",
    "research/intake/B/T011_T024_DUAL_LIST_MODE3_VECTOR_NATIVE_20261101_12H.md",
    "research/intake/B/T011_T024_GROUP34_DUAL_BUCKET_ELIGIBILITY_NATIVE_20261101_11H.md",
    "research/intake/B/T011_T024_GROUP34_PROXIMITY_RATIO_100TICK_NATIVE_20261101_10H.md",
    "research/intake/B/T013_T024_528E86_GROUP1C_GATE_DISPATCH_NATIVE_20261101_20H.md",
    "research/intake/B/T013_T024_KB_CANDIDATE_528E86_GATE_20261101_20H.tsv",
    "research/intake/B/T013_T024_KB_CANDIDATE_MODE0_DISPATCH_GATES_20261101_21H.tsv",
    "research/intake/B/T013_T024_MODE0_DISPATCH_UPSTREAM_GATES_NATIVE_20261101_21H.md",
    "research/intake/B/T024_DUAL_CALLER_FACTOR_PROVENANCE_STATIC_20261101_22H.md",
    "research/intake/B/T024_GROUP_REF_FTOL_YFLIP_NATIVE_20261101_19H.md",
    "research/intake/B/T024_KB_CANDIDATE_REF_FTOL_YFLIP_20261101_19H.tsv",
    "research/intake/B/T024_KB_CURATION_SOURCE_MAP_20261101_19H.tsv",
    "research/intake/E/E-20261031-06H-TRAINING-COUNT-CROSSWALK.md",
    "research/intake/E/E-20261031-07H-LEADER-CACHE-CORRECTION.md",
    "research/intake/E/E-20261031-08H-CACHE-DUPLICATE-CLEANUP.md",
    "research/intake/E/E-20261101-00H-COORD-RECT-RAW-ONLY.md",
    "research/intake/E/E-20261101-01H-VIEWFLAG-WRITER-CONSUMER.md",
    "research/intake/E/E-20261101-02H-OFF-EXACT-VSLOT-NEGATIVES.md",
    "research/intake/E/E-20261101-2249-T020-INTAKE-MANIFEST.md",
    "research/intake/E/E-AUDIT-20261031-09H-T020-T011-BULK-ERASE-BOUNDARY-01.md",
    "research/intake/E/E-AUDIT-20261031-10H-T020-T011-PARTIAL-ERASE-GUARD-01.md",
    "research/intake/E/E-AUDIT-20261031-11H-T020-T011-SUCCESSOR-BEFORE-ERASE-01.md",
    "research/intake/E/E-AUDIT-20261031-12H-T020-T013-SIGNED-DUAL-FIELD-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-13H-T020-T013-FIXED-ANCHOR-CORRECTION-01.md",
    "research/intake/E/E-AUDIT-20261031-14H-T020-T013-POSTRANK-UNIT8-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-15H-T020-T013-KIND8-PREQUEUE-RNG-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-16H-T020-T013-BUCKET-MERGE-SIGNED-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-17H-T020-T013-DRAIN-RESTORE-CAP-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-18H-T020-T013-RNG-CONTEXT-NEGATIVE-INFERENCE-01.md",
    "research/intake/E/E-AUDIT-20261031-19H-T020-T013-A14-DRAW-BOUNDARY-01.md",
    "research/intake/E/E-AUDIT-20261031-20H-T020-T013-SCRIPT-LIST-COUNTER-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-21H-T020-T013-HEAD-SENTINEL-COORD-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-22H-T020-T013-ALT-LIST-RESET-ORDER-GATE-01.md",
    "research/intake/E/E-AUDIT-20261031-23H-T020-T013-RECT-INSET-WINAPI-01.md",
    "research/intake/E/E-INTAKE-MANIFEST-20261101-2352-T020-09H16H.md",
    "research/intake/E/E-INTAKE-MANIFEST-20261102-0049-T020-17H23H.md",
    "research/intake/E/E-LEGACY-20261028-29-SOURCE-CROSSWALK-PART1-20261102.md",
    "research/intake/E/E-OFFLINE-20261101-0351-T020-T013-SCAN-RECT-VCALL-GATE-01.md",
    "research/intake/E/E-OFFLINE-20261101-0453-T020-T013-THREE-CALLER-RETURN-USE-01.md",
    "research/intake/E/E-OFFLINE-20261101-0549-T020-DUAL-CALLER-LATCH.md",
    "research/intake/E/E-OFFLINE-20261101-0644-T020-T013-CROSS-SCOPE-INTEGRITY-01.md",
    "research/intake/E/E-OFFLINE-20261101-0745-T018-T020-POINTER-IDENTITY-NORMALIZATION-01.md",
    "research/intake/E/E-OFFLINE-20261101-08H-T018-T020-CALLER-TEMPORAL-IDENTITY-01.md",
    "research/intake/E/E-OFFLINE-20261101-09H-T018-T020-G2-BIJECTION-ORDER-01.md",
    "research/intake/E/E-OFFLINE-20261101-10H-G2-DEFINITION-RUNTIME.md",
    "research/intake/E/E-OFFLINE-20261101-11H-T018-T020-G012-ARTIFACT-ATOM-01.md",
    "research/intake/E/E-OFFLINE-20261101-12H-T018-T020-CROSS-RUN-ALIAS-ADMISSION-01.md",
    "research/intake/E/E-OFFLINE-20261101-13H-PARENT-SYMLINK-GATE.md",
    "research/intake/E/E-OFFLINE-20261101-14H-PINNED-HANDLE-PROVENANCE.md",
    "research/intake/E/E-OFFLINE-20261101-15H-SIX-GATE-COVERAGE.md",
    "research/intake/E/E-OFFLINE-20261101-16H-CNB02-SOURCE-ADMISSION.md",
    "research/intake/E/E-OFFLINE-20261101-INTAKE-BATCH-MANIFEST.md",
    "research/intake/E/E-CNB02-GOLDEN-EVIDENCE-ACCEPTANCE-PLAYBOOK-20261102.md",
    "research/intake/E/E-LEGACY-20261020-31-CROSSWALK-BATCH01-20261102.md",
    "research/intake/E/E-LEGACY-20261020-31-CROSSWALK-BATCH02-20261102.md",
    "research/intake/E/E-LEGACY-20261020-31-CROSSWALK-BATCH03-20261102.md",
    "research/intake/E/E-LEGACY-20261020-31-CROSSWALK-BATCH04-20261102.md",
    "research/intake/E/E-LEGACY-20261020-31-CROSSWALK-BATCH05-20261102.md",
    "research/intake/E/E-LEGACY-20261020-31-CROSSWALK-BATCH06-20261102.md",
    "research/intake/E/E-LEGACY-20261020-31-CROSSWALK-BATCH07-20261102.md",
    "research/intake/E/E-LEGACY-20261028-29-SOURCE-CROSSWALK-PART2-20261102.md",
    "research/intake/E/E-PR17-CITATION-AND-CURATOR-RECONCILIATION-20261102.md",
    "research/intake/E/E-SOURCE-DETAIL-DAT-DRIFT-20261024-22H.md",
    "research/intake/E/E-SOURCE-DETAIL-G1-CLICK-SAVE-ORDER-20261025-15H.md",
    "research/intake/E/E-SOURCE-DETAIL-G2-PLACEHOLDER-IDENTITY-20261026-13H.md",
    "research/intake/E/E-SOURCE-RECEIPT-INDEX-193-20261102.tsv",
    "research/intake/E/E-T020-REPRO-ASSET-RECEIPTS-20261102.tsv",
    "research/intake/E/E-VA-MENTION-INDEX-20261102.tsv",
    "research/intake/E/INDEX.md",
    "research/intake/E/repro/t020_cnb02_g1_phase_contract_matrix_20261025_16H.py",
    "research/intake/E/repro/t020_cnb02_g2_roster_shape_diagnostic_20261026_08H.py",
    "research/intake/E/repro/t020_cnb02_receipt_provenance_gate_20261021_2345.py",
    "research/intake/REA/REA_20261101_09H_11H_CACHE_SEEK_RECOVERY_STATIC.md",
    "research/save_analysis_20261101/pkg/hakushin_compat/__init__.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/diplomacy_native_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/legacy_rng.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/native_stream_strings.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/normal_save_body_and_tail.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/normal_save_complete_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/power_native_full_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/power_runtime_writer_tail.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/real_save_frontmatter.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/save_envelope.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/spot_native_full_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/spot_runtime_writer_fragment.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/unit_native_full_wire.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/unit_native_wire_prefix.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/unit_runtime_prefix.py",
    "research/save_analysis_20261101/pkg/hakushin_compat/world_graph_native_wire.py",
    "research/save_analysis_20261101/tools/run_body_tail.py",
    "research/save_analysis_20261101/tools/tail_segments.py",
    "research/save_analysis_20261101/tools/tail_generations.py",
    "research/save_analysis_20261101/tools/tail_late_generations.py",
    "research/save_analysis_20261101/tools/field_stats.py",
    "research/save_analysis_20261101/tools/relation_checks.py",
    "research/save_analysis_20261101/tools/findings_vs_save.py",
    "research/save_analysis_20261101/tools/verify_ref.py",
    "research/save_analysis_20261101/tools/asmgrep.py",
    "research/save_analysis_20261101/tools/pseudo_grep.py",
    "research/save_analysis_20261101/tools/findings_offsets.py",
    "research/save_analysis_20261101/tools/kb_lookup.py",
    "research/save_analysis_20261101/tools/list_deps.py",
    "research/save_analysis_20261101/README.md",
    "sources/legacy_comments_20261011.tsv",
    "sources/legacy_symbols_20261011.tsv",
)
# Reviewed portable reference and recovered research paths.
FILES += (
    'docs/superpowers/plans/2026-11-05-reference.md',
    'reference/README.md',
    'reference/UPDATING.md',
    'reference/relations.jsonl',
    'reference/structs/Ctx.md',
    'reference/structs/FrameWnd.md',
    'reference/structs/GameManager.md',
    'reference/structs/GameTask.md',
    'reference/structs/Player.md',
    'reference/structs/Power.md',
    'reference/structs/Spot.md',
    'reference/structs/StatusWnd.md',
    'reference/structs/TurnState.md',
    'reference/structs/UnitDef.md',
    'reference/symbols/00402C40.md',
    'reference/symbols/00406E20.md',
    'reference/symbols/0040D0A0.md',
    'reference/symbols/0040E220.md',
    'reference/symbols/0040E2F0.md',
    'reference/symbols/0040ED80.md',
    'reference/symbols/0040F000.md',
    'reference/symbols/0040F320.md',
    'reference/symbols/00415CF0.md',
    'reference/symbols/00416220.md',
    'reference/symbols/00416870.md',
    'reference/symbols/004189B0.md',
    'reference/symbols/00419938.md',
    'reference/symbols/0041EBE0.md',
    'reference/symbols/0041EF50.md',
    'reference/symbols/00420900.md',
    'reference/symbols/00423D70.md',
    'reference/symbols/004243C0.md',
    'reference/symbols/00424C80.md',
    'reference/symbols/00427040.md',
    'reference/symbols/004270F0.md',
    'reference/symbols/00428010.md',
    'reference/symbols/00428710.md',
    'reference/symbols/00428F84.md',
    'reference/symbols/00429C60.md',
    'reference/symbols/0042F860.md',
    'reference/symbols/00431BE0.md',
    'reference/symbols/00431FB0.md',
    'reference/symbols/00432EE0.md',
    'reference/symbols/004335E0.md',
    'reference/symbols/00433754.md',
    'reference/symbols/004338D0.md',
    'reference/symbols/00433B62.md',
    'reference/symbols/00433E80.md',
    'reference/symbols/00435550.md',
    'reference/symbols/00435C10.md',
    'reference/symbols/00436080.md',
    'reference/symbols/004365F0.md',
    'reference/symbols/00436870.md',
    'reference/symbols/0043B5A0.md',
    'reference/symbols/00448E90.md',
    'reference/symbols/00449500.md',
    'reference/symbols/0044CF80.md',
    'reference/symbols/0044DCE0.md',
    'reference/symbols/0044E3F0.md',
    'reference/symbols/0044F470.md',
    'reference/symbols/004518FA.md',
    'reference/symbols/0045190B.md',
    'reference/symbols/00451915.md',
    'reference/symbols/00452D90.md',
    'reference/symbols/00455520.md',
    'reference/symbols/00455CF0.md',
    'reference/symbols/00455D90.md',
    'reference/symbols/004591F0.md',
    'reference/symbols/0045B850.md',
    'reference/symbols/0045BE10.md',
    'reference/symbols/0045E1E0.md',
    'reference/symbols/0045E5F0.md',
    'reference/symbols/0045E7F0.md',
    'reference/symbols/0045EAC0.md',
    'reference/symbols/0045F960.md',
    'reference/symbols/0045FD3E.md',
    'reference/symbols/0045FF4B.md',
    'reference/symbols/00460000.md',
    'reference/symbols/0046065C.md',
    'reference/symbols/00460E90.md',
    'reference/symbols/00460F10.md',
    'reference/symbols/00461DA0.md',
    'reference/symbols/00463610.md',
    'reference/symbols/004637A0.md',
    'reference/symbols/00463CA0.md',
    'reference/symbols/00464290.md',
    'reference/symbols/0046453F.md',
    'reference/symbols/004647D0.md',
    'reference/symbols/00466BA0.md',
    'reference/symbols/00466F60.md',
    'reference/symbols/00467DE0.md',
    'reference/symbols/00467F40.md',
    'reference/symbols/00470550.md',
    'reference/symbols/004705F0.md',
    'reference/symbols/00470700.md',
    'reference/symbols/00470830.md',
    'reference/symbols/004708A0.md',
    'reference/symbols/004708D0.md',
    'reference/symbols/004716C0.md',
    'reference/symbols/00471AF0.md',
    'reference/symbols/00471D20.md',
    'reference/symbols/00471E80.md',
    'reference/symbols/00474F10.md',
    'reference/symbols/00475C60.md',
    'reference/symbols/00476D60.md',
    'reference/symbols/00479740.md',
    'reference/symbols/00479A30.md',
    'reference/symbols/0047A1A0.md',
    'reference/symbols/0047BB50.md',
    'reference/symbols/0047C280.md',
    'reference/symbols/0047D770.md',
    'reference/symbols/0047E3A0.md',
    'reference/symbols/00481260.md',
    'reference/symbols/0048ABF0.md',
    'reference/symbols/0048AD30.md',
    'reference/symbols/0048B4A0.md',
    'reference/symbols/0048BC70.md',
    'reference/symbols/0048BF60.md',
    'reference/symbols/0048C880.md',
    'reference/symbols/0048D6A0.md',
    'reference/symbols/0048EEE0.md',
    'reference/symbols/0048F080.md',
    'reference/symbols/0048F720.md',
    'reference/symbols/0048F9E0.md',
    'reference/symbols/004922A0.md',
    'reference/symbols/00492710.md',
    'reference/symbols/00492890.md',
    'reference/symbols/00492D80.md',
    'reference/symbols/004930C0.md',
    'reference/symbols/0049356A.md',
    'reference/symbols/00493630.md',
    'reference/symbols/0049CD60.md',
    'reference/symbols/0049D1B0.md',
    'reference/symbols/0049E560.md',
    'reference/symbols/0049E780.md',
    'reference/symbols/0049E8B0.md',
    'reference/symbols/0049ED90.md',
    'reference/symbols/0049F7D0.md',
    'reference/symbols/004A1250.md',
    'reference/symbols/004A17C8.md',
    'reference/symbols/004A17D8.md',
    'reference/symbols/004A18B1.md',
    'reference/symbols/004A2793.md',
    'reference/symbols/004A2ED6.md',
    'reference/symbols/004A304A.md',
    'reference/symbols/004A5F53.md',
    'reference/symbols/004A60D1.md',
    'reference/symbols/004A6E40.md',
    'reference/symbols/004A6FE1.md',
    'reference/symbols/004A71AA.md',
    'reference/symbols/004A7A90.md',
    'reference/symbols/004AE0F0.md',
    'reference/symbols/004AEDDA.md',
    'reference/symbols/004B044F.md',
    'reference/symbols/004B47FC.md',
    'reference/symbols/004B9930.md',
    'reference/symbols/004B9AA0.md',
    'reference/symbols/004B9AD0.md',
    'reference/symbols/004B9B73.md',
    'reference/symbols/004B9E50.md',
    'reference/symbols/004BBAE0.md',
    'reference/symbols/004BCF20.md',
    'reference/symbols/004BCF70.md',
    'reference/symbols/004BD170.md',
    'reference/symbols/004BD2A0.md',
    'reference/symbols/004BDE40.md',
    'reference/symbols/004BE220.md',
    'reference/symbols/004BE340.md',
    'reference/symbols/004BE388.md',
    'reference/symbols/004BE3E0.md',
    'reference/symbols/004BE480.md',
    'reference/symbols/004BE820.md',
    'reference/symbols/004BF2B0.md',
    'reference/symbols/004BF410.md',
    'reference/symbols/004BF520.md',
    'reference/symbols/004BF570.md',
    'reference/symbols/004BF630.md',
    'reference/symbols/004BF6A0.md',
    'reference/symbols/004BF720.md',
    'reference/symbols/004BF780.md',
    'reference/symbols/004C1200.md',
    'reference/symbols/004C1FC0.md',
    'reference/symbols/004C21F0.md',
    'reference/symbols/004C2240.md',
    'reference/symbols/004C24B0.md',
    'reference/symbols/004C5800.md',
    'reference/symbols/004C7040.md',
    'reference/symbols/004DEC70.md',
    'reference/symbols/004DEF40.md',
    'reference/symbols/004DFBB0.md',
    'reference/symbols/004E4C70.md',
    'reference/symbols/004E4F60.md',
    'reference/symbols/004E53B0.md',
    'reference/symbols/004E70E0.md',
    'reference/symbols/004E7ED0.md',
    'reference/symbols/004EC1E0.md',
    'reference/symbols/004ED030.md',
    'reference/symbols/004EE0C0.md',
    'reference/symbols/004EE110.md',
    'reference/symbols/004EE170.md',
    'reference/symbols/004EE1B0.md',
    'reference/symbols/004F93A0.md',
    'reference/symbols/005001B0.md',
    'reference/symbols/005023E0.md',
    'reference/symbols/00502DD0.md',
    'reference/symbols/005050EE.md',
    'reference/symbols/0050B220.md',
    'reference/symbols/00514AA0.md',
    'reference/symbols/00514C80.md',
    'reference/symbols/00514D60.md',
    'reference/symbols/00514F10.md',
    'reference/symbols/00515060.md',
    'reference/symbols/00515150.md',
    'reference/symbols/005151D0.md',
    'reference/symbols/005154F0.md',
    'reference/symbols/005158A0.md',
    'reference/symbols/00521560.md',
    'reference/symbols/00521A00.md',
    'reference/symbols/00521AF0.md',
    'reference/symbols/00526030.md',
    'reference/symbols/00526510.md',
    'reference/symbols/00526A40.md',
    'reference/symbols/00526E50.md',
    'reference/symbols/005271A0.md',
    'reference/symbols/00527710.md',
    'reference/symbols/00527EA0.md',
    'reference/symbols/00527ED0.md',
    'reference/symbols/00527F60.md',
    'reference/symbols/00528320.md',
    'reference/symbols/00529DC0.md',
    'reference/symbols/005421D0.md',
    'reference/symbols/00542280.md',
    'reference/symbols/00543E00.md',
    'reference/symbols/00544290.md',
    'reference/symbols/005445E0.md',
    'reference/symbols/005450C0.md',
    'reference/symbols/005454D0.md',
    'reference/symbols/00545740.md',
    'reference/symbols/00545CC0.md',
    'reference/symbols/00545EC5.md',
    'reference/symbols/00546F70.md',
    'reference/symbols/005470FF.md',
    'reference/symbols/00547490.md',
    'reference/symbols/005479F0.md',
    'reference/symbols/00547AF0.md',
    'reference/symbols/00547DB0.md',
    'reference/symbols/0054A170.md',
    'reference/symbols/0054A1C0.md',
    'reference/symbols/0054A660.md',
    'reference/symbols/0054A7B0.md',
    'reference/symbols/0054ADA0.md',
    'reference/symbols/0054B280.md',
    'reference/symbols/0054E0B0.md',
    'reference/symbols/0054E420.md',
    'reference/symbols/0054E7B0.md',
    'reference/symbols/0054ED95.md',
    'reference/symbols/0054F074.md',
    'reference/symbols/0054F245.md',
    'reference/symbols/005501A0.md',
    'reference/symbols/00550D80.md',
    'reference/symbols/00550E70.md',
    'reference/symbols/005510E5.md',
    'reference/symbols/00551167.md',
    'reference/symbols/00551490.md',
    'reference/symbols/00551574.md',
    'reference/symbols/00551C6A.md',
    'reference/symbols/00551E50.md',
    'reference/symbols/00551FB2.md',
    'reference/symbols/00552EF0.md',
    'reference/symbols/00553390.md',
    'reference/symbols/005537BF.md',
    'reference/symbols/005559B0.md',
    'reference/symbols/00555AD0.md',
    'reference/symbols/00555D69.md',
    'reference/symbols/00555E15.md',
    'reference/symbols/00555F19.md',
    'reference/symbols/0055A000.md',
    'reference/symbols/0055B010.md',
    'reference/symbols/0055B590.md',
    'reference/symbols/0055B5B0.md',
    'reference/symbols/0055BAB0.md',
    'reference/symbols/0055BC60.md',
    'reference/symbols/0055D712.md',
    'reference/symbols/0055D7FF.md',
    'reference/symbols/0055D8F6.md',
    'reference/symbols/0055D93A.md',
    'reference/symbols/0055D95F.md',
    'reference/symbols/0055D99C.md',
    'reference/symbols/0055D9DD.md',
    'reference/symbols/0055D9FC.md',
    'reference/symbols/00560650.md',
    'reference/symbols/005606A2.md',
    'reference/symbols/00560CA0.md',
    'reference/symbols/00561120.md',
    'reference/symbols/00562140.md',
    'reference/symbols/00565700.md',
    'reference/symbols/00565730.md',
    'reference/symbols/00565750.md',
    'reference/symbols/00567EC0.md',
    'reference/symbols/005681C0.md',
    'reference/symbols/00569530.md',
    'reference/symbols/0056F6F0.md',
    'reference/symbols/0056F720.md',
    'reference/symbols/0056F880.md',
    'reference/symbols/00570C90.md',
    'reference/symbols/00571A40.md',
    'reference/symbols/00571B70.md',
    'reference/symbols/00573BD0.md',
    'reference/symbols/00574D70.md',
    'reference/symbols/00574E30.md',
    'reference/symbols/00575110.md',
    'reference/symbols/00575A60.md',
    'reference/symbols/005769B0.md',
    'reference/symbols/00576F10.md',
    'reference/symbols/00577100.md',
    'reference/symbols/00577260.md',
    'reference/symbols/00577310.md',
    'reference/symbols/00577405.md',
    'reference/symbols/005774A0.md',
    'reference/symbols/00577600.md',
    'reference/symbols/00578B70.md',
    'reference/symbols/00579940.md',
    'reference/symbols/00579EB0.md',
    'reference/symbols/0057A6E0.md',
    'reference/symbols/0057A764.md',
    'reference/symbols/0057A7D0.md',
    'reference/symbols/0057A830.md',
    'reference/symbols/0057AA00.md',
    'reference/symbols/0057B870.md',
    'reference/symbols/0057BE30.md',
    'reference/symbols/0057C9B0.md',
    'reference/symbols/0057CFA0.md',
    'reference/symbols/0057CFD0.md',
    'reference/symbols/0057D1D0.md',
    'reference/symbols/0057D8B0.md',
    'reference/symbols/0057DD10.md',
    'reference/symbols/0057DF90.md',
    'reference/symbols/0057E1D0.md',
    'reference/symbols/0057E4E0.md',
    'reference/symbols/0057EB40.md',
    'reference/symbols/0057F570.md',
    'reference/symbols/0057FC90.md',
    'reference/symbols/0057FFD0.md',
    'reference/symbols/00580280.md',
    'reference/symbols/00582D90.md',
    'reference/symbols/00583A80.md',
    'reference/symbols/00583CF0.md',
    'reference/symbols/00583DC0.md',
    'reference/symbols/005846A0.md',
    'reference/symbols/00584830.md',
    'reference/symbols/00584970.md',
    'reference/symbols/00585AD0.md',
    'reference/symbols/00586320.md',
    'reference/symbols/00587CC0.md',
    'reference/symbols/00588470.md',
    'reference/symbols/0058A400.md',
    'reference/symbols/0058A540.md',
    'reference/symbols/0058A650.md',
    'reference/symbols/0058AFA0.md',
    'reference/symbols/0058B7F0.md',
    'reference/symbols/0058C0E0.md',
    'reference/symbols/0058DA40.md',
    'reference/symbols/0058E870.md',
    'reference/symbols/0058EFD0.md',
    'reference/symbols/0058F7E0.md',
    'reference/symbols/00593890.md',
    'reference/symbols/00595320.md',
    'reference/symbols/005964C0.md',
    'reference/symbols/00596AA0.md',
    'reference/symbols/005972E0.md',
    'reference/symbols/005973AF.md',
    'reference/symbols/00597412.md',
    'reference/symbols/00597960.md',
    'reference/symbols/00597A50.md',
    'reference/symbols/00597B00.md',
    'reference/symbols/00598450.md',
    'reference/symbols/005985C0.md',
    'reference/symbols/00598980.md',
    'reference/symbols/00598CE0.md',
    'reference/symbols/0059C3B5.md',
    'reference/symbols/0059C418.md',
    'reference/symbols/005A3DF0.md',
    'reference/symbols/005A3EA0.md',
    'reference/symbols/005A4100.md',
    'reference/symbols/005A8740.md',
    'reference/symbols/005A89A0.md',
    'reference/symbols/005A9CC0.md',
    'reference/symbols/005AA130.md',
    'reference/symbols/005AA6E0.md',
    'reference/symbols/005AAEC0.md',
    'reference/symbols/005B0400.md',
    'reference/symbols/005B0600.md',
    'reference/symbols/005B47B0.md',
    'reference/symbols/005B5010.md',
    'reference/symbols/005B6BBB.md',
    'reference/symbols/005B6E99.md',
    'reference/symbols/005B6EAB.md',
    'reference/symbols/005B797C.md',
    'reference/symbols/005B79D7.md',
    'reference/symbols/005BB6E0.md',
    'reference/symbols/005CF970.md',
    'reference/symbols/005D0B8A.md',
    'reference/symbols/005D16C0.md',
    'reference/symbols/005D1B80.md',
    'reference/symbols/005D3D00.md',
    'reference/symbols/005D3DA0.md',
    'reference/symbols/005D3F60.md',
    'reference/symbols/005D4030.md',
    'reference/symbols/005D4160.md',
    'reference/symbols/005D4420.md',
    'reference/symbols/005D44C0.md',
    'reference/symbols/005D4900.md',
    'reference/symbols/005D4980.md',
    'reference/symbols/005D49F0.md',
    'reference/symbols/005D4A60.md',
    'reference/symbols/005D4AE0.md',
    'reference/symbols/005D4D20.md',
    'reference/symbols/005D5BD0.md',
    'reference/symbols/005D9E70.md',
    'reference/symbols/005D9F40.md',
    'reference/symbols/005DA070.md',
    'reference/symbols/005DA550.md',
    'reference/symbols/005DA930.md',
    'reference/symbols/005DA9F8.md',
    'reference/symbols/005E06C0.md',
    'reference/symbols/005E3B70.md',
    'reference/symbols/005E6C70.md',
    'reference/symbols/005E6CA0.md',
    'reference/symbols/005E6CD0.md',
    'reference/symbols/005E6E10.md',
    'reference/symbols/005E6F10.md',
    'reference/symbols/00626D5C.md',
    'reference/symbols/006385BC.md',
    'reference/symbols/00639C5C.md',
    'reference/symbols/00639CD4.md',
    'reference/symbols/0063A4BC.md',
    'reference/symbols/0063A8E4.md',
    'reference/symbols/0063A9E4.md',
    'reference/symbols/0063B058.md',
    'reference/symbols/0063B060.md',
    'reference/symbols/0063B070.md',
    'reference/symbols/0063B080.md',
    'reference/symbols/0063B100.md',
    'reference/symbols/0065BCAC.md',
    'reference/symbols/0065BCFC.md',
    'reference/symbols/0065BD4C.md',
    'reference/symbols/0065BD58.md',
    'reference/symbols/0065BD5C.md',
    'reference/symbols/0065BD9F.md',
    'reference/symbols/0065BEA8.md',
    'reference/symbols/0065BED8.md',
    'reference/symbols/0065BEE4.md',
    'reference/symbols/0065BEEC.md',
    'reference/symbols/0065BEF0.md',
    'reference/symbols/0065BF18.md',
    'reference/symbols/0065CD28.md',
    'reference/symbols/0065EB64.md',
    'reference/symbols/0067B938.md',
    'reference/symbols/0067B93C.md',
    'reference/symbols/0067E978.md',
    'reference/symbols/0067EB30.md',
    'reference/symbols/0068B568.md',
    'reference/symbols/0068B578.md',
    'reference/symbols/0068B588.md',
    'reference/symbols/008795F0.md',
    'reference/symbols/00879610.md',
    'reference/symbols/00879628.md',
    'reference/symbols/008797FC.md',
    'reference/symbols/0087980C.md',
    'reference/symbols/0087981D.md',
    'reference/symbols/00879820.md',
    'reference/symbols/00879821.md',
    'reference/symbols/00879822.md',
    'reference/symbols/00879823.md',
    'reference/symbols/0087983C.md',
    'reference/symbols/0087984F.md',
    'reference/symbols/00879E48.md',
    'reference/symbols/00879E68.md',
    'reference/symbols/0087A1B8.md',
    'reference/symbols/008BA538.md',
    'reference/symbols/008BA5BC.md',
    'reference/symbols/008BA5DC.md',
    'reference/symbols/008BB6D8.md',
    'reference/symbols/008BCD48.md',
    'reference/symbols/008BCDCC.md',
    'reference/symbols/008BCDE0.md',
    'reference/symbols/008BCF00.md',
    'reference/symbols/008BCF10.md',
    'reference/symbols/008BE040.md',
    'reference/symbols/008BE2F0.md',
    'reference/symbols/008BE388.md',
    'reference/symbols/008BE3A0.md',
    'reference/symbols/008BE7F4.md',
    'reference/symbols/00AAD434.md',
    'reference/symbols/00AC0914.md',
    'reference/symbols/00AC0918.md',
    'research/recovered/BATTLE_SCRIPT_IMPORT_ORDER_NATIVE_20261011.md',
    'research/recovered/DAT_UI_V4_STATUS_PANEL.md',
    'research/recovered/DEVLAB_MINIMAP_NATIVE_CONTRACT_20261011.md',
    'research/recovered/DEVLAB_NATIVE_PARENT_PRIORITY_RESEARCH_20261011.md',
    'research/recovered/DEVLAB_NATIVE_SAVE_COMPLETE_WIRE_20261011.md',
    'research/recovered/DEVLAB_NATIVE_SKILL_CAPABILITY_20261011.md',
    'research/recovered/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md',
    'research/recovered/DEVLAB_TERRAIN_MOVETYPE_20261011.md',
    'research/recovered/README.md',
    'research/recovered/RECOVERY_LEDGER.tsv',
    'tools/reference.py',
    'tools/test_reference.py',
)
# Reviewed second recovery batch.
FILES += (
    'research/recovered/COVERAGE.md',
    'research/recovered/COVERAGE.tsv',
    'research/recovered/dev_evidence/DEV_EVIDENCE_LEDGER.tsv',
    'research/recovered/dev_evidence/README.md',
    'research/recovered/dev_evidence/reports/MINIMAP_NATIVE_STATIC_AUDIT_20261011.json',
    'research/recovered/dev_evidence/reports/NATIVE_SKILL_CAPABILITY_SUBSET_20261011.json',
    'research/recovered/dev_evidence/src/hakushin_compat/native_minimap_static_subset.py',
    'research/recovered/dev_evidence/src/hakushin_compat/native_skill_capability_subset.py',
    'research/recovered/dev_evidence/tests/test_native_minimap_static_subset.py',
    'research/recovered/dev_evidence/tests/test_native_skill_capability_subset.py',
    'research/recovered/exp/EXP_CACHED_RECORD_LIFETIME_20261021.md',
    'research/recovered/exp/EXP_CACHE_STRING_KEY_RECORD_ABI_20261021.md',
    'research/recovered/exp/EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md',
    'research/recovered/exp/EXP_KIND4_DISPATCH_PRODUCERS_20261021.md',
    'research/recovered/exp/EXP_RECOVERY_LEDGER.tsv',
    'research/recovered/exp/EXP_SAVE_TREE_POINTER_VS_INLINE_20261021.md',
    'research/recovered/exp/EXP_SIMPLEBATTLE_LIFECYCLE_20261022.md',
    'research/recovered/exp/EXP_SUMMON_DESTRUCTOR_NORMAL_VTABLE_20261022.md',
    'research/recovered/exp/EXP_SUMMON_OWNER_RESEARCH.md',
    'research/recovered/exp/EXP_THREE_PRODUCER_CROSSJOIN_20261021.md',
    'research/recovered/exp/EXP_TYPED_OFFSET_CENSUS_20261022.md',
    'research/recovered/exp/README.md',
    'tools/recovery_coverage.py',
    'tools/test_recovery_coverage.py',
)
# Reviewed screened findings and citation registry.
FILES += (
    'reference/sources.json',
    'research/recovered/findings/PEER_SCRIPT01_FINDINGS_20261011.md',
    'research/recovered/findings/README.md',
    'research/recovered/findings/SCREENING.json',
)
# Reviewed scheduled result metadata and symbol source recovery.
FILES += (
    'reference/FIELD_MENTIONS.md',
    'research/recovered/rea_runs/ACQUISITION_COUNTS.json',
    'research/recovered/rea_runs/QUEUE_RECOVERY_LEDGER.tsv',
    'research/recovered/rea_runs/README.md',
    'research/recovered/rea_runs/SCHEDULE_RECOVERY_LEDGER.tsv',
    'research/recovered/rea_runs/logs/progress_sync_20261011T153958076Z.json',
    'research/recovered/rea_runs/runs/20261009T193808151Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T194358486Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T203528568Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T211647219Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T212627835Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T213635897Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T215200079Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T215905915Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T220712454Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T221558628Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T222501703Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T223622536Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T224617297Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261009T225741694Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261011T112315808Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261011T113414092Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261011T114202395Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261011T124000308Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261011T133432356Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261011T144115307Z/RUN_RESULT.json',
    'research/recovered/rea_runs/runs/20261011T153309850Z/RUN_RESULT.json',
    'research/recovered/rea_runs/snapshots/QUEUE_20261105_READBACK.json',
    'research/recovered/symbol_sources/README.md',
    'research/recovered/symbol_sources/SYMBOL_SOURCE_17H_REDACTION.tsv',
    'research/recovered/symbol_sources/SYMBOL_SOURCE_LEDGER.tsv',
    'research/recovered/symbol_sources/T011_TRAINING_CACHE_FULL_RANGE_ERASE_NATIVE_20261031_09H.md',
    'research/recovered/symbol_sources/T011_TRAINING_CACHE_INIT_ERASE_DUPLICATE_NATIVE_20261031_08H.md',
    'research/recovered/symbol_sources/T011_TRAINING_PARTIAL_ERASE_NATIVE_20261031_10H.md',
    'research/recovered/symbol_sources/T013_BUCKET_LIST_MERGE_COMPARATOR_NATIVE_20261031_16H.md',
    'research/recovered/symbol_sources/T013_CANDIDATE_A14_PER_NODE_RANDOM_SCORE_NATIVE_20261031_19H.md',
    'research/recovered/symbol_sources/T013_DUAL_SCORE_RANK_FIELD_NATIVE_20261031_12H.md',
    'research/recovered/symbol_sources/T013_DUAL_SCORE_SORT_ANCHOR_TIE_CORRECTION_NATIVE_20261031_13H.md',
    'research/recovered/symbol_sources/T013_FIRST_HEAD_SENTINEL_COORD_BRANCH_NATIVE_20261031_21H.md',
    'research/recovered/symbol_sources/T013_INPUT_DRAIN_RESTORE_LIST_CAP_NATIVE_20261031_17H.md',
    'research/recovered/symbol_sources/T013_KIND8_RANDOM_PAYLOAD_QUEUE_NATIVE_20261031_15H.md',
    'research/recovered/symbol_sources/T013_UNIT18654_LIST_WRITER_ERASE_NATIVE_20261031_20H.md',
)
# Reviewed B, DEV, A/C report batches and paginated memory index.
FILES += (
    'reference/fields/owner-B%E3%81%AE%E6%9D%A1%E4%BB%B6%E3%81%AFSkill-9a75118c880e-001.md',
    'reference/fields/owner-BattleUnit-00e02c9dd7e7-001.md',
    'reference/fields/owner-BattleWnd-f883f037623b-001.md',
    'reference/fields/owner-C4%E3%81%A7sentinel-8161154ab304-001.md',
    'reference/fields/owner-DAT_65E5E4-fe964e624efe-001.md',
    'reference/fields/owner-DemoPerson%E3%81%AEvtable-4ba98af8c016-001.md',
    'reference/fields/owner-Diplomacy-bd4076f29ec7-001.md',
    'reference/fields/owner-E-a9f51566bd67-001.md',
    'reference/fields/owner-FPU-7d204500cf94-001.md',
    'reference/fields/owner-G-333e0a1e2781-001.md',
    'reference/fields/owner-GM-b3910ba413cc-001.md',
    'reference/fields/owner-GameManager-3554a873139a-001.md',
    'reference/fields/owner-GameTask-4d74fe14ec73-001.md',
    'reference/fields/owner-HP%E7%9B%B8%E5%BD%93-5137fc343291-001.md',
    'reference/fields/owner-HP%E9%A0%85%E7%9B%AE%E3%81%AE%E4%B8%8A%E9%99%90%E3%83%9D%E3%82%A4%E3%83%B3%E3%82%BF%E3%81%AFtarget-d61af2ffe852-001.md',
    'reference/fields/owner-M-08f271887ce9-001.md',
    'reference/fields/owner-MP%E5%80%99%E8%A3%9C-a2c69b883de8-001.md',
    'reference/fields/owner-NULL-fb329000228c-001.md',
    'reference/fields/owner-P-5c62e091b8c0-001.md',
    'reference/fields/owner-Person-6007db63e18e-001.md',
    'reference/fields/owner-Player-64aee8c6cbd0-001.md',
    'reference/fields/owner-Power-848e96567d6b-001.md',
    'reference/fields/owner-R-8c2574892063-001.md',
    'reference/fields/owner-RAM%E4%B8%8A%E3%81%AF1byte%E3%81%AEUnit-70392055092e-001.md',
    'reference/fields/owner-Rush-34ebcd9fcba8-001.md',
    'reference/fields/owner-SimpleUnit-0f660d847a1f-001.md',
    'reference/fields/owner-Skill-6df1bb18a59a-001.md',
    'reference/fields/owner-Spot-74f8092562bd-001.md',
    'reference/fields/owner-SpotElm-809afba9601e-001.md',
    'reference/fields/owner-TempStatusWnd-bbd656040568-001.md',
    'reference/fields/owner-Troop-80e595625fa8-001.md',
    'reference/fields/owner-Unit%E3%81%AE%E7%AC%AC4vector%E5%BE%8C%E3%81%AB-8a7a0aa5a316-001.md',
    'reference/fields/owner-Unit%E3%83%99%E3%82%AF%E3%82%BF-f155ab21620e-001.md',
    'reference/fields/owner-Unit-4e545960f1bf-001.md',
    'reference/fields/owner-Unit-4e545960f1bf-002.md',
    'reference/fields/owner-UnitData-61b53927b138-001.md',
    'reference/fields/owner-UnitDef-c35784074dad-001.md',
    'reference/fields/owner-V9%E6%93%AC%E4%BC%BCC%E3%81%A7%E3%81%AFkind8%E3%81%ABUnit-f7c6b4e44a7b-001.md',
    'reference/fields/owner-VA0x577827%E3%81%A7Skill-7951c810b864-001.md',
    'reference/fields/owner-VA0x577830%E3%81%A7Skill-2b89f0071bcf-001.md',
    'reference/fields/owner-actor-50c9c4aeb40b-001.md',
    'reference/fields/owner-addBaseLevel-7fbd6b83b3c0-001.md',
    'reference/fields/owner-addCapa-0793e17722e1-001.md',
    'reference/fields/owner-addCastle-2f2f1ac26590-001.md',
    'reference/fields/owner-addGain-67403f04ca32-001.md',
    'reference/fields/owner-addTraining-678eacc4e541-001.md',
    'reference/fields/owner-addTrainingUp-2c6bd70165b3-001.md',
    'reference/fields/owner-anchorUnit-299ee081e3f0-001.md',
    'reference/fields/owner-app-a172cedcae47-001.md',
    'reference/fields/owner-base-cae662172fd4-001.md',
    'reference/fields/owner-bow-c177affdff64-001.md',
    'reference/fields/owner-byte-1c31626f568a-001.md',
    'reference/fields/owner-c-2e7d2c03a950-001.md',
    'reference/fields/owner-call0x577260%E3%81%ABEBX-4b32607f7d48-001.md',
    'reference/fields/owner-caller%E6%AC%A0%E8%90%BD%E3%81%AE%E5%90%8C%E7%A8%AE%E7%B4%A2%E5%BC%95%E8%B2%A0%E4%BE%8B%E3%82%84-d522ea8a569b-001.md',
    'reference/fields/owner-candidate-dda18a0e21ae-001.md',
    'reference/fields/owner-care-f9ed2b54fd72-001.md',
    'reference/fields/owner-child-ddc9e6691942-001.md',
    'reference/fields/owner-constructor%E3%81%AE0x5442E4%E3%81%AF-0f9941afbdb7-001.md',
    'reference/fields/owner-context-ea7792a26f40-001.md',
    'reference/fields/owner-count-6c35493a2b93-001.md',
    'reference/fields/owner-ctx-0230c6b1d833-001.md',
    'reference/fields/owner-def-cb8379ac2098-001.md',
    'reference/fields/owner-def-cb8379ac2098-002.md',
    'reference/fields/owner-defense%E5%81%B4%E3%81%AFUnit-3c65d4627e2a-001.md',
    'reference/fields/owner-dext-0a392f6bb969-001.md',
    'reference/fields/owner-effect-dcb576426a17-001.md',
    'reference/fields/owner-end%E3%81%AF-1d0aefecc4be-001.md',
    'reference/fields/owner-engine-ed9f6f250686-001.md',
    'reference/fields/owner-fields-bfe5d697162d-001.md',
    'reference/fields/owner-first-a7937b64b8ca-001.md',
    'reference/fields/owner-flags-2934fb49d6b3-001.md',
    'reference/fields/owner-global-8001c2743965-001.md',
    'reference/fields/owner-group-ad936fcbed63-001.md',
    'reference/fields/owner-head-9f2e6d33a371-001.md',
    'reference/fields/owner-heal-599f8341fe3e-001.md',
    'reference/fields/owner-hitcontext-b4ac51a365bf-001.md',
    'reference/fields/owner-hp-93969d193161-001.md',
    'reference/fields/owner-i-de7d1b721a1e-001.md',
    'reference/fields/owner-iVar3-04c71520f7b0-001.md',
    'reference/fields/owner-iVar4-ebdb35afe065-001.md',
    'reference/fields/owner-in_ECX-4f3e3c12e493-001.md',
    'reference/fields/owner-initializer0x455FFA%E3%81%8Cbyte-0968582b1458-001.md',
    'reference/fields/owner-int-6da88c34ba12-001.md',
    'reference/fields/owner-joi-8cc885468e04-001.md',
    'reference/fields/owner-joi2-e65b2bf22f65-001.md',
    'reference/fields/owner-linked-2272bea616a0-001.md',
    'reference/fields/owner-list-a330395cc0a5-001.md',
    'reference/fields/owner-local-25bf8e1a2393-001.md',
    'reference/fields/owner-m-62c66a7a5dd7-001.md',
    'reference/fields/owner-magic-3be7a505483c-001.md',
    'reference/fields/owner-manager-6ee4a469cd4e-001.md',
    'reference/fields/owner-master-fc613b4dfd67-001.md',
    'reference/fields/owner-member-e31ab643c44f-001.md',
    'reference/fields/owner-missile-3fa1d3c4460b-001.md',
    'reference/fields/owner-mode-e642b12901a6-001.md',
    'reference/fields/owner-mode1%E3%81%A7%E3%82%820x57D8B0%E5%85%A5%E5%8F%A3%E3%81%AEUnit-04410ded7a79-001.md',
    'reference/fields/owner-mode2%E6%AC%84-2924c7804c7b-001.md',
    'reference/fields/owner-mode6%E3%81%AFSkill-62aebe4a7864-001.md',
    'reference/fields/owner-move-683a62ce15fb-001.md',
    'reference/fields/owner-mprec-9aa10cb18ccb-001.md',
    'reference/fields/owner-node-545ea5384610-001.md',
    'reference/fields/owner-nt6%E3%81%AE%E5%AE%9F%E5%8A%B9Skill-f03f809860ea-001.md',
    'reference/fields/owner-obj-772a5fb04f9b-001.md',
    'reference/fields/owner-object-2958d416d08a-001.md',
    'reference/fields/owner-offset-c1d60fe5815f-001.md',
    'reference/fields/owner-out-762069bc07a6-001.md',
    'reference/fields/owner-owner-4c1029697ee3-001.md',
    'reference/fields/owner-p-148de9c5a7a4-001.md',
    'reference/fields/owner-pModel-286e71c7bf3e-001.md',
    'reference/fields/owner-param_2-5f059d7c5789-001.md',
    'reference/fields/owner-parent-e47125968b3b-001.md',
    'reference/fields/owner-power-07d715edb696-001.md',
    'reference/fields/owner-powerup-eb7cf991174b-001.md',
    'reference/fields/owner-ptd-d11a2775d60c-001.md',
    'reference/fields/owner-q-8e35c2cd3bf6-001.md',
    'reference/fields/owner-r-454349e422f0-001.md',
    'reference/fields/owner-reader%E3%81%A7%E3%81%AF-82389af89890-001.md',
    'reference/fields/owner-rec-cb41b38387d6-001.md',
    'reference/fields/owner-record-70ce871f8a3d-001.md',
    'reference/fields/owner-result%E3%81%AF-95196e66aaf5-001.md',
    'reference/fields/owner-s-043a718774c5-001.md',
    'reference/fields/owner-scene-4f48f7207ceb-001.md',
    'reference/fields/owner-score-a575b79868a2-001.md',
    'reference/fields/owner-second-16367aacb67a-001.md',
    'reference/fields/owner-sentinel-2b7847b7b705-001.md',
    'reference/fields/owner-skill-9c53c074d7ac-001.md',
    'reference/fields/owner-speed-bbccb9c002d5-001.md',
    'reference/fields/owner-spot-be2bdbb3100e-001.md',
    'reference/fields/owner-stack-6ee08e6eb3bc-001.md',
    'reference/fields/owner-state-4ba69735ca53-001.md',
    'reference/fields/owner-std%3A%3Astring-71fc1fac5cd5-001.md',
    'reference/fields/owner-summon-2815cb02b95b-001.md',
    'reference/fields/owner-sword-a44c47b1ee24-001.md',
    'reference/fields/owner-t-e3b98a4da31a-001.md',
    'reference/fields/owner-tail-0c62f876ef1d-001.md',
    'reference/fields/owner-target%E3%81%A8Unit-d9817836ed44-001.md',
    'reference/fields/owner-target%E5%BA%A7%E6%A8%99-9ca02a200b12-001.md',
    'reference/fields/owner-target-34a04005bcaf-001.md',
    'reference/fields/owner-this-1eb79602411e-001.md',
    'reference/fields/owner-tree-dc9c5edb8b2d-001.md',
    'reference/fields/owner-turn-9b473845f684-001.md',
    'reference/fields/owner-turnproc-cd2eb2171e89-001.md',
    'reference/fields/owner-ud-f0a85e81a4cd-001.md',
    'reference/fields/owner-unit-385cfdbc00ec-001.md',
    'reference/fields/owner-vcall-3d9d5373b3d4-001.md',
    'reference/fields/owner-vec-38a4fdfc27ed-001.md',
    'reference/fields/owner-vector-b0d51c58c8b9-001.md',
    'reference/fields/owner-vf-c70d6cef7d4f-001.md',
    'reference/fields/owner-virtual-e2efdd7db924-001.md',
    'reference/fields/owner-vslot-a0fcafa53039-001.md',
    'reference/fields/owner-vt-28d46654d818-001.md',
    'reference/fields/owner-vtable-f176ff0365e1-001.md',
    'reference/fields/owner-vtbl-ea21b65a314e-001.md',
    'reference/fields/owner-window%E6%A7%98entity%E3%81%AE-f681e3b86b07-001.md',
    'reference/fields/owner-window-44ff7b02c80d-001.md',
    'reference/fields/owner-word-98c1eb4ee934-001.md',
    'reference/fields/owner-zero%E3%81%AA%E3%82%89Skill-a83313cd755f-001.md',
    'research/intake/B/INDEX.md',
    'research/recovered/b_reports/B_REPORT_RECOVERY_LEDGER.tsv',
    'research/recovered/b_reports/B_T011_T012_MISSILE_VTABLE_SLOT38_OFFLINE_20261022_1813.sanitized.md',
    'research/recovered/b_reports/B_T011_T012_T013_OFFSET_ATTR_GATE_OFFLINE_20261022_2245.sanitized.md',
    'research/recovered/b_reports/B_T012_T013_ALLFUNC_HITCTX_EXP_OFFLINE_20261023_1017.md',
    'research/recovered/b_reports/B_T012_T013_BATTLEWND_ACTIVE_TREE_INSERT_OFFLINE_20261023_0417.sanitized.md',
    'research/recovered/b_reports/B_T012_T028_STATIC_RETPOINTER_BRANCH_ABI_OFFLINE_20261024_1209.md',
    'research/recovered/b_reports/B_T012_T028_STATIC_RETURN_DEATHBRANCH_OFFLINE_20261024_1111.md',
    'research/recovered/b_reports/DEFERRED.tsv',
    'research/recovered/b_reports/README.md',
    'research/recovered/b_reports/SANITIZATION_RECEIPTS.tsv',
    'research/recovered/b_reports/T011_SUPER_BRACE_STATUS_RETURN_ABI_NATIVE_20261025_02H.md',
    'research/recovered/b_reports/T011_T012_EXP_TRAINING_DEATH_CROSSWALK_NATIVE_20261029.md',
    'research/recovered/b_reports/T011_T013_GROUP1E_ALL25_CALLER_AL_POSTCALL_NATIVE_20261101_08H.md',
    'research/recovered/b_reports/T011_T024_DUAL_LIST_MODE3_VECTOR_NATIVE_20261101_12H.md',
    'research/recovered/b_reports/T011_T024_GROUP34_DUAL_BUCKET_ELIGIBILITY_NATIVE_20261101_11H.md',
    'research/recovered/b_reports/T011_T024_GROUP34_PROXIMITY_RATIO_100TICK_NATIVE_20261101_10H.sanitized.md',
    'research/recovered/b_reports/T012_STRATEGY_BATTLE_BOUNDARY_INTERFACE_20261021.md',
    'research/recovered/b_reports/T012_STR_RATIO_PRESENCE_ABI_AND_SPARSE_CFG_NATIVE_20261024_20H.md',
    'research/recovered/b_reports/T012_SUMMON_CORE_54E7B0_CONTRACT_20261013.md',
    'research/recovered/b_reports/T013_CATEGORY_WEIGHT_RNG_INLINE_HELPER_NATIVE_20261031_00H.md',
    'research/recovered/b_reports/T013_HEAL_FINISH_UNREGISTER_POOL_REUSE_NATIVE_20261027_10H.md',
    'research/recovered/b_reports/T013_INSERT_ALL10_CLEANUP_SHARED_TAIL_NATIVE_20261025_09H.md',
    'research/recovered/b_reports/T013_MODE2_CATEGORY_LABEL_AND_UNIT_WRITER_NATIVE_20261030_23H.md',
    'research/recovered/b_reports/T013_MODE2_POSTREFILL_SCORE_DISPATCH_NATIVE_20261030_21H.md',
    'research/recovered/b_reports/T013_POSTSELECT_ATAN2_FLOOR_ABI_JOIN_NATIVE_20261029_12H.md',
    'research/recovered/b_reports/T013_POSTSELECT_FOUR_CALLER_MODE_NATIVE_20261029_15H.md',
    'research/recovered/b_reports/T013_RANK_CLEANUP_TO_PERUNIT_EVENT_CALLCHAIN_NATIVE_20261031_14H.md',
    'research/recovered/b_reports/T013_RNG_CONTEXT_CARRY_NO_DIRECT_CMP_NATIVE_20261031_18H.md',
    'research/recovered/b_reports/T013_T024_528E86_GROUP1C_GATE_DISPATCH_NATIVE_20261101_20H.md',
    'research/recovered/b_reports/T013_VIEW_OFF_COMPARE_VSLOT5C_NATIVE_20261101_02H.md',
    'research/recovered/b_reports/T024_FALLBACK_FLAG_LATCH_FOURWAY_NATIVE_20261025_23H.md',
    'research/recovered/b_reports/T024_FOURWAY_LOOKUP_TWOMODE_ABI_NATIVE_20261026_00H.md',
    'research/recovered/b_reports/T024_GLOBAL65EB64_MODE_WRITERS_NATIVE_20261026_01H.md',
    'research/recovered/b_reports/T024_UNIT_ACTION_PRIORITY_CHAIN_NATIVE_20261025_17H.md',
    'research/recovered/dev_reports/BATTLE_DEFINITION_STAGE_20261011.md',
    'research/recovered/dev_reports/DEVLAB_ACTUAL_SAVE_GOLDEN_20261011.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261010_16H_STATIC_UNIT_SAVE.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261010_EB40_HEAL_172.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261010_EVENT_AI.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261010_SOURCEBOOK_180.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261010_SPATIAL_EVENT_156.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261010_STATIC_COMPAT_121.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261011_MODE6_DISTANCE_233.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261011_PARALLEL_STATUS.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261011_STATUS_DEXT.md',
    'research/recovered/dev_reports/DEVLAB_HANDOFF_20261011_TYPED_DAMAGE_215.md',
    'research/recovered/dev_reports/DEVLAB_NATIVE_LOADER_STAGE_20261011.md',
    'research/recovered/dev_reports/DEVLAB_WORLD_SCENE_BRIDGE_20261011.md',
    'research/recovered/dev_reports/DEV_REPORT_RECOVERY_LEDGER.tsv',
    'research/recovered/dev_reports/MAIN_DECOMP_STAGE_20261011.md',
    'research/recovered/dev_reports/PEER_SCRIPT01_RTTI_CLASSES_20261011.md',
    'research/recovered/dev_reports/README.md',
    'research/recovered/other_reports/DEFERRED.tsv',
    'research/recovered/other_reports/OTHER_REPORT_RECOVERY_LEDGER.tsv',
    'research/recovered/other_reports/README.md',
    'research/recovered/other_reports/T009_CONTEXT_MODEL.md',
    'research/recovered/other_reports/T025_DREAM_CLEARDAZO_GUARD_CONTRAST_20261015.md',
    'research/recovered/other_reports/T025_FARM_COUNT_PRODUCER_CONSUMER_NEW_TURN_20261015.md',
    'research/recovered/other_reports/T025_FREE_INITIAL_DIPLO_VECTOR_ARITY_CROSSWALK_20261014.md',
    'research/recovered/other_reports/T025_FREE_ROAM_LEVELUP_TWO_BAND_GATE_20261015.md',
    'research/recovered/other_reports/T025_GAMECLEAR_CALLSITE_ACHIEVEMENT_POSTYIELD_20261015.md',
    'research/recovered/other_reports/T025_GAMECLEAR_YIELD_AFTER_VICTORY_GATE_20261015.md',
    'research/recovered/other_reports/T025_POSTBATTLE_FRAMEINSTALL_SC_FREE_PREGUARD_20261015.md',
    'research/recovered/other_reports/T025_WORLD_ENTRY_SNAPSHOT_COM_DIPLO_QUEUE_JOIN_20261016.md',
    'research/recovered/other_reports/T025_WORLD_NEW_TURN_MERCHANT_LECTURE_YIELD_BOUNDARY_20261015.md',
    'research/recovered/other_reports/T029_CASTLE_VS_SIEGE_COUNTER_PHASE_CROSSWALK_20261015.md',
)
# Reviewed second authored-report batches and source-location metadata.
FILES += (
    'reference/fields/owner-A4%E3%81%A7candidate-a2bac052718f-001.md',
    'reference/fields/owner-AL-b7aea05ac84d-001.md',
    'reference/fields/owner-AND-bd972cc4f15d-001.md',
    'reference/fields/owner-BOTH-8c458494c5d0-001.md',
    'reference/fields/owner-C-6b23c0d5f35d-001.md',
    'reference/fields/owner-E6%E3%81%A7node-6e91ce12bd0e-001.md',
    'reference/fields/owner-F0%E3%81%8C-35314356f157-001.md',
    'reference/fields/owner-Heal%E7%94%A8vtable-31ee64de70fa-001.md',
    'reference/fields/owner-N-8ce86a6ae65d-001.md',
    'reference/fields/owner-O-c4694f2e93d5-001.md',
    'reference/fields/owner-S-8de0b3c47f11-001.md',
    'reference/fields/owner-Scratch-abe50eeb8aa5-001.md',
    'reference/fields/owner-and-6201111b83a0-001.md',
    'reference/fields/owner-at-b1d6b91b67c2-001.md',
    'reference/fields/owner-begin-e6f07d43b5c2-001.md',
    'reference/fields/owner-callback-f2579d976934-001.md',
    'reference/fields/owner-cap-45e84635bc48-001.md',
    'reference/fields/owner-deque-e93b27204f48-001.md',
    'reference/fields/owner-dword-e94a50a45e6e-001.md',
    'reference/fields/owner-flag-807d0fbcae7c-001.md',
    'reference/fields/owner-grid-0f2a693e93e2-001.md',
    'reference/fields/owner-including-031af55b1821-001.md',
    'reference/fields/owner-input-c96c6d5be8d0-001.md',
    'reference/fields/owner-key-2c70e12b7a06-001.md',
    'reference/fields/owner-kind-0b27c158feb3-001.md',
    'reference/fields/owner-later-1d9283d848ea-001.md',
    'reference/fields/owner-len-71fa9faaa6f8-001.md',
    'reference/fields/owner-no-9390298f3fb0-001.md',
    'reference/fields/owner-offsets-bb9567a24fab-001.md',
    'reference/fields/owner-opposed-ae04a7da6a71-001.md',
    'reference/fields/owner-random-a441b15fe9a3-001.md',
    'reference/fields/owner-ref-3ff6c05723bb-001.md',
    'reference/fields/owner-return-7187f0675eb3-001.md',
    'reference/fields/owner-select-b1a36d25d963-001.md',
    'reference/fields/owner-skips-7932e297e0ce-001.md',
    'reference/fields/owner-slot-6558838331b7-001.md',
    'reference/fields/owner-source-41cf6794ba42-001.md',
    'reference/fields/owner-value-cd42404d52ad-001.md',
    'reference/fields/owner-vs-f130559f0e7f-001.md',
    'reference/fields/owner-whose-55efa0938f9f-001.md',
    'reference/fields/owner-with-0695b563acde-001.md',
    'reference/fields/owner-write-10fd874b68da-001.md',
    'reference/fields/owner-writes-531995e8b52d-001.md',
    'research/recovered/GITHUB_EXACT_BODY_LINKS.tsv',
    'research/recovered/GITHUB_QUEUE.tsv',
    'research/recovered/GITHUB_SOURCES.md',
    'research/recovered/GITHUB_SOURCE_CATALOG.tsv',
    'research/recovered/ac_batch2/DEFERRED.tsv',
    'research/recovered/ac_batch2/README.md',
    'research/recovered/ac_batch2/REPORT_LEDGER.tsv',
    'research/recovered/ac_batch2/T016_GAMEPLAY_SYSTEMS.md',
    'research/recovered/ac_batch2/T025_FREE_WATCH_LEAGUE_ROSTER_CROSSWALK_20261014.md',
    'research/recovered/ac_batch2/T025_LEAGUE_FAKE_EU_CARVEOUT_CROSSWALK_20261015.md',
    'research/recovered/ac_batch2/T025_MZ_ROAMER_DUAL_RELOCATION_EVENT_ROUTES_20261016.md',
    'research/recovered/ac_batch2/T025_POO15_DECLARATION_REFERENCE_CENSUS_20261014.md',
    'research/recovered/ac_batch2/T025_RANDOMSET_TAIL_SABO_HAPPY_UNGUARDED_WORLD_20261015.md',
    'research/recovered/ac_batch2/T025_RANDOMSET_TARGET_SCOPE_DREAM_CONTRAST_20261015.md',
    'research/recovered/ac_batch2/T025_RANDOM_CASTLE_PRE_GUARD_PHASE_MATRIX_20261015.md',
    'research/recovered/ac_batch2/T025_RSC_INITIAL_DIPLO_ROSTER_LIFECYCLE_20261014.md',
    'research/recovered/ac_batch2/T025_RSC_TRAINING_ROSTER_PHASE_CROSSWALK_20261014.md',
    'research/recovered/ac_batch2/T025_WORLDWAR_CCC_DUAL_LIFETIME_CLEAR_REBIND_20261015.md',
    'research/recovered/ac_batch2/T025_WORLDWAR_EU_TALENT_LV25_VS_LEAGUE_20261015.md',
    'research/recovered/ac_batch2/T025_WORLD_CLEAR_BEFORE_FIRST_SETUP_CROSSWALK_20261015.md',
    'research/recovered/ac_batch2/T025_WORLD_PREGUARD_MORALE_NOTICE_INITIALIZATION_20261015.md',
    'research/recovered/ac_batch2/T034_SHIMOKITANO_TEA_SUBGAME.md',
    'research/recovered/b_batch2/B_T012_T013_SPATIAL_CELL_MIGRATION_OFFLINE_20261023_0716.md',
    'research/recovered/b_batch2/DEFERRED.tsv',
    'research/recovered/b_batch2/PREFLIGHT.json',
    'research/recovered/b_batch2/README.md',
    'research/recovered/b_batch2/REPORT_LEDGER.tsv',
    'research/recovered/b_batch2/T011_TRAINING_COUNT_PROVENANCE_NATIVE_20261031_06H.md',
    'research/recovered/b_batch2/T011_TRAINING_LEADER_BONUS_MEMO_NATIVE_20261031_07H.md',
    'research/recovered/b_batch2/T012_RUSH_GAMETASK_VIRTUAL_STATUS_GATE_NATIVE_20261027_17H.md',
    'research/recovered/b_batch2/T013_BATTLE_AI_DUAL_MODE_DISPATCH_JUMPTABLE_NATIVE_20261030_13H.md',
    'research/recovered/b_batch2/T013_GLOBAL65BD9E_QUOTA_QUARTER_WRITERS_NATIVE_20261101_01H.md',
    'research/recovered/b_batch2/T024_ACTION_STATE45D_AL0_BRANCH_NATIVE_20261025_18H.md',
    'research/recovered/b_batch2/T024_FIRST_UNIT_SHARED_GATE_TWO_CALLERS_NATIVE_20261026_02H.md',
    'research/recovered/b_batch2/T024_GROUP_REF_FTOL_YFLIP_NATIVE_20261101_19H.md',
    'research/recovered/b_batch2/T028_CANDIDATE_VECTOR_VS_SECOND_SET_NATIVE_20261028_11H.md',
    'research/recovered/b_batch2/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md',
    'research/recovered/b_batch2/T028_DEAD_EVENT_CONTEXT_MAP_RANGE_REPLACE_NATIVE_20261024_07H.md',
    'research/recovered/b_batch2/T028_DEQUE_FIFO_ALT_SPAWN_SHARED_NATIVE_20261026_15H.md',
    'research/recovered/b_batch2/T028_DUAL_DEATH_ENTRY_SENTINEL_HP_GATE_NATIVE_20261024_0808.md',
    'research/recovered/b_batch2/T028_EFFECT_ALFLAG_CALLSITE_SENTINEL_MATRIX_NATIVE_20261029_08H.md',
    'research/recovered/b_batch2/T028_LOYAL_DOWN_POINTER_KEY_GUARD_NATIVE_20261028_06H.md',
    'research/recovered/b_batch2/T028_NAMED_RESOLVER_SENTINEL_ROSTER_SEED_NATIVE_20261028_07H.md',
    'research/recovered/b_batch2/T028_NULL_VECTOR_CANDIDATE_DESTRUCTION_NATIVE_20261028_12H.md',
    'research/recovered/b_batch2/T028_RESULT_TUPLE_18CALLERS_INDEX3_NULL_SINK_NATIVE_20261029_01H.md',
    'research/recovered/b_batch2/T028_RETREAT_OK_POSTPASS_VTABLE68_NATIVE_20261029_20H.md',
    'research/recovered/b_batch2/T028_RETREAT_OK_QUEUE_DRAIN_ELIGIBILITY_NATIVE_20261029_19H.md',
    'research/recovered/b_batch2/T028_ROSTER_VECTOR_DUAL_SET_PRODUCER_NATIVE_20261028_10H.md',
    'research/recovered/b_batch2/T028_ROUTE_CACHE_PAYLOAD_ERASE_FULLCLEAR_NATIVE_20261027_02H.md',
    'research/recovered/b_batch2/T028_SIGNED_MODE_TWO_EFFECT_SUBOBJECTS_NATIVE_20261029_09H.md',
    'research/recovered/b_batch2/T028_TEMP_SET_INSERT_ABI_NATIVE_20261028_04H.md',
    'research/recovered/b_batch2/T028_VISITED_TREE_DEDUPE_QUEUE_PRECHECK_NATIVE_20261026_16H.md',
    'research/recovered/b_batch2/T028_WANDER_MERCENARY_TEMPLATE_DISPATCH_NATIVE_20261028_15H.md',
    'research/recovered/e_reports/DEFERRED.tsv',
    'research/recovered/e_reports/README.md',
    'research/recovered/e_reports/REPORT_LEDGER.tsv',
    'research/recovered/e_reports/SCOPE_AUDIT.md',
    'research/recovered/e_reports/T020_E_T011_CACHE_LIFECYCLE_ACCEPTANCE_20261031_08H.md',
    'research/recovered/e_reports/T020_E_T011_LEADER_CACHE_ACCEPTANCE_20261031_07H.md',
    'research/recovered/e_reports/T020_E_T011_TRAINING_BRANCH_ACCEPTANCE_20261031_06H.md',
    'research/recovered/e_reports/T020_E_T013_ALT_LIST_RESET_ACCEPTANCE_20261031_22H.md',
    'research/recovered/e_reports/T020_E_T013_BTLLIMIT_CLOCK_ACCEPTANCE_20261031_02H.md',
    'research/recovered/e_reports/T020_E_T013_BUCKET_MERGE_ACCEPTANCE_20261031_16H.md',
    'research/recovered/e_reports/T020_E_T013_CATEGORY_WEIGHT_RNG_ACCEPTANCE_20261031_00H.md',
    'research/recovered/e_reports/T020_E_T013_CATEGORY_WRITER_ACCEPTANCE_20261030_23H.md',
    'research/recovered/e_reports/T020_E_T013_COORD_GATE_RECT_ACCEPTANCE_20261101_00H.md',
    'research/recovered/e_reports/T020_E_T013_DRAIN_RESTORE_CAP_ACCEPTANCE_20261031_17H.md',
    'research/recovered/e_reports/T020_E_T013_DUAL_SCORE_SIGNED_ACCEPTANCE_20261031_12H.md',
    'research/recovered/e_reports/T020_E_T013_EFFECTIVE_CONTEXT_ACCEPTANCE_20261031_03H.md',
    'research/recovered/e_reports/T020_E_T013_EMPTY_REPOPULATE_ACCEPTANCE_20261030_20H.md',
    'research/recovered/e_reports/T020_E_T013_EQUAL_RANGE_ERASE_ACCEPTANCE_20261030_19H.md',
    'research/recovered/e_reports/T020_E_T013_FIXED_ANCHOR_CORRECTION_ACCEPTANCE_20261031_13H.md',
    'research/recovered/e_reports/T020_E_T013_HALFBIAS_RNG_EXHAUSTIVE_ACCEPTANCE_20261031_01H.md',
    'research/recovered/e_reports/T020_E_T013_HEAD_SENTINEL_COORD_ACCEPTANCE_20261031_21H.md',
    'research/recovered/e_reports/T020_E_T013_KIND8_PREQUEUE_ACCEPTANCE_20261031_15H.md',
    'research/recovered/e_reports/T020_E_T013_LABEL_WEIGHT_FANOUT_ACCEPTANCE_20261031_04H.md',
    'research/recovered/e_reports/T020_E_T013_MODE2_DUALGATE_ACCEPTANCE_20261030_15H.md',
    'research/recovered/e_reports/T020_E_T013_MODE2_PRIMARY_ACCEPTANCE_20261030_14H.md',
    'research/recovered/e_reports/T020_E_T013_MODE2_RANGE_UNIT_ACCEPTANCE_20261030_18H.md',
    'research/recovered/e_reports/T020_E_T013_MODE3_EBX_ACCEPTANCE_20261031_05H.md',
    'research/recovered/e_reports/T020_E_T013_OFF_EXACT_VSLOT_ACCEPTANCE_20261101_02H.md',
    'research/recovered/e_reports/T020_E_T013_PAIRWISE_DISTANCE_ACCEPTANCE_20261030_16H.md',
    'research/recovered/e_reports/T020_E_T013_POSTRANK_UNIT8_ACCEPTANCE_20261031_14H.md',
    'research/recovered/e_reports/T020_E_T013_POSTREFILL_ACCEPTANCE_20261030_21H.md',
    'research/recovered/e_reports/T020_E_T013_RECT_BOOL_WINAPI_ACCEPTANCE_20261031_23H.md',
)
FILES += (
    'reference/fields/owner-CALL0x4FAA60%E3%81%A7manager-6df428c033f1-001.md',
    'reference/fields/owner-Heal%E8%87%AA%E8%BA%AB%E3%81%AE-8fd5e7738ca8-001.md',
    'reference/fields/owner-Main-eb814be3ca3b-001.md',
    'reference/fields/owner-PUSH%E5%88%86%E6%88%BB%E3%81%99%E3%81%A8%E6%97%A7ESP-e0e0ab641f30-001.md',
    'reference/fields/owner-SLOT-12dd6f102b80-001.md',
    'reference/fields/owner-Unit%E6%A7%98S-42b2ce17601c-001.md',
    'reference/fields/owner-Unit-4e545960f1bf-003.md',
    'reference/fields/owner-arg-b25f03dedd69-001.md',
    'reference/fields/owner-candidate_context-bcfc66f35d11-001.md',
    'reference/fields/owner-compiled-64ebd2677178-001.md',
    'reference/fields/owner-controller-c1472135b14c-001.md',
    'reference/fields/owner-core%E8%87%AA%E4%BD%93%E3%81%AFSkill-c61391462fc1-001.md',
    'reference/fields/owner-effects-888ad3a8bb06-001.md',
    'reference/fields/owner-entry-923fe53966c6-001.md',
    'reference/fields/owner-find-e6640de835ad-001.md',
    'reference/fields/owner-iStack_38-bc6fe148c700-001.md',
    'reference/fields/owner-iVar5-2c1894b297e9-001.md',
    'reference/fields/owner-in_EAX-ac8de0aa2a6f-001.md',
    'reference/fields/owner-length-0f82aca66af9-001.md',
    'reference/fields/owner-old-cba06b5736fa-001.md',
    'reference/fields/owner-over-5fb6a47e368e-001.md',
    'reference/fields/owner-param_1-3e44daf95428-001.md',
    'reference/fields/owner-producer%E3%81%A8manager-cbf4ffb0027c-001.md',
    'reference/fields/owner-recipient-665d0698dbc8-001.md',
    'reference/fields/owner-result-f6a214f7a5fc-001.md',
    'reference/fields/owner-returned-68752bf62253-001.md',
    'reference/fields/owner-set-6ee0eb490ff8-001.md',
    'reference/fields/owner-the-b9776d7ddf45-001.md',
    'reference/fields/owner-x-2d711642b726-001.md',
    'reference/static_calls.tsv',
    'reference/static_calls_source.json',
    'research/recovered/b_batch3/B_T011_T012_T013_OFFSET_TREES_OFFLINE_20261022_2310.md',
    'research/recovered/b_batch3/B_T012_RENDER_ORDER_ROUTE_OFFLINE_20261022_1912.md',
    'research/recovered/b_batch3/B_T012_T013_COLLISION_CLEANUP_OWNER_OFFLINE_20261023_0009.md',
    'research/recovered/b_batch3/B_T012_T013_DUAL_POOL_RANGE_FANOUT_OFFLINE_20261023_0909.md',
    'research/recovered/b_batch3/B_T012_T013_VSLOT70_LIVE_VECTOR_OFFLINE_20261023_1109.md',
    'research/recovered/b_batch3/DEFERRED.tsv',
    'research/recovered/b_batch3/README.md',
    'research/recovered/b_batch3/REPORT_LEDGER.tsv',
    'research/recovered/b_batch3/T011_FOLLOW_COMPILER_RUSH_RESULT_LINK_NATIVE_20261027_20H.md',
    'research/recovered/b_batch3/T011_MEMBER_FACTORY_REENTRY_GATE_OFFLINE_20261021_0510.md',
    'research/recovered/b_batch3/T011_SUMMON_CALLER_GROUP_PROVENANCE_NATIVE_20261027_15H.md',
    'research/recovered/b_batch3/T011_T012_SUPER_SCRIPT_PARSER_PRODUCER_NATIVE_20261024_22H.md',
    'research/recovered/b_batch3/T011_T013_GROUP34_WEIGHTED_SQRT_AL1_NATIVE_20261101_09H.md',
    'research/recovered/b_batch3/T012_ENTRY_CONTEXT_FALLBACK_SUPPORT_AND_RESET_20261021.md',
    'research/recovered/b_batch3/T012_RUSH_SKILL_INTERVAL_FIRST_TICK_BURST_NATIVE_20261027_18H.md',
    'research/recovered/b_batch3/T012_UNIT_VIRTUAL80_579290_CONTRACT_20261013.md',
    'research/recovered/b_batch3/T013_CASE8_MAP_VECTOR_STRIDE_WRITER_NATIVE_20261024_06H.md',
    'research/recovered/b_batch3/T013_GAMEMANAGER_GLOBAL_BACKLINKS_NATIVE_20261027_12H.md',
    'research/recovered/b_batch3/T013_HEAL_DEFERRED_TICK_DISPATCH_NATIVE_20261027_09H.md',
    'research/recovered/b_batch3/T013_MAP_INSERT_CALLSITE_COVERAGE_NATIVE_20261025_06H.md',
    'research/recovered/b_batch3/T013_MODE2_ALT_DUALFLAG_AND_MODE3_NATIVE_20261030_15H.md',
    'research/recovered/b_batch3/T013_MODE2_DOUBLE_UNIT_SUM_RATIO_BRANCH_NATIVE_20261030_22H.md',
    'research/recovered/b_batch3/T013_MODE2_EMPTY_RANGE_REPOPULATE_NATIVE_20261030_20H.md',
    'research/recovered/b_batch3/T013_MODE2_EQUAL_RANGE_ERASE_NATIVE_20261030_19H.md',
    'research/recovered/b_batch3/T013_MODE2_VECTOR_RANGE_INSERT_UNIT_GATE_NATIVE_20261030_18H.md',
    'research/recovered/b_batch3/T013_RECT_INSET_BOOLEAN_NATIVE_20261031_23H.md',
    'research/recovered/b_batch3/T013_SUPPORT_EFFECT_54E0B0_CONTRACT_20261013.md',
    'research/recovered/b_batch3/T013_TROOP_RTTI_HALF_RATIO_GATE_V9_20261023_1708.md',
    'research/recovered/b_batch3/T024_SELECTION_UNLINK_RESET_TAILJMP_NATIVE_20261025_21H.md',
    'research/recovered/b_batch3/T024_TEMP_SELECTION_UI_ADAPTER_NATIVE_20261025_22H.md',
    'research/recovered/b_batch3/T028_ALT_GRID_EIGHT_DIRECTION_CLEARANCE_NATIVE_20261026_14H.md',
    'research/recovered/b_batch3/T028_BATTLE_MODE_CONFIG_PRODUCER_NATIVE_20261028_00H.md',
    'research/recovered/b_batch3/T028_CACHE_INSERT_RESULT_NOT_CONSUMED_AND_SHARED_HASH_NATIVE_20261027_04H.md',
    'research/recovered/b_batch3/T028_DEADEVENT_COUNT_COLOR_QUEUE_NATIVE_20261027_21H.md',
    'research/recovered/b_batch3/T028_FALLBACK_GLOBAL_PAIR_RETABI_NATIVE_20261026_13H.md',
    'research/recovered/b_batch3/T028_FIRST_SET_EXCLUSION_RESOLVER_BACKLINK_NATIVE_20261028_05H.md',
    'research/recovered/b_batch3/T028_POSTRET_TEMP_TREE_RANGE_ERASE_CALLSITE_CORRECTION_NATIVE_20261030_08H.md',
    'research/recovered/b_batch3/T028_QUEUE_SINK_SHARED_DIALOG_ARITY_GUARDS_NATIVE_20261029_02H.md',
    'research/recovered/b_batch3/T028_RETREAT_DUAL_ATTEMPT_POSTRET_EDGE_NATIVE_20261030_05H.md',
    'research/recovered/b_batch3/T028_RETREAT_SPOT_RESERVATION_RELEASE_NATIVE_20261029_23H.md',
    'research/recovered/b_batch3/T028_SPATIAL_GRID_CTOR_FLAG_PROVENANCE_NATIVE_20261026_11H.md',
    'research/recovered/b_batch3/T028_SPATIAL_GRID_DUAL_ERASE_AND_MOVE_NATIVE_20261026_09H.md',
    'research/recovered/b_batch3/T028_SPATIAL_INSERT_TWO_MODES_NATIVE_20261026_10H.md',
    'research/recovered/b_batch3/T028_THIRD_SELECTOR_CALLER_RETURN_GATE_NATIVE_20261030_10H.md',
    'research/recovered/b_batch3/TRANSFORMATIONS.json',
    'tools/export_static_calls.py',
    'tools/test_static_calls.py',
)
FILES += (
    'reference/fields/owner-field-c0d2856b74d0-001.md',
    'research/recovered/GITHUB_DISCOVERY_DIFF.tsv',
    'research/recovered/MEMORY_RELATION_REVIEW.md',
    'research/recovered/SCHEDULE_CHAT_CHECK.md',
    'research/recovered/c_topics/DEFERRED.tsv',
    'research/recovered/c_topics/README.md',
    'research/recovered/c_topics/REPORT_LEDGER.tsv',
    'research/recovered/c_topics/REVIEW_RECEIPT.tsv',
    'research/recovered/c_topics/T026_EDUCATION_MATRIX.md',
    'research/recovered/c_topics/T027_MERCHANT_PRICE_PURCHASE.md',
    'research/recovered/random_events/README.md',
    'research/recovered/random_events/REPORT_LEDGER.tsv',
    'research/recovered/random_events/T032_RANDOM_EVENT_EFFECTS.md',
)
ALLOWED = set(FILES) | {MANIFEST}
RESTRICTED = (
    re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[A-Za-z0-9._-]+"),
    re.compile(r"(?i)\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"(?i)\b(?:github_pat_|gh[pousr]_)[A-Za-z0-9_-]{18,}\b"),
    re.compile(r"(?i)\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"-----BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY-----"),
)
TASK = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{2,48}\Z")

class Blocked(Exception):
    pass

def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def digest(data):
    return hashlib.sha256(data).hexdigest().upper()

def command(parts, check=True):
    try:
        p = subprocess.run(parts, cwd=KB, capture_output=True,
                           timeout=60, text=True, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Blocked(f"外部コマンド失敗: {parts[0]} / {type(e).__name__}")
    if p.returncode and check:
        # Don't echo raw process output; it can contain private credentials.
        raise Blocked(f"外部コマンド拒否: {parts[0]} {parts[1]} (exit={p.returncode})")
    return p.stdout.strip(), p.returncode

def git(*args, check=True):
    return command(("git", "-C", str(KB), *args), check=check)

def ensure_root():
    top, rc = git("rev-parse", "--show-toplevel", check=False)
    if rc or Path(top).resolve() != KB.resolve():
        raise Blocked("knowledge の独立Gitリポジトリでない")
    return True

def safe_files(root=KB, enforce_git=False):
    problems, hashes = [], {}
    ignore = root / ".gitignore"
    if not ignore.is_file():
        problems.append(".gitignore がない")
    else:
        content = ignore.read_text(encoding="utf-8")
        for mandatory in ("/*", "/tools/*", "/sources/*",
                          "/generated/", "!/symbols.tsv", "!/structs.tsv"):
            if mandatory not in content.splitlines():
                problems.append(".gitignore 必須規則欠落: "+mandatory)
    for relative in FILES:
        f = root / relative
        if not f.is_file() or f.is_symlink():
            problems.append("不足・リンク: "+relative)
            continue
        raw = f.read_bytes()
        hashes[relative] = (digest(raw), len(raw))
        if len(raw) > 2_000_000 or b"\x00" in raw:
            problems.append("サイズまたはバイナリ不適切: "+relative)
            continue
        try:
            s = raw.decode("utf-8-sig")
        except UnicodeError:
            if relative.endswith(".bat"):
                try:
                    s = raw.decode("cp932")
                except UnicodeError:
                    problems.append("解読不能: "+relative)
                    continue
            else:
                problems.append("UTF-8以外の原稿: "+relative)
                continue
        # The standard Git SSH transport identity is not a private email.
        sanitized = s.replace("git@github.com:", "git-ssh-remote:")
        if any(p.search(sanitized) for p in RESTRICTED):
            problems.append("機密の可能性あり（出典を確認）: "+relative)
    if enforce_git:
        ensure_root()
        tracked, _ = git("ls-files", "-z")
        for relative in tracked.split("\x00"):
            if relative and relative not in ALLOWED:
                problems.append("許可外のGit追跡対象: "+relative)
        staged, _ = git("diff", "--cached", "--name-only")
        for relative in staged.splitlines():
            if relative and relative not in ALLOWED:
                problems.append("許可外のステージ済みファイル: "+relative)
    return problems, hashes

def manifest(hashes):
    return ("# Generated locally by sync_knowledge.py\n"
            "path\tsha256\tbytes\n" +
            "".join(f"{k}\t{h}\t{size}\n"
                    for k,(h,size) in sorted(hashes.items())))

def write_manifest(hashes):
    path = KB / MANIFEST
    tmp = KB / (MANIFEST + ".tmp")
    if tmp.exists():
        raise Blocked("manifestの前回の一時ファイルがある")
    tmp.write_text(manifest(hashes), encoding="utf-8", newline="\n")
    os.replace(tmp, path)

def verify_staged_bytes(names):
    """Index objects must contain exactly the bytes recorded in the manifest."""
    for name in names:
        actual = git("hash-object", "--no-filters", "--", name)[0]
        indexed = git("rev-parse", ":" + name)[0]
        if actual != indexed:
            raise Blocked("Git indexと原本のバイトが一致しない: " + name)

def verify_manifest(hashes):
    f = KB / MANIFEST
    if not f.is_file():
        return False
    return f.read_text(encoding="utf-8") == manifest(hashes)

def branch():
    return git("branch", "--show-current")[0]

def clean():
    return not git("status", "--porcelain", "--untracked-files=all")[0]

def private_repo():
    ensure_root()
    url, _ = git("remote", "get-url", "origin")
    accepted = (f"https://github.com/{REPO}", f"https://github.com/{REPO}.git",
                f"git@github.com:{REPO}", f"git@github.com:{REPO}.git")
    if url not in accepted:
        raise Blocked("origin URLが指定の非公開研究リポジトリと一致しない")
    vis, _ = command(("gh","repo","view",REPO,"--json","visibility","--jq",".visibility"))
    if vis.upper() != "PRIVATE":
        raise Blocked("GitHub private 設定を確認できない")

def journal(action, status, task="", message=""):
    folder = KB / ".git"
    if not folder.is_dir():
        return
    item = dict(timestamp=stamp(), action=action, status=status,
                task=task, detail=message[:240])
    with open(folder / "kb-sync-journal.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False)+"\n")

@contextlib.contextmanager
def lock(action):
    path = KB / ".git/kb-sync.lock"
    if not path.parent.is_dir():
        raise Blocked("Git未初期化")
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    except FileExistsError:
        raise Blocked("他の操作がロック保持中。勝手に解除しない")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dict(action=action,time=stamp(),pid=os.getpid()), f)
        yield
    finally:
        path.unlink(missing_ok=True)

def audit_or_block(require_git=False):
    issues, hashes = safe_files(enforce_git=require_git)
    if issues:
        raise Blocked("; ".join(issues[:8]))
    return hashes

def start(task):
    audit_or_block(True)
    with lock("start"):
        if branch() != MAIN or not clean():
            raise Blocked("developがクリーンでない、または別ブランチ")
        private_repo()
        git("fetch", "origin", MAIN)
        if git("rev-parse","HEAD")[0] != git("rev-parse","origin/"+MAIN)[0]:
            raise Blocked("GitHubのdevelopが先行または分岐。ff-onlyの確認が必要")
        new = "work/kb-"+task
        git("switch","-c",new)
        base = dict(branch=new, base=git("rev-parse","HEAD")[0], created=stamp())
        (KB/".git/kb-sync-base.json").write_text(
            json.dumps(base,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        journal("start","LOCAL_ONLY",task,new)
        print("STARTED",new)

def checkpoint(task):
    before = audit_or_block(True)
    with lock("checkpoint"):
        b = branch()
        if b != "work/kb-"+task:
            raise Blocked("作業IDと作業ブランチが一致しない")
        basefile = KB/".git/kb-sync-base.json"
        if not basefile.is_file():
            raise Blocked("作業開始のベースSHA記録がない")
        base = json.loads(basefile.read_text(encoding="utf-8-sig"))
        if base.get("branch") != b:
            raise Blocked("開始時のブランチ情報不一致")
        if git("diff","--cached","--name-only")[0]:
            raise Blocked("他のステージ変更があるため中止")
        write_manifest(before)
        git("add","--",*FILES,MANIFEST)
        after = audit_or_block(True)
        verify_staged_bytes((*FILES, MANIFEST))
        if after != before or not verify_manifest(after):
            raise Blocked("競合: 書込み中に内容/SHAが変化。indexを確認するまで中断")
        staged = git("diff","--cached","--name-only")[0].splitlines()
        if not staged:
            print("NO_CHANGE")
            return
        git("commit","-m","knowledge checkpoint: "+task)
        sha=git("rev-parse","HEAD")[0]
        journal("checkpoint","LOCAL_ONLY",task,sha)
        print("LOCAL_CHECKPOINT",sha)

def verify_portable_publication():
    """Require portable exports and their reviewed evidence in the explicit Git set."""
    ledger = "research/recovered/RECOVERY_LEDGER.tsv"
    registry = "reference/sources.json"
    try:
        data = reference.load(KB)
        required = set(reference.render(KB, data))
        required.update((ledger, registry, "reference/relations.jsonl"))
        with (KB / ledger).open(encoding="utf-8-sig", newline="") as stream:
            required.update(row["destination"] for row in csv.DictReader(stream, delimiter="\t"))
        citations = json.loads((KB / registry).read_text(encoding="utf-8-sig"))
        required.update(entry["path"] for entry in citations.values())
        required.update(row["source"]["path"] for row in data["relations"])
        for name in ("reference/static_calls.tsv", "reference/static_calls_source.json",
                     "tools/export_static_calls.py"):
            if (KB / name).exists():
                required.add(name)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise Blocked("Portable publication inputs invalid; rerun reference/coverage checks: " + str(error)) from error
    tracked = set(git("ls-files", "-z")[0].split("\0"))
    issues = []
    for name in sorted(required):
        if name not in ALLOWED:
            issues.append("not explicitly ALLOWED: " + name)
        if name not in tracked:
            issues.append("not Git-tracked: " + name)
    if issues:
        raise Blocked("Portable publication blocked: " + "; ".join(issues[:8])
                      + ". Review these exact paths, update FILES/.gitignore as needed, "
                      "then checkpoint them before publishing.")


def publish():
    hashes=audit_or_block(True)
    with lock("publish"):
        b=branch()
        if not b.startswith("work/kb-") or not clean() or not verify_manifest(hashes):
            raise Blocked("作業ブランチではない/dirty/manifestが不一致")
        private_repo()
        basefile=KB/".git/kb-sync-base.json"
        if not basefile.is_file():
            raise Blocked("作業開始SHAがない")
        base=json.loads(basefile.read_text(encoding="utf-8-sig"))
        if base.get("branch")!=b:
            raise Blocked("作業ブランチと基準SHAが異なる")
        for script in ("reference.py", "recovery_coverage.py"):
            command((sys.executable, "-B", str(KB / "tools" / script), "check"))
        verify_portable_publication()
        git("fetch","origin",MAIN)
        if git("rev-parse","origin/"+MAIN)[0]!=base.get("base"):
            raise Blocked("リモートdevelopが進んでいる。競合確認が必要")
        sha=git("rev-parse","HEAD")[0]
        git("push","origin","HEAD:refs/heads/"+b)
        remote=git("ls-remote","--heads","origin","refs/heads/"+b)[0]
        if not remote.startswith(sha+"\t"):
            raise Blocked("push後のリモートSHAが一致しない")
        journal("publish","SYNCED",b,sha)
        print("SYNCED",b,sha)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("action",choices=("audit","status","manifest","start","checkpoint","publish"))
    ap.add_argument("task",nargs="?")
    args=ap.parse_args()
    try:
        if args.action=="audit":
            audit_or_block((KB/".git").exists())
            print("AUDIT_PASS",len(FILES))
        elif args.action=="manifest":
            before=audit_or_block((KB/".git").exists())
            if (KB/".git").exists() and branch() != MAIN and not branch().startswith("work/kb-"):
                raise Blocked("manifest生成は許可されたGitブランチでのみ可能")
            write_manifest(before)
            after=audit_or_block((KB/".git").exists())
            if before != after or not verify_manifest(after):
                raise Blocked("manifest保存中に原本が変化")
            print("MANIFEST_WRITTEN",len(after))
        elif args.action=="status":
            problems,fs=safe_files(enforce_git=(KB/".git").exists())
            print("SOURCE_COUNT",len(fs),"ISSUES",len(problems))
            for problem in problems: print("ISSUE",problem)
            if (KB/".git").exists():
                print("BRANCH",branch(),"CLEAN",clean())
                print("MANIFEST_OK",verify_manifest(fs))
        else:
            if args.action in ("start","checkpoint"):
                if not args.task or not TASK.fullmatch(args.task):
                    raise Blocked("作業IDを英数字・ハイフンで指定")
                (start if args.action=="start" else checkpoint)(args.task)
            else:
                publish()
        return 0
    except Blocked as err:
        print("BLOCKED",str(err))
        journal(args.action,"BLOCKED",args.task or "",str(err))
        return 2

if __name__=="__main__":
    sys.exit(main())

