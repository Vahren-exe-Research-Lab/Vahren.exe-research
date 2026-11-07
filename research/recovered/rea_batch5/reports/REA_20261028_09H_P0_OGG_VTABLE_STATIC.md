# 迫真戦記 ver0.67 REA 09H｜OggDecoder 間接CALLのvtableスロットを静的解決
研究ID: `REA-LOCAL-20261028-09H-P0-OGG-RESET-VTABLE-SLOT-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。正式REA新規VERIFIED=0、Golden実測=0、strict MATCH=NOT RUN。

## 前提・先行照合
- MASTER、レーン所有権、REA README/QUEUE/PROGRESS/WAVES、2026-10-11最終保存済sync(64/64)、10/21検索DB README/BUILD_MANIFEST、08H研究証拠(32/32)を確認した。
- EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 旧検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
- 統合V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
- 新規REA/Ghidra、原作ゲーム実行は行わず、既存CLIと保存PEの対象数十バイト、SQLite read-onlyのみを調査。

## 新規 STATIC-A: 間接CALLの具体的なスロットを原作PEで解決
- `0x00501E7E: MOV dword ptr [ESI], 0x006395CC` でOggDecoderオブジェクトのvptrを設定。
- vtable `0x006395CC` の5エントリは順に `0x00501DF0, 0x00501F10, 0x00502000, 0x00502020, 0x00501EB0`（原作PEの値をread-only取得）。
- `0x00501E93: CALL 0x00502020`。該当関数は `0x00502022 MOV ESI,ECX` → `0x00502024 MOV EAX,[ESI]` → `0x00502026 MOV EDX,[EAX+0x10]` → **`0x0050202A CALL EDX`**。
- 従って、**このコンストラクタから渡されたvptrが維持される経路**に限り、間接CALL `0x0050202A` は `0x00501EB0`（vtable+0x10）に解決する。一般の仮想呼出し全体を解決したわけではない。
- `0x00502038 CALL 0x005D16C0`（旧08Hで確認済みのrbファイルopen）より**前に**cleanup/resetが走る。

## 新規 STATIC-B: スロット関数は状態に応じた解放＋初期化
- `0x00501EB4 CMP byte ptr [ESI+5],1` と `0x00501EB8 JNE 0x00501EC9`：状態フラグが1のときだけ `0x00501EC1 CALL 0x005CFE00`。
- `0x005CFE00`の保存済擬似Cは内部領域（対象オブジェクト+0x118）のコーデック関連メモリ解放を示す。詳細な解放順と副作用は未正式VERIFIED。
- その後 `0x00501ED8` / `0x00501EEB` の2回のmemsetでデコーダ内部領域をゼロ初期化し、オブジェクトのサイズ・状態フィールドを0化、`0x00501F07 RET`。
- 初回構築時は状態=0からreset経由でopenへ進む。再open時に状態=1なら以前のコーデックを解放してから新規ファイルを開く構造。**ファイルopenが失敗しても以前の状態は既に消去される可能性**があり、失敗後のユーザー可視挙動は実機VERIFY。

## DB監査・正式指標
- 旧検索DBの `indirect_calls` に `0x0050202A` 1件、同siteの直接`calls`0件。分類は正しく、vtable slotの値をGhidraが補完しないこと自体は索引欠落ではない。
- `0x00501E93,0x00502038,0x00501EC1` は旧検索DBの直接CALLにそれぞれ1件。2DBの `PRAGMA quick_check` はok。既存スナップショット/独立PEを横断監査。
- 自動静的監査 **27/27 PASS**。既存正式VERIFIED 64/64（Wave1〜5、最終保存syncを参照）、今回新規VERIFIED 0。TODO/VERIFY/BLOCKEDの正式差分0/0/0。
- 関数別5種証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY+NATIVE CROSSCHECK、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY+VTABLE_SLOT_PE_NATIVE。これだけでREAの完全な5証拠を新規VERIFIED扱いにしない。
- Golden PASS 0、完全複製率未測定。実行時vptrの変更・別インスタンス・関数 `0x005CFE00` 内の追加間接CALL `0x005CFEEE` は引き続きVERIFY。

## Golden条件と次回研究
- 設計のみ：同じOggDecoderインスタンスでA読込→B読込、A読込→不正B読込の2系列。旧状態の解放・バッファ/状態初期化・エラー復帰・音声再生/ファイルhandle残存を原作と再実装で比較する。実測0。
- 次回 P0： `0x005CFEEE` のコールバックポインタの設定元、呼出条件、ABIを旧検索DB・PEから先に調査。または `0x005CA1D1..0x005CA4EB` のUnicode/console戻り値の前回未解決経路。
- 研究成果は自担当 `rea_lab/decomp_task` にのみ独立新規保存。原本ZIP/EXE/SAVE、MASTER、QUEUE/PROGRESS、既存RUN、A〜E、検索DB、Git、スケジュールは変更しない。
