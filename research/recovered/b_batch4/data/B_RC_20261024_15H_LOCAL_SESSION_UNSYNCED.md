# 迫真戦記 新B｜15時台 CONNECTION / OFFLINE-UNSYNCED 復旧記録

ID: `B-RC-20261024-15H-LOCAL-SESSION-01`。2026-10-24 15:16 JST、B owner/T012。

最初のDesktop Commander Local Compact `read_multiple_files` （PC正本MASTER・B規約・B HANDOFF）: `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。分類 **CONNECTION**、新規安全拒否なし。PC上の最新checkpoint・owner予約・既存ID/重複・未同期回収（22ファイル vs 後続10研究）・既拒否資料・Library訂正版は確認不能。PC保存0、PC readback0、原本/Git/設定/Work/スケジュール操作0。

ユーザーが許可した既存ZIPのみをread-only取得。ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、CRC 34/34 PASS。SQLite manifest SHA一致、quick_check=ok。EXEはZIP不収録につき今回原作SHA現物検証なし。旧安全拒否範囲及び拒否済み本文/コマンドへの再試行・迂回0。

独立解析（詳細=`B_T012_STR_STACK_ALIAS_LOOKUP_OFFLINE_20261024_15H.md`；証拠=`B_T012_STR_STACK_ALIAS_LOOKUP_EVIDENCE_20261024_15H.json`）：`B-OFFLINE-20261024-15H-T012-STR-STACK-ALIAS-LOOKUP-01`。`0x00599BD0`内の`auStack_1628 + 0x20 == iStack_1608`を`0x004647D0`の`param_4[8]`書込と結び、欠損時0・成功時node+0x20の出力を限定STATIC-GHIDRAとして確認。PC正本への同期は未実施、正式READY0/GOLDEN0/strict0。

次回: PC接続復帰後に最新MASTER/HANDOFF/安全拒否/PC既存ID/ownerを優先、意味的重複・競合を照合し、B所有data/exeとB HANDOFFへ許可された増分だけを一度同期。現状**OFFLINE-UNSYNCED / VERIFY / NOT READY**。
