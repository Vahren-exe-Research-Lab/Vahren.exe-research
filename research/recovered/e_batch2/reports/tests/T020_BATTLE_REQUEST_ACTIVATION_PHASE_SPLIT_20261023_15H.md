# E T018/T020｜戦闘要求と初期化・ScriptBattle実行・active化の混同防止（2026-10-23 15時台）
ID: E-AUDIT-20261023-15H-T018-T020-REQUEST-ACTIVATION-SPLIT-01
分類: STATIC CROSSWALK / VERIFY / DESIGNED_NOT_RUN / NOT READY。原作Gameplay新規実行0。
SOURCE: 現行V3 search_current.py read-only function/callers/flow-callers(0x004922A0,0x00492890,0x004338D0,0x0048D6A0)、BATTLE_STAGE17_ACTIVATION_BOUNDARY_20261022.json、E既存T020 Stage17/14時台クロスウォーク。
EXE識別SHA: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（索引のsource値、今回EXE実バイト再ハッシュ無し）。
V3 guard: PASS_ACTIVE_V3_STATIC / 14 input hashes / E8 CALL 44889 / E9,EB JMP 6324 / errors 0 / Gameplay NOT_RUN。
## 実PE直接CALLと局所書込みの段階差（同一run実通過は未証明）
要求/準備候補: 0x00491870内0x004921CD、0x00521D90内0x00522297/0x005222AAの計3 E8 → 0x004922A0。関数は+0x1EED43へparam_2格納、+0x1EEDBCを0へresetし、@battlefield/@battledefense/@battleattack公開処理候補を含む。
別の初期化連鎖: 0x004B9930内0x004B99CD E8 → 0x0048D6A0。さらに同関数内0x0048E9F0 E8 → 0x004338D0（VM処理候補）。
条件付active経路: 0x004338D0内0x00433E58 E8 → 0x00492890（ScriptBattle RTTI分岐内）。0x00492890は+0x1EEC3Cに2、+0x1EEC44に1を格納する静的コードがあり、後方に0x00492A4E/5B/68のcallback候補。
V3の0x00492890へのE8 callerは0x00433E58の1箇所、0x004922A0へのE8 callerは上記3箇所。互いの関数内部から相互を直接E8 CALLする記録は無い。
注意: これは2系統が排他的である証明ではない。非直接経由の接続、実行順序、ScriptBattle実体とUI起源、callback成否は全てVERIFY。
## E Golden受入差分
G0: 合法旧UIからの操作receiptとmode遷移receiptを別stageで保持。0x004922A0到達だけでmode2/active1・三陣営配置完了とは判定しない。
G1: 直前SAVE実byte/SHA、入力時刻、同一PID・起動世代・戦闘時間窓を必須。PID一致のみでも別戦闘は分離。
G2: +0x1EEC44=1だけでcallback完了・MAP・実三side・ordered Unit/Troopを確定しない。実視認または同runの合法な原作一次証拠が必要。
T020負例: RA-01=request CALLだけでG0/G2完備; RA-02=ScriptBattle RTTIだけで旧通常UI起源を否定; RA-03=active書込だけでpost-callback完了; RA-04=初期化呼出の静的連鎖を実到達と誤認。期待値はREVIEW/VERIFY、実原作PASSは不可。
既存E Stage17のactive-before-callback、Stage13のG1不充足、14時台の跨PID禁止と重複計上しない。今回は「0x4922A0の要求候補」と「0x492890のactive化候補」をV3の別callee/callerとして対照した差分のみ。
T019: GameClear DAT13/TXT2字句scope差はRESOLVED据置。script2勝者/phase flag/TXT loader/gwrite後続はVERIFY。新規確定矛盾0。
状態: E DYNAMIC OBSERVED 0 / actual Golden PASS 0 / strict MATCH 0 / 新規正式READY 0。旧checkpoint196/READY596(A115,B229,C136,D116)、34Task 9/21/4は旧値・再集計無し。
前回OFFLINE-UNSYNCED暫定26研究は未照合、原本EXE/DAT/SAVE/ZIP/他owner/REA/dev_lab/Git/Work/設定/automation変更無し。
旧安全拒否T018表境界、12:47 T020 V3配列ノート、12:49 MASTER復旧、C T026/T032、D T030、0x5710C0等を再試行・別tool/path/shell/Remote/ZIP迂回しない。
次: 同一native runで要求・初期化・active後callback・G2実MAP/出撃名簿を時刻付receiptで分離して捕捉。EがMASTER正式採録するのはowner/READY/SHA/ID重複/競合を満たす場合だけ。