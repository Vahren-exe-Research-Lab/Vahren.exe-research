> Historical E-owner report, sanitized for private intake. PC original: `tests/T020_E_DAT_SNAPSHOT_CHRONOLOGY_AUDIT_20261029_11H.md`; original SHA-256 `DE1312A0F4998DE89B4AACFBB003E739796D900F3B68DC0E9BDBCF65E70C63DF` verified 2026-11-02. Safety-refusal targets redacted; original-byte equality NOT claimed. Existing study, STATIC/SYNTHETIC/VERIFY and NOT_CURATED; historical case counts not rerun, original-game Golden NOT RUN, formal READY NOT PROVEN.

# 迫真戦記 E｜旧原作観測とpre-X20 DAT snapshotの時相・研究用追加DATの初期存在監査（2026-10-29 11H）
研究ID: E-AUDIT-20261029-11H-T018-T020-DAT-SNAPSHOT-CHRONOLOGY-01
Owner: E/T018,T020（T019は出典時相の検討のみ）。状態: PC LOCAL / STATIC SOURCE CHRONOLOGY / VERIFY / NOT READY。

## 出典・独立確認
- Windows Local CompactでMASTER末尾、解析規約とA-D HANDOFF、REA decomp_task/PROGRESS、dev_lab実装計画、T018/T019、E09H/10H、search_index README・BUILD_MANIFESTを読取。
- pre-X20 原記録 data/KARATE_X20_20261022/manifest.json：実バイトSHA256=85B418A60F9D2873CADE38E05574C70A0D969E3B3E274842111087BE9F2FC412、内部created=2026-10-22T02:49:40.102405+09:00、Windows file created=2026-10-21T17:49:40.601Z。
- pre-X20 manifestには591 DATが登録され、その中に6000_スキルテスト/work_observation.dat（記載SHA256=64E1796E9FD8BC04C67A5B21A3BD79B58EBAF70E9D3858E41868755AD6807228）が既に含まれることをPython -B read-onlyで確認した。
- 2026-10-24 21H旧Eの実ファイル監査は591/591一致。2026-10-29 10H receipt実バイトSHA256=363A660795172DC61D4A3006D9AE7255E55DE0CF29763889FB601B5BD80D03FFは590一致/欠落1/差異0で、同一のwork_observation.datが欠落。
- 元の591→現在590の差は研究用追加DATの存否。現在の590セットは旧10/25に記録された『追加を除く590セット』と集合SHA一致。ただし旧配布ZIP原本の真正性、旧プロセスが読み込んだDAT世代は未証明。

## 新規の時相クロスウォーク（既研究の実バイト記録を使用、ゲームの新規起動なし）
- 10/21 G0報告はPID23272、最初のnative mode2 active UTC14:31:37.765392Z（資料自身SHA256=87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C）。旧E05:50で同一PIDの15:14:40.580007Z第二戦闘窓を区別済み。双方を単一runと合体させない。
- BATTLE_USER実機3run（PID13620/28432/32468）のSUMMARY末尾は各15:48:52.275807Z、16:32:49.548884Z、16:47:33.709049Z。旧3runの非原子的RAW8・失敗5は構造補助証拠であり、E原作Golden観測数ではない。
- 10/22 02:49 JSTのpre-X20 manifest creationは10/21 UTC17:49Zであり、上記最後の16:47:33Z SUMMARYより約1時間2分後。X20テスト改変がこれら10/21の先行観測を遡及汚染したとは認定しない。しかしmanifestの後日snapshotは当該runのloaded DAT bytesを遡及証明できない。
- 追加work_observation.datのSHAは10/22 02:49作成記録に含まれる。『10/25に初めて追加された』という作成日認定は支持されない。10/25は少なくとも観測・記録済み時点であり、追加の実際の初回作成日時はUNKNOWN。
- pre-X20という呼称は『空手20倍変更前』だけを指し、配布元official-release-pure DATを証明しない。追加DATのsource origin・当時のプロセス再読込・入手元ZIP同一性は別途VERIFY。
- 10/21 auto.savについてA= C09C098C...（mtime12:18Z）とB=EA0D5CC6...（同名同長5953848B）の異SHAは既E04:50で確認済み、今回も同一run直前SAVEへ昇格しない。

## 受入fixture・回帰・非昇格
- 新E独立fixture tests/T020_E_DAT_SNAPSHOT_CHRONOLOGY_FIXTURES_20261029_11H.json：6ケース、source SHAと日時の境界を記録した設計資料。ゲーム・新fixture自身の動作テストはNOT RUN。旧拒否済session joinコードの再実装ではない。
- 既存E 10H source-epoch gate 12/12 PASS、09H native-CNB02 preflight 22/22 PASSをPython -Bで再実行。合計34/34 PASS、いずれも旧E合成テストであり新テスト数0、original Gameplay PASS0。
- Golden合法観測に必要なのは同一実戦闘のG0合法UI、G1直前SAVE実bytes/SHA・入力、G2実選択MAP/3side/ordered Unit/Troopとactive window、G3結果、G4戦略World前後差分。現行DAT集合とEXE manifest SHAが一致するだけではstrict MATCH資格なし。
- T019新規確定Wiki/DAT/EXE矛盾0。GameClear DAT13/TXT2字句scope差RESOLVED、script2 winner/phase flag/TXT実読込/gwrite復帰/decide11用途はVERIFY。今回の『10/25追加』作成日ラベルへの注意は研究資料の出典時相であり原作バグではない。

## 正本状態・安全・引継ぎ
- MASTER最後の公式checkpoint196、READY596=A115/B229/C136/D116。34 Task DONE9/IN_PROGRESS21/VERIFY4は旧値であり全件再計算NOT RUN。新READY統合IDなし、MASTER書込0。
- 原作DYNAMIC OBSERVED0／actual Golden PASS0／strict MATCH0。B 11H T013研究はSTATIC/VERIFY/NOT READYで代理READY統合なし。
- [SAFETY_HOLD] 過去の拒否対象・経路は本収録の範囲外。拒否カテゴリのみ保全し、再試行・迂回は行わない。
- 新規安全拒否0・接続障害0。SHA取得用の最初のpython -cはPowerShell/JSON quotingでSyntaxError（OTHER/RECOVERED、書込0）。通常Get-FileHash read-onlyで7資料のSHA取得を完了。
- 保全済みLibrary原本23件とPC旧133件の旧成果を破棄・上書きせず、旧OFFLINE-UNSYNCED全意味重複照合は未完。原作DAT/EXE/SAVE/ZIP、A-D/REA/dev_lab、Git/Work、設定、automationは変更しない。
- 次: 旧合法原作のG0-G2が同run・同DAT loaded epoch・同SAVE/input/MAP/ordered rosterに結合できる一次資料を優先。受領できない場合はVERIFY/NOT RUN、静的後日snapshotから補完推測しない。