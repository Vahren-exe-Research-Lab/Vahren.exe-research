# REA-20261022-0337-T014-GLOBAL-SAV-EDI-IDENTITY-ABI-STATIC-01
- 日時: 2026-10-22 03時台 JST。owner: REA独立、対象T014。REA内P0・MASTER上は別優先。状態 STATIC / VERIFY / NOT READY。既存0234の疑義をASMから進展させた独立証拠（旧成果上書き無し）。
- 原EXE source SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（保存済みmanifestとREA証拠由来。今回現物未再hash）。
- DB現物 SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、BUILD_MANIFESTと一致。SQLite ro+immutable integrity_check=ok、関数10456（内部10268/外部188）。
- 先読: MASTER、evidence/ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、最新20261011T153958076Z sync、既存runs/4705F0 assembly、REA_20261022_0234/0137/0047。既知情報を新規VERIFIEDへ二重加算しない。
## 新規差分1：global.sav親関数の同一stream objectを実ASMのESP相対アドレスで解決
- 読取専用元: `exe/T014_GLOBAL_DISASM.txt` SHA256=165AA4FE07A8F7B7AE392B5CB962365947DC076758D08D5F324DAAC0C78F94A2。`exe/T014_CODEC_HELPERS.txt` SHA256=FF408CCC2E2700D184EB37E9BA17ADCCA10C4EAAEC5C73A0FAD8459D38FC1187。
- 基準S1=0x4282DF時ESP。`0x4282E6 PUSH ECX`後の`0x4282E7 LEA EDX,[ESP+0x48]`は S1+0x44。`0x4282EB PUSH EDX`→`0x4282F4 CALL 0x429C60`がctor第1引数にそのポインタを渡す。
- `0x429D25 RET 8`を保存済ASMで直接確認。ctorは2スタック引数をcallee-cleanupし、通常帰還後ESP=S1に戻る。以後readerまでの`PUSH 0x30`は`ADD ESP,4`で均衡する。
- `0x4283A2 PUSH EAX`後の`0x4283A3 LEA EDI,[ESP+0x48]`=S1+0x44、直後`0x4283A7 CALL 0x4705F0`。`0x42843B PUSH ESI`後の`0x42843C LEA EDI,[ESP+0x48]`=S1+0x44、直後`0x428444 CALL 0x4705F0`。**両方ともctor第1引数と同一アドレス**。
- 基準S2=0x428A07時ESP。`0x428A0E PUSH ECX`後の`0x428A0F LEA EDX,[ESP+0xF0]`=S2+0xEC、`0x428A17 PUSH EDX`→`0x428A1F CALL 0x429C60`。
- 通常帰還後ESP=S2。`0x428AD7 PUSH EAX`後の`0x428AD8 LEA EDI,[ESP+0xF0]`=S2+0xEC→`0x428ADF CALL 0x4705F0`。`0x428B73 PUSH ESI`後の`0x428B74 LEA EDI,[ESP+0xF0]`=S2+0xEC→`0x428B7F CALL 0x4705F0`。**こちらも両token読込はctor第1引数と同一アドレス**。
- 以上は親2関数・token CALL4箇所の通常実行経路における**スタックオブジェクト・アドレス同一性のASM静的証明**。例外分岐・破壊的memory overwrite・途中vptr変更不存在までは証明しない。
## 新規差分2：Ghidra疑似Cの引数復元の具体的誤差
- `0x429C60`のGhidra擬似C宣言は`int *FUN_00429c60(int *param_1)`だがASMは`MOV EBX,[ESP+0x28]`/`MOV EDI,[ESP+0x2C]`、親側は2回PUSH、末尾は`RET 8`。**最低限、2つのスタック引数を取るABI**であり1引数の擬似C宣言を関数ポインタ型に流用しない。第2引数の意味はVERIFY。
- `0x4705F0`はGhidra上`void FUN(void)`だが、親側は`PUSH 出力先`＋`LEA EDI,stream`、既存REA ASMは`0x47067A MOV ECX,[ESP+0x14]`で出力先を読み、`0x470621 MOV EAX,[EDI]`でstreamを参照し、`0x47068F RET`。**EDI暗黙stream＋caller-cleanupの1stack出力先引数**。C標準呼出規約名までは確定しない。
- 既存正式REA asm `runs/20261011T144115307Z/4705F0_procedure_assembly.json` SHA256=ABFEC03B75063AED83FFA49B5D95B06D964E940C745DC60AA9A4CBAE062E821F、既存 Evidence ID=ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d（再利用のみ）。
- ctorの`0x429CC8 LEA EBP,[EBX+0x10]`、`0x429CCC MOV [ESI+0x38],EBP`、`0x429D03 PUSH EBP`→`0x429D0B CALL 0x42A7A0`はbuffer subobjectとの連鎖を補強。ctorの初期stringbuf vptr=0x0063848Cは旧0137既知、追加VERIFIED扱いにしない。
## xrefs・ABI・残る検証
- Ghidra検索CLI callers 0x4705F0 から上記4サイトを再照合。callees 0x429C60 は`0x429D0B→0x42A7A0`、related 0x470980 depth2 は`0x470611→0x470980`、`0x4709D5→0x42EC60`、`0x4709EF/0x470A2F/0x470A5F/0x470A76→0x470AAC`。CLIはread-only。
- ABI静的到達点: global.sav親2つ→同一stack stream address→EDI implicit token reader→`0x470610 PUSH EDI`→0x470980。間接CALLスロット+0x04/+0x08/+0x18/+0x1Cの実指先は未解決。動的vptr不変性、EOF時state、0x470980戻値/終了ABIはVERIFY。
- 正式5種(info/pseudo/assembly/callers/callees): 0x4705F0の既存証拠を流用、今回の0x428010/0x428710/0x429C60/0x470980新規完全セット=0、Evidence ID新規=0、REA VERIFIED新規=0。古いWave1～5=64/64はprogress_sync既存値。Wave6正式登録0、候補TODO12/BLOCKED4/VERIFY0は前回報告値、今回の正式状態差分0/0/0。
- Golden原作実機PASS=0、strict MATCH=0、再実装率未計測。設計のみ: global.sav読込の複数tokenで同一stream address/streambuf vptr観測、正常/短EOF/invalid byteを比較（NOT RUN）。
- 環境: Local接続成功、開始時owner直下active.lock無し、他のLocalセッション3件は不干渉。DB整合性PASS、FreePhysicalMemory=12609480KiB、CPU値取得不能。新規Ghidra/REA起動0回、実行0秒、調査総時間未計測。新規安全拒否0件。
- 原本ZIP/EXE/SAVE、MASTER、研究A～E、T018、dev_lab、QUEUE/PROGRESS、既存RUN/evidence、Git/公開先/スケジュール無変更。本新規ファイルだけREA ownerへ保存。保存後独立readbackとSHAを別途検証。
- 次のP0: 0x470980の正式既存許可証拠を再点検し、`0x470610 PUSH EDI`で渡したstream引数の扱い/ret4、0x470AAC正常帰還とstate bit更新をASMで照合。vtable slotsのtargetは非推測で別証拠待ち。拒否済みCALL_INDEX_V2/0x429620/Wave6/REA-exportは再試行・迂回禁止。
