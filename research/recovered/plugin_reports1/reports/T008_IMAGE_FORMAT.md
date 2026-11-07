# T008 image.dat / imagedata.dat 形式仕様
調査日: 2026-10-06

## 結論
[CONFIRMED] image.dat / image2.dat は標準BMP (BITMAPINFOHEADER=40, 32bpp, BI_RGB) のatlas画像。
[CONFIRMED] imagedata.dat / imagedata2.dat はatlas寸法・透明色・論理名→矩形対応を持つmetadata。
[CONFIRMED] 迫真戦記とVahren701の対象8ファイルを全件EOFまでparseし、全矩形がatlas範囲内。

## imagedata形式
- offset 0: width u32LE
- offset 4: height u32LE
- offset 8: 4-byte color key。on-disk順は B,G,R,A。
- offset 12以降: record列。
- record = ASCII/NUL終端 name + left/top/right/bottom 各u32LE。
- right/bottomはexclusive。抽出サイズ=(right-left, bottom-top)。
- EOF marker = ASCII ________ + NUL (9 bytes)。trailing bytesなし。

## target実測
- image.dat: 2048x441, 32bpp, 3,612,726 bytes。imagedata.dat: 497 records。
- image2.dat: 2048x32, 32bpp, 262,198 bytes。imagedata2.dat: 16 records。
- metadata color keyは両方 BGRA=(1,0,0,0) → RGB=(0,0,1)。
- Vahren701でも同形式。image=1024x985/806 records、image2=1024x896/493 records。
- 全4 metadataでduplicate name=0、bounds violation=0、EOF後trailing=0。

## 参照・上書き
- 論理chip名はmetadata record名でatlas矩形へ解決する。
- Wikiはchip/の同名素材がimage.dat内chipを、chip2/がimage2.dat内skill chipを上書きすると明記。
- 2018年独立解析器もpacked atlasを先に展開し、その後loose chip/chip2を同名パスへコピーして上書きする。
- 透明化は後続修正でalpha込みの完全一致ではなくRGB color-key一致へ変更されている。

## 根拠
- evidence/t008_image_probe.py / T008_IMAGE_FORMAT.json / T008_IMAGE_CROSSVERSION.json
- pCYSl5EDgo/Wahren commits 99d2cd84... (BGRA訂正), bbe3bf03... (RGB color-key/loose上書き)
- Vahren Wiki「カテゴリ別諸構成」「掲示板抜粋」
