# 迫真戦記 新E｜T020/T028 メッセージ→共通dialog処理の静的出典照合

- 研究ID：`E-OFFLINE-20261028-1645-T020-T028-DIALOG-ROUTE-PROVENANCE-01`
- 時点：2026-10-28 16:45 JST／所有者E（T020回帰、T018受入条件、T019矛盾分類のみ）
- 分類：`OFFLINE-UNSYNCED / STATIC INDEX VERIFIED / SYNTHETIC EXECUTED / VERIFY / ORIGINAL GAME NOT RUN / NOT READY`
- 成果：B15で報告された「放浪／傭兵」2つのメッセージ経路が同じ `0x0052CF50` を呼び、その共通関数から `0x0043F470` の `dialog` 系構築処理へ進む、**直接CALLによる静的連鎖**を旧検索DBで独立照合した。実画面表示、所属変更、死亡・放浪・傭兵化の実効状態を証明したわけではない。

## 出典・境界

- Desktop Commander Local Compactを第一優先で試みた。`list_directory`（PC研究ルート）と `read_file`（研究規約）ともに `INVALID_ARGUMENT / McpServerError: Session terminated`。これは**CONNECTION**であり、禁止された操作の安全拒否ではない。PC自体のオンライン状態は未確認。新規安全拒否なし。
- 復旧ID：`E-RC-20261028-1645-LOCAL-SESSION-TERMINATED-01`。保存済み：この文書と比較JSON、Pythonテスト。未保存：WindowsのE所有資料とMASTERへの反映、最新A～D/REA確認。影響：READY正式統合と最新34 Task確認不可。次の許可された行為：接続が正常化した際、前回安全拒否箇所を避けつつ許可されたE資料と必要なHANDOFFを確認してから、所有権・重複・source hash・READYを再照合する。
- ChatGPT Libraryの `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を正規に取得し、原本ZIPを改変せず一時領域へ `search.sqlite` と `search.py` のみコピー、`mode=ro&immutable=1` で参照。
- ZIP SHA256（今回実測）：`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。34エントリを列挙。
- SQLite SHA256（今回実測）：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、`PRAGMA quick_check=ok`。
- 対象EXE SHA256（2026-10-21 `BUILD_MANIFEST.json` 期待値）：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。**今回原作EXE現物のハッシュを再計算していない**。
- 今回参照したGhidra擬似Cは旧10/21スナップショットであり、原作者のソースコードでも現在PCの最新解析でもない。2026-10-28 B15研究の存在とそのメッセージ条件は**前回会話報告を継承**。B15研究ファイル自体は今回PCから独立読み戻しできていない。

## 独立照合したCALL site

| 呼び出し元 | CALL site | 直接呼び出し先 | 観測種別 |
|---|---|---|---|
| `0x00497BB0` | `0x004989BA` | `0x00436BC0` | B15放浪テンプレート近傍の文字列処理経路 |
| `0x00497BB0` | `0x004989E7` | `0x0052CF50` | 後続の共通処理 |
| `0x00497BB0` | `0x00498C67` | `0x00436BC0` | B15傭兵テンプレート近傍の文字列処理経路 |
| `0x00497BB0` | `0x00498C95` | `0x0052CF50` | 後続の共通処理 |
| `0x0052CF50` | `0x0052D047` | `0x0043F470` | 共通処理内の直接CALL |
| `0x0043F470` | `0x0043F72F` | `0x00416E80` | `"dialog"`処理付近 |
| `0x0043F470` | `0x0043F73F` | `0x00416B90` | `"dialog"`処理付近 |
| `0x004051D0` | `0x004051E8` | `0x00402710` | 別系統の文字列バッファ処理 |

- `0x0052CF50` は索引上、**21種類のcaller・計39箇所の直接CALL**から使用される。`0x00497BB0` からは **8箇所**。したがってこの関数を「放浪専用」「傭兵化専用」の状態遷移関数と呼ぶ根拠はない。
- 擬似C `0x0052CF50` は `FUN_0052ad90()`、複数の文字列コピー `FUN_00402710`、`FUN_0043f470()` 等を呼ぶ。共通処理にUI系の副作用があり得るが、どの画面表示が実際に起きるか、どの条件で実行されるかは**DYNAMIC未観測**。
- 擬似C `0x0043F470` は `"dialog"` と `"decide11"` の両文字列を使用。`"decide11"` は引数条件に応じた**デフォルト文字列経路**にあり、B14の `decide11` 選択と数値10／25の因果や同一インスタンスを意味しない。終端でvtable経由の間接CALL候補があるが**静的に実体を確定しない**。
- `0x004051D0` は `+0x14/+0x10` を調整して `0x00402710` を呼ぶ短い処理。メッセージ後に隣接するからといって、ユニットのゲーム内寿命・所属変化を決める破棄関数とは扱わない。

## T020の実施・受入ゲート

- 保存物：`T020_T028_DIALOG_ROUTE_CASES_20261028_1645.json`（直接CALL 8件、誤接続の負例4件、Golden不適格の負例8件）。
- 実行コード：`t020_dialog_route_provenance_gate_20261028_1645.py`。読み取り専用の旧SQLiteに対し、source SHA、DB整合性、CALL site、fan-in、擬似C内文字列とGoldenの負例を検証。
- 結果：**28/28 PASS**、終了コード0。これは**STATIC INDEX + SYNTHETIC NEGATIVE**の検証であり、実ゲームの互換PASSではない。
- `0x4989BA`・`0x498C67` の文字列処理到達と `0x4989E7`・`0x498C95` の共通dialog系CALLを結び付けても、原作画面での「放浪」「傭兵化」表示、ユニット所属変更、World状態の変化を同時に証明したことにはならない。
- B13の14件比較fixtureは未実行のまま保持。B14/B15等の別版テスト成功値は今回の28件に合算しない。

## T018 Golden（合法旧原作G0/G1/G2）

- 2026-10-21 ZIPの `research_snapshot/tests/T018_GOLDEN_CORPUS.md` 旧1473–1478行の契約を読取。`sci1`, `po2/sp2→sp16` は**原作script側の候補**であり、実際の選択MAPや3sideを静的に確定しない。
- G0：未改変原作の合法UI操作→同一runの戦闘開始。G1：その戦闘直前SAVE生バイト/SHA＋旧EXE識別・入力時刻/ハッシュ。G2：同一戦闘の実MAPバイト/SHA、攻撃・防御・支援3陣営、実際に出撃したordered Troop/Unitと配置。
- G3：戦闘結果、G4：戦略World差分も現時点で未採取。メッセージ文字列の静的経路・文字列ウィンドウ構築はG3/G4を代替しない。
- 今回新規 **DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0**。G0/G1/G2は`NOT RUN`、実機比較は`NOT READY`。

## T019、MASTER、拒否継承

- T019の新規**確定矛盾=0**。今回の`decide11`同名文字列は意味・入力文脈の同一性を未検証なので **VERIFY、矛盾として登録しない**。
- GameClearのDAT13箇所/TXT2箇所の検索範囲差RESOLVED、`script2`優先順位・phase flag・TXT実読込・`gwrite`復帰VERIFYは**前回報告値を継承**。今回は最新T019ファイル再読込なし。
- MASTER最終既知**checkpoint196 / READY596（A115/B229/C136/D116）**、34 Task **DONE9 / IN_PROGRESS21 / VERIFY4 / 重複0**。すべて**2026-10-28 12時台までの旧確認値**であり、現在のMASTER最新値ではない。今回正式READY統合**0件、IDなし**。所有者・READY・競合の最新チェック未実施。
- 2026-10-28 13時台の`E-RC-20261028-1353-READONLY-PS-SAFETY-01`および`E-RC-20261028-13H-E13-REPORT-APPEND-SAFETY-02`は継続BLOCKED。拒否操作を別shell/tool/path/ZIPで再試行していない。旧T018表境界、T019拒否済みXREF、C T026/T032、D T030 TSV、`0x5710C0`等もBLOCKED継続。
- 2026-10-25 OFFLINE-UNSYNCEDと他レーンとの完全意味重複照合は未完了。今回Windows PCへの同期は**未実施**。Git/push、A～D、REA、dev_lab、原本EXE・ZIP・SAVE、設定、スケジュール、Workへの変更なし。

## 次の優先箇所

1. Eの追加解析候補：`0x0043F470`で組み立てられる「dialog」の実パラメータと登録結果を静的に区別し、B14 `decide11`の10/25と同一視する誤実装を防止。T019は新規矛盾とせずVERIFY。
2. E最優先：合法原作の**同一戦闘G0→G1→G2**を一次証拠でひも付け、G3/G4の画面観測と実World差分まで採取する。実機観測までactual Goldenとstrict MATCHを0維持。
3. PC接続復帰後、現行E所有資料と最新HANDOFF、owner/重複/READYを照合し、同一ID既統合と10/25未同期との競合がないものだけ一度正式反映する。安全拒否された操作は対象外のまま保持。
