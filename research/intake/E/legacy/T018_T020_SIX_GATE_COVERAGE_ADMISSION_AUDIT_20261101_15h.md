> **2026-11-03 E owner intake / sanitized Library source.** Existing ID `E-OFFLINE-20261101-15H-T018-T020-SIX-GATE-COVERAGE-ADMISSION-01`; Library original `T018_T020_SIX_GATE_COVERAGE_ADMISSION_AUDIT_20261101_15h.md`, raw-file SHA-256 `1773BE35508775E85059409940DE4C1191D3969D7820346C116CD8593C9A8BCB` independently measured (2026-11-03). Current authorized PC `tests/` copy was not independently source-matched, so do **not** treat this as PC byte-preservation. Author-era PC/HEAD status below is historical only. 1 pre-existing protected/refusal-reference or sensitive-path line(s) omitted; this Git blob is a sanitized derivative, not byte-identical to the Library file. No reexecution of historical model tests or original game; actual Golden PASS 0, strict MATCH 0, new READY 0, MASTER delta 0. **PUBLISHED_INTAKE / SYNTHETIC|VERIFY / NOT_CURATED.**

# 迫真戦記 新E｜G012既存6検証器の横断実行・原作一次証拠不足の受入境界（2026-11-01 15時台 JST）

**研究ID** `E-OFFLINE-20261101-15H-T018-T020-SIX-GATE-COVERAGE-ADMISSION-01`  
**owner/task** E／T018・T020。T019は矛盾状態の継承・未確定の分類のみ。  
**状態** `OFFLINE-UNSYNCED / SYNTHETIC / STATIC-SOURCE / VERIFY / NOT RUN / NOT READY`。正式READY新規統合0件。

## 1. 出典とアクセス

- Desktop Commander Local Compact にて研究PCの `MASTER_LEDGER.md`、`ANALYSIS_LANES_PROTOCOL.md`、knowledge README/SYNC 等を `read_multiple_files` で要求。接続前 `UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`（**接続/レート制限障害**）。安全拒否ではない。再試行迂回なし。接続失敗ID `E-CONN-20261101-1551-LOCAL-SSE429-01`、影響：PC正本の最新checkpoint/owner/READY/競合/既存E原文は未確認。EのPC資料に書込みもしていない。
- ChatGPT Libraryの正式なユーザー提供オフラインZIP `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を読取専用で取得し、ZIP実測SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、全34/34 ZIPエントリCRC PASS。旧 `research_snapshot/tests/T018_GOLDEN_CORPUS.md` の実測SHA256 `CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120`。
- GitHub非公開研究KB `ButaMonky/Hakushin067-Research-Knowledge` の`develop` HEAD `0225b2e1cd5c710137a3d921f593d158df06624a`をread-only確認。`README.md` blob `43595153...`、`SYNC_STATUS.md` blob `f069136a...`、`GHIDRA_V9_COVERAGE_REPORT.md` blob `786f7fc5...`、`KNOWLEDGE_CURATION_PROTOCOL.md` blob `4d6da0d1...`、`REF_BATTLE_TAKEOVER.md` blob `3ca8c39e...`。PC HEADと一致したという意味ではない。V9本体の再解析、原作EXE実行、Git変更は0回。
- 既存09〜14時台のE所有検証器6本は `previous E offline-research artifact path/` 等の既存成果を実読し、SHA256を記録。各ソースのSHAは同梱JSON receiptを参照。旧ソースは変更せず `python -B` で単独の `run()`/`execute()` を再実行した。

## 2. 今回の独立成果：6ゲートを全件再実行して能力境界を固定

| 既存スコープ | 今回再実行の合成条件 | 結果 |
|---|---:|---:|
| 09h G2 Unit/Troop全単射・順序 | 117 | 117/117 PASS |
| 10h Unit定義・runtime MAP・VM/RNGの前提 | 66 | 66/66 PASS |
| 11h G0/G1/G2証拠のローカル実バイト検査 | 72 | 72/72 PASS |
| 12h original/replacement別run証拠の別名検査 | 45 | 45/45 PASS |
| 13h 親パス・symlink成分の検査（POSIX） | 36 | 36/36 PASS |
| 14h open済み記述子・パス差替え（POSIX） | 45 | 45/45 PASS |
| **合計** | **381** | **381/381 PASS、fixture ID重複0** |

実行は一つの新しい横断runnerで実施し、すべて一意のfixture ID・期待判定・実際判定を確認。ローカル一時フォルダのみ使用。今回は旧試験を**新規381ケースと主張しない**。追加成果は6独立ゲートの再現可能な単一実行受領票、範囲/証拠SHAの横断台帳、および下記C-NB02原作観測候補の不足項目を具体化したこと。

**重要な未解決点**：381件は6本それぞれの**独立した合成テスト**であり、連結した単一のG0→G1→G2受入runnerではない。14hのファイル固定テストはG1相当の単体POSIX試験で、09hの三陣営・10hのVM/RNG・11hの証拠ファイル・Windows実機File IDを同時に判定したわけではない。従って「統合済みGoldenゲート」「Windows防護済み」「実機互換PASS」とは表現しない。別runnerのPASSを足して原作実証分母にしてはいけない。

## 3. 旧原作sourceで再確定したG012候補・G0受入の障害

旧T018原文の**1157行・1473〜1478行・1657行**をオフラインZIPから今回直接読んだ。`C-NB02`は`scenario sci1 / po2,sp2 → sp16`戦闘候補、`s16.map`候補100×100、旧source記載SHA256 `641F460592C3CE5EF09E64D4EF69ED5BE1F3DE9D52C7BC71AA5D6F3FBF74E440`。**実選択MAPの今回測定値ではない**。原文の初回turn1戦争抑止記述から、turn2以降の可達性は VERIFY のまま。旧save1/2のSpot別Unit保存数32/48は**実戦出撃Unit/Troopの証拠ではない**。

原文を基に `T018_CNB02_ORIGINAL_G012_ADMISSION_CANDIDATE_20261101_15h.json` を作成した。源データは `static_candidate` のみ記入し、G0原作UI開戦、G1戦闘直前の実SAVE・入力・原作EXEハッシュ、G2実MAP/三陣営/ordered Unit・Troop/配置・向き・epoch/VM/RNGはすべて`null`と`NOT RUN`。旧新比較入力・新エンジン実測も未取得。時間実体としてのG1 SAVE/入力はG0より前のものを求めるが、受入チェックはG0確認後に行ってもよい。一次資料の取れない値は補完しない。

本回の計上：**G0 NOT RUN、G1 NOT RUN、G2 NOT RUN、DYNAMIC OBSERVED 0、actual Golden PASS 0、strict MATCH 0、実機比較0、正式READY新規0**。

## 4. T019・知識ベース

T019の新規確定Wiki/DAT/EXE矛盾**0件**。旧GameClear DAT13/TXT2検索範囲差は旧RESOLVED、`script2`/loader・実行順序は VERIFY を維持。今回の旧T018 source再読はG0達成度の検査であり、現行wiki/DAT/EXE全原本との三者直接照合ではないため、T019の新規RESOLVEDを増やさない。

`KB_CANDIDATE` = 本研究ID（E/T018/T020）。対象は**比較検証器・Golden出典表の受入範囲と統合断絶**。先行既存IDは09〜14時台の6件。今回の新規VA/CALL site/オフセット・nativeバイト発見なし、`N/A`。source は上記旧T018 SHA、GitHub `REF_BATTLE_TAKEOVER.md` blob SHA、今回検証器6本のSHA/receipt。分類 `STATIC`=source原文照合、`SYNTHETIC`=381 PASS（再実行）、`INFERRED`=ゲート未連結の受入上のリスク、`DYNAMIC`=0、`Golden`=0、`READY`=0。共有KBへの書込・Git/pushは専任curatorのためEは実施しない。

## 5. MASTER状態・拒否の保護・次の一手

認可PC MASTER最新版は未読。最終確認値は**旧checkpoint 196、旧READY 596（A115/B229/C136/D116）、34 Task旧DONE9/IN_PROGRESS21/VERIFY4**。現在もそうであるとは断定しない。正式READY統合IDなし/0件。過去のOFFLINE-UNSYNCEDは一切完成扱い・巻戻し・二重加算していない。


**再開位置**：(1) 自然なPC接続回復後、MASTER最新版・レーン規約・最新A-D HANDOFF・REA保存RUN・E所有T018/T019/T020・dev_lab計画・PC知識DB/HEADを読み取る。(2) 研究ID・owner・source hash・時刻・合意・READY・重複・既統合・旧拒否/未回収を突合。(3) E所有資料に許される範囲だけを一度反映、`VERIFY/NOT READY`から不当に昇格させない。(4) 最優先は合法原作UIでC-NB02のG0/G1/G2一次観測の成立可否と、source候補を実選択MAP/出撃配置と混同しない受入。独立合成テストの細分化より、真の原作観測・旧新同条件比較に移行する。
