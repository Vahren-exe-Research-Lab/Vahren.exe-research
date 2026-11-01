# Eレーン未収録知見：Golden受入と研究回収の入口（2026-11-01）
研究ID: E-PC-20261101-2110-T018-T019-T020-KB-CURATOR-DELTA-01
owner E / T018,T019,T020。状態: `STATIC`/`VERIFY`/`SYNTHETIC_PRIOR_ONLY`/`ARCHIVED_UNVERIFIED`、実機Golden PASS=0、strict MATCH=0、新規READY=0。
**このファイルは原作の一次資料ではなく、許可済みPCのE所有報告に基づく検索・回収用要約。**

## 対応するPC原文と出典SHA256
| 研究ID（短縮） | PC相対資料 | SHA256 |
|---|---|---|
| E17H-G012 | `tests/T020_E_G012_OFFLINE_RECONCILIATION_20261101_17H.md` | `F3014188EC9729B8786569CC1CD8A03585E601C46B3A14F9B594976E4A9637CA` |
| E18H-OFFLINE39 | `tests/T020_E_OFFLINE_39_ADMISSION_TRIAGE_20261101_18H.md` | `D7A4498270737DC4E756638758BCAB1B9FD0E1EBF68592614D85F08FE66B7245` |
| E19H-KB | `tests/T020_E_KB_FINDABILITY_CROSSWALK_20261101_19H.md` | `11FF3B1318C85E3748D811BB36EF83962CCF51AA9FAFEE697444150C96F0CF95` |
| E20H-G0 | `tests/T020_E_G0_SAVE_RUN_SOURCE_SCOPE_CROSSWALK_20261101_20H.md` | `21AD936F1A013F88E10E1FE05D51880708247DD1DADAEDB63FD1721DBA4D466F` |
| T018 | `tests/T018_GOLDEN_CORPUS.md` | `CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120` |
| T019 | `wiki/T019_CONTRADICTIONS.md` | `102AFAB94359902D5E74E4B8C55D06CD46269B85DB1B7D0A426FCDE2ED6FC25B` |
これらのSHAは既存EのPC実測受入記録と今回のPC readbackに基づく。GitHub`RESEARCH_SOURCE_CATALOG.tsv`はE17～20Hの6個のreport/receiptを列挙するが原文本文のGitHub保存証明ではない。

## 将来のAIが参照すべき結論
- **T018 G0/G1/G2:** 原作の合法UIによる同一戦闘開始、直前同一runのSAVE byte SHA/入力時系列、実MAP・3陣営・順序付きUnit/Troopを一つのbattle_key/runへ結合する。候補`s16.map`や保存側Spot/Unitを実配備結果にしない。別PID、同PID別戦闘時間窓、観測ファイルの再利用は不適格。
- **T020:** 原作と新実装が同一不変SAVE/MAP等を`SHARED_IMMUTABLE_INPUT`として共有することは正当な試験設計になり得る。一方`ORIGINAL_INDEPENDENT_OBSERVATION`と`REIMPLEMENT_INDEPENDENT_OBSERVATION`は各run別の一次証拠とSHA/ファイルID/時刻である必要がある。旧検証器の無条件同パス拒否は入力/観測の役割別に限定する。Windows file identity・親folder再解析・atomic captureは未実証。
- **T019:** GameClear `DAT13/TXT2`は検索対象範囲の差で訂正済み`RESOLVED`。script2同名優先、TXT runtime読込、phase flag、gwrite後段は`VERIFY`で、新規原作確定バグ0。候補VA `0x50C9A0`等を独立STATIC再照合なしに辞書へ登録しない。
- **過去合成試験:** E09～15Hの381/381・E16Hの19/19は各過去の合成fixture結果であって、本GitHub収録時の再実行・原作ゲーム互換性の証明ではない。

## 残る未同期・保全の順番
1. 2026-11-01 03～16HのオフラインE研究は現行GitHub目録に該当研究ID 0件。旧07～16Hの39ファイル・合計1,338,930バイトの過去SHA検証履歴があるが、**今回は39実体の再取り込みはしていない**。Library/PC実体と当時のmanifestを再検証し、ID/同一SHA重複を除き安全な要約と機械可読manifestだけを収録する。
2. REAは11/1 03～16H Library研究群（以前のcurator監査では67ファイル）と未同期原文、BはHOLD21・10/25欠落と03H/07H保全失敗を元ownerと再照合する。拒否済みデータ本体の代替取得はしない。
3. source`MASTER_LEDGER.md`の最終公式checkpoint196/READY596（A115/B229/C136/D116）、34 Task DONE9/IN_PROGRESS21/VERIFY4は**旧最終確認値**であり、この収録で更新しない。新実機Golden/strict MATCH=0。

## Curatorの次の安全な一手
PC `tests/T020_E_KB_CANDIDATE_HANDOFF_20261101_19H.json`、`tests/T020_E_G0_SAVE_RUN_SOURCE_SCOPE_RECEIPT_20261101_20H.json` と上記ソースSHAを照合して、既存`REF_BATTLE_TAKEOVER.md`との差分だけE/T018受入一覧へ統合。旧安全拒否・他owner・ゲーム原本を保護。生SAVE/原作EXEや個人PCパスをGitへ送らない。
