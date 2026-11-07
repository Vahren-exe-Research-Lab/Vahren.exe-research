# 迫真戦記 ver0.67｜REA 2026-10-28 21時台：Oggシリアル配列の早期return時の所有権・解放非対称性

**研究ID:** `REA-OFFLINE-20261028-21H-P0-OGG-SERIAL-EARLY-RETURN-OWNERSHIP-STATIC-01`  
**分類:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**対象:** `0x005CF010`（BOS/serial/Vorbis識別処理）、`0x005CF4D0`（連結索引・再帰呼び出し）、主要CALL site `0x005CF167`, `0x005CF5BE`, `0x005CF628`、_free site `0x005CF1D5`, `0x005CF643`。

## 1. 実行前検査・出典と非重複

- WindowsのDesktop Commander Local Compactは読み取り試行時 `McpServerError: MCP SSE probe returned 429` を返した。接続・レート制限の問題であり安全拒否ではない。Remote側の機器状態確認では「Saito Offline、最終接続5時間前」。PC最新MASTER/QUEUE/PROGRESS、owner、active.lock、CPU/RAMは未取得。PC正本へは書いていない。
- ChatGPT Libraryに実在したユーザー提供の `Vahren.exe` と `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を読み込み、実行環境へ読取り用コピーとして取得。SHA256はEXE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、PACK `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、索引SQLite `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。すべて期待値一致。ZIP全34項目CRC正常、SQLite integrity_check `ok`。
- ZIPに保存された旧PROGRESSは2026-10-09時点の15/16であり、過去報告の正式VERIFIED64件と合算しない。旧研究17/18/19/20時台の監査はそれぞれ92/92・120/120・133/133・115/115 PASSで再現した（これらは新発見・新VERIFIEDではない）。
- 10/21 Ghidra12.1.4の検索DBから**対象関数のみ**関数・callers/callees・relatedを取得。`0x005CF010`擬似CのSHA256 `07A09BCD302AED04DF436A21A46DC2826EE4EF3E4B100487C39E8F08DA636DBE`、`0x005CF4D0`は`B0586B68BDF8D49943E9DB10D1F337F693E964F95DAC75EDEC19EE27B61FDA63`。機械出力擬似Cを正本ソースとは見なさない。独立に原作PE32機械語、直接CALL相対変位、分岐相対変位を検査した。

## 2. 新発見A：同じ-133でも、配列の所有権が異なる

`0x005CF010`はBOSシリアル番号の一時配列を`0x005CF0F2`の`_realloc`または`0x005CF0FE`の`_malloc`で確保し、`0x005CF109 MOV [EDI], EAX`で呼出し元から渡されたポインタの保存先を更新する。`0x005CF112`では配列へシリアルを書き込む。

**重複BOSシリアル**では、比較結果の分岐`0x005CF0C3 -> 0x005CF1CB`により、`0x005CF1D5`で同配列を`_free`し、`0x005CF1DD`と`0x005CF1E3`でポインタと件数を0に戻す。その後`0x005CF1E9`で-133を指定し、共通後片付けへ進む。これは20時台に報告済みの経路。

**新しい差分:** Vorbisヘッダ解析`0x005CF167 CALL 0x005D44C0`が非0を返す場合、`0x005CF171 JNE 0x005CF1E9`で直接-133の共通後片付けへ飛ぶ。この分岐は**前述の配列`_free`／ポインタ0化を実行しない**。シリアル配列が既に確保された入力でヘッダ解析に失敗するなら、同じ-133エラーでも配列が残る場合がある。共通後片付け`0x005CF1F2 CALL 0x005D3DE0`と`0x005CF1FB CALL 0x005D3D00`は、別のパース用オブジェクトを受け取る（シリアル配列ポインタの引数ではない）。

## 3. 新発見B：呼出し元がエラー時に解放をスキップ

呼出し元`0x005CF4D0`では、ローカル所有配列ポインタを`0x005CF528 MOV [EBP+08],EAX`、カウントを`0x005CF52B MOV [EBP-08],EAX`で0に初期化。`0x005CF5AB LEA EDX,[EBP-08]`、`0x005CF5AF LEA EAX,[EBP+08]`で双方の**アドレス**を`0x005CF5BE CALL 0x005CF010`へ渡す。

- CF010が非0で終了すると、`0x005CF5CB JNE 0x005CF701`に分岐する。`0x005CF701`はレジスタ復元・returnのエピローグであり、シリアル配列を解放する命令を持たない。
- CF010成功後の再帰CALL `0x005CF628 CALL 0x005CF4D0`が非0でも、`0x005CF635 JNE 0x005CF701`で同じエピローグに直行する。
- 親が配列を解放する`0x005CF643 CALL _free`には、**再帰CALLが成功した場合だけ到達する**（`0x005CF63B`でローカルポインタを検査）。

**結論（条件付き）:** 一時シリアル配列を確保した後、重複ではないVorbisヘッダの異常または再帰子側の異常で戻ると、親が所有する配列を解放する機会を失う。別の参照・外部所有の証明は未完了であり、**潜在的なメモリリーク候補**である。実際のゲームで異常ファイルを再生して漏れることやヒープの最終所有者を追跡したわけではない。「同じ-133でもクリーンアップが異なる」と「子エラーで親が解放しない」は**一つの所有権リスク区分**で管理し、二重計上しない。

## 4. 分岐モデル・Golden準備

以下は**原作を実行した試験ではなく**原作PEの分岐条件に対応した合成所有権モデル。

| シナリオ | 配列free | 返却状態 | 静的懸念 |
|---|---|---|---|
| 同一BOS serial重複 | CF010で`_free`、ポインタと件数0 | -133 | この局所配列は解放済み |
| serial追加後、Vorbisヘッダ異常 | CF010特殊freeを経由しない／親はエピローグへ | -133 | ローカル配列が残る可能性 |
| 親がserial配列を持ち、再帰子でエラー | 親`0x005CF643`をスキップ | 子の非0コード | ローカル配列が残る可能性 |
| 正常な再帰復帰 | 親が条件付きで`_free` | 正常 | 期待される所有権解放 |

Golden実測は**0件**。後日許された環境で、（A）重複シリアル、（B）追加後の不正Vorbis identification/setup header、（C）複数リンクでの子側失敗、（D）正常連結を分離した入力fixtureを設計し、実際のheap所有・解放イベントの観測可否を判断する。元原作データの改変や実行は今回行わない。

## 5. 監査・正式REA・PC安全

- 独立検査：**94/94 PASS**。原作EXEバイト断片、E8 direct CALL、Jccの変位、索引CALLの一致、関数擬似C SHA、前回監査、分岐モデルを含む。94関数を新規抽出した意味ではない。検証スクリプトの初回実行では検証側のGhidra擬似C文字列表記の期待値が合わず93/94で失敗したため、実際の表記に合わせて検証器を訂正した。最終94/94を確認。
- 関数別正式5種類証拠：info=`INDEX_ONLY`、pseudo=`INDEX_ONLY + native交差照合`、assembly=`TARGETED_PE_NATIVE`、callers=`INDEX_ONLY + E8照合`、callees=`INDEX_ONLY + E8照合`。**REA正式5証拠完成0関数、新規正式VERIFIED0**。
- 正式TODO/VERIFY/BLOCKED差分=0/0/0。独立オフラインVERIFY論点1件を追加整理（正式台帳未変更）。原作ゲームGolden PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。
- 新規REA/Ghidra起動=0、原作ゲーム起動=0、Work使用なし。PC CPU負荷／空きRAM／active.lock=不明。スクリプトの実行時間は検証JSONを参照。研究全体所要時間は未測定。
- 原本ZIP/EXE/SAVE、PCのMASTER/QUEUE/PROGRESS/既存RUN/他レーン/Git/公開先/スケジュールを変更していない。安全拒否済み範囲やWave6は一切操作していない。

## 6. 次回再開位置・同期条件

次は`0x005CFA10`と`0x005D1490`という**他の`0x005CF010`直接呼出し元**について、同じエラー伝搬と一時配列所有権を比較する。また`0x005CF320`のEOF/読込エラー伝搬を追跡する。今回の-133ケースに対し、実際にVorbis解析失敗へ至る最小のパケット条件を静的に確定する。

PC復帰後、**最新版**`MASTER_LEDGER.md`／解析規約／`QUEUE.json`・`PROGRESS.md`／既存evidence/runs／owner/active.lock／研究ID・SHA・競合を先に確認し、REA担当範囲で非重複なら一度だけ同期。**Libraryや会話へ保存した事実とPC正式台帳に反映した事実は区別する。**
