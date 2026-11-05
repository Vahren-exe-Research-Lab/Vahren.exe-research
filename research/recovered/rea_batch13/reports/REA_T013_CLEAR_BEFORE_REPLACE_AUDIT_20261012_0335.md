# REA T013: 候補vector更新のclear-before-replace再解釈（2026-10-12 03:35 JST）
- 区分: STATIC-SAVED-EVIDENCE / 新規Ghidra取得0 / 新VERIFIED+0。参照した実行証拠は承認済み同一SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 規約: MASTER_LEDGER・ANALYSIS_LANES_PROTOCOL・README・QUEUE・PROGRESS・最新RUN_RESULT/syncをread-only確認。既存A〜E、MASTER、T018、MCP設定、Git、automation、原本には変更なし。
- PC確認: CPU約38.74%、空き物理RAM 16,787,052KB（約16.0GiB）、java/javaw/ghidra表示なし、active.lock=False、承認コピーSHA一致。重いREA/Ghidra起動なし。
## 発見 T013（保存済みassembly・pseudoの交差照合）
1. 0x57CFA0の0x57CFA0..0x57CFB5: ESIが保持するvectorのbegin=[ESI]とend=[ESI+4]を読み、非空ならECX=end、EDX=end、EAX=beginで0x5158A0を呼ぶ。0x5158A0は最初のCMP ECX,EDXが等しいので即RET、EAX=beginは不変。呼出元は戻ったEAXを[ESI+4]へ格納する。すなわちこの呼び方は一般range copyではなく、vectorの論理endをbeginに戻す「clear」動作。
2. 直後0x57CFC2..0x57CFC7で5値をPUSHし0x57CFD0を呼び、入力rangeを対象vectorに挿入。0x57CFA0は元配列への単純追記ではなく、空にしてから新規rangeで置換する更新経路を有する。ただし所有権/要素破棄/確保位置の完全意味はWave6補助関数が未解析なのでVERIFY。
3. 親0x57B870の0x57BA46..0x57BA58では0x514F10が返すbegin/endを0x57CFA0へ渡す経路を確認。別経路0x57BA6C..0x57BA97でも同一の0x5158A0（ECX=EDX=endなので即RET）→vector.end=begin→0x57CFD0を明示的に実行する。したがって少なくとも二つの更新枝で古い候補rangeを残すappendではなくclear-before-range-insertを確認。
4. ABI注意: 0x5158A0のGhidra pseudoはvoidだがEAXが戻り値として実使用される。0x57CFD0のpseudoは4引数相当に見えるが実assemblyは5 PUSH / RET 0x14、今回も疑似関数宣言の自動流用は禁止。候補の意味/戦闘AI選択順序は未確定。
## 根拠ID
- 0x57CFA0 assembly ev_65ab310aa388f22a6840b91176516ae019845155a3de0f0f739d125e7ad14789 / pseudo ev_af8c7dc6fe7871eb38bb0c219d8494ae7fa96d2e11c2b198fda926e5c813fb61。
- 0x5158A0 assembly ev_d4d1952d5b5e5da305467de47caec6d2ce02aadfbc2cd5475a12f7f41e291e80 / pseudo ev_256892f9bf4a31e4d302c31129c7094cad30e15db60647104f40fe356ba63239。
- 0x57B870 assembly ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c / pseudo ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc。
- 0x57CFD0 assembly ev_08eb96aea33c3dbd4a1ae58fa08f3b20bfb31b8ccea4539a5bc0044cbb4887b5 / info ev_f85bc7f40298b5ec205b3f4f8c0365f48b2fa30e5e8afc42691ec110f5c23efa。
## 未解決・次回
- Wave1〜5: 64/64 static VERIFIED（Wave5 16/16、P0 29/29、P1 35/35）、今回増分0。Wave6未正式登録・暫定0/16（候補P0 5/P1 11、未着手16・関数単位VERIFY0）。
- 最新sync logs/progress_sync_20261011T153958076Z.json は64/64で、QUEUE/PROGRESSは旧EPERMによる表示stale。既往失敗のrenameを再試行せず、ACL/force/他tool/pathの回避禁止。
- 次回優先: T013の0x515750 / 0x515790 / 0x5159B0 / 0x57D180について、正式キュー更新の安全な復旧後に最大4関数/回・Ghidra 900000ms・request 960000ms・単一MCPで5方法取得。現状は既存証拠のみ再照合。
- 研究DONE9/34（次回最新MASTERを優先）、旧EXE実機golden PASS0、ゲーム再実装率は測定していない。