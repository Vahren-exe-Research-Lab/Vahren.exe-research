# 迫真戦記v0.67｜古い解析環境の保管・移行判断（2026-10-21）

## 結論

**原本・古いGhidra・旧SQLite・初期擬似Cを削除・改名・移動しない。** 過去の研究再現、差分比較、修復ロールバックに価値があり、古いスクリプトが絶対パスで依存していることが分かった。急な削除・一括置換は保守上のリスクが高い。

代わりに、正規の現行窓口を **`Hakushin067_FunctionRepair_20261021.gpr` ＋ `search_current.py` ＋ `HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite`** に固定する。将来の新しい研究では必ず `00_START_HERE_ACTIVE_RESEARCH.md` を先に読む。

## 確認済みの古い参照を持つ資料

`CURRENT_LEGACY_ENTRYPOINT_AUDIT_20261021.json` による非破壊走査：
- 旧参照語句を含む資料・スクリプト：**116ファイル**。
- 旧`search.sqlite`が登場：95ファイル。旧`search.py`が登場：28ファイル。
- 旧Ghidra`Hakushin067_Index`が登場：18ファイル。途中版`Hakushin067_ABI_Fixed`が登場：10ファイル。
- 数字はファイル内の文字列出現であり、116ファイルが実際に誤動作するという意味ではない。歴史的説明・正当な差分解析も含む。
- 他レーンの`exp_research_20261021/EXP_*.py`の一部は元DBを直接参照。**現行解析として再実行する前には担当レーンで差分と依存を照合**。勝手に変更しない。
- `headless_analysis/BuildOfflineBundle_20261021.py`は旧検索DB・CLIを梱包するスクリプト。オフラインパックを新たに発行するなら、今回作成した`HAKUSHIN067_CURRENT`系で別のパックを作るべき。
- `RunFullDecomp_20261020.ps1`等の旧Ghidra指定は当時の環境の再現用として必要。機械的な置換禁止。

## 誤認しやすい事実

- 旧`search.sqlite`: 内部10,268／全10,456、Ghidra元の参照一部を保持。修復済み6関数・イベント1,107参照owner復元・ABI新擬似Cがない。
- 現行`HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite`: 内部10,274／全10,462、修復済み10件C、Ghidra現行参照243,670件、正しい関数範囲11,091区間、元EXE PE再配置57,921件、確認済みABI3件。
- 現行の参照は以前のGhidraより**5件増えた**（直接CALL1、条件分岐4）。参照の関数所有者は1,107件回復。
- `0x0048D6A0`のRET`0x0048EA5A`は元Ghidraに登録済み。旧Stage5の2個のテスト名（`ghidra_declared_end_short`と`actual_ret_outside_ghidra`）は誤った仮の終端`entry+size`に基づく。**元Ghidraの誤りではない**。
- 雇用画面V2はユーザー実機で失敗。静的研究の修復をもってゲーム側が修復済みとはしない。

## 運用ルール（他AIに渡す）

1. 最初に`search_index/CURRENT_ACTIVE_RESEARCH_STATE_20261021.json`を読み、`verify_active_research_state_20261021.py`を実行して状態を確認する。
2. `search_current.py`から関数・CALL・データ参照・範囲・検証済みABIを取得する。旧`search.py`単体の結果で「参照なし／未存在」と結論しない。
3. 修復されていない擬似Cは推定であり、DLL化には原EXE機械語・RET解放量・レジスタ引数・戻り値・例外経路の個別認証が必要。
4. 新しい修復は原本Ghidraや現行DBを上書きせず、新しい版数の独立Ghidra複製／SQLite／マニフェストを生成する。
5. 他レーンA〜E・Stage5・MASTER・保存・ゲーム製品コードは担当所有者が最新版照合後に修正。差分を単純にコピー／置換しない。
6. 旧資産の削除検討は、依存スクリプト移行・完全バックアップ・所有者確認・復旧検証が終わってから。それまでは**論理的なLEGACY扱いで保管**。

## 状態

`ACTIVE_STATIC_VERIFIED`。Windows実機で新規DLLフックは未実行。原本ゲーム・セーブ・EXE・DAT・古いGhidra・MASTERは未変更。Project Libraryの引継ぎ資料はガイドに従って扱う。
