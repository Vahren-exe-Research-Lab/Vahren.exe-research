# T007 .map バイナリ形式仕様
調査日: 2026-10-06

## 結論
[CONFIRMED] 迫真戦記 ver0.67 の151 mapと Vahren701 の191 mapは、同一の可逆形式として100%解析できた。
[CONFIRMED] 全342ファイルでEOFまで過不足なく消費し、parse→re-encodeがbyte-for-byte完全一致した。
よってT007の完了条件「任意mapを読み書きできる仕様」は満たす。

## フォーマット
- byte0: width (u8)
- byte1: height (u8)
- 以後は y=0..height-1、各y内で x=0..width-1 のcell列。
- 各cellは0個以上のentryを持ち、0xFFでcell終了。
- entry = type:u8 + name:UTF-8 bytes + 0xFE。
- target/V701全件でname終端に0xFFを使うentryは0件。
- type=0: field chip。type=1: object chip。
- type>=2: unit配置。direction=(type & 0x0F)-2、formation=type>>4。
- unit名は2017年解析器では読込時にlowercase化される。raw file自身はUTF-8 name bytesを保持する。
- map全体に別途EOF marker/checksum/size fieldはない。width*height cellを読み終えた位置がEOF。

## target実測
- 迫真戦記: 151/151 parse成功、151/151 exact round-trip、trailing byte 0。
- 最大width=250、最大height=250、最大name長=21 bytes。
- Vahren701: 191/191 parse成功、191/191 exact round-trip、trailing byte 0。
- 最大width=160、最大height=150、最大name長=22 bytes。
- 2017年独立解析器はname 50-byte超をエラーにするが、これはengine本体上限とは未確定。現行実データは22byte以下。

## 根拠
- evidence/t007_map_roundtrip.py
- evidence/T007_MAP_ROUNDTRIP.json
- evidence/T007_MAP_CROSSVERSION.json
- pCYSl5EDgo/Wahren commit ff43d1b83732dad07af10130c597ace10a8f79ce, Code/Map/MapLoadAsync.cs（reader/writer双方）