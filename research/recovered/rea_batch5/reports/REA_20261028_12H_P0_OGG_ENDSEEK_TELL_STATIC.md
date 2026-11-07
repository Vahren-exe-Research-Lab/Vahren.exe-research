# 迫真戦記 REA 12H｜Ogg seekable初期化のEND-seek / tell ABIと失敗条件
研究ID: `REA-LOCAL-20261028-12H-P0-OGG-ENDSEEK-TELL64-STATIC-01`
状態: PC-SAVED / STATIC / VERIFY / NOT READY（新規正式VERIFIED=0 / 原作Golden実測=0）。

## 出典・非重複
隔離EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
2026-10-21検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
前回11Hの48/48と、2026-10-11保存済syncのWave1-5計64/64を確認し重複追加なし。旧QUEUE/PROGRESSはrename EPERMでstaleのため正式数を再計上しない。
保存済CLI `function 0x005D1310` / `callers` / `callees` およびread-only PE32逆アセンブル、旧・V9 SQLiteの照合を実施。Ghidra一括再実行なし。

## P0-A｜未解決CALLINDの具体的なOggファイル経路
Ogg open時 `0x005D16F8 MOV EDX,0x005CFDD0` (seek)、`0x005D1706 MOV EDI,0x005B797C` (tell) が4-callback構造体へ書込。
`0x005D14E5` で `[ESI+0x2C4]=seek`、`0x005D14F5` で `[ESI+0x2CC]=tell`。seekable側の `0x005D1689 CALL 0x005D1310` に入る。
`0x005D1363/65/67/69 PUSH 2; PUSH 0; PUSH 0; PUSH datasource` → `0x005D136A CALL EAX`。
これはx86 cdeclで `seek(datasource, 0LL, SEEK_END=2)` に相当する。続く `0x005D1375 CALL EAX` は `tell(datasource)`。
固定のOgg rb open登録経路に限定した候補解決であり、他datasourceの動的書換えを一般化しない。
## P0-B｜END-seekの戻り値は直接確認されない
`0x005D136A CALL EAX` の直後は `0x005D136C MOV EDX,[ESI]` → `0x005D136E MOV EAX,[ESI+0x2CC]` → `0x005D1374 PUSH EDX` → `0x005D1375 CALL EAX`。
この間にseek戻り値EAXを比較・保存する分岐がない。**seek失敗の即時判定はせず、tellの返り値に進む**。
従ってseekが失敗してもtellが非-1を返す条件では、ここで直ちに失敗扱いしない可能性がある。OS側や後続デコードでの実挙動はNOT RUN。

## P0-C｜tellの32bit結果を符号拡張して64bit長に保持
`0x005D1375 CALL EAX` → `0x005D1377 CDQ` で、32bitのtell戻り値EAXをEDX:EAXへ符号拡張する。
`0x005D137B/7E` が戻り値low32を `[ESI+0x10]` と `[ESI+8]` に、`0x005D1381/84` がsign-high32を `[ESI+0x14]` と `[ESI+0xC]` に格納。
`0x005D139B–0x005D13A3` で-1番兵を検査し、失敗なら `0x005D13A7 MOV EAX,0xFFFFFF7D` → `0x005D13B0 RET`（-131）。
CALLIND登録が欠ける場合も-1長をセットし同じ失敗分岐に到達。正常なtellの実データ範囲は32bit signedに制約され、大容量Ogg境界の実障害は未検証。
tell成功なら `0x005D13C5 CALL 0x005CEE10`、さらに `0x005D140D CALL 0x005CF4D0` 等の後続ヘッダ処理へ進む。後者の負戻り値を-128に変換する経路は `0x005D141B`。

## 検索基盤・監査・証拠等級
初期検索DBの `0x005D136A` と `0x005D1375` はそれぞれ間接CALL候補1件。V9 ghidra_refsは両siteとも0件（収録方式が異なり、これだけで欠落とは断定しない）。`0x005D1689→0x005D1310` は双方のDBに直接CALL1件ずつ。
旧・V9両DB read-only `PRAGMA quick_check=ok`。独立検査 **50/50 PASS**。5証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY+NATIVE CROSSCHECK、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY+NATIVE、callees=INDEX_ONLY+CALLBACK REGISTRATION。新規のREA正式5証拠完了=0、既存正式VERIFIED=64維持、新規=0。正式TODO/VERIFY/BLOCKED差分0/0/0。
## Golden（設計のみ / NOT RUN）
(1) 正常rb Oggの開封後にseek(0,SEEK_END)とtellが呼ばれるか、終端と戻り値が一致するか。(2) seek失敗/tell成功という特殊datasourceで後続初期化へ進むか。(3) tell=-1で戻り値-131と資源解放状態が一致するか。(4) 2GiB前後のオフセットと大容量Oggで32→64符号拡張が影響するか。(5) seek不可でstate3へ移る原作/再実装比較。
原作ゲーム実測PASS=0、strict MATCH=NOT RUN、完全複製率=未計測。

## 安全・保存・再開
PC接続あり、active.lockなし、Java/Ghidra先行プロセスなし。開始時空き物理メモリ約15.59GiB、CPU負荷未測定。単独静的監査約1.14秒、全研究所要時間未測定。REA/Ghidra新規実行0、ゲーム実行0、Work使用なし。
読み取り用PowerShell→Pythonの最初の日本語パスが文字化けしてWinError123。Pythonコードに非ASCIIパスを渡さず研究ディレクトリへSet-Locationして相対参照し正常復旧。安全拒否ではなく新Ghidraを起動していない。
原本ZIP/EXE/SAVE、MASTER、QUEUE/PROGRESS、既存RUN、A〜E/T018/dev_lab、Git、公開先、検索DB、毎時設定は未変更。今回の新規研究ファイルだけREA ownerに保存し、保存後独立読戻しする。
次のP0：`0x005D13C5→0x005CEE10` 内 `0x005CEE80` のseek callback、64bit残量から32bit wrapperへの変換と負戻り値伝播を独立調査。その他 `__write_nolock` Unicode/consoleの戻り値補正は別件VERIFYのまま。
