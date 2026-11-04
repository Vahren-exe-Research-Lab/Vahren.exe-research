# 迫真戦記 ver0.67｜REA 16時台 P0 DirectMusic bad_allocの最外側CRT SEH
研究ID: REA-LOCAL-20261026-16H-P0-DMUSIC-CRT-SEH-XCPT-FILTER-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY。2026-10-26 16時台 JST。
研究用PE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
既存Ghidra検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 開始時・重複の分離
MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、15Hの報告・EVIDENCE、検索基盤README/MANIFESTを先読。旧QUEUE/PROGRESSは既知EPERMでstale、保存同期ログ20261011T153958076Zの64件を参照（今回新規計上しない）。
15Hで確定済み: 0x004BE480/0x004BD2A0にはC++ catchなし、0x00555CD0の2個のcatchは0x00555DEFの呼出位置を保護しない。今回は**さらに外側のCRT例外フィルタ**を新たに調べた。

## 新規静的証拠A：DirectMusicからEXE entryまで
0x004BE480（new失敗）→0x004BD2A0（CALL site 0x004BD3E4）→0x00555CD0（CALL 0x00555DEF）→0x005554F0（CALL 0x00555918）→___tmainCRTStartup 0x005B84D7（CALL 0x005B85EC）→PE entry 0x005B8644（0x005B8649はJMP）。原作PEとGhidra索引を照合。
0x005554F0は本範囲の機械語内に自身のFS:[0]例外登録がなく、0x00555918の呼出し後に通常後片付け（0x00555929のDeleteDC相当、Direct3D関連Release、CoUninitialize相当）が続く。例外時に通常命令順へ戻るとは仮定しない。

## 新規静的証拠B：CRTにはSEH4の外側フィルタがある
- 0x005B84D9 PUSH 0x006412C0、0x005B84DE CALL 0x005BB680（__SEH_prolog4）。
- scope header（0x006412C0）: FFFFFFFE / 00000000 / FFFFFF88 / 00000000。
- scope row（0x006412D0）: enclosing=FFFFFFFE, filter=0x005B8606, handler=0x005B861A。
- 0x005B8572でEH state=0に変更した後、0x005B85ECで0x005554F0を呼ぶ。従ってこの外側SEH filterは起動側のcallを覆う。
- filter 0x005B8606は0x005B8612で0x005BE999（__XcptFilter）を呼ぶ。例外handler 0x005B861Aは0x005B862Aの__exit等へ分岐する。
**訂正**: 15H時点の「3関数のcatch外」を「更に外側にもcatchが無い」と拡大解釈してはいけない。SEH4フィルタは存在する。ただしそれがC++例外を処理するかは別問題。

## 新規静的証拠C：C++ bad_allocは初期状態のXcptFilter対象外
- 0x005B6C2B→0x005B864E（__CxxThrowException@8）経由のRaiseException用静的定数0x00609978は **0xE06D7363**。
- 0x005BC596: CRT __initptdがPTD+0x5Cに既定例外表0x0060B198を設定。
- 既定表は12×3 DWORD。例外コードは C0000005, C000001D, C0000096, C000008D..C0000093, C00002B4, C00002B5（全12）。**E06D7363は存在しない**。初期handler slotも12件とも0。
- __XcptFilterの0x005BE9BBは1件12byteずつ比較し、0x005BE9BEの表長は0x90(144=12×12)。不一致側0x005BE9D6/0x005BE9E3でEAX=0を返す。
- 従って、default PTD表・無改変runtime・他に適合catchがないという条件では、外側SEHはbad_allocを捕捉せずEXCEPTION_CONTINUE_SEARCH相当に進む。**ゲームの実機クラッシュ確認ではない**。
- VEH、未調査の追加例外ハンドラ、外部ランタイム変更、OSの終端動作は未確認。通常終了経路のCOM/DC解放不実行と「恒久的リーク」は同一ではない。

## Ghidra body長の扱い
検索索引の ___tmainCRTStartup size_bytes=319 を関数先頭から直線的なbyte spanと仮定すると0x005B8616で終わり、0x005B8612のCALL命令末端や0x005B861Aのhandlerを取りこぼす。原作機械語では0x005B8643のRETまで続く。これは body size と線形ASM範囲を同一視しない警告であり、Ghidra DBの関数帰属情報そのものが不正だとは断定しない。

## 独立監査・結果・差分
REA_20261026_16H_P0_STARTUP_SEH_AUDIT.py でPE SHA、SQLite SHA/quick_check、旧64件、PE entry、対象native ASM、SEH scope、RaiseExceptionコード、12件の例外表、CALL site、通常後片付け位置を照合。**43/43 PASS**、初回実行約0.36秒。保存時再照合もPASS。
REA形式証拠：info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY。新規正式5種完全充足=0、新規正式VERIFIED=0。既往Wave1〜5=64/64（旧同期ログのみ）。
正式QUEUE/PROGRESS TODO/VERIFY/BLOCKEDの書込差分=0/0/0。今回独立のVERIFYは「標準CRTフィルタがbad_allocをcatchしない」という条件付き仕様と、グローバルVEH等の存在未調査。原作ゲームGolden実測PASS=0、strict MATCH・完全複製率は未測定。

## Golden（設計のみ、NOT RUN）
1. 初期状態で管理配列newを失敗させた場合のC++例外コード、CRT __XcptFilter返値、終了経路を記録。
2. 2番目の0x5C byte new失敗時、+0x70の配列free/COM解放の有無を追跡。
3. 正常終了では0x00555929後のDeleteDC/Release/CoUninitializeが呼ばれることを比較。
4. default例外表・signal変更後・外部VEH登録ありを分離し、明示catch有無を比較。
全て未実行。安全拒否済みVA/Wave6/REA export操作には接触しない。

## 保存・安全・次回
PC接続成功、active.lockなし。空きメモリ約12.28GiB、CPU負荷16%（開始時PC全体の単発値）。研究総時間不明。新規REA/Ghidra/ゲーム起動0回、Work0回。
保存先はREA所有decomp_taskのみ。原本ZIP/EXE/SAVE、A〜E、MASTER、T018、dev_lab、QUEUE/PROGRESS、旧run、Git、公開先、スケジュールは不変更。旧OFFLINE-UNSYNCED成果は未同期のまま。
次P0：0x005BE999の例外表変更者・signal API経路と、0x004BE480 +0x70配列の全参照/後片付け有無を既存DBから追跡。原作クラッシュ・メモリリークの確定はGoldenまで保留。
