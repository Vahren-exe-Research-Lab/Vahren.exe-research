# REA T014 — global.sav 既存キー更新・新規挿入の分岐監査（2026-10-12 09:37 JST）
- 範囲: REA保存済みrun `20261011T113414092Z` の0x428710（T014）をread-only照合。新規REA/Ghidra実行0、関数VERIFIED増加0。承認コピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 を今回再hash MATCH。原本EXEは実行・変更しない。
- info `ev_18083c1e4b216eb84426042a80e5dd8d28b884882f59162ab8f5fe1cb74a64d6` (entry 0x428710, length3252, noncontiguous 4 ranges)
- pseudo `ev_562ea04990ecb04a74ea0796d27a7c629a061894e46952f31b87c452af188775`
- assembly `ev_a8b58058d05e576dbaa8ebd22736dcfa684d5fb5289e0897e1e5834eb351ec4b`
- callers `ev_21421f53fb9052bf2f3b7cbee448c0bfe34b814e644d49db93939e7b14d7719a` (resolved 0x514270/0x567210/0x567840)
- callees `ev_607a477af0d6bc95128190a05f5ff119d4c08a35d1691703c6e75331d4b7adc0`
## 今回の局所的な新確認
- 0x428757..0x42879B: guard bit `0xB09620 & 1` の初回経路で、`0xB09604` の固定文字列を「----------」（10文字）に初期化する。
- 0x428831..0x4288C6: global.sav がFindFirstFileAで見つからなければCreateFileA(disposition4 OPEN_ALWAYS)を実行し、既定marker文字列を長さ+1（NULを含む）でWriteFile後CloseHandleへ進む。これを完全な新規save妥当性・初期ファイル形式として一般化しない。
- 0x4289B0..0x428A1F: 既存ファイルサイズを取得、読込、`0x4270F0`を通して復号、`0x429C60`でstreamを構成。
- 0x428ADF..0x428B4A: 共通token reader `0x4705F0` を用い、10文字markerとの文字列内容・長さ一致ならrecordループを脱出。通常recordは0x428B7F token/0x428B8D int32を読み、`0x4A69B0`へ渡す。
- 0x428C31..0x428C5D: `0x4C1200` tree lookupの結果がsentinelと異なる（既存node）場合、node+0x28で辿ったpayload+0x1C DWORDに新数値を**その場で上書き**して新規node挿入をせず進む。
- 0x428C62..0x428CD9: tree lookupの結果がsentinel（未登録）の場合、0x20-byte candidateを作り、payload+0x1Cへ値を格納し、`0x436560 -> 0x436680 -> 0x4A69B0` によって**新規挿入経路**へ進む。
- 0x428DB3..0x428EAA: tree entryごとに`0x470830`で文字列2件と`0x4628F0`でDWORD数値をstreamへ出力し、最後に共通終端token `0xB09604` を出力。0x428F59 encryption `0x427040`、0x428F84 WriteFile、0x428F8B CloseHandle。
- 0x428EC2..0x428ED4: 更新時CreateFileA(disposition4 OPEN_ALWAYS)。既存長より短くなる場合に末尾残留の可能性はあるが、先行事前操作やdecoderの余剰扱い・実ファイル短縮は今回未証明。これを確定破損バグとしない。
## 再実装の留保／進捗
- T014: global.savは「キーがあればpayload DWORDを更新、無ければnodeを追加、その後全件を直列化し直す」局所フロー。重複キーの全保存形式・順序の全保証、I/O return検査の上位作用、EOF、不正/不足バイト、旧EXE実機結果はVERIFY。
- 0x4705F0のGhidra resolved caller13件のうち、既存7件に今回0x428710を加えて**8/13用途分類済み**。未分類5件=0x45EAC0,0x470550,0x58E480,0x5A90E0,0x5B0400。間接呼出は13に含まれない。
- Wave1〜5: 16/16,10/10,10/10,12/12,16/16＝64/64 STATIC VERIFIED、P0=29/29、P1=35/35、今回+0。Wave6候補0/16、候補P0=5/P1=11、未着手16・関数単位VERIFY0。研究MASTER checkpoint83 DONE9/34（21 IN_PROGRESS/4 VERIFY）、旧EXE実機golden PASS0、ゲーム再実装率は測定していない。
- 最新保存sync `logs/progress_sync_20261011T153958076Z.json`: QUEUE更新STALE_RENAME_DENIED、PROGRESS更新SKIPPED_QUEUE_STALE。以前拒否されたrename/overwrite/syncを反復・迂回せず、正式Wave6開始を保留。
- 今回Local preflight: CPU12%、空きRAM15.55GiB、Java/Ghidra/REAプロセス検出なし、active.lockなし、target SHA MATCH。重い解析実行0秒、軽量調査総経過時間未計測。REA6.1.0/Ghidra12.1.4・単一セッション・最大4関数・Ghidra900000ms/request960000ms維持。
- 次回: 保存済みT014 0x45EAC0ほか4 callerの証拠所在を調べ、証拠不足なら機能ラベル未確定のままとする。Wave6開始は正式キュー問題の安全な解消後のみ。
- 所有境界: 本新規REA専用文書のみ作成。原本ZIP/EXE、A〜E/MASTER/T018、他研究、Git/push、MCP設定、automation、安全拒否0x5710C0..0x571500/REA抽出の操作はしない。
