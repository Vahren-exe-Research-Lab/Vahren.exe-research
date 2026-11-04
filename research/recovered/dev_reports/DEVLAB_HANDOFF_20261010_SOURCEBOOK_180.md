# 迫真戦記再開発 ソースコード化着手checkpoint（2026-10-10）

## 結論

- Ghidraの保存済み疑似コードを **39個の別々の .c ファイル**にまとめた。これはoriginal C++ではなく**非コンパイル可能なGhidra C風中間表現**。既存DEVLABのPython互換モデルは実行可能な新規ソースとして別に保持。
- 提出物: `dev_lab/recovered_source/INDEX.md` (Task別39関数一覧)、`ghidra_c_pseudocode/FUN_XXXXXXXX.c` (39)、`manifest.json` (5-method evidence IDs、code SHA、caller/callee)、`verified_call_graph.mmd` (39関数内の呼出グラフ)、`SOURCE_RECONSTRUCTION_ROADMAP.md` (Ghidra→独立再実装の対応表と優先順位)。
- 包装: `dev_lab/recovered_source_snapshot_20261010.zip` は上記＋`dev_lab/src/hakushin_compat/*.py` とテストと開発READMEをまとめた**ローカルのみ**のソースアーカイブ。ゲームEXE/アセット/実saveは含めない。Ghidra C疑似コード自体はビルドできない。

## 件数差分の原因と裏付け

- 最新REA `CURRENT_STATUS_20261010.md` の**39/48**は正しいが、14個の `rea_lab/decomp_task/runs/*/RUN_RESULT.json` だけでは`VERIFIED`の総数が**37**であり、初見で2件不足した。
- 差分2件は**最初期の別保存** `rea_lab/results/run_20261009T175957025Z_{550E70,576E30}_{info,pseudo,assembly,callers,callees}.json`に存在。`rea_lab/results/VALIDATED_EVIDENCE_20261010.json`はSOURCE_SHA一致、13/13 report presence、全ファイルJSON SHA256とevidence IDが既に検証済み。
- 新規`dev_lab/src/hakushin_compat/saved_ghidra_sourcebook.py`に2系統を統合。通常run37の1関数5-method checked/evidence ID/run SHA、初期2のファイル実SHAとvalidated manifestとinside evidence IDを独立検証。結果**39 unique VERIFIED**、duplicate0、欠陥のあるrun record5件はVERIFYのまま除外。
- initial 2＝`0x550E70` ダメージ計算（static body 1,566 bytes/81 basic blocks）、`0x576E30` 死亡系抵抗（static body72bytes/6 blocks）。静的5点証拠取得であって意味論や実機goldenの完了ではない。
- **新規Ghidra decompilation process 0件**。以前SAFETY_REFUSALとなったGhidra/REA起動を別shell/tool/path/Remoteで再試行していない。

## 自動テスト・開発への位置づけ

- `tests/test_saved_ghidra_sourcebook.py`5件：37+2=39、legacy SHA、全疑似コードSHAと関数入口、証拠ID、unknown invalid evidence拒否、ソース実ファイルの完全性。
- `tests/test_package_source_snapshot.py`3件：ZIP内部パスの安全、39個 .c、Python source、実EXE・セーブ・画像・音楽不収録、manifest内SHAの全件一致。
- `dev_lab/run_checks.ps1`全回帰を一回実行し、**Python unittest 180/180 PASS（直前172＋8）**。MAP151/151、atlas513、context204、script590（14,591,845byte）、parent21,214、AST516 body、RTS1v1/2v2合成clock/VM/AIの既存検査も正常終了、末尾`DEV_LAB_ALL_CHECKS_PASSED`、exit0。
- 旧EXEの通常ゲーム動的TARGET OBSERVED=0、新エンジンstrict REIMPLEMENT MATCH=0。180件は証拠照合＋プロトタイプ内の合成/静的テストだけ。元作者ソース復元/ゲーム完成割合は測定できない。

## 次の具体的なソース再実装課題

1. `0x550E70`のレジスタ引数・skill mode1..6・resistanceとFPU数値変換をGhidra pseudo/assemblyの差分を解消しながらtyped domain modelへ切り出す。
2. `0x551490`負値heal gateのx87 dext contestと実stat mutationの条件、`0x576E30`等の抵抗map値を一本化して検証。
3. `0x57B870` AI search・`0x57EB40` callee（本体の証拠は未取得）・movement/Unit targetingを独立したtick engineへ統合。
4. `0x4321B0`のイベント呼出/元stack・`0x4930C0` root if/rif実行の未取得body、脚本special registryを、原作script実行と分離して段階的に復元。
5. 全Unit/Spot/Power save decoderとUI/音声を再構築。セーブファイル・通常ゲーム観測はユーザーがPC操作可能になるまで一括保留。

## 書込所有権

- 変更したのは`dev_lab/src/hakushin_compat/`内の2つの生成/包装Python、`dev_lab/tests/`の8つの新単体試験、`dev_lab/recovered_source`とsource ZIP、`dev_lab/README.md`/`docs/IMPLEMENTATION_PLAN.md`/本handoffのみ。
- 原本ZIP/EXE、`MASTER_LEDGER.md`、A〜E各`data/`/`exe/`/`evidence/`、REA保存済みソース・既存QUEUE/PROGRESS、Git・OS設定・MCP・Remote・automationを変更していない。

## 再現操作（正常に保存済み）

1. `python -m hakushin_compat.saved_ghidra_sourcebook` （保存済みJSONからのみ39疑似C抽出）
2. `python -m hakushin_compat.package_source_snapshot` （ローカルZIP生成）
3. `dev_lab/run_checks.ps1` （全回帰）
各コマンドの詳細・必須データは`dev_lab/README.md`。新規Ghidraや旧EXEを自動で起動しない。

## 追加：39関数のcallgraph依存関係監査

- 新規ソース解析ファイル dev_lab/recovered_source/DEPENDENCY_AUDIT.md を追加。manifest.jsonの保存済みcallees配列を静的集計：直接call参照406、39内63、39外343、外側unique address173、その他 EXTERNAL等ラベル18。
- 343は元関数中のcall参照の本数で、必須の未解析関数343件や原本ゲームソース網羅率ではない。間接call未計上。system/CRT helperも含むため、次に意味別分類してクリーンなAPIへ再構成する。
- 起動0x004B78C0は39外に37本、map初期化0x005001B0は30本、event0x004321B0は22本の直接参照を持つ。39関数を単純に接続しても実行可能プログラムにならない根拠。
