# 迫真戦記 REA｜2026-10-31 03H｜Vorbis type1→type3→type5状態遷移と未検証の確保失敗（P0）
研究ID：`REA-LOCAL-20261031-03H-P0-VORBIS-ID-COMMENT-TRANSITION-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。前回02Hのルータ・type別入口ガードと01Hのtag上限は既知として重複計上しない。

## 新規の局所ASM・既存V9索引照合結果
- **type1本体 `0x005D3F60`**：`0x005D3F61`で `EDI+0x1C` の依存ポインタを取得。NULLなら `0x005D3F68` で -129を返す。最初の32bit読込値が非0なら `0x005D3F80` で -134を返す。
- `0x005D3F92` が `EDI+4`、`0x005D3F9D` が `EDI+8` にbit-readerの結果を格納する。成功経路では `0x005D3FED` と `0x005D3FF2` により **EDI+8>=1かつEDI+4>=1**、ブロック長下限64／上限8192・大小順序、最後のframing bit=1を要求し、`0x005D4029`から0を返す。
- そのため **type1正常終了→同じ外側オブジェクトが維持される**条件では、type3の事前ガード `0x005D4576` の `outer+8 != 0` が成立する。02H報告のルータの動作と接続できるが、全ての入力・スレッド・破損状態まで保証はしない。
- **type3本体 `0x005D4030`**：`0x005D4045/0x005D4053` で長さ範囲を検査し、`0x005D4061` の確保結果を `0x005D4069` で `ESI+0xC` に格納する。type5の事前ガード `0x005D455B` が参照する値は、この確保結果と対応する。
- `0x005D40B7` で要素数を `ESI+8` に記録、`0x005D40BE/0x005D40C8` で2配列を確保して `ESI+0/+4` に保持し、各文字列を `0x005D412C` のヘルパーで読み込む。末尾 `0x005D413A` のframing bitが1のとき `0x005D4159` 以降0で成功、異常は `0x005D4148` でcleanupを実行して -133を返す。
- **VERIFY（実行時安全性）**：type3は上記確保結果のNULLチェックが局所ASM上で見えない。`0x005D4069`直後、文字列長が非0なら `0x005D407D`で確保ポインタに書き込む。長さ0ならNULLでも成功経路へ進む余地があり、「type3が0を返せばtype5のpointerガードも必ず通る」とは証明できない。メモリ不足・allocator失敗の実機再現はしていない。
- type1のフィールド・framing条件不成立は `0x005D401A` からcleanupして -133。初期NULL（-129）／version不一致（-134）の早期returnとは別経路。type3のエラー値 -133 と合わせて、親関数 `0x005CF010` の上位伝播は継続VERIFY。

## 検査・出典・重複境界
- 静的監査：**43/43 PASS**、計測1.3851秒。独立のPE32 x86 Capstone機械語・生CALL site照合＋読み取り専用V9 SQLiteの関数存在・quick_check・旧02H証拠・2026-10-11正式同期記録を検査。ゲーム／新規REA/Ghidraの起動は0。
- ソース：研究専用`hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。統合V9索引 `HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。V9は合成静的索引でありREA正式5手法に自動昇格しない。
- 今回の証拠：`REA_20261031_03H_P0_VORBIS_HEADER_TRANSITION_EVIDENCE.json`、audit・probe各Python。従来正式STATIC VERIFIED **64/64維持**、新規正式VERIFIED **0**、正式5種新規完備 **0**。正式TODO/VERIFY/BLOCKED書込差分 **0/0/0**。既存QUEUE/PROGRESSのEPERM不一致には触れない。
- 原作Golden実測PASS **0**、完全複製率 **未測定**。ABI・allocation failure・境界外読込・再入・実ゲーム挙動は未確定。PCオンライン、active.lockなし、Java/Ghidra競合検出なし。検査時空きRAM=9,933,476KiB（約9.47GiB）、CPU負荷と総作業時間不明。

## 再開位置
次回P0：`0x005CF010`でtype1（-129/-134/-133）およびtype3（-133）由来の戻り値が上位にどう変換・伝播するかを親の各CALL site `0x005CF167`/`0x005CF279`から追跡。特にtype3長さ0またはcalloc失敗時に `ESI+0xC` がNULLでもsuccess扱いされ得るかを静的分岐と独立Golden条件案で分ける。実機テストは別途正当な環境・ownerの条件成立時のみ。
