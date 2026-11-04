# B-20261029-1613-T013-MODE1-VTABLE68-CLASS-DISPATCH-01｜T013 mode1の仮想関数+0x68経由・Unitクラス分岐
Owner B / T013（T011・T024・T028参照）｜2026-10-29 16時台 JST｜STATIC ORIGINAL PE ASM/PE pointers + Ghidra STATIC / INFERRED / VERIFY / NOT READY
## 入力・安全・復旧
- Local Compact ONLINE。MASTER最終正式cp196/READY596（旧確認値、更新なし）、ANALYSIS_LANES_PROTOCOL、B5 owner、HANDOFF、回収監査を読取。旧search.sqliteは整理で元位置不在、別名統合V9のみ使用。Ghidra本体・ゲーム未実行。
- original PE copy rea_lab/targets/hakushin067_Vahren.exe 2,910,720 B SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（PC実バイトread-only再検証）。V9 sqlite現物SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、V9検索CLIはimmutable/query_only。
- 既存SAFE134 byte-verified/HOLD21安全関連、Library B147の54件1-byte差、10/25 14H研究全文未回収を継続。旧安全拒否・0x5710C0..0x571500・0x5767B0下流は解析せず迂回なし。
## 新増分：直接CALLゼロでもvtable dispatchに接続
- V9 callers/flow-callers：0x544D10と0x578110はいずれもE8直接CALL 0件。これだけで未使用とは断定不可。refs-to/pe-toで.rdataの以下4 pointerを抽出し、原作PEのDWORDを個別read-onlyで照合。
- SimpleUnit vtable base 0x63A4BC、slot +0x68=0x63A524→0x544D10（PE offset 0x239924）。writer 0x5442DE は原PE `C7 06 BC A4 63 00`。対応constructor 0x544290 Ghidra上SimpleUnit::vftable。
- StaticUnit vtable base 0x63A85C、slot +0x68=0x63A8C4→0x578110（PE offset 0x239CC4）。writer 0x559EF4 `C7 06 5C A8 63 00`。constructor 0x559EC0。
- SimpleStaticUnit vtable base 0x63A8E4、slot +0x68=0x63A94C→0x578110（PE offset 0x239D4C）。writer 0x55AE2C `C7 06 E4 A8 63 00`。constructor 0x55ADD0。
- Unit vtable base 0x63A9E4、slot +0x68=0x63AA4C→0x578110（PE offset 0x239E4C）。writer 0x56F8DD `C7 45 00 E4 A9 63 00`。constructor 0x56F880。
- 原PE4 slotの生DWORDは全て上記関数VAに一致、RVA→file mappingはPE section tableから算出。vtableラベル・constructor属性はGhidra静的分類で、実インスタンス/最終型は別証明。
## 新増分：呼び出し側の原生間接CALL
- V9 function 0x44CF80内にGhidra `(**(code **)(*piVar2 + 0x68))(1)`。原作PE 0x44D033に `8B 11`（mov edx,[ecx]）、0x44D035 `8B 42 68`（mov eax,[edx+68]）、0x44D038 `6A 01`（push 1）、0x44D03A `FF D0`（call eax）を生バイトで独立照合。直接E8ではなくvtable+0x68経由でbyte/int引数1が渡る経路を示す。
- 同関数Ghidraではグループ内のUnit候補を巡回し、Unit様+0x18615、+0x74や関連状態等に条件を課してから仮想CALLする。Ghidra擬似CはABI未検証；インスタンスの真の型・call時の戻り・到達条件と副作用はVERIFY。
- 既15Hの0x544D10/0x578110入口初期化とmode1→0x57D8B0への結合を繰返し新成果計上しない。今回の新規分は型別vtable slot4本とcaller0x44D03Aを結ぶ上流dispatch。SimpleUnitと他3クラスで同slotの関数実装が異なる。`retreat`文字列があることのみで敗走挙動を確定しない。
## 重複・Golden・状態
- B所有 data/T0*.md+LANE_B_HANDOFF 384ファイルを新0x44D03A/0x44D035/slot4住所で検索し先行literal一致0。旧T011 class RTTIと15H入口の解明は旧知として再計上0。10/25欠落・他レーンの意味的完全dedupはVERIFY。
- Golden必要：無改変旧EXEと20倍改変前DAT、同SAVE/MAP/input/RNG、実際に各Unit class 4種を用意しvtable+0x68値、0x44D03A到達条件/param 1、+0x1867E/F before/after、0x57D8B0 mode1・戻り、可視移動/敗走と次tickを同一合法runで観測。DESIGNED_NOT_RUN。
- 旧原作Gameplay Golden PASS0／strict MATCH0／新正式B READY0／E MASTER統合0／Task DONE0。STATIC / INFERRED / VERIFY / NOT READY。
- NEXT P0：0x44CF80への上流E8 callerとそのUnitグループsource、+0x68仮想関数の真のRNG/副作用、+0x1867F入力区別。T024通常AI・T028士気敗走・T011召喚EXP・T012ダメージ残P0維持。原本・他lane・MASTER・REA/dev_lab・Git・Work・設定・schedule変更なし。
