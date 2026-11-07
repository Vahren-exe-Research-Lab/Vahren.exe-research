# 迫真戦記ver0.67 追加監査チェックポイント（2026-10-22）

**作業ID:** REDEV-GHIDRA-PE-CANONICAL-V2-20261022  
**状態:** CURRENT STATIC VERIFIED / GAMEPLAY NOT RUN / ORIGINALS UNMODIFIED

## 現行環境

- 現行Ghidra: `Hakushin067_FunctionRepair_20261021.gpr`（今ターンの変更なし）。
- **現行DB:** `HAKUSHIN067_CURRENT_CANONICAL_V2_20261022.sqlite`  
  SHA256 `20B069B6E002FA0B0098C6BE3BB26F2C6FB971C4D4AC0A717EC109986E7E74BE`
- **現行検索:** `search_current.py`。現在は上記V2を参照。
- **現行マニフェスト:** `CURRENT_ACTIVE_RESEARCH_STATE_20261022.json`。
- **現行検証:** `verify_active_research_state_20261022.py`、エラー0件。
- **最新オフライン検索パック（PCのみ保存）:** `HAKUSHIN067_CURRENT_AI_OFFLINE_PACK_20261022.zip`。25,449,274 bytes、SHA256 `78B637F942F069AA6E49F7D2C0B43BA58F00FD4AC4AB75238A0C24E8688EE0D7`。

## 新たな発見・修正

前の統合DBに、旧Ghidraに基づくPE再配置の古いメタデータが**156レコード**あった。
- 150件：再配置スロットの関数ownerがNULLだが、修復済みGhidraでは `0x004A1250` に属する。
- 6件：関数復元済み `0x004B65D0` 等が、PE表で未分類コードのまま残っていた。
- PEの「未分類 .text」を指す件数は87→81に訂正。参照なし `NO_GHIDRA_XREF` は711件のまま。
- 修復済みGhidraから57,921 PE再配置位置を読み取り専用で再抽出、全件比較。156件の旧新ラベルは`pe_relocation_label_changes`テーブルに保存。
- **旧DBは削除も上書きもしない。** 新DBは新規ファイルとして生成。

## 全体の独立検証

- 旧canonical→V2：関数10,462件、Ghidra参照243,670件、関数範囲11,091件、FTS検索10,462件、ABI3件、旧文字列4,298件、未解決制御命令5,145件は**全行一致**。
- 修復されたPE再配置57,921行は元PEスロットと修復済みGhidra再抽出データに**全行一致**。
- SQLite `PRAGMA integrity_check` PASS。
- 現行検索CLIの14テスト**14/14 PASS**。
- 最新ZIPのCRC・各ファイルSHAを確認。展開後のオフライン検索8テスト**8/8 PASS**。
- 修復済みGhidraの`.rep`内容ハッシュは前回の確認値と一致し、改変なし。
- 元検索DBのSHA256は `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` で不変。

## 次の修正候補（未完了）

- Ghidraの関数所有者が不明な通常直接CALL **3,024件**、集中領域 `0x005Exxxx～0x0060xxxx`。
- Ghidraが実ターゲットを静的に確定できないCALL **5,141件**。別に特殊INT3終端4件。
- ABI認証は3関数のみ。未認証関数を通常のDLLフックに採用しない。
- 雇用画面V2はゲーム実機で失敗済み。別チャットが担当。本監査はゲームの修復ではない。

## 従来の文書を誤用しない

`00_START_HERE_ACTIVE_RESEARCH.md`を2026-10-22版へ切り替え、旧案内・旧CLIは`*_20261021_ARCHIVED.*`として保存。
2026-10-21の旧スナップショット検証器はCLI／案内の変更を検出し、`STALE_OR_INVALID`（終了3）になることを確認。これは**意図した版切替**であり、元ゲーム／旧Ghidra／旧DBの破壊ではない。現行検証器を使う。

## 失敗・未保存・再開位置

- `REDEV-CANONICAL-V2-COUNTER-KEY-01`：V2生成器の初回実行でゼロ件のCounterキー参照がKeyError。メタデータ出力前に停止。コード修正後、再試行・全行検証PASS。ソースDB／EXE変更なし。
- `REDEV-CANONICAL-V2-MANIFEST-WRITE-01`：新manifest生成器の作成時に書込モードの順序を誤った。**専用の新規スクリプトだけ**を正しい内容で再生成し、manifest出力とstateハッシュ検証PASS。
- `REDEV-CURRENT-V2-LIBRARY-SYNC-01`：クラウド向けの小型共有レポート作成時に、コンテナ実行環境が接続エラー。**Libraryへの今回の新パック・新サマリーの同期は未完了**。本PC上の全研究結果・今回のレポートは保存済み。再開時はクラウド側のファイル作成/アップロード環境を確認し、**最新版の現行パック/マニフェストを再同期**する。エラーで元成果を再計算し直さない。
- 本チェックポイントは`search_index`内に書き込み、原EXE、旧Ghidra、旧SQLite、MASTER、他レーン所有ファイルは変更していない。

## 現行検証コマンド

```powershell
$ix='[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
python -B (Join-Path $ix 'verify_active_research_state_20261022.py')
python -B (Join-Path $ix 'search_current.py') stats
python -B (Join-Path $ix 'search_current.py') pe-to 0x004B65D0
```
