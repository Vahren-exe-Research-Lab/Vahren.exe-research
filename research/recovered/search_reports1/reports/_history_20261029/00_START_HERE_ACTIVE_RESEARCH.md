# 【最初に読む】迫真戦記ver0.67 最新解析（2026-10-22 / 第3版）

**CURRENT研究正本：**`Hakushin067_FunctionRepair_20261021.gpr`＋`search_index/HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite`＋`search_index/search_current.py`

> 過去のGhidraや検索DBは削除しない。ただし**古い`search.sqlite`、V2 SQLite、2026-10-21版のAI_OFFLINE_PACKを新規調査の正本にしない。**

## 何が直ったか

- 内部10,274関数、外部188、Ghidraの記録済み全参照243,670件、関数body 11,091区間、PE再配置57,921件を現行Ghidra基準で検索可能。
- 既存の経験値・訓練ABI3件、DATイベント関数の範囲修正、復元6関数を組み込み。**それ以外のABIは未検証**。
- PE再配置旧ラベル156件は前版で訂正済み。
- 新しい第3版は、Ghidraの`UNCONDITIONAL_CALL`51,213件について、**原EXE機械語E8（直接CALL）44,889件とE9/EB（JMP）6,324件を分離**。すべて原EXEの命令バイト・相対分岐先と一致。**JMPが必ず他関数への末尾呼び出しとは限りません。**
- 従来の単語単位検索が部分一致を見落とす問題を修復。`search`=文字列の**部分一致**、`search-token`=FTS5**単語／フレーズ**検索。検索結果には該当箇所付近の抜粋を表示。

## PowerShellでの標準操作

```powershell
$ix='[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
python -B (Join-Path $ix 'verify_active_research_state_v3_20261022.py')
python -B (Join-Path $ix 'search_current.py') stats
python -B (Join-Path $ix 'search_current.py') function 0x004A1250 --max-chars 4000
python -B (Join-Path $ix 'search_current.py') callers 0x004D4A50
python -B (Join-Path $ix 'search_current.py') jump-callers 0x005B6635
python -B (Join-Path $ix 'search_current.py') flow-callers 0x005B6635
python -B (Join-Path $ix 'search_current.py') search ctx_ea
python -B (Join-Path $ix 'search_current.py') search-token ctx_eax
python -B (Join-Path $ix 'search_current.py') abi 0x00551E50
```

`callers`/`callees`は**E8直接CALLのみ**。E9/EBは`jump-callers`/`jump-callees`に分離。`flow-callers`は両方を区別して表示。DLLフックを設計する時は、戻り値・レジスタ入力・例外処理・スタック解放をさらに確認する。

## 元データの取り扱い

- 元原作EXE、DAT、セーブ、Ghidraの`Hakushin067_Index`、古いSQLite／Pseudoc、研究A〜E／Stage5正本、MASTERは変更・削除しない。
- `HAKUSHIN067_CURRENT_CANONICAL_V2_20261022.sqlite`は今回の比較元の旧現行版、V3は別名の独立DB。`search_current_V2_20261022_ARCHIVED.py`も保存。
- **ユーザーが検証した雇用画面V2は失敗している。** 解析基盤の修正とゲーム本体の修復は別案件。
- 機械解析の全関数が修復済みという意味ではない。まだ未所属E8や動的CALLが残る。推測でcallerを捏造しない。
- 関数`0x0048D6A0`は元Ghidraで`RET 0x0048EA5A`まで既に登録済み。旧Stage5の「Ghidra終端欠落」は分割関数範囲の誤認。
- 最新の`CURRENT_ACTIVE_RESEARCH_STATE_V3_20261022.json`がACTIVE指標。`verify_active_research_state_v3_20261022.py`が合格してから解析する。古い検証器が`STALE`を報告することは現行V3の不具合を意味しない。

**STATIC VERIFIED ≠ GAME RUNTIME VERIFIED。**
