# 迫真戦記 ver0.67｜REA 20時台：OggDecoderの二段階破棄とワーカースレッド停止条件
研究ID：REA-LOCAL-20261025-2034-P0-OGG-TEARDOWN-THREAD-WAIT-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。独立静的監査71/71 PASS、原作Golden実測0、正式VERIFIED増分0。

## 最初に照合した基盤・非重複
- MASTER/レーン規約/REA README・QUEUE・PROGRESS・過去run一覧・2026-10-11最新progress_syncをread-only確認。同期記録Wave1～5=16+10+10+12+16=64/64、QUEUE/PROGRESSはEPERM後の古い状態を保持。
- 19時台ID REA-LOCAL-20261025-1934-P0-OGG-STREAM-GATE-STATIC-01 は状態+0x44の上位失敗判定とワーカースレッド開始まで確認済み。18時台はOggDecoder vtable +0x10 cleanupを解決済み。これらを新発見に二重計上しない。
- 原作研究専用EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 初期Ghidra search.sqlite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。SQLite quick_check=ok。
- 新規REA/Ghidra実行なし。既存検索DBを先に使用、対象の局所機械語のみpefile+Capstoneで別系統照合。

## 新発見1：失敗cleanupからの二段階OggDecoder破棄
- 0x004BEAFE PUSH 1、0x004BEB00 JE 0x004BEB86、0x004BEB88 CALL 0x004BF2B0。上位音声初期化失敗時にはparam=1でcleanupへ入る。
- 0x004BF2F0～0x004BF32Fは[owner+9]!=0かつ[owner+0xA0]!=NULLを条件とするOgg/stream側経路。stream側+0x44が非0なら0x004BF318のvtable +0x48処理と0x004BF31C→0x00502330を経由。非0・ゼロいずれでも0x004BF321→0x004BF327 CALL 0x00502160。
- 0x00502160は0x00502164で0x005021E0によりワーカースレッドの停止待機を先に行い、その後COM系参照[stream+8]を仮想+8で解放する。
- [stream+0]のdecoderについて、0x005021AF/0x005021B2でvtable+0x10を呼んだあと、0x005021BC/0x005021C0でvtable+0x00を引数1付きで呼び出す。0x005021C2/0x005021C5に双方の所有ポインタをNULL化する命令が存在。
- 既存で確定していたOgg vtable=0x006395CCのslot0は0x00501DF0、slot+0x10は0x00501EB0。新規の制御接続により、実際のOggDecoderオブジェクトでは「cleanup→deleting destructor(flag=1)」の**二段階破棄**となる。
- 0x00501DF0は0x00501DF9で再び0x00501EB0を呼んでから、0x00501DFEでdelete flag bit0を検査し、非ゼロ時に0x00501E0C→0x005B6BBBでヒープ領域を解放する。つまり同一オブジェクトにcleanupを二度実行する経路だが、0x00501EB0が先に[decoder+5]を0へ戻し、0x00501EB4/0x00501EB8のゲートで2回目の内部FILE* cleanupは抑止される。
- 上記は通常のOgg vtableでの静的到達経路。別vtable設定時、例外、非正規状態、並行操作中の完全保証はしない。

## 新発見2：スレッド待機ループに総待機期限がない
- 0x005021E3 MOV BYTE [ESI+0x4C],1で終了要求を立て、+0x48のスレッドハンドルがあれば0x005021F9でWaitForSingleObject(handle,100)を実行。
- 戻り値0（WAIT_OBJECT_0）なら0x00502204へ脱出。戻り値-1（WAIT_FAILED）でも同じ脱出。その他の値では0x005021F3へ戻って待機する。**100msは1回当たりの待機であり、総待機100msではない**。
- ループ脱出後の0x00502205/0x00502208は+0x4Cと+0x48を0に戻す。ここではCloseHandleの直接呼び出しを確認していないが、CRTの__beginthread側のハンドル管理を別途検証するまではリークと断定しない。
- 0x005023E0のworkerは0x00502410で同じ+0x4Cを読み、0x00502565/0x00502567でSleep(100)、0x0050256D/0x00502570で再び+0x4Cを検査する。通常の終了要求とpoll間隔が接続した。
- WaitForSingleObjectがWAIT_FAILEDを返してworkerが実際には稼働中だった場合、0x00502160は後続のdecoder解放へ進む可能性がある。**VERIFY仮説であり実ゲームの確定UAFではない**。__beginthreadが返すハンドルの寿命・外部close・スケジューリングを追跡する。

## 独立監査と正式REA境界
- ローカルREA専用新規監査：REA_20261025_20H_P0_OGG_LIFETIME_AUDIT.py、機械可読出力：REA_20261025_20H_P0_OGG_LIFETIME_EVIDENCE.json。
- 検査内訳：原作SHA/DB SHA/ImageBase、対象機械語44条件、vtable2、SQLite quick_check、関数6、直接CALL8、間接CALL6、worker direct callers0の検査1。合計71/71 PASS（各検査キーはJSON参照）。
- REA正式 info/pseudo/assembly/callers/callees：新規完備0関数（既存Ghidra機械出力・関数索引・xrefs参照＋局所ASM独立検査）。正式新規VERIFIED=0、正式TODO/VERIFY/BLOCKED**書込差分**=0/0/0。
- 既存静的VERIFIED=64/64（2026-10-11保存済同期の過去値）。旧runの正式再実行なし。原作ゲームGolden実測PASS=0、strict MATCH未測定、完全複製率未測定。

## 原作Golden条件案（DESIGNED / NOT RUN）
1. 正常Oggの作成・破棄時、decoder destructorは1回、decoder cleanupは呼出し経路により複数回になり得るがFILE* closeは所有時だけ1回であること。
2. 失敗Oggからの初期化後にstream resetを行い、+0x44/+0x48とdecoder所有ポインタが一致して解放されること。
3. workerがSleep中の通常停止要求と待機の反復回数を記録する。100msは反復単位であること。
4. 異常WaitForSingleObject戻値、__beginthread失敗戻値、別vtable時のdelete flagをそれぞれ分離（実際の注入検証は未実行）。

## PC状態・書込境界・次の研究
- PC接続成功。開始時active.lock=False。専用REA/Ghidra/Java競合検出なし。空きRAM約10.79GiB。CPU負荷不明。監査初回0.6511秒、再検査0.5562秒、保存監査0.5512秒。研究全体時間不明。新規REA/Ghidra/ゲーム実行0。
- 安全拒否済Wave6/0x5710C0..0x571500および09時台拒否追記を未実行。REA所有フォルダの20時台新規ファイルのみ作成。MASTER、QUEUE、PROGRESS、runs、他レーン、原本、Git、Work、スケジュールは無変更。
- 13/14時台Libraryオフライン成果はPC正本への正式同期未実施、今回もそのまま保持。
- 次回P0は0x005B7D14の__beginthreadのハンドル返却・終了処理、0x005023E0の全exitを検索基盤から追跡。次に0x005022C4のCOM vtable offset+0x0C実体とdecoder破棄経路を独立検証する。
