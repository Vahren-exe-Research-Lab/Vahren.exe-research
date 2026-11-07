# 迫真戦記 ver0.67｜REA 2026-10-28 07H P0 CRT ファイル長変更・ゼロ拡張静的監査
研究ID: `REA-LOCAL-20261028-07H-P0-CHSIZE-ZEROFILL-WRITELOOP-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED=0、原作ゲームGolden PASS=0。
原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
10/21索引DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 1. 先行照合・新規範囲
MASTER、A～E owner規約、REA README/QUEUE/旧PROGRESS/最新 sync(20261011T153958076Z)、検索README/BUILD_MANIFEST、06H証拠を先読。PCオンライン、active.lockなし。06H監査再実行40/40 PASS。
07Hは06Hが残した第2呼出元 `0x005D2FC9` を分析。検索CLI `callers 0x005C9E03` から caller function `0x005D2F0C` を特定。単独の `function 0x005D2FC9` はNOT_FOUNDだが、これはCALL siteであって関数入口ではない。正しい `function 0x005D2F0C` は `__chsize_nolock`（438 bytes、Ghidra VS2010 library match）。この区別を新規索引欠落と誤認しない。
06Hは `__write_nolock` 内部の部分書込・戻り値ABIを調査済み。今回はその関数の別用途（ファイルサイズ伸張／縮小）だけを独立追加した。

## 2. STATIC-A：第2呼出元はゼロ埋めファイル拡張
`0x005D2F26` 現在位置、`0x005D2F42` ファイル終端を `__lseeki64_nolock` で取得。x86で戻り値はEDX:EAX、`0x005D2F59 SUB ESI,EAX` / `0x005D2F5B SBB EDI,EDX` で要求最終サイズと現ファイル終端の64-bit差分を算出する。
正の拡張差分には `0x005D2F6D MOV EBX,0x1000`（4096 B）と `0x005D2F73 PUSH 8` → `0x005D2F75 GetProcessHeap` → `0x005D2F7C HeapAlloc` を使用。Windows HeapAlloc flags 8 = HEAP_ZERO_MEMORYでゼロ初期化したバッファを確保する。
`0x005D2FA0 PUSH 0x8000` → `0x005D2FA8 CALL 0x005D30C2` は `__setmode_nolock` で**一時的にbinary mode**へ切替える（改行変換防止）。`0x005D2FB2..0x005D2FC2` で残量と4096の小さい方を選び、`0x005D2FC3` buffer、`0x005D2FC6` fdをpush、`0x005D2FC9 CALL 0x005C9E03` でゼロデータを追記する。
`0x005D2FD1 CMP EAX,-1` が失敗判定。非-1なら `0x005D2FD6 CDQ` と `0x005D2FD7 SUB` / `0x005D2FD9 SBB` で64-bit残量から**実際の返却書込バイト数**を差し引き、正の残量は `0x005D2FDD JG 0x005D2FB2` で再試行する。06Hの一般`__flush`とは異なり、この伸張loopは部分書込を残量から差し引いて続行する。

## 3. STATIC-B：縮小・失敗時・復帰の分岐
要求サイズ < 現終端の場合、`0x005D303D` で要求サイズへseekし、`0x005D3053` でOSハンドルを取得して `0x005D305A CALL [0x006091D8]`（KERNEL32!SetEndOfFile）により切詰めを要求。失敗時 `0x005D307A` でerrno=13(EACCES)、`0x005D3087` GetLastErrorを_doserrnoへ格納する経路を確認。
拡張時のHeapAlloc失敗は `0x005D2F8E` でerrno=12(ENOMEM)。書込-1の場合は `0x005D300C` で_doserrno確認、値5なら `0x005D301B` でerrno=13(EACCES)へ変更する経路を確認。
拡張loopを離れると `0x005D2FE6` で保存済みモードを `__setmode_nolock` に渡して復元し、`0x005D2FFF` HeapFreeで一時バッファを解放する。成功時は `0x005D30A8` のseekで**元のファイル位置へ復帰**してから `0x005D30BB XOR EAX,EAX`（成功0）となる。失敗時 `0x005D2F94` → `0x005D2F99 MOV EAX,[EAX]`（errno値を戻す）へ分岐して元位置復帰を省く経路がある。よってこのCRT helperの失敗時にはseek済み現在位置が残り得る（要Golden観測）。
無進捗について、対象loopの終了条件は `EAX==-1` または残量0/負への到達。正の書込要求に対しhelperが**0を返し続ける仮定**では、残量が減らず再試行し続ける形。実ファイルの当該状況における0返却到達性・hangは未確認、ENGINE_BUG確定不可。

## 4. IAT・検索索引・5種証拠
固定IATをPEインポートテーブルから独立確認: `0x00609188` GetProcessHeap、`0x00609134` HeapAlloc、`0x00609154` HeapFree、`0x006091D8` SetEndOfFile、`0x00609158` GetLastError。すべてKERNEL32.dll（実行中のIAT変更は対象外）。
初期DB `calls` / V9 `native_callsite` とも、`0x005D2FC9` (__write_nolock)・`0x005D2FA8`・`0x005D2FEC` (__setmode_nolock)・`0x005D2742` (__chsize_nolockへの上位CALL)の**4箇所各1件**。この範囲の直接CALL索引漏れ0。
5種: info=INDEX_ONLY、pseudo=INDEX_ONLY+NATIVE cross-check、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY+NATIVE。独立静的監査52/52 PASS。正式REAの5種類の新規証拠パックは未取得。原作ゲームGolden PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。
既存Wave1～5の最終保存同期=64/64 VERIFIED（旧QUEUE/PROGRESSのEPERM表示は古い）。新規VERIFIED=0。正式TODO/VERIFY/BLOCKED差分=0/0/0。今回静的証拠はゲーム実行結果ではない。

## 5. 次回の優先研究・安全なGolden設計
次VAは `0x005D2370` の `0x005D2742` call-site（ゲームコードとの到達関係/CRTのみの使用状況）と、前回繰越 `0x005CA1D1..0x005CA4EB`（console/Unicode部分書込の正確な補正）。
Golden候補は**原本と無関係な使い捨てファイル**で、要求長の境界[現在長, +1, +4095, +4096, +4097]、任意の現在位置からの増減、失敗注入時のmode/カーソル/errno変化を比較する設計。いずれも今回実行なし。ファイル拡張loopの0バイト無進捗観測は安全な強制停止とタイムアウトを前提とし、現時点では設計のみ。
他ownerのT014/T015資料・E正本や検索DB自体は未変更。原本ZIP/EXE/SAVE、QUEUE/PROGRESS、既存RUN、Git、公開先、スケジュール変更なし。REA/Ghidra新規実行なし、Work使用なし。
