# 迫真戦記 ver0.67 REA｜2026-10-30 08H：Ogg入力からWAVEFORMATEXへの固定16bit制約と半周PCMフレーム境界
研究ID：`REA-LOCAL-20261030-08H-P0-OGG-BITS16-PRODUCER-HALF-FRAME-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。Golden実測PASS0、正式REA新規VERIFIED0、正式5種証拠完備0。

## 前提と非重複
対象は元EXEと同一SHAの研究専用コピー（SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）。統合V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、`PRAGMA quick_check=ok`、対象関数の索引存在を確認。
既存REA Wave1～5の正式静的VERIFIEDは2026-10-11同期ログの64/64を維持。QUEUE/PROGRESSは旧EPERMによる表示差分があり、今回は修正しない。
10/25 OggDecoderロード、10/30 06HのN/Hの算術、07Hのraw32とlow16幅不一致は既発見として再計上しない。今回は**producer固定値と到達条件**、**16bit/奇数Hzの新境界モデル**を追加。

## 新しい静的根拠：ロード成功経路でbits/sampleは16に固定
`0x00501E20` constructorは `0x00501E56/5C/62` でdecoder `+0x108/+0x10C/+0x110` をゼロ初期化し、`0x00501E93`から`0x00502020`を呼ぶ。
`0x00502020`では `0x0050202A CALL EDX`（vtable `+0x10` cleanup）、`0x00502038 CALL 0x005D16C0`（Ogg開封）、`0x00502040 TEST EAX,EAX` と `0x00502042 JE 0x0050204C` により成功時のみ後段へ進む。
成功時 `0x00502060 CALL 0x005D0F70` による情報ポインタの `+4` を `0x0050206B` でdecoder `+0x108`へ保存、`+8` を `0x0050207F` で `+0x10C`へ保存。**`0x00502071 MOV DWORD PTR [ESI+0x110],0x10` によりbits/sampleのraw32値を16固定**し、最後に `0x00502085` でready(`+5`)=1とする。
`0x00501EB0` cleanupは `0x00501EF3/F9/FF` で3フィールドを0に戻す。形式builder `0x00502100` はreadyを先に検査し、`0x0050224F`から呼び出される。よって通常の成功済みOggDecoder生成経路では、07Hの `bitsRaw=0x00010008` や `bitsRaw=1` をbuilderへ渡す経路は見つからない。全プログラムの未知write/メモリ破壊まで否定するものではない。

## 修正される07H・06H合成条件の到達可能性
07Hの16bit高位語を使用した `nBlockAlign=8193`、1bitによる `nBlockAlign=0`、06Hの8bit奇数長N（11,025Hz/mono8）と07Hの1Hz/mono8でH=0は、**算術テストとしては正しいが、このOggLoader通常成功経路では入力前提が成立しない**。実ゲームで起きると宣言していない先行結論を、今回さらに絞った。
通常の小さな正のチャンネル数C、周波数R、16bit時は `blockAlign=2C`、`N=2CR`（32bit overflow無しの場合）、`H=CR`。したがってNは偶数であり、Ogg経路で8bit由来の奇数Nを一般化しない。

## 新規VERIFY：奇数サンプルレートは16bitでも半周境界がフレーム内へ入る
44,100Hz/stereo16なら `blockAlign=4,N=176400,H=88200,H%align=0`（対照）。
11,025Hz/mono16なら `align=2,N=22050,H=11025,H%align=1`。11,025Hz/stereo16なら `align=4,N=44100,H=22050,H%align=2`。44,101Hz/stereo16もHがalignで割り切れない。
worker `0x005023E0` がHを作り、既知の `0x00502479` / `0x0050250D` で半周更新するため、**サンプルレートが奇数のOgg** について半周境界がPCMブロック整列境界からずれる静的候補となる。Vorbis parserが11,025Hzを受容するか、DirectSound Lockが受容・補正・失敗するか、実音声に影響するかは未観測／VERIFYでありエンジン不具合断定禁止。

## 今回の監査と保存条件
`REA_20261030_08H_P0_OGG_FIXED16_PRODUCER_AUDIT.py`で局所PE+Capstone機械語、V9既存info/pseudo/callers/callees、独立計算、旧同期・先行証拠を照合。**56/56 PASS・0.8697秒**。これは新規正式REA5種証拠の取得やゲームGolden実測を意味しない。
PC接続成功、開始時`active.lock`不在。解析用Java/Ghidra/REA競合プロセスは開始前のプロセス一覧で未検出、FreePhysicalMemory約11.4GiB。CPU負荷・総作業時間は不明。新REA実行・全関数再解析・原作ゲーム実行はいずれも0。
出力先はREA所有 `rea_lab/decomp_task` の08H新規ファイルのみ。原本、MASTER、QUEUE、PROGRESS、既存runs、他レーン、Git、Work、公開先、スケジュールは変更していない。正式TODO/VERIFY/BLOCKED書込差分0/0/0、完全複製率未測定。安全拒否済みVA・Wave6・REAエクスポートへの再試行0。

## 次回P0・Golden条件（NOT RUN）
次の候補はVorbisヘッダのchannel/rate producer（`0x005D1490` → `0x005D1310`および周辺）、正常入力に対する数値制約・0値排除条件、`0x00501F10`の奇数Lockサイズでの実読込長と`0x00502580`EOF条件。
独立Golden試験案：11,025Hz mono16/stereo16の有効Oggと44,100Hz stereo16対照を用意し、Lock HRESULT/返却領域サイズ、OvRead返却byte数、Unlock成否、PCM境界、state+0x54/+0x58、停止時刻を採取する。今回実ゲーム観測は0件。
