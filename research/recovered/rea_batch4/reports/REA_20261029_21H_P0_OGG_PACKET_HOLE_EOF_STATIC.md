# 迫真戦記 REA｜2026-10-29 21H Oggパケット欠損・上位復号の終了値変換
研究ID：`REA-LOCAL-20261029-21H-P0-OGG-PACKET-HOLE-EOF-CALLER-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。原作音声の実機Goldenは未実測。正式REA5種証拠の新規VERIFIEDなし。
## 出典と前回との差分
`MASTER_LEDGER.md`、`ANALYSIS_LANES_PROTOCOL.md`、REA `README/QUEUE/PROGRESS`、20H独立監査・証拠・読戻しと既存`progress_sync_20261011T153958076Z.json`を先読。旧QUEUE/PROGRESSのEPERMによるstale表示は既存正式64/64を上書きしない。
対象隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。統合V9 DB SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、`quick_check=ok`。PC標準V3は変更なし。
V9 `callers 0x005CFA10` で2つのE8 CALLを確認：`0x005D0E43`（owner `0x005D0B60`）と`0x005D0FFA`（owner `0x005D0FB0`）。V9 `function` にて`0x005CFA10/0x005D3BC0/0x005D3AB0/0x005D0B60/0x005D0FB0`を限定取得、独立にPE機械語をデコード。
## P0 新規：パケット欠損を示す-1とパケット終端-2は別経路
`0x005D3BC0`（`0x005CFA9F`で呼出）は対象キューがない／空なら0（`0x005D3BC8/0x005D3BCF`）。キューがあれば`0x005D3BD9`から`0x005D3AB0`を呼出す。
`0x005D3AB0`は`0x005D3AC9`でエントリの`0x400`フラグを検査。立っている場合は`0x005D3AD8`でカーソル増、`0x005D3AE0`で`[EAX+0x24]`更新、`0x005D3AEB`で-1返却。通常のエントリ処理でも`0x005D3BA3`でカーソル増、`0x005D3BAB`で保存し、`0x005D3BB6`で1返却。
上位`0x005CFA10`では、キュー結果-1が`0x005CFAB1`の分岐から`0x005CFC6E`の**-3**へ変換される。一方`0x005CFDC4`の**-2**は別の入力・状態境界で返す。21H新規の差分は、欠損エントリのカーソルが進むことと、二つの上位callerの異なる終了処理。
`0x005CFAD9`で復号wrapperの非0結果を次のパケット探索へ戻すことは20H確認済みで再計上せず。同一欠損エントリを単純に無限再試行すると断定できない。上流が新規破損パケットを供給し続ける場合の停止性・経過時間は未解決。
## P0 新規：二つのcallerによる戻り値契約の相違
**PCM出力側** `0x005D0FB0`：`0x005D0FFA CALL 0x005CFA10` → `0x005D1002 CMP EAX,-2` → `0x005D1005 JE 0x005D12CD` → `0x005D12CF XOR EAX,EAX`。したがって-2だけは0へ変換。その他は`0x005D100B TEST EAX,EAX`、正数なら`0x005D100D JG 0x005D0FD1`で再試行、0以下なら`0x005D100F`からEAXを保って戻る。-3はこの直接経路で0に変換されない。
**シーク/位置更新側** `0x005D0B60`：`0x005D0E43 CALL 0x005CFA10` → `0x005D0E4B TEST EAX,EAX` → `0x005D0E4D JG 0x005D0E60`。0以下なら`0x005D0E52 CALL 0x005CFF10`を使い位置フィールド`+0x50/+0x54`を更新。V9擬似Cでは`0x005CFF10`はリンクされたストリームの長さを合計する候補だが、21Hの機械語独立検査の対象外のため正確なシーク互換はVERIFY。
## 証拠境界・検証・安全
監査`REA_20261029_21H_P0_OGG_PACKET_EOF_AUDIT.py`：**48/48 PASS**、1.361秒。局所ASM・4直接CALL照合・DB/EXE SHA・旧20H 38/38と正式64/64を検証。`REA_20261029_21H_P0_OGG_PACKET_EOF_EVIDENCE.json`にassertion一覧。Ghidraからはinfo/pseudo/callers/calleesを参照しASMを別手段で照合したが、REA正式5種一式の新規取得0・新規正式VERIFIED0・正式TODO/VERIFY/BLOCKED差分0/0/0。既存64/64維持、ゲームGolden実測PASS0、完全複製率未測定。
PCオンライン、開始時空きRAM約11.03GiB、active.lockなし、先行Java/Ghidraなし。CPU負荷・作業全体の経過時間は未測定。REA/Ghidra再実行なし、ユーザー安全拒否済みVA・Wave6・既存RUNに触れず。MASTER、QUEUE、PROGRESS、他owner、原本、検索DB、Git、スケジュールは無変更。
独立読戻しは`REA_20261029_21H_P0_OGG_PACKET_HOLE_EOF_READBACK.py`および`REA_20261029_21H_P0_OGG_PACKET_HOLE_EOF_READBACK.json`に記録する。保存・読み戻しが未成功の場合はPC-SAVEDと扱わない。
**次回**：まず`0x005CFF10`の機械語による64bit位置値・エラー-131契約と、`0x005D12E0`がPCM側-3をどう処理するかを調査。連続破損パケット時の確実な停止条件は原作Golden未実測のためVERIFYに維持。
