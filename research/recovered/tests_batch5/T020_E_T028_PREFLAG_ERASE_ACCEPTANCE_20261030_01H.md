# 研究E T020 退却Spot-index range-eraseのflag前呼出を回帰契約へ追加（2026-10-30 01H）
研究ID: E-AUDIT-20261030-01H-T020-T028-PREFLAG-ERASE-PROVENANCE-01
状態: STATIC SOURCE PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作Gameplay NOT RUN。
## 出典と今回の独立差分
- B owner ID B-20261030-0113-T028-SPOT-INDEX-EQUALRANGE-ERASE-01。B詳細 data/T028_SPOT_INDEX_EQUAL_RANGE_ERASE_NATIVE_20261030_01H.md の実SHA256=98C6A37BF0FFDB2306EC939E3E262B7AE4A8091A6E71C4EA400E709244251B7E、SOURCE VERIFY/NOT READY。
- 前E00H検証コード t020_e_t028_vector_helper_mode_gate_20261030_00H.py の実SHA256=F68E64DDE7BFD41BCD898B8ED7A87303A166BCF08E7EE0614D1BACDC21359C93。過去コードは上書きせず継承。
- B原作ASM根拠：0x598469 CALL0x416080→0x59847C CALL0x415CF0（初回key）、0x5984C7 CALL0x416080→0x5984DA CALL0x415CF0（各vector entry）、flag判定0x5984DFより前。従ってflag0でも範囲探索とerase-rangeへの呼出経路が存在する。vector長0でも初回key経路は残る。
- 0x415CF0はfirst/lastに応じて0x415D0A→0x416870全消去候補、または0x415D8F→0x416220逐次消去。実際に何node削除されるか、key比較0x402C40の等価性、tree owner、元GAMEでの到達はVERIFY。B sideより強い動的断定を行わない。
## T020 追加受入条件・検証
- 新規22件のSTATIC制御フロー由来の**合成**fixture：tests/T020_E_T028_PREFLAG_ERASE_CASES_20261030_01H.json、検証器 tests/t020_e_t028_preflag_erase_gate_20261030_01H.py。
- 合成モデルは、正常に呼出が進む仮定で初回1+vector長のerase-range callsiteを数える。**実際の削除node数はUNKNOWN**。flag0・vector0を無副作用と誤認しない。
- unsupported claim（lookup-only、no mutation、full clear、1node除去、Golden PASS）、comparator未確定、0x5AC5E7のCFG未確定、site/mode不一致、不明入力をfail closed。
- 新規SOURCE_PINS 2/2 PASS、新規合成22/22 PASS。既存00H mode18/18、23H予約21/21、22H容量18/18も独立再実行PASS。合計79/79 SYNTHETIC PASS、原作GameplayはNOT RUN、strict MATCH0。
## MASTER / T018 / T019
- E正式checkpoint196、READY596=A115/B229/C136/D116は前回正式確認値。34 Task DONE9/IN_PROGRESS21/VERIFY4は旧値（全件再集計なし）。今回B sourceはVERIFY/NOT READYなので新規正式READY統合0。MASTERは未編集。
- C-NB02 旧合法UI G0限定観測あり。G1同一戦闘の直前未改変SAVE+入力、G2 ACTIVEのMAP/攻防援軍3side/順序付きUnit/Troop、G3、G4の連結済一次証拠は不足。E Golden認定DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2検索scope差のみRESOLVED；script2優先/phase flag/TXT runtime/gwrite復帰/decide11はVERIFY。
## 安全・復旧 / 再開
- 新規安全拒否0、PC接続障害0。既存T018表境界、E session-join/T019 XREF、C T026/T032、D T030 TSV、禁止0x5710C0等はBLOCKEDのまま。同じ操作を別shell/tool/path/Remote/ZIPで迂回しない。
- OFFLINE-UNSYNCED古い成果の全ID・意味重複照合は未完了。原本EXE/DAT/ZIP/SAVE、A-D/REA/dev_lab、Git、Work、設定、automation変更なし。
- 次：B owner 0x402C40 comparator / 0x416220 node removal帰結の一次証拠が得られた場合のみ受入分類更新。同時に合法同run G0-G1-G2の旧SAVE/UI入力/MAP/名簿receiptの有無を優先監査。
