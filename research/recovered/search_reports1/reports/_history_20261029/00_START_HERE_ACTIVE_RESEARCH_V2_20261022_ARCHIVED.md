# 【必読・現行】迫真戦記 ver0.67 解析・検索の参照先（2026-10-22）

## ACTIVE：修復済みGhidra + PEラベル修正済み検索DB（第2版）

このファイルがPC上の解析入口です。旧Ghidra、旧SQLite、旧擬似C、旧AI_OFFLINE_PACKは削除せず履歴として保存していますが、**新規の解析には現行指定を優先**してください。

| 対象 | **現在の参照先** | 運用 |
| --- | --- | --- |
| Ghidraプロジェクト | `Hakushin067_FunctionRepair_20261021.gpr` | ACTIVE。修復済み6関数・イベントCFG・ABI3件 |
| 検索SQLite | `search_index/HAKUSHIN067_CURRENT_CANONICAL_V2_20261022.sqlite` | **ACTIVE**。PE再配置の旧ラベル156件を修正 |
| 検索CLI | `search_index/search_current.py` | ACTIVE。上記V2 DBへ接続 |
| 検証・マニフェスト | `search_index/CURRENT_ACTIVE_RESEARCH_STATE_20261022.json` | PC本体と同じ内容か検証 |
| 全参照の元Ghidra証拠 | `search_index/CURRENT_REPAIRED_GHIDRA_REFS_20261021.jsonl` | ACTIVEのGhidraで再抽出した全243,670件 |
| 最新PE分類証拠 | `search_index/CURRENT_PE_RELOCATION_GHIDRA_20261022.jsonl` | ACTIVE Ghidraで57,921件を再照合 |

## PowerShell実行例

```powershell
$ix='[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
python -B (Join-Path $ix 'verify_active_research_state_20261022.py')
python -B (Join-Path $ix 'search_current.py') stats
python -B (Join-Path $ix 'search_current.py') function 0x004A1250 --max-chars 7000
python -B (Join-Path $ix 'search_current.py') callers 0x004D4A50
python -B (Join-Path $ix 'search_current.py') abi 0x00551E50
python -B (Join-Path $ix 'search_current.py') pe-to 0x004B65D0
```

## 現行V2の証明範囲

- 全関数10,462件（内部10,274・外部188）、修正済み擬似C10件、Ghidra全参照243,670件、関数区間11,091件、PE再配置57,921件。V1から関数／参照／擬似C／ABI情報は一切変更していません。
- PE再配置の旧メタデータ**156レコード**を修正：参照元owner150件、未分類コード誤表示6件。コード単位anchor／typeの変更1件ずつは既知156件に含まれます。
- 「未分類 .text を指すPE再配置」は元87件から**81件**。6件は修復済み関数先頭であると確認。
- `NO_GHIDRA_XREF`は引き続き711件。PE再配置は「再配置可能なアドレス値」であり、関数ポインタ・CALLであるとは限りません。
- Ghidraに取り込めた関数は**全ての関数ではありません**。呼出規約を機械語で検証したのは3関数のみ。フック作業には各対象関数のABI個別検証が必要です。
- 戦闘初期化 `0x0048D6A0` は元GhidraにRET`0x0048EA5A`まで登録済み。旧Stage5の「欠落」は誤判定。分割2区間の関数サイズを連続サイズと誤解したことが原因です。
- 雇用画面V2は**ユーザーの実機検証で失敗**。今回の解析索引修正は雇用画面のゲーム本体不具合を修正するものではありません。

## 履歴／旧データは残すが正本にしない

- `Hakushin067_Index.gpr` = LEGACY ORIGINAL（未修復）。`Hakushin067_ABI_Fixed_20261021.gpr` = LEGACY途中版。
- `search_index/search.sqlite`と`search.py` = LEGACY初期検索（10,268内部関数／古いCALL所属）。再現用だけ。
- `search_index/HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite` = V1旧PE分類。元ソースとして保存、標準ではない。
- `search_index/search_current_20261021_ARCHIVED.py`および`00_START_HERE_ACTIVE_RESEARCH_20261021_ARCHIVED.md` = 過去の入口の保存版。
- 2026-10-21の`verify_active_research_state_20261021.py`は現行CLI・案内を更新したため、PC上で旧スナップショットとしてSTALEを検出する可能性があります。これはV2更新による意図した差異です。**現行確認には20261022版の検証器を使ってください。**
- 他レーンA〜E、Work所有ファイル、旧Stage5資料の旧パス参照は一括置換しません。既存の116ファイルの言及は`CURRENT_LEGACY_ENTRYPOINT_AUDIT_20261021.json`に記録済みです。

## 保護・次回更新規則

原EXE・原Ghidra・既存SQLite・DAT・SAVE・MASTER・Workキューは上書き禁止。新しい解析結果が生じたら**新規バージョンのプロジェクト／DB／マニフェスト**を作り、全行・SHA・元の範囲を照合した後だけACTIVEを切り替えます。

**STATIC VERIFIED ≠ GAME RUNTIME VERIFIED。** PCがオフラインのときは最新版オフライン研究ZIPを参照し、古いパックを誤って再発行しないでください。
