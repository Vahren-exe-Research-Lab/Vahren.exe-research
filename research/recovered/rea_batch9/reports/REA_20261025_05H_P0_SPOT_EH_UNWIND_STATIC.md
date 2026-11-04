# 迫真戦記 ver0.67｜REA 2026-10-25 05時台 P0: Spot初期化例外時のguard巻戻しとEH状態マップ
研究ID：`REA-LOCAL-20261025-0535-P0-SPOT-EH-UNWIND-GUARD-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED=0、原作Golden実測PASS=0。
原作EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
2026-10-21初期検索DB SHA256：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9 SQLite SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 先読・非重複
MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、旧同期ログ（64/64、21 runs、STALE_RENAME_DENIED）、初期検索README/BUILD_MANIFEST/search.sqlite、前回04H報告・JSON・auditを参照した。原作ゲーム、REA、Ghidraは新規実行しない。04Hのatexit破棄対象・例外/NULL差分は既知として再計上しない。

## P0新発見A：例外ハンドラの実際のunwind表
`0x00597BA0` は `0x00597BA2 PUSH 0x005F8B89` でEHハンドラを登録する。`0x005F8B9A MOV EAX,0x006511BC` から、対象FuncInfoは `0x006511BC` と原作PEで確認した。
FuncInfoは magic=`0x19930522`、maxState=2、unwindMap=`0x006511AC`。そこに2項目がある。
- state 0 → toState -1 → `0x005F8B70`：`[0x00B0B0D8] & ~1` を書き戻し、**初期化フラグのbit0だけを解除**。
- state 1 → toState -1 → `0x005F8B7E`：`[EBP-0x10]` を引数に `0x005B6BBB`（free系）を呼び出す。
これは現物のEHメタデータ・機械語による静的解釈。OS/C++例外実行のライブ観測ではない。

## P0新発見B：初期化失敗でguardを戻す経路が存在
`0x00597BF9` がbit0を検査、初回の `0x00597C02` がbit0をセットし、`0x00597C0E` はEH state0を保存する。その後 `0x00597C12` でグローバルhelperコンストラクタを呼ぶ。
よってコンストラクタ（前回04Hで`0x2C`確保失敗→`__CxxThrowException`を確認）が例外送出し、このフレームのEH巻戻しが発生する場合、state0対応の `0x005F8B70` が**guard bit0を解除する**経路を持つ。
コンストラクタが正常復帰して`0x00597C1C`のatexit登録を経た後、`0x00597C24`で状態を-1に戻す。**通常戻り値でのatexit登録失敗を示すEAX判定は、この直後に存在しない。** そのような失敗が実際に起き得るかは未確認。

## P0新発見C：Spot生成中例外用の別cleanup
`0x00597C3D`で0x36C確保、`0x00597C45`で確保結果をローカルに保存、`0x00597C49`でEH state1にする。その後`0x00597C6B`でSpot生成処理を呼ぶ。
state1のunwindエントリは`0x005F8B7E`から`0x005B6BBB`への解放。確保済みメモリの例外時cleanup候補である。EBP基準の保存位置と生成元ポインタの厳密なABI対応、および例外の実到達は追加VERIFY。
通常NULLの分岐と例外巻戻しを混同しない。原作のメモリリークや実際の例外頻度は結論しない。

## アドレス訂正
04H報告の次回対象`0x005F8B71/0x005F8B79`はx86命令の**途中**にあたる。正しい命令先頭は`0x005F8B70`（MOV）と`0x005F8B78`（MOV）であり、関数またはfuncletの開始VAとして71/79を使わない。指示先を訂正したので旧成果を重複再解析しない。

## 独立監査・REA進捗
原作SHA、初期検索DB SHA、V9 SHA、SQLite quick_check、EH FuncInfo/UnwindMap、ASM20命令、直接CALL4件、V9 CALL索引3件、疑似C・ABI状態などを照合し、**37/37 PASS**。失敗した初回検査35/37（監査側のバイト表記・疑似Cラベル期待値誤り）は採用せず、修正後のみ保存。監査検査数は関数数ではない。
新規REA五種 `info/pseudo/assembly/callers/callees` の正式完成は0関数（Ghidra擬似C、部分ASM、索引情報をREA証拠へ自動昇格しない）。過去64件の正式VERIFIEDは旧同期ログの値を維持。今回新規VERIFIED 0件、正式TODO/VERIFY/BLOCKED書込差分 0/0/0、Golden PASS 0、strict MATCH 0、完全複製率未測定。

## Golden候補（DESIGNED / NOT RUN）
(1) helperコンストラクタ例外時にguard bit0が解除され、次の呼出しで初期化を再試行するか。(2) atexitが例外ではなく異常戻り値を返す場合のguardと終了処理登録の状態。(3) Spotコンストラクタ途中で例外が生じる場合に保存済みmalloc領域が解放されるか。(4) 正常経路では初期化guardが保持されるか。いずれも実機検証0件。

## 安全性・障害・保存
PCオンライン、05時台の事前確認でactive.lockなし、Java/Ghidra/REAプロセスなし、空きRAM約15.89GiB。CPU全体負荷と研究全体の所要時間は未測定。監査単体1.15～1.62秒程度。
初期監査2項目は期待値指定の誤り（OTHER）。初回JSON保存では末尾の文字列`\\n`混入によりreadback JSONDecodeError（OTHER / safety refusalではない）。当回の新規監査コードのみを修正し、同じ新規JSONを再生成して別Pythonプロセスで `READBACK True / 37/37 PASS` を確認。記録ID `REA-LOCAL-20261025-05H-EVIDENCE-JSON-LITERAL-01`。
保存対象はREA担当`decomp_task`の新規成果のみ。原本/MASTER/QUEUE/PROGRESS/旧run/A～E/Git/Work/スケジュールは不変更。既拒否VA 0x5710C0..0x571500、既拒否Wave6、0x004BC9C0検索を再試行せず。
次回：EH state1のローカル格納とEBP相対の対応、`0x00597C1C`の戻り値失敗契約、`0x0049E490`の検索ノード+0x28の型をP0として継続。正式なABI確定は未完了。
