# 迫真戦記 ver0.67 REA｜P0 D3D9補助初期化のFPU最小誤差探索と停止条件
研究ID: REA-LOCAL-20261027-07H-P0-D3D9-FPU-MINIMA-NONTERMINATION-STATIC-01
日時: 2026-10-27 07時台 JST。状態: PC-SAVED / STATIC / VERIFY / NOT READY。Golden: NOT RUN。
対象PE32 x86 SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧Ghidra DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 DB SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 研究対象と従来成果との差分
06Hで0x00559690後段の間接CALL18件、直接CALL site 0x00559830 → 0x00559990、子関数の間接CALL群をSTATIC確定済み。今回は既存のGhidra全関数擬似Cを再収集せず、子関数0x00559990（0x00559990～0x00559D22）の**ループ停止条件をx87 status byteと実命令から追加検証**。06Hの43検査と今回の58検査は別検査項目であって、解析完了関数数として合算しない。
Ghidra search.py function/callers/callees/relatedをread-only実行。direct callerは0x00559690のsite 0x00559830。Ghidra pseudoは機械出力・型推定であり、独立の関数別REA 5方法証拠ではない。

## NEW STATIC: 「収束許容差」ではなく「2座標がともに過去最小から悪化」で終了
0x00559B49: FLD [0x0063B0A8] → 初期走査値float32 = -2.0。
0x00559B63: FLD [0x0063B150] → 2本の最小誤差初期値float32 = 1,000,000.0。
0x00559B77～0x00559C1D: D3DXMatrixLookAtLH / D3DXVec3Unproject ×2 / D3DXPlaneIntersectLine の計算・反復。
0x00559C1F～0x00559C3E: 誤差e1 = abs(-1.0 - 交点座標1)。double基準値 [0x0063B148] = -1.0。
0x00559C42～0x00559C5F: 誤差e2 = abs(1.0 - 交点座標2)。
0x00559C6B/0x00559C7C: FCOM/FCOMP → FNSTSW AX; 0x00559C73/0x00559C80 TEST AH,5 → JP/JNP判定。
有限のordered値では、0x00559C83のJNP→0x00559CDB退出は **e1 > best1 かつ e2 > best2** の場合のみ。どちらか一方が等しい・改善したなら続行する。
0x00559C87～0x00559CA7: それぞれ旧best > 新誤差の時だけ最小値を更新。等値・unorderedでは更新しない。Ghidra疑似Cのwhile(true)と整合。
0x00559CB3 / 0x00559CCC: float走査値からqword [0x0063B140] = 0.009999999776482582を減算、float32へ格納。
0x00559CBD / 0x00559CD6: 共通入口0x00559B77へ無条件後方JMP。対象ループ内に独立した反復回数・整数カウンタ上限は見つからない。
## NEW VERIFY: 未終了条件と数値停滞
判定は「両方の誤差が過去最良より大きい」であり、「誤差が所定閾値未満になった」ではない。単調改善・片側だけ改善・片側等値が続く条件では有限の反復上限をコードから保証できない。
x87 unordered比較（NaN等）は上記JP/JNP判定を通常のordered比較と異なる経路へ進めるため、仮に交点の一座標にNaNが継続出現すると終了条件が成立しない可能性がある。NaNのゲーム内到達性とFPU例外マスク状態は未確認。
float32へ格納するため、合成入力 z=-262144.0 に対して float32(z - 0.009999999776482582) == z を独立検査で確認。一方z=-131072.0では減算が反映される。もしループが長時間退出せずこの領域まで進めば更新量が丸め落ち、同一走査値を繰り返す懸念がある。ゲーム実機で到達した証明ではない。
0x00559B69 は IAT 0x006092E4 (=D3DXPlaneIntersectLine) をEBXへ格納し、0x00559C1D CALL EBXの直後0x00559C1Fで出力浮動小数点を読み込む。戻り値EAXをその場で検査していない。交差失敗時のAPI結果・出力未更新・有限値保証はVERIFY。
これは**潜在的な初期化ハング条件**の静的発見であり、実ゲームで無限ループが発生するという確定結論ではない。CPU負荷や実ゲーム挙動も直接測っていない。

## 認証と成果区分
原作PE・旧/V9 DBのSHA256、両SQLite quick_check、既存06H 43/43、旧RUN_RESULTの対象SHA/REA6.1.0/Ghidra12.1.4、最終syncログのWave1～5=64/64を照合。QUEUE/PROGRESSには既存EPERMによるstale不整合が残るため、修正・再試行せず旧RUN+syncを優先する。
今回の独立静的監査 58/58 PASS。合成float32・比較モデルは原作ゲームGoldenではない。新規正式VERIFIED=0。正式TODO/VERIFY/BLOCKEDの書込差分は各0。Golden実測PASS=0、strict MATCH/完全複製率=未測定。
5種証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。全5種のREA証拠を追加取得していないので0件VERIFIED。
## 次の合法研究・再開位置
1. P0: 0x00559C1Dの交点出力がNaN/無限/未初期化になり得る初期入力、D3DXPlaneIntersectLineと2件のD3DXVec3Unproject失敗時の挙動を、元の保存静的資料から限定検証する。実機証明は別。
2. P0: 0x00559990を呼ぶ0x00559690の初期値・3Dオブジェクト生成の条件と、0x00879838の値consumerを追跡し、反復不成立条件の到達性を狭める。
3. P1: 第二BGMベースディレクトリDAT_0068B38Cの書込元とパスサイズ上限は従来VERIFYを維持する。
新規REA/Ghidra/ゲーム/Work起動なし。禁止VA 0x5710C0..0x571500、既拒否Wave6・REA exportへの再試行なし。MASTER/QUEUE/PROGRESS/既存RUN/A～E/原本/Git/スケジュールは変更しない。ownerフォルダ内の新規ファイルだけ保存し独立readbackする。
