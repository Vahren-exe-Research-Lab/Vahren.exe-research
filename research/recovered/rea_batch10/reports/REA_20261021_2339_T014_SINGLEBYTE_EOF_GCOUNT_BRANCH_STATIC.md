# REA-20261021-2339-T014-SINGLEBYTE-EOF-GCOUNT-BRANCH-STATIC-01
- 日時/担当: 2026-10-21 23:39 JST / REA独立 / T014 P0。状態 STATIC/VERIFY/NOT READY。既存ID上書き無し。
- 参照起点: MASTER cp195、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、既存runs/20261011T153309850Z/RUN_RESULT.json、logs/progress_sync_20261011T153958076Z.json、10/21 21:35・22:36独立記録、10/12・10/21 01:33既存文字列reader監査を先読。
- 原EXE識別(索引manifest記録): SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回EXE現物再ハッシュ無し。
- 検索CLI/DB read-only実測: search.sqlite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、search.py SHA256 DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0、双方BUILD_MANIFEST一致、SQLite PRAGMA integrity_check=ok。
- CLI限定対象: function 0x42ECF0 / 0x42E700 / 0x42E7D4 / 0x42EC60 / 0x470700 / 0x42CC80 / 0x470980 / 0x470AAC / 0x4705F0。新Ghidra/REAなし。禁止・既拒否Wave6 T013 4 VA/0x429620/旧CALL_INDEX_V2照合/CEAエクスポートには再問い合わせ無し。
## 今回の差分A：Wave6安全候補0x470980の1-byte EOF区分と取得数
- 0x470980：Ghidra機械疑似C SHA256 850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446、248 bytes。保存索引ではcallers 0x4705F0 site 0x470611が1件、Ghidra内部のdirect cleanup sites 0x4709EF/0x470A2F/0x470A5F/0x470A76→0x470AACが4件。
- 初期化 param_1[2]=0、param_1[3]=0（gcount低/高候補）。sentry 0x42EC60へsite 0x4709D5で入り、sentry falseのときは1byte取得処理へ進まずcleanup。
- バッファ位置/残量が利用可能なら現在byteをunsigned 0..255に広げる経路がある。不足時はvtable+0x18を呼び、返ったuintが0xFFFFFFFFならcleanupへ進む。
- uint 0x000000FF（データbyte 0xFF）と0xFFFFFFFF（EOF int_type sentinel）は一致しない。従ってデータ0xFFをEOFとして扱わないのが索引疑似Cの候補動作。後段token readerのsigned-char拒否とは別層。
- 0xFFFFFFFF以外なら、バッファ消費可能時にはポインタ+1/残量-1/取得数+1、そうでなければvtable+0x1C呼出後に取得数+1の候補経路。vtable+0x18に対応するcomputed site 0x470A1B、+0x1Cにsite 0x470A66、tie側computed site 0x4709D0。vptr実体・副作用・戻値は未確定。
- 0xFFFFFFFFの経路ではGhidra疑似C上は取得数+1を通らない。正常な1byte取得成功時は低32bits加算、carry時高32bits+1。原作動的gcount値は未実測。
## 今回の差分B：callerとcleanupの二段判定
- 0x4705F0：コードSHA256 86E597D129AFE91C0A27CEF00A3E529B959C5BFCAA1A1B6221DFCDFF0F138889。site 0x470611→0x470980。返値候補iVar3!=-1の場合のみ DAT_00B060F8[i]へbyteを格納し、その後stream state&7を検査してLoadExceptionへ分岐する。0xFF拒否・255上限自体は既存REA資料にあるため再加算しない。
- 0x470AAC：code SHA256 EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D。疑似Cはunaff_ESI!=unaff_EBXならsite 0x470AC5→0x426E00、最後に親frame EBP-0x14を戻値とする。一方block側0x42E7D4（SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C）は親frame EBP-0x14非0でsite 0x42E7F2→0x426E00。両者を同じ「状態フラグslot」と断定しない。
- 0x42E700（code SHA E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76）→0x42ECF0（code SHA 509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21）site 0x42E77F、virtual+0x20 site 0x42ED07はbulk転送経路。1-byte 0x470980の仮想+0x18/+0x1Cと別APIであり、EOF/partial状態を単一実装へ雑に統合しない。
- Ghidraは0x470980をvoidと推定する一方0x4705F0はintとして消費、0x470AACは親frame returnを記述。0x42ECF0もvoid対親uint64の矛盾。いずれもASM未照合のため戻値ABI、EBP slotの実意味、state引数はVERIFY。
## 差分の限界・安全・次の再開
- 先行REA 0x4705F0の5種VERIFIEDは既存RUNの成果（asm ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d）。今回0x470980・0x470AAC等の新規正式info/pseudo/assembly/callers/calleesの5種セット0、Evidence ID新規0、VERIFIED新規0。索引本文/機械xrefsはREA正式証拠に転換しない。
- W1..W5旧正式保存sync 64/64、Wave6未登録0/16、候補TODO12（P0=2）/既拒否BLOCKED4（P0=3）/関数VERIFY0、今回正式差分0/0/0。QUEUE/PROGRESSの古いEPERM表示は変更しない。MASTER DONE9/34は旧確定値で全件再判定無し。
- Golden DESIGN/NOT RUN: stream state初期0と例外mask0を別設定し、byte 0x00/0x20/0x7F/0x80/0xFF/EOFでgcount低高、返値、stream flags、文字列への格納とLoadExceptionを独立観察。stream fail・tie・バッファ枯渇の条件も区別。実機原作PASS0、新旧strict MATCH0、再実装率未測定。
- 接続Local成功、最新decomp_task一覧にactive.lock無し。Local既存対話セッション2件は非介入。CPU/RAM負荷は今回未測定、調査全所要時間未計測、新Ghidra/REA実行時間0秒。新規安全拒否/接続障害0。
- 次は0x470980・0x470AACの戻値/状態レジスタ（EAX, ESI, EBX, EBP-0x14）の許可済み既存証拠を探し、block 0x42E7D4のcleanupとの違いを維持する。拒否済み命令照合を別ツール/経路で再実施しない。
- 変更はREA owner内の本独立新規文書のみ。原本・A〜E/MASTER/T018/dev_lab/Git・QUEUE/PROGRESS/runs/旧evidence・設定/スケジュール未変更。正式MASTER同期無し。保存後はreadbackとSHAで検証する。