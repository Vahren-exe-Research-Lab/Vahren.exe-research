> **2026-11-03 E owner intake / sanitized Library source.** Existing research ID `E-OFFLINE-20261101-12H-T018-T020-CROSS-RUN-ALIAS-ADMISSION-01`. Original Library file `T018_T020_CROSS_RUN_ALIAS_AUDIT_20261101_12h.md`; actual raw Library SHA-256 `638F53757F091144F1278DAFD41BB91E5FDA6AC59EAD76F783205332B321DBD2` measured 2026-11-03. Original research PC `tests/` same-named report absent on the current authorized PC; PC↔Library SHA equivalence is **not** claimed. The archived text below is historical synthetic/static analysis and its older PC-unavailable statements describe the 2026-11-01 authoring snapshot, not this intake run. 1 line(s) referring to pre-existing protected/refusal scope or sensitive absolute paths omitted; none was used to recover denied material. Git blob is a **sanitized derivative**, not byte-identical to the Library source. No original game was executed; Golden PASS 0, strict MATCH 0, new READY 0, MASTER formal delta 0. **PUBLISHED_INTAKE / VERIFY / NOT_CURATED.**

# 迫真戦記 E/T018・T020 — G0/G1/G2 保存証拠の実体所有権検証 (2026-11-01 12時台)

- **研究ID**: `E-OFFLINE-20261101-12H-T018-T020-CROSS-RUN-ALIAS-ADMISSION-01`
- **owner / tasks**: E / T018 (Golden admission), T020 (regression); T019 tracked only; no A–D/REA/dev_lab change
- **判定**: `OFFLINE-UNSYNCED / SYNTHETIC / VERIFY / NOT READY`
- **参照元**: 既存E 09・10・11時台の検証器（SHAは検証receiptを参照）、会話に保存された旧MASTER状態、GitHub private knowledge `develop` の `GHIDRA_V9_COVERAGE_REPORT.md`（blob SHA `786f7fc5647a54a08609d28db2f673c7dbfd6b36`）、`KNOWLEDGE_CURATION_PROTOCOL.md`（blob SHA `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`）を読取。両文書は静的索引の限界を明記。
- **PC状態**: Local Compact read は `MCP SSE probe returned 429`。一時接続障害と分類。PC原本・MASTER・REA・T019現物は今回は読めていない。新規安全拒否はなし。
- **実行範囲**: 11時台の比較器を変更せず読取専用で再利用。原作EXEは実行・新規取得せず、Ghidra/Javaの再解析なし。既存SHA `E8DAC301...8767187` はユーザー提供の**期待値・メタデータ**であり、今回原本バイトから再計算していない。

## 新規に確認した検証器上の欠陥（合成証拠のみ）

11時台比較器は、同じ合成SAVEのバイト列を original/replacement の独立した観測と見せかけても、manifest 各run内の `relative_path` 重複がなく、SHA256・サイズ・battle keyが合っている限り、`MODEL_G012_LOCAL_BYTES_INTEGRITY_ONLY` を返す。

そのため「異なるrunから採取した独立した証拠実体」であることを追加の受入前提としなければ、G1原本と新実装の試験データを取り違える余地がある。**これは11時台の合成比較器の守備範囲漏れであり、原作ゲームまたは新エンジンの不具合を意味しない。**

今回の実測（Python temp filesのみ）では、11時台検証器が次を通した：

1. 同一パスを2 run から参照 (`g1_save`、`g1_input`)、またはoriginal/replacementがパスを入れ替える。
2. 元ファイルとは別名のパスでも同一inodeを指すハードリンクを他runの証拠として提示する。
3. パスが一意でも所有runと異なる名前空間の下に配置する。
4. `source_bytes_proven=true`、または根拠のない `independent_observation_evidence` という自己申告属性を追加する。

独立追加ゲートは、全run通算の相対パス・解決先・inode一意性、role専用ディレクトリ整合性、自己申告のsource/owner証拠非昇格を検査する。内容が偶然同一でも異なる実体ファイルなら検証は通す（ただし**最終結果は常にVERIFY、Golden認定は0**）。inode に基づく補助検査は環境依存があるため、Windows導入時は同等のファイルID検査と所有run識別子の二重検証が必要。

## T020 独立回帰

| 項目 | 結果 |
|---|---:|
| 15変種 × 3 seed | **45/45 PASS** |
| 先行11時台の検出範囲外で通過した負例 | **24/24確認** |
| 追加の所有権検査で検出した新範囲の負例 | **24/24** |
| 正常系合成fixture | 6件（すべて`VERIFY_SYNTHETIC_ARTIFACT_BYTES_ONLY_NOT_GOLDEN`） |
| 初回期待値不一致 | 3件。交換済みパスは別roleを指すが同一パスではないため、正しい分類`VERIFY_ARTIFACT_ROLE_NAMESPACE`へ期待値を修正。最終45/45。 |
| 元11時台・09時台・10時台ソース変更 | **なし** |
| DYNAMIC OBSERVED / actual Golden PASS / strict MATCH | **0 / 0 / 0** |

Receipt内に全45件の expected, actual, legacy11h result, pass、先行検証器3本のSHA256を格納。

## T018 G0/G1/G2 合法Golden受入

G1は合法原作で実際に保存された戦闘直前SAVEのバイト列+SHA256と、同一sessionの順序付き実入力ログが必要。G0は未改変原作UIの実戦闘開始が追跡可能であることが必要。G2は同一戦闘の実MAP・三陣営・順序付き出撃Unit/Troopに加え、定義・実行時MAP・観測可能なVM/RNG状態と正しいcapture barrierが必要。原本/置換実装は**別々のrun/session/証拠ファイル実体**として採取し、Unit/Troop対応は外部証人で立証する。ハッシュや自己申告だけでは実行真偽・合法性・原子性を証明しない。

## T019 矛盾とKB

新規Wiki/DAT/EXE一次比較は**NOT RUN**、新規確定矛盾 **0件**。GameClear検索範囲差は従来のRESOLVED、読み込み順序は従来のVERIFYのまま（PC正本に未照合）。

**KB_CANDIDATE**: E-T018/T020, 「G012の原作/置換証拠のファイル実体所有runの一意性」。新たなVA/CALL site/offsetの証拠は今回なし（N/A）。基礎となる原作バイト・原作Golden/READYの根拠なし。GitHub KBへの正式反映は専任の担当へ委任し、現時点で辞書登録しない。

## MASTER・継承・再開位置

- PC MASTERは今回取得できず正式統合 **0件**。最後の報告に基づく**旧確認値**はcheckpoint **196**、READY **596** (A115/B229/C136/D116)、34 Task **DONE9 / IN_PROGRESS21 / VERIFY4**。新たな照合で更新した値ではない。
- **正式反映条件**: PC復旧後にE正本、MASTER最新版、owner/task、source SHA、ID/時刻重複、同研究先行反映、READY証拠、競合、旧拒否履歴を読み直す。新12時台成果を候補として重複なし・owner承認を満たした場合に一度だけE管理資料へ取り込む。旧成功checkpointへ戻さない。新fixtureはGolden PASS/READYには昇格しない。
- **次の優先作業**: 合法原作 G0/G1/G2 の結合された実証拠の取得条件と保存資格のレビュー、およびPC復旧後の正式監査。Windowsでのrun別ファイル識別を併せて検討。

**安全注記**: path/inode別名の検出は誤った証拠の受入防止のための合成検査である。原作EXE/SAVE/ZIPや拒否済み範囲には触れていない。
