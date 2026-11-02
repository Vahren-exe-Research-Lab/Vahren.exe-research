> Owner-E archived research, sanitized for private intake. PC source `tests/T020_E21_ARTIFACT_BYTE_ATTESTATION_AUDIT_20261028_23H.md` original SHA-256 `58FA92D44F38FC4F128A77C66A3EFDA90026622F838BFB439CD084D3B3C4E3AB` rechecked 2026-11-02 JST. Historical synthetic-only run counts are as reported, **NOT rerun now**, no original game Golden, no READY, NOT_CURATED. Source not byte-identical after safety redaction.

# E23 互換監査：E21合成artifact byte pinと原作Golden証拠の非同一性
研究ID: E-AUDIT-20261028-23H-T018-T020-E21-ARTIFACT-BYTE-ATTESTATION-01
担当E、T018/T020、T019参照。STATIC / SYNTHETIC EXECUTED / VERIFY / NOT READY。
## 差分と入力証拠
- PCのE22 fixture：T020_E21_G2_SCHEMA_BRIDGE_CASES_20261028_22H.json。元E21 artifact digest申告7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA。
- 今回ChatGPT会話添付のE21原本（E_20261028_2149/T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json）を別のコンテナでSHA256計算し、上記とbyte hash一致を確認。PC内の同原本再hashやLibrary→PC同期を完了したとは主張しない。
- E22のG2診断はsource SHAが64桁であることを確認するだけで、源artifact bytesを読み込まない。本件でsource_pin(expected, bytes or None)を独立実装し、SHA形式/bytesなし/型不正/値不一致/byte一致を5階級で判定。
- byte一致成功も「合成artifact同一性」だけ。G0合法UI/G1同run直前未改変SAVE＋入力/G2実MAP・三side・順序付きUnit/Troopを保証しない。原作EXEのマニフェストSHAも動的キャプチャとは別の証拠。
- E21 G2はattack/support出撃だけでdefense出撃の一次証拠がない。map_shaは合成rawの識別であり、native map bytes/識別IDの独立receiptを代用しない。defend→defenseラベル変換もVERIFY。
## 検証
- 新規tests/t020_e21_source_attestation_gate_20261028_23H.py：source SHA falsification、正常合成bytes、原作証拠に昇格しない規則、攻防出撃・map/EXE/manifest欠落、自己申告native偽装を計20件検証、PC実行20/20 PASS。
- Prior protected/denied operations and targets remain SAFETY_HOLD. This report does not republish denied source details.
- 旧EXE Gameplay NOT RUN。DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0。T019新規原作矛盾0、GameClear DAT13+TXT2はSOURCE-SCOPE RESOLVED、script2/phase/TXT/gwrite/decide11はVERIFY継承。
## 正本・拒否・保全
- MASTER末尾・TASK QUEUEの今回の総当たり集計は実施せず。最後に公式確定したcheckpoint196／READY596（A115/B229/C136/D116）、34 Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値。新規正式READY統合0、ID重複再計数なし。
- B T028最新read-only HANDOFFは16H STATIC/VERIFY/NOT READY。REA PROGRESSは古い索引で新READYの根拠にせず。DEV計画もread-only。
- Prior protected/denied operations and targets remain SAFETY_HOLD. This report does not republish denied source details.
- 今回のPC書込はE所有の本報告・新fixture・新検証scriptのみ。他owner/MASTER/REA/dev_lab/原本/Game/Git/Work/設定・scheduleは変更なし。
## 次回
- 同一原作戦闘の合法UI/未改変SAVE/input/実MAPとordered出撃名簿を別個の信頼できるreceiptで収集。E21資料のPC正式同期は所有者・source SHA・同ID・READY・既統合・重複/競合を確認してから一度だけ。
