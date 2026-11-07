# 迫真戦記 REA｜2026-10-29 01H OggDecoder FILE* ownership/return gate 静的調査
研究ID: `REA-LOCAL-20261029-01H-P0-OGG-FILE-HANDLE-LIFETIME-GATES-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。正式VERIFIED新規0、Golden実測0。
## 情報源・既存成果と今回の差分
- 先行00H: `0x005CF010` NULLシリアル引数と `0x005D1630` 初期化returnは調査済み。21-23Hのallocation/ownership問題も既報告として二重計上しない。
- 今回対象: `0x005D16C0`（file-open wrapper）、そのCALL site `0x005D1712`、上位 `0x00502020`、間接CALL `0x0050202A`、cleanup `0x005CFE00`。
- 原作と同一SHAの隔離EXE: `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 10/21検索DB `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、統合V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
- Ghidra `function/callers/callees/related` の対象抽出を先行、PE32 native Capstone命令・vtable word・2つのSQLite CALL refsで独立照合。新規Ghidra/REA実行なし。
## P0-A: ファイルを開く上位wrapの条件付きclose
- `0x005D16C9`から開くモード文字列 `0x0065B5B4` はPE上で `rb\0`。 `0x005D16CF`は `_fopen`。
- `0x005D16D9 TEST EBX,EBX` / `0x005D16DB JNE 0x005D16E5`。fopen NULLでは `0x005D16DD OR EAX,0xFFFFFFFF`により**-1**を返し、decoder初期化へ進まない。
- fopen成功後は `0x005D16EA`に `_fread`、`0x005D16F8`にseek wrapper `0x005CFDD0`、`0x005D1701`に `_fclose`、`0x005D1706`に `0x005B797C` のコールバックポインタをスタック上に組み立て、`0x005D1712 CALL 0x005D1630`。
- `0x005D171C TEST ESI,ESI` / `0x005D171E JE 0x005D1729`。**非0エラーでは** `0x005D1721 CALL _fclose` を直接実行。**0成功では**直接fcloseをスキップし、ハンドルの寿命はdecoder側へ移る（所有権転送の静的契約）。
- `0x005D172A MOV EAX,ESI`：返却コードを改変せず上位へ戻す。fopen失敗の-1、下位初期化の負数などを別々に残す。
## P0-B: 内部cleanupと二重close回避経路
- `0x005D1490` は `0x005D14E3 MOV [ESI],EDI` でFILE*、`0x005D14EE MOV [ESI+0x2C8],ECX` でclose callbackを格納。
- 先行解析で確認した `0x005D1587 MOV [ESI],0` と `0x005D1695 MOV [ESI],0` は、それぞれ内部cleanupに進む失敗経路上にある。
- `0x005CFE00` の `0x005CFEDF TEST ECX,ECX` / `0x005CFEE3 MOV EAX,[ESI+0x2C8]` / `0x005CFEEE CALL EAX` は、FILE*とcallbackの両方が非NULLのときだけ呼ぶ。内部初期化エラーでFILE*を0にしてcleanupする場合、そこでfcloseせず、外側wrapのfcloseへ委ねるため二重closeを回避する設計と整合。
- **注意**: `0x005D1630` のstate mismatch -131経路では同じcleanupが保証されない。例外・異常状態・残留FILE*の到達可能性は未実測VERIFY。すべてのエラーが安全だとは結論しない。
## P0-C: vtable経由の再オープン前resetを解決
- `0x00501E7E` はdecoder所有オブジェクトへvptr `0x006395CC` を設定。PEの `[0x006395DC]`（vptr+0x10）= **0x00501EB0** を直接読み取り。
- `0x0050202A CALL EDX` は直前の `[vptr+0x10]`取得なので、当該コンストラクタ型についてreset先 `0x00501EB0` を静的に特定（多態的派生型一般は未検証）。
- `0x00501EB4` はobject+5==1の場合のみ `0x00501EC1 CALL 0x005CFE00`、それ以外ではdecoderをzero-fillしてreset。正常再生済みobjectの再初期化前にFILE*をclose callback経由で解放する。
- `0x00502038 CALL 0x005D16C0` 後に `0x00502040 TEST EAX,EAX`。非0では `0x00502046 XOR AL,AL`（bool false）、0では `0x0050208A MOV AL,1`（bool true）。upper APIは数値エラーコードをboolに集約する。
## 検証結果と安全・次回
- 参照は `0x005D16C0`, `0x005D1630`, `0x00502020`, `0x00501EB0`, `0x005CFE00`; 対象CALL siteは `0x005D16CF`, `0x005D1712`, `0x005D1721`, `0x00502038`, `0x00501EC1`, `0x005D158D`, `0x005D169B`。
- 自動audit **57/57 PASS**（命令31件＋旧/V9参照14件＋SHAやsnapshot等。関数数や正式VERIFIED数ではない）。独立したreadbackは別ファイルに記録。
- 既存sync `progress_sync_20261011T153958076Z.json` の Wave1-5正式64/64を再利用。今run正式VERIFIED追加0、5種完全新規取得0、正式TODO/VERIFY/BLOCKED差分0/0/0。古い `PROGRESS.md` はEPERMで15/16のまま、正本に反映しない。
- 新規5種充足: info=INDEX_ONLY; pseudo=INDEX_ONLY+PE_NATIVE_CROSSCHECK; assembly=TARGETED_PE_NATIVE; callers/callees=INDEX_ONLY+PE_NATIVE_CROSSCHECK。完全パッケージの取得なし。
- 原作ゲームGolden PASS **0**、strict MATCH=NOT RUN、完全複製率=未測定。
- 17〜22HのLibrary OFFLINE-UNSYNCED成果は今runでは統合しない。原本、MASTER、QUEUE、PROGRESS、既存RUN、他レーン、Git、公開先、スケジュールは変更しない。Workなし。
- 次のP0候補: `0x00501EB0` の異常状態reset条件・`0x005D1630` の -131後のdecoderポインタ寿命、`0x005CFEEE` のclose callback ABI（特にFILE*がNULLでない場合の正常解放）を静的照合し、メモリ確保失敗のクラッシュ実測とは区別する。
