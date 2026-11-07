# REA-20261022-0047-T014-TOKEN-EAX-MINUS1-STATE-PRIORITY-STATIC-01

- 日時: 2026-10-22 00時台 JST。owner REA独立、Task T014/P0、状態 STATIC / VERIFY / NOT READY。既存成果を上書きしない。
- 解析元EXE: 新Ghidra検索基盤のBUILD_MANIFEST記録 SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。今回EXE現物の再hashなし。
- 新検索DB: `search.sqlite`現物 SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、BUILD_MANIFEST一致、SQLite `PRAGMA integrity_check=ok`、約0.962秒。検索CLIのみ使用、Ghidra/REA新規起動0。
- 先読: MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、runs一覧、2026-10-11同期記録、10/21 21:35・22:36・23:39のT014独立報告、10/12保存文字列読込・global scratch監査、10/21 01:33の255byte境界監査。既知の255byte上限/0xFF区分・符号付きASCII判定・取得数は新規カウントしない。
- 根拠A（保存済み正式REA assembly、既存VERIFIEDを再利用）: `runs/20261011T144115307Z/4705F0_procedure_assembly.json`、evidence `ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d`。読取成功。関数0x4705F0のREA5種は既存成果であり、新規には数えない。
- 根拠B（Ghidra12.1.4検索DB機械疑似C、REA VERIFIEDではない）: 0x470980 SHA `850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446`; 0x470AAC SHA `EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D`; 0x4705F0 SHA `86E597D129AFE91C0A27CEF00A3E529B959C5BFCAA1A1B6221DFCDFF0F138889`; 0x42EC60 SHA `BA687A12FA8459739AA47BE9E79DC502205A11B3CBF3DB07972208DA265C7D8F`; 0x426E00 SHA `7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43`。
- 旧runは既に存在（Wave1..5）。`runs`の再帰ファイル名探索では `470980_procedure_assembly.json` の既存証拠0件。これは「当該フォルダに見当たらない」であり、全ての資料に存在しないと断定しない。

## 新たに絞り込んだ重要な条件分岐（1byte reader戻値とtoken読取）

保存済み0x4705F0の**実アセンブリ**は以下の順序を示す。
1. `0x4705F4..0x470600`: global scratch `0xB060F8`を`0x400`バイト零初期化。既報。
2. `0x470610 PUSH EDI; 0x470611 CALL 0x470980` → `0x470616 CMP EAX,-1; 0x470619 JZ 0x470621`。**EAX=-1なら現在の1文字をscratchへ格納せず**、EAX!=-1なら`0x47061B MOV [ESI+0xB060F8], AL`。この呼出元のEAX依存はASM根拠あり。呼出先のABI復元はなお未確定。
3. `0x470621..0x47063B`: 直後にstream stateを読み、下位bit0/1/2のいずれかが立てば`0x470690`のLoadException経路。条件は `(state & 7)!=0`（既報、ASMで再照合）。
4. `0x47063D..0x470645`: その状態検査を通過してから現在位置のscratch byteを検査、0なら正常な終端として`0x470664`へ進む。ゼロ初期化された位置へEAX=-1時には格納しないため、**「呼出先から戻る・EAX=-1・post-call state&7==0」の3条件を仮定した場合、NUL入力と同じ正常終端経路へ入る**。これは局所制御フローの条件付き結論で、原作が実際にEOFでその状態を返す証明ではない。
5. `0x470647..0x470662`: 有効な非NUL byteは符号付き0x20..0x7F検査後、添字を増やし255に達すると次byteを読まず終了（既報、境界挙動を再加算しない）。

## 今回の論理的成果: エラーの優先順位と正常終端条件を分離

次表は**CALLEEから通常帰還したあとの**局所的な条件付き結果である（新しいゲーム動作観測ではない）。

| 0x470980の呼出元から見た戻値 | 通常帰還後のstate | 0x4705F0内の帰結 |
| --- | --- | --- |
| EAX=-1 | `state&7=0` | 格納を飛ばし、零初期化scratchにより**現在までのprefixを正常tokenとして返しうる** |
| EAX=-1 | `state&7!=0` | scratch終端判定より先に**LoadException** |
| EAX=0 | `state&7=0` | 0を格納したうえで**通常NUL終端** |
| EAX=0x41 | `state&7=0` | 'A'を格納し、長さ上限まで反復 |
| EAX=0x80 | `state&7=0` | byte格納後、signed比較で**LoadException**（既知条件） |

- さらに0x470980内部・0x470AACで例外が投げられた場合は、そもそも0x4705F0のEAX/state検査に戻らない。0x470AACは`unaff_ESI!=unaff_EBX`のときsite 0x470AC5→0x426E00を呼ぶ候補。0x426E00はstream例外mask交差でios_base::failureを投げ得る。よって少なくとも**（1）callee例外、（2）callerのLoadException、（3）callerの正常NUL終端**という別々の結果候補を持つ。例外経路の優先度・状態ビットの生成を一括のif文へ単純化しない。
- callee内`0x470AAC`のEAX/ESI/EBX/親フレーム`EBP-0x14`の実値伝播と、`0x470980`が真のEOFで`-1`を返すか、stateを何にするかは未解決。特に**「EOFなら無条件にprefix正常受理する」という主張は不適切**。
- 既報の上限255個の非NUL字を読んだ場合の終端は、EAX=-1でもNUL byteでもない**長さによる第三の終端要因**。今回の追加は「戻値-1が現れたときのstate gateと零初期化scratchの結合」、およびcallee例外を含む優先順位の明示である。

## 追加静的CALL根拠と未解決点
- `0x470611: 0x4705F0→0x470980`（保存REA asm・Ghidra CALL双方）。`0x4709D5: 0x470980→0x42EC60`、`0x4709EF/0x470A2F/0x470A5F/0x470A76: 0x470980→0x470AAC`、`0x470AC5: 0x470AAC→0x426E00`（Ghidra CALL索引）。
- 未解決の間接CALL: `0x4709D0` (CALL EAX、tie候補)、`0x470A1B` (CALL EAX、vptr+0x18候補)、`0x470A66` (CALL EDX、vptr+0x1C候補)、`0x470AE3` (CALL EAX、cleanup vptr+8候補)。実行時vptr/対象関数を確定扱いしない。
- 次のP0: 許可済み既存ASMがあるかownerの既存runs/evidenceで再照合したうえで、0x470980/0x470AACの正常帰還EAXと親EBP-0x14由来、ESI/EBX→0x426E00の入力、およびcallee内throw可否を決着する。既拒否CALL_INDEX_V2照合や0x429620 CLI命令取得を他ツール・経路で再実行しない。

## 検証指標・保全
- 正式REA新規info/pseudo/assembly/callers/callees完全セット0、Evidence ID新規0、REA VERIFIED新規0。旧W1..5: 16+10+10+12+16=64/64（2026-10-11最終保存sync）。Wave6の正式QUEUE登録0件（今回UTF-8 JSON解析で確認）、**候補**TODO12/BLOCKED4/VERIFY0は過去報告値で正式キュー上の状態ではない。正式TODO/VERIFY/BLOCKED差分0/0/0。
- Golden: 実ゲーム0回、旧EXE PASS0、新旧strict MATCH0、再実装率未計測。設計ONLY: valid `A\0`・truncate `A`・immediate EOF・valid255/256byte・0x80を各々、reader戻値EAX・post-call state/mask・gcount・scratch結果・例外型まで別々に観測する。**NOT RUN**。
- PC Local接続成功。decomp_task直下にactive.lockなし。既存Local対話セッション3件は操作・停止しない。2026-10-22 00:46 JSTの簡易計測CPU31%、FreePhysicalMemory=14592564KiB（約13.92GiB）。Java/Ghidra process0、新REA/Ghidra実行0秒、調査総所要時間は未計測。
- 診断: PowerShell `ConvertFrom-Json`による旧QUEUE読取は環境の文字化けでパースエラー。その後Python標準`json.loads(...,encoding=utf-8)`でread-only解析に成功。区分TOOL_FAILURE_RECOVERED、SAFETY_REFUSALではない。旧QUEUE等は変更なし。
- 旧原本ZIP/EXE/SAVE、A〜E、MASTER/T018/dev_lab、QUEUE/PROGRESS、既存runs/evidence、Git/公開先/スケジュールは一切変更しない。REA owner配下への本独立新規報告のみ保存、既存IDや正式VERIFIEDを重複加算しない。
