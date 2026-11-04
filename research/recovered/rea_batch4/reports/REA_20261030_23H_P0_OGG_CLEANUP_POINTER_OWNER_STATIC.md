# 迫真戦記 REA｜2026-10-30 23H｜Ogg cleanupバッファ所有権と最終callback（P0）
研究ID：`REA-LOCAL-20261030-23H-P0-OGG-CLEANUP-OWNERSHIP-ALLOCATOR-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。22Hの間接dispatch先4関数の発見を再計上しない。
## 今回の新規静的証拠
- `0x005D1490` で `0x005D1540 call _calloc`（1×0x20）→`0x005D1549 mov [esi+0x48],eax`、`0x005D154C call _calloc`（1×0x10）→`0x005D1557 mov [esi+0x4C],eax` を原作同一SHA研究コピーのCapstone ASMで確認。
- `0x005CF010` はポインタ値を引数として `0x005CF06B→0x005D3DA0`（初期化）・`0x005CF074→0x005D3CE0`（初期化）。前者 `0x005D3DC4 call _calloc`（1×0xE50）と `0x005D3DCC mov [esi+0x1C],eax` により、0x20バイト管理構造体の内部で追加heap所有を開始する。
- `0x005CFA10` はlink mode=0時に `0x005CFBAB/0x005CFBB4` から `outer+0x48/+0x4C` に保持された**ポインタ値**を `0x005D3DE0/0x005D3D00` へ渡す。リンク再初期化は `0x005CFC2F→0x005CF010`。
- `0x005CFE00` の最終解放はlink配列のelement strideを0x20と0x10に分け、`0x005CFE56/0x005CFE61` で各要素をcleanupしてから、`0x005CFE80/0x005CFE89` で所有配列をfreeする。
- **新規の例外境界**：`0x005CFE00` は `0x005CFEE3` で `outer+0x2C8` の関数ポインタを読み、`outer[0]!=0` かつ関数ポインタ非NULLなら `0x005CFEEE call eax` を実行する。これは22Hに解決した内部descriptor型デストラクタ3箇所とは別の、最終cleanupでのユーザーcallbackである。実際のcallback先と副作用は未同定。
## 境界と実装上の注意
- malloc/callocが成功し通常heap契約が保たれる限り、`outer+0x48/+0x4C` の2つの生存heapブロックとouter自身は別allocationであり、直接のフィールド別名参照は生じない。一方NULL返却、破損ポインタ、サイズ・リンク数不整合、free後使用、再入による状態変化は否定できない。
- `0x005CF4D0` の `0x005CF5BE→0x005CF010` はstack上の一時領域を渡す別caller。すべての使用例がouter+0x48/+0x4Cと解釈されるわけではない。
- V9擬似Cは機械出力、ネイティブABIの正式確定ではない。5種正式REA証拠の新規一式0／新規VERIFIED0。
## 監査・保存
- 原本研究コピーSHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 SQLite SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、quick_check=ok。V9 info/pseudo/callers/callees索引と局所PE assemblyを照合。
- 監査42/42 PASS（0.8869秒）。初回40/42はCapstoneの変位表記4/8と0x4/0x8の照合文字列不一致（分類OTHER）。監査スクリプト内だけ修正、結果未保存のまま再実行し42/42 PASS。RECOVERY-ID：`REA-RECOVERY-20261030-23H-FORMAT-ONLY-01`、未反映差分なし。
- 以前の正式STATIC VERIFIED 64/64（保存済syncログ）、正式TODO/VERIFY/BLOCKED書込差分0/0/0、原作Golden実測PASS0、完全複製率未測定。ゲーム/REA/Ghidra再実行0。
- PCオンライン、開始時active.lock不在。確認時FreePhysicalMemory=11148480 KiB（約10.63GiB）、CPU負荷・全作業時間不明。原本/MASTER/QUEUE/PROGRESS/旧RUN/他lane/Git/自動化設定は変更なし。
## 次回
- `0x005D3E2B/0x005D3E5D/0x005D3E9C` のtag読出しから、tag writerと有効範囲を追跡。別途 `0x005CFEEE` callbackの設定元をV9 refsから追い、外部再入によるstate guard不変条件への影響をVERIFY。
- Golden条件案：link=0/1、count=0/1/2、alloc成功/失敗、EOF/ハードエラー、callback有無を区別し、位置・state・フレーム消費・復旧性を比較。**未実測**。

