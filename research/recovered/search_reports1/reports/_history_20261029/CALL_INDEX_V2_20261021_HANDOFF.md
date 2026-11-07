# 迫真戦記ver0.67 CALL索引V2 再抽出と補完（PC実施）
- 作業ID: REDEV-CALL-INDEX-V2-20261021
- 実施日: 2026-10-21 JST
- 状態: STATIC VERIFIED / Ghidra READ-ONLY / RAW PE E8 44,888/44,888 PASS / GAME NOT RUN
- 元の EXE、Ghidra プロジェクト、search.sqlite、CALLGRAPH.jsonl、MASTER、各レーン、ゲーム製品コードは変更していない。
- 本回は Ghidra 12.1.4 の `-noanalysis -readOnly` で既存プロジェクトを開き、関数範囲に限定しない新規抽出を実行した。
- EXE: `rea_lab/targets/hakushin067_Vahren.exe` / SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- 旧DB SHA256（処理前後一致）: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`
- 新DB SHA256: `FE721CCA9B35C2584783397B56AC70BB8610F26F0D8B896A2E0FDA5F078FA4C5`

## 確定した欠落原因
既存 `HakushinReferenceExport.java` は `fm.getFunctions(true)` を列挙し、`listing.getInstructions(fn.getBody(),true)` だけを調べる。関数に属さない認識済み命令を取りこぼす。
新Ghidra抽出で `0x004A5B28` と `0x004A5B54` は共に `CALL 0x004D4A50`、flow=UNCONDITIONAL_CALL、Ghidra call refあり、しかし `fm.getFunctionContaining(site)` は両方 null と確認。
原作の機械語でもそれぞれ `e823ef0200` と `e8f7ee0200`、呼び先 `0x004D4A50` を再計算して一致。
これらを「関数0x004A1250に確定所属」とは新DB内で自動設定していない（関数のbody未所属を隠さない）。

## 全体集計
- 全Ghidra認識命令走査: 613,083、うちflow-is-callまたはE8候補56,356。
- 実際のCALLニーモニック50,028件のうちE8直接CALL 44,888、間接/未解決5,140。
- 旧DB直接参照 47,550のうち新しいE8に一致42,210、新たに発見2,678、旧索引だけ5,340。
- 新独立CALL索引の全参照: 50,228件（同一site/targetの重複除去済み）。
- 新規2,678は全件Ghidra関数ownerなし、全件原作EXEバイトのE8相対先とGhidra CALL参照に一致。
- 旧索引だけの5,340は保存している。JMPなどが呼び出し相当扱いされたものもあり、すべて誤解析とは見なさない。
- Ghidra直接参照とE8相対計算の不一致: 0件。
- 旧検索DBは変更なし、新DBのSQLite quick_check=ok、検証JSON=PASS。
## 新たに保存したファイル（いずれも search_index/）
- `HakushinGlobalCallProbeV2_20261021.java`: Ghidra全命令横断抽出用の新規スクリプト
- `GLOBAL_CALLS_V2_20261021.jsonl`: Ghidra認識済みCALL候補の一次保存
- `GLOBAL_CALLS_V2_20261021.script.log` と `*.console.log`: 実行証跡
- `build_call_index_v2_20261021.py`: 旧DBと新抽出の非破壊的マージ
- `CALL_INDEX_V2_20261021.sqlite`: 新しい独立索引、`direct_calls` / `unresolved_indirect` / `metadata`
- `CALL_INDEX_V2_20261021_validation.json`: 補完件数とセンチネル2箇所の証拠
- `audit_call_index_v2_pe_20261021.py` / `CALL_INDEX_V2_20261021_PE_AUDIT.json`: EXE原バイトとの44,888件独立照合
- `query_call_index_v2_20261021.py`: 検索コマンド
- このHANDOFFおよび別途生成する配布ZIP
- 既存ファイルの上書き0。作業結果は独立保存済み。PC以外への完全DB同期は未実施。

## 検索方法
PowerShellで `$ix = '[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'` とした後、
- `python -B (Join-Path $ix 'query_call_index_v2_20261021.py') stats`
- `python -B (Join-Path $ix 'query_call_index_v2_20261021.py') callers 0x004D4A50` → 8箇所（2新規+6既知）。
- `python -B (Join-Path $ix 'query_call_index_v2_20261021.py') callees 0x004A1250`
- `python -B (Join-Path $ix 'query_call_index_v2_20261021.py') unowned --limit 30`

## 重要な制限・次の研究
- 新索引の `GLOBAL_ONLY` の `caller_va = NULL` は意図的。所有関数を推測で埋めない。Ghidraの認識済み命令・EXE機械語という静的証拠であり、実機到達やイベント実行回数は証明していない。
- `LEGACY_ONLY` 5,340は旧Ghidra参照のまま保持。CALLニーモニックでないtailcall/JMPの分類は別途精査。
- Ghidra未認識バイト内のCALLや間接CALLの実ターゲットは未確定。
- 新V2は独立DB。従来の `search.py` は引き続き旧DBを読むため、完全CALL検索には新CLIを使うこと。
- 今後: 関数body外の2,678件をCFG/スイッチテーブルと照合し、根拠に基づきcaller所属を付与する第二段階。元プロジェクト変更や広域再解析は不要。
- V2雇用ソート実装DLLは本研究で変更していない。イベント経由の再描画はゲーム実機で要確認。
