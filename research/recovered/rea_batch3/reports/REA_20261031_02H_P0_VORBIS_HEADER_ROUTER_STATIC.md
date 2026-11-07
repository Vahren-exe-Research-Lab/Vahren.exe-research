# 迫真戦記 REA｜2026-10-31 02H｜Vorbisヘッダ種別ルータとセットアップ入口（P0）
研究ID：`REA-LOCAL-20261031-02H-P0-VORBIS-HEADER-TYPE-ORDER-GATE-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。01Hのtag値writer/配列境界、00Hのfclose callbackは再計上しない。

## 独立した新規静的知見
- V9 CLIで`0x005D4160`への直接CALLは **1件のみ**：`0x005D44C0`の`0x005D4564`（E8 `e8f7fbffff`）。ルータ `0x005D44C0` の呼出元は `0x005CF010` の **2箇所**（`0x005CF167`、`0x005CF279`）。
- `0x005D4420` は先行判定関数。NULL packetを拒否、packet+8が非0、先頭8bitが**1**、続く6byteが実バイト `76 6f 72 62 69 73`＝`vorbis` の場合にのみ1を返す。それ以外は0。CALL site `0x005CF148`。
- `0x005CF010` は先行判定成功の経路で `0x005CF160` に `[EDI+0x58]=3` を書き、その直後の `0x005CF167` からルータを呼ぶ。別の`0x005CF279` は後続パケット処理ループ内。ここで`outer+0x58`とルータが参照する`param_1+8`を同一フィールドと混同しない。
- `0x005D44C0` は先頭8bitのtypeと同じ6byte `vorbis` signatureを検査し、正しいsignatureのとき **type 1/3/5** だけをそれぞれ別処理へdispatchする。type=1 → `0x005D45B0 call 0x005D3F60`、type=3 → `0x005D4583 call 0x005D4030`、type=5 → `0x005D4564 call 0x005D4160`。
- type=1の前提：`0x005D4592`でpacket+8が非0、`0x005D459B`でouter+8が0。type=3の前提：`0x005D4576`でouter+8が非0。type=5の前提：`0x005D4553`でouter+8が非0、`0x005D455B`で第2引数+0xCが非0。**tag writer `0x005D4160` へ行く前に、両方の事前条件が必要**。
- 署名不一致は`0x005D45BE`で `0xFFFFFF7C`（signed -132）、NULL packet・不正type・順序条件不成立は`0x005D45A3 / 0x005D45C8`で `0xFFFFFF7B`（signed -133）。type 1/3/5の内部callee独自の失敗コードは別であり、一律-133ではない。

## 証拠・範囲
- 根拠：原作と同SHAの**研究専用コピーEXE** `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` のCapstone局所ASM／生定数、統合V9 SQLite `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` のinfo/pseudo/callers/callees。DBはread-only／SQLite quick_check=ok。
- 監査スクリプト：`REA_20261031_02H_P0_VORBIS_HEADER_ROUTER_AUDIT.py`。**50/50 PASS**。REA正式5種証拠 `info/pseudo/assembly/callers/callees` 完備の新規件数0、新規正式VERIFIED0。既存正式64/64は最新保存済syncログの値であり、今回の新規分母ではない。
- 正式TODO/VERIFY/BLOCKEDへの書込差分 **0/0/0**。古いQUEUE/PROGRESSのEPERM不整合はそのまま。ゲームGolden実測PASS **0**、完全複製率は未測定。
- これは静的な分岐条件の確認で、ヘッダ順序の原作実機挙動・入力長不足・バッファ破損・並行変更・再入を実証していない。callee ABIも正式未検証。**正常なVorbis仕様一般の証明ではない。**

## 保全と次の一手
- PCオンライン、開始時`active.lock`なし、Java/Ghidra競合なし、空き物理RAM=11,335,444 KiB（約10.81 GiB）。CPU負荷・全作業時間不明。新しいREA/Ghidra/ゲーム起動は0。
- `decomp_task`専用の新規ファイルだけを保存し、MASTER/QUEUE/PROGRESS/既存RUN/A–E/原本/Git/自動化設定は変更していない。
- 次回は `0x005D3F60` のtype1成功時にouter+8が非0へ遷移する書込、`0x005D4030` の第2引数+0xC初期化、`0x005CF010` の戻りコード変換を**逐次の状態機械**として検査する。Golden候補：type 1→3→5正常順序、type 5先行、signature1byte改変、NULL/切断header、状態値の組合せ（すべて未実測）。
