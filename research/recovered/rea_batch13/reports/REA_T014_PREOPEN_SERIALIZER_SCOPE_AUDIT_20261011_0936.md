# REA T014 — CreateFileA直前の0x435C10の役割境界（2026-10-11 09時台 JST）
状態: CONFIRMED-SAVED-ASSEMBLY（局所呼出順序）＋OWNER-A-CROSSCHECK（既存native意味同定）。ファイル残存・呼出元事前削除・実ゲームはVERIFY。
対象は承認済みhash E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回source bytesの再hashなし、新規Ghidra/REA実行0。
対象関数VA 0x460000、Task T014。保存run 20261009T212627835Z。
info: ev_76fca377cfc1ee6b6dd225934568ef4fb94e52cc359d35beff1ccb7ef68d99c3
pseudo: ev_06e5a34750f37c054b3f916ca1d135ab52b3b62b35043ac84ffc8b0a668e05c4
assembly: ev_fec99c35153c8902d10879722c3a8fcb90bcdd434f62a9dedd7878e352529394
callers: ev_91099310a072569d892f9a238b2b7849ecf367b30cd5bbcd0c8fbb0f74bc7724
callees: ev_3ed77f73bd20825ba6b7b67779b97a50404d10e858d64bc85630b7d585c0a0a0
## 独立クロスチェック
0x460571: string writer 0x470830、0x460585: 0x471D20、0x460596: 0x435C10、0x4605CA: CreateFileAの順に保存Ghidra assemblyで確認。
A所有data/T014_GLOBAL_SAVE.mdの「normal save tail」節では0x471D20をDiplomacy runtime状態writer、0x435C10をworld-base+0x504のSpotElm/SpotPath/SpotEscapePath graph serializerと同定し、reader対応0x471AF0/0x435550を記録。
従って0x435C10を「事前にファイルをDelete/Truncateしている候補」として最優先監査する根拠は弱い。主機能はstream graph直列化として独立資料でも整合。
ただしcalleeに隠れたfilesystem副作用の完全不存在を証明するものではない（直接全命令を今回再取得せず）。
0x4605BE: disposition=4（OPEN_ALWAYS）、0x4605D4..DD: INVALID_HANDLE_VALUE時cleanup、0x460687: WriteFile、0x46068E: CloseHandleを保存assemblyで再照合。
0x460000内の直APIフローはOPEN_ALWAYSを切詰め操作へ変更せず、WriteFileの戻り値/実書込長をこの局所経路では検査しない。
## 未確定・次回
優先1: caller 0x45F960（auto.savを含む）・0x53A100の同パス事前削除/rename/切詰めを、既存owner-A保存nativeで追加検証。
優先2: 0x46060Aの間接virtual呼出の副作用、loaderのファイル長/余剰末尾処理、合法な旧EXE UI長→短save実測（PASS0、現時点で実行せず）。
既存T014を変更せずVERIFY維持。A〜E/MASTER/T018/QUEUE/PROGRESS/Git/設定/automationは編集対象外。
## 集計（保存run14本/最新sync 20261009T230531140Z）
Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12。合計39/48 STATIC VERIFIED、今回新規0。P0 20/21、P1 19/27、TODO8、VERIFY1。
研究MASTER cp83 DONE9/34（IN_PROGRESS21/VERIFY4）、旧EXE Gameplay golden PASS0。ゲーム再実装率は測定していない。
PC: Local sessions0、Java/Ghidra/REA名process検出なし、CPU n/a・空きRAM未測定。active.lockはdecomp_task直下の一覧に無し。重い解析0・逆コンパイル0分、監査所要時間未計測。
過去SAFETY_REFUSALのrun_decompile.ps1、0x5710C0..0x571500新逆解析、REAテキスト抽出は再試行・迂回せず。