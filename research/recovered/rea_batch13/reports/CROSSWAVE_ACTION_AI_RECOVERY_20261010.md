# REA 横断解析：ノックバック後の行動・探索・自然回復の時系列（2026-10-10 10時台 JST）

状態：**保存済み静的証拠の横断比較／TRACE FIXTURE DESIGNED・NOT RUN**。新規Ghidra実行は0。原作実機golden PASS0・新エンジンMATCH0。
目的：戦闘Unitの更新処理にある「カウンタ加算」と「処理実行」を同一視しない。REAの既存W3/W4証拠とT012/T013 owner資料をread-only照合した検証設計。

## 使用した確定済み証拠
- W3 `0x57DF90` (T012, recovery): `runs/20261009T223622536Z/RUN_RESULT.json`、pseudo=`ev_5a3e17e1d68d81c9aa62213f2e77e5ca9d1c90c4e1fda186678a72e6a88684ce`、assembly=`ev_e50e0ad44fe14809a8e00c7e3754f2816f095b4d9686c6ba0d876d5ee0a337a1`。5種のGhidra結果は既にVERIFIED（今回の新規取得ではない）。
- W4 `0x57B870` (T013, target refresh): `runs/20261009T225741694Z/RUN_RESULT.json`、pseudo=`ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc`、assembly=`ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`。5種証拠は既にVERIFIED。
- 両runのsource SHAは `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。ゲーム実行なし。調査資料は `data/T012_BATTLE_CALC.md` §11/§26、`data/T013_AI.md` 冒頭／support／confusion各節。

## 保存nativeで確認済みの局所的契約
1. T012の2つのUnit update loopはaction counter `+0x1E530`をknock残時間 `+0x1E4E0` 分岐より前で加算する。knock中は通常action/recovery core `0x57DF90`へ進まない。**counter蓄積とrecovery実行は別**。
2. T013の同update系はsearch counter `+0x1E534`もknock分岐より前で増分する場合がある。ただしknock中にsearch core `0x57B870`を必ず呼ぶか、正常復帰初tickのaction/search両順序は全path未確定。
3. recovery core `0x57DF90`で `poi<0 && hprec>=0` はHP回復blockをskip、`sil<0 && mprec>=0` はMP回復blockをskip。負のhprec/mprecは各skip条件外。HP計算結果が負ならvfunc+0x70へのdeath-like分岐があり、MPは0下限へclamp。
4. T013/W4よりsearch counterが閾値に達しても**cached primary targetが非NULLなら`0x514D60`を呼ばない**。target NULL時はcall可能。support capability `+0x137`非0なら別の`0x514F10`へ進み得る。

## 新たに識別した横断リスク（HYPOTHESIS／実機未観測）
- ノック中にaction/search counterがともに進んだ場合、復帰直後にaction・recovery・search refreshが同一updateに密集する**可能性**がある。ただし実際のcall順、復帰時remainingゼロ判定、refresh実行可否は未確定。
- そのtickにpoi/sil負値とhprec/mprec正値が共存すれば、回復block skipも重なる。さらにcached targetがあれば「search threshold満了=新たな敵選択」とはならない。
- 「ノック中はaction counter停止」「search閾値到達で毎回primary再探索」「毒なら負hprecも停止」「沈黙なら負mprecも停止」の4種類の単純化はいずれも静的根拠と衝突する。
