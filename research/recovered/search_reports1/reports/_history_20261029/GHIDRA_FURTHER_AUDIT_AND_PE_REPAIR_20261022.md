# 迫真戦記ver0.67｜Ghidra現行解析の追加監査とPE分類修復（2026-10-22）
- 作業ID: `REDEV-GHIDRA-PE-CANONICAL-V2-20261022`
- 状態：**STATIC VERIFIED / Ghidra READ ONLY / ゲーム実行なし**。
- 現行Ghidra: `Hakushin067_FunctionRepair_20261021.gpr`（**今回の作業では変更なし**）。
- 現行検索DB: `search_index/HAKUSHIN067_CURRENT_CANONICAL_V2_20261022.sqlite`
- SHA256: `20B069B6E002FA0B0098C6BE3BB26F2C6FB971C4D4AC0A717EC109986E7E74BE`
- 検索CLI: `search_index/search_current.py`（第2版へ接続するよう更新済み）。
- PC上の現行版表示: `headless_analysis/00_START_HERE_ACTIVE_RESEARCH.md`
- 現行状態・検証: `CURRENT_ACTIVE_RESEARCH_STATE_20261022.json`, `verify_active_research_state_20261022.py`。

## 発見1：現行DBに旧Ghidra由来のPEメタデータ156件が残存

先行 `HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite` には、PE再配置57,921件分の分類が旧Ghidraプロジェクトのまま収録されていた。修復済みGhidraをread-onlyで開き直し、`HakushinCurrentPERefAudit20261022.java` で57,921件すべて照合した。

**変化したレコードは156件（重複排除）**：
- 150件：PE再配置のソーススロットがイベント関数`0x004A1250`に所属しているのに、旧ラベルではownerがNULL。
- 6件：以前は`.text`未分類とされていたが、現在は復元済みの6関数（例`0x004B65D0`）に含まれる。
- コード単位アンカーの差分1件と型の差分1件も確認。156件と重複する。
- Ghidraが確認できるXREFの有無`NO_GHIDRA_XREF`は711件で変化なし。
- PE再配置の**参照スロット・アドレス値**は57,921件すべて変更なし。

## 修復方法と独立検査

旧DBをそのまま保全し、**第2版SQLiteを別名で作成**した。`pe_relocations`には修復済みの所有関数・分類・コード単位を反映、`pe_relocation_label_changes`で旧値と新値156件の比較を保持。`ghidra_snapshot_project`を全57,921件に明示した。

独立検査の合格項目：
- Ghidra参照243,670件・全関数10,462件・関数範囲11,091件・検証済みABI3件・旧文字列4,298件・未解決制御命令5,145件・FTS全文索引10,462件は**全行不変**。
- PE再配置57,921件を原EXE由来のスロットデータおよび修復後Ghidra JSONLと**全件照合**。
- 修復後「未分類 `.text` を指す再配置」**81件**（旧87件から6件訂正）。この81件が真の関数かどうかはまだ未確定。
- SQLite `integrity_check=ok`、元の旧DB・元EXE・修復済みGhidraプロジェクト不変。
- 現行版のCLI検索14/14テスト合格、現行状態検証器PASS（エラー0件）。

## 残る未解決箇所の分類

現在のGhidra参照243,670件のうち、`source_function_va=NULL`が22,478レコード。ただしこのうち**15,991件は正常なデータオブジェクトからの参照**（先頭4,358＋内部11,633）なので、関数未解決と同一視しない。
- 命令開始位置からの関数未所属参照：**6,487件（6,413の異なる参照元アドレス）**。
- このうち未所属の通常直接CALL **3,024件**、computed CALL13件。大半は`0x005Exxxx～0x0060xxxx`に集中。
- 呼出先・分岐先が未確定の制御命令5,145件（CALL5,141、INT3特殊終端4）。間接CALLの実ターゲットを推測で追加しない。
- 分割された関数本体はGhidraの正しい機能の場合がある。元Ghidraでも532関数は複数範囲を持つ。サイズだけで欠損と判断しない。
- 次の優先度：高密度の未所属コード領域を親関数の制御フローと照合し、例外処理・catch関数を避けながら**局所的なGhidra複製修復**を試す。全レーン一括再解析や未確認ABIの書き換えはしない。

## 旧版の扱い

- `HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite`、`search_current_20261021_ARCHIVED.py`、20261021版案内は歴史的資産として別名保管。
- 元の`Hakushin067_Index.gpr`、旧`search.sqlite`、原本EXE、DAT、セーブ、MASTER、他レーンの資料には手を加えていない。
- 現行CLIとROOT案内は20261022を示すよう更新したため、**20261021の旧検証器はスナップショット不一致を返す可能性がある**。現行確認には20261022版を使う。
- 解析修復は雇用画面V2（実機で失敗済み）の動作修正ではない。戦闘フックを実機で安全に動かせるという保証もない。

## 再検証（PowerShell）

```powershell
$ix='[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
python -B (Join-Path $ix 'verify_active_research_state_20261022.py')
python -B (Join-Path $ix 'search_current.py') stats
python -B (Join-Path $ix 'search_current.py') pe-to 0x004B65D0
python -B (Join-Path $ix 'search_current.py') callers 0x004D4A50
python -B (Join-Path $ix 'test_current_cli_v2_20261022.py')
```

**今後のAIは必ず`CURRENT_ACTIVE_RESEARCH_STATE_20261022.json`を最初に確認してください。** 未検証の研究結果を既成事実として再利用しないこと。
