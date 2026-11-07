# B-20261029-1908-T028-RETREAT-OK-DRAIN-ELIGIBILITY-01｜T028 retreat_okイベントからのqueue drain・Unit存在判定
日時: 2026-10-29 19H JST｜Owner B/T028（T013/T024参照）｜STATIC ORIGINAL-PE ASM / INFERRED / VERIFY / NOT READY
## 証拠源・先行回収・安全境界
- Desktop Commander Local Compact PC ONLINE。MASTER公式最新既知checkpoint196 / READY596は再集計なし、ANALYSIS_LANES_PROTOCOL、B5 owner、LANE_B_HANDOFF、共通復旧ハブ、2026-10-29 18H成果を先読。旧SAFE134/HOLD21、B147資料54件1B差、2026-10-25 14H欠落原文はOPENのまま。既拒否対象0x5710C0..0x571500や以前の拒否命令/ファイルは非接触。
- 原作解析copy rea_lab/targets/hakushin067_Vahren.exe 実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。統合V9 DB実SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、00_START_HERE_UNIFIED_V9_20261023.md/CLIを明示的に使用。PC標準V3未変更、元README/manifest/旧search.sqliteは整理後不在。原作ゲーム/Ghidra再実行0、java/ghidra稼働・search_index active.lock検出0。
## 今回の独立した原作命令証拠
- V9 callers(0x49D1B0) 7直接E8：0x449765,0x449E5C,0x44B770,0x44C767,0x44CE70,0x44CFA0,0x522121。7 site列挙は前18Hの既知結果であり新規加算0。今回は最後の0x522121と、前二siteの引数伝播を原作ASMで新規確認。
- 0x5220D9 PUSH 0x62B448（原作現物文字列ASCII retreat_ok\0）→0x5220DE CALL 0x402670→0x5220E3 CALL 0x43F330。戻ALとBL=0を比較するイベント判定（BL=0は0x521DD2 XOR EBX,EBXと到達経路からINFERRED）。
- 成立枝: 0x5220F0 CMP DWORD[0x87F6F0],1 / 0x5220F7 JNE離脱、0x5220FD MOV DL,[EBP+0x18] / 0x522102 JNE 0x52216E。よって後続queue処理はグローバル値1、EBP+0x18=0の枝に限定。
- 0x522104/107で[[EBP+0x14]+0x1D]を比較。非0なら0x52211Bへ直行。0なら0x52210C MOV ECX,[EBP+0x194]→0x522112 CALL0x49D030（DL=0）→0x522117 TEST AL→0x522119 JE0x52216E。下位ゲート非成立では0x49D1B0も状態4書込も迂回。
- 0x49D030原PEではDL=0時、参照S=[EBP+0x194], C=[S+0x0C]について [C+0x54]==0、[C+0x50]!=0、[[S+0x10]+0x38]!=0、[S+0x1EED54]!=0、[[C+0x50]+0x79]!=0 が揃ってAL=1の枝（0x49D030/33/39/43/60/64/6C/6F/74）。0x49D030自体は既10/26 T024で別用途のAL意味確認済みのため関数発見を再計上せず、今回新規はretreat_ok・DL=0との結合。
- 通過時 0x52211B MOV ESI,[EBP+0x194]→0x522121 E8 CALL0x49D1B0。先18H 0x44CF97はmanager[EBX+4]+0x504をESIとしたが、今回のretreat_ok入口は+0x504演算なし。同一object baseであると断定しない（型/alias VERIFY）。
- 0x522126..522165で[EBP+0x38]/+0x3Cの外側pointer配列を走査。各要素+0x1Cが0の時だけ0x522150 CALL0x5694E0、AL=0なら0x522157 JE0x52216Eで早期離脱。要素+0x1C!=0ならskip。全要素通過、または外側vectorが空なら0x522167 MOV DWORD[EBP+0x20],4。値4のゲーム上の意味はVERIFY。
- 0x5694E0実ASMは入力EAXの+0x0C..+0x10内側Unit pointer配列を走査し、Unit+0x1867C==0かつ+0x1867E==0が一件でも存在する場合AL=0、存在しなければAL=1（空配列も1）。従って外側対象の一つが未処理eligible Unitを持てばstate4書込を抑止する形。ただしUnit生存/敗走・イベント成功の意味はINFERREDで未実機確認。
- 別上流0x449730の0x44974F/53 gateでは[EDI+0x0C]!=0かつ[EDI+0x16]!=0の時0x449755 MOV ESI,[EDI-0x8C]→0x44975B ADD ESI,0x504→0x449761 byte+0x16=0→0x449765 queue drain。0x4498E0の0x449E48/4C gateでは同一byte条件で0x449E52 LEA ESI,[EAX+0x504]→0x449E58 flag0→0x449E5C drain。+0x16はこの二入口のone-shot latch候補、resetタイミングはnative確定、再セット条件VERIFY。
## 範囲・既知との非重複・再実装影響
- 新しい接続は retreat_okイベント→二段gate→queue callback/drain→外側/内側Unit状態判定→state4条件付きwrite、および3 CALL site間のESI provenance差。既18Hの0x49D1B0内部 callback+0x58 / state2 break / drain自体は再計上0。前T024の0x49D030 predicate本体も再計上0。
- B-own data/T011,T012,T013,T024,T028*.md＋HANDOFF 365文書を先行全文字列スキャン。retreat_ok/0x5694E0の先行hit0、0x522121は18H詳細のみ1、0x49D030は旧T024研究4件にあり。別表記・未回収10/25・他owner意味論完全dedupはVERIFY。
- 元PE窓SHA：0x521D90/5269B 269738D288019D06CB677FD1C91FF9D3B7A29E3A9B091E12932885F7668BAA57；0x49D030/95B 0F9A4A99B586A902C95B4F49467E44516090BFF3FF3F24F26F87CF4977BEC4A0；0x5694E0/70B 21EB560D3D28992C70630681A9A7618DBBE13F4AEA03913096085A9B698DECB5。
- 0x49D1B0のvirtual+0x58具体的class・queue操作の副作用、0x49D030のstatus語義、EBP+0x20=4の戦況遷移、0x522121時のESI型、call後の可視敗走はVERIFY。Ghidra擬似C署名はnative ABIではない。
## Golden必要条件・状態・NEXT
- 原作未改変EXEとx20改変前DAT、同一SAVE/MAP/input/RNGでretreat_ok条件、global[0x87F6F0]=1/非1、EBP+0x18/linked+0x1D/0x49D030 DL0とAL、queue begin/end＋callback、外側+0x1C/内側Unit+0x1867C/+0x1867E、EBP+0x20の遷移、可視戦闘・翌tickを同一runで合法取得する。DESIGNED_NOT_RUN。
- 原作Gameplay Golden PASS0、strict MATCH0、新B正式READY0/E MASTER統合0/Task DONE0、STATIC/INFERRED/VERIFY/NOT READY。新SAFETY_REFUSAL0・旧拒否迂回0。B文書以外、原本/MASTER/他owner/REA/dev_lab/Git/Work/設定/schedule変更0。
- NEXT：0x52216E以降のstate4消費先（旧拒否対象除外）、0x49D1B0 vtable+0x58の型別実体、+[0x1EEC3C] writer・queue entry producer、T028敗走とT024通常AIからの確定接続。