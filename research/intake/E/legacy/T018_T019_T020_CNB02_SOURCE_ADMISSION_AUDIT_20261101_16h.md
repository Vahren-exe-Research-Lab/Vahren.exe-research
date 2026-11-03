> **2026-11-03 E owner intake / sanitized Library source.** Existing ID `E-OFFLINE-20261101-16H-T018-T019-T020-CNB02-SOURCE-G012-ADMISSION-01`, author timestamp 2026-11-01. Source Library original `T018_T019_T020_CNB02_SOURCE_ADMISSION_AUDIT_20261101_16h.md` has independently measured raw SHA-256 `5131D85237594DBCBD051A53D8A096301CCE1729A92A7DEB62EB1C11BC967109` (2026-11-03). Original authorized research PC `tests/` was not byte-compared to Library, therefore **not** claimed identical. 1 protected/sensitive-scope reference line(s) omitted; Git blob is sanitized derivative. Historical test claims are archived, **not rerun**. Golden PASS 0 / strict MATCH 0 / new READY 0 / MASTER formal delta 0. **PUBLISHED_INTAKE / STATIC-SNAPSHOT|SYNTHETIC|VERIFY / NOT_CURATED.**

# 迫真戦記 研究E｜16時台：C-NB02合法原作G012の出典・欠損監査／T019矛盾境界

研究ID: `E-OFFLINE-20261101-16H-T018-T019-T020-CNB02-SOURCE-G012-ADMISSION-01`。owner **E**、tasks **T018/T019/T020**。分類 **OFFLINE-UNSYNCED / STATIC SNAPSHOT / SYNTHETIC NEGATIVE TEST / VERIFY / ORIGINAL NOT RUN / NOT READY**。

## 結果と改善点

**新しい具体成果は、15時台のC-NB02候補JSONを2026-10-21原文に戻して出典照合し、G0～G2が成立していない具体的な欠損を機械的に出したこと。** 先行の6独立検証器の再実行381/381 PASSは今回の新規テストではない。今回新規の「入力不足をGoldenに昇格させない」合成負例19件は**19/19 PASS**。原作戦闘比較結果は0件。

- 原作オフラインZIPは実バイトSHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` と一致。34/34 ZIP entry CRC問題なし。旧T018本文SHA256 `CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120` と一致。引用16行を実読、固定anchor不一致**0**。
- 旧T018由来のC-NB02 `sci1/po2/sp2→sp16`、候補`map=s16`、Spot保存数、turn1の戦争抑止を再確認（旧source 1157, 1175–1182, 1246, 1473–1478, 1657–1659行）。最新PC正本ではなく**2026-10-21スナップショット**に限った証拠。
- 15時台のC-NB02観測候補には**G1 6・G0 4・G2 8・新実装比較4、計22個の必要な観測値が未記入**。加えて、旧source契約と比較して**11の明示的な観測・監査欄が既存JSON schemaに存在しない**。この11欄はすべて今回設計の追加候補（強制した場合にゲームUIで取得できると実証したものではない）。旧T018の「初期HP/MP/status」「実戦形態」「押下/解放」「証拠run一意性」「原作・新実装それぞれの観測根拠」が特に重要。
- `s16.map`が実戦で選ばれたとは断言できない。`sp16`を`po16`と変換しない。save1/2掲載Unit IDから実出撃集合やTroopを生成しない。戦場種別の継承/上書き、初期HP/MP、生成世代、VM/RNG、原子captureは**VERIFY/INELIGIBLE**を許容し、採取不能な値を補完しない。
- 負例は、source SHA偽装、owner変更、sp16→po16、保存数すり替え、candidateを観測済み扱い、旧381合成回帰のGolden昇格、dynamic/PASS/strict/READY/MASTER統合の虚偽昇格、入力同等性の証拠なし真化など**19/19が期待する拒否・保留状態を出す**。正当な実機正例は0件、WindowsのファイルID・同一時点atomicityはNOT RUN。

## T019矛盾履歴・未解決を区別

古いMASTERスナップショットの`T019`表（旧185行）はIN_PROGRESS。T019の`GameClear`関連`C-007`は、旧MASTER 1152～1170行で**過去のnative分岐の読み違えを訂正し、Wikiとの誤認矛盾を取り下げている**。zero-arg `setGameClear()`のshort側とarg-presentのfull ending側を逆転させた旧メモを再採用しない。旧T018のcase `T018-E-REP-BATTLE`（1152～1163行）はDYNAMIC OBSERVED0を明記。後続`R_HZN`や`C-017～019`、`INPUT-FOCUS-GATE`は旧T018の1242行でOPEN/VERIFYであり、今回閉鎖も新規確定矛盾認定も行わない。**今回の新規T019確定矛盾0**。現行wiki・DAT・EXE三者の最新直接照合はPCアクセス不能でNOT RUN。

## 出典・責任境界

1. Desktop Commander Local Compact `read_multiple_files` によりPCの`MASTER_LEDGER.md`/分析規約/KB README/SYNC/T018/T019を優先取得しようとしたが、`INVALID_ARGUMENT: McpServerError: Session terminated`。**接続障害**。復旧ID `E-CONN-20261101-1652-LOCAL-SESSION-01`。この障害だけではPC電源OFFと断定しない。安全拒否ではない。PCへの再接続は次回自然な復帰時に正規手段で再試行。
2. User Libraryの元ZIP（今回materializeした**読み取り専用コピー**）内の旧`research_snapshot/tests/T018_GOLDEN_CORPUS.md`、旧MASTERと、Libraryで保存済み15時台の独立研究ID `E-OFFLINE-20261101-15H-T018-T020-SIX-GATE-COVERAGE-ADMISSION-01`のcandidate JSONとsynthetic receiptを照合。15時台の実検証は今回の観測ではない。元ZIP/EXE/SAVE/DBは変更していない。
3. 非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge`のread-only `develop` HEAD `0225b2e1cd5c710137a3d921f593d158df06624a`を枝APIで再確認。`README.md` blob `43595153...`、`SYNC_STATUS.md` blob `f069136a...`、`GHIDRA_V9_COVERAGE_REPORT.md` blob `786f7fc5...`、`KNOWLEDGE_CURATION_PROTOCOL.md` blob `4d6da0d1...`、`symbols.tsv` blob `3fcf2d43...`。PCのdevelop/MASTERとは一致未確認。
4. 原作EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`は旧snapshotの記載値（今回原本EXEの実SHAを再測定していない）。新規VA/CALL site/offset発見なし。今回Ghidra/Java/ゲームは起動していない。

## MASTER/Golden/READY

- 現PC MASTER checkpoint、34 Task最新状態・READY新規証拠・所有者合意は未確認、現行正本書込みは**BLOCKED（接続障害）**。旧最終確認の参考値は**checkpoint 196 / READY 596（A115/B229/C136/D116） / DONE9・IN_PROGRESS21・VERIFY4**。旧値を現在値と断定しない。
- **新規正式READY統合ID なし（0）／DYNAMIC OBSERVED 0／actual Golden PASS 0／strict MATCH 0**。OFFLINE-UNSYNCED独立成果を完了に昇格しない。

## KB_CANDIDATE（専任curator審査待ち）

- ID: `E/T018-T019-T020-CNB02-SOURCE-G012-ADMISSION-GAP-16H`。owner E、task T018/T019/T020。先行E IDは15時台`SIX-GATE-COVERAGE-ADMISSION-01`と10月21日原文`T018-E-REP-BATTLE-20261013`。
- 証拠: relative path `research_snapshot/tests/T018_GOLDEN_CORPUS.md`、上記SHAと原文行。今回作成のE所有 `t018_t019_t020_cnb02_admission_preflight_20261101_16h.py` およびJSON receipt。新規VA/CALL/offset `N/A`。
- STATIC: 旧原文・schema照合。SYNTHETIC: 19件の負例。INFERRED: 欄の欠落が将来誤昇格リスクになる。VERIFY: 正規PC sourceと実機UI可達、hidden state、Windows FileID。DYNAMIC: 0、Golden:0、READY:0。今回の11追加候補欄を共有knowledgeに自動登録してはならない。

## 再開位置

PC復帰後、`MASTER_LEDGER.md`、レーン規約、A-D最新HANDOFF/owner/READY、REA保存RUN、`dev_lab/docs/IMPLEMENTATION_PLAN.md`、E所有T018/T019/T020とKB/V9正本を**読み取り専用で先に確認**。旧source SHA・候補ID・旧拒否・合意・timestamp・競合・既統合を照合。今回候補は**Eの許可された文書へ一度だけ、VERIFYのまま**反映可否を審査する。最優先は合法原作C-NB02 G0/G1/G2一次証拠の回収条件、残る未記入22観測欄と追加候補11欄の必要/任意/INELIGIBLE決定。観測不可を推定で埋めない。
