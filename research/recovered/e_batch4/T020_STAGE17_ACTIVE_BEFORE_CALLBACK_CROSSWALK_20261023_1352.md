# E T018/T020｜Stage17 active書込とside callbackの受入境界（2026-10-23）
ID: E-AUDIT-20261023-1352-STAGE17-ACTIVE-PRECALLBACK-GATE-01
状態: STATIC CROSS-SOURCE / E-OWNED / VERIFY / DESIGNED_NOT_RUN / NOT READY。
出典: search_index/BATTLE_STAGE17_ACTIVATION_BOUNDARY_20261022.json（Stage17 V2 receiptにSHA 18165D01E2A87F3188EA44AB5C890AFDBF6E822B14D07839E6416C45313F8F7A と記載）、同BATTLE_STAGE17_VALIDATION_V2_20261022.json、BATTLE_STAGE13_PACKET_REQUIREMENTS_20261022.json、E既存tests/T020_NATIVE_PREBATTLE_AND_EXIT_TRANSIENT_GATE_20261022_0646.md、T020_SAME_PID_DUAL_BATTLE_WINDOW_CROSSWALK_20261022_0550.md。
原作EXE出典SHA（保存Stage17資料記載、今回原本再計算なし）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。CURRENT指標V3、旧10/21 DBは新正本に使用しない。
## 本回の横断照合
Stage17保存ASMは0x492960でmode2相当書込、0x49296Aで[ESI+0x1EEC44]=1を設定し、その後0x492A4E/5B/68に間接CALL(FF D0)が並ぶ。関数内の静的先後関係であり、合法原作の同一実行で3件とも実際に完了した観測ではない。
Stage17の8 RAWアーカイブはすべてGameEvent_slot=0、first_Unit_slot=98だがfirst_native_pass_observed=false。後続tickのslot配置を最初のtickと同一視しない。
同資料は普通のWarでもScriptBattle/VMを経由し得ると明記。ScriptBattleオブジェクト存在だけで脚本専用戦闘と分類しない。
Stage17検証16/16 PASSはSTATIC_ARCHIVE_EVIDENCE_ONLY、user_new_success_report=REPORTED_NOT_YET_CORROBORATED、full_G1=false、external_roundtrip=false。過去8 RAWを新しい完了Goldenとして加算しない。
## T020負例受入ゲート（試験設計のみ）
ACT-01: active=1 snapshotだけでside callback完了/実名簿確定を主張 => VERIFY_INCOMPLETE。
ACT-02: 0x492A4E/5B/68が静的に存在するだけで実行済/3side参加を主張 => VERIFY_STATIC_ONLY。
ACT-03: archived first_Unit_slot=98を初回Task passの順序として転用 => BLOCK_UNSUPPORTED_FIRST_PASS。
ACT-04: ScriptBattle RTTI存在を脚本専用戦闘とする => BLOCK_UNSUPPORTED_CLASSIFICATION。
ACT-05: 0x433E58→0x492890が戻ったことだけで以降の同Task passのUnit更新が無いと主張 => VERIFY_TIMING。
ACT-06: 同PIDでも別watch時間窓のSAVE/名簿を接合 => REJECT_CROSS_WINDOW。
ACT-07: Stage17 static PASS/ユーザー成功報告のみをactual Golden/strict MATCHに計上 => BLOCK_PROOF_PROMOTION。
合格に必要な新証拠: 合法旧UI操作と攻防Spot、同戦闘直前SAVE bytes/SHAと入力時刻、active前後の同窓一次記録、side callback完了と実MAP/3side/ordered deployed Unit・Troop、G3終了とG4 World差分、new buildの対応入力と実出力。
## 継続状態
新規Gameplay DYNAMIC OBSERVED 0、actual Golden PASS 0、strict MATCH 0。T020上記fixture実行0、原本バイト再検査0、E新READY統合0。
T019: GameClear DAT13/TXT2は字句検索scopeのみRESOLVED、script2同名winner/phase実効/TXT runtime/gwrite復帰はVERIFY、原作新確定矛盾0。
MASTER cp196/READY596=A115/B229/C136/D116、34 Task DONE9/IN_PROGRESS21/VERIFY4は前回確認値（再計数無し）。過去OFFLINE-UNSYNCED暫定26は未照合、今回の研究をPC正式READYへ算入しない。
安全境界: 12:47 T020 V3 dispatchノートと12:49 MASTER復旧追記の拒否操作、旧T018表境界/C T026/T032/D T030/0x5710C0等は別BLOCKED据置。同一拒否を再実行・別tool/path/shell/Remote/ZIP迂回しない。
次: Stage17と旧watch2の日時/初期状態を一致させる一次receiptの有無をread-only調査。原本EXE/ZIP/SAVE、他owner、REA、dev_lab、Git/Work/設定/automationは無変更。