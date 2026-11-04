# REA P0 01時｜DirectSound8終了処理・再充填CALLと二段階cleanup
研究ID: REA-LOCAL-20261026-0136-P0-DS8-SHUTDOWN-REFILL-DOUBLE-CLEANUP-STATIC-01
状態: STATIC / VERIFY / NOT READY、PC側独立証拠。Game Golden実測0、新規正式REA VERIFIED 0。
原作EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
search.sqlite SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 旧研究との差分と新証拠
00時台は0x502220 QueryInterface失敗→0x502330 buffer+8未検査参照を報告済み。今回は0x004BF2B0の上位cleanup呼出条件と0x502330異常系を独立接続。前回のQI発見は新発見に再計上しない。
- 0x004BF303 CMP BYTE PTR [EDI+0x44],BL ; 0x004BF306 JE 0x004BF321。streamフラグが0ならStopと0x502330を省略。
- 0x004BF318 CALL EDX は[buffer vtable+0x48]を使用。IDirectSoundBuffer8であればStop。
- 0x004BF31C CALL 0x00502330 はStopの直後、上記status非ゼロの場合に呼ばれる。0x502330は初期化時だけではなく終了処理経路からも呼ばれる。
- 0x004BF321 MOV EAX,[ESI+0xA0] ; 0x004BF327 CALL 0x00502160。Stop/0x502330を省略しても、streamオブジェクト非NULLならここへ到達する。
- 0x00502330: 0x0050233Dでdecoder+0のNULLは検査するが、buffer8+8への0x0050234D参照前に明示的NULL検査をしない（00時台から既知）。
- 0x00502354 buffer8 vslot+0x34呼出結果は未検査。0x00502387 vslot+0x2C呼出の後は0x00502389 TEST EAX / 0x0050238B JS 0x005023C9。
- 0x005023CB CALL 0x00502160: Lock系失敗時の内部cleanup。上位0x004BF2B0はその後0x004BF327で再度0x00502160を呼ぶ経路が存在する。
- 0x00502160は正常経路でポインタとstatusをクリアするため、二度呼び出しが直ちに二重freeを意味しない。異常時idempotenceや実ゲーム発生率は未確認。

## 監査・境界
原作機械語20箇所、Ghidra直接CALL4サイト、間接CALL5サイト、EXE/DB SHA各1、SQLite quick_check1を独立assert → 32/32 PASS。検索基盤から関数 0x004BF2B0 / 0x00502220 / 0x00502330 / 0x00502160 を確認。新REA実行なし。
5種証拠 info/pseudo/callers/callees = INDEX_ONLY、assembly=TARGETED_SOURCE。新規5種完備0 / 新規VERIFIED0。旧Wave1–5 64/64は2026-10-11同期ログに基づき据置。QUEUE/PROGRESS/MASTER書込差分0、TODO/VERIFY/BLOCKED書込差分0/0/0。
実機Golden PASS0、strict MATCH未測定、完全複製率未測定。00時・23時台の既往安全拒否FLS操作、Wave6、禁止VA、REA exportを再試行しない。
PCオンライン、active.lock不在、専用Java0、空きRAM約13.62GiB（単発観測）。CPU負荷・総所要時間不明。過去13/14時オフライン成果は未同期。
次は0x00502330の0x005023BF Unlock結果未検査、0x004BF2B0二度cleanup時の具体的レジスタ・フィールド状態を静的照合し、Golden条件のみ設計。実ゲームは未実行。
