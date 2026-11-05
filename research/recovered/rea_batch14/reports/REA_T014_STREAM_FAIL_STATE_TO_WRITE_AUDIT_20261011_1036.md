# REA T014 通常セーブwriterのstream状態分岐 — 保存済み静的証拠監査（2026-10-11 10時台 JST）
状態: CONFIRMED-SAVED-ASSEMBLY（関数0x460000の局所branchのみ）。stream failure時の実際のI/OとgameplayはVERIFY。新規Ghidra実行0。
対象: 承認済み解析コピーを扱った保存REA run 20261009T212627835Z（対象source SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187）。今回の実ファイルhash再計算なし。
VA: 0x460000 / Task T014 / 保存runでinfo・pseudo・assembly・callers・calleesの5結果がVERIFIED。
info: ev_76fca377cfc1ee6b6dd225934568ef4fb94e52cc359d35beff1ccb7ef68d99c3
pseudo: ev_06e5a34750f37c054b3f916ca1d135ab52b3b62b35043ac84ffc8b0a668e05c4
assembly: ev_fec99c35153c8902d10879722c3a8fcb90bcdd434f62a9dedd7878e352529394
callers: ev_91099310a072569d892f9a238b2b7849ecf367b30cd5bbcd0c8fbb0f74bc7724
callees: ev_3ed77f73bd20825ba6b7b67779b97a50404d10e858d64bc85630b7d585c0a0a0
## 今回追加確認した命令レベルの分岐
- 0x4605D4..5DD: CreateFileAが-1なら0x4606ADへ直行（既知）。それ以外でstream状態検査へ入る。
- 0x4605E3..5EF: stream系object vptr offsetからfield indexを得て、stack状態byteに0x06 maskでTEST。非0なら0x46061Cへ。
- mask=0の分岐は0x4605F1..60Aで仮想関数offset+0x28を呼ぶ（引数0,0,1,2）。0x46060Cと0x460613が返却された長さ/位置候補をEAX・EBXへ格納し0x460638に合流。
- mask非0の分岐0x46061C..631ではglobal[0x6098B4]およびglobal[0x6098B0]を使用し、EAX=0にする。0x460638でEBX+=EAX。
- 両分岐は0x46063A..65Cの変換helper 0x42A340→暗号化helper 0x427040へ合流し、0x46067D..687のWriteFile到達経路が残る。stream状態mask非0だけを理由とする、この局所での即時cleanup分岐はない。
- 0x46068D..68E CloseHandle、0x460694以降はbuffer容量条件（既知）。WriteFile戻り値の局所チェックは見えない。
## 留保と互換実装への影響
- global[0x6098B0/0x6098B4]の静的値・意味、mask0x06の正確なstd::ios状態対応、仮想関数戻りの妥当性と例外経路は未確定。pseudoの型推論は警告付きのため、fallback書込byte数や破損発生を決めつけない。
- 『stream状態異常ならwriterは一切WriteFileしない』という仮定を再実装に埋め込まない。正常・異常streamのbuffer生成・byte countと上位save完了通知は独立VERIFY。
- 呼出元 0x45F960 / 0x53A100 の事前削除・事後確認は未解析。旧EXE gameplay goldenはNOT RUN、原作確定バグとはしない。
## 進捗と安全
- Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12。重点累計39/48 STATIC VERIFIED、今回増加0、P0 20/21・P1 19/27、TODO8/VERIFY1。
- MASTER最新cp83、研究DONE9/34。旧EXE実機golden PASS0。ゲーム再実装率は測定していない。
- 保存済みREA証拠のread-only監査で新規重いREA/Ghidra/Java・原本実行なし。安全拒否済操作の再試行・迂回なし。A-E/MASTER/T018/QUEUE/PROGRESS/他領域/Git/MCP/automationは変更しない。
