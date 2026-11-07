# 迫真戦記 REA｜2026-10-30 13H｜Vorbisシーク系の第2フレーム消費経路
研究ID: `REA-LOCAL-20261030-13H-P0-VORBIS-SEEK-SECOND-COMMIT-INVARIANT-STATIC-01`。
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作Golden実測PASS=0、完全複製率未測定。

## 新規範囲と非重複
11Hの`0x005D5790`未検査戻り値、12Hの`0x005D0FB0`通常PCM復号側の不変条件は既知として二重計上しない。今回は**もう一方の呼出元`0x005D0B60`**を独立検証した。
統合V9で`0x005D5790`への直接CALLは`0x005D128D`と`0x005D0E17`の2箇所。後者の親は`0x005D0B60`。
`0x005D0DF6`で`0x005D5730`から残フレーム数を取得。 `0x005D0DFB`でEDIへ、`0x005D0E01..0x005D0E0C`で符号付き上位32bit＋下位unsignedの比較により要求フレーム数との小さい方をEDIに採る。
`0x005D0E17`は選択したEDIを`0x005D5790`へ渡す。直後`0x005D0E1C`は戻りEAXを判定せず他値を読み、`0x005D0E21..0x005D0E2C`でシーク位置を加算する。
有効な安定状態`0<=cursor<end<=INT_MAX`・正の要求・正しいshift計算なら、`take=min(end-cursor,wanted)`なので`cursor+take<=end`。合成10005件でこの算術条件を確認した。**失敗戻り値の未検査は事実だが、安定正常経路のガード失敗を意味しない**。
上位は`0x005D0E90`から`0x005D0F5F`でこのヘルパーを呼ぶ。原作Oggラッパー`0x00501F10`の`0x00501FB7`と`0x00502000`の`0x00502015`から`0x005D0E90`へ入る2経路はいずれも`FLDZ`で0.0を渡す。通常PCM復号とは別の0位置へのシーク／リセット文脈として限定できる。
`0x005D0E43`は不足フレーム時に`0x005CFA10`でページ更新を試み、失敗側`0x005D0E52`で`0x005CFF10`を呼ぶ。これらの実際のEOF・回復結果は未実測。

## 出典・監査
EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
V9 DB SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
局所PE機械語＋V9関数・E8参照＋12H保存証拠の**46/46 PASS**、監査所要**0.9048秒**。新規正式REA 5種完備=0、VERIFIED=0、既存64/64維持、正式TODO/VERIFY/BLOCKED差分0/0/0。V9のinfo/pseudo/callers/calleesと局所PE ASMは正式REA5種ファイルではない。
PC接続正常、監査前active.lock不在、確認時空きRAM約14.99GiB。CPU負荷・全作業時間不明。新REA/Ghidra・ゲーム実行なし。
限界: ポインタ破損・同時状態変更・負数や巨大seek・32bit shift溢れは未検証。音声不具合確定・再実装READY・Golden PASSではない。
所有境界: `rea_lab/decomp_task/`のみ新規保存。原本、MASTER、QUEUE、PROGRESS、旧run、他レーン、Git、スケジュールは変更していない。
次回: `0x005D0E21/0x005D0E27`の32bit shiftと64bit加算境界、`0x005D0E43`のページ更新および`0x005D0E52`の復旧位置を解析。
