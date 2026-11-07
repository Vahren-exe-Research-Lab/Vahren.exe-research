# REA 2026-10-25 11時台｜独立静的証拠のPC保存・再読取
研究ID：REA-LOCAL-20261025-1137-P0-CRT-GLOBAL-XREF-STATIC-01
保存対象：REA_20261025_11H_P0_CRT_GLOBAL_XREF_STATIC.md / REA_20261025_11H_P0_CRT_GLOBAL_XREF_EVIDENCE.json。新規2ファイル。既存資料上書きなし。
PC保存確認後、PowerShell Get-FileHashと独立Pythonプロセスで読み戻し・JSON parse・研究ID本文一致を検査。
REA_20261025_11H_P0_CRT_GLOBAL_XREF_STATIC.md：4622 bytes / SHA256 3A118E3997DB1C666F96C999F4BB404817527D31D894C7D7257B929DAF6CD93D
REA_20261025_11H_P0_CRT_GLOBAL_XREF_EVIDENCE.json：2580 bytes / SHA256 3CBF7AA917E35914639530FF1153B67D1A457538364E76F6C890063CD421CE37
独立Python readback：TRUE。JSON IDと報告書ID一致、監査36/36、グローバル2件。検証は静的条件でありVERIFIED関数数と異なる。
初回PowerShell Get-Content -RawによるID比較でFALSEとなったため、.NETの明示的UTF8 ReadAllTextと独立Pythonで再検査し両方TRUE。証拠本文・SHAは変更せず。
旧Wave1～5の過去同期VERIFIED64件を変更・再加算せず。新規REA5形式の関数別完備0、正式VERIFIED増0、TODO/VERIFY/BLOCKED書込差分0/0/0。原作Golden0、strict MATCH0、完全複製率未測定。
事前lockなし、競合専用Java/REA/Ghidraプロセスなし、空きRAM13.83GiB。CPU負荷と研究総時間は未計測。一次read-only監査0.666秒。新規Ghidra/REA/原作ゲーム実行0。
既拒否09H監査スクリプト56行は変更せず、他shell/path/toolでの拒否迂回なし。MASTER/QUEUE/PROGRESS/既存runs/他レーン/原本/Git/Work/スケジュール無変更。
継続位置：`0x005C30BE`巨大確保分岐とerrno優先順位、および`0x005BBA68`の関数アドレス経由間接到達の候補。状態STATIC/VERIFY/NOT READY。