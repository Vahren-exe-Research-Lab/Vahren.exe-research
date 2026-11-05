# REA保存済み証拠の独立監査：event参加参照の三分岐slot選択 (2026-10-11 02時台 JST)
判定: CONFIRMED-SAVED-ASSEMBLY（関数0x4321B0内部のみ）。参照slotのゲーム上の意味と実機再現はVERIFY。
対象: T006/T010/T014、承認済みコピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（保存run記録から、今回再計算なし）。
一次証拠: runs/20261009T225741694Z/4321B0_procedure_assembly.json; ev_56f9a3557ec9eaa37a3dae138562b66cdde8d20a39e915d61d3e8c37709157db
照合: 同run/4321B0_procedure_pseudo_code.json; ev_6443778f30890c0e5cb33fc7bbabf54b8cd665a1424f7b354c6bd439dbac2051
# 観測した命令と条件
- 0x4329B6..0x4329DB: 2入力参照を個別にNULL補完。NULLなら[engine+0xC]+0x58を代入、非NULLは元値を維持。0x4329E1で+0x1EED54/55の2byteを0、+0x1EED56を0にする。
- 0x432A74..0x432AD2: まずrefA+0x1D非0、または0x40B200(literal VA0x636224)が非0ならflagA=1（+0x1EED54）。flagA=1の場合、flagBを評価せず分岐。
- flagA=0の場合のみrefB+0x1D非0、または0x40B200(literal VA0x63622C)が非0ならflagB=1（+0x1EED55）。同じ呼出内でflagAとflagBが同時に1になる経路は見えない。
- 0x432AD9..0x432B3A: flagの組合せでengine+0x1E8630/34/38から選んだ値を+0x1EED48と+0x1EED44へ設定。
| flagA | flagB | +0x1EED48 | +0x1EED44 |
|---|---|---|---|
| 0 | 0 | value at +0x1E8634 | value at +0x1E8638 |
| 1 | 0 | value at +0x1E8634 | value at +0x1E8630 |
| 0 | 1 | value at +0x1E8630 | value at +0x1E8634 |
- 0x432B49で+0x1EEC4Dへ1書込、その後も実行継続。二つの出力slotは同一値のコピーではなく3ケースの選択結果。
# 互換実装への境界・残課題
- 上記は保存済み静的アセンブリの局所分岐。+0x1E8630/34/38の型・意味・有効期間、0x40B200 comparator実効、他関数の書換、旧EXE実機挙動はVERIFY。
- NULL補完先+0x58のオブジェクト型も未確定。flagA/Bを独立に同時成立させたり、NULLを0のまま使う簡略化は当該関数の分岐と異なる。
- 比較設計DESIGNED/NOT RUN: refA/B null/non-null、+0x1D bit、各literal predicateを分け、flagA/Bと2出力slotの値を別記。internal slotが合法に観測できない場合はgolden INELIGIBLE。
- Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、39/48静的VERIFIED。今回増加0。旧EXE golden actual PASS0、研究DONE9/34（cp77）、ゲーム再実装率未測定。
- 新規REA/Ghidra/旧EXE実行なし。既往安全拒否されたbatch、extract、CPU/RAM probeや別経路迂回なし。MASTER/他レーン/T018/QUEUE/PROGRESS/原本/Git/MCP/automation変更なし。