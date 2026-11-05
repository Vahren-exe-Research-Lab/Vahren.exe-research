# 迫真戦記 ver0.67｜REA T014 局所静的証拠：`GameManager+0x1EF150`の解除経路と遮断先

- **研究ID**：`REA-OFFLINE-20261023-0545-T014-LATCH-RELEASE-READERS-STATIC-01`
- **時刻**：2026-10-23 05:45 JST（オフライン研究）
- **分類**：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- **範囲**：REA独立読取・検証のみ。原本EXE/ZIP/SAVE、研究PC正本、A〜E・MASTER・T018・Git・スケジュールは変更しない。

## 1. 入手資料・先行成果・重複防止

Desktop Commander Local CompactでMASTER・規約・REA README/QUEUE/PROGRESSへの先読みを試行したが `UNAVAILABLE: MCP SSE probe returned 429 from openai.org`。**安全拒否ではなく接続制限**。PCのオンライン状態・CPU/RAM・active.lock・現行正本は不明。再試行を繰り返さず、実在・権限を確認できたChatGPT Libraryの`Vahren.exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`decomp_task.zip`を読取専用で利用。ZIP内 `research_snapshot/evidence/ANALYSIS_LANES_PROTOCOL.md` とMASTERの旧コピー、旧REA README/QUEUE/PROGRESS、検索基盤README/BUILD_MANIFESTを参照した。旧REA ZIPのCRC PASS、検索パック全34エントリCRC PASS、検索DB integrity_check=ok。旧PROGRESSは15/16の歴史的値で、後日の64/64報告と合算しない。

| 原資料 | SHA256（現物照合） |
|---|---|
| 原作EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| 2026-10-21オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内検索SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

既存REA 2026-10-23 03:31で`+0x1EF148`の同disp32機械語16サイトは**読出しのみ**、書込元未解決と報告。04:34で`+0x1EF150`によるFadeSheetカウンタ巻戻しと、`0x54344D`の1代入を報告済み。今回の新規増分は**`+0x1EF150`の解除3サイトを機械語で特定し、同フィールドの全8個の直接disp32サイトを読み4/書き4に分類、3個の解除がそれぞれ異なる条件から到達する点を根拠付けたこと**。旧知のSETや巻戻しは二重計上しない。E/A等の現行正本には未照合のため、他レーンの新規件数に加算しない。

## 2. 原作 `.text`全体の厳密なdisp32検索と証拠

PE32 `.text`の実raw領域で4バイトLE変位 `50 F1 1E 00` を検索すると**8サイト**。各サイトで命令先頭のopcodeを原作EXEから照合し、保存済みSQLiteの対応する8関数の個別擬似C SHAを確認した。これは**完全な別名参照や構造体コピー、全命令意味論の網羅ではない**。

| site VA | 親関数VA | 実命令要約 | 分類 |
|---|---|---|---|
| `0x4414B0` | `0x441460` | `CMP BYTE [EAX+0x1EF150],0` | 読出し |
| `0x4DBC7E` | `0x4DBA80` | `MOV BYTE [ECX+0x1EF150],0` | **解除①** |
| `0x4DBD66` | `0x4DBCE0` | `MOV BYTE [EDX+0x1EF150],BL` | **解除②** |
| `0x513C82` | `0x513C60` | `CMP BYTE [EAX+0x1EF150],0` | 読出し |
| `0x521D5C` | `0x521A00` | `MOV BYTE [ECX+0x1EF150],BL` | **解除③** |
| `0x526B34` | `0x526A40` | `CMP BYTE [EAX+0x1EF150],0` | 読出し |
| `0x54344D` | `0x543440` | `MOV BYTE [EAX+0x1EF150],1` | 設定（既知） |
| `0x543966` | `0x543900` | `CMP BYTE [EDX+0x1EF150],0` | 読出し（既知） |

`0x4DBD46 XOR EBX,EBX` と `0x521A8D XOR EBX,EBX`が原作機械語で成立し、当該通常経路でBLを0として流すことを支持する（関数呼出規約や全ての不正飛入経路まで動的に証明していない）。よって直書き0が1箇所、BLを介した0書込が2箇所、設定1が1箇所の計4書込サイト。

## 3. 3つの解除経路の個別条件

**解除① `0x4DBC7E`**：`0x4DBC37`で`[ESI+0x1E0]+1`を更新し、`0x4DBC40`で上限`[ESI+0x1E4]`と比較、`0x4DBC42 JG 0x4DBC78`で完了分岐。`[ESI+0x70]→+4`で受信者を取り、`0x4DBC7E`でラッチを0にして、`[ESI+0x1B8]`も0にする。その後`0x4DBC8C`からvtable `+0x24`を経由して`"change"`通知を呼ぶ。完了前は`0x4DAEF0(1)`経路に進み、同じ解除を行わない。

**解除② `0x4DBD66`**：`0x4DBCE0`内で`PtInRect`結果が真になったあと、`[ESI+0x208]`を加算して閾値`[ESI+0x20C]`を超えた場合、`0x4DBD50 JG 0x4DBD5D`から`[ESI+0x98]→+4`の受信者へ`BL=0`を書き込み、`[ESI+0x1E0]`も0にする。その後vtable `+0x24`の`"change"`を呼ぶ。入力が矩形外・未達閾値の場合はこの解除を書き込まない。

**解除③ `0x521D5C`**：`0x521A00`では`0x521C89 MOV ECX,[ESI-0x8C]`により受信者候補を取得し、`[ECX+0x20]==0`、参照先`+0x1EEC4C`、対象フラグ`+0x24/+0x25`、グローバル`0x8BA1C8/1CC`と`0x8BA064/0x8BA044`を段階的に照合する。特定の入力/条件を通った`0x521D4A JG`または`0x521D52 JNE`から`0x521D5C`へ進み、BL(0)を書き込む。`0x521D54`で最後のグローバル条件により解除をスキップする経路もある。したがって**無条件解除ではない**。この関数のGhidra疑似Cにジャンプテーブル解析警告があるため、全前駆支配関係の完全証明はVERIFY。

**重要な順序**：解除①・②ではラッチを0にしてから関連オブジェクトのフラグを0にし、**その後**仮想`"change"`コールバックを呼ぶ。コールバック前に既に解除済みとなり得るため、「change後にだけ解除する」互換実装は静的順序と一致しない。ただしcallbackが実ゲームで何を行うかは別問題。

## 4. 読出し4経路は用途が違う

- `0x4414B0`は非ゼロなら`0x4414BB JNE 0x441CF9`へ移動して、通常の後続処理を飛ばす。
- `0x513C82`は`+0x1EF148 != 0`、`[receiver+0x20]==0`かつ`+0x1EF150==0`という**3つの条件**を満たす場合だけ続く。
- `0x526B34`にも同型の3条件（`+0x1EF148 != 0`、map要素数0、ラッチ0）があり、ラッチ非ゼロなら`0x526B3B JNE 0x526E34`へ分岐する。ただし2関数の具体的入力/画面効果は独立未実測。
- `0x543966`はラッチ非ゼロなら`0x54396D JNE 0x543959`となり、FadeSheetの進行カウンタを1戻して復帰する（04:34の既知事実）。

設定経路は`0x543440`の `0x543445 CALL 0x5433D0`の**後**、`0x54344D`で`+0x1EF150=1`にする。既知の`0x5433D0`内map初回登録・仮想CALL可否とは別に、**ラッパーへの通常復帰後にラッチを設定する**構造。仮想CALLが必ず成功したか、描画が完了したかを示すフラグだと決め付けない。

### 再実装/G0・Goldenの未実行試験条件

同一プロセス・同一Sheetインスタンスで、`0x543445`呼出前後の`GameManager+0x1EF150`、どの解除サイトを通ったか、解除前後の`+0x1B8/+0x1E0`、`"change"`callback入口、`0x54396D`による巻戻し、`+0x1EF148`と`+0x1EF144`の値、戦闘初期化`0x48D6A0`入口を時刻・呼出site・同一オブジェクトIDと合わせて採録する。解除処理の通過だけで合法プレイヤーUI由来のG0や実機Golden PASSと断定しない。戦闘入口の別調査・EのT018採録条件を横取りせず、独立証拠として渡す。

## 5. 独立検証・未解決・記録状態

- 検証器：`verify_rea_t014_latch_lifecycle_20261023.py`。原作PE `.text`の8サイトの実命令バイトとオフセット集合、追加9命令、相対分岐7件、保存済み擬似C 8件の個別SHA、SQLite直接CALL1件、ZIP CRC/検索DB SHA/DB整合性を**合計47個の条件で検証し、PASS**。プログラム実行は検証器のみ。検証器単体実行1.368秒、調査全体の所要時間は未計測。
- `+0x1EF150`直接記載8件（読4/書4）の**調査範囲限定**。別名・bulk copy・他セクションの実行・動的コード生成は未調査。`+0x1EF148`書込元は引き続き**未解決**（今回も証拠を捏造しない）。また3つの解除関数が常にグローバルGameManager実体を指すこと、画面内の全到達条件も未実測。
- 正式REAの**info/pseudo/assembly/callers/callees新規5点セット0件**。今回新規正式VERIFIED **0件**。過去Wave1〜5の64/64は前回過去報告値、最新PC正本では未再確認。正式TODO/VERIFY/BLOCKED更新**0/0/0**（最新値は不明）。ゲームGolden PASS **0**、strict MATCH **0**、完全複製率**未測定**。新Ghidra/REA実行0、原作ゲーム起動0。PC負荷不明。
- 研究成果の保存先：ChatGPT Libraryの`/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`に今回IDの報告/JSON/再検証Pythonのみ新規作成予定。**Libraryアップロードの実成否は別途readback照合後に更新する**。研究PC正本への同期なし。

**接続障害/再開記録ID**：`REA-RC-20261023-0545-LOCAL-SSE429-01`。対象：MASTER/規約/REA README・QUEUE・PROGRESS・runs・evidence・active.lockの先読。試行：Desktop Commander Local Compact `read_multiple_files`。失敗理由：MCP SSE 429（CONNECTION、非安全拒否）。未保存：本増分はWindows正本未保存・Libraryへ分離記録。影響：所有権最新照合と正式台帳反映不可。許された再開：PC復帰時に最新QUEUE/PROGRESS/MASTER/owner/lock/既存run/同一source SHA・研究ID衝突を比較し、REA所有資料だけ安全に**一度**採録する。既拒否VA・Wave6・REA export等の迂回は行わない。

**次回P0**：まず`+0x1EF148`の別名/バルク書込元探索（直接disp32での不存在と**書込不存在**を混同しない）。次に`0x521A00`の解除③入口と`[ESI-0x8C]`受信者生成元の確定、`+0x1EF150`解除→FadeSheet再開→`0x1EF144=2`への遷移経路を局所追跡。ゲームGoldenは引き続きNOT RUN。
