# 迫真戦記 REA 2026-10-24 16時台 Library保存・独立読み戻し記録

**研究ID:** `REA-OFFLINE-20261024-1633-P0-DEFERRED-EXCLUSION-SET-INDIRECT-WRITER-STATIC-01`  
**分類:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**Library保存フォルダ:** `/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`  
**研究PC正本への同期:** **未実施**。

以下の3件は `files.manage_library(upload)` の `status=succeeded` を受け、**Libraryに保存された個別ファイルID**から `files.materialize` で別ディレクトリへ再取得し、元の各ファイルとバイト列が完全一致（SHA256一致）することを独立に確認した。

| ファイル | Library file ID | 保存後読み戻しSHA256 | 結果 |
|---|---|---|---|
| `REA_OFFLINE_20261024_1633_P0_DEFERRED_EXCLUSION_WRITER_AUDIT.md` | `file_0000000077488230a8b97048e4538ec4` | `088521AAD5FDF46A82C3B0FC5294C168F8EBC2A6708DCA0A09DBF17E20F2C9E0` | PASS |
| `REA_OFFLINE_20261024_1633_P0_DEFERRED_WRITER_EVIDENCE.json` | `file_00000000434c8230a9a322ede92cfdd1` | `20392722B82DEA7B7ED3C14AD278370100F616C498399824E17C08707981110D` | PASS |
| `verify_rea_20261024_16h_deferred_set_writer.py` | `file_0000000048748230ae3c99ed73846248` | `53C27B3E26C5EF5DB6280197E4D4D550E4AADBBB5FF41C067918CEF860084711` | PASS |

**別プロセス再実行:** 保存した監査プログラムをLibraryから読み戻したコピーから起動し、同じ旧ZIP/原作一致EXEを読み取り専用で検証。**87/87 PASS**。事前JSONと再実行JSONは `audit_seconds` （実行時間の観測値）のみを除いて完全一致。

**正式評価:** 機械語・参照関係に基づく限定的静的検証。正式REA `VERIFIED`の新規追加0、原作Golden0、実行到達性・ポインタ寿命・10,274関数版現行DBとの照合は未完了。正式QUEUE/PROGRESSは変更していない。

**接続障害:** `REA-RC-20261024-1633-LOCAL-SESSION-TERMINATED-01`。Desktop Commander Local Compact の一括読取 `McpServerError: Session terminated`。安全拒否ではない。PC正本MASTER/owner/latest queue/active.lock不明。安全拒否済み対象の再試行・迂回なし。

**次の再開位置:** PCが利用可能になったら現行DB・MASTER・QUEUE・PROGRESS・既存ID・owner/lockを最初にread-only照合。今回のIDが正本にないこと、ハッシュ衝突や同等発見の重複がないことを確認した後、REA所有範囲だけ一度同期。その他の製品コード/他レーン/Git/スケジュールは変更しない。
