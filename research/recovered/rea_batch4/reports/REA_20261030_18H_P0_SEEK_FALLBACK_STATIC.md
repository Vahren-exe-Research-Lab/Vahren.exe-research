# 迫真戦記 REA｜2026-10-30 18H｜Oggシーク代替経路のhelper実体と戻り値
研究ID：`REA-LOCAL-20261030-18H-P0-OGG-SEEK-FALLBACK-HELPER-AND-RETURN-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。旧17Hを非重複照合。原作Golden実測0、完全複製率未測定。

## 新規P0静的成果
- **0x005D48E0は状態復旧関数ではない。** 17-byteのread-only getterで、`0x005D48E6 mov ecx,[eax+0x1c]`→`0x005D48E9 mov eax,[ecx+0xe48]`→`0x005D48F0 ret`。呼出 `0x005D0D95` の戻りEAXは `0x005D0D9D mov ebx,eax` からshift countへ受け渡される。17Hの「復旧関連」としていた意味づけを**「位置換算用shift値取得」に修正**する。フィールドの厳密な単位はVERIFY。
- **0x005D0D89は単純なエラーreturnでもhelperによる状態resetでもなく、共通のシーク位置調整経路。** `fldz`、`0x005D0D8E fst qword ptr [esi+0x68]`、`0x005D0D92 fstp qword ptr [esi+0x70]` により二つのdoubleを0.0へする。続いて `0x005D0DAA→__allshr(0x005D1C50)`、`0x005D0DB1→__allshl(0x005D1C30)` で64bitの位置/フレーム換算を行う。
- `0x005D0DF6→0x005D5730` の残量取得、`0x005D0E17→0x005D5790` の消費、`0x005D0E43→0x005CFA10` のページ更新を経由。ページ更新が正数なら次に進み、0以下なら `0x005D0E52→0x005CFF10` で取得した64bit長を `[esi+0x50:+0x54]` へ直接代入する。`0x005D0E63/74` は到達目標に満たなければ戻り、目標に達すれば `0x005D0E7A xor eax,eax`→`0x005D0E82 ret`。
- **前回17Hの-128 / -2が同一入口に流れる発見は維持**するが、戻り値0で終わるにはループが目標へ到達する必要がある。失敗時に必ず成功応答・再生復旧するとまでは言えない。`0x005CFF10` の状態不正時-131と値未検査代入は既存14H成果を確認しただけで新規計上しない。
- 未確定：ページ更新0/負数の実到達条件、負の総長による再試行継続/停止、shift値の正当範囲、間接呼出、ゲーム上の音声結果。無限ループ/音切れ/原作バグとは断定しない。

## 証拠・監査・安全
- 出典：同一SHA専用PE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` と統合V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、V9 SQLite quick_check=ok。
- 関数：`0x005D0B60`、`0x005D48E0`、`0x005D1C50`、`0x005D1C30`、`0x005CFF10`。E8 CALL site: `0x005D0D95`、`0x005D0DAA`、`0x005D0DB1`、`0x005D0DE3`、`0x005D0E17`、`0x005D0E43`、`0x005D0E52`。V9 info/pseudo/callers/calleesと専用PE局所assemblyを独立突合したが、**正式REAの関数別5種証拠取得ではない**。
- 独立静的監査：**49/49 PASS**（0.8634秒）。17H readback 27/27と保存済み正式64/64の既存syncを先に照合。新規正式VERIFIED 0、新規正式5種完備0、正式TODO/VERIFY/BLOCKED変更0/0/0。
- PC接続正常、preflight時 `active.lock` 不在、Java/Ghidra競合プロセス表示なし。空きRAM約14.34GiB、CPU負荷と総所要時間は不明。新規Ghidra/REA解析、ゲーム起動なし。
- 保存先 `rea_lab/decomp_task/` の18H固有ファイルのみ。MASTER、QUEUE、PROGRESS、既存RUN、原本、A〜E、Git、公開先、スケジュールは無変更。

## 再開位置
まず `0x005CFF10` の-131が、シーク復旧ループのどの状態遷移で保持/解消されるかを `0x005CFA10` との結合条件から確認。続いて上位初期化 `0x00502020` のエラー分岐へ前回16/17Hの -128/-132/-133 を接続する。
Golden案はEOF(-2)、hard-error(-128)、総長失敗(-131)、正常ページでシーク位置/戻り値/終了性を比較。**全条件未実測**。
