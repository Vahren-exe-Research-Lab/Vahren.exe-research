# 迫真戦記 ver0.67｜REA 2026-10-25 12時台 P0 _realloc 巨大サイズ・errno優先順位
研究ID：REA-LOCAL-20261025-1236-P0-REALLOC-OVERFLOW-ERRNO-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。原本は変更せず、原作ゲームGoldenはNOT RUN。
## 既存との差分（08～11時台結果は二重計上しない）
- _realloc入口VA 0x005C30BE、Ghidra保存済み疑似C・直接caller/callee、原作SHA一致PEのCapstone x86機械語を相互照合。
- **新規:** 0x005C311C CMP ESI,-0x20 → 0x005C311F JBE 0x005C30EC はunsigned判定。size<=0xFFFFFFE0がHeapReAllocへ進み、size>0xFFFFFFE0はOS呼出を行わない。
- **新規:** 巨大サイズ時は0x005C3122 CALL 0x005BBA77(__callnewh)の戻り値を検査せず、0x005C312D MOV [EAX],0xCでerrno=12、NULLを返す。new-modeの比較0x005C3109より前にこの経路を取るため、new-mode=0でもこのhandler呼出命令へ到達できる。handler自身が例外を送出すれば通常のerrno返却には到達しない。
- **新規:** 有効サイズでHeapReAlloc失敗時、new-mode=0なら0x005C3151 → 0x005C3158 GetLastError → 0x005C315F __get_errno_from_oserr。mode!=0なら0x005C3112 __callnewh、非0返却でretry、0返却後に0x005C3139 → 0x005C3140 GetLastError → 0x005C3147 __get_errno_from_oserr。元のOSエラーはhandler実行前に保存されていないため、handlerがLastErrorを変更した場合の差はVERIFY。
- **分岐区別:** _realloc(NULL,size)は0x005C30CC _mallocへ直接委譲。_realloc(nonNULL,0)は0x005C30DF _free後NULL。size=0の挙動をこの2つで統一しない。
- handler設定関数0x005BBA68を表す32bit絶対VA値のlittle-endian生バイトはPE各生セクション内に0件。相対CALL・算術構築・runtime変更・外部フックの不存在は証明しない。以前の直接caller1件は継承扱い。
## 独立監査と出典
- EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、初期SQLite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、統合V9 SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。一致。
- Capstone22命令、直接CALL6件、間接CALL3件（0x005C30FD/3140/3158）、new-mode data_refs、旧sync件数、検索SQLite quick_check、PE32ベース、setter絶対ポインタ生参照を独立検証。**40/40 PASS**、監査単体約1.039秒。これは関数数ではない。
- 保存済み検索DBは新規Ghidra実行なしでread-only照会。旧RUN_RESULTの一例 runs/20261009T212627835Z/RUN_RESULT.json はsource SHA、REA6.1.0/Ghidra12.1.4、5証拠の記録を照合。過去sync 64/64は維持するが全64件の再監査を意味しない。
- 五種証拠：info=既存検索基盤、pseudo=既存Ghidra機械出力、assembly=今回の22局所命令、callers=既存検索索引、callees=既存検索索引。新規正式五種完備=0、**新規VERIFIED=0**、正式TODO/VERIFY/BLOCKED書込差分0/0/0、Golden PASS=0、strict MATCH=0、完全複製率=未測定。
## 状態・障害・次回
- 事前preflight：PC接続成功、active.lockなし、検出したJava/Ghidra/REA競合プロセスなし、空きRAM約14GiB。CPU負荷と研究全体所要時間は未測定。新規REA/Ghidra/ゲーム実行0。
- 当回監査初回はWindowsのロケール依存read_text()が旧UTF-8 syncログの日本語パスを誤復号してJSONDecodeError。障害ID REA-LOCAL-20261025-12H-AUDIT-ENCODING-01。監査コードのみ明示的encoding='utf-8'に修正し最終40/40 PASS。安全拒否ではない。09時台の安全拒否済み未完成ファイルは未編集。
- 次P0：0x005C303C calloc乗算overflow時のerrno/handler分岐を同一原作SHAで独立照合。HeapReAlloc後handlerによるGetLastError変更はdynamic VERIFYのまま。
- 原本ZIP/EXE/SAVE、MASTER、QUEUE、PROGRESS、既存runs、A-E、Git、Work、既存スケジュールの変更なし。