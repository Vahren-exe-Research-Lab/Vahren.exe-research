# 迫真戦記 REA｜2026-10-30 04H：DirectSound Lock/Unlock二領域ABI・実書込側の独立照合
研究ID：`REA-LOCAL-20261030-04H-P0-DSLOCK-PAIR-FIRSTREGION-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。原作実機Golden PASS0、新規正式REA VERIFIED0。
## 事前・出典
原本と別の研究用コピー `rea_lab/targets/hakushin067_Vahren.exe` のSHA256は `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
統合V9 `headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` のSHA256は `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
MASTER・レーン規約・REA README/QUEUE/旧PROGRESS・syncログ・03H既存証拠・V9現行案内を読み、正式64/64維持と旧QUEUE/PROGRESSのEPERM陳腐化を確認。03H 53/53、IID5/5、独立readback14/14を照合。
0x00502330 V9疑似CはABI未検証で原典ソースではない。局所原作SHAのCapstone機械語で再照合。関数本体0x00502330..0x005023D7。直接CALL site: 0x005022E9（0x00502220）・0x004BF31C（0x004BF2B0）。
## 新規P0証拠：Lock第1/第2領域のstack localマッピング
`S` を `SUB ESP,0x10; PUSH ESI; PUSH EDI` 完了時のESPと定義。
`0x0050235B..0x00502387` のpushとLEA（pushによるESP変位を考慮）よりLock引数は `(stream+8, offset=0, bytes=0, &ptr1[S+0x0C], &bytes1[S+0x08], &ptr2[S+0x14], &bytes2[S+0x10], flags=2)`。
`0x00502370/74/78/7C` は4つの出力localを呼出前に0初期化。COM vtable+0x2C Lockは0x00502387、`TEST EAX,EAX; JS 0x005023C9` のため負のHRESULTでは後片付けへ進む。
## 新規P0証拠：デコーダは第1領域にのみ書込み、Unlockは二領域ペアを渡す
`0x0050238D MOV EAX,[ESP+8]` はbytes1、`0x0050239B MOV EAX,[ESP+0x18]` はpush3個後のptr1参照。0x005023A0でdecoder vtable+0x04を `(ptr1,bytes1,0,0)` で間接CALLする。
`0x005023A2 MOV ECX,[ESP+0x10]` はbytes2、`0x005023A6 MOV EDX,[ESP+0x14]` はptr2。`0x005023B2..0x005023BF` は引数を `Unlock(stream+8,ptr1,bytes1,ptr2,bytes2)` と順序どおり再構築し、COM vtable+0x4Cを呼ぶ。
**第2領域はデコーダの引数にならない。** ただしLockはoffset=0、flags=DSBLOCK_ENTIREBUFFER(2)なので、通常のAPI仕様に従えば第1領域が全体を含み、第2領域はNULL/0となる。二領域時の未充填は条件付きVERIFYであり、直ちに不具合とは判定しない。
Unlock戻り値の検査はなく、0x005023C2でAL=1となる。デコーダ戻り値も0x005023A2で上書きされる。戻り値未検査は以前の研究済みで、**今回は具体的な4引数の対応と領域の利用範囲の照合だけ**を新規差分とする。
参考：Microsoft IDirectSoundBuffer8 Lock https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee418073(v=vs.85) / Unlock https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee418153(v=vs.85)
## 検証・安全・未検証
独立機械語・保存済みV9索引・先行証拠の監査は `REA_20261030_04H_P0_DSLOCK_ARGS_AUDIT.py` **65/65 PASS**（0.9037秒）。`REA_20261030_04H_P0_DSLOCK_ARGS_EVIDENCE.json` へ全命令、stackマッピング、結果を新規保存。新REA/Ghidra実行0。原作ゲーム起動0。
REA 5種は info=V9、pseudo=V9、assembly=局所Capstone、callers=V9、callees=V9 の既存索引＋追加局所照合であり、正式REA info/pseudo/assembly/callers/calleesの新規5種完備0件・正式VERIFIED追加0。既存64/64を維持、正式TODO/VERIFY/BLOCKED差分0/0/0。Golden実測0、完全複製率未測定。
PCは接続正常、active.lock無し、Java/Ghidra実行競合無し、確認時空きRAM約12.1GiB。CPU負荷・研究全体時間不明。原本/MASTER/QUEUE/PROGRESS/既存runs/A～E/Git/公開/スケジュール無変更、未同期オフライン成果は未統合。
**次の関数:** `0x005023E0`（workerのPCM Lock・二領域・再生位置更新）、`0x00502580`（EOF側）。先にowner/最新差分を確認し、Lock返却領域の処理、Unlockへ実書込バイト数が一致するかを追う。動的GoldenはDESIGNED / NOT RUN。
