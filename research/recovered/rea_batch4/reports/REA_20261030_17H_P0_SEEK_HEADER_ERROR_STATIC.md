# 迫真戦記 REA｜2026-10-30 17H｜Oggページreadのシーク/ヘッダ多段エラー契約
研究ID: `REA-LOCAL-20261030-17H-P0-OGG-SEEK-HEADER-ERROR-PATH-DIVERGENCE-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。ゲーム・Golden未実測。既存16Hのページ更新 `-128→-2→0` と重複計上しない。

## 新規P0静的発見
V9の直接E8 CALL（元EXEと照合）: `0x005D0CC1→0x005CEB90`、`0x005CF035/0x005CF17D/0x005CF2AA→0x005CEB90`。
シーク本体 `0x005D0B60` では `0x005D0CC1` の64bitページ取得戻り値を `0x005D0CC9 test edx,edx` → `0x005D0CCB jl 0x005D0D89` で判定する。
`-128`（callbackハードエラー）、`-2`（EOF）は共に上位32bitが `0xFFFFFFFF` のため、**両者とも同じ `0x005D0D89` の代替処理へ進む**。この地点では即時の負数returnではない。
代替入口では `fldz`、`[esi+0x68]` / `[esi+0x70]` への0.0書込、`0x005D0D95 call 0x005D48E0`、`0x005D0DAA call 0x005D1C50` 等へ続く。ただし最終return・対象音声の損失・状態復旧の成功は**未証明**。
さらに `0x005D0CAE/0x005D0CB0/0x005D0CB3` は直前エラーのうち `-3` を特別扱いしてページ取得へ進める。負数を一律終了にしてはならない。

## ヘッダ構築内の3つのページ読込地点の差異
| 読込CALL site | -128に対する局所挙動 | その他の負の64bit戻り値 |
|---|---|---|
| `0x005CF035`（既存16H） | `0x005CF03D/42` で比較して元の `EDX:EAX` を返す | `0x005CF058` で `-132` へ |
| `0x005CF17D`（今回） | `0x005CF185` / `0x005CF18A` / `0x005CF18D` で分離して `0x005CF216` の `-128` へ | `0x005CF193/195` で `0x005CF21D` の `-132` へ |
| `0x005CF2AA`（今回） | `0x005CF2B2` / `0x005CF2B4` でまとめて `0x005CF1E9` の `-133` へ | 同じ `-133` |
第3経路は `0x005CF206 mov eax,edi` を通じ結果を返し、`0x005CF20A` で `this+0x58` を2に戻す後処理へ接続する。初期化の段階ごとにエラーの外向きの値が異なる。
**実到達条件・後続cleanup全分岐・間接呼出・再生音への影響はVERIFY**。単なる原作実装癖候補として記録し、確定不具合とは宣言しない。

## 非重複・証拠範囲・保存
既存15H/16Hは`0x005CFA10`ページ更新によるエラー収束と`0x005CEB90`の下位原因を解析。今回は未監査だったシーク直接readerとヘッダ第2/3 readerの返却分岐を個別照合した。
出典: 同一SHA専用PE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。V9 SQLite quick_check PASS。
V9の**info/pseudo/callers/callees＋局所PE assembly**を比較したが、これらはREAが保存する正式5種関数別証拠の獲得ではない。
独立監査 **52/52 PASS（0.9008秒）**。既存正式STATIC VERIFIED **64/64**、新規正式VERIFIED **0**、新規5種証拠完備 **0**、TODO/VERIFY/BLOCKED正式差分 **0/0/0**。原作Golden **0**、完全複製率は未測定。
PC接続正常、owner `active.lock` 不在。Java/Ghidra/REA競合プロセス未検出、空き物理RAM約 **14.71GiB**（確認時）、CPU負荷・総作業時間不明。新規REA/Ghidra/ゲーム起動なし。
保存先 `rea_lab/decomp_task/` の17H固有資料のみ。原本、MASTER、QUEUE、PROGRESS、既存RUN、他レーン、Git、公開先、スケジュールに変更なし。

## 次回再開・Golden条件
第一優先 `0x005D48E0`：`0x005D0D89` エラー後代替入口の構造と戻り値、`0x005D1C50/0x005D1C30` 連携を追跡する。次にヘッダ `0x005CF010` の `-128/-132/-133` が上位初期化APIにどう見えるか照合。
Golden設計：正常ページ、callback `-128`、EOF `-2`、読込上限 `-1`、破損ページ `-3` を、初期ヘッダ第1/2/3読込とシークの別条件として記録する。実ゲーム未実測のためPASS 0。
