> Private E-owner 02H historical research, PC original `tests/T020_E23_TYPED_G2_CROSS_CONTRACT_AUDIT_20261029_02H.md` measured SHA-256 `0674BDEEFA3F9669FEDE7906F538DAFC1943354FB118A4023E7A803579E02AF4` on 2026-11-02 JST. Safety-sanitized rather than exact-byte publication. Earlier synthetic 117/117 is historic, **not rerun now**. Original gameplay Golden PASS 0, strict MATCH 0, formal new READY 0, NOT_CURATED.

# 迫真戦記 新E｜型厳密G2投影と三陣営・出撃対応の合成クロスゲート（2026-10-29 02H）
研究ID: E-AUDIT-20261029-02H-T018-T020-TYPED-G2-CROSS-CONTRACT-01
Owner: E/T018/T020（T019参照）。Status: PC LOCAL / STATIC CODE CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READY。

## 出典と既存成果の継承
- Windows Desktop Commander Local CompactでMASTER末尾、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA PROGRESS、dev_lab IMPLEMENTATION_PLAN、E T018/T019/T020をread-only照合。
- 基準はE所有 tests/t020_e23_typed_projection_gate_20261029_01H.py（SHA256 73182ABD6C920B37BA7FD5F522657633C949ABD0F83FD37A57CECFC2D90909A8）と tests/t020_e21_g2_schema_bridge_gate_20261028_22H.py（SHA256 F64B8D6D67FAC6067A54860ECD3493F69E6B4270E63FACDA1E3CED6A7F3FC3F4）。
- 旧EXEの2026-10-21 manifest SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187を引継ぎ。今回原本EXE再ハッシュ・新Ghidra解析はNOT RUN。
- E21の実fixtureバイトはWindowsへ正式同期しておらず、今回のテストは01H specimen由来の合成dataに限定する。

## 新しい一対一照合結果
- 01H型厳密gateはG2文字列・数値型およびsource SHAを検査するが、三陣営のrole/side ID一意性、攻防各出撃receipt、出撃順序の連続性、宣言外フィールドを同時には検査しない。
- 再現: 01H specimenに攻撃側出撃のみ存在する場合、01H strict_bindは SYNTHETIC_TYPED_PROJECTION_BOUND_NOT_NATIVE を返す。しかし、22H E所有bridgeは NO_DEFENSE_ROSTER_RECEIPT を報告する。
- 今回の独立Eゲートは01H typed SHA+JSON+run検査に続き、合成v1正確なfield set、3 role(attack/defend/support)一意・side ID一意、所属先存在、攻防の各出撃、0..N-1の順序、未知のnative確認フィールド不採用を検査。
- supportの出撃がゼロでもschema-onlyで拒否せず、defend→defenseは検査専用aliasであり旧原作native意味の同一性は未確認。Unit/Troop名を一意のnative instance IDと誤認しない。
- MAP IDの一次証拠、active-enter/exit、実際のMAP bytes、合法UI・直前SAVE/input、同一runの外部witnessがないため、全件で原作Golden/strict MATCH認定を禁止する。
- 合成サンプルの攻撃・防御roster追加で SYNTHETIC_G2_CROSS_CONTRACT_CONSISTENT_NOT_NATIVE。これは「合成内部の契約整合」に限り、original gameplay proofではない。

## T020回帰
- 新規 tests/t020_e23_typed_g2_cross_contract_20261029_02H.py をE所有testsに追加、25/25 PASS（Python -B unittest、0.012秒）。
- Prior protected or refused source/operations remain SAFETY_HOLD, not retrieved or retransmitted.
- 新コードSHA256=1E7F28E49BDE27C7E8B371D8824321F1A41D0A2560D8CA042FA00A9D5AF4FB90（実PC bytes）。
- 旧T018/T020検証器、既存合成fixture、MASTER、他owner成果は修正していない。

## T018/T019・統合境界
- C-NB02合法旧UI G0開戦、G1同一run直前未改変SAVE bytes/SHA＋入力、G2真のMAP ID/bytes・攻防支援side・ordered deployed Unit/Troop・active window、G3可視戦闘結果、G4戦略World差分は同一runの一次証拠未充足。
- 今回の旧原作DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0、新規正式READY統合ID=なし。
- T019新規確定原作矛盾0。既存GameClear DAT13/TXT2 source-scope差RESOLVED、script2同名winner/phase flag/TXT実読込/gwrite復帰/decide11用途VERIFY。
- MASTER最終公式checkpoint196・READY596（A115 B229 C136 D116）を末尾から確認。34Task DONE9/IN_PROGRESS21/VERIFY4と全ID重複なしは旧確認値であり、今回全件再集計はNOT RUN。
- 10/25以降OFFLINE-UNSYNCED、E21原fixtureのPC bytes、他ownerとの意味重複・READY/合意照合は未完了。今回の結果はNOT READY、正式MASTERへ昇格しない。
- Prior protected or refused source/operations remain SAFETY_HOLD, not retrieved or retransmitted.
- Prior protected or refused source/operations remain SAFETY_HOLD, not retrieved or retransmitted.
- 次はE21実bytesを正規経路で照合できる時だけsource pinとG2診断を再接続。優先順位は同一合法原作G0/G1/G2一次証拠の取得と、旧T018 runnerの非破壊的受入結線。
