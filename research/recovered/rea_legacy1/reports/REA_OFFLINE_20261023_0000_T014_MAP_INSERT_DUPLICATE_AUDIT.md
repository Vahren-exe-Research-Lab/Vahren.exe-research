# 迫真戦記 ver0.67｜REA T014 P0・キー登録重複処理の独立静的監査

- 記録ID: `REA-OFFLINE-20261023-0000-T014-MAP-INSERT-DUPLICATE-OWNERSHIP-STATIC-01`
- 実施時刻: 2026-10-23 00時台 JST（予定実行開始 00:00:19）
- 区分: **OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY**
- 今回の対象: `0x416B90` / `0x4165B0` / `0x416E80` / `0x5433D0`、未解決間接CALL `0x543428`

## 先行確認・出典

Desktop Commander Local Compactの最初のREAD要求は `INVALID_ARGUMENT: McpServerError: Session terminated` で終了。**接続障害であり安全拒否ではない。** PCオンライン状態、owner、`active.lock`、CPU/RAM、最新QUEUE/PROGRESS/既存runは確認不可。原本PCへの書込なし。

正規のChatGPT LibraryからオフラインZIPと原作 `Vahren.exe`、既存MASTER・解析レーン規約を取得。ZIPのCRCは**34/34 PASS**、SQLite integrity_check **ok**。元EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、オフラインZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。保存済みGhidra検索DBは2026-10-21版でありPC現行正本とは未照合。既存run/PROGRESSは旧パックのスナップショットであり最新ではない。

## 今回の新規静的発見（前回の「重複キー未確定」を具体化）

`0x54340B CALL 0x416E80` が **0x2Cバイト**の新規候補ノードを生成し、続く `0x543417 CALL 0x416B90` が既存のキー付きmapへ渡す。`0x416B90`の正常分岐は単一の「毎回挿入」ではなく、**新規挿入 / 既存キー重複**で異なる。

1. **新規挿入**： `0x416C3C` と `0x416C86` はともに `CALL 0x4165B0`。その後`0x416C4C`／`0x416C96` が出力先`+4`へ `1`（挿入成功）を代入。`0x4165F7 INC ECX`→`0x4165F8 MOV [EDI+8],ECX`により **mapの要素数を1加算**する。
2. **既存キー重複**： `0x416C6A CALL 0x405370` の比較後 `0x416C71 JE 0x416CA1` が別の正常経路。`[EBX+0x20] >= 16` なら新候補の文字列ヒープを `0x416CAB CALL 0x5B6BBB` で解放し、`0x416CC8 CALL 0x5B6BBB` で新候補ノード本体を解放。`0x416CD5 MOV [EAX],ESI` が既存ノードのiteratorを返し、`0x416CD9 MOV BYTE [EAX+4],0` が「挿入なし」を返す。ここでは `0x4165B0` は呼ばれず、正常経路ではmap件数は加算されない。
3. **オフセット誤認防止**：`0x416CA1 CMP [EBX+0x20],0x10` の `EBX` は**候補ノード**であり、その`+0x20`は文字列のバッファ容量。`0x5433F6 MOV EBX,[ESI+0x20]` の `ESI=context` の場合に読む**map要素数**とは、同じオフセット表記でも別オブジェクトである。

`0x416B90` の新規／重複両経路は `RET 0x0C`（スタック引数12バイト回収）。出力先は先頭4バイトにiterator、続く1バイトに挿入真偽を持つ。Ghidra疑似Cと原作EXEの機械語の両方に対応。候補文字列・ノード解放は静的証拠からの分類であり、実行失敗時の完全な例外安全性までは未証明。

## P0間接CALL `0x543428` との関連

`0x5433F6 MOV EBX,[context+0x20]` は登録**前**のmap件数を保存し、`0x543417`による新規／重複キー処理の**結果フラグを参照せず**、`0x54341C TEST EBX,EBX`→`0x54341E JNE 0x54342A`により、事前件数が0のときのみ`0x543428 CALL EAX`へ進む。ここから下記の区別を導ける。

| 登録前のmap | キー | 挿入フラグ | 件数変化 | このガードによる仮想CALL |
|---|---|---:|---:|---|
| 空（0件） | 新規 | 1 | +1 | 条件ガード上は実行側 |
| 非空 | 新規 | 1 | +1 | スキップ |
| 非空 | 既存 | 0 | 0 | スキップ |

※正常な局所制御フローが前提。上位追加条件、例外、副作用と仮想CALL内の処理は未検証。特に`context+0x10`が指す二次オブジェクトの**writer・vptr・具体的な呼出先VAは引き続き未解決**。今回それを特定したとはしない。

## 自動再検証と進捗

同梱の独立検証器で原作PE32のVA→ファイル位置を復元して命令バイト**37/37 PASS**、CALL相対参照**7/7 PASS**、分岐先**2/2 PASS**、4関数のGhidra疑似C SHA **4/4 PASS**、SQLite直接CALL索引**7/7 PASS**、間接CALL`0x543428`索引 PASS。実行時間**0.72749秒**。総調査時間未計測、PC負荷不明。

REA正式`info/pseudo/assembly/callers/callees`の5証拠は**新規完成0関数、VERIFIED昇格0**。既存Wave1–5 VERIFIED **64/64**は過去報告値（今回未再認証）、古いPROGRESSの **15/16** は別の時点・範囲なので加算しない。正式TODO/VERIFY/BLOCKED差分 **0/0/0**、原作ゲームGolden PASS **0**、strict MATCH **0**、再実装率未計測。

## 旧成果との重複と次の再開位置

2026-10-22 16:33はキー登録順序、19:46はmap件数、20:35は11サイトの空mapガード、22:36はchoice別経路の調査。**今回の増分は `0x416B90` の二経路・メモリ解放・結果フラグ・件数非増加を元EXE命令で具体化したこと**であり、11サイトや既存VERIFIEDを再計上しない。

次のP0は`context+0x10`への書込元→生成・vptr設定の関数範囲と参照関係を既存検索DBで追う。PC復帰時は最新MASTER/QUEUE/PROGRESS/owner/lock/既存ID/ハッシュを照合してからREA担当所有範囲だけ同期する。安全拒否対象`0x5710C0..0x571500`・既拒否Wave6への再試行なし。原本EXE/ZIP/SAVE、他レーン、MASTER、Git、スケジュールは変更していない。

機械可読証拠: `REA_OFFLINE_20261023_0000_T014_MAP_INSERT_DUPLICATE_EVIDENCE.json`。再検証器: `verify_rea_t014_insert_duplicate_20261023.py`（SHA256 `5B8793229EBB794D1818EC0B007CFF8657880236D123FA968129718ED9F85709`）。**この報告の作成だけでLibrary保存・PC同期・独立readbackが完了したとは扱わない**。保存操作の実結果は別途報告する。
