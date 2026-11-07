# REA-LOCAL-20261024-02H-P0-F720-MAP-FILTER-ABI-STATIC-01
日時: 2026-10-24 02時台 JST / owner=独立REA / P0 / STATIC・VERIFY・NOT READY / 新規成果（当初PC-SAVED-PENDING-READBACK）
## 正本・重複照合
- 承認済み対象コピー: rea_lab/targets/hakushin067_Vahren.exe。今回実バイトSHA256 = E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 統合V9: HAKUSHIN067_UNIFIED_V9_20261023.sqlite。verify=V9_INDEPENDENT_READBACK_PASS / SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
- 先行REA_20261024_0137_P0_DEMO_VSLOT0C_SOURCE_TAIL_STATIC.mdほか0～1時台の保存成果、README/QUEUE/PROGRESS/旧RUN/MASTER/所有規約を参照。先行のDemoPerson初期化ABI、0x583C70→0x597B00 tail JMP、Wave1～5の64/64は再計上しない。
## 新規P0：0x0048F720（第2ソース選定元）の実ABIと探索ロジック
- V9ではfunction 0x0048F720: 223 bytes、body 0x0048F720～0x0048F7FE、疑似CはORIGINAL_20261020_GHIDRA_PSEUDOC_UNCORRECTED、verified_abi=0、outgoing E8 CALL 0。Capstone独立逆ASMでは84命令、最後の0x0048F7FCはRET 4。
- native入力はEAXに検索対象コンテナへのポインタ、スタック第1引数（0x48F72A: MOV EBP,[ESP+0x14]）に所有コンテキストへのポインタ。0x48F720 SUB ESP,8とEBX/EBP保存後のオフセットを考慮。暗黙EAXを無視した通常Cプロトタイプは不可。
- 0x48F723 MOV EAX,[EAX+4]→0x48F726 MOV ECX,[EAX]で入力側ノード列の先頭を取得。ECXとヘッダEAXが等しければ0戻り経路。列を進めながらノードキー[ECX+0x0C]を使用。
- 0x48F73C MOV EDI,[EBP+0x1EED34]から比較先木ヘッダを取得。0x48F74F/0x48F752/0x48F757/0x48F75Cによって、キーとのunsigned順序を使い比較先木を辿る（lower_bound型）。キーが既登録なら候補を採択しない。
- 0x48F786 CMP [EAX],EDIで「木で一致キーが見つからない」側を確認し、0x48F78A CMP [ECX+0x18],0が非ゼロなら0x48F7EDへ。リストから『比較先木に未登録かつ+0x18非ゼロ』の最初の候補を選ぶロジックに整合。木キーや候補フラグのゲーム上の意味は未確定。
- 成功return: 0x48F7ED ECX=[ECX+0x14]、0x48F7F0 EDX=[ECX]、0x48F7F2 EAX=[EDX+0x0C]。途中に**2回の間接参照**があり、[node+0x14]+0x0Cを直接返すという短絡は誤り。
- 候補なし: 0x48F7E4 XOR EAX,EAX →0x48F7EA RET 4。成功側0x48F7FCもRET 4。stack引数は4byte callee cleanup、結果はEAX。register保存とcaller実体を静的根拠とし、完全フックABI認定はしない。
## 新規P0：簡略戦闘CALL siteとNULL前提条件
- V9 callers 0x48F720=PE検証済E8直接CALL 7箇所、今回すべてを元EXEのrel32で独立確認。対象siteは 0x40F393 / 0x434EF3 / 0x48FBD9 / 0x4901C1 / 0x4905F2 / 0x49381E / 0x4F66ED。
- 0x40F370 ESI=[ [0x8B8D28]+4 ]+0x504、0x40F38D EAX=[0x8B8E4C]、0x40F392 PUSH ESI、0x40F393 CALL 0x48F720。このEAX戻り値を0x40F398 CALL 0x583C70へ直接渡し、0x40F3A3で戻り値を[0x8B8E64]へ保存。第1側0x40F383→0x597B00と選択経路が異なる。
- 0x583C74 MOV EDI,EAX直後、0x583C76 CMP [EDI+0x94],0にNULLガードなし。0x48F720にはEAX=0の正常returnがあるため、この呼出経路には候補存在の前提条件が必要（または異常入力でNULL参照の可能性）。**原作バグ・通常クラッシュと断定しない**。実際のソース入力リスト・木内容・0x48F720の0戻り到達可否を同runで検証する。
- 呼出側0x40F393直後にスタックADD ESP,4はなく、callee RET 4と一致。V9疑似Cの巨大インデックス param_1[0x7bb4d] はnativeの[EBP+0x1EED34]と同値。Cの見かけの引数だけからABIを決めない。
## 独立検証と限界
- PE32 RVA→rawをpefileで独立変換、Capstone x86で0x48F720 223byteを84命令として解析。指定27箇所の命令生バイト27/27一致、CALL site E8 rel32=7/7一致、RET 4二経路、内部直接E8 0、原EXE SHA PASS。
- V9関数情報・callers/callees検索を使用。REA正式info/pseudo/assembly/callers/callees五種を新たに取得した関数0、VERIFIED+0、TODO/VERIFY/BLOCKED正式変更0/0/0。Wave1～5既存同期64/64、Golden PASS0、strict MATCH0、完全複製率未測定。
- preflight active.lock=False、Java/Ghidra検出なし、空き物理RAM13.23GiB。CPU負荷不明、総作業時間未計測。REA6.1/6.4差、拒否Wave6、旧QUEUE/PROGRESS EPERMが残り、新REA/Ghidra runを起動しない。
- 通常の読み取り専用検査においてPowerShell here-string終端1件、Python一時検証コードの文字列引用2件の構文エラーが発生。修正して別途検証完了（安全拒否ではなく、実行可能成果の保存失敗ではない）。禁止操作は再試行していない。
## 次P0（DESIGNED・NOT RUN）
- 0x40F393から到達する0x48F720の入力木/列の生成元、特に[EBP+0x1EED34]とノード+0x18/+0x14の所有者を追跡。候補なしEAX=0と0x583C70の前提条件を同一戦闘runの原作証拠で検証する。
- 0x0040F320における第1 0x597B00と第2 0x48F720→0x583C70の初期化順序、および0x4103D5/0x4103E2の動的型を別受入証拠で確定。Golden未実行。
- 原本ZIP/EXE/SAVE、他レーン、MASTER/T018、旧REA RUN/QUEUE/PROGRESS、Work/Git/スケジュール、V9 DB/標準V3は変更しない。本人所有の新規固有ID成果のみ書込み。
