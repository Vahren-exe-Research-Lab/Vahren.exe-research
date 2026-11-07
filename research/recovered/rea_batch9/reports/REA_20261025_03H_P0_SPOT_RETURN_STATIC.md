# 迫真戦記 ver0.67｜REA 2026-10-25 03時台 P0: Spot参照・共有fallbackと3関数のEAX戻り値
研究ID：`REA-LOCAL-20261025-0336-P0-SPOT-RESOLVER-EAX-CACHE-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED=0、ゲームGolden実測PASS=0。
原作SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
統合V9 SQLite SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 先読・基盤と非重複
MASTER_LEDGER、レーン規約、REA README/QUEUE/PROGRESS、Wave1～5同期ログ`progress_sync_20261011T153958076Z.json`、02H owner引数証拠と01H/00H関連記録を先読。旧2026-10-21 search_indexのREADME/BUILD_MANIFESTを確認し、新規索引クエリは統合V9専用CLIを使用。
PCオンライン、`active.lock`なし、Java/Ghidra/REA競合プロセス検出なし、空きRAM14.63GiB・CPU瞬時11%。REA/Ghidra/ゲーム起動0。旧syncは64/64（Wave別16+10+10+12+16、21 runs）。QUEUE/PROGRESSの旧表示はrename EPERMによるSTALEとして扱い、本runで上書きなし。
02H既知：`0x00597BA0`のEAXがowner/this候補としてcallerで使われる、Ghidraはvoidと誤表示。今回の追加：戻り値の**2段階の具体的な生成元**、別の2関数のGhidra return省略、キャッシュの分岐と失敗経路を独立機械語で確認。過去と同じ関数を「新規VERIFIED」として再計上しない。

## 新発見A｜0x0049E490はvoidでなく検索値をEAXで返す
V9 pseudoc `void __fastcall FUN_0049e490(char *param_1)` は返値を記載しないが、原作ASMは以下を実行する。
- `0x0049E4BF MOV EAX,ECX`：ECXを文字列入力として扱い、`0x0049E4E0～E4EF`で文字列長と一時キーを生成する。
- `0x0049E4F9 LEA EAX,[ESI+0x1EEBCC]` と `0x0049E50B CALL 0x004C1200`：ESIに依存する検索木からイテレータを取得する。
- `0x0049E524 MOV EAX,[ESP+8]`; `0x0049E528 CMP EAX,[ESI+0x1EEBD0]`：検索結果がend sentinelか判定する。
- `0x0049E530 XOR EAX,EAX`：sentinelなら0、`0x0049E534 MOV EAX,[EAX+0x28]`：存在時はノード`+0x28`の値を返す。
- `0x0049E54A CALL 0x005B6513`はsecurity-cookie照合で正常復帰時にEAXを変更しない。したがって`0x0049E552 RET`まで戻値EAXが保存される。
検索ノード`+0x28`の厳密な静的C++型は未確定（利用上はSpot系オブジェクトポインタ候補）。**Ghidraのvoid宣言をhook型として採用しない。**

## 新発見B｜0x00597BA0は検索ヒットをキャッシュより優先する
- `0x00597BD0/BD6/BD9`：`[EDI+0xB0]`経由で管理データの`+0x504`をESIへ導出し、`0x00597BDF CALL 0x0049E490`。
- `0x00597BE4 TEST EAX,EAX`; `0x00597BE6 JNE 0x00597C79`：**検索が非0を返したら、その値を即返す**。
- 0時 `0x00597BEC MOV EAX,[0x00AC0990]`; `0x00597BF3 JNE 0x00597C79`：キャッシュ既存なら同じグローバルを返す。
- キャッシュ未初期化時、`0x00597C32 PUSH 0x36C`→`0x00597C3D CALL 0x005B6C2B`：割当。失敗時`0x00597C72 XOR EAX,EAX`、成功時`0x00597C6B CALL 0x005A8110`で構築。
- `0x00597C74 MOV [0x00AC0990],EAX`：新規値（または割当失敗時NULL）を保存。成功時のみ重複生成が避けられる。初期化ガード`0x00B0B0D8`とatexit登録も存在。
**通常正常復帰経路の値：命名検索の取得値／共有fallback／新規生成結果／割当失敗のNULL**。検索木にNULL値が格納される場合も後者へ進む。共有fallbackが全入力で正しい同一managerになるとは限らない。

## 新発見C｜0x005A8110はSpotコンストラクタでEAXに生成先を返す
V9 pseudoは`void __thiscall FUN_005a8110(...)`だが、原作ASMは `0x005A8145 MOV EBP,[ESP+0xA0]`で生成先を保持し、`0x005A8177 MOV [EBP],0x006385BC`でSpot vtableを設定する。
正常出口`0x005A870B MOV EAX,EBP` → `0x005A8726 CALL 0x005B6513` → `0x005A8731 RET 8`。cookie関数の成功経路はEAX無変更。したがって実際に利用されるEAXはコンストラクタの生成先ポインタ。
呼出元`0x00597C64 PUSH ECX` / `0x00597C65 PUSH EAX` / `0x00597C66 MOV ECX,0x00B0B008`を照合。**戻値ポインタの動作は静的確認したが、完全な`thiscall`宣言・障害時ABIは未承認。**

## 管理者同一性への影響
02Hに確認した`0x004917B3`と`0x00491E99`のowner引数は、ここで解決される値の出所が異なる。
条件付き仮説：両方の名前検索が非0なら各ノードの`+0x28`値を使うため、異なるポインタになり得る。両者が非ヒットかNULL値で、共有キャッシュが作成済みなら同じ`0x00AC0990`を受け取る。一方、同じvptr/管理者を必ず共有するとの静的証明にはならない。
次は、owner Xを通した `R=[[X+0x0C]+4]` とroot `0x008BE2F0` の等価条件を、検索木ヒットとfallbackで分けて調査する。

## 検証指標
原作・V9実SHA、SQLite quick_check、機械語32箇所、原作E8算術とV9のE8 site5件（各2条件）、3関数の疑似C存在・ABI未検証・void宣言を独立照合。**56/56 PASS**、保存後の別プロセス実行も**56/56 PASS**、JSON一致読戻し**PASS**。
ここでの56は機械的検査項目であって関数完成数ではない。正式REA `info/pseudo/assembly/callers/callees`の新規完全5種セット=0、正式VERIFIED+0、TODO/VERIFY/BLOCKED書込差分0/0/0。既存Wave1～5は**64/64**を保持。ゲームGolden実測PASS=0、strict MATCH=0、完全複製率未測定。
限定ASMと索引擬似Cを組み合わせたSTATIC資料であり正式ABI修復や動的検証ではない。

## 異常・安全・次の一手
初回の`python -c`でPowerShellの引用符が崩れSyntaxErrorが発生（`REA-LOCAL-20261025-03H-CLI-QUOTING-01`、OTHER）。ファイル変更前の構文エラーであり安全拒否ではない。新規REA所有の読み取り専用probeを作成し、正常な原本ASM照合を実行した。安全拒否済み`0x004BC9C0`検索、`0x5710C0..0x571500`、Wave6/exportの再試行・迂回は0。
次のP0：`0x0049E490`の検索木node`+0x28`の具体型とname一致・同一node条件、`0x005A8110`の生成先所有権・cache破棄登録`0x005971A0`、呼出元`0x00490590/0x00491870`のEDI値の分岐別同定。Golden設計（DESIGNED/NOT RUN）：検索ヒット／NULL格納／fallback初回／fallback再利用／alloc失敗／別owner名の二重呼出し。
REA ownerディレクトリ内の新規ファイルのみ保存し、原作、MASTER、QUEUE/PROGRESS、既存run、他レーン、Git、Work、スケジュールは変更しない。

