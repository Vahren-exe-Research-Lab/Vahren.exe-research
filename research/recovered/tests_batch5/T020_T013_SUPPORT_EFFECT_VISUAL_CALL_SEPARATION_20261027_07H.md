# E-AUDIT-20261027-0745-T020-T013-EFFECT-VFX-NONIDENTITY-01
日時: 2026-10-27 07:45 JST / owner E / T020、T018のG2誤受入防止
状態: STATIC SOURCE RECONCILIATION / SYNTHETIC EXECUTED / VERIFY / NOT READY / TARGET GAME NOT RUN
## 一次出典と所有権
- B owner ID: B-20261027-07H-T013-SUPPORT-EFFECT-DISPATCH-VISUAL-BYPASS-01。B HANDOFF/detailは明示的に NOT READY、正式代理統合禁止。
- B原資料: data/T013_SUPPORT_EFFECT_VISUAL_BYPASS_NATIVE_20261027_07H.md、今回E read-only確認の現物 SHA256 F3BBE0F0C839CF12D1ED1902B750C8CA13EFB3538BA0EBD1F5BB86216A18AE3C。Bが報告した対象EXE識別SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。EはEXEバイトの再ハッシュなし。
- B限定ASM根拠: 単体 caller 0x57FA99 と複数候補 caller 0x57FE17 → 0x54E0B0。actor/skill/candidateは効果オブジェクト+0x78/+0x80/+0x94に格納。
- 視覚登録省略側: 0x54E2BC の+0x85=0x0101から 0x54E2C5 JMP 0x54E30D。視覚登録側: 0x54E2C7..0x54E304で+0x85=1。正常継続すると両側とも0x54E30Dを経て0x54E317 CALL 0x551490。
- Bの直接E8照合5/5一致（Eは今回ASM再採取せず）。0x551490内部にはSkill+0x230/RNG/早期returnがあり、callee到達とHP/status変化を同一視しない。
## E独立T020受入差分
- [EFFECT-CALL-01] VFX非登録経路でも、正常継続条件が満たされれば効果coreのCALL到達候補は残る。可視VFXの有無を効果未呼出の証拠にしない。
- [EFFECT-CALL-02] VFX登録試行を視覚表示の実成功と同一視しない。VFXと実HP/MP/statusとcore CALLを別々の観測列にする。
- [EFFECT-CALL-03] CALLを確認しても実効果成功とみなさない。早期return・失敗・RNGの未確定部分はUNKNOWN/VERIFY。
- [EFFECT-CALL-04] 候補参照ポインタは効果入力であり、G2の原作確定出撃Unit/Troop名簿ではない。NULL・メモリ寿命・対象identityは原作receiptなしで補完しない。
- [EFFECT-CALL-05] この制御フローは局所・正常継続の条件付き。例外/NULL/呼出未到達に対する絶対保証に拡張しない。
## 実行済み独立テスト
- tests/t020_t013_effect_vfx_independence_gate_20261027_07H.py、現物SHA256 8EE3F6CE10D5B73361C2D527C83A1A23A1B36F910A01AEDDA6EBBF3DCF6E3AD4。
- Python -B unittest: 10 tests, OK, exit=0。visual登録あり/なしの双方でcore CALLを一度だけ記録し、actor/skill/candidate参照保存、早期returnでHP未変化、合成変化/VFX独立、合流前中断、G2名簿非同一を検証。
- すべて合成fixture（toy HP+5を含む）。本家エンジン/VFX/HP式の再現試験ではない。原作Gameplay実機テスト0、Golden合格0、新旧strict MATCH0。
## T018 Golden / T019 / MASTER
- C-NB02 G0合法旧UIによる開戦Spot・操作、G1同一戦闘直前SAVE実byte/SHA＋入力、G2実MAP SHA・攻防支援3side・順序付き出撃Unit/Troopは全て受入未充足。G3戦闘結果・G4戦略World差分も未充足。新規E DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
- T019新規確定矛盾0。GameClear DAT13/TXT2は字句検索scope差のみRESOLVED、script2同名優先/phase flag/TXT runtime採用/gwrite復帰はVERIFY。今回T019の拒否済XREF検索は一切実施していない。
- MASTER TASK QUEUEを07Hに直接抽出・再集計: 34 IDs一意、DONE9/IN_PROGRESS21/VERIFY4。最終正式checkpoint196、READY596=A115/B229/C136/D116は過去MASTERの正式値（全READY履歴の新規再集計なし）。本回新規正式統合ID0。
## 復旧・安全・次の一手
- OTHER RECOVERY-ID E-RC-20261027-0745-REA-PROGRESS-PATH-01: 初回 rea_lab/PROGRESS.md 読取はENOENT。正しい rea_lab/decomp_task/PROGRESS.md をread-only再確認し復旧。作業やデータの消失なし、安全拒否ではない。
- 新規安全拒否0。既存T018表境界/session-join、T019拒否XREF、C T026/T032、D T030 TSV、0x5710C0と06H境界事件はBLOCKED継続、代替tool/shell/path/Remote等の迂回0。旧OFFLINE-UNSYNCED成果は正式未統合。
- PC書込は本E-owned T020報告と新E-owned T020合成テストだけ。MASTER/A-D/REA/dev_lab/EXE/DAT/SAVE/ZIP/Git/Work/設定/automationは変更しない。
- 次は同一合法戦闘のG0 UI+入力→G1 prestate SAVE→G2 MAP・3side・順序名簿の一次receiptが揃うかを安全な保存済み資料から照合。Bの支援効果を新仕様として受入する場合もB READYと別途原作実測を必要とする。
