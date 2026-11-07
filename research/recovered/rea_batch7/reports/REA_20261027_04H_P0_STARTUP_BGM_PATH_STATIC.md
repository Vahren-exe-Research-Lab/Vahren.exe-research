# 迫真戦記 ver0.67 REA | P0 BGMベースパスと起動条件・戻り値ABI
研究ID: REA-LOCAL-20261027-04H-P0-STARTUP-BASE-RETURN-ABI-STATIC-01
日時: 2026-10-27 04時台 JST。状態: PC-SAVED / STATIC / VERIFY / NOT READY。Golden NOT RUN。
原作EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 新規静的事実A: 0x00556F00はALにbool相当値を返す
旧Ghidra10/21検索索引の0x00556F00機械生成疑似Cは「void FUN_00556f00(void)」「return;」だが、原作PE32の命令0x00557209は MOV AL,BYTE PTR [ESP+0x17]、0x00557231は RET。
0x00556F3Bでstack byte 0x17に1を入れ、0x005571B9でBL(0)に変更する経路がある。少なくともこの戻り値は無意味なvoidではない。
親0x005554F0の0x00555904から直接CALLし、直後0x00555909でTEST AL,AL、0x0055590BでJE。索引DB双方に0x00555904→0x00556F00のCALLが登録される。
0x0055590Dは0x00559690を呼び、その返りALを0x00555914でTEST、成功側のみ0x00555918で0x00555CD0へ進む。0x00555CD0は前回までに音声初期化を含むことを確認済み。
厳密な仕様では、0x00556F00の戻り値で直接BGM初期化が決まるのではなく、さらに0x00559690の戻り値判定が介在する。0x00559690自身の戻り値の定義/全異常経路は未確認。

## 新規静的事実B: 1番目のベースパス長が初期起動時の分岐に影響する
0x00556F40はグローバルDAT_0068B380を0と比較し、非0なら0x005571DEへ分岐して通常のメッセージループを迂回する。
このグローバルは旧Ghidra索引・前回BGM研究上で第一ベース文字列DAT_0068B370の文字列長フィールド(+0x10)と整合する。2番目のベースはDAT_0068B38C。
0x00557165 MessageBoxA戻り値を0x0055716Bで6(IDYES)と比較し、Yesなら0x005571BFへ。Yes以外では0x00557175 MOV [DAT_0068B380],EBX で長さ0、0x00557183/0x00557188でSSO/heapポインタ先頭をNUL終端し、0x005571B4で0x00556F50に戻る。
0x005571B9ではWM_QUIT（GetMessageA=0）側で戻り用stack byteを0にする。この一連は「第一ベースの消去・待機再試行」と、ウィンドウ終了を区別する実装の証拠となる。
Yes選択の意味（どのパスか）、どのUIで選択させるか、DAT_0068B38Cの設定元やパス内容は未検証。実ゲームでの動作は断定しない。

## 既存成果との差分・証拠の限界
03H研究は0x004BD2A0による「第一/第二ベース + bgm/ と直接サブフォルダ」登録、および2048Bのringを既に確定。今回は起動関数0x00556F00の返り値ABIと第一ベースの消去・音声初期化条件の連鎖のみを追加。03H 65/65と正式Wave1-5 64/64を新規件数に加算しない。
原作PE32 Native Capstone20命令、両SQLite SHA256・quick_check、両DB3 CALL、旧DB直接WRITE xref 0x00557175→0x0068B380、過去65/65、64/64同期ログの計37条件PASS。
info=INDEX_ONLY, pseudo=INDEX_ONLY, assembly=TARGETED_PE_NATIVE, callers=INDEX_ONLY, callees=INDEX_ONLY。正式REA5種類の新規完全取得0、新規VERIFIED=0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。
原作Golden PASS=0、strict MATCH/完全再現率=未測定。REA/Ghidra/原作ゲーム/Work新規起動なし。既存検索DBに変更なし。
研究PCローカル接続あり・active.lock無し・開始RAM空き12.42GiB・CPU1%単発。監査実行1.218秒、save付き1.232秒。研究全体所要時間は未測定。
原本ZIP/EXE/SAVE、MASTER、QUEUE、PROGRESS、旧runs/evidence、他レーン、Git、公開先、スケジュールは不変。安全拒否操作の再試行なし。

## 次のP0
0x00559690の戻り値ABI・Direct3D初期化失敗時の分岐を機械語で独立確認し、0x00556790およびDAT_0068B370/DAT_0068B38Cの設定経路、第一パス長が0になった後にBGMバンクがどう構築されるかを照合する。長い入力の1024/2048バッファ越境到達性は条件付きVERIFY維持。

