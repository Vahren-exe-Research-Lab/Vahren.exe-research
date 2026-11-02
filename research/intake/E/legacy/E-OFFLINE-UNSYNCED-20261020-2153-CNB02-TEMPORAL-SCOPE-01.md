# E-OFFLINE-UNSYNCED-20261020-2153-CNB02-TEMPORAL-SCOPE-01

research_id: `E-OFFLINE-UNSYNCED-20261020-2153-CNB02-TEMPORAL-SCOPE-01`  
owner: E  
tasks: T018 / T019 / T020 (historical E Golden acceptance boundary)  
source_relative_path: `tests/T018_CNB02_TEMPORAL_SCOPE_20261020_2153.md` (relative to authorized `_REDEV_RESEARCH`)  
source_original_sha256: `AD5AFCB9CD1D48FE70BE0C0A607D9069423B80F90BBDDBBD82841292EF37129C`  
source_original_bytes: 2604  
source_sha_verified_at: 2026-11-03 JST (authorized PC, Get-FileHash read-only)  
evidence_kind: STATIC / SYNTHETIC historical / VERIFY; NOT an original gameplay run  
va_call_offsets: null for new E-native verification; other-owner native references, if any, are read-only source references  
golden_status: NOT_RUN / actual original-game PASS 0 / strict MATCH 0  
ready_status: NOT_READY / no formal MASTER update  
prior_ids_and_errata: Refines 2044 gate with distinct source read-site epochs; followed by 2244 NOT_RUN evidence-class guard.  
publication_class: OWNER_INTAKE_ONLY / NOT_CURATED  

## Sanitized historical owner report

# T018 C-NB02 読取時点別 SOURCE gate｜2026-10-20 21時台
研究ID: E-OFFLINE-UNSYNCED-20261020-2153-CNB02-TEMPORAL-SCOPE-01
状態: STATIC SOURCE RECHECK / SYNTHETIC TESTED / NATIVE VERIFY / GAMEPLAY NOT RUN
所有: E（T018主・T019/T020参照）。正式READYではない。MASTER更新・checkpoint追加なし。
出典: 原作正規化 po2_battle.dat 全166行を今回Localでread-only再照合。
原文: storeBattleSpot(@aaa)→storePowerOfSpot(sp16,@bbb)→VS_toono条件/set(battleevent,1)/routine→storePowerOfSpot(sp16,@bbb)再取得→VS_inyume条件/set/routine→clear(@aaa/@bbb)→yaju_VS_ton条件。
独立増分: 20:44版のSOURCE gateは battleevent_is_zero、battleSpot_is_sp16、sp16_power_is_unowned を複数siteで共用でき、条件評価時点の出典が曖昧。
今回: 4 read-site(VS_toono/VS_inyume/yaju_VS_ton/inyume_dead_to_win)を分離した合成検証器と24 unittestを作成。値の他stage転記は不可。
合成例: 第一候補の条件をtrue、後続別siteのbattleevent_is_zero=false→前者SOURCE_COMPATIBLE_ONLY、後者SOURCE_BLOCKED。原作runtimeの結果とは主張しない。
ChatGPT側の基盤525+553+572+578+594に本差分24件を適用し、618 PASS/0 FAILを独立再実行。全件は合成/監査テスト。GAMEPLAY互換性PASSではない。
オフライン成果名: E_OFFLINE_20261020_2153_CNB02_TEMPORAL_SCOPE_DELTA_618.zip
ZIP SHA256: 9bc57de0a0d704193ee006a3b54b4a7d8d781a5f31235d18ab92d408f632bfaa
PCのPython実装・追加24件は未同期。旧2044 SOURCE gate、E所有T018の既存設計を置換しない。
G0: sci1/po2/sp2→sp16合法通常戦闘の旧UI・選択実入力・同run IDを原作から採取待ち。
G1: 同run戦闘直前SAVEの原本バイトSHAとSAVE/攻撃入力時刻・trace SHAを採取待ち。T018/T024順序差はVERIFY。
G2: 旧実MAP・攻防支援3side・ordered Troop/Unit・death callback/choice演出を採取待ち。
ゲーム原作EXE未実行。G0/G1/G2、T024 8条件、T020 6条件 NOT RUN。原作DYNAMIC OBSERVED0、Gameplay actual PASS0、strict MATCH0。
READY: 今回正式新規0。checkpoint195、READY595=A115/B228/C136/D116は前回全文確認値。34Task DONE9/IN_PROGRESS21/VERIFY4（未再判定）。
次回: 最新MASTER/規約、E所有T018設計、B未統合26候補、RUN CAPACITYと予約/競合を照合。観測資料がない限りGolden PASS加算禁止。

## Independent limits and next verification

Only the historical E-owner research note is preserved here. Historical synthetic test claims were not rerun in this intake. Its original file-byte SHA was checked; content removed from the original is limited to old safety/refusal routing metadata and any protected-address references. Existing safety holds remain unchanged; this GitHub copy does not include refused source evidence. Before any Golden or READY claim, independently obtain matching same-run legal G0 UI/input, G1 immediately preceding SAVE bytes/time/order, and G2 original MAP, three sides, and ordered deployed Troop/Unit source receipts. Any original source code and fixtures previously said to remain on ChatGPT only are NOT implied to exist on the authorized PC.
