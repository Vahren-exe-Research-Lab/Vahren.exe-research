# E T018/T020｜簡略戦闘return0の描画可否を決めるprimary vtable slot
研究ID: E-AUDIT-20261023-1850-T020-FASTSIM-DRAW-VSLOT-01
日時: 2026-10-23 18:50 JST / owner E / STATIC, VERIFY, NOT READY / 原作Gameplay NOT RUN
出典: rea_lab/targets/hakushin067_Vahren.exe （研究コピー・読取のみ）
EXE実SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
索引: search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite / 既存manifest SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
既存証拠: E tests/T020_FASTSIM_RETURN0_UI_BRANCH_AUDIT_20261023_1745.md と REA_20261023_17H_P0_BATTLEWND_SECONDARY_VTABLE_FASTSIM_STATIC.md、REA_20261023_1833_P0_DEMOPERSON_VSLOT18_STATE4_STATIC.md（後二者はread-only/NOT READY）。
## 今回の非重複差分
BattleWnd primary vtable=0x00638074、secondary vtable=0x006380CC（primaryから+0x28）は既知。
primary vtable+0x0C、PE VA 0x00638080に原EXE実ポインタ 0x00452D90 を確認。secondary+0x04は別の 0x0040E220 であり混同禁止。
0x0040D220: 0x40D263では渡されたchar引数が0なら描画bodyへジャンプ。非0なら0x40D26C MOV EAX,[EDI]→0x40D26E MOV EDX,[EAX+0x0C]→0x40D271 PUSH 1→0x40D273 CALL EDX→0x40D275 TEST AL,AL→0ならbodyをスキップ。
原作x86 bytes 0x40D26C=8b078b500c6a01ffd284c00f84...、0x452D90=807c240400741181b9a400000008000080740532c0c204008a8184000000c20400。
0x00452D90はABIを機械語で確認: [ESP+4] char!=0かつ[this+0xA4]!=0x80000008ならAL=0/RET4。その他はAL=[this+0x84]/RET4。
0x40E220のreturn0局所: 0x40E27A ESI=EDI-0x28 (BattleWnd primary)→0x40E286 PUSH 1→0x40E288 ECX=ESI→0x40E28E CALL 0x40D220。
対照0x40D0A0局所: 0x40D0CB PUSH 0→0x40D0CD ECX=0x008B8C90→0x40D0D2 CALL 0x40D220。引数0はvirtual検査を通らない。
条件付き結論: return0からのarg2=1、受信者primary vptr=0x638074が不変なら、[primary+0xA4]==0x80000008 かつ [primary+0x84]!=0 の場合のみ描画body進入が許可される。
この条件は描画API成功、画面更新完了、戦闘終了/勝敗、戦略World commitの証拠ではない。vptr差替え/他経路/例外/実ゲーム値はVERIFY。
E専用のT020負例fixtureで「フラグ有りだがmode不一致」「mode一致だがフラグ0」「vptr不明」「arg2=0のbypass」を独立判定。SOURCE STATICのまま原作Goldenには昇格させない。
## 統合・拒否・再開
今回MASTER正式READY追加0。checkpoint196/READY596=A115,B229,C136,D116、34Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値・全件再集計なし。
E原作 DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。G0合法旧UI、G1同一戦闘直前SAVE+入力、G2真MAP/三陣営/ordered Unit/Troop、G3結果、G4世界差分は未充足。
T019 GameClear DAT13/TXT2字句scope RESOLVED、script2 winner/内部flag/TXT実load/gwrite復帰はVERIFY・新規確定矛盾0。
12時台安全拒否2件、旧T018表境界、C T026/T032、D T030、0x5710C0等はBLOCKEDで元拒否操作を再試行しない。OFFLINE-UNSYNCED暫定26研究は未同期/未照合。
次: 実原作同一battle-windowでvptr・primary+0xA4/+0x84・描画到達とG3/G4を別receipt採取する。正式MASTER統合はowner/source hash/READY/重複競合を確認後のみ。
## T020保存・回帰実行の追補（同一研究ID）
V9擬似C＋研究コピー原作EXEの実byteを独立照合。source SHA/primary slot/secondary slot/vcall PUSH1/getter 33bytes/return0 caller/通常描画callerの **7/7 STATIC byte checks PASS**。
E fixture最終18例中 **18/18 SYNTHETIC PASS**、ID重複0、失敗0。原作起動・runtime vptr値採取・描画観測・World commit検証はすべてNOT RUN。
保存した最終JSON fixture SHA256=5AA997A94D0DB6FFD63D198375B0583391369E35AD1A4C5E08BB0CF2DBF007A8。
保存したPython gate SHA256=3720D43222CEAA4E7392C2A83065CDEEBC697C08EE8716B31199A4FCE69FCF93。PCに3ファイル保存・read_multiple_filesで3/3直接読み戻し成功。
検証器はpython -B実行で副作用なし。MASTER/他owner/REA・検索DB・Git/Work・設定・スケジュールは変更していない。

## 二段階modeゲート／時点混同防止（独立追加）
0x40E220 native 0x40E22CでEAX=0x80000008、0x40E231は[secondary+0x78]、0x40E23Aは[secondary+0x7C]と比較してから進む。後者はBattleWnd primary+0xA4に相当する。
しかし0x40E27Fの0x40E2F0呼出後、return0で0x40E28E→0x40D220へ進み、0x452D90がprimary+0xA4を再参照する。この間にmode値・vptr/flagが変化しない証拠は無い。
新規G17は入口mode既知だが描画判定時mode未観測→VERIFY_MODE、G18は入口一致・描画判定時不一致→STATIC_BODY_SUPPRESSEDを要求。入口の保存snapshotを描画時の動的事実に代入してGoldenへ昇格しない。
