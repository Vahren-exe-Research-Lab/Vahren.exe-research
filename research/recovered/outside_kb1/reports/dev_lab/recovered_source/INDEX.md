# 保存済みGhidra疑似Cソース — 再開発用sourcebook

**保存済み重点関数: 64件。新たに逆コンパイルした件数: 0。**

Ghidraが生成したC風の**疑似コード**を、証拠が5点すべてVERIFIEDの関数に限定して取り出したものです。
**元作者のC++ソースではなく、そのままコンパイルできるCプログラムでもありません。**
不明な構造体/引数/呼出規約/グローバル定数が残り、挙動の実機照合も未実施です。
復元作業では元ファイルの疑似コードを直接書換えるのではなく、独立の互換ソースに分岐を実装します。

旧ゲーム実機golden=0、strict互換MATCH=0。48件は重点サンプルでありEXE全体の割合ではありません。

| 原アドレス | Task | 静的サイズ(byte) | 内部call先(件) | 疑似C |
|---|---|---:|---:|---|
| `0x00433E80` | T005 | 797 | 1 | [FUN_00433E80](ghidra_c_pseudocode/FUN_00433E80.c) |
| `0x00463280` | T005 | 340 | 1 | [FUN_00463280](ghidra_c_pseudocode/FUN_00463280.c) |
| `0x004693F0` | T005 | 108 | 2 | [FUN_004693F0](ghidra_c_pseudocode/FUN_004693F0.c) |
| `0x00504400` | T005 | 1485 | 3 | [FUN_00504400](ghidra_c_pseudocode/FUN_00504400.c) |
| `0x00505210` | T005 | 3717 | 2 | [FUN_00505210](ghidra_c_pseudocode/FUN_00505210.c) |
| `0x0050A5E0` | T005/T006 | 616 | 0 | [FUN_0050A5E0](ghidra_c_pseudocode/FUN_0050A5E0.c) |
| `0x0050A850` | T005/T006 | 489 | 0 | [FUN_0050A850](ghidra_c_pseudocode/FUN_0050A850.c) |
| `0x00464290` | T005/T011 | 802 | 1 | [FUN_00464290](ghidra_c_pseudocode/FUN_00464290.c) |
| `0x004647D0` | T005/T011 | 1157 | 1 | [FUN_004647D0](ghidra_c_pseudocode/FUN_004647D0.c) |
| `0x00465060` | T005/T011 | 1082 | 1 | [FUN_00465060](ghidra_c_pseudocode/FUN_00465060.c) |
| `0x004A6700` | T005/T014 | 478 | 0 | [FUN_004A6700](ghidra_c_pseudocode/FUN_004A6700.c) |
| `0x0040B200` | T006/T010 | 84 | 0 | [FUN_0040B200](ghidra_c_pseudocode/FUN_0040B200.c) |
| `0x004321B0` | T006/T014 | 3124 | 4 | [FUN_004321B0](ghidra_c_pseudocode/FUN_004321B0.c) |
| `0x004637A0` | T006/T014 | 338 | 1 | [FUN_004637A0](ghidra_c_pseudocode/FUN_004637A0.c) |
| `0x0046F4C0` | T009 | 555 | 3 | [FUN_0046F4C0](ghidra_c_pseudocode/FUN_0046F4C0.c) |
| `0x00432EE0` | T010 | 1663 | 2 | [FUN_00432EE0](ghidra_c_pseudocode/FUN_00432EE0.c) |
| `0x004930C0` | T010 | 573 | 0 | [FUN_004930C0](ghidra_c_pseudocode/FUN_004930C0.c) |
| `0x00565700` | T010 | 35 | 0 | [FUN_00565700](ghidra_c_pseudocode/FUN_00565700.c) |
| `0x004C1200` | T012 | 136 | 0 | [FUN_004C1200](ghidra_c_pseudocode/FUN_004C1200.c) |
| `0x00546F70` | T012 | 1308 | 6 | [FUN_00546F70](ghidra_c_pseudocode/FUN_00546F70.c) |
| `0x00547DB0` | T012 | 513 | 4 | [FUN_00547DB0](ghidra_c_pseudocode/FUN_00547DB0.c) |
| `0x00550D80` | T012 | 234 | 1 | [FUN_00550D80](ghidra_c_pseudocode/FUN_00550D80.c) |
| `0x00550E70` | T012 | 1566 | 7 | [FUN_00550E70](ghidra_c_pseudocode/FUN_00550E70.c) |
| `0x00551490` | T012 | 2479 | 6 | [FUN_00551490](ghidra_c_pseudocode/FUN_00551490.c) |
| `0x00551E50` | T012 | 457 | 1 | [FUN_00551E50](ghidra_c_pseudocode/FUN_00551E50.c) |
| `0x00576E30` | T012 | 72 | 1 | [FUN_00576E30](ghidra_c_pseudocode/FUN_00576E30.c) |
| `0x00578B70` | T012 | 893 | 3 | [FUN_00578B70](ghidra_c_pseudocode/FUN_00578B70.c) |
| `0x0057DF90` | T012 | 484 | 0 | [FUN_0057DF90](ghidra_c_pseudocode/FUN_0057DF90.c) |
| `0x005D1B80` | T012 | 28 | 0 | [FUN_005D1B80](ghidra_c_pseudocode/FUN_005D1B80.c) |
| `0x004E7ED0` | T012/T013 | 814 | 1 | [FUN_004E7ED0](ghidra_c_pseudocode/FUN_004E7ED0.c) |
| `0x00514D60` | T013 | 430 | 2 | [FUN_00514D60](ghidra_c_pseudocode/FUN_00514D60.c) |
| `0x00514F10` | T013 | 234 | 2 | [FUN_00514F10](ghidra_c_pseudocode/FUN_00514F10.c) |
| `0x005154F0` | T013 | 207 | 1 | [FUN_005154F0](ghidra_c_pseudocode/FUN_005154F0.c) |
| `0x005155C0` | T013 | 115 | 0 | [FUN_005155C0](ghidra_c_pseudocode/FUN_005155C0.c) |
| `0x005158A0` | T013 | 51 | 0 | [FUN_005158A0](ghidra_c_pseudocode/FUN_005158A0.c) |
| `0x0057B870` | T013 | 812 | 7 | [FUN_0057B870](ghidra_c_pseudocode/FUN_0057B870.c) |
| `0x0057CFA0` | T013 | 48 | 2 | [FUN_0057CFA0](ghidra_c_pseudocode/FUN_0057CFA0.c) |
| `0x0057CFD0` | T013 | 397 | 0 | [FUN_0057CFD0](ghidra_c_pseudocode/FUN_0057CFD0.c) |
| `0x00427040` | T014 | 174 | 1 | [FUN_00427040](ghidra_c_pseudocode/FUN_00427040.c) |
| `0x004270F0` | T014 | 148 | 0 | [FUN_004270F0](ghidra_c_pseudocode/FUN_004270F0.c) |
| `0x00428010` | T014 | 1640 | 5 | [FUN_00428010](ghidra_c_pseudocode/FUN_00428010.c) |
| `0x00428710` | T014 | 3252 | 7 | [FUN_00428710](ghidra_c_pseudocode/FUN_00428710.c) |
| `0x00429C60` | T014 | 200 | 0 | [FUN_00429C60](ghidra_c_pseudocode/FUN_00429C60.c) |
| `0x00435550` | T014 | 1672 | 2 | [FUN_00435550](ghidra_c_pseudocode/FUN_00435550.c) |
| `0x0045E1E0` | T014 | 1028 | 7 | [FUN_0045E1E0](ghidra_c_pseudocode/FUN_0045E1E0.c) |
| `0x0045E5F0` | T014 | 453 | 3 | [FUN_0045E5F0](ghidra_c_pseudocode/FUN_0045E5F0.c) |
| `0x00460000` | T014 | 2096 | 4 | [FUN_00460000](ghidra_c_pseudocode/FUN_00460000.c) |
| `0x004705F0` | T014 | 256 | 0 | [FUN_004705F0](ghidra_c_pseudocode/FUN_004705F0.c) |
| `0x00470700` | T014 | 99 | 0 | [FUN_00470700](ghidra_c_pseudocode/FUN_00470700.c) |
| `0x00470830` | T014 | 105 | 0 | [FUN_00470830](ghidra_c_pseudocode/FUN_00470830.c) |
| `0x00471AF0` | T014 | 559 | 2 | [FUN_00471AF0](ghidra_c_pseudocode/FUN_00471AF0.c) |
| `0x00471D20` | T014 | 144 | 1 | [FUN_00471D20](ghidra_c_pseudocode/FUN_00471D20.c) |
| `0x0058E870` | T014 | 1861 | 3 | [FUN_0058E870](ghidra_c_pseudocode/FUN_0058E870.c) |
| `0x0058EFD0` | T014 | 2050 | 1 | [FUN_0058EFD0](ghidra_c_pseudocode/FUN_0058EFD0.c) |
| `0x005964C0` | T014 | 1489 | 4 | [FUN_005964C0](ghidra_c_pseudocode/FUN_005964C0.c) |
| `0x00598980` | T014 | 859 | 2 | [FUN_00598980](ghidra_c_pseudocode/FUN_00598980.c) |
| `0x0040ED80` | T031 | 45 | 2 | [FUN_0040ED80](ghidra_c_pseudocode/FUN_0040ED80.c) |
| `0x00479740` | T031 | 20 | 1 | [FUN_00479740](ghidra_c_pseudocode/FUN_00479740.c) |
| `0x00479A30` | T031 | 278 | 1 | [FUN_00479A30](ghidra_c_pseudocode/FUN_00479A30.c) |
| `0x004B78C0` | T031 | 3452 | 3 | [FUN_004B78C0](ghidra_c_pseudocode/FUN_004B78C0.c) |
| `0x004C1FC0` | T031 | 258 | 1 | [FUN_004C1FC0](ghidra_c_pseudocode/FUN_004C1FC0.c) |
| `0x005001B0` | T031 | 4857 | 3 | [FUN_005001B0](ghidra_c_pseudocode/FUN_005001B0.c) |
| `0x005B6E99` | T031 | 18 | 0 | [FUN_005B6E99](ghidra_c_pseudocode/FUN_005B6E99.c) |
| `0x005B6EAB` | T031 | 33 | 0 | [FUN_005B6EAB](ghidra_c_pseudocode/FUN_005B6EAB.c) |

## ソース復元上の優先課題

1. 関数ごとに引数、返り値、構造体フィールド、呼出規約を明示する。
2. `undefined4`, `float10`, `FUN_...`, `DAT_...`, global pointerの意味を分けて復元する。
3. 元の制御フローと乱数消費・早期returnをgoldenで比較する。
4. 原作script、Asset、Mapの読み込みと戦略/戦闘runtimeを独立実装する。

証拠IDやcaller/callee一覧は `manifest.json` に保存されています。
呼出グラフは `verified_call_graph.mmd` （保存済み39関数間に限定）です。
