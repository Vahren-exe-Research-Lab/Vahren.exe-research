# 迫真戦記 新E｜dialog呼出wrapperの5経路別指紋とT018 Golden証拠系譜ゲート

- 研究ID：`E-OFFLINE-20261028-1949-T020-DIALOG-WRAPPER-FINGERPRINT-AND-GOLDEN-LINEAGE-01`
- 時点：2026-10-28 19:49 JST、E担当（T018/T019/T020）。
- 分類：`OFFLINE-UNSYNCED / STATIC INDEX VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY / GAME NOT RUN`。
- 保存先：ChatGPT Library `/迫真戦記/E_OFFLINE_UNSYNCED/`（アップロード・読み戻しの成否は別receipt参照）。Windows MASTERと他owner正本は本runでは未読・未編集。

## 1. 出典・PC接続

Desktop Commander Local Compact を最初に使用したが、研究ルート `[LOCAL_RESEARCH_ROOT]` の `list_directory(depth=1)` が `INVALID_ARGUMENT / McpServerError: Session terminated` で失敗した。**CONNECTION**に分類し、SAFETY_REFUSALとは区別する。PCが実際に電源オフかどうかは未確認。復旧ID `E-RC-20261028-1949-LOCAL-SESSION-TERMINATED-01`。Windows版最新MASTER/所有者/READY/他lane HANDOFF/REA/dev_labの読取・正式統合は今回BLOCKED。

許可された代替経路としてChatGPT Libraryの実ファイル `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を取得し、原本を変更せず `search.sqlite` と `search.py`、スナップショット規約を作業用コピーへ展開した。ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、SQLite `PRAGMA quick_check=ok`。検索DBは `mode=ro&immutable=1`、`PRAGMA query_only=ON` で限定照合。Ghidra/Java自動解析なし。原作EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` はマニフェスト記録値であり、**EXE現物を本runでハッシュ計算していない**。

今回参照したのは2026-10-21のGhidra擬似Cと直接CALL DBである。全て旧スナップショット由来の静的根拠で、原作の実機挙動・仮想関数先・呼出引数実値を確定していない。前回E16:45～18:49の研究文書、比較fixture、Python検証コードを読み戻して重複を確認した。

## 2. 新しいT020静的成果：dialog wrapperは同一構築経路ではない

2026-10-21の直接CALL索引で`0x0043F470`の**直接callerが次の5関数・各1箇所**であることを確認した。前回「5 caller」が既知だったため今回の新規寄与は、各callerの**文字列関連関数の呼出件数と局所後始末の違い**をすべて同じDB/SHAで照合した点にある。

| wrapper VA | dialog CALL site | `0x402710` COPY系 | `0x402800`構築系 | `0x5B6BBB`解放系 | `0x52AD90`初期化系 |
|---|---|---:|---:|---:|---:|
| `0x0052CCF0` | `0x0052CDDE` | 3 | 1 | 3 | 1 |
| `0x0052CE50` | `0x0052CF23` | 1 | 3 | 1 | 1 |
| `0x0052CF50` | `0x0052D047` | 4 | 0 | 4 | 1 |
| `0x0052D2E0` | `0x0052D3B4` | 0 | 4 | 0 | 1 |
| `0x0052D3D0` | `0x0052D4C3` | 1 | 3 | 1 | 1 |

全5関数で`0x52AD90`がdialog呼出に先行する。ただし表内の「COPY」「構築」「解放」は**コード上の用途候補を区別するためのラベル**で、全行の引数・C++オブジェクト型・表示形式が確定した意味ではない。とくに`0x52D2E0`から`0x5B6BBB`への直接CALLが0件であることは、**間接呼出・callee・例外経路を含む全メモリ解放がない証明ではない**。

### 追加発見：`0x0052D3D0`には長さ閾値に応じたポインタ取得の分岐がある

擬似C上、`in_stack_00000018 < 0x10` のとき `pcVar2 = (char *)&param_1`、そうでない場合は `pcVar2=param_1` から進み、`\0` に達するまで走査してから文字列構築へ進む。これは文字列の小容量表現を示唆するが、Ghidraが付けたスタック変数名・入力型が正しいかは不明で、**実際の境界は原作ASM、G0–G4実観測で追加検証が必要**。他4wrapperへのこの分岐の類推はしない。

T020の互換実装で5つを「同じ文面」「同じ4引数」「同じ後始末」「必ず表示される一種類のdialog」として一括処理しない。いずれも`0x0043F470`へ到達しうる**静的なCALL関係**であり、登録成功・コールバック・表示・放浪/傭兵化・World差分とは別の受入項目として管理する。

## 3. 新しいT018 Golden G0/G1/G2証拠系譜ゲート

前回18:49の非空run ID一致ゲートを発展させ、G0・G1・G2の**独立した各証拠record**が共有すべき属性を合成fixtureで検査した。G0の合法UI開戦証拠、G1の戦闘直前未改変SAVE+入力、G2の原作実MAP/三陣営/ordered Troop・Unit・座標について、同一非空run_id・scenario・旧EXE SHA・旧DAT SHAの3段階一致を必須とする。各段階のcapture SHA、有効なSHA形、G1の時刻がG0開戦以前・G2記録がG0以後、攻/防/支援の3つの**別個の陣営ID**、所属陣営に対応した順序連続の配備名簿をそれぞれ検査した。

合成負例には、run ID一致なのに**G1のEXE SHAだけ違う**、同じrun IDでも**G2のscenarioが違う**、三陣営の役割は揃っているが**陣営IDが重複**、Unit名簿のside IDが未登録、順序欠番・重複、SAVE取得が開戦より後、原作未改変性なし、入力・MAP SHA欠落などを含む。

このfixtureは**schema readinessの静的/合成試験のみ**。合成データが形式的に通っても `actual Golden PASS` として計上せず、`native_receipt_verified=true` という自己申告だけでも計上しない。外部採取の一次証拠と真正性チェックは**本テストには実装していない**。G0/G1/G2、G3戦闘結果、G4戦略World差分の旧原作合法実測は引き続きNOT RUN。保存済み`sp16/s16.map`などの候補情報はactual MAP・配備名簿へ流用しない。

## 4. 新規回帰検証、再実行、検証不能域

新規 `T020_DIALOG_WRAPPER_FINGERPRINT_GOLDEN_LINEAGE_CASES_20261028_1949.json` と `t020_dialog_wrapper_fingerprint_golden_lineage_gate_20261028_1949.py` は、5 wrapperの全CALL site/呼出先一対一、コード文字列SHA、呼出件数、`0x52D3D0`の閾値分岐、T018独立receiptの合成ケースをテストする。

- 新規：**58/58 PASS（unittest終了コード0）**。検証種別：`STATIC INDEX / SYNTHETIC EXECUTED`。
- 旧E18:49：36/36 PASS（今回再実行）。旧E17:45：46/46 PASS（再実行）。旧E16:45：28/28 PASS（再実行）。**今回実行の合計168/168 PASS**。13時台の拒否による14件NOT RUNは合算しない。
- 原作Gameplay：**NOT RUN**。新旧actual Golden：**0 PASS**。新旧strict MATCH：**0**。原作DYNAMIC OBSERVED：**0**。
- E18:49のfixtureは原本保持。新しい合成試験の58件を前回の36/46/28件と区別して記録する。過去の説明だけを根拠に原作機械語の新規実測を名乗らない。
- 作業中に新fixtureのschemaを改良した際、旧ゲートとの構造不一致による合成テスト**2件FAIL**、続いて一時的な編集スクリプトの入力誤り**2回**が発生。失敗は一時作業領域に限定され、最終版で **58/58 PASS** を再実行して復旧。復旧ID `E-RC-20261028-1949-LOCAL-TEST-SCHEMA-OTHER-RECOVERED-01`。旧版をREADY扱いせず、新ファイルだけを保存対象とした。

## 5. T019・MASTER・owner/READY・拒否保護

T019の今回調査範囲で新規確定矛盾0件。5 wrapperの文字列構築差は**仕様差候補**であり原作バグや矛盾確定ではない。B14 `decide11`の10/25と登録既定`decide11`の意味の同一性は引き続きVERIFY。GameClear DAT13箇所/TXT2箇所の検索範囲差は既存RESOLVED、`script2`優先順位・phase flag・TXT実読込・`gwrite`復帰は既存VERIFYを継承する（今のT019正本は未読）。

MASTER最終既知の正式状態は**2026-10-28 12時台までの旧値** checkpoint **196**、READY **596（A115/B229/C136/D116）**、34 Task：DONE9 / IN_PROGRESS21 / VERIFY4 / ID重複0。**今回最新MASTERを未読、これらを今回確認値・最新値と主張しない**。今回の正式READY新規統合 **0件（統合IDなし）**。A～D/REAの最新owner・既統合・READY・競合は未確認。本研究IDはE新規だが正式checkpointへ追加しない。

既存安全拒否 `E-RC-20261028-1353-READONLY-PS-SAFETY-01`、`E-RC-20261028-13H-E13-REPORT-APPEND-SAFETY-02`、T018表境界/session-join、T019拒否済みXREF、C T026/T032、D T030 TSV、`0x5710C0`などは全てBLOCKED維持。今回新規安全拒否0件。拒否された操作は別shell/tool/path/Remote/ZIPで再試行していない。2026-10-25 OFFLINE-UNSYNCED成果と最新他レーンとの意味的重複照合未完。Windows MASTER、A～D/REA/dev_lab、原本EXE/ZIP/SAVE、Git/push、Work、設定、他自動化には変更なし。

## 6. 保存・再開

本回のE所有新規文書・比較fixture・実行コード・SHA receiptの4ファイルを独立してLibrary `/迫真戦記/E_OFFLINE_UNSYNCED/` へ保存対象とする。PC復帰後は本IDと10月25日以降未同期IDを**所有権→重複→source SHA→READY→競合→合意**の順で確認し、既存統合IDを除外したものだけ一度正式反映する。拒否済みMASTER複合照合・追記を別経路でリトライしない。

次の研究優先順位は①C-NB02の合法旧原作同一戦闘G0/G1/G2の一次receipt取得、②全5wrapperの呼び出し側実引数と`0x0043F470`の引数マッピングの限定ASM照合、③登録結果・間接CALL・World変化を別々のGolden比較段階にすること。今回本研究はNOT READY、原作旧戦闘を起動していない。
