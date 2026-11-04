# 迫真戦記 REA｜2026-10-29 22H Ogg復号負値→PCM転送量の型境界
研究ID：`REA-LOCAL-20261029-22H-P0-OGG-NEGATIVE-PCM-COUNT-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**（保存後readback待ちで先にreport作成）。正式REA新規VERIFIED=0、ゲームGolden=0。
## 正本照合・非重複
MASTER、5レーンprotocol、REA README/QUEUE/PROGRESS/WAVES、21H report・evidence、既存64/64 progress-sync先読。現行検索索引は10/29移行済V9（旧 `search.sqlite` は整理済・不存在）。従来V3案内は現在の入口ではない。
隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` を実ファイル照合。SQLite quick_check=ok。
出典はV9 `function` 検索で `0x005CFF10/0x005D12E0/0x00501F10`、`callers` で関係を照合。さらに隔離PEの指定VAをCapstone x86で独立デコード。21Hの-3由来と16/16+後続正式64/64は再計上しない。
## P0新規1：復号ラッパの戻り値型を訂正
`0x005D12E0` は `0x005D1303 CALL 0x005D0FB0` の後、`0x005D1308 ADD ESP,0x24` → `0x005D130B POP EBP` → `0x005D130C RET`。EAXを書き換えないため下位関数の戻り値を保持。
V9のこの関数の疑似Cは `void` とするが、呼出側 `0x00501F91 CALL 0x005D12E0` → `0x00501F96 MOV ESI,EAX`。実機械語のデータフローは戻り値を明示的に使用。**Ghidra疑似Cのvoid表示は実コード利用実態と不一致**。ABI正式VERIFIEDには昇格しない。
## P0新規2：復号エラー-3が符号なし転送量になる候補
21H既存証拠では欠損packet `0x005D3AB0` -1 → 上位 `0x005CFA10` -3 → `0x005D0FB0` が非-2負値を保持。22Hはその上の `0x00501F10` に焦点。
`0x00501F96 MOV ESI,EAX`、`0x00501F9B TEST ESI,ESI` → 非0なら `0x00501FBF`、`0x00501FC2 ADD EDI,ESI`、`0x00501FC4 CMP EDI,EAX`、`0x00501FC6 JAE 0x00501FDF`。後に `0x00501FE6 MOV [EAX],EDI`、`0x00501FEA MOV AL,1`。
**条件付き静的帰結：** 初回 `EDI=0` で-3を受けると32bit加算結果は `0xFFFFFFFD`。要求サイズが1～`0xFFFFFFFD`ならunsigned JAEで完了分岐へ入り、転送数の出力先へ `0xFFFFFFFD` を書く。ゲーム中にこの条件が成立するか、呼出元がどう扱うかは未検証。実際の範囲外書込・クラッシュとは断定しない。
## P0新規3：位置取得の64bit負値と負添字の範囲
`0x005CFF10`: `0x005CFF20 MOV EAX,0xFFFFFF7D` と `0x005CFF25 OR EDX,0xFFFFFFFF` は64bitの **-131**。`0x005CFF88/8D` も同じ。
`0x005CFF3F/41` は負の番号を再帰和の経路に分岐し、各link値を `0x005CFF5A ADD EBX,EAX` / `0x005CFF5C ADC [EBP-4],EDX` で64bit集計。`0x005D0E4F PUSH -1` → `0x005D0E52 CALL` → `0x005D0E5A/5D` で `+0x50/+0x54` にEDX:EAXを保存。-131の上位消費契約はVERIFY。
## 静的監査と正式境界
`REA_20261029_22H_P0_OGG_NEGATIVE_PCM_AUDIT.py` の独立静的検査 **53/53 PASS、0.885秒**。参照元SHA2件、SQLite quick_check、正式64/64、21H 48/48、5関数、5 CALL site、31局所ASM＋型演算・lock等を検査。誤ったものがあれば保存せず失敗する。
新規正式REA5種（info/pseudo/assembly/callers/callees）取得 **0**、正式VERIFIED **0**、TODO/VERIFY/BLOCKED正式差分 **0/0/0**。Wave既存STATIC 64/64維持。5種形式の単独収集ではなくV9索引＋独立ASM照合の補強。
原作実機Golden PASS **0**、完全複製率 **未測定**。安全拒否済みWave6/VA、ERA exportは未試行。新REA/Ghidra起動なし。
PCはオンライン、22H前点検時 `active.lock` 無し・Java/Ghidra先行なし、空きRAM約 **12021 MiB**。CPU負荷・総経過時間は未測定。全run・原本・MASTER・他レーン・Git・スケジュールは変更していない。
## 次のVERIFY
まず `0x00501F10` の間接呼出先・所有vtableを調べ、`0x00501FE6` の転送数の実際の利用者を追う。-3到達が通常のOgg音声で起き得るか、原作Goldenは別途確認。
次に `0x005CFF10` -131戻り値を `0x005D0B60` が位置計算の分岐でどのように消費するかを追跡。-1以外の負indexも合計になる仕様の妥当性はVERIFY。
安全な再開位置：`REA_20261029_22H_P0_OGG_NEGATIVE_PCM_EVIDENCE.json` の checks / `REA_20261029_21H_P0_OGG_PACKET_EOF_EVIDENCE.json` / V9 `callers 0x00501F10`（E8直接呼出0でも間接到達は未否定）。
