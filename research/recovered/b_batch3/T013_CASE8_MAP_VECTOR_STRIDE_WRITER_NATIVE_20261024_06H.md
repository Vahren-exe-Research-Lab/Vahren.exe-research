# B-20261024-0616-T013-MAP-VECTOR-STRIDE-WRITER-01｜case8 map値vectorの0x1C stride・clone・登録入口
[TASK/OWNER/STATE] B/T013主。2026-10-24 06時台 JST。STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / STATIC-DERIVED / VERIFY / NOT READY。T011/T012/T024/T028は今回新成果なし。
[PRECHECK] Local Compact成功。MASTER E正式checkpoint196/READY596（既存値）、規約、B5担当資料、LANE_B_HANDOFF、既存拒否・復旧索引を読取。2026-10-21計22ファイル回収記録と旧「10研究未同期」のID照合は未解決、後発Library訂正版2・08:10/14:14拒否本文も未解決。
[INDEX] CURRENT_ACTIVE_RESEARCH_STATE_LATEST.jsonはV3正本を指す。2026-10-24本run既存read-only validator = PASS_ACTIVE_V3_STATIC、input SHA 14/14、E8 CALL44889、JMP6324、errors=[]、gameplay NOT_RUN。Ghidra/REA再解析なし。
[ORIGINAL] rea_lab/targets/hakushin067_Vahren.exe Get-FileHash SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187現物再計算一致。PEをopen read-only、image base 0x400000、pefile + Capstone x86/32で必要な小窓のみ解析。原作ゲーム未起動・未改変。
[NEW-1 DIRECT] 0x0049C780の0x0049C901-0x0049C915 native：0x49C905でiteratorとmap header比較、0x49C912 LEA ECX,[EAX+0x28]、0x49C915 E8→0x0042E8E0。存在時、node+0x28の3DWORD descriptorから別の値vectorをdeep-copyする経路と整合。
[NEW-2 STRIDE] 0x0042E8E0 native 0x42E918-0x42E935：source[1]-source[0]を0x92492493の定数乗算・符号補正で28byte（0x1C）単位に割る。0x42E958-0x42E964は要素数*0x1Cで容量末尾を設定。0x42E97F E8→0x00430300。
[NEW-3 ELEMENT] 0x00430300 native 0x430361 E8→0x00402710 string copy、0x430369 ADD ESI,0x1C、0x43036C ADD EAX,0x1C、0x430389 ADD ESI,0x1C。Ghidraはsourceとdest双方のstride0x1Cおよびstring length+0x10/capacity+0x14による構築を示す。これにより対象値の28byte連続stringオブジェクト配列をSTATIC-ASM確認。
[STRUCTURE] node+0x0Cは長さ/容量を持つ28byte string key候補（前回0217 node+0x1C length/+0x20 capacity）。node+0x28 begin, +0x2C end, +0x30 capacity-end はvector<string様>の3pointerと静的に整合。実C++テンプレート名・allocator・ABI全体はVERIFY。
[NEW-4 TWO RETRIEVAL FORMS] 既05H 0x49C54F..0x49C589はnode+0x28が指す先頭stringのみコピー。一方0x49C915→0x42E8E0および0x49CC59→0x42E8E0は値vector全体をcloneする経路。単一値文字列getterと配列getterを同一挙動に統一しない。
[NEW-5 WRITER CANDIDATE] 0x0049CD60 nativeは0x49CDB5→0x415530で一時vectorへappend、0x49CDCB→0x49F1F0で既キー範囲検索、0x49CDDE→0x49EE60でerase候補、0x49CDF2→0x49F730でkey+vector pair複製、0x49CE02→0x49FE30でnode構築、0x49CE0D→0x49F7D0でmap挿入を直接CALL。これは当該mapへの登録/更新候補経路であり、他の全writer網羅ではない。
[NEW-6 NODE OWNERSHIP] 0x0049FE30 Ghidraは0x3C-byte node allocateを示す。0x0049FF70の原作native 0x49FFAB→0x405300後に0x49FFB0..0x49FFDEでpair+0x1Cの3 pointerを新側へ移し、旧側を0化。容量再計算ではなくvector ownership transferをSTATIC-ASM確認。alloc失敗/exception中の所有権はVERIFY。
[INFERRED] この0x49CD60枝は一時vectorを作り既キー探索/erase/insertを経るため、当該経路の旧値置換候補と整合。ただし同名keyの重複順・挿入の正確な例外/既値統合・別script writerの優先規則は未解決。0x49CD60の実DAT命令識別もVERIFY。
[PROVENANCE] Window VA0x49C901 len0x2F SHA256=9FF9D1254DCB2CABDCCF4955081EEC47335DD0AEBFBC85B11BD15884A90CB833。
[PROVENANCE] Window VA0x42E8E0 len0xC0 SHA256=10AC8C0B3D5B3FD6237E7672781BF05DA52D30FE150DEDAB2243A89577F639F9。
[PROVENANCE] Window VA0x430300 len0x8C SHA256=3358BAAAB766F627895076C17D5EAA710E2532B3F3CDB08EA9B56A6E41418133。
[PROVENANCE] Window VA0x49CD60 len0x16C SHA256=2C1523156C54BE7D221EF9A995B48696D10D28AAF45981F100E9D223422E1710。
[PROVENANCE] Window VA0x49FF70 len0x89 SHA256=B0D024F94A3F3BF1EF8CBBEAD780464E3E824E635862B24316F95D393C94B2C7。
[DEDUP] 05Hの0x49C572先頭element、04H outparam、03H producer、02H comparatorは参照のみ・新READY再計数0。今回初の差分は+28/+2C/+30の0x1C stride実証、vector全件copy API、map挿入候補鎖、node pointer ownership transfer。B T013_AI/HANDOFF内の新VA照合一致なし（実施済みSelect-String）。
[GOLDEN] 旧無改変EXE・20倍強化前DAT・同SAVE/MAP/input/RNGを揃え、map欠損/空/値1/値2以上・同key更新前後・文字列15/16B・先頭/全件getterの可視結果を別々に比較。原作Gameplay Golden PASS0、strict MATCH0、DYNAMIC0。DESIGNED_NOT_RUN。
[BOUNDARY] 禁VA0x5710C0..0x571500・0x514C50・0x5769B0 XREF・既T024/旧拒否文書payloadへの再試行/迂回なし。初回0x49C8EAからの非命令境界disasm 6命令は破棄、確認済み0x49C901からの正規命令のみ証拠化（OTHER/RECOVERED）。MASTER/他lane/REA/dev_lab/原本ZIP/EXE/DAT/SAVE/Git/Work/設定/schedule不変更。
[NEXT] 0x49CD60の実DAT命令caller・node duplicate policy 0x49F7D0の条件、0x49F1F0→0x49EE60の削除範囲、登録値の配列順を許可済の軽量read-only範囲で確認。T011/T012/T024/T028のP0継続。
[FINAL] B新READY0、MASTER E統合0、Task DONE0、old Gameplay PASS0、strict MATCH0。B所有detail、T013_AI、LANE_B_HANDOFF保存readbackを各独立で確認するまで本IDはNOT READY維持。