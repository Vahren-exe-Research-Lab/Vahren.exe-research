# 研究E｜T020 selector後段 +0xD0 sentinel／局所RNG分岐受入（2026-10-30 11H JST）
研究ID: E-AUDIT-20261030-11H-T020-T028-SENTINEL-BRANCH-RNG-01
状態: STATIC / NATIVE PE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作Gameplay0、正式READY追加0。
## 入力・所有権
Desktop Commander Local Compact ONLINE。MASTER cp196 / READY596(A115,B229,C136,D116)と規約・A-D HANDOFF・E T018/T019/T020・V9現行案内・DEV計画を読取専用確認。
参照B: data/T028_T013_SELECTOR_D0_SENTINEL_RNG_GATE_NATIVE_20261030_11H.md、SHA256=6A6AE20A74A4CB05E8139CDD285CEECA7C61F2364AD8844CE0660D8923AB3385。B研究はVERIFY/NOT READY。
B-20261030-1115-T028-T013-APPEND-SAFETY-01はB owner2資料＋B HANDOFF追記の拒否。B側反映0/3、迂回・代理追記なし。本E受入は独立した合成試験であり、B READY統合の代替ではない。
原作研究PE SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9はユーザー選択CURRENT状態、B既存SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。今回E新Ghidra起動なし。
## E独立の機械検証と意味
局所PE 0x447BB8+0xB0、0x447D52+0x155のSHAを2/2一致。RNGの直接E8 CALL 0x447C6E/0x447E1A→0x5B6EABを2/2、double 0x63B348=1000000.0・0x63B0B0=2.0を2/2実バイト確認。
局所state分岐: selectorをskippedしても初期local flag=1が残り得る。selector NULLまたは走査Unit+0x1AD非零はflag0経路。関連先+0x10が零、またはflag0で+0xD0 sentinel 1000000.0に進む。
逆に関連先+0x10が非零かつflag1で計算経路へ進み、ローカル比較の有限値下限2.0をモデル化。計算式・x87 NaN/Infinity/丸めは今回の合成スコア入力からは導けない。
0x447C6Eは両枝共通、0x447E1Aは計算枝限定としてfixture化。数えるのはこの局所2 CALL siteのみであり、全ゲームRNG回数ではない。
T020新規fixtureは有効分岐5×pointer条件2×合成finite値3=30、過剰解釈の拒否10、計40。新規40/40 PASS（再実行結果は個別検証器ログ）。前時点の合成累計428は過去記録値であり今回は全件再実行していない。
## Golden / T019 / 統合
G0合法旧UI、G1同一run未改変直前SAVEと操作、G2実MAP・攻守支援3side・ordered deployed Unit/Troop、G3/G4終結・World差分が同一caseでそろうまでDESIGNED_NOT_RUN。旧x20改変DATや異run auto.sav SHAを混用しない。DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。
T019確定原作矛盾追加0。GameClear DAT13/TXT2の字句scope差RESOLVED、script2優先/phase flag/TXT実読込/gwrite/decide11用途はVERIFY。
MASTER最終正式checkpoint196、READY596、34Task DONE9/IN_PROGRESS21/VERIFY4（元TASK QUEUE直接参照、統合更新なし）。新B READY0、E正式統合0。MASTERに書込なし。
旧安全拒否T018表境界・E session-join/T019 XREF・C T026/T032・D T030 TSV・0x5710C0をBLOCKED維持。OFFLINE-UNSYNCED/SAFE/HOLD・他レーン意味重複未解決。元拒否操作の再提出/迂回なし。
E tests内の新規検証Python・fixture JSON・本報告・readback receipt以外の書込なし。原本ゲーム、A-D、REA、dev_lab、Git/Work/設定/スケジュール変更なし。
次回: 0x447E82の真のproducerと4 consumerの同一object/同一frame証拠、局所RNG以外の抽選、C-NB02 G0/G1/G2原作一次記録を優先。
