# REA/T015 過去OFFLINE 03–05Hの回収｜Vorbis residue 次元・算術上限・EOF訂正

**区分** `PUBLISHED_INTAKE / SOURCE_LIBRARY_OFFLINE / STATIC / VERIFY / NOT READY`。2026-11-01 03/04/05時台の**既存3研究IDを新規発見に二重計上せず**、過去報告の意味と訂正をPRIVATE GitHubで検索可能にする。PCのREA正本に同期したことや最新V9で原研究全体を再実行したことを意味しない。

## 研究ID・訂正関係
1. `REA-OFFLINE-20261101-03H-P0-VORBIS-CODEBOOK-DIMENSION-DUAL-BUILDER-PROVENANCE-STATIC-01`：`0x005D9F40` と `0x005DA070` が元コードブックの先頭DWORD（dimension）をコンパイル済みレコードの先頭へコピーする二系統。原本指示点 `0x005D9F64/66` と `0x005DA0B2/B4`。`0x005DFFC0` が `inner+0xB20` の `0x38`-byte entryから対象を選び、`instance+0x10`を介してtype2復号 `0x005E0DC0` の`0x005E0E0C IDIV`に渡すと報告。03Hの「0x005E00E0 IMUL局所overflow拒否が見えない」は**危険性の確定ではない**。次の04Hが正常未改変parser成功時について範囲を限定して訂正。
2. `REA-OFFLINE-20261101-04H-P0-VORBIS-RESIDUE-POWER-BOUND-CORRECTION-STATIC-01`：03Hの推測を訂正。成功パーサにおいてentries `E<=0xFFFFFF`、classification count `B=ReadBits(6)+1` は `1..64`、dimension `D>=1` のとき `0x005DFF80 IMUL` の後で `0x005DFF83 CMP` と `0x005DFF85 JG reject` が累積 `B^D > E` を排除する。帰納的に直前の `P<=0xFFFFFF` と `B<=64` なら次の乗算は最大 `0x3FFFFFC0 < 0x7FFFFFFF` で符号overflowしない。未改変状態でinitへ伝播すれば `0x005E00EF` の `P*4 <= 0x03FFFFFC`、同条件下の分母非ゼロを静的に支持。**alias書換、別のinit入口、メモリ確保失敗・実ゲーム到達性はVERIFY**。03Hを削除・重複計上しない。
3. `REA-OFFLINE-20261101-05H-P0-VORBIS-RESIDUE-EOF-LATCH-PARSER-INIT-GATE-STATIC-01`：04Hの正常readerという前提を補強。最初の6bit読込 `0x005DFE5C` がEOF -1なら `0x005DFE61 INC` により一時的にB=0となるが、reader `0x005E6E10` のEOF cursor/flagラッチにより続く8bit読込 `0x005DFE68` も -1となり、`0x005DFE75 JL` がパーサ失敗へ進む条件付き経路。以前の`REA-LOCAL-20261031-07H-P0-VORBIS-BITREADER-EOF-BOUND-STATIC-01`のEOFの再発見には数えない。特殊reader改変、異常aliasと本物のVorbis type2パケットは未検証。

## 原資料の所在・SHAと独立照合の限界
Library上の各元レポートとreadback receiptを今回**直接閲覧**。下記のファイルSHAはその当時のreadback記録からの**保存済み受領値**であり、今回PC現物の当該MD bytesを再hashした意味ではない。

| 研究IDの時台 | LibraryのREPORT（出典basename） | 以前のreceipt記録SHA256 | 旧監査履歴 |
|---|---|---|---|
| 03H | `REA_OFFLINE_20261101_03H_CODEBOOK_DIMENSION_REPORT.md` | `D64F34432FF9DEEB75C7D54DA24C60812F98EA18C0E67121051954D4B5CF744B` | 81/81 STATIC |
| 04H | `REA_OFFLINE_20261101_04H_RESIDUE_POWER_BOUND_REPORT.md` | `E97C8188341EE702E41475CBD87E5E4E64ED4A4974DD90EF0936D039481C3B91` | 100/100 STATIC |
| 05H | `REA_OFFLINE_20261101_05H_RESIDUE_EOF_LATCH_REPORT.md` | `A52B5A3C705D5180CB3FB88172CD0CB0675E5D2A7A85C4424EE35561A37A36AF` | 170/170 STATIC |

Library根拠ディレクトリ `/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`。元資料には各時台の `*_EVIDENCE.json / *_AUDIT.py / *_READBACK.json`、一部 `*_LIBRARY_RECEIPT.json` があり、元実体はGitHubにコピーしていない。旧オフライン索引 `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、元ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。元PEのSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。

**今回PC上で限定再確認した命令窓**：`0x005D9F64`（source→compiledのmov pair）、`0x005DA0B2`（同）、`0x005DFF80`（IMUL/CMP/JG、窓SHA `9C0748651F0C8696F55D4771A26087FF275FBD911E7E20EFA66CB7BEF38F0083`）、`0x005DFE5C`（6bit→8bitの連続CALL、窓SHA `9E453A15C3D28D1375EB77A1E0B0CC60FD74CDD53280D15820C82641023A5EA8`）、`0x005E0E0C`のIDIV。統合V9は今回 read-only検索済み、PE/V9 SHA一致とSQLite quick_checkは別の同run P0監査でPASS。**旧81/100/170監査の全項目を今回再実行したわけではない。**

## KB_CANDIDATE・次の検証と未統合数
owner `REA/T015`、参照VA `0x5D9F40/0x5DA070/0x5DFE10/0x5DFFC0/0x5E0DC0/0x5E6E10`、CALL site `0x5DFE5C/0x5DFE68/0x5D5922/0x5D5B51`、offset `inner+0xB20`, `entry+0x00`, `instance+0x10`, `reader+0x0C`。候補は既存 `REF_AUDIO_VORBIS.md` の正常init／異常EOF境界および必要な住所辞書へcuratorが反映する。**本3件は旧研究の再公開であり、新正式5点証拠完備0、VERIFIED0、原作Golden PASS0、strict MATCH0、READY0**。

今回の3 IDを除く03–16Hオフライン回収残は**11 ID**（14から3を減算。別の11/1 01–02Hや17–23H成果との重複は別管理）。06H以降はPrivate Issue #3 のソース・訂正と照合し、owner限定intakeへ段階的入庫する。正常パーサからinitまでの同一オブジェクト寿命／alias書換、実データtype2到達性、malloc失敗動作はVERIFYのまま。
