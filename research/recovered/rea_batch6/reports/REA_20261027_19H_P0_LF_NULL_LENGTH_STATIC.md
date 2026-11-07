# 迫真戦記 ver0.67｜REA 19時台 P0：LF-onlyで発生し得る巨大文字列長を後段まで追跡
研究ID：`REA-LOCAL-20261027-19H-P0-LF-NULL-SIZE-STRING-STATIC-01`。状態：PC-SAVED / STATIC / VERIFY / NOT READY。
## 出典・非重複
MASTER・レーン規約・REA README/QUEUE/PROGRESS/最終旧sync・既存18時台成果を読取。既存Wave1〜5 64/64は継続、旧PROGRESS 15/16は古い。旧18時台研究はNULL差分発生の候補までであり、今回は**下流string代入と容量確保・例外経路**を新規に照合した。
承認済みPEコピーSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、統合V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。両SQLiteはread-only/immutableでquick_check=ok、直接CALL siteを照合。
10/21検索CLI `function/callers/callees/related 0x00402800`、`function 0x00402710,0x00402A40,0x00557A20,0x00558CF0`、`strings/symbols`を使用。擬似CはINDEX_ONLY、確認は原作PEのx86 ASMを対象限定で独立逆アセンブル。
## 新規発見：NULL由来の長さが巨大なunsigned countとして後段へ伝搬
既存18時台：LF-only行の場合、ストリームが区切りLFを消費し、`0x00557C6E CALL 0x005B83B0`（_strpbrk）の返却がNULLとなる候補。
**今回の追加**：`0x00557C7D SUB EAX,ECX`は、戻り値NULL=0から行バッファのアドレスECXを32bit減算し、結果を`0x00557C81 PUSH EAX`経由で`0x00557CA4 CALL 0x00402800`へ長さとして渡す。CALLと減算の間にNULLチェック分岐なし。
`0x00402800`は文字列代入相当。新規構築された空文字列の初期容量は15。渡された長さをEDIに受け、`0x0040286A CMP EDI,-2`→`0x0040286D JBE 0x00402879`で通常の巨大長（UINT_MAX以外）を通し、`0x0040287C CMP EAX,EDI`から`0x00402887 CALL 0x00402A40`で容量拡張へ進み得る。
`0x00402A40`ではサイズを調整して`0x00402ABA CALL 0x005B6C2B`（割当候補）へ進み、失敗側には`0x00402AEE CALL 0x005B864E`（C++例外送出候補）がある。つまり、NULL直後に必ずアクセス違反と断定するより、**不自然に大きなサイズでの割当要求／例外**をまず疑うべき構造。
32bitの純粋な算術例：行バッファアドレス`0x0012F000`なら`0 - addr mod 2^32 = 0xFFED1000`。これは実測されたスタックアドレスではない。長さが`0xFFFFFFFF`と一致する特殊条件や、例外捕捉・heap結果は未検証。
## 既存検証と限界
`0x00557C4A/5B`には短い行や空行をスキップする条件がある。LF-onlyかつ正常ストリームで長さ>2の行が実際に問題の`_strpbrk`へ到達するか、例外が上位で捕捉されるか、ゲームがどう反応するかはVERIFYであり原作実機未実測。
スナップショット`a_system/debug_paper.txt`はCRLF×5・最終行改行なし（SHA256 `867E889A74C302F17C1398C2A8311E0C1F305896BC8CBFE43010C8127295B988`）。元の配布設定ではLF-only条件が成立することを示すものではない。
**39/39独立静的監査PASS**。監査条件数と関数数は別。関数別証拠 info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED=0、TODO/VERIFY/BLOCKED正式差分0/0/0、Golden PASS=0、strict MATCH未実施、完全複製率未測定。
## 再開位置
次の優先は`0x00557C4A`に至る入力行長条件と、`0x00402A40 -> 0x005B6C2B/0x005B864E`の例外伝搬・catch境界。Golden候補：CRLF正常、LF-onlyの長さ2/3/10、末尾改行なし、1024byte上限。全件DESIGNED / NOT RUN。
実ゲーム・新REA・Ghidra・Workは起動せず、原本・他レーン・MASTER/QUEUE/PROGRESS・既存RUN・Git/スケジュールは未変更。保存・独立読戻しの最終結果は別READBACKに記録する。CPU負荷は不明、空きRAM事前約11.7GiB、全作業時間未測定。
