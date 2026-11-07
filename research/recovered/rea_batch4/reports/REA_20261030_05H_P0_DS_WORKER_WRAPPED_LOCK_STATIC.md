# 迫真戦記 REA｜2026-10-30 05H：DirectSound workerの半周Lockと第2領域の受渡し
研究ID：`REA-LOCAL-20261030-05H-P0-DS-WORKER-WRAP-LOCK-ABI-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。正式REA新規VERIFIED=0、原作Golden実測PASS=0。
## 出典・非重複
隔離EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
現行統合V9 DB SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
MASTER・所有規約・REA README/QUEUE/PROGRESS・最終sync 64/64・04H 65/65監査および19/19 readback・現行V9案内を先読。旧QUEUE/PROGRESSはrename EPERM後の陳腐化を優先しない。
04Hの初期充填 `0x00502330`（Lock offset0、ENTIREBUFFER）とは**別のworker関数 `0x005023E0`**を解析。二重計上はしない。
## 新規静的発見：再生位置で切り替わる2つのLock
`h=[stream+0x28]>>1`（0x005023EC/0x005023F0）。workerは `0x00502445` でGetCurrentPosition（vtable+0x10）を呼ぶ。
`0x00502479` のLock（vtable+0x2C）はカーソル `>=h` の場合、`offset=0, dwBytes=h, flags=0`。
`0x0050250D` のLockはカーソル `<h` の場合、`offset=h, dwBytes=2*h, flags=0`。
**後者のdwBytesはhではなく2*h。** DirectSoundの実バッファ長が2*hならLock範囲は後半から前半へ回り、ptr1/bytes1とptr2/bytes2の**2領域**を返す条件となる。サイズ一致・API実挙動は未実測。
## ABIの修正：Ghidra疑似Cのunaff_*は実際のUnlock引数ではない
workerの `S` を0x005023EFでPUSH EDI完了時のESPと定義。出力localは `[S+0x14]=ptr1, [S+0x10]=bytes1, [S+0x1C]=ptr2, [S+0x18]=bytes2`。
`0x0050249E` / `0x0050252E` はデコーダvtable+4へ `(ptr1,bytes1,&actualBytes,&EOF)` のみを渡す。
`0x005024BD` / `0x0050254D` はDirectSound vtable+0x4C（Unlock）へ `(COM,ptr1,bytes1,ptr2,bytes2)` の全組をスタック経由で渡す。Ghidraのunaff_EBX/EBP/ESI/EDIは推定不正確。
従って巻戻りを伴うLockで**第2領域はUnlock対象だが、デコーダの書込対象にならない**。アプリが意図的に再生中の前半を温存する設計の可能性があり、未初期化・不具合とはまだ言えない。
## 追加VERIFY候補
`0x005024CE` は前半書込時EOFで `stream+0x58=2`、`0x00502557` は後半書込時EOFで `stream+0x58=1`、`0x00502562` は `stream+0x54=actualBytes` を保存。
`0x00502580` 側は状態2ならカーソル<半分で状態1へ移し、状態1なら `cursor >= actualBytes` で1を返す（0x005025DE～0x005025E3）。後半へのオフセット加算が見えず、条件付き早期EOF候補。上位callerおよび動的再生位置未確認のため**VERIFYのみ**。
## 検証と所有境界
局所Capstone x86原作機械語＋現行V9 readonly索引＋前回独立保存証拠の検査：**89/89 PASS（0.9354秒）**。新規REA/Ghidra起動0、実機Golden0。
5種：info=V9、pseudo=V9、assembly=局所Capstone、callers/callees=V9索引（正式REA5種証拠新規完備0）。正式64/64維持、TODO/VERIFY/BLOCKED正式書込差分0/0/0、完全複製率未測定。
PC接続正常、active.lock無し、Java/Ghidra競合無し、preflight空きRAM約11.75GiB。CPU負荷と総所要時間は不明。原本・MASTER・QUEUE・PROGRESS・既存RUN・他レーン・Git・スケジュール無変更。
次：`0x00502580` の上位caller、`0x00502220`のDirectSoundバッファ生成長の対応、後半EOFの実機Golden条件を確認。安全拒否済みVA/操作は触れない。
