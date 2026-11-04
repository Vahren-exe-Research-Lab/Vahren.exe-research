# B-20261019-0117-01｜T012主・T013参照：既保存damage caller別context+0x0Eとflash補助ゲート
[DATE/OWNER] 2026-10-19 01時台 JST、B/T012 primary・T013 reference。新規EXE逆解析は行わず、既保存x86の異なるcallerを静的相互照合。
[TARGET] 同梱原作Vahren.exe既保存SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。原本実行・書換0。
[SAVED EVIDENCE] exe/T012_DAMAGE_CALLER_CONTEXTS.txt（計1045行）、exe/T012_DAMAGE_CORE_DUMP.txt（583行）、exe/T012_FLASH_DAMAGE_WRAPPER_576F10_NATIVE_20261013.txt。いずれも既保存解析資料、対象原本からの新しい抽出無し。
[E=0 GROUP 1] VA0x546B1A..0x546B53：Unit+0x7C hit contextにUnit/Skillを書き、0x546B31でbyte[ctx+0x0E]=0、0x546B53で条件付きCALL 0x550E70。
[E=0 GROUP 2] VA0x546DA6..0x546DDF：Unit+0x7C contextを構築、0x546DC1でbyte[ctx+0x0E]=0、Skill+0x24C>=0かつ+0x27C!=0なら0x546DDFでCALL 0x550E70。
[E=0 PRE] 同callerの0x546D46でUnit+0x18688方向更新、0x546D52でUnit+0x94からSkill+0x278を減算、0x546D5FでUnit+0x1868C=0。これらは命中・HP効果保証でない。
[E=0 PRIOR ALREADY KNOWN] 特殊missile allfunc VA0x547F3F..0x547F60は0x547F5Cでctx+0x0E=0（T012既§28で既知）。本IDで単独新規計上しない。
[E=1 GROUP 1] VA0x57E3FB..0x57E43A：Unit+0x7C contextを構築、0x57E416でbyte[ctx+0x0E]=1、Skill+0x24C/+0x27C条件成立時0x57E43AでCALL 0x550E70。
[E=1 GROUP 2] VA0x57E7A5..0x57E7E0：Unit+0x7C contextを構築、0x57E7BAでbyte[ctx+0x0E]=1、条件成立時0x57E7E0でCALL 0x550E70。
[E=1 PRE] VA0x57E74D Unit+0x18688方向store→0x57E759 MP減算→0x57E75F Unit+0x1868C=0。+0x74>1では追加state書込の可能性。illusion gate時0x57E7EAへ逸れるため常時damage coreに到達しない。
[UNKNOWN GROUP] VA0x54DAFEもCALL 0x550E70だが既保存窓の0x54DAFAは[esi+0x78] contextを渡すだけで、+0x0E setter/valueを当該窓から確定できない。E=0/1へ分類禁止。
[COMMON CALLEE] 保存core VA0x55116Eでbyte[context+0x0E]を検査し0なら0x55119Bへskip。1かつSkill+0x248>0なら0x551196でCALL 0x576F10（局所分岐、到達時のみ）。
[WRAPPER BOUNDARY] 保存0x576F10はUnit+0x1867C==0かつUnit+0x8D==0を別途要求し、+0x185F8 ring更新を経て0x576F57 CALL 0x4DFBB0。ctx E=1だけでflash実作用/可視変化を証明しない。
[NEW DELTA] 既T012§28のallfunc E=0と既§92のcommon core E-gate単体では未接続だった、複数callerのE=0対E=1と方向/MP前処理の組を同一VA資料から限定STATICに結合。既B midnightのMP/AL stage監査を新規再計上しない。
[FACT VS VERIFY] 確定は保存済callerにおけるcontext byte値と条件付きCALL関係のみ。同一target/Skill identityのruntime到達、0x550E70正常帰還、+0x248 effective、flash登録の副作用、HP変化・命中・RNG・次tickはVERIFY。
[REIMPLEMENT] DamageContext.eventFlag(+0x0E)をcaller別明示入力として保持。normal kind1/AI/missile allfuncの名称だけでflagを一律決定せず、damage result・flash wrapper eligibility・MP debit/方向更新・target filterを段階別に記録。
[GOLDEN] 合法旧原作で該当caller/技能・flag差を観測可能なときだけold/new同EXE/DAT/SAVE/map/input/capture SHA・seed可否・Unit/Skill/target・発射/HP/MP/状態・次tickを比較。内部flagしか見えない条件はINELIGIBLE。DESIGNED_NOT_RUN。原作Gameplay PASS0、新旧strict MATCH0。
[DEDUP/BLOCKED] MASTER cp187正式584(A115/B217/C136/D116)へB側書込・加算0。B-20261018-1813-01はowner NOT READY、E2053(B2021x2)/E2145(B2109)正式拒否別BLOCKED。拒否済VA0x5710C0..0x571500等を逆解析・迂回しない。
[READY GATE] 本detail＋data/T012_BATTLE_CALC.md＋data/T013_AI.md＋evidence/LANE_B_HANDOFF.mdに同ID追記し個別4/4読み戻し後のみB LIMITED STATIC SAVED-NATIVE CROSSJOIN READY。E正式統合PENDING。Task DONE増0。
