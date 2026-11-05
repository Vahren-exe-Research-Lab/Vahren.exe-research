# 迫真戦記 ver0.67｜統合V9 研究入口（2026-10-23）

## 推奨する研究版
**関数検索・戦闘境界調査の新規作業は統合V9を明示的に使用する。**

- SQLite：HAKUSHIN067_UNIFIED_V9_20261023.sqlite
- 検索CLI：search_unified_v9_20261023.py
- 原本SHA・生成物SHA・全カウント：UNIFIED_V9_INTEGRITY_20261023.json
- 非破壊再検証・ビルダー：build_unified_v9_20261023.py
- 分類：STATIC COMPOSITE VERIFIED / STANDALONE / GAME RUNTIME NOT RUN
- **注意：PC標準の search_current.py と CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json は依然V3である。V9へ自動切替済みと扱わない。**

## なぜV9統合が必要か
V4-EHは952コンパイラ例外ハンドラ、V5は初期化・終了登録、V6はPE未所属コード、V7/V8は後続断片を復元した。従来V8の参照記録は243,670件。一方、10月23日の別Ghidra複製 Hakushin067_AtexitTailRepair_20261023 は35個のat-exit/cleanup関数bodyと243,678件の参照を保持。**V8と後日の別Ghidraは枝分かれ**しており、標準V3や古いV8をそのまま最新とすると研究が欠ける。

V9は従来V8のDBをSQLiteバックアップで丸ごと継承し、後日の出典ファイルのSHAを固定して追加修復を融合した。35関数のうち10はV8にも同VA・同bytes・同body rangeで存在するため、元V8定義全文を退避したうえで後日版の命名と疑似Cに更新し、残り25関数のみ新規追加した。

| 項目 | 従来V8 | 統合V9 |
|---|---:|---:|
| 登録関数 | 11,925 | 11,950 |
| Ghidra function_body | 11,737 | 11,762 |
| Function range | 12,557 | 12,582 |
| Ghidra参照 | 243,670 | 243,678 |
| ネイティブ E8/E9/EB 索引 | 51,213 | 51,214 |
| 未所属の記録済み直接E8 | 0 | 0 |
| 未所属の索引対象JMP | 24 | 1 |
| PE再配置 | 57,921 | 57,921 |
| 確認済みABI | 3 | 3 |

- 旧V8参照243,670件の対応を照合し、後日版の追加8件を統合。
- 新しく判明したE8直接CALL 0x00604D7F → 0x005B6BBBの元EXE命令・相対呼出先を照合。
- 既存参照の所有者145件を更新、旧V8側の所有者74件を維持。
- PE再配置全57,921件を照合し、許可できる更新146件のみ適用。
- 旧V8のEH952、初期化/終了登録423、PE-gap66、末尾ポインター3、断片19、ABI3を保存。
- 先行10関数のV8定義は統合DBの unified_v9_atexit_function.original_function_json に保持。後日版の未検証ABIを完成ABIとして宣言しない。

**V9は複数の既存Ghidra分岐を統合したSQLite索引であり、単一のGhidra .gpr自体は新設していない。**

## 調査用コマンド
PCのPowerShellから以下を実行。ゲームの起動・改変は不要。

~~~powershell
$ix = "$HOME\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index"
python -B (Join-Path $ix "build_unified_v9_20261023.py") verify
python -B (Join-Path $ix "search_unified_v9_20261023.py") stats
python -B (Join-Path $ix "search_unified_v9_20261023.py") function 0x00492890 --max-chars 4000
python -B (Join-Path $ix "search_unified_v9_20261023.py") function 0x00493630 --max-chars 4000
python -B (Join-Path $ix "search_unified_v9_20261023.py") function 0x00604D70 --max-chars 4000
python -B (Join-Path $ix "search_unified_v9_20261023.py") callers 0x005B6BBB --limit 20
python -B (Join-Path $ix "search_unified_v9_20261023.py") abi 0x00551E50
~~~

preflight は出典SHAと重複10/追加25の幾何検査。build は新規出力専用で、既存V9 DB・マニフェスト・CLIがある場合は上書きを拒否する。既に構築済みなので普段は verify と検索CLIだけを使用する。

## 実行・読み戻し確認
- preflight：PASS（35のうち既存10は同一幾何、新25は他の関数範囲と衝突なし）。
- build：正常終了、141,033,472バイトの統合SQLiteを作成。
- verify：V9_INDEPENDENT_READBACK_PASS、SQLite quick_check=ok、DB/CLI SHA・主要テーブル件数の一致。
- CLI stats / function 0x00604D70 / callers 0x005B6BBB：統合DBから実データ返却。
- V9 DB SHA256：2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
- CLIの最新SHAはUNIFIED_V9_INTEGRITY_20261023.jsonを参照。
- ゲーム実機でのDLLフック、戦闘往復、Golden、原作互換：未実行・未証明。

## PC標準の旧V3が残る理由
2026-10-22のV4昇格は既存 search_current.py の置換でWinError5（アクセス拒否）となった。今回、当該拒否済み操作を別shell・別tool・ACL変更で迂回していない。従来V3のLATESTポインタ、search_current.py、元Ghidra、V3～V8 DB、元EXE・DAT・MAP・セーブは無変更。**標準ポインタの正式昇格は未完了**と明記する。

標準化には正常な権限・所有者・競合確認、新V9専用validator、他AIが使用する全参照先との更新整合が必要。それまでもV9は別名CLIを使い直ちに研究可能である。

## 他のAI / Workへの重要指示
1. 新規静的関数検索ではV9 CLIを指定。過去レポートの再現は当時の版を保持し、SHAを合わせる。
2. 戦闘入口・出口は BATTLE_TAKEOVER_OBSERVABILITY_CONTRACT_20261023.md、機械可読ゲートは BATTLE_TAKEOVER_OBSERVABILITY_MATRIX_20261023.json、索引は BATTLE_BRIDGE_RESEARCH_INDEX.mdを参照。
3. 新Ghidra 35関数はあくまでAtexit関数の静的復元であり、新しいゲーム操作35種類や安全なDLL ABIの証明ではない。
4. 今後、単一Ghidraプロジェクトも必要なら別の統合・検証作業とする。V8と後発V7AのGhidra分岐を無検証で上書きしない。
5. Work所有コードと共有キュー、E所有MASTER、A～D/REA所有資料を本研究の都合だけで編集しない。

## 次の技術課題
- 正規の管理手順が許可する条件でのみV9をPC標準に昇格し、新manifest/validator・配布オフライン版を更新する。
- 原作戦闘のG1同時点参加名簿・G2安全Task/VM保持・G3外部EXE往復・G4結果一回適用・G5戦略Golden・G6クラッシュ復旧の実証は未完。
