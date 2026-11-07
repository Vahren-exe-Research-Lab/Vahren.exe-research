# 迫真戦記 ver0.67｜REA 19時台：OggDecoder生成と音声ストリーム初期化の失敗ゲート
研究ID：REA-LOCAL-20261025-1934-P0-OGG-STREAM-GATE-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。正式VERIFIED新規0、原作Golden実測0。

## 先行根拠と非重複
- 直前研究：REA-LOCAL-20261025-1836-P0-OGG-VSLOT10-RELOAD-LIFETIME-STATIC-01。OggDecoder vtable +0x10 -> 0x00501EB0、再ロード前cleanup、constructor戻値がファイル読込の成否を表さないことは既発見。今回の新規発見として再計上しない。
- 2026-10-11進捗同期ログ wave1-5=16+10+10+12+16=64/64。QUEUE/PROGRESSのEPERM由来の古い状態は修復せず、保存済みrunとsyncを優先。
- 対象EXE：SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 検索DB：SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。

## 新発見A：上位呼出元による3段階ゲート
- 0x004BE820の処理では、0x004BEA9C PUSH 0x3E8、0x004BEAA8 CALL 0x005B6C2B で0x3E8バイトを確保する。確保失敗は0x004BEABEの分岐を通じて0x004BEAE0でEAX=0とする。
- 確保成功時は0x004BEAD7でファイル名のアドレス、0x004BEAD8で新規オブジェクトアドレスを積み、0x004BEAD9 CALL 0x00501E20（OggDecoder constructor）。既存研究通りctorは内部loadが失敗してもthisポインタを返す。
- 0x004BEAE9でサウンド状態オブジェクトをESIへ設定し、0x004BEAEF CALL 0x00502220。EAXは直前のctor戻値（確保失敗なら0）が渡される。このcalleeはESIの+4が0、EAXが0、またはdecoderの+5が0なら0x00502321へ進んで状態バイト+0x44を0にして復帰する。
- 【新発見】上位呼出元は0x00502220のAL戻値を直接TESTしない。0x004BEAF4でESIをロードし直した後、0x004BEAFA CMP BYTE PTR [ESI+0x44],0 → 0x004BEB00 JE 0x004BEB86 と、状態バイトで判定する。
- 失敗ゲート0x004BEB86では0x004BEB88 CALL 0x004BF2B0 により上位オブジェクトの後片付けへ進む。これにより「ctorが非NULLを返すだけでは成功とならない」ことを上位でも確認。
- 制限：cleanupの全所有権・例外経路、malloc失敗からの例外はこの局所静的解析では全保証できない。

## 新発見B：音声バッファ初期化と間接CALL
- 0x00502220は0x0050224Fで0x00502100を呼び、decoder(+0x108/+0x10C/+0x110)からストリーム形式情報を構築する。戻りALが0なら後段を実行しない。
- 0x005022C4 CALL EAX（+0x0C vtable slot）、0x005022D9 CALL EDX（+0x00）、0x005022E5 CALL EDX（+0x08）の3間接CALL候補はSQLite indirect_callsにも一致。COM/インタフェース参照元の実行時vtable同定が未了であり、具体的関数VAや意味論はVERIFY。
- 0x005022C6 TEST EAX,EAX → 0x005022C8 JS 0x00502314 は負戻値のエラーゲート。負なら0x00502316で0x00502160を呼びリセットして失敗復帰。別の0x005022E9 → 0x00502330初期化の失敗判定は0x005022EE TEST AL/0x005022F0 JE 0x0050231B。
- 【新発見】0x005022F2でワーカースレッドハンドル(+0x48)が0なら、0x005022FBでスレッド関数0x005023E0を積み、0x00502300でCRT __beginthread(0x005B7D14)を呼ぶ。戻りEAXを0x00502308で+0x48へ保存後、明示的な失敗値検査なく0x0050230BでAL=1、0x0050230Eで成功状態+0x44=1を設定する。スレッド生成失敗時の実ゲーム挙動は未実測／VERIFY（確定バグ認定しない）。
- 0x005023E0自体はGhidra疑似C上で+0x4C stopフラグ、state +0x50に関わり、0x005021E0はWaitForSingleObject(100)を実行する。スレッド終了・例外・タイムアウト時の競合は今後検証。

## 独立した静的検証
- 原作隔離EXEバイト→pefileでPEロード→Capstoneによる機械語確認、SQLite read-only参照を独立照合。監査スクリプト：REA_20261025_19H_OGG_STREAM_GATE_AUDIT.py。
- 証拠JSON：REA_20261025_19H_OGG_STREAM_GATE_EVIDENCE.json。56/56 PASS（EXE/DB SHA、ImageBase、機械語39箇所、DB quick_check、関数索引3件、直接CALL7件、間接CALL3件）。
- Ghidra疑似Cは検索済み機械出力。REA正式5証拠 info=索引参照、pseudo=既存Ghidra、assembly=局所照合、callers/callees=保存索引参照。関数別のREA形式5種を新規に完備したのではないため正式VERIFIED新規0件。
- 正式TODO/VERIFY/BLOCKED書込差分0/0/0（VERIFY事項はこの独立メモのみ）。原作Golden PASS=0。strict MATCH/完全複製率は未測定。

## Golden候補（NOT RUN）
1. 有効Oggを与え正常初期化：上位状態+0x44=1／音声処理継続の有無。
2. 破損Ogg／存在しないOgg：ctorポインタ非NULLでもdecoder+5=0、stream側flag+0x44=0、失敗cleanupまでの到達回数。
3. 音声インタフェース初期化失敗：0x005022C4で負の戻値を模擬し、0x00502160呼出回数と後始末を照合。
4. ワーカースレッド生成失敗：戻値・state+0x44・thread handle+0x48を比較（実機未実行）。

## PC・運用・次のVA
- PC接続成功。開始時active.lock無し、解析専用Java/REA/Ghidraプロセス検出なし。空き物理メモリ約13.3GiB、CPU負荷は測定できず不明。監査単体0.8217秒／保存実行0.5574秒、研究全体所要時間不明。新規REA/Ghidra/ゲーム実行0。
- 書込はREA所有の19時台新規スクリプト、証拠JSON、本報告、readbackのみ。原本、MASTER、QUEUE、PROGRESS、runs、他レーン、Git、Work、スケジュールは変更しない。09時台安全拒否済追記とWave6拒否操作への再試行0。
- 13/14時台OFFLINE成果のPC正本同期はなお未実施。今回もREADY/正式VERIFIEDへ昇格しない。
- 次回P0：0x004BF2B0から0x00502160への失敗後の所有権解放（decoder本体のdestructor vtableとdeallocateの対応）、0x005023E0スレッド終了と0x005021E0待機関数のハンドル寿命、0x005022C4の動的vtable実体の厳密同定。
