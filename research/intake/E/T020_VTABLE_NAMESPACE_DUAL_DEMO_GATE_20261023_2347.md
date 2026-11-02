# PRIVATE E source archive — existing ID: E-AUDIT-20261023-2347-T020-VTABLE-NAMESPACE-DUAL-DEMO-GATE-01

Original owner E PC path: tests/T020_VTABLE_NAMESPACE_DUAL_DEMO_GATE_20261023_2347.md. Original raw SHA-256 rehashed 2026-11-02: 5CACBE624CB58F7F665A5666C86088A7142E7B2261FC40B6ADD54C91FF6169B7. This published report intentionally redacts historical safety-refusal details, so it is not byte-identical to the original source. This E-owned crosswalk separates BattleWnd and DemoPerson virtual call namespaces and cites REA analyses read-only; never infer actual 3-side deployed roster from two internal DemoPerson objects. E replay expects private REA source evidence and is not standalone.

Status: PUBLISHED_INTAKE / STATIC + SYNTHETIC + VERIFY / NOT_CURATED / NOT_READY. Any source version/callsite belongs to its 2026-10-23 index epoch, not independently recertified current V9. Past reported tests were NOT rerun. Native original Golden PASS 0, strict MATCH 0, formal READY 0, no new MASTER changes. REA/B owner original findings are read-only references, never republished or reassigned.

---

# T018/T020｜BattleWndとDemoPersonのvtable名前空間・簡略戦闘2側dispatch受入ゲート
ID: E-AUDIT-20261023-2347-T020-VTABLE-NAMESPACE-DUAL-DEMO-GATE-01 / Owner E / STATIC CROSSWALK・VERIFY・NOT READY / 旧原作Gameplay NOT RUN。
## 新しい証拠照合（前22:52 cleanup-CFGとは独立）
- 出典E: tests/T020_FASTSIM_RETURN0_PRIMARY_VTABLE_DRAW_GATE_20261023_1850.md（Eによる旧EXE機械語確認）。
- 出典REA（read-only・READBACK VERIFIED・NOT READY）: rea_lab/decomp_task/REA_20261023_22H_P0_DEMO_DUAL_VCALL_STATIC.md と REA_20261023_23H_P0_BATTLEWND_DEMO_GLOBAL_IDENTITY_STATIC.md / 同EVIDENCE.json / 同READBACK.md。
- 元研究コピーEXEの記録SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9索引記録SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。今回EXE/DB実バイト再ハッシュなし。
- BattleWnd primary vtable 0x638074 の +0x0C(cell 0x638080)=0x452D90 は「return0後の描画ゲート」用。BattleWnd secondary vtable 0x6380CC の +0x04 は 0x40E220。
- DemoPerson secondary vtable 0x638054 の +0x04(cell 0x638058)=0x449730 は別の「簡略戦闘ループ更新」用。**同じslot offsetでもreceiver class/vptr/source cellが異なる**。
- 原作静的値: BattleWnd固定基準0x8B8C90 +0x1C8=0x8B8E58、+0x1CC=0x8B8E5C。REA23Hは0x40CB90初期化、0x40CCF0で各NULL時生成、0x40F320で両globalを参照する証拠を追加。
- REA22H: 0x40E40CでBattleWnd側+0x288>0かつ先行条件通過の候補経路に限り、0x40E42Eで+0x1C8側DemoPerson secondary+4、続いて0x40E445で+0x1CC側DemoPerson secondary+4を間接CALL。PEに直接CALLが0件でもvirtual不在とは言えない。
- 重要な未証明条件: 0x40E2F0のEDIがその実行時に0x8B8C90であること、globalが非NULL・同runで安定・指定型vptrであること、+0x288実値、2CALL実到達、処理結果・戦略World反映。
## E独立の受入境界
- G0/G1/G2は合法旧UI起源・同一戦闘の直前SAVE bytes/SHA+入力・実MAP/三陣営/ordered Unit/Troopの別receiptで判定。内部2側dispatchの静的証拠はG2実出撃名簿の代用品にならない。
- T020拒否: 別run混合、slot名の混同、EDI推測でglobal同一性を確定、片側だけを両側完了に拡張、+0x288未観測なのに分岐確定、CALL命令の存在を実ゲームの実行証明に昇格。
- Historic refused targets and operations remain BLOCKED and are not disclosed/reproduced in this sanitized E report.
## 実行/保存/統合
- テスト出力・件数・SHAは独立検査後に追記/報告する。対象は tests/T020_VTABLE_NAMESPACE_SYNTHETIC_CASES_20261023_2347.json と tests/t020_vtable_namespace_gate_20261023_2347.py。
- 本成果がPCへ保存されても、REAはNOT READYでありMASTER正式採録対象ではない。Eの検証設計と受入区分のみ新規差分。
- 現行Golden G0-G4全未充足／今回新規DYNAMIC OBSERVED0・actual Golden PASS0・strict MATCH0。T019新確定矛盾0（GameClear DAT13/TXT2字句差RESOLVED、script2優先・flag・TXT実load・gwrite復帰VERIFY）。
- 最終正式checkpoint196・READY596(A115/B229/C136/D116)、34 Task DONE9/IN_PROGRESS21/VERIFY4は前回旧確認値・今回未再集計。OFFLINE-UNSYNCED暫定26未照合、新規正式READY0。
- 次: 合法C-NB02同run G0/G1/G2一次証拠の最優先採取。内部dual virtualはもし合法観測が成立したときだけ同PID/run/capture SHAと整合させる。
## PCでの保存後検査（同一run）
- Local CompactによるE所有レポート・JSON・Pythonの直接読み戻し3/3成功。Python -B実行成功。
- REA所有の23時台JSONは公開済み保存readback SHA256と今回再計算値の一致を検査。JSON内の先行25/25 native検証証跡・2 global slot算術・4 vtable target/3 E8 siteとE既存18:50 primary/secondaryラベルを軽量照合してPASS（原作PEを今回新規逆アセンブルしたのではない）。
- T020新規13件はSYNTHETIC比較13/13 PASS。原作Gameplay NOT RUN／actual Golden PASS0／strict MATCH0。JSON SHA256 C26703BF1EF536BEE82A66D86FB6906F2A617B77A7E0B6229D46B20C08588533。
- 検証器SHA256 3B7B21A59FBCF43C3EBDC3FFABFB1B59C37DAD25D2683D09A3A78F9062EBE4C8。新規正式READY0・MASTER正本変更0、今回の新規安全拒否0。既存拒否はBLOCKED維持。
