# REA-LOCAL-20261023-1638-P0-FASTSIM-500TICK-RESULT-STATIC-01
日時: 2026-10-23 16時台 JST / owner=REA / 状態=PC-SAVED-PENDING-READBACK, STATIC, VERIFY, NOT READY。未統合。関連Task: T010/T012（戦闘時間・結果）、T015（表示）。**T014はSAVE担当であり、本件をT014成果に計上しない**。
## 出典と非重複
- 原作の承認済み専用コピー `rea_lab/targets/hakushin067_Vahren.exe` SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回実測）。
- 今回の検索正本は統合V9 `HAKUSHIN067_UNIFIED_V9_20261023.sqlite`。SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。V9 verify=V9_INDEPENDENT_READBACK_PASS。V9は統合SQLiteでありPC標準CLIのV3を変更していない。
- V9で 0x0040E220 / 0x0040E2F0 / 0x00514C80 を検索、callers 0x0040E2F0 は 0x0040E27F E8_DIRECT_CALL 1件。0x0040E220 のE8/E9フローcallerは0件（間接ポインタ経由の呼出し不在を意味しない）。
- 先行REA_20261023_1537_P0_BTL_TIMER_MODE_SPLIT_STATIC.mdで確定済みなのは `0x40E3AE PUSH 1 → 0x40E3B0 CALL 0x492D80` と上限500候補。本件の**新規差分**は二陣営の生命判定の独立EAX、return 0/1/2と上位callerの接続、500上限の正確な境界。
## 重大な静的発見：0x0040E2F0は最大500 tickの限定反復
- 0x0040E220の実ASM: 0x40E22C MOV EAX,0x80000008、0x40E231/0x40E23A で [EDI+0x78/+0x7C]を比較し、0x40E243で[EDI+0x19C]を検査。成立したときのみ0x40E27D EAX←(EDI-0x28)、0x40E27F E8 CALL 0x40E2F0。
- 0x40E2F0は入口EAXをEDIに保存（0x40E2F7 MOV EDI,EAX）。通常のスタック引数だけで完結する関数としてフックしない。V9 ABI=未認定。
- loopの0x40E3AE PUSH 1 / 0x40E3B0 CALL 0x492D80 / 0x40E3B5 TEST AL / 0x40E3B7 JNE 0x40E622：時間更新が非0ならシミュレーションはreturn 0。
- 0x40E3BD–0x40E3D3でmagic 0x51EB851Fによる除算近似と IMUL 0x32、余り==0時に以下の陣営生存判定。初回iteration=0、その後50,100,…,450で判定する経路。
- 0x40E608でiterationをロード、0x40E60Cで[EDI+0x288]をDEC、0x40E612でiteration+1、0x40E617 CMP EAX,0x1F4（500）、0x40E61C JL loop。500回実行完了なら0x40E622 XOR EAX,EAXでreturn 0。**500はtick数の上限であってミリ秒・実フレーム時間ではない**。
## 二陣営判定：見た目が重複した関数は別オブジェクトを検査
- 0x40E3D5 MOV EAX,[EDI+0x1CC] → 0x40E3DB CALL 0x514C80。AL!=0かつ[EDI+0x28C]<=0なら0x40E62Cへ進みreturn **2**。
- 0x40E3F0 MOV EAX,[EDI+0x1C8] → 0x40E3F6 CALL 0x514C80。AL!=0かつ[EDI+0x28C]<=0なら0x40E65Fへ進みreturn **1**。
- 0x514C80はEAXから [+0x48,+0x4C] のポインタ配列を取り出し、各要素の +0x18613、+0xB0、+0xA8、+0x1E530、+0x228、+0x1867C を検査。条件を満たすユニットが一件でもあればreturn AL=0 (0x514CE2)、いなければAL=1 (0x514CDD)。ここは静的条件の再構成であり「死亡」の全ケースを保証しない。
- **同じ0x514C80を2回呼ぶ理由は入力EAXが+0x1CC側と+0x1C8側で違うから**。Ghidra疑似Cの`FUN_00514c80()`を引数なしと見なして重複排除するのは誤り。
## カウンタ満了時の追加間接CALL（P0 / VERIFY）
- 0x40E40C CMP [EDI+0x288],0。<=0なら0x40E639で[EAX vptr+0x18]を間接CALL（0x40E644 FF D2）し、その戻り値が4でなければreturn **2**。
- 最初のslot+0x18が4なら、[EDI+0x1CC]の別オブジェクトのvptr+0x18を0x40E658 FF D2でCALL。戻り値!=4ならreturn **1**、4ならreturn **2**（静的分岐順序）。
- vptr実体・slot+0x18の実装先と戻り値4の意味は未確定。この2箇所を「勝敗が完全確定」としない。CALLはFF D2、E8直接CALLではない。
## 上位へ返される契約（静的のみ）
- 0x40E27Fの戻り値が0の場合、0x40E28E E8 CALL 0x0040D220（スタックには1がpush済み）。この経路は0x493630へ入らない。
- 戻り値1または2の場合は0x40E2A0のvirtual slot+0x10を実行後、0x40E2A2 CMP EBP,1→SETE→MOVZX EDX,CL→PUSH EDX（0/1）し、0x40E2B9 E8 CALL 0x00493630。次に0x40E2BE CALL 0x0040F000→0x40E2C3 CALL 0x0048ABF0、条件付きで0x40E2D2 CALL 0x0048EEE0へ進む。
- 0x00493630への最終boolは`sim_return == 1`。ただし、値1/2と攻撃側/防御側・勝利/敗北の対応は今回の静的証拠だけでは未確定。
- 0x0040F000のGhidra疑似C上で+0x288/+0x28Cを0に戻す経路があり、勝敗通知前後の状態保存・後処理順序を動的Goldenで検証する必要がある。
- **0x0040E220は直接E8 caller 0、flow-callers(E8/E9/EB)も0。呼出元が存在しない証拠ではなく、UI vtable/関数ポインタ等の登録元を次に追跡する。**
## 独立検証と正式進捗
- 実バイトPE32からpefileで RVA→file offsetを変換し、Capstone x86で0x40E220、0x40E2F0、0x514C80の要所を独立ASM。Python一時コマンドは`-B -c`でread-only実行しファイルを作成しない。
- 指定命令バイト21/21 PASS、E8 rel32ターゲット6/6 PASS（0x40E27F→0x40E2F0、0x40E3B0→0x492D80、0x40E3DBと0x40E3F6→0x514C80、0x40E2B9→0x493630、0x40E28E→0x40D220）。V9検索の0x40E2F0 caller 1件と整合。
- V9独立readback: `V9_INDEPENDENT_READBACK_PASS`、functions=11950、E8+JMP native索引=51214、unowned_e8=0。標準V3は変更していない。V9の疑似Cは元2026-10-20版（関数ABI未認証）、raw ASMを優先。
- 既存 Wave1～5 VERIFIED=64/64 は `logs/progress_sync_20261011T153958076Z.json`の既存保存値（queueUpdate=STALE_RENAME_DENIED）、今回の新規正式REA VERIFIED=0、正式5種類info/pseudo/assembly/callers/calleesが新規揃った関数=0。正式TODO/VERIFY/BLOCKED書込差分=0/0/0。
- 原作ゲームGolden実測PASS=0、strict MATCH=0、完全複製率=未測定。新規REA/Ghidra起動=0。PC確認時CPU load=21%、空きRAM約17.83GiB、java/ghidraプロセス0、active.lockなし。調査全体所要時間は未計測。
- RAW成果の扱い: 今回は非重複の呼出経路と分岐条件の追加解析だけを認定。原本、MASTER、A～E、QUEUE/PROGRESS、過去RUN、Git、スケジュールは変更しない。13時台に安全拒否された別Python検証器作成は再試行していない。
## Golden条件設計（すべてNOT RUN）
- 同じ入力で最大500 tick到達→return0→0x40D220側（途中の時間終了・勝敗・副作用がない条件を用意）。
- 50 tickごとの+0x1CC側AL=1と+0x28C<=0→return2、同様に+0x1C8側AL=1→return1、両方AL=1なら検査順の優先度を検証。
- +0x28C>0で判定ゲートが抑止される場合と、+0x288<=0でvptr+0x18の戻り値4/非4を比較。
- 上位0返却時と1/2返却時の+0x288/+0x28C状態、0x493630第4引数bool、0x40F000後の清掃と戦略マップ側の勝敗反映をGolden比較。
## 次回再開位置
P0: 0x0040E220の登録元・間接caller、0x40E644/0x40E658の動的vptr先を静的初期化経路から追う。0x00493630の第4引数boolと戦闘終了の結果code 0/1/2の実意味をA/Eと照合。read-onlyで続行。REA正式出力/未確認ABIは増やさない。

## PC保存・独立readback確認
- 本レポート全42行を別のread_file操作で読み戻し、研究ID・元EXE SHA・V9 SHA・新規差分・検証件数・次P0を確認。最終状態は **PC-SAVED / READBACK VERIFIED / STATIC / VERIFY / NOT READY**。既存ファイルに追記・上書きせず本件固有名で新規作成。
