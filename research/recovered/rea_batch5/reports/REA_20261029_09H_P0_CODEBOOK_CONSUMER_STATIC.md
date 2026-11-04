# 迫真戦記 REA｜2026-10-29 09H Ogg codebook mode1 到達性と戻値ABI
研究ID: `REA-LOCAL-20261029-09H-P0-OGG-CODEBOOK-MODE1-REACH-ABI-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。ゲームGolden NOT RUN。新規正式REA VERIFIED=0。

## 旧研究・基盤の照合
- MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、共通ルール、REA README/QUEUE/PROGRESS、最新有効sync、08H記録・証拠・readback、検索基盤README/BUILD_MANIFESTを読取。旧RUNは最新有効syncのWave1～5=64/64を維持。QUEUE/PROGRESSにはEPERM由来の古い表示がある。
- 隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、索引DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。hash一致、SQLite quick_check=ok。
- 08Hに発見された `0x005D9F40` の `[EDI+0x14]` NULL格納と直後CALL `0x005D9970` は既知として維持し、再計上しない。今回追加は **直接call graph上の到達条件と戻値/使用フィールド**。

## P0-A：mode1分岐の到達範囲
- `0x005D57C0` の検索DB上の直接callerは `0x005D5BD0`、CALL site `0x005D5BDE` の1件のみ。
- 原作x86 `0x005D5BDA PUSH 0` → `0x005D5BDE CALL 0x005D57C0`。第3引数（mode）=0を実命令で確定。 `0x005D58AF CMP [EBP+0x10],0` / `0x005D58B6 JE 0x005D5AFF` により、この既知の直接callerではmode1分岐へ進まない。
- `0x005D9F40` の検索DB直接callerは `0x005D57C0` / CALL site `0x005D5922` のみ。ここはmode != 0側である。従って08Hの「不正codebookでNULLを格納、後続でどうなるか」は **静的に存在するmode1経路の条件付き危険**であり、通常direct callerからのゲーム内再現を証明しない。関数ポインタ等の間接caller可能性はVERIFYのまま。

## P0-B：NULLが直後のhelperで使用されるとは限らない
- mode1 `0x005D9F40` の `0x005D9F72 CALL 0x005D97C0` → `0x005D9F78 MOV [EDI+0x14],EAX` はNULLを検査せず格納する。続けて `0x005D9F7B CALL 0x005D9970` → `0x005D9F80 MOV [EDI+0x2C],EAX`。
- `0x005D9970` の局所ASMは渡された **元の入力構造体** の `[EAX]` と `[EAX+4]` を読み、整数計算を繰り返す。格納直後の `[EDI+0x14]` ポインタをこのhelperが参照する証拠はなく、**直後のCALLでNULL参照が発生すると断定した見方を修正**。遅延consumerや別経路のNULL参照は未検証。
- `0x005D9970` のGhidra擬似Cは `void` と出るが、x86帰還時にEAX計算値が残り、callerが `[EDI+0x2C]` に保存する。**calleeのvoid宣言と実使用が不整合**。ABI解釈時はEAXを無視してはいけない。
- `0x005DA02E XOR EAX,EAX` → `0x005DA032 RET` より `0x005D9F40` は確認済み正常帰還で0。上位mode1ループ `0x005D5922 CALL` 後は `0x005D5927 MOV EAX,[EBP-4]` で結果を上書きし、返値エラーを判定しない。

## 監査・証拠等級・次の実施点
- `REA_20261029_09H_P0_CODEBOOK_CONSUMER_PROBE.py`: 対象ASMを隔離EXEから読む独立probe。 `REA_20261029_09H_P0_CODEBOOK_CONSUMER_AUDIT.py`: SHA/SQLite/旧sync/旧08H結果/索引6関数/直接CALL4組/native19地点を検証。**37/37 PASS、0.530秒、exit 0**。証拠JSONは `REA_20261029_09H_P0_CODEBOOK_CONSUMER_EVIDENCE.json`。
- 5種の区別: info=検索索引、pseudo=既存Ghidra機械生成物、assembly=隔離EXE局所Capstone、callers/callees=既存SQLite direct CALL。**新規REA正式5種セット=0**、既存Wave1～5 **64/64**、新規正式VERIFIED=0、正式TODO/VERIFY/BLOCKED差分=0/0/0。原作Golden実測PASS=0、完全複製率は不明。
- PCオンライン、開始時active.lock無し、先行Java/Ghidraは検索時に検出なし、RAM空き約16.01GiB。CPU使用率と研究全体の総時間は未測定。新Ghidra/REA/原作ゲーム/Workは実行せず。
- 原本ZIP/EXE/SAVE、MASTER、A～E/T018、QUEUE/PROGRESS/旧RUN、索引DB、Git/公開物/スケジュールに変更なし。10/28未同期オフライン成果は未統合。
- 次のP0: **通常mode0で実行される `0x005DA070` が生成する `[codebook+0x14]` の下流consumer** を `0x005D4D20` と関連decoder処理から追跡し、NULL/OOMリスクの到達条件をmode1と混同せず調べる。実ゲームはNOT RUN。
