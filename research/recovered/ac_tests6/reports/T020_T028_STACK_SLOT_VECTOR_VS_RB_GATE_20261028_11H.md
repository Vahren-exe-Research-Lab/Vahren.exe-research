# E-AUDIT-20261028-11H-T020-T028-STACK-SLOT-VECTOR-VS-RB-01
Owner: E / T020。2026-10-28 11H JST。STATIC ORIGINAL BYTE CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READY。
## 出典・継承
- Desktop Commander Local Compact ONLINE。MASTER_LEDGER.md TASK QUEUE/最終checkpoint、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA PROGRESS、dev IMPLEMENTATION_PLAN、T018 Golden/T019矛盾、検索索引旧README/BUILD_MANIFESTをread-only参照。Ghidra/Javaの再解析なし。
- 新規B intake: B-20261028-11H-T028-CANDIDATE-VECTOR-VS-SECOND-SET-01。B詳細 data/T028_CANDIDATE_VECTOR_VS_SECOND_SET_NATIVE_20261028_11H.md SHA256 999B59CBD7EA8C833BEC209D9242CADCBFCAFDF987425E4B4F36585C3ACAE166。B status STATIC/VERIFY/NOT READY。
- 既存E10 Python tests/t020_t028_roster_vector_dual_set_producer_gate_20261028_10H.py SHA256 E1FE6F9AA6CE64193BD3EBAFF5C3F2C2F44BB12C3C245FB37E14CFE4226D393F。旧B10 2集合insertの既知証拠は再計上しない。
- 原作EXE研究用コピー rea_lab/targets/hakushin067_Vahren.exe をread-only SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187と照合。原作ゲームは起動していない。V3現行索引を対象とするB報告の静的意味は未確定箇所を含む。
## 今回のE独立クロスチェック
- 同じLEAの文字列 `[ESP+0x98]` でも、push回数が異なる。第2RB集合の0x493AED `[ESP+0xA0]` は2pushで元ESP+0x98、0x49460F/0x495161 `[ESP+0x98]` は4pushで元ESP+0x88。**0x497BB0のECXは第2RB集合でなく別vector**と区別する。
- 第1RB集合は元ESP+0x74。元ESP+0x88 candidate vector、第2集合元ESP+0x98を3つの別slotとして保持。文字列offsetだけのpointer同一視は不合格。
- 0x497BB0ではcandidate+0x75と+0x77が共に0、ECX非NULLの局所枝のみ0x4C1290へ、ECX NULLなら0x463590へ、flagのいずれか非0なら0x5846A0側へ分岐。vector appendをRB set insertと扱わず、効果成功も推測しない。
- 0x460E90到達時のフィールドzero/+0xC0=100/+0xE4=24は「当該CALL到達時」の局所補正に限定し、全候補の無条件resetと扱わない。
- EXE実バイトの4窓SHA256をB11資料指定値と4/4一致、REL32直接CALLを0x494618,0x49516A,0x497C21,0x497C31,0x4984AB,0x498D78,0x4C12AC,0x4C12CCの8/8で再計算一致。B11詳細現物SHAとE10コードSHAも2/2一致。Ghidra新解析・原作実行は0。
- **第2RB集合の真のconsumerは未発見（VERIFY）**。今回のvector writerをsecond-tree consumerとしてMASTERへ採録しない。
## T020回帰・厳密受入
- 新規 tests/t020_t028_stack_slot_vector_vs_rb_gate_20261028_11H.py、SHA256 A5476B07415F52CEA7BA3CBE75E7A094DAAAF37F401FE704E280A220566E1868。Python -B unittest新規30/30 PASS (exit0)、既存E10 40/40 PASS (exit0)、今回実行した2ファイル合計70/70 PASS。全T020累積値ではない。
- 30 testの対象：B11/E10/EXE SHA、4窓native SHA、8site CALL、push補正と3slot非同一、flags 0/非0組合せ/NULL ECX、候補reset条件、入力型境界、G0-G2不可時NO GOLDEN/actual観測不足/同一run欠落/新側結果欠落。すべてSTATICまたはSYNTHETICで実原作PASSではない。
- Golden最優先は合法原作UIのG0戦闘開始・ユーザー操作と同run証拠、G1直前SAVE byte SHAと順序付き入力、G2現物MAP SHA・三陣営・出撃Unit/Troopの順序・実配置。G3可視結果・G4戦略World差分も別の一次receiptが必要。20倍強化DATを無改変baselineと誤認しない。
- 新規 original gameplay DYNAMIC OBSERVED 0 / actual Golden PASS 0 / strict MATCH 0。今回静的/合成テスト成功を実機比較へ昇格しない。
- T019 新規確定矛盾0。既知GameClear DAT13/TXT2の字句検索scope差はRESOLVED、script2同名優先/phase flag/TXT実読込/gwrite復帰はVERIFY。異なるstack slotの混同は研究解釈の訂正であり原作エンジンBUG認定ではない。
## MASTER・所有権・安全・再開
- TASK QUEUE今回独立34件、一意34、DONE9/IN_PROGRESS21/VERIFY4。最後の正式checkpoint196、READY596(A115/B229/C136/D116)はMASTER旧正式記録の継承（READY全履歴再集計なし）。B11 NOT READYにつき今回の正式READY統合ID0、MASTER追記0。
- 2026-10-25 14H OFFLINE-UNSYNCED研究の完全意味重複と他owner全履歴との網羅照合は未完、正式統合BLOCKED。B側11H詳細・owner・HANDOFFは読取のみ、Eから変更しない。
- 既存T018表境界/session-join、T019 XREF、C T026/T032、D T030 TSV、0x5710C0ほか安全拒否は継承し、拒否元の再試行・別tool/path/shell/Remote/ZIP迂回なし。今回新規安全拒否0、接続失敗0。
- 本回のPC変更はE所有T020新Pythonと本報告書のみ。MASTER、A-D/REA/dev_lab、原本EXE/DAT/SAVE/ZIP、Git/push、Work、設定、scheduleには書込0。
- NEXT P0: 合法原作同一戦闘G0/G1/G2を一次receiptで満たすこと。P1: B11の元ESP+0x88 vector のproducer/consumerと第2RB集合の真のconsumerを別々に検証。0x497BB0の後段条件と候補ポインタ型はVERIFY。
