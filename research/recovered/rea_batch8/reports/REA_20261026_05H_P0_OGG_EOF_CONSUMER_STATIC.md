# REA P0｜OGG EOF ラッチの読取側・曲送り境界（2026-10-26 05時台）
研究ID: REA-LOCAL-20261026-0535-P0-OGG-EOF-LATCH-CONSUMER-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY。実機Golden 0、新規REA正式VERIFIED 0。
Source EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
Ghidra検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 今回の新規事実（04時台のworker書込調査と区別）
1. 05時台の限定Capstone xref probeで +0x58/+0x54 を読むstream自身の関数0x00502580（105 bytes）を特定。callers: 0x004BF780（CALL site 0x004BF7C8）1件。そのcaller: 0x004BE220（0x004BE29D）1件。そのcaller: 0x004C24B0（0x004C26CF）。
2. Ghidra検索CLI function/callers/relatedで上の辺を確認。原作同SHAの機械語を別手法Capstoneで照合。検索DB疑似Cは機械出力でありREA5種証拠ではない。
3. 0x00502580: [ESI+0x58]==0 はAL=0。==2 はvtable+0x10 (CALL site 0x005025AA)でカーソル取得し、HRESULT>=0 かつplayCursor < (size+0x28)/2 なら 0x005025B6 で+0x58=1へ移行。この呼出しではAL=0のまま。
4. +0x58が非0かつ2以外の場合、vtable+0x10 (CALL site 0x005025D4)でカーソル取得し、HRESULT>=0 かつunsigned playCursor >= [ESI+0x54] なら 0x005025E3 でAL=1。それ以外はAL=0。
5. 0x005025B0はcmp dword ptr [esp + 4],edi。GhidraのpuVar4変数は誤ったポインタ意味付けで、実際は出力された再生位置DWORDとHの比較。0x005025DEも実DWORD値比較。
6. 0x004BF780: manager+8==0・manager+9!=0のOGG分岐で[manager+0xA0]をESIへ置き、0x00502580をCALL。0x004BF7CD/CFはTEST AL / SETE AL。すなわちヘルパーAL=1で上位の継続判定はfalseになる。
7. 0x004BE220: 0x004BE29Dで0x004BF780をCALLしAL==0で0x004BE2AB cleanup、0x004BE2CAで曲インデックスを加算、0x004BE307で0x004BDE40をCALLし次曲処理へ。ほかのゲート(manager+0x24、backend+0x38、param_2&0x1F等)も存在し、無条件の曲送りではない。
8. 0x00502160 cleanupは0x005021CD/0x005021D0で+0x58/+0x54双方を0に戻す。旧worker書込(+0x58=1/2,+0x54=actualBytes)と読取、曲送り、クリアを接続した。以前の04時台50/50やWave64件を二重計上しない。

## 要VERIFY: 半バッファ判定の非対称性
worker 0x005024CEは前半更新時EOFでstate2を記録。0x00502557は後半更新時EOFでstate1を記録。後半更新Lock(offset=H, request=2H)の最初の領域だけをデコードする。
state2はplayCursor<Hまで待ってstate1に遷移する。state1はplayCursor>=actualBytesだけを見る（H加算なし）。EOFが後半で起きた直後、playCursor<HかつplayCursor>=actualBytesなら後半を再生する前に曲送り候補になる。これは静的経路に基づく疑義で、原作不具合と断定しない。GetCurrentPosition失敗時はAL=0。

## Golden設計（合成条件。原作ゲームNOT RUN、PASS 0）
- N=8192/H=4096。state2, pos=5000 → helper=0,state2を維持。state2,pos=2000 → helper=0,state1へ遷移。state1,bytes=1000,pos=999 → helper=0。state1,bytes=1000,pos=1000 → helper=1、上位のOGG継続判定false。これはASMの分岐を整理した机上入力であってゲーム実測ではない。
- EOFが後半で発生しstate1,bytes=1024,pos=2000（前半内）という状態に到達した場合、helper=1。実際にこれが発生し早期曲送りとなるかは、バッファカーソル、呼出頻度、音声停止時のタイミングを採取するGoldenで確かめる。
- 失敗系はGetCurrentPosition HRESULT<0、stop要求、長さNの奇数、loop有効空OGGを別々にテスト。動的実行は今回0。
- 追加注意：state==2以外の非ゼロ値も第2分岐へ進む。通常生成源はstate1/2のみだが破損値経路は未検証。

## 保存・既存証拠との非重複
- 前回研究：REA-LOCAL-20261026-0431-P0-OGG-WORKER-PINGPONG-EOF-STATIC-01。今回はconsumer 0x00502580の状態機械、0x004BF780の戻り値反転、0x004BE220の曲送り分岐が新規。
- 05時台証拠：REA_20261026_05H_STREAM_EOF_XREF_PROBE.py（限定2領域探索、候補絞り込み）、REA_20261026_05H_EOF_CHAIN_DISASM.py（対象3関数のASM/DB直接照合）、REA_20261026_05H_EOF_GATE_AUDIT.py（48静的条件）、REA_20261026_05H_EOF_LATCH_EVIDENCE.json（exclusive createと読戻しPASS）。
- 既存正式Wave1～5=64/64は2026-10-11ログによる旧同期値。04時台以前の監査件数を今回へ加算しない。今回の正式5証拠: info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_SOURCE / callers=INDEX_ONLY / callees=INDEX_ONLY。正式新規5種完備0、VERIFIED+0。正式TODO/VERIFY/BLOCKED書込差分0/0/0。
- DB quick_check=ok、EXE/DBの実計算SHAは上記一致。新規専用監査48/48 PASS、独立別プロセス確認はREADBACKへ。原作ゲームGolden0・strict MATCH未測定・完全複製率未測定。
- 今回の補助probeは初回に外部関数識別子EXTERNAL:00000001を16進数へ変換してValueError。SQLite正本・原本は不変で、外部行を除外する通常のコード修正後に成功。安全拒否ではない。日本語報告書書込前のJS引用符エラーはツール実行前の失敗でPCファイル無変更、その後正常保存。
- 前回の13/14時台OFFLINE-UNSYNCED成果はこのrunで同期していない。原本/MASTER/QUEUE/PROGRESS/既存runs/他レーン/Git/Work/スケジュールは無変更。新規REA・Ghidra起動0、実ゲーム実行0。

## 次回
P0次回：0x004C24B0の更新周期・バックエンド選択と0x004BF780戻り値の実条件を照合し、EOF後のstop/nextトリガを時系列で確定。read-onlyを先行し、Goldenは未測定のまま隔離。
