# T028 退却先選択：Spot候補の容量・予約計数のstrict gate（22H）
研究ID: B-20261029-2213-T028-RETREAT-SPOT-CAPACITY-STRICT-GATE-01
日時: 2026-10-29 22:13 JST / Owner B T028（T011/T013/T024参照） / STATIC ORIGINAL PE ASM + V9 GHIDRA / INFERRED / VERIFY / NOT READY

## 前提・復旧・安全
Desktop Commander Local Compact ONLINE。MASTER最終記録cp196/READY596は以前の正式値であり本回再集計・MASTER編集なし。ANALYSIS_LANES_PROTOCOL、B5 owner、B HANDOFF、B復旧索引と旧21H詳細を読み取り専用で照合。
旧SAFE134/HOLD21、Library B147中54件の1byte差、10/25旧原文、既拒否8件は未解決。過去の拒否操作・禁止領域への再試行や迂回なし。
原作解析copy rea_lab/targets/hakushin067_Vahren.exe の実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。統合V9 sqlite実SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。ゲーム/Ghidra再実行なし。

## 新規原作ASM・分岐
0x5AC308で候補ESIとarg1を比較し同一候補を除外、0x5AC315でESI==0を除外、0x5AC32A CALL0x5E72E5 RTTI照合、0x5AC334失敗なら0x5AC3E2へ。
RTTI通過後0x5AC33A MOV EBP,[ESI+0xA0]、0x5AC342 CALL0x597B00、0x5AC347 CMP [ESP+0xC0],EAX、0x5AC34E JNE0x5AC568で候補走査へ戻る。arg2と0x597B00返却参照が一致する場合だけ次の容量比較へ。
0x5AC354 MOV EDI,EBP→0x5AC356 CALL0x597A50、0x5AC35B ADD EAX,[EBP+0xB8]、0x5AC361 CMP EAX,[EBP+0x88]、0x5AC367 JL0x5AC57D。**signed32で (0x597A50の計数値 + 候補+0xB8) < 候補+0x88 のときだけ即採用**。等号は採用しない（通常非overflow前提）。
0x5AC57D..0x5AC5D8はcleanup後EAX=EBPを返すことを元PEで確認。前21H既知0x568329/2Fは、採用後のSpot様EAXを保存しEAX+0xB8を++する。+0xB8は単純参照カウンタと断定できず、**容量計算に投入される予約・占有計数候補**に分類を訂正。
容量不足時0x5AC36D CMP BYTE [ESP+0xC4],0 / 0x5AC375 JE0x5AC3E0。21H既知の退却CALL 0x5682C3 は第3引数0のため、0x5AC377→0x597D50の追加候補を探索するbranchを通らず、通常の別候補探索経路へ進む。直ちに全検索失敗とは限らない。
0x597A50のV9擬似Cはlinked要素にFUN_00402710→0x467DE0、戻り非NULLかつ対象+0x78!=0で値を加算する。実体の型・戦略部隊数との対応は未確証（GHIDRA_STATIC）。0x597B00のV9擬似Cはarg1由来+0xB0、+0x2E0の木構造探索と返却先+0x58候補を含み、Spot本人と呼ぶのは暫定。

## 根拠・非重複・Golden・次
元PE Capstone読取: 0x5AC308..0x5AC424、0x5AC568..0x5AC5D8。128byte窓0x5AC308 SHA256 CA88DB38C5CD5B519862C972C633BD6041CA24DE4DBA6AE04569B232B86D6221。V9 functions 0x5AC1A0/0x597A50/0x597B00、原PE E8 CALL site 0x5AC342/0x5AC356。
旧21H既知: arg3=0、secondArg+0x10!=0、退却先不存在時の文字列・Unit vtable抑止。今回の増分: arg2同一性gate、0x597A50+Spot+0xB8とSpot+0x88のstrict比較、即採用とfallback抑止、+0xB8意味分類の補正。旧結論を再計上しない。10/25欠落研究と他lane意味的完全dedupはVERIFY。
Golden DESIGNED_NOT_RUN: 無改変原作EXE・x20前DAT、同SAVE/MAP/input/RNG、同じSpotで計数+0xB8が容量-1/容量/容量+1、arg2一致/不一致、候補0/1/複数、選択後+0xB8増分と別機構による減分、表示・翌tickを同run記録。signed overflow/exceptionも別VERIFY。
STATUS: STATIC/INFERRED/VERIFY/NOT READY。原作Gameplay Golden PASS0、strict MATCH0、新規B正式READY0、E MASTER統合0、Task DONE0。次: 0x597A50実ASMと+0xB8減算writer、0x597B00参照先実体・候補列挙順、0x52CCF0通知受入、T024 AIとの上流連結。
保存対象は本B詳細・data/T028_MORALE.md・evidence/LANE_B_HANDOFF.mdのみ。原本EXE/ZIP/DAT/SAVE、MASTER/他owner/REA/dev_lab/Git/Work/設定/スケジュール不変更。
