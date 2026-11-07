# REA-LOCAL-20261024-07H-P0-B136-FIRST-INSERT-INVARIANT-STATIC-01
2026-10-24 07時台 JST / owner=REA / P0 / PC-SAVED / STATIC / VERIFY / NOT READY

## 事前照合
- MASTER_LEDGER.md、ANALYSIS_LANES_PROTOCOL.md、REA README/QUEUE/PROGRESS/WAVES、06HのMarkdown/JSON/READBACK、保存済み進捗sync、search_index README/BUILD_MANIFESTを読み取り専用で確認。PC接続成功。既存成果上書きなし。
- 進捗の実証拠: logs/progress_sync_20261011T153958076Z.json、Wave1〜5=16+10+10+12+16=64/64 VERIFIED。旧QUEUE/PROGRESSはEPERMによるstale。今回の解析分を二重計上しない。
- 原作隔離コピーSHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- search.sqlite SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（BUILD_MANIFEST一致）。

## 新規P0発見：0x47D770の入力ツリーはF9E0前にノード挿入を試みる
- 06H既知: 0x47D9B6 CALL 0x48F9E0 の第2スタック引数は固定コンテナ 0x00B136A8。今回の新規焦点は、その直前にある構築経路。
- 0x47D7D1/0x47D7DD は B136B8 初回初期化フラグを処理し、0x47D800で B136AC ヘッダを格納。0x47D817/0x47D820/0x47D82B はヘッダの自己リンクと終端フラグ+0x20/+0x21=1を作る。
- 0x47D878 ECX=0xB136A8 → 0x47D87D CALL 0x436340（旧ノード再帰解放）。0x47D887/0x47D88F/0x47D896 でヘッダを自己リンクし、0x47D89B で [0xB136B0] = 0に戻す。
- 0x47D8EB〜0x47D923の準備処理を経て、0x47D925 EDX=0xB136A8 → 0x47D932 CALL 0x476A50（0x24バイト新ノードを確保しキー/値を組立）。
- 0x47D937 PUSH 0xB136A8 → 0x47D942 CALL 0x476720（挿入ディスパッチ）。この時、新ノードのポインタは 0x47D93C MOV EBX,EAX で渡る。
- 0x476720はヘッダ終端フラグ+0x21を確認（0x47674F→0x476759）し、空ツリー経路では0x476788でヘッダの自己リンクを照合して0x476797 CALL 0x476830へ進む。0x476830の通常挿入経路は0x4768AE INC ECX → 0x4768AF MOV [EDI+8],ECXで件数を増加する。
- 0x47D98A CMP [EBP+0x94],0、0x47D991 JE 0x47DA04。**この分岐を越えた場合のみ**0x47D9B6 CALL 0x48F9E0へ進む。通常の割当・挿入が成功してこのCALLに到達した場合、入力0xB136A8は少なくとも1ノードを持つ経路が静的に確認できた。
- 従来の「このcallerに空入力を渡し得る」懸念は、**この経路の正常到達に関しては絞られた**。他4callerや例外・破損・再入・途中の副作用を含む完全な非空不変条件までは証明していない。

## NULL問題との区別
- 既存0x48F9E0では入力ツリーから出力を再構築し、0x48FBD9で0x48F720候補選択。0x48F720は候補の+0x18と比較ツリーで除外できる。**入力非空でも選択結果非NULLは保証されない**。
- 0x48FBF7は保存した候補を0x583C70へ渡す既知経路。ゲームクラッシュの実測なし。原作バグと断定しない。
- 新規の関数CALL件数を二重計上しない。06Hで既知だった0x47D9B6は、今回その直前の挿入と初回空ツリー経路を追加解析したもの。
- 検索DBの参照表は0xB136A8を0x47D878/925/937/9AE/DA25で参照すると登録。実バイト独立照合では計27命令、E8相対CALL先8箇所、索引参照site5件が全一致（重なりを含む40静的判定; 40関数解析を意味しない）。

## 判定・次
- 0x47D770/0x476720/0x476830はGhidra保存疑似Cと限定ASMを独立照合。REA正式5種(info/pseudo/assembly/callers/callees)の新規完全取得0、正式新規VERIFIED0。TODO/VERIFY/BLOCKED差分0/0/0。
- 原作ゲームGolden PASS0、strict MATCH0、完全複製率未測定。新REA0、新Ghidra0、ゲーム実行0。
- PC確認時点: CPU 6%（瞬間値）、空きRAM約14.18GiB、Java/Ghidraプロセス0、active.lockなし。総実行時間は正確に計測せず。
- 次P0: 0x476C50で新規ノード値の+0x18が確実に非ゼロか確認。0x48F720の比較ツリー除外条件を0x47D770の値と接続。別系統0x8BA6F4は0x51CEF0の初期化と0x5A4260のクリアを起点に追跡。
- この結果は静的/VERIFY/NOT READY。MASTER・他lane・QUEUE・PROGRESS・既存run・原本・Git・スケジュールには書込なし。安全拒否なし。
