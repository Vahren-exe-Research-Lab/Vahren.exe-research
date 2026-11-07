# 迫真戦記 REA｜2026-10-29 06H Ogg初期化失敗の経路とread callback到達性
研究ID: `REA-LOCAL-20261029-06H-P0-OGG-INIT-CALLBACK-STATIC-01`。状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。正式新規REA VERIFIED=0、原作Golden実測0。

## 開始時・既存成果との照合
- Desktop Commander Local接続正常。MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、共通ルール、REA README/QUEUE/PROGRESS、保存済RUN・旧sync、2026-10-21検索DB README/BUILD_MANIFEST、直近05H EVIDENCE/STATIC/READBACKを先読。
- `logs/progress_sync_20261011T153958076Z.json` のWave1〜5合計は **64/64 STATIC VERIFIED**。QUEUE/PROGRESSの旧数値と一部TODO表示はrename EPERMによるstale。正式件数を上書き・二重計上しない。
- 05Hで既報の `0x005CF970` state3->4失敗時-137、`0x005D0FB0` の間接CALL `0x005D1076`を未解決P0として引き継ぎ。今回は**初期化失敗を作る具体的な分岐**と**通常OggDecoder fill経由でのcallback非到達性**を補強する。既知の-137を独立不具合として増算しない。
- 隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。両SHA一致、SQLite quick_check=ok、開始時active.lock無し、Java/Ghidra先行プロセス無し、空きRAM約16.74GiB。

## P0-A｜0x005D57C0 → 0x005D5BD0 → 0x005CF970
- 入力準備関数 `0x005D57C0` は `0x005D57CA MOV ESI,[EAX+0x1C]`、`0x005D57CD TEST ESI,ESI`。NULL時に `0x005D57D1 LEA EAX,[ESI+1]` から **1** を返す。Ghidra生成擬似Cの `if (piVar1==NULL) return 1` と一致。
- caller `0x005D5BD0` の `0x005D5BDA PUSH 0` / `0x005D5BDE CALL 0x005D57C0` から、今回の実行経路では引数3が0であり初期化の該当側へ入る。
- `0x005D5B40 MOV EAX,[EBX]` / `0x005D5B42 TEST EAX,EAX` / `0x005D5B44 JE 0x005D5B89` により、各ブロックの入力ポインタがNULLなら失敗整理へ移る。非NULLでも `0x005D5B51 CALL 0x005DA070` の戻りが非0なら `0x005D5B59 TEST` / `0x005D5B5B JNE 0x005D5B89` で同じ整理へ進む。
- 整理側は非NULLの各ブロックを `0x005D5B9D CALL 0x005D9E70` で解放・入力スロットを0化し、`0x005D5BB8 CALL 0x005D4AE0`、`0x005D5BC2 OR EAX,-1` と `0x005D5BC9 RET` で **-1** を返す。正常完走経路では0。ここでのNULL・helper失敗は独立した条件であり頻度は未実測。
- 上位 `0x005D5BD0` は `0x005D5BDE` 後のEAX非0を `0x005D5BE7 TEST` / `0x005D5BE9 JE` で判別し、失敗時は `0x005D5BF3 MOV EAX,1` として返す。さらに `0x005CF970` が `0x005CF9A1 CALL 0x005D5BD0` の非0を `0x005CF9AD MOV EAX,0xFFFFFF77` = **-137** に変換する。05Hのstate3->4失敗条件を下位ABIへ紐付けた。

## P0-B｜0x005D1076間接CALLはこの通常read wrapper経由では通らない
- `0x005D0FB0` の `0x005D1065 MOV EAX,[EBP+0x24]` は第8引数の関数ポインタ、`0x005D1068 TEST EAX,EAX` / `0x005D106A JE 0x005D107B` はNULLならcallを飛ばす。非NULL時の `0x005D1072..1075` は4引数をpush、`0x005D1076 CALL EAX` / `0x005D1078 ADD ESP,0x10` はcaller cleanupのcdecl相当。read後のoptional callback（PCM変換直前）の可能性が高いが、正式関数名・全callersは未確定。
- 通常fill `0x00501F10` が呼ぶ `0x005D12E0` wrapperは `0x005D12EC PUSH 0`、`0x005D12EE PUSH 0` を先に積んで `0x005D1303 CALL 0x005D0FB0`。9引数のうち最終2引数（callbackとuserdata）がNULLとなるので、**このwrapper経由の読込では0x005D1076へ分岐しない**。
- ただし、`0x005D0FB0` の別callerや引数付きAPIがcallbackを渡す可能性、およびcallback先関数の具体的ABI/作用は未確認。検索DBのcomputed siteに固定targetを捏造しない。

## 証拠の範囲と次の研究
- 出典: 10/21検索DB `search.py function` 0x005D57C0/0x005D0FB0/0x005DA070、`callers/callees` 0x005D57C0、関数・直接CALLのSQLite read-only照合、および隔離PE32から対象命令だけCapstoneで復号。
- 独立監査 `REA_20261029_06H_P0_OGG_INIT_CALLBACK_AUDIT.py` は **48/48 PASS、0.444秒、failed=[]**。これは静的assert数であり48関数の逆コンパイル成功ではない。
- info=検索索引、pseudo=保存Ghidra機械出力、assembly=隔離PE対象命令、callers/callees=検索索引＋native CALL site。**今回新しいREA正式5種取得は無し、正式VERIFIED=0追加、既存64/64、正式TODO/VERIFY/BLOCKED差分0/0/0**。本研究の追加確認はVERIFYのまま。
- Golden設計（未実行）: source header NULL、各ブロック入力ポインタNULL、`0x005DA070` 非0/0、正常0の4系列で `0x005D57C0` 戻り1/-1/0と上位-137/状態4遷移を原作と比較。callback NULL/非NULLの両API経路を別試験にする。原作Golden実測PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。
- PCオンライン。対象runでは新規Ghidra/REA・原作ゲーム・Workを実行せず、監査のみ。監査実行0.444秒、研究全体の所要時間とCPU負荷は不明。原本ZIP/EXE/SAVE、他owner、MASTER/T018/dev_lab、既存RUN、QUEUE/PROGRESS、検索DB、Git、公開先、スケジュール変更なし。10/28のLibrary未同期成果は未統合で保全。
- **次のP0:** `0x005DA070` の非0戻り源（内部メモリ確保・コードブック木構築失敗等）をtarget nativeで限定し、`0x005D0FB0` の他callerからcallback `0x005D1076` へ到達する経路を安全に列挙する。生成擬似Cだけで追加関数を正式VERIFIEDにしない。
