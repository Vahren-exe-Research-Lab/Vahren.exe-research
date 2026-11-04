# 迫真戦記 REA｜2026-10-29 13H Oggモード別静的関数表と間接CALL確定
研究ID：`REA-LOCAL-20261029-13H-P0-OGG-RESIDUE-MODE-DISPATCH-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。REA正式5種新規=0、正式VERIFIED増分=0、ゲームGolden=NOT RUN。

## 事前照合と旧研究との関係
- Local PCオンライン。MASTER/5レーン規約/共通ルール、REA README/QUEUE/PROGRESS、最新有効sync、既存12Hレポート・EVIDENCE/READBACK、Ghidra検索基盤README/BUILD_MANIFESTを先読。
- 隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、検索SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` は今回のauditで実測一致。SQLite quick_check=ok。
- 有効sync `logs/progress_sync_20261011T153958076Z.json` のWave1〜5=64/64。古いQUEUE/PROGRESSはEPERM staleなので集計しない。12H=53/53 PASSは保存済み根拠として確認。
- 開始時 active.lockなし、Java/Ghidra先行プロセスなし、空きRAM約16.33GiB。10/28未同期Library成果は未統合。禁止Wave6・安全拒否VA/REA再エクスポートは未試行。

## 新たなP0：静的関数表の本当の参照構造
- 12Hに見つけた `0x0061AE7C/9C/BC` の3関数ポインタは、**3つの8スロット（0x20バイト間隔）で構成するモード別ディスパッチ表の各+0x1Cスロット**である。
- 二段の静的表 `[0x00612E60+4*mode]` がテーブル本体 `0x0061AE60/0x0061AE80/0x0061AEA0` を選び、各テーブルの `+0x1C` は順に `0x005E08A0 / 0x005E0B20 / 0x005E0DC0`。
- `0x005DF96C MOV EDX,[ECX+EAX*4+0x520]` がchannel側のモード選択値を取得、`0x005DF973 MOV ECX,[EDX*4+0x612E60]` で表を選択、`0x005DF97D MOV ECX,[ECX+0x1C]` でハンドラを取得、**`0x005DF991 CALL ECX`** で実行する。`0x005DF99D ADD ESP,0x14` はこの呼出しが5引数であることを裏づける。
- したがって12Hの「仮想関数テーブル候補」は、**この経路に限ればオブジェクトvptrによるdispatchではなく、mode-indexedの静的関数ポインタ表**と訂正する。C++仮想関数テーブルかどうかの一般論ではなく、実際の参照コードに基づく分類。
## 8スロットの差分と別CALL site
| mode | 表の先頭VA | +0x14 | +0x18 | +0x1C (復号wrapper) |
|---:|---|---|---|---|
| 0 | `0x0061AE60` | NULL | NULL | `0x005E08A0` |
| 1 | `0x0061AE80` | `0x005E0960` | `0x005E0900` | `0x005E0B20` |
| 2 | `0x0061AEA0` | `0x005E0B80` | `0x005E0CF0` | `0x005E0DC0` |

- 3モードに共通する `+4=0x005DFE10`、`+8=0x005DFFC0`、`+0x0C=0x005DFC60`、`+0x10=0x005DFC90` もPEの32bit little-endianデータで一致。mode0の `+0` もNULL、mode1/2の `+0` は `0x005DFD10`。
- `0x005D42A8 JS` と `0x005D42AE CMP EAX,3` / `0x005D42B1 JGE` は**その局所経路では**mode<0またはmode>=3を拒否し、`0x005D42B7` で `0x612E60` を索引、`0x005D42C6 CALL EDX` で `+4`のハンドラを呼ぶ。
- `0x005D3E9C`→`0x005D3EA4`→`0x005D3EA7` は表の `+0x0C`、`0x005D4BE7`→`0x005D4BF4`→`0x005D4BF8` は `+0x10` を選んで間接CALL。
- `0x005DF6F9`→`0x005DF703`→`0x005DF717` は `+0x14`、`0x005DF75F`→`0x005DF769`→`0x005DF788` は `+0x18` を参照する。この2スロットはmode0でNULLのため、**mode0へ到達しうるか・事前guardがあるかが重要な未検証点**。実際のNULL CALLやクラッシュは証明していない。
- 機械語、Ghidra索引の間接CALL候補、6地点のデータxrefs、32bit表スロットを照合。直接caller=0の関数が上記の表経由で到達候補を持つことを具体化。ただしゲーム中の呼出し実測はない。

## 検証格付け・状態
- 独立静的監査 `REA_20261029_13H_P0_OGG_RESIDUE_MODE_DISPATCH_AUDIT.py` は **73/73 PASS、0.600秒**。独立読み戻しは別プロセスで実施。全体所要時間とCPU負荷は不明。
- 5種類：info=検索DB入口情報、pseudo=既存Ghidra擬似C、assembly=隔離PEから局所Capstone、callers/callees=既存検索DBのdirect/indirect参照。**REA正式5種証拠新規取得0**、正式STATIC VERIFIED **64/64維持**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。
- Golden実測PASS=0、完全複製率は不明。今回のモード別関数表の発見を旧12H callback解決と二重計上しない。
- 原本ZIP/EXE/SAVE、他レーン・MASTER・T018・QUEUE/PROGRESS・旧RUN・検索DB・Git・公開先・自動化設定は変更なし。REA所有の新規PROBE/AUDIT/EVIDENCE/STATIC/READBACK成果のみ保存。
- 次回優先：`0x005DEDF0` 内 `+0x14/+0x18` 間接CALLのmode0到達条件をcallersとガード分岐で照合。`+0x520` 書込元が各modeの範囲保証を維持するか追跡し、mode0でNULLハンドラを実行しないことを確認する。ゲームGoldenは実測可能な別担当への条件設計に留める。
