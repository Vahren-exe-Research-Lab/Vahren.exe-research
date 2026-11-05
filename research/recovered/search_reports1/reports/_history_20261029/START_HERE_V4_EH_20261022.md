# 【現行V4】迫真戦記ver0.67 解析入口 — 2026-10-22

最初に `CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json` を読み、指定された版のマニフェストと検証器を確認してください。

| 用途 | 現行 |
| --- | --- |
| Ghidra | `Hakushin067_EHRepair_20261022.gpr` |
| 統合SQLite | `HAKUSHIN067_CURRENT_CANONICAL_V4_EH_20261022.sqlite` |
| 検索CLI | `search_current.py` |
| 版固定の根拠 | `CURRENT_ACTIVE_RESEARCH_STATE_V4_EH_20261022.json` |
| PC検証 | `verify_active_v4_eh_20261022.py` |
| オフライン検証 | `verify_offline_v4_eh_20261022.py` |

## 今回の修復

元EXEの命令、ハンドラ登録のPUSH、FH3例外処理テーブルを照合して、未登録だった**952個のコンパイラ例外処理ハンドラ**を別関数として復元しました。以前のゲーム関数へ無理に結合していません。

- 内部関数11,226、外部188、合計11,414。増加分はコンパイラの補助処理であり、ゲーム機能が952個解明されたという意味ではありません。
- 952個すべてGhidraを開き直して再確認・再逆コンパイル済み。
- 未所属E8直接CALLは2,040→635件、未所属E9 JMPは984→32件。
- Ghidraの参照総数243,670、原PEの再配置57,921は維持。所属更新3,309参照とPE関連の所属2,043件を再抽出結果へ同期。
- 以前のABI修正3件、イベント関数の修復、復元6関数、ゲーム部分の旧擬似C・関数範囲を保持。

## 誤用防止

**例外処理ハンドラの登録関係は、普通のCALLやDLLから呼べる関数宣言ではありません。** `analysis_role=COMPILER_FH3_HANDLER` はゲーム機能とは区別し、ネイティブABIは未検証として扱います。全体で検証済みABIは引き続き3件だけです。

`callers`/`callees`は原PEのE8のみ。`jump-callers`はE9/EB、`flow-callers`は両方を区別して表示します。`search`は部分一致、`search-token`はFTS5単語検索です。

例：`python -B search_current.py function 0x005E7988` でEHハンドラと登録元の静的証拠を確認できます。

## 保存方針

`Hakushin067_FunctionRepair_20261021`、旧V3/V2検索DB・旧ZIPは差分再現用として残します。元EXE、DAT、セーブ、初期Ghidra、他レーン、MASTERは変更しません。旧版を現行だと誤認しないでください。

雇用画面V2はユーザーの実機確認で失敗しています。この解析修復はその不具合を直したものではありません。ゲームの起動、DLLの注入、戦闘録画器の変更は行っていません。

**STATIC VERIFIED ≠ GAME RUNTIME VERIFIED。** 635件の未所属E8や動的CALL先、追加ABIは引き続き調査対象です。
