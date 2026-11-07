# 【最初に読む】迫真戦記 ver0.67 解析資産の現行指定（2026-10-21）

## 重要：旧Ghidra・旧DBを最新版と取り違えないこと

このフォルダ内には履歴再現のため古い解析も保存している。**古いものは削除しないが、新しいフック実装や関数調査に直接採用しない。**

| 資産 | 状態 | 正しい使い方 |
| --- | --- | --- |
| `Hakushin067_FunctionRepair_20261021.gpr` | **ACTIVE／修復済みGhidra（ただし全件修復ではない）** | 新規の静的解析はここから開始 |
| `Hakushin067_ABI_Fixed_20261021.gpr` | LEGACY／3 ABIのみ修復した途中版 | 修正履歴の再現だけ |
| `Hakushin067_Index.gpr` | LEGACY／未修復の元Ghidra | 機械解析の原本・差分比較専用 |
| `search_index/HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite` | **ACTIVE／検索用統合SQLite** | 修復済み関数・参照・ABIの優先情報 |
| `search_index/search_current.py` | **ACTIVE／検索CLI** | AI・他レーンにまず渡す |
| `search_index/search.sqlite` / `search_index/search.py` | LEGACY／2026-10-20の初期DBとCLI | 旧解析の再現用。新規調査の最終根拠には使わない |
| `search_index/REFERENCE_INDEX_V4_20261021.sqlite` / `REFERENCE_INDEX_AUDITED_WITH_PE_20261021.sqlite` | HISTORICAL／修復前の参照所有者 | 複製プロジェクト修復前の比較用 |
| `full_pseudoc_20261020/`、以前のAI_OFFLINE_PACK | LEGACY／10,268元関数の擬似C | 証拠・履歴保存。修正済み10件の代替には使わない |

## 操作コマンド（PowerShell）

```powershell
$ix='[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
python -B (Join-Path $ix 'search_current.py') stats
python -B (Join-Path $ix 'search_current.py') function 0x004A1250 --max-chars 5000
python -B (Join-Path $ix 'search_current.py') callers 0x004D4A50
python -B (Join-Path $ix 'search_current.py') abi 0x00551E50
python -B (Join-Path $ix 'search_current.py') owner 0x004A5B28
python -B (Join-Path $ix 'verify_active_research_state_20261021.py')
```

## 根拠・変更範囲

- 内部関数 10,274 = 元10,268＋未登録6件。外部関数188件はそのまま。
- 修正済み擬似Cは10件（新設6、既存イベント関数1、ABI3）。残りは元Ghidraからの推定擬似C。
- 新Ghidraの全243,670参照と関数区間10,274件は独立全件照合済み。
- `0x004A1250` の関数範囲へ1,107件の参照が対応し、`reloadMenu`の2件 `0x004A5B28 / 0x004A5B54` の所属を回復した。
- 明示的に確認したフックABIは **3関数だけ**。戻り値・EAX特殊引数を含め、他の関数の擬似C署名をDLL関数ポインタとして使わないこと。
- `0x0048D6A0` は元Ghidra自身が `RET 0x0048EA5A` まで認識。以前の「終端欠落」報告は誤判定。元Ghidraの`getBody()`が分割2区間を持つ。
- **雇用画面V2はユーザー実機で失敗済み。** 解析修復がV2の動作成功を意味しない。V2不具合の担当は別チャット。
- 原作EXE、DAT、SAVE、MASTER、研究A〜E/戦闘Stage5の担当所有ファイルは変更していない。

## 複数AIで作業するとき

最初に`search_index/CURRENT_ACTIVE_RESEARCH_STATE_20261021.json`とこの案内を読む。新規調査は`search_current.py`を使い、古い`search.py`だけを見て「存在しない」「参照がない」と結論しない。旧プロジェクトを直接更新しない。解析が変わったら新たな世代のコピー・ハッシュ・検証マニフェストを作り、ACTIVE指定を更新する。

`search_index/CURRENT_LEGACY_ENTRYPOINT_AUDIT_20261021.json`には、旧参照先を持つスクリプト・資料を読取専用で列挙した。別レーン所有ファイルを一括置換しないこと。

**これは静的解析基盤の現行指定。原作実機やDLLフックの包括的な安全保証ではない。**
