# REA-LOCAL-20261023-1435-P0-BTL-AUTO-GATE-STATIC-01
- 分類: REA独立 / P0 / STATIC・VERIFY・NOT READY。主な意味領域=T010（戦闘時計）、T015（戦闘入力/UI）への参考情報。T014はSAVEであり、本研究をT014正式進捗へ誤計上しない。
- 差分: 2026-10-23 13時台の0x5656A0時間更新・btl_auto比較は既知。本回新規は0x526140の実ASM条件、ESI出所、状態+0x20変更、原作CP932文字列の照合、2つの上位CALL siteおよび特殊値除外の接続。
- ソース: research/rea_lab/targets/hakushin067_Vahren.exe SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（対象専用コピーをread-onlyで直接計算）。
- CURRENT検索: HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite SHA256=0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25。verify_active_research_state_v3_20261022.py 実測PASS_ACTIVE_V3_STATIC / guarded files14 / errors0。
- 旧search.sqliteは現行正本ではない。旧SHA=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。削除・更新しない。
- 本体原作EXEを実行せず、専用コピーのPE32 VA->RVAをpefileで参照し、Capstone5.0.7で当該関数を独立逆アセンブル。Ghidra pseudocだけによる意味の断定を避けた。

## 核心: 自動操作切替の静的ゲート
- 0x005656A0: 0x5656A0 CMP DWORD PTR [0x67B938],0x80000008、0x5656AB JNE 0x5656B5。特殊値なら0x5656AD INC DWORD PTR [0x67B93C]→RET、この呼出で後述btl_auto一致判定を通らない。
- 通常値: 0x5656BE DEC [0x67B93C]（正なら）、0x5656C6 CALL 0x564CD0、0x5656E0 CALL 0x46F4C0（literal 0x629078='btl_auto'、default PUSH 0x64=100）、0x5656E5 CMP [0x67B93C],EAX、0x5656EB JNE 0x5656F8。
- 一致時: 0x5656ED MOV ESI,[0x0067B86C] (bytes 8b356cb86700)、0x5656F3 CALL 0x00526140 (bytes e8480afcff)。重要: 0x00526140のESIは上位関数で保持されたESIではなく、このcall直前のglobal読出しに由来する。
- CURRENT V3 E8 verified caller of 0x526140: 0x5656F3のみ。0x5656A0のE8 verified callers: 0x492FA9 (0x492D80) / 0x49B346 (0x49B280)。前者・後者ともフレームカウンタ+0x1EED64の%10 == 0相当ゲートをGhidra擬似Cで確認。後者はPE E8実バイトとも一致。
- 0x526140 entryは直接ESI参照: 0x526167 CMP BYTE PTR [ESI+0x18],0、0x526170 MOV EAX,[ESI+0x14]、0x526175 JE 0x52626C。最初の2条件を満たさなければ作用なし。
- その後、[ESI+0x14]+0x1D==0なら[ESI+0x194]を使い、関連obj+0x54==0 / +0x50!=0 / 別参照+0x38!=0 / +0x1EED54!=0 / obj+0x50の指先+0x79!=0という追加ゲート。途中失敗は0x52626Cのエピローグへ。
- 条件成立時: 0x5261CD MOV DWORD PTR [ESI+0x20],5 (bytes c7462005000000)。その後、0x5261D4 context取得、0x52622F CALL 0x4369B0、0x526267 CALL 0x52CCF0。呼出先のABIはVERIFIEDではなく、5という値のUI上の完全な意味も未実測。

## 原本の文字列・フォーマッタ
- CP932 .rdata 0x0062B230（実バイト読取）: 「残り時間が%%%を切りましたので強制自動操作モードになります\nユニットの移動指定は出来ません\nスキル選択と退却は出来ます」。表示文面はゲーム内の意思決定を示唆するが、実際の入力停止・AIの行動選択は未測定。
- 0x5261BF MOV EAX,[ESI+0x190]、0x5261C5 PUSH 100、0x5261C8 MOV ECX,0x62B220 ('btl_auto')、0x5261D4 CALL 0x46F4C0。0x5261F2 MOV EDI,EAX。
- 0x52621F PUSH 0xC8、0x526224 PUSH EDI、0x526225 PUSH 0x62B230、0x52622F CALL 0x4369B0。0x4369B0→0x436BC0で '%%%' の数値文字列置換をGhidra疑似C上確認（ABIはVERIFY）。
- 注意: 判定関数0x5656A0のbtl_auto参照元は[DAT_0067B868+4]+0x1B8、通知構築側0x526140の参照元は[ESI+0x190]。これらが実行時に同じ設定オブジェクトであるか未確定で、表示値と閾値の同一性はVERIFY。
- VA 0x0067B86CについてV3 ghidra_refsで直接参照は0x5656ED READのみ、writeの直接参照は0。原作.data初期値は0。レジスタ別名書込やゲーム初期化時の所有者を未追跡であり「writerなし」とは断定しない。

## 証拠分類・残課題
- Native E8索引: 0x5656F3→0x526140 / 0x492FA9→0x5656A0 / 0x49B346→0x5656A0。機械語は0x5656A0と0x526140全関数をCapstoneで直接照合、raw stringはpefile bytes+CP932 decodeで取得。
- 検索済み疑似Cは未補正であり、0x526140 / 0x5656A0 / 0x49B280 / 0x492D80 / 0x4369B0 / 0x436BC0のABIを原作C型として扱わない。REA正式のinfo/pseudo/assembly/callers/callees新5種証拠セット0・新EVIDENCE-ID0・新VERIFIED 0。
- 既存REA証拠: 2026-10-11 logs/progress_sync_20261011T153958076Z.jsonでWave1-5 64/64。ただしQUEUE.json/PROGRESS.mdはEPERMによるstaleを維持。新調査で64件を加算・再認定しない。
- 正式TODO/VERIFY/BLOCKED編集差分=0/0/0。今回の別メモ上のVERIFYは(1)0x67B86Cの所有者/間接writer、(2)ESI+0x20=5の消費側、(3)btl_auto二経路の設定一致、(4)通知文・AI切替の実行観測。
- 実ゲームGolden PASS=0、strict MATCH=0、完全複製率=未測定。新規REA/Ghidra run=0。調査総実行時間=未計測。PC瞬時CPU LoadPercentage=0、空きRAM18.24GiB（単一サンプル、持続負荷ではない）。
- 最新MASTER・ANALYSIS_LANES_PROTOCOL・REA README/QUEUE/PROGRESS・保存済み最後RUN_RESULT・最新progress_syncを先読。active.lockなしを確認。原本、MASTER、他レーン、QUEUE/PROGRESS、既存runs、Git、スケジュールは変更なし。
- 前回2026-10-23 13時台に安全拒否された検証用Pythonの新規作成は未解決、今回は同Python・拒否Wave6・REAエクスポートを再実行せず、独立なMarkdown静的メモのみ新規作成。
- 次P0: 0x0067B86Cへの別名writerと生成関数、ESI+0x20==5を分岐条件に使うconsumer、0x526140の2種類のbtl_auto取得元の同一性、0x49B280側での時間更新の条件分岐をV3静的証拠で深掘り。T010/T015正式正本への統合は各owner判断まで未実施。
- 状態: REA-LOCAL-20261023-1435-P0-BTL-AUTO-GATE-STATIC-01 = PC-SAVED-PENDING-READBACK / STATIC / VERIFY / NOT READY。

## 保存後の独立検証確定（同回）
- 独立read_fileで全34行の内容を読み戻し、read-only Pythonで追認：追記前ファイル6303byte / SHA256 D252028BA9DC419A165602BD437126229DECA12BE46459318ECADBC56A8B3FC0 / ID一致。原作PE命令8/8一致、V3 SQLite E8 CALL site 3/3一致、CP932通知文字列照合2/2一致、DB quick_check=ok。
- 最終状態: PC-SAVED / READBACK VERIFIED / STATIC / VERIFY / NOT READY。追記前SHAは受領時点の版に対応するもので、最終ファイルSHAは別途再計算する。
