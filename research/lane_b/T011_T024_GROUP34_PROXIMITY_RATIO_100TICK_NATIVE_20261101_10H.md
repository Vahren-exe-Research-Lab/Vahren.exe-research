> **B-OWNED PRIVATE RESEARCH INTAKE — PUBLISHED_INTAKE / NOT_CURATED / STATIC-VERIFY / NOT READY**. Historical local owner report recovered and SHA256-readback verified from the authorized PC on 2026-11-01 22H JST. This is a text-only sanitized copy, not original game assets or the curated KB. Duplicate-path mirrors carry the SAME research ID; count once.
>
> research_id: `B-OFFLINE-20261101-10H-T011-T024-GROUP34-PROXIMITY-GATE-01`; owner: B; tasks: T011,T024; local_source_relative: `data/T011_T024_GROUP34_PROXIMITY_RATIO_100TICK_NATIVE_20261101_10H.md`; **original local report SHA256: `6B99F9F4A10C2498386FB12F7924621CFA07F9D656D484235F96B2845AE9E247`** (GitHub sanitized copy intentionally hashes differently). Original EXE identifying SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (prior verified reference; not rehashed this hour). Golden PASS=0; strict MATCH=0; DYNAMIC=0; READY=0.
>
> The historical text below retains its historical `OFFLINE-UNSYNCED` label describing original evidence collection; this new GitHub staging does not retroactively change that observation. Private GitHub branch/readback is the new preservation state; curator reviews all semantics and source SHA separately.

# 迫真戦記 ver0.67｜新B T011/T024：group+0x34 の空間的近接判定への使用と100tick再評価（2026-11-01 10H JST）

**研究ID** `B-OFFLINE-20261101-10H-T011-T024-GROUP34-PROXIMITY-GATE-01`。**owner** B。**tasks** T011/T024（T013は最終対象選択への接続未証明につきVERIFYのみ）。**判定** `OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY`。原作ゲームの **Golden PASS=0 / strict MATCH=0 / DYNAMIC=0 / 正式READY=0**。

## 1. 接続・証拠源・未保存回収

最初に `Desktop Commander Local Compact` を使用して `[RESEARCH_ROOT]/MASTER_LEDGER.md`、`evidence\ANALYSIS_LANES_PROTOCOL.md`、`evidence\LANE_B_HANDOFF.md` の読み取りを試行したが、`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org` で失敗。**接続/レート制限**であり安全拒否ではない。今回はPCの現行MASTER、B所有資料、最新checkpoint/READY/重複、03Hタイムアウト書込みの実在・内容を確認できていない。03HのPC保存結果はUNKNOWN。04〜09Hの独立成果は研究PC未同期であり、今回の成果も同期していない。前回04〜09Hに作成した資料はChatGPT作業環境に残存するものを確認し、既存のSHA台帳20件/20件と照合済み。SAFE134は過去スナップショット継承のみで今回の全件監査ではない。安全HOLD21、10/25原文欠落、GitHub側B全量バックアップ不足は未解決。

独立静的証拠はChatGPT Libraryから取得した**原作EXE**（SHA-256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（SHA-256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、ZIP CRC34/34 PASS）、`HAKUSHIN_B_LANE_SAFE_RECOVERY_20261029_V3.zip`（SHA-256 `059B91381C1B58214353769006E0F4049FCDE393A6B7970F4513602878A2B2C9`、CRC136/136 PASS）、pack内 `search.sqlite`（SHA-256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、`PRAGMA quick_check=ok`）である。原作は**起動していない**。再Ghidra解析・原作バイナリへの書込みなし。

非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` から `README.md`、`SYNC_STATUS.md`、`symbols.tsv`、`structs.tsv`、`REF_BATTLE_AI_MORALE.md`、`GHIDRA_V9_B_REVIEW_TOP150.tsv`、`GHIDRA_V9_COVERAGE_REPORT.md`、`KNOWLEDGE_CURATION_PROTOCOL.md` を読取専用で照合。Git blob SHA: `symbols.tsv=3fcf2d436c21f3fc91791a91e75c9a800167ca4d`、`structs.tsv=d79f03b1dbac67012882b0cb691d6af479610a01`、`REF_BATTLE_AI_MORALE.md=83fb9b91a84e8190042802ed7af5666ca51f7f8c`。最新のPC研究全量を反映するミラーではない。今回の `0x569360` は前回09Hの `0x569280` の**消費先新規接続**であり09H計算式は再発見として数えない。04〜09H HANDOFF/pack内B復旧既知IDの確認範囲では同一研究IDなし。PC現行正本に対する完全な重複否定は保留。

## 2. 核心：group+0x34 は Unit群の近接判定閾値に使われる

関数入口 `VA 0x569360`（原作PEのE8入口実体、Ghidra `functions/0056/00569360.c`、ファイルSHA-256 `309A88BD46955E9873936F91AF03731C50156A1B2476FAAA18EEE9F5696AAF1C`）。グループを第1引数、比率doubleを第2引数として受け取る経路（**完全ABIはVERIFY**）。対象配列 `group+0xC..+0x10` の最初の条件適格Unitをアンカー候補として採用する。適格条件は `Unit+0x1867C==0 && Unit+0x1867E==0`。適格アンカーがなければ真を返す経路がある。

アンカーごとの近接許容半径の候補値は、通常の符号付き32bit非オーバーフロー範囲で `R = group+0x34 + 2 * anchorUnit+0x228`。ただしアンカーについて `Unit+0xB0==0 && Unit+0xA8==0 && Unit+0x1E530 < global[0x65BC5C]` が同時成立すると、`anchorUnit+0x228` 寄与は**0に抑制**。このオフセット値が本当のゲーム意味として射程・当たり判定幅かどうかはVERIFY。

原作ASM検査窓：`0x569392` と `0x56939B` の2つの `Unit+0x1867C/+0x1867E` 判定、`0x5693A4` の `+0xB0`、`0x5693B3` の `+0xA8`、`0x5693BC..0x5693C2` の `+0x1E530` と `global[0x65BC5C]`、`0x5693E7` の `Unit+0x228`、`0x5693ED/0x5693F2` の `group+0x34` と加算、`0x56940B/0x569414` の相手Unit生存条件、`0x56941D/0x569429/0x56942F/0x569435` の双方座標 `+0x220/+0x224`、`0x569443/0x569446/0x569449` の距離2乗、`0x569453 -> 0x5E3B70` の直接E8とFSQRT系列。

**アンカー以外の**同じく `+0x1867C==0 && +0x1867E==0` なUnitだけを数える。ユークリッド距離 `sqrt((x1-x2)^2+(y1-y2)^2)` が `R` 以下なら近接数を1加算する。比率 `nearby / eligibleOther` が第2引数double以上なら真、下回れば偽とする（通常の有限数）。** eligibleOtherが0件の場合は真を返す**。原作は浮動小数比較/NaN/整数オーバーフロー/座標の尺度が未確定のため厳密モデルはVERIFY。資料中の0件・1件・2件・3件の近接数例は**SYNTHETIC_ONLY**で実機Goldenではない。

**09Hとの重要なフィルタ差**：`0x569280` のgroup+0x34集計では `Unit+0x1867C` を主に除外したが、`0x569360` の近接比率は `Unit+0x1867C` と `Unit+0x1867E` の**両方**を条件とする。計算式と判定関数で「対象人数」を同じと決めつけない。

## 3. 呼び出し元で0.5を渡す＝半数以上の近接判定

`0x56AB20`（Ghidra `functions/0056/0056AB20.c`、SHA-256 `124E47F6664898EAC07375C89F0A082D0417191D88290B99638AFA83C051A0E3`）からの2個の直接CALL、`0x56ADC1 -> 0x569360` および `0x56AE85 -> 0x569360` を原作E8相対オフセットで独立照合。両者は `0x63B050` のdouble定数 `0.5` を引数として利用する。グループタイマー `group+0x3C` は `0x56AB6D` で加算され、主な対象分岐は `group+0x3C % 100 == 0`（ただし事前の group+0x1C、管理画面状態、他の事前ゲートで経路が省略される）。

`group+0x44==0` かつ近接判定が真なら新規再配置経路をスキップする分岐がある。`group+0x44!=0` の経路で判定が真なら `0x56ADE9 -> 0x569700` / `0x56AE77 -> 0x569730` の状態別後続処理が呼ばれ、`group+0x44` を0へ戻す。判定が偽なら `0x56AE92` 側の分岐へ進む。**従って「半数以上が近接しているか」が集団更新判断に使われる静的経路があるが、実際の移動指示や戦闘AI全体の出力は未確定。**

同じグループ数値 `+0x34` は `0x528DB0` の命令窓 `0x5290A7` と `0x5290DD` にも出現し、条件によって**異なる集計器**へ寄与する。単なる描画用数値と断定できない。二つの集計器の意味はVERIFY。

## 4. group+0x1D初期化と100tickの初期位相

初期化関数 `0x568080`（Ghidra `functions/0056/00568080.c`、SHA-256 `CB626F94AD9C0DC6226D9D08E0624ACB4E74082397FED7EA6C9C71FE945DFFA7`）の `0x5680BE` は機械語 `C7 46 1C 00 01 00 00`。32bit little-endianで `DWORD [group+0x1C] = 0x00000100`、従って**初期値は `+0x1C=0, +0x1D=1, +0x1E=0, +0x1F=0`**。`0x5680CF` と `0x5680D2` は `group+0x34` および `group+0x30` のゼロ初期化。これは09H以前に未解決だった `group+0x1D` の**初期設定元**を追加した事実である。他のsetter/clearerは未網羅。

`0x5680E9 -> 0x5B6EAB` はrand呼出、スケールdouble `0x63B080=1/32768`、`0x63B060=100` の近傍計算、`0x568102 -> 0x5D1B80` は整数変換、`0x568109` は `group+0x3C` に結果保存。`group+0x3C` は乱数に基づく**0..100付近の初期位相**であり、複数グループの `%100` 再評価をずらす意図の可能性がある。個々の整数範囲、x87丸め設定、RNGコール順序、100tickの実時間換算はVERIFY。

## 5. 訂正と実機Goldenに必要な観測

誤用を避けるため、前回09Hの `group+0x34` を「士気」「攻撃力」と断定しない。今回は**近接比率の距離閾値として使う**根拠を得たが、+0x228や+0x34のゲーム内名称はまだ未承認。グループ `+0x1C/+0x1D/+0x1E/+0x30/+0x34/+0x3C/+0x44` を別フィールドとして扱う。`+0x1867C` の喪失・退場意味論、`+0x1867E` の別状態意味論、最終攻撃対象、敗走条件、実移動完了はVERIFY/NOT READY。

Golden前提：同一の原作 `Vahren.exe`・DAT・SAVE・MAP・入力・RNGシードと元スレッド/イベント時系列を記録し、tick前後の `group+0x1D/+0x1C/+0x1E/+0x30/+0x34/+0x3C/+0x44`、Unitオフセット `+0x1867C/+0x1867E/+0x220/+0x224/+0x228/+0xA8/+0xB0/+0x1E530`、`global[0x65BC5C]`、グループ内0・1・2・3・4名、eligibleOther 0/1/2/3、境界ちょうど半数/半数未満、境界距離R、+0x44両値を測定し、`0x569360` の返り値と後続 `0x569700/0x569730` の実際の次ティック状態を照合すること。これがない限り**Golden PASS0・strict MATCH0**を保持。

## 6. 実行した検証／保存とKB_CANDIDATE

読取専用検査 `data/B_20261101_10H_GROUP34_PROXIMITY_READONLY_VERIFY.py` → `data/B_OFFLINE_20261101_10H_GROUP34_PROXIMITY_EVIDENCE.json`。対象PEの39命令窓、7直接E8、4 double、5擬似Cを含む**合計62/62件PASS**。テスト数は証拠検査であり実機Golden数ではない。一次出典として `functions/0056/00569360.c`、`functions/0056/0056AB20.c`、`functions/0056/00568080.c`、`functions/0056/00569280.c`、`functions/0052/00528DB0.c` の相対パスおよび証拠JSON内の各SHA/VAを保存する。既存の禁止VA `0x5710C0..0x571500`、その他既拒否操作への直接・迂回アクセスはしない。

**KB_CANDIDATE（自動確定禁止）**：研究ID `B-OFFLINE-20261101-10H-T011-T024-GROUP34-PROXIMITY-GATE-01` / B owner / T011・T024 / VA `0x569360`, `0x56AB20`, `0x568080`, `0x528DB0`; CALL sites `0x56ADC1`, `0x56AE85`, `0x569453`, `0x5680E9`, `0x568102`, `0x56ADE9`, `0x56AE77`; group `+0x1C/+0x1D/+0x1E/+0x30/+0x34/+0x3C/+0x44`、Unit `+0x1867C/+0x1867E/+0x220/+0x224/+0x228`、global `0x65BC5C`。一次ソース/Line/SHA: Ghidra擬似C上記ファイル全体（各SHAは証拠JSONに保存）/EXE VAおよび実バイト（各命令SHAは証拠JSONに保存）。**STATIC**はbytes/E8/オフセット・定数、**INFERRED**は距離比/行動の説明、**VERIFY**は符号・FPU・実ゲーム条件・対象選択・Golden、**NOT READY**。統合専任だけが共有knowledgeへ反映。A-E/REA担当・MASTER・Git・原本への直接変更なし。

**PC復帰時の必須再開順**：PC正本MASTER/権限/安全HOLD/担当HANDOFF/既存ID重複・競合を読取→03H書込の存在・同一性・SHAを確認→04〜10HのOFFLINE資料のSHAと最新研究IDを照合して一度だけB許可資料へ取り込む（衝突なら上書きせず調査）、保存readback→KB専任へ候補渡し。PC不通ならまず `0x569360` の他の正規CALL・`group+0x1D` setter/clearer、`0x528DB0` 二つのsink、AIの優先順位・最終対象への接続を追加調査。T011の召喚経験値、T012のダメージ・回復・状態、T013の最終対象、T024戦闘AI、T028士気・敗走P0は未解決のまま保持。