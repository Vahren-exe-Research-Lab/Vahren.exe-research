# REA-LOCAL-20261024-04H-P0-F720-OWNER-PROVENANCE-STATIC-01
日時: 2026-10-24 04時台 JST / owner=REA / 優先P0 / PC-SAVED-PENDING-READBACK / STATIC / VERIFY / NOT READY
## 事前確認・根拠正本
- Desktop Commander Local Compact接続成功。MASTER_LEDGER / ANALYSIS_LANES_PROTOCOL / decomp_task README, QUEUE, PROGRESS、03H/02H既存研究とsearch_index README/BUILD_MANIFESTを先読。既存成果を破棄・再計上しない。
- 旧run最新同期 `logs/progress_sync_20261011T153958076Z.json`: Wave1-5の64/64 VERIFIED、21 runs。QUEUE/PROGRESSはrename EPERMで古い表示。両正本の上書き・修復・sync再実行なし。
- コピー `rea_lab/targets/hakushin067_Vahren.exe` は読取専用SHA256実測 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- search_index/search.sqlite SHA256実測 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF = manifest一致。Ghidra内部10268関数、build自動テスト34/34は既存実績（今回再実行していない）。
## 新規P0-01：0x008B8E4Cの呼出時所有者を追跡
- 保存済みGhidra検索 `search DAT_008b8e4c` で、0x0040D0A0が書込、0x0040F320が参照と判明。0x0040D0A0のdata_refsでWRITE site 0x40D0B4を確認。検索索引に見つからない別の間接書込・aliasを「存在しない」と断定しない。
- 原作native 0x40D0AE: `[0x8B8E48]=EDI`（stack引数由来）。0x40D0B4: `[0x8B8E4C]=EAX`。0x40D0B9: `[0x8B8E50]=ECX`。0x40D0BF: `[0x8B8E54]=0`。0x40D0C6: `CALL 0x40F320`。**3つのポインタ保存とフラグ初期化が0x40F320より前**という局所順序を原作バイトで確定。
- 上位5直接CALL: 0x491FFB/0x49204F/0x492143/0x4921F7/0x492473 → 0x40D0A0。全5箇所で `ECX=EBP+0x1EED30`, `EAX=EBP+0x1EED20`, `PUSH [EBP+0x1EED1C]`。DLは上記順で 1/0/0/0/1。ここでのEBPは呼出関数がstackから取得したcontext pointer。
- 結果、0x40F320から読む `[0x8B8E4C]` は上位contextの `+0x1EED20` コンテナへの **ポインタ**。ローカル実行経路では偶然の未初期化値ではなく、0x40D0A0により事前設定される。

## 新規P0-02：入力コンテナ・比較コンテキストを区別
- 0x40F38D `EAX=[0x8B8E4C]`; 0x40F392 `PUSH ESI`; 0x40F393 `CALL 0x48F720`; 0x40F398 `CALL 0x583C70`。間に戻り値NULLガードなし（03H既知、再計上しない）。
- 0x48F723 `EAX=[EAX+4]`→0x48F726 `ECX=[EAX]`→0x48F734 `CMP ECX,EAX`→0x48F736 `JE 0x48F7E1`。先頭=ヘッダ（空のセンチネル）のとき 0x48F7E4 `EAX=0`→0x48F7EA `RET 4`。
- 0x40F367..0x40F370では別に `ESI = [[0x8B8D28]+4] + 0x504` を生成。0x48F72Aがstack引数として EBP=ESI を取得し、0x48F73Cが `EDI=[EBP+0x1EED34]` を読む。**候補listの所有元（上位call context）と、照合木の読出元（ESI派生context）を同一物と断定しない**。
- 0x49AF10の独立nativeを追加照合: 0x49AF3B `XOR EDI,EDI`; 0x49B055/0x49B05E/0x49B066 が `[+0x1EED24]` にあるヘッダの+4/0/+8へヘッダ自身を保存; 0x49B069 `[EBP+0x1EED28]=EDI=0`。このlistには**空となる初期化/クリア経路がある**。ただし同一時点の0x40F393到達を意味しない。
## NULL契約の更新・制限
- [STATIC] 以前は不明だった `0x8B8E4C` の書込元と5callerの入力生成を確定。0x48F720が空listでNULLを返す分岐も原作バイト上で接続。
- [VERIFY] 0x49AF10のlist reset以後に追加されるノード、比較木、0x40D0A0を呼ぶ5モードの前提条件は未解明。**正常な戦闘初期化でNULLになること、クラッシュすることは未証明**。0x40F000/0x48ABF0その他の間接副作用を含む到達性検査を残す。
- [VERIFY] 呼出元EBPと比較用ESIのオブジェクト同一性、各コンテナの所有・破棄、完全なフックABIは未検証。
## 独立検査・研究境界
- 再現可能なread-only監査: `REA_20261024_0437_P0_F720_OWNER_BYTE_AUDIT.py`。pefile+Capstoneで元EXEを逆アセンブル。指定22機械語列をbyte exact照合22/22、8 E8相対CALL先8/8、コピーEXE SHA PASS、検索DB SHA PASS。検査スクリプトSHA256 F72B87051A6C75430FF453EE3418E345B67426E4CD5BD3065CD4372C5F4B831A。
- Ghidra既存indexで function 0x40D0A0(info/pseudo/callers/callees) / function 0x40F320 / 0x48F720 / 0x49AF10 を照会。ASMは原作の選択領域のみ独立照合。新しいREA info/pseudo/assembly/callers/callees五種一式完備は0関数、新VERIFIED=0、正式TODO/VERIFY/BLOCKED差分=0/0/0。
- 原作ゲーム/Golden実測=0、strict MATCH=0、完全複製率未測定。新Ghidra/REA実行=0。Work/Remote/Git変更=0。CPU/総作業時間は未測定。接続時active.lockなし、Java/Ghidra検出なし、空きRAM13.09GiB。
- 読取専用Python `-c` の一回目はWindows引数引用とパス文字化けでSyntaxError。禁止操作/安全拒否ではない。以降はREA所有に監査スクリプトを新規保存して実行・byte検証成功。元コピー・共有正本・既存成果は不変。
## 次のP0・Golden計画
- `0x0049AF10`以後の `+0x1EED24` ノード挿入・削除と `+0x1EED28` 件数、および `0x00491870/0x004922A0` の各戦闘開始ガードを追跡。次点は `0x0040F000/0x0048ABF0` の前処理副作用。Goldenは正常ケース/候補0件想定ケースを保存・無改造原作で比較設計、NOT RUN。
- 原本ZIP/EXE/SAVE、他lane、MASTER、QUEUE/PROGRESS、既存run、検索DB、Git、ユーザビリティ、既存スケジュールを変更しない。正式統合はE担当。
