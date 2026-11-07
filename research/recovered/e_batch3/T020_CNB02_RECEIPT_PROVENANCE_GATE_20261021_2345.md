# T018/T020｜C-NB02 出典・時相・出撃名簿証拠ゲート
ID: E-AUDIT-20261021-2345-CNB02-RECEIPT-PROVENANCE-GATE-01
分類: E所有・STATIC / SYNTHETIC / NOT READY / OLD GAMEPLAY NOT RUN。
原作EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（既存search_index manifest値、今回バイト再計算なし）。
## 既存E受入器との差分
既存 tests/t020_battle_return_commit_gate_20261021_2147.py は old_hashes/captures に "present" を入れても型上は合格し得る。これは合成shape設計用でバグ確定ではないが、実測Goldへ昇格させる場合の証拠ゲートとして不十分。
独立した tests/t020_cnb02_receipt_provenance_gate_20261021_2345.py を追加し、既存2147コードは変更しない。
全source hash・stage capture hashは64桁hex、EXE SHAは許可されたv0.67に一致が必要。文字列"present"やSTATICのみの観測を拒否。
G0 UI entrance、G1 戦闘直前SAVE+入力は厳密な相互順序を固定しない（入口確認とSAVE採取は前後し得る）。ただし両者はG2実配置より前、G2<=G3戦闘終了直前<G4戦略復帰の順序が必要。
全G0-G4は同一run IDと別stage capture証拠を保持し、G2には可視MAPと攻防支援3side（支援無しは空配列）・順序付きUnit/Troop識別を要求。
二重commitを拒否し、new build/capture不足はNO_STRICT_COMPARISON、合成で全欄充足でもSYNTHETIC_SCHEMA_ONLYとする。
## 証明できないこと
SHA形状が正しくても対象ファイルの存在・バイト一致・合法原作での収録自体は自動証明できない。schema判定ELIGIBLE_FOR_REVIEW_NOT_MATCHはGameplay PASSでもstrict MATCHでもない。
旧原作C-NB02合法sci1/po2/sp2→sp16のG0/G1/G2、終了G3/G4はNOT RUN。原作DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
出撃名簿がUIから全部見えない場合はINELIGIBLE/VERIFYに留め、保存参照・STATIC関数から埋めない。G3/G4の実結果やEXE→新実装1:1差分も未検証。
## 参照・保護
根拠: E既存tests/T020_BATTLE_RETURN_COMMIT_GATE_20261021_2147.md と同py、tests/T018_GOLDEN_CORPUS.md、MASTER cp195、A/B/C静的参照は従来既証拠のみ。
旧安全拒否のT018表境界・GameClear修正assert・部分JSON・22:52 flag XREFは再試行しない。原本/A-D/REA/dev_lab/Git/Work/設定/scheduleは変更しない。
