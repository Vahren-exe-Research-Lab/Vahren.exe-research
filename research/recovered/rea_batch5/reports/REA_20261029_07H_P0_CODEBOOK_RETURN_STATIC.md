# 迫真戦記 REA｜2026-10-29 07H Ogg codebook初期化の成功/失敗境界
研究ID: `REA-LOCAL-20261029-07H-P0-OGG-CODEBOOK-RETURN-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED=0。原作Golden実測PASS=0。
## 開始前の根拠・重複防止
- Desktop Commander Local接続成功。MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、共通ルール、REA README/QUEUE/PROGRESS/WAVES、既存RUN/最新sync、検索基盤README/BUILD_MANIFEST、直近05H/06H報告と証拠を照合。
- 初期キュー/PROGRESSの一部はrename EPERMで古い。2026-10-11最新成功sync `progress_sync_20261011T153958076Z.json` はWave1～5 **64/64 STATIC VERIFIED**。正式新規数0、TODO/VERIFY/BLOCKED差分0/0/0。
- 隔離研究EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、両方一致、SQLite quick_check=ok。
- 旧06Hで `0x005DA070` 非0が上位 `0x005D57C0→0x005D5BD0→0x005CF970` の-137に通じることを記録済み。本回は同じ-137を二重計上せず、**0x5DA070の返値が非0となる実際の下位条件**を絞る。
## P0-A｜0x005DA070のcodebook入口と早期成功分岐
- 入力 `[EBX+4]` の要素数を走査し、各コード長 `[ECX]` が **0より大きい** ときだけEDI（正の長さ件数）を増やす: `0x005DA0A0 CMP [ECX],0` / `0x005DA0A5 INC EDI`。
- `0x005DA0B6 TEST EDI,EDI`、`0x005DA0B8 JLE 0x005DA53D`。正の長さが0件なら `0x005DA53D XOR EAX,EAX` → `0x005DA548 RET` に直行。**空/非正長のみのcodebookがこの関数内では0（成功扱い）で帰る**。これが音声データとして正常かどうかは未実測。
- 正の長さがある場合、`0x005DA0C4 PUSH EDI; 0x005DA0C5 PUSH ECX; 0x005DA0C6 PUSH EDX; 0x005DA0C7 CALL 0x005D97C0`。EDX=長さ配列、ECX=全件数、EDI=正の長さ件数。Ghidraの引数省略が起こりやすい地点なのでnative PUSHも保存。
## P0-B｜明示エラー -1 の実際の境界
- `0x005DA0E9 TEST EDX,EDX` / `0x005DA0EB JNE 0x005DA103` は下位 `0x005D97C0` のNULLだけを明示失敗として捕捉。NULLの場合 `0x005DA0EE CALL 0x005D9ED0` でcodebookを片付け、`0x005DA0F6 OR EAX,-1` / `0x005DA102 RET`。前回06Hの上位変換により -1 → 上位1 → -137。今回新規判明は **どこで-1が生成されるか**。
- `0x005D97C0` はコード長を使う構築ヘルパーで、検証分岐 `0x005D9828 JNE 0x005D993D` と `0x005D98E3 JNE 0x005D9952` がともに保持配列を `_free` してNULL帰還する。前者は長さに対する割付済み範囲の検査、後者は最終コード空間の超過検査として読める。具体的なbit列の境界はGolden未実測のためVERIFY。
- 一方、`0x005D97C0` の `0x005D97DD CALL _malloc` は直後にNULL判定せず、正長エントリで `0x005D982E MOV [EBX],ESI` に到達し得る。したがって「メモリ確保失敗なら確実に-1、さらに-137」という一般化は**不可**。
## P0-C｜後続メモリ確保の非検査とread callback呼出元数
- `0x005DA070` の後続 `0x005DA1A7 CALL _malloc` の返値は `0x005DA1AC` で[ESI+0x14]に代入され、`0x005DA1F8`で再ロード、`0x005DA201`で書込。間に局所的なNULL条件分岐は確認できない。
- 他に `0x005DA218 CALL 0x005D99F0` → [ESI+0x10]、`0x005DA224 _malloc` → [ESI+0x18]、`0x005DA255 _malloc` → [ESI+0x1C]、`0x005DA2D4 _calloc` → [ESI+0x20]。後続配列がNULLの場合の実際の振る舞い、CRT終了動作、OOM再現性は**未検証**。
- 検索DB `calls` では `0x005D0FB0` の直接callerは `0x005D12E0` / CALL site `0x005D1303` **1件**。06H確認のwrapperはcallback第8・9引数を0にする。これは *確認済みの直接caller* の限定であり、computed CALL・関数ポインタ経由の不存在証明ではない。
## 独立監査・証拠等級
- `REA_20261029_07H_P0_CODEBOOK_RETURN_PROBE.py`：隔離PE対象範囲のCapstone x86静的逆アセンブルとSQLite直接CALL照合。
- `REA_20261029_07H_P0_CODEBOOK_RETURN_AUDIT.py`：原本識別、旧64/64と06H 48/48、DB quick_check、7関数の索引、直接CALL・30箇所のtarget native命令などを検証。**57/57 PASS、0.690秒、failed=[]**。これは静的assert数であり正式関数VERIFIED数ではない。
- info=SQLite関数索引、pseudo=保存Ghidra生成擬似C、assembly=隔離PE対象命令、callers/callees=SQLite direct CALLとsite。一式の新規REA独立5種エクスポートは **0件**。正式64/64維持、正式TODO/VERIFY/BLOCKED差分0/0/0、Golden実測0、strict MATCH=NOT RUN、完全複製率未測定。
- GhidraのCは機械出力。AV/ヒープ破損など実挙動は実ゲームで測っておらず、NULL経路も条件付き推定として扱う。
## Golden試験設計・保存/再開
- (NOT RUN) ①コード長すべて0 ②単一正長エントリ ③同長過密等で`0x5D9828`検査異常 ④ `0x5D98E3`の過剰割付 ⑤通常複数正長、の各系列で `0x5DA070` の0/-1、上位の-137、cleanup、音声のふるまいを比較。破損OGG入力は隔離してデータ原本を変更しない。
- オンライン。開始時active.lock無し、Java/Ghidra先行プロセス無し、RAM空き約15.78GiB、CPU使用率不明。新Ghidra/REA/実ゲーム/Workは起動せず、軽量静的監査0.690秒、研究全体所要時間不明。
- 新規REA所有ファイルのみ保存。原本ZIP/EXE/SAVE、MASTER、A～E、T018、RUN、QUEUE/PROGRESS、検索DB、Git、スケジュールは未変更。10/28のLibrary未同期証拠も保留。
- **次のP0：** `0x005D97C0` の2種エラー分岐のコード長条件を入力ベクトルとして形式化する。必要なら `0x005DA070` でNULLを調べず使うmalloc結果を、戻値レジスタの追跡で確認する。新規Golden試験は許可・隔離条件が整うまでNOT RUN。
