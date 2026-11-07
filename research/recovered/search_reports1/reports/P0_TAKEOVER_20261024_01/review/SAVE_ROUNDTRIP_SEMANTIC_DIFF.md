# save4→save5 ID別構造差分
研究ID P0_TAKEOVER_20261024_01。EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、V9 DB SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
対象: runtime/save_roundtrip/save4.sav → save5.sav。SHAはD8300FC3D0DB699D0D10C3EE7E85B79C4A78B03433B72A568A625494903DE345 → FDDA88452B23A91DC8EC1EACB2FD31A088C2237A29A79F474798D79FD85681B6。
判定: 全差分を保存構造上で特定。ゲーム上の同値・G5完全PASSは未証明。native observer全解除後のユーザー操作によるload/saveと親から報告されており、bridge起因と断定しない。
方法: dev_labの既存normal_save_complete_wire.py/Unit等codecをread-only再利用、bytecode生成無効。全sectionをparseして両方の暗号化bytesまで完全再構築一致。再利用parser自体の独立実装ではない。importしたsourceのSHAをJSONに保存。
5468 UnitのID集合・順序は一致、追加/削除0。5455 Unitは構造/record bytes不変、13 Unitだけ変更。Numeric3858件・Spot138件・Power30件に加えDiplomacy44bytes・WorldGraph9750bytesも構造と再構築bytes完全一致。

## 13 Unitの正確な差分
| 保存Unit ID | field | before→after | record長増分 |
|---|---|---|---|
| eu9, eu10, eu11, eu12, eu13, eu15, eu16, eu37 | prelude.dwords[192]（native保存record +0xC0） | 90→100、それ以外不変 | 0 |
| azs | string_vectors[3]（+10C/+110） | 615→616要素、末尾へsp_masupa_azs 1個 | +14 |
| ndk | string_vectors[2]（+FC/+100） | 615→616要素、末尾へsp_ndk 1個 | +7 |
| pinky | string_vectors[3]（+10C/+110） | 28→29要素、末尾へsp_pinky 1個 | +9 |
| van | string_vectors[2]（+FC/+100） | 1230→1232要素、末尾へsp_vanban,sp_vanban2各1個 | +21 |
| ymnu | string_vectors[2]（+FC/+100） | 615→616要素、末尾へb_rocket_ramen 1個 | +15 |
追記合計66bytesは各ASCII+NULの長さ合計と一致。既存配列prefixは全て保持。反復要素があるため『末尾追記と同一の列変化』を意味し、実際のnative挿入操作位置を観測したものではない。
headerはunknown_u32x5の最後のみ15→16（plain offset29）。scenario sci1/power po2/leading3と他headerは不変。フィールド意味を時刻/回数などへ推測しない。
保存Unitはwriter-shaped recordであり、戦闘runtime Unitクラスの同名offsetと混同しない。+C0およびvectorのゲーム上の語義・変化原因は未確定。文字列名からskill有効化等を断定しない。

## 全体差分の扱い
最初のUnit差分plain offset2756486はazs record（開始2747516）内。以後、可変長string追加によりsection開始位置が累積66bytesずれる。同位置比較701009bytes差を70万項目の変更や破損と数えない。
units長3455699→3455765、spots61258/powers8889/diplomacy44/world9750は各長不変かつbytes同一。Unitの全既知raw scalar、tail14dword、tree、他string等は上表のfield以外不変。
構造変更の全列挙はSAVE_ROUNDTRIP_SEMANTIC_DIFF.json（完全before/afterとcompact_unit_diffs）、再実行はcompare_save_roundtrip.py。原SAVE/他レーンparser変更なし。
再開: save5→save6を同じID・fieldで比較し、+C0変更と配列追記が再発/収束するかを判定。既存native reader/writerまたはDATの根拠が得られるまで正当変動/バグ/bridge原因のいずれにも断定しない。load実行はユーザー報告でnative loader hookは未採取、外部結果commit Golden試験でもない。

補足: envelopeの保存key28も2ファイル間で異なる。上の66bytes/field比較は復号plaintextに対するもの。各SAVEはそれぞれの保存keyで元ciphertextへ完全再構築できる。key生成原因/RNG状態の同値は未証明。
