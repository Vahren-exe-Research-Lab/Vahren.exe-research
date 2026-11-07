# 迫真戦記 REA｜2026-10-28 16H Ogg buffer圧縮／確保失敗と上位呼出元
研究ID: `REA-LOCAL-20261028-16H-P0-OGG-BUFFER-ALLOC-RETURN-GATE-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。正式新規VERIFIED=0、原作Golden実測=0。

## ベースラインと非重複
直前15H `REA-LOCAL-20261028-15H-P0-OGG-CRC-RESYNC-CURSOR-STATIC-01` の59/59既存証拠を別途参照。15HのCRCテーブル/破損再探索は再計上しない。
隔離PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
10/21旧検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
V9検索DB SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
旧PROGRESSの15/16は既知EPERMの古い表示。正式は既存syncのWave1-5合計64/64（今回追加0）。

## P0-A｜0x005D3500 バッファの圧縮・追加確保
`0x005D3512` で使用済みcursor `+0x0C` を読む。非0の場合 `0x005D3519` でfilled `+0x08` から引き、残量が正のとき `0x005D352A` のコピーを使って `buffer+cursor -> buffer` へ残データを詰める。`0x005D3532` でcursorを0に戻す。
空き容量 `capacity(+0x04) - filled(+0x08)` が要求量以上なら再確保せず `base+filled` を返す。
不足すると `0x005D3549` で **new_size = remaining_filled + request + 0x1000** と計算。buffer非NULLなら `0x005D3558` `_realloc`、NULLなら `0x005D3562` `_malloc`。
これは正常経路の4KiB余裕確保の確認で、単なる2048B固定バッファではない。

## P0-B｜新規：メモリ確保失敗時のNULL引渡し経路
`0x005D356A` は確保戻り値EAXが0か検査。0なら `0x005D356F` で `0x005D34C0` を呼び、既存bufferをfreeして構造体先頭から `+0x18` まで7 DWORDを0化する。
`0x005D3578` で `EAX=0` のまま返る（NULL）。このfail経路はバッファ保持でなく**既存内容の解放と状態初期化**。
呼出元 `0x005CF320` は `0x005CF386` の戻りEAXを検査せず、`0x005CF395 PUSH EAX` でread callback `0x005CF39C` の転送先として引き渡す。
呼出元 `0x005CEB90` も `0x005CEC18` の戻りEAXを検査せず、`0x005CEC27 PUSH EAX` で `0x005CEC2E` のread callbackへ引き渡す。
さらに初期化 `0x005D1490` は `0x005D150E` のEAXを `0x005D1518 PUSH EAX` で `0x005B8730` のコピー処理へ渡す。これも直後のNULL検査を行わない。
確保失敗時にNULLを渡す**命令経路**が静的に確認できるが、CRT側のNULLチェック・異常処理・実機での発生可能性は未実測。クラッシュやデータ破損と断定しない。

## P0-C｜更新ヘルパーの戻り値も上位で未検査
`0x005D3590` は負のcapacityまたはfilled+read > capacityなら-1、成功時はfilled更新後に0を返す。
`0x005CF3A9 CALL 0x005D3590` の直後はstack戻しとEDI(read数)の検査であり、ヘルパー戻りEAXは検査しない。`0x005CEC3B` 呼出元も同型。
現行の正常read経路なら直前 `0x005D3500` が予約済みのため通常は失敗しないが、異常状態でのエラー伝搬は別途VERIFY。

## P0-D｜探索の終了条件はCRCの失敗とは別
`0x005CF320` では `0x005CF348` のページ解析結果が負なら64bit内部位置を正方向へ補正してループ、正ならページ処理、0ならバッファ補充を試みる。
readが0の経路 `0x005CF4B7` は `__errno()` を呼び出すが、戻り値への比較・読み取りがなく共通returnへ移る。
一方 `0x005CEB90` のread0経路 `0x005CEC53/58` はerrnoの値を比較し、0なら-2、非0なら-128。**2つのread利用関数のEOFエラー扱いを同一にしてはいけない**。
これらのreturnが上位OggDecoderへどう反映されるかは、`0x005CF4D0`／`0x005D1310` で次回確認。

## 検査・対象CALL site
対象 `0x005D3500` / `0x005D34C0` / `0x005D3590` / `0x005CF320` / `0x005CEB90` / `0x005D1490`。
旧検索DB CLI `function 0x005D3500`、`callers`、`callees`、`related --depth 2` で限定抽出。原作PE上の対象命令をCapstoneで独立比較。
直接CALL `0x005CEC18, 0x005CF386, 0x005D150E -> 0x005D3500`、および0x005D3500の4直接CALL、`0x005CF3A9 -> 0x005D3590` は旧DB/V9双方に各1件。
間接CALL `0x005CEC2E`、`0x005CF39C` の具体的登録先は既存read-callback研究を参照。今回新規正式5種証拠一式の取得なし。
5種: info=INDEX_ONLY / pseudo=INDEX_ONLY+NATIVE CROSSCHECK / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY+NATIVE CROSSCHECK / callees=INDEX_ONLY+NATIVE CROSSCHECK。
監査61/61 PASS・失敗0、両SQLite quick_check ok、前回15H 59/59証拠状態を照合。正式Wave1-5 64維持、新規VERIFIED0、公式TODO/VERIFY/BLOCKED差分0/0/0。

## Golden条件・安全・再開
モデルのみ: filled=3000、consumed=1200、要求2048ならremaining1800、再確保サイズ7944バイト。これはPython算術fixture、ゲームGoldenではない。
実ゲームのGolden PASS0、strict MATCH NOT RUN、完全複製率未測定。最小の隔離テストでallocator失敗を強制した場合のNULL/errno/上位returnと、正常／破損ページ連続／EOFの挙動を比較するのが将来の条件。今は実行しない。
PC online、開始時active.lockなし、空きRAM約15.96GiB、Java/Ghidra先行プロセスなし。CPU負荷と研究全体時間は未測定。
今回の書込みはREA owner新規probe・audit・evidence・報告・readbackのみ。原本、MASTER、QUEUE/PROGRESS、旧RUN、他owner、Git/公開/スケジュール不変。REA/Ghidra/ゲーム/Work新規実行0。
次P0: `0x005CF4D0`、`0x005D1310` の0/負/正戻り値消費と上位EOF伝搬；その後、`0x005D3500` growth size integer overflow条件をverify。
