# 迫真戦記 新B｜未同期25候補の回収・重複照合スナップショット（2026-10-20 15:15 JST）

- RECOVERY-ID: `B-RC-OFFLINE-20261020-1515-LOCAL-SESSION-01` / Lane B T011・T012・T013・T024・T028。
- 目的: 10月19～20日の回収候補をID単位でロスなく集約し、既存のREADY/安全拒否と分離してPC復旧時の重複検査を最短化。**新しいEXE証拠や仕様を確定するものではない**。
- Source: ChatGPT Library `T011_T012_T013_T024_T028_UNSYNCED_RECOVERY_REGISTER_20261020.md` (2026-10-20 02:18:47 UTC)、`T011_T012_T013_T024_T028_OFFLINE_RECOVERY_INDEX_20261020_1117.md` (02:20:29 UTC)、`T012_T013_T024_T028_GOLDEN_ADMISSIBILITY_AND_RECOVERY_20261020_1214.md` (03:19:33 UTC)、`T013_SUPPORT_RECORD_BYTE_PROVENANCE_OFFLINE_20261020_1313.md` (04:24:45 UTC)、`T013_SAVED_REA_ARCHIVE_COVERAGE_GAP_OFFLINE_20261020_1408.md` (05:16:18 UTC)。個別研究内容は原本ZIP/EXEから今回新たに検証していない。
- PC Local: MASTER read_fileで `INVALID_ARGUMENT: McpServerError: Session terminated`。接続障害であり安全拒否ではない。Remote/Work/Git/原本操作なし。**PC未保存 / Library版のみ保存対象 / OFFLINE-UNSYNCED / NOT READY**。
- 最後に会話で報告されたPC checkpoint194 (10時台) はこのrun未確認。Library `/MASTER_LEDGER.md` checkpoint187 は旧版。予約・E統合済み・現行B HANDOFFとの差分は不明。
- 旧候補22（10/19:7、10/20 03～09:15）+ 12時・13時・14時の新設計/監査候補3 = **照合候補25 ID**。**25件の独立発見という意味ではない**。
- 未確認のPC保存をNOと断定しない。`B-20261019-1317-01`は詳細PC保存・HANDOFF安全拒否と会話で報告されたため現状は「PC詳細保存との報告 / 実査できない」。
- 今回新規正式READY=0、MASTER統合=0、実機Gameplay Golden PASS=0、strict MATCH=0。PC CPU/RAM負荷=不明。

## 回収候補25 ID（重複の可能性は下表のグループ列参照）

| 研究ID | Task | 主題（報告ベース） | 重複照合群 | 現状 |
|---|---|---|---|---|
| `B-OFFLINE-20261019-1009-01` | T012/T013 | 0x4E7ED0 grid conversion / negative coordinates | GRID-NEGATIVE | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261019-1116-02` | T012/T013 | 0x546F70→0x4E7ED0 direction/mode/latch cross-path | FIRE-DIRECTION | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261019-1217-03` | T013 | 0x514D60 primary/fallback, dual pointer return | TARGET-SELECTOR | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261019-1217-04` | T013 | 0x514F10 global scratch logical reset | GLOBAL-SCRATCH | 会話/索引あり・NOT READY |
| `B-20261019-1317-01` | T013 | 0x57DA1F aux null gate; native detail/index reported PC saved; HANDOFF refused | AUX-CACHE | クラウド詳細あり・NOT READY |
| `B-OFFLINE-20261019-1414-05` | T013 | 0x514D60/0x57DA1F nullness crossjoin synthetic | AUX-CACHE | クラウド詳細あり・NOT READY |
| `B-OFFLINE-20261019-1516-06` | T012/T013 | 0x57B870 cache origin vs virtual+80 branch design | CACHE-ORIGIN-V80 | クラウド詳細あり・NOT READY |
| `B-OFFLINE-20261020-0316-01` | T024/T028 | addLimit(514) boss-death vs endgame AI time gates | BOSS-TIMER | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0316-02` | T028 | rank/MUR level morale synthetic boundary matrix | MORALE-RANK | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0409-01` | T013 | 0x514D60 distance tie retains earlier enumerated candidate | TARGET-SELECTOR | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0409-02` | T013 | 0x514D60 32-bit squared distance overflow candidate | DISTANCE-INT32 | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0517-01` | T012/T013 | 0x4E7ED0 signed-coordinate divide-by-32 truncation toward zero | GRID-NEGATIVE | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0613-01` | T013 | 0x514F10→0x5158A0 global scratch end=begin | GLOBAL-SCRATCH | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0613-02` | T013 | primary stealth RNG consumed before distance compare | TARGET-SELECTOR | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0709-01` | T013 | 0x514F10 support-candidate collection local self-exclusion absent | SUPPORT-SELF | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0709-02` | T013 | 0x514D60 fallback local stealth check absent | TARGET-SELECTOR | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0815-01` | T013 | 0x57B870 support Unit-local vector logical reset | UNIT-SUPPORT-CACHE | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0815-02` | T013 | 0x57B870 ability/refresh gate before support vector rebuild | UNIT-SUPPORT-CACHE | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0908-01` | T013 | 0x514F10 24byte record +04/+14 builder writes unknown | SUPPORT-RECORD | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0908-02` | T013 | 0x514F10 signed 32bit support distance overflow candidate | DISTANCE-INT32 | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-0908-03` | T013 | support capability/confusion/element_heal 16-case design | SUPPORT-SELF | 会話/索引あり・NOT READY |
| `B-AUDIT-OFFLINE-20261020-0517-02` | T012 | 0x4E7ED0 nongrid-radius synthetic audit (not newly confirmed) | GRID-RADIUS | 会話/索引あり・NOT READY |
| `B-OFFLINE-20261020-1214-01` | T012/T013/T024/T028 | Golden admissibility gate / observable vs internal evidence, synthetic 10/10 | GOLDEN-ADMISSIBILITY | クラウド詳細あり・NOT READY |
| `B-OFFLINE-20261020-1313-01` | T013 | 24B support record 16 written + 8 unknown provenance byte mask; synthetic 5/5 | SUPPORT-RECORD | クラウド詳細あり・NOT READY |
| `B-OFFLINE-20261020-1408-01` | T013 | Saved REA archive only 62 functions; consumers unresolved; synthetic audit 8/8 | SUPPORT-RECORD | クラウド詳細あり・NOT READY |

## 最優先の意味的重複照合（数え直しをしない）

- `GRID-NEGATIVE`: 10/19 `1009-01` と10/20 `0517-01` は同一の0x4E7ED0負座標変換が主題。新規独立証拠として2件加算しない。
- `GLOBAL-SCRATCH`: 10/19 `1217-04` と10/20 `0613-01` は0x514F10のend=begin再確認。
- `BOSS-TIMER`: `0316-01` とPC保存済み報告 `B-20261020-1015-02` はaddLimit/終盤ゲート部分が重複。新しいT024/T028正式READYに転用しない。
- `TARGET-SELECTOR`: 10/19 `1217-03` に、10/20 `0409-01/0613-02/0709-02` の距離tie/stealth/RNG/fallbackが重なる。局所的増分と既知基礎を分離。
- `SUPPORT-RECORD`: 10/20 `0908-01` は元観察、`1313-01` はbyte-mask合成検証器、`1408-01` は保存REA62関数の限定coverage監査。3件は同一不明8B問題の**段階別資料**であり、3件の新たな仕様確定ではない。
- `DISTANCE-INT32`: `0409-02` は攻撃selector、`0908-02` は支援builder。共通する32bit演算を一回だけ基礎説明し、対象関数の異同は保持。
- `AUX-CACHE`, `CACHE-ORIGIN-V80`, `UNIT-SUPPORT-CACHE`: 分岐経路・出自・vector再構築の対象が違うため、単語が似ていても機械的には同一成果として潰さない。

## Safety拒否：8件の復旧メタデータのみ（操作や本文の再提出禁止）

- `B-20261018-1813-01` / `B-RC-20261018-1813-T011-T012-HANDOFF-SAFETY-01` — detail saved reported / HANDOFF safety refusal。**BLOCKED-METADATA-ONLY**。
- `B-20261019-0117-01` / `B-RC-20261019-0117-T012-T013-READY-ANNOTATION-SAFETY-01` — READY annotation safety refusal。**BLOCKED-METADATA-ONLY**。
- `B-20261019-0210-02` / `B-RC-20261019-0210-T012-HANDOFF-SAFETY-01` — HANDOFF safety refusal。**BLOCKED-METADATA-ONLY**。
- `B-20261019-0725-01` / `B-RC-20261019-0730-T012-T013-HANDOFF-SAFETY-01` — HANDOFF and recovery write safety refusal。**BLOCKED-METADATA-ONLY**。
- `B-20261019-0814-01` / `E-RC-20261019-0850-B0814-MASTER-SAFETY-01` — E MASTER integration safety refusal (E-owned)。**BLOCKED-METADATA-ONLY**。
- `B-20261019-1317-01` / `B-RC-20261019-1756-T013-HANDOFF-SAFETY-01` — HANDOFF safety refusal; same B-2019-1317 candidate above。**BLOCKED-METADATA-ONLY**。
- `B-20261019-1914-01` / `B-RC-20261019-1914-T011-DETAIL-SAFETY-01` — detail write safety refusal。**BLOCKED-METADATA-ONLY**。
- `B-20261019-2010-01` / `B-RC-20261019-2010-T024-INDEX-SAFETY-01` — index write safety refusal。**BLOCKED-METADATA-ONLY**。

## PC接続回復時の回収チェックポイント

1. PC MASTER TASK QUEUE/checkpoint/P0、規約、B HANDOFF、担当5タスク最新資料を順番に読んで版/競合/予約と個別IDの保存状態を確認。
2. `B-20261020-1015-01/02` のPC保存・B READY報告を再確認。これらを今回の25件へ加算しない。E統合はE担当のみ。
3. JSON内のIDとクラウド出典を照合し、`RECOVERED / DUPLICATE / PC-REPORTED-SAVED / OFFLINE-UNSYNCED / BLOCKED / VERIFY` を個別判定。
4. 過去の拒否された同一操作・証拠本文を別tool/shell/path/Remote/Cloudで迂回しない。許されたメタデータの管理と独立した軽量検証のみ。
5. 真に独立しているB担当の確認済み増分だけに正式B-日時-連番IDを採番して、Bのdata/exeまたはevidence/LANE_B_HANDOFFへ小単位で保存し、独立読み戻し・重複チェック。MASTERは変更しない。
6. 状態表を更新する。保存できない部分は対象ID/時刻/理由/未保存内容/出典/次の合法的な再開位置をチャットまたはBクラウド独立台帳に残す。

**補足**: この文書とJSONは内容一覧の復旧用スナップショット。研究コード・原本EXE/ZIP/SAVE/REA本体/設定/他レーン/MASTERには一切手を加えない。スケジュールの有効状態・頻度・時刻も維持。
