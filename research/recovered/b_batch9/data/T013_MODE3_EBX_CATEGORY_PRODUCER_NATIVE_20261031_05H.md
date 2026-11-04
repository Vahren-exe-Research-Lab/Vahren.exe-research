# B-20261031-05H-T013-EBX3-INPUT-01｜mode3枝のcategory引数はEBX=3、後段の3→6/7変換（原作ASM）
Owner: B/T013（T024連携候補）｜2026-10-31 05H JST｜STATIC / INFERRED / VERIFY / NOT READY
## 先行資料・復旧・範囲
- Desktop Commander Local CompactでMASTER cp196/READY596（直近の既確定値、今回は全件再計数なし）、evidence/ANALYSIS_LANES_PROTOCOL.md、B HANDOFF、T011_DATA_MODEL.md、T012_BATTLE_CALC.md、T013_AI.md、T024_HAKUSHIN_BATTLE_AI.md、T028_MORALE.md、2026-10-29復旧索引、04H詳細を読取。
- 既拒否済みB要約3件および関連保留資料はBLOCKEDのまま、代替経路での再実行0。Library147件のうち54件byte差、10/25原文未回収、全レーン意味的重複照合はOPEN。今回の旧原作実行0、Ghidra全体解析0。
- 原作解析用PE 2,910,720 bytesの今回実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。局所PE窓0x44BBB0..0x44C78F SHA256=038074665B67A98162A469F99444886898148A5DF2EB2BD939132BEB5EA61CE2。
- 統合V9 HAKUSHIN067_UNIFIED_V9_20261023.sqlite 実SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、SQLite mode=ro quick_check=ok。0x49D1B0 V9擬似CはSTATIC・ABI未検証。既知旧README/BUILD_MANIFEST/search.sqlite ENOENTのため2026-10-29現行V9を明示使用。
## 新規原作x86命令上の差分
- 0x44C70F～0x44C71Aのx87結果ゲートを通ると、0x44C71C manager=[ESP+0xC8]、0x44C72B MOV EBX,3、0x44C730 MOV [manager+0x20],EBX。ここでmode3設定とcategory引数producerが同一値3を共有。
- 0x44C733..0x44C74D はmanager+0x38/+0x3CのUnit*配列を巡回し、各要素+0x1C==0なら0x44C73F PUSH0 /0x44C741 PUSH0 /0x44C743 CALL0x5690C0。先行04Hの行動指示writer0x577220とは別処理。
- 0x44C74Fのmanager+0x18非零または0x44C75Eのmanager+0xA5非零なら0x49D1B0をskip。両方0なら0x44C755..0x44C767でESI=[manager+4]+0x504をセットしCALL0x49D1B0。その関数はvectorを巡回しvtable+0x58間接CALLを行い、条件によりvtable+0x24へ'break'を送る。間接calleeの副作用・ABIはVERIFY。
- 0x44C76C PUSH EBX /0x44C76D PUSH EBP /0x44C76E CALL0x449500→0x44C773 JMP0x44CC23。0x49D1B0はネイティブ本体内のEBX一時使用をPUSH/POPで保護し、0x5690C0もEBXを保存するが、0x49D1B0内vtable間接CALLを含むため全calleeのregister preservationは未実機検証。標準x86非volatile規約を満たす条件で引数category=3が成立。
- 0x449500の元PE 0x449500..0x4495D7 SHA256=8EE452BCE82BF92A932692E18BE9E567537F197F2B62DFB97AE709427B6E384A。manager+0x78==+0x7C（Unit配列空）なら0x44950F→0x4496EDでこの関数のUnit更新なし。非空かつmanager+0x98>10ではcategory3を保持し、<=10では0x44952D..39から3→6、さらにgroup+0x1EF244!=0かつmanager+0x18==0なら0x4495C3..D7で6→7。
- よってこの直接CALL経路のラベルは条件付きで3='push'、6='advance'、7='even'（既23Hラベル表）。category3はcategory1/7にのみ掛かるbtl_limit時間閾値枝0x44953B..B7を通らない。ラベルは最終行動・移動/攻撃成功の証拠ではない。
## 重複・保留・受入
- B所有T011/T012/T013/T024/T028のMD 398資料を保存前に検索し、0x44C72B一致0、0x44C755一致0、研究ID一致0。0x44C76Cは04H既知1件で新址扱いせず。旧21Hのmode+0x20=3、旧23Hのラベル、旧04Hの12 direct callerは重複計上0。新規差分はEBX producer→可変引数direct site→0x449500 3/6/7分岐の接続。
- VERIFY: vtable間接CALL先のEBX保存と副作用、Unit配列空/非空の合法到達、manager+0x98/18/A5・groupflag実値、カテゴリ別RNG消費、Unit+0x1E4FC/+0x1E4F8書込と翌tick、間接/仮想経由の他のcategory4/5入力。
- Golden必要条件: 無改変ver0.67原作EXE・20倍化前DAT、同一SAVE/MAP/input/RNG、上記各gateとUnit更新前後・翌tickを同一runで実測。旧原作Gameplay Golden PASS0・strict MATCH0・新規正式B READY0・E MASTER統合0・Task DONE0。STATIC/INFERRED/VERIFY/NOT READY。
- 次回: 0x49D1B0内vtable+0x58呼出先の合法な静的特定（既拒否範囲を除外）、0x44C778/0x44C789との条件分岐比較、0x577220後の実移動対象制御、T011召喚EXP・T012ダメージ・T024通常AI・T028士気P0。原本・MASTER・他lane・REA/dev_lab/Git/Work/設定/schedule書込禁止を継続。
