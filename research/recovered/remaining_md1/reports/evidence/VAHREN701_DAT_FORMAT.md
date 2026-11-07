# Vahren701 encrypted script .dat format

調査日: 2026-10-05

## 結論
Vahren701 の `a_default/script/**/*.dat` 250件は、未知のコンパイル形式ではなく、Vahren.exe の公開仕様にある `debug_paper.txt -> encode` で暗号化された通常のスクリプトである。

全250件が先頭4 byte `01 02 03 04` を共有する。Vahren.exe ver7.01 の静的解析では、このマーカーを生成・判定する対になる2関数が確認できた。

## encode routine
- VA `0x424AC0`
- `[buffer+0..3] = 01 02 03 04`
- `[buffer+4..31]` に28 byteのランダム鍵を格納
- 元平文は `buffer+32` から配置される
- ファイル先頭基準の位置 i>=32 の各byteに `key[i mod 28]` を加算（mod 256）。payload相対index jなら `key[(j+32) mod 28]`。
- 暗号化後サイズは元サイズ + 32 byte

主要命令:
- `0x424ACC mov dword ptr [edi], 0x04030201`
- `0x424AFB mov byte ptr [edi+esi+4], cl` (28-byte key)
- `0x424B32 mov al, byte ptr [esp+...]`
- `0x424B36 add byte ptr [esi+edi], al`

## decode routine
- VA `0x424B50`
- 先頭DWORDが `0x04030201` でなければ非暗号化としてそのまま扱う
- 28 byte鍵を `buffer+4` から取得
- ciphertext byteから周期28の鍵を減算（mod 256）
- 復号後に `buffer+32` から先頭へ `len-32` byteをmemmove/memcpy
- 戻り長は `len-32`

主要命令:
- `0x424B59 cmp dword ptr [ebx], 0x04030201`
- `0x424B6A lea eax, [ebx+4]` + 28-byte copy
- `0x424BA8 mov al, byte ptr [esp+...]`
- `0x424BAC sub byte ptr [esi+ebx], al`
- `0x424BB4..0x424BBD` で32-byte header除去用copy
- `0x424BC5 lea eax, [edi-0x20]` (decoded length)

## encoder call site / already-encoded判定
VA `0x51A632` で読み込んだ本文先頭相当 `[buffer+0x20]` を `0x04030201` と比較。
未暗号化なら `0x424AC0` を呼び、暗号化済みなら再暗号化しない。
これはWikiの「すでに暗号化されてるファイルはスルー」と一致する。

## 実データ統計
- script .dat: 250 / 250 が `01 02 03 04` header
- header key bytes: 7000 byte（250*28）
- 観測範囲: 8..119
- 鍵は固定値ではなくファイルごとに異なる
- image.dat系のBMP/画像データはこの形式ではない

## 外部仕様との照合
Vahren Wiki「シナリオ製作講座」では、`debug_paper.txt` に `encode` を記述すると対象scenarioのscriptフォルダの全datを暗号化し、暗号化済みはスルーすると説明されている。
https://w.atwiki.jp/vahren_ency/pages/411.html

## 再実装仕様
reader:
1. 先頭4 byteを検査。
2. 非 `01 02 03 04` なら通常の平文script readerへ渡す。
3. 一致時は28-byte keyを取得。
4. `payload = file[32:]` とし、各 `payload[j] = (payload[j] - key[(j+32) % 28]) & 0xff`。
5. 得られたbyte列を通常のscript encoding/parserへ渡す。

writer/encode互換が必要な場合:
- 4-byte magic + 28-byte key + 加算済みpayloadを生成する。payload[j]には `key[(j+32)%28]` を加える。
- 完全な乱数生成方式の再現は、既存暗号datの読込互換だけなら不要。Vahren.exeとbyte-for-byte同一のencoder出力が必要なら別途PRNG特定Taskを設ける。

## 確度
暗号化/復号のデータ変換仕様: CONFIRMED（実dat header + Vahren.exe静的解析 + Wikiの三点一致）。
PRNGの具体的生成分布: 未確定。ただし復号互換には影響しない。

## 2026-10-06 clean-room golden correction
- 初期メモにあった `key[(i-32)%28]` は誤り。disassemblyの剰余計算は `esi`（ファイルoffset、32から開始）自体に対して行われる。
- 正式式は file offset `i>=32` で `key[i % 28]`。payload相対index `j=i-32` なら `key[(j+32)%28]`。
- `evidence/t022_decoder_golden.py` でVahren701 script 250/250を復号し、250/250がCP932 strict decode成功。
- 同一header keyを使って再encodeすると250/250で元暗号datとbyte-for-byte一致。失敗0。
- この結果により既存dat reader/writer変換仕様はCONFIRMED。新規encodeの乱数key生成PRNGだけは別問題。