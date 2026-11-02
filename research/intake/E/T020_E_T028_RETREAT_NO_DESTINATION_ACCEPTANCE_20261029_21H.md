> Archived E-owner historic source (not a new study ID). Original relative path: `tests/T020_E_T028_RETREAT_NO_DESTINATION_ACCEPTANCE_20261029_21H.md`; authorized PC original SHA-256: `26BB28F003EBF575CFE29742F7F47127F1482F77663AFFCBAB2D03CCE0452982` (verified 2026-11-02 JST). This text removes prior refusal/guard details; it is NOT byte-identical with original. Historical tests were NOT rerun. Evidence: STATIC / SYNTHETIC / VERIFY; ORIGINAL_GAME_GOLDEN=0, STRICT_MATCH=0, NEW_READY=0, NOT_CURATED. B owner's original native study remains B-owned and read-only.

# 迫真戦記E｜T028退却先不在のT018/T020観測・回帰境界（2026-10-29 21H）
研究ID: E-AUDIT-20261029-21H-T020-T028-RETREAT-NO-DESTINATION-SOURCE-VISIBILITY-01
状態: PC LOCAL / SOURCE READ ONLY / SYNTHETIC EXECUTED / VERIFY / NOT READY / 原作実機 NOT RUN。
## 一次資料と所有権
- B所有詳細 data/T028_RETREAT_NO_DESTINATION_EARLY_FAILURE_NATIVE_20261029_21H.md をLocal Compactで全文読取。実ファイルSHA256 EE0831A672E0AFA56D17F4ED278C1B49260C0D3120E47ACB6ABAD4F02A01135A。
- B研究ID B-20261029-2112-T028-RETREAT-NO-SPOT-EARLY-FAIL-01 は STATIC/INFERRED/VERIFY/NOT READY。B owner/HANDOFFを編集せず正式READYへの代理統合はしない。
- 現行V9 pointerは CURRENT_V9_SELECTED_BY_USER_20261029、pointer実SHA256 4A767242C465DB302ACF5FAF582202E4B604E0708492712792F35745F3F5669A。V9 DB実SHAはB所有証拠から継承、今回E独立再ハッシュなし。
- 元EXE識別SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（B出典、今回EXE新ハッシュなし）。旧原本ゲームは非起動・非編集。
## 新規E側の受入境界（Bの確定分と未観測を厳格分離）
- 0x568265/0x568274の条件で検索pathを飛ばす場合は、「退却先が無い」と判定しない。0x568280のUnit vector空は合法到達を含めVERIFY、確定BUG認定禁止。
- 検索成立時0x5682C3→0x5AC1A0の引数3=0、callee戻り0の場合のみ0x5682CB→0x568325の失敗メッセージ文字列を返し、同じ局所の0x568335 Unit vtable+0x68処理をskipするSTATIC条件。
- 戻り非0の場合は0x568329のUnit+0x1B4 link更新、0x56832Fの対象+0xB8加算に進むSTATIC条件。実際の退却完了・SAVE更新は推測しない。
- CP932原生文字列「の部隊は退却に失敗しました／退却出来る領地がありません」の存在と、caller 0x522239→0x52CCF0候補は、画面表示・通知タイミングの実測証拠ではない。
- T019: この分岐は原作BUGやWiki矛盾の確定ではない。新規確定矛盾0。既存GameClear DAT13/TXT2 source-scope RESOLVED、script2/phase/TXT loader/gwrite/decide11 VERIFY据置。
## T020新規テスト・Golden条件
- 新規JSON T020_E_T028_RETREAT_EARLY_FAIL_CASES_20261029_21H.jsonに8件の合成負例、Python t020_e_t028_retreat_source_visibility_gate_20261029_21H.pyに状態分類と出典guardを独立追加。既拒否E session-join codeを使用・再実行しない。
- PC Python -B 実行: SYNTHETIC ROUTE 8/8 PASS、PROVENANCE CONTRACT 3/3 PASS。旧EXEや新エンジンの挙動を試験したPASSではない。
- この退却分岐の旧実機発生phaseは未特定。C-NB02に結合するなら原作G0合法UI開戦、G1同一run直前無改変SAVE bytes/SHA＋操作列、G2 ACTIVEの実MAP・三陣営・順序付きUnit/Troop、G3実終戦、G4戦略World差分を別receiptで要求する。退却文字列の表示は別の可視観測項目とする。
- 戦略画面のみで発生する退却routeならC-NB02のG0-G2を機械的に強制せず、合法旧UI入力・前後SAVE/所属/Spot/Unitの時系列を別case familyとして固定。内部pointerだけではGolden不適格。退却先不在と通常退却の別runは差分として条件ごとに比較し、同一runと偽らない。
- 今回の原作Golden認定DYNAMIC OBSERVED 0 / actual Golden PASS 0 / old-new strict MATCH 0 / 新規正式READY統合0。
## 正本・安全・再開
- MASTER最終公式checkpoint196、READY596=A115/B229/C136/D116（E既確認旧値、全件再集計なし）。34 Task DONE9/IN_PROGRESS21/VERIFY4も旧値。新B 21HはNOT READY。
- 旧OFFLINE-UNSYNCED全件意味重複は未照合。MASTER/他lane/REA/dev_lab/原本/Git/push/Work/設定/自動化は変更なし。PC書込は本E独立ノート・JSON・gateの3件だけ。
- 次: 合法原作UIで退却先不在の画面と前後Worldが観測可能かを検討し、原作旧G0-G4のC-NB02一次証拠探索を最優先。B新研究のREADY/owning proofが整うまで統合保留。
