# 迫真戦記 ver0.67 — AI検索基盤
Task ID: HAKUSHIN-AI-SEARCH-20261021

対象: ver0.67 同梱 hakushin067_Vahren.exe。SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。

このフォルダはすべて派生した検索成果を保存します。原本EXE、既存Ghidraプロジェクト、10,268件の擬似Cファイル、MASTER、REAキュー、研究A〜E、Gitは変更していません。

- search.sqlite: SQLite FTS5全文検索。Python標準sqlite3で使用可能。
- search.py: オフラインのJSON/Markdown出力CLI。外部AI/APIへ通信しません。
- build_index.py: 元ファイルからDBを再生成。既存DBを置換するときは --replace-derived。
- selftest.py と test_report.json: 統合テスト、元の全10,268ソースの一致チェック。
- DB_BUILD_RESULT.json / GHIDRA_EXPORT_STATUS.json: 検証済み件数・原本識別・所要時間。
- CALLGRAPH.jsonl: 直接CALL参照、間接呼び出し候補、未解決CALLを分離した内部全関数のグラフ。
- DATA_REFS.jsonl / DATA_POINTER_REFS.jsonl: コードと静的データからの非CALLデータ参照。
- STRING_INDEX.jsonl: Ghidraで定義済み文字列と型/デコード状態。
- SYMBOLS.jsonl: Ghidraのシンボルと名前に基づくRTTI/vtableの候補フラグ。
- TASK_LEDGER.md: 進捗と中断・再開ポイント。
## PowerShell使用例

    cd '[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
    python .\search.py stats
    python .\search.py function 0x575DF0 --limit 12 --max-chars 20000 --format json
    python .\search.py function 0x575A60 --limit 8 --max-chars 6000 --format markdown
    python .\search.py callers 0x5684B0 --limit 20
    python .\search.py callees 0x575DF0 --limit 20
    python .\search.py related 0x575DF0 --depth 2 --limit 30
    python .\search.py search 'param_1' --limit 8
    python .\search.py search '0x40ED80' --limit 8
    python .\search.py name 'FUN_00575' --limit 12
    python .\search.py strings 'generic' --limit 10
    python .\search.py symbols 'vftable' --limit 10
    python .\search.py function 0x00599BD0 --limit 5 --max-chars 180000

--max-chars は返すコード/各文字列の長さ上限（初期14,000、最大1,000,000）。
--limit は出力リスト件数上限（初期12、最大100）。
--depth は関連関数の検索深さ（0〜2）。
--format は json または markdown。--output ファイル名 で新規ファイルに保存可能。既存ファイルには上書きしない。

AIへ渡す際は、まず該当関数と関連1〜2段階を絞り、必要な出力だけを使ってください。
## データの意味・制約

内部関数10,268件には擬似C本文を登録。外部188件にはローカル本文がないため、本文NULLとして登録し、架空のコードを作りません。

calls: GhidraのRefType.isCallでcomputed/indirectでない参照のみ。命令位置はsite_va。indirect_calls: computed CALLまたはP-code CALLINDの候補。仮想呼出し・関数ポインタは未確定であり、対象関数は推測で埋めません。unresolved_calls: 未解決参照を別管理します。data_refsはCALLと区別します。

strings: Ghidraの定義済み文字列のみ。デコード不能ならtextはNULLで、display_representationを保持します。encoding_hintは型由来の仮情報で断定ではありません。RTTI/vtableフラグはシンボル名による機械的分類で、C++構造体の復元ではありません。間接呼出し先の完全解析やゲームの実機Golden比較は未実施です。

Ghidraで確認できた直接呼び出し: 0x575DF0 → 0x5684B0、site 0x575F6C と 0x575F8C（UNCONDITIONAL_CALL）。

## 再生成・再検証

    cd '[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
    python .\selftest.py
    python .\build_index.py --replace-derived
    python .\selftest.py

検索DBだけの再生成はGhidra起動不要。--replace-derived は作成済みと認証できる同じ元SHAの検索DBだけを完成後に差し替えます。未知のDBは拒否します。search.sqlite.building が残っている場合、先行実行状態を確認するまで停止します。

Ghidra情報の再抽出は必要なときだけ RunGhidraReferences.ps1 を使用。-process -noanalysis -readOnly、既存出力があると上書きを拒否します。

ChatGPT・DeepSeek・Kimi・REAにはローカルCLIの実行を許可するか、必要なJSON/Markdownだけ渡してください。外部AIへの自動送信はしません。
