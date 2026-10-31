# Script grammar, command VM, context and timing — curated A/T005–T010

Target: Hakushin ver0.67 original PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187. Original-script/native x86 clauses STATIC, proposed implementation INFERRED, unobserved runtime effects VERIFY. Original gameplay Golden PASS=0, strict MATCH=0.
Authoritative owners: data/T005_FORMAL_GRAMMAR.md, exe/T006_TARGET_DISPATCH.md, data/T009_CONTEXT_MODEL.md and data/T010_EVENT_SCHEDULER.md. Check their correction history, not early checkpoint text in isolation.

## 1. Grammar and variant lookup (T005)
- ver0.67 has 590 script DATs, normally CP932; named structures with one parent, if/rif/while, battle blocks, line/block comments and context-sensitive semicolon handling. Switch/case/foreach/default have no use in this target corpus; later-language features are not automatically compatible.
- Expressions rank multiplication/division before addition/subtraction before comparisons, AND before OR. An @ prefix may mean a string variable; a standalone @ as a property is explicitly present but null/suppressing. Keep these separate in the AST.
- Generic scenario-qualified property lookup checks qualified child→ancestor keys before unqualified child→ancestor keys; ancestral member@rsc=@ can conditionally suppress ordinary child member. Specialized list/member reader behavior remains VERIFY.
- Duplicate assignments depend on key and parser: generic property insert-if-absent vs special/list callbacks that may clear/rebuild/merge. The independent 2017 parser's overwrite semantics do not establish ver0.67 behavior.
- Source: data/T005_FORMAL_GRAMMAR.md, grammar, explicit-null, inheritance and callback crosswalk. Any earlier denied owner HANDOFF edit remains BLOCKED and is not re-submitted here.

## 2. Command dispatch and stateful execution (T006/T010)
- Registry maps event/call to opcode0, routine to opcode1, save7, wait9, battleEvent10. Missing registry command leaves sentinel 0x80000008 and runtime cleanup/return: source typos chat3/eras/fafeout are ignored, not automatically corrected or syntax-fatal.
- event/call and routine invoke common native 0x4321B0 using different flags/return conventions and scene-dependent event markers; cannot collapse AST operations. wait stores counter at engine+0x1EED58 and resumes per interpreter pass; it is not OS sleep.
- battleEvent schedules active ScriptIF roots: normal if removed after first true, rif remains active, root false does not run else. Distinct from ordinary scene-event invocation.
- Battle clocks: getTime uses resettable +0x1EED60, isInterval uses absolute +0x1EED64, getLimit uses independent 10-tick cadence. resetTime clears only the former; native isInterval(n>0) rounds n to 10*ceil(n/10). Actual per-scene display/tick outcomes remain VERIFY.

## 3. Original context defaults, duplicate precedence and corrected clamps (T009)
- Normalized context.dat SHA256 C87F523F8B3DC41112132B48917FFAE2E2435B30EAB61EC87C96679CDA7B3547, 204 active assignments / 203 unique keys. battle_fast first on at line42 and later off at line83. Original generic target parser uses insert-if-absent, so effective loaded battle_fast=ON, while hardcoded fallback=off. The earlier 2017-parser “last wins/off” conclusion was superseded.
- Runtime context conversion varies by key: some values are raw integers, some are multiplied by 0.01, zero may be a preserve-default sentinel, and some scale is applied by the later consumer rather than at parser initialization. Model raw assignment, compiled result and consumer-time value separately.
- IMPORTANT ERRATUM: older T009 checkpoint32 said no initial capacity24 clamp at an early write site. Later checkpoint33 found 0x45C4EA..0x45C509 post-override MAX24 for scenario spot_capacity and war_capacity, with no minimum clamp on negative signed values. support_range/my_range/myhelp_range get MIN1. Spot-specific capacity zero falls back to scenario value before MAX24, and negative Spot.capacity can remain negative.
- Target hardcoded fallback values differ from newer Vahren701 and independent 2017 code (e.g. employ_range target1 vs independent2, btl_unitmax target500 vs independent300). Do not import newer defaults into ver0.67. Source: data/T009_CONTEXT_MODEL.md, native fallback/typed consumer sections and checkpoint33 correction.
- REIMPLEMENT/VERIFY: execute duplicate resolution per key, then typed compile and late normalization; identify actual legal scene state and downstream negative-value behavior before Golden. Old game gameplay PASS0, strict MATCH0.
