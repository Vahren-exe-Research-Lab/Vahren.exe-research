# 迫真戦記 REA｜2026-10-31 01H｜Vorbis setup tag writer/配列境界ガード（P0）
研究ID：`REA-LOCAL-20261031-01H-P0-VORBIS-SETUP-TAG-BOUND-WRITER-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。22Hの3つの間接CALL・呼出先4関数、00Hのfclose登録元は再計上しない。

## 今回の新規静的証拠
- `0x005D4160` は `0x005D4167` で外側引数の `+0x1C` からinner構造体を取得し、Vorbis setupの種別(tag)を書き込む。Ghidra V9疑似Cと原作同一SHAのCapstone ASMを照合。
- ビットリーダ `0x005E6E10` は `0x005E6E25` のマスク表 `0x00623E40` を利用し、正常時 `0x005E6EE2` でANDマスクを適用。6bit=0x3F、8bit=0xFF、16bit=0xFFFF。範囲外/読込不足は `0x005E6EE9..0x005E6F03` で `0xFFFFFFFF` を返す。
- `0x005D4201 / 0x005D4274 / 0x005D42E7` の6bit countは +1 され **1..64**、各tag配列とpointer配列は `0x100/4=64` 要素。先頭 `0x005D417D` の8bit countは +1 され **1..256**、`inner+0x720..+0xB1F` に256個のポインタを格納する。
- **2種tag群**：`0x005D4225` から16bit tag取得→`0x005D422D` で `[EDI-0x100]` へ格納→`0x005D4235` 負数reject / `0x005D423E` >=2 reject→`0x005D4244` 表引き。tagは正常時0/1のみ。
- **3種tag群**：`0x005D4298` 取得→`0x005D42A0` 格納→`0x005D42A8` 負数reject / `0x005D42B1` >=3 reject→`0x005D42B7` 表引き。tagは正常時0/1/2のみ。
- **1種tag群**：`0x005D430B` 取得→`0x005D4313` 格納→`0x005D431B` 負数reject / `0x005D4324` >=1 reject→`0x005D432A` 表引き。tagは正常時0のみ。
- 異常tagはtable dereference・現要素pointer書込より前に `0x005D43FD` へ分岐し、`0x005D4401 call 0x005D3DE0` でcleanup、`0xFFFFFF7B` を返す。6bit countの取得失敗 `-1+1=0` も同じエラー分岐へ向かう。
- 22Hの「表長を超えるtagで範囲外参照する可能性」は **このwriterの成功経路では上限ガードが存在する**ため修正。ただし、別writer、後からのtag改変、破損、解放済みpointer、競合/再入は引き続きVERIFY。

## 証拠境界と進捗
- ソースEXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。V9統合DB SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
- V9 info/pseudo/callers/callees索引＋独立局所ASM、マスク表実値、直接CALL・分岐VAを照合。独立静的監査 **38/38 PASS**（所要秒数は証拠JSON参照）。
- 新規REA正式5種証拠完備0、正式VERIFIED増加0。既存正式STATIC VERIFIED **64/64**（`logs/progress_sync_20261011T153958076Z.json`）。正式TODO/VERIFY/BLOCKED書込差分 **0/0/0**。QUEUE/PROGRESSの旧EPERM不整合は無変更。
- 原作ゲームGolden実測PASS **0**。ゲーム完全複製率は未測定。新規REA/Ghidra・ゲーム実行は行っていない。
- 初回監査37/38はCapstoneへ「Ghidra body byte合計694」をlinear disasmの長さとして指定し、分離body range間の6バイト隙間を含めず正常return末尾を切った監査側ミス。RECOVERY-ID `REA-RECOVERY-20261031-01H-LINEAR-DISASM-LENGTH-01`（OTHER）、証拠JSON未保存で停止→linear span700へ変更、38/38 PASS。原本・既存成果無変更。未保存発見なし。
- 研究担当所有 `rea_lab/decomp_task/` だけ新規保存。MASTER/QUEUE/PROGRESS/既存RUN/A-E/原本/Git/スケジュール変更なし。PCオンライン、開始時active.lockなし、空きRAM約10.53GiB。CPU負荷/総実行時間は不明。

## 次回優先
- `0x005D4160` に対する他のcallerと初期化の前提、`0x005D3DE0` への到達前のtag/pointer alias、`0x005D44C0` におけるsetup header parsing経路の一貫性を調査する。
- Golden条件案：tag負数/上限0,1,2,3、各count最大64/256、truncated bitstreamでの `0xFFFFFFFF`、cleanup時のfree重複/範囲を個別テスト（すべて未実測）。
