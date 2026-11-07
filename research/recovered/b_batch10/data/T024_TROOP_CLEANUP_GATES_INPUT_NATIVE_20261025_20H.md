# T024｜Troop候補整理と入力座標経路からUnit+0x45D解除への入口条件（2026-10-25 20時台）
ID: B-20261025-2008-T024-TROOP-CLEANUP-GATES-INPUT-01
OWNER: B / T024（T028死亡連携は参照のみ）。STATUS: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA-DERIVED / INFERRED / VERIFY / NOT READY。
## 事前監査・証拠源
- Desktop Commander Local Compact接続成功。MASTER checkpoint196/READY596はE側旧正式値（再集計なし）。規約、B全5 owner、B HANDOFFの19HまでのID/拒否/未同期状態、旧search_index README/BUILD_MANIFESTを読取。
- 対象rea_lab/targets/hakushin067_Vahren.exe現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧search.sqlite現物SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF＝manifest。
- 既存Ghidra擬似C source: full_pseudoc_20261020/functions/0056/005684B0.c (356B) / functions/004D/004DE410.c (633B)。今回の主要分岐は上記SHAの原作PEをCapstoneで独立限定逆アセンブルして照合。V3最新guardの今回再実行はなし、前19H PASSは既報。
- active.lock候補2箇所なし、事前Get-Processのjava/javaw/ghidra/Vahren/pythonなし。Ghidra全面再解析・REA・旧原作実行なし。
## 新しい増分A：0x5684B0 の0x527ED0を呼ぶ2経路の到達条件
- この関数の原作PE 356B限定SHA256=3FE540D32DC6819BA79593B389D01EE25E37D6FCC9160D729678E38282FF6E92。0x5684BD CMP BYTE [EDI+0x1D],0 / 0x5684C4 JE0x56856FでTroop様ownerの+0x1Dにより経路分岐。
- +0x1D!=0枝: [EDI+0xC/+0x10]の4Bポインタspanを走査、各Unit+0x1867C!=0の要素では0x5684EBでUnit+0x1867D=0、0x568501 CALL0x5B6720で残部を前詰め、[EDI+0x10]を-4。
- 上記フィルタ後の0x56851C差分に対し0x56851F TEST EBX(=0xFFFFFFFC),ECX／0x568521 JNE0x568539。4B境界整合を前提にspanが空なら0x56852C PUSH EDI→0x56852D CALL0x527ED0。その後は0x568532..38で即ret。
- +0x1D==0枝: 0x56857Bで生存候補countを0初期化、0x568585..59AでUnit+0x1867C==0の要素数を集計。count>0なら先頭Unit+0x8C==0かつ+0x1F8!=0を判定し0x5685C5 JMP0x527EA0、条件を満たさない場合は0x568614側へ終了。0x527ED0経由とは異なる。
- 同枝でcount<=0の場合は0x5685CAでowner+0x1C=1。先頭Unit+0x8C==0かつ+0x1F8!=0なら0x5685F7 PUSH EDI→0x5685F8 CALL0x527ED0。続いてowner+4のglobal+0x1EF140==2なら0x56860F CALL0x4C22B0。空spanでの先頭Unit参照の安全性・実到達条件はVERIFY。
- 2つの0x527ED0 CALLは前19H既知。今回新規は+0x1D別の削除/集計手順、+0x1867C/0x1867D/+0x8C/+0x1F8のgate、+0x1C=1とmode==2後処理の到達条件。
## 新しい増分B：0x4DE410から0x528870への入力・座標gate
- この関数の原作PE 633B限定SHA256=AEB8E6DCD2CC64621DCFDE134B8BF21FAF426FBE485FE15D6DCE9844FEA6919F。0x4DE431 CMP [ECX+0x1EF148],0／JEで無効なら返値EAX=1。0x4DE490 CALL EBX(PtInRect候補)後0x4DE492 EAX==1でなければEAX=6で終了。
- 0x4DE4B0 CMP BYTE PTR [EBP+8],0 / JE0x4DE608によってモード引数0側へ。0x4DE60E CMP [EBX+0x14],0 / JE0x4DE43B（ここではEBX=[ESI+0x9C]）。
- 成立時0x4DE618/639で座標を[ESI+0x198/+0x1A0] doubleで換算し0x4DE62C/641 CALL0x5D1B80、0x4DE64D CALL0x528870。0x4DE652 TEST AL／JE0x4DE670、非0時0x4DE65A MOV [ESI+0x1A8],0xA、0x4DE664 MOV [ESI+0x1AC],ECX、0x4DE66A MOV [ESI+0x1B0],EDI。
- これは前19H既知の0x528870自体の+0x45D解除とは別に、呼出元でのguardとAL成功時のowner座標・状態フィールド更新を接続した静的成果。0x4DE410の直接callersは旧Ghidra索引で0、間接/仮想呼出経路と具体的プレイヤー入力意味はVERIFY。
## 重複・制約・Golden
- B T024/T028/HANDOFF事前literal照合：0x5685CA/0x5684BD/0x4DE608/0x4DE652/0x4DE431/0x5685A1は各資料0 hit。前19Hの0x56852D/0x5685F8/0x4DE64D、+0x45D解除および前17/18H priorityは再計上しない。他lane・Library・オフライン全ID意味重複はVERIFY。
- 未同期：旧14H B-OFFLINE-20261025-1411-T011-COUNTER-REPLACE-ERASE-01 の全文正式同期、10/21回収22+後続10+Library訂正版2のID全照合は未完。13H T013 detailは15H readback回収済。
- Golden必要: 無改変旧EXE・20倍強化前DAT・同SAVE/MAP/input/RNGでTroop+0x1D(0/非0)×Unit+0x1867C(0/非0)×候補数0/1/複数×先頭Unit+0x8C/+0x1F8、別系でglobal+0x1EF148/PtInRect/arg0と+0x14を観測、+0x45D/+0x20C/owner+0x1A8/+0x1AC/+0x1B0の前後・次tick/可視結果を比較。DESIGNED_NOT_RUN。
- 原作Gameplay Golden PASS=0、strict MATCH=0、新B正式READY=0、MASTER統合=0、Task DONE増加=0。関数型/呼出全網羅/例外/破損vector/実AI意味・Unit生成フラグ+0x45D=1はVERIFY。
- 安全: 既拒否（0x5710C0..0x571500ほか）と拒否済み証拠/コマンドを再試行・迂回しない。原本・MASTER・他lane・REA/dev_lab/Git/Work/設定・scheduleを変更しない。
- NEXT P0: 0x527EA0と0x527ED0の状態変更差、Unit+0x1D/+0x1Cのwriterとowner属性、0x4DE410への合法間接caller、0x528870成功時+0x45Dと+0x1A8の次tick連携。