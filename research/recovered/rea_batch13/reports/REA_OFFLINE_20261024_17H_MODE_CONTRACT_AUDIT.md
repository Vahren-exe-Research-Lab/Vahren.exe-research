# 迫真戦記 ver0.67｜REA P0 オフライン独立静的研究（2026-10-24・17時台）

**研究ID** `REA-OFFLINE-20261024-17H-P0-DEFERRED-MODE-FLAG-COST-DENOM-CONTRACT-STATIC-01`  
**状態** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**原本** `Vahren(2).exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`  
**資料** 旧 `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`  
**旧DB** SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`

## 0. 接続・正本の優先順位・非重複判定

17時台、Desktop Commander Local Compactで `MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、`rea_lab/decomp_task/README.md/QUEUE.json/PROGRESS.md` と検索基盤の先読を一括試行したが、**`McpServerError: MCP SSE probe returned 429 from openai.org`** により利用不能。接続障害であって安全拒否とは区別する。Windows PCの最新正本、owner/lock、CPU/RAM、現行DBのチェックは未実施。PCへの書込・新規REA/Ghidra実行なし。

代わりに実在を確認したLibraryの旧オフラインZIP、`Vahren(2).exe`、同ZIP内の古い `MASTER_LEDGER.md`・担当規約・REA `PROGRESS.md`・`search_index/README.md`・`BUILD_MANIFEST.json` を読取。旧 `PROGRESS.md` は2026-10-09時点の情報で最新REA状態ではない。全関数再抽出せず関数 `0x0052EB20`、`0x0048A4B0`、`0x004F9000` と局所CALLを検査した。

別途保存された 2026-10-22 Ghidra V3ハンドオフは標準DBを10,274内部関数（`HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite`）と案内し、V4ハンドオフは11,226内部関数のEH修復候補が**標準入口へ未昇格**と明記する。今回の旧DB10,268内部関数はそのどちらでもない。ハンドオフもPCで再確認できておらず、PCの現時点状態とは断言しない。

16時台の `REA-OFFLINE-20261024-1633-P0-DEFERRED-EXCLUSION-SET-INDIRECT-WRITER-STATIC-01` と既存証拠JSONを照合。今回のPE検査36命令箇所のうち**33箇所は直前16時台の検査対象外**、重複は3箇所。CALL検査9箇所のうち8箇所が直前16時台の対象外。**過去の全Waveとの完全な非重複証明ではない**ため、REA VERIFIEDや累計解析件数へ加算しない。

## 1. P0新発見A：遅延除外ノードに「モード由来の1bitフラグ」が入る

`0x0052EB20` では保存状態 `state+0x4A8` を `1`、`3`、`4` と比較して、いずれかなら一時的なキーのフラグを `1`、それ以外なら `0` に設定する。

```asm
0x52EC81  CMP EAX,1
0x52EC86  CMP EAX,3
0x52EC8B  CMP EAX,4
0x52EC90  XOR AL,AL     ; 他モードは0
0x52EC94  MOV AL,1      ; 1 / 3 / 4 は1
0x52ECB2  MOV [ESP+0x50],AL
```

直後の `0x52ECB6 CALL 0x0048A4B0` で新しいノードを生成する。コンストラクタでは `0x48A4D8`・`0x48A4DC` でキーの32bitフィールド2個をコピーし、`0x48A4E2`/`0x48A4E5` で **一時キー+8のバイトをノード+0x14へコピー**している。これは以前の「除外集合にノードが挿入される」事実に対する新しいフィールド意味論である。ただし、ゲーム上のフラグ名や使用箇所はまだ不明。

続く `0x004F9000` は `node+0x0C` の**符号なし32bitキーのみ**で木を検索し、同値キーなら `0x004F90B0` において新しいノードを解放して `0x004F90BB` で挿入成功フラグを0にする。この重複経路には既存ノード `+0x14` を上書きする操作がない。したがって、**この挿入処理単体では、既存キーへの再挿入はモード由来フラグの更新にならない**。ただし他の更新関数の有無や実ゲームで同じキーが再投入されるかは未証明。

## 2. P0新発見B：モード4は書込後の負担処理を省き、モード3は負担量を半減する

`0x52ED57 CMP [state+0x4A8],4` → `0x52ED5E JE 0x52EFEC` は反復中の `0x52ECC0 CALL 0x004F9000` **より後**に配置されている。すなわちモード4は候補/除外集合への処理を飛ばすのではなく、**反復処理後の追加評価・費用更新を飛ばす**。

非モード4経路では二つのコンテナを集計したのち、`0x52EE93 CALL 0x005D1B80` の結果（整数）を使用する。モード3だけは `0x52EE98 CMP ... ,3`、`0x52EEA3 CDQ`、`0x52EEA4 SUB EAX,EDX`、`0x52EEA6 SAR EAX,1` により**符号付き整数を0方向へ丸める半減**が適用される。その後、金額相当値が正で、最初の集合の要素数が `state+0x190` から取得する容量の`-2`より小さい場合に限り、`0x52EED2 SUB [EAX+0xC4],EBX` が実行される。

従って正常経路の局所モデルは以下。

| 入力モード | 除外ノードに格納するフラグ | 追加負担・補助処理 |
|---|---:|---|
| 1 | 1 | 通常の整数変換結果を使用 |
| 3 | 1 | 整数変換結果を**0方向に丸めて半減** |
| 4 | 1 | 追加負担部分を通らない |
| その他（例: 0/2） | 0 | 通常の整数変換結果を使用する分岐構造 |

**注意**: `state+0x4A8` の値域が本当に上表のすべての値に到達すること、`[EAX+0xC4]` がゲーム画面で何と表示されるかは未確定。ゲーム固有の金銭/信頼などの名称に昇格しない。

## 3. P0要VERIFY：FPU除算の分母ゼロに局所ガードが見当たらない

`0x52EB60/64/68` はスタック上の**別々の3変数**を0で初期化する。`0x52EBAE` は第1集合の積算（`[ESP+0x18]`）、`0x52EBB2` は第1集合のカウント（`[ESP+0x20]`）、`0x52EDB6` は第2集合の積算（`[ESP+0x1C]`）であり混同しない。

```asm
0x52EE7B  FILD  DWORD PTR [ESP+0x18]  ; 第1集合の積算値
0x52EE7F  FIDIV DWORD PTR [ESP+0x1C]  ; 第2集合の積算値で割る
```

`DAT_008BA714`（第2集合）が空、または第2集合の算定結果の合計が0のとき、この局所経路では分母が0になる。モード4の場合は `0x52ED5E` で手前からスキップされるが、その他のモードに**このFIDIV直前の分母非ゼロガードは確認できない**。

この観測は「ゲームがゼロ除算でクラッシュする」という確定バグではない。x87制御語、マスク状態、CPU例外、`0x005D1B80` の丸め・不正値処理、上位の状態不変条件が不明。Goldenテストでは第2集合空、合計0、モード4、それ以外を個別に比較すべき。

## 4. 正常終了時の状態と再開契約

`0x52EFF3 MOV [ESI+0x4A8],EDI`（ここではEDI=0）により正常復帰前にモードが0に戻る。`0x52EFF9 CALL 0x005A4520` は終了直前に呼び出される。正常末尾は `0x52F011 RET 4`。`state+0x4AC/+0x4B0` を**この関数内で明示的にNULLへ戻す命令は確認されていない**。外部呼出先が破棄/移動する可能性や状態オブジェクト寿命は未調査であり、キャッシュポインタが安全に再利用できるとはいえない。

## 5. 独立検証実績（今回の検査と過去の正式REAを区別）

- read-only PE32の画像ベースとsectionマップから、**指定命令36/36一致**。
- ネイティブ機械語の `E8 CALL` ターゲット9/9と、旧SQLite登録の呼出site・caller・callee9/9が一致（旧DBに紛れるE9/JMPは本結果へ加算しない）。
- ZIP・EXE・SQLiteのSHA256 3/3一致、PE image base1/1、SQLite integrity1/1、Ghidra旧pseudo SHA3/3一致、局所モードモデル6/6一致。**総68/68 PASS**。
- Python標準ライブラリのみ。新Ghidra実行0、REA実行0、原作EXE実行0、Golden新規PASS0、strict MATCH0、完全複製率未測定。
- 正式REAの `info / pseudo / assembly / callers / callees` 新規5種完全充足**0関数**、新規VERIFIED**0件**。過去報告Wave1～5 `64/64` は今回未再確認。正式TODO/VERIFY/BLOCKEDへの書込差分**0/0/0**。独立VERIFY論点は追加1件で正式キューには未反映。

検証単体の所要時間は約1秒。調査全体の時間は未計測。研究PCのCPU/RAM負荷は不明。**この68件は検査項目数であり、68関数を逆コンパイルした数ではない。**

再実行：

```powershell
python verify_rea_20261024_17h_mode_contract.py --exe 'Vahren(2).exe' --zip 'HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip' --output 'REA_17H_CHECK.json'
```

## 6. 次回P0と安全な同期位置

最優先は `0x004F9000` の**既存ノード+0x14フラグ消費元**の読取追跡と、`0x0052EB20` に渡る `DAT_008BA714` の生成・合計ゼロ到達条件。次に `0x005A4520` による参照先の破棄順・所有権を調べる。モード別の実機Golden候補は「同キーをモード1/4で連続投入した場合」「モード3の奇数半減」「第2集合空/ゼロ積算」「モード4による評価バイパス」「正常終了直後のstateポインタ寿命」。いずれも未実測・未実装。

PC復帰時は現行V3/V4のアクティブ状態を最新の`CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json`と検証器で確かめ、最新MASTER/QUEUE/PROGRESS/owner/lock・ハッシュ・既存ID・衝突を照合してからREA所有の未同期成果だけを一度反映する。安全拒否済みVA/Wave6/REA exportを繰返さず、他レーン・MASTER・Git・原本・スケジュールは変更しない。

**RECOVERY-ID** `REA-RC-20261024-17H-LOCAL429-OFFLINE-01`。接続失敗の影響はPC正本同期・正式REA再認定・現行DB比較ができないこと。オフライン側では根拠と再現スクリプトを独立保管して継続した。
