# 迫真戦記 REA｜2026-10-28 23H OggDecoder初期化メモリ確保・解放ガード
研究ID: `REA-LOCAL-20261028-23H-P0-OGG-INIT-ALLOC-CLEANUP-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式VERIFIED=0／旧EXE Golden実測PASS=0。
## 先行成果との非重複・出典
- 16Hの`0x005D3500`バッファ確保失敗とNULL渡し（既存）を新規計上しない。17〜22Hの索引確保・BOS/serial・一時配列・Ghidra到達不能誤認も別研究として維持。
- 今回の新規焦点は`0x005D1490` **後半初期化時の3個のcalloc戻り値**と`0x005CFE00` **2配列まとめて解放する条件ガード**。
- 原作と同SHAの隔離コピー`rea_lab/targets/hakushin067_Vahren.exe` SHA256 = `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 初期SQLite SHA256 = `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。統合V9 SHA256 = `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
- Ghidra検索CLI `function 0x005D1490`/`0x005CFE00`/`0x005D3D00`/`0x005D3DE0`・`related 0x005D1490 --depth 2 --limit 30`、PE32のCapstone独立命令境界、旧/V9の直接CALL参照を突合。
## P0-A：成功経路にある未検査のcalloc戻り値
| 呼出site | 保存/レジスタ | 最初のポインタ書込 | 静的な結果 |
|---|---|---|---|
| `0x005D15A0` `_calloc` | `[ESI+0x40]=EAX` | `0x005D15B1 MOV [EAX],ECX` | NULLを返すと直後にNULL書込候補 |
| `0x005D15D2` `_calloc` | `[ESI+0x38]=EAX`, `EDI=EAX` | `0x005D15E8 MOV [EDI],0` | NULLを返すと直後にNULL書込候補 |
| `0x005D15E0` `_calloc` | `[ESI+0x3C]=EAX` | `0x005D15FE MOV [EAX],EDX` | NULLを返すと直後にNULL書込候補 |
上記3区間にEAXのNULL検査・分岐はない（機械語で確認）。正常条件での明白な越境アクセスを示すものではなく、**メモリ確保に失敗したとき限定**のVERIFY論点。
## P0-B：cleanupの2配列解放が非対称な条件で一括スキップされる
- `0x005D1539`はstream件数`[ESI+0x34]=1`を設定し、`0x005D1540` `_calloc(1,0x20)`の結果を`+0x48`、`0x005D154C` `_calloc(1,0x10)`を`+0x4C`へ代入。
- 解放関数`0x005CFE00`は`0x005CFE36`で**+0x48==NULL**を確認すると`0x005CFE39 JE 0x005CFE91`。さらに`+0x34==0`でも`0x005CFE40 JE 0x005CFE91`。
- いずれかの早期ジャンプは`0x005CFE80`（`_free(+0x48)`）と`0x005CFE89`（`_free(+0x4C)`）の**両方を飛ばす**。
- `+0x48==NULL`、`+0x4C!=NULL`なら、cleanup関数自身は後者をfreeせず、`0x005CFEFB`の構造体全消去まで進む。実際の経路・他owner参照・CRT失敗処理は未確認のため**条件付きメモリリーク候補**とする。
- 逆の条件（`+0x48!=NULL`、`+0x4C==NULL`）では配列要素破棄helper`0x005D3D00`の擬似CはNULL引数を許容する。NULL時に必ずクラッシュすると断定しない。
## P0-C：既存Ghidra擬似Cとの相違
`0x005D1490`の索引配列確保は、Ghidra擬似Cが`_calloc(2,4)`と簡略化しているが、原作命令`0x005D159A LEA ECX,[EDI+2]`から`PUSH 4; PUSH ECX`を経て`0x005D15A0 CALL _calloc`へ進むため、実際の確保件数は**EDI+2**。EDIは直前の`0x005CF010`が返した補助件数から取得する動的値であり、常に2とみなしてはならない。
`0x005D1614`の共通`_free`到達性は22Hの既報告を維持し、今回の新発見には数えない。
## 検証・指標・次回
- 対象：`0x005D1490`, `0x005CFE00`, caller `0x005D1630`。旧DB/V9で対象10箇所のCALL siteはいずれも1件。SQLite両quick_check=ok。
- 独立監査 **67/67 PASS**（1検査=1関数の意味ではなく命令位置・参照・ハッシュ・旧runなどの条件）。既存RUN`20261011T153309850Z`の4件×5種がVERIFIEDであることを再照合。syncのWave1〜5 **64/64**を維持。旧PROGRESS`15/16`はEPERMによる古いスナップショット。
- 5種証拠：info=INDEX_ONLY、pseudo=INDEX_ONLY+PE_CROSSCHECK、assembly=TARGETED_PE_NATIVE、callers/callees=INDEX_ONLY+PE_CROSSCHECK。新規正式5種一括取得=0、新規VERIFIED=0、公式TODO/VERIFY/BLOCKED差分=0/0/0、オフラインVERIFY論点1群。Golden実測PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。
- 安全：REA/Ghidra/ゲーム/Work起動なし。原本/MASTER/QUEUE/PROGRESS/旧RUN/他lane/Git/公開/スケジュール変更なし。新規REA owner資料のみ。
- 次回P0は`0x005CF010`へNULLシリアル配列が渡された際の挙動と、`0x005D1630`が初期化失敗をどう返すか。これらを独立証拠で照合して初めてクラッシュ・リークの到達可能性を判断する。未同期17〜22H Library成果は正本・既存ID・所有権・ハッシュ・競合確認後に一度だけ同期。
