# 迫真戦記ver0.67 信用度回復監査（2026-10-26）

## 静的解析：CONFIRMED
- `a_default/script/context.dat:226` に `trust_up = 100`。説明文は「ターン開始時に全回復」。
- `Vahren.exe` の `FUN_00471E80`、`0x00472111..0x00472158` に回復処理。Unit+`0xC4` が100未満なら `trust_up` を加算し、超過分を100に丸める。
- `trust_up` 文字列アドレス `0x006338A4`、取得命令 `0x00472127`。勢力マスターのUnit解決関数 `0x005916E0`。
- Unit serializer `0x0058EFD0` と loader `0x0058E870` がUnit+`0xC4` をint32で保存・復元する。
- `event_world.dat:100-103` は `trust0 > 0` で `addTrust(@plau,-100)` と `sub(trust0,1)`。
- `102_ランダムイベント/randomev11-20.dat:537` の `set(trust0,3)` がその起点。3ターン限定の打消し。

## 実セーブ照合：CONFIRMED
- 読取専用で実セーブを共通28-byte加算暗号方式から復号。4つの `----------` 区切りでNumeric/Unit/Spot/Powerを区別。
- `auto.sav` (10/26 07:02): sci1, player po2, runtime master yaju, checkturn=6, trust0=0, master trust=100。
- `save1.sav` と `save2.sav`: sci1/po2/yaju, checkturn=6, trust0=0, trust=100。
- `save3.sav`: sci1/po2/yaju, checkturn=19, trust0=0, trust=100。
- 4件とも異常値は保存されていない。これだけでは低下から回復した過程の実機確認にはならない。
- 原作とPCのcontext.dat/event_world.datはSHA256一致。保存先・EXEの原本は一切変更しない。

## 判定と次のテスト
- STATIC: 回復経路あり。SAVE: 所持セーブでは100。RUNTIME: 信用度が回復しない不具合は未再現・原因未確定。
- 信用度が100未満の画面で別スロット保存 → 本ツールで `trust`, `trust0`, `master`, `checkturn` を収集。
- 次の自ターン開始後にもう一度別スロット保存。`trust0=0` なのに改善しない場合は `FUN_00471E80` 到達・後続減算・UI参照先を調査。
- 読取専用の検査スクリプト: `data/trust_recovery_probe_20261026.py`。呼出例: `python trust_recovery_probe_20261026.py auto.sav save1.sav`。
- 既存解析参照: `evidence/VAHREN701_DAT_FORMAT.md`, `data/T014_GLOBAL_SAVE.md`。追加のゲーム/DAT/EXE修正なし。
