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
安全: 既存E安全拒否操作・T018表境界等は再試行/別経路迂回0。原本・他レーン・REA/dev・Git/Work/automation変更0。
PC負荷: 未測定。RUN CAPACITY: 正本から今回数値実測なし。DEVLAB担当直接送信/受領なし。
同期条件: PC最新MASTER/OWNER・READY IDs・既存E検証器とSHA/機能重複・安全拒否境界を照合して一度だけ取り込み。今回PCには本設計記録のみ、Python本体は非同期。
