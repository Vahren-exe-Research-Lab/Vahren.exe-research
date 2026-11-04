# B-20261030-0515-T028-DUAL-RETRY-POSTRET-MODE1-JUMP-01
Owner B / T028（士気・敗走）/ 2026-10-30 05H JST / STATIC + INFERRED + VERIFY / NOT READY
## 証拠源と前提
- Desktop Commander Local Compact PC ONLINE。MASTER cp196 / 正式READY596（既存E確定値）、ANALYSIS_LANES_PROTOCOL、B5 owner・B HANDOFF・復旧HUB/索引を先読。旧SAFE134/HOLD21・Library54件1byte差・10/25原文未回収はOPEN。
- 原作解析コピー rea_lab/targets/hakushin067_Vahren.exe を起動・変更せず、実バイト2910720B SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。PE32原ASMをpefile+Capstoneで局所逆ASM。
- 統合V9 HAKUSHIN067_UNIFIED_V9_20261023.sqlite SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、immutable読み取り専用 quick_check=ok。V9 function 0x5AC1A0はint(param1,param2,char param3)という未検証疑似CでありABI確定値ではない。元Ghidra再解析0。
## 新規 native 条件の接続（既知0x5AC5E3の「RET後到達不明」を部分解消）
- 0x495026 XOR EDI,EDI、0x495028 TEST EDI / 0x49502A JLE 0x495032で初回index=0の+0x77検査をskip。0x495032 Unit+0x1B4非NULLなら0x49505Cで既存候補を再使用。
- Unit+0x1B4がNULLなら0x495041 TEST EDI、0x495043 SETG CL、0x495046 MOVZX EDX,CL → 0x49504D PUSH EDX（第三引数）/ 0x495050 CALL 0x5AC1A0。index0ではflag0、index1ではflag1。
- 0x495062 TEST EBX／0x495064 JNE 0x49553Cで候補成功時既知退却処理へ。NULLなら0x49506A INC EDI / 0x49506B CMP EDI,2 / 0x49506E JL 0x495028。2回目index1では0x49502C CMP BYTE [ESI+0x77],0→0x495030 JE 0x495070で退却先再検索を省略。index2は処理しない。
- 既知0x5AC1A0の0x5AC36D CMP BYTE [ESP+0xC4],0 / 0x5AC375 JE 0x5AC3E0は第3引数のnonzero gate候補。通過時0x5AC384 CALL 0x597D50。V9のparam3=charは未検証ABIなのでnative引数スタック対応を原作初期フレームと実機でVERIFY。
- 0x5AC3AC MOV EDX,[EDI+ECX*4]で追加候補list要素を取得、0x5AC3AF CMP BYTE [EDX+0x77],0 / 0x5AC3B3 JNE 0x5AC3BF、続く0x5AC3B5 CMP BYTE [EDX+0x75],0 / **0x5AC3B9 JE 0x5AC5E3**。両byteが0なら明示的に5AC5E3へ分岐する。
- 0x5AC5E3 PUSH 1、0x5AC5E5 PUSH EDX、0x5AC5E6 PUSH EBP → **0x5AC5E7 CALL 0x598450(mode=1)**。これは0x5AC5D8 RETの後ろにあるが、0x5AC3B9からの直接条件分岐が存在する。旧00Hの「RET後なので通常到達不明」を「STATIC CFG上の入口あり」に訂正。実行時成立はVERIFYでありDYNAMICとしない。
- 0x5AC5EC以降は候補listの解放・一部後始末から共通RETへ合流する構造。0x598450(mode1)自体の副作用は旧00/01H研究を参照し、新規再計上0。
- 追加観測: 0x494F8E [EBP+0x1EED54]→CL、0x494F98 [ESP+0x6F]への保存は確認。ただし0x494FD1 SUB ESP,0x1Cが後続にあり、0x495596 [ESP+0x6F]の同一slotだと断定できない。stack flag producerは引続きVERIFY（安易な相関禁止）。
## 原作証跡・重複・境界
- 原PE窓SHA256：0x495020..0x495080（96B）=24406079AB36E5CFD8FE06FBE2BAF7BBCB67A38581AD15F1D470A9054903BE1E；0x5AC340..0x5AC3D0（144B）=6271D18B2D7CBC390A43E2504A7D45924CA74FDE98A70FD12CDA70C4D594DEA1。
- B所有T028*.md＋HANDOFFで新サイト0x5AC3B9/0x5AC3AF/0x49506A/0x495043先行literal0件。0x5AC5E3先行3資料あり、当該site・mode1 CALL自体は既知で新規加算0。未回収10/25・他laneの完全な意味的重複はVERIFY。
- 静的論理: 「初回0→失敗時のみ再試行候補1、ただしUnit+0x77が0なら中止」「追加候補の+0x75/+0x77両0はmode1 helperへのCFG枝」を接続。実ゲームのSpot可否・全局的到達性・再帰/副作用・RNG・有効な退却は未確定。
## Goldenと再開
- 原作無改変EXE・x20改変前DATを確認し、同SAVE/MAP/入力/RNGで既存Spot有無、初回成功/失敗、+0x77=0/1、追加候補+0x75/+0x77組合せ、容量境界、flag0/1 helperの呼出しと退却・予約カウンタ・通知・翌tickを採取するまでDESIGNED_NOT_RUN。原作Gameplay Golden PASS0／strict MATCH0／新正式READY0／E MASTER0／DONE0。
- 次回P0：0x5AC3B9→0x5AC5E3のCFG前提/0x598450(mode1)の実副作用とdataflow、0x494F98/0x495596の実stack slot同一性、+0x77 field producer。T011召喚EXP、T012傷害、T013最終対象、T024通常AIも継続。
- SAFE_REFUSAL新規0／既拒否の別tool・shell・path迂回0。原本/MASTER/他lane/REA/dev_lab/Git/設定/automation/Work不変更。