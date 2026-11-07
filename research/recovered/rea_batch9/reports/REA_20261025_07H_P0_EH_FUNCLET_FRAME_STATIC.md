# 迫真戦記 ver0.67｜REA 2026-10-25 07時台 P0：Spot C++例外funcletのEBP由来を静的確定

研究ID：`REA-LOCAL-20261025-0736-P0-SPOT-EH-FUNCLET-EBP-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED=0、実機Golden PASS=0。
原作PE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
初期検索DB SHA256：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`
統合V9 SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`

## 先読・重複照合
MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、過去05H/06H報告および06H EVIDENCE、旧同期ログ `progress_sync_20261011T153958076Z.json`、初期検索README/BUILD_MANIFEST、V9入口を参照。
旧同期ログはWave1～5の64/64、21 runs。QUEUE/PROGRESSは既知のrename EPERMで古い表示のため最新同期ログを優先し、過去64件を新規計上しない。
検索CLI（初期DB）で `function/callers/callees 0x005BA85F`、`function/callees 0x005B9D3C`、`function/callers 0x005BFB10`、`function 0x005B8B54` を調べ、V9で `function 0x005B8B1E` を照合。機械語はSHA一致のREA承認済み対象コピーをread-only分解。

## 新規P0成果：06Hの「funclet EBP=Sなら同じmallocポインタ」という仮定を静的に解消
原関数 `0x00597BA0` の入口ESPを `S` と定義。冒頭の `PUSH -1 / PUSH handler / PUSH FS:[0]` によりSEH登録ノードは `S-0x0C`。
`0x00597BBA LEA EAX,[ESP+0x10]`（この時ESP=S-0x1C）→ `0x00597BBE MOV FS:[0],EAX` より、実際に登録されるポインタは `S-0x0C`。
例外ハンドラ `0x005F8B89` は `0x005B8B1E` にJMPし、`0x005B8B3F` から内部ハンドラ `0x005BA85F` を直接CALLする。
`0x005BA8C6 PUSH [EBP+0x0C]` により元のEH registration-nodeを `0x005B9D3C ___FrameUnwindToState` の第一引数として渡す。
同関数の `0x005B9D4B MOV EBX,[EBP+8]` は登録ノードのアドレスをEBXへ保持し、`0x005B9DA7 PUSH EBX` で `0x005BFB10 __CallSettingFrame@12` の第二引数として渡す（第一引数はUnwindMapのactionポインタ）。
`0x005BFB18 MOV EAX,[EBP+0x0C]` と `0x005BFB1B ADD EAX,0x0C`、`0x005BFB1E MOV [EBP-4],EAX`、`0x005BFB2B MOV EBP,[EBP-4]` の命令列はfunclet呼出前の **EBP=登録ノード+0x0C=S** を構成し、`0x005BFB35 CALL EAX` でUnwindMap actionを呼ぶ。
`0x006511BC` FuncInfo の maxState=2・unwindMap `0x006511AC` のstate1 actionは `0x005F8B7E`。このfuncletでは `MOV EAX,[EBP-0x10]` → `CALL 0x005B6BBB`。
元Spot関数の `0x00597C45 MOV [ESP+0x0C],EAX` はESP=S-0x1Cなのでmalloc結果を `S-0x10` に保存。よって **state1の正規MSVC unwind呼出しが到達したとき、cleanupの `[EBP-0x10]` は同一スロット `[S-0x10]`** を読み、free系に渡す、と機械語・メタデータの静的接続で示せた。
前回06HのEBP由来未証明は「正規state1 unwindパスの静的契約」に限り解決。ただし他のレジスタ契約や例外実機挙動は未検証で、関数フック可能な完全ABIのVERIFIEDではない。

## 条件と残るVERIFY
- state1に実際に到達するには、該当スコープで例外が発生し、標準MSVC EH処理が巻き戻す必要がある。実機でのctor throw、malloc失敗、二重解放・リーク有無は未観測。
- 初期化guardのstate0巻戻しとatexit終了登録は05H研究の既知成果であり再計上しない。
- `0x005BFB35` は機械語では間接CALL EAX。UnwindMap actionとして `0x005F8B7E` に到達するのはstate1の条件付き経路であり、全呼出しが同funcletへ進むと誤断定しない。
- `0x005BA85F` / `0x005B9D3C` / `0x005BFB10` はGhidraのC推定・MSVC library matchingだけでなくPEの実命令で追跡したが、REAの関数別5種証拠（info/pseudo/assembly/callers/callees）を新規一式完成させたわけではない。

## 独立監査とGolden
`REA_20261025_07H_P0_EH_FUNCLET_FRAME_AUDIT.py` で原作、初期検索DB、V9各SHA、V9 quick_check、x86命令29箇所、FuncInfo/UnwindMap、S基準スタック算術、旧64件ログ等を検査し **46/46 PASS**。別Pythonプロセスで再実行 **46/46 PASS / READBACK PASS**。46は検査条件であり関数数ではない。
実機Golden候補：state1へ入るSpot constructor throw → `S-0x10` に保存した唯一のmallocポインタがcleanupのfree引数へ渡ることを追跡する。**DESIGNED / NOT RUN**。原作Golden PASS=0、strict MATCH=0、完全複製率未測定。
正式REA差分：新規VERIFIED=0、5方法全件達成=0、QUEUE/PROGRESSへのTODO/VERIFY/BLOCKED書込差分=0/0/0。
## PC状態、障害、所有権、再開位置
PCオンライン、Desktop Commander Local Compactで接続成功。事前確認 `active.lock=False`、Java/Ghidra/REA名の解析プロセス検出なし、空きRAM約15.01GiB。全体CPU負荷と研究全体の経過時間は未測定。独立監査単体1.511秒、再実行0.958秒。
read-only探索の初回Python標準入力ではPowerShell側Unicode pipeで日本語パスが `????` に置換され `OSError Errno 22`（OTHER）。その後、既存REA担当ディレクトリへSet-Locationし、ASCII相対パスのread-only解析で正常化。安全拒否ではない。拒否操作・Wave6・REA export・既拒否VAの再試行なし。
REA担当 `decomp_task` に当回の新規audit/JSON/report/readbackのみ保存し、旧run、QUEUE/PROGRESS、MASTER、原本、A～E、T018、dev_lab、Git、Work、既存スケジュールを変更しない。
次のP0は `0x005B6C2B` のNULL返却/throw振分、`0x00597C1C` のatexit登録戻り値の未チェックが生む静的契約、そして `0x0049E490` 検索ノード+0x28の実型のうち未解析優先度を比較する。今回のEBP=S立証を再調査・二重計上しない。
