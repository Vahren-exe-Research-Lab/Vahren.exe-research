# B-20261029-2013-T028-RETREAT-POSTPASS-VTABLE68-01｜retreat_ok共通後段のUnit仮想dispatchと戻り値ABI
日時: 2026-10-29 20H JST｜owner B/T028（T013・T024 cross-reference）｜STATIC ORIGINAL-PE ASM / INFERRED / VERIFY / NOT READY
## 証拠源・回収・境界
- Desktop Commander Local Compact PC ONLINE。開始前にMASTER、ANALYSIS_LANES_PROTOCOL、B HANDOFF、T011/T012/T013/T024/T028の担当資料、旧復旧索引、共通RECOVERY_HUB/操作規約をread-only確認。E MASTER既知checkpoint196/READY596を再集計せず。旧SAFE134/HOLD21、B Library54件1byte差、2026-10-25旧原文未回収はOPEN。
- 原作解析コピー rea_lab/targets/hakushin067_Vahren.exe 実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9統合DBを専用CLIでread-only使用、verify=V9_INDEPENDENT_READBACK_PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。PC標準V3は変更なし。active.lockなし、重いGhidra/Java新規起動なし。
## 今回の独立増分：retreat_okの共通後段
- 既19Hの0x5220E8条件成立かつglobal[0x87F6F0]==1の枝から、0x522102 [EBP+0x18]!=0、0x522119 predicate AL=0、0x522157 0x5694E0 AL=0は、いずれも0x52216Eへ合流。0x522167 [EBP+0x20]=4は全候補通過時だけ。一方global!=1の0x5220F7 JNE 0x523204はこの後段をskip。従って『state4が書かれない＝イベント後続が全停止』ではない（STATIC CFG）。
- 0x52216E MOV ECX,EBP→0x522170 E8 CALL 0x528700、0x522175 PUSH EAX/0x522176 LEA→0x52217B E8 CALL 0x525C90。前者は2026-10-25 T024で既知の owner+0x364/+0x368 spanに応じたlist adapter（再計上0）。後者はコピー用0x525E80を呼び新しいlinked-list sentinelを作る（V9擬似C、native E8）、選択listの独立複製と推定。
- 0x52218C/0x522197～0x5221A8のlist gateを通過したnodeについて0x5221B0 [ESP+0x1C]→0x5221B4 ECX=[node+8]→0x5221B7 E8 CALL 0x5681C0。list end到達まで0x52223E/0x522248経由で巡回。0x522252→0x406B80で作業listを破棄。node実型と対象集合の完全性はVERIFY。
## 今回の独立増分：calleeの実ASMと戻り値
- 0x5681C0はGhidra擬似Cでは void __fastcall と表記されるがnative 0x568382 XOR EAX,EAXと0x568325 MOV EAX,ESI→0x568384共通exitがあり、0x5221BC MOV ESI,EAX→0x5221BE CMP ESI,EBXで戻りEAXを実際に検査している。従ってvoid契約を再実装/フックABIとして採用不可。
- 0x568265/0x56826Bにある [ESI+8]+0x18、0x568274でmanager+0x1EF22C、0x568290で先頭Unit+0x18610 の条件を満たす場合のみ0x5682C3 CALL 0x5AC1A0側へ進む。0x5682CB EAX==0の場合0x5682CF..0x568325でglobal stringに文字列を構築し、非零pointerをEAX返却して0x568335後段をskip。文字列の具体的意味・成功/失敗命名はVERIFY。
- 正常後段0x568335..0x56836Cは[ESI+0x0C]/[ESI+0x10]の4B pointer vectorを走査。0x56834D CMP BYTE [ECX+0x1867C],0→非零なら0x56835Eへskip、零なら0x568355 MOV EAX,[ECX]→0x568357 MOV EDX,[EAX+0x68]→0x56835A PUSH1→0x56835C CALL EDX。vector長を各回再読し、通常終了時0x568382 EAX=0。
- 16H・17H既知のslot+0x68はSimpleUnit→0x544D10、StaticUnit/SimpleStaticUnit/Unit→0x578110のmode1入口（今回のvtable map自体は再計上0）。今回の新規増分はretreat_ok共通後段→list copy→0x5681C0→各Unit+0x1867Cゲート→slot+0x68(arg1)という別の静的到達経路。実機での動的class、反復回数、退却行動・通知はVERIFY。
- 0x5221BE EAX非零の場合0x5221C6..0x522239で文字列を組み0x522239 CALL0x52CCF0。0x5681C0の非零ポインタを通知側へ渡すパスがあり、Ghidra上のvoidと矛盾するnative戻り値の消費点。具体UIの表示・実行タイミングはVERIFY。
## 既存成果重複・出典・復旧状態
- PE E8 site bytes: 0x522170=e88b650000→0x528700、0x52217B=e8103b0000→0x525C90、0x5221B7=e804600400→0x5681C0。0x568355.. native=8b018b5068...（vslot0x68）。窓SHA256: 0x52216E..0x52225F(242B)=292489E6D475371FBE78E9280A5445D0B60E474459E4518BBCD411A79A008CE8、0x5681C0(493B)=AEDE9147D0DD7957F4568FEF450D9706021DA71640E8B73008B0C3F4A3E41E2A、0x525C90(163B)=D27EF45A72988E18B8039B2E9BFB9B5BF17BC7642F1AD182F9D8F20669D65710。
- 新VA 0x5221B7/0x5681C0/0x56835C/0x525C90はB所有365 markdown・既存B HANDOFFで先行literal0。0x528700は2026-10-25 T024既発見2件、単体を新規計上しない。2026-10-29 19Hのstate4 writer/0x5694E0も再計上しない。旧2026-10-25の未回収原文、他laneの意味的完全dedupはVERIFY。
- 既存安全拒否済み0x5710C0..0x571500と拒否済み証拠/コマンドは未接触・迂回0。今回CONNECTION/SAFETY_REFUSALは0。PC分析は全てread-only（保存文書のみB owner書込）。
## Golden・次回・状態
- 原作未改変EXEと20倍改変前DAT、同一SAVE/MAP/input/RNGでretreat_ok成立/global1、+0x18非零、predicate 0、Unit条件AL0、state4書込成功/抑止をそれぞれ測定。0x528700のlist分岐、0x525C90のnode順序、0x5681C0の+0x18610/+0x1867C、slot+0x68 dispatchとEAX戻り、0x52CCF0の可視挙動・翌tickを同一合法runでGolden化。DESIGNED_NOT_RUN。
- 原作Gameplay Golden PASS0、strict MATCH0、新B公式READY0、E MASTER統合0、Task DONE0。STATIC / INFERRED / VERIFY / NOT READY。次=T028 0x5681C0前段+0x1EF22C writerと0x5681C0戻り文字列/0x52CCF0、副経路mode1本体のフラグ副作用、T024通常AIとの交差、T011召喚経験値/T012ダメージP0。
- 原本EXE/DAT/SAVE/ZIP、MASTER、他lane/REA/dev_lab/Git/設定/Work/scheduleは無変更。保存・readback・SHA/ID一意の証跡は本runの後続receiptを参照。
