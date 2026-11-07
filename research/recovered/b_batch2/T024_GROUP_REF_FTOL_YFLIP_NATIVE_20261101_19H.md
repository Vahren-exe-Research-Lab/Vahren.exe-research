# 迫真戦記ver0.67｜B/T024：グループ距離ソートの変換座標・Y符号反転・ftol分岐（2026-11-01 19H）
研究ID：`B-20261101-19H-T024-GROUP-REF-FTOL-YFLIP-CROSSJOIN-01`。owner B/T024（T011関連）、T013最終ターゲットはVERIFY。STATIC_NATIVE / STATIC_V9 / INFERRED / VERIFY / NOT READY。原作実機Golden PASS=0、strict MATCH=0、DYNAMIC=0、新規正式READY=0。

## 既存成果との差分・重複禁止
先行18H `B-20261101-18H-T024-DUAL-REFERENCE-COORD-AND-PC-RESTORE-01` は、2系統が`0x5D1B80`を呼び、`0x8BE048/+0x4C`を別々に設定して`0x529DC0`へ進むことを確認済み。19H `B-KB-20261101-19H-T024-CURATABLE-SOURCE-MAP-01` は既存9 IDを整理済み。本件はその新たな「変換後浮動小数点→符号反転→整数化」native鎖の限定照合であり、旧CALLやftol自体を新発見に再計上しない。
`knowledge/kb.py addr 0x5D1B80` は既に `ftol`（F付録A、STATIC）、`addr 0x5D1BB6` は `_ftol2`（legacy_20261011）と命名済み。B旧 `B-20261026-20H-T028-ATAN2-TRUNC-DISPATCH-01` もglobalによる変換経路分岐を先行記録。**汎用ftolの再命名・辞書二重登録は不要**。

## 原作PE限定ASMとIAT実体
原作 `Vahren.exe` 読取専用SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回実バイト再hash一致）。PE import実体：IAT `0x6092BC` = `d3dx9_35.dll!D3DXVec3TransformCoord`（pefileのIMPORT 188 entries内で一致）。
第1のNative窓 `0x529666..0x5296A8`（67B SHA256=`95310B821F55D9E064722BEE224984662295B7644D580663402FD9DDB031F7C4`）：`0x529666 call [0x6092BC]` → `0x52966C fld [esp+0x94]` → `0x529673 fchs` → `0x529675 fstp [esp+0x94]` → `0x52967C fld [esp+0x90]` → `0x529683 call 0x5D1B80` → `0x529688 fld [esp+0x94]` → `0x52968F mov edi,eax` → `0x529691 mov [0x8BE048],edi` → `0x529697 call 0x5D1B80` → `0x52969D mov [0x8BE04C],eax` → `0x5296A8 call 0x529DC0`（最後のCALLは18H既検証）。
第2のNative窓 `0x529826..0x529868`（67B SHA256=`7E44296479FCFCA638009D355B8A6286858B432E8720408458BA2332B510B9AB`）：`0x529826 call [0x6092BC]` → `0x52982C fld [esp+0x94]` → `0x529833 fchs` → `0x529835 fstp [esp+0x94]` → `0x52983C fld [esp+0x90]` → `0x529843 call 0x5D1B80` → `0x529848 fld [esp+0x94]` → `0x52984F mov esi,eax` → `0x529851 mov [0x8BE048],esi` → `0x529857 call 0x5D1B80` → `0x52985D mov [0x8BE04C],eax` → `0x529868 call 0x529DC0`（最後のCALLは既検証）。
両系統で **D3DX変換後の[esp+0x94]をFCHSで反転**、[esp+0x90]と反転済+0x94をそれぞれ `ftol` に渡して整数化した2成分を共有globalへ保存する。元のtransform入力・基準点、各経路の座標値の相違、実際の画面Yとの同一視はVERIFY。これは距離ソートの結果ではなくその直前の基準座標のproducer経路（STATIC）である。

## ftol変換分岐・再実装上の注意
`0x5D1B80..0x5D1B9B` 28B SHA256=`0FB02D573DE8004722053C9183D23507379DB1E668B77352ECBDEA372ED3645A`。Native `0x5D1B80 cmp dword[0xB14A40],0`→ `0x5D1B87 je 0x5D1BB6`、nonzeroは `0x5D1B92 fstp qword[esp]` と `0x5D1B95 cvttsd2si eax,[esp]`（有限・範囲内なら0方向整数化）。zero側は別V9関数 `0x5D1BB6` に分岐し、その `0x5D1BC5 fistp qword[esp+0x10]`／`0x5D1BC9 fild qword[esp+0x10]` が実在。先行T028/T013の既解明を再発見と数えない。
従って「D3DXが整数を直接返す」「常に四捨五入」「常に0方向に丸める」「`0x5D1B80`のV9 28B擬似Cだけで全経路完結」と記述してはいけない。global `0xB14A40`・x87 control word・SSE/MXCSR・負数/±0/NaN/範囲外・例外はVERIFY。V9のABIも未検証。

## 出典・保存とKB_CANDIDATE
Original PEの指定SHA、上記3限定窓の実バイトSHA、Capstone 32bit限定逆ASM、PE IAT解析、統合V9 `function 0x5D1B80/0x5D1BB6` と `knowledge/kb.py addr` が一次/補助根拠。先行出典 `data/T011_T024_DUAL_REFERENCE_COORD_NATIVE_20261101_18H.md` SHA256=`4C4C5C55D7CCB849BB93CE445B6669CE2B8BC5A0F451088EBB4E42F944658FBC`。新規命令VAはB HANDOFFの旧字句検索で0件だったが全レーン意味的重複ゼロは保証しない。
`KB_CANDIDATE` owner=B/T024 ID=上記、source=本ファイル、重要VA=`0x529666/0x529673/0x529683/0x529697/0x529826/0x529833/0x529843/0x529857`、global=`0x8BE048/+0x4C`、IAT=`0x6092BC`、既登録 `ftol`=`0x5D1B80/0x5D1BB6`。GitHub `REF_BATTLE_AI_MORALE.md` には「two coordinate outputs / Y FCHS / mode-dependent ftol / source ID」の追加を専任キュレーターが原本・訂正を検査した後に検討。symbols.tsvのftol新規行は**不要**。共有knowledge/Git/MASTERはBから編集しない。

## P0・Golden・安全
真の戦闘AI対象/移動先への接続、実機座標、全global writers、FPU制御語、最終0x569730効果、T011召喚EXP/T012 HP状態/T013最終対象/T028敗走はP0/VERIFY。原作実機Goldenには改変前DAT+同一SAVE/MAP/input/RNG/tickの2系統変換前後浮動小数点、`0xB14A40`、global結果、ソート結果と次tick行動の同一run receiptが必要。Golden PASS0/strict MATCH0/DYNAMIC0/新READY0。
PC 07H核心4件・03H保存不明・10/25原文欠落はOPEN（今回復旧成功とは主張しない）。HOLD21、既拒否VA/コマンドはBLOCKEDのまま。禁止操作の再試行/迂回、元EXE起動、原本/他owner/rea_lab/MASTER/knowledge/Git/設定/schedule書込なし。
