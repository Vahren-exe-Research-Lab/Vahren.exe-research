# B-20261019-2213-01 | T024 編隊配列29/30の三兵科共通穴（SOURCE-ONLY）
[SOURCE] 2026-10-19 JST。迫真0.67 CORE 正規化済み read-only data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_軍楽隊なし版.dat。未改変原作ZIP/EXEは実行・書込なし。
[SCOPE] 同sourceの砲兵/歩兵/騎兵リーダー配列を while(countVar(... ) > counter) の中でslot 0..50へコピーする明示if群だけを機械的に抽出。新EXE解析・VA/xref取得なし。
[FACT-CAV] 原文L1811-1812: form_general_numcav ==29 なら addv(@form_generalcav30,@form_cav_idx)。index30のif無し、31なら@form_generalcav31。0..50中にifは50件。
[FACT-INF] L1926-1927: form_general_numinf ==29 なら addv(@form_generalinf30,@form_inf_idx)。index30のif無し、31なら@form_generalinf31。ifは50件。
[FACT-ART] L2042-2043: form_general_numart ==29 なら addv(@form_generalart30,@form_art_idx)。index30のif無し、31なら@form_generalart31。ifは50件。
[EXTRACTION] 3系統それぞれ入力index0..50の51候補中、明示分岐50、missing-input={30}、mismatch={(29,30)}、slot29向けaddv分岐0。対象の保存済み正規化原文をLocal read_fileし、分岐条件とaddv先の正規表現で静的照合。
[RESET] 同一source先頭のclear(@form_generalcav29)、clear(@form_generalinf29)、clear(@form_generalart29)は存在。該当3ループではslot29を再投入せず、input29をslot30へ配置する。
[CONSUMERS] 歩兵slot29はL2168頃のf_c_kaimetsu死亡判定とL2598頃のsmoveTroopへ、砲兵slot29はL2195頃のa_c_kaimetsu判定とL2879頃のsmoveTroopへ参照される。騎兵slot29はL2170台の左翼死亡判定に参照。
[LOCAL CONSEQUENCE] 入力列が30人以上ならこの3ループの29番目(0起点)のleaderはslot30へ入る。31人以上なら30番目(0起点)のleaderを入れるifがなく、その回のslot29はこの3ループから供給されない。他経路からの書込・空値の実作用はVERIFY。
[BOUNDARY] これは原文の三つのコピー表に限定した確定形状。原作戦闘で30/31人の各兵科leaderが合法生成されるか、実際の編隊・敗走flag・移動指示への影響は未観測。原作バグ/実行時戦闘結果との一致は未確定。
[DEDUP] 以前のT024全滅flag参照/三兵科のリスト構造・fake leader301件の既証拠は再READYしない。今回だけの増分はcav/inf/art全3ループの入力29→slot30、入力30分岐欠落と下流slot29参照の結合。
[REIMPLEMENT] raw scriptの明示tableと正規化された理想連番tableを混同しない。旧互換実装では各兵科別{input-index,actual-slot,leader-ID,slot-state,consumer-call}を追跡し、検証前に29→29や30→30へ無断修正しない。
[GOLDEN] 合法旧battleでcav/inf/artの実leader count=29/30/31/32、各0起点input28/29/30/31の識別可能なunit、getTime=29/30・集合interval前後を観測。原作と再実装の攻防側、map、unit配置順、移動先、死亡判定、次tickを旧EXE/DAT/SAVE/map/input/capture SHAを固定して比較。
[GOLDEN-STATE] DESIGNED_NOT_RUN。通常UIで兵科lead countが観測できず合法条件を構築不可ならINELIGIBLE。原作Gameplay Golden PASS=0、新旧strict MATCH=0、新Task DONE=0。
[VERIFY/NEXT] 1) ループ前@form_cav/@form_inf/@form_art構築条件と上限、2) slot29への他writer/読取、3) no-entry空値のnative API semantics、4) 30/31人合法原作の可視再現、5) 既存T024詳細/HANDOFF重複監査。
[STATUS] SOURCE-ONLY STATIC candidate; B OWNED detailed receipt。T024正本/HANDOFFの独立readback成立後に限定READY判断。MASTER checkpoint191/公式588(A115/B221/C136/D116)は参照のみ。
[SAFETY] 旧T024 B-RC-20261019-2010-T024-INDEX-SAFETY-01とT011等安全拒否は独立BLOCKED。拒否元本文の再提出/代替経路への移送なし。MASTER/T018/他owner/原本/REA/dev_lab/Git/push/automationは変更しない。
