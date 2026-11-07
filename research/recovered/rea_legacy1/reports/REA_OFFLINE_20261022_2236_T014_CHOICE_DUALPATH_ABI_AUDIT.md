# 迫真戦記 ver0.67｜REA独立・choice 13バイト分岐の原本機械語解決

- 独立ID：`REA-OFFLINE-20261022-2236-T014-CHOICE-DUALPATH-ABI-STATIC-01`
- 実施日：2026-10-22 22時台（JST）
- 分類：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- 所有範囲：REA独立証拠のみ。T014/T006の正式レーン、MASTER、QUEUE、PROGRESS、原作EXE、Git、他研究レーン、既存自動化は未変更。
- 今回の増分：**前回21:37に未読だった13バイトを原作EXEから実際に取得**し、独立した別分岐であることを機械語・相対分岐・SQLite索引の3観点から確かめた。以前の11件を新規発見と二重計上しない。

## 基盤・アクセスの記録

PC正本への `Desktop Commander Local Compact.read_multiple_files` は `UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org` で失敗（原因区分 CONNECTION / RATE LIMIT、**SAFETY_REFUSALではない**）。PC稼働状態、実CPU/RAM、active.lock、現行MASTER/QUEUE/PROGRESS/旧runsの最新版は未確認。安全拒否済みのVAやWave6・REAエクスポートを別経路で試していない。

許可済みChatGPT Libraryの実在する `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren.exe` を読み取り専用で材料にした。前者は34ファイルでZIP CRC PASS、後者SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回実測）。ZIP SHA256=`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`（今回実測）。展開した検索DBは`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（今回実測、マニフェストと一致）、SQLite `PRAGMA integrity_check=ok`。Ghidra 12.1.4の既存2026-10-21出力を利用し、新規Ghidra・REA・原作ゲーム実行はいずれも0。

オフライン包内の`research_snapshot/MASTER_LEDGER.md`、`research_snapshot/evidence/ANALYSIS_LANES_PROTOCOL.md`、`research_snapshot/rea_lab/decomp_task/PROGRESS.md`、検索DBのREADME/BUILD_MANIFESTを読取。旧PROGRESSの初期キューは15/16 VERIFIED（2026-10-09時点）。別の過去報告でいうWave1–5の64/64は現在正本未照合の**過去値**で、双方の累積加算なし。既存`runs`の最新現物は今回未取得。

## 重要な訂正：13バイトは「仮想CALL直後に実行する後処理」ではない

前回21:37の `REA-OFFLINE-20261022-2137-T014-CHOICE-BRANCH-SPAN-STATIC-01` は `0x41E8B3 JNE 0x41E8CE` が間接CALL `0x41E8BF` の後ろ13バイトを跳び越す、と正しく計算したが、その13バイトの役割は未確定だった。

今回、原作EXEから以下を独立して取得した（データはVA 0x0041E8C1～0x0041E8CDの連続13バイト）。

```asm
0x41E8C1   EB 0B             JMP 0x41E8CE
0x41E8C3   6A 00             PUSH 0
0x41E8C5   6A 01             PUSH 1
0x41E8C7   33 DB             XOR EBX, EBX
0x41E8C9   E8 52 53 03 00    CALL 0x453C20
0x41E8CE   A1 70 B7 8B 00    MOV EAX, [0x008BB770]
```

**`0x41E8C1`は無条件JMPであり、直前の間接CALLの正常復帰後は`0x41E8C3`に落下しない。** `0x41E8C3`にはより前の`0x41E877`から独立した条件分岐が到達する。つまり、問題の13バイトは「後処理の余剰区間」ではなく、**通常経路を飛ばすJMP（2バイト）＋別経路専用ブロック（11バイト）**だった。前回のアドレス差13自体は正しいが、それを「間接CALLの追加副作用候補」と捉える必要はない。

### 2つの分岐条件は別物

原本実命令から得られる局所制御フローは次のとおり。

```text
0x41E86C  CALL EDX       ; [global +0x0c] 由来の間接呼出し
0x41E86E  PUSH 0         ; 後続の2経路に共通する先行引数
0x41E870  MOV ECX, 0x008BB6D8
0x41E875  TEST AL, AL
0x41E877  JNE 0x41E8C3 ───────────────────────┐
             │ AL==0                          │ AL!=0
0x41E881  CALL EDX ([global+0x24])           │
             │                                │
        choiceキーを0x416B90で登録               │
0x41E8B3  JNE 0x41E8CE (map登録前件数>0)        │
             │ map登録前件数==0                │
0x41E8BF  CALL EDX ([context vptr+0x1c])       │
0x41E8C1  JMP 0x41E8CE                         │
                                              │
                                   0x41E8C3 PUSH 0
                                   0x41E8C5 PUSH 1
                                   0x41E8C7 XOR EBX,EBX
                                   0x41E8C9 CALL 0x453C20
                                              │
                                  0x41E8CE <──┘
                          共通の decide11 引数による仮想CALL
```

- `0x41E877`短分岐 `75 4A` → `0x41E8C3`（`AL!=0`）。`AL`は直前の間接CALL `0x41E86C`の戻り値下位バイト。呼出先VA/全実行条件は未確定。
- `0x41E8B3`短分岐 `75 19` → `0x41E8CE`（登録前map件数がゼロでない経路）。`AL`分岐とは独立。
- `0x41E8C1`短ジャンプ `EB 0B` → `0x41E8CE`。したがって`0x41E8BF`のCALL後は、別経路の描画処理を**実行しない**。
- `0x41E8C9`はx86の相対CALL実測 `E8 52 53 03 00` → `0x453C20`。Ghidra直接CALL索引も同site/targetで一致。`0x41E8AC` → `0x416B90`も索引一致。
- `0x41E8CE`以降は両側が収束。Ghidra疑似Cでも`"decide11"`に相当する最後の間接CALLを確認。異なる分岐の共通終端処理を省かない。

### 別経路の引数契約

`0x453C20`は保存済みGhidra疑似Cで`BitBlt`、条件付き`DrawFrameControl`等を持つ描画関連関数候補。`0x453F1C RET 0x0C`を原作機械語で確認。呼出時のstack引数は、**分岐より前の`0x41E86E PUSH 0`と、分岐先の`PUSH 0; PUSH 1`の計3つ**。このため先頭引数から `1, 0, 0` の順となる（ECXは`0x008BB6D8`）。古いGhidra疑似Cの`FUN_00453c20(1,0,0)`とも整合。呼出先が正常RETを実行すれば3個の4byte引数を回収する。

ここで分岐前の`PUSH 0`を見落とすと、引数は2個なのに`RET 0xC`だと誤解し、誤ったABI・スタック不整合を報告する可能性がある。**今回この呼出siteのスタック対応も追加証拠とした。** 描画が毎回発生するとは断定しない（内部条件がある）。

## 独立検証

`verify_rea_t014_choice_dualpath_20261022.py`で原作PEのsection/RVAをstd-libのみで解析し、28命令列の原本バイト一致、相対分岐3箇所・CALL2箇所の再計算、SQLiteの関数擬似Cハッシュ2件、直接CALL索引2件、間接CALL索引4箇所、PRAGMA integrity_check、SHA、ZIP CRC、前回の21:37 JSONとの非重複連携を行った。すべてPASS。スクリプト実測時間**約0.60秒**。研究全体の所要時間・PC負荷は未計測/不明。

対象となったGhidra擬似Cのハッシュ：`0x41E710 = 202C2A1909EB7873AE758A24290D535EB3DFB640CE7CBE905580A68BCCB99F6F`、`0x453C20 = 3C4DD8B2AF010A0003F91F8DEDD5681B7EA252CC18CA48FAE79B9D154188BDED`。自動抽出の擬似Cは**REA正式5種証拠**（info/pseudo/assembly/callers/callees）の代わりではない。

## 差分、未確定点、次の再開位置

- 旧「13バイト未読」VERIFY：**今回の独立静的確認で解決**。旧アドレス算術は訂正不要だが、余剰後処理の可能性という留保は具体的な二分岐構造へ更新する。
- 関数`0x41E710`および`0x453C20`のABIと分岐を局所的に確認。関数全域・すべての実行時例外経路、描画成否、実動作までは未確定。
- **次P0**：`0x543428` の`context+0x10` writer、実際のvptrとvtable+`0x1C`の呼出先VAの解決。既存DBで`0x5433D0`/`0x4321B0`から取得する。拒否済みVAには触れない。
- **次P0補助**：choice の`0x41E86C`/`0x41E881`が具体的にどのインスタンスのvptr+0x0C/+0x24を使うかは未確定。静的に固定できる範囲だけ確認。
- 研究PC復帰後：MASTER/QUEUE/PROGRESS/旧runs/evidence/owner/lock/既存ID/ハッシュ/競合を確認し、REA所有資料へ安全な増分のみ一度同期。A所有T014/T006やMASTERを直接編集しない。

正式REAの新規VERIFIED **0**、新規5種完全充足 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**（PC正本未変更）、ゲームGolden実測PASS **0**、strict MATCH **0**、完全複製率 **未計測**。今回の研究結果はオフライン証拠でありREADYにはしない。

**接続復旧ID**：`REA-RC-20261022-2236-LOCAL-429-01`、試行：Local CompactでPC資料を読取、結果：MCP SSE probe 429、未保存発見：PC正本同期不能、影響：最新PROGRESS/所有権未確認、許可された次手：Libraryに独立証拠保存→復帰時再照合。安全拒否は新規なし。新Ghidra/REA実行なし。
