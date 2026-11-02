# PRIVATE E/T018–T020: sanitized historical 2026-10-24 07H source

Existing study ID `E-AUDIT-20261024-07H-T018-T020-WAR-ANCHOR-EPOCH-01`. Original E source `tests/T020_WAR_ANCHOR_EPOCH_AUDIT_20261024_07H.md`, source raw SHA-256 `ABA10728EE4AE890F23D4EBB769BF7FF755CDF7DFFA1EADF7D3A088B6E001FEF`, verified from authorized PC on 2026-11-02. The refusal-scope metadata line is redacted, so this copy is not raw-byte-identical. REA-owner native watcher is a **read-only cited source** (not republished). Historic 10/10 synthetic and watcher SHA findings below are past-run receipts, **not current reruns**. `PUBLISHED_INTAKE / NOT_CURATED / VERIFY` only: native gameplay Golden PASS 0, strict MATCH 0, new READY 0; neither post-battle pointer nor attack_count establishes original G2/G4. Companion PC-only-watcher-dependent Python and fixture: [`repro/t020_war_anchor_epoch_gate_20261024_07H.py`](repro/t020_war_anchor_epoch_gate_20261024_07H.py), [`repro/T020_WAR_ANCHOR_EPOCH_CASES_20261024_07H.json`](repro/T020_WAR_ANCHOR_EPOCH_CASES_20261024_07H.json).

---

# E-AUDIT-20261024-07H-T018-T020-WAR-ANCHOR-EPOCH-01｜戦闘前の候補揺動と終了後の残存ポインタ
Owner: E / T018,T020。分類: STATIC_AUDIT_OF_SAVED_DYNAMIC_EVIDENCE / NOT READY / New Gameplay NOT RUN。
## 出典（read-only）
- REA保存原作watch: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl
- JSONL SHA256: 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7
- 観測EXE SHA256（既保存READYの申告値、今回原本再ハッシュなし）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- REA既保存G0報告/READYとE-06Hの監査を継承。新原作起動なし。PID 23272、実ログ234行。
## 新たに抽出したEの受入境界
- mode1/active0からmode2への移行前、`attack_count` は0,1,2,3の4種類。`battlefield_ptr` はNULLを含め20種類。
- 戦闘開始直前には ptr=0x41675048 / attack_count=2 が観測されたが、それ以前のmode1では候補ポインタと件数が頻繁に変化。数値やポインタを単独のbattle_idにしてはいけない。
- mode2最初のactive0は2026-10-21T14:31:34.951083Z、active1は14:31:37.765392Z、active0は14:33:34.325867Z、mode1復帰は14:33:35.933687Z。
- mode2/active1の保存イベント全件で ptr=0x41675048 / count=2 は一定。ただしptrが同じことはMAPやrosterの実取得・戦闘IDの同定ではない。
- mode1復帰後も既保存watch期間の`battlefield_ptr=0x41675048`・`attack_count=2`は維持される。非NULL ptrやcount>0を戦闘active/G3 outcome/G4 commitと誤認しない。
- SnapshotError `unexpected nil tree node` の28試行は連番1..28で、active1化直後0.001秒〜約12.373秒の短窓に集中。watch自体は900秒まで継続、完成packet保存数0。
- 28件の失敗を『active期間116.56秒に均等に継続して失敗した』とは言えない。これが次回C/REA所有採取器の改善検討向け新規差分。
## T018 / T019 / T020判定
- E_G0: REA旧原作native active遷移は既観測。合法UIのSpot実ID/操作結合が不足しE完全受入は未充足。
- E_G1: 同run戦闘直前SAVEバイトSHA/操作入力receipt未取得。前段ptr一致・attack_count一致を代用しない。
- E_G2: 原作MAP・攻防支援3side・ordered deployed Troop/Unitは未取得。nil decoder失敗から復元値を捏造しない。
- E_G3/G4: active0とmode1復帰は観測。勝敗/World変化/一度だけcommitを断定しない。
- T019新しい原作仕様矛盾0。GameClear DAT13+TXT2検索範囲差RESOLVED、script2/flag/TXTロード/gwrite復帰VERIFY据置。
- T020: 新たなanchor誤用負例を独立fixtureにし、原作ログSHAと状態時系列を検証。fixturesはSYNTHETICでGAMEPLAY PASSと混同しない。
## 安全・再開
- E専用の新規文書/fixture/checkerのみ作成。A-D/REA/dev_lab/原本EXE・DAT・ZIP・SAVE/Work/Git/設定/他automation変更なし。
- 旧安全拒否はBLOCKEDのままであり、拒否対象の内容や保護範囲は本保存コピーに再掲しない。
- 旧正式checkpoint196/READY596(A115/B229/C136/D116)、34 Task DONE9/IN_PROGRESS21/VERIFY4は前回確認値で今回未再集計。新規READY0。
- E新規DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。OFFLINE-UNSYNCED暫定26件は正式重複照合前・未同期。
- 次は合法UI G0→同戦闘直前SAVE+input G1→終了時点の実MAP/三side/ordered roster G2の同run一次receipt。C/REAが採取器を直す場合は失敗タイミングと再試行間隔を別ownerへread-onlyで共有。

## 07時台検証の実行receipt
- Local Compact `python -B tests/t020_war_anchor_epoch_gate_20261024_07H.py` 実行成功：原作ログSHA PASS、STATE_CHANGE25、PRE候補count4種類/ptr20種類、MODE2全28、ACTIVE24、POST103、失敗試行28連番をassertで確認。
- T020独立のanchor誤受入防止合成fixture 10/10 PASS（原作実戦10回ではない）。G0 native observedは旧1run、E新DYNAMIC OBSERVED0／actual Golden PASS0／strict MATCH0。
- PC保存と直接readback 3/3成功。fixture SHA256=2413262032B320D7E930E190BE6450D5EAA0823DFF8D1B8A40B3C8E103C1AC19、checker SHA256=5E8E54EF219692D19058C27624EDF3D77711BD5C7D945809DB70A71DCAAA39E8。
- REA進捗ファイルの旧想定path `rea_lab/PROGRESS.md` はENOENT（OTHER、read-only参照失敗、書込0）。`rea_lab/README.md` と既保存REA watch/G0報告を利用し、接続障害・安全拒否ではない。新安全拒否0。
