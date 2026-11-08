# CLAUDE-T040-CHIP-ATLAS-HEIGHT-CAP-20261108 — キャラチップ・アトラスの高さ上限 2048px の正体（3か所）と起動順序

担当 / 課題 / 観測日・出典の版: Claude（Claude Code セッション）/ T040 image.dat・image2.dat 容量制限解除 / 2026-11-08 / 迫真戦記 ver0.67 `Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（PE timestamp 1476792537。タイトル名EXEは .text 同一のため同じVA）

対象: 迫真戦記ver0.67 / 0x42C2B0（アトラス構築）・0x42D830（chip/ フォルダ列挙）・0x555CD0（共有転送DIB作成）・0x562C40／0x562B60／0x562F50（テクスチャ作成・転送）/ グローバル 0x879E68・0x879E78・0x87A1F8・0xAADD10・0x879720〜0x879734・0xAADA78

## 結論

1. `image.dat`＋`chip\`（ユニット用）と `image2.dat`＋`chip2\`（スキル用）は、それぞれ起動時に**1枚の縦長アトラス**へ積まれる。高さの上限 2048px は Vahren.exe の**3か所の即値**で決まる。
   - `0x42C3A6 cmp esi,0x800 / jle` … 合計の高さが 2048 を超えると MessageBox「（ユニット｜スキル）のキャラチップ量が規定サイズを越えました。一部削除して切り詰められます。」（文字列 0x636458、種別語 0x636444/0x63644C）
   - `0x42C485 mov dword [esp+0x20],0x800` … 高さを 2048 に切り詰め
   - `0x555CFB push 0x800` … テクスチャ転送用の**共有DIB（0xAADD10、BITMAP 0x879720〜、画素 0x879734、stride 0x87972C）を 2048×2048 で作る**、その高さ（`0x423B60(w,h)` の第2引数。第1引数 0x555D00 が幅）
2. 3か所を同じ値へ上げれば、高さ 2600px／6500px のアトラスで警告なし・正常表示（下の実機確認）。**最初の2か所だけ**を上げると、0x562F50 内の転送ループ `0x56307D mov ecx,[edi+edx]` が共有DIBの外を読み書きしてアクセス違反（0xC0000005）で落ちる（実機確認）。
3. テクスチャは `0x562C40`→`0x562B60` で幅・高さを2の累乗に切り上げ、`IDirect3DDevice9::CreateTexture(w,h,1,0,D3DFMT_A8R8G8B8,D3DPOOL_MANAGED)`（vtable+0x5C）で作成。UV 縮尺は浮動小数（+4/+8）で保持するため、高さの変更に追従する。GPU の最大テクスチャ寸法の確認はしていない（この環境の D3D9 caps は 16384×16384）。
4. アトラス内の並び: `image.dat` の画像を上端に置き、その下へ `chip\` の個別画像（0x42D830 が FindFirstFile で列挙、PNG 等）を詰める。例: 6500px の image.dat を置くと `_town3`（chip\_town3.png）は y=6622 に配置された。原作素材のままでのアトラス高さは 2048 以下（テクスチャ 2048×2048）。
5. 読み込み済みチップの表 `g_ChipAtlasMap`（0x879E68）は MSVC std::map で、オブジェクト +4 が head、+8 が要素数。ノードは +0/+4/+8 が左・親・右、+0xC が名前 std::string、+0x28〜+0x34 が矩形（left,top,right,bottom、right/bottom は排他）、+0x39 が isnil（0x42C95E の読み方と、起動中プロセスの読み取りで確認。原作素材＋試験画像で 2963 件）。
6. image.dat の不透明画素は alpha=255、透過色以外でも alpha=0 の画素は透明として描かれる（試験画像で確認）。既存 T008（image.dat は 32bpp BI_RGB）に対する補足。
7. 起動順序: Hakushin ローダーの通常プラグインは `DirectInput8Create` 時（実測で起動後約13秒）に読み込まれるが、アトラス読込（試験環境で約8秒目に警告）と共有DIB作成はそれより前。したがって**この上限の変更は通常プラグインでは間に合わず**、`dinput8.dll` の DllMain（EXE エントリより前）で行う必要がある。

## 確度

- 1・3・4・5: STATIC（逆アセンブル）＋ DYNAMIC（利用者自身の環境で、起動中プロセスのメモリ読取）
- 2: DYNAMIC（3か所: 警告なし・テクスチャ 2048×4096／2048×8192・画面で目印5個を目視。2か所のみ: 0x56307D でクラッシュ、Windows イベントログ ID 1000 の例外オフセット 0x16307D）
- 6: DYNAMIC（alpha=0 の目印が見えず、255 にすると表示）
- 7: DYNAMIC（DLL 列挙の時刻観測。3秒・6秒で HakushinCore 未読込、本番相当で約13秒後に読込）

## 根拠

- 静的解析: 本セッションで Vahren.exe（上記SHA）を capstone で逆アセンブル。0x42C2B0〜0x42CB60、0x42D830〜、0x423B60、0x423CB0、0x555CD0〜0x555D46、0x562B60〜0x5630B0、インポート（LoadImageA 0x6091F8、MessageBoxA 0x6091FC、BitBlt 0x609014、AlphaBlend 0x6091E8、CreateDIBSection 0x60905C）。
- 実機: 利用者の試験用コピーで、外部からの3か所書換え起動・dinput8 早期パッチ起動の両方を観測。原作素材のままの環境でも3か所の書換えと表示無変化を確認。
- 実装と試験: `ButaMonky/Vahren.exe-Extensions` PR #6（ブランチ `feat/early-image-limit-20261108`、`core/hakushin_early_patch.c`、`docs/IMAGE_LIMIT.md`、合成試験 19 項目、試験シナリオ生成 `tools/image_limit_test.py`）。

## 関連

- T008（image.dat／imagedata.dat 形式）: 形式は変わらない。高さの上限が EXE 側の3か所であること、alpha の扱い（結論6）を補足。
- 既存辞書 `0x879E68 g_ChipAtlasMap`: ノード配置・head 位置を補足（結論5）。
- readme の「chip1・2を容量削減したもので書き換えました」（ver6.53）は、この 2048px 枠に収める作業と整合（推定）。

## 採録候補

- symbols: `0x42C2B0 ChipAtlas_Build(suffix)`、`0x42D830 ChipAtlas_PackLooseChips`、`0x555CD0 TextureStaging_Create`、`0x562C40 Texture_CreateFromDib`、`0x562B60 Texture_CreatePow2`、`0x562F50 Texture_UploadFromDib`、`0x423B60 Dib_CreateTopDown(w,h)`、`0xAADD10 g_TextureStagingDC`、`0x879720 g_TextureStagingBitmap (BITMAP)`、`0x879E78 g_ChipAtlasTexture`、`0x87A1F8 g_ChipAtlasTexture2`、`0xAADA78 g_ChipAtlasBuildDC`
- 命令途中の位置（関数入口と分けて）: 0x42C3A6、0x42C485、0x555CFB、0x56307D
- REF: `REF_STARTUP_LOADING.md`（起動順序とプラグイン読込時刻）、T008 の補足

## 未確認・不足

- 0x42C3A6 の関数 0x42C2B0 が image2 側で呼ばれる経路（呼出元 0x42D364 は1か所。suffix "2" 判定 0x40B200 から推定）の個別確認
- 幅 2048 を超える image.dat の扱い（未試験。幅の上限チェックは見当たらない）
- max_height 16384 での実機（未試験）
- 他版（Vahren701 等）の同等箇所（未調査）

## 実機Golden / READY

Golden 比較・READY は未実施。上記の DYNAMIC は利用者自身の環境での観測に限る。

## 次の確認

- image2.dat 側（スキル）で 2048 超の試験
- 統合担当による symbols / REF への採録判断

## 保存状態

担当PRに保存（このファイル）。正本 develop への反映は統合担当の判断待ち。
