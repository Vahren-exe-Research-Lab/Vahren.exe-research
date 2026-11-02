# E T020｜07H 軽量集計コマンドのOTHERエラー回復記録
RECOVERY-ID: E-RC-20261030-07H-T020-PS-AUDIT-OTHER-01
日時: 2026-10-30 07H JST。Owner: E。分類: OTHER / RECOVERED、SAFETY_REFUSALではない。
最後の既知成功: E06Hの合成266/266、MASTER checkpoint196/READY596。今回B07一次ノートのread-onlyハッシュA62F2BFC272326AE24A94807637A9F370644995ABF2F1182179E7357A14DB945。
失敗1: PowerShell既定実装が演算子「??」を受理せず、集計用コマンドがParserError。Python再実行には到達せず、ファイル変更・未保存差分なし。
失敗2: 修正後、11検証器は終了コード0で全実行。しかし一時集計のMeasure-Objectはhashtableのpass/totalフィールドをpropertyとして認識せず、合計値null。検証器の失敗ではない。
初回集計構造の問題: 21H検証器はSYNTHETIC 8/8行の後にsource-check 3/3を出す。最後のPASSだけを取る簡易パーサが3/3を拾う誤集計を確認し修正。
回復: 各検証器の正規出力を区別し、合計をPowerShell foreachで整数加算する軽量read-only監査を実行。全11検証器exit0、T020合成299/299 PASS（既存266＋新規33）。
保存済み: E-own tests下の新py、fixture、acceptance文書、readback JSON。独立実バイトSHA3/3一致・receipt JSON解析PASS、MASTER SHA不変。旧拒否を迂回しておらず、SAFETY_REFUSAL新規0。
未完了: 原作実ゲームG0/G1/G2一次証拠・actual Golden/strict MATCH、B07のREADY、および旧OFFLINE-UNSYNCED意味照合。
次: 旧原作合法同run capture・B ownerの0x510850/0x5AC5B5根拠をread-only確認。再発時も検証対象（合成/出典/実ゲーム）を混同しない。