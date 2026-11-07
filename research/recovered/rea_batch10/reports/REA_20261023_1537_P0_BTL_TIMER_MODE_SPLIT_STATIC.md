# REA-LOCAL-20261023-1537-P0-BTL-TIMER-MODE-SPLIT-STATIC-01
- 日時: 2026-10-23 15時台 JST。状態: PC-SAVED-PENDING-READBACK / STATIC / VERIFY / NOT READY。owner: REA。関連参照: T010（戦闘時計）/T015（入力・戦闘画面）、他lane未統合。T014(SAVE)への正式加算なし。
- source PE32専用コピー: rea_lab/targets/hakushin067_Vahren.exe SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（実測）。
- ACTIVE V3 SQLite: HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite SHA256=0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25（実測）。verify_active_research_state_v3_20261022.py=PASS_ACTIVE_V3_STATIC、14 hash verified、errors=[]。旧search.sqliteは非正本。
- 既存重複照合: 前回2026-10-23 14:35のREA_20261023_1435_P0_BTL_AUTO_TRANSITION_GATE_STATIC.mdを先読。0x5656A0→0x526140の特殊値/自動操作閾値経路は既知。本回の差分は0x492D80のモード引数による「タイマー更新関数の選択」と0x49B280への条件付き委譲、ABI入口の静的証明。
## P0新規差分: 戦闘時間更新の2モード分岐
- 0x00492D87: CMP BYTE PTR [EBP+8],0 (bytes 807d0800)、0x00492D90: JE 0x00492EB8 (0f8422010000)。0x00492D8Eで EBX←EAX（外側オブジェクト参照）。引数0なら下記通常側、非0なら別側。
- 非0・+0x1EEDBC==0: 0x00492D9F～0x00492DBEで+0x1EED64と+0x1EED60を増分、IDIV 10の余り0で0x00492DC6から時計値を直接更新。特殊値0x80000008なら+0x0067B93Cを加算、通常値で残量>0なら減算。0x005656A0は呼ばれず、この経路からbtl_auto閾値判定は発生しない。
- 非0・+0x1EEDBC!=0: 0x00492E4C～0x00492E8Fの付加条件/フレーム更新後、IDIV 10の余り0で0x00492E95 CALL 0x00565700（E8 e866280d00）。0x00565700は時計カウンタのみ更新しbtl_auto照会しない。0x00492E9B CALL 0x004930C0。時間tickと自動操作は同一処理ではない。
- 0・Engine+0x1EED18!=0: 0x00492EB8 CMP [EBX+0x1EED18],0→0x00492EC3 CALL 0x0049B280 (E8 e8b8830000)。呼出直前0x00492EC1で EDI←EBX。0x0049B280内部は0x0049B2B1等のグローバル/状態ゲート成立後、+0x1EEDC4と+0x1EEDC8が等しいとき+0x1EED64を増分し、IDIV 10で余り0なら0x0049B346 CALL 0x005656A0。
- 0・Engine+0x1EED18==0: 0x00492FA9 CALL 0x005656A0 (E8 e8f2260d00)。前段0x00492F85で+0x1EED64を増分し、IDIV 10の余り0で実行。さらに0x00492FDFの余り分岐で20の倍数なら0x00492FE1 CALL 0x0049D5B0（意味未確定）。
- 0x005656A0は前回確定のとおり通常時計値の場合btl_auto閾値比較を経て0x005656F3 CALL 0x00526140へ進む可能性あり。非0側の時計更新のみの経路と区別する。動的切替挙動・表示は未実測。
## ABI・独立証拠
- 0x00492D80の入口はEAXをEBXに退避し、[EBP+8]下位1 byteのフラグを検査。正常return例0x00492EB5 RET 4 (c20400)。よってEAX暗黙入力とstack 4-byte callee cleanupが少なくとも当該経路で必要。C関数prototypeは未確定。
- 既存V3 search_current.py function/callers を参照後、専用コピーをpefile+Capstone x86で独立逆アセンブル。raw E8+rel32を別計算して7/7 PASS: 0x492E95→0x565700、0x492FA9→0x5656A0、0x49B346→0x5656A0、0x492EC3→0x49B280、0x5656F3→0x526140、0x49B400/0x49B491→0x49B5C0。V3 caller索引一致。
- 検証用の一時的なread-only Python式は一度byte比較式の誤記で0/7となったが同回で修正・再実行し7/7 PASS。対象機械語が変わった証拠ではない。新規Pythonファイルは作成していない。
- function info/pseudo/callers/callees検索はV3から取得したもの。asmは部分独立確認。ただし正式REA info/pseudo/assembly/callers/callees 5点セットとして保存した対象関数は0件、新規VERIFIED=0。
- 過去64/64はlogs/progress_sync_20261011T153958076Z.json（Wave1～5）にある保存済みREA成果であり加算なし。QUEUE/PROGRESSはEPERMによるSTALE_RENAME_DENIED維持、正式TODO/VERIFY/BLOCKED編集=0/0/0。Golden実測PASS=0、strict MATCH=0、完全複製率未測定。
- 研究PC時点: active.lockなし、CPU負荷12%（瞬間値）、空きRAM約17.96GiB（瞬間値）。Ghidra/REA新規実行0、Workなし。調査全体時間は未計測。原本・MASTER・他lane・Git・QUEUE/PROGRESS・既存runs・スケジュールは変更なし。
- 次P0: 0x00492D80の0/非0モードを設定するcallerの引数逆追跡、0x0049B280における0x0049B5C0到達時の0/1結果引数、0x0067B86C writerと状態+0x20=5 consumerの別名参照を探す。実ゲームGoldenで0/非0モードの時間進行・btl_auto発火差を比較（今回はNOT RUN）。
## 保存・readback確定
- 2026-10-23 15時台: 別read_fileで上記20行を全行再取得してID/VA/差分/検証結果を確認。最終状態: PC-SAVED / READBACK VERIFIED / STATIC / VERIFY / NOT READY。PC正本に一度のみ新規保存し、既存ファイル・他owner領域は変更していない。
## 同回追加発見：2つのcallerがモードを固定値で選択
- 現行V3の0x00492D80 direct callersは2件のみ: 0x0040E3B0 (属0x0040E2F0) / 0x00433607 (属0x004335E0)。PE raw E8相対変位と一致。
- 0x0040E3AE PUSH 1 → 0x0040E3B0 CALL 0x00492D80 (bytes 6a01 / e8cb490800)。呼出元0x0040E2F0は反復ループ内で呼び、AL!=0なら0x0040E622側へ、別途local_1c上限500の分岐あり。非0時計更新側を使う候補。これがCPU対CPUの簡略戦闘そのものかはVERIFY。
- 0x004335E0は+0x1EEC3Cの状態=2を選び、0x004335FAで+0x1EEC44!=0のとき0x00433601 PUSH 0 → 0x00433605 MOV EAX,ESI → 0x00433607 CALL 0x00492D80 (bytes e874f70500)。0モードは状態フラグ付きの上位処理から選択される。呼出後+0x1EEC44を再確認して条件付きで0x004338D0へ移る。
- この同じ0x004335E0で状態=6は0x004335F5 E9 JMP 0x00433E80（bytes e986080000）。V3では直接CALLではなくJMPと分類すべき。Capstone + independent raw rel32 3/3 PASS、V3 callers（2件）と照合。ABIの実機状態・入力意味は未VERIFIED。
- 検証範囲を同回更新: raw E8/JMP 相対ターゲット合計10/10 PASS（先の7件+上記3件）。REA正式5種新証拠0、新VERIFIED 0、実機Golden0、正式台帳編集0。
- 次回P0更新: 0x0040E2F0が何のゲームモードから呼ばれるかをcallerで遡り、0x004335E0の状態2/6と原作Battle end情報の関係を区別する。記録は独立静的成果、PC本体ゲームはNOT RUN。