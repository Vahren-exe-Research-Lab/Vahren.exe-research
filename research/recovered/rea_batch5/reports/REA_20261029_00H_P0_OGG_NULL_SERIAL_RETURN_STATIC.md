# 迫真戦記 REA｜2026-10-29 00H Ogg serial NULL gate と初期化戻り値
研究ID: `REA-LOCAL-20261029-00H-P0-OGG-NULL-SERIAL-RETURN-GATE-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。正式新規VERIFIED=0、Golden実測PASS=0。
## 前回までと今回の差分
- 2026-10-28 21H/22Hの所有権・一時配列解放調査、23Hのcalloc未検査とcleanup非対称性は既存成果。二重計上しない。
- **今回追加でPE機械語を検査した箇所**: `0x005CF010` の引数NULL gate、`0x005D1630` のreturn state ladder、および2呼出し元 `0x005CFA10` / `0x005D1490` の引数の違い。
- 旧runとsearch.sqlite/V9を照合し、新しいREA問合せ/全関数再解析なし。未同期17-22H成果は現在のPC正本に統合せず保留。
## P0-A: NULL serial配列引数でシリアル記録部分を丸ごとスキップ
- `0x005CF094 TEST EAX,EAX` の EAX は第4引数（`[EBP+0x14]`）のポインタ。続く `0x005CF096 JE 0x005CF116` はNULLなら管理配列を使う区間を飛ばす。
- 管理区間は `0x005CF098` で第5引数（`[EBP+0x18]`）を参照し、`0x005CF0F2`=`_realloc`, `0x005CF0FE`=`_malloc`, `0x005CF112`=シリアル値書込まで続く。
- `0x005CFA10` のCALL site `0x005CFC2F` 前に `0x005CFC25 PUSH 0` / `0x005CFC27 PUSH 0` があり、NULLペアを渡す。シリアル配列の追加/重複照合は行わないが、Vorbisパケット解析・エラー判定まで無効になるわけではない。
- 反対に `0x005D1490` のCALL site `0x005D1572` は `0x005D1565 PUSH EAX` / `0x005D156C PUSH ECX` でローカル配列ポインタと件数のアドレスを渡す。21Hの一時配列所有権問題はこの経路には関連する。
## P0-B: 上位 `0x005D1630` の4つの戻り経路
- `0x005D165F CALL 0x005D1490` 後、`0x005D1667 TEST EAX,EAX` / `0x005D1669 JNE 0x005D16B2`：初期化の戻り値が非0ならそのまま返す。ここではcleanupを重複実行しない。
- 戻り値0で `[ESI+0x58]!=1` なら `0x005D1671 MOV EAX,0xFFFFFF7D`、すなわち **-131**。これは先行初期化後の状態不整合経路であり、メモリ確保エラー一般を-131に置換するものではない。
- `[ESI+0x58]==1` なら状態を2へ設定。`[ESI+4]==0` は `0x005D16A9` で状態3、EAX=0の成功戻り。
- `[ESI+4]!=0` は `0x005D1689 CALL 0x005D1310`。その戻り値が0なら成功として返し、非0なら `[ESI]=0` を設定し `0x005D169B CALL 0x005CFE00` で後片付けして戻り値を保持する。
## 検証と厳密な判定
- EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、旧search.sqlite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、統合V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`を再照合。
- 独立audit **48/48 PASS**（SHA/lock/27命令/呼出site/SQLite整合/旧RUNなどの条件）。call site6件は旧DB/V9の双方で各1件。原作exe実行なし。
- 旧syncログ `progress_sync_20261011T153958076Z.json` によるWave1-5 VERIFIED **64/64**、新規正式VERIFIED **0**。PROGRESS.mdの15/16はEPERM由来の旧表示。正式TODO/VERIFY/BLOCKED差分=0/0/0。
- 今回の5種証拠: info=INDEX_ONLY; pseudo=INDEX_ONLY+PE_CROSSCHECK; assembly=TARGETED_PE_NATIVE; callers/callees=INDEX_ONLY+PE_CROSSCHECK。新規REA五種完全証拠=0。Golden実測PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。
- 既存の23H確保失敗時クラッシュ候補は今回の上位return経路によって**安全に捕捉されると証明されたわけではない**。実際の例外・異常メモリ状態で通常returnに到達するかはVERIFY。
## 安全・保存・再開
- PC接続成功。active.lockなし、java/Ghidra先行プロセスなし、空きRAM約12.63GiB。CPU使用率/全体時間は未測定。探索probe 約0.816秒、独立audit 約4.325秒。REA/Ghidra/ゲーム/Work起動なし。
- REA所有新規ファイルのみ新設。原本ZIP/EXE/SAVE、MASTER、QUEUE/PROGRESS、他owner、Git、公開先、スケジュールは変更せず。
- 新規資料: `REA_20261029_00H_P0_OGG_NULL_SERIAL_PROBE.py` / `REA_20261029_00H_P0_OGG_NULL_SERIAL_AUDIT.py` / `REA_20261029_00H_P0_OGG_NULL_SERIAL_RETURN_EVIDENCE.json` / 本ファイル。
- 次回P0: `0x005D16C0` caller `0x005D1712` における非0エラーの上位伝搬と、`0x005D1490` から通常returnできないメモリ確保失敗時の境界。追加の実測をしない限り原因・クラッシュ発生率は仮説のまま保持する。
