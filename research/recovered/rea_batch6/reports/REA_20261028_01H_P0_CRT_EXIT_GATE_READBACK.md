# REA 2026-10-28 01H｜独立保存・読み戻し記録
ID: `REA-LOCAL-20261028-01H-P0-CRT-SEH-NATIVE-EXIT-GATE-STATIC-01`
読み戻し対象: 同時刻新規probe.py、audit.py、evidence.json、STATIC.md。REA所有 `rea_lab/decomp_task/` に計4ファイル新規保存し、Windows側の `Get-Item` と `Get-FileHash` で存在・サイズ・ハッシュを確認。
Audit SHA256: `A3FF221614DF3449AD7FC7E76592A456B60D6A788372F456FC25E5BF82DBE554`
Evidence SHA256: `053704977F963DF7AD7684889DCB519C02761804BBC93AA5703DBCBB063433F8`
Static report SHA256: `13E4BC394A5587B63551A87E0E320EBD719ECF082A8C2167E31A8A419E26469B`
別PowerShellプロセスで `python REA_20261028_01H_P0_CRT_EXIT_GATE_AUDIT.py` を独立再実行：**27/27 PASS、failure=[]、約1.194秒**。元の保存時実行約1.945秒。PE COM descriptor RVA=0/Size=0。3直接CALL siteの旧索引/V9登録件数はいずれも0。
先行Sync 64/64 VERIFIED、前回00H 25/25に一致。REA新規VERIFIED=0、Golden=0、既存QUEUE/PROGRESS/MASTER更新なし。
稼働：PC接続成功、active.lock無し、Java/Ghidraプロセス検出なし、空き物理RAM約11255MiB（取得時点）、CPU使用率不明、全研究時間未測定。新規REA/Ghidra/原作実行0。Work無し。
障害：調査段階の複雑なPythonワンライナーにSyntaxError（OTHER）；独立スクリプト化で復旧。PowerShell出力の日本語パスがコンソール表示だけ文字化けしたが、ハッシュ・解析の結果は正常。安全拒否ではなく、別ツール迂回もなし。
保存・未同期：REA所有ファイル5件（この記録を含む）。既存他レーン正本やGitへ未同期、Formal READY/VERIFIEDには昇格しない。今回の新規成果はSTATIC・VERIFY・NOT READY。次の許可済み再開位置は `0x005BB4CF` のdoexit分岐で、原作ゲームGoldenはNOT RUN。
