# 迫真戦記 ver0.67｜B T028：放浪・傭兵結果vectorのphase1読取／排出経路（23時台）
研究ID: B-20261028-2315-T028-RESULT-QUEUE-PHASE1-FLUSH-01　owner: B/T028　状態: PC-SAVED / STATIC-ORIGINAL-PE-ASM / STATIC-V9-COMPOSITE / INFERRED / VERIFY / NOT READY
## PRECHECK / 未同期
Local Compact PC接続成功。E所有MASTERの最終正式cp196/READY596、解析規約、B HANDOFF・T028 owner、旧安全拒否・未同期回収索引、旧README/BUILD_MANIFEST、現行V3 pointer・統合V9の独立案内を読取。PCのB詳細は16Hが最後で17〜22HのOFFLINE研究6件は未同期。旧10/25 14H全文/他lane完全意味dedupはVERIFY。
旧原作copy rea_lab/targets/hakushin067_Vahren.exe（2910720 bytes）実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9独立verify=V9_INDEPENDENT_READBACK_PASS、SQLite SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、11,950関数。標準CURRENT pointerはV3のまま・変更なし。Ghidra再解析/原作起動なし。
## 増分1：管理vectorの消費関数と呼出のphase分岐を特定
V9擬似C全文検索で+0x1EEC74 consumerを関数0x0048C880（3608 bytes）に同定。原作native関数SHA256 441795CC17AE77C73508DC3EB7940A8E28CE7FCFF706FF0742E9425E9B0CDB66。
直接callerは0x004B99C0 CALL 0x0048C880（原作E8 bb2efdff）。関数0x004B9930の0x004B9970でmanager+0x1EF144を取得し、0x004B997B JMP [EAX*4+0x004B99FC]。原作jump tableのindex1は0x004B99B9で、0x004B99C0 CALL時の引数はmanager+0x504。これはphase selector=1経路のSTATIC接続。
0x0048C8BE MOV [EBP+0x1EEC3C],1 をnative確認。過去15〜22Hの放浪/傭兵送信先選択で見えた同offsetのflag=1分岐と接続する可能性は高いが、全callerが同一manager実体を渡す保証はVERIFY。
## 増分2：5要素刻みの読取と、明示的なvector排出
0x0048CBD3 MOV ECX,[EBP+0x1EEC78]／0x0048CBD9 SUB ECX,[EBP+0x1EEC74]、直後の0x92492493を用いたdivide-by-0x1C最適化、0x0048CBF2 JE 0x0048CF4F（要素0なら処理skip）を原作ASMで確認。
0x0048CBF8 MOV EBX,2 / 0x0048CC01 MOV [ESP+0x20],0x38 の初期値で読取開始し、0x0048CF20 ADD [ESP+0x20],0x8C (=5×0x1C)、0x0048CF34 ADD EBX,5、0x0048CF47 JB 0x0048CC10で次の組へ反復。したがって消費loopは**5要素ごと**に進む。Ghidra擬似Cが示す内部参照と対応するが、レコード全5項目の型・各生成元・端数の合法性はVERIFY。
分岐後処理は0x0048CE5C CALL 0x0052CF50 と 0x0048CF0B CALL 0x0052CCF0（2つの文面処理経路、厳密なUI意味は未確定）。17〜22Hで判明した0x00434B10の**2要素追加**だけで5要素レコード完成と断定しない。残る要素のproducerとevent系列の同一性はVERIFY。
0x0048D2AC/[EBP+0x1EEC78] と0x0048D2B2/[EBP+0x1EEC74]を比較、非空時0x0048D2C2 CALL0x417160、0x0048D2E0..0x0048D306で0x1C刻みの文字列要素を条件付き解放／SSO初期化、0x0048D30C MOV [EBP+0x1EEC78],EAXでendを戻す。**consumer後の排出/再利用**を確認（buffer領域そのもののfreeや保存上限を意味しない）。
## 独立native検証と非重複
原作 capstone x86-32/native PE読取で当該比較・stride・clearを確認。相対E8サイト 0x4B99C0→0x48C880 / 0x48CE5C→0x52CF50 / 0x48CF0B→0x52CCF0 / 0x48D2C2→0x417160 / 0x48D2E8→0x5B6BBB は5/5一致。原作jump table index1=0x4B99B9も実バイト検査。
既存22Hは0x434B10でのappend（+0x1EEC74）と共有8-slot一時文字列だけの報告。今回の新規は **0x48C880 consumer → phase1ディスパッチ → 5-element stride → clear**。PCのB T028*.md/T028_MORALE.md/LANE_B_HANDOFF.mdで0x48c880・0x48ce5c・0x48cf0b等の先行literal一致0。PC外や10/25全文の意味重複は未検証。
## 未同期回収と拒否台帳
PC外で実在する17〜22Hのオフライン研究レポートは6件（17: MERCENARY_ELIGIBILITY_BOOL、18: TYPE2_NESTED_POINTER、19: TYPE2_FIELD_LIFECYCLE、20: ARBEIT_RNG_GATE、21: WANDER_MERCENARY_DUAL_RESULT_SINK、22: ALTERNATE_RESULT_VECTOR_PAIR）。ChatGPT会話添付/LIBRARY側に保存報告・読取可能な添付あり。Windows正本へ全文はまだ同期していない。過去の既安全拒否はそのままBLOCKED、今回は迂回・再投入なし。
今回の回復識別: B-RC-20261028-2315-T028-OFFLINE-17-22H-PENDING-01（CONNECTION RECOVERED、OFFLINE CONTENT STILL UNSYNCED）。旧10/25 14H全文、各17〜22H証拠JSON/検証スクリプト、owner/重複/READYと過去拒否境界の完全照合後に一度だけB担当へ同期する。MASTER統合はE担当。
## GOLDEN / 判定 / 次の調査
原作無改変ver0.67 EXE＋20倍強化前DAT、同一SAVE/MAP/入力/RNGで、flag・phase・記録される全5要素とUI/Unit/Worldの前後を原作で同一run観測するまでGolden NOT RUN。Gameplay Golden PASS=0、strict MATCH=0、新規B READY=0、MASTER統合=0、Task DONE増加=0、NOT READY。
次は0x00434B10の2要素を補う残り3要素producerと、0x0048C880入口に到達するphase=1条件／旧flagとの同一object、0x52CCF0と0x52CF50可視差分を特定。T028士気・敗走本体、T013最終対象選択、T024戦闘AI、T011召喚親子・死亡、T012ダメージ状態のP0は維持。
原本EXE/DAT/ZIP/SAVE、MASTER・他lane・REA・dev_lab・Git・Work・設定・scheduleには書込無し。
