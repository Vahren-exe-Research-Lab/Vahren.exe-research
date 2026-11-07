# B-20261017-2114-01｜ZNMブーメラン子分岐のnext_interval・next_last・onehit宣言（T012主/T011補助）
[DATE/CLASS] 2026-10-17 21時台JST。限定STATIC ORIGINAL SOURCE × PRE-SAVED PARSER CROSSJOIN。原作Gameplay Golden actual PASS0／new-old strict MATCH0／Task DONE増0。B所有の既存root→MP heal graph B-20261017-2017-01を再計数しない。
[ORIGINAL] 正規化原作 a_default/script/31_ユニットスキル/U_1_5_マリナーズ～革命企画.dat の1-based L5044-5120。root znm_boom の next3 はnt1,nt2（L5052）。これは原文であって実際の子実行順序ではない。
[BRANCH A] skill znm_boom_nt1:sk_ms は next3=nt1_b,nt2_b（L5076）、next_last=on（L5077）。skill znm_boom_nt2:znm_boom_nt1 は next_interval=5（L5082）、next3=znm_boom_bomb1,znm_boom_bomb2（L5083）、next_last=@（L5084）を自分で明示。raw親辺・明示@は区別。
[BRANCH B] skill znm_boom_nt1_b:znm_boom_nt1→next3=znm_boom_nt3,znm_boom_nt4（L5087-5090）。nt3:nt1 はattack_us=7/onehit=on/hard=2（L5104-5106）、next=znm_boom_heal/next3=@（L5108-5109）を直接宣言。
[BRANCH C] skill znm_boom_nt4:znm_boom_nt3 は next_interval=5（L5115）、next=@（L5116）、next3=znm_boom_bomb1,znm_boom_bomb2（L5117）を明示。nt3由来のnext=healをnt4へ無条件合成しない。
[SAVED VA/XREF] 既存B-owned data/T011_NEXT_ORDER_INTERVAL_NATIVE_20261013.md：保存済0x59C3EB raw next_interval property lookup→0x59C410 CALL0x4647D0→0x59C418 MOV [compiled Skill+0x274],EAX取得field+0x20。原文の2箇所の5をnative実効Skill+274へ反映するには、有効parent/attribute/lookupとこのproducerへの到達が前提。新規逆解析や原本実行なし。
[IMPORTANT VERIFY] next_last=on/@とonehit=on/attack_us=7/hard=2のnative consumer・親継承結果・nt3とnt4の発射/帰還・5のtick/時相単位・NEXT実発火順序は未解決。+274 parser格納を即「5tick間隔」とは呼ばない。nt4はnt3を親指定するがonehit等の実効継承もVERIFY。
[NEW/DEDUP] 先行B-20261017-2017-01が記録した原文root/next3/MP healグラフは再READY加算0。今回の独立増分はnt1対nt2のnext_last明示差、nt2/nt4のnext_interval=5、nt3のhit関連宣言とnt4の別branch原文対照、既保存+274 producerへの条件付き接続だけ。
[REIMPLEMENT] Skill.raw parent、next、next3、next_interval、next_last、onehit、attack_us、hard、ExplicitNullを独立保持し、nt2とnt4が同じ間隔宣言を持つから同一効果/同一時刻と推定しない。技発動→子選択→投射/回帰→MP支払/回復→hit/HP→後段更新を別stageにする。
[GOLDEN] 合法な原作Unit znmを確認できる場合のみ同一旧EXE/DAT/SAVE/input/seed・動画時刻/各SHAを固定し、投擲前/子発射/帰還/爆発/回復・次tickで弾数/間隔/HP/MP/対象をnewと比較。子branch可視識別不可ならINELIGIBLE。旧Gameplay PASS0、strict MATCH0、DESIGNED_NOT_RUN。
[OPEN/NEXT] T012最終攻撃HP/射撃Unit+0x1E560 latch・+0x18688方向・0x4E7ED0・MP fallback、T013 target priority、T011親解決とraw next_last producer。禁止0x5710C0..0x571500/0x58021E..0x580340等新逆解析・安全拒否案件の迂回無し。
[SAFETY] 原本ZIP/EXE/SAVE、MASTER/T018、他lane・REA/dev_lab/Work/WRQ、Git/push、設定/automationへの書込・実行0。Localのみ、PC CPU率n/aで低負荷不明・重いREA/Ghidra/Java/tests未起動。
[STATE] DETAIL SAVED; T011/T012 owner＋B HANDOFF独立readbackを完了するまでNOT READY。EのみMASTER正式統合。