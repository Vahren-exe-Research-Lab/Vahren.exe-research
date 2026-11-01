# 通常セーブ解析の道具（2026-11-01 Claude）

結果は `REF_SAVE_FORMAT.md`（知識ベース直下、出典 S1101）。この中身はその再現用の道具だけで、セーブファイル・復号した平文・解析の出力（out/）は入れていない。

## 中身
- `pkg/hakushin_compat/` … 研究PCの `dev_lab/src/hakushin_compat` から必要な 15 本だけを写したもの（2026-11-01 時点）。`__init__.py` は空。
  - `normal_save_body_and_tail.py`（今回追加）… 本体を世界地図グラフの終わりで止め、後ろの古い残りを `stale_tail` として返す。本体は保存鍵で暗号化し直し、ファイル先頭と 1 バイトまで一致することを確かめる。
- `tools/`
  - `run_body_tail.py` … save1〜3・auto を読み、本体の長さ・見出し・件数を `out/body_tail_summary.json` に出す。
  - `tail_segments.py` → `tail_generations.py` → `tail_late_generations.py` … 古い残りを鍵ごとの区間に分け、古いセーブを読めるところまで読む。
  - `field_stats.py`・`relation_checks.py`・`findings_vs_save.py` … 項目ごとの値の分布と、FINDINGS の意味との照合。
  - `verify_ref.py` … REF に書いた数値の再計算と、セーブが変わっていないことの確認。
  - `asmgrep.py`・`pseudo_grep.py`・`findings_offsets.py`・`kb_lookup.py`・`list_deps.py` … 研究PCの保存済み機械語・疑似コード・FINDINGS・辞書を読むだけの補助（研究ルートの資料が要る）。

## 使い方
- 研究PCでは `dev_lab/_work/save_20261101/` に同じ配置で置いてあり、そのまま動く。
- 別の場所では、セーブのフォルダを環境変数 `HAKUSHIN_SAVE_DIR` で指定する（save1.sav・save2.sav・save3.sav・auto.sav を読み取りだけで開く）。`tools/` から `python -B run_body_tail.py` の順に実行すると `../out/` に結果ができる。
- 原作のセーブは読み取りだけ。配布しない。
