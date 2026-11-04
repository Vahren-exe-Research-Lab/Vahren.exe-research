# 研究B｜0x4E7ED0 非grid分岐の二重半径gate（2026-10-13 01:17 JST）
証拠ID: B-20261013-0117-01 / Owner T012/T013 / Status: VERIFY-PENDING-READBACK → 最終HANDOFFのREADY記録を優先。
種別: CONFIRMED-SAVED-GHIDRA-ASSEMBLY（局所関数内の正常分岐）／実機・FPU・原作環境はVERIFY。
既存 T012_BATTLE_CALC.md §60 の「非grid時に有効半径で候補を判定」を増補するだけ。4E7ED0本体全体の新規復元、caller xrefの再探索、拒否済0x5470F0→4E7ED0方向/RNG crosswalkの代替保存ではない。
一次資料: rea_lab/decomp_task/runs/20261009T224617297Z/4E7ED0_procedure_assembly.json（read-only）。
evidence_id=ev_4b52004127ec175ac9c1971618398099d6a721f800f5f5b083599764a1aab2a8、source SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（過去の保存値）。
対象: 0x4E7F99..0x4E8202（param1+3C==0の分岐）。+3C!=0の方向grid単一セル分岐は旧§60にあり再計上しない。

## 新規の局所確定：領域列挙用と候補合格用で半径が別々
[ACTOR WINDOW] 4E7F9D/7FA6は actor Unit+B0 と+A8 を非zero判定。双方0のときだけ4E7FAFでglobal65BC5Cを読んで signed actor+1E530 と比較する。
actor +B0!=0 または +A8!=0 または signed actor+1E530>=global65BC5C の場合、4E7FC1で actor+228 を取り、4E7FD3で+0x20する。
それ以外（B0=0、A8=0、counterがthreshold未満）は4E7FBDでEAX=0とした後、やはり4E7FD3で+0x20する。つまり列挙窓の入力幅は通常32bit演算の範囲で (effective_actor_radius + 32)。
この値をdoubleにし、4E7FE2..4E8019の角度変換・5E41E0/5E40B0/5D1B80を経て候補grid領域を列挙する。厳密な幾何学外形、x87/CRT丸め、overflowは未確定で円全走査などへ置換しない。

[CANDIDATE PASS] 4E8124/812E/8137/8149はcandidate+65非0、+1AE==0、candidate+1D0 != actor+1D0、candidate+1D4 == actor+1D4の順で検査する。+1867Cやstealthを本局所へ勝手に追加しない。
4E816D call44D8F0の距離を4E8172で+0.5した後、4E817B call5D1B80で整数化する。ここは54E系の別floor式を持込まず、runtime依存の返値EAXを明示する。
4E8180/8189でcandidate+B0と+A8を非zero判定し、双方0の場合はsigned candidate+1E530<global65BC5Cで候補半径を0にする(4E81A0)。
その他ではcandidate+228を候補半径とする(4E81A4)。4E81AA CMP EAX,ESI → 4E81AC JL 4E81F9、つまり距離整数EAXがeffective_candidate_radiusより厳密に小さい場合だけAL1正常RETへ。
列挙窓のactor半径+32と、最終判定のcandidate半径(場合により0)は**別役割**。candidate半径が0の通常非負距離では成功しない（範囲・数値前提つき）。

## return・副作用・接続
この分岐を含む主関数の正常RETは4E7F8A/4E7F96/4E81F6/4E8202、いずれもRET 0x10（旧§60の全体記載と矛盾なし）。
4E81F9はAL1、4E81EDはAL0。これらの値は「候補が条件に合致したか」という局所選択結果で、弾の命中・被害やMP消費の成功ではない。
当該保存assemblyに直接CRT 5B6EAB callはない。ただし44D8F0/5E41E0/5E40B0/5D1B80の内側の総乱数・例外までゼロと断定しない。
局所4E7F99..4E8202は戻りまでのstate writeをstack局所へ限定しており、Unit+1E560/18688/MPへの直接storeはこの区間で確認されない。caller側の別storeは既存成果に従う。
[REIMPLEMENT] 対象Unit identity・元配列順・actor幅とcandidate受入半径・各gate・数値helper returnを独立traceする。距離変換前に成功/不発を仮定せず、HP/MP/発射・RNG副作用を先取りしない。
[VERIFY] candidate/actor B0,A8,+1E530各producer、radius+228の正確な論理名、global65BC5C、座標gridの容量・別数値関数の精度/MXCSR、caller実到達、無効pointer/負幅、合法技能と結果は未確定。
[GOLDEN-DESIGNED/NOT RUN] 合法に到達できる原作sceneが特定されたら、actor/candidate両者のB0/A8 0/非0、+1E530閾値直下/等号、radius0/小/大、distance=radius-1/radius/radius+1を比較。可視行動・HP/MP・投射・時間/RNGのみをgoldenに採用し、隠れslotだけはINELIGIBLE。
[CHECK] B専用exe/T012_DUAL_RADIUS_STATIC_CHECK_20261013.pyとdata/T012_DUAL_RADIUS_STATIC_CHECK_20261013.json。保存REA命令列とbranch truth-tableを局所確認。原作実機PASS0 / new strict MATCH0 / 新Task DONE0。
[NEXT] T012の技能内MP fallback/射撃効果、T013のactual owner bindingとWorkの候補接続、T011 cross-kind parent resolverを、既存READYと重複しない独立証拠に限定して継続する。EのみMASTER/T018正式統合。
