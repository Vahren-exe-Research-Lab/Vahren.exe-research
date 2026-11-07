# 新B T028｜符号付きmodeによる2系統effect subobject選択（2026-10-29 09H）
ID: B-20261029-0910-T028-SIGNED-MODE-TWO-EFFECT-SUBOBJECTS-01
Owner: B/T028。Status: STATIC ORIGINAL-PE ASM + V9 PSEUDOC / INFERRED / VERIFY / NOT READY。
## 根拠・復旧
- Local Compact ONLINE。E MASTER最終正式既知checkpoint196/READY596（全件再計数なし）。ANALYSIS_LANES_PROTOCOL、B5 owner末尾、LANE_B_HANDOFF/安全保全索引を先読。
- SAFE134 byte照合済/HOLD21安全関連、B147うち54件1B差の旧監査、10/25 14H原文不明は未解決。拒否済みVA/操作・不完全スクリプトの読込実行/再提出/迂回0。
- 旧search_index README/BUILD_MANIFEST/search.sqliteは読取のみ。新規検索は別名統合V9 CLI/SQLite、verify=V9_INDEPENDENT_READBACK_PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。PC標準V3は無変更。
- 対象copy rea_lab/targets/hakushin067_Vahren.exe 2910720B、今回実バイトSHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。pefile+Capstone 32-bit read-only。MAIN window 0x4A3A00 length0x1DA SHA256=4E636368B4F4398CF0BDE1882EB99C0B9E03F6F614EF73B712568A65D8C2CB72、helper0x4189B0 length0x25 SHA256=3BA61613D854BA230369D44D30A9E916C84225D16CA498C498E5FD30BD676032。
## 新 native sign/provenance
- caller owner=FUN_004A1250。0x4A3A33..40で入力vectorの(end-begin)/4を得てEBX=3、[EBP-0xF04]=3を初期設定。0x4A3A46 CMP count,2; 0x4A3A49 JB 0x4A3A63ならmode=3を維持。
- count>=2では0x4A3A4B EDX=EBX-2=1、0x4A3A4E CALL0x415750、0x4A3A55 CALL0x4528A0の後、0x4A3A5A EBX=[EAX+4]で2番目の項目由来の整数を採る。0x4528A0のGhidra署名void、実際の型/取得APIと例外はVERIFY。
- 0x4A3A82 CALL0x49E490直後0x4A3A87 TEST EAX→0x4A3A89 JNE 0x4A3AD0。一方0x49E490はGhidra擬似Cではvoidであり、EAXを意味的なbool戻り値と断定しない。false経路0x467DE0→0x583CF0→0x597BA0もある。
- 0x4A3AD0 TEST EBX、0x4A3AD2 JS 0x4A3ADF。非負modeは0x4A3AD4 PUSH EBX→0x4A3AD5 CALL0x4189B0。負modeは既08Hの0x4A3ADF CMP EBX,-1→0x4A3AE2 SETE CL→0x4A3AEB CALL0x431BE0。-1だけAL=1、ほかの負値はAL=0。
## 新しい2サブオブジェクトの識別
- 0x4189B0のnative：0x4189B6 [vtable+0x64]→0x4189BB CALL EDX→0x4189BD TEST AL→falseなら0x4189D0。true時0x4189C1 EAX=[ESP+0xC]でmodeを受け、0x4189C5 ESI+=0x1E0→0x4189CB CALL0x5AA130。
- 非負値経路は対象オブジェクトOの O+0x1E0 をeffectサブ領域として使う。一方既知の負値経路0x431BE0→0x431BF1 ECX=O+0x260→0x431BF7 CALL0x5AA6E0。2領域を1つのeffectとして統合しない。
- 0x5AA130のV9擬似Cは入力modeをサブ領域+0x78に保存し、0..11のswitchで値/色候補を選択後、座標・登録を更新する（unverified ABI）。0x5AA6E0は既知AL1/0分岐と内包矩形縮退を持つ別callee。実描画/ダメージ/士気/敗走の意味はVERIFY。
## 二つ目の候補経路（新しいguardの結合）
- 0x4A3B1E CALL0x467F40の非NULL側で0x4A3B33 CALL0x593400。後者V9擬似Cはparam1+0x68の木を走査し結果vectorへ候補ポインタをappendする（型/実体VERIFY）。
- 0x4A3B46..50は候補vectorの4byteポインタ件数でloop。0x4A3B66 [vtable+0x64]→0x4A3B69 CALL EAX、falseはskip。trueならmode>=0時0x4A3B8F CALL0x4189B0、mode<0時0x4A3BA7 CALL0x431BE0。
- 候補vector枝では先に0x4A3B69の仮想判定、その後どちらのhelperも内部で同slot+0x64を再判定。二度の仮想呼出が常に同値・副作用なしとは限らず、virtual実体/変動をVERIFY。
## ネイティブCALL・重複監査
- 独立PE REL32: 0x4A3A4E→0x415750、0x4A3A55→0x4528A0、0x4A3A82→0x49E490、0x4A3AEB→0x431BE0、0x4A3B33→0x593400、0x4A3BA7→0x431BE0、0x4189CB→0x5AA130の7/7一致。0x4A3AD5/0x4A3B8F→0x4189B0もCapstone命令で確認（追加REL32再算出は別回）。
- 08H既知0x4A3ADF/0x4A3AEB/0x4A3BA7/-1 sentinel/wrapper3件は再計数0。B5 owner+HANDOFFで新site 0x4A3A38/0x4A3A5A/0x4A3B33/0x4A3B66/0x4A3B8F/0x4189CBの先行字句0件。他lane/未発見10/25の意味的完全dedupはVERIFY。
## 再実装・Golden判定
- mode省略→3、>=0→O+0x1E0/0x5AA130、負値→O+0x260/0x5AA6E0、-1と他負値、候補0件/1件/複数件、仮想判定が2回変わるedgeを独立fixtureとして切り分ける。現状まだ設計のみ。
- 原作無改変EXE＋x20強化前DAT確認＋同じSAVE/MAP/input/RNGで両枝の合法実到達、オブジェクト世代・両領域/次tick、士気/敗走/対象選択への効果を同一runで記録するまでGolden DESIGNED_NOT_RUN。Gameplay Golden PASS0、strict MATCH0、新READY0、E MASTER統合0、Task DONE0。
- 次回: 0x5AA130のmode switchとO+0x1E0の型/登録先、0x593400→0x467E90の候補origin、0x49E490のreturn ABI、T013最終target/T024通常AI/T028士気敗走。T011召喚・T012計算継続。
- 新安全拒否0、旧拒否の再実行/別経路迂回0。原本、MASTER、他lane、REA/dev_lab、Git/Work/設定/schedule書込0。
