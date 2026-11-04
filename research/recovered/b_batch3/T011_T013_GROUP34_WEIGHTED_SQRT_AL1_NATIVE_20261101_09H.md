# 迫真戦記 原作ver0.67｜B担当 T011/T013：グループ+0x34集計とAL=1登録条件（2026-11-01 09H JST）

研究ID：`B-OFFLINE-20261101-09H-T011-T013-GROUP34-WEIGHTED-SQRT-01`。担当B、T011/T013。T028との関連は**未証明**。状態 `OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY`。原作実機Golden PASS=0、strict MATCH=0、新規READY=0。

## 証拠源、保全、重複

Desktop Commander Local Compactの最初の正本参照は `UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org` により失敗。接続/レート制限であり、安全拒否ではない。したがって今回のPC上MASTER、LANE_B_HANDOFF、最新READY/Task Queue、03Hタイムアウト書込の存在・同一性は未確認。03H未確定と04～08H未同期成果は引き続き回収優先。SAFE134は10/31の過去スナップショットを継承し今回全件再照合なし、HOLD21・10/25原文未回収・B GitHub保全不足は未解決。禁止VAと拒否済み操作に再アクセスしていない。

ChatGPT Libraryで得た読取専用の原作`Vahren.exe`のSHA-256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（CRC34/34）、`HAKUSHIN_B_LANE_SAFE_RECOVERY_20261029_V3(4).zip`（CRC136/136）、pack内`search.sqlite`（SQLite quick_check=ok）を使用。原作を起動せず、Ghidra全体再解析をしない。

非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge`の`develop`からREADME/SYNC_STATUS/KNOWLEDGE_CURATION_PROTOCOL、`symbols.tsv`、`structs.tsv`、`REF_BATTLE_AI_MORALE.md`、V9横断レポートを**読取専用**で参照。`symbols.tsv`には対象の `0x569280` と `0x568FB0` の登録なし。GitHub全文検索の`0x569280`も該当なし。ただしGitHubはPC研究資料の完全鏡像ではなく、最新PCとの重複・競合を保証できない。08H研究ID `B-OFFLINE-20261101-08H-T011-T013-GROUP1E-CALLSITES-AL-POSTCALL-01` による `0x5695B0` の直接CALL25件とAL設定値分類は**既知**として非重複計上する。

## 新規静的検査：`0x569280` とグループ+0x34

原作実バイト `0x569280` より222バイトのSHA-256=`B3E227C031A013EC693F1AC2DBF6CF729DAE4F77FDDDD78CE352CA14BE6FA7FA`。対応Ghidra擬似C `functions/0056/00569280.c` SHA-256=`196E85C4BF1DDC4A4D10EFF87BCEFB422AD49B6E7E1262F9B3CFAFBEE6C50D74`。原作レジスタ上でEBXをグループポインタとして使うが、正式なC ABIは未確定。

- `0x56928C`で`group+0x34=0`に初期化し、メンバーポインタ配列 `group+0xC..+0x10` を巡回する。`Unit+0x1867C!=0`を除外し、生存扱いのUnit数を`n`とする。
- 対象Unitについて `Unit+0xB0==0 && Unit+0xA8==0 && Unit+0x1E530 < global[0x65BC5C]` の場合、そのUnitの集計寄与は0。それ以外は `2×signed32(Unit+0x228)` を加算する（`0x5692E3`読出、`0x5692ED`のLEAで二倍）。
- `n>0`では `0x56930D`の符号付き `IDIV n` によって合計を整数除算した `A=trunc(Σ寄与/n)` を得る。`n=0`なら`group+0x34=0`のまま戻る。整数オーバーフロー・不正な配列、負値の全ケースは未検証。
- `group+0x30==1` (`0x56930F`) の枝では、`group+0x38`を読み込み、`0x56931A`の符号付き比較と`0x56931C`のJGEで、**通常の非負数範囲では** `group+0x34=A×min(n,group+0x38)` とする。
- `group+0x30!=1`では、E8 `0x56933A→0x5E3B70`（内部 `0x5E3BAC` FSQRT）、E8 `0x569345→0x5B6ED0`（Ghidra擬似Cではceil系列）、E8 `0x56934D→0x5D1B80`（浮動小数→整数）を経て`0x569352`で積、`0x569355`で保存する。したがって通常の正有限数では `group+0x34≈A×ceil(sqrt(n))` と**推定**。FPU制御語、端数処理、負値、例外・オーバーフローはVERIFY。特にこの経路をRNG呼び出しとみなしてはいけない。

この+0x34は「グループ集計値」の静的証拠であり、士気、HP、攻撃力等のゲーム内意味は未特定。

## `0x568FB0` からの呼出と初期化ゲート

`0x568FB6`は`group+0x1D`を検査。0の場合は主要メンバー後処理と`0x569280`の呼び出しを迂回する。非ゼロの経路では各メンバー `Unit+0x1867D` を0にし、生存Unitの再評価を通した後、`0x569027`でグループ内ポインタ配列のendをbeginに合わせ、`0x56902C`から `0x569280` をCALL。したがって**同一初期化実行内で配列が空のままなら**`group+0x34`は0になる。一方、再入や他副作用はVERIFY。`group+0x1C/+0x1D/+0x1E/+0x30/+0x34/+0x38`は混同しない。

## 既存AL=1分類に対する新規条件分析

- `0x5282C0`では`group+0x1C==0` (`0x5282C5`) と先頭Unit `+0x1FA==0` (`0x5282DA`) が条件。`manager+0x348`のリンク集合で同一グループの既登録を避け、`0x528304→0x5299E0`の後 `0x52830A mov al,1`、`0x52830C→0x5695B0`、`0x528312→0x529B60`へ進む。空配列ならローカル分岐 `0x5282D4 xor eax,eax` の後 `0x5282DA cmp byte [eax+0x1FA],0` になるよう静的に見えるため、**空配列の呼出前提・上位保証はVERIFY**。実機クラッシュとは主張しない。
- `0x5284A0`では入力Unitが非NULLで `Unit+0x8C==0`、`Unit+0x1F8!=0`、`Unit+0x1867C==0`、`Unit+0x1D0!=0`、`Unit+0x1867E==0`、`Unit+0x1FA==0` の条件で `0x5284E2→0x568710` の後 `0x5284E8 mov al,1`、`0x5284EA→0x5695B0` に進む。ALL25件AL分類の重複再計上ではなく、**この2経路の条件列**を新しい証拠とする。

## 検証・範囲・Golden受入条件

`data/B_20261101_09H_GROUP34_WEIGHTED_SQRT_NATIVE_READONLY_VERIFY.py` は原作/pack/検索SQLite/既存復旧ZIPのみ読取。`data/B_OFFLINE_20261101_09H_GROUP34_WEIGHTED_SQRT_EVIDENCE.json` に独立ASM窓・E8相対CALL・8擬似C・各SHAと**58/58 PASS**を保存。注：機械語一致はSTATICのみで意味論やGoldenの証拠ではない。

Goldenには同一原作EXE/DAT/SAVE/MAP/入力/RNGから実ゲームで`n=0,1,2,3,4,5`、`group+0x30`が1/非1、`group+0x38`がn未満/同値/超過、Unitフィールド`+0xA8/+0xB0/+0x1E530/+0x228`の分岐、`group+0x1D`の0/非0、AL=1登録の重複・空グループ、実際の観測値と次ティックの一致が必要。現状Golden0/strict0、正式READY0。

## KB_CANDIDATE（統合専任への未確定依頼）

`B-OFFLINE-20261101-09H-T011-T013-GROUP34-WEIGHTED-SQRT-01` / owner B / T011,T013 / VA `0x569280`,`0x568FB0`,`0x5282C0`,`0x5284A0` / CALL sites `0x56902C`,`0x56933A`,`0x569345`,`0x56934D`,`0x52830C`,`0x5284EA` / group offsets `+0x1C/+0x1D/+0x1E/+0x30/+0x34/+0x38` / Unit offsets 上記 / source PE SHA, pseudo SHA 上記・機械可読検証JSON / STATIC, INFERRED, VERIFY / NOT READY。現時点で正式なsymbols.tsvや共有KBへ自動登録しない。

## P0・次回再開点

(1) PC復帰時、03H研究詳細の存在/SHAと04～09Hの未同期成果・最新MASTER/owner/重複/READYを先に確認し、承認されたBファイルへ一度だけ反映する。(2) `group+0x34`を読む消費側の関数を検索しゲーム意味を絞る。(3) `group+0x1D`の実所有書き込み元の特定（単純テキスト一致は他構造体を混同）。(4) `0x5282C0/0x5284A0`の上流で空グループ不変条件と成功/失敗を検証。(5) T011召喚EXP、T012ダメージ/状態、T013最終対象、T024通常戦闘AI、T028敗走は引き続きP0。既存拒否21件の迂回禁止、MASTER/Git/他lane/原本/設定/スケジュールの変更なし。
