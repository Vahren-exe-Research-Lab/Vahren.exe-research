# 迫真戦記 新B｜T013 支援候補24Bレコードのバイト出自別検証（13時台・オフライン）

- **RECOVERY-ID**: `B-RC-OFFLINE-20261020-1313-LOCAL-SESSION-01`
- **研究候補ID**: `B-OFFLINE-20261020-1313-01`（正式B証拠IDではない）
- **OWNER/TASK**: B / T013。T012の支援判定は参照のみ。
- **分類**: `STATIC-RECHECK × NEW TEST FIXTURE / DESIGN-SYNTHETIC / OFFLINE-UNSYNCED / NOT READY`
- **PC接続**: 最初のLocal `MASTER_LEDGER.md`末尾120行read_fileは成功（4484行と表示、末尾資料の一部のみ取得）。その後、解析規約の取得ではtimeout/`McpServerError: Session terminated`、追加の規約再読でも同接続失敗。**TASK QUEUE・最新版規約・B HANDOFF・担当5資料の必須一式を確認できていないため、PC書込はゼロ。** 接続障害であり安全拒否ではない。Remote/Work未使用。
- **旧最新版の取扱い**: 10時台の会話報告はcheckpoint194、Library `/MASTER_LEDGER.md`は2026-10-18 16:59 UTC・checkpoint187。今回の一部末尾表示だけで最新checkpoint/既存証拠ID重複を確定しない。
- **回収出典**: Library `/迫真戦記再開発プロジェクト/data/T011_T012_T013_T024_T028_UNSYNCED_RECOVERY_REGISTER_20261020.md`、同`OFFLINE_RECOVERY_INDEX_20261020_1117.md`、前回`GOLDEN_ADMISSIBILITY_AND_RECOVERY_20261020_1214.md`。未同期の10/19～10/20研究候補22件・安全拒否メタデータ8件は既索引を参照し、再採番/再READY化しない。

## 保存済みREAへの限定静的照合（既存結果の再確認）

- 入力は**REA出力の既存保存物** Library `/decomp_task.zip`（updated 2026-10-18 17:01 UTC、SHA256 `e1ecf0b9c9a315df3eae39bc88399b54150ed0622baee813d945d31f7d2442cb`）。保存JSONが記載する対象EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。原本EXE/ZIPは実行・変更・再hashしていない。
- `runs/20261011T112315808Z/514F10_procedure_assembly.json`、`runs/20261011T144115307Z/5154F0_procedure_assembly.json` の `checked.ok=true`、target SHA一致。保存済みASMから局所領域のみ読取（Ghidra/REA新規実行なし）。
- `0x514FCA MOV [ESP+0x20], ESI`（record +0x00の4byte）、`0x514FD7 FSTP double ptr [ESP+0x28]`（record +0x08..0x0Fの8byte）、`0x514FDF MOV [ESP+0x30], ESI`（record +0x10の4byte）、`0x514FDB LEA EAX,[ESP+0x20]`→`0x514FE3 CALL 0x5154F0`。
- 追加ヘルパー`0x5154F0`の外部参照経路は6 DWORD（record+0,+4,+8,+12,+16,+20）をコピーする。内部参照経路の別処理は**先行PC B限定READY報告 `B-20261020-1015-01`と意味重複するため新規事項として再採番しない**。
- 上の**builder局所保存窓内**ではrecord+0x04..07および+0x14..17への明示的なwriteは確認できない。以前の`B-OFFLINE-20261020-0908-01`を**再確認**したのであって、新しい未初期化バグの確定ではない。

## 今回独立作成した増分：byte-provenance診断フィクスチャ

| 24byte record offset | builder局所での状態 | フィクスチャ上の扱い |
|---|---|---|
| `+0x00..03` | Unit pointerを明示書込 | `WRITTEN`（与えた入力が同一なら比較可能な候補） |
| `+0x04..07` | 明示書込未確認 | `UNSPECIFIED`（本診断で差異を別欄に隔離） |
| `+0x08..0F` | double距離を明示書込 | `WRITTEN`（入力/演算境界は別VERIFY） |
| `+0x10..13` | Unit pointerを明示書込 | `WRITTEN` |
| `+0x14..17` | 明示書込未確認 | `UNSPECIFIED`（本診断で差異を別欄に隔離） |

**新規設計**: 24byte全体を一律`MATCH/MISMATCH`と判定せず、局所builderで明示された16バイトの差分位置と、出自未確定の8バイトの差分位置を別の配列に出す。`UNSPECIFIED`の8バイトは「確実にゼロ」「未使用」「バグ」「strict比較の永久除外」を意味しない。後段readerによる実作用・呼出元初期化・他経路writerが確定するまで、**原作互換性の合否ではなく検査対象を仕分ける診断に限定する**。

### 検証実行

- Python標準ライブラリのみ。テスト `test_T013_514F10_RECORD_BYTE_MASK_20261020.py` は既存REA ZIPを**read-only**で開く。ZIP SHA、保存REAメタデータ2/2、builder命令5点/局所書込未確認2点、copy元DWORD 6点、24byte長検査、written 16位置/unspecified 8位置の単独差分をチェック。
- **独立検証結果：unittest 5/5 PASS、0 failures/errors（SYNTHETIC + STATIC-RECHECK）**。各byte差分の比較テストはオフラインで生成した数値列であり原作実機観測ではない。
- 検証用ファイルは制限内のB所有`data/`に独立保存し、MASTERや既存HANDOFFへは許可未確認のまま書込まない。保存後Library APIで別読取確認する。

## 意味重複・境界と未解決事項

- 本調査は既存`B-OFFLINE-20261020-0908-01`の静的指摘から**新たに検証器を作成したことだけが増分**。`B-20261020-1015-01`配列内部alias append、`B-OFFLINE-20261020-0815-01` Unit-local vector再構築、`B-OFFLINE-20261020-0613-01` global scratch resetと混同しない。
- 次回: 現行PC MASTER/規約/HANDOFFとT013所有資料を必ず先読。append先/後段consumerに+4/+20参照があるか、スタックの事前初期化の別経路はあるか、既存証拠と重複していないかを**既存保存資料の許可範囲のみ**で照合する。許可された新規独立増分だけB資料に保存・別読取で確認後HANDOFF候補とする。安全拒否を迂回しない。
- その他P0: T012 `0x580280`実作用/MP fallback/最終攻撃結果、T011クロス種継承、T013候補列挙順・stealth RNG・後段キャッシュ消費、T024通常AI/簡易AI実状態、T028士気効果寿命と`getLimit/addLimit`実作用。
- **当回新規正式READY 0、MASTER正式統合0、原作Gameplay Golden PASS 0、新旧strict MATCH 0**。PC負荷不明。PC未保存／クラウドに本資料・検証器だけ別途保存。従来安全拒否案件はBLOCKED維持。スケジュール未変更。
