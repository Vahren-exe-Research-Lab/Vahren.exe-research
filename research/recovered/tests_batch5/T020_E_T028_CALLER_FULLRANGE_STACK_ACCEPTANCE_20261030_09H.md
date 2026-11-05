# 研究E｜T020/T028 post-RET caller-specific full-range消去受入（2026-10-30 09H JST）
研究ID: E-AUDIT-20261030-09H-T020-T028-CALLER-FULLRANGE-STACK-01
状態: STATIC / SOURCE+PE BYTE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作ゲームNOT RUN。正式READY 0。
## 入力・照合
B owner研究: B-20261030-0916-T028-POSTRET-FULLERASE-PROVEN-01、data/T028_POSTRET_FULLRANGE_CALLER_ARGUMENT_PROOF_NATIVE_20261030_09H.md。
B詳細実SHA256: 4C892AA112D27DE3EBBC3D02C8154BD306BA422AE363A7E11102EC32D4CDFECD。
元PE研究用コピーSHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9は2026-10-29選択済み（READ-ONLY）。
## 新しいEの独立照合
callsite 0x5AC611はPE32のE8 rel32からcallee 0x510850に一致。0x5AC601から21バイトSHA=A53E7A689661E398DEE277860E8933E7B9EC90F7FAB50A7B85653FDF99E2F814。
callee 0x510850から37バイトSHA=831A504E2009B2001517E43B86AED1B835CD83D7A6D338B3E6F024F28F2C3372。両窓の元PE由来実バイトを照合。
B表記「0x15B / 0x25B」はそれぞれ 0x15 bytes / 0x25 bytes の長さ記載。初回E検証で誤ってhex整数0x15B/0x25Bと解釈しSHA不一致（OTHER）→独立Capstone ASM・byte幅診断で確定訂正、同一E検証コードの幅のみ修正し再実行PASS。安全拒否ではない。
callee入力はSを呼出前ESPとしたときP=[S+0x38]（tree head）、B=[P]、begin=B/end=P。PUSH2個後はESP=S-8、ESI=S+0x30、EAX=S+0x34。calleeのEAX=[EDI+4]=PゆえCMP(B,[P])一致・CMP(P,P)一致。
したがって**このcaller限定で0x510867全域erase**へ分岐し、partial 0x5108DFに進まない。空木であっても「全域ルートを選択」と「実際のnode解放数」は異なる。他callerのpartialは禁止していない。
### T020テスト
新規36合成fixture: 正常24（8種類のstack基点×tree 0/1/4）、不正/過剰帰属拒否12。新規36/36 PASS、PE窓SHA 2/2、E8 rel32 1/1。
対象の既存T028 gate 12本も再実行し、計13/13検証器exit0。合成回帰従来336件＋新規36件=372件すべてPASS。21H provenance 3条件を別集計すれば検査総数375。
原作EXEのゲームプレイ0、実破棄/二重free/Spot+0xB8/士気/通知/翌tick観測0。Game DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
## MASTER・Golden・T019
MASTERの公式checkpoint196、READY596（A115/B229/C136/D116）は既知公式値を維持。現在のTASK QUEUE34行を再集計してDONE9/IN_PROGRESS21/VERIFY4。B09研究NOT READY、READY新規統合0。MASTER変更なし。
T018 C-NB02合法G0 UI開戦、G1同run直前未改変SAVE＋press/hold/release入力SHA、G2実MAP＋攻防援三陣営＋順序付きUnit/Troop、G3戦闘終結、G4World差分はまだ同run一次証拠不充足。x20改変DAT、別watch、合成fixtureは代用不可。
T019新規確定原作矛盾0。GameClear DAT13/TXT2字句scopeのみRESOLVED、TXT実読込/script2勝者/phase flag/gwrite/decide11はVERIFY。
## 安全・再開
旧安全拒否のT018表境界/E session-join/T019 XREF/C T026/T032/D T030 TSV/0x5710C0はBLOCKED維持、再試行・迂回0。旧OFFLINE-UNSYNCED意味重複未照合。今回新規安全拒否0、コマンドの初回幅解釈エラーはOTHER/RECOVERED。
書込範囲はE-owned testsの新規validator/fixture/byte診断/本監査/独立readback記録のみ。原本、MASTER、A-D、REA、dev_lab、Git/Work/設定/自動化は変更しない。
次: 0x5AC5BD返値が0x495050以降で使われる境界、partial callerとの差、合法原作G0-G1-G2同一run証拠の受入確認。正式統合は所有者・READY証拠・ID重複・時刻・SHA・競合再照合後のみ。
[RECOVERY-ID E-RC-20261030-09H-T020-WINDOW-WIDTH-OTHER-01] 初回検証のB表記長を0x15B/0x25B（hex値）と誤解してPE窓SHA assertion失敗。独立read-only診断で21B/37Bのnative SHAと実ASMを確認。E新検証器の幅を訂正後36/36 PASS、未完了assert0。安全拒否ではない。
[RECOVERY-ID E-RC-20261030-09H-E-DRAFT-OTHER-02] E作成用JSでstructuredClone未定義のため、書込ループより前に停止、PCへの変更0。対象内容は別のE独立実装として新規構成し正常保存。08H監査文書の事前推測ファイル名read ENOENTも、E testsのdirectory一覧で既存実名を特定し復旧。いずれも拒否経路の再提出ではない。
