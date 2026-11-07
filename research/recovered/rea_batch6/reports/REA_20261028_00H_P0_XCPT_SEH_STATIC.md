# REA 2026-10-28 00時台｜P0 CRT例外アクション表とSEH4のC++例外ゲート
研究ID：`REA-LOCAL-20261028-00H-P0-XCPT-ACTIONTABLE-SEH4-CXXGATE-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**（原作ゲームGolden未実行）。
## 根拠と前回差分
23Hの`0x005B8612 CALL 0x005BE999`・SEH4 scope発見を再利用し、今回初めて**CRTの例外アクション表の全12スロット**と、SEH4 dispatcherのC++例外専用分岐を原作PEから独立照合した。
原作EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
初期search.sqlite SHA `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。統合V9 SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
## 新規静的証拠A：CRT既定アクション表
- `0x005BC596 MOV [ESI+0x5C],0x0060B198`は`__initptd`の既定表ポインタ設定。 `0x005BE9AE`で`__XcptFilter`が`[ESI+0x5C]`を読む。
- `0x005BE9BB ADD EAX,0xC`、`0x005BE9BE LEA EDI,[ECX+0x90]`：12バイト×12件の比較。
- PEの`0x0060B198`から全12×12バイトを直接読み、コードは`C0000005, C000001D, C0000096, C000008D..C0000093, C00002B4, C00002B5`。12個のaction初期値は全て0。
- **C++ EH例外コード`0xE06D7363`は既定12件に存在しない**。`0x005BE9D6 XOR EAX,EAX`から不一致は0を返す経路。既定表・通常コード一致比較を前提とした静的判定であり、実動作観測ではない。
## 新規静的証拠B：SEH4 dispatcherはフィルター戻り値で分岐
- `0x005B8612 CALL 0x005BE999`で起動SEH filterが例外コードをCRT分類関数へ渡す。既存両DBはこの直接CALLのsite登録0件のまま。
- `0x005BB769 CALL 0x005C35F2` → `0x005BB772 TEST EAX,EAX` → `0x005BB774 JS`（負）／`0x005BB776 JG 0x005BB7BF`（正）。
- 正の場合だけ`0x005BB7C2 CMP [ECX],0xE06D7363`と条件付き`0x005BB7EA CALL [0x609AF8]`に到達。非正のフィルター戻り値ではこのC++例外オブジェクト破棄分岐を通らない。
- **既定表とC++例外コードの組み合わせでは、当該起動SEH4フィルターの正値catch/handler経路は選択されない**という条件付き結論。別の上位/外部ハンドラー・実行時のテーブル差替・例外伝搬は未確認。
## 精度・限界
独立読取専用native監査 **25/25 PASS**（失敗0、初回1.564秒、証拠保存時1.249秒）。前回23H 27/27とWave1～5 64/64は重複計上せず。
関数別5証拠：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED **0**、5種完全充足 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。新規ローカルVERIFYは既定表の実行時変更可能性と例外伝搬先。
原作Golden PASS **0**／strict MATCH NOT RUN／完全複製率未測定。CPU負荷・全体所要時間は不明、開始時空きRAM約11050MiB、active.lock無し、Java/Ghidra稼働未検出。新規REA/Ghidra/ゲーム起動0、Work不使用。
原本/MASTER/QUEUE/PROGRESS/既存RUN/A～E/Git/公開先/スケジュールは変更しない。REA所有の新規証拠のみ保存。
次回：`0x005B861A`のhandler末尾と`0x005BB625`のunhandledフィルター後続、あるいは`_pxcptacttab`の初期化後書換えxrefsを優先。実機GoldenはDESIGNED/NOT RUN。
