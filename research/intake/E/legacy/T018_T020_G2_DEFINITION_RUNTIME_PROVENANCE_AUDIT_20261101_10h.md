> **2026-11-03 E owner intake / sanitized Library source.** Existing ID `E-OFFLINE-20261101-10H-T018-T020-G2-DEFINITION-RUNTIME-PROVENANCE-01`; Library original `T018_T020_G2_DEFINITION_RUNTIME_PROVENANCE_AUDIT_20261101_10h.md`, raw-file SHA-256 `D34E63965ABC21631C00EE89623026A653CAE1B6816B01E1EB1587114D6E18B9` independently measured (2026-11-03). Current authorized PC `tests/` copy was not independently source-matched, so do **not** treat this as PC byte-preservation. Author-era PC/HEAD status below is historical only. 1 pre-existing protected/refusal-reference or sensitive-path line(s) omitted; this Git blob is a sanitized derivative, not byte-identical to the Library file. No reexecution of historical model tests or original game; actual Golden PASS 0, strict MATCH 0, new READY 0, MASTER delta 0. **PUBLISHED_INTAKE / SYNTHETIC|VERIFY / NOT_CURATED.**

# 迫真戦記 新E 10時台｜G2定義・runtime MAP・VM/RNG・観測出典を分離する受入前監査

- 研究ID：`E-OFFLINE-20261101-10H-T018-T020-G2-DEFINITION-RUNTIME-PROVENANCE-01`
- 所有者：E、T018/T020。T019は矛盾候補としての分類のみ（正式矛盾登録なし）。
- 研究状態：`OFFLINE-UNSYNCED / SYNTHETIC / VERIFY / NOT READY`。Golden `DYNAMIC OBSERVED=0 / actual PASS=0 / strict MATCH=0`。
- 時点：2026-11-01 10時台 JST。

## アクセスと先行根拠

Desktop Commander Local Compact の `MASTER_LEDGER.md` 先頭のread_fileを試行し、`UNAVAILABLE / MCP SSE probe returned 429 from openai.org`。接続・レート制限障害、**安全拒否ではない**。別経路でPCアクセスを迂回していない。PC MASTER、所有者、READY、競合、現行knowledge HEADは未確認。

直接読んだ継続資料：前回09hのE所有スクリプト `e_offline_20261101_09h/t018_t020_roster_bijection_order_gate_20261101_09h.py`（SHA256 `99A2B540AE1A88BEAD551185A7477C0C141B6F7A96AD3D6428B19EC7D754355F`）、同監査報告・fixture、ならびに非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` develop の `REF_BATTLE_TAKEOVER.md` blob `3ca8c39e0a654001acdc7db8bfb2e4c1c9a976f7`、`GHIDRA_V9_COVERAGE_REPORT.md` blob `786f7fc5647a54a08609d28db2f673c7dbfd6b36`、`KNOWLEDGE_CURATION_PROTOCOL.md` blob `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`、`SYNC_STATUS.md` blob `f069136afc073d8435daae3797855214fa9d17ef`、`README.md` blob `43595153b4a109d6c4d2ac6738d2ec86965b2f24`。PCとGitHubのHEAD一致は主張しない。

静的な構造の背景は先行KBにあるE+`0x1E8630/34/38`の三Side、Side+`0x48/4C/50` Unit vector、Side+`0x38/3C/40` Troop vector、Troop+`0x0C/10/14` member vector、Unit+`0x1C8`共有record、MAP管理M=G+`0x1EF570`、M+`0xE8` owner、owner+`0x90` grid pointer。**今回これらの機械語を再検証したのではない**。原作EXE/SAVE/SQLiteは一切実行・再解析していない。

## 新規成果：前回09hの合成チェックで未評価だった3種類

前回09hゲートはUnit/Troopの一対一、所属・順序を正しく比較するが、追加フィールドを比較する仕組みをまだ持たない。前回ゲートを変更せず、独立した追加チェックを作り負例を注入した。

1. **Unitのdefinition_key**：新実装のUnitが別の定義へ差し替わっても、09hゲートは`MODEL_G2_SYNTHETIC_EQ`と報告した。今回の追加チェックでは、等しい合成定義か、同等性を明記した合成alias対応に限り通し、意味の異なる/欠落した定義は`VERIFY_DEFINITION_*`へ留保する。原作の定義名が移植先で一致するとは限らず、実原作同等性にはDAT/定義対応の独立出典が必要。09hモデルの不具合と実製品の不具合を混同しない。
2. **実行時MAP・VM/RNG状態**：09hはMAPファイルのSHAだけを比較しており、MAP管理の実行時格子・Unit配置・VM進行・乱数状態を代弁しない。合成のgrid digestが異なる負例を追加し、`MODEL_RUNTIME_MAP_DIFF`、VM/RNG digest差を`MODEL_VM_RNG_DIFF`、欠落/偽装を`VERIFY_*`へ分類。これらのdigestは**単なる合成プレースホルダー**であり、完全な原作MAP/VM/RNG保存仕様を確定したものではない。
3. **G0/G1/G2の一次証拠**：09hの`source_artifact_sha256`は64桁文字列かを確認するだけで、実ファイルのバイト列・法的取得経路・同一実行/入力を検証しない。合成の形式的に正しい偽SHAを受理する負例を明示し、全ケースのGoldenは`NOT_RUN_SYNTHETIC`又は`VERIFY_G0_G1_UNTRUSTED_OR_MISSING`に固定。合成で「観測済み」ラベルを付けても昇格させない。

## T020独立試験結果

既存09hゲートを**実際にimportしread-only実行**した上で、前回未対象の22変種×3つの合成戦闘＝**66ケース**を比較。各ケースで、旧判定と追加チェックの独立期待値、Golden状態の3フィールドを照合した。

- **66/66 PASS**、case ID重複0、終了コード0。
- 旧ゲートで`MODEL_G2_SYNTHETIC_EQ`となるが、definition関連で保留すべき例 **15件**。
- 同じくruntime MAP差異を見逃す負例 **3件**、VM/RNG差異を見逃す負例 **6件**。
- source SHAが妥当な書式でも、実ファイル読み戻し証明を持たない状態は**Gold PASSへ一切計上していない**。
- 09hのMAPファイル差分／Troop順序差分は旧ゲートの元判定を維持し、弱いゲートの「PASS」に変更しない。
- 今回のPASSは**検証器の合成fixture期待値との一致**であり原作互換性PASSではない。

## T018の合法Golden受入ゲート

- **G0**：未改変合法原作UIから実際に開始した戦闘のrun/session ID、時刻、原作ビルド/実SHA、操作列、合法観測方法の出典。
- **G1**：同じrunの直前SAVEの**実バイト**SHA、時点・入力と順序、G0/G2を結び付ける一次出典。SHA文字列の自己申告では不可。
- **G2**：同じrunの実MAPファイル・読み込み後runtime格子、三SideのPower、出撃Unit/Troop**各インスタンスと順序**、共有recordと独立Unitを分離する識別証拠、VM/RNGの捕捉範囲と未捕捉を明記。トークンが異なるプロセス間のポインタ数値と等しい必要はない。保存対象範囲の不明部分は未検証に残す。
- G0/G1/G2の単独合成PASSや静的なアドレス一致では、`DYNAMIC OBSERVED`、actual Golden PASS、strict MATCHを増やさない。

## T019矛盾/KB_CANDIDATE

- 新たな**Wiki/DAT/EXEの確定矛盾 0件**。今回は比較器の証拠欠落（比較モデル側の穴）を発見したので、T019の原作仕様矛盾とはしていない。
- 既存GameClear DAT13/TXT2の検索範囲差は旧RESOLVED、実読み込み/実行順序はVERIFYのまま。新しい再検証なし。
- KB_CANDIDATE ID：本研究ID。先行owner研究 `P0_TAKEOVER_20261024_01`の構造オフセットに関連。新規VA/CALL site・ASM・DAT行番号は**今回なし**。参照上記private KB blobと09hスクリプトSHA。知識の差分は「G2 corpus採用前にdefinition binding・runtime MAP・VM/RNG・一次証拠の検証が必要」。`STATIC=prior evidence only / SYNTHETIC=66/66 / INFERRED=comparison risk / DYNAMIC=0 / GOLDEN=0 / READY=0`。共有KB登録は専任担当へ。

## MASTER、所有者、拒否履歴、再開位置

- MASTER最新未取得：**旧最終確認checkpoint 196 / READY596（A115/B229/C136/D116）/ 34 Task DONE9, IN_PROGRESS21, VERIFY4**。最新値と断定しない。新規正式READY統合ID **なし（0件）**。
- 接続障害 ID：`E-CONN-20261101-10H-LOCAL-SSE-429-01`。日時：2026-11-01 10時台JST。試行：Local CompactでMASTERの先頭を読み取る。結果：429 / UNAVAILABLE。保存済み：今回のオフライン研究成果、既存09hは変更なし。未保存：PC MASTER/READY照合・E正本反映。影響：同一ID/所有権/コンフリクト未確認。許可された次手：接続自然復旧後にMASTER→分析規約→各担当HANDOFF/REA保存RUN→E所有文書、READY元SHA/時刻/合意/既統合をチェックし、一度だけ正式判定。接続障害に対する別シェル/Remote迂回は行わない。

成果：この監査報告、検証器、66ケース受入結果JSON、SHA保存台帳。PC正式統合はBLOCKEDだが調査は継続可能。
