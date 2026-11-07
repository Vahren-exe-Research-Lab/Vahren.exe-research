# B-20261016-1313-01｜T028/T011 Web姉貴本編とランシナのUnit・Class・死亡イベント原文連結
[DATE/OWNER] 2026-10-16 13時台JST。T028 primary/T011 xref。STATIC SOURCE限定。旧原作Gameplay Golden PASS0、新旧strict MATCH0、Task DONE+0。
[MASTER/DEDUP] E checkpoint162公式559(A115/B194/C134/D116)。B-20261016-1210-01の36 event分類とweb/web_rのaddLimit差はE統合済みで再加算しない。
[SOURCE 1] 正規化原作10_ユニット/B_1_クレイジーサイコレズ.dat の unit boss_web:base1 は class=c_boss_web と dead_event=boss_web_demoralization を直接宣言（death参照 L211）。同ファイルのclass c_boss_web:a01a はchange=c_boss_web_2*15、c_boss_web_2:a01a2 はchange=c_boss_web_3*25、c_boss_web_3:a01a3 は別親宣言。
[SOURCE 2] 正規化原作5000_ランダムシナリオ/RB_ボス人材.dat L211-226 の unit boss_web_r:boss_web は class=c_boss_web_r と dead_event=boss_web_r_demoralization（L225）を自身で宣言。親Unitが本編名であっても自身のraw dead_eventは別名。
[SOURCE 3] 同ファイルL228以降のclass c_boss_web_r:c_boss_web →change=c_boss_web_r2*15、c_boss_web_r2:c_boss_web_2 →change=c_boss_web_r3*25、c_boss_web_r3:c_boss_web_3。二つの派生の親は本編各段のClassであり、ランシナClass1→2→3のchange辺とは異なる。
[EVENT REF] 正規化50_その他新システム/siki_ボス側近.dat L90-111 の boss_web_demoralization はpushRank(boss_web)・rank direct skillTroop・条件付きaddLimit(514)。L237-245 の boss_web_r_demoralization はpushRank(boss_web_r)・setv(@commander,boss_web_r)・routine(base_demoralization)。siki.dat L536-548のbaseはskillTroop(@commander,...)。body差そのものは既存B-1210-01へ参照。
[NEW SCOPE] 新しいのは2つのUnit raw dead_event指定、Unit親辺、本編/ランシナの対応Class親辺とchange辺、両event bodyの参照先を同じ宣言グラフに結合した点。既T011 cross-kind一般則 B-20261013-2018-71も再採番しない。
[EXE/XREF] T028既保存共通死亡path VA0x5789F2→0x4321B0を参照。個別Unitの実event field writer/dispatch、Class/Unit親resolver・実changeの新native解析は実施しない。
[FACT/VERIFY] 宣言文字列と原文親・変更先・個別dead_event存在はCONFIRMED SOURCE。実効継承の上書き/属性順、Unit+0x1861C effective field、Rank・合法旧battle dispatch・士気/limit効果、原作の別eventはVERIFY。原作BUG・実発火・効果成功を断定しない。
[REIMPLEMENT] unitParent/classParent/classChangeTarget/rawDeadEvent/resolvedDeadEvent/eventBodyを独立stageとし、boss_web_rのrawイベントを親boss_webの本編イベントへ勝手に潰さない。
[GOLDEN] 合法原作本編boss_webとランシナboss_web_rについて、旧new同SAVE SHA/seed/入力で実Unit/Class、死亡前後rank0/2/4・chuboss_alc有無・可視士気/limit/dialog/HP/MP/次tickを比較。旧captureなしDESIGNED_NOT_RUN、内部IDだけはINELIGIBLE。旧Gameplay PASS0/strict0。
[FILES/GATE] detail、本B owner T028_MORALE.md、B xref T011_DATA_MODEL.md、B HANDOFFの4点保存・独立readback成功時だけ B限定SOURCE READY。EのみMASTER/T018正式統合、同時加算しない。
[LOAD/SAFETY/NEXT] Local sessions0、CPU実率不明。原本ZIP/EXE/SAVE、他レーン、REA/dev_lab/Work/WRQ、Git/Remote、設定・automation不変更。重い逆解析・禁止VA新規取得0。次はT012最終弾/HP/MP、T013順位、T011継承実効を優先。
