# REA 2026-10-25 14時台｜READBACK記録

研究ID `REA-OFFLINE-20261025-1436-P0-CALLOC-ABI-FILE-LOADER-STATIC-01`  
状態：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
原作EXE起動：0回。新規Ghidra/REA実行：0回。PC-SAVEDは未確認。

独立監査 `85/85 PASS`。別プロセスで監査を再実行した証拠JSONは**元JSONとバイト完全一致**。旧研究を二重計上せず、原作Golden=0、新規正式REA VERIFIED=0。

| ファイル | SHA256 | bytes |
|---|---|---:|
| `REA_OFFLINE_20261025_14H_CALLOC_ABI_REPORT.md` | `ce6eed82c72855e9857ef5723dc9902f3cd94f3f27ecbe766bcf6328858741ea` | 9829 |
| `REA_OFFLINE_20261025_14H_CALLOC_ABI_EVIDENCE.json` | `ba8e8e0221ee6b4277f505221ffbfdb892f6b699bd593b8225aa1075a365784b` | 13883 |
| `REA_OFFLINE_20261025_14H_CALLOC_ABI_AUDIT.py` | `5f36b2a08338dc8bb4ce6f3159011cbeef0a1acdcc7e5d8e6dee509f5b5a9619` | 12226 |

検証元：Libraryから明示的に取得した旧オフラインZIPと原作研究用EXE（SHA、CRC一致）、Ghidra SQLiteの読み取り専用一時コピー。独立x86 machine byte / E8 CALL target / Ghidra CALL + indirect CALL/ data_ref照合。

PC接続エラー：`INVALID_ARGUMENT: McpServerError: Session terminated`。安全拒否ではない。PC側MASTER/QUEUE/PROGRESS未変更、PC readback未実施。Library保存・復元検証は別途実行後に確定する。
