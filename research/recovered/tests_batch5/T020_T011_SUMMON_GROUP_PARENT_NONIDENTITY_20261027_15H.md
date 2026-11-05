# E-AUDIT-20261027-1549-T020-T011-SUMMON-GROUP-PARENT-NONIDENTITY-01
[OWNER/STATUS] E / T020・T018。2026-10-27 15:49 JST。STATIC OWNER-EVIDENCE CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作ゲーム新規実行・Golden比較なし。
[PC/PRECHECK] Desktop Commander Local Compact接続成功。MASTER_LEDGER、evidence/ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA decomp_task/PROGRESS、dev_lab/docs/IMPLEMENTATION_PLAN、T018 GOLDEN CORPUS、T019矛盾、search_index README/BUILD_MANIFESTを先読。既拒否XREF、T018表境界、禁止VA等は再試行なし。
[B OWNER 15H] B-20261027-1514-T011-SUMMON-CALLER-GROUP-PROVENANCE-01：data/T011_SUMMON_CALLER_GROUP_PROVENANCE_NATIVE_20261027_15H.md 5229 bytes、SHA256 FCC6CA977366126DEDC22D025B7FE25429DFBE83C59D9C41DEAB52A4B465B48D（E新テストで現物hash検証PASS）。B所有STATIC/VERIFY/NOT READY、代理READY統合なし。
[ORIGINAL SOURCE PIN] 原作EXE識別SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（search_index BUILD_MANIFEST + Bの実PE証跡より、E本回原本再hashなし）。2026-10-21 Ghidra indexをE本回再生成せず。
[CONCRETE DELTA] B静的経路ではsource Sは第1stack引数で、SummonFlash+0x7Cへ同Sが格納され得る。holder H=[S+0xC]は管理参照、child+0x1D0は分岐によりGroup pointerを保持し得る。4 caller VA=0x54DF4B/0x550219/0x57F484/0x57F492。S/H/Group/childの共有は一意summon-parent ID・EXP還元先の証明ではない。
[E ACCEPTANCE] 同Group配下の異source、NULL Group、同sourceの異Group、別run/生成世代でのpointer再出現を別fixtureとして扱う。group_ptr/holder_ptr/source_ptrだけでparent_idを充足させない。parentの証拠欄へ見かけ上64桁のSHAを入れても実バイト真正性は未保証。
[G2 BOUNDARY] 戦闘中に新規生成された子Unitは原作開戦時G2のordered deployed Unit/Troopと混同しない。初期配置・戦闘中召喚のphase receiptを分離し、追記時のUnit数増加をG2の事後補完と扱わない。実ゲームの生成順・識別は未観測。
[NEW E TEST] tests/t020_t011_summon_group_parent_nonidentity_20261027_15H.py をE所有で新設。B15 detail実byte SHA pin、group親非一意、epoch/run隔離、source/effect流れ、caller 4経路、未保証親ラベル、G2初期配置非同一、NULL入力など14項目。
[EXECUTION] Local Python -B実行：unittest 14/14 PASS、exit code 0、0.002s。全casesは合成入力、B owner detailのみ実ファイルbyte attestation。旧実ゲームGameplay PASS/strict MATCHへ加算しない。
[T019] GameClear DAT13/TXT2ソース範囲差RESOLVED維持、script2同名定義優先/phase flag/TXT実ロード/gwrite復帰はVERIFY。今回の新規確定矛盾0。
[T018/GOLDEN] C-NB02 G0合法開戦旧UI・Spot/入力、G1同一run直前SAVE bytes＋input、G2真MAP/三陣営/ordered deployed Unit/Troop、G3終了、G4戦略World差分は全未充足。新規原作DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。X20改変前DAT基準の独立照合必須。
[MASTER/COUNT] 最終既知正式checkpoint196、READY596=A115/B229/C136/D116（READY全履歴再計算なし）。今回MASTER TASK QUEUEを直接再集計し34 Task/unique34、DONE9/IN_PROGRESS21/VERIFY4を確認。新規E正式統合ID0・MASTER編集0。
[SAFETY/CONTINUITY] 新規安全拒否0、PC接続障害0。T018表境界/session-join、T019拒否済XREF/06H逸脱、C T026/T032、D T030 TSV、0x5710C0など旧BLOCKEDは不変。OFFLINE-UNSYNCEDは正式未統合。原本EXE/DAT/SAVE/ZIP・A-D/REA/dev_lab・Git/push・Work・設定・schedule変更0。
[NEXT] C-NB02同一合法戦闘のG0/G1/G2 raw evidence収集が依然P0。B側で4 caller別Sの実身元・召喚parent IDとEXP credit先を確認できればEの現在のnegative gateに別証拠receiptを追加し、先に原作実測を与えない限りstrict一致に昇格しない。
[READBACK/SHA] 新Eコード全文138表示行相当・本記録全文17行相当をLocal Compact独立read_fileで確認し指定marker全件存在、MASTER 34IDユニークもread-only確認。Get-FileHash(SHA256) コード=092050A11FD392D06BE3CA48EA406AB128CD4EC219DEC2EDAB073BD24C5D9B63。本文SHAは追記後に独立取得する。
