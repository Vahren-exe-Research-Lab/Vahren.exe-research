# B-20261030-14H-T013-MODE2-PRIMARY-UNIT-MODE3-GATE-01｜mode2の小隊先頭候補選択とmode3への遷移
Owner B / T013（T024・T028関連） / 2026-10-30 14時台 JST。STATIC / INFERRED / VERIFY / NOT READY。新正式READY0、原作Gameplay Golden PASS0、strict MATCH0。
## 開始前の確認・安全境界
Desktop Commander Local Compactオンライン。MASTER（E最終正式cp196/READY596の旧値）、ANALYSIS_LANES_PROTOCOL、B所有T011/T012/T013/T024/T028、LANE_B_HANDOFF、復旧HUB、13H詳細を先読。旧11H B-RC-20261030-1115-T028-T013-APPEND-SAFETY-01の要約3件はBLOCKED据置で再試行・迂回無し。旧SAFE134/HOLD21、Library54件1-byte差・10/25未回収原文OPEN。
原作解析用PE=rea_lab/targets/hakushin067_Vahren.exe 2910720 bytes SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9別名SQLite=HAKUSHIN067_UNIFIED_V9_20261023.sqlite 141033472 bytes SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、immutable read-only quick_check=ok。旧README/BUILD_MANIFEST/search.sqlite不在は既知OTHER、V9入口を使用。active.lock=False、java/ghidraプロセス検出なし。
## 新たな原作ASM経路：mode2 0x44A100 → 0x44BBB0
0x44A0F8 LEA EAX,[EDI-0x90]、0x44A0FF PUSH EAX、0x44A100 CALL0x44BBB0。0x44BBDD EBP=[ESP+0xC8]でそのmanagerを受ける。V9擬似Cは型/ABI未確証のため原作ASMを優先。
0x44BCBD EAX=[EBP+0x1C]、0x44BCC0 ECX=[EAX+0x38]、0x44BCCA EAX=[EAX+0x3C]。管理下のgroupポインタvectorを反復。0x44BCEE EBX=[ECX+EAX*4]で個別groupを取り出す。
0x44BCF1 EBX+0xC0の木head、0x44BD06..1Dで使用済nodeのpayload処理/ノード解放、0x44BD28..3Fでheadリンクを自己参照へ戻し、0x44BD42 [EBX+0xC4]=0（木countと推定）へ初期化。payloadの意味や解放例外はVERIFY。
0x44BD4C..59ではgroup+0x0C..+0x10のUnitポインタ配列個数を算出、DL=1で走査開始。0x44BD73 ESI=[ECX+EAX*4]、0x44BD7A CMP BYTE PTR [ESI+0x1867C],0 / 0x44BD81 JE 0x44BD9A。最初にこのbyte=0の候補が出ればそこでloopを抜ける。候補がないと0x44BD98 XOR ESI,ESI。
0x44BD9A MOV [EBX+0xB8],ESI。非NULLなら0x44BDAD CALL0x565780、0x44BDBB CALL0x5158E0へ、NULLなら0x44BDC0へ。group+0xB8はこの経路の選択Unit参照と静的推定。+0x1867Cの論理名と下位の実副作用はVERIFY。
## 条件付きのmode2→mode3遷移をcallerと接続
group走査後、0x44BDE8 CMP DWORD PTR [ESP+0x68],0が非0なら0x44BEC5へ。0の経路は0x44BDF5で[[EBP+4]+0x1EF22C]を確認し、その値が非0の場合0x44BE0A MOV DWORD PTR [EBP+0x20],3。続いてmanager+0x38..3Cの配列を走査、group+0x1C=0なら0x44BE19 PUSH0 / 0x44BE1B PUSH0 / 0x44BE1D CALL0x5690C0。local +0x68は意味・producer未確定で「選択候補0」を断定しない。
13H既知の0x44A084 MOV ECX,[EDI-0x70]はmanager=EDI-0x90ゆえ同じmanager+0x20をdispatch modeとして読む。よって条件成立ならmode2処理内部で次回dispatchをmode3へ移す書き込みが存在する（STATIC）。実tickで遷移すること・callee0x5690C0の状態作用は未実測。
## mode1との独立差分（同時分析）
0x44B240（mode1）は0x44B372～389でUnit+0x1867C==0のみUnitData=Unit+0x1C8の+0x1C4を合計し、0x44B393/3A2で分岐条件に応じて合計の最大/最小を更新。group中Unit+0x1A4==2の別集計が0x44B3CF..4BFに存在し、manager+0xA7 gateを通る。これらはmode2の「最初の有効Unitポインタ」保存と異なるが、scoreのゲーム上の意味・乱数分岐はVERIFY。
## 証拠・非重複・受入
原作PEバイト窓：0x44BCE0+272B SHA256=AF7CA919852D359769BD6A9231243F48E3FD47A01FB8CAC027450F36712F3FD8、0x44BDF2+160B SHA256=1A3E39624256AB888FF7E2DC474A25C93FED069C501A598F983705D397C4D0C1。原PE静的ASMとV9擬似Cの二重照合、LIVEではない。
B所有data/exeのT011/T012/T013/T024/T028 Markdown + HANDOFF計384件で新VA 0x44BD9A/7A/42、0x44BDF5、0x44BE0A、0x44B391、0x44B400先行literal0。13H mode dispatch/0x44B240/0x44BBB0入口自体は既知で新規再計上しない。10/25未回収原文・他lane全意味重複はVERIFY。
Golden必須：無改変原作EXE・20倍変更前DAT・同一SAVE/MAP/入力/RNG、mode2 caller実到達、各group+0xC0/+0xC4/+0xB8、Unit+0x1867C=0/非0/空群、[ESP+0x68]・+0x1EF22C両値、翌tickのmanager+0x20と実選択・行動を原作同runで取得。DESIGNED_NOT_RUN、PASS0/strict0。
次は0x44BEC5の非ゼロ枝、0x44BDAD/0x44BDBB後処理、0x5690C0副作用、T011召喚EXP/T012 damage/T024通常AI/T028士気。原本/MASTER/他owner/REA/dev_lab/Git/Work/設定/automation変更なし。本B詳細・data/T013_AI.md・evidence/LANE_B_HANDOFF.mdのみowner保存候補。安全拒否済み要約11Hの再提出なし。
