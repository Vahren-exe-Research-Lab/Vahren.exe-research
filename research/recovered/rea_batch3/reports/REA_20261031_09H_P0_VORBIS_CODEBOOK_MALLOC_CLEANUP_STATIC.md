# REA｜2026-10-31 09H｜Vorbis codebook配列確保失敗とcleanup（P0）
研究ID: `REA-LOCAL-20261031-09H-P0-VORBIS-CODEBOOK-MALLOC-CLEANUP-STATIC-01`
owner=REA / task=T015 / **PC-SAVED STATIC + INFERRED / VERIFY / NOT READY**。
前回08H `REA-LOCAL-20261031-08H-P0-VORBIS-CODEBOOK-INIT-WIDTH-STATIC-01`の追加検証であり、同VA/旧発見を新規件数として重複計上しない。

## ベースライン・事前チェック
- 原作同一SHA研究専用PE: `rea_lab/targets/hakushin067_Vahren.exe`、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 read-only DB: `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`、SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
- MASTER / ownership protocol / QUEUE / 古いPROGRESS / runs照合: `logs/progress_sync_20261011T153958076Z.json`の正式64/64を採用。新規5種証拠取得なし。
- 前回08H証拠、knowledge README/SYNC_STATUS、非公開developのcoverage・curation、KB addr/docs/research、V9 function/callers/calleesを読取専用で確認。
- ローカル `active.lock` 不在、Java/Ghidraプロセスなし。空きRAM約17.39GiB（確認時）、CPU負荷/総所要時間不明。Ghidra/REA/原作ゲームは起動せず。

## 静的差分1：同じ配列フィールド+0x08に到達する別々のmalloc経路
| E8 call site | target | 保存命令 | 配列書込の例 | 経路 |
|---|---|---|---|---|
| `0x005DA604` | `0x005B9BC8` | `0x005DA60E`: `[ESI+0x08]=EAX` | `0x005DA676`: `[ECX+EBX*4]=EDX` | ordered |
| `0x005DA6D6` | `0x005B9BC8` | `0x005DA6DB`: `[ESI+0x08]=EAX` | `0x005DA71A` / `0x005DA725` | unordered |
| `0x005DA811` | `0x005B9BC8` | `0x005DA819`: `[ESI+0x20]=EAX` | `0x005DA837`: `[EDX+ECX*4]=EAX` | lookup type 1/2 |
三箇所ともE8の5byte相対呼出先をPEとV9 `native_callsite`で一致確認。malloc戻り値をフィールドへ保存する前にNULL判定はない。**入力が実際に正数の配列要素書込へ進み、かつ確保が失敗する場合にのみ**NULL参照の危険がある（DYNAMIC未確認）。

## 静的差分2：cleanupはNULL許容、ただし書込前の保護ではない
- `0x005D9E70`は`[ESI+0x24]`（初期化marker）が非0なら解放へ進む。
- `0x005D9E7D/80/82` で `+0x20` ポインタが非NULLの場合だけ `0x005D9E85` の `_free` を呼ぶ。
- `0x005D9E8D/90/92` で `+0x08` ポインタが非NULLの場合だけ `0x005D9E95` の `_free` を呼ぶ。
- その後0x00〜0x24の10 dwordを0にし、`0x005D9EBD`で本体を解放する（callerは生存した本体ポインタを渡す前提）。
- `0x005DA857`からこのcleanupへ直接CALL。V9上のほかのcallerは `0x005D3ECC/0x005D5B60/0x005D5B9D`。いずれも新規ABI VERIFIEDではない。
- **失敗後にcleanupへ到達できるケース**ではNULLのフィールドも処理できる。一方、各配列書込で先に例外が起きた場合にはcleanupが介入できる保証はない。

## 静的差分3：CRT malloc(0)の取り扱いと再試行
- `0x005B9BC8`の`0x005B9BF9`でサイズ引数EBXを検査。0の場合は`0x005B9C01`でEAX=0、`0x005B9C03`でEAX=1とし、`0x005B9C04`からサイズ1としてヒープ確保に進む。
- `0x005B9C0D`はヒープ確保関数ポインタへの間接CALL。戻り値の0を`0x005B9C15/17`で判定し、条件次第でnew-handler側へ進み再試行する経路が存在する。
- 従って**要素数0に伴うmalloc(0)を即NULLと扱う推論は誤り**。ただし、最終的な確保失敗でNULLが返る可能性は残り、成功が保証されるわけではない。
- 実際の失敗頻度、CRT new-mode設定、外部heap callback、実機クラッシュは未観測。CRT全体のABIについても正式確認はしない。

## 監査・復旧・正本保護
- `REA_20261031_09H_P0_VORBIS_CODEBOOK_ALLOC_CLEANUP_AUDIT.py` はPE+V9をread-onlyで独立照合し、**48/48 PASS、0.8322秒**。
- 初回監査47/48は監査側の命令開始位置の取り違え（`0x005DA719`は`inc eax`、書込命令は`0x005DA71A`）。`RECOVERY-REA-20261031-09H-ASM-START-01` としてここに残す。修正後PASS、新規証拠のみ保存。
- `knowledge/kb.py candidates 0x...` は引数形式の不一致でusageエラー。正しいhelpを確認済み、`RECOVERY-REA-20261031-09H-KB-ARGS-01`。安全拒否・接続障害ではない。
- 新規正式5種証拠(info/pseudo/assembly/callers/callees)完備0、新規VERIFIED0。既存正式STATIC VERIFIED **64/64維持**、正式TODO/VERIFY/BLOCKED差分0/0/0、原作Golden実測PASS0、完全複製率未測定。
- MASTER/QUEUE/PROGRESS/既存RUN/原本/Git/共有knowledge/A〜E/スケジュール変更なし。

## KB_CANDIDATE（統合専任のみ審査）
- 既存連続研究IDは本書冒頭・08H証拠を参照。owner=REA/task=T015。
- `0x005DA604` / `0x005DA6D6` → malloc後にcodebook `+0x08`、`0x005DA811` → `+0x20`。配列書込は正要素数時に起こり、ローカルNULLガード未確認。STATIC / INFERRED / VERIFY。
- `0x005D9E70`: marker `+0x24`、`+0x20`と`+0x08`のNULLガード、解放順と本体解放。STATIC、失敗時の正常終了は未保証。
- `0x005B9BC8`: サイズ0→1のCRTラッパーと確保再試行候補（条件付き、STATIC/VERIFY）。
- 根拠: 本書のE8 CALL site・native PE命令VA、同名 `_EVIDENCE.json` のASM bytes/照合48件、README記載の源SHA。オリジナルヘッダ異常系の実ゲームGolden PASS=0、READY=NO。
- 共有知識辞書に直接反映せず、KB統合専任へ渡す未承認候補。ソースSHAや矛盾を確認してから審査。

## 次回の安全な再開位置
`0x005D3DE0` と `0x005D57C0` の4つのcleanup callerをV9/PEのCALL siteと比較し、codebook配列の所有権・二重解放防止の条件を調査。特に+0x24 markerと各aliasが異常パスでも維持されるかVERIFY継続。必要なら`0x005B9BC8`のnew-handler終了条件も別証拠で補強。再解析/原作ゲーム実行は禁止のまま。
