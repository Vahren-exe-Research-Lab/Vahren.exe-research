# Wave4 契約テスト設計 — 旧EXE実機観測なし / NOT RUN

本書は `rea_lab/decomp_task` で保管する **新エンジン向けgolden比較計画**。T018本体や他レーン資料は編集しない。各テストの結果欄は原作観測=NOT RUN、新実装=NOT RUN、比較=NOT ESTABLISHEDとする。

| Fixture案 | 入力・事前条件 | 静的解析が示す注目契約 | 旧EXE動的観測で必ず記録する項目 |
|---|---|---|---|
| EV-ROOT-IF | `battleEvent` root `if(condition)`、false→true→true | trueでactive rootから除去、次tick以降再実行しない（T010既存native） | if条件評価tick、then実行回数、active rootのentry数、else実行有無 |
| EV-ROOT-RIF | 同一条件・root `rif(condition)`、false→true→true | trueでもroot残存し次tick再評価する（T010） | tickごとの条件・then回数・root残存 |
| EV-HISTORY | `event/call/routine`をworldとbattleの各sceneで実行 | `0x4321B0`はflagとbattle stateでqueue/history書込経路分岐 | `@evtend_name`読値、`yet(name)`、保存→再開後の履歴 |
| EV-NESTED | nested event→call→routine→returnとwait | execution stack群は複数、共通呼出は`0x4321B0`、waitはVM counter | 各関数entry/exit・queue depth・wait残tick・最終履歴 |
| SAVE-4GROUP | numeric map＋1Unit＋1Spot＋1Powerの最小状態を保存 | `0x460000` writer / `0x45E1E0` readerは4群を固定順で処理、各群空string terminator | 文字列/数値順、実ファイルbyte境界、group数、load後state |
| SAVE-EMPTY | 4群の一部を空集合とする | group境界はrecord countでなくempty string marker | 空group連続時のbyte境界とload移動位置 |
| SAVE-UNIT | 一つのUnitにHP/MP/7status・skills・arbeit・item_skillを設定 | `0x58EFD0` / `0x58E870` は逐次scalar/28byte-vectorとstringを扱う | 保存前後の値・vector順・engine再生後の差 |
| SAVE-CORRUPT | 末尾欠落、制御文字を含む候補値 | `0x470830` writerでASCII制御文字の扱いが単純コピーではない | 受入/拒否、エラー種別、正常化の有無（本家の安全なテスト環境でのみ） |
| AI-SEARCH-TICK | `unit_search_bdr=100`、同一seed、ターゲットあり/なし | Unit+0x1E534閾値未満は既存target再利用、到達時だけ再選択＋counter jitter | full scan tick列、reset値、乱数消費数、target ID |
| AI-PRIMARY-FALLBACK | SimpleUnitとSimpleStaticUnit候補を同時設置 | native primaryとfallbackは別pool、stealth gateはprimary側 | 候補除外順、distance比較、stealth RNG、最終target |
| AI-FORCED | target除去と強制counter満了 | `0x57B870`/T013のforced refreshは通常間隔と別 | 強制トリガーと次検索tick、cache更新 |
| RNG-SAVE-LOAD | save/load前後のseedとnumeric RNG output | save stateとCRT `srand(GetTickCount)` の寿命は別 (T031) | numeric map値、次のRNG出力、reseed発生時刻 |
| TIME-ABS-REL | battle進行→resetTime→isInterval(5)/getTime | resetTimeは相対elapsedのみ0、absolute tickは保持 (T010) | isInterval成立tick・getTime値・remaining limit |

## 合格判定の4レベル

- **SOURCE**: 対象ver0.67スクリプト/EXE保存済み静的証拠と入力fixtureが対応する。
- **TARGET**: 旧EXEで合法・安全な実際の操作と出力を観測し、seed、シーン、入力順序と出力をgolden化する。
- **MATCH**: 同条件の新エンジンで数値、順序、乱数消費、UI外部挙動を比較し一致する。
- **REGRESSION**: strict modeの全既存goldenが新改良後も一致する。

現時点では**SOURCEの一部だけ**。上記全fixture TARGET=NOT RUN、MATCH=NOT RUN、ゲーム完全互換率を数値化しない。過去に安全拒否されたEXE実行やREの操作は別shell/toolで迂回しない。

参照する保存済み証拠: `runs/20261009T225741694Z/`、`runs/20261009T224617297Z/`、既存 `data/T010_EVENT_SCHEDULER.md`、`data/T013_AI.md`、`data/T014_GLOBAL_SAVE.md`。根拠と仮説を分け、T018のE所有者が使う場合もread-only引用に限定する。

## 2026-10-10 09時台 — 既存REA証拠から追加した比較設計（TARGET未観測／NOT RUN）

| 設計ID | 対象 | 静的な検証条件 | 後で旧EXE実機から採取する観測 | 状態 |
|---|---|---|---|---|
| `SAVE-TAIL-ORDER-6` | T014 / `0x45E1E0` | four sentinel loop → `CALL 0x471AF0`@`0x45E53E` (外交) → `CALL 0x435550`@`0x45E54C` (Spot/Path graph)。先頭4groupと末尾2object sectionの区切りを混同しない。 | 一部空group・複数Power参照・複数SpotPathを含む正常savの保存/ロード後状態とセクションoffset。 | SOURCE/NOT RUN |
| `AI-CACHED-TARGET-THRESHOLD` | T013 / `0x57B870` | counter `<B`/`>=B` × cached target NULL/非NULLを分ける。`>=B`でもcached targetが非NULLならprimary helper `0x514D60`非呼出。 | target pointer、distance cache、primary候補探索呼出数、更新tick、RNG draw位置。 | SOURCE/NOT RUN |
| `AI-SUPPORT-INDEPENDENT` | T013 / `0x57B870` | `>=B`かつ `+0x137`非0なら、cached targetの有無と別にsecondary builder `0x514F10`へ到達可能。特定の状態ではsecondary builderの呼出経路が分岐する。 | +0x137、cached target、support候補list、各helper呼出列、行動結果、RNG消費。 | SOURCE/NOT RUN |
| `EVENT-WRITER-BRANCH` | T006/T014 / `0x4321B0` | battle-active `+0x1EEC44`と呼出flag `in_stack_0000002c`両方非0なら、この関数内のnumeric writer `0x4637A0`をskip。通常分岐は同siteを経由。 | event/call/routineごとのflag/scene/marker variable、保存前後の`yet()`値、frame depth。 | SOURCE/NOT RUN |

保存済み一次証拠は `runs/20261009T225741694Z` の3関数の info/pseudo/assembly/callers/callees。`data/T014_GLOBAL_SAVE.md`・`data/T013_AI.md`をread-only照合。実測のgolden PASSやstrictエンジンMATCHとは扱わない。過去に拒否された実行操作は再試行せず、旧EXEをこのREAタスクから起動しない。
