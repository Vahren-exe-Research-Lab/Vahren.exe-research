# E-OFFLINE-UNSYNCED-20261021-0050-CNB02-CHAIN-01

research_id: `E-OFFLINE-UNSYNCED-20261021-0050-CNB02-CHAIN-01`  
owner: E  
tasks: T018 / T019 / T020 (historical E Golden acceptance boundary)  
source_relative_path: `tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md` (authorized `_REDEV_RESEARCH` root)  
source_original_sha256: `B0D464FD2C3C142B241E3C0F12228EDC77DEA9EF8E3E218E48C5414911FC4DE1`  
source_original_bytes: 3600  
source_sha_verified_at: 2026-11-03 JST (authorized PC, read-only hash)  
evidence_kind: STATIC / historical SYNTHETIC / VERIFY; NOT an original gameplay run  
va_call_offsets: null for newly verified native E evidence; B/native refs, if any, remain citation-only  
golden_status: NOT_RUN / original gameplay PASS 0 / strict MATCH 0  
ready_status: NOT_READY / no formal MASTER change  
prior_ids_and_errata: Refines 2348 UI-G0 with same-run G1 SAVE/input before battle start, and G2 visible capture chronology.  
publication_class: OWNER_INTAKE_ONLY / NOT_CURATED  

## Sanitized historical E-owner report

# 研究E：C-NB02 G0/G1/G2同一run・時系列整合ゲート（2026-10-21 00:50 JST）
作業ID: E-OFFLINE-UNSYNCED-20261021-0050-CNB02-CHAIN-01
分類: STATIC SOURCE VERIFIED / SYNTHETIC TESTED / 原作DYNAMIC OBSERVED=0 / Gameplay Golden actual PASS=0 / strict MATCH=0。
[NEW DELTA] 前回G0単段UI入口判定とT018/T024順序ゲートの間をつなぎ、同一run/sessionを明示したG0/G1/G2観測票でsave・attack・battle start・G2 capture時刻を整合検査する独立検証器をChatGPT環境に作成。
[SOURCE] 原作正規化po2_battle.dat 166行の冒頭をLocal read-only確認。event po2_battleはsp16に対しVS_toono→sp16再取得→VS_inyume→yaju_VS_tonの局所順。合法な攻撃UI到達と旧エンジン実発火は未観測。C-NB02 sci1/po2/sp2→sp16のSpot/P+0x68静的情報は実攻撃可能性の証明でない。
[CHRONOLOGY] G1のsaveとattackは各battle startより前、同時刻記録は曖昧として拒否。G2画面捕捉が申告battle startより先なら拒否。異なるタイムゾーン表記はUTC同時刻へ正規化して比較。
[POLICY] SAVE→attackならT018/T024両規約でメタデータ順序整合。attack→SAVE→battleならT018 review可でもT024 VERIFYとなる別flag。どちらが原作合法UIで可能か実機未観測。
[NEGATIVE] G0で一度ATTACK_UNAVAILABLEでも後に攻撃可能へ変化する場合を否定しない。G1/G2が申告されてもG0が不可だった時点とは別の追加画面証拠が必要というflagのみ。未観測stageはnullを維持。
[PROVENANCE] SHA256書式の検査は元バイト実検査・真正性証明と異なる。OPERATOR_UI_UNAUTHENTICATEDでもREVIEW止まり、SYNTHETICはゲームPASSに換算しない。
[RESULT] 新規Pythonゲート28合成テストPASS/0FAIL。前回のG0単段16テストと併せて44件を同一ChatGPT環境で実再実行PASS/0FAIL。既存履歴650件を今回は再走査・合計加算していない。
[FILES] ChatGPT環境のE_CNB02_CHAIN_20261021_0050.zipに新コード、NOT_RUN観測票、テスト、ログ、SHA manifestを保全予定。Python本体/fixtureのWindows PC側同期は未実施。
[MASTER] 直前read-onlyでMASTER 4484行末尾checkpoint195を確認。公式READY595=A115/B228/C136/D116は過去の独立照合値。今回公式READY追加0、checkpoint変更0。34 Task DONE9/IN_PROGRESS21/VERIFY4は未再判定。
[GOLDEN] G0合法旧通常UI開始、G1同run直前SAVE実バイト/SHA＋入力、G2実MAP/三side/出撃Unit・Troopの全てNOT RUN。T024比較8/T020変更6条件NOT RUN。T019既知矛盾とREA新確定差分は今回進展なし。
[DEVLAB-006] old実体file hashes・録画・UI入力・session/run・SAVE/attack/start order・三side/実deployを独立に収集。未実測内部select/battleeventはnull。等価なold/new実captureが揃う前にMATCHを付けない。開発担当へ直接送信・受領確認なし。
[NEXT] 合法UIでG0が開戦可能なrunを撮影し、G1直前SAVE actual bytesと操作時系列、G2画面+三side+実ロスターを紐づけて初めて旧原作Golden監査へ進める。

## Limits and next validation

The original E-owner source file exists and its byte SHA256 was rechecked; the GitHub copy removes previous refusal-routing/protected-address metadata lines and does not contain the refused evidence. Historical synthetic results were not rerun. A paper/STATIC/SYNTHETIC gate cannot replace genuine same-run original-game G0 legal UI/action, G1 immediately preceding SAVE actual bytes + timezone-aware input order, and G2 actual MAP/three-side/deployment evidence. Reproduction artifacts stated as ChatGPT-only in the old report remain UNVERIFIED for the authorized PC, not implicitly synced.
