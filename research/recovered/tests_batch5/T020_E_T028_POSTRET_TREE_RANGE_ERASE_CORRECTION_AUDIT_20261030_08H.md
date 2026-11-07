# 研究E｜T020 T028 post-RET木範囲消去・呼出位置の訂正（2026-10-30 08H JST）
研究ID: E-AUDIT-20261030-08H-T020-T028-POSTRET-RANGE-ERASE-CALLSITE-CORRECTION-01
状態: STATIC / INDEPENDENT PE E8 BYTE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY。正式READY新規統合0。
## 入力・由来
B所有: B-20261030-0808-T028-POSTRET-TREE-ERASE-CORRECTION-01。data/T028_POSTRET_TEMP_TREE_RANGE_ERASE_CALLSITE_CORRECTION_NATIVE_20261030_08H.md、LANE_B_HANDOFF、T028 ownerをread-only照合。
B詳細実SHA256: 72BAB2F1A6FD259B5F6ABDB23DD89178728FCC0DBE7B45AA133C1EF8EA657025。
原作研究PE実SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原本ゲームではなくrea_lab/targets解析コピーのみread-only。
統合V9の関数0x510850出力ではE8_DIRECT_CALLとして0x510867→0x44D0D0、0x5108DF→0x510C20を記録。ABIは未検証。
## 07H誤記訂正と08H独立成果
旧07H E文書の「0x5AC609 CALL0x510850」は誤り。B08H原生ASM訂正をEの新独立BYTEゲートで照合した。
研究PEの0x5AC609はE8でない。正しい直接E8 CALLは0x5AC611→0x510850。07H文書・検証器の過去成果を消去/改変せず、当該siteだけ本08Hを正本の後続訂正とする。
研究PEの他の4直接E8 CALL（0x510867→0x44D0D0、0x5108DF→0x510C20、0x44D0E6→0x4ED240、0x44D0EE→0x5B6BBB）も独立rel32算術とPE section mappingで一致。計5/5。
範囲境界を{first,last,leftmost,head}とした局所synthetic gateでは、first==leftmostかつlast==headならfull-range→0x44D0D0、そうでなくfirst==lastならempty-range、その他partial-range→0x510C20を選ぶ。
空木でfirst==last==leftmost==headの場合はfull-range優先のcall経路となる（実ノード解放数は0の可能性）。木count・iterator identity・head初期値・例外処理の実作用はVERIFY。
0x5AC61B head解放、0x5AC627別container cleanup、0x5AC631→0x5AC5B5後段を別操作とし、Spot+0xB8/0x598450の別木との同一性は未確定。二重free・解放成功・士気変化を既成事実にしない。
## 新規Eテスト／前回からの計数差
E新規 tests/t020_e_t028_postret_tree_range_erase_correction_gate_20261030_08H.py と tests/T020_E_T028_POSTRET_TREE_RANGE_ERASE_CASES_20261030_08H.json。
新規37（full9、empty8、partial10、reject10）すべてPASS、ネイティブE8 site 5/5一致、原作ゲームNOT RUN。
既存T028回帰11検証器は全exit0。従来の合成回帰公称299件に今回37件を足して336件。なお21Hのroute8件とは別にprovenance確認3条件があり、それも含むチェック総数は339。これらはすべて合成/静的・非Golden。
## MASTER / T018 / T019
PC MASTER最終正式checkpoint196、READY596（A115/B229/C136/D116）。TASK QUEUE34行を直接再計数= DONE9/IN_PROGRESS21/VERIFY4。B08研究はVERIFY/NOT READYで正式統合0。MASTER更新なし。
T018旧合法C-NB02: G0通常開戦UI、G1同run直前未改変SAVE+input、G2実MAP・三陣営・ordered Unit/Troop、G3結果、G4戦略再入World差分の同run一次receipt未完成。特にx20改変DATや別PIDのwatchは接合しない。DYNAMIC OBSERVED0/actual Golden PASS0/strict MATCH0。
T019確定矛盾新規0。GameClear DAT13/TXT2の検索範囲差のみRESOLVED、TXT runtime loader、script2先勝ち・phase flag、gwrite・decide11用途はVERIFY。
## 安全・再開
旧T018表境界、E session-join、T019 XREF、C T026/T032、D T030 TSV、禁止0x5710C0の安全拒否を迂回・再提出しない。旧OFFLINE-UNSYNCEDの意味的重複統合は未完了。
本回PC変更はE所有testsの新3成果物と読み戻し記録のみを予定。原本/MASTER/他owner/REA/dev_lab/Git/Work/設定/自動化を変更しない。
次はB ownerに0x5AC601/0x5AC605境界pointerの正確な入力と0x5AC5BD戻りconsumerの一次証拠を依頼する受入条件を保持。EはG0/G1/G2同一戦闘の一次receiptとGolden比較runnerを優先。
