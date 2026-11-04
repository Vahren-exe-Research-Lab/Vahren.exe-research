# 迫真戦記 ver0.67｜REA 2026-10-30 11H P0：奇数HzでのPCM余剰消費とフレーム非整列の静的条件
研究ID：`REA-LOCAL-20261030-11H-P0-ODDRATE-DECODE-ADVANCE-ALIGN-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**（実ゲームGolden PASS 0、完全複製率未測定）。
## 既存成果からの差分
10Hの奇数Hz→-131→EDI巻き戻り、10/29 22Hの負戻値unsigned判定、09HのVorbis正サンプルレート許容は既知。今回の新規部分は**Vorbis成功時の実フレーム消費点（0x005D128D）とbyte-count戻り（0x005D12B7/0x005D12BA）を、上位の再書込先と接続し、PCM消費超過・内部フレーム境界ずれを定量化したこと**。
## 静的根拠
- 研究専用PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、既存統合V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。V9 quick_check=ok、旧run sync正式64/64、10H監査57/57を照合。
- `0x005D1046` の割算と `0x005D105B MOV EAX,-131` は要求長が1 PCMフレーム未満の際のエラー経路候補。正常な正数復号では `0x005D128D CALL 0x005D5790` にてフレームを消費し、`0x005D12B7/BA`で `frameBytes * frameCount` をEAX返却。エラー経路はこれらの消費処理を通らない。
- `0x00501F87 LEA EDX,[EDI+ECX]` が出力先を設定し、`0x00501F91 CALL 0x005D12E0`で復号。`0x00501FC2 ADD EDI,ESI` は負の -131 も加算する。初期メモリは `0x00501F5D CALL 0x005BE400` でゼロ化される。
- 前提：Vorbis側に十分なPCMがあり、正数返却が要求サイズ以下の最大フレーム整数倍になり、DirectSoundのLockが半周の非整列サイズを受理し、第1領域を要求長で返すこと。**原作実機での成立は未証明**。
## 独立合成モデル（書込先のバイト位置とVorbisの実消費バイト数は別）
16bit・チャンネル数C、1秒バッファ長=2*rate*C、半周H=rate*C、フレームサイズF=2*C。奇数rateならH mod F=C。-131は上位EDIを131戻すがVorbis消費位置は戻さない。正数返却の総和は、最終EDI=Hの条件でH+131*(負返却回数)になる。
| 11,025Hz | H byte | -131回数 | 正数復号総byte | Hからの超過 | フレーム非整列の書込開始byte |
|---|---:|---:|---:|---:|---|
| Mono C=1 | 11,025 | 1 | 11,156 | +131 | 10,893 |
| Stereo C=2 | 22,050 | 2 | 22,312 | +262 | 21,917 / 21,918 |
| 3ch C=3 | 33,075 | 3 | 33,468 | +393 | 32,941 / 32,942 / 32,943 |
| 4ch C=4 | 44,100 | 4 | 44,624 | +524 | 43,965 / 43,962 / 43,967 / 43,964 |
44,100HzのC=1..4対照では-131=0、正数復号超過0、非整列書込0。両群とも合成書込範囲は半周内であり、**このモデルだけからオーバーランは導けない**。
## 追加境界と未解明
極低レート1Hz/monoでは最初の1byte要求に-131が返る合成経路があり、EDIの32bit表現は`0xFFFFFF7D`となってunsigned完了判定へ進む。ただしVorbisヘッダ以外の初期化・DirectSound受理は不明。実環境の実害・音声不連続・sample alignment・EOF発火についてはVERIFYを維持。
## 監査・運用
`REA_20261030_11H_P0_ODDRATE_ADVANCE_AUDIT.py` を使用してPE命令・V9関数/CALL・既存証拠・1〜4ch合成計算 **60/60 PASS、0.8371秒**。新Ghidra・REA・原作ゲーム実行なし。正式新規REA5種完備0、新規正式VERIFIED0、既存64/64維持、正式TODO/VERIFY/BLOCKED差分0/0/0、Golden0。
PC接続正常。開始時active.lockなし、Java/Ghidra競合なし、空きRAM約15.43GiB。CPU使用率・総作業時間は不明。原本/MASTER/QUEUE/PROGRESS/RUN/A〜E/Git/スケジュール変更なし。未同期オフライン成果を統合済みとは扱わない。
## 再開位置
`0x005D5790`の消費フレームの内部状態更新、`0x005023E0`における実際のLock HRESULT/領域長と半周境界、`0x00502580`のEOF判定との整合を優先。Goldenは11,025Hz mono/stereo・44,100Hz stereo、短尺/途中欠損を独立に比較し、実機未測定はPASSしない。
