# 迫真戦記ver0.67 全参照の棚卸しと一括索引復旧（2026-10-21 JST）
- 作業ID: `REDEV-REF-CENSUS-BULK-20261021`
- 状態: **STATIC VERIFIED / Ghidra read-only / 復旧済み（Ghidra認識済み参照に限定）**
- 現時点の未完了: PC版ゲーム実行観測、間接CALL先の全解決、関数に属さない命令のCFG所有者復元、未解析機械語の到達可能性判定。
- 原本EXE、元Ghidraプロジェクト、旧search.sqlite、既存V2/V3索引、MASTER、Work管理コード、原作DAT/SAVEを変更していない。
- 旧EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- 旧search.sqlite SHA256（監査前後一致）: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`
- **新しい完全参照索引**: `REFERENCE_INDEX_COMPLETE_AUDITED_20261021.sqlite`、SHA256 `DEAAB8580232AD88EF45B18F52518D05363FF9DCA7A87BEA62050EFC0443ADC0`

## 全量監査の結果
- Ghidra記録済み参照: 243,665件、参照元238,917箇所。
- Ghidra全参照の抽出を別プログラムと突合し、保存索引243,665行と**行単位で全件一致／不一致0**。
- 前版までに未収録だった65,299件の内訳: 条件JMP49,652、無条件JMP11,287、計算JMP864、計算CALL3,492、特殊計算CALL終端3、間接参照1。
- 前版の直接CALL／CALL相当JMP／コード→データ／データ内部参照は新Ghidra原本との差分0（既存178,366レコード）。
- Ghidra登録の`UNCONDITIONAL_CALL` 51,212件（E8直接CALL44,888件＋CALL相当JMP6,324件）を取得。
- コードからのデータ参照111,163、定義済みデータ先頭4,358、データ内部11,633。分岐参照は分類を保った。
- 同じ(site,target,reference_type)を持つ正規参照が2件存在：`0x005E0423` → `Stack[-0x64]` (`DATA`)。重複排除によって1件消さず、独立した`ref_id`で2件とも保存。

## 機械語・CFGの残留課題（索引の確定参照に混入させない）
- .text 2,129,920バイトのうち、命令2,078,543、定義データ3,890、未分類47,487（計5,483区間）。
- 未分類域に生のE8候補67。39は既知命令アドレスへ相対分岐し、47は未分類区間先頭からCapstoneで線形逆アセンブルしたCALL境界に一致。
- ゲーム実行中の到達・正しい関数境界は未確認。上記67件を`unverified_raw_e8`テーブルにだけ収録し、`ghidra_refs`の確定CALLには加えない。
- Ghidra参照の未分類.text向け15件はDATA参照で、同領域へのGhidra記録済みフロー参照は0。これだけで非到達を証明しない。
- Ghidra関数未所属の命令18,388。以前補完した関数未所属のE8直接CALL2,678件について関数所有者はnull維持。
- 未解決制御命令5,144件は`indirect_unresolved`へ保管。実行時の関数ポインタ・仮想CALLの到達先は推測で埋めない。
- 元の10,268内部関数と188外部関数（旧DB計10,456）は変更・再解析していない。

## 参照方法（既存search.pyは元DBのまま）
PowerShellで以下を使用：
```powershell
$ix='[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
python -B (Join-Path $ix 'query_complete_reference_index_20261021.py') stats
python -B (Join-Path $ix 'query_complete_reference_index_20261021.py') to 0x004D4A50 --limit 20
python -B (Join-Path $ix 'query_complete_reference_index_20261021.py') from 0x004A5B28
python -B (Join-Path $ix 'query_complete_reference_index_20261021.py') function 0x004A1250
python -B (Join-Path $ix 'query_complete_reference_index_20261021.py') indirect --limit 20
python -B (Join-Path $ix 'query_complete_reference_index_20261021.py') unknown-e8 --limit 20
```
- `0x004D4A50`へのCALLは8件（旧6件＋`0x004A5B28`, `0x004A5B54`）が検索結果に存在。
- `function 0x004A1250`では関数未所属CALL2件は出ない。別途`to`で個々のアドレスを参照する（関数所有者を創作しない）。

## 検証・保全
- 元Ghidraプロジェクトは `-noanalysis -readOnly -max-cpu 2` で参照。
- Ghidra全613,083命令／RefSource238,917／全参照243,665を2方式で一致検証。
- 元EXE上E8相対CALL44,888件のバイト・呼出先完全一致（別V2 raw PE監査）。
- 新索引 `PRAGMA quick_check=ok`、243,665行を出典JSONLから1件ずつ独立再読して**全行一致**、旧DB統計7テーブルを再確認。
- 雇用画面再描画関数`0x004D4A50`参照8件、`reloadMenu`分岐内の新規2件を検索実行で再確認。
- ソースファイルハッシュ全件不変。Ghidra認識外の機械語やゲーム実行時の動作を「完成」とはしない。
- 元の`search.py`や`search.sqlite`は自動更新されない。以後の全参照確認は**新しいquery CLI**を使用。
- 復旧ID: `REF-RC-20261021-VALIDATOR-NULL-KEY-01`。独立検証でGsonがNULLフィールドを省略したため初回KeyError、検証器のみ`dict.get`へ修正し全件PASS（原DB／製品コードへの影響0）。
- 担当所有範囲のMASTER／Workキュー／他レーン資料は書き換えていない。これらへ正式統合する場合は担当者が最新版・重複・所有者を照合する。
- 次の研究: 非所属CALLの関数CFG所有者決定、実際の未分類コード候補の局所検証、間接ディスパッチ復元、V2雇用UIの実機確認。別個のP0／研究対象であり本索引の完了と混同しない。

