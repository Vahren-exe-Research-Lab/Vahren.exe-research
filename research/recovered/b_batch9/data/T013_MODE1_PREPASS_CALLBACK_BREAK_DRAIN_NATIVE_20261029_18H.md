# B-20261029-1813-T013-PREPASS-CALLBACK-BREAK-DRAIN-01｜T013 mode1候補走査前の効果queue callback / break / drain結合
Owner B：T013主、T024/T028照合対象｜2026-10-29 18H JST｜STATIC ORIGINAL-PE ASM＋V9／INFERRED／VERIFY／NOT READY

## PRECHECK・一次出典
- Desktop Commander Local Compact接続可。MASTER最終E公式cp196/READY596は旧値、ANALYSIS_LANES_PROTOCOL・LANE_B_HANDOFF・B担当資料・既存復旧を先読。PC上の旧search_index/README.mdとBUILD_MANIFEST.jsonはENOENT（10/29整理後）、代わりに公式00_START_HERE_UNIFIED_V9_20261023.mdとV9 CLIのみ読取。
- V9 verify実行結果=V9_INDEPENDENT_READBACK_PASS；DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。PC標準V3変更0、Ghidra再解析なし、active.lockなし。
- 原作解析用PE rea_lab/targets/hakushin067_Vahren.exeを限定read-only：実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原本ゲーム実行・変更なし。
- 復旧状態：SAFE134 byte検証/HOLD21安全関連保留、旧B147中54件1byte差、2026-10-25 14H研究原文未回収は前回確認のままOPEN。今回全件の再同期・semantic dedup完了は主張しない。拒否済VA/拒否済操作を再試行しない。

## ORIGINAL-PE ASMとV9静的証拠（新規増分）
- CALL先0x49D1B0は旧17Hの0x44CFA0 E8で到達すると既知（重複計上0）。今回その実引数基盤を確認：0x44CF80 CMP manager[EBX+0xA5],0 →非0ならprepass無；0x44CF8A CMP [EBX+0x18],0、0x44CF8Eで[EBX+0x20]=4、+0x18非0ならprepass無。両フラグ0の時0x44CF97 `MOV ESI,[EBX+4]` / 0x44CF9A `ADD ESI,0x504` / 0x44CFA0 CALL0x49D1B0。ESIはEBXと同一ではない。
- 0x49D1B0ではbase=ESIの+0x1EEBBC（begin）・+0x1EEBC0（end）の差を4で割った要素数を取得（0x49D1B0/1B6/1BF）。0x49D1C4 `TEST EAX,EAX`、zeroなら0x49D1ECへ。非zeroは0x49D1CC `[begin+EDI*4]`の要素pointerを取得し0x49D1CF `[ECX]` vtable→0x49D1D1 slot+0x58→0x49D1D4 `CALL EDX`。
- callbackごとに0x49D1D6..0x49D1EAでbegin/endを再取得し現在のlengthと更新済みEDIを比較するため、反復回数は初回固定長ではない（callbackによるvector変更の有無・安全性はVERIFY）。element型とvirtual+0x58の効果もVERIFY。
- 0x49D1EC..0x49D201：queue begin!=endかつ`[ESI+0x1EEC3C]==2`の場合に限り、0x49D203 `[ESI+4]` objectのvtable+0x24を0x49D212 CALL。0x49D20B PUSH0、0x49D20D PUSH 0x631B78。原PE文字列0x631B78はASCII `break\0` を直接確認。"break"が実際の敗走/戦闘打切を意味するかはVERIFY。
- 0x49D214..0x49D240：begin!=endなら0x49D224 `MOV EAX,ECX`→0x49D226 `SUB EAX,ECX`でコピー長0を生成、0x49D236 E8→0x5B6720（V9がmemcpy系と表示）後0x49D240 `[ESI+0x1EEBC0]=begin`へ更新。vectorの論理サイズをzeroにする。コピーhelperの例外/副作用とobject所有権解放は未確定。
- 0x44CFA5..0x44CFABの既知`[EBX+0x48]==[EBX+0x4C]` group走査skipはこのprepassの後。したがってmode1 vslot+0x68候補実行が0件でも、manager前提条件次第で別queue callback / break送出 / drainは先行し得る（CONTROL-FLOW INFERRED、実機NOT OBSERVED）。
- 関数0x49D1B0はV9 callers 7件（0x449765,0x449E5C,0x44B770,0x44C767,0x44CE70,0x44CFA0,0x522121）；今回調べたのは0x44CFA0経路のみで、他6入口のESI provenance・到達条件はVERIFY。
- PE original窓0x49D1B0 length163 SHA256=84A3BC483316BAB2A3FF176B1A15F8DAE076268771066B6BB521596FDDCA1436、native disassemblyとV9擬似Cを照合。Ghidra prototype void/indirect vslotはABI未確定のためCソース同等とは扱わない。

## DEDUP・失敗・Golden・再開
- B所有data/T011,T012,T013,T024,T028*.md＋HANDOFF計364件、0x44CF97/0x49D1C4/0x49D1CF/0x49D1FA/0x49D20D/0x49D236の先行literal一致0。0x49D1B0自体は17H既知（2 hit）で再計数0。別表記・他owner・欠落10/25資料の完全意味重複は未完了。
- 解析時PowerShell/Python引用符に起因するParserError 1件はOTHER/RECOVERED、同一許可PCの通常read-onlyを正しい引用符で再実施。安全拒否0。原本/他lane/REA/MASTER/Git/Work/設定/schedule変更0。
- Golden必要条件：未改変原作EXE・x20改変前DAT、同一SAVE/MAP/入力/RNG、manager +0xA5/+0x18/+0x20、ESI派生元、queue begin/endと各vslot+0x58の前後、+0x1EEC3C=2/非2、break通知、group空/非空、下位vslot+0x68・可視移動/敗走・次tickを同一合法runで観測。DESIGNED_NOT_RUN。
- 原作Gameplay Golden PASS0／strict MATCH0／新B正式READY0／E MASTER統合0／Task DONE0。STATUS=STATIC/INFERRED/VERIFY/NOT READY。
- NEXT：0x49D1B0他6入口の正しいESIとmanager段階、virtual+0x58型、`[ESI+0x1EEC3C]` writerの状態意味、0x44CF80 group producer、T024 AI/T028敗走との実対応。拒否済領域には接触しない。