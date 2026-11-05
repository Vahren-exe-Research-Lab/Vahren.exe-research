# 迫真戦記 ver0.67｜Ghidra関数終端の誤解に対する訂正・全関数範囲監査
- 調査ID: `REDEV-GHIDRA-BODY-GEOMETRY-20261021`
- 日付: 2026-10-21 JST
- 判定: **元Ghidraの0x0048D6A0終端欠落という報告はFALSE POSITIVE**。
- 対象原作EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 既存検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。ともに変更なし。
- 原Ghidraプロジェクト `Hakushin067_Index` を `-noanalysis -readOnly` で実際に開き、関数本体を直接確認した。Ghidraプロジェクト、EXE、DAT、セーブ、MASTER、他レーンのStage5正本は変更していない。

## 0x0048D6A0 の真のGhidra関数本体（元のプロジェクトで実証）
- Ghidra `Function.getBody().getNumAddresses()` = 5,016バイト。
- **範囲は連続していない**。第1区間 `0x0048D6A0..0x0048E964`（4,805バイト）、第2区間 `0x0048E988..0x0048EA5A`（211バイト）。
- `Function.getBody().getMaxAddress()` = **`0x0048EA5A`**。`FunctionManager.getFunctionContaining(0x0048EA5A)` は既に `0x0048D6A0` を返す。
- `0x0048EA42`（FS:[0]の復元）、`0x0048EA52`（`__security_check_cookie`）、`0x0048EA57`（ESP復元）、`0x0048EA5A`（`C3 RET`）は全てGhidraの同関数内部で認識済み。
- `0x0048EA5B` は関数外、`0x0048EA60` は次関数の入口。例外処理／分割区間を維持した正しい登録である。
- `entry 0x0048D6A0 + size 0x1398 - 1 = 0x0048EA37` は**存在しない「仮の連続終端」**。Stage5が採用した `0x0048EA38` は単に `entry + 5016` の値で、Ghidraから取得した本当の関数終端ではない。
- 元の保存済みGhidra擬似C末尾にも例外チェーン復元・cookie検証・returnが既に存在した。この関数には**Ghidra境界修正を行わないこと**。

## 問題となったStage5記録（所有者へ訂正依頼）
- `battle_scene_builder_epilogue_extended_20261021.py` は`body_bytes_exported=5016`に基づいて`exported_body_end_va=0x0048EA38`をハードコード。Ghidra Function.getBody()の分割区間を確認していない。
- `BATTLE_SCENE_BUILDER_EXTENDED_EPILOGUE_PE_20261021.json` の `status: STATIC ORIGINAL PE / Ghidra BODY BOUNDARY OVERFLOW` は誤った判定名。
- `BATTLE_BRIDGE_STAGE5_VALIDATION_V2_20261021.json` の合格項目 `ghidra_declared_end_short=true`、`actual_ret_outside_ghidra=true` は不成立。Stage5全21テストのうちこの2つの根拠を撤回・正しい境界検証へ置換する必要がある（他19項目を自動的に不合格とみなす意味ではない）。
- PE実バイトに復帰命令がある事実や `RET`・ECX関連のABI研究自体は否定しない。別途native hook実機検証は未実施。
- Stage5の資料や他レーン所有ファイルは**本チャットから書き換えていない**。Stage5担当が本資料を受け取って元の結論／チェック名を更新すること。

## 全関数範囲を再検査した結果
- 元Ghidra内部関数10,268件を全件読取。多区間関数**532件**／関数本体区間総数11,083。
- **365件**は実際のRETが「入口＋size_bytes」から計算した仮終端を越える。これをGhidraの境界不具合と判定してはいけない。
- 例外として`0x005B7240`の`_strchr`は関数本体の最小アドレスが`0x005B7230`で、入口が最小アドレスとは限らない。
- `getBody().getNumAddresses()`は本体の全区間に含まれるバイト数、**最大番地や連続スパン長ではない**。正しい計算はGhidra API `getBody().getAddressRanges()`、`getBody().getMaxAddress()`、`contains(addr)`。
- 調査した全10,268関数で既存`search.sqlite`の`size_bytes`と実Ghidraの本体バイト数は一致。元Ghidra自身のサイズ値は壊れておらず、下流での意味解釈が問題。
- Ghidraの別の本当の解析漏れ（例: DATイベント`0x004A1250`からのswitch分岐先がGhidra関数体から漏れた問題）は、この「分割bodyの正しい例」と混同しない。前者は既に修復用複製プロジェクトで修正・再検証済み。

## 修正済み検索資産（非破壊）
- `ALL_FUNCTION_BODY_RANGES_ORIGINAL_20261021.jsonl`: Ghidraから直接抽出した10,268件の本体区間、RET位置、幅、隙間。
- `FUNCTION_BODY_GEOMETRY_ORIGINAL_20261021.sqlite`: 元DBはそのまま、関数・各区間の検索を追加した独立索引。SHA256 `0046D26E41D5A0E7D6C942F9D8EAF67A5A2F7F9D14B77DE02921AAF5D43D7571`。
- `BATTLE_INIT_ORIGINAL_GHIDRA_BODY_AUDIT_20261021.json`: 元Ghidraの正確な2区間／RET所属証拠。
- `BATTLE_INIT_GHIDRA_END_CORRECTION_20261021.json`: 誤判定を検出する再発防止検証JSON。
- `BATTLE_INIT_SCENE_NATIVE_ABI_20261021.json`: 原作機械語のECX準備・RET、静的根拠。フックの実機合格ではない。
- `query_function_body_geometry_20261021.py`: 正しい範囲によるアドレス検索、関数検索、統計。
- `validate_battle_init_geometry_correction_20261021.py`: 元PE、元Ghidra JSON、全関数range DB、Stage5誤判定を機械的照合してPASS。
- 本件で「元Ghidraプロジェクト内0x48D6A0を修正」する必要はない。元のFUNCTION_INDEXや`search.sqlite`を再生成する必要もない。

## 使用方法（Windows）
```powershell
$ix='[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\headless_analysis\search_index'
python -B (Join-Path $ix 'query_function_body_geometry_20261021.py') stats
python -B (Join-Path $ix 'query_function_body_geometry_20261021.py') function 0x0048D6A0
python -B (Join-Path $ix 'query_function_body_geometry_20261021.py') containing 0x0048EA5A
python -B (Join-Path $ix 'validate_battle_init_geometry_correction_20261021.py')
```

## 状態・残課題
- `GHIDRA_ABI`: 呼び出し元`0x004B99C7`で`LEA ECX,[ESI+0x504]`、`0x004B99CD`で`CALL 0x0048D6A0`、関数末尾は`RET`（即値解放なし）。全て原PEから確認。完全な呼出し規約・他の間接caller・動作上の呼び出し安全性は未検証。
- `CONFIRMED`: 0x0048D6A0の関数終端漏れという報告はfalse positive。スクリプト`battle_scene_builder_epilogue_extended_20261021.py`の推論式が問題。
- `FIXED`: 10,268件の実区間を保持したsidecar SQLiteと検索CLI・検証器を保存。既存DBやGhidra本体を変更することなく誤解を防止。
- `TODO`: Stage5担当者が以前の2つの不正確なPASS条件を改訂し、正しい区間APIを使用するよう実装・記録を変更。
- `RECOVERED`: 調査途中、PowerShell引用符・逆アセンブル開始位置の違いでローカル検証スクリプト初回失敗。専用Python/正確な命令開始位置で再試行成功。元ファイル・研究正本への影響なし。
- `NOT_RUN`: 元ゲームを実行したDLLフック、実機Golden比較、動的関数ポインタ、未分類コードの到達判定。
- 担当所有範囲外のMASTER、Stage5、戦闘開発コード、Work成果は変更しない。

