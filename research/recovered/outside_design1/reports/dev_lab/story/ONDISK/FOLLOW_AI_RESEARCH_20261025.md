# ON-STAND-FOLLOW｜召喚術者への追従とCPU AI制御の調査
作成日：2026-10-25 JST / 静的証拠のみ／実機の追従・距離実証はNOT RUN。
## 第一候補：エンジン内蔵 satellite
- 公開仕様：https://w.atwiki.jp/vahren_ency/pages/389.html — `satellite=on` でリーダーまたは召喚術者へ追従。数値指定時はその距離まで近づく。標準距離 `radius*2+32`。
- 迫真戦記の原作DATにも32箇所で `satellite` を確認。使用例：`ghostnomi` には無し、`mona0071`（`F20_summon.dat` 1654付近）`satellite=30`、`sakerobo` 75、`achamo` 50、`MKMK姉貴` 70。
- 召喚実績：`F20_summon.dat` の `s_monaka` は `add2=mona0071,mona0072`、その `mona0071` に `satellite=30`。**召喚体にも適用されている根拠**。
## 既存EXEの静的根拠：V9 DB
- 既存 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` をread-onlyで検索。
- `satellite` の原文字列は 0x006281E8, 0x006281F4, 0x00628200。いずれも `FUN_00571B70` から参照。
- `FUN_00571B70` でUnit+0x1E594に追従対象ポインタ候補、Unit+0x1E598に追従距離候補を書込。初期値は `Unit+0x228*2+32`。
- `FUN_0057D1D0` は Unit+0x1E594を読み追従先の有効性と位置を参照、+0x1E598も参照して追跡移動候補へ至る。
- `FUN_0057A9E0` はUnit+0x1E594対象の有効性をチェック。これらはGhidra擬似Cであり完全な原本Cではない。
## CPU専用DATの役割は異なる
- `a_default/script/Ai戦闘制御_軍楽隊なし版.dat` は一万～数千行の戦闘陣形指揮。 `smoveTroop()` を207箇所で使用し、右翼/中央/左翼を指揮官に集合させる。
- スタンドの追従自体は **このAI DATに依存せず**、class衛星指定で本体AIが動く。全ユニットへ同ファイルの特殊指揮を流用する必要はない。
- `moveTroop()`: 対象へ通常の追尾命令。 `moveTroopFix()`: 攻撃より移動を優先させるためスタンドの平常追従に不向き。 `smoveTroop()`: 直線移動、障害物の問題に注意。
## 独立した試作・比較
- `stand_proto/stand_summon_fixture.dat` の class に `satellite=64`、`element_lost=on`。
- `stand_autostart_theft_fixture.dat` も召喚した敵スタンドに `satellite=64` を設定し、従来の強制 `moveTroopFix` は除去。
- `stand_proto/stand_follow_command_fallback.dat` は追従命令方式との比較専用。実ゲームで両方を同時ロードしない。
## 厳密射程は別
- `satellite=64` は追従時の目標接近距離であり、召喚者から半径64を**超えないハード制約ではない**。戦闘中に戦闘AI、プレイヤー指示、移動障害などで離れる場合があるか実機検証が必要。
- 必要な絶対射程Rと位置・HP共有は、DAT単独で保証できるとまだ証明されていない。
- 原作本体・他レーンはread-only。独立テストで実機追従PASSと偽装しない。