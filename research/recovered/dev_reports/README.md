# 開発ラボの関数・メモリ契約報告

2026年11月5日、`RESEARCH_SOURCE_CATALOG.tsv` の `dev_lab/docs/` から16本文（保存版133,610 bytes）を回収した。14件は原本とバイト一致、2件は個人用絶対パスのゲームルート接頭辞を各1回だけ `<GAME_ROOT>` に置換した全文版で、先頭に回収版注記を付けた。原本・保存版SHA256、変換内容、未回収理由は [9列の回収台帳](DEV_REPORT_RECOVERY_LEDGER.tsv) に記録する。

目録のファイル名だけで未収録とは判定せず、現在の原本SHAを全Git追跡ファイルの実バイトSHAと比較した。既存の総合回収台帳にある本文とFINDINGS部分版は対象外。別名で一致した2本文は新規コピーせず既存本文へリンクし、残り25件は優先順位または全文レビュー未実施として保留した。要約・同一知見が既存REFに無いという主張ではない。

## セーブ・ロードとオブジェクト

- [Unit/Spot/Powerの保存プレフィクス](DEVLAB_HANDOFF_20261010_16H_STATIC_UNIT_SAVE.md): string検査、4ベクタ、タグ境界、writerとreaderの未確証を区別。
- [初期実セーブと訂正](DEVLAB_ACTUAL_SAVE_GOLDEN_20261011.md): numericの旧1960/2593件を内部訂正1958/2591件とともに保持。同名key・異aux・保存順序の根拠。個人パス置換版。
- [通常ロードのID参照と分岐](DEVLAB_NATIVE_LOADER_STAGE_20261011.md): 0x45E1E0、0x435550のmode0/1、0x49E490の解決候補。保存ID一致とnative pointer再束縛を区別。
- [scene APIとUnit→DAT照合](DEVLAB_WORLD_SCENE_BRIDGE_20261011.md): numeric代表readerを0x470700へ訂正。Spot/Power/Unitの保存関係、手動配置fixture、未解決alias、推測禁止の後続方針。
- [RTTIクラス表](PEER_SCRIPT01_RTTI_CLASSES_20261011.md): vftable、this調整、継承の作者作成一覧。virtual slot数は上限値であり、メソッド意味や完全ABIの証明ではない。

セーブの現行解釈は [REF_SAVE_FORMAT](../../../REF_SAVE_FORMAT.md) を先に読む。上記古い資料のDiplomacyという名前はTurnStateへ訂正されている。0x471AF0/0x471D20とG+0x1EF4B4を外交と決め付けない。過去3保存のbyte一致を、後段残留データや任意保存の全構造・旧ゲームロード成功へ一般化しない。

## ダメージ・状態異常と数値変換

- [型付きdamage初版](DEVLAB_HANDOFF_20261011_TYPED_DAMAGE_215.md): 0x550D80/0x550E70/0x551E50、分岐順、linked award、変換oracleの境界。
- [mode6と距離減衰](DEVLAB_HANDOFF_20261011_MODE6_DISTANCE_233.md): 既消費2draw後の固定値上書き、3回目の変換、距離分岐、x87未確定点。
- [状態異常dispatch](DEVLAB_HANDOFF_20261011_PARALLEL_STATUS.md): chance消費順、28byte候補stride、抵抗成立時は次候補、未知helper境界。
- [dext式とpipeline](DEVLAB_HANDOFF_20261011_STATUS_DEXT.md): runtime係数、2draw、signed wrap、unknown効果後に停止する合成モデル。
- [EB40 callerと負値heal](DEVLAB_HANDOFF_20261010_EB40_HEAL_172.md): AL参照の異なる2caller、抵抗成立は全体終了、dext失敗は次候補という非同一性。
- [精密検証と後続訂正](MAIN_DECOMP_STAGE_20261011.md): 混合攻撃式の **2-R** 訂正、通常7status、SSE変換、Ghidra疑似Cの欠落。古いtyped modelの1-Rやmode6未完成状態を現行仕様に転記しない。

Fraction・callback・合成試験はnative x87の丸め・FPU状態・実機副作用を検証したものではない。テスト件数・静的取得数・DONE/READY・Golden0は各報告の当時値。今回の回収で再実行・昇格していない。

## VM・探索・定義表示

- [event/routine/waitとAI合成モデル](DEVLAB_HANDOFF_20261010_EVENT_AI.md): call-frame、引数一度評価、ASTサンプル、状態回復。個人パス置換版。
- [後続compat訂正](DEVLAB_HANDOFF_20261010_STATIC_COMPAT_121.md): refresh checkとprimary実呼出を区別、primary/fallback pointer分離、28byte shuffle、pushRand2の疎な出力。
- [空間・event分岐](DEVLAB_HANDOFF_20261010_SPATIAL_EVENT_156.md): 0x4E7ED0のgrid/radius、0x4321B0の参照・評価順、missile latch、異なる50反復guard。
- [原DAT定義の表示接続](BATTLE_DEFINITION_STAGE_20261011.md): 宣言位置とSHA、曖昧な親の部分表示、F3入力契約。宣言HPは戦闘中HPではなく、markerは参加Unitではない。
- [39関数sourcebookの来歴](DEVLAB_HANDOFF_20261010_SOURCEBOOK_180.md): 当時37run+2legacyの差分とcall参照集計。非コンパイル可能な疑似Cと独立Pythonを区別する。後日のREA queue64を39取得当時と混同しない。

EVENT_AIの旧full search集計はSTATIC_COMPAT121のrefresh/primary区別を併読する。PARALLEL_STATUSに記載されたZIP SHAはSTATUS_DEXTで更新履歴が記録されている。原ZIPや生成ソースを今回開いた・回収したという意味ではない。

## 既存本文・保留と安全境界

- `DAT_UI_V4_RESEARCH_20261101.md` は [既存UI研究本文](../../DAT_UI_V4_RESEARCH_20261101.md) と現原本SHA一致。
- dev版 `REF_SAVE_FORMAT_20261101.md` は目録版から変化しているが、現在の原本は [現行REF_SAVE_FORMAT](../../../REF_SAVE_FORMAT.md) と完全一致。
- その他の計画・大きな混在index・手動観測手順等25件は台帳の `DEFERRED_NOT_FULL_REVIEWED` 行に保持。内容の可否判断を済ませた扱いにはしない。
- [既回収FINDINGS部分版](../findings/README.md) の省略範囲と付録は再読・再回収しない。元FINDINGS全文の回収は行っていない。

HOLD21名・サイズの明示metadataを確認し、保留本文・保護native範囲・原EXE/DAT/SAVE/ZIP/DB・元ソースdumpは収録しない。参照先のnative probe、疑似C、JSON、画像、ゲーム素材へは追従していない。報告中の過去の拒否・未取得は当時のmetadataとして保持し、再試行や別経路取得を指示しない。本文に含まれる過去の操作手順・所有権・チャット向け依頼は歴史資料であり、現在の操作指示ではない。
