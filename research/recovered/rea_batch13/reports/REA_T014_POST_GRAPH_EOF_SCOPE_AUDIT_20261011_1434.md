# 迫真戦記 ver0.67 / REA T014 通常save readerの末尾EOF確認範囲（2026-10-11 14時台 JST）
状態: CONFIRMED-SAVED-NATIVE（0x45E1E0局所return経路）/ VERIFY（calleeと上位callerの検証）。実ゲームNOT RUN。
承認済みコピーSHA256（保存RUN_RESULT記録）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回のhash再計算なし。
対象 VA 0x45E1E0 / T014 / 保存run runs/20261009T225741694Z/RUN_RESULT.json。Ghidra関数長1028 bytes、非連続4 ranges。
info ev_5da50720924339f770fe37dd127f90a1d8faff1b1c9c80922819ec9f7c999ef0
pseudo ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e
assembly ev_69ab9492fa443fe12c5fb3e0d6230b5c7bb67fcca9fbc5c2915973a18d18e124
callers ev_25b1ebae191adb744c52e90f5c7faa796423ecd9edc00b29aa5a5b241415b65e
callees ev_1c6253652438f3553d6e578d8b3afdc47b832a780c4732bf2d4117a9ca1a3f42
## 追加の独立静的照合
- 保存済みGhidra pseudoと既存 native exe/T014_NORMAL_LOAD_PROBE.txtのVA 0x45E536..0x45E5EFを突合。
- 0x45E53Eで外交reader 0x471AF0、0x45E54Cでworld-map/Spot-Path graph reader 0x435550を呼ぶ。両方とも戻り値に対する局所成否分岐は見えない。
- 0x45E551..0x45E5CCではbuffer capacity（0x10）・一時オブジェクトの後始末に移行し、0x45E5D3..0x45E5EFは例外フレーム/stack-cookie後処理とreturn。最後の0x435550呼出後、0x45E1E0の通常終了経路に明示的な末尾EOF一致確認や残りファイル長判定は見えない。
- 既存writer 0x460000はCreateFileA OPEN_ALWAYS(4)を使用する（別保存run 20261009T212627835Z / assembly ev_fec99c35153c8902d10879722c3a8fcb90bcdd434f62a9dedd7878e352529394）。同一パス長→短上書きで末尾残存があり得る、という以前の条件付き論点に対し、reader core内の直接EOF検査は見当たらないと範囲を限定して補足。
- ただし0x435550がファイル終端・余剰データを自ら検査するか、0x45E1E0の上位callerが保存後のstream位置を確認するかは未確認。『末尾ごみを必ず許容』『旧セーブの確定バグ』と断定しない。
## 次回優先
0x435550内の余剰byte処理 / 0x45E1E0上位callerのstream state判定 / 合法な短いセーブ再保存での実機golden（未実行）を独立課題として区分。原本EXE実行はしない。
## 数値と禁止操作
今回の新規REA/Ghidra=0、VERIFIED増加0。Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12、計39/48。P0 20/21, P1 19/27, TODO8, VERIFY1。MASTER確認checkpoint83・研究DONE9/34。旧EXE golden PASS0。ゲーム再実装率は測定していない。
既往安全拒否run_decompile.ps1・extract_verified・0x5710C0..0x571500の再試行/迂回0。原本、A-E、MASTER、T018、QUEUE、PROGRESS、Git/MCP/automation変更なし。