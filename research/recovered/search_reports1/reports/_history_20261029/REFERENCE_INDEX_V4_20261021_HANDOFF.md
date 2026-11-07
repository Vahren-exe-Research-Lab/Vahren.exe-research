# 迫真戦記 ver0.67｜CALL・データ参照の取りこぼし独立監査と補修V4
- 作業ID: REDEV-REFERENCE-INDEX-V4-20261021。状態: STATIC VERIFIED / PC LOCAL / GHIDRA READ-ONLY / GAME NOT RUN。
- 目的: 前回V2 CALL補修後の見落としを再調査し、参照索引を非破壊的に補完する。
- 原作EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 元検索DB `search.sqlite` SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（事前事後一致）。
- CALL V2 DB SHA256: FE721CCA9B35C2584783397B56AC70BB8610F26F0D8B896A2E0FDA5F078FA4C5（不変）。
- Reference V3 DB SHA256: C42BD4293E4D92B045BC62C13E412214811B8BB9DF5CE103F33E815A03BEFEB5。
- **最新 Reference V4 DB SHA256: 796AEAB32AE8FC8B288721A292FEC834F6243B515550E5403010BEEF20C88951。**
- いずれも元のGhidraプロジェクトと原作EXEは変更しない。研究A〜E、EのMASTER、Workの製品コード・キューも変更していない。

## Ghidra保存命令の範囲
- `listing.getInstructions(true)` で613,083命令を調査。
- 関数の所属なし命令18,388（計71,162バイト）。元関数内に属する命令からのDATA参照107,934件は旧DBと一致。
- 関数外からの新DATA参照3,229件。コード由来のデータ参照索引は107,934→111,163件。
- CALL E8命令44,888件の元PEバイト・E8相対先は全件一致。
- `JMP/CALL_TERMINATOR` 6,324件のうち旧索引のみに5,340件、V2でも欠けていた984件を補完。
- 984件の新JMPは元PEバイトからE9相対先を再計算し全件一致。既存の5,340件もV3生成時に機械語E9と照合。
- **制御移動の索引**: 直接CALL 44,888 + JMP終端6,324 = 計51,212件。
- 関数ownerがNULLの制御移動3,662件（CALL 2,678・JMP 984）。callerの関数は推測で埋めていない。
- 解決先を与えていない制御命令5,144件: CALL 5,140 + INT3の特殊computed終端4。INT3は実関数呼出しとして扱わない。
## 静的データからの参照も再検査
- `getReferenceSourceIterator(currentProgram.getMemory(),true)` で全参照元238,917アドレスを走査。
- 旧`DATA_POINTER_REFS.jsonl`は定義済みデータ**先頭**からの参照4,358件を保存。新Ghidra確認でも完全一致。
- 定義済みデータの内部オフセットから新たに11,633件を検出。undefined-data-sourceからの追加参照は0件。
- **静的データ由来参照**を4,358+11,633=15,991件へ補完。
- 内部参照には `pointer[21]`、`FuncInfo`、`RTTICompleteObjectLocator`、`UnwindMapEntry` 等が含まれる。
- PEヘッダーやメタデータも含む。全15,991件が関数ポインタであるとは断定しない。
- 例: `MercenaryWnd` vtable `0x00639154` の先頭1件+内部20件=全21スロット検出。
- スロット15/16/17/18の関数は 0x004D78F0/0x004D79C0/0x004D8E40/0x004D9D50。
- `0x004D4A50` への直接CALLは修復後も8件、うち 0x004A5B28 と 0x004A5B54 はowner=NULL。
- 認識済み命令の集計 `.text`の2,129,920バイト中2,078,543バイトが命令として定義済み。差51,377バイトにはpadding/embedded data/未逆アセンブルが混在し得る。未定義コードと断定しない。

## 保存ファイルと検索（すべて同じsearch_index配下）
- **`REFERENCE_INDEX_V4_20261021.sqlite`**：V3を継承した最終独立DB。テーブル `flow_refs`, `data_refs`, `static_data_refs`, `unresolved_control`, `metadata`。SQLite quick_check=ok。
- `query_reference_index_v4_20261021.py`：索引検索CLI（読み取り専用）。`target`, `caller`, `site`, `code_data_target`, `static_data_target`, `root`, `stats`, `unowned`, `unresolved`。
- `REFERENCE_INDEX_V4_20261021_REPORT.json`：SHA・各参照数・先頭/内部参照の区別。
- `REF_COVERAGE_20261021.json` と `REF_COVERAGE_UNOWNED_DATA_20261021.jsonl`：コード領域の独立Ghidra監査結果。
- `DATA_SOURCE_COVERAGE_20261021.json` と `DATA_SOURCE_UNCOVERED_20261021.jsonl`：定義済みデータ内部オフセットの独立Ghidra監査結果。
- `CALL_INDEX_V2_GAP_AUDIT_20261021.json`, `REF_COVERAGE_DEEP_CROSSCHECK_20261021.json`：旧/新照合。
- 機械解析を全部やり直さず、既存Ghidraプロジェクトを `-noanalysis -readOnly` で調査した。

## PowerShell検索例
```powershell
$ix = '[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
python -B (Join-Path $ix 'query_reference_index_v4_20261021.py') stats
python -B (Join-Path $ix 'query_reference_index_v4_20261021.py') target 0x004D4A50
python -B (Join-Path $ix 'query_reference_index_v4_20261021.py') root 0x00639154
python -B (Join-Path $ix 'query_reference_index_v4_20261021.py') unowned --limit 20
```

## 未解決と取り扱い
- **未解決1:** ownerなしの3,662制御移動は関数ベース`caller`検索で取りこぼす。位置`site`または対象`target`検索では捕捉できる。CFG/大規模switch body再構成が必要。
- **未解決2:** 5,140間接CALLについて関数ポインタを追跡できていない。呼び出し先を単純に埋めない。
- **未解決3:** .text認識命令外51,377バイトには未認識コードがあり得る。存在しないとは断言できない。
- **未解決4:** ランタイム可到達性、フックの再入、DLLのABI互換、雇用画面の実機挙動は全てNOT RUN。本索引補修はDLLの動作保証ではない。
- **再開優先:** 3,662のowner候補をswitch table/CFGから識別し確度を付与。その後に間接CALLのターゲット、未認識領域を局所調査。
- **工数節約:** 旧Ghidraプロジェクトから全逆コンパイル再実施は不要。旧`search.py`は旧DBを参照するため、参照探索は新V4 CLIを使う。

## 失敗・復旧履歴（放置禁止）
- `REDEV-CALL-V4-FAIL-SHELL-01`: Python -c のPowerShell引用符ミスでSyntaxError。非書込確認、後続は専用Pythonファイルへ変更して復旧。
- `REDEV-CALL-V4-FAIL-BUILD-01`: V3初回16進数 `0x/0X` 比較バグで停止、途中DBを `REFERENCE_INDEX_V3_20261021_FAILED_ADDR_CASE.sqlite` に隔離。
- `REDEV-CALL-V4-FAIL-BUILD-02`: 4件のINT3をJMPと誤集計して停止、途中DBを `REFERENCE_INDEX_V3_20261021_FAILED_JMP_COUNT.sqlite` に隔離し分類を修正。
- `REDEV-CALL-V4-FAIL-BUILD-03`: 初回V4で旧DATA参照のtarget_data_typeと新しいsource_root_typeを同列に格納していたことを発見。旧成果を `REFERENCE_INDEX_V4_20261021_SUPERSEDED_TYPE_FIELD.*` として隔離、2列に分離して新V4生成・検証済み。
- これらは静的検証器内の実装問題で、原作や旧DBの損傷ではない。失敗した中間ファイルは再利用禁止、正常版V4のみ使用。
- 既存MASTER・レーン正本・Work製品コード未更新。担当所有者による採用・統合は別途必要。

