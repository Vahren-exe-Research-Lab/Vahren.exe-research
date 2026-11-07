# REA P0｜Ogg DirectSound QueryInterface失敗分岐の静的検証
研究ID: REA-LOCAL-20261026-0036-P0-OGG-QI-HRESULT-NULL-GATE-STATIC-01
状態: STATIC / VERIFY / NOT READY。原作ゲームGolden実測0、新規REA VERIFIED 0。
source SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
search.sqlite SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 根拠／前回との差
既存19H証拠では0x005022C4/0x005022D9/0x005022E5の間接CALL 3件のみ登録。今回の新規内容はQueryInterfaceのGUID・戻り値無検査・後段NULLアクセス条件の接続。
旧19H読取専用PE probeを今回再実行。原作EXE/DB SHA一致、SQLite quick_check='ok'、Capstone ASM出力を確認。新規Ghidra/REA実行なし。
Ghidra検索CLIで0x00502220/0x00502330/0x00502160の関数・参照・擬似Cを照合。擬似Cは形式的VERIFIEDではない。

## 呼出系列（PE32 x86）
0x005022A9: [esi+8]!=0 なら既存バッファ経路0x005022E7へ分岐。
0x005022C4: CALL EAX（[ecx]vtable+0x0C）。CreateSoundBuffer候補。直後0x005022C6 TEST EAX,EAX / 0x005022C8 JS 0x00502314により負HRESULTならcleanup。
0x005022D2～D9: push edi（out=&[esi+8]）、push 0x0060971C（RIID）、push eax（元buffer）、CALL EDX（vtable+0）。IID bytes=49A425682475824D920F50E36AB3AB1E → GUID 6825a449-7524-4d82-920f-50e36ab3ab1e（IID_IDirectSoundBuffer8）。
0x005022DB～E5: QueryInterfaceの戻りEAXを検査せず、元bufferを改めてロードしてvtable+8のRelease候補CALL。
0x005022E7～E9: 続いて0x00502330に無条件CALL（0x005022E9）。
0x0050233B/3D: 0x00502330は[esi+0]（decoderポインタ）だけをNULL検査。0x0050234A mov eax,[esi+8] / 0x0050234D mov ecx,[eax]でbuffer8ポインタを無条件参照。
0x0050234F/54: vtable+0x34経由CALL。通常のIDirectSoundBuffer8ならSetCurrentPositionスロット。

## 推論の範囲
CreateSoundBuffer成功後、QueryInterfaceが失敗し、かつ[esi+8]に有効な旧ポインタが存在しない場合、0x0050234DでNULL参照となる可能性がある。失敗時に常にクラッシュするとは断定しない。通常COM QueryInterface失敗時の出力ポインタ処理と実ゲーム異常系は未実測。
0x005022D9 QueryInterface戻値は0x005022DBで上書きするため失敗判定の分岐が見えない。これは既存のスレッド生成失敗経路とは別の新規VERIFY事項。
未特定: 実環境でのIID対応、CreateSoundBufferが返す実インタフェース、失敗時バッファ8の実値、例外ハンドラや周辺呼出元での救済。

## 保存・進捗境界
既存64/64は2026-10-11保存済み同期記録（今回増加0）。QUEUE/PROGRESS/MASTERは未変更。新規5種証拠完備0、TODO/VERIFY/BLOCKED正式書込差分0/0/0。13/14時のOFFLINE-UNSYNCED成果は未同期のまま。
新規静的調査の監査PASS件数は集計しない（今回新規専用監査スクリプトなし）。既存19H監査56/56を再計上しない。完全複製率未測定。
23H安全拒否対象FLS検索/監査、Wave6、0x5710C0..0x571500、REAエクスポートには触れていない。
次: 0x00502330のNULL到達条件と同一関数の既存buffer8経路、0x004BE820の失敗cleanupとの整合を許可範囲の保存済み証拠から照合。Golden設計のみ、実機PASS0。