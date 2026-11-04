# 迫真戦記 ver0.67 REA｜P0 BGM探索バンク構築・直下ディレクトリ列挙・2KiBリング領域
研究ID: REA-LOCAL-20261027-03H-P0-DMUSIC-2K-RING-BGM-SUBDIR-BANK-STATIC-01
実施: 2026-10-27 03時台 JST。分類: PC-SAVED / STATIC / VERIFY / NOT READY。Golden: NOT RUN。
対象EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 既存成果との差分
02Hでは0x004BDAF0の2つの検索パスバンクと0x00406CF0（16×1024B）の存在確認まで完了。本研究では初期化側の0x004BD2A0と別ヘルパー0x00406D50を限定解析し、バンクに投入されるパス形式、ディレクトリ列挙条件、独立した大容量バッファを追加固定した。02H 56/56、旧REA 64/64を新規に二重計上しない。

## 新規STATIC A：二系統の「bgm/」+直下ディレクトリ
0x004BD2A0は第1の動的ベースパスDAT_0068B370、第2のDAT_0068B38Cを使用する（いずれも実行時の文字列内容は未確定）。
原作の文字列定数0x0062FFC8・0x0062FFE4は「bgm/」、0x0062FFD0・0x0062FFECは「bgm/*」、0x0062FFDC・0x0062FFF8も「bgm/」、0x0062FFD8・0x0062FFF4は「/」。
第1バンクでは0x004BD4CF→0x00406D50で基点「ベース+bgm/」を作成し、0x004BD51E→0x00429A00で登録。0x004BD563→0x00406CF0で「ベース+bgm/*」を作り、0x004BD56CのFindFirstFileAを実行する。
検索結果は0x004BD580のFILE_ATTRIBUTE_DIRECTORY(0x10)を満たしたときだけ候補となり、0x004BD5C8/0x004BD618の比較分岐を通過すると0x004BD664→0x00406D50で「ベース+bgm/+ディレクトリ名+/」を構築、0x004BD6A8→0x00429A00で登録される。0x004BD6DBのFindNextFileAで次の候補へ進み、0x004BD6EFでFindCloseする。
第2バンクでも0x004BD775→0x00406D50と0x004BD7C0→0x00429A00で基点を追加し、0x004BD805→0x00406CF0と0x004BD80EのFindFirstFileAで列挙。0x004BD821でディレクトリ属性を確認後、0x004BD8D0→0x00406D50で直下名を加え、0x004BD917→0x00429A00で第2バンクへ追加し、0x004BD956/0x004BD966でFindNextFileA/FindClose。
**確認されたこの関数内の列挙はベース直下の「bgm」配下を一階層調べる構造で、再帰処理の存在までは確認していない。** 2つの動的ベースパスの役割・優先設定元はVERIFY。

## 新規STATIC B：0x00406D50は独立した16×2048Bリングバッファ
0x00406D50はDAT_00AC0864をインクリメントし0x10で0へ戻す（0x00406D50, 0x00406D5C, 0x00406D61, 0x00406D68）。
0x00406D6DのSHL EAX,0xBにより2048B単位のスロットを選択、0x00406D75でDAT_00AB4460をベースにし、0x00406D70/0x00406D7Eで2048B memsetを呼ぶ。0x00406DAFのrep movsdと0x00406DBBのrep movsbで複数のNUL終端文字列を連結する。
既知の0x00406CF0は別カウンタDAT_00AC0860、別ベースDAT_00ABC460、16×1024B。0x00AB4460+0x800×16=0x00ABC460で、両バッファ群はアドレス上で隣接する。
0x00406D50の0x78バイトを独立逆アセンブルした範囲では、CMPはカウンタの0x10比較だけ。連結する全入力長を0x800と照合するチェックは見つからない。合計長+NULが2048以下ならスロット内、2049以上ならスロット容量超過の条件付き危険がある。
ただしスクリプト/入力側の制限、OSのパス長制限、長い入力の実行到達性は未確定。クラッシュ・実際の破壊の発生は未証明で、P0 VERIFYを維持。0x00406CF0の1024B側についても従来のVERIFYを維持する。

## 検証・独立性
原作PE32・IAT、原作機械語30アンカー、文字列定数8件、旧SQLiteと統合V9の4 CALL site（0x004BD4CF/0x004BD664/0x004BD775/0x004BD8D0）、リングカウンタxrefs、2バンク確保先、02H証拠、旧64件をそれぞれ照合。**65/65 PASS**（監査条件数。新規関数数ではない）。
旧DB・V9ともimmutable/read-onlyでSQLite quick_check=ok。全関数一括再解析/REA/Ghidra実行なし。
5証拠分類: info=INDEX_ONLY_V9 / pseudo=INDEX_ONLY_V9 / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY_V9 / callees=INDEX_ONLY_V9。REAの独立5種類証拠を新たに全完備した関数は0。新規正式VERIFIED=0、旧Wave1～5の64/64は保存済み同期記録を保持、正式TODO/VERIFY/BLOCKED書込差分0/0/0。原作ゲームGolden=0、strict MATCH/完全複製率は未測定。

## 安全・次の研究
active.lock無しを確認後に自担当rea_lab/decomp_taskの新規固有ファイルだけ作成。原本ZIP/EXE/SAVE、MASTER、QUEUE、PROGRESS、旧RUN、A～E、T018、Git、公開、スケジュールは変更しない。安全拒否既往対象は調査・再試行しない。
次は0x00556F00等のDAT_0068B370/0x0068B38C設定経路と、0x004BD2A0で先に作る検索バンクの実パス意味、個々の文字列長上限を絞る。DirectMusic関連の実行Goldenは未実測。