# 迫真戦記 REA｜2026-10-30 07H：Ogg PCM形式の16bit切詰めと32bit積の境界
研究ID：`REA-LOCAL-20261030-07H-P0-OGG-PCM-FORMAT-TRUNCATION-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。原作Golden実測PASS=0、正式REA VERIFIED新規=0、正式5種証拠完備新規=0。

## 出典・先行成果との照合
対象は同一SHAの研究専用EXE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
現行V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。SQLite quick_check=ok、対象4関数登録・ABI未承認。
旧run及び2026-10-11同期ログでWave1～5の正式STATIC VERIFIEDは64/64。QUEUE/PROGRESSのEPERM由来の陳腐化は解消したと扱わない。
10/25 19Hの形式builder同定、10/30 06HのN=約1秒・奇数サイズ、10/26 05HのEOF判定、10/26 00HのQueryInterface失敗経路は既発見であり、新規扱いしない。

## 新規P0静的証拠：WAVEFORMATEXのフィールド幅と乗算入力幅の不一致
`0x00502100` は `0x00502100 CMP BYTE PTR [EDX+5],0` のreadyフラグのみを確認する。
`0x00502111 MOVZX ECX,WORD PTR [EDX+0x108]` → `0x00502118` で`wChannels`へ16bit保存、`0x00502125` → `0x0050212C`で`wBitsPerSample`へ16bit保存する。
一方`0x00502130 MOV ECX,DWORD PTR [EDX+0x110]`、`0x00502136 IMUL ECX,DWORD PTR [EDX+0x108]`、`0x0050213D SHR ECX,3`、`0x00502147 MOV WORD PTR [EAX+0xC],CX`は**raw32値同士の積からnBlockAlignを16bit切詰め**する。`0x00502140 MOVZX EDX,CX`、`0x00502143 IMUL EDX,[EAX+4]`、`0x0050214D MOV [EAX+8],EDX`は**切詰め済みblockAlign×raw32 sampleRateの32bit積**をnAvgBytesPerSecへ置く。
`0x0050224F`でbuilderを呼ぶ上位`0x00502220`はAL成否のみを確認し、`0x00502260`から`0x00502269`でnAvgBytesPerSecをDSバッファ長+0x28へ転記して`0x005022C4`のCreateSoundBufferへ進む。観測した区間内には幅0や長さ0の独立した数値検査・下限clampはない（OS/デコーダ側の先行検査有無は未確認）。

## 数値境界モデル（すべて合成値であり原作実機で未観測）
通常44,100Hz・2ch・16bit：nBlockAlign=4、N=176,400、H=88,200（**既知再現用**、新規算入しない）。
11,025Hz・1ch・8bit：N=11,025、H=5,512（**06H既知**）。
形式1Hz・1ch・8bit：N=1、workerのH=0。形式44100Hz・2ch・1bit：nBlockAlign=0、N=0。いずれもDirectSoundが受容するかは未検証で、実再生到達を主張しない。
`bitsRaw=0x00010008`・ch=1・rate=44100の場合、wBitsPerSample=8なのにnBlockAlign=8,193、N=361,311,300。低16bitへの保存とraw32積のずれを示す**合成反例**である。通常のOgg/Vorbisデコーダがこの入力を生成できる証拠はない。
rate=`0x40000000`・2ch・16bitならblockAlign=4でも32bitでN=0になる（32bitラップの合成境界）。この形式の有効性・ゲーム実行到達は一切証明していない。

## 監査、保存範囲と次のVERIFY
read-only統合V9索引(info/pseudo/callers/callees)＋専用EXE局所Capstone(assembly)と独立合成算術の検査：**49/49 PASS、0.888秒**。正式REA5種証拠を新規取得していないため新規VERIFIED=0。正式TODO/VERIFY/BLOCKED書込差分=0/0/0、完全複製率未測定。
PC Local接続正常、開始時active.lockなし、Java/Ghidra競合プロセス検出なし、空きRAM約11.8GiB。CPU負荷・研究全体の実行時間は不明。新規REA/Ghidra、原作ゲーム、Goldenはいずれも実行0。
出力はREA所有`rea_lab/decomp_task`の07H新規ファイルのみ。MASTER、QUEUE、PROGRESS、旧runs、他レーン、原本、Git、Work、スケジュールは変更なし。
次は`0x00501E20`と関連するOggデコーダのproducerにおける`+0x108/+0x10C/+0x110`の値域制約を確認し、合成境界が実データから到達可能かを切り分ける。`0x00502580`のEOF state1/2と短い実読込長を組み合わせたGolden試験条件も検討する（実測せず）。
