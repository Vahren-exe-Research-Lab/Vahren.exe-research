# 迫真戦記 REA｜2026-10-30 14H｜Vorbis seek フォールバックと32bitシフト監査
研究ID: `REA-LOCAL-20261030-14H-P0-VORBIS-SEEK-ROLLBACK-SHIFT-STATIC-01`。
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作Golden実測PASS=0、完全複製率未測定。

## 今回の独立確認と非重複
13Hは`0x005D0E17`の第2フレーム消費呼出と安定時のmin条件を確認済み。今回はその後の**整数幅・失敗時のシーク位置代入**のみ新規監査し、13Hの発見を二重計上しない。
`0x005D0E1F`: `mov eax,edi`、`0x005D0E21`: `shl eax,cl`、`0x005D0E26`: `cdq`、`0x005D0E27/2C`: 64bit位置のlow/highに`add/adc`。シフト後の32bit符号を64bitに拡張する。
合成数値例: frame数`0x20000000`・shift=2なら数学的バイト加算は+2147483648だが、機械語の差分は**-2147483648**。小さい4096フレーム・shift=2では正しく+16384。
**上記の巨大フレーム値が通常のVorbisバッファに現れる証拠はなく、原作バグと断定しない。**
`0x005D0E43`のページ更新戻り値が0以下の場合、`0x005D0E52`で`0x005CFF10(this,-1)`の64bit戻り値を呼び、`0x005D0E5A/5D`で無条件に位置フィールド`+0x50/+0x54`に格納する。
`0x005CFF10`は状態`+0x58<2`、またはリンクソース無効時などに、`EAX=0xFFFFFF7D / EDX=0xFFFFFFFF`（-131）を返すことを局所機械語で確認。
**ページ更新失敗と総長取得失敗が同時に成立する仮想状態**では、位置=-131が格納され、`0x005D0E63/66`のsigned-high比較から非負ターゲットへの後退分岐が可能。無限ループ・実ゲーム再現は未証明。

## 根拠、判定、保存境界
使用出典: 研究用EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、統合V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
V9は非破壊独立verify PASS、旧REA syncで正式64/64維持。対象のV9 info/pseudo/callers/callees＋局所PE ASMは正式REAの5種別証拠ではない。新規正式VERIFIED=0、正式5種完備=0、正式TODO/VERIFY/BLOCKED差分=0/0/0。
静的監査**50/50 PASS**（0.8585秒）、数学的合成ケース7組。開始時active.lockなし、PC接続正常、開始確認時空きRAM約15.84GiB。CPU負荷・全作業時間不明。
専用owner `rea_lab/decomp_task/` の新規14Hファイルだけを保存。原本/MASTER/QUEUE/PROGRESS/既存RUN/他レーン/Git/スケジュールは無変更。REA/Ghidra新規解析・原作ゲーム実行なし。
未確認: `0x005CFA10`のEOF/異常状態遷移、`0x005CFF10`の通常有効性、`0x005D0E90`の呼出時間範囲、シフト上限到達可能性。
次回再開: **`0x005CFA10`の失敗種別**、`0x005D0E90`の時間境界とloop終了、`0x005CFF10`が返す正規の総バイト長を優先して呼出xrefs/ASM/ABIを照合。
