# T028 退却ベクタ補助の実副作用：RB-tree key範囲削除（flag0も削除）
研究ID: B-20261030-0113-T028-SPOT-INDEX-EQUALRANGE-ERASE-01
時刻: 2026-10-30 01時台 JST / owner B / T028 / STATIC ORIGINAL ASM + V9 STATIC PSEUDOC / INFERRED / VERIFY / NOT READY

## 証拠源・復旧・境界
Local CompactでPC ONLINE、MASTER cp196/READY596（古い公式値）、B規約/HANDOFF/5 owner・復旧索引を先読。旧SAFE134/HOLD21、B147の54件1-byte差、10/25旧原文はOPEN。
原作解析用PE rea_lab/targets/hakushin067_Vahren.exe 実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。ゲーム原本は未起動・不変更。
統合V9 SQLite実SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、既存verify結果V9_INDEPENDENT_READBACK_PASS。標準V3を切替えない。旧README/BUILD_MANIFESTは既知ENOENT（OTHER）。Java/Ghidra/active.lock検出0。

## NEW ORIGINAL ASM：先行キーと全ベクタ要素で同じ削除ペア
0x59845F PUSH EBP(第2引数)、0x598465 ESI+=0x1C、0x598469 E8 CALL0x416080；0x59846E/472で戻りの2iteratorをpushし、0x59847C E8 CALL0x415CF0。このペアはvector+0xD4/+0xD8走査より前に無条件で現れる。
0x598481/487 vector begin/end読出、stride 0x1C。要素ごとに0x5984C7 E8 CALL0x416080→0x5984DA E8 CALL0x415CF0、flag分岐0x5984DFより前。したがってflag0でも、初回+各vector entryに対応するtree範囲の削除が実行される。
0x416080の原作ASM 0x4160A7/ABは探索keyの+0x10/+0x14を取得。V9擬似Cではtree node+0x1Cとの比較を0x402C40に委ね、2 iteratorをoutparamへ格納。標準的なequal_range様取得と推定、比較等価性/多重key/ABI exactはVERIFY。
0x415CF0原作ASM: 0x415CFC first==head.begin, 0x415D00 last==headなら0x415D0A→0x416870による全消去、0x415D12..1D sentinel更新、0x415D23 tree count0。その他は0x415D34 first!=lastを検査、0x415D8F→0x416220でnodeを逐次除去。よって読み取り専用探索でなくtree erase-rangeの実副作用をもつ。
0x5984A8はvector=0でも初回key処理の後に跳躍。前00Hで既知のflag0による0x402710/0x467DE0/0x463590省略はこのtree削除を抑止しない（既知flag分岐の再発見計上0）。

## 誤差・非重複・Golden
original PE function-window SHA: 0x598450/366B=0E1746CD6B13007270F6D2F853795925CBBE89A231FCD5E5DA5CF4013DC79CAA；0x416080/408B=CE446C931EAF2E9EE1347094B8E5CD13814065A267F3D5D34FFD27182D0F56C2；0x415CF0/182B=66E4BA9721B6187C1DF5B3CF72410CCB077F5FD393B07142FB84D33349200506。
PE E8 native bytes: 0x598469=e812dce7ff、0x59847C=e86fd8e7ff、0x5984C7=e8b4dbe7ff、0x5984DA=e811d8e7ff、0x415D0A=e8610b0000、0x415D8F=e88c040000。全て原作解析用PE読み取り専用。
B関連371 Markdown照合で0x598469/0x59847C/0x415D0A/0x416220先行文字列一致0、0x5984C7/0x5984DAは前00H既知として再加算0。10/25旧原文・他lane意味的重複はVERIFY。
初回PE RVA変換せずdisassemble=empty（OTHER/RECOVERED、書込0）、正規VA−imagebase再照合で修復。安全拒否0・既拒否別経路迂回0。
原作実機Golden DESIGNED_NOT_RUN：無改変旧EXE/x20前DAT、同SAVE/MAP/input/RNGでflag0/1、vector0/1/2、tree空/一致/不一致/複数keyを分け、delete前後tree node/count/Spot参照/+0xB8と可視退却・翌tickを合法観測。Gameplay PASS0、strict MATCH0、新B READY0、E MASTER統合0、Task DONE0。
次=0x402C40比較符号・tree entry+0x1C keyの型、0x416220 destructor/erase後残りtree count、0x495580前後の+0x1B4関係、T011/T012/T013/T024 P0。原本/他owner/MASTER/REA/dev_lab/Git/Work/設定/automation不変更。
