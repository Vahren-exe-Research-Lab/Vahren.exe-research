# E-OFFLINE-UNSYNCED-20261020-2044-CNB02-SOURCE-ELIGIBILITY-GATE-01

research_id: `E-OFFLINE-UNSYNCED-20261020-2044-CNB02-SOURCE-ELIGIBILITY-GATE-01`  
owner: E  
tasks: T018 / T019 / T020 (historical E Golden acceptance boundary)  
source_relative_path: `tests/T018_CNB02_SOURCE_GATE_20261020_2044.md` (relative to authorized `_REDEV_RESEARCH`)  
source_original_sha256: `92B78B26BD6060F87AFE901C64FDC4CBBE41F5F2D123895DA74A431121102ABD`  
source_original_bytes: 3010  
source_sha_verified_at: 2026-11-03 JST (authorized PC, Get-FileHash read-only)  
evidence_kind: STATIC / SYNTHETIC historical / VERIFY; NOT an original gameplay run  
va_call_offsets: null for new E-native verification; other-owner native references, if any, are read-only source references  
golden_status: NOT_RUN / actual original-game PASS 0 / strict MATCH 0  
ready_status: NOT_READY / no formal MASTER update  
prior_ids_and_errata: Precedes and is refined by E-OFFLINE-UNSYNCED-20261020-2153-CNB02-TEMPORAL-SCOPE-01 and 2244 evidence-class report.  
publication_class: OWNER_INTAKE_ONLY / NOT_CURATED  

## Sanitized historical owner report

# E-CNB02-SOURCE-GATE-20261020-2044｜独立3値静的受入・死亡フック分離
作業ID: E-OFFLINE-UNSYNCED-20261020-2044-CNB02-SOURCE-ELIGIBILITY-GATE-01。研究E/T018,T019,T020/DEVLAB-006。分類STATIC SCRIPT+SYNTHETIC TESTED/NATIVE VERIFY/GAMEPLAY NOT RUN。
既存DEDUP: T018_GOLDEN_CORPUS.md T018-E-NB02-EVENT-CP108にinyumeb/u_inyume異hookは既記録。19:52 SELECT-LIFETIME研究も先行。新READY追加0、原作新BUG確定0。
一次資料1: 正規化2000_勢力ストーリー/po2_battle.dat全166行をE直接read-only確認。VS_toono/VS_inyume/yaju_VS_tonの3分岐と死後inyume_dead→VS_inyume_winの5条件を字句照合。
一次資料2: 正規化20_クラス/1919_その他.dat L566-576でclass inyumeb:inyumeのdead_event=inyume_dead。
一次資料3: 正規化10_ユニット/94_放浪_ホモガキ・養殖.dat L388-447でunit u_inyume:base1/class=c_inyume/dead_event=inyume_demoralization、class c_inyume:inyume。
一次資料4: 正規化50_その他新システム/siki.dat L2366-2373でevent inyume_demoralization→条件付きdialog→routine(base_demoralization)を確認。
検証器: ChatGPT独立コピー cnb02_source_gate.py。source predicate個別true/false/nullからSOURCE_COMPATIBLE_ONLY/SOURCE_BLOCKED/SOURCE_UNRESOLVEDを返す。actual PASSやold/new MATCHを発行しない。
重要境界: VS_inyumeはturn<5、sp16無所属、inPower(po2,u_inyume)==0等が字句条件。VS_toonoもsp16未所属とinSpotを要求。yaju_VS_tonにはsp16字句gateなし。
死亡時yet(VS_inyume)==0、yet(VS_inyume_win)、select==1、getBlueCount()<1等は別評価時点。選択UI時のselect値を死亡時値へ自動コピーしない。
同時に2イベントの元gateがtrueでもbattleevent setter/Yield/再開のnative意味はVERIFY。死亡instanceの宣言hookとruntime発火を混同しない。
追加合成テスト16件PASS/FAIL0。旧基盤525＋553/572/578差分を独立再展開し578件PASS/FAIL0。別suite合計594合成PASS/FAIL0、原作Gameplay actual PASS0。
G0合法旧sci1/po2/sp2→sp16侵攻、G1直前SAVE+操作時系列、G2実MAP/三陣営・ordered Troop/Unitの原作実機観測は全NOT RUN。T024比較8、T020作者変更6もNOT RUN。
PC正本MASTER最新末尾checkpoint195。最終全文再集計の正式READY595(A115/B228/C136/D116)・DONE9/IN_PROGRESS21/VERIFY4は先行E報告値で、今回全ID再抽出していない。
本PC文書は研究メタデータのみ。新検証器・16testのPC転送は未実施。DEVLAB直接受領未確認。MASTER更新0、正式READY追加0。
原本ZIP/EXE/SAVE、他レーンHANDOFF、REA/DEV、Git/Work、既存自動化は不変更。PC terminal sessions0、CPU実率不明。
次回は新証拠の版/OWNER/重複と原作G0合法採取条件を再照合。旧実観測なしにGolden/strict加算禁止。

## Independent limits and next verification

Only the historical E-owner research note is preserved here. Historical synthetic test claims were not rerun in this intake. Its original file-byte SHA was checked; content removed from the original is limited to old safety/refusal routing metadata and any protected-address references. Existing safety holds remain unchanged; this GitHub copy does not include refused source evidence. Before any Golden or READY claim, independently obtain matching same-run legal G0 UI/input, G1 immediately preceding SAVE bytes/time/order, and G2 original MAP, three sides, and ordered deployed Troop/Unit source receipts. Any original source code and fixtures previously said to remain on ChatGPT only are NOT implied to exist on the authorized PC.
