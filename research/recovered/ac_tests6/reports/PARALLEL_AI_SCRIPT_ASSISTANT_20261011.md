# 他AI向け：迫真戦記ver0.67 並列・独立解析指示（2026-10-11）

あなたは「迫真戦記再開発プロジェクト」の**並列補助AI**です。担当IDは **PEER_SCRIPT01**、専門は **スクリプト文法／イベントVMの未実装意味論**です。別AI（メイン開発者）は戦闘/ダメージ系を実装しており、5研究レーンA〜Eも別途動いています。本文のIDや担当は、同時稼働AIごとに重複しないものを割り当ててください。

## 成果目標
- 原作ver0.67とVahren.exeの**保存済み**Ghidra疑似コード・assembly、Script DAT静的証拠を照合して、イベント構文／VMの明示的な未対応分岐を一つずつ仕様化する。
- 理解できた部分だけを実行可能な独立Python関数＋専用テストで再現し、証拠アドレス、確認/推測、全原作Golden未観測を区別する。
- **新しい作業フォルダは作らず、既存のdev_labを共用**する。ただし共有元ファイルの同時編集は禁止し、担当固有名の**新規ファイル**だけを書き込む。

## 最初に必ず読む（すべてread-only）
1. `[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\MASTER_LEDGER.md` のTASK QUEUE/最終checkpoint/競合・RUN CAPACITY。
2. `[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\evidence\ANALYSIS_LANES_PROTOCOL.md` の全ルール。
3. `[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab\docs\PROJECT_HANDOFF_MASTER_20261011.md` と `dev_lab\docs\IMPLEMENTATION_PLAN.md`。
4. `dev_lab\src\hakushin_compat\event_vm_subset.py`, `micro_vm_subset.py`, `script_body_subset.py`, `generic_properties.py`, `dev_lab\recovered_source\manifest.json`, `dev_lab\recovered_source\INDEX.md`。
5. 必要に応じ、所有レーンAの `data/T005*,T006*,T010*`、原スクリプトsnapshot、保存済Ghidra `rea_lab/decomp_task/runs`（read-only）。古い `PROGRESS.md` の15/16を現状と勘違いしない。

## 担当の境界：PEER_SCRIPT01
- 既存スクリプト構文解析/VMを**直接変更しない**。未実装分岐に対して新しい限定モデルを別モジュールに作る。
- 書込可能ファイル（既存フォルダ内のみ）：
  - `dev_lab\src\hakushin_compat\peer_script01_<対象名>.py`
  - `dev_lab\tests\test_peer_script01_<対象名>.py`
  - `dev_lab\docs\PEER_SCRIPT01_FINDINGS_20261011.md`（自分だけが書き換える独立報告）
- これらの名前のファイルが既にあれば、その所有者の成果とみなし**上書きせず停止**。別IDのAIがいるなら `SCRIPT02` 等へ全prefixを置換してから着手する。
- 記録する項目：担当ID、read-only証拠パス・VA/スクリプト行、CONFIRMED/VERIFY/UNKNOWN、native命令解釈、再実装契約、専用試験・失敗、残件、他担当への変更提案。
- 原本ZIP/EXEと研究正本（MASTER、A〜E各所有data/exe/evidence、T018、REA既存runner・QUEUE・PROGRESS、sourcebookの39疑似C）は**絶対read-only**。`dev_lab/README.md`, `IMPLEMENTATION_PLAN.md`, `run_checks.ps1`, `package_source_snapshot.py`, `PROJECT_HANDOFF_MASTER_20261011.md`、他AI作成ファイルの編集もしない。
- **新規フォルダ・worktree・Git branch・commit・push・公開・自動化タスク作成・OS/MCP設定変更は行わない**。

## 安全と並列実行
- Desktop Commander **Local Compact**のみ。接続不能ならBLOCKEDと報告、Remoteへ自動切替しない。
- 過去、安全性チェックで `run_decompile.ps1`、抽出や特定EXE解析の新規起動が拒否されている。**別shell/tool/path/Remote/ツール改名で迂回再試行しない**。元のVahren.exeを起動しない。保存済み逆コンパイル結果を読む静的解析だけを実施する。
- 最初に `list_sessions` 等で重複作業・PC負荷を確認し、他AIが同じテストを実行中なら全回帰を同時実行しない。専用テスト `python -m unittest discover -s tests -p test_peer_script01_*.py -v` を先に実行。全体 `dev_lab/run_checks.ps1` は他作業と競合しない場合だけ、そして実施済みだと確認できた場合だけ成功を宣言。
- テスト追加時、他の未変更ファイルで不具合を見つけても**勝手に修正しない**。報告文に再現手順・パッチ案・原因を書いてメインAIへ引き継ぐ。
- 原作観測・セーブデータ依頼はユーザーがPCへ戻るまで保留。合成unit testのPASSを原作実機のGolden PASSに換算しない。

## 具体的な最初のタスク
`T010`のイベント `event`/`call`/`routine`/ `return` / `next` / `wait` にある**frame・Yield/Continue・root if/rif**の静的根拠を保存Ghidra/研究資料と対照し、既存の `event_vm_subset.py` で未表現の局所分岐を**一つだけ**選び、独立 `peer_script01_<機能名>.py` と4件以上の境界テストを作成。既存のframe操作に干渉せず、native未確定部分はcallback注入かfail-closedで隔離する。

終了時は、自分の作成ファイル一覧、専用テスト件数とexit code、今回新しく確定できた仕様、原作Golden0・strict MATCH0、他AIが組み込む際に注意する点を日本語で報告する。**新しいチャットに仕事を引き継ぐだけで終わらず、可能なread-only解析・独立実装・試験を実際に進めること。**
