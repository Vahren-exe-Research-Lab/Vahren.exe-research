# REA 2026-10-28 04H｜P0 CRT通常終了コールバックとストリーム後始末
研究ID: `REA-LOCAL-20261028-04H-P0-CRT-STREAM-FLUSH-CALLBACK-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。ゲームGolden実測0。REA新規正式VERIFIED 0。
原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
初期索引 SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。統合V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 先読・非重複
MASTER・owner規約・REA README/QUEUE/PROGRESS、保存済64/64同期、検索DB manifestと旧03H監査38/38を確認。前回は通常終了領域`0x00609674`に`0x005BDAB1`が登録される点まで。今回はその先の関数本体・副作用・索引差を独立検証し、既存発見を二重計上しない。

## STATIC A｜通常終了の関数0x005BDAB1
原作PEの`0x00609674`のDWORDは`0x005BDAB1`。当該入口から`0x005BDAD0 RET`までの原作x86機械語を独立読取した。
- `0x005BDAB1 CALL 0x005BD9F7`：毎回`__flushall`を呼ぶ。
- `0x005BDAB6 CMP BYTE PTR [0x0068DFD4],0`、`0x005BDABD JE 0x005BDAC4`：フラグが非0の場合のみ`0x005BDABF CALL 0x005CA6DB`（`__fcloseall`）。
- `0x005BDAC4 PUSH [0x00B13A00]`、`0x005BDACA CALL 0x005B71E8`：CRT FILE*配列へのポインタを`_free`へ渡し、`RET`。
- `0x005BB4FE MOV BYTE PTR [0x0068DFD4],AL`のALは第三引数`[EBP+0x10]`由来。したがってこのclose条件は`doexit`のreturnフラグに結び付く。対象は動的な通常終了時の分岐条件であり、実ゲームの終了動作は未実測。

## STATIC B｜flush/close処理の対象範囲
`0x005BD9F7`は`PUSH 1 / CALL 0x005BD91D (flsall)`。呼出先は全FILEスロットを走査し、存在・flag&0x83条件で`0x005BDB12`によるFILEロック後、`0x005BD986 CALL 0x005BD8D5`（`__fflush_nolock`）へ進む。`EAX != -1`なら成功件数を増加させ、ループ終了時にロック解放する。書込み先、実際のflush結果は未実測。
`0x005CA6DB (__fcloseall)`はindex 3から開始。`0x005CA71B CALL 0x005B7A4E`で開いているFILEをcloseし、index>=20では`0x005CA73A CALL [0x006090A0]`（IAT=`DeleteCriticalSection`）、`0x005CA748 CALL 0x005B71E8`、`0x005CA753`でスロットをNULL化する。すべてのスロットが必ずopenであるとの主張ではない。

## STATIC C｜quick/return条件による互換Golden設計
`doexit`のquick=1では`0x0060966C..0x00609678`の通常コールバックを飛ばすので、今回の`0x005BDAB1`にも到達しない。quick=0の場合のみ登録済みコールバックとして実行し得る。return=0ではフラグ0なので`__flushall`→`_free`、return=1ではフラグ非0なので`__flushall`→`__fcloseall`→`_free`の経路がある。終了済みguardや登録値のランタイム変更、実際の例外フローにより到達性は変わり得る。GoldenはそれぞれDESIGNED / NOT RUN。

## 検索DBの重要な差異
初期Ghidra検索DBの`0x005BDAB1`は関数としてNOT_FOUND。実際の直接CALL site `0x005BDAB1`、`0x005BDABF`、`0x005BDACA`も各0件。一方、**統合V9には同じ3 siteが各1件登録済み**。旧索引の不足をV9にも誤って一般化しない。既存V9を改変せず証拠を残す。

## 判定・復旧記録
PE・両検索DB SHA一致、SQLite quick_check両方ok、先行64/64と03H 38/38整合。独立native監査 **42/42 PASS**（失敗0）。途中の初回監査40/42は機械語切り出し末端がCALLの途中だった問題と、V9の既登録CALLを欠落と仮定した検査の誤り。対象範囲を広げ、V9の実測に従って修正し再監査して42/42 PASS。拒否・接続障害ではない。
REA5種証拠: info=INDEX_ONLY、pseudo=callback NOT_FOUND（子関数INDEX_ONLY）、assembly=TARGETED_PE_NATIVE、callers=PE静的登録値、callees=PE-native+V9。新規5種完備0、正式VERIFIED+0、TODO/VERIFY/BLOCKED正式差分0/0/0、旧ゲームGolden PASS0、strict MATCH未実施、完全複製率未測定。
PC: 接続成功、active.lockなし、Java/Ghidraなし、空きRAM 12.7GiB、CPU約3%（単発取得）。保存時監査約1.15秒、全作業時間未測定。新規REA/Ghidra/ゲーム/Work実行0。原本・MASTER・QUEUE・PROGRESS・既存runs・他レーン・Git・公開先・スケジュールは不変更。
次のP0候補は`0x005BD8D5 (__fflush_nolock)`の失敗値/書込側副作用、および`0x005B861A`の例外コードが`__exit`に伝わる経路。いずれも旧証拠と重複照合してから実施する。
