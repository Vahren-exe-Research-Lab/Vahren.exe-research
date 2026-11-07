# B-20261028-14H-T028-DECIDE-SELECTOR-FLAG-WEIGHT-01｜候補状態+0x74による decide3/decide11 と数値パラメータの分岐
Owner: B / T028。2026-10-28 14時台 JST。STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / INFERRED / VERIFY / NOT READY。新正式READY0、E MASTER統合0、Task DONE0。
## PRECHECK / 安全境界
Desktop Commander Local Compact ONLINE。MASTER最後のE正式checkpoint196/READY596（既知値・全件再集計ではない）、ANALYSIS_LANES_PROTOCOL、B所有T011/T012/T013/T024/T028、LANE_B_HANDOFF最新13Hと旧拒否・未同期索引、legacy README/manifest、V3正本案内を読取。2026-10-25 14H OFFLINE研究全文と他owner意味的全照合は未回収VERIFY。
原作 EXE rea_lab/targets/hakushin067_Vahren.exe SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回実バイト再計算一致）。V3 DB SHA256=0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25（実バイト一致）。verify_active_research_state_v3: PASS_ACTIVE_V3_STATIC、入力14一致、errors[]、original gameplay NOT_RUN。検査したactive.lock二箇所なし、Java/Ghidraプロセス検出なし。旧原作実行・全面再解析なし。
## 今回の原作ASM新増分（関数0x00497BB0）
既11H/12Hの0x497C0D/0x497C12 candidate+0x77/+0x75両0なら即vector追加/清掃、片方非0なら別枝へ、という分岐は既知で再計上しない。今回はその**非0枝** 0x497C3B..0x497CB4 の数値と文字列producerを照合。
- 0x497C41 CALL0x5846A0の後、0x497C4D MOV CL,BYTE [EBP+0x74]、0x497C55 TEST CL、0x497C57 JE0x497C63。candidate+0x74!=0なら0x497C59 MOV DWORD [ESP+0x34],0x1F4（500）、0x497C61 JMP0x497C7B。
- candidate+0x74==0なら0x497C63 MOV EDX,[ESP+0xB0]→0x497C6A MOVZX EAX,BYTE [EDX+0x1D]。0x497C6E NEG /0x497C70 SBB /0x497C72 AND EAX,0xF /0x497C74 ADD EAX,0xA。したがって対象byte==0なら数値10、!=0なら25。0x497C77 [ESP+0x34]=EAX。
- 0x497C7B MOV EDX,0x632838、0x497C80 TEST CL、0x497C82 JNE0x497C89、0x497C84 MOV EDX,0x632840。原作PE実文字列は0x632838='decide3'、0x632840='decide11'。+0x74!=0→'decide3'＋500、+0x74==0→'decide11'＋10/25の同一分岐。0x497CAF CALL0x402800は選んだ名前を渡す文字列操作経路。
- 条件表（STATIC）: (+0x77==0 AND +0x75==0)は従来のECX null/non-null早期枝（本分岐不実行）。それ以外の枝で (+0x74!=0)→decide3/500、(+0x74==0 && [param-like +0x1D]==0)→decide11/10、(+0x74==0 && [param-like +0x1D]!=0)→decide11/25。
## 機械語・証拠・重複
原作 PE VA0x497C3Bから160 bytes SHA256=2E3298C913E9F2016EA1443BCA5E493E9172F7C57FA790A44B4711F96B78168D。限定x86-32 Capstone解読、E8 REL32 site0x497C41→0x5846A0、0x497CAF→0x402800 の原作machine byte両方一致（2/2）。現行V3 function 0x497BB0はSTATIC擬似C（ABI未検証）で候補+0x74と文字列分岐を補助照合。
B所有T011/12/13/24/28 data/exe MarkdownとHANDOFF計328ファイルの新VA 0x497C4D/59/63/74/7B/84 の事前直接一致0。'decide3'文字列自体は先行T012_ENTRY_CONTEXT_FALLBACK_SUPPORT_AND_RESET_20261021.mdでも登場（別VA 0x490180の言及）するため**新発見として再計上しない**。今回の固有差分は0x497BB0におけるcandidate flagと2文字列・3数値のnative producer接続。
## 解釈限界・Golden・再開
値500/25/10の用途（timer/優先度/choice timeoutなど）は未確定。'decide3'/'decide11'のゲーム上の意味、+0x74/+0x1Dの型、原作Gameplayでの合法到達、乱数や可視UIへの影響はVERIFY。数値を士気値や死亡件数と断定しない。前回13HのECX=NULL caller4箇所も+0x75/+0x77の両0が必要なので、無条件破棄と誤読しない。
無改変ver0.67 EXE＋20倍化前DAT、同SAVE/MAP/input/RNGでcandidate(+75/+77)=00/01/10、+74=0/非0、arg+1D=0/非0、ECX=NULL/非NULL、後続string/数値・索引・実戦視覚を原作合法runで検証するまでDESIGNED_NOT_RUN。原作Gameplay Golden PASS0/strict MATCH0、新正式READY0/E MASTER統合0/DONE0、NOT READY。
次P0: 0x497CAF後段の数値[ESP+0x34]実消費siteとdecide literal対象、13Hの四NULL caller上位flag、第二赤黒木の実consumer、T028士気・敗走/T013最終対象/T024 AI/T011召喚親子。旧10/25未同期全文は別記録保持。既安全拒否VA0x5710C0..0x571500・0x58021E..0x580340と拒否済み操作を再試行・別tool/shell/path/Remote/ZIPで迂回しない。MASTER/他owner/REA/dev_lab/原本EXE/DAT/ZIP/SAVE/Git/Work/設定/schedule書込なし。
