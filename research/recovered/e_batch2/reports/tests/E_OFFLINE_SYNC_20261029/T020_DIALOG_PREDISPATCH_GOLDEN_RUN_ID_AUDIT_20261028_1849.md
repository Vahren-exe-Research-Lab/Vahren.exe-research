# 迫真戦記 新E｜dialog登録前の式文字列解決・Golden同一run拘束

- 研究ID: `E-OFFLINE-20261028-1849-T020-PREDIALOG-EXPR-GOLDEN-RUN-ID-GATE-01`
- 実施: `2026-10-28 18:49 JST` / E担当 T018・T019・T020
- 判定: `OFFLINE-UNSYNCED / STATIC INDEX VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY / GAME NOT RUN`
- PC接続: `CONNECTION/RATE_LIMIT`、Desktop Commander Local Compact のread_multiple_filesが `UNAVAILABLE; McpServerError: MCP SSE probe returned 429 from openai.org` で不成立。**安全拒否とは分類しない**。
- 使用原本: ChatGPT Library `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。コピーから読取専用利用。2026-10-21検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` / SQLite `quick_check=ok`。
- 原作EXE: マニフェストの識別値 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。EXE現物の今回再ハッシュ・実行は**していない**。Ghidra/Java再解析も行っていない。
- 研究前に前回E17:45の実資料・T020コード/fixture、2026-10-21スナップショットの分析レーン規約を確認。PCの最新MASTER・A～D HANDOFFは未読。

## 1. 今回新規に確認した静的実装境界

前回E17:45は `0x0043F470` の`decide11`既定文字列と登録結果と間接CALLの違いを確認した。今回の新規照合対象は**登録前の式文字列解決関数 `0x0049C450`**、およびT018 Goldenの同一戦闘IDの比較契約である。

- `0x0052CF50` の `CALL site 0x0052D047 → 0x0043F470`、`0x0043F470` の `0x0043F5A4 → 0x0049C450`、`0x0043F72F → 0x00416E80`、`0x0043F73F → 0x00416B90` を旧DBで確認。`0x0049C450`の直接callerは **8関数・144 CALL**。従ってこの関数を「放浪・傭兵化専用」とは認定しない。
- `0x0043F470` 擬似Cでは `FUN_0049c450(... +0x504, local_2c)` が `in_stack_00000038` による`decide11`分岐より**前**、また`_DAT_0087f6f8=0`と`local_78=*(iVar2+0x20)`、ノード構築・登録より**前**にある。この順序は局所擬似C上の確定。`_DAT_0087f6f8`の値のゲーム上の意味は未確定。
- `0x0049C450` は `param_1+0x14` の非0を見て、`0x0042F860`判定に失敗した場合に`0x0049ECA0`へ進む経路を持つ。次の`local_34`が特殊値か、対象の`+0x28/+0x2C`が空区間であれば`DAT_0068B3A8`を選ぶ。そうでなければ`local_34+0x28`にある先頭ポインタを使う。一方、条件を満たさない側では`param_1+4`を選ぶ。**この3種の入力選択は合成fixtureでモデル化したが、実ゲームでどの経路が発生するかは未観測**。
- `0x0049C450`の出力先文字列相当構造体では`param_3+0x14=0xF`、`param_3+0x10=0`、先頭バイト0をセット後、`FUN_00402710`で文字列相当を複写する。この処理は登録前の入力形成であってダイアログ表示成功ではない。
- `0x0052CF50` のデコンパイルは`FUN_00402710`を4箇所呼ぶが、引数スタック推定だけでは`0x0043F470`の`in_stack_00000038/54`に入る**実バイト値の一対一対応はまだ確定できない**。従って放浪・傭兵化が必ず`decide11`を選ぶという推論は保留。
- `0x0049C450`の処理途中が例外・異常で中断しうることまで含め、上記は**静的到達可能経路**であり、すべての実行でノード登録やコールバックが行われるとはしていない。

### コード文字列SHA256（2026-10-21 Ghidra SQLiteから再算出）

| 関数 | SHA256 |
|---|---|
| `0x0043F470` | `07C974DFCD0D8191E6A7D7B2486BF726AF44472B87873A96A51EA0DB9928F52E` |
| `0x0049C450` | `CCDDAF474CBCB8EBF5F273A418B5B9D4AF2431867DBE3E2F8D50C8A38C248DE5` |
| `0x0052CF50` | `48C20B956C4ECEA1E89E12615D34C2EFD25B6EBEA8BC342EE739F00F1EEF3BC7` |

*注意: 上記は擬似CテキストのSHAであり、原作EXE機械語のSHAではない。間接CALL先・実画面表示は未同定。*

## 2. T020比較fixture・T018同一run強化

新規fixture `T020_DIALOG_PREDISPATCH_CASES_20261028_1849.json` と回帰テスト `t020_dialog_predispatch_golden_run_gate_20261028_1849.py` を作成。

- 直接CALL正例 **7件**、誤結線負例 **4件**、式文字列選択合成ケース **7件**、G0/G1/G2対応付け合成ケース **8件**。SQLite整合・ソースSHA・コード順序・出力構造体初期化・caller数などの静的検証を合わせ、**新規36/36 PASS**。
- T018の追加受入条件: G0/G1/G2の`run_id`が、同じ空欄や単なる`same_battle_key=true`ではなく**非空の同一識別子**で一致すること。未改変SAVE、入力、MAP、三陣営、ordered Troop/Unit、生データSHAとsource rankも別々に必要。run一致・構造だけ満たす**合成例はあくまでschema readiness**で、原作actual Golden PASSではない。今回の負例には、別run混在、全run ID不明、MAP欠落、SHA欠落、変更済みSAVE、出撃名簿不完全を含む。
- 既存のE17:45 **46/46 PASS**、E16:45 **28/28 PASS**も同じZIP由来のDBで再実行。**今回実行の総数110/110 PASS**。13時台の安全拒否によりNOT RUNとなった14 fixtureは数えていない。
- いずれも`STATIC / SYNTHETIC EXECUTED`。原作戦闘・Golden比較runnerの実データ照合は **NOT RUN**。G0/G1/G2の一次証拠は収集していない。

## 3. T019・Golden・MASTER

- 新規確定T019矛盾: **0件**（今回の限定調査範囲）。`decide11`の異なる選択経路の意味一致は`VERIFY`で据置。
- 既知T019: GameClear DAT13箇所/TXT2箇所の字句検索範囲差はRESOLVED、`script2`同名定義優先順位/phase flag/TXT実読込/`gwrite`復帰はVERIFY。**最新T019正本は今回未読**。
- T018: G0合法UIでの開戦、G1同一戦闘直前の未改変SAVE・入力、G2同一戦闘MAP・攻防支援三陣営・ordered Troop/Unit、さらにG3戦闘結果とG4戦略World差分が必要。**今回 DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0**。
- MASTER最終既知正式値（**10/28 12時台の旧確認値に限る**）: checkpoint **196** / READY **596** = A115+B229+C136+D116 / Task **34** = DONE9+IN_PROGRESS21+VERIFY4、ID重複0。**今回はPC正本未読、再確認値ではない**。READY新規正式統合 **0件**、統合IDなし、正本未変更。

## 4. 接続障害・拒否履歴・再開条件

今回の接続障害: `E-RC-20261028-1849-LOCAL-SSE-429-01`。18:49 JST Desktop Commander Local Compact のread_multiple_files要求（MASTER、レーン規約、開発計画の3ファイル）で `MCP SSE probe returned 429 from openai.org`。分類 **CONNECTION/RATE_LIMIT**、安全拒否ではない。未完了: 今回PC正本のcheckpoint・owner・READY・A～D/REA最新HANDOFF確認とPC正本同期。最終成功: 前回17:45 Libraryに保存したE成果と、今回2026-10-21 ZIPの静的調査・36/36合成回帰+過去74/74再検証。PC未保存差分: 本研究のE資料3点。再開: 接続が自然復旧し、拒否対象を再試行せずに許可された最新MASTER/owner/READY/ID重複/競合が確認できる場合のみ二重計上せず正式照合。

今回の新規 **SAFETY_REFUSAL=0**。既存の `E-RC-20261028-1353-READONLY-PS-SAFETY-01`、`E-RC-20261028-13H-E13-REPORT-APPEND-SAFETY-02`、T018表境界・session-join、T019拒否済みXREF、C T026/T032、D T030 TSV、`0x5710C0`などのBLOCKEDを維持。これら拒否済み操作を別tool/shell/path/Remote/ZIPで再試行していない。2026-10-25 OFFLINE-UNSYNCEDと他レーンとの意味的重複照合は未完。

## 5. 優先次手

PCオンライン復旧時に最新E所有T018/T019/T020とA～D/REA HANDOFF、READY/所有権/重複・競合を**許可された方式**で突き合わせる。原作合法UIの同一戦闘からG0・G1・G2のrun_idとバイトハッシュを一次証拠として回収し、G3・G4の対応を確認する。ASMによる`0x0052D047`呼出の実引数対応、`0x0049C450`の入力分岐とダイアログ表示・World反映の関係はVERIFYのまま保留。

**一切変更していないもの:** Windows MASTER、A～D、REA、dev_lab、原作EXE/ZIP/SAVE、Git/push、Work、設定、他自動化。オフライン派生コピーとE所有の新規資料のみ作成。
