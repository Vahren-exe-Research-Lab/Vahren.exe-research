# 構造体事典（自動生成。元データは structs.tsv）

オフセットは構造体の先頭から。std::string は、文字列の本体（16 バイトの内部バッファまたはポインタ）が書いたオフセットにあり、+0x10 に長さ、+0x14 に容量がある。

## UnitDef

| オフセット | 型 | 名前 | 意味 | 確かさ | 出典 |
|---|---|---|---|---|---|
| `+0x1C` | str | `id` | ユニット ID（例: hide、a030+0）。定義表のキー | 静的確認 | C(§93: 0x585AD0 が参照) |
| `+0x74` | u8 | `isMaster` | マスター（君主）の印。1 なら解雇ボタンが出ない | 実機確認 | C(§93, x32dbg 0x55D98F) |
| `+0x78` | u8 | `isNeutralLeader` | 独立部隊（中立）のリーダーの印 | 静的確認 | F§26 |
| `+0x7A` | u8 | `isVassal` | 陪臣の印。1 なら「召上げ」ボタンが出る | 実機確認 | C(§93, x32dbg 0x55D98F) |
| `+0x84` | str | `roamSpot` | 放浪先のスポット名 | 静的確認 | F§26 |
| `+0xEC` | vec | `skills` | 技能リスト | 静的確認 | F§24 |
| `+0x158` | ptr | `friendSet` | friend 集合（遅延生成） | 静的確認 | F§30 |
| `+0x160` | u32 | `friendSetSize` | friend 集合の件数 | 静的確認 | F§30 |
| `+0x168` | i32x15 | `stats` | 能力値 15 個（level, hp, mp, attack, defense, magic, magdef, dext, speed, hprec, mprec, move ほか）。v4 一覧はここを読む | 実機確認 | F§91, W(dat_ui_v3_runtime.h) |
| `+0x1A4` | ptr | `ctx` | 所属する文脈（ctx = G+0x1B8）。v4 はこれが一致する def だけを使う | 実機確認 | F§91 |

## GameManager

| オフセット | 型 | 名前 | 意味 | 確かさ | 出典 |
|---|---|---|---|---|---|
| `+0x1B8` | struct | `ctx` | ユニット定義などを持つ文脈（ctx）。埋め込み | 実機確認 | F§91 |
| `+0x4C4` | map | `numVars` | DAT の数値変数の表 | 実機確認 | W(work_dat_ui_context.h), F§90 |
| `+0x504` | struct | `engine` | スクリプトエンジン E | 静的確認 | F§82 |
| `+0x1EF144` | i32 | `sceneId` | 場面番号（0=タイトル、4=シナリオ選択 …） | 静的確認 | W(dat_ui_selector_plugin.c) |
| `+0x1EF4EC` | u8 | `flag_1EF4EC` | 0 でなければ詳細パネル 1 組目のボタンを作らない（意味は未確認） | 静的確認 | 本セッション(0x55D70E) |

## Ctx

| オフセット | 型 | 名前 | 意味 | 確かさ | 出典 |
|---|---|---|---|---|---|
| `+0x2FC` | map | `unitDefs` | ユニット定義の表（std::map、キーはユニット ID） | 実機確認 | F§91 |
| `+0x300` | ptr | `unitDefs_head` | unitDefs の先頭ノード | 実機確認 | F§91 |
| `+0x304` | u32 | `unitDefs_size` | unitDefs の件数 | 実機確認 | F§91 |
| `+0x30C` | map | `varStore` | 変数ストア | 静的確認 | F§63.1 |
| `+0x32C` | set | `roamingSet` | 放浪中のユニットの集合 | 静的確認 | F§26 |

## Power

| オフセット | 型 | 名前 | 意味 | 確かさ | 出典 |
|---|---|---|---|---|---|
| `+0x1D` | u8 | `isPlayer` | プレイヤーが操作する勢力の印。1 のときだけ詳細パネルに雇用・解雇ボタンが出る（同盟国も 0） | 実機確認 | C(§93) |
| `+0x24` | str | `name` | 勢力の名前 | 静的確認 | F§32 |

## FrameWnd

| オフセット | 型 | 名前 | 意味 | 確かさ | 出典 |
|---|---|---|---|---|---|
| `+0x8` | i32 | `left` | ウィンドウの左端（TempStatusWnd で確認） | テストのみ | W(work_selector_*.h) |
| `+0x10` | i32 | `right` | ウィンドウの右端 | テストのみ | W(work_selector_*.h) |
| `+0x84` | u8 | `shown` | 表示中の印（WarWnd+0x84 = 0x8BA5BC、TempStatusWnd+0x84 = 0x8BCDCC） | 実機確認 | C(§93), W |
| `+0xA4` | u32 | `state` | 状態。通常は 0x80000008 | 実機確認 | C(§93) |
| `+0xBC` | str | `name` | ウィンドウの名前（WarWnd は 'war'） | 静的確認 | C(§93) |

## StatusWnd

| オフセット | 型 | 名前 | 意味 | 確かさ | 出典 |
|---|---|---|---|---|---|
| `+0x98` | ptr | `owner` | 表示の所有者。通常StatusWndと一覧TempStatusWndで同一、所有者+4はゲーム文脈。 | 実機確認 | W(DAT_UI_V4_STATUS_PANEL.md,2026-10-29) |
| `+0x9C` | ptr | `anchor` | 基準の相手（Player と比べている） | テストのみ | W(work_selector_hover_context.h) |
| `+0x1B8` | ptr | `targetDef` | 表示しているユニットの定義（g_StatusWnd では 0x67EB30、TempStatusWnd では 0x8BCF00） | 実機確認 | C(§93), W |
| `+0x1BC` | i32 | `pressedIndex` | 押されているボタンの番号（0=雇用/召上げ、1=解雇、2=アイテム、0x80000008=なし） | 静的確認 | F§95 |
| `+0x1C4` | u8 | `btnHire` | 「雇用」ボタンを作った印 | 実機確認 | C(§93) |
| `+0x1C5` | u8 | `btnExtract` | 「召上げ」ボタンを作った印 | 静的確認 | C(§93) |
| `+0x1C6` | u8 | `btnDismiss` | 「解雇」ボタンを作った印 | 実機確認 | C(§93) |
| `+0x1C7` | u8 | `btnItem` | 「アイテム」ボタンを作った印 | 静的確認 | C(§93) |
| `+0x1C8` | rect[] | `hoverRects` | 説明表示の対象の矩形（16 バイトずつ） | テストのみ | W(work_selector_skill_hover.h) |
| `+0x12F8` | u32 | `hoverCount` | 説明表示の対象の数 | テストのみ | W(work_selector_skill_hover.h) |

## Player

| オフセット | 型 | 名前 | 意味 | 確かさ | 出典 |
|---|---|---|---|---|---|
| `+0x324` | i32 | `cursorX` | マウスの X | 静的確認 | 本セッション |
| `+0x328` | i32 | `cursorY` | マウスの Y | 静的確認 | 本セッション |
| `+0x42C` | ptr | `hoverOwner` | 説明表示を受け持つウィンドウ | 静的確認 | 本セッション |

