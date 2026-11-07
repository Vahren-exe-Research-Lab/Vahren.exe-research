# REA P0｜Ogg worker 0x005023E0：二相バッファ更新・EOF分岐・間接CALL
研究ID：REA-LOCAL-20261026-0431-P0-OGG-WORKER-PINGPONG-EOF-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。新規正式REA VERIFIED0、Golden実測0。
原作研究用EXE SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
検索DB SHA256：0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
前回研究：REA-LOCAL-20261026-0334-P0-OGG-LOCK-DECODER-ONE-SEGMENT-ABI-STATIC-01。前回のInit fill・vtable確定・p2未書込は旧成果であり再計上しない。

## 新規P0-01｜ワーカースレッドは0x00502330を呼ばない
- Ghidra12.1.4検索DB：worker 0x005023E0 は414バイト。callers/calleesの直接CALL索引はいずれも0。0x005022FBから関数アドレスを__beginthreadへ渡すDATA参照があり、直接CALL無しは未使用を意味しない。
- 独立PE/Capstone全関数逆アセンブル：worker内にGetCurrentPosition/Lock/Decoder::fill/Unlock相当の間接CALLを直接持ち、前回初期化専用0x00502330へのCALL無し。
- vtable+0x10を0x00502445（再生カーソル取得）、+0x2Cを0x00502479/0x0050250D（Lock）、decoder+0x04を0x0050249E/0x0050252E（Ogg設定なら0x00501F10）、+0x4Cを0x005024BD/0x0050254D（Unlock）で呼ぶ。0x00502567はSleep(100)に相当するimport間接CALL。
- Ghidra間接CALL索引は8 site。前記CALL targetは通常のDirectSoundBuffer8およびOggDecoder vtableという前提を満たした場合の解決であり、実機vptrは未採取。

## 新規P0-02｜再生カーソルによる二相交互更新
- 0x005023EC/0x005023F0：stream+0x28を2で割ってH=floor(N/2)とする。0x00502410：stream+0x4C終了要求なら終了。
- 0x00502420：stream+0x50==1のみ通常動作。+0x50==3なら0x0050242Fで内部位相EDIを0へ戻す。それ以外は更新せずSleep(100)。
- 0x00502445：DirectSoundBuffer8 vtable+0x10で再生カーソルposを取得（HRESULT検査無し）。
- EDI==0かつpos>=H（0x00502447/4F/53）なら0x00502479 Lock(offset=0, bytes=H, flags=0)。Lock HRESULT<0なら更新せず次のSleep。
- Lock成功→0x0050249E decoder vtable+0x04→0x005024BD Unlock。戻り値を検査せずEDI=1へ切替（0x005024BF）。
- EDI==1かつpos<H（0x005024DA/E3/E7）なら0x0050250D Lock(offset=H, bytes=2H, flags=0)。0x00502506のLEA [EBP+EBP] をbytesにpush、0x0050250BのEBPをoffsetとしてpush。
- 後段は0x0050252E decoder fill→0x0050254D Unlock、戻値を検査せずEDI=0（0x0050254F）。ここでbytes=2HはHではない。範囲が折返す際はp2/len2が非ゼロになり得る。
- 両分岐ともDecoderにLockの第1領域p1/len1を渡し、第2領域p2/len2はUnlockへ渡すのみ。第2領域が非ゼロでも未更新なのは確定した機械語上のデータフローだが、再生中半分を保持する意図なら異常とは限らない。

## 新規P0-03｜EOFの方向情報と実読込byte数
- worker側decoder呼出はNULL出力でなく、0x0050248A/0x0050251AのEOF out pointerと0x0050248F/0x0050251Fの実読込bytes out pointerを渡す。前回0x005023A0初期化経路のNULL/NULLとは異なる。
- decoder 0x00501F10：0x00501F54でEOF outを0へ毎回初期化。非loopのread==0では0x00501FDCでEOF=1、実読込bytesを0x00501FE6で出力。loop flag==1なら0x00501FB7で読込位置を先頭へ戻して同要求を続行する。
- EOF=1で第1半分を書いた場合、0x005024CEでstream+0x58=2。第2半分を書いた場合、0x00502557でstream+0x58=1。どちらも0x0050255E/62でstream+0x54に実読込bytesを書き込む。
- decoder return値、Unlock HRESULT、再生カーソル取得HRESULTをworkerは検査しない。Lock HRESULTは負値なら次周期へ進み、内部位相は維持される。
- ループ対象が毎回read==0を返す場合、decoder内でreseek→read0の繰返しに出口が見当たらない。空loop OGGなどで本当に発生するかはVERIFYであり、再現済みのハングではない。

## 独立証拠・既存成果の区別
- REA_20261026_04H_P0_WORKER_READONLY_PROBE.py：原作EXE SHA・DB SHA検査付きで0x005023E0/0x00502330/0x00501F10をCapstoneで逆アセンブル。原本もDBもread-only。
- REA_20261026_04H_P0_WORKER_AUDIT.py：worker機械語33箇所・関数境界・8間接CALLサイト等、独立静的監査50/50 PASS。REA_20261026_04H_P0_WORKER_PINGPONG_EVIDENCE.jsonは保存済み監査JSON。
- Ghidra検索：function 0x005023E0/0x00501F10/0x00502220、callers 0x005023E0、related depth2、callees 0x00502330。機械語と疑似Cを相互照合。Ghidraの疑似CにはUnlock引数のunaff_*等の不完全な表現があり、実引数はASMを優先。
- 5種類証拠：info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_SOURCE / callers=INDEX_ONLY（関数ポインタDATA参照別途確認） / callees=INDEX_ONLY。新規関数別の正式5種完備0、新規REA VERIFIED0。
- 既存正式Wave1～5 64/64は2026-10-11保存 logs/progress_sync_20261011T153958076Z.json の既存成果（QUEUE/PROGRESSのrename EPERM表示は旧）。64は旧累計で今回の新規加算なし。
- 正式TODO/VERIFY/BLOCKED書込差分0/0/0。新規独立VERIFY：二相Lockのp2/len2と保持内容、EOF状態の読み手、GET cursor失敗、loop空入力、odd N、worker終了との競合。
- 原作ゲームGolden PASS 0 / strict MATCH未測定 / 完全複製率未測定。REA/Ghidra/ゲームを新規起動していない。Work使用0。FLS拒否済み操作、Wave6、禁止VAは実行していない。

## 再開位置
P0次回：stream+0x58と+0x54のconsumer/クリアタイミングをxrefs/機械語で追跡し、EOFと停止・ループ・再生復帰の対応を確定する。通常Golden案：N=8192、H=4096でpos 5000→2000を跨ぐときLock(0,4096)→Lock(4096,8192)になるか、p2/len2/内容を実ゲームで確認。異常Golden案：短い非loop、空loop、GetCurrentPosition/Lock/Unlock失敗を別々に検証（いずれも未実行）。
13/14時台オフライン成果のPC正本同期は本runでもしていない。原本/MASTER/QUEUE/PROGRESS/既存runs/他レーン/Git/公開/スケジュールを変更しない。
