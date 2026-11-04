# 迫真戦記 ver0.67｜REA 21時台 P0 DirectMusic +0x70 配列寿命・個数不一致監査
研究ID：REA-LOCAL-20261026-21H-P0-DMUSIC-ARRAY-COUNT-TEARDOWN-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY（2026-10-26 JST）
原作研究コピーSHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
統合V9 DB SHA256：2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 既存研究との非重複境界
12H「+0x70配列freeが既知shutdown経路で見つからない」、13H「DAT_0065BED8デバッグ設定で変更可、上限10のみ」、14H「new(0)相当でも内部で1 byte確保」、19H「COM失敗共通出口」、20H「CoCreateInstance失敗時[out] NULL保証」は旧成果であり再計上しない。
**今回新規の限定証拠**：初期化とshutdownの両方が所有オブジェクト内のcapacityではなく、同じ可変グローバルDAT_0065BED8を別時点に読み込むことを機械語で独立対照。加えてshutdownに直結する7関数中の+0x70参照とfree引数の出所を限定監査し、配列要素のNULL化と配列ポインタそのものの解放・NULL化が異なることを明示。

## ネイティブ機械語上の根拠
- init `0x004BE480`: `0x004BE4E0 CALL 0x005B5C0B`で配列を確保、`0x004BE4E5 MOV ECX,[0x65BED8]`、`0x004BE4EB MOV [ESI+0x70],EAX`、`0x004BE4F7 MOV EDX,[ESI+0x70]`。取得した個数の範囲でスロットを0初期化する。
- teardown `0x004BE6B0`: `0x004BE7B3 XOR EDI,EDI`、`0x004BE7B5 CMP [0x65BED8],EDI`、`0x004BE7BB JLE 0x4BE7FA`（0以下なら全ループスキップ）。
- `0x004BE7C0 MOV EAX,[ESI+0x70]`、`0x004BE7C3 CMP [EAX+EDI*4],0`、非NULL要素に対し`0x004BE7D7 CALL EDX`（vtable+0x98、既報CloseDown同定）、`0x004BE7E5 CALL EDX`（vtable+8、Release）、`0x004BE7EA MOV [EAX+EDI*4],0`（**配列要素**を0にする）。
- `0x004BE7F1 INC EDI`、`0x004BE7F2 CMP EDI,[0x65BED8]`、`0x004BE7F8 JL 0x4BE7C0`。shutdownは**ループ終了判定でもグローバル値を再読み**する。
- 親`0x00555CD0`：`0x00555E60 CALL 0x004BE6B0` → `0x00555E71 CALL 0x004BE600` → `0x00555E77 CALL 0x005B6BBB`。最後はオブジェクト本体を渡している。

## 今回の7関数限定の所有権対照
| 関数 | 対象+0x70の直接命令 | freeの具体的な入力 |
|---|---|---|
| 0x004BD9A0 constructor | なし | 対象外 |
| 0x004BE480 initializer | +0x70へ確保ポインタを保存、後に読出し | +0x70をfreeしない |
| 0x004BE6B0 shutdown | +0x70を3回読出し、配列要素を0化 | 0x004BE6F0は+0xA0由来のEDIをfree |
| 0x004BE600 destructor | +0x70参照なし | 0x004BE651は内部木領域、0x004BE667/0x004BE686は文字列領域 |
| 0x004BF2B0 stop/reset helper | +0x70直接参照なし | 間接COM操作あり、+0x70 free未同定 |
| 0x00502160 nested-object cleanup | +0x70直接参照なし | オブジェクト内部のCOM release、+0x70 free未同定 |
| 0x00555CD0 outer owner | +0x70直接参照なし | 0x00555E77は親オブジェクト本体をfree |

限定した7関数には、**+0x70配列ポインタを直接引数としてfreeする実命令も、[ESI+0x70]を0に戻す実命令も見つからない**。一方、配列要素だけは明確にNULL化している。これは12Hの疑いを広いshutdown呼出経路で再点検した新しい補強であり、EXE全関数のalias/free不存在を保証するものではない。

## 新しい条件付き VERIFY：allocation count と teardown count が分離
初期化時に使ったDAT_0065BED8をオブジェクト内に記録するcapacityフィールドは今回の経路では見つからない。teardownは別時点の同じグローバルを読む。したがって、**オブジェクトの生存中にこの値を変更できた場合**は次の危険性が成立し得る。
- init=0、teardown>0：少なくとも4バイトスロットを読み始めるが、init 0での割当要求は既報の0-byte→CRT内部1-byte経路。境界外読取の可能性。
- init=1、teardown=10：1要素分に対し10要素まで走査し得る。境界外アクセス候補。
- init=10、teardown=1：残る9個のCOM参照がshutdownでReleaseされない可能性。
- teardown<=0：`0x004BE7BB`で配列走査を実行しない。すべての参照が未解放になり得る。

**重要な制限**：DAT_0065BED8を実行中に変更できること・同一オブジェクト生存中の再設定経路は**未証明**。デバッグ設定の読込が初期化前に一度だけであれば、この差異は通常プレイでは発火しない。元ゲームのクラッシュ・リークの確定診断ではない。

## 監査・正式進捗
- 対象を7関数に限定し、原作PE32実バイトをCapstone独立decode、統合V9の既存検索索引とSHA256/SQLite quick_checkを照合した。**独立静的検査51/51 PASS**（検査条件数であって関数数ではない）。新規Ghidra全件再解析・REA問い合わせは実施しない。
- REA5方法：info=INDEX_ONLY_V9 / pseudo=INDEX_ONLY_V9 / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY_V9 / callees=INDEX_ONLY_V9。正式の独立5種完備0関数、**新規REA VERIFIED 0件**。
- 旧Wave1–5=64/64は2026-10-11の同期ログ`logs/progress_sync_20261011T153958076Z.json`に由来する過去成果であり再加算なし。QUEUE/PROGRESSは過去のEPERM後staleであるため書換えない。
- 正式TODO/VERIFY/BLOCKEDの**書込差分**=0/0/0。新規の独立VERIFY候補は正式キューにはまだ追加しない。
- 原作ゲームGolden実測PASS=0。strict MATCH・完全複製率は未測定。Work未使用。原本、MASTER、A～E、既存RUN、Git、公開先、スケジュール無変更。

## 実行環境と次のP0
PC SAITO online、21:51 JST時点active.lockなし、Java/Ghidra稼働検出なし、空き物理RAM約14,484MiB、CPU使用率28%（PC全体の単発値、今回の処理専用値ではない）。独立監査単体は約1.19秒、研究全体の厳密な所要時間不明。ゲーム実行、REA再実行、Ghidra起動はいずれも0回。
試行と障害：21H読み取り用probe初回でV9索引のカラム名を`caller_va`と誤指定したが、正しい`caller_function_va`へ修正。途中オフセット開始のdisasm診断も削除し、関数入口から整列decodeし直した。安全拒否なし。禁止VA/Wave6/REAエクスポートを再試行していない。
次P0：`0x00558000`のDAT_0065BED8書込みが初期化後にも呼ばれ得るかをcallers→時系列で検証。続いて`0x004BE480`を複数回呼ぶ経路、他のaliasが+0x70を解放するかを、関数限定で裏付ける。
Golden設計（NOT RUN）：デバッグ個数0/1/10の通常起動・終了、Loader/PerformanceのCoCreate失敗、2番目のnew失敗で、HeapAlloc/HeapFreeとCOM AddRef/Releaseを観測。個数のmid-run変異はまず実行経路があると証明された場合に限り試験。オフライン成果の正式同期は行わない。
