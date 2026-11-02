# E-OFFLINE-UNSYNCED-20261020-2348-G0-TRIAGE-01

research_id: `E-OFFLINE-UNSYNCED-20261020-2348-G0-TRIAGE-01`  
owner: E  
tasks: T018 / T019 / T020 (historical E Golden acceptance boundary)  
source_relative_path: `tests/T018_CNB02_G0_UI_ROUTE_TRIAGE_20261020_2348.md` (authorized `_REDEV_RESEARCH` root)  
source_original_sha256: `9B7F07C743B5C1BC3B37E57521DE5190324ADF41089A102E4FEB63F74EC82783`  
source_original_bytes: 4141  
source_sha_verified_at: 2026-11-03 JST (authorized PC, read-only hash)  
evidence_kind: STATIC / historical SYNTHETIC / VERIFY; NOT an original gameplay run  
va_call_offsets: null for newly verified native E evidence; B/native refs, if any, remain citation-only  
golden_status: NOT_RUN / original gameplay PASS 0 / strict MATCH 0  
ready_status: NOT_READY / no formal MASTER change  
prior_ids_and_errata: Refines earlier 2044/2153/2244 synthetic G0 eligibility checks; follow-on 0050 same-run chronology.  
publication_class: OWNER_INTAKE_ONLY / NOT_CURATED  

## Sanitized historical E-owner report

# E T018 C-NB02 G0通常UI入口の独立トリアージ（2026-10-20 23時台）
作業ID: E-OFFLINE-UNSYNCED-20261020-2348-G0-TRIAGE-01
分類: STATIC SOURCE VERIFIED / SYNTHETIC TESTED / RUNTIME VERIFY / Gameplay NOT RUN。E所有の新規独立研究資料、正式READYではない。
[LOCAL READONLY] MASTER末尾checkpoint195、前回確定READY595=A115/B228/C136/D116。今回正式READY追加0、MASTER非変更。34 Task DONE9/IN_PROGRESS21/VERIFY4は前回値・今回再判定なし。
[SOURCE] 原作正規化po2_battle.dat L1-29をLocal read-only再読。VS_toono→VS_inyume→yaju_VS_tonの局所条件順。前二つはsp16のSpot/Power条件を持ち、VS_inyumeにはturn<5条件あり。原作実発火は未観測。
[CROSSWALK] C保存 T025_WRQ_C_BATTLES_CAPTURE_REFERENCE_GATES_20261013.jsonをread-only再読。sp16のPower+0x68逆参照はsave1/auto/save2いずれも空。save1/save2 Spot.member Unit48。これらは旧native所有勢力・合法攻撃・実出撃名簿の証拠にはならない。
[NEW DELTA] G0合法UIをNOT_RUN/ATTACK_SELECTABLE/ATTACK_UNAVAILABLE/UNDETERMINEDで区別。UIで攻撃操作が無効でもそのsnapshotだけの事実とし、C-NB02が全局面で到達不能とは断定しない。run ID・TZ付時刻・original EXE SHA・capture SHA・UI入力SHAがない実観測主張はVERIFY。
[SIMULATION REPLAY] 525基盤＋553/572/578/594/618/22時台の検証器差分をChatGPT独立環境で再構成。28モジュールを個別実行し634件PASS/0 FAIL。重いstrict JSONモジュールは一度短いtimeout後に8.61秒実行で16 PASS。旧一括634 suiteはTIMEOUTのまま（分割成功と区別）。
[NEW SYNTHETIC] cnb02_g0_ui_route_gate.pyおよび16合成テストを別途実行して16 PASS/0 FAIL。確認できた分割合成テスト計650件。単一650 suite RUNなし。ゲームEXE起動0、Gameplay Golden actual PASS0、old-new strict MATCH0。
[GOLDEN] G0旧通常UI合法開戦、G1同run事前SAVE bytes+SHAとSAVE/攻撃/開始時系列、G2実MAP・3side・ordered Troop/UnitはいずれもNOT RUN。T018対T024 SAVE順序の受入規約差はVERIFY。T024 8例/T020 6条件もNOT RUN。
[T019/REA] ZNM help15/raw10、cook_heal help3000/raw1500、po/poo、GameClear、角度二重keyなどVERIFY維持。REA新pseudo-vs-ASM確定差分0。
[DEVLAB] DEVLAB-003/006へ: 保存Power逆参照から攻撃可否を推論しない。G0 UI入口/G1 SAVE順序/G2 map+sideの証拠を別gateにし、仮入力からGAMEPLAY PASSを出さない。直接送信・受領確認は未実施。
[OFFLINE PACKAGE] ChatGPT作業環境 E_OFFLINE_20261020_2348_CNB02_G0_ROUTE_TRIAGE_SEGMENTED650.zip（SHA256 966aaf0a405f5142269c180a3dc4c95025c9917a04978a7021ca4c25ecb1ca73）。Python本体/16テストはPC未同期で、PCへ保存するのはこの独立研究要約だけ。
[NEXT] 将来PC実装取込時は既存E T018と重複・最新MASTER/規約・SHA・競合・READY権限を一度だけ照合。合法UI G0の真正なscreen/input receiptを優先。

## Limits and next validation

The original E-owner source file exists and its byte SHA256 was rechecked; the GitHub copy removes previous refusal-routing/protected-address metadata lines and does not contain the refused evidence. Historical synthetic results were not rerun. A paper/STATIC/SYNTHETIC gate cannot replace genuine same-run original-game G0 legal UI/action, G1 immediately preceding SAVE actual bytes + timezone-aware input order, and G2 actual MAP/three-side/deployment evidence. Reproduction artifacts stated as ChatGPT-only in the old report remain UNVERIFIED for the authorized PC, not implicitly synced.
