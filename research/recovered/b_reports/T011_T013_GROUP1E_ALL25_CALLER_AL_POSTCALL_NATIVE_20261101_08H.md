# 迫真戦記 ver0.67｜新B 2026-11-01 08H｜group+0x1E setter全25直接CALLのAL入力と直後の処理分類

**研究ID** `B-OFFLINE-20261101-08H-T011-T013-GROUP1E-CALLSITES-AL-POSTCALL-01`。Owner B・T011/T013、T028との関係はVERIFY、T012/T024に新規READYなし。
**判定** `OFFLINE-UNSYNCED / STATIC_NATIVE / STATIC_GHIDRA / INFERRED / VERIFY / NOT READY`。原作Golden PASS=0、strict MATCH=0、READY新規0。

## 1. 証拠・回収・安全監査
- 08Hの最初にDesktop Commander Local CompactでPCの `MASTER_LEDGER.md` を`read_file`で要求したが、`UNAVAILABLE: MCP SSE probe returned 429 from openai.org` となりPC最新正本未確認。**接続障害（transient 429）でありSAFETY_REFUSALではない**。Remoteや他shell経由での同拒否操作の迂回なし。
- 研究PCにあるか不明な03H保存結果は**UNKNOWN**。04H～07HはChatGPT作業環境の既存報告と独立readback receiptを確認。今回08Hも**PC/GitHub未同期**。今回の生成は新規研究IDで行い、既存IDやPCファイルは上書きしていない。
- 認可済みChatGPT Libraryの`Vahren.exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`HAKUSHIN_B_LANE_SAFE_RECOVERY_20261029_V3(4).zip`を読み取り専用で使用（原作の起動なし）。原作SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、旧ZIP 911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2（CRC34/34）、SQLite 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（quick_check=ok）、B安全復旧ZIP 059B91381C1B58214353769006E0F4049FCDE393A6B7970F4513602878A2B2C9（CRC136/136）がいずれも期待値と一致。
- B安全復旧ZIPの134ファイルは旧スナップショット、保留21件は変更せず。旧B ZIP 136エントリ中で今回の `0x5695B0/0x568FB0/0x5282C0/0x5284A0` 具体的論点の本文ヒット0。GitHub private `develop` の `README.md`、`SYNC_STATUS.md`、`symbols.tsv`（blob `3fcf2d436c21f3fc91791a91e75c9a800167ca4d`）、`structs.tsv`、`GHIDRA_V9_B_REVIEW_TOP150.tsv`、`KNOWLEDGE_CURATION_PROTOCOL.md`、`REF_BATTLE_AI_MORALE.md`を閲覧し、関連する既登録シンボル、研究境界を参照。**最新PC全文索引との非重複はVERIFY**。
- 過去の禁止VA `0x5710C0..0x571500`、既拒否操作・証拠は調査・取得・迂回していない。再逆コンパイル/全体Ghidra起動/原作ゲーム起動/他ownerファイル改変/Git操作なし。

## 2. 新規：0x5695B0に入る25直接CALLの隠れたALはすべてnativeで設定済み
- 旧検索SQLite `calls` が列挙する `callee_va=0x005695B0` は**25 E8 site / 14 caller関数**。この**25件についてのみ**全件独立にnative E8相対変位を復号してターゲットが `0x5695B0` となることを確認。間接CALL/vtableはこの数に含めない。
- 25/25件でCALL直前2バイトが `32 C0`（`xor al,al`）または `B0 01`（`mov al,1`）である。`AL=0` **21件**、`AL=1` **4件**。旧Ghidraの `FUN_005695b0` が `in_AL` を示すだけでは呼び出し契約が隠れるが、今回の直接CALLでは動的な未定義ALを経由しない。**フックABI全体が確定したわけではない**。
- 07Hに独立確認した `0x5695B6: mov [ebp+0x1E],al` と `0x5695E3: E8 -> 0x576F70` への追加証拠。新規なのは**全25 siteのnative入力値／直後の経路分類**であり07Hの既発見setterは新発見として二重計上しない。

## 3. CALL直後の処理：AL=0を2系統へ分離（新規）
- **AL=0の18件**：`CALL 0x5695B0` の直後に `push esi; E8 -> 0x568FB0`。このヘルパーは `0x568FB6: cmp byte ptr [group+0x1D],0`、`0x568FBC: je 0x569031` により **group+0x1D==0ならヘルパー本体を通らない**。非ゼロ経路では各メンバーの `Unit+0x1867D=0`、生存Unit（`+0x1867C==0`）だけ再評価 `0x568FED E8->0x576F70`、非空ベクトルのendポインタ更新 `0x569027`、`0x56902C E8->0x569280` が確認できる。グループ状態更新とmember解除は別ゲート。
- **AL=0の残り3件**（`0x420269`、`0x528356`、`0x528416`）：直後は `ESI` に対象を設定し `E8->0x568460`。こちらは生存メンバーの `Unit+0x186A4` と `+0x186A8` に `0x80000008` を書き込む (`0x568487`,`0x56848D`)。`0x568FB0` の`group+0x1D` 分岐／member+0x1867Dクリアとは**別の後処理**であり、同一の「group reset」に統合してはいけない。
- **AL=1の4件**（`0x527BAD`、`0x5280C9`、`0x52830C`、`0x5284EA`）はいずれも直後の`0x568FB0`/`0x568460`呼出を示さない。`0x52830C`に限り `push edi; E8->0x529B60`を確認。追加関数のゲーム的な役割やランタイム到達可能性はVERIFY。

### 25 CALL site独立検証台帳（元PE bytes + 旧Ghidra静的索引）

| E8 CALL site | Caller関数 | AL | 直後の経路 |
|---|---|---:|---|
| `0x00402031` | `0x00401EE0` | 0 | `0x568FB0` |
| `0x004021C7` | `0x00401EE0` | 0 | `0x568FB0` |
| `0x0041FF3B` | `0x0041FE00` | 0 | `0x568FB0` |
| `0x0042003E` | `0x0041FE00` | 0 | `0x568FB0` |
| `0x004201C4` | `0x0041FE00` | 0 | `0x568FB0` |
| `0x00420218` | `0x0041FE00` | 0 | `0x568FB0` |
| `0x00420269` | `0x0041FE00` | 0 | `0x568460` |
| `0x004202FD` | `0x0041FE00` | 0 | `0x568FB0` |
| `0x004B5D5A` | `0x004B4710` | 0 | `0x568FB0` |
| `0x004C709E` | `0x004C7040` | 0 | `0x568FB0` |
| `0x004C74DF` | `0x004C72C0` | 0 | `0x568FB0` |
| `0x004C7576` | `0x004C72C0` | 0 | `0x568FB0` |
| `0x00526D38` | `0x00526A40` | 0 | `0x568FB0` |
| `0x00526FB2` | `0x00526E50` | 0 | `0x568FB0` |
| `0x00527A92` | `0x00527890` | 0 | `0x568FB0` |
| `0x00527BAD` | `0x00527890` | 1 | 指定3helper直後なし |
| `0x00527C9A` | `0x00527890` | 0 | `0x568FB0` |
| `0x00527F95` | `0x00527F60` | 0 | `0x568FB0` |
| `0x005280C9` | `0x00527F60` | 1 | 指定3helper直後なし |
| `0x00528186` | `0x00528150` | 0 | `0x568FB0` |
| `0x0052830C` | `0x005282C0` | 1 | `0x529B60` |
| `0x00528356` | `0x00528320` | 0 | `0x568460` |
| `0x00528416` | `0x00528320` | 0 | `0x568460` |
| `0x005284EA` | `0x005284A0` | 1 | 指定3helper直後なし |
| `0x0052857C` | `0x00528540` | 0 | `0x568FB0` |

## 4. 出典と再現
- 元PEからの命令根拠：setter `0x5695B6`、cleaner `0x568FB6/0x568FBC/0x568FDD/0x568FED/0x569027/0x56902C`、sentinel `0x56847E/0x568487/0x56848D`。25サイトの原バイト（`AL_setter_site`、`E8`）とcaller所有関数、pseudoSHAは `data/B_OFFLINE_20261101_08H_GROUP1E_CALLSITE_EVIDENCE.json` に個別記録。
- 旧Ghidra擬似C `full_pseudoc_20261020/functions/0056/005695B0.c` lines 14-29 SHA `E77606970E7A7CFD3A614DE73111383A632C7C52773251301AD044D2DE613D96`、`00568FB0.c` lines 14-39 SHA `D7BAF26F8AAD7FA6E86AECACD45197400EE7F5484D9141C3FCAD25C0102AFD79`、`00568460.c` lines 14-30 SHA `927E3DCB39A67DF02A3BAA5A10F572D5957B720DC619CEC113E2A2EE3BA12CFB`。元ASMと意味の衝突時はnative優先。`0x568FB0`へのCALLsiteと`0x568460`へのCALLsiteはソース差分上も区別する。
- 再現スクリプト `data/B_20261101_08H_GROUP1E_CALLSITE_READONLY_VERIFY.py` は原作EXEとzip/sqliteをread-onlyで照合し、25 native E8、AL命令25、直後helper分類、2関数の条件分岐・書込native bytes 9、焦点関数6 pseudo/native SHAを検査。生成JSONの状態はSTATICのみ。

## 5. 知識統合候補と研究リスク
- **KB_CANDIDATE**：`0x5695B0`の明示的AL=0/1分布（旧索引内25 direct sites）、`0x568FB0`の`group+0x1D` gateと`Unit+0x1867D=0`、`0x568460`の`Unit+0x186A4/A8` sentinel clear、AL=1の条件付きメンバー追加とみられる別経路。既存`group+0x1C`（喪失集約）・`+0x1D`（group処理ゲート）・`+0x1E`（setter入力）を同名に統合しない。研究PC復帰時に辞書重複・owner・V9現行・READYを照合して専任統合担当に委ねる。
- **VERIFY**：`group+0x1D`の意味、clearとaddの実際のゲーム状態、`0x569280`の計算/乱数・副作用、Unit/SimpleUnit/StaticUnit別の入力到達、全25条件分岐の実機実行率とタイミング。`group+0x1C`と士気・敗走の同一視禁止。
- **Golden必要条件**：同一ver0.67でAL0/1の4経路、group+0x1D=0/1、member vector空/1/複数、member+0x1867C=0/1、member+0x1867D=0/1、`+0x186A4/A8`のBefore/After、グループ+0x1C/+0x1E、タイマー・DAT・RNG・対象候補順を原作実機で観測。実機原作Golden PASS **0**、strict MATCH **0**、新規正式READY **0**。
- **既存未解決P0**：T011の召喚EXP/親子/死亡と+0x1Dリセットの整合、T012のダメージ・回復・状態、T013の最終対象選択、T024通常AI、T028士気・敗走。今回の結果はこれらを解明済みへ昇格しない。

## 6. 未同期・再開点
- 03HのPC書込みtimeoutは存在/内容/SHA未確認。04H/05H/06H/07Hのsandbox成果は過去の独立readbackの状態を継承。今回08Hは新規 sandbox 成果のみ。10/25原文不足・GitHub B資料保全不足・保留21は引き継ぎ、SAFE134のPC最新全件再検証は未実行。
- PC復帰後はまず新解析でなく最新`MASTER_LEDGER`、`ANALYSIS_LANES_PROTOCOL`、`LANE_B_HANDOFF`、安全拒否/復旧索引、03Hファイルを読み戻す。続いて04H～08HのID・SHA・owner・重複・READYを照合してB所有文書に一度だけ採用。共有KB/MASTER/GitはBから触れない。
- オフライン次回は `0x568FB0`のgroup+0x1Dの設定元・解除元の安全な既存証拠、`0x569280`の後処理の分岐、4つのAL=1 callerで登録条件を比較する。禁止領域・既拒否根拠は未接触のまま。
