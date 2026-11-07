# REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01
2026-10-24 09時台 JST / REA P0 / PC-SAVED・STATIC・VERIFY・NOT READY

## 先行確認と重複防止
- MASTER・ANALYSIS_LANES_PROTOCOL・REA README/QUEUE/PROGRESS・runs目録・08H静的報告/JSON・検索README/BUILD_MANIFESTを先読。検索CLIから0x48F720、0x48F9E0、0x565780、0x5158E0、0x47D770、0x4868D0および0x1eed34/0x1eed30参照を確認。
- 既知の「外側1ノード、内側count=1、フィルタあり」を再発見件数に加算しない。今回の対象は **3種RB-treeのsentinel ABI、unsignedの除外契約、および戻り値ゼロの二義性**。
- 原作承認済みコピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。検索DB SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、BUILD_MANIFEST一致。
- 最新保存済みsync（20261011T153958076Z）=Wave1-5 64/64、旧QUEUE/PROGRESSはrename EPERMでstale。新規5種証拠完結0／新規REA VERIFIED0。MASTER/他レーン/QUEUE/PROGRESS/既存run等への書込みなし。

## 新規A：見かけが似た3種類のRB-treeノードを混同できない
| 役割 | sentinel byte | キー | 静的根拠 |
|---|---|---|---|
| 外側候補tree | node+0x21 | node+0x0C | 0x48F790 / 0x48F799 |
| 除外対象tree（context+0x1EED30、headは+0x1EED34） | node+0x19 | node+0x0C | 0x48F73C / 0x48F747 / 0x48F760 |
| 内側データtree | node+0x11 | node+0x0C | 0x5158EE / 0x515900 |
- 全て単純な「同一レイアウトのset/map」として実装するのは誤り。共通iteratorを作るなら **ノード型ごとのsentinel offset** を引数として明示すること。
- sentinelは値0の通常ノードと非0の終端ノードを分岐する。外側の+0x18は内側treeの件数でありsentinelではない（08H既知）。

## 新規B：0x48F720の除外条件は外側キーのunsigned等値判定
- 0x48F73Cはheadを[EBP+0x1EED34]から取得。0x48F752の比較と0x48F755 JAE、0x48F773/0x48F776 JBは **unsigned 32-bit** キー順を使う。
- 比較tree内に **同じ外側キー+0x0C** が存在したら棄却。存在しなければ0x48F78Aの内側件数非ゼロを検査し、0x48F7ED→0x48F7F2で **内側先頭ノードのキー+0x0C** をEAXで返す。
- 先頭候補が除外・内側空の場合は外側treeの次候補へ進む。最後まで不採択なら0x48F7E4のXOR EAX,EAXで0を返し、0x48F7EA RET 4。

## 新規C：正常な選択でも返値0を排除できない（ゲーム到達はVERIFY）
- 08Hは「内側tree件数が正」を固定。**これは戻り値非ゼロを証明しない**。0x48F7F2は内側先頭ノード[EDX+0x0C]を無検査でEAXへコピーする。
- 0x5657AF→0x5657B3→0x5657B5は呼出元が渡した値を新規ノード+0x0Cへ無条件に複製。0x5158E0初回空tree挿入（0x51593A）ではキーが0かどうかの検査は示されない。この範囲に限り、ノードの存在とキー非ゼロは別条件。
- 0x47D8EBの[ESP+0xE0]アドレスを0x47D8F2で0x565780へ渡す経路を確認。ただし、そのスタック値の由来と、原作の有効入力で値0が起こることは未証明。
- よってF720のEAX=0には、(a)採択できる候補なし、(b)採択された内側先頭キーが0、という **静的に区別できない2種の帰結** がある。後者の実到達はVERIFY。
- 下流は0x48FBD9 F720→0x48FBDE EAXをESI保存→0x48FBF5 ESIからEAX再設定→0x48FBF7 CALL 0x583C70。0x583C76は[EDI+0x94]を局所NULLチェックなしに参照する（従来既知）。現実の原作クラッシュは未観測、確定バグとは扱わない。

## 機械検証・再現性
- 独立監査 `REA_20261024_09H_P0_THREE_TREE_PREDICATE_AUDIT.py`：原作機械語指定29/29、相対E8 CALL 7/7、Ghidra索引の対象5関数行5/5、一時的な **合成モデル** 4/4 PASS。合成モデルはゲームGoldenに算入しない。
- 関数SHAは索引から読み、F720 2D9CB26D..., 5158E0 84C96699..., 565780 C08510FE..., 47D770 606F18A9..., F9E0 01FA8FF9...を確認。証拠は部分ASM＋検索済疑似Cであり正式REA 5種(info/pseudo/assembly/callers/callees)の新規完成ではない。
- 既存Wave1〜5:64/64 VERIFIED（保存済みsync値）、新規VERIFIED0／正式TODO-VERIFY-BLOCKED差分0/0/0。実機Golden PASS0、strict MATCH0、完全複製率未測定。新規REA・Ghidra実行0、原作ゲーム起動0。
- PC接続成功、active.lockなし、空きRAM約14.25GiB、Java/Ghidraプロセス検出なし（調査前）。CPU・全実行時間は未計測。
- read-only syncをPowerShell標準読込した最初の試行で日本語パスが文字化けしConvertFrom-Jsonに失敗。監査スクリプト側でUTF-8 read_textして正常確認。**接続障害・安全拒否ではない**。ファイルは変更なし。

## 次のP0
1. 0x47D770の0x47D8EBで使用する[ESP+0xE0]スタック値の生成源と非NULL条件を追う（0x565780入力実体同定）。
2. context+0x1EED30比較treeへの書込・消去元、0x47D9B6到達前のkey集合を追い、0x48F720採択条件が満たされるかを判定。
3. 0x521D90→0x8BA6F4など他のF9E0 callerも個別の正常到達条件を解析。Goldenは本家ゲーム実測まではNOT RUN。
