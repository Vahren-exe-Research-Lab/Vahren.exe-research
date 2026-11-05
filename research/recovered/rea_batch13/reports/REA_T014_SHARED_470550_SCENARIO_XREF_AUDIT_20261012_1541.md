# REA T014 — 共通0x470550の追加scenario xref（2026-10-12 15時台 JST）
- 区分: SAVED NATIVE READ-ONLY CROSSCHECK。REA/Ghidra新規0、5-method新証拠0、VERIFIED増加0、ゲームEXE実行なし。
- 参照専用: exe/T014_LOAD_CORE_DUMP.txt、exe/T014_NORMAL_LOAD_PROBE.txt、exe/T014_NORMAL_SAVE_CORE.txt、exe/T010_PHASE_XREFS.txt、exe/T033_SCENARIO_LITERAL_XREFS.txt。
- 前回メモでは0x470550のcallsiteは3件。今回、別の既存native資料で第4の異なるcallsiteを確認。
## 保存済みnative資料に確認できる直接CALL
| CALL VA | 既存資料 | 直後の処理 |
|---|---|---|
| 0x45E2D8 | T014_LOAD_CORE_DUMP.txt:62 | ADD ESP,0xC / temporary整理 |
| 0x45ECBB | T014_NORMAL_LOAD_PROBE.txt:619 | ADD ESP,0xC / 一時文字列解放判定 |
| 0x4CFC2A | T014_NORMAL_SAVE_CORE.txt:1296 | ADD ESP,0xC → 0x4CFC54でscenario literalをpush、0x4CFC66で0x4647D0をcall |
| **0x539364** | **T033_SCENARIO_LITERAL_XREFS.txt:2355**（T010_PHASE_XREFS.txt:815にも同site） | ADD ESP,0xC → 0x539385でscenario literalをpush、0x539397で0x4647D0をcall |
- 第4地点の実命令：0x53935A LEA ECX,[EBP-0x29C] → 0x539364 CALL 0x470550 → 0x539369 ADD ESP,0xC → 0x539385 PUSH 0x62A72C ('scenario') → 0x539392 MOV EDX,0x62A724 → 0x539397 CALL 0x4647D0。
- 0x4CFC2A地点も3個のstack pointerを準備し、共通helperからscenario property lookupへ進む。関数名を「T014専用save reader」と確定するのは不適切。
## 不明点と証拠限界
- 4件は検索対象の保存済みexe資料にあるcallsite集合であり、0x470550の直接xrefs総数ではない。callee本体、ABI、戻り値、副作用、0x539364の高水準処理所属はVERIFY。
- 0x4705F0 callers ID ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87 は別関数の証拠。0x470550に対する5-method VERIFIEDへ転用しない。
- 0x58E480の本体契約とUnit marker 0x68B9D0のraw bytesは引き続きVERIFY（取得証拠IDなし）。
## 現状・次回
- 保存済みsync progress_sync_20261011T153958076Z.jsonでWave1〜5合計64/64 VERIFIED。P0 29/29・P1 35/35、今回+0。Wave6は暫定0/16（P0 5・P1 11、未着手16・関数単位VERIFY0）、正式キュー未登録。
- QUEUE.json/PROGRESS.mdはSTALE_RENAME_DENIED。既往EPERMの反復・別shell/tool/path迂回をせず、新規runner/syncは起動しない。
- MASTERの最新既知値DONE9/34、IN_PROGRESS21/VERIFY4。旧EXE実機golden PASS0。ゲーム再実装率は測定していない。
- preflight CPU0%、空きRAM15.42GiB、Java/Ghidra/REA0、active.lock無、承認済みcopy SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187実測一致。重い解析実行0秒、軽量照合総時間未計測。
- 次回は0x58E480/0x470550の*既存*証拠・callsiteを優先。Wave6正式登録後のみ対象を追加し、同一関数の重複取得は禁止。
- 制限REA6.1.0/Ghidra12.1.4、単一MCP、4関数上限、Ghidra900000ms/request960000ms。禁止範囲0x5710C0..0x571500および既往拒否抽出は未実行。
- 原本ZIP/EXE、A〜E、MASTER、T018、その他研究、Git/push/MCP/自動化設定は無変更。
