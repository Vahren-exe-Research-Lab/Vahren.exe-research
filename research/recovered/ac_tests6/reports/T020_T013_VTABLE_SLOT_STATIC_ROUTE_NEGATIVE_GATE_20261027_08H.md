# E-AUDIT-20261027-08H-T020-T013-VTABLE-SLOT-ROUTE-NEGATIVE-01
[DATE/OWNER] 2026-10-27 08時台 JST / E T020（T018の誤Golden昇格防止）。STATIC SOURCE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY。旧原作ゲームNOT RUN。
[SOURCE] B-20261027-08H-T013-EFFECT-VTABLE-TICK-JOIN-01、B-owned data/T013_EFFECT_VTABLE_TICK_JOIN_NATIVE_20261027_08H.md（B receipt時現物SHA256 BC7C1A54F77F2C345A73C7DFFF6B05472B000EA0B7F43886BA8C9CCE2CADD1AF、4143B）、B HANDOFF。EはB owner資料をread-only参照。EXE identity SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187は既manifest/B現物照合値（Eは原本EXEを新規hashせず）。
[STATIC SLOT] B native PE .rdata上、vtable base0x63A604、slot+0x04(0x63A608)→0x54E420(update)、slot+0x24(0x63A628)→0x54E3F0(helper)。pool writer 0x550B3B/0x550C29は同vtableを記入するが、ゲーム中の間接dispatch発生はVERIFY。
[STATIC CALL] 0x54E420内部の保存E8呼出位置0x54E4A3と0x54E595は共に0x551490。Skill+0x9C正の系統は当該呼出中の0x551490へ必ず至る訳ではなく0x4C60F0側へ進む。対象生存/Skill+0x48/効果待ち閾値は局所条件。別の即時候補0x54E317→0x551490と遅延候補の経路を混同しない。
[NEW E ACCEPTANCE] (1) vtable slot実バイト一致と動的call実行を別段階とする。(2) helper+0x24を効果core呼出と誤認しない。(3) 条件別に「静的に到達可能」「当該経路では別処理」「実ゲーム未観測」を区別する。(4) callsiteが同一calleeを向いても各呼出が実行された証明ではない。(5) effectの候補UnitをG2実配備のTroop/Unit名簿へ流用しない。
[TEST] tests/t020_t013_vtable_route_static_gate_20261027_08H.py：Python -B unittest 10/10 PASS、exit code0（SYNTHETIC ONLY）。vtableオフセット2件、2slot対応、core 2callsite、即時/遅延分離、+0x9C正負別、+0x48別、未知分岐、全静的経路のobserved=falseを検査。実原作のHP/RNG/VFX再現は含まない。
[TEST HASH] Python実ファイルSHA256 79B6B80A0CC0B924FA17EBAD3A96113EC95C60EA9D6BB4AAA2307EA1916E926B。コード全文Local Compact readback成功。TEST status = STATIC SYNTHETIC PASS / OLD GAME NOT RUN。
[T018 G0] C-NB02合法旧UI、sci1/po2/sp2→sp16の開戦Spotと操作原証拠が受入未充足。今回新原作DYNAMIC OBSERVED0。
[T018 G1] 同一戦闘の直前SAVE実byte/SHAと原作入力トレースが受入未充足。既auto.sav更新時刻/同名異SHAの問題は未解消。
[T018 G2] 実MAP ID/SHA、攻・防・支援3side、確定出撃Unit/Troopの順序付き名簿が受入未充足。支援候補/効果対象/静的poolはG2の代用不可。
[GOLDEN] G0..G4未充足、actual Golden PASS0、old/new strict MATCH0。C-NB02はDESIGNED_NOT_RUN。新たな旧原作実機成功を宣言しない。
[T019] 新規確定矛盾0。GameClear DAT13件/TXT2件の字句scope差はRESOLVED、script2同名優先/phase flag/TXT実読込/gwrite復帰はVERIFY。旧拒否済T019 XREF照会は実施せず。
[MASTER] 現時点の既知正式checkpoint196、READY596=A115/B229/C136/D116、34 Task DONE9/IN_PROGRESS21/VERIFY4（本回TASK QUEUE再集計=34、一意）。READY新規統合ID0。B08研究はSTATIC/VERIFY/NOT READY、MASTERへの代理統合0。
[SAFETY] Eの独立新T020コードと本報告以外書込無し。既拒否T018表境界/session-join、T019 XREF、C T026/T032、D T030 TSV、0x5710C0、06H安全境界事件はBLOCKED継承。拒否元を別tool/shell/path/Remote/ZIPで再試行しない。旧OFFLINE-UNSYNCEDは正式未統合。
[NEXT] 最優先は合法旧原作G0→G1→G2一次receipt収集（開戦Spot/UI、同run直前SAVE bytes+SHA・入力、実MAP/3side/ordered roster）。Bのvtable実dispatch観測・時系列の追跡はB所有、READYになるまでEが仕様確定へ昇格しない。
