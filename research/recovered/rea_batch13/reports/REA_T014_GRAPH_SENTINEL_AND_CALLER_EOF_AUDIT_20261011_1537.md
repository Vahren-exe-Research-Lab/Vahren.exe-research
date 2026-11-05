# REA独立静的監査 / T014 通常save graph最終sentinelからloaderへ戻る経路（2026-10-11 15時台 JST）
状態: CONFIRMED-SAVED-NATIVE（直接命令と局所分岐）/ VERIFY（間接callee・実save・上位ユーザー可視動作）。旧ゲームNOT RUN、新Ghidra/REA0件。
対象コピーのsource SHA256は保存run記録 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回は実体のSHA再計算なし。
対象VA: reader core 0x45E1E0 / graph reader 0x435550 / load wrapper 0x45E5F0（研究T014）。
一次参照: rea_lab/decomp_task/runs/20261009T225741694Z/RUN_RESULT.json と、read-only既存native exe/T014_NORMAL_LOAD_PROBE.txt / exe/T014_TAIL_PAIR_DUMP.txt。
REA 0x45E1E0: info ev_5da50720924339f770fe37dd127f90a1d8faff1b1c9c80922819ec9f7c999ef0; pseudo ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e。
REA 0x45E1E0: assembly ev_69ab9492fa443fe12c5fb3e0d6230b5c7bb67fcca9fbc5c2915973a18d18e124; callers ev_25b1ebae191adb744c52e90f5c7faa796423ecd9edc00b29aa5a5b241415b65e; callees ev_1c6253652438f3553d6e578d8b3afdc47b832a780c4732bf2d4117a9ca1a3f42。
## 今回の独立した接続点
- 保存REAのcallers結果は0x45E1E0の解決済direct callerとして0x45E5F0を1件返す。indirect caller全件不在の証明ではない。
- 0x45E5F0: 0x45E691 CreateFileA(GENERIC_READ / OPEN_EXISTING=3)、0x45E6C4 file size取得、0x45E6E3 ReadFile、0x45E6E9 CloseHandle、0x45E6F2 decode 0x4270F0。その後0x429C60経由で読み取り用streamを作る。
- 0x45E75Eで 0x45E1E0 をcallし、戻った直後は0x45E763 add esp,4→0x45E76E 0x5B71DD→0x45E780 0x428680→buffer cleanup→0x45E7B2 ret 8。coreの後に直接のstream position/size/EOF比較は見えない。
- 0x45E1E0は0x45E53E 0x471AF0（外交）、0x45E54C 0x435550（Spot graph）へ順にcallし、0x45E551以降cleanup、0x45E5EF return。core後に直接EOF比較は見えない。
- 0x435550は先頭group sentinel 0x65C828を0x4355A8から比較、続く0x65C844/0x65C860と最後の0x65C87Cを使った文字列終端判定を持つ。
- 最終の0x65C87C比較（0x435ADE..0x435B32）で一致側は0x435BBDのcleanupへ進み、0x435BEA ret 8に至る。最終sentinelを読んだ後の直接stream残量/物理EOF比較は見えない。
## 推論と限界
- 本reader chainの通常終了経路では『全入力を消費した』ことを明示検証していない。正しい最終sentinel以後に余剰byteが残る場合、当該direct pathはその存在だけでは失敗しない可能性がある。
- ただし、ReadFile/decode/stream helper/各virtual readerが例外を投げる、より上位のcallerが再検証する、ファイルを事前truncateする等の可能性は残る。『必ず余剰を許容』『旧ゲーム確定バグ』『ゲーム実機成功』とは断定しない。
- writer 0x460000がOPEN_ALWAYSで明示truncateしない従来確認と独立に照合。短い再保存→旧末尾残存は依然条件付きVERIFY。
## 次回優先と運用
- T014: 0x45E5F0の直接caller/後続処理、0x429C60 stream構築/0x4270F0 decode失敗時の扱い、0x435550末尾のvirtual payload error伝播を保存済み証拠で確認。
- Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12、累計39/48。新規VERIFIED0、P0 20/21・P1 19/27、TODO8/VERIFY1。MASTER checkpoint83、DONE9/34、旧EXE actual golden PASS0、ゲーム再実装率未測定。
- CPU n/a、空きRAM未測定、Local sessions0、Java/Ghidra/REA/Vahren名一致なし、active.lockはディレクトリ表示なし。新規REA/Ghidra解析0、実行時間0分、静的監査時間未計測。
- 既往run_decompile.ps1安全拒否・禁止VA/抽出を再試行せず、原本・A-E・MASTER・T018・QUEUE/PROGRESS・Git・設定・automation変更なし。