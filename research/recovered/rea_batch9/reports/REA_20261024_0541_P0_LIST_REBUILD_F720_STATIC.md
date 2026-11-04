# REA-LOCAL-20261024-0541-P0-RESET-REBUILD-F720-STATIC-01
日時: 2026-10-24 05時台 JST / owner=REA / P0 / PC-SAVED / STATIC / VERIFY / NOT READY

## 事前確認・非重複
- PC Desktop Commander Local Compact正常接続。MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、先行02-04H研究、search_index README/BUILD_MANIFESTをread-only先読。
- Wave1-5 の64/64 VERIFIEDは既存logs/progress_sync_20261011T153958076Z.jsonの保存値。QUEUE/PROGRESSはEPERM staleのまま。正式REA新規VERIFIED=0、旧64件を再計上しない。
- 読取専用対象コピーSHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- search.sqlite SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（BUILD_MANIFESTと一致）。
- 最新04Hでは0x49AF10によるlist初期化と0x48F720のNULL戻り値のみ確定。今回は「別の0x48F9E0 resetから候補再構築まで」の経路を独立解析。

## P0新発見①：0x48F9E0がリストを空にした直後に再構築処理を呼ぶ
- 0x48FBA4: LEA ESI,[EBP+0x1EED20]、0x48FBB2: EAX=[ESI+4]。
- 0x48FBB9/BC/C4: headerの+4/0/+8にheader自身を設定。0x48FBC7: [ESI+8]=EBX（先行パスのEBX=0はGhidraと実ASMの全レジスタ経路要継続精査）。
- 0x48FBD1: CALL 0x498E60 → 0x48FBD7: MOV EAX,ESI → 0x48FBD9: CALL 0x48F720。
- よって0x48FBD9呼出の直前には再構築関数が存在する。reset直後の一瞬の空状態だけで0x48F720が必ずNULLを返すとは結論できない。

## P0新発見②：0x498E60→0x498F90→0x476830 の挿入・件数更新を実バイトで接続
- 0x498E65は入力range端の一致を比較、空rangeなら0x498ED5へ直接分岐。非空ならノード巡回。
- 0x498E70: EDX=[ESI+4]、0x498E7B: EDX=ESI、0x498E7D: CALL 0x498F90。
- 0x498F97: EDI=EDX、0x498F99: [EDI+8]件数テスト。空コンテナへの初回挿入候補で0x498FA8 node生成、0x498FB4 CALL 0x476830。
- 既存要素がある場合にも0x498F90の各比較分岐から0x4991A0を呼び、0x4991B5で0x476830へ到達可能（重複時は挿入無し）。
- 0x47685C: EDI=ECX、0x47685E: ECX=[EDI+8]、0x4768AE INC ECX、0x4768AF MOV [EDI+8],ECX。つまり挿入成功経路の件数更新はnativeで立証。
- 元0x48F9E0のESIは対象コンテナ0x1EED20、ヘッダ+4・件数+8に一致する。Ghidra単体では欠けやすいESI/EDX/ECX引数受渡しを実ASMで補強。

## P0新発見③：候補選択後のNULL契約は別の初期化経路にも存在
- 0x48FBD9 CALL 0x48F720の戻り値を0x48FBDEでESIに保持。
- 0x48FBE0で別の入力をEAXへ置き換え、0x48FBEA CALL 0x597B00の結果を+0x1EED4Cへ保存。
- 0x48FBF5でEAX=ESIを復帰し、0x48FBF7 CALL 0x583C70へ渡し、結果を+0x1EED50へ保存。
- 0x583C76に[EAX+0x94]相当の参照がある既存03H知見と接続。0x48F9E0でもF720戻り値に明示NULL検査が見当たらない局所経路を確認。ただし実際のNULL発生・クラッシュは未証明。
- 入力rangeが非空で、0x498E60により少なくとも1件の有効候補が保持されることが必要な可能性。要素重複・採択条件や後続lookupが0にならない不変条件は未解決。

## P0新発見④：戦闘分岐タイマーおよび代替経路を区別
- 0x4918B4: EAX=[EBP+0x1EED5C]、0x4918BC: <=0なら0x492270退出、正値はDECして保存後0より大なら退出。今回対象の0x40D0A0呼出候補はtimerが1→0になった反復に限定される局所制御。
- 0x4923EB/0x4923F1では+0x1EED43が0ならFadeOutSheet経路、非0なら0x4922A0内部で0x492473 CALL 0x40D0A0に到達。+0x1EED43が非0だけでは別の分岐条件や前提を全保証しない。
- 04Hの5 CALL先と入力生成は既知成果につき「新しい5箇所」と再計上しない。

## 静的証拠・負荷・保存境界
- 再現Python: REA_20261024_05H_P0_LIST_RESET_PROBE.py（read-only解析、対象EXEは実行しない）。
- 元SHA PASS、検索DB SHA PASS、選定命令25/25、直接E8 CALL先13/13 PASS。これは関数全体の証拠網羅率ではない。
- 使用情報: search.py function 0x48F9E0/0x498E60/0x498F90/0x4991C0/0x4991A0/0x476830/0x491870/0x4922A0、callers/callees、原作EXEのCapstone ASM。
- 5種情報(info/pseudo/assembly/callers/callees)のうち新規REA正式一式充足0関数。今回のASMは特定区間のみ、新規VERIFIED0、正式TODO/VERIFY/BLOCKED差分0/0/0。
- Golden原作ゲーム実測0、strict MATCH0、完全複製率未測定。新REA/Ghidra実行0。試験は静的のみ。
- 事前環境: active.lockなし、Java/Ghidra0、空きRAM13.13GiB、CPUサンプル0%。調査全体の正確な実行時間は不明。
- 旧RUN/QUEUE/PROGRESS/MASTER/A-E/T018/Git、元ZIP/EXE/SAVE、検索DB、スケジュールは変更しない。安全拒否なし。

## 再開優先
- 0x48FBCA周辺の入力rangeの所有元と件数、0x498E60の全duplicate/insert条件を検証し、0x48F720結果がNULLにならない保証を調べる。
- 0x40F320側の0x48F720入力listと0x48F9E0のrebuild済みlistが同じ実体・時間順序で使われるかを追跡。静的経路だけで実行時不変条件を確定しない。
- 同じ先行IDとの重複照合後に、REA所有領域へ一度だけ正式同期可能。EのMASTER統合は別担当、READY昇格不可。
