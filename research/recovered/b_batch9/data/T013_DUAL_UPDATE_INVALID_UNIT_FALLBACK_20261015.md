# B-20261015-0409-01｜T013/T012 二つの通常AI更新入口と invalid Unit 後処理の同一callee（限定STATIC）
[OWNER/STATUS] T013 primary／T012 reference。既存B-20261015-0321-01の後続だけを独立照合。B OWNER READY CANDIDATE、3資料＋HANDOFFの読戻し後のみBOUNDED READY。実機原作Gameplay PASS0／新旧strict MATCH0／Task DONE+0。
[ORIGIN] 迫真戦記ver0.67対応保存Vahren.exe SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。B所有exe/T012_ACTION_KNOCK_ORDER.txt／exe/T013_SEARCH_CALLERS.txtの保存済x86のみLocal read-only利用。原本実行・新逆解析なし。
[ROUTE FIRST] VA0x545B42 search 57B870→0x545B47 call57DBB0→0x545B4C/4E AL非0なら直ちに0x545CB5 epilogue。AL=0時は0x545B54 Unit+1867E!=0 又は0x545B60 signed Unit+D4<0で0x545C9Fへ。
[FIRST INVALID] VA0x545C9F push 0／0x545CA1 push ESI(Unit)／0x545CA2 call57D8B0。0x545CA7/CA9戻りAL!=0なら0x545CB5へ直行。AL=0なら0x545CAB call57C600→0x545CB0 call57DF90→0x545CB5 epilogue。
[ROUTE SECOND] VA0x57AFC2 search57B870→0x57AFC9 call57DBB0→0x57AFCE/D0 AL非0なら0x57B36E epilogue。AL=0かつ0x57AFD6 Unit+1867E!=0 又は0x57AFE2 signed Unit+D4<0で0x57B358へ。
[SECOND INVALID] VA0x57B358 push 0／0x57B35A push EBP(Unit)／0x57B35B call57D8B0。0x57B360/362戻りAL!=0なら0x57B36Eへ直行。AL=0なら0x57B364 call57C600→0x57B369 call57DF90→0x57B36E epilogue。
[FACT] 保存命令上は2つの異なるtick callerで「search→57DBB0のAL判定→Unit不適格枝→57D8B0(Unit,0)の第2AL判定→第2AL=0のみ57C600/57DF90」という対応が成立。57DBB0のAL≠0早期帰還では、この局所invalid枝の57D8B0/2callをスキップする。
[SCOPE/DEDUP] 旧B-20261015-0321-01の2caller search/57DBB0接続、B-20261013-0023-01のsecond通常更新と、既T012 0x545C4B/0x57B30Dの1E530回復gateは再採番しない。新増分は両caller invalid枝の57D8B0第2ALと可視でない後処理2callの分岐対応のみ。
[VERIFY] 57D8B0／57C600／57DF90の副作用・内部receiver/戻値のゲーム意味、ESI/EBPの実合法Unit種、57DBB0 virtualの追加副作用、HP/MP/target/RNG/投射/次Unitは未確定。両callerが同時tickで実行されるとは断定しない。第2ALは成功shot/命中を意味しない。
[REIMPLEMENT] caller first/second、57DBB0 AL、Unit+1867E／signed +D4、57D8B0(Unit,0) AL、57C600/57DF90呼出実有無、returnPC、選択target・HP/MP/RNG cursorを別receiptとし、早期帰還で無条件cleanupを流さない。
[GOLDEN] 合法未改変原作と新実装の同SAVE SHA／seed／Unit/Skill/配置/入力で対象有無・HP割合・不適格Unit状態・後続の可視移動/射撃/HP/MP・次tickを照合する設計のみ。old capture無しDESIGNED/NOT RUN、内部ALのみはINELIGIBLE、original Gameplay PASS0／new-old strict MATCH0。
[NEXT] 57D8B0の既保存合法参照と両calleeのUnit alias・副作用を、禁止範囲へ新規逆解析せず確認。T012 Skill+A18/A1C・Unit+1E560/+18688・4E7ED0とMP/攻撃結果、T013優先順位、T011親解決は引続きVERIFY。
[SAFETY] 原本ZIP/EXE/SAVE、MASTER/T018/他レーン/REA/dev_lab/Work/WRQ/Git/push/Remote/設定/automation書込0。安全拒否済0x5710C0..571500／B過去拒否詳細を再提出・迂回しない。PC CPU実率n/a、重量処理0。