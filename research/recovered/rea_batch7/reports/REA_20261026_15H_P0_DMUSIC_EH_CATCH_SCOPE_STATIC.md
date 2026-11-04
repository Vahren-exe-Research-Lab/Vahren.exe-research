# 迫真戦記ver0.67｜REA 15時台 P0 DirectMusic bad_alloc 例外スコープ監査
研究ID: REA-LOCAL-20261026-15H-P0-DMUSIC-EH-CATCH-SCOPE-STATIC-01
日時: 2026-10-26 15時台 JST。状態: PC-SAVED / STATIC / VERIFY / NOT READY。
原作研究用EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
既存Ghidra search.sqlite SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 旧知見と新知見の境界
既報14H: debug設定負数、配列 new の bad_alloc候補、0x005B5C11 tail-JMP、初期化途中の後片付け未解決。これらは新規成果に再計上しない。
今回新規: MSVC EH3 FuncInfoの実データを原作PEから直接読取、3段階の例外ハンドラ・unwind map・catchスコープを突き合わせた。
検索DBからCALL: 0x004BD3E4 (0x004BD2A0→0x004BE480)、0x00555DEF (0x00555CD0→0x004BD2A0)を照合。

## 独立静的証拠
- 子0x004BE480: EH handler 0x005E79BB→FuncInfo 0x00641AB0（magic=0x19930522, maxState=1, nTryBlocks=0）。
- 子unwind map 0x00641AA8: state0→state-1, cleanup 0x005E79B0。機械語 0x005E79B4 CALL 0x005B6BBB（free系）。
- 0x004BE4E0: +0x70管理配列確保、0x004BE4EB: pointer保存。これらはまだEH state=-1の段階である。
- 0x004BE522: 別の0x5C byteオブジェクトを確保。0x004BE530でEH state0設定、0x004BE56Fでstate=-1へ戻す。unwindのfreeはこの一時オブジェクトに対するものと整合する。+0x70配列のfreeはこの子EH mapに存在しない。
- 親0x004BD2A0: EH handler 0x005F2A36→FuncInfo 0x0064C28C（magic同一、maxState=7、nTryBlocks=0）。7つのunwind actionは一時new領域free、静的フラグ解除、局所文字列後片付け等であり、子の管理配列freeではない。
- 上位0x00555CD0: EH handler 0x00600A68→FuncInfo 0x00657D10（maxState=3, nTryBlocks=1）。TryBlockMap 0x00657CFC: tryLow=0, tryHigh=0, catchHigh=2, nCatches=2。
- Catch descriptor 0x00657CDC: RTTI名 `.?AVGameException@@`、handler 0x00555EBC。第2descriptor 0x00657CEC: catch(...)、handler 0x00555F02。**catchが存在しないわけではない**。
- ただしBGM初期化call 0x00555DEF時のowner EH stateは-1のまま。保護対象のstate0設定は0x00555E3A（0x004B9930呼出0x00555E3D直前）、state-1復帰は0x00555E45。よって、この2本のcatchは **0x00555DEF経由のbad_allocを捕捉するスコープではない**。
- 子0x004BE480と親0x004BD2A0はnTryBlocks=0。C++ EH登録自体があっても、それだけでcatchが存在すると解釈しないこと。

## 結論と未確認
[STATIC-CONFIRMED] 配列確保時のbad_allocは少なくとも上記3関数の表示されたcatchに入らず、更に上位へ伝播する構造。
[VERIFY] 2番目の0x5C byte newでbad_allocが発生すると、先に確保された+0x70配列についてこの子unwind mapによる解放が確認できない。上位の別クリーンアップ、process exception handler、実際のリーク/異常終了は未実測。バグ確定には昇格させない。
[VERIFY] GameException/catch(...)は別のtryスコープのみ。BGMのエラーを捕捉するという以前の一般的推測があれば訂正する。
[DESIGNED / NOT RUN] 配列new失敗、0x5C new失敗、InitAudio失敗を独立注入し、catch到達、+0x70 free、COM Release、終了コードを比較する。原作実機Golden PASS=0。

## 監査と取扱い
監査 `REA_20261026_15H_P0_DMUSIC_EH_SCOPE_AUDIT.py`: PE実バイト・Capstone・MSVC FuncInfo/UnwindMap/TryBlockMap・Ghidra SQLite read-only・既存同期ログを照合。初回41/43（2つのhandler-stub未採取）。解析対象にhandlerの機械語を追加して最終43/43 PASS、保存後再実行を別途確認する。
REA5種: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規正式VERIFIED=0。旧Wave1–5=64/64は2026-10-11の保存同期記録、二重計上せず。正式QUEUE/PROGRESS TODO/VERIFY/BLOCKED書込差分=0/0/0。完全複製率・strict MATCH未測定。
PC接続OK、active.lockなし。メモリ空き約18.99GiB、CPU 37%（単発PC全体観測）。監査単体約0.405秒。総作業時間未測定。新規REA/Ghidra/原作ゲーム起動=0、Work=0。
原本ZIP/EXE/SAVE、A～E/MASTER/T018/dev_lab、旧run/証拠、Git・公開先・スケジュールは変更しない。以前の安全拒否対象への試行なし。13・14時台の過去OFFLINE-UNSYNCED成果は未同期。
## 次回
上位0x00555CD0のcallerと更に外側のcatch（特にbad_alloc/例外全般）を検索DB→限定ASM→FuncInfoで追跡。次いで+0x70配列の全書込・free xrefsを限定調査。上位復旧確認前にGolden成功・クラッシュ確定・リーク確定とはしない。
