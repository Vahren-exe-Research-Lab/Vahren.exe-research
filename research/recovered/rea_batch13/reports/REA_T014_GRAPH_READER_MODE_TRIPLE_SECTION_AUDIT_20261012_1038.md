# REA T014 — Spot経路グラフreaderのmode分岐と3セクション（2026-10-12 10:38 JST）
- 状態: CONFIRMED-SAVED-STATIC（命令・疑似コードの局所分岐とcallsite）/ VERIFY（callee本文、動的到達、マーカーbytes、互換結果）。新規REA/Ghidra実行0、Ghidra新証拠0、関数VERIFIED増分0、旧EXE実機実行0。
- 正本: MASTER checkpoint83 DONE9/IN_PROGRESS21/VERIFY4、規約ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、最新runとsyncをread-only照合。承認コピーSHA256今回再計算MATCH=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 主関数 0x435550 / T014 / saved run 20261011T124000308Z: info `ev_8fc065296a08a2f672a520399680a38404d656f96ecd59f4747278ec964409a4`、pseudo `ev_7a9e58e9b0b538edf453aaf98e7755f5ebedda9102d81657c549716351eec905`、assembly `ev_775c749267e95e4682d3e76c638e9a612068de9345aedb4557eabd74e6eaafe2`、callees `ev_c4837ec9612a87de6e6c808ce950dde13e92ada453d6d4ac779eabc2d905b175`。body非連続4 ranges、1672bytes、完了run。
- 根本呼出元 0x45E1E0 / T014: assembly `ev_69ab9492fa443fe12c5fb3e0d6230b5c7bb67fcca9fbc5c2915973a18d18e124`、pseudo `ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e`。0x45E547 PUSH 1 → 0x45E54C CALL 0x435550で通常save rootはparam_2=1経路を呼ぶ。
## 既存保存証拠から今回追加した局所分岐の対応
- 0x435550は共通の先頭token/header一致検査後、param_2==0とparam_2!=0で後段を分岐。先頭headerの文字列値・失敗時例外は別途検証。
- mode 0（param_2==0）: Unit相当の対象オブジェクト+0x1EEBD0の既存treeをclearし、+0x1EEC70を0へ初期化する経路。3セクションごとに0x5B6C2Bで0x36C,0x240,0x240 byteのオブジェクトを確保（構築0x4319B0,0x431E00,SpotEscapePath vtable）し、virtual +0x5Cをmode 0で呼ぶ。各レコードを0x436680→0x463280へ接続して挿入。これを一般的な全save reset条件と断定しない。
- mode 1（param_2!=0）: 既存treeの上記clear/新規allocate経路ではなく、global側の0xB128B8,0xB12678,0xB12438にある3つの静的インスタンスを利用し、各サブreaderを最後の引数1でcallする。実際のcallee内部で他状態を更新しないことは未証明。
- section #1: sentinel長/文字列 `0x65C854/0x65C844`、0x435774 CALL `0x5A90E0`、this=0xB128B8、呼出回数はループ内でレコード数に依存。
- section #2: sentinel長/文字列 `0x65C870/0x65C860`、0x4357F0 CALL `0x5B0400`、this=0xB12678。
- section #3: sentinel長/文字列 `0x65C88C/0x65C87C`、0x435874 CALL `0x5B0400`、this=0xB12438。この同一calleeをsection #2と共有するがthisが異なる。markerの実バイト列と3構造の意味はVERIFY。
- 裏付け: `0x4705F0` callers `ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87`に0x5A90E0と0x5B0400が存在。保存済み全calleeファイルread-only走査でも両者の直接親は0x435550。両callee自身の5種類のREA証拠ファイルはruns内未発見。resolved referencesのみで間接caller網羅は不可。
## 実装への影響／次回
- 3区分のdelimiterと異なる読込器・thisを単一均一セクションとして潰さず、normal saveのmode=1とmode=0のclear/construct経路を分離する。mode0の実caller、mode1のオブジェクト寿命/更新副作用、各callee本文のない箇所はVERIFY継続。
- 共通token reader 0x4705F0のresolved caller13中、独立に用途分類確定は引続き8件。今回2件(0x5A90E0,0x5B0400)は親における用途「graph subreader」まで局所確認（独立callee仕様未確定）。未分類5件0x45EAC0/0x470550/0x58E480/0x5A90E0/0x5B0400を完了扱いしない。
- 最新sync progress_sync_20261011T153958076Z.json=Wave1 16/16,Wave2 10/10,Wave3 10/10,Wave4 12/12,Wave5 16/16、合計64/64 VERIFIED、P0=29/29、P1=35/35。Wave6未正式登録0/16、候補P0 5/P1 11、未着手16/関数VERIFY0。旧EXE実機golden PASS0、ゲーム再実装率は測定していない。
- EPERMによりQUEUE.json=STALE_RENAME_DENIED、PROGRESS=SKIPPED_QUEUE_STALE。既往失敗rename/sync/代替path更新を再試行しないためWave6 heavy decompileを開始せず。次回は保存済証拠のmode0 callerをread-only xrefsで調べ、必要なら正式キューの安全な復旧後に限り新規4件以内。
- Local preflight 2026-10-12 10:35:06 JST: CPU43%、RAM free15.28GiB、先行java/javaw/Ghidra/REAなし、active.lockなし、承認コピーSHA MATCH。重い解析0秒、read-only軽量調査開始~10:35／記録~10:38、REA6.1.0/Ghidra12.1.4・単一MCP・最大4件/Ghidra900000ms/request960000msの制限維持。
- 原本ZIP/EXE、A〜E、MASTER、T018、他研究、Git/push/公開、MCP/OS設定、既存スケジュールは無変更。0x5710C0..0x571500及び既往拒否済みREA抽出を別経路で迂回しない。
## 追加xref照合（同じread-only調査）
- 0x435550 procedure_callers evidence `ev_d1841901f69673cb231af84c3fcf0492745639a21fe18d79f05fdff8a3fc5dec`（runs/20261011T124000308Z）にはdirect callerが正確に `0x45E1E0` と `0x45EAC0` の2関数。前者のmode=1は前記PUSH 1で確定、**後者0x45EAC0がmode 0を渡すかは未確定**。
- 0x45EAC0は0x4705F0 caller setにも含まれ、normal-save rootとは別のtoken消費・graph読込上位関数の候補として優先する。ただし0x45EAC0自身の保存済み5-method本文証拠は未発見なので「関数の完全分類済み」へ昇格しない。


## 2026-10-13 04時台 — SpotPath/EscapePath reader 0x5B0400 のmode別終端／リンク条件（REA-T014-5B0400-MODE-20261013-0445）
- [STATUS / SCOPE] T014。既存owner `data/T014_GLOBAL_SAVE.md` §「SpotPath / SpotEscapePath shared payload」に6フィールド順・endpoint名と再解決は既記録。重複発見として再加算せず、今回は**未記載の欠損endpoint枝とリンク引数条件／具体的reader-mode分岐**のみ追加する。保存済みlocal native静的照合であり、REA/Ghidra新規解析0、新しいinfo/pseudo/assembly/callers/callees一式なし、関数0x5B0400を新VERIFIEDにしない。
- [PRIMARY] `exe/T014_SPOT_PATH_VFUNCS.txt` 282行以降の `0x5B0400..0x5B05F2`／直後別関数writer `0x5B0600`。対象保存nativeファイルSHA256 F95EF8CC0ECDFAE026F2B873C735C9B69F37689265F392CE1720110C6A77E23F（04:45 JST実測）。親Ghidra `0x435550` assembly ID `ev_775c749267e95e4682d3e76c638e9a612068de9345aedb4557eabd74e6eaafe2`、callee ID `ev_c4837ec9612a87de6e6c808ce950dde13e92ada453d6d4ac779eabc2d905b175`、`0x4705F0` callers ID `ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87`。5-methodの新規evidence IDではない。
- [ABI/BRANCH] `0x5B0437 CMP BYTE [EBP+0x10],0`、`0x5B0447 JE 0x5B04E7`。呼出の第三stack引数low byteが非0なら**一時領域への読込／discard系**、0なら**当該objectへ読み込む経路**。THIS=ECX→EBX、stream pointer=[EBP+8]→EDI。未知world/registry入力=[EBP+C]は実型VERIFY。RET 0xC。親mode=1 direct `0x4357F0/0x435874`は同関数を別this=0xB12678/0xB12438で呼ぶ。
- [NONZERO / DISCARD] `0x5B0468,0x5B0484,0x5B0491,0x5B049E` の`0x4705F0`計4回＋`0x5B0477 CALL 0x4707D0`計1回＋`0x5B04AB CALL 0x470700`計1回。取得先はESP上の一時領域（同領域を複数回再利用）で、**EBX+0x6C/+0x88/+0x1E8/+0x204/+0x220/+0x23Cへ直接storeは当該非0枝に無い**。文字列一時objectの条件付free `0x5B04B3..0x5B04C4`後、共通epilogue `0x5B04C7`。読取・stream cursor変化は発生するので「完全no-op」ではない。
- [ZERO / REAL PAYLOAD] `0x5B04E7..0x5B0538`でobject+0x6C string、+0x88 byte-reader、+0x1E8/+0x204/+0x220 string、+0x23C dword-readerに直接格納。writer `0x5B0600` は同順（owner既知）。追加で`0x5B055D`と`0x5B0577`の `0x49E490` により+1E8/+204から取り出した2名称の参照先pointerを取得。
- [MISSING ENDPOINT] `0x5B057E TEST EDI,EDI → JE 0x5B05D2`、`0x5B0582 TEST ESI,ESI → JE 0x5B05D2`。**どちらか一方でも解決結果が0なら、`0x5B05D2`の異常処理ブロック**（`0x5B6522`準備→`0x5B864E`呼出）へ向かい、通常`0x5AFB30`リンク処理を通らない。後続にINT3が並ぶ。calleeが具体的に何をthrow/表示するか・例外捕捉と復帰はVERIFYで、静的に「エラーhelper到達」だけを確定する。未解決endpointを黙って省く実装はnative一致と断定不可。
- [CONDITIONAL LINK FLAG] 両pointer非0の場合にも`0x5B0586 TEST EBX,EBX`の条件があり、非0では`0x5B0599 CALL 0x5E72E5`を実行。`0x5B05A1 TEST EAX`非0なら`0x5B05B3 CALL 0x5AFB30`へ**第3stack引数=1**、それ以外は`0x5B05C8 CALL 0x5AFB30`へ**第3stack引数=0**。同じ2解決pointerでもこのフラグを無条件1に固定しない。5E72E5の意味、flag1/0のゲーム内意味、5AFB30の全副作用はVERIFY。
- [PARENT MODE0 CORRECTION] 旧本メモ末尾「0x45EAC0がmode0を渡すか未確定」は保存済み `REA_T014_DUAL_MODE_CALLSITE_CONFIRMED_20261012_1142.md` のnative `0x45EF25 PUSH 0 →0x45EF34 CALL 0x435550`で**callsiteの渡す値0は確認済み**。ただしGhidra側caller関数境界 `0x45EAC0`の実入口/所属は依然VERIFY。従来文言を局所訂正するだけでGhidra caller 13を別高水準関数13件と断定しない。
- [REIMPLEMENT/GATE] 0x5B0400のmode非0ではstream cursorは進むがobject field set／graph rebindを行わない局所枝。mode0ではフィールド復元→2 endpointの照合→エラーまたは条件付きlink flag。再構築型ロード時にmodeを混ぜず、5E72E5/5AFB30/5B864Eが未実装なら各calleeの直前で正常復帰を偽造せずVERIFY。Task T014 ownerへの読み取り連携対象、owner原本へ代行書込しない。
- [TEST DESIGN ONLY] 合成case: mode非0のstream消費（4string+byte+DWORD）とobject不変、mode0の6 field書込、片方のendpointだけ欠損→5B05D2、両方存在かつpredicate false/true→5AFB30 flag0/1、callee未帰還時のresume。全件DESIGNED/NOT RUN、原作実機golden0。
- [PROGRESS/SAFETY] MASTER checkpoint94・34Task DONE9/IN_PROGRESS21/VERIFY4。既存Wave1..5=64/64 STATIC VERIFIED（P0 29/29、P1 35/35）、新VERIFIED+0、Wave6候補0/16（P0 5/P1 11、TODO16／取得済み関数VERIFY0）。QUEUE/PROGRESSはrename EPERM旧表示のまま。対象copy SHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` 04:40 JST再確認。重い解析・新Ghidra/REA起動0。REA6.4.0/Ghidra12.1.4、単一MCP・上限4関数/回・900000/960000ms維持。原本EXE/ZIP、A-E/MASTER/T018、dev_lab/Work、Git、MCP/設定・既存schedule変更0。既往拒否済み0x5710C0..0x571500やexporterは再試行しない。
