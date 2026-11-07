# B-20261030-17H-T013-MODE2-TWO-STAGE-SHUFFLE-RNG-01 | 2026-10-30 17H | T013/T024 mode2の距離木の後段シャッフルと候補効果
分類: STATIC / INFERRED / VERIFY / NOT READY。原作Gameplay Golden PASS=0、strict MATCH=0、新規B READY=0。
担当B。ソース: 統合V9の原作対応E8 native CALL indexおよびGhidra擬似C。原作ゲーム非実行、再逆コンパイルなし。
原作EXE参照SHA256(統合manifestの識別値): E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回EXE現物独立再hashなし。
統合V9 DBは本runの既存validator verifyでV9_INDEPENDENT_READBACK_PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、PC標準変更なし。
## 前runとの境界
16H既知: 0x44C0FE以降で2候補木のUnit座標+0x220/+0x224から二乗距離を構築し、0x44C1AD/0x44C1BCで距離木へ挿入。同距離ノードは独立全採用保証なし。本runでは再計上しない。
## 新しい直接CALL接続 (統合V9 native E8 index)
0x44C310 CALL 0x44D730 (E8 1B140000)、0x44C323 CALL 0x501CA0 (E8 78590B00) はmanager+0xA7 != 0 の第1候補処理側。
0x44C43B CALL 0x44D730 (E8 F0120000)、0x44C44E CALL 0x501CA0 (E8 4D580B00) は後続の第2候補処理側。後者は前者の+0xA7 gateとは別配置。
第1候補で0x44C3C3 CALL 0x5690C0、0x44C3D6 CALL 0x579AA0、第2候補で0x44C541 CALL 0x5690C0、0x44C554 CALL 0x579AA0をnative E8 indexで確認。
0x501CA0内部には0x501CBBと0x501CCDの2つのCALL 0x5B6EAB (乱数候補) が記録されている。
## 擬似Cで確認できる条件付き流れ
0x44BBB0擬似Cでは、木の候補を0x44D730経由でvector化した後、範囲非空なら0x501CA0を呼び、要素を並べ替える。第1段はmanager+0xA7 != 0の時のみ入る。
第1段は候補の+0xC4 != 0かつ候補木先頭のdoubleキー <= _DAT_0063B2D8 の条件を経て、別木のkeyとの照合結果で0x5690C0と0x579AA0へ進む。
第2段は別の木から候補vectorを作りシャッフル後、登録nodeの+0x18 payload/keyと別木を照合して0x5690C0/0x579AA0へ進む。第2段の条件は第1段と同一ではない。
0x501CA0擬似C: index=1から各位置iで0x5B6EABの低15bitを取得し、(i+1)で剰余、位置iと位置rをswap。これはFisher-Yates型の逐次シャッフルと解釈できる(INFERRED)。
候補数n<=1ではシャッフル乱数消費0、2<=n<=32767では通常各要素1 drawでn-1 draw。n>32767では追加RNG分岐を持つため単純n-1と断定しない。
距離の木順そのままで最終ターゲットを決める実装ではなく、候補vector化後の乱数状態が優先順位・最終行動に影響し得る(INFERRED)。Ghidraのvoid/fastcall等はnative ABI証明ではない。
## 未確認・重複と受入
今回はT013 owner全1423行、B HANDOFF直近700行、16H詳細で0x44C323/0x44C44E/0x501CA0/0x501CBB/0x44C541先行文字列0、新IDも0。Bの他資料・10/25欠落・他lane全文の意味的重複はVERIFY。
0x44D730擬似Cにはunreachable warningが多数あり、vector生成の正確なABI、+0xC4/keyの型と閾値、0x5690C0の契約、同一キー処理、乱数状態共有・候補数はASM/DAT/実機でVERIFY。
原作Golden必要条件: 無改変EXE、x20改変前DAT、同SAVE/MAP/input/RNG、manager+0xA7 0/1、候補木0/1/2/複数・同/異距離、各シャッフル前後vector、0x5B6EAB draw回数/状態、0x5690C0実引数・選択Unitと翌tick。
新しい原作実機Golden PASS0・strict MATCH0・正式READY0。次に0x44C310/0x44C43B引数、0x44D730/0x4634F0 native範囲操作、0x44C3C3/0x44C541のABIと2段の優先条件を確認。T011召喚EXP/T012 damage/T024通常AI/T028士気も未解明P0。
復旧: 11H拒否済の3要約追記はBLOCKEDのまま再試行0。旧SAFE134/HOLD21、Library54件1B差、10/25原文未回収OPEN。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/スケジュールは未変更。
