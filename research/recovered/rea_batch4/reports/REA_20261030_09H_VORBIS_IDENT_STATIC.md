# 迫真戦記 ver0.67｜REA P0 Ogg Vorbis identification header gate（2026-10-30 09H）
研究ID：`REA-LOCAL-20261030-09H-P0-VORBIS-IDENT-RATE-GATE-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。原作Golden実測0、正式REA新規VERIFIED0。

## 前提・重複除外
対象は同一SHAの研究専用EXE（SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）および統合V9 DB（`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`）。旧runは既存Waveの静的64/64を維持、正式5種新規完備0。既知08HのOggビット深度16固定、07Hの整数幅、06HのPCMサイズは再計上しない。

## 今回の独立静的根拠
V9の関数境界・疑似C・E8 CALL台帳と、研究専用PEからCapstoneで局所逆アセンブルした原命令を照合。
- `0x005D1572 → 0x005CF010`：Ogg open時のヘッダ取得処理。`0x005CF167 → 0x005D44C0`：Vorbisヘッダ種別でdispatcherへ。
- `0x005D44C0` は識別ヘッダ type=1 / signature `vorbis` を検査し、`0x005D45B0 → 0x005D3F60` へ進む。
- `0x005D3F87` の8bit読み込みを `0x005D3F92 MOV [EDI+4],EAX` でchannelsへ保存。次の32bit読み込み結果を `0x005D3F9D MOV [EDI+8],EAX` でsampleRateへ保存。
- `0x005D3FED CMP [EDI+8],1 / 0x005D3FF0 JL` は符号付きサンプルレート1以上を要求。`0x005D3FF2 CMP [EDI+4],1 / 0x005D3FF5 JL` はチャンネル数1以上を要求。
- `0x005D3FF9..0x005D4008` はVorbisブロック長の順序・下限64・上限8192を検査。`0x005D4014 CMP EAX,1` は終端framing bitを検査。
**今回の新規限定結論：有効識別ヘッダの11,025Hzはこの単独検査では拒否されず、奇数Hz禁止の分岐も当該関数には見つからない。** 他のVorbisセットアップ・デコーダ・DirectSound段階の成功は未証明。

## 追加確認・限界
先行08Hの半周非整列（mono16:11025 bytes % 2=1、stereo16:22050 bytes %4=2）に、識別ヘッダの正のsampleRate条件を接続した。**実機音声の不具合、パケット全体の許容、コールバックABI確定の主張ではない。**
独立監査 `43/43 PASS`（0.871秒）、PC側V9 `PRAGMA quick_check=ok`。初回監査42/43は自作監査プローブの0x005D1490取り込み漏れによるもので、本体コード異常でも安全拒否でもない。修正後43/43 PASS。
REA5種はinfo/pseudo/callers/calleesが既存V9索引、assemblyのみ今回の対象PE局所照合。正式REA新規5種完備0・VERIFIED0、TODO/VERIFY/BLOCKED正式更新0/0/0、Golden0、完全複製率未測定。
開始前PC接続正常、active.lockなし、Java/Ghidra対象プロセス0、空きRAM約11.68GiB。CPU負荷・研究全時間は未測定。新Ghidra/REA起動なし。MASTER、QUEUE、PROGRESS、既存RUN、他owner、原本、Git、スケジュール無変更。

## 次の優先検証
`0x00501F10` のOvRead byte count（奇数半周Lock時の入力サイズと戻り値）、`0x005023E0` の第1領域実長とUnlock値、`0x00502580` のEOFカーソル条件を突合。実機Golden候補は11,025Hz mono/stereo Ogg と44,100Hz対照。原作Golden未実測、実機挙動はVERIFYを維持。
