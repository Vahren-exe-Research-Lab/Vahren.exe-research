# 迫真戦記 ver0.67｜REA 2026-10-25 06時台 P0 Spot例外フレーム・再試行経路
研究ID：`REA-LOCAL-20261025-0636-P0-SPOT-EH-FRAME-SLOT-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式VERIFIED=0、実機Golden PASS=0。
原作PE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
初期Ghidra検索DB SHA256：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`
統合V9 SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`

## 先読・重複防止と範囲
MASTER_LEDGER・ANALYSIS_LANES_PROTOCOL・REA README/QUEUE/PROGRESS・過去runs・旧progress_sync(20261011T153958076Z)・10/21初期検索README/BUILD_MANIFEST/search.sqliteと05H研究報告/JSON/監査コードを参照。
過去同期ログはWave1～5計64/64・21runを示すが、QUEUE/PROGRESSは既知のrename EPERMによる古い表示。64件を今回の新規数へ加算しない。
検索CLI `function 0x00597BA0`, `callers 0x005A8110`, `callees 0x00597BA0`, `related --depth 2`, `function 0x005B8B1E` を使用。Ghidra・REA・原作ゲームの新規実行なし。既拒否操作の迂回なし。

## 新しい静的成果A：0x00597BA0のローカル保存位置を機械語から算術導出
関数入口ESP=Sとすると、`push -1` / `push handler` / `push FS:[0]` でSEHレコード位置はS-0x0C。
`sub esp,8; push esi; push cookie`の後はESP=S-0x1C。ctor/atexit/malloc各呼出しの引数分は正常にpop/retされ、この位置へ戻る。
- `0x00597C45 MOV [ESP+0x0C],EAX`：malloc結果を **S-0x10** に保存。
- `0x00597C49 MOV [ESP+0x18],1`：EH stateを **S-0x04** に設定。
- `0x005F8B7E MOV EAX,[EBP-0x10]`：unwind funcletがcleanup引数を取得。
- `0x005F8B82 CALL 0x005B6BBB`：その値をfree系に渡す。
この2つのオフセットは、funclet EBPが呼出元入口のSであるMSVC-EHフレーム対応を仮定すると **同じS-0x10スロット** を指す。
ただし**実際の例外ハンドラがfuncletへ渡すEBPの由来は未検証**。同一ポインタ確定・ABI VERIFIEDとは判定しない。
追加の独立補強：`0x005F8B89`のEHハンドラが参照するregistration-recordはS-0x0Cで、`[EDX-0x10]`がS-0x1Cのcookie値、`EDX-0x0C`がcookie XOR基準S-0x18と一致。これはSEHレコード算術の確認であり、funclet EBP引渡契約そのものの証明ではない。
05Hで確認済みのEH state0による初期化フラグ復元・state1 free関数の存在は新規件数に二重計上しない。

## 新しい静的成果B：Spot確保NULL後の再試行経路
`0x00597C49`は確保結果のNULL判定`0x00597C51`より先にEH state1へ設定する。NULLなら`0x00597C53 JE 0x00597C72`→EAX=0→`0x00597C74`が共有Spotキャッシュ`0x00AC0990`へNULLを書き込む。
初回helper初期化成功時に立つ`0x00B0B0D8`のguard bit0は、この通常NULL分岐では解除されない。
その後の別呼出しで名前検索が失敗しcacheもNULLのままなら、guard==1によりhelperコンストラクタ/atexit登録を省略して `0x00597C2C→0x00597C3D` の**Spot用malloc再試行**へ進める。
前提：例外発生や他コードによるglobal値変更なし。正常NULLからの後続再試行を原作実機で観測したわけではない。

## 関数・CALL siteと証拠格付
P0対象：`0x00597BA0`（resolver）、`0x005F8B7E`（EH cleanup funclet）、`0x005F8B89`（handler）、`0x005B8B1E`（GhidraがMSVC CxxFrameHandler3相当と表示）。
CALL：`0x00597C3D→0x005B6C2B`、`0x00597C6B→0x005A8110`、`0x005F8B82→0x005B6BBB`。既存Ghidra索引とPEを区別。
関数別REA正式5種（info/pseudo/assembly/callers/callees）新規完全セット=0。局所PE ASMは独立STATIC、未検証ABIはVERIFY。原作Golden PASS=0、strict MATCH=0、完全複製率は未測定。
## 監査・Golden・再開位置
新規監査は `REA_20261025_06H_P0_SPOT_EH_FRAME_AUDIT.py`。原作・2 SQLite SHA、V9 quick_check、33箇所の独立ASM照合、スタック位置算術、2 CALL索引、ABI未検証値、旧64件ログをチェックし**50/50 PASS**。保存後は独立別Pythonプロセスで**50/50 PASS / READBACK True**。50は静的検査項目数で、関数数・Goldenではない。
設計のみのGolden：初回helper正常初期化→Spot malloc=NULL→再入時にhelper ctor/atexitが重複しないか→Spot malloc再試行とcache書戻し。別ケースはSpot ctor throw時のfreeの引数同一性。いずれも NOT RUN。
次P0：`0x005BA85F`のMSVC EH funclet呼出時にEBPをどの値に設定するか追跡し、**EBP=S**の仮定を機械語で成立/否定する。続いて `0x005B6C2B`の例外仕様とatexit戻り値の契約を分離。既存解析へ二重計上しない。

## PC状態・保存・安全
Windows研究PCのLocal Compact接続成功。preflight時 `active.lock=False`、Java/Ghidra/REA名プロセスは検出されず、空きRAM約14.53GiB。CPUサンプル0%（瞬時値であり研究中の最大負荷ではない）。作業全体の所要時間は未計測。監査実行1.01〜1.39秒程度。
保存先：`rea_lab/decomp_task/` の今回新規作成した調査Python、監査Python、証拠JSON、本報告、readback記録のみ。所有外・原本・MASTER・QUEUE/PROGRESS・旧run・Git・Work・スケジュールは不変更。
過去安全拒否のVA `0x5710C0..0x571500`、Wave6、`0x004BC9C0`等は再試行していない。
正式TODO/VERIFY/BLOCKED書込差分=0/0/0。変更のない過去64/64は過去値のまま。
