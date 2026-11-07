# B 23H: 0x542280のdouble優先と整数差fallback（STATIC V9）
research_id: B-20261101-23H-T024-542280-OPTIONAL-DOUBLE-FALLBACK-01
owner: B; tasks: T024; T013の最終対象接続はVERIFY; observed_at: 2026-11-01 23H JST; intake_at: 2026-11-01 23H JST
source_relative_paths: data/T024_OPTIONAL_DOUBLE_FALLBACK_THUNK_V9_STATIC_20261101_23H.md; rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite (DB is NOT uploaded)
source_sha256: 7054AB145A67A5CA10D60C9850CA0256690EFBF1061C945893BB3C0D0A1A4BEC (PC report Get-FileHash and text readback on 23H)
v9_database_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE (prior manifest; DB not rehashed this run)
original_exe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (prior manifest, EXE not rehashed this run)
individual_ghidra_pseudoc_sha: UNVERIFIED_SOURCE (composite V9 row read, per-C-file SHA/line not obtained)
evidence_kind: STATIC_V9 / INFERRED / VERIFY; golden_status: ORIGINAL_GAME_PASS0; strict_match: 0; dynamic: 0; ready_status: NOT_READY; intake: PUBLISHED_INTAKE/NOT_CURATED
prior_ids: B-20261101-22H-T024-DUAL-CALLER-FACTOR-PROVENANCE-CROSSJOIN-01 (2 caller producers), 20H/21H T013/T024 mode0 dispatch gates. This ID adds internal 0x542280 branch, not a new claim of final target.
## 直接確認した限定静的証拠
V9 Ghidra pseudoc function 0x542280 body [0x542280,0x5422BC], 61B: if global double at 0x63B0B8 differs from object double at +0x50, return object+0x50; else return FUN_005E743A( object int+0x40 minus object int+0x38 ) plus global double at 0x62A190. The sentinel interpretation, original FP compare direction and native ABI are VERIFY, not guaranteed C semantics.
V9 direct E8 0x5422B0 bytes E8 85 51 0A 00 ->0x5E743A. V9 0x5E743A 10-byte pseudoc __cintrindisp2(), 0x5E743F E9 CC DA FF FF ->0x5E4F10 is tail JMP, NOT a CALL. Exact intrinsic conversion/time/RNG side effects not inferred.
V9 caller 0x5271A0 uses direct E8 0x52722F/0x527258/0x52728B/0x52729C/0x5273BA ->0x542280, then 0x5272AB ->0x528DB0 or 0x52727A ->0x569730 along distinct routes. 0x528870 instead 0x528919/0x5289EF ->0x5E743A directly, adds 0x62A190, and 0x528A04 ->0x528DB0 / 0x52893D ->0x569730. These input producers must not be conflated; their actual gameplay effect not yet proven.
KB_CANDIDATE: VAs 0x542280,0x5E743A,0x5E4F10,0x5271A0,0x528870,0x528DB0,0x569730; CALL 0x5422B0->0x5E743A; JMP 0x5E743F->0x5E4F10; offsets object+0x50/+0x40/+0x38, globals 0x63B0B8/0x62A190.
next_validation: native 0x542280 comparison instruction/constant actual values, +0x50 writer, 0x5E4F10 ABI, legal unmodified original gameplay same EXE/DAT/MAP/SAVE/input/RNG/tick through selected Unit action. Golden0/strict0/READY0.
recovery: 03H UNKNOWN、07H core4 missing、10/25 missing source/54byte discrepancy OPEN、旧HOLD21 safety refusal unchanged; no retries of rejected VA/XREF. Curator alone may update develop/REF/symbols/structs.
