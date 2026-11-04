# 迫真戦記 REA 10H｜OggDecoder 解放間接CALLのFILE* close登録と二重close防止
研究ID: `REA-LOCAL-20261028-10H-P0-OGG-FILE-CLOSE-CALLBACK-STATIC-01`
状態: PC-SAVED / STATIC / VERIFY / NOT READY。新規正式VERIFIED 0、Golden実測 0。
## ベースライン
原作PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
Ghidra検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`
V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
先行09H Ogg vtable証拠27/27、REA wave1-5 64/64保存済syncを重複なしで照合。
## STATIC-A：間接CALLのOgg読込経路における具体的な登録元
`0x005D16C0` 内の `0x005D1701 MOV ESI,0x005B7A4E`（`_fclose`）→`0x005D170B MOV [EAX+8],ESI`。
渡す4コールバックは `0x005B77CB` read、`0x005CFDD0` seek、`0x005B7A4E` close、`0x005B797C` tell。
`0x005D1712 CALL 0x005D1630` → `0x005D165F CALL 0x005D1490`。
`0x005D14D7 MOV ECX,[EBP+0x18]` と `0x005D14EE MOV [ESI+0x2C8],ECX` がclose関数を内部構造体に保持。
`0x005CFE00` の `0x005CFEDA MOV ECX,[ESI]` → `0x005CFEDF TEST ECX,ECX` → `0x005CFEE3 MOV EAX,[ESI+0x2C8]` → `0x005CFEE9 TEST EAX,EAX` → **`0x005CFEEE CALL EAX`**。
従って **上記Oggファイルopen経路で同じ関数ポインタが保持される場合**、CALLINDの具体的なターゲットは `0x005B7A4E (_fclose)`。一般の全呼出元・動的書換え先まで確定したわけではない。
## STATIC-B：失敗時の二重fclose防止ゲート
正常なクリーンアップ経路はdatasourceとclose callbackの両方を非NULL確認し、closeへ `PUSH ECX` で `FILE*` を1引数渡し、caller側が `ADD ESP,4` で戻す（cdecl）。
一方、`0x005D1587` / `0x005D1695` は `MOV [ESI],0` してから `0x005CFE00` を呼ぶ。これによりその時点ではcallback close条件を満たさない。
`0x005D16C0` の `0x005D171C TEST ESI,ESI` → 不成功なら `0x005D1721 CALL 0x005B7A4E` により上位がFILE*を直接closeする。
この静的な所有権分離は成功時callback close/失敗時wrapper closeと整合。すべての異常経路・例外・動的close数は未実測。

## 検索DB・監査
read-only SQLite quick_checkは旧・V9ともok。旧のindirect_callsに`0x005CFEEE`1件、direct callsは0件。V9 ghidra_refsには同CALLIND site登録0件（直接CALLとして誤登録したものも0件）。
`0x005D165F`、`0x005D1712`、`0x005D1721`の直接CALLは初期検索DBとV9で各1件。旧DBとV9のテーブル構造が異なるので、同一SQLを使って比較しない。
独立監査 **43/43 PASS**、既存VERIFIED 64/64、新規0、正式TODO/VERIFY/BLOCKED差分0/0/0、ゲームGolden PASS0、strict MATCH NOT RUN、完全複製率未測定。
5証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY+NATIVE CROSSCHECK、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY+CALLBACK_ARGUMENT_NATIVE。REA正式5証拠揃いではない。
## Golden条件（DESIGNED / NOT RUN）
正常Ogg A→別B再openではA側が1回closeされるか。初回open失敗、内部初期化失敗、open成功後のデコーダ初期化失敗では FILE*のclose回数・返却エラー・handle残存を原作と再実装で比較。
追加観測候補: `0x005CFE00` がオブジェクト内のcallback以外から呼ばれる場合、既存のsource状態とメモリ上の実vptr/関数ポインタを検証する。
## 安全・未解決・再開
原本・MASTER・QUEUE・PROGRESS・既存RUN・他レーン・検索DB・Git・公開先・毎時スケジュールは変更せず。REA/Ghidra新規実行0、旧EXE/Golden実行0、Work不使用。
初回監査スクリプト作成時に構文エラー、その後V9を旧DBのcallsテーブルと同じだと仮定してOperationalError。双方修正済みで43/43 PASS。安全拒否ではない。
次回P0: `0x005D1490` の seek callback `0x005CFDD0` を `0x005D14AC` で呼ぶ条件・ABIと、0バイト/エラー復帰の所有権を重点研究する。Unicode/console `__write_nolock` は別件VERIFY保持。
記録は `rea_lab/decomp_task` のみに新規保存。run結果・動的挙動の偽装は行わない。
