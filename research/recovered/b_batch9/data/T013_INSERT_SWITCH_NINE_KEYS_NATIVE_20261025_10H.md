# B-20261025-10H-T013-INSERT-SWITCH-NINE-KEYS-01｜T013：巨大dispatch関数の辞書insert 10箇所を9 opcode値に分類

- Owner: B/T013。状態 STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA-DERIVED / VERIFY / NOT READY。
- 目的: 09Hで後処理を10/10確認した 0x004AE0F0 のinsert入口条件を非重複増分として分類。
- Source EXE: `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（このrunで現物ハッシュ一致）。
- Search DB: `rea_lab/headless_analysis/search_index/search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（manifest照合一致）。
- Pseudoc: `full_pseudoc_20261020/functions/004A/004AE0F0.c`、search.py function出力 code_sha256 `BAAA402D3C909CEE8CCB5285397D9CE5E782A8D000336B4731A17A6599DBD588`。擬似Cはゲーム実測/厳密な意味論を示さない。

## PE-native opcode dispatch
- Native 0x004AE162: EDX=[EBP+8]。0x004AE168 ECX=[EBP-0x1214]、0x004AE16Eで[EDX+0x1EEF74]と比較；等しい時0x004AE17BでECX=0x80000008、異なる時0x004AE176でECX=[ECX+0x28]。
- 0x004AE188 `CMP ECX,0x53` / 0x004AE18B `JA 0x004B37BB` / 0x004AE191 `JMP [ECX*4+0x004B37EC]`。すなわち 0..0x53 のswitch dispatch（負数やsentinelもunsigned boundでdefault）。
- 現物jump-table 0x004B37EC..0x004B393B (0x54×4B) SHA256 `A608315D79CB723219191FAE8122A6E613700E3DE643FB8859CCFAE2ADC735DA`。
- 対応表はnative table入口の静的アドレスとGhidra case bodyのinsert siteをJOINしたもの（case内部全pathの到達性はVERIFY）。

| Case ECX | Jump-table entry target | 辞書挿入 CALL site | 備考 |
|---|---|---|---|
| 0x01 | 0x004AE280 | 0x004AE35F | 1経路 |
| 0x24 | 0x004AFFD2 | 0x004B00C8 | 1経路 |
| 0x25 | 0x004B0100 | 0x004B01F8 | 1経路 |
| 0x26 | 0x004B0230 | 0x004B03AA | 1経路 |
| 0x29 | 0x004B05EF | 0x004B06C7 / 0x004B07A1 | 2条件分岐 |
| 0x2A | 0x004B07B1 | 0x004B087D | 1経路 |
| 0x3B | 0x004B1EBA | 0x004B20ED | 1経路 |
| 0x48 | 0x004B31ED | 0x004B345C | 1経路 |
| 0x51 | 0x004B04C2 | 0x004B05B0 | 物理VA順とopcode順は別 |

## 0x29 two-way branch
- Native 0x004B0657 reads local-1268; 0x004B065D reads local-1264; 0x004B0663 `CMP ECX,EAX`; 0x004B0665 `JNE 0x004B06FF`。equal側が0x004B06C7 insert、non-equal側が0x004B07A1 insertへ進むとGhidra CFGと整合。
- Ghidra上はcase0x29で `local_126c == local_1268` のempty-range相当分岐（分岐前のloader・一部オフセットがASM表示とずれている可能性あり）。正確な配列型・キー値producer・2種の挿入先の同一性はVERIFY。
- 原作ASM 0x004B06C7 / 0x004B07A1 共に `CALL 0x0049F7D0`、戻り直後 `0x004B06D2 CALL 0x0049CED0` または `0x004B07AC JMP 0x004B06D2`。後処理自体は09H既発見で再計数0。
- PE bounded bytes SHA256: 0x004AE0F0 len210 `2B568FE925CE3226CDB253817DFAF00011968806474CB3C78C2363DE988A16C9`、0x004B05EF len128 `5720DEF4E2343F7EC3365FD5F1F9567EA5814D3E123FF49D4ADC8093EC49ACAF`。

## Dedup / remaining / golden
- B T013/T028/HANDOFF全文で 4AE181/4B37EC/4B0665/4B06FF/1EEF74 の記載を検査し既記録ゼロ。09H 10/10 cleanup、06H CALL-count、05H result ABIを再計数しない。他lane/未同期全件との意味重複はVERIFY。
- 10/21回収22資料と後発10研究・Library訂正版2等の全ID回収・同期は未完。既拒否操作の別経路再試行0、新拒否0。ACTIVE Ghidra / 原本実行・改変・再逆コンパイル0。
- READY 0、Task DONE 0、E MASTER統合 0、原作Gameplay Golden PASS 0、strict MATCH 0。
- Golden: 無改変旧EXE + x20強化前DAT + 同一SAVE/MAP/input/RNGで実際のcase選択、辞書内容、挿入の重複/非重複、death_event連動、次tickまで動的採取が必要（DESIGNED_NOT_RUN）。
- NEXT: 0x004B05EFで構築する2つの入力列の型と生成元、case0x29の2分岐それぞれのキー・値、0x4B20EDのcase3B条件を原PE限定照合。active.lock/高負荷時はread-only。
- 書込権: 本B data・data/T013_AI.md・evidence/LANE_B_HANDOFF.mdのみ。PC readbackは別receiptで記録。