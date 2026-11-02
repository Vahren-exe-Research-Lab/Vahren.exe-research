# E-OFFLINE-UNSYNCED-20261020-2244-CNB02-EVIDENCE-CLASS-01

research_id: `E-OFFLINE-UNSYNCED-20261020-2244-CNB02-EVIDENCE-CLASS-01`  
owner: E  
tasks: T018 / T019 / T020 (historical E Golden acceptance boundary)  
source_relative_path: `tests/T018_CNB02_EVIDENCE_CLASS_BOUNDARY_20261020_2244.md` (authorized `_REDEV_RESEARCH` root)  
source_original_sha256: `0B6637393E1408CE83403C85973D7BB485A001E2A9616B62BC346C9690BAB123`  
source_original_bytes: 3162  
source_sha_verified_at: 2026-11-03 JST (authorized PC, read-only hash)  
evidence_kind: STATIC / historical SYNTHETIC / VERIFY; NOT an original gameplay run  
va_call_offsets: null for newly verified native E evidence; B/native refs, if any, remain citation-only  
golden_status: NOT_RUN / original gameplay PASS 0 / strict MATCH 0  
ready_status: NOT_READY / no formal MASTER change  
prior_ids_and_errata: Erratum / strengthening of 2153 read-site gate: NOT_RUN truth values cannot be silently treated as observed game conditions.  
publication_class: OWNER_INTAKE_ONLY / NOT_CURATED  

## Sanitized historical E-owner report

# T018 C-NB02｜NOT_RUN条件値混入の独立監査（2026-10-20 22時台）
ID: E-OFFLINE-UNSYNCED-20261020-2244-CNB02-EVIDENCE-CLASS-01
担当: E / T018（T024/DEVLAB-006受入提案）。非READY・非MASTER正式統合。
資料: PC MASTER checkpoint195、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA PROGRESS、DEVLAB IMPLEMENTATION_PLAN、保存E T018、原作normalized po2_battle.dat全166行。すべてread-only参照。
分類: STATIC SOURCE RECHECK / SYNTHETIC REPRODUCED / NATIVE VERIFY / GAMEPLAY NOT RUN。
【新規差分】前回E独立cnb02_temporal_scope_gate.pyのNOT_RUN入力が、未観測にもかかわらずVS_toono条件をtrueで埋めるとSOURCE_COMPATIBLE_ONLYと出すケースを再現。
旧ツール自体も実機PASS=0を維持するので「誤Gameplay PASS」ではない。問題はNOT_RUNとsynthetic条件値が混在し、下流レビューを誤誘導し得ること。
独立追加gate cnb02_evidence_class_gate.py: NOT_RUNなら各read-site条件は未入力/nullのみ許可。true/falseを入れる計画はSYNTHETICへ分類し、ゲーム実観測扱いしない。
前回のread-site4段とSOURCE gateの判定ロジックは変更せず、補助チェックとして追加。元v1と追加gateの検証境界を混同しない。
合成追加16 unittest PASS/FAIL0。source gate16+temporal24+今回16=3群56 PASS/FAIL0を独立実行。
全歴史テスト618+今回16の一括再実行は長時間処理がtimeoutとなり今回合格主張不可。上記56件のみ今回の実証。
NOT_RUNテンプレート独立CLI: exit1、status NOT_RUN、Gameplay PASS0。SYNTHETIC例: exit0、status SYNTHETIC_SOURCE_DESIGN_ONLY、Gameplay PASS0。
ChatGPT側成果: 新Python、16 tests、G0/G1/G2 operatorテンプレート、read-site NOT_RUN/SYNTHETIC例、実行ログ。PC側Python実装・テスト実体は未同期。
【G0】sci1/po2/sp2→sp16の通常UI合法開戦、実turn/choice/入力trace・capture SHAは未観測。内部battleevent/selectはnull。
【G1】同一runの直前SAVE bytes/SHAとSAVE→attack→battle開始の入力時系列を観測要。T018/T024の順序規約差はVERIFY。
【G2】実MAP ID/hash・攻/防/支援の3side・出撃順のTroop/Unitと可視死亡処理は未観測。
T019既矛盾候補・REA新確定差分なし、DEVLAB-006受入案: NOT_RUNの真偽値を元ゲームのsource truthに見せない。
旧EXE/DAT/SAVE実行・編集0、ゲーム原作DYNAMIC OBSERVED0、Gameplay actual Golden PASS0、strict MATCH0。
公式新READY0、checkpoint更新0。前回正式595=A115/B228/C136/D116は最終照合報告値、今run全件再集計なし。34Task 9/21/4は未再判定。
PC負荷: 未測定。RUN CAPACITY: 正本から今回数値実測なし。DEVLAB担当直接送信/受領なし。

## Limits and next validation

The original E-owner source file exists and its byte SHA256 was rechecked; the GitHub copy removes previous refusal-routing/protected-address metadata lines and does not contain the refused evidence. Historical synthetic results were not rerun. A paper/STATIC/SYNTHETIC gate cannot replace genuine same-run original-game G0 legal UI/action, G1 immediately preceding SAVE actual bytes + timezone-aware input order, and G2 actual MAP/three-side/deployment evidence. Reproduction artifacts stated as ChatGPT-only in the old report remain UNVERIFIED for the authorized PC, not implicitly synced.
