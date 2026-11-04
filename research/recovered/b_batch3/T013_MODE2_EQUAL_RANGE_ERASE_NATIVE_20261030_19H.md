# B-20261030-19H-T013-EQUAL-RANGE-ERASE-01 | 2026-10-30 19H JST | T013 mode2 2系統の等値キー範囲検索・消去
STATUS: STATIC / INFERRED / VERIFY / NOT READY。原作Gameplay Golden PASS 0、strict MATCH 0、B新正式READY 0、E MASTER統合 0、DONE 0。
[SOURCE] Desktop Commander Local Compact ONLINE。読み取り専用原作解析コピー rea_lab/targets/hakushin067_Vahren.exe 2910720B、実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
[INDEX] 統合V9 SQLite HAKUSHIN067_UNIFIED_V9_20261023.sqlite 141033472B、実SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、SQLite immutable mode read-only quick_check=ok。既存標準V3無変更。
[PRECHECK] MASTER E旧正式checkpoint196/READY596を旧記録として参照、ANALYSIS_LANES_PROTOCOL・B所有5タスク・LANE_B_HANDOFF・共通復旧ハブ・18H detailを読取。先行18H保存3/3/readback3/3、11H要約3件の安全拒否BLOCKED、SAFE134/HOLD21・Library byte差54件・10/25原文は未回収のまま。原本/gameplay/重いGhidra再解析なし、active.lock 3候補なし、java/Ghidraプロセスなし（pythonw.exe 1件あり）。
[NEW FUNCTION ABI] V9 pseudoc 0x579AA0（118B、verified_abi=0）を原作x86 ASMで照合。0x579AA2 EBP=[ESP+0xC]は木、0x579AB6 EDI=[EAX]はレジスタEAXで渡すkey pointer参照、0x579AB8/0x579AF3 はnode+0x0Cとの符号なし比較。
[NEW RESULT] 0x579B07 MOV EAX,[ESP+0x14]は出力先を取得、0x579B0D MOV [EAX],EBX、0x579B0F MOV [EAX+4],EDX の2つのiteratorを書き込み、0x579B13 RET 8。直接E8 outgoing call 0。**木への登録ではなく、同じkeyに対応する境界ペアを探すread-only検索（出力先2wordの更新だけ）**。
[CALLSITE A] 0x44C37Fは距離木node+0x18 payloadを[ESP+0x18]へ保存。0x44C3D2 LEA EAX,[ESP+0x20]は直前2PUSHによる+8 stack shiftでそのpayloadを指すkey pointerとなる。0x44C3CC push outpair/0x44C3D1 push tree→0x44C3D6 CALL0x579AA0（V9 PE-verified E8）。
[ERASE A] 0x44C3DB/DFは2word境界を取得し0x44C3E3/E4 PUSH、0x44C3E5 ESI=out iterator、0x44C3E9 EAX=同じlocal tree、0x44C3ED CALL0x510850。木から該当key範囲を削除する流れ。既知0x5690C0のUnit条件gateの**後**に実行する。
[CALLSITE B] 0x44C4A0は距離木node+0x18 payloadをEDIへ取得、0x44C4A9で[ESP+0x28]へ保存。0x44C550 LEA EAX,[ESP+0x30]は2PUSH後の同payloadのkey pointer、0x44C54A/B push outpair/tree→0x44C554 CALL0x579AA0（V9 PE-verified E8）。
[ERASE B] 0x44C559/55Dで2word境界取得、0x44C561/562 PUSH、0x44C563 ESI=out iterator、0x44C567 EAX=同じlocal tree、0x44C56B CALL0x510850。0x44C570は戻り後local [ESP+0x3C]を判定しゼロなら0x44C57F→0x56F130へ向かう別枝（意味/所有権VERIFY）。
[RANGE-CLEAR BOUNDARY] 既知0x510850の0x51085F/863の2条件が全域一致なら0x510867→0x44D0D0 full clear、それ以外に0x51087A..0x5108DF→0x510C20 partial erase。09H 0x5AC611 callerとは異なり本2callerはkey検索結果を渡すため全域/部分の双方を想定し、常時fullとは断言しない。
[NEW DELTA] 17Hの2段shuffle、18Hの0x5690C0 gate・0x579AA0 E8呼出位置そのものは既知で新規計数0。今回は**0x579AA0 native ABI/unsigned-key検索と2word出力、caller2件のkey provenance、0x510850消去への結合、先行『候補登録』という役割の誤解訂正**を独立追加。
[PROOF] 原PE capstone x86 native window SHA256: 0x579AA0+118B=88E3A96E339A1FC2BA4FC4F8559EA41FF862D6FC6884EDA71464BBC10097AD88; 0x44C310+249B=497E6A8465F49BBE6465BFD4F9112E1E0D9029327DBE078E29443A78D1C9B59D; 0x44C42E+354B=7A9F01E76357FDCE9A82D9E372C288547E0C5769D1BCDE95DEC770C3DEEABE69; 0x510850+155B=9597FAE366EDF0313210225A8454747A24021CA4E0B831AEF393502BC7E4E943。
[DEDUP] B所有T011/T012/T013/T024/T028のdata/exe Markdown＋B HANDOFF計389件をread-only照合し、新址0x579B0D/0x579AB8/0x44C3ED/0x44C56B/0x44C570/0x44C3D2と本研究IDは先行literal 0。10月25日欠落全文/他lane含む完全意味的重複はVERIFY。
[KNOWN LIMIT] keyの構造体/Unit実体、treeの多重キー可否、erase後のiterators/残存候補、0x56F130の副作用、malloc/free所有権、最終対象Unit・モードとRNG接続は静的のみ。native ABIをhook prototype確定に使わない。
[GOLDEN] 無改変原作EXEと20倍テスト改変前DATを使用し、同一合法SAVE/MAP/入力/RNG条件でmode2 candidate 0/1/複数、同key/異key混在、2木の前後サイズ・pair境界・削除量・+0x48/target・翌tickの動作を測る。DESIGNED_NOT_RUN。
[RECOVERY] 今回OTHER=誤名T011 owner ENOENT、PowerShell -c引用符エラー、Python raw string末尾backslash SyntaxErrorを正規の読取操作で修正済み。安全拒否0・既拒否された本文/命令/VAの再提出・迂回0。11H拒否3要約はBLOCKEDを維持し本runで再提出しない。
[NEXT] 0x44C570→0x56F130の枝とB段残木処理、0x579AA0同key範囲境界、0x510850後のtarget更新を優先。T011召喚/EXP、T012 damage、T024通常AI、T028士気は未解明P0で継続。
[SCOPE] B所有 data/T013の詳細・担当owner・LANE_B_HANDOFF以外への書込禁止、MASTER/他lane/REA/dev_lab/原本/Git/Work/設定/automationには書かない。