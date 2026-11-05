# セーブ形式の知識ベース更新案（2026-11-01 Claude、出典 S1101）

本文: `dev_lab/docs/REF_SAVE_FORMAT_20261101.md`（出典ID S1101）。`new/REF_SAVE_FORMAT.md` は同じ内容の写し。
既存研究の誤りの一覧は本文 §9。

## 中身

| ファイル | 内容 |
|---|---|
| rows_symbols_add.tsv | 新しい 8 行（見出しの読み書き 0x4708D0・0x470550、0x45FD3E、0x45E5F0、0x4708A0、Unit/Spot/Power の読込 3 関数） |
| rows_symbols_replace.tsv | 既存 6 行の書き換え。0x471AF0/0x471D20 は名前も変える（Diplomacy → TurnState）。確かさは変えない |
| rows_structs_add.tsv | 新しい 64 行（UnitDef 24、Spot 10、Power 15、TurnState 5、GameManager 4、Ctx 6）。新しい構造体 TurnState を含む |
| rows_structs_replace.tsv | 既存 8 行の誤りの修正・補足: UnitDef+0x1C（DAT の unit タグ）、+0x74（プレイヤー本人）、+0x78（隊長）、+0x84（+0x94 が長さ）、+0x158（std::set 本体）、+0x168（+0x174 は所持金）、Power+0x24（盟主）、GameManager+0x1EF4EC（phase）。確かさは変えない |
| apply_rows.py | 行を差し込む。既定は試し（`new/` に結果を作るだけ） |
| new/ | 試しの結果（2026-11-01 時点の knowledge から作成）と REF の写し |

試しの結果: symbols 365→373 行、`check_symbols.py --compare` でエラー 0・警告 0。structs 42→106 行、確かさ・オフセットの形式と重複の検査で問題なし。
ApplyKnowledge.java で Ghidra に入れたとき欄が重ならないよう、str の長さ欄（+0x10）と i32x15 の範囲に入る位置（UnitDef+0x94、+0x174）は別の行にせず、既存行の説明に書いた。

## 確かさの引上げ候補（AI は変えない。人が出典を見て判断）

- 0x598CE0・0x596AA0・0x471AF0・0x471D20 は「推定」のまま。書出し・読込の順をすべて保存命令で確かめ、実セーブ 4 件で 1 バイトまで一致したので「静的確認」に上げてよいと考える。上げるときは `build_kb.py --accept-confidence-change`。

## 反映の手順（汎用一覧の反映 KB-DATUI-20261101 が終わった後）

1. ユーザー: `_REDEV_RESEARCH\knowledge` で `python -B tools/sync_knowledge.py start KB-SAVE-20261101`
2. Claude: `python -B dev_lab\_work\kb_save_20261101\apply_rows.py --apply`。書く前に大きさ・更新時刻・ハッシュを確かめ、書いた後に読み直して照合する。
3. `python -B knowledge\tools\build_kb.py --check` → `build_kb.py` → 既存テスト → `sync_knowledge.py checkpoint KB-SAVE-20261101` → `publish`。

## 注意

- `REF_SAVE_FORMAT.md` は `sync_knowledge.py` の許可リスト（FILES）に入っていないため、knowledge に置いても checkpoint されない。入れるには許可リストへの 1 行追加と `test_sync_knowledge.py` の確認が要る（ユーザー判断）。入れない場合は dev_lab/docs の本文を出典として使う。
- 実際のセーブファイル・復号した平文は、ここにも知識ベースにも置かない。
