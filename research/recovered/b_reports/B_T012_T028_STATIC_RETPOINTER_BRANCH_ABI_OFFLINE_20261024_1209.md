# 迫真戦記 新B｜T012/T028 StaticUnit死亡時のオブジェクト取得ABI（OFFLINE）

- 研究ID: `B-OFFLINE-20261024-1209-T012-T028-STATIC-RETPOINTER-BRANCH-ABI-01`。日時 2026-10-24 12:09 JST。
- 復旧ID: `B-RC-20261024-1209-LOCAL-SESSION-AND-PRIOR-REFUSAL-BOUNDARY-01`。状態 **OFFLINE-UNSYNCED / STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / VERIFY / NOT READY**。
- PC接続: Desktop Commander Local Compact最優先の `MASTER_LEDGER.md` 読取で `McpServerError: Session terminated`。CONNECTION障害で、安全拒否の代替経路探索は実施しない。最新PC MASTER / B HANDOFF / owner / READY / 22回収vs10研究重複 / 訂正版2件 / 旧拒否本文の照合は不能。
- 証拠: Libraryから取得した `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34件CRC PASS。原作Vahren.exe SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（manifest一致 / quick_check=ok）。いずれも読み取り専用で、PC正本ではない。Ghidra/REA再解析・原作ゲーム起動・EXE/DAT/SAVE変更なし。

## 今回の新規増分：擬似Cの `void` と原作EAX戻り値が食い違う

StaticUnitの vtable+0x70 = `0x0055ABA0` の死亡・文字列非空経路では、`0x0055AC35 SUB ESP,0x1C` で28バイトの一時文字列用領域を確保。`0x0055AC54 CALL 0x00402710`で`Unit+0x1E7F8`から文字列を複製し、`0x0055AC59 MOV ECX,[EDI+0x1DC]`の後、`0x0055AC5F CALL 0x004678A0`へ渡す。

**Ghidra SQLiteの`0x004678A0`擬似C宣言は `void __thiscall FUN_004678a0(int,undefined4)` だが、これは戻り値について不十分。** 原作ASMにはEAXを明示設定する少なくとも3つの経路がある。

| 原作VA | 事実（原作ASM） | 解釈 |
|---|---|---|
| `0x004678DA` | スタック側条件が0かを判定 | 空/特殊経路候補（入力式の厳密型はVERIFY） |
| `0x00467928` | `MOV EAX,0x00B08698` | グローバル構築済みレコードを返す経路 |
| `0x00467974` | `MOV EAX,ESI`（直前に`ESI=[EAX+0x28]`） | 辞書で既存ノードが見つかった時の結果参照 |
| `0x0046799B`→`0x00467A1A` | `EDI`に生成先を保持し`MOV EAX,EDI` | 新規構築レコードを返す経路 |
| `0x00467A3A` | `RET 0x1C` | スタック側28バイト引数をcalleeが回収 |
| `0x0055AC65` | `CMP DWORD PTR [EAX+0x74],EBX`（直前にEAX変更なし） | **呼出元がEAXの参照先を即座に使用する確証** |

Ghidraのvoidだけを信じて戻り値を消すと、この死亡時の分岐を再現できない。戻り先の**厳密なC++型・所有権・非NULL保証はVERIFY**。新規生成時の割当失敗条件まで原作BUGと断定しない。

## 出力レコード`+0x74`による2分岐にはABI差

`0x0055AC65 CMP DWORD PTR [EAX+0x74],EBX` / `0x0055AC68 JNE 0x0055AC7E` の直後、いずれも外側の先行`PUSH EBX`を維持したまま異なるCALLへ進む。

| `record+0x74` | CALL site | CALL直前の付加レジスタ・スタック | 呼出元での回収 |
|---|---|---|---|
| 0 | `0x0055AC71 → 0x00580280` | `PUSH EBX,EDI,EAX`、`EDX=0,ECX=0` | `0x0055AC76 ADD ESP,0x10` = 合計4引数分 |
| 非0 | `0x0055AC84 → 0x0054F720` | `PUSH EDI,EAX`、`EAX=0,ECX=EDI` | `0x0055AC89 ADD ESP,0x0C` = 合計3引数分 |

**両経路は単なるcallee差ではなく、caller側スタック引数数とレジスタ準備も異なる。** `0x0054F720`のグローバル再利用poolの存在自体は2026-10-21 B既存成果なので新発見として計上しない。`0x00580280`については呼出siteだけを証拠に使用し、関数本体は調査・検証対象から除外する。

## 安全境界・再開記録

今回の静的検索の初期段階で、歴史的拒否範囲の照合が遅れ、**既拒否領域`0x0058021E..0x00580340`に含まれる`0x00580280`へ1回CLI function問合せを発行してしまった**。既存B snapshotの拒否記録を見つけた時点で範囲の再取得を中止し、その出力を今回の解析根拠・成果には使用していない。以後の当該callee本体再読取・別経路迂回は0件。既拒否`0x005710C0..0x00571500`も調査していない。**この確認順序の誤りは解消済みと偽らず、復旧IDで次回へ引き継ぐ**。次回、過去拒否一覧を照合してからアドレスベースのクエリをする。

既存重複境界: B snapshot T012/T011/HANDOFF内で`0x00467928`/`0x00467974`/`0x00467A1A`/`0x0055AC65`/`0x0055AC71`/`0x0055AC84`の記載0件と確認。旧Bで知られた`0x0054F720` pool・StaticUnit vtable・文字列長分岐・AL=1の既死問題は既成果として扱う。**PC最新全IDとは未照合でREADYにしない。**

## Golden条件・次P0

原作実機のGoldenには無改変ver0.67 EXE SHA・DAT・同一SAVE/MAP・同一Unit型/Skill/入力/RNGを固定し、StaticUnit死亡時の文字列あり/なし、解決先グローバル/既存/新規と`record+0x74`の0/非0、両後続CALLの対象/副作用・EXPs/イベント・レコード寿命を観測する必要がある。違いが観測できない・原本不一致の比較はGoldenに計上しない。

次P0: B権限内で`0x004678A0`の3結果の`+0x74`生成元・所有権と、`0x0055ABA0`の通常callerが返却ALを使うかを、**拒否済み範囲以外**の原作ASM/既存研究から追跡。PC復帰後、最新MASTER→B HANDOFF→未同期ID→owner/READYを先に照合し、B所有T012/T028およびHANDOFFに重複排除して一度だけ取り込み（E以外MASTER変更禁止）。

実機Golden PASS **0** / strict MATCH **0** / 新規READY **0** / DONE増加 **0**。PC保存/readback **未実施**。ZIP・EXE・SAVE・DAT・Git・他lane・REA・Work・設定・スケジュールの変更なし。研究状態 **OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY**。

### 原作PEの限定区間SHA256（各区間end exclusive）

| source name | VA範囲 | SHA256 |
|---|---|---|
| caller_string_argument_then_resolver | `0x0055AC35..0x0055AC64` | `0E01C53673518F7AA6E2BE09B8A2385FFDD9B1BE30822813E68F4252F9EF180F` |
| caller_result_split_and_two_abi_routes | `0x0055AC64..0x0055AC91` | `90800584C5E08F1A397A98976F78BD3EF6D1C1646590937B42DF25ACBF7138BC` |
| resolver_global_return_path | `0x004678D2..0x00467932` | `4CC8264648FC282D36CD05C749D7D46604E2B9464AB65DC4795EC309EA3A7CCC` |
| resolver_found_return_path | `0x00467932..0x0046797B` | `AF08912F5A6490DEE37357F4BD2A629D1561E1EBFA63ED47470173BE893BE57D` |
| resolver_allocated_return_path | `0x0046797B..0x00467A3D` | `9620EB9B3D6F75304248200FEAF3CC05ADABB853C9C970E5FEDBD1768C581103` |

## 追加照合：既知3箇所のvslot+0x70 callerによる返却ALの消費

11時台の「死亡済みでもAL=1」を受けて、**callerがそのALを新規死亡として使うか**の直後の命令を調査した。今回の範囲で次を原作ASMから確認。

| virtual CALL site | 直後の原作ASM | 狭義の帰結 |
|---|---|---|
| `0x00551154`（`0x00550E70`） | `0x00551156 MOV EAX,[EBX+0x1C8]` → `0x00551167 CALL 0x00551E50` | 返却EAX/ALは直後に上書き。ここでALを新規死亡flagとして直接使う根拠なし |
| `0x00578E1E`（`0x00578B70`） | `0x00578E20 MOV [ESP+0x18],0x00627E4C` → `0x00578E28 CMP BYTE [ESI+0x8C],0` | 直後にはAL判定せず別state検査へ。関数全域での副作用まで否定は不可 |
| `0x0057E04D`（`0x0057DF90`） | `0x0057E04F MOV ECX,[ESP+0x10]` → SEH復元/レジスタPOP/`0x0057E060 RET` | この終了経路では返却ALを直接判定せず復帰 |

**つまり既死亡AL=1が必ず死亡イベントを二重実行する、という推論は支持されない。** 第三者/上位呼出の状態変化は別問題としてVERIFY。これら3 call siteは前回10時台の既存証拠で、今回の新規増分は**CALL後のAL非消費という局所的なcontrol-flow確認**だけ。

限定原作PEの追加SHA256：

- `0x00551154..0x0055116C` `F847117E7531C209AD12C9E2AA72A26B825DE6A8CB69981E2DC710973E05C9ED` (damage_caller_post_vcall)
- `0x00578E1E..0x00578E35` `904BC791E97F120FC77DA5723642FF4D5FCD64D44D0FAF3BA7035E280ECE0E34` (status_caller_post_vcall)
- `0x0057E04D..0x0057E061` `A30D8D85B1551745F67D709857413FE3334F5C9F94E7EE76079C4134C2FA98DB` (regen_caller_post_vcall)

## 保存段階の追記（Libraryの版ズレに注意）

Library B `data/`へ最初の本文・JSONは**2/2アップロード成功・2/2読み戻し成功**。その後、既知3つのvcall caller直後に関する追加照合をローカル本文・JSONへ追記したが、**Library既存2件への更新は`container_session_unavailable: No active container session was found for container_path`で2回とも失敗**（CONNECTION / TOOL TRANSPORT。安全拒否ではない）。したがって、Library側にあるものは**追加照合前の版**。最新内容はこのコンテナファイル本文・JSONにのみ保存（readback済み）され、**Library最新追記未同期**。PC正式正本への保存・読み戻しは依然0。後続実行はまず両版のSHA・既存ID・同名重複の状態を比較し、二重追加や誤ったREADY化をしない。更新不能状態を記録したまま次回へ引き継ぐ。
