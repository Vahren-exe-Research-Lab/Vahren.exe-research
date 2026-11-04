# REA-LOCAL-20261023-1942-P0-PERSON-STATE4-WRITER-STATIC-01
日時: 2026-10-23 19時台 JST。owner=REA、対象=T010/T012（P0）、状態=PC-SAVED / READBACK VERIFIED / STATIC / VERIFY / NOT READY。
## Source / preflight
- Desktop Commander Local CompactでMASTER・解析規約・REA README/QUEUE/PROGRESSと前回18時台MD/JSONを先読。保存済み進捗同期 logs/progress_sync_20261011T153958076Z.json はWave1-5=64/64、queueUpdate=STALE_RENAME_DENIED。raw PROGRESS=15/16の旧表示。修正せず。
- 承認済み原作研究コピー rea_lab/targets/hakushin067_Vahren.exe の実バイトSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 現行検索の出典は統合V9 HAKUSHIN067_UNIFIED_V9_20261023.sqlite、SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。既存verify=V9_INDEPENDENT_READBACK_PASS（functions 11950）。PC既定検索CLIはV3のまま。
- 研究PCのactive.lock=false、新ファイル同名なし、Java/Ghidra検出なし。REA所有REA_*.mdの対象VA 0x44CF80/0x44CF8E/0x44B5EA/0x44CF57検索結果0。PC空きRAM約15.12GiB/総30.78GiB（瞬間値）、CPU/作業全所要時間未計測。
## 今回の新規証拠：状態コード4への直接書込元を追加特定
- 前回確定済みの0x005146E0=MOV EAX,[ECX+0x20];RET（DemoPerson等のvslot+0x18 state getter）および0x40E644/0x40E658・return1/2/500反復は既存成果であり二重加算しない。
- 新規状態writerは関数入口0x0044CF80（0x0044CF8Eは関数内部でありentryではない）。Ghidra V9疑似Cと原作PE32 x86のCapstone独立実バイトを照合。
- 0x0044CF80 80BBA500000000 = CMP BYTE PTR [EBX+0xA5],0。0x44CF88 751B = JNE 0x44CFA5（条件が非0ならstate書込を飛ばす）。
- 0x44CF8A 807B1800 = CMP BYTE PTR [EBX+0x18],0。0x44CF8E C7432004000000 = MOV DWORD PTR [EBX+0x20],4。このstate=4は+0xA5==0なら+0x18の値にかかわらず実行する。
- 0x44CF95 750E = JNE 0x44CFA5。+0x18==0のときのみ0x44CFA0 E8 CALL 0x0049D1B0を実行する。その後、+0x48/+0x4Cおよび+0x38/+0x3Cのvector処理へ進む。
- V9 PE検証済みE8 callersは4箇所: 0x44AEBF（owner 0x44AE70）、0x44B700（0x44B240）、0x44C705（0x44BBB0）、0x44CF3E（0x44CD70）。unaff_EBXを利用するhelperであり通常C ABIと決め打ちしない。
## 関連する同一+0x20 state書込（今回独立ASMで確認）
- state=1: 0x44C789 C7432001000000（owner 0x44BBB0）。state=2: 0x44B7B0 / 0x44CF57 各 C7432002000000（owners 0x44B240 / 0x44CD70）。
- state=3: 0x44B5EA / 0x44B730 / 0x44CE60 各 C7432003000000（owners 0x44B240 / 0x44CD70）。state=4: 0x44CF8E（owner 0x44CF80）。
- 動的state=1または2の式に接続する候補: 0x44B0BF MOV [ESI+0x20],EDX、0x44B1A5 MOV [ESI+0x20],ECX（owner 0x44AE70）。Ghidra疑似Cでは比較式の真偽+1だが、FPU/乱数/呼出規約は未監査。
## 重要な解釈制限
- この直接writer群が前回0x0040CCF0生成の2つのDemoPersonインスタンスへ動的に実際に到達するかは、継承・具体caller・オブジェクト寿命を最後まで追っていないためVERIFY。共通Person系+0x20 state layoutと静的整合するだけで到達性を保証しない。
- 状態4は「stateフィールドが4」と判明したのみ。勝利、敗北、撤退、戦闘終了などのゲーム語彙は未確定。0x44CF80の+0xA5および+0x18の意味も未確定。
- PE .textの汎用[reg+0x20] writer列挙は別型への書込を多数含む。Ghidra疑似Cは元ソースではない。全writerの列挙完了を宣言しない。
## 検証・正式進捗・次回
- 独立read-only検証: state即値7件 + 動的state命令2 + 分岐等5 + E8直接CALL5 = 19/19 PASS、原作実バイト／RVA→offset／E8相対先をPython pefile/structで照合。新Ghidra/REA 0、旧EXE実ゲーム実行0。
- 公式info/pseudo/assembly/callers/callees 5証拠セット新規完成0、正式新VERIFIED0。既存Wave1-5 64/64据置、正式TODO/VERIFY/BLOCKED書込差分0/0/0、実機Golden PASS0、strict MATCH0、完全複製率未測定。
- 既存原本ZIP/EXE/SAVE、MASTER、A-E、QUEUE/PROGRESS、runs/evidence、他owner、Git、Work、UI/操作、スケジュールは変更しない。過去安全拒否を再試行しない。
- 次P0: 0x44AE70/0x44B240/0x44BBB0/0x44CD70のEBX receiver originを原作ASMで追ってDemoPerson実体への到達を検証し、+0xA5/+0x18の定義とstate4→結果1/2への動的可到達性を分離する。続いてBattleWnd +0x28 vslot+0x04の実行時CALL siteを研究する。
