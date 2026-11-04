# 迫真戦記 REA 14H｜Oggページ読込コールバック／EOF・CRC・バッファ状態
研究ID：`REA-LOCAL-20261028-14H-P0-OGG-READ-EOF-CRC-STATIC-01`
状態：PC-SAVED / STATIC / VERIFY / NOT READY。既存正式VERIFIED=64（維持）、新規=0、原作Golden実測=0。

## 出典・非重複
隔離PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
2026-10-21検索DB: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
前回13Hの56/56保存証拠を照合、sync保存済みWave1-5合計64/64を照合。正式数の二重計上なし。
対象は未解決CALLIND `0x005CEC2E`（関数入口`0x005CEB90`）とページバッファヘルパー。13Hのseek64/32研究とは別の新規観測。

## P0-A｜固定Ogg rb経路のreadコールバックを解決
`0x005D16EA MOV ECX,0x005B77CB`、`0x005D16EF MOV [EAX],ECX`で4コールバックの第1要素をreadへ登録。
`0x005D14DD MOV [ESI+0x2C0],EAX`がreadポインタをOgg内部構造体へ保持。
`0x005CEC28 MOV EAX,[ESI+0x2C0]`、`0x005CEC2E CALL EAX`で呼出。
この**登録経路に限定**してCALLINDの実体は`0x005B77CB`（MSVC2010の`_fread`）と整合。動的書換え・別datasourceは未確定。
`0x005CEC1F/20/25/27`で順に`PUSH FILE* / 0x800 / 1 / buffer`。cdecl引数順は`fread(buffer,1,2048,FILE*)`。
`0x005B77D9`は`_DstSize=-1`、`0x005B77DE`から`_fread_s`を呼ぶ。戻ったread数EAXを`0x005CEC30`でEDIへ退避。
`0x005CEC3B`は正数readを`0x005D3590`のbuffer filled-byte countに加算。CALL直後にそのhelperのEAXを検査せずread数EDIを検査する点は要注意（正常確保経路では容量を予約）。

## P0-B｜EOFとエラーを区別する
`0x005CEBF9/BEFE`でread前の`errno`を0へ明示初期化。
`0x005CEC35 TEST EDI,EDI`でreadが正ならappend後に再探索、負なら`0x005CEC72`へ。
readが0なら`0x005CEC53 __errno`と`0x005CEC58 CMP [EAX],0`を実行し、非0で-128、0で-2を返す。
したがって同じ0バイト読込でも「errnoなしのEOF」と「errnoありの失敗」を区別する条件分岐。
ただしCRTの`ferror`フラグ等を別途確認する命令はこの局所分岐にはなく、実際のすべての失敗形態を網羅する保証はない。
`0x005CEC69`の-1は別の探索終了番兵。戻り値はEDX:EAXの符号拡張に注意。

## P0-C｜OggSページ・CRC検証とバッファリセット
`0x005D35C0`は`0x005D35F2 CMP [EDI],0x5367674F`（リトルエンディアンASCII `OggS`）でページを判定。
`0x005D35FE`はヘッダ+0x1Aのsegment countを取得、固定27バイト+segment tableとpayload lengthの和が入っているか確認。
`0x005D3668 CALL 0x005D33F0`はheader+payloadのCRC表計算、`0x005D3673`でヘッダ内の元チェックサムと比較。
不一致・magic非一致は`0x005D36C8`の`_memchr`で次の'O'候補を探索する経路を持ち、単純な即時失敗ではない。
前回13Hのseek成功後`0x005CEE94 CALL 0x005D39F0`は、管理領域+4が負なら-1、非負なら+8,+C,+10,+14,+18の5DWORDを0へリセット。メモリ解放・ファイルcloseまで行う関数ではない。

## 索引・証拠等級
旧DBの`indirect_calls`にsite`0x005CEC2E`が1件、V9の`ghidra_refs`は0件（異なる収録方式、欠落断定なし）。
ページ解析直接CALL`0x005CEBD9 -> 0x005D35C0`は旧DB/V9双方1件。SQLite quick_checkは両方ok。
独立read-only PE/SQLite監査 **62/62 PASS**（約1.13秒）。対象命令、登録値、固定CALL、read引数、magic、helper5領域、ハッシュ、旧証拠を個別照合。
5種: info=INDEX_ONLY / pseudo=INDEX_ONLY+NATIVE CROSSCHECK / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY+CALLBACK REGISTRATION。
新規REA正式5種証拠一式=0、正式TODO/VERIFY/BLOCKED差分=0/0/0。ゲームGolden PASS=0、strict MATCH=NOT RUN、完全複製率=未計測。

## Golden設計（NOT RUN）・次回
(1) 正常Oggで2048バイト以下/超の断続読み、末尾でerrno=0と失敗時errno!=0の戻り値を比較。
(2) CRC破損、OggS以外のprefix、segment count=0/255、payload長不足で再探索開始点と-1/-2/-128を比較。
(3) read callback=0、datasource=0、malloc失敗とfread失敗の境界を分離し、再実装のクラッシュ/復旧条件を確認。
(4) 13Hで見つかった64bit/32bit seek乖離後に読込bufferの5領域resetが正しく行われるか比較。
次P0は`0x005D35C0`のCRC破損時cursor移動と`0x005D33F0`のCRC table/index exactness、または`0x005CF320`の読込共有経路。
`__write_nolock` Unicode/console補正は既存VERIFYを保持。

## 安全・保存
PC接続正常、active.lockなし、Java/Ghidra先行プロセスなし。空きRAM約13.90GiB、CPU負荷は未測定。
REA/Ghidra新規実行0、ゲーム実行0、Work0。正式QUEUE/PROGRESSは古いEPERM状態につき変更せず、保存済syncを優先。
原本ZIP/EXE/SAVE、MASTER、既存RUN、他owner、DB、Git、公開・スケジュールは未変更。
今回の所有REA領域に新規probe/audit/evidence/report/readbackのみを追加。独立再監査・SHA読戻しをreadback文書へ記録。
