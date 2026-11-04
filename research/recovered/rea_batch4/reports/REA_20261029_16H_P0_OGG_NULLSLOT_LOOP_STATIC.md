# 迫真戦記 REA｜2026-10-29 16H Ogg mapping0x0C 経路のNULLスロット到達条件
研究ID：`REA-LOCAL-20261029-16H-P0-OGG-NULLSLOT-LOOP-GATE-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。この回の新規REA正式5種=0、新規正式VERIFIED=0、原作ゲーム=NOT RUN。

## 事前照合・非重複
- PC Local接続正常。MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、15H既存EVIDENCEおよび有効syncを読取。QUEUE/PROGRESSは既知EPERMによりstaleであり、`logs/progress_sync_20261011T153958076Z.json`を正式64/64の根拠とした。
- 2026-10-29整理後の統合V9を正本として使用。旧search.sqlite/READMEは存在せず、復元・再取得は行わない。隔離PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、統合V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=okを監査。
- 15Hのmapping表+0x0C=`0x005DEDF0`、通常+0x10=`0x005DF7D0`、residue mode0の+0x14/+0x18=NULLは再照合に留め、**新規発見として二重計上しない**。

## 新しいP0証拠：mode0 NULL呼び出しを避ける局所分岐
- 関数 `0x005DEDF0` の `0x005DEE78 MOV EAX,[EDX+ECX*4+0x220]` はresidue側の処理用ポインタを取得し、`0x005DEE82 MOV [EBP-8],EAX` に保存する。Ghidra擬似Cでは `piVar7=*(int **)(iVar4+0x220+iVar6*4)` に相当。mode番号ではなく配列/グループ側のポインタである。
- `0x005DF640 MOV EAX,[EBP-8]`、`0x005DF643 XOR ECX,ECX`、`0x005DF64B CMP [EAX],ECX`、**`0x005DF64D JLE 0x005DF7A3`** は、このポインタ先頭のsigned countが0以下なら2つのNULLスロットCALLを含む内側のループをスキップする。
- 一方、count>0で上記のブロックに達すると、`0x005DF6F2` が各要素のmodeを `+0x520` から読み、`0x005DF6F9` でモード表を選択。`0x005DF703` は+0x14をロードして **`0x005DF717 CALL ECX`** を実行する。そのCALLが正常に返れば、`0x005DF769` は+0x18をロードして **`0x005DF788 CALL EDX`** へ進む。
- **`0x005DF673 JLE 0x005DF6EF` は内側のグループ収集処理を飛ばすだけで、上記CALLそのものを回避しない。** これは今回の新しい限定的な到達条件分析である。
## 判定の限界
- residue mode0表 `0x0061AE60` の+0x14および+0x18は両方0。したがって、`0x005DEDF0` の該当ループへ実際に入り、count>0かつmode0を選べば、最初のCALLはNULLへ向かう機械語配置になっている。ただし**mapping表+0x0Cを通ってこの関数へ入る上位CALLをまだ特定していない**。この条件がゲームで成立する、クラッシュする、と断定しない。
- 統合V9 CLI `callers 0x005DEDF0 --limit 12` は直接E8 CALLを0件と報告する。15Hまでのmapping表に対する既知3静的使用位置は+0x04/+0x08/+0x10であり+0x0Cではない。間接・alias・動的経路の不存在は未証明。
- `0x005D4160` のmode範囲検査は0・1・2を許容するので、mode0自体を不可能にする根拠ではない。`0x005DEDF0` が使う先頭countの実値・mode0との組合せ・上位mapping選択経路はVERIFY。元Ghidra擬似Cにはstack spacebase/unreachable block警告があり、単独ではABIを確定できない。

## 静的検証・保存境界・次回
- `REA_20261029_16H_P0_OGG_GUARD_PROBE.py` と `REA_20261029_16H_P0_OGG_SOURCE_POINTER_PROBE.py` は隔離PE読取のみ。監査 `REA_20261029_16H_P0_OGG_NULLSLOT_LOOP_AUDIT.py` は **39/39 PASS、1.045秒**、別JSON `REA_20261029_16H_P0_OGG_NULLSLOT_LOOP_EVIDENCE.json` に機械語と検証条件を保存。事前の一行PythonコマンドはWindows引用処理のSyntaxErrorで失敗（解析証拠に使用せず、専用probeで正常取得）。拒否ではなく引用方法の構文エラー。
- 5種の根拠：info=既存V9関数レコード、pseudo=既存V9未修正Ghidra、assembly=隔離PEの局所Capstone、callers=V9直接CALL0件/表XREF、callees=局所の間接CALL+テーブル32bit値。**新規REA正式5種取得0、正式VERIFIEDは64/64維持、正式TODO/VERIFY/BLOCKED差分0/0/0**。
- 原作ゲームGolden実測PASS=0、完全複製率=未測定。開始時空きRAM約16.37GiB（OS値）、CPU負荷・研究全体の所要時間=不明。REA/Ghidra新規実行なし、active.lockなし。
- 書込みはREA自身の新規PROBE/AUDIT/EVIDENCE/本報告と独立readbackのみ。MASTER、A〜E、T018、QUEUE/PROGRESS、旧RUN、隔離EXE、V9 DB、原本、Git、公開・スケジュールは変更しない。10/28未同期オフライン成果はこの回では統合せず保持。
- 次回優先：`0x0061AE40` 表の+0x0Cを取り出す未発見caller/alias、`0x005DEDF0` の先頭countを設定する `0x220` 配列の構築元、mode0におけるcountの実条件をread-only調査。保守的Golden fixtureは「mode0/先頭count>0/別mapping進入の有無」を独立3条件として扱う。
