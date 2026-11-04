# 迫真戦記 ver0.67｜REA 2026-10-25 04時台 P0: Spot共有fallbackとatexit実体の分離
研究ID：`REA-LOCAL-20261025-0433-P0-SPOT-CACHE-ATEXIT-OWNER-SPLIT-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式REA VERIFIED=0、ゲームGolden実測PASS=0。
原作EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
統合V9 SQLite SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 先読・対象・非重複
MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、旧sync 20261011T153958076Z（64/64、21 runs）、2026-10-21検索索引のREADME/BUILD_MANIFEST、03H/02H関連報告、04H既存IDを参照。
対象は `0x00597BA0`（Spot fallback生成）、`0x005971A0`（静的helper初期化）、`0x00608C20`（atexitコールバック）、`0x00432DF0`（helper解放）。03HはEAX戻値・初回生成を解明済み。今回新しいのは **atexitの本当の破棄対象**と初期化失敗の分岐差。
原作/Ghidra全体再解析・原作ゲーム実行・REA新規起動は実施していない。既存成果を新規VERIFIEDへ加算しない。

## P0発見A｜登録されるatexitコールバックはSpot cache直接破棄ではない
- `0x00597BF9 TEST BYTE PTR [0x00B0B0D8],1` と `0x00597C02 OR DWORD PTR [0x00B0B0D8],1` で初期化ガードを操作。
- `0x00597C09 PUSH 0x00B0B008` → `0x00597C12 CALL 0x005971A0` は**global helper 0x00B0B008のコンストラクタ実行**。
- `0x00597C17 PUSH 0x00608C20` → `0x00597C1C CALL 0x005B6BA4 (_atexit)` でコールバック登録。
- 原作実バイト：`0x00608C20 PUSH 0x00B0B008` → `0x00608C25 CALL 0x00432DF0` → `0x00608C2A RET`。
- `0x00432DF0`の既存Ghidra擬似Cは、helperの文字列バッファ解放・`0x00415CF0`の木構造解放・free処理を示す。
**したがってこの登録が直接解放するのは0x00B0B008のglobal helperであり、fallback Spotポインタ `0x00AC0990` の解放とは同一視できない。**
V9には`0x00608C25→0x00432DF0`と`0x00608C20`のatexit登録がすでに存在する。これを索引の新規修復件数として計上しない。

## P0発見B｜初期化例外とSpot生成NULLは別条件
- `0x005971DD PUSH 0x2C`→`0x005971E2 CALL 0x005B6C2B`：global helperの木番兵ノード用メモリ確保。
- `0x005971EC JE 0x005972B5`：確保失敗は`std::bad_alloc`構築経路を経て`0x005972D9 CALL 0x005B864E (__CxxThrowException)`へ到達。
- 対照的にSpotの`0x36C`確保は`0x00597C32 PUSH 0x36C`→`0x00597C3D CALL 0x005B6C2B`で、`0x00597C53`の失敗枝は`0x00597C72 XOR EAX,EAX`→`0x00597C74 MOV [0x00AC0990],EAX`。
**初回fallback失敗を単一の「NULLを返す」として扱うのは誤り。** helper初期化の確保失敗は例外経路、後段Spot確保失敗はNULL経路を持つ。例外に対する上位catch、guard rollback、メモリ確保APIの例外仕様は未確認。

## P0発見C｜cache globalへの直接参照範囲
PEの`.text`を4-byte即値`0x00AC0990`で全走査すると、リテラルの出現は**2箇所**（`0x00597BED`読出し命令内部、`0x00597C75`書込命令内部）。callback `0x00608C20`ではこのグローバル値を直接参照しない。
これは生バイトの字面探索であり、レジスタ・ポインタ間接参照や別名アドレス、実際のオブジェクト寿命を網羅した証明ではない。メモリリーク、ゲーム終了までの保持、cleanup無し等は**断定しない**。

## 機械検査とREA計上
原作SHA、統合V9 SHA、SQLite quick_check、ASM18命令、E8ターゲット4件、V9参照3件、疑似C/ABI記録2関数、既存atexit登録、callback callsite owner、.textリテラル3集合などを独立監査：**38/38 PASS**。検査項目数は関数数ではない。
正式REAの`info/pseudo/assembly/callers/callees`新規5種完全セット=0。Ghidra索引・生ASM部分・V9既存証拠は正式REA取得に読み替えない。
既存Wave1～5は旧同期64/64（Wave別16+10+10+12+16）。QUEUE/PROGRESSの古い表示はrename EPERMによりSTALEで、本runでは不変更。正式TODO/VERIFY/BLOCKED差分0/0/0、新規VERIFIED0、Golden PASS0、strict MATCH0、完全複製率未測定。

## Golden条件と未解明
DESIGNED/NOT RUN：検索ヒット、キャッシュ初回生成、キャッシュ再利用、helper番兵確保失敗時の例外、Spot 0x36C確保失敗時のNULL、正常終了atexit時のhelper破棄。実機観測は0件。
P0次候補：`0x005F8B71/0x005F8B79`でのinit guard unwind復帰、`0x00432DF0`が片付ける木要素の型、`0x00AC0990`のポインタ別名経由の所有権、`0x0049E490`検索ノード`+0x28`の厳密な型。

## PC・書込み・障害
PC接続成功。preflightで`active.lock=False`、認識できるJava/Ghidra/REA解析プロセスなし。CPU負荷・空きRAM・研究全体の所要時間は未測定。最終監査の単体時間は約1.394秒、独立readbackは約2.041秒。
監査初回保存時、JSON末尾にエスケープ済みの文字列`\\n`を追加したため、独立読戻しで`JSONDecodeError: Extra data`が発生。障害ID `REA-LOCAL-20261025-04H-EVIDENCE-JSON-ESCAPE-01`（OTHER / safety refusalではない）。今回新規作成した監査スクリプトの当該1行を修正し、自分の当回EVIDENCEのみ再生成、独立プロセスで`READBACK True`と38/38 PASSを確認。不正JSON時の値は採用しない。
保存先は`rea_lab/decomp_task`内の当回新規ファイルだけ。原作・MASTER・QUEUE/PROGRESS・既存runs・他レーン・Git・Work・スケジュール無変更。既拒否の`0x004BC9C0` CLI、`0x5710C0..0x571500`、Wave6/REA exportには触れていない。正式同期ではなくREA担当範囲の独立STATIC記録。
