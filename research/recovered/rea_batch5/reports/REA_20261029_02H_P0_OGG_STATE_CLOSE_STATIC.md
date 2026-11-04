# 迫真戦記 REA 2026-10-29 02H｜Ogg state=-131 と FILE* close callback ABI 静的照合
研究ID: `REA-LOCAL-20261029-02H-P0-OGG-STATE131-CLOSE-ABI-STATIC-01`
判定: **PC-SAVED / STATIC / VERIFY / NOT READY**（原作ゲームGolden実測0、新規正式VERIFIED0）
## 既存成果との差分
- 前回01H: `0x005D16C0` が fopen→`0x005D1630`→失敗時fclose、decoder解放は `0x005CFE00`、resetは `0x00501EB0` と判明済み。16H以降のメモリ確保失敗、21/22Hの一時配列所有権、23HのNULL書き込み候補は再計上しない。
- 今回は**-131分岐の到達可能性**と**間接close呼出し`0x005CFEEE`の具体的な引数・ABI・return処理**を、旧検索DB/前回01H証拠/原作PEネイティブ命令で独立クロスチェックした。
- EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`；旧検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。前回01H証拠SHA256 `BE999B20127FB132E38290E282C38203C2E694A63B5AE752383738C86D365431`。
## 発見A｜-131は通常正常returnから実質到達不能
- `0x005D1490`の`0x005D1572 CALL 0x005CF010`の戻り値をEDIへ保存。`0x005D1582 TEST EDI,EDI`→`0x005D1584 JNS 0x005D1597`。負値時には`0x005D1587`でdecoder FILE*を0、`0x005D158D`で内部cleanupし`0x005D1595`からreturn合流、負値を返す。
- 非負値経路では初期配列を確保・初期化した後、`0x005D1609 MOV [ESI+0x58],1`。正常returnは`0x005D161D MOV EAX,EDI`。よって**return=0なら通常命令列ではdecoder+0x58が1にセット済み**。
- 上位`0x005D1630`は`0x005D165F`で下位を呼び、`0x005D1667 TEST EAX,EAX`→非0なら即return。0のときだけ`0x005D166B CMP [ESI+0x58],1`を実行し、不一致で`0x005D1671 MOV EAX,0xFFFFFF7D`（-131）を返す。
- したがって**-131は通常のvalid decoder状態・正常return経路からは到達しない整合性チェックと判定**。下位から上位へ渡す途中の不正メモリ書込、オブジェクト別名、外部スレッドによる変更、異常malloc/例外処理などは排除できない。ゲームで-131が出ないと断定するものではない。
## 発見B｜close callbackの一引数cdecl相当ABIと戻り値破棄
- `0x005D1701 MOV ESI,0x005B7A4E`（保存索引で`_fclose`、VS2010 CRT）、`0x005D170B MOV [EAX+8],ESI`でov_callbacksのcloseスロットへ設定。`0x005D14EE MOV [decoder+0x2C8],ECX`でDecoderへ転写。
- `0x005CFE00` cleanup末尾は`0x005CFEDF TEST ECX,ECX`（FILE*非NULL）と`0x005CFEE3 MOV EAX,[ESI+0x2C8]`→`0x005CFEE9 TEST EAX,EAX`の両条件で呼出しを制御。`0x005CFEED PUSH ECX`、`0x005CFEEE CALL EAX`、`0x005CFEF0 ADD ESP,4`のため**引数はFILE*一つ、caller cleanup 4バイト**であり既知`_fclose(FILE*)`のcdecl ABIと整合する。
- `0x005CFEF3`以後はdecoder領域`0x2D0`バイトのzero-fillへ進み、通常return値は0。**close callback戻り値を呼出し元へ伝える分岐は無い**。fclose自体の失敗が上位へ伝播するかは別レイヤー検証が必要だが、本cleanupは伝えない。
## 発見C｜オブジェクトflagによる二重close回避境界
- `0x00501EB0` resetは`0x00501EB4 CMP BYTE PTR [ESI+5],1`で、1の場合だけ`0x00501EC1 CALL 0x005CFE00`、それ以外では0x2D0バイトを無条件zero-fillする。
- `0x00502020`では先にresetし、`0x00502038 CALL 0x005D16C0`。非0return時は`0x00502046 XOR AL,AL`で偽、成功時だけ`0x00502085 MOV BYTE PTR [ESI+5],1`。
- この組合せは、**失敗時に外側wrapが閉じたFILE*を次のresetで再度閉じない**ことと整合。途中状態破損ではdecoderのリソースが残ったままzero-fillされる可能性は別途VERIFY。
## 静的証拠、監査と進捗
- 情報源: 10/21 Ghidra `search.py function` 0x005D1630/0x005D1490/0x00501EB0/0x005CFE00/0x005B7A4E/0x005D16C0、`related --depth 2 --limit 30`、PE native Capstone、read-only SQLite CALL 9本、01H証拠。
- 54/54 PASS: PE native指定命令39件・旧DB直接CALL 9件・EXE/DB/01Hハッシュとロック・旧64/64同期ログ・SQLite quick_check。これは**検査数であり解析関数数ではない**。
- 5種証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY+TARGETED_NATIVE_CROSSCHECK、assembly=TARGETED_PE_NATIVE、callers/callees=INDEX_ONLY+PE_CALLSITE_CROSSCHECK。新規5種完全パッケージ0、新規正式VERIFIED0。既存正式Wave1〜5=64/64（2026-10-11 syncログ、QUEUE/PROGRESSはEPERM古値）。
- 正式TODO/VERIFY/BLOCKED差分=0/0/0。新規の独立VERIFYは「異常なstate==0などで-131が実行される条件」と「close callback失敗の上位への伝播」の**既存FILE寿命問題の精密化**として一群にまとめ、故障件数を増やさない。
- Golden原作実測PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。新Ghidra/REA、ゲーム、Workを起動しない。原本/他owner/MASTER/QUEUE/PROGRESS/Git/公開先/スケジュールは変更しない。
## Golden条件案と次の優先関数
- DESIGN/NOT RUN: 正常Ogg成功→flag1→resetでclose一回；fopen失敗→flag0→resetでcloseなし；索引初期化失敗→内部でFILE*ゼロ化→外側でfclose一回；異常内部state強制による-131分岐；close callbackのエラー返却の観測。**いずれもゲーム実測PASSに算入しない**。
- 次のP0は`0x005D1490`初期化内の残存異常分岐、`0x005D1630`のstate+0x58に対する代入者のxrefs・`0x00501EB0`の派生型vtable/flag条件を絞り込む。新規REA実行は正式手続き/資源確認が揃う場合のみ。
- 10/28 17～22HのLibraryオフライン成果は未同期。最新版既存ID/owner/lock/ハッシュを照合するまで統合しない。

