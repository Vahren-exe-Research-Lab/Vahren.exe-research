# 迫真戦記ver0.67｜REA独立静的研究 2026-10-25 14時台

- **研究ID**：`REA-OFFLINE-20261025-1436-P0-CALLOC-ABI-FILE-LOADER-STATIC-01`
- **状態**：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- **優先対象**：`0x005D1490` の `_calloc` 呼出しと ABI／間接CALL、補助 `0x005D1630`・`0x005D16C0`・`0x00502020`、前回未解決 `0x0068DC80`
- **差分の扱い**：13時台の `REA-OFFLINE-20261025-1333-P0-CALLOC-OVERFLOW-CALLERS-STATIC-01` を残す。本報告は**別の呼出元におけるGhidra推定の誤り・ABI・確保失敗時の利用側処理**を扱い、既存の乗算ガード発見を二重計上しない。

## 1. 基盤・未同期の境界

Desktop Commander Local CompactでWindows PCのMASTER、プロトコル、REA README/QUEUE/PROGRESS、検索基盤を一括先読しようとしたが、`INVALID_ARGUMENT: McpServerError: Session terminated`。**接続障害**であり安全拒否ではない。PC起動状態、CPU/RAM、現在のactive.lock、最新owner/QUEUE/PROGRESSおよび旧runの現存性は確認できない。

代替としてLibrary `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `/Vahren.exe` の実在・アクセスを確認し、読み取り専用で調査。EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、ZIP内 `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` を実測・一致。ZIP全34エントリのCRC・SQLite quick_checkもPASS。SQLiteは一時ファイルの read-only immutable 接続でのみ照会し、原本、ZIP、DBを変更していない。

**重要**：使用DBは2026-10-21の旧スナップショットで、2026-10-22のcanonical V3より古い。ZIPのREA `PROGRESS.md` は2026-10-09時点の `15/16`。PC現行正本や過去報告の `Wave1～5 64/64` と同一・統合済みとみなさない。

## 2. P0新発見：Ghidra `_calloc(2,4)` が実際の機械語と一致しない

Ghidra疑似Cの `FUN_005d1490`（`0x005D1490`）は、後段の割当てを `piVar3 = _calloc(2,4);` と表示する。しかし原作のx86命令は次のとおり。

```asm
0x005D1597  MOV EDI,[EBP-0x0C]  ; 呼出先が設定する値
0x005D159A  LEA ECX,[EDI+2]
0x005D159D  PUSH 4               ; 各要素4バイト
0x005D159F  PUSH ECX             ; 要素数は (EDI+2) の実行時値
0x005D15A0  CALL 0x005D1C71     ; _calloc
```

**実際の第1引数は固定値2ではなく、`uint32_t(EDI+2)`**。`EDI`は直前に`[EBP-0x0C]`から読まれ、`0x005D1572`で呼ぶ`0x005CF010`に渡すローカル出力ポインタの値として設定される経路がある。Ghidraの `calloc(2,4)` を正本扱いすると必要バッファサイズが誤る。

`0x005D15B6`の `LEA EAX,[EDI*4]` が後続の `memcpy` バイト数となる。配列の先頭8バイトをメタデータに使い、残りに`EDI`件の4バイトデータをコピーする設計と整合する。**型・個数の完全な意味、元ファイルのフォーマット、入力上限はVERIFY**。

## 3. P0新発見：明示されないレジスタABIと4引数callback

`0x005D1630`では`0x005D163A MOV ESI,[EBP+0x0C]`と`0x005D165B MOV EAX,[EBP+8]`を準備してから、`0x005D165F CALL 0x005D1490`を行う。`0x005D1490`は受け取った`ESI`を構造体ポインタとして使用し、`EAX`の値を内部で利用する。Ghidra疑似Cの `unaff_ESI` / `in_EAX` は通常の引数一覧に反映されていないため、**再実装・フック時にレジスタ契約を落としてはいけない**。

また `0x005D14AC CALL EBX` は直接CALLではなく、DBにも `CALL EBX` / `POINTER_OR_VIRTUAL_UNDETERMINED` と記録されている。機械語の直前で `PUSH 1`、`PUSH 0`、`PUSH 0`、`PUSH EDI` を行い、呼出し後に `ADD ESP,0x10`で16バイトを解放する。Ghidra疑似Cが `(*param_4)()` と**引数を省略している箇所**だが、実際には**4つのスタック引数を渡す間接CALL**である。ターゲットの完全なABIと戻り値意味はなおVERIFY。

呼出しチェーンはGhidra直接CALL索引と原作E8相対CALLで一致した。

`0x00502020` → CALL site `0x00502038` → `0x005D16C0`（fopen/fread/fcloseを用いるファイル入力系）→ `0x005D1712` → `0x005D1630` → `0x005D165F` → `0x005D1490`。ゲーム側のファイル入力に接続される可能性は高いが**対象ファイル形式・個別ゲーム機能の識別は未確定**。

## 4. 新規VERIFY：戻り値NULLを使う前に検査していない分岐

少なくとも次の3箇所で、`_calloc`の戻り値がNULLでないことを確認する分岐を挟まずにデリファレンスする局所経路を機械語から確認した。

| `_calloc` CALL | 最初の対応する利用 | 注意 |
|---|---|---|
| `0x005D15A0` | `0x005D15B1 MOV [EAX],ECX` | NULLの場合は書込に到達し得る |
| `0x005D15D2` | `0x005D15E8 MOV [EDI],0` | EDIは直前のcalloc結果 |
| `0x005D15E0` | `0x005D15FE MOV [EAX],EDX` | `ESI+0x3C`経由で結果を再読込 |

この内部 `_calloc`（`0x005D1C71`）は呼出先の失敗でNULLを返し得ることを先行調査と今回のバイト照合で確認した。よって**資源枯渇時に解放不能なクラッシュ経路があり得る**が、実際のゲームで失敗条件が生じるか、より外側で入力・確保が保証されるかは未確認であり、確定バグや脆弱性認定はしない。

`EDI+2` と `EDI*4` は32bit算術なので、異常に大きな `EDI` の場合に加算・乗算が循環する数理上の可能性がある。例：仮にEDI=`0xFFFFFFFE`なら `EDI+2` は0、`EDI*4` は `0xFFFFFFF8`。**入力がこの値に達するという証拠はなく、仮想境界条件としてのみ記録**する。`0x005CF010`の出力上限および呼出し元の条件を先に確認すべき。

## 5. 前回P0の補足：timeout共有変数は3種類のCRT wrapperが読む

`DAT_0068DC80`に対する旧Ghidra `data_refs` は計6件、**READ6 / WRITE0**、`pointer_refs`は0。`__malloc_crt`（`0x005BAFAE`）に2件、`__calloc_crt`（`0x005BAFF3`）に2件、`__realloc_crt`（`0x005BB03F`）に2件。各wrapperにはSleep待機／再試行の論理がある。**新規差分**として、`__realloc_crt`は`0x005BB05B`で要求サイズ=0を判定し、0ならSleep再試行せず戻ることをASMで独立確認した。

直接参照がすべてREADであっても、アドレス計算・間接書込み・外部ランタイム更新がない証明にはならない。通常ロード後の変数不変性は**引き続きVERIFY**。この6直接READとcalloc guardの発見は13時台と重複するので新規件数には加算しない。

## 6. 独立監査・証拠階級

`REA_OFFLINE_20261025_14H_CALLOC_ABI_AUDIT.py` はPython標準ライブラリのみを使用し、ZIP CRC、EXE/ZIP/SQLiteハッシュ、SQLite quick_check、関係する9関数の保存済みGhidraコード、対象x86命令バイト、E8相対CALLの実着地点13件とCALL索引、間接CALL `0x005D14AC`、6つのdata_refs、ポインタ参照、算術モデルの計**85/85件PASS**。別プロセスでも **85/85 PASS**、再生成した証拠JSONは完全に同一バイト列。数字85は**検査項目数**であり85関数のVERIFIEDではない。

REA正式証拠5種類の現況：`info`・`pseudo`・`callers`・`callees`はGhidra索引の**参考情報のみ**、`assembly`は原作EXEの**対象箇所の抜粋のみ**。REA所定の関数別5点セットの正式取得・内容検証・登録は行っていない。**新規正式VERIFIED=0**。既存Wave1～5 `64/64` は過去の報告値として維持・非合算。古いZIP内の `15/16` とも合算しない。

正式QUEUE/PROGRESSを書いていないので**正式TODO/VERIFY/BLOCKED/VERIFIED書込差分は0/0/0/0**。当回は新規調査メモ上のSTATIC・VERIFY候補が増えただけで、正式カウントには反映していない。**原作ゲームGolden=0（未実機測定）、strict MATCH=0（実測なし）、完全複製率未測定**。

## 7. 保存・安全・次回

PCオンライン状況、CPU/RAM、PC total runtimeは**不明**。新規Ghidra・REA・原作ゲーム実行はすべて0回。Python独立監査はおよそ1.86秒（再実行時の単体計測）。前回09時台に安全拒否された別監査ファイル・Wave6・指定禁止VA・既存正本・他レーン・Git・Work・既存スケジュールには触れていない。

今回の4成果（本報告、JSON、監査Python、READBACK）は当回の `/mnt/data` と許可されたLibrary `REA_OFFLINE_UNSYNCED` のみ保存予定。**PC-SAVEDとは記録しない**。Libraryへのアップロード可否と読み戻しの実績はREADBACKへ追記して別途確定させる。

**次回優先**：`0x005CF010`の`param_5`（件数出力）更新経路および上限判定を呼出元`0x005D1490`と突合し、`0x005D15A0`の確保数 `EDI+2` が正常入力でどこまで増え得るか確認する。間接CALL `0x005D14AC` の実ターゲットはcallback登録元のxrefとfreadのABIから限定する。PC復帰後は**最新MASTER/QUEUE/PROGRESS・owner・lock・既存ID・source SHA・競合**を照合し、REA所有範囲だけ一度同期する。

**障害ID：** `REA-RC-20261025-1436-LOCAL-SESSION-TERMINATED-01`。試行：Local Compact read_multiple_files 1件。理由：`INVALID_ARGUMENT / McpServerError: Session terminated`。種別：`CONNECTION`。影響：PC現行正本・同期不能。許可された続行方法：アクセス確認済みLibrary資料と隔離一時コピーで静的研究、後日正本との重複照合。
