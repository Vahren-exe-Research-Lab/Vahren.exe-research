# 迫真戦記 REA｜2026-10-29 08H Ogg codebook長配列の拒否境界（静的モデル）
研究ID: `REA-LOCAL-20261029-08H-P0-OGG-CODEBOOK-VECTORS-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作実機GoldenはNOT RUN、正式新規REA VERIFIED=0。
## 開始前・重複回避
- Desktop Commander Local経由でMASTER、レーン規約、共通作業規則、REA README/QUEUE/PROGRESS、最新有効sync、07H成果、検索DBのREADME/BUILD_MANIFESTを照合。直近07Hの57/57 PASSは既存成果として維持し、再加算しない。
- 最新有効sync `progress_sync_20261011T153958076Z.json` はWave1～5が **64/64 STATIC VERIFIED**。QUEUE/PROGRESSは一部EPERM由来のstale。正式TODO/VERIFY/BLOCKEDの差分は **0/0/0**。
- 解析対象は隔離EXEのSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、検索DBは `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。両SHA一致、SQLite quick_check=ok。
## P0-A｜拒否分岐の命令レベル根拠
- `0x005D97C0` で、コード長が正かつ32未満のとき `0x005D981D CMP ECX,0x20` → `0x005D9824 SHR EAX,CL` → `0x005D9828 JNE 0x005D993D`。現在の符号の使用量が `value >> length != 0` なら、`0x005D9941 CALL _free` 後にNULLを返す。
- 全コードを処理した後、引数3が **1以外** なら `0x005D98C2 CMP ESI,1` / `0x005D98C5 JE` で検査を実行。`0x005D98D5 SUB ECX,EAX` / `0x005D98DA SHR EDX,CL` / `0x005D98DC TEST` / `0x005D98E3 JNE 0x005D9952`。各len=1..32の状態値の下位lenビットが非0なら `0x005D9953 CALL _free` 後NULL。
- nativeの17命令署名と2 callerのSQLite直接CALL siteを独立照合。caller `0x005DA070` / site `0x005DA0C7` は第3引数へ正の長さの数を渡す。caller `0x005D9F40` / site `0x005D9F72` は保存済Ghidra擬似C上で第3引数0。両者を同じ検証モードと誤認しない。
## P0-B｜Python 32bit状態遷移モデルによる具体的な入力例
- **[1,1,1]、第3引数3 → 前段拒否 `0x005D9828`**。2件消化後、長さ1の状態値が2となり、3件目では `2 >> 1 !=0`。過剰割付のテストベクトル。
- **[2,2]、第3引数2 → 後段拒否 `0x005D98E3`**。前段は通過するが最終状態の長さ1下位ビットが残る。不完全なコード空間のテストベクトル。
- **[1,2] → 後段拒否**、**[1,2,2] → 非NULL**、**[2,2,2,2] → 非NULL**、**[1,1] → 非NULL**。これらは静的モデル上の結果であり、Ogg bitstreamの合法性や実ゲーム動作の証明ではない。
- **[1] を第3引数1で渡すと非NULL、第3引数0で渡すと後段拒否**。第3引数1では最終検査をskipするnative分岐があり、上位呼び出し元ごとに同じ長さ配列でも判定が違う。0を含む[0,1]でも同じ差をモデル確認。
- [32]も第3引数1で非NULL/0で後段拒否。長さ33以上は配列境界問題があり、このモデルからは除外した。malloc失敗や実機エラー後処理も未検証。
## 根拠・限定・保存
- 監査: `REA_20261029_08H_P0_CODEBOOK_VECTOR_AUDIT.py` が隔離PE Capstone、SQLite直接CALL・関数擬似C SHA、既存sync、16ベクトルを照合し、**46/46 PASS、0.479秒、exit 0**。`REA_20261029_08H_P0_CODEBOOK_VECTOR_EVIDENCE.json` に全ベクトル/各チェックを新規保存。
- 5方法: info=SQLite関数索引、pseudo=既存Ghidra機械出力、assembly=隔離PE局所命令、callers/callees=既存callgraph。この回で新しく取得したREA正式5種一式は **0**、新規正式VERIFIED **0**、既存64/64維持、ゲームGolden PASS=0、完全複製率未測定。
- PCオンライン。開始時active.lock無し、Java/Ghidra先行プロセス無し、空きRAM約16.15GiB。CPU負荷と研究全体の所要時間は不明。新規Ghidra/REA、原作ゲーム/Workは起動していない。
- 原本ZIP/EXE/SAVE、MASTER、A～E/T018、既存RUN、QUEUE/PROGRESS、検索DB、Git/公開先/スケジュールは未変更。既往10/28未同期Library研究は未統合のまま維持。
- **次のP0**: `0x005D9F40` が `0x005D97C0` のNULLを格納した後に0を返す可能性のある上位エラー処理・NULL使用consumerを追跡。並行して `0x005DA070` の単一正長codebookが正常に初期化完了するかはNOT RUNで留保。
## 08H追補：第3引数とNULL戻り値のnative callsite
- `REA_20261029_08H_P0_CODEBOOK_CALLSITE_PROBE.py` で隔離PEを再読込。`0x005D9F6E PUSH 0` → `0x005D9F70 PUSH EAX` → `0x005D9F71 PUSH ECX` → `0x005D9F72 CALL 0x005D97C0` を独立ASM確認。引数3=0は擬似Cだけの推定ではない。
- 同callerは `0x005D9F78 MOV [EDI+0x14],EAX` でNULLを含む戻り値を保存し、直後に `0x005D9F7B CALL 0x005D9970`。この局所区間にEAX=0のガードは無い。関数全体・上位のエラー扱いは次回VERIFYであり、実機不具合確定ではない。
- 反対側では `0x005DA0C4 PUSH EDI` / `0x005DA0C5 PUSH ECX` / `0x005DA0C6 PUSH EDX` / `0x005DA0C7 CALL` を独立確認。両callerの第3引数の差は原作命令で確認済み。追補probeは上記46/46監査とは別の読取専用実行。
