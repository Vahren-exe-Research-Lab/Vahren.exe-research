# REA T014 通常セーブのI/O戻り値経路の独立監査（2026-10-11 07時台 JST）
状態: CONFIRMED-SAVED-ASSEMBLY（0x460000局所制御フローのみ）／実機でのエラー時挙動は VERIFY。新規逆コンパイル0件。
対象: 迫真戦記ver0.67承認済みコピーの保存済みREA run 20261009T212627835Z。source SHA/終了SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回実ファイルの再hashなし）。
対象関数: 0x460000, T014, Ghidra entry 0x460000, length 2096 bytes, status VERIFIED（元runで5操作整合）。
info: ev_76fca377cfc1ee6b6dd225934568ef4fb94e52cc359d35beff1ccb7ef68d99c3
pseudo: ev_06e5a34750f37c054b3f916ca1d135ab52b3b62b35043ac84ffc8b0a668e05c4
assembly: ev_fec99c35153c8902d10879722c3a8fcb90bcdd434f62a9dedd7878e352529394
callers: ev_91099310a072569d892f9a238b2b7849ecf367b30cd5bbcd0c8fbb0f74bc7724
callees: ev_3ed77f73bd20825ba6b7b67779b97a50404d10e858d64bc85630b7d585c0a0a0
## 局所命令の新規交差照合
- 0x4605B7..0x4605CA: CreateFileA引数はGENERIC_WRITE 0x40000000、share=0、OPEN_ALWAYS(4)、FILE_ATTRIBUTE_NORMAL(0x80)。既存A/T014で確認済みの条件を再確認。
- 0x4605D4..0x4605DD: CreateFileAがINVALID_HANDLE_VALUE(-1)なら0x4606ADの共有後始末へ直接分岐し、WriteFile/CloseHandleの両callを飛ばす。
- 正常handleなら0x46065Cの暗号化helper 0x427040を経て0x460687: WriteFile、0x46068E: CloseHandleを連続呼出。
- WriteFile直後にその戻り値(EAX)のtest/cmpはなく、bytesWritten出力用stack slotの予定長との比較もこの局所後段では見られない。次の0x460694のCMPは文字列buffer capacity 0x10対[ESP+0xEC]であり、I/O成否フラグ比較ではない。
- CreateFileA失敗時とWriteFile/CloseHandle後はいずれも0x4606ADの共通cleanupへ合流し、関数はvoid型としてretする（保存Ghidra疑似コードとも整合）。本関数内の明示的なI/O error result返却は確認できない。
## 厳密な限定／再実装向け
- 上記は単一writerの局所静的分岐のみ。上位callerによるファイル存在・sizeの事後検査、CRT/SEH経路、I/O障害のユーザー表示、失敗セーブの再ロード結果は未検証。原作の確定バグ／silent corruptionとは断定しない。
- 既存A/T014のglobal.sav Writer 0x428F84でのWriteFile返値非検査とは別の、通常 .savの独立callsite証拠であり、旧ゲームgolden PASSへの加算はしない。
- 実機Golden設計候補は、正常save→size/再ロード成功を可視確認する合法UI試験と、I/O失敗時の挙動を分けること。原本起動禁止につき今回実行せずNOT RUN。
## 進捗・安全
- Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、累計39/48 STATIC VERIFIED。今回新規VERIFIED0、未着手8/VERIFY1、P0 20/21・P1 19/27。最新MASTER cp82は研究DONE9/34、旧EXE実機golden PASS0。再実装率未測定。
- ローカル保存済み証拠のread-only再監査のみで新Ghidra/REA/EXE起動なし。既往拒否のrun_decompile.ps1、0x5710C0..0x571500、REA text抽出、CPU/RAM shell probeは再試行・迂回しない。QUEUE/PROGRESS・A～E・MASTER・T018・原本・Git/設定/automationを変更しない。
