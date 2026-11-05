# DAT 汎用 UI v3 の呼び出し仕様（Claude 2026-10-28、FINDINGS §88）

候補の数（1〜49）と数値列（0〜4）を DAT から自由に決められる汎用選択 UI です。
plugin がない、または plugin が要求を拒否したときは、原作の choice が同じ候補で動きます（fallback）。
v1/v2 と同じ変数名と同じ手順を使い、v1/v2 の固定 ID・固定ラベルの制限をなくしています。

## 1. DAT 側で用意するもの（`hk_ui_select_v3` を呼ぶ前）
| 変数 | 種類 | 内容 | 必須 |
|---|---|---|---|
| `@hk_ui_candidates` | 文字列リスト | 候補の ID。N 個（1〜49）、重複なし | 必須 |
| `@hk_ui_label0` 〜 `@hk_ui_label{N-1}` | 文字列（要素 1 個） | 画面に出す名前。原作の choice にも同じ文字が出る | 必須 |
| `hk_ui_count` | 数値 | N（候補リストの長さと一致しなければ拒否） | 必須 |
| `@hk_ui_columns` | 文字列リスト | 数値列の見出し。0〜4 個 | 任意 |
| `@hk_ui_values` | 文字列リスト | 数値変数の**名前**を、行優先で N×列数 個（行 0 の列 0, 列 1…, 行 1…） | 列が 1 個以上なら必須。列が 0 なら空 |
| `hk_ui_index` | 数値 | -1 にしておく | 必須 |
| `hk_ui_status`, `hk_ui_backend`, `hk_ui_after` | 数値 | 0 にしておく | 必須 |
| `hk_ui_before` | 数値 | 0 にしてから `add(hk_ui_before,1)` で 1 にする | 必須 |

- ID・名前・見出し・変数名は 1〜64 バイト（CP932）。`&` と制御文字は使えない（原作の choice が `&` を展開するため）。
- `@hk_ui_values` に書く変数名は互いに重複させず、`hk_ui_index` などの出力用の変数名も使えない。
- 呼び出し: `routine(hk_ui_select_v3)`。`hk_ui_select_v3` は `claude_gen_choice_wrapper_v3.py` で生成した event を DAT に置く。

## 2. 結果
| 変数 | 意味 |
|---|---|
| `hk_ui_index` | 選んだ候補の番号（`@hk_ui_candidates` の順で 0 から）。Cancel のときは N |
| `hk_ui_status` | 1＝決定、2＝Cancel、3＝エラー（wrapper が choice の後に計算） |
| `hk_ui_backend` | 1＝plugin の画面で選んだ、0＝原作の choice で選んだ |
| `hk_ui_after` | wrapper の最後に 1 増える |

plugin の画面で「キャンセル」（Esc・右クリックでも可）を押したときは、何も書かずに plugin の画面だけが閉じ、原作の choice がそのまま待ちます（v1/v2 と同じ）。

## 3. plugin 側の検証（`work_dat_ui_v3.h`）
1. `routine(hk_ui_select_v3)` を予約名として認識する（`work_dat_ui_literal_v3.diff`）。
2. `wdu3_capture`: 文字列マップと数値マップを、上限付きで 2 回読み、バイト単位で一致することを確かめる。件数・重複・長さ・`&`・出力用変数との衝突・レコードのアドレスの重複・`hk_ui_count`==N を確認する。
3. `wdu3_phase_ready`: index=-1、status=0、backend=0、before=1、after=0。
4. `wdu3_bind`: 原作の ChoiceWnd が表示中であること、owner+4 が同じ VM、件数 N+1、結果変数 `hk_ui_index`、ラベル 0..N-1 が wrapper の文字列 `&@hk_ui_label<i>&` で最後が `Cancel`、close スロットが期待値、`hk_ui_index` のレコードが snapshot と同じで値も同じ。2 回読んで一致すること。
5. `wdu3_commit_plan`: 書くのは `hk_ui_index`＝行番号、`hk_ui_backend`＝1 の 2 つだけ。その後、寿命ゲート経由で原作の close を 1 回呼ぶ（v1/v2 と同じ）。

## 4. 未確認（ACTUAL が必要）
- choice の引数に書いた `&@hk_ui_label0&` が、字句解析で `&` を残したまま保存され、描画時に文字列変数 `hk_ui_label0` に展開されるか（§85 の静的根拠だけ）。違っていた場合は `wdu3_native_label()` の 1 か所と生成器だけを直す。ワイルドカードで受け入れてはいけない。
- 49 分岐の wrapper の解析時間と、各 choice の yield と再開。
- `clear(@リスト)` を、まだ存在しないリストに使ったときの動き。
- 原作での実測は 0。Golden/MATCH は 0 のまま。
