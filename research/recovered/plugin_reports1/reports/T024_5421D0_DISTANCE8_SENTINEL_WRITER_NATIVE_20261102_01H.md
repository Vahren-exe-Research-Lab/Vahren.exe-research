# B/T024 2026-11-02 01H | 0x5421D0 原作native：8.0距離比較による+0x50角度sentinel writer
research_id: B-20261102-01H-T024-5421D0-8DIST-SENTINEL-WRITER-01
owner: B; tasks: T024 (T013 final target is VERIFY); status: STATIC_NATIVE / STATIC_V9 / INFERRED / VERIFY / NOT READY.
Original Gameplay Golden PASS=0; old/new strict MATCH=0; DYNAMIC=0; new READY=0.
## Source and research isolation
Original ver0.67 PE Vahren.exe SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (independently read-only rehashed in this run; original not executed).
Native original PE window [0x5421D0,0x542271) 161 bytes SHA256 E86BF3E5B665DC3F0952A8F86419D705C0542154BD1B89A673A2DD0A0492C449.
Read-only verifier: data/B_20261102_01H_T024_5421D0_NATIVE_READONLY_VERIFY.py SHA256 2A3741E2B3C21AC0EC6AE7FAA4C8989877308C71D54F1A703D2EC7E62F02A84D (saved, read back, exit successful).
V9 CLI source: rea_lab/headless_analysis/search_index/search_unified_v9_20261023.py with HAKUSHIN067_UNIFIED_V9_20261023.sqlite (prior integrity SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE, not rehashed this run). V9 pseudo-C and caller graph are STATIC only, native ABI UNVERIFIED.
V9 callers 0x5421D0: only directly indexed E8 CALL at 0x527344 (raw e887ae0100) from 0x5271A0. Indirect callers not exhausted.
## New source evidence: writer, not another claim of atan2 discovery
At 0x5421D0..0x5421DD function stores input axes into [ESI+0x34/+0x38/+0x3C/+0x40].
0x5421E0..0x5421F3 subtracts axes, signed integer IMUL squares twice, ADD sums, then FILD signed sum; 0x5421FC E8→0x5E3B70 computes sqrt (known static helper). 32-bit overflow, sign and FP edge behavior remain VERIFY.
0x542201 FLD double [0x62A198]=8.0; 0x542207 FCOMP ST(1); 0x542209 FNSTSW AX; 0x54220B TEST AH,05; 0x54220E JP 0x542219 (skip sentinel assignment); 0x542210 FLD double [0x63B0B8]=10000.0; 0x542216 FSTP qword [ESI+0x50].
In normal finite, non-overflowing case, square-root distance >8.0 causes sentinel write +0x50=10000.0; <=8.0 takes 0x54220E JP and does not write +0x50 here. NaN / signed wrap / FPU exception branches NOT confirmed by game observation.
0x54221B compares an input flag; nonzero branch 0x542221 FMUL double [0x63B238]=1.25 and conditional +0x48 storage/clamp; zero branch 0x542243 skips this scaling. Flag semantic and native ABI are VERIFY.
0x54224A increments [ESI+0x30], 0x54224D CMP +0x30,0x20 then 0x542253 resets if >32; first-init gate 0x542256 CMP [ESI+0x2C],0, 0x542261 flag=1 and 0x542268 E8→0x4C3D30. Lifetime and UI side effects VERIFY.
## Connection to established reader, deduplication and acceptance
Earlier B-20261102-00H-T024-542280-NATIVE-ATAN2-SENTINEL-ERRATUM-01 proved that 0x542280 compares +0x50 with 10000.0 and on equality computes atan2 of the TWO signed coordinate deltas plus float-rounded pi. This run establishes an actual writer/gate upstream; does not re-count reader/atan2, previous 23H error, or 26 Oct atan2 descriptor.
knowledge/kb.py addr 0x5421D0 and research 0x5421D0 --task T024 returned no registered symbol or indexed report at run time, but this is not complete cross-lane ownership proof. KB_CANDIDATE: VA 0x5421D0, callsite 0x527344, offsets +0x34/+0x38/+0x3C/+0x40/+0x48/+0x50/+0x30/+0x2C and globals 0x62A198/0x63B0B8/0x63B238; STATIC/INFERRED/VERIFY/NOT READY.
Golden needed: legitimate original-game inputs with signed delta lengths <8,=8,>8 and previous +0x50, same DAT/SAVE/MAP/input/RNG/ticks, observable next call 0x542280, target/Unit and action, plus identical replacement-engine outcomes. No original game run.
Recovery inherited: 03H report UNKNOWN, 07H four core files missing, 10/25 original and 54-byte mismatch OPEN, old safety HOLD21. Do not inspect previously denied 0x5710C0..0x571500 or 0x5769B0 XREF. No MASTER/other-lane/knowledge edits.
Next safe inspection: search +0x50 constructor/default initializer, verify 0x527344 gate in caller 0x5271A0, follow +0x50 value past 0x542280 to 0x528DB0/0x569730; T011 summon/EXP, T012 damage/heal/status, T013 final targeting, T024 other AI, T028 morale remain P0.
