# E-AUDIT-20261025-05H-T018-T019-T020-WORLD-FIGHT-FLAG-EPOCH-01
Owner E/T018,T019,T020 | 2026-10-25 05H JST | STATIC SOURCE VERIFIED / native timing VERIFY / NOT READY / Golden NOT RUN.
## 今回の一次照合（Local Compact read-only、normalized CORE）
- scenario1.dat L1,28-30: sci1 に world=wev1、fight=fev1。実byte SHA256 F85C127D452FA5E78DB828EDACC36159EC6450B74F4EBB03DC975B5B3AD6F649。
- event_world.dat L2-4,59-60,約70-80: wev1 内で set(battleevent,0) と set(battlebgmchange,0) が isNewTurn() 条件分岐より前にある。実SHA256 523B389E2E985D3924D83246E076343F8AA1EA2C610044B1739E6792EB7E7D9A。
- event_world.dat には背景付きイベント等で同じWorld eventが再入し得る旨の作者コメントがあり、複数entryへの注意が記される。これは注釈であり今回の旧EXE実機挙動ではない。
- 100_イベント汎用/event_battle.dat L1-20: fev1 は if(isPlayer(po2)) の真で routine(po2_battle) を記述。実SHA256 A4943F347A1F29034BD46680CFE9BA1EC78656D62B8E1531C8C201A30C9017E2。
- 2000_勢力ストーリー/po2_battle.dat L1-31: VS_toono・VS_inyume・yaju_VS_ton は順に battleevent==0 をgateとし、それぞれ set(battleevent,1) が routine(event) より前。実SHA256 DABAEB974585C3E7FA1F66190792C11F786E3915F723BF7D6C9F0BB8D446A88A。
- normalized *.dat の set(battleevent,0) 完全文字列検索は event_world、free_ev_world、ev_rnd、ev_dream、event_test の計5ファイル5箇所。これは字句scopeであり、loader採用・全経路・実行回数の証明ではない。
## 独立差分と既知成果の重複境界
- 先行C-20261013-1208-01（evidence/T025_WRQ_NB02_EVENT_GATE_CROSSWALK_20261013.json）は sci1→fev1→po2_battle、3イベントのguardと順序、inyume_dead のClass/Unitコールバック差を既記録。これらを今回の新発見・READYとして再計上しない。
- 新たにE比較契約へ追加する差分は、sci1側の battleevent リセットがWorld new-turn二重呼出防止guardより前に配置される事実と、Fight側の事前setを『ターン固定の永続フラグ』とみなせない境界。
- world前段 routine(castleset/randomset) 等のYield/実到達順、実際のworld再入、変数scope、yet marker保存性、select取消後の値、現runのフラグ値はVERIFY。静的順序を旧EXEの可視動作や実行済みとして扱わない。
## T020 新規負例fixtureの判定設計（いずれも DESIGNED / NOT RUN）
- F01: 同一turnかつWorld entry数不明で battleevent を前戦闘から機械的に継承する → FLAG_EPOCH_UNPROVEN。
- F02: getTurnは同じだがWorld event再入が観測済、new-turn guardの内側でしかresetされないと仮定 → WRONG_RESET_SCOPE（source STATIC）／旧EXEの実reset時刻はVERIFY。
- F03: G0のSpot IDだけ一致し操作勢力が未確定なのにpo2_battle演出を固定する → PLAYER_POWER_UNPROVEN。
- F04: VS_inyumeのdialog選択を取消し、表示演出無しをbattleevent=0と推定する → FLAG_AFTER_CHOICE_UNPROVEN。
- F05: 先行VS_toono候補と後続VS_inyume候補の両方を同時発火確定とする → EVENT_ORDER_UNPROVEN。
- F06: 同じscene/turn/SpotだがWorld entry時系列・battleevent初期receipt不明の二つのrunを同一Goldenと判定する → RUN_PHASE_UNPROVEN。
- 受入票へ {run_id, old_exe_sha, old_DAT_set_sha, scenario, controlling_power, turn, world_event_entry_receipt_or_null, native_battleevent_or_null, visible_event_choice, G0_spots, G1_SAVE/input_SHA, G2_map/3side/ordered_roster, source_receipt_SHA, eligibility} を別欄で保持。
## 管理・判定
- T019 新規確定Wiki/DAT/EXE矛盾0。GameClear字句scope RESOLVED、script2優先・phase flag・TXT実読込・gwrite復帰VERIFY据置。
- 公式MASTER最終checkpoint196/READY596 (A115/B229/C136/D116) は旧確認値。34Task DONE9/IN_PROGRESS21/VERIFY4は2026-10-25 02H再集計の旧値。今回新規READY統合0、MASTER書込なし。
- C-NB02合法旧UI G0、同run直前SAVE+入力 G1、実MAP/三side/確定Unit/Troop G2、戦闘終了 G3、World差分 G4 は未充足。E新規実機DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- 過去のT018表境界/E session join/他レーンC T026/T032/D T030/禁止0x5710C0等安全拒否はBLOCKEDのまま。旧OFFLINE-UNSYNCED採否保留。禁止再試行や迂回なし。
- 本記録だけE所有testsへ新規保存。原本EXE/ZIP/SAVE/DAT、他owner、REA/dev_lab、MASTER、Git/Work、設定/スケジュール変更なし。
- NEXT: 同一原作runでWorld entry→fight fev1→po2 special event→G3→World復帰の合法可視receiptを収集。入力・観測時刻・source hashで結合し、flag値が観測不能ならnullのまま比較対象を限定する。
