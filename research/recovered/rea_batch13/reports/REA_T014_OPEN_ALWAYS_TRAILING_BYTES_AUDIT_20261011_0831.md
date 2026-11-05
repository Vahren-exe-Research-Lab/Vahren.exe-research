# REA T014 — 通常saveのOPEN_ALWAYSと末尾残存リスク（2026-10-11 08時台 JST）
状態: CONFIRMED-SAVED-ASSEMBLY（0x460000局所API呼出と分岐のみ）／末尾残存・ロード影響・原作不具合はVERIFY。新規REA/Ghidra実行0件。
対象: ver0.67承認済み解析コピー、saved run 20261009T212627835Z、source/end SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回再hashなし）。
関数: 0x460000、T014、info ev_76fca377cfc1ee6b6dd225934568ef4fb94e52cc359d35beff1ccb7ef68d99c3。
pseudo ev_06e5a34750f37c054b3f916ca1d135ab52b3b62b35043ac84ffc8b0a668e05c4
assembly ev_fec99c35153c8902d10879722c3a8fcb90bcdd434f62a9dedd7878e352529394
callers ev_91099310a072569d892f9a238b2b7849ecf367b30cd5bbcd0c8fbb0f74bc7724
callees ev_3ed77f73bd20825ba6b7b67779b97a50404d10e858d64bc85630b7d585c0a0a0
## 既存静的証拠の新規照合
- 0x4605B7..0x4605CA: CreateFileAへGENERIC_WRITE=0x40000000, share=0, creationDisposition=4 (OPEN_ALWAYS), flags=0x80, template=NULLを渡す。CREATE_ALWAYS(2)やTRUNCATE_EXISTING(5)ではない。
- 0x4605D4..0x4605DD: INVALID_HANDLE_VALUEなら書込を飛ばしてcleanupへ。
- 0x46065Cで0x427040を呼んだ後、0x46067D..0x460687でWriteFile(hFile, buffer, EBX byte count, &stackBytesWritten, NULL)を1回呼ぶ。
- 0x46068D..0x46068Eで直ちにCloseHandle。0x460694のCMPはbuffer capacityと比較し、I/O戻り値や実書込長の検査ではない（前回監査を再確認）。
- 保存済みGhidra pseudoはCreateFileA(...,4,0x80,...), WriteFile(...), CloseHandle(...)と一致。保存済み関数の外部API直接呼び出し中、SetEndOfFile / SetFilePointer / truncating reopen は確認されない。
## 解釈と未確定事項
- Windows APIのOPEN_ALWAYSは既存ファイルを切り詰めず開く。したがって『同一パスの既存saveが新payloadより長い、かつ事前に削除・切詰めされない』場合には、従来の末尾バイトが残る可能性がある。
- これは**条件付きの互換性リスク**であり、現時点でゲーム画面のセーブ破損/原作バグと認定しない。呼出元0x45F960/0x53A100や事前helper 0x435C10による削除、別の保存経路、readerがEOF以降を無視するかは未検証。
- 次回優先: 既存の合法な静的証拠で0x45F960/0x53A100および0x435C10の事前ファイル処理が判明するか調べる。原作実機goldenはNOT RUN、制御された長→短save UI比較は将来の試験設計のみ。
## 進捗・安全
- Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、累計39/48静的VERIFIED。今回増加0。P0 20/21・P1 19/27・TODO8・VERIFY1。MASTER最新cp83、研究DONE9/34。旧EXE Gameplay golden PASS0。ゲーム再実装率は測定していない。
- PC: Local接続成功、start時terminal session0、process CPU n/a、RAM未測定、active.lockはdecomp_task一覧で検出なし。新Ghidra/Java/REA実行時間0分、今回監査経過時間未計測。
- 過去SAFETY_REFUSALのrun_decompile.ps1/0x5710C0..0x571500/REA extract、およびCPU/RAM shell調査は再試行・迂回なし。原本/QUEUE/PROGRESS/MASTER/A-E/T018/dev/Git/MCP/automationを変更しない。