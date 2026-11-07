# 迫真戦記 REA｜2026-10-30 06H：Oggの実バッファ長と半周Lock境界
研究ID：`REA-LOCAL-20261030-06H-P0-OGG-BUFFER-DURATION-EOF-EDGE-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。原作Golden PASS=0、正式REA VERIFIED新規=0、5種正式完備新規=0。

## 参照の健全性・重複除外
研究用EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
現行統合V9 SQLite SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。SQLite quick_check=ok。
10/29更新の`headless_analysis/00_START_HERE_ACTIVE_RESEARCH.md`は統合V9を現行と明記。10/23の旧案内に残る「既定V3」は古い記載。
旧run保存・`logs/progress_sync_20261011T153958076Z.json`に基づく初回Wave1〜5は64/64 STATIC VERIFIED。旧QUEUE/PROGRESSのEPERM不整合を修復・再集計しない。
10/25 19Hには形式builder、10/26 04Hには二相worker、10/26 05Hには0x00502580→0x004BF780→0x004BE220のEOF曲送りと早期終了疑義、10/30 05HにはLock/Unlockの引数対応が既に記録済み。**これらの発見は今回の新規に算入しない。**

## 新規の横断静的証拠：実バッファ長Nの生成元を初めてEOF半周系へ接続
`0x00502100`はdecoderのチャンネル数(`+0x108`)、サンプルレート(`+0x10C`)、bits/sample(`+0x110`)からWAVEFORMATEXを組み立てる。
`0x00502136 IMUL`、`0x0050213D SHR 3`、`0x00502140 MOVZX EDX,CX`、`0x00502143 IMUL`、`0x0050214D MOV [EAX+8],EDX`により、ブロック整列幅の16bit値と秒間バイト数(`nAvgBytesPerSec`)を作成する。
`0x0050224F`でこのbuilderを呼び、`0x00502260`で`stream+0x14`の`nAvgBytesPerSec`を読み、`0x00502269`で`stream+0x28`（DSBUFFERDESC.dwBufferBytes）へ転記。バッファ生成は`0x005022C4`の間接CALL。
worker `0x005023EC`→`0x005023F0`が`H=floor(N/2)`を作る。`0x00502479`は`Lock(0,H)`、`0x0050250D`は`Lock(H,2H)`。**Nは標準PCM条件なら約1秒分、半周Hは約0.5秒分**となる。32bitオーバーフローや異常形式、API側の最小最大制約は未保証。
標準例44,100Hz・2ch・16bitでは`N=176400,H=88200`。後半Lock要求はoffset=88,200 / bytes=176,400で、API仕様上の分割は`ptr1=88,200 / ptr2=88,200`の想定。decoderが書くのは第1領域のみ（既知）。
奇数例11,025Hz・1ch・8bitでは`N=11025,H=5512`。後半Lockはoffset=5512 / bytes=11024、分割想定は**ptr1=5513、ptr2=5511**。workerが想定する半周長Hより、後半第1領域が1byte長い。実機でこの形式を受容することや影響はVERIFY。

## API仕様から新たに整理したリスク（未実機検証）
Microsoft DirectSoundBuffer8::Lock文書では、循環バッファのwrapで2領域を返すことと、返却したポインタは**書込用途のみ**で既存内容が読取可能とは保証しないことが明記される。カード側メモリなら一時システムメモリへ書き、Unlock時に転送する場合がある。
従って後半Lock`(H,2H)`で第2領域を**書き込まずにUnlockする設計**は、「再生中の前半が必ず保全される」とはAPI契約から証明できない。ハードウェア/ドライバ依存の雑音・無音・音切れをVERIFYとする。**不具合が再現したとは宣言しない。**
Microsoft一次資料： https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee418073(v=vs.85)

## EOF側との接続とGolden試験案
`0x00502557`後半EOF→state1、`0x00502562`実読込bytes保存、`0x005025DE`はplayCursorとactualBytesを直接比較しHを足さない。これは**10/26 05H既発見**のため、新規解析件数へ算入しない。今回、Nの具体式と通常44.1kHzの半秒単位を接続した。
Golden設計：44.1kHz stereo16・短い非loop Ogg（前半/後半の各EOF）、11.025kHz mono8 odd N、DirectSoundの第2領域実返却長、Unlock前後のPCM、Play cursor、state`+0x58`、actualBytes`+0x54`、曲送り時刻を別々に採取。実ゲーム起動・観測は**0件**。

## 検証・保存境界
`REA_20261030_06H_P0_PCM_BUFFER_DURATION_AUDIT.py`で原本と同SHAの専用コピー・V9 SQLite(read-only/immutable)・Capstone局所ASM・旧成果を独立照合：**62/62 PASS（0.8563秒）**。
初回は監査命令VAを`0x00502261`と1byte誤記して61/62。正しい命令入口`0x00502260`へ修正後に62/62 PASS、初回は成果JSON未保存。安全拒否ではない。
info/pseudo=V9既存索引、assembly=局所独立機械語、callers/callees=V9索引。正式新規5種完備0、正式VERIFIED+0、TODO/VERIFY/BLOCKED書込差分0/0/0。原作Golden PASS0、完全複製率未計測。
PC接続成功、active.lock無し、Java/Ghidra/REAの解析競合未検出、空きRAM約12.1GiB。CPU負荷と研究全体所要時間は不明。新規Ghidra/REA・ゲーム実行なし。
書込はREA所有`decomp_task`内の06H独立成果のみ。原本/MASTER/QUEUE/PROGRESS/既存runs/他レーン/Git/公開先/スケジュールは変更しない。
次回：`0x00502100`でodd Nや異常形式の境界値、`0x005023E0`第2領域をUnlockする場合の実メモリ依存と`0x00502580`EOF終端挙動の合成Golden条件を深掘り。旧発見を二重計上しない。

### 監査経過の追補
独立readback初回17/18では、監査スクリプトが日本語報告内の旧成果日付を`20261026`という連結表記で検索したため1項目失敗。報告に実在する表記`10/26`に照合条件を修正し再実行した。証拠そのものの不一致・安全拒否ではない。
