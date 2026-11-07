# B-20261015-1715-01｜T012/T013 kind4 57F190のsentinel時+294距離gateとcache座標fallback
[OWNER/CLASS] 2026-10-15 17時台JST、T012 primary/T013 crossref。既存保存x86に限定したSTATIC caller CFG/branch dataflow。原作Gameplay PASS0・新旧strict MATCH0・Task DONE+0。B限定READY候補。
[SOURCE/HASH] exe/T013_SKILL_HANDLERS_BOUNDED_NATIVE_20261013.txt 内 0x57F190..0x57F4C7。元EXE SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。新規EXE/REA/Ghidra解析・原本実行なし。
[PREEXISTING] 57F190 kind4入口、Unit+1E570とSkill+298先行gate、Skill+278 MP、Skill+210 cooldown、54E7B0 effect は既T013_WORK_SKILL_HANDLERS_BOUNDARY_20261013.md と B-20261013-0151-03。これらを再READYにしない。
[FACT GUARD] 57F2B8 LEA EAX,[ESP+20]→57F2C6 CALL 576E80。57F2CB Skill+294を[ESP+10]へ保持。57F2D5/57F2D7で+294=0なら57F32Eへ、非zeroでも57F2D9で[ESP+20]!=0x80000008なら57F32Eへ。
[FACT TARGET REQUIREMENT] 上記双方に該当せず「+294非zero かつ [ESP+20]==sentinel」の場合のみ、57F2E3がUnit+1E574を確認し、nullなら57F2EB→57F1AC AL0 ret4。非nullなら57F2F1..57F310でUnit中心/対象中心とZ差の二乗和を作成。
[FACT NUMERIC] 57F314 FILD distanceSquared→57F318 CALL 5E3B70→57F31D FILD Skill+294→57F321 FCOMPP→57F323 FNSTSW AX→57F325 TEST AH,5→57F328 JNP AL0。順序付きx87値ならSkill+294が変換後距離より小さい場合にAL0となる構造。5E3B70の正確な返値・x87非有限値・CW/roundingはVERIFYであり単純sqrtと断定しない。
[FACT AFTER DEBIT] 57F366..57F36CでUnit+94からSkill+278減算。続く57F372..57F3C3は元[ESP+20]がsentinel以外ならbuffer座標を使用。sentinel時は57F393..57F3A4でSkill+294非zeroかつUnit+1E574非nullの条件が揃えば、57F3A6..57F3BFでcache対象の(+40,+48)中心と+4Cを座標localへ代入。それ以外は初期sentinelを保持。
[BOUNDARY] 同関数内で「MP前に限られた距離/target gate」「MP後の候補座標fallback」が異なる段。57F3C3のSkill+254 virtual判定と57F46DのSkill+74による54E7B0/他経路選択までの全副作用、call576E80 actual outputと対象の生存はVERIFY。+1E570/+1E574/+1E580は同一視しない。
[NEGATIVE CROSSCHECK] 既REA保存run_20261009T175957025Z_576E30_{info,pseudo,assembly}.json の関数範囲は0x576E30..0x576E77。今回のCALL先0x576E80とは別関数で、その擬似コードを576E80 writerとして流用不可。
[DELTA] 既B-20261015-1611-01はkind2 57EB40のsentinelと同一frame alias、既B-20261015-0110-01はtarget cache consumer。今回は独立kind4 57F190の「+294かつsentinelに限るpre-debit距離gate」と「post-debit cache座標代入」の順序だけを新単位とする。
[REIMPLEMENT] kind4 receiptにSkill+294、first576E80 buffer/sentinel、selected cache+1E574、distanceSquared/5E3B70 return/x87 compare、pre-debit reject、post-debit fallback coordinates、MP debit PC、later +254/+74 effect PCを別々に保存。未知calleeを正常成功と仮定しない。
[GOLDEN] 合法kind4技能の+294=0/正、方向buffer valid/sentinel、cache有無・境界近傍・MP cost±1を原作と新側の同SAVE SHA/seed/inputで可視Unit生成/効果/HP/MP/対象/次tick比較（DESIGNED_NOT_RUN）。内部sentinelやx87だけではINELIGIBLE。旧Gameplay actual PASS0/new-old strict MATCH0。
[VERIFY/NEXT] 576E80書込と正常return、5E3B70意味、Skill+294実効parser、kind4合法可達、後続54E7B0/54F720 effect、T012 +A18/+A1C/latch/4E7ED0、T013最終target優先、T011クロス種はOPEN。
[READY GATE] detail+T012+T013+LANE_B_HANDOFF 4点別々にID/VA/VERIFY/PASS0を読み戻してから限定STATIC READY。MASTER cp152と正式件数の変更はEのみ、既拒否IDはNOT READYのまま。原本/他lane/REA/dev_lab/Work/WRQ/Git/push/設定/automation変更なし。
