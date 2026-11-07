# 迫真戦記ver0.67 戦略⇄外部戦闘EXE Stage6：終了ABIとASLR実測準備
研究ID: BRIDGE-20261021-RESEARCH-06 / 2026-10-21 JST。
状態: STATIC ORIGINAL PE + SYNTHETIC VALIDATED / ORIGINAL GAME NOT RUN / WORK NOT USED。
原本Vahren.exe SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
研究正本はsearch_index配下のMarkdown/JSON/Python。原本EXE、セーブ、他レーンA～E/MASTER、製品、Git、スケジュールは変更なし。

## F06-01｜元0x493630の5経路と引数・戻りの正規ABI（ORIGINAL PE VERIFY）
直接E8 CALLは0x40E2B9 BattleWnd、0x49303A/0x493082/0x4930A1自然tick、0x4A1764 scriptの5サイト。CALL索引V2と独立PEのopcode bytes一致。
- ECX: 通常/scriptでは [GameEvent E+0x1EED1C] の値、BattleWndでは [BattleWnd+0x190] の値。
- EDX: 通常/scriptでは &E+0x1EED20、BattleWndでは [BattleWnd+0x194] の値。
- stack[entry+4]=GameEvent* E。0x49366Bでprologue後[ESP+0x130]へ置き直す。
- stack[entry+8]=raw result flag。結果判定の0x494858では[ESP+0x134]の下位byteを読む。
- native return 0x494855はRET 8（stack引数2 DWORDはcallee側でpop）。Ghidra擬似Cの __fastcall 解釈だけでフックの関数ポインタを確定しない。
- 自然tick 0x49303A/0x493082 push1、0x4930A1 push0。BattleWndは直前のEBP==1をSET Eでboolean化。scriptはpush EDI（opcode5の意味は下節）。
- caller別の戻り後も異なる。BattleWndは0x40F000/0x48ABF0/条件付0x48EEE0を実行、通常tickはGameEvent Task/VMへ戻り、scriptはAL1でYieldする。callerやscene kindを結果packetから省かない。
証拠: BATTLE_FINISH_STAGE6_NATIVE_CALLER_ABI_PE_20261021.json、BATTLE_FINISH_STAGE6_EXACT_NATIVE_ABI_GATE_20261021.json。
## F06-02｜AttackMap要素数はnative結果反映の重要gate（ORIGINAL PE VERIFY）
- 0x4936E4/F1/FEの3side虚関数+0x14と、0x493746 active clear、pending/roots clearが0x494667より先に存在。旧A/B成果は重複計上しない。
- 0x494655 XOR EDI,EDI。0x494667 CMP DWORD [EBP+0x1EED28], EDI、0x49466D JNE 0x494858。つまりE+0x1EED28 (attack_map数)が非0のときのみ結果flag判定へ進み、0なら0x494673から別処理/RET8側。
- 0x494858 CMP BYTE [ESP+0x134],0。raw flag非0なら0x494F8E、0なら0x494866側へ分岐。これはcallerのnatural win/defense flagのsemanticと整合する。
- 0x494855 RET8の後ろに0x494858があるが、前方0x49466Dからこの位置への直接JNE predecessorをPEで独立検証。単なるテキスト順のfallthroughではない。
- 設計上、外部戦闘のために原作AttackMapのcountを0にしてfreezeすると、元nativeの通常戦略結果枝を飛ばし得る。反対にnative finishを省略すると前段Unit/LvUp/Task/VM処理が欠ける恐れ。
- native finishingを一回だけ適用し、AttackMap・Power・Spotの所有者を終了まで保持。新Python apply_battle_endとnative finishの二重反映は禁止。
証拠: BATTLE_FINISH_STAGE6_COMMIT_BRANCH_GUARD_PE_20261021.json、BATTLE_FINISH_STAGE6_RET8_CROSSBRANCH_PE_20261021.json、BATTLE_FINISH_STAGE6_NATIVE_WINDOWS_20261021.json。

## F06-03｜script win結果の初期仮説を再評価し既知flag0を再確認
- 原作DAT dispatcher opcode5 jump-table entryは0x4A174A (win)、opcode4は0x4A166E (continue)。0x4A1302 XOR EDI,EDIの後にjump-tableへ進む。
- opcode5の直接経路0x4A174A→0x4A175C PUSH EDI→0x4A1764 native finishではEDI=0（callee-saved EDI前提）。A所有exe/T006_TARGET_DISPATCH.mdの既存resultFlag0説明と一致する。
- opcode4 continueは0x4A1670 MOV EDI,-4でFrameStackのcursorを減算する別経路。古いリニア逆アセンブルだけではwinのflagが-4かもという疑義が出たが、元ジャンプ表に基づき誤推論を回避した。
- Stage6の preliminary BATTLE_FINISH_STAGE6_SCRIPT_WIN_FLAG_DISCREPANCY_20261021.json は未確定仮説であり、BATTLE_FINISH_STAGE6_SCRIPT_WIN_OPCODE5_RESOLVED_20261021.jsonで訂正。新規bugとして登録しない。既存A成果のREADY加算0。
## F06-04｜原本ASLRとlive pointer補正をPEで確認
- 原本Vahren.exeと研究対象コピーはSHA完全一致。MODタイトル名の実行体は異なるSHAであるため同じABI/RVAを無確認で適用しない。
- preferred base 0x00400000、SizeOfImage 0x00750000、DLLCharacteristics 0x8140（DYNAMIC_BASE=true）、relocation block 582。GameManager RVA0x004BE2F0、GameEvent RVA0x004BE7F4、SceneInit RVA0x0008D6A0、Finish RVA0x00093630。
- 実アドレスは loader module base + RVA。以前のStage3パーサーはPlayer/Enemy/Troop vtableのpreferred VAを固定比較しており、rebased live snapshotでは誤拒否となる恐れ。
- battle_aslr_aware_detached_bridge_v4_20261021.pyを追加。入力detached memoryのモジュールbaseと原EXE SHAを検査、既知side/troop vtableだけを**複製したバイト列内で** preferred VAへ正規化し、既存V3を再利用する。実原作プロセスを変更しない。
- 合成テスト test_battle_aslr_detached_v4_20261021.py 8/8 PASS。actual live module baseそのものはNOT OBSERVED。
根拠 BATTLE_BRIDGE_STAGE6_ASLR_PE_LAYOUT_20261021.json。

## F06-05｜将来のG0/G1に向けてReadProcessMemory事前検証器を作成
- battle_native_readonly_live_probe_stage6_20261021.pyは--pid必須。署名一致したVahren.exeだけをOpenProcess(READ|QUERY)で開き、EnumProcessModulesExで実ベースを読み、RVAでGameEvent/Task/3sideのmode/active/countなどを調べる。
- DLL注入、書込、ポーズ、breakpoint、入力操作、原本EXEの起動は一切なし。MAP最終選択、イベントVM詳細、CRT TLS乱数状態、実selected Unit一覧は未取得として明記。
- Windows Python64bit自プロセスにReadProcessMemoryを使って4byte値0xBADC0FFEを読み戻すselftest成功。ただし原本ゲームは実行中でなく元Vahrenプロセス接続実績0、100%ゲート非合格。
- 保護のため実ゲーム用32bit pointer境界は残したまま、selftestのみ64bit自プロセスreadに修正した。
根拠 BATTLE_LIVE_READONLY_PROBE_SELFTEST_20261021.json。
## 完了基準・再開・障害記録
技術実証準備の従来主観スコア47.5%を据え置き。Work引継ぎの客観的ゲートは2/9、原作⇄外部EXE⇄原作の実機戦闘往復0件。G0合法実戦、G1同run開始packet、G2 native Task/VMの停止再開、G3無変更往復、G4終了一回commit、G5戦略Golden一致、G6クラッシュ・セーブ復帰が未達。
RECOVERY BRIDGE-20261021-RC06-01 OTHER/RESOLVED: battle_finish_native_segments_stage6_20261021.pyの初回Python改行SyntaxErrorを括弧追加で修正、同一原本PEから結果JSON成功。
RECOVERY BRIDGE-20261021-RC06-02 OTHER/RESOLVED: live probe selftest初回は64bit Python自己pointerの4GiB超でValueError。selftest限定でAPI直接読取りに修正、0xBADC0FFE読取PASS。実原本メモリ読取なし。
RECOVERY BRIDGE-20261021-RC06-03 OTHER/RESOLVED: Stage6 Markdownファイル生成のJS記述に意図しないバッククォートが入り、生成前SyntaxError。文章をコピペ可能な分割文字列に修正し保存・読み戻し。安全拒否や情報喪失ではない。
過去の安全拒否済み解析を迂回して再試行していない。正式レーンowner HANDOFF、MASTER、Git、Work、スケジュールは未変更。
次回研究ID BRIDGE-20261021-RESEARCH-07。原作save2 C-NB02を合法UIで開始した時の正規読取と、実native以後の一回commit・ロード復旧を最優先。現在の手元実機には該当Vahren.exeプロセスなし。

## 補足 F06-06｜Windowsモジュール実ベース列挙のセルフテストも成功
battle_native_readonly_modulebase_selftest_20261021.pyを別途作成し、自己Python64bitプロセスでWin32 EnumProcessModulesEx/GetModuleFileNameExWによる実loadbase取得、さらにReadProcessMemoryでMZ先頭2byte一致を確認。証拠 BATTLE_BRIDGE_MODULEBASE_SELFTEST_20261021.json。これはユーザーゲームではなく自己プロセスのみ（実原作メモリ取得0、WOW64実機時の成立はVERIFY）。既存のReadProcessMemory単体セルフテストに加え、モジュール位置特定経路も実行可能と確認した。
