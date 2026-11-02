> Archived E-owned original research report; sanitized PRIVATE intake, not byte-identical. Original PC `tests/T020_E_OFFLINE_39_ADMISSION_TRIAGE_20261101_18H.md` remeasured SHA-256 `D7A4498270737DC4E756638758BCAB1B9FD0E1EBF68592614D85F08FE66B7245` at 2026-11-02 JST. STATIC/SYNTHETIC/VERIFY as the historic report states; **new native run 0, Golden PASS 0, strict MATCH 0, new READY 0, NOT_CURATED**. 39 historical offline-source file receipts and their old test counts are provenance metadata only: raw offline bundles are **not** mirrored here and cannot substitute for G0–G2.

# 研究E｜07〜16Hオフライン39証拠のPC復帰・受入前監査（2026-11-01 18H JST）
研究ID E-PC-20261101-18H-T018-T019-T020-OFFLINE39-ADMISSION-TRIAGE-01
Owner E/T018,T019,T020。PC ONLINE / STATIC+SYNTHETIC / VERIFY / NOT READY。今回の原作実行・新規native解析・READY統合は0。
## 読取と出典
Desktop Commander Local CompactでMASTER(4642行)、PROTOCOL、A～D HANDOFF、REA PROGRESS、DEV計画、T018/T019/17H T020、knowledge README/SYNC_STATUSを参照。GitHub非公開developのKNOWLEDGE_CURATION_PROTOCOL・GHIDRA_V9_COVERAGE_REPORTもread-only取得。
PC SHA256 MASTER=E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3 / T018=CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120 / T019=102AFAB94359902D5E74E4B8C55D06CD46269B85DB1B7D0A426FCDE2ED6FC25B。
既存PC 17H報告 tests/T020_E_G012_OFFLINE_RECONCILIATION_20261101_17H.md のSHA256=F3014188EC9729B8786569CC1CD8A03585E601C46B3A14F9B594976E4A9637CA をread-only確認。
現在最後のMASTER checkpoint196、公式READY596（A115/B229/C136/D116）。34Task DONE9/IN_PROGRESS21/VERIFY4は旧確認分類・本回全件再判定なし。
固定manifest E_OFFLINE_MANIFEST_20261101_17h.json SHA256=1F60BA8A065AC7A523059840817507842271B08E68621ADA8FD88141C52E64B1。07〜16H合計39ファイル/1,338,930 bytes、39固有SHA。実バイト/size/SHAの独立再照合39/39一致。
うち07Hの4件は本回の実行作業環境に不在だったため、ChatGPT Library保存原本から取得して4/4一致。残る35件も35/35一致。これは会話作業環境の検証でありPC上へ39原文を同期済みと主張しない。正式統合も未実施。
## 新規重複審査の結果
07/08H: candidate pointer/caller差・時系列IDの合成条件。B側T011/T024の既存owner意味論と照合が必要で、Eがproxy READY化しない。
09/10/11H: rosterの一対一/順序、定義/実行時MAP・VM/RNG、証拠実バイト結合。PC既存10/29 T020 native-CNB02 join preflightのG0〜G4不足欄と重複あり。全部を独立新仕様として採録しない。
- 以前の拒否済み操作・資料・保護範囲は SAFETY_HOLD として維持。内容取得・再試行・迂回は行わない。
15H: 381/381は09〜14Hの既存6ゲート再実行であり、新規381試験でも完全Golden結合器PASSでもない。
16H: 不足22/追加11欄はPC T018旧合法受入票・10/29 T020 join票と意味的重複があり、17Hに旧T018 source SHA一致確認。差分個別承認前はVERIFY。
## 新規T018/T020設計上の訂正候補（DESIGNED / NOT RUN）
「共有される不変の再生入力SAVE/MAP」と「原作から独立採取した一次観測資料」と「新実装の独立出力資料」を別種として定義する。
- 以前の拒否済み操作・資料・保護範囲は SAFETY_HOLD として維持。内容取得・再試行・迂回は行わない。
G0合法旧UI開始、G1同一戦闘直前SAVE bytes+SHA/入力列と時刻、G2実MAP/攻防支援3side/順序付きUnit・Troop、必要ならG3/G4を実sourceで結ぶ。可視取得できないVM/RNG内部値は推測値を補填しない。
- 以前の拒否済み操作・資料・保護範囲は SAFETY_HOLD として維持。内容取得・再試行・迂回は行わない。
新規正式READY ID 0。DYNAMIC OBSERVED 0 / actual Golden PASS 0 / strict MATCH 0。T019新規確定Wiki/DAT/EXE矛盾0、GameClear DAT13/TXT2検索scope RESOLVED、script2実効優先/TXT loader/gwrite復帰VERIFY。
- 以前の拒否済み操作・資料・保護範囲は SAFETY_HOLD として維持。内容取得・再試行・迂回は行わない。
次はPC旧T018・10/29 T020と16Hの受入欄を1対1比較してEのみの純増を仕分け、合法G0/G1/G2一次receiptが採取された場合のみ厳格に受理する。39原文の一括コピー/上書きやMASTERへの無審査統合を行わない。

## 18H現物T018・10/29 T020・16H票の欄別クロスウォーク（再発見を除外）
出典: PC tests/T018_GOLDEN_CORPUS.md のC-NB02 §T018-E-20261015-1049（付近1471-1481）と§T018-E-20261017-OBSFORM-CNB02-CROSSWALK（1655-1660）、PC tests/T020_E_NATIVE_CNB02_JOIN_PREFLIGHT_20261029_09H.md、16H Library引継票（SHA256は17H reportと固定manifest参照）。
G0 UI実侵攻・合法scenario/turn/phase・開戦観測: 10/15 T018既存 → 16H再掲、純増0。候補の戦場種別(野戦/攻城)は独立nullable補足候補、実戦未取得。
G1 旧EXE SHA・直前SAVE byte/SHA・入力SHA・押下保持解放時刻: 10/15 T018と10/17 T018に既存 → 16H再掲、純増0。実DAT構成manifest・同一battle-key・capture許諾receiptは追加候補だが旧資料全体との重複審査前で確定純増件数を付けない。
G2 実MAP ID/SHA、攻防支援3side、順序付きUnit/Troop・隊長/配下・位置/向き・開始frame: 10/15 T018既存 → 16H再掲、純増0。runtime格子・Unit定義と生成世代・初期HP/MP/status・capture epoch/barrierは受入補助候補に限定。
G2 VM/RNG等の画面不可視内部値: 既T018 10/17票はunknown/INELIGIBLEを明記。16H側の追加欄は必須観測へ昇格不可。任意の静的補助としてのみ扱い、欠落を偽値で埋めない。
新実装側build/capture SHA・旧新同入力・identity対応・G3/G4不足: 10/15 T018・10/29 T020に既存。16Hは独立一次証拠を提供しておらず、正式受入0。
判定: 16Hの「22未取得」は未取得件数という監査記述であり、22新仕様でも22確定不具合でもない。「追加11欄」の新規性は現段階で未確定。今回の欄重複照合はSTATIC/VERIFYで、合法原作観測・回帰合成の新実行0。
