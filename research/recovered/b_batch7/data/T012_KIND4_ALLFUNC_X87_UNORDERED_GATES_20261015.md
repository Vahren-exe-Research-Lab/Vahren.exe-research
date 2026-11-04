# B-20261015-1817-01｜T012/T013 x87 range compare の unordered 境界（限定STATIC）
[DATE/OWNER] 2026-10-15 18時台JST、T012 primary/T013 crossref。既保存EXE disassemblyとx87条件コードのみ。原作Gameplay actual PASS0 / strict MATCH0 / Task DONE+0。
[EXE] 原作対応SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187（既保存資料記載値）。原本EXE/ZIPの実行・変更、新規逆解析なし。
[SOURCE-A] B保存exe/T012_ALLFUNC_FLOW_PROBE.txt VA0x54708D FILD squared→0x547091 CALL 5E3B70→0x547096 FILD Skill+294→0x54709C FCOMP ST(1)→0x54709E FNSTSW AX→0x5470A0 TEST AH,05h→0x5470A3 JNP fail(0x54747E)。続いて0x5470A9 FILD Skill+298→0x5470AF FCOMPP→0x5470B1 FNSTSW AX→0x5470B3 TEST AH,41h→0x5470B6 JE fail(0x547480)。
[SOURCE-B] B保存exe/T013_SKILL_HANDLERS_BOUNDED_NATIVE_20261013.txt VA0x57F314 FILD d²→0x57F318 CALL 5E3B70→0x57F31D FILD Skill+294→0x57F321 FCOMPP→0x57F323 FNSTSW AX→0x57F325 TEST AH,05h→0x57F328 JNP AL0(0x57F1AC)。この枝に入る上流の+294!=0、stack sentinel、selected cache非nullは既B-20261015-1715-01。
[CPU-SEMANTICS] x87 FCOM(PP)結果の C0=AH.bit0、C2=AH.bit2、C3=AH.bit6。ordered lhs<rhsは C0/C2/C3=1/0/0、lhs=rhsは0/0/1、lhs>rhsは0/0/0、unorderedは1/1/1。
[TRUTH-UPPER] TEST AH,05h の結果（lhs=Skill+294 vs rhs=5E3B70後のST値）は less:01h→parity odd→JNP taken（fail）、equal:00h→not taken、greater:00h→not taken、unordered:05h→parity even→not taken。したがって枝の局所判定は**ordered check<computedValueのみreject**。NaN/UNORDEREDが実際に発生・復帰するとは断定しない。
[TRUTH-LOWER] allfuncのTEST AH,41h; JEは（lhs=Skill+298 vs rhs=同ST値）ordered lhs>rhsの場合のみmask=00hでreject。ordered less:01h、equal:40h、unordered:41hはJE不成立。従ってこの二つの比較だけなら unordered は両gateを素通りする（x87例外がマスクされて比較が完了した場合に限る）。
[STACK-GRAIN] allfunc初回 FCOMP ST(1) は比較後ST0を1個popして距離候補ST値を残し、次の FILD+FCOMPP で2個pop。kind4側はFCOMPPで2個popして後段へ。実際の5E3B70 return、FPU CW例外マスク/丸め、外側x87状態全履歴はVERIFY。
[DELTA-DEDUP] 既T012§34の有限数上限/下限 inclusive、B-20261015-1715-01のkind4前後MP/cache分岐は再計上しない。本IDは両callerのx87 TEST/JNP/JEについて**unorderedの条件成立表とスタックpop差**を追加した限定CPU分岐証拠1件。
[REIMPLEMENT] 比較を単純な「NaNならfalse」predicateへ無条件置換しない。ただしx87例外/NaN到達を原作成功として偽装しない。段階別に raw int d²、5E3B70 return、CW/NaN/ordered flag、upper/lower gate、MP以前のreject、後続callPCを区別する。
[VERIFY] 5E3B70実数値/呼出ABI、入力d²の符号付きoverflow後の実挙動、NaN生成・mask/no-mask、合法原作戦闘での実可達性、後段発動/命中/HP/MP/RNG、strict等価性。実機PASS0。
[GOLDEN] old未改変原作を正当な別観測で可視captureできる場合のみ、同SAVE SHA/seed/inputでcheck・range_min各距離の未満/等号/超過、整数矩形中点、合法大座標の可視行動/Unit生成/HP/MP/次tickをnewと比較。内部x87 flagsだけはINELIGIBLE、DESIGNED_NOT_RUN。
[OWNERSHIP/NEXT] B data/T012_BATTLE_CALC.md、data/T013_AI.mdおよび evidence/LANE_B_HANDOFF.md へID参照・4点readback後のみ B LIMITED STATIC READY。MASTER/T018正式統合はEのみ。次回は旧証拠で576E80 writer、Skill+A18/A1C対象、4E7ED0/攻撃結果、T011継承を優先。