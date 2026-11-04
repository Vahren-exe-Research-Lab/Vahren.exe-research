# 迫真戦記 REA 11H｜Ogg seekコールバックの64-bit引数・seekability判定
研究ID: `REA-LOCAL-20261028-11H-P0-OGG-SEEK-CAPABILITY-ABI-STATIC-01`
状態: PC-SAVED / STATIC / VERIFY / NOT READY。新規正式VERIFIED=0、Golden実測=0。

## 出典と既存成果の非重複
対象コピーEXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
初期検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
先行10H close callback証拠43/43・正式64/64の既存syncを読取照合。旧QUEUE/PROGRESSはEPERMによる古い状態があり、正式集計には利用しない。
旧検索CLI: `function 0x005CFDD0`, `callers 0x005CFDD0`, `callees 0x005D1490`, `function 0x005D1490`。追加独立証拠は隔離コピーPE x86命令デコード、read-only SQLite。

## STATIC-A｜CALLIND 0x005D14ACを実体に結合
`0x005D16F8 MOV EDX,0x005CFDD0` → `0x005D16FD MOV [EAX+4],EDX`。Oggファイルopen経路で登録されたseek callbackが `0x005D1490` に渡る。
`0x005D1497 MOV EBX,[EBP+0x14]` で callback、`0x005D149B MOV EDI,EAX` で datasourceをセット。
CALL site前のpush順序は `0x005D14A5 PUSH 1`, `0x005D14A7 PUSH 0`, `0x005D14A9 PUSH 0`, `0x005D14AB PUSH EDI`, `0x005D14AC CALL EBX`。
x86 cdecl stackから、`seek(datasource, (int64)0, SEEK_CUR=1)` の初期試験呼出し。callerは `ADD ESP,0x10`。
これは固定Ogg open経路の解決であり、すべての動的callbacksを恒常的に断定しない。

## STATIC-B｜0x005CFDD0で64bit offset上位を破棄
`0x005CFDD3 MOV EAX,[EBP+8]` をNULL検査、NULLなら `0x005CFDDA OR EAX,-1` で失敗復帰。
非NULL時は `0x005CFDDF MOV ECX,[EBP+0x14]` (whence)、`0x005CFDE2 MOV EDX,[EBP+0x0C]` (offset下位32bit)。
`PUSH ECX; PUSH EDX; PUSH EAX; 0x005CFDE8 CALL 0x005D1B04 (_fseek)`、`ADD ESP,0x0C`。計34byteの関数全体で `[EBP+0x10]` (offset上位32bit) の参照は0。
従って、このseek wrapperはOgg型の64bit offsetを受けても、CRT `_fseek` へ符号付き下位32bitだけを渡す。2GiB以上の絶対位置や4GiB境界等で互換性上の制約になり得るが、実際のOggファイルでの障害は未観測。

## STATIC-C｜seek失敗は即時のopen失敗とは別
`0x005D14B4` でcallback戻り値を保存し、`0x005D1528 CMP [EBP-4],-1`、-1以外なら `0x005D152E MOV [ESI+4],1`。
失敗やNULL callback時にも初期化処理自体は継続し、seekableフラグは設定されない。
上位 `0x005D167A CMP [ESI+4],0`：非0なら `0x005D167E` からstate=2と追加初期化、0なら `0x005D16A9` からstate=3。後続のheader parse/資源解放まで正常成功を保証するものではない。
`0x005D1B04 (_fseek)` は `whence in {0,1,2}` を検査し、不正ならerrno=22経路、正規経路は `0x005D1B56 CALL 0x005D1A7A`。最終的なOS seekの成功・失敗は未実測。

## 監査・所有権
初期DB: 間接CALL `0x005D14AC` は1件、直接CALL `0x005CFDE8→0x005D1B04` も1件。統合V9のghidra_refsでは間接CALL siteは0件、直接CALLは1件。V9と旧DBは収録範囲が違うので、即座に索引欠落と断定しない。両SQLite `PRAGMA quick_check=ok`。
独立静的監査 **48/48 PASS**、新規正式5証拠パッケージ0、既存正式VERIFIED64維持、新規0、正式TODO/VERIFY/BLOCKED差分0/0/0。
証拠5種：info=INDEX_ONLY / pseudo=INDEX_ONLY+NATIVE CROSSCHECK / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY+CALLBACK REGISTRATION / callees=INDEX_ONLY+NATIVE CALLFRAME。
Golden: DESIGNED / NOT RUN。通常のrb Ogg再open、初期seekが失敗する特殊datasource、2GiB境界を跨ぐseekの成否・返却値・資源解放数を原作と比較する条件。現在実測PASS=0、strict MATCH=NOT RUN、完全複製率=未計測。
安全拒否・接続障害なし、active.lockなし、先行Java/Ghidraなし。REA/Ghidra新規起動0、原作ゲーム実行0、Work不使用。
原本・A〜E・MASTER・T018・既存RUN・QUEUE/PROGRESS・Git・検索DB・スケジュールは未変更。研究記録のみREA所有領域へ新規保存。
次のP0：`0x005D1310` のseekable branchと、`[ESI+0x2C4]` コールバックの後続の実seek CALLINDを辿り、初回試験と通常seekで高32bitが失われる範囲を確定する。Unicode/consoleの `__write_nolock` は別件VERIFYとして継続。
