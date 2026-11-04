# E-AUDIT-20261024-08H-T018-T020-DAT-MUTATION-EPOCH-01｜X20試験DATの時相と原作Golden適格性
Owner E / T018,T020。2026-10-24 08時台 JST。分類 STATIC_AUDIT_OF_SAVED_DYNAMIC_EVIDENCE + CURRENT_BYTE_CHECK / VERIFY / NOT READY。新規Gameplay NOT RUN。
## 原作G0とX20改変の時系列
- 既存REA原作G0 first_active=2026-10-21T14:31:37.765392+00:00（JST 2026-10-21 23:31:37）。PID23272。既存G0報告 source EXE SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。Spot実ID/Map/名簿は未確定。
- X20 manifest applied_at=2026-10-22T02:49:40.662779+09:00、restored_at=2026-10-22T04:46:19.660325+09:00、現status=RESTORED。G0 first_activeはX20実適用より前で、同じX20変更が当該G0 runを汚染したとの推論は時系列に反する。
- X20適用～復元の時間帯に採取した原作観測を無改変DAT Goldenへ流用しない。別ゲーム起動・既存プロセスのDATキャッシュ等は確認しておらず、時刻だけで汚染/無汚染を一般化しない。
## 今回独立したread-only実バイト検査
- source: data/KARATE_X20_20261022/manifest.json; 実バイトSHA256 85B418A60F9D2873CADE38E05574C70A0D969E3B3E274842111087BE9F2FC412。
- 原作G0 report: rea_lab/headless_analysis/search_index/BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json; 実バイトSHA256 87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C。
- manifest.changed_files 8件の現存DATを直接SHA256計算。8/8が変更前before_sha256と一致、0/8がX20適用後after_sha256と一致。ゲーム直下TEST_MOD_KARATE_X20_ACTIVE.mdも不存在。現時点のX20変更8件について復元状態と整合する。
- 追加でmanifest.all_dat_before全591件の現物DAT SHA256を読み取り専用照合：591/591一致、missing0、modified0。現時点でこのsnapshotに含まれるscript DATのbyte一致は確認済み。ただしmanifest作成時のbaselineが配布初版と同一である証明や、当時G0プロセスが読み込んだ全DAT・SAVE・MAPの直接receiptにはならない。EXE SHA一致だけもDAT同一性の証拠にはならない。
## T018/T019/T020受入の変更点
- G0: 原作native mode2/active1は既保存観測であり、合法旧UIの元Spot/対象Spot実IDとの完全receiptは未充足。G1: 同run直前SAVE bytes/SHAと入力履歴未取得。G2: 実MAP/攻撃・防御・支援/ordered Unit・Troop未取得。G3/G4: 戦略復帰観測はあるが勝敗・World差分未取得。
- DAT provenance gate: observation epochとDAT改変時間帯を区別し、実DATセットのbyte/SHA receiptを要求。X20事前G0とX20適用中の別runを同一の無改変Goldenに統合しない。
- T019新規原作仕様矛盾0。RESULT.mdの適用記録とmanifestの現RESTOREDは時点差（旧結果文書は歴史的記録）であり矛盾確定しない。GameClear DAT13/TXT2検索範囲差RESOLVED、script2勝者/phase flag/TXT runtime/gwrite復帰VERIFY維持。
- 新規T020 fixtureは7/7 SYNTHETIC PASS。PC read-only実データは変更8DAT before hash 8/8一致、全591 script DAT before hash 591/591一致・欠落0・差分0。旧原作Gameplay新実行0、新規E DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
## 保存・重複/権限
- tests/t020_dat_restore_epoch_gate_20261024_08H.py SHA256 26A551A40AE05D29CB066E21039E8AD9C3C080646D0F23073FC06590B2EA9C7A。
- tests/T020_DAT_RESTORE_EPOCH_CASES_20261024_08H.json SHA256 2D226F1DBBE1DC75BB3B6BE1D9D04D54696C2AF053B5B31FD66B02EE01B56771。
- MASTER最後の正式checkpoint196/READY596=A115/B229/C136/D116（旧確認値）。34 Task DONE9/IN_PROGRESS21/VERIFY4（旧値、全再集計なし）。新READY正式統合0。旧OFFLINE-UNSYNCED暫定26件は未照合・未正式同期。
- 旧安全拒否T018表境界、E旧拒否一式、C T026/T032、D T030 TSV、REA VA0x5710C0はBLOCKED維持・再試行/迂回0。原本EXE/DAT/ZIP/SAVE、他owner/REA/dev_lab/Git/Work/自動化は書込・変更なし。
- NEXT: C-NB02合法旧UIのSpot実ID付きG0・同run直前SAVE bytes/SHA+入力G1・確定MAP/三陣営/出撃Unit/Troop G2を新採取し、DAT hashと採取時点を結び付ける。Eはsource manifest/epoch/実byteを審査し、他レーン採取器には手を加えない。
