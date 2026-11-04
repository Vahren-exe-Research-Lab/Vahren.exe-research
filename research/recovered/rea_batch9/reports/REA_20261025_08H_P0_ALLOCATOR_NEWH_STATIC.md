# 迫真戦記 ver0.67｜REA 2026-10-25 08時台 P0 Spot allocator / new-handler / bad_alloc
研究ID：`REA-LOCAL-20261025-0836-P0-SPOT-ALLOC-NEWH-THROW-STATIC-01`  
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED=0、Golden実測PASS=0。
原作 SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`  
2026-10-21 初期DB SHA256：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`  
統合V9 DB SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`

## 先読・過去成果との境界
`MASTER_LEDGER.md`、`ANALYSIS_LANES_PROTOCOL.md`、REA `README/QUEUE/PROGRESS`、最新同期ログ `progress_sync_20261011T153958076Z.json`、検索基盤 `README/BUILD_MANIFEST`、07H Spot EH報告/証拠/監査を参照。従前Wave1-5は保存同期ログで64/64。QUEUEとPROGRESSの古い表示はrename EPERMによる既知ドリフトであり、今回は変更も再同期も行わず、64件の二重計上なし。
既往07Hで `EBP=S` を導出済み。今回はそれを再計上せず、07Hの次P0 `0x005B6C2B` の**malloc/handler/throwの分岐と戻り値**だけを追加調査。

## 新規静的成果：0x005B6C2Bは通常NULLを返さない
初期Ghidra検索CLIで `function/callers/callees/related 0x005B6C2B` と `function 0x005BBA77` を取得し、同一SHAの承認済み研究用PEコピーからx86機械語をread-only分解。
- `0x005B6C45 CALL 0x005B9BC8`：malloc系を呼ぶ。`0x005B6C4B TEST EAX,EAX` → `0x005B6C4D JE 0x005B6C35`：NULLなら戻らずhandlerへ進む。
- `0x005B6C4F LEAVE` → `0x005B6C50 RET`：**通常RETはEAXが非NULLだった場合だけ**。EAXをゼロクリアしない。Ghidraの `void FUN_005b6c2b(size_t)` 推定は実際のポインタ利用を表せない。
- `0x005B6C38 CALL 0x005BBA77`：`__callnewh`へ。`0x005B6C3E TEST EAX,EAX` / `0x005B6C40 JE 0x005B6C51`。0以外なら `0x005B6C42` のmalloc再試行、0なら例外構築へ。
- `0x005B6CA5 CALL 0x005B864E`：`__CxxThrowException@8` にbad_allocを送出。`0x005B6CAA INT3`。このパスから通常RETへ合流しない。
- `0x005BBA82 CALL [0x006091C0]` はDecodePointer系、`0x005BBA8F CALL EAX` はnew-handler呼出候補。間接CALL 2箇所はGhidra索引上も候補、具体的ハンドラ実体は未固定。
## Spot側の重要な先行結論訂正
`0x00597C32 PUSH 0x36C` → `0x00597C3D CALL 0x005B6C2B` → `0x00597C51 TEST EAX,EAX` → `0x00597C53 JE 0x00597C72` は機械語上存在する。
しかしこのCALLが原作の未改変 `0x005B6C2B`へ正常に戻る限り、EAXは非NULLであり、**直後のJEによるNULL分岐は通常のmalloc失敗だけでは到達しない**。malloc失敗かつnew-handlerが失敗/存在しなければbad_allocを送出して通常の続行をしない。
前回04H/06Hで「Spot malloc失敗→NULL共有キャッシュ→次回再試行可能」とした説明は、コードのNULLチェック存在としては正しいが、**原作標準allocator経由で実際に通れる通常経路とみなす部分はSUPERSEDED/VERIFY**。以前の報告書は消さず、この訂正を新規独立IDとして付与。フック差替、異常ランタイム、ctor側の戻り値・別NULL要因は未評価。
この区別は再実装に重要。bad_alloc例外を単純なNULL返却へ変えると、原作のstate0/state1巻戻し・上位catchとの整合性が壊れる可能性がある。

## 独立静的監査・証拠種類
`REA_20261025_08H_P0_ALLOCATOR_NEWH_AUDIT.py` は元PE SHA・初期DB/V9 SHA・旧64件同期ログ・PE image base・34機械語・直接CALL4件・間接CALL候補2件・DB整合性・Ghidraのvoid推定との差を検査。結果 **49/49 PASS**。保存時および別プロセス再実行でも **49/49 PASS**、JSON照合 **READBACK PASS**。
5種の形式的充足：info=検索索引のみ、pseudo=機械Ghidra出力あり（戻り値型要訂正）、assembly=関連命令の独立取得のみ、callers/callees=Ghidra索引参照のみ。**REA正式のinfo/pseudo/assembly/callers/callees 5種一式を新規保存・承認したわけではない**。新規VERIFIED=0、5方法充足=0、TODO/VERIFY/BLOCKED正式書込差分=0/0/0。

## Golden条件（DESIGNED / NOT RUN）
1. 初回malloc成功：handler呼出なし、非NULLポインタEAXでRET。
2. malloc初回失敗、handlerが成功を返し次のmallocが成功：再試行後に非NULLでRET。
3. malloc失敗、新handler不在/0：bad_alloc経路、Spot関数のNULLチェックに正常復帰しない。
4. Spot constructorの例外：以前に確定したstate1巻戻しで確保ポインタをcleanup、二重解放なしを別の安全な検証環境で確認。
5. handlerが繰り返し非0だがmallocが成功しない場合：再試行・無限継続またはhandler側例外を区別。ゲームの実機故障注入は未実行。
これらは設計のみ。原作Golden PASS=0、strict MATCH=0、完全複製率=未測定。
## 保存・安全・再開位置
PCにDesktop Commander Local Compactで接続成功。研究開始時 `active.lock=False`、独立した競合Java/Ghidra/REA解析プロセスは未検出。空きRAM約15.36 GiB（確認時）。CPU全体の負荷および研究全体の所要時間は不明。監査単体0.801秒、保存時0.542秒、別プロセス再実行0.546秒。新規REA/Ghidra/原作ゲーム実行はいずれも0。既知の安全拒否VA/Wave6/REA exportや別toolでの迂回は行わず、原本・旧run・QUEUE/PROGRESS・MASTER・A-E・Git・Work・スケジュールには変更なし。
初回SQLite schema探索でPowerShellの引用符が落ちPython SyntaxErrorとなった（OTHER / 一時的コマンド組立ミス）。同内容をSQLプレースホルダを使う通常のread-only queryとして成功させた。安全拒否ではない。研究成果は上記独立IDに結び、当回作成のファイル以外を修正しない。
次P0：`0x005B9BC8` の内部new-handler再試行と `0x005B6C2B`との二重handler/例外優先順序を検査。次点は `0x00597C1C` atexit結果、`0x0049E490`検索ノード実体。06Hの再試行可能性に関する主張は正式知見へ昇格せず訂正とともに保持する。
