# REA-LOCAL-20261024-0043-P0-DEMOPERSON-PAIR-INIT-ABI-STATIC-01
- 日時: 2026-10-24 00:43 JST / owner=REA / P0=T010/T012 / PC-SAVED-PENDING-READBACK / STATIC / VERIFY / NOT READY。
- 対象: 承認済み研究専用コピー rea_lab/targets/hakushin067_Vahren.exe。今回SHA256実測 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 索引: HAKUSHIN067_UNIFIED_V9_20261023.sqlite SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。verify V9_INDEPENDENT_READBACK_PASS、functions=11950、refs=243678、標準検索はV3のまま。
- 事前照合: MASTER/ANALYSIS_LANES_PROTOCOL/REA README・QUEUE・PROGRESS・旧runのsync・23H MD/JSON/readback・V9入口。22H/23H成果の二重計上なし。
## 今回新規：DemoPerson主vtable +0x08 の両陣営交差初期化 ABI（機械語確定）
- DemoPerson主vtable 0x00638030、slot +0x08 は 0x00638038にある32bit pointer 0x00514A80（研究コピーPE実バイト独立確認）。
- 0x00514A80 は31byte関数。0x514A80 MOV EAX,[ESP+4] / 0x514A84 MOV DL,[ESP+8] / 0x514A88 [ECX+0x14]=EAX / 0x514A8F [ECX+0x18]=DL / 0x514A92 [ECX+0x1C]=[ESP+0xC] / 0x514A95 [ECX+0x20]=0x64 / 0x514A9C RET 0x0C。
- ABI（この特定関数に限る）: ECX=this、stack[+4]=source pointer、stack[+8]の下位8bit=側識別値、stack[+0xC]=相手DemoPersonポインタ、callee側RET 12で3引数を掃除。V9 GhidraはABI未認定のためASMを優先。
- 0x0040F3BC MOV EAX,[0x008B8E5C] → 0x40F3C1 ECX=[0x008B8E58] → 0x40F3C9 EDX=[[ECX]+8] → PUSH EAX → PUSH 0 → PUSH [0x008B8E60] → 0x40F3D6 CALL EDX。
- 第1呼出がDemoPerson型であれば: this=[0x008B8E58]、[this+0x14]=[0x008B8E60]、[this+0x18]=0、[this+0x1C]=[0x008B8E5C]、[this+0x20]=100。
- 0x40F3D8 EDX=[0x008B8E58] → 0x40F3DE ECX=[0x008B8E5C] → 0x40F3E6 EAX=[[ECX]+8] → PUSH EDX → PUSH 1 → PUSH [0x008B8E64] → 0x40F3F3 CALL EAX。
- 第2呼出がDemoPerson型であれば: this=[0x008B8E5C]、[this+0x14]=[0x008B8E64]、[this+0x18]=1、[this+0x1C]=[0x008B8E58]、[this+0x20]=100。
- **新規差分**: 2オブジェクトが相手ポインタを+0x1Cに交差保持し、+0x18の設定値は0/1と非対称、+0x20は両側とも100に初期化する。23Hではvtable slot存在のみ既知で、引数/RET 12/書込先/交差参照は今回初確認。
- 同関数の直接E8 callerをV9で検索すると0件。これは未使用の証明でなく、上記2つが間接CALLだから。関数入口・命令列・呼出点を直接機械語と突合。
## 状態4と比較する際の注意
- 既存0x005146E0は[this+0x20]の32bit値を返し、既存0x0044CF80は条件付きで+0x20へ4を代入する。今回の100は初期化値として確認したもので、HP/勝敗の意味や遷移順序は断定しない。
- +0x18は後続の0x00447810で分岐材料、0x0044CF80では状態4書込後の追加CALL条件として使用。初期化時に第1=0、第2=1という差異があるため、両側を同一フラグ値で再実装しない。
- sourceの+0x14は0x40F383の0x00597B00戻り値（0x008B8E60へ保存）/0x40F398の0x00583C70戻り値（0x008B8E64へ保存）。両返り値のゲーム上の型はVERIFY。
- 呼出順は0x40F320内の命令配置で第1→第2の順。より上位の呼出元は0x40D0A0のE8 CALL site 0x40D0C6。全戦闘におけるruntime順序/例外時/別型vtable差替え・寿命は未実測。
## 検証と進捗
- 原作PEのRVA/raw変換後Capstone disasmを実施。関数0x514A80と呼出元0x40F3xxの指定機械語バイト35/35 PASS、PE vtable pointer 1/1 PASS、元EXE SHA 1/1 PASS、V9 DB verify PASS。35/35は指定命令照合件数であり関数全経路の網羅ではない。
- V9: callers 0x514A80 直接E8=0、callers 0x40F320 は0x40D0C6→0x40F320 1件。原作Golden実機0 / strict MATCH0 / 完全複製率未測定。
- 既存REA Wave1～5は旧保存ログ logs/progress_sync_20261011T153958076Z.json で64/64=16+10+10+12+16。queueUpdate=STALE_RENAME_DENIED。今回新規正式info/pseudo/assembly/callers/callees 5方法フルセット0、新VERIFIED0、TODO/VERIFY/BLOCKED正式書込差分0/0/0。
- 2026-10-24 00:43 JST事前確認 CPU LoadPercentage=74%、空きRAM=8.21GiB、Java/Ghidra検出0、active.lockなし。高負荷・MEA/REA版差・Wave6拒否・QUEUE/PROGRESS EPERMのため新REA/Ghidra起動0。ゲーム起動0、全作業時間未計測。
## Golden条件の設計（全NOT RUN）
- 両DemoPersonを新規生成するケースで、主vtable +0x04後に+0x08両側実行→第1(+0x18=0)/第2(+0x18=1)、+0x1C相互参照、+0x20=100を同run/同時点で観測する。旧原作の合法な観測・捕捉が得られるまでPASSとしない。
- 片側を既存ポインタとして再利用した時、主vtableのruntime型の違い、初期値上書き、+0x0C初期化の影響、状態4への遷移を区別して実測する。
- +0x20が100→4となる条件、+0x18=0/1で0x44CF80付随CALLが異なる条件、シミュレーションの戻り値0/1/2と結果反映を同一戦闘の系列で比較する。
## 調査の限界と安全措置
- 仮想CALLはFF D2/FF D0。これは5byte直接E8 CALLフックではない。実測ABI、オブジェクト同一性、実際のクラス替え、寿命、成功復帰条件はなおVERIFY。
- 本回の一時Python read-only試行1件で日本語パスの標準入力encodingによるOSError22（OTHER）。環境変数を経由した通常の読み取りで成功。SAFETY_REFUSALは発生しておらず、拒否操作の迂回なし。
- 保存範囲: REA所有の新規固有名レポート/証拠のみ。原本ZIP/EXE/SAVE、MASTER・A～E/T018、旧QUEUE/PROGRESS/RUN、Ghidra DB、Work/dev_lab、Git、スケジュール不変更。
- 正式Wave6に未登録の禁止候補4VA、禁止0x5710C0..0x571500、拒否済REA抽出や既拒否コード作成には非介入。
- 次P0: 0x40F320の主vtable +0x0C両側CALL site 0x4103D5/0x4103E2が+0x20=100の直後に何を変更するかを静的に追跡。0x40D0A0の入場呼出しと0x40E2F0更新時の+0x18/peer参照を別証拠で照合。
- 読み戻し待ち: 本ファイルと機械可読JSONを新規保存し、別操作で存在・内容・SHAを独立再読取後に別receiptで最終確定する。
