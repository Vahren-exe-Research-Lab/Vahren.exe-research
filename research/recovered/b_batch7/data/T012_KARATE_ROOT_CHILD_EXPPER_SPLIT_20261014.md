# B-20261014-1517-01｜T012/T011: 迫真空手rootとnext3子技能のexp_per異種指定
[DATE/OWNER/STATUS] 2026-10-14 15:17 JST。T012 primary、T011技能宣言・T013 child経路参照。新規STATIC原文×既存B保存nativeの限定crosswalk。実戦/実効Skill/実EXPはVERIFY、旧原作Gameplay actual PASS0・新strict MATCH0・Task DONE+0。
[SOURCE PATH] data/normalized/hakushin067_core/a_default/script/30_スキル/F11_sword.dat（原作ver0.67 COREの読み取り専用正規化コピー）。
[ROOT1] 1-based L1124-1142 skill sw_karate1:zan1 は exp_per = off (L1136)、just_next = sw_karate_js_joi (L1138)、pair_next = karate_pr0 (L1131) を直接宣言。
[ROOT0] L1188-1202 skill sw_karate0:sk_sw0 は exp_per = off (L1199)、next = sw_karate_js_joi (L1200)、pair_next = karate_pr0 (L1195) を直接宣言。
[JOINT] L1203-1219 sw_karate_js_joi.next3=sw_karate_js_joi2 (L1212)→joi2.next3=sw_karate_js,sw_karate_jsb,sw_karate_js2 (L1218)。二rootと3子グラフは既登録B-20261014-1017-01の事実であり、今回の新件数には再計上しない。
[CHILD-DIRECT] L1225-1242 skill sw_karate_js は func=missile (L1234)、collision=none (L1228)、damage=-3 (L1232)、exp_per=65 (L1241) を直接宣言。直接のroot offとは異なる数値指定である。
[CHILD-ANOTHER] L1243-1257 sw_karate_jsb:sw_karate_js と sw_karate_js2:sw_karate_js は明示親を持ち、自身の節にはexp_perの直接指定が無い。ただし親のexp_per=65を実際に継承するかはVERIFY。jsbはattr=sw/str=attack*100/next=punch_hit、js2はattr=msw/str=magic*10（既B1017、再採番なし）。
[PRIOR NATIVE VA] B所有exe/T011_STRUCTURE_DISPATCH_PROBE.txt と T012_BATTLE_CALC.md§78-81：parser VA0x59BDC8 off literal 0x624D00 比較、0x59BDFB fld qword[0x63B290]=-123456.0→0x59BE05 Skill+0x2A8書込。on枝0x59BE29..2Bは1.0、numeric枝0x59BE33..56は整数×double[0x63B070]=0.01。ここでは保存済み命令を参照しただけで新EXE逆解析なし。
[CONDITIONAL COMPILATION] 各節の原文exp_perが通常Skill property compilerの実効値に採用されるなら、両rootのSkill+0x2A8は-123456.0、直接子sw_karate_jsは65×0.01=0.65（IEEE754 double丸め込み）。子jsb/js2実効値・root/childのPointer作成順/派生dispatchは未実証。
[CONSUMER/RESULT] B既存T012§59/75/77-81の0x551E50 hit-side helperにはSkill+0x2A8 sentinel=-123456.0の早期exit gateがある。上記原文とnative consumerを直結できるのは条件付き予測のみ。child collision=none・damage=-3のため命中/EXP付与の保証は全くなく、EXP-like linked+0x16Cの可視意味もVERIFY。
[NEW DELTA] 既B1017は攻撃子3本のattr/damage、B079/080は汎用exp_per parserを確定済み。今回初めて**同一空手宣言next-chainの2root off vs 直接子65**を横断し、rootのEXP設定を攻撃family全体へ一律伝播する誤実装を防ぐ。MASTER/B HANDOFF/T011/T012全文で空手×exp_perの同一明記をread-only照合し重複発見0（意図的に汎用規則を再READY化しない）。
[REIMPLEMENT] 各Skillノードのraw propertyとeffective +0x2A8を個別保持し、runtime child factory/jobに実使用Skill pointer、hit context+D、HP virtual結果、0x551E50呼出/早期gate、linked+0x16C変化、MP、RNGを別receiptに残す。raw root offを子に機械的コピーせず、逆に子65をrootへ拡張しない。
[GOLDEN-DESIGNED/NOT RUN] 合法原作/許可済controlled DATで技能実所持・root0/1起動を先に確認し、同じ旧SAVE/SHA/seed/入力でroot本体、joi/joi2、子js/jsb/js2の可視発射とtarget HP、caster MP、可視EXP/Level・次RNG/行動を新旧比較。内部Skill+2A8だけならINELIGIBLE。controlled DAT観測は未改変本家Goldenと区別。
[VERIFY/NEXT] typed inheritance/@解決、jsb/js2 exp_per effective、collision=noneの実作用、0x551E50 hit-side合法経路、EXP進行の確定意味、原作実機PASS/新strict MATCH、T012 MP fallback/+1E560 latch/4E7ED0・T013 target優先を継続。Eのみ正式MASTER/T018登録。
[SAFETY] 原本ZIP/EXE/SAVの変更・起動0。新REA/Ghidra/重いプロセス0。過去安全拒否VAやB-0317書込の経路迂回・再提出0。MASTER/T018・他owner・REA/dev_lab/Work/WRQ/Git/push/Remote/設定/automation編集0。CPU率n/aでPC低負荷の断定なし。
[STATUS] OWNER DETAIL SAVED-CANDIDATE; T012/HANDOFF登録＋3箇所readback前はNOT FORMALLY READY。