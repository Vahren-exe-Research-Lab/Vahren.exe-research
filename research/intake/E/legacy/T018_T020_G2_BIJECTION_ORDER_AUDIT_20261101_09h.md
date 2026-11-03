> **2026-11-03 E owner intake / sanitized Library source.** Existing research ID `E-OFFLINE-20261101-09H-T018-T020-G2-BIJECTION-ORDER-01`. Original Library file `T018_T020_G2_BIJECTION_ORDER_AUDIT_20261101_09h.md`; actual raw Library SHA-256 `1F4E9A31904772FA5990F8F324EDA234A204FD5C0D317834DEA00EBFC26C07A1` measured 2026-11-03. Original research PC `tests/` same-named report absent on the current authorized PC; PC↔Library SHA equivalence is **not** claimed. The archived text below is historical synthetic/static analysis and its older PC-unavailable statements describe the 2026-11-01 authoring snapshot, not this intake run. 1 line(s) referring to pre-existing protected/refusal scope or sensitive absolute paths omitted; none was used to recover denied material. Git blob is a **sanitized derivative**, not byte-identical to the Library source. No original game was executed; Golden PASS 0, strict MATCH 0, new READY 0, MASTER formal delta 0. **PUBLISHED_INTAKE / VERIFY / NOT_CURATED.**

# 迫真戦記 新E｜T018/T020 G2三陣営のUnit/Troop順序・一対一対応の独立受入ゲート（2026-11-01 09時台 JST）

- **研究ID:** `E-OFFLINE-20261101-09H-T018-T020-G2-BIJECTION-ORDER-01`
- **owner/task:** E / T018・T020（T019について確定矛盾を再分類せず調査）
- **分類:** `OFFLINE-UNSYNCED / SYNTHETIC MODEL ONLY / VERIFY / NOT READY`
- **観測・受入:** `DYNAMIC OBSERVED=0`, `actual Golden PASS=0`, `strict MATCH=0`, `new READY=0`。
- **PC接続:** Desktop Commander Local Compact の最初の `read_multiple_files`（MASTER、evidence/ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、dev_lab IMPLEMENTATION_PLAN、knowledge、旧Ghidra index）の接続層が `UNAVAILABLE: MCP SSE probe returned 429 from openai.org`。これは**接続/レート制限障害**であり、禁止操作に対する安全拒否ではない。別Desktop tool/pathで迂回せず、本成果は独立隔離ファイルとして作成。PC正本・所有者・READY・衝突は今回未確認。

## 1. 出典・重複照合と境界

- 直前E資料 `prior E 08h source report (Library archival copy)`（本作業環境で実読、SHA256 `1688171315BDB14A1487443E476E66E23A8A839983CEE405205AC1CF5F029451`）。既存08hは**単一candidateのcaller別identity/時系列条件**を60合成ケースで検証済みであり、今回再計上していない。
- 非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` **develop** の次をGitHub connectorでread-only実読：`README.md` blob `43595153b4a109d6c4d2ac6738d2ec86965b2f24`、`GHIDRA_V9_COVERAGE_REPORT.md` blob `786f7fc5647a54a08609d28db2f673c7dbfd6b36`、`KNOWLEDGE_CURATION_PROTOCOL.md` blob `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`、`SYNC_STATUS.md` blob `f069136afc073d8435daae3797855214fa9d17ef`、`REF_BATTLE_TAKEOVER.md` blob `3ca8c39e0a654001acdc7db8bfb2e4c1c9a976f7`。GitHubファイルの実読をもってPC HEADの一致や全MASTER確認とはしない。
- `REF_BATTLE_TAKEOVER.md` のG2研究境界：三Side参照 E+`0x1E8630/34/38`、SideのUnit-vector `+0x48/4C/50`、Troop-vector `+0x38/3C/40`、Troop member-vector `+0x0C/10/14`。共通定義・共有recordを複数Unitが参照し得るため、**definition_keyや生pointerで独立Unitを自動重複除去しない**。実MAP/VM/生成世代の完備は未検証。
- 旧原作PE SHA256はユーザー指定の `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。**今回原作EXE・SQLiteを新たに読み直していない**。元Ghidra V9も今回PCから取得していない。原作ゲームは起動していない。新規の静的native事実の主張なし。

## 2. この回の独立増分：G2一体比較での偽一致を抑止

前回08hのcaller別参照値比較とは別に、G0/G1に続く**同一戦闘・同一時点のG2三陣営を「順序付きの一体スナップショット」として比較する合成前処理**を新規作成。

1. **三Side固定順・Power・MAP:** attack/defend/reinforce、Power token、MAP SHA256、battle join とprebattle-G2 phaseを比較。Power tokenは合成例であり、実原作のPower IDそのものを断定しない。
2. **UnitとTroopの別個の全単射:** `Unit` 5個と`Troop` 4個のサンプルを、個別のsource→replacement witness bindingsで一対一対応付ける。Unitはspawn-eventが対応することをモデル上検査し、異なる元プロセスポインタはそれ自体を一致/不一致判定に使わない。Troopは**同じmember構成でも別Troopであり得る**ため、member-list比較より先にTroop IDの証拠付き対応を確認。
3. **順序保存:** SideのUnit順、Troop順、各Troop内member順を独立に評価。Unitの同名定義や同一recordへの参照は独立Unitを潰す根拠にならない。Troopの並び順はmember-listが同一でも無条件に無視しない。
4. **証拠・重複の負例:** 不正な/重複したUnit/Troop ID、bindingの欠落・非全単射、世代不一致、偽装した`DYNAMIC_VERIFIED`、別battle/phase、MAP/source SHA不正、NULL roster pointer、同一capture内のraw pointer alias、u32範囲外をそれぞれ`VERIFY_*`へ隔離。
5. **表現の限界:** `MODEL_G2_SYNTHETIC_EQ`は合成入力の整合性だけを表し、実原作と新実装の照合・G2受入・Golden PASS・strict MATCHを表さない。synthetic ID / witness / digestを現実の観測証拠に昇格させない。

## 3. 独立検査の実行・修正履歴

- 合成fixture：**117件**（battle種別スナップショット3セット×39条件）。独立読み戻しから再計算した期待値一致：**117/117 PASS**、ID重複0。終了コード0。
- ケース分類：モデル同等9件／モデル相違24件／検証待ち・拒否84件。これは**合成モデルの仕様分類**であり実ゲーム結果の分布ではない。
- 最初の実行は **96/105 PASS** で9件不一致（Unit重複がmember先行エラーとして判定される6件、binding対象を交換したのにbirth witness未更新が3件）。重複検査を先行し、交換側のgeneration witnessを試験定義どおり更新して **105/105 PASS**。初回9件の不一致を記録から消去していない。
- 次に**Troop別IDが存在してもmember順が偶然同じだとTroop順変更を検出しない偽一致**を発見。UnitだけでなくTroopにも別途全単射を追加し、同一member-listのTroop入替負例を含め最終117件に拡張。
- さらに、Unit-vectorへ実在Unitとして登録されたNULL pointerと同時点に同一raw-pointerを持つ2個の異なるUnit IDを、モデル上の同等とするのは危険として `VERIFY_NULL_ROSTER_PTR` と `VERIFY_RAW_PTR_ALIAS` に変更（実ゲーム側のaliasの意味は別途観測必要）。
- 読み戻し用**独立スクリプト**の初回は、意図的に不正originへ書き換えた負例を「全件正常origin」と誤ってassertして停止。負例のみ許容するよう訂正し、最終117/117再実行・fixture/receipt ID突合・JSON再解析・結果照合に成功。これを原作互換のPASSと混同しない。

## 4. T018 Golden・T019・MASTERの扱い

- **T018 G0:** 未改変合法原作UI上の戦闘開始と選択操作・時刻・原作source識別。**G1:** 同じ戦闘の直前SAVEの実バイトSHAと入力確定順序・実EXE/DAT source識別。**G2:** 実MAPの読み込み内容/ハッシュ・攻守援軍Power・Unit/Troopの順序と生の観測証拠を同じbattle/run/frameに結合。今回のG2合成モデルに埋めたPower/Unit IDは実観測の代替にならない。G3/G4も未実測。
- **T019:** 新規確定Wiki/DAT/EXE矛盾 **0件**。GameClear DAT13/TXT2の検索範囲差は旧RESOLVED、loader/実行順はVERIFYを維持。新しい「Troop ID抜きで順序比較すると偽一致」は**比較fixture設計上の欠陥**であってWiki/DAT/EXEの新たな矛盾ではない。
- **T020:** 単一targetのcaller別比較に加えて、G2 roster全体のUnit/Troop複数インスタンス・alias・順序・欠落を回帰入口に導入する候補。現在runnerに取り込まれておらず正式PASSではない。
- **MASTER:** PC正本を今回取得できず。旧最終確認値 **checkpoint196、READY596件（A115/B229/C136/D116）、34 Task DONE9 / IN_PROGRESS21 / VERIFY4**。すべて旧確認値で、最新再集計なし。**今回の正式READY統合IDなし／0件**。
- 新規安全拒否 **0**。旧B側HOLD21、10/25未回収原文、過去のOFFLINE-UNSYNCED・旧安全拒否は引き続き未処理。

## 5. KB_CANDIDATE / 正本未同期 / 再開位置

- **KB_CANDIDATE** ID `E-OFFLINE-20261101-09H-T018-T020-G2-BIJECTION-ORDER-01`、E/T018,T020。関連構造体: E+`0x1E8630/34/38`、Side `+0x48/4C/50` と `+0x38/3C/40`、Troop `+0x0C/10/14`。関連先行VA: `0x4E53B0`、CALL sites `0x545A02 / 0x57AD8C / 0x57D982`（すべて**先行研究からの参照**で今回追加したnative解析ではない）。一次出典は上記private GitHub `REF_BATTLE_TAKEOVER.md` blobと前回08h報告SHA。新しい合成fixtureと検証器SHAは同フォルダのreadback台帳参照。
- 候補主旨：G2の全体fixtureでは、Unit lineage/出生イベント・SideとTroopのordinal/identityを別々に照合し、同一record別Unitと同じmember別Troopを潰さない。実原作での1対1対応証拠は未採取。`STATIC=previous only; SYNTHETIC=117/117 PASS; INFERRED=comparison hazard; DYNAMIC=0; Golden=0; READY=0`。
- 接続障害ID：`E-CONN-20261101-09H-LOCAL-SSE-429-01`。試行内容：Local Compactで既存MASTER/規約/HANDOFF/KB等をread_multiple_files。失敗結果：`UNAVAILABLE / MCP SSE probe returned 429 from openai.org`。保存済み：独立合成研究・監査器・fixture・receipt・readback。未保存：PC MASTER確認/正式統合。影響：最新owner、READY、競合、SOURCE SHA、PC受入条件を未確認。次の許可された手：通常接続が自然に回復した際、MASTER最新版→レーン規約/各HANDOFF→REA保存RUN/E資料→正式READY同一ID/source SHA/所有権/時刻/合意/競合→既統合を確認し、許可範囲内へ一度だけ取り込み可否を判定。
- PC/他レーン/REA/dev_lab/共有knowledge/Git/push/原本EXE/ZIP/SAVE/Work/スケジュールには変更を加えていない。

## 出力

`T018_T020_G2_BIJECTION_ORDER_AUDIT_20261101_09h.md`（本報告）、`t018_t020_roster_bijection_order_gate_20261101_09h.py`、`T018_T020_G2_ROSTER_BIJECTION_FIXTURES_20261101_09h.json`、`T018_T020_G2_ROSTER_BIJECTION_RECEIPT_20261101_09h.json`、`verify_g2_readback_20261101_09h.py`、`T018_T020_G2_ROSTER_BIJECTION_READBACK_20261101_09h.json`。
