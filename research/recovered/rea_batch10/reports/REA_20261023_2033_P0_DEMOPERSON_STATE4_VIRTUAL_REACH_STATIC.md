# REA-LOCAL-20261023-2033-P0-DEMOPERSON-STATE4-VIRTUAL-REACH-STATIC-01
日時: 2026-10-23 20時台 JST。owner=REA、関連T010/T012（P0）、状態=STATIC / VERIFY / NOT READY。PC-SAVED / READBACK VERIFIED（本報告とJSONを別読取で照合済）。
## 先読・出典・重複照合
- Local Compact接続成功。MASTER/解析規約/REA README・QUEUE・PROGRESS・既存同期ログ・19時台MD/JSON・V9入口をread-only確認。承認済み研究コピーEXEの今回SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 統合V9 SQLiteの今回SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、独立verify実行exit0 / V9_INDEPENDENT_READBACK_PASS。functions=11950、refs=243678。標準ポインタV3のまま、上書きなし。
- 既存19時台の0x44CF80状態4 writer/4 caller、18時台のDemoPerson+0x20 state getter、17時台のBattleWnd・16時台の500反復は既発見として非重複。本件の新規差分は **DemoPerson由来のvirtual更新入口から既writerへの静的連結を証明**、state4で飛ばす分岐を確定したこと。
## 新規P0証拠1：DemoPersonとEnemyの+0x90副vtable／更新入口
- 0x0040CD69・0x0040CDC4: どちらも C7869000000054806300 = MOV [ESI+0x90],0x00638054。前回の0x0040CCF0で条件付き生成される0x188-byte DemoPerson二実体の副vptr初期化である。
- PE実データ: DemoPerson secondary vtable=0x00638054、vptr-4=0x0063C604 (RTTI COL)、COL+4のsubobject offset=0x90。slot+0=0x0044D8E0、**slot+4=0x00449730**（pointer cell 0x00638058）。
- Enemy secondary vtable=0x00638B84、vptr-4=0x0063D708、RTTI subobject offset=0x90。slot+0=0x0044D8E0、**slot+4=0x004498E0**（pointer cell 0x00638B88）。DemoPersonとEnemyはこの副vfuncの実装が異なる。
## 新規P0証拠2：副オブジェクトthisの-0x90補正で状態writerに繋がる
- DemoPerson vfunc 0x00449730: 0x44973D MOV EDI,ECX。0x4498B8 LEA ESI,[EDI-0x90] → 0x4498BE CALL 0x44AE70 → 0x44AEBD MOV EBX,ESI → 0x44AEBF CALL 0x44CF80。
- 同じDemoPerson vfuncの別分岐: 0x449880 LEA EAX,[EDI-0x90] → 0x449886 CALL 0x44CD70 → 0x44CD74 MOV EBX,EAX → 0x44CF3E CALL 0x44CF80。
- writer 0x44CF8E MOV DWORD PTR [EBX+0x20],4 は既確認の 0x44CF80+0xA5==0 gate下の命令。よって副vfuncに正規のthis=object+0x90が渡り、対応する分岐を通る**静的経路**では、対象はそのDemoPerson主オブジェクト+0x20まで追跡できる。
- Enemy vfunc 0x4498E0: 0x4498ED MOV EDI,ECX、0x44A097 LEA ESI,[EDI-0x90]→0x44A0A3 CALL 0x44AE70、0x44A11C LEA EAX,[EDI-0x90]→0x44A122 CALL 0x44CD70。Enemyも同じwriterへ到達する**条件付き静的経路**を持つ。
## 新規P0証拠3：DemoPersonの状態4は当該更新分岐を通さない
- 0x449870 MOV EAX,[EDI-0x70] はthis=obj+0x90ならobject+0x20を読む。0x449876 TEST EAX、0x449878 JE 0x44988Dでstate0を0x44AE70へ送る。
- state非0なら0x44987A DEC EAX→0x44987B CMP EAX,2→0x44987E JA 0x4498C3。すなわちstate1..3は0x449886→0x44CD70へ進めるが、**state4ではJAが成立してその経路をskip**する。0x4498C3の共通0x44A260後処理までは残るので「フレーム更新全体が止まる」とは言わない。
- 同じstate getter 0x005146E0 MOV EAX,[ECX+0x20] が0x40E644/0x40E658経由でstate4を比較することは既発見。今回の新規解明は「生成DemoPerson→副vtable→更新→state4 writer→更新分岐skip」の**構造的な接続**である。
## 検証・非確定・再開位置
- 独立原作PE32/Capstone確認で指定命令27/27 bytes+asm一致、二つの副vtable pointer/RTTI構成8/8一致。V9直接caller索引0x44CF80=4件、0x44AE70=2件、0x44CD70=2件と対照。合成実行ではなく原作実バイトの静的証拠。
- 未確定：実行時に当該仮想スロットが呼ばれるCALL site、DemoPerson二実体が全条件で生成されること、state4到達時の実ゲーム状態、0xA5/0x18の意味、state4と攻防勝敗の語彙対応、vptr変更と寿命。**STATIC PATH != DYNAMIC OBSERVED**。
- REA新起動0/Ghidra新起動0、正式5証拠(info/pseudo/assembly/callers/callees)新規完全組0、新規VERIFIED0。既存Wave1-5 64/64はlogs/progress_sync_20261011T153958076Z.json由来、QUEUE/PROGRESSのEPERM stale残存・正式TODO/VERIFY/BLOCKED変更0/0/0。原作実機Golden PASS0、strict MATCH0、複製率未測定。
- 保存前負荷一時観測CPU4%、空きRAM15.34GiB/総30.78GiB、Java0、active.lockなし。全体所要時間は未計測。原本/MASTER/A-E/QUEUE/PROGRESS/既存runs/Work/dev_lab/Git/UI/スケジュールは無変更。
- 次P0: DemoPerson +0x90 slot+4 に到達する実行時indirect CALL siteの同定と、0x44A1A0/0x514740を経由する初期state+0x20、0xA5/+0x18の型/書込元を追跡。原作GoldenはE-ownerと区別しNOT RUN維持。
