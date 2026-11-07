# 迫真戦記 ver0.67 / REA独立T014：byte→DWORDセーブ形式のUnit 7連続フィールドと非正規wire再書込の境界

- **記録ID** `REA-OFFLINE-20261022-0937-T014-WIRE4-UNIT7-CANONICAL-01`／作成 `2026-10-22T09:46:39+09:00`
- **状態** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。所有範囲はREA独立T014。PC正本・MASTER・QUEUE・PROGRESS・原本EXE/SAVE・Gitは未変更。
- **接続復旧ID** `REA-RC-20261022-0937-LOCAL-SESSION-TERMINATED-01`。Local CompactでMASTER/規約/REA README・QUEUE・PROGRESSの先読を一括試行した結果、`INVALID_ARGUMENT: McpServerError: Session terminated`。**CONNECTION**であり安全拒否ではない。PC電源状態不明。最新runs/QUEUE/PROGRESS/owner/lockの確認不能＝PC正式同期不可。
- **offline入力** Libraryユーザー提供 `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。ZIP CRC 34/34 PASS、SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、検索CLI SHA256 `DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0`はBUILD_MANIFESTと一致、SQLite `integrity_check=ok`。元EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` はmanifest記録値で原EXE現物の再hashではない。
- `research_snapshot/MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、`rea_lab/decomp_task/PROGRESS.md` は先読したが、**2026-10-09の旧スナップショット**。現PCの最新REA既存runは未閲覧。既存の報告上Wave1〜5 64/64 VERIFIEDは今回新規計上せず、旧ZIP内15/16へ巻き戻さない。

## 新規の横断静的証拠（2026-10-22 08:43既知の+0x1C/+0x1Dの単なる反復ではない）

**1. Unit reader `0x0058E870`の7連続byte**：保存済みGhidra疑似Cが `0x4707D0`に `object+0x74`、`+0x75`、`+0x76`、`+0x77`、`+0x78`、`+0x79`、`+0x7A`をこの順に渡す。直接CALL索引 sites は `0x58E8F3 / 0x58E903 / 0x58E90F / 0x58E91B / 0x58E927 / 0x58E933 / 0x58E93F`。その後`0x470700(object+0x80)`で4-byte値を取得する（親関数の該当個所）。**この7フィールドのwire転送要求は各4バイト、合計28バイト**（ストリーム正常時）。メモリ上は連続7バイトであり、単純な7バイトmemcpy方式では互換性を失う。`+0x70`のDWORD読込は7件より前、`+0x80` DWORDは7件の直後にある。従って**7連続byteと直後のDWORD**の転送要求幅は `7*4+4=32バイト`。さらに先行`+0x70`のDWORDも合算すると対象フィールド合計36バイトだが、**間に文字列読込があるため36バイトの連続固定長ブロックではない**。

**2. Unit writer `0x0058EFD0`の独立対応**：検索DBの`0x4708A0`直接CALLは sites `0x58F03D / 0x58F047 / 0x58F051 / 0x58F05B / 0x58F065 / 0x58F06F / 0x58F079` の**7連続件**と、別位置`0x58F1E1`の追加1件。reader側にも前記7件とは別に`0x58EA95`に1件あり、双方計8件。`+0x80`の書込はwriter疑似Cで7連続CALLの直後に配置される。**7対7の個数と順序は静的に一致**するが、writerの各呼出し元ALのフィールド割当はGhidra疑似Cが省略しているので個別オフセットまで確定とはしない。

**3. 二連byte decoder `0x005964C0`の中間状態**：CALL sites `0x59650D→0x4707D0`（`+0x1C`）→`0x59651D→0x4707D0`（`+0x1D`）。対応writer `0x596AE3/0x596AED→0x4708A0`。`0x4707D0`の保存済み疑似Cは `0x42E700`による4-byte読込→stream state検査→異常なら`LoadException`→正常なら`DAT_00B060E8`下位1byteを格納、という順序。第1成功・第2失敗では、少なくともhelper直列実行中は第1byteの代入後に第2の例外が発生し得る。**外側catch・オブジェクト破棄・巻き戻しの有無は未解決**。ユーザーに見えるセーブ破損や部分適用バグがあると断定しない。

**4. noncanonical wireの再書込正規化**：`0x4708A0`は入力byteを`&0xFF`として4-byte書込、`0x4707D0`は4-byte読込後に最下位1byteだけを採る。したがって成功した読込と再書込を合成すると、例えば `78 56 34 12` → **値`0x78`** → `78 00 00 00`。上位3byteの非ゼロを拒否する局所検査はGhidra疑似Cで確認できないが、**上位レイヤーの別検査がないことは未証明**。byte値に対して `decode(encode(byte))` は合成モデル上同一だが、任意の4-byte入力に `encode(decode(wire))==wire` は成立しない。

## 合成検査（ゲーム実行ではない）

- Pythonで `state=0..255` に対する読込ヘルパーの異常ガードを構造式で比較。`(((state>>2)|state)&1)!=0 || (state&6)!=0` と `(state&7)!=0` は **256/256同値**。ガード真224、偽32。**実ストリーム状態の分布や例外到達率を意味しない**。
- 全byte `0..255` のゼロ拡張4-byte形式の合成往復 **256/256一致**。2種類の非ゼロ上位3byteを添えた入力 **512/512で正規化により元wireと不一致**。
- 7 flagsの合成fixture: `00 01 7F 80 FF 55 AA`（メモリ側）→ `00 00 00 00 01 00 00 00 7F 00 00 00 80 00 00 00 FF 00 00 00 55 00 00 00 AA 00 00 00`（wire側28byte）。**NOT RUN / NOT GOLDEN**。

## 根拠・5種類証拠・重複防止

| VA | Ghidra疑似C SHA256 | 今回の役割 |
|---|---|---|
| `0x4707D0` | `A6F57840EB564D48C00D8757E6CE0CDEB98DE66016C5C5C327BC6E429DF3A45B` | reader helper/state gate/格納順 |
| `0x4708A0` | `4A51D26D7141B63406F7EDEF0FE7A04E5B34AE4DC8BD7905C3A2FDDDE08ADD43` | 4byte zero-extended writer |
| `0x5964C0` | `A3A43FB167F7CEDE8A2E9AB94D364F8B62CC2F13A62294BDB3BA1868C7C5F41A` | 2byte連続読込 |
| `0x596AA0` | `AC59C5508CEA1686A98F84FF9D72F58F7C476D70CB6479E5DCD5A189B3858D11` | 2byte連続書込 |
| `0x58E870` | `6DA6821B4DD091F6F6BADE169E0CD7AC49CB8F7F2FD8DA371D98F742537E9CE7` | Unit側7+1 caller |
| `0x58EFD0` | `48EE29E392738F66450D2473ACDB27C00D617FFBE3270912381C21C1B800587A` | Unit側7+1 writer |

SQLiteは各関数の`code_sha256`を実コードテキストから再計算し **6/6一致**。検索DBのinfo相当・pseudo・callers・calleesは使用できたが、**REA正式5種類（info/pseudo/assembly/callers/callees）を各関数で取得して確認したわけではない**。該当ASM・詳細call-siteレジスタ・正常return・ABIは今回未取得、REA新規`VERIFIED=0`。過去の2026-10-22 08:43報告が発見済みの+0x1C/+0x1D、byte wire4、2フィールド8byteは**新規発見として再計上しない**。またA所有の古い資料ですでにUnit reader/writerの存在が指摘されているため、関数同定そのものも新規扱いにしない。今回の増分はUnit **7連続fieldの幅／caller順序**、上位3byte非canonical再書込、例外時の中間状態条件。

- **正式指標**：Wave1〜5 `64/64`はユーザーの前回までの**PC過去報告値**（今run未検証）、Wave6候補TODO12/BLOCKED4も前回報告値。新規`VERIFIED=0`、新規5種類証拠充足0、公式TODO/VERIFY/BLOCKED変更0（PC未確認ゆえ新差分認定しない）、旧EXE実機Golden PASS=0、新旧strict MATCH=0、実ゲーム実装率未測定。
- **新規Ghidra/REA起動**：0。原EXE起動0。PC CPU/RAM不明（PCアクセス不可）。今回のローカルSQLite軽量検証スクリプト実行は `0.462秒`；作業全体時間未計測。既拒否VA/操作再試行0。
- **保存**：PC側保存/読戻し `NOT DONE`。このMarkdownとJSONをLibrary `迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED`に別々に保存しreadbackの可否を検証する。PC復帰時は最新MASTER/QUEUE/PROGRESS/owners/lock/既存ID/sha照合後に一度だけREA所有範囲へ同期すること。Library保存成功はPC正本同期を意味しない。
- **次の安全な再開位置**：承認済み保存native ASMにある`0x59650D/0x59651D`の呼出し時のstack/レジスタを確認し、`0x4707D0`の隠れたdest pointer ABI（疑似Cに`void()`と未初期化`puStack_c`がある）を確定する。Unit writer 7件`0x58F03D..0x58F079`のAL出所を保存済み合法ASMで追跡する。第2読込失敗時の外側巻き戻しは独立したGolden条件として設計し、実測まではVERIFYのままにする。
