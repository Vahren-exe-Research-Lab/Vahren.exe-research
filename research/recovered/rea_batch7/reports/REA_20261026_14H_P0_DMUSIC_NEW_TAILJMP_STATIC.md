# 迫真戦記 ver0.67｜REA P0 DirectMusic管理配列のoperator newラッパー／失敗契約
研究ID: `REA-LOCAL-20261026-14H-P0-DMUSIC-NEW-TAILJMP-THROW-STATIC-01`
日時: 2026-10-26 14時台（JST）
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。新規REA正式VERIFIED=0、原作Golden実測=0。
研究用PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
Ghidra12.1.4初期DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`

## 非重複の新知見
13時台には `DAT_0065BED8` がdebug設定で0/負数になり得て、配列のnew要求量 `count=-1` で `0xFFFFFFFF` に飽和することを固定済み。2026-10-25 08～11時台のCRT _malloc/new-handler研究は、通常malloc失敗時のbad_allocとhandler初期化を解析済みであり、今回は加算しない。
**新規**: 配列確保の呼出先 `0x005B5C0B` は11バイトのホットパッチ形式ラッパーで、`0x005B5C11 JMP 0x005B6C2B` によって同じスタック引数を保ったままoperator new相当へtail transferする。
`0x004BE4DF PUSH ECX` → `0x004BE4E0 CALL 0x005B5C0B` → `0x005B5C11 JMP 0x005B6C2B` → `0x005B6C45 CALL _malloc` → 成功時EAX非NULLを保持して `0x005B6C50 RET`。
呼出元 `0x004BE4EB MOV [ESI+0x70],EAX` には、直前の例外throwに対する明示的なNULL比較は存在しない。
Ghidra擬似Cの `void FUN_005b5c0b(void)` と `void FUN_005b6c2b(size_t)` は、実際のEAXポインタ利用を表現していない。戻り値やABI復元の際に機械語を優先すること。
**索引分類注意**: 新検索DBの `calls` に `0x005B5C11 → 0x005B6C2B` がUNCONDITIONAL_CALLとして登録されるが、実バイトはCALLでなく**JMP**。09時台に別関数で3箇所の同種例があり、今回は別のsiteを新たに確認した。

## 負値・ゼロ値の到達先
- `count=1` → 要求サイズ4。 `count=10` → 40。正常new成功なら配列初期化へ進む。
- `count=0` → `operator new(0)` → `_malloc(0)` は `0x005B9BF9..0x005B9C03` でHeapAllocへ**1バイト**を渡す。成功なら非NULLを格納し、`0x004BE4F5`からCOM要素初期化ループを飛ばす。サイズ0は即NULLとは限らない。
- `count=-1` → 要求サイズ `0xFFFFFFFF`。 `_malloc 0x005B9BD1 CMP EBX,-0x20` + `0x005B9BD4 JA 0x005B9C45` によりHeapAlloc前に巨大サイズ分岐する。`0x005B9C46 __callnewh`、`errno=12`、`EAX=0`で戻る経路を持つ。
- そのNULLを外側new `0x005B6C2B` が検出し、`0x005B6C38 __callnewh` が0なら `0x005B6CA5 __CxxThrowException`（bad_alloc）に進む。**通常のNULL返却はしない**。
- 10/25 10時台の独立成果では通常CRT初期化後のhandlerはNULL、new-modeは0と整理済み。これが実際の状態なら `-1` はbad_alloc経路へ進み、`stream+0x70`への正常保存以前に制御を外れる（上位catch/終了処理は未検証）。
- handlerが非NULLになった場合や、別の例外を投げた場合の再試行・例外優先順位は実機未測定。これらを確定バグ・クラッシュと断言しない。

## 独立監査と判定
監査スクリプト: `REA_20261026_14H_P0_DMUSIC_NEW_TAILJMP_AUDIT.py`。研究用PEのCapstone復号、関数境界、先行DBのCALL索引、SQLite quick_check、旧64件同期ログ、数値条件を限定照合。**48/48 PASS**。
初回は `0x005B6CAA INT3` が127バイト関数の**外側**にある点を見落とし47/48。監査条件の対象を関数外単一命令として別取得し、48/48へ訂正。安全拒否ではない。既存研究ファイル・既存検索DB・原作は非変更。
5種: info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY。REA正式5種完全充足0・新規VERIFIED0。旧Wave1～5 64/64は過去同期ログの値を維持し二重計上しない。正式TODO/VERIFY/BLOCKED書込差分0/0/0。Golden PASS0、strict MATCH/完全複製率未測定。
安全: Local接続成功、active.lockなし、開始時RAM約17.72GiB、競合Java/Ghidra/REA名プロセス未検出。CPU負荷・研究全所要時間は不明。新規REA/Ghidra/原作ゲーム実行0、Work0。安全拒否済みWave6/VA/FLS/exportおよび拒否済み09H監査ファイルには非接触。原本、MASTER、QUEUE/PROGRESS、既存runs/evidence、A～E、Git、公開先、スケジュールを変更しない。
未同期の旧13時台・14時台オフライン成果は今回も未同期。

## 次回P0とGolden条件（DESIGNED / NOT RUN）
まず `0x004BE480` のC++ EH unwinderおよび上位 `0x004BD2A0` のcatch/終了経路を限定調査し、bad_alloc時に`stream+0x70`やloader COM状態をどう破棄するか区別する。
別途安全な隔離テスト設計: debug設定なし/count=1, count=0, count=-1, count=11、CRT handler NULL/非NULL、bad_alloc捕捉、alloc済み配列の終了時free確認。ゲームGoldenは未実行で0。

