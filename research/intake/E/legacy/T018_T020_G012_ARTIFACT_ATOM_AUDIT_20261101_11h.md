> **2026-11-03 E owner intake / sanitized Library source.** Existing ID `E-OFFLINE-20261101-11H-T018-T020-G012-ARTIFACT-ATOM-01`; Library original `T018_T020_G012_ARTIFACT_ATOM_AUDIT_20261101_11h.md`, raw-file SHA-256 `F811809B90D4719320EE7BF0DE0E5A964FA0FB8202DA1149CF878E148A3D1AED` independently measured (2026-11-03). Current authorized PC `tests/` copy was not independently source-matched, so do **not** treat this as PC byte-preservation. Author-era PC/HEAD status below is historical only. 1 pre-existing protected/refusal-reference or sensitive-path line(s) omitted; this Git blob is a sanitized derivative, not byte-identical to the Library file. No reexecution of historical model tests or original game; actual Golden PASS 0, strict MATCH 0, new READY 0, MASTER delta 0. **PUBLISHED_INTAKE / SYNTHETIC|VERIFY / NOT_CURATED.**

# 迫真戦記 新E｜2026-11-01 11時台：G0/G1/G2 raw artifact bindingと混在epoch防止

- **研究ID:** `E-OFFLINE-20261101-11H-T018-T020-G012-ARTIFACT-ATOM-01`
- **owner/task:** E / T018, T020。T019は確定原作矛盾の登録なし。
- **状態:** `OFFLINE-UNSYNCED / SYNTHETIC / VERIFY / NOT READY`。`DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0 / new READY=0`。
- **PC接続:** 2026-11-01 11時台JST、Local Compactで `MASTER_LEDGER.md` を直接 `read_file` したが `UNAVAILABLE: MCP SSE probe returned 429 from openai.org`。接続/一時的レート制限障害で**安全拒否ではない**。Remote等の別経路でPCを再接続していない。

## 出典・重複照合

- このターンに実読した既存E成果：09h Unit/Troop全単射比較スクリプト `t018_t020_roster_bijection_order_gate_20261101_09h.py`、10h definition/runtime provenance差分スクリプト `t018_t020_g2_provenance_semantics_gate_20261101_10h.py` とそれぞれの監査報告。旧09hが三陣営の順序・個体IDを、旧10hが定義/MAP/VM/RNGプレースホルダーを扱っていることを確認し、それらを**改変せず**本11hゲートが実際にimportして使用。
- 非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` `develop` の `README.md` blob `43595153b4a109d6c4d2ac6738d2ec86965b2f24`、`SYNC_STATUS.md` blob `f069136afc073d8435daae3797855214fa9d17ef`、`REF_BATTLE_TAKEOVER.md` blob `3ca8c39e0a654001acdc7db8bfb2e4c1c9a976f7`、`GHIDRA_V9_COVERAGE_REPORT.md` blob `786f7fc5647a54a08609d28db2f673c7dbfd6b36`、`KNOWLEDGE_CURATION_PROTOCOL.md` blob `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a` をGitHub connectorからread-only取得。**現在のPC/GitHub HEAD一致は未確認**。
- 先行構造オフセット E+`0x1E8630/34/38`、Side vectors +`0x48/4C/50` / +`0x38/3C/40`、Troop member vector +`0x0C/10/14` は`REF_BATTLE_TAKEOVER.md`の先行STATIC/INFERRED出典であり、今回原作機械語・Ghidra DB・DAT・SAVEを新たに読んでいない。原作EXEの期待SHAは従来の `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。

## 新たに確認した比較設計の穴と対策

既存09/10hは合成のSHA文字列や `battle_join_key` の形・一致を主に検査していた。だが、自己申告の64桁文字列は**実際のG0 UIトレース、G1 SAVE/入力、G2 snapshotのバイト列を検査した証拠ではない**。また、同じ `battle_join_key` と等しいruntime SHA文字列を持っていても、G2 roster/grid/VM/RNGが一回の原子スナップショットから来たとは限らない。

そこで**個別blobの実バイトSHA**、同一session/run/battle、G1→G0→G2の時系列、G2 frame-epoch/barrier一致、既存09/10hのデータ構造との内容一致を検査する隔離合成runnerを作成。意図的な不正変更として「保存ファイルだけ変更」「SHAだけ変更」「SHAを再計算して改ざんを隠すが既存G2 snapshotとは食い違う」「異なるrunの入力混入」「G2のepoch/barrier混入」等を区別する。実ゲームの原子的キャプチャ方法や正しい時間閾値は**未検証**であり合成ゲートの通過をGoldenとして採用しない。

## T020検証

- 合成3 run × 24バリアント＝**72ケース、72/72期待値一致、失敗0、case ID重複0**。全成功ケース中、単にローカルblob整合が成立するbaselineは**3件**であり、残り69件は不正または証拠不足の期待された検出（いずれも「原作互換PASS」ではない）。
- 09/10hゲートは読取専用import。既存ファイルの変更なし。保存先のテストファイルは隔離した一時ディレクトリにのみ生成、テスト後自動消去。
- 原作ゲームの起動、PE/SQLite再解析、実SAVE/G0/G1/G2採取なし。原作互換性 `DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0`。
- 具体的な合法Golden入手/差分照合条件を `T018_T020_G012_CAPTURE_BINDING_CONTRACT_20261101_11h.md` に分離して記録。誤った実測昇格を防ぐため合成ゲートはあらゆる正例にも `MODEL_G012_LOCAL_BYTES_INTEGRITY_ONLY` しか返さない。

## T019 / KB_CANDIDATE

- **新規確定Wiki/DAT/EXE矛盾0件。** 今回の穴は比較モデルの証拠真正性ギャップであり、GameClear DAT13/TXT2の旧RESOLVED、loader/実行順VERIFYは変更しない。
- **KB_CANDIDATE:** 本研究ID、E/T018,T020。先行VA/CALL siteは今回新しく取得していない。先行構造は上記private GitHub `REF_BATTLE_TAKEOVER.md` blobを参照。10hと09hスクリプトの実SHA256は新11h receiptに保存。差分は「G0/G1/G2のblobと比較snapshotのbyte-level binding、session/phase/G2 frame/epoch検証」。原作/source line・native SHAの新規発見なし。`STATIC=prior source only / SYNTHETIC=72/72 / INFERRED=acceptance gap / VERIFY / DYNAMIC=0 / GOLDEN=0 / READY=0`。辞書更新は知識専任担当に委ねる。

## MASTER、拒否、未同期

- PC正本 MASTER最新 **未取得**。**最終確認済みの旧値**は checkpoint **196**、READY **596件**（A115/B229/C136/D116）、34 Task **DONE9 / IN_PROGRESS21 / VERIFY4**。今回再集計値ではない。新規正式READY統合IDなし / **0件**。
- 新規接続障害ID `E-CONN-20261101-11H-LOCAL-SSE-429-01`。時刻 2026-11-01 11時台JST。試行 `Desktop Commander Local Compact.read_file(MASTER_LEDGER.md,0..99)`、結果 `MCP SSE probe returned 429 from openai.org`。保存済み：11h検証器・receipt・受入契約・研究報告。未保存/未実行：PC MASTER、A-D/REA owner、E所有資料の最新チェック・正式統合。影響：READY同一ID・owner承認・SOURCE SHA・競合は未監査。**次の許可された手:** 自然復旧後、MASTER→規約→A-D/REA保存RUN→E T018/19/20→READY根拠/owner/time/同一ID/競合→一度だけ統合可否判断。
- PC正本/MASTER、A-D、REA、dev_lab、原本EXE/ZIP/SAVE、生成DB、共有knowledge、Git/push、Work、スケジュール・設定を**変更していない**。

## 次優先

合法原作G1直前SAVE・入力、G0 UI開始、G2同一戦闘の三陣営と実MAP/VM/RNGの一次証拠入手条件を明確化し、原作観測が得られるまでCOMPAREをVERIFYに固定。復旧時はowner/READY/競合を先に照合し、11hの独立ゲートをE所有の正式比較runner/文書に採用可能か判定する。
