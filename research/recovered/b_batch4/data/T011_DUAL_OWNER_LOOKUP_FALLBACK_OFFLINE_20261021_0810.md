# 迫真戦記ver0.67 新B T011｜2種類のowner-tree lookupと`0x583CF0`フォールバック（08時台／OFFLINE）

- **研究候補ID:** `B-OFFLINE-20261021-0810-01`。担当B/T011。**正式証拠IDではない**。状態 `STATIC-SAVED-PSEUDOC / INFERRED / VERIFY / OFFLINE-UNSYNCED / NOT READY`。
- **接続復旧ID:** `B-RC-20261021-0810-LOCAL429-01`。2026-10-21 08時台 JSTにDesktop Commander Local Compactで `%USERPROFILE%\Documents\迫真戦記\_REDEV_RESEARCH\MASTER_LEDGER.md` の末尾を読取試行。実エラー `UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。分類CONNECTION/TRANSIENT（**安全拒否ではない**）。Remote不使用、PC正本への保存/最新版照合は未実施。
- **出典:** ユーザー提供 `HAKUSHIN067_AI_OFFLINE_PACK_20261021(1).zip` outer SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。ZIP 34件CRC PASS。`search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` とBUILD_MANIFEST一致。SQLite複製は`mode=ro&immutable=1`、`search.py`は派生コピーを検索。原本EXEは実行・書換なし。
- **原作識別:** ver0.67 EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` はZIPマニフェスト記載値。今回EXE実体ハッシュ再算出なし。資料はGhidra生成擬似Cであり原作ソース/ASMや実機挙動ではない。
- **独立照合:** `0x00583CF0`、`0x00583DC0`、`0x00467E90`、`0x00467DE0` のSQLite擬似CはZIP内全関数擬似Cの同名 `.c` と4/4 byte完全一致。関数コードSHA先頭16桁: D4F4F50FFBA4DA16 / 9ACAED8DB47886D4 / 71E2830BF144D1F0 / BBAABFDEFFD065F8。

## 新しいSTATIC差分A｜2つの検索関数は別tree headと別backlinkを使用

| 関数VA | lookupに使うcontext上のhead | hit条件と返値 | **hit時の書込み** | 共通callee |
|---|---|---|---|---|
| `0x00467DE0` | `context+0x300` | 結果node != headで`node+0x28`のrecordを返却、missでは0 | `record+0x1A4 = context` | `0x004C1200`（site `0x00467E1C`） |
| `0x00467E90` | `context+0x2F0` | 結果node != headで`node+0x28`のrecordを返却、missでは0 | **`record+0xB0 = context`** | `0x004C1200`（site `0x00467ECC`） |

- 両lookupに共通する `0x004C1200` は内部で `0x004682B0`（site `0x004C1209`）と `0x00402C40`（siteはDBを必要時参照）の比較を利用する。ルーチン共有は同じ木インスタンスや同一型の証明ではない。headは明確に`+0x300`と`+0x2F0`で異なる。
- **今回の増分:** 前回 `B-OFFLINE-20261021-0716-01`で既知の`0x467DE0`→`record+0x1A4`に加え、今回新たに`0x467E90`→`record+0xB0`という**第二のbacklink書込み**を確認。`+0x1A4`と`+0xB0`を同一フィールドに潰さない。両者が同一Unit型とは未確定。

## 新しいSTATIC差分B｜`0x00583CF0`の二段階処理と戻り値

- 擬似C入口の条件：`*(int*)(in_EAX+0x94)==0`のとき、`context=*(int*)(in_EAX+0x1A4)`、`head=*(int*)(context+0x2F0)`としてheadを起点に走査。ループの対象recordは`node+0x28`、そこから`record+0x20`を参照し、`0x00415460`（CALL site `0x00583D63`）で比較。`*piVar5 != iVar3`なら`return iVar2`の早期帰路がある。
- ループの走査更新は`0x00405440`（site `0x00583D70`）。この関数にはtree nodeの`+0x2D`を使ったnext候補処理がある（RAW STATIC）。
- 上記走査で早期returnしなかった場合、**`0x00583D82 -> 0x00583DC0`**を呼ぶ。返値が0、または返値recordの`+0x94`が0なら即0を返す。`0x583DC0`の既知STATICでは入力`+0x78=0 && +0x94=0`のときownerの`+0x300`を走査し、別候補を返す場合がある。
- このフォールバックを通過できた場合（または最初から入力`+0x94!=0`の場合）、擬似Cではrecordの`+0x84`から`0x00402710`を呼び出す（site `0x00583D27`）。`0x00402710`は文字列の長さ/容量を参照するコピー系helper候補。その後**`0x00583D32 -> 0x00467E90`**へ進む。`0x467E90`が成功すると、返されたrecordの`+0xB0`を更新する。
- この経路は**`0x583DC0`で代替record探索→`0x583CF0`で`+0x94`再検査→`+0x84`を用いた`0x467E90`再検索**という二段階の静的候補。`0x583CF0`擬似Cには`in_EAX`等の暗黙レジスタや疑似スタックがあるため、厳密なthiscall引数・返却されるrecord同一性、`+0x84`のゲーム上の意味、`0x402710`の実際の引数配置はASMで要VERIFY。疑似C本文の行順はmachine CALL site昇順と一致しないため、実命令の直列順と誤認しない。
- 直接CALLの個別siteは保存済みSQLiteの`calls`表を照合した。`0x583CF0`内：`0x583D27 -> 0x402710`、`0x583D32 -> 0x467E90`、`0x583D63 -> 0x415460`、`0x583D70 -> 0x405440`、`0x583D82 -> 0x583DC0`。このsite列挙が各条件分岐の動的実行を保証するわけではない。

## 再実装・Golden境界

- **実装影響（INFERRED）:** `+0x1A4` と `+0xB0` の2つの検索由来参照、および`context+0x2F0`と`context+0x300`の異なるindexを区別し、`0x583CF0`の早期return・フォールバック失敗0・lookup成功の境界を保持する。いずれも原作の可視目的、所有権/寿命/破棄規則の確定ではない。
- **Golden（DESIGNED/NOT RUN）:** 原作合法操作で同名member、未配置member、既存/再生成member、異所属などの差を作れるかを先に調査。旧EXE・DAT・SAVE・MAP・入力/seed観測可否・capture SHAと同じ新実装条件を記録し、可視ユニット数/所属/能力/選択結果を比較。非可視内部head・backlink・`+0x94`等を旧実機観測できなければUNKNOWN、捏造MATCH禁止。
- **実測:** 新規原作DYNAMIC OBSERVED 0、原作Gameplay Golden PASS **0**、strict MATCH **0**、B限定READY追加 **0**、E MASTER統合追加 **0**、Task DONE追加 **0**。ASM/native実効果・DAT到達条件・RNG順は未確認VERIFY。安全拒否された旧VA領域は今回検索・逆解析なし。

## 重複・回収・再開

- **前回との差分:** `B-OFFLINE-20261021-0510-01`は生成再入、`0610-01`は第一backlinkと挿入、`0716-01`は第一tree内部head`+0x300`と後段消費。今回に限る追加は**第二lookupの`+0xB0`/`+0x2F0`区別と`0x583CF0`の分岐後lookup接続**。2026-10-21収録のT011/B HANDOFFスナップショット内で今回3VA（`583CF0`、`583DC0`、`467E90`）の説明は未検出、現時点のLibrary B dataに同名文書無し。最新PC資料との内容重複・予約・統合状態は接続429で未確認。重複確定・READYにしない。
- **旧復旧索引:** 10/20分26候補二次分類`X14/P4/I0/D1/C4/L2/O1`と過去PC回収12ファイルは**履歴**。旧安全拒否12件、168行不完全JSON INVALID、`B-OFFLINE-20261021-0200-01` PC同期時のタイムアウト/状態不明は継続。今回旧成果のPC実体回収0件、既拒否操作の再試行0件、クラウド新研究記録だけを保存対象にする。
- **保存:** Library `/迫真戦記再開発プロジェクト/data/T011_DUAL_OWNER_LOOKUP_FALLBACK_OFFLINE_20261021_0810.md` にこの文書を保存し、別readで研究ID/CALL/NOT READY/復旧IDを確認する。**PC未保存／PC HANDOFF未更新。** 読み戻し成功前はクラウド保存済みと断言しない。
- **次回:** PCが使える場合は新規調査より前にMASTER最新版/TASK QUEUE/規約/B HANDOFF/5owner/復旧索引と重複・拒否ID・予約を読取、`0200`のPC部分保存有無もwriteなしで確認し、非拒否の未同期差分だけ保存/独立readback。オフラインなら`0x583CF0`の各直接callerの入力条件（`+0x94=0/非0`）および`0x467E90`の呼出元/ASM引数を軽量検索。`+0x78/+0x94`のwriter確認は可能な証拠範囲のみ。原本・他owner・MASTER・REA/dev_lab・Git/push・Work/Remote・スケジュール/設定変更なし。PC CPU/RAM実負荷不明。
