# 迫真戦記 REA 13H｜Ogg後方64KiB探索とseek64/32 ABI不一致
研究ID: `REA-LOCAL-20261028-13H-P0-OGG-BACKSCAN-SEEK64-ABI-STATIC-01`
状態: PC-SAVED / STATIC / VERIFY / NOT READY。正式VERIFIED追加0、ゲームGolden実測0。

## 出典・先行成果との非重複
隔離EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
2026-10-21検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
12Hの50/50、保存済syncのWave1〜5合計64/64を再照合。正式数を二重計上しない。
旧QUEUE/PROGRESSはEPERMで古いため集計の根拠には使わない。
read-only `search.py function 0x005CEE10`、`callers`、`callees`、関連`0x005CEB90`/`0x005CF4D0`、隔離PEの対象命令、旧/V9 SQLiteを使用。
既存の11H/12Hはseekコールバックの32bit化と終端tellを特定済み。本13Hの追加点は後方64KiB反復・戻り値別分岐・実カーソルと内部カーソルの乖離条件。

## P0-A｜間接CALL 0x005CEE80 の引数と到達元
関数入口`0x005CEE10`、関数内のCALL site `0x005CEE80`。上位直接CALL `0x005D13C5`（seekable Ogg初期化）および`0x005CF574`/`0x005CF723`（後段探索）を索引照合。
`0x005CEE1E`で内部位置のhigh32 `[EBX+0xC]`、`0x005CEE22`でlow32 `[EBX+8]` をロード。
`0x005CEE48 ADD EDI,0xFFFF0000`、`0x005CEE4E ADC ESI,EAX`（EAX=-1）により64bit位置を0x10000=65536ずつ減らす。負値になれば`0x005CEE62..6A`で0へクランプ。
`0x005CEE72 MOV EAX,[EBX+0x2C4]`でseek callbackを取得。固定rb Ogg open経路では登録値は`0x005CFDD0`。
`0x005CEE7C PUSH EDX(0=SEEK_SET)` / `7D PUSH ESI(high32)` / `7E PUSH EDI(low32)` / `7F PUSH ECX(datasource)` / `0x005CEE80 CALL EAX` / `0x005CEE82 ADD ESP,0x10`。
したがって`seek(datasource, candidate64, SEEK_SET)`形式。関数ポインタ差替え・別datasourceへの一般化はしない。

## P0-B｜戻り値、内部位置とバッファ状態
`0x005CEE6C`のdatasource NULLは`0x005CEEA7 EAX=0xFFFFFF7F`（-129）。
callback NULLまたは`0x005CEE85 CMP EAX,-1`でseek失敗時は`0x005CEEA0 EAX=0xFFFFFF80`（-128）。
seekが-1以外なら`0x005CEE8E/91`で候補64bit位置を`[EBX+8/+0xC]`へ格納し、`0x005CEE94 CALL 0x005D39F0`で内部バッファ状態のリセット経路へ進む。
`0x005CEEAC CDQ`等により失敗時の符号拡張した64bit戻り値を返せる。成功後`0x005CEEEA CALL 0x005CEB90`から後方のデータ解析が続く。
`0x005CEFB9 JE 0x005CEE45`に後方探索の再反復枝がある。これは一度のseekで終わらない経路。

## P0-C｜既存seek wrapperの32bit化と新たな不整合条件
seek callback `0x005CFDD0`は64bit引数の上位`[EBP+0x10]`を読まず、`0x005CFDE2`で下位32bitだけ取り出して`0x005CFDE8 CALL 0x005D1B04 (_fseek)`する。34バイト全体でhigh32参照なし。
一方、呼び出し側はseekが成功すると候補の**high32も含めて**内部位置に記録する。
例えば候補=0x100010000なら、渡す64bit値は4GiB+64KiB、実際の_fseekのoffsetは0x00010000（64KiB）へ切り詰められる。_fseekが成功した場合、ファイル実位置とデコーダ内部位置に4GiBの乖離が発生し得る。
この値は**静的なABIに基づく条件付きモデル**であり、巨大Oggでの再現実測ではない。実際のファイル境界やOSの動作、他の回復経路はVERIFY。
`0x005CEB90`の後続処理および連続Oggチェーンの正確な境界判定は未確定。擬似Cだけで意味を固定しない。

## 検索DB・監査等級
初期DB: `0x005CEE80` はindirect_calls=1、`0x005D13C5→0x005CEE10`はdirect=1。V9は各0/1（間接CALLの収録方式が異なるため欠落断定なし）。
両DBのread-only `PRAGMA quick_check=ok`。独立監査 **56/56 PASS**、初回1.37秒、証拠保存時1.176秒。
5証拠: info=INDEX_ONLY / pseudo=INDEX_ONLY+NATIVE CROSSCHECK / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY+NATIVE / callees=INDEX_ONLY+CALLBACK REGISTRATION。
新規正式5証拠一式=0、既存Wave1〜5 VERIFIED=64維持、新規=0、正式TODO/VERIFY/BLOCKED差分0/0/0。Golden PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。

## Golden設計（実測なし）・再開位置
(1) 64KiB境界前後の有効/無効Oggで後方探索の呼出し回数・初期位置を比較。(2) datasource NULL、seek callback NULL、seek=-1を区別して-129/-128と資源解放状態を観測。
(3) sparse fileで2GiB/4GiB境界を跨ぐcandidate64のseek位置・内部カーソル・後続読取の整合を比較。(4) chained Oggの識別/ページ探索を原作と再実装で比較。
PC接続成功、active.lockなし、Java/Ghidra先行プロセスなし、開始時空きRAM約14.32GiB、CPU負荷不明、研究全体の所要時間不明。
新規REA/Ghidra実行0、原作ゲーム0、Work0。原本・MASTER・QUEUE/PROGRESS・旧RUN・A〜E・検索DB・Git・公開・スケジュールを変更しない。
次P0: `0x005CEB90` のOgg page候補検出と`0x005CEC2E`のread callback、`0x005D39F0`のバッファ初期化範囲を追跡する。Unicode/console `__write_nolock` は別VERIFY。
